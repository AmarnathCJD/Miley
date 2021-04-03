  
name: Fix
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Find and Replace
        uses: jacobtomlinson/gha-find-replace@master
        with:
          find: "Luna"
          replace: "Evie"
      - name: Create Pull Request
        uses: stefanzweifel/git-auto-commit-action@v4
        with:
          commit_message: 'Auto Fixes'
          commit_options: '--no-verify'
          repository: .
          commit_user_name: AmarnathCdj
          commit_user_email: AmarnathCdj@users.noreply.github.com
          commit_author: AmarnathCdj <Amarnathcdj@users.noreply.github.com>
