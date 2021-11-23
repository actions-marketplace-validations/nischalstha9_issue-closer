from github import Github, Commit
import re
import os

# regex for getting issue numbers from commit message
pattern = re.compile(
    r'(close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved)\s+#(\d+)')

# print(os.environ)

token = str(os.environ['INPUT_TOKEN'])  # Github Token from YAML File
# Repository base branch input from YAML File
base_branch = str(os.environ['INPUT_BASE_BRANCH'])


# initializing new Github Object with Github Access Token
g = Github(token)

# get repository on basis of repository input in YAML File
repo = g.get_repo(str(os.environ['INPUT_REPO']))


def close_issue_from_commit_msg(commit: Commit):
    """
    Closes Issues Reading Issue Numbers from Commit Message.
    For example: commit message: 'close #18 resolve #19' closes issues number 18 and 19.
    """
    commit_msg = commit.commit.message.lower()
    matches = re.findall(pattern, commit_msg)
    closed_issues = []
    if len(matches) > 0:
        for issue in matches:
            issue = repo.get_issue(number=int(issue[1]))
            if (issue.state == 'open'):
                issue.edit(state='closed')
                closed_issues.append((issue.number, issue.user.login))
                print(f"Issue {issue.number} is closed")
    return closed_issues  # returns closed issue numbers and issuer name


def get_comment_string_from_closed_issues(closed_issues):
    """
    Return Comment string, including issue number and mentioning issue creator's login.
    Takes List of Tuples generated from close_issue_from_commit_msg function.
        Ex: [(issue_number->int, issue_user->String), ......]    
    """
    try:
        issuers_string = ""
        for i in closed_issues:
            issuers_string += "- Issue #" + \
                str(i[0]) + " by @" + str(i[1]+"\n")
        return issuers_string
    except:
        return ""


if __name__ == "__main__":
    if os.environ.get('GITHUB_EVENT_NAME') == "push":
        current_branch_name = str(
            os.environ['GITHUB_REF'].split("refs/heads/")[-1])
        branch = repo.get_branch(branch=current_branch_name)
        branch_head_commit = branch.commit
        closed_issues = close_issue_from_commit_msg(branch_head_commit)
        if len(closed_issues) > 0:
            issue_cmnt_string = get_comment_string_from_closed_issues(
                closed_issues=closed_issues)
            branch_head_commit.create_comment(
                body="Auto issue closer closed following issues:\n"+issue_cmnt_string)
    else:
        pulls = repo.get_pulls(state='close', sort='created',
                               direction='descending', base=base_branch)
        for pr in pulls:
            print("Pull Request no: "+str(pr.number) + " is processing...")
            if pr.is_merged():
                commits = pr.get_commits()
                for commit in commits:
                    closed_issues = close_issue_from_commit_msg(commit)
                    # print(closed_issues)
                    if len(closed_issues) > 0:
                        issuers_string = get_comment_string_from_closed_issues(
                            closed_issues=closed_issues)
                        pr.create_issue_comment(
                            body="Pull request merged and issue-closer closed following issues:\n"+issuers_string)
            print("Pull Request no: "+str(pr.number) + " finished processing.👍️")
            break  # breaked so that loops over only last pull request merge
