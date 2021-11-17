# Github Issue Auto Closer

sample action file: <br/>

```
name: Issue Closer

on:
  push:
    branches: 
      - "master" # i want issues to be closed only when pushed directly to these branches
  pull_request:
    branches: 
      - "*" # i want issues to be closed when pr are merged to these branches

jobs:
  issue-closer:
    runs-on: ubuntu-latest
    steps:
    - uses: nischalstha9/issue-closer@master
      with:
        token: ${{ secrets.GITHUB_TOKEN }} #github secret token
        repo: 'nischalstha9/learining_github_actions' #repo name
        base_branch: 'master' #repo base_branch
```