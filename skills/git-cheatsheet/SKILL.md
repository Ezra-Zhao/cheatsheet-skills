---
name: git-cheatsheet
description: 'Use when the user needs git commands for daily work or emergencies: config and aliases, staging and committing, branching and merging, undoing changes, stashing, rebasing, recovering lost commits with reflog, cherry-pick, and fixing mistakes safely. One tested command per task, dangerous ones marked.'
---

# Git Cheatsheet — 30 Practical Commands

Thirty real-world git commands for daily work and emergencies. Each entry tells you **what it does**, gives you **one command to copy**, and tags the scenario. Dangerous commands are marked ⚠️.

> 🌍 Read this project in your language: [中文](README.md) · [Español](README.es.md) · [Português](README.pt.md)

---

## ⚙️ Setup

### Set your identity (do this once)
Every commit you make is stamped with this name and email.
```bash
git config --global user.name "Your Name"     # your display name
git config --global user.email "you@example.com"  # your email
```
🏷️ `#setup` `#first-time`

### Make `main` the default branch
New repos (and `git init`) will use `main` instead of `master`.
```bash
git config --global init.defaultBranch main   # default branch for new repos
```
🏷️ `#setup` `#config`

### Add command aliases
Shortcuts for commands you type a hundred times a day.
```bash
git config --global alias.st status            # git st  -> git status
git config --global alias.co checkout          # git co  -> git checkout
git config --global alias.br branch            # git br  -> git branch
git config --global alias.lg "log --oneline --graph --all -20"  # git lg -> pretty log
```
🏷️ `#setup` `#productivity`

---

## 📅 Daily workflow

### See what's changed (short format)
Compact status: branch, staged (`M`), unstaged, untracked.
```bash
git status -sb   # -s = short, -b = show branch + ahead/behind
```
🏷️ `#daily` `#status`

### Stage changes interactively
Pick exactly which hunks go into the commit — no more "oops, that file too".
```bash
git add -p        # walk through each hunk: y = stage, n = skip, s = split
```
🏷️ `#daily` `#staging`

### Commit (and fix the last one)
Write a clear message; `--amend` rewrites the most recent commit instead of adding a new one.
```bash
git commit -m "Add login validation"   # normal commit
git commit --amend --no-edit           # fold new staged changes into the last commit
```
🏷️ `#daily` `#commit` · ⚠️ don't amend commits already pushed

### Read history as a graph
One line per commit, with branch lines drawn — the fastest way to understand a repo.
```bash
git log --oneline --graph --all -20   # last 20 commits, all branches
```
🏷️ `#daily` `#history`

---

## ↩️ Undo (carefully)

### Unstage a file (keep the edits)
Removes the file from the staging area; your working-tree changes stay.
```bash
git restore --staged <file>   # unstage, keep edits
```
🏷️ `#undo` `#staging`

### Discard working-tree changes in a file
Throws away unstaged edits in one file. There is no undo for this.
```bash
git restore <file>            # ⚠️ permanently discards unstaged changes in <file>
```
🏷️ `#undo` ⚠️ `#destructive`

### Reset: three modes, know the difference
`--soft` keeps everything staged, `--mixed` unstages but keeps edits, `--hard` deletes everything.
```bash
git reset --soft HEAD~1    # undo last commit, keep changes staged
git reset --mixed HEAD~1   # undo last commit, unstage, keep edits (default)
git reset --hard HEAD~1   # ⚠️ undo last commit AND delete all changes
```
🏷️ `#undo` ⚠️ `#reset`

### Revert a pushed commit (the safe undo)
Creates a *new* commit that undoes an old one — safe for shared branches.
```bash
git revert <commit-sha>   # safe undo; use this instead of reset on pushed work
```
🏷️ `#undo` `#safe`

---

## 🌿 Branches

### List branches (local and remote)
See all branches and which one you're on; `-vv` also shows upstream tracking.
```bash
git branch -a    # all local + remote branches
git branch -vv   # verbose: upstream + last commit per branch
```
🏷️ `#branch` `#inspect`

### Create and switch to a new branch
One command to branch off and start working; `switch -c` is the modern spelling.
```bash
git checkout -b feature/login   # classic
git switch -c feature/login     # modern equivalent
```
🏷️ `#branch` `#workflow`

### Merge without fast-forward
Keeps a visible merge commit so the branch's history stays grouped.
```bash
git merge --no-ff feature/login   # merge, always creating a merge commit
```
🏷️ `#branch` `#merge`

### Delete branches (local and remote)
`-d` refuses if unmerged (safe); `-D` forces. Remote delete needs a push.
```bash
git branch -d feature/login          # safe delete (fails if unmerged)
git branch -D feature/login          # ⚠️ force delete, even if unmerged
git push -d origin feature/login     # delete the branch on the remote too
```
🏷️ `#branch` `#cleanup`

