import re, os
pattern = re.compile(r'(close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved)\s+#(\d+)')

from github import Github

print(os.environ)

token = str(os.environ['TOKEN'])
# print("=====>",token2)
# token = os.environ['token']
base_branch = str(os.environ['BASE_BRANCH'])

def close_issue_from_commit_msg(commit):
    commit_msg = commit.commit.message.lower()
    matches = re.findall(pattern, commit_msg)
    if len(matches)>0:
        for issue in matches:
            issue = repo.get_issue(number = int(issue[1]))
            if (issue.state == 'open'):
                issue.edit(state='closed')
                print(f"Issue {issue.number} is closed")

g = Github(token)

repo = g.get_repo(str(os.environ['REPO']))
branch = repo.get_branch(branch=base_branch)
branch_head_commit = branch.commit
close_issue_from_commit_msg(branch_head_commit)


pulls = repo.get_pulls(state='close', sort='created', direction='descending', base=base_branch)
for pr in pulls:
    print("Pull Request no: "+str(pr.number) + " is processing...")
    if pr.is_merged():
        commits = pr.get_commits()
        for commit in commits:
            close_issue_from_commit_msg(commit)


    break #breaked so that loops over only last pull request merge
