gp() { git add -A; git commit -m "$1"; git push; }  # Git add, commit, and push to repo
alias gp=gp

# resets a git cache, then add. Usefule for resetting .gitignore
git_reset_cache() { git rm -r --cached .; git add -A;}
alias git_reset_cache=git_reset_cache

# resets everything to the current git branch. Note: very destructive
alias git_kill='git reset --hard && git clean -fd'
alias git_kill=git_kill