---

## 🔁 Rebase

### Rebase your branch onto main
Replays your commits on top of the latest `main` — a linear, clean history.
```bash
git fetch origin             # get the latest main first
git rebase origin/main       # replay your commits on top of it
```
🏷️ `#rebase` `#workflow`

### Interactive rebase: rewrite recent history
Squash, reorder, reword, or drop your last few commits before sharing.
```bash
git rebase -i HEAD~3   # opens an editor: pick / squash / reword / drop
```
🏷️ `#rebase` `#history-cleanup`

### Finish or bail out of a rebase
Resolve conflicts, stage, then continue — or abort to return to where you started.
```bash
git rebase --continue   # after resolving conflicts and staging them
git rebase --abort      # cancel everything, back to pre-rebase state
```
🏷️ `#rebase` `#conflicts`

### The golden rule of rebase
**Never rebase commits that others have already pulled.** Rewriting shared history breaks your teammates' repos. Rebase your own private branches freely; use `revert` or `merge` for shared ones.
🏷️ `#rebase` `#rule`

---

## 📦 Stash

### Stash unfinished work
Shelve your changes (tracked files) with a message, work on something else, come back later.
```bash
git stash push -m "WIP: half-done login form"   # stash with a message
```
🏷️ `#stash` `#wip`

### List, restore, and drop stashes
`pop` restores and deletes the stash; `apply` restores but keeps it.
```bash
git stash list                 # see all stashes
git stash pop                  # restore newest stash and delete it
git stash apply stash@{1}      # restore a specific stash, keep it stored
git stash drop stash@{0}       # delete a stash you no longer need
```
🏷️ `#stash` `#wip`

---

## 🌐 Remote

### Inspect remotes
Check which URLs `origin` (and others) point to — first step when push/pull misbehaves.
```bash
git remote -v   # list remotes with fetch/push URLs
```
🏷️ `#remote` `#debug`

### Fetch and prune stale branches
Download remote changes without merging; `--prune` removes local tracking of deleted remote branches.
```bash
git fetch --prune   # update remote refs, clean up deleted branches
```
🏷️ `#remote` `#sync`

### Pull with rebase
Updates your branch by replaying your commits on top of incoming changes — no merge bubbles.
```bash
git pull --rebase   # fetch + rebase instead of fetch + merge
```
🏷️ `#remote` `#sync`

### Publish a branch and set its upstream
`-u` links your branch to the remote so future `git push` / `git pull` need no arguments.
```bash
git push -u origin feature/login              # first push: publish + set upstream
git branch --set-upstream-to=origin/main main  # re-point an existing branch's upstream
```
🏷️ `#remote` `#publish`

---

## 🆘 Rescue kit

### Recover "lost" commits with reflog
Almost nothing is truly lost: `reflog` records every move of HEAD for ~90 days.
```bash
git reflog                        # find the SHA of the "lost" commit
git checkout <sha>                # inspect it safely (detached HEAD)
git branch rescue <sha>           # or: put it on a new branch to keep it
```
🏷️ `#rescue` `#recovery`

### Cherry-pick a commit onto your branch
Copy one specific commit (by SHA) from anywhere onto your current branch.
```bash
git cherry-pick <commit-sha>   # apply that commit here
```
🏷️ `#rescue` `#porting`

### Bisect: find the commit that broke things
Binary-searches history between a known-good and known-bad commit.
```bash
git bisect start
git bisect bad                    # current HEAD is broken
git bisect good v1.2.0            # v1.2.0 was fine
# git checks out commits; test each, then: git bisect good|bad
git bisect reset                  # done: back to where you started
```
🏷️ `#rescue` `#debugging`

---

## 🚀 Advanced

### Worktree: two branches, one repo, two folders
Check out a second branch in a separate directory — no more stashing to review a hotfix.
```bash
git worktree add ../hotfix hotfix-branch   # new folder ../hotfix on hotfix-branch
git worktree list                          # see all worktrees
git worktree remove ../hotfix              # clean up when done
```
🏷️ `#advanced` `#multitask`

### Submodules: repos inside repos
Clone and update nested repositories (common in large projects).
```bash
git clone --recurse-submodules <url>          # clone with submodules included
git submodule update --init --recursive       # init/update submodules in an existing clone
```
🏷️ `#advanced` `#submodules`

### Shallow clone: download less
Clone only recent history — much faster for huge repos you just need to build.
```bash
git clone --depth 1 <url>   # latest snapshot only, no full history
```
🏷️ `#advanced` `#performance`

---

## Reference

Official documentation: https://git-scm.com/doc

## Contributing

Found a wrong command, a missing scenario, or a bad translation? Pull requests are welcome — keep entries to the format above (heading / one line / code block / tags) and verify every command is real before submitting.

## License

MIT © 2026 Guangyi Zhao. See [LICENSE](LICENSE).
