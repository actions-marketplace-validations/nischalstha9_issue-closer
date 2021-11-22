import re, os

#regex for getting issue numbers from commit message
pattern = re.compile(r'(close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved)\s+#(\d+)')

from github import Github, Commit
# print(os.environ)

token = "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" #Github Token from YAML File
base_branch = "master" #Repository base branch input from YAML File


def close_issue_from_commit_msg(commit:Commit)->None:
    """
    Closes Issues Reading Issue Numbers from Commit Message.
    For example: commit message: 'close #18 resolve #19' closes issues number 18 and 19.
    """
    commit_msg = commit.commit.message.lower()
    matches = re.findall(pattern, commit_msg)
    if len(matches)>0:
        for issue in matches:
            issue = repo.get_issue(number = int(issue[1]))
            if (issue.state == 'open'):
                issue.edit(state='closed')
                print(f"Issue {issue.number} is closed")

#initializing new Github Object with Github Access Token
g = Github(token)

#get repository on basis of repository input in YAML File
repo = g.get_repo("nischalstha9/learining_github_actions")
issue = repo.get_issue(number=13)
pr = repo.get_pull(16)
# cmnt = issue.create_comment("This is tagged comment from issue closer!")
cmnt = "This is tagged comment from issue closer! \n@"+str(issue.user.login) + "\n #" + str(16)
print(cmnt)
cmnt = pr.create_issue_comment(body=cmnt)
