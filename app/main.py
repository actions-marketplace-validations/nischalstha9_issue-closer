import re, os

#regex for getting issue numbers from commit message
pattern = re.compile(r'(close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved)\s+#(\d+)')

from github import Github, Commit
# print(os.environ)

token = str(os.environ['INPUT_TOKEN']) #Github Token from YAML File
base_branch = str(os.environ['INPUT_BASE_BRANCH']) #Repository base branch input from YAML File


#initializing new Github Object with Github Access Token
g = Github(token)

#get repository on basis of repository input in YAML File
repo = g.get_repo(str(os.environ['INPUT_REPO']))

def close_issue_from_commit_msg(commit:Commit)->str:
    """
    Closes Issues Reading Issue Numbers from Commit Message.
    For example: commit message: 'close #18 resolve #19' closes issues number 18 and 19.
    """
    commit_msg = commit.commit.message.lower()
    matches = re.findall(pattern, commit_msg)
    if len(matches)>0:
        closed_issues = []
        for issue in matches:
            issue = repo.get_issue(number = int(issue[1]))
            if (issue.state == 'open'):
                issue.edit(state='closed')
                closed_issues.append((issue.number, issue.user.login))
                print(f"Issue {issue.number} is closed")
        return closed_issues # returns closed issue numbers and issuer name


if os.environ.get('GITHUB_EVENT_NAME')=="push":
    branch = repo.get_branch(branch=base_branch)
    branch_head_commit = branch.commit
    close_issue_from_commit_msg(branch_head_commit)
else:
    pulls = repo.get_pulls(state='close', sort='created', direction='descending', base=base_branch)
    for pr in pulls:
        print("Pull Request no: "+str(pr.number) + " is processing...")
        if pr.is_merged():
            commits = pr.get_commits()
            for commit in commits:
                closed_issues = close_issue_from_commit_msg(commit)
                print(closed_issues)
                try:
                    issuers_string = ""
                    for i in closed_issues:
                        issuers_string += "- "+ str(i[0]) + "by @" + str(i[1]+"\n")
                    pr.create_issue_comment(body="Pull request merged and issue-closer closed following issues:\n"+issuers_string)
                except:
                    pass
        print("Pull Request no: "+str(pr.number) + " finished processing.👍️")
        break #breaked so that loops over only last pull request merge
