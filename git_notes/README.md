# Notes on git courses from Code School #

## git_notes1.txt: git Real:##

#### Basic commands ####

* `git add` (add files to the staging area)
* `git commit` (commit changes)
* `git log` (see history of commits)
* `git status` (see what has changed and which branch you are on)
* `git init` (make a new repo in the directory you are within)
* `git diff` (see what has changed since the last commit)
* `git diff --stages` (see changes in staged files)
* `git checkout -- FILENAME` (revert `FILENAME` to last commit)
* `git reset --soft HEAD^`, or ` git reset --hard HEAD^` (undo commit, `--soft` puts back in staging, `--hard` undoes commit and deletes changes. One carrot per commit to be undone)

#### Remote repos: ####

* `git remote add REPO_NAME URL_TO_REPOSITORY` (add remote to local machine)
* `git remove -v` (list remotes)
* `git push` (push to remote)
* `git pull` (pull from remote)
* `git remote rm` (Delete remote)
* `git clone URL_TO_REPO.git LOCAL_NAME` (clone a remote repo locally)

#### Branching and tags: ####

* `git branch BRANCH` (create a new branch, or `git branch -d BRANCH` to delete it)
* `git merge` (merge two branches)
* `git checkout -b BRANCH` (to create and checkout a new branch)
* Merge commits.
* Merge conflicts.
* `git branch -r` (show remote branches)
* `git fetch` (fetch all new remote branches)
* `git remote show origin` (see where remote branches came from)
* `git push origin :branch_name` (delete the remote version of branch_name)
* `git remote prune origin`
* `git tag` (list tags)
 * `git tag -a tag_name -m` "Commit message for new tag name)
 * `git push --tags` (push tag name to current commit)
* `git checkout old_tag_name` (revert code to previously tagged version)

#### Rebasing: ####

* To make cleaner history for repos:
 * `get fetch` (pull remote repo, but don't merge it)
 * `git rebase` (hopefully sorted)
* If conflicts occur:
 * Edit conflicts in file
 * `git add FILENAME` (add the new changes)
 * `git rebase --continue` (finish the rebase)
* Alternatively, undo the rebase:
* `git rebase --abort` (undo progress on rebase)
* Local rebasing:
 * `git checkout branch_name` (switch to branch)
 * `git rebase repo_branch_is_from` (add commits from original repo to new branch)
 * `git checkout repo_branch_is_from` (switch to original repo)
 * `git merge branch_name` (do a fast-forward merge of branch into original)

#### History: ####

* `git log` (show commit history)
* `git log --oneline -p` (show commit history with patches explicitly)
* `git log --pretty=oneline` (each commit in log is only one line)
* `git log --pretty=format: "%h %ad- %s [%an]"`, where:
 * `%h` is SHA hash
 * `%ad` is author data
 * `%an` is author name
 * `%s` is subject
* `git log --oneline --stat` (number of insertions and deletions per commit)
* `git log --oneline --graph` (gives a tree, SSH hash tags and commit messages)
* `git log --since=one.month.ago --until=one.minute.ago` (log in time range)
* `git log --since=2000-01-01 --until=2012-01-01` (explicit time range - same commands can be used in `git diff`)
* `git diff HEAD HEAD^` (compare between different commits, remember `HEAD^` and `HEAD~5` nomenclature)
* `git diff SHAhash1..SHAhash2` (difference between two named commits)
* `git diff branch1 branch2` (difference between two branches)
* `git blame FILENAME --date short` (show history of commits for file)

#### Logs: ####

* Put files (or paths with wildcards) in `.gitignore`.
* `git rm --cached NAME_OF_FILE` (to stop tracking file - then add to `.gitignore` and commit the change)


#### Configuration: ####

* `git config --global color.ui true` (make user interface coloured)
* `git config --global core.editor emacs` (make emacs the text editor for merge conflicts, etc)
* `git config --global alias.st "status"` (create an alias of `git st` for `git status`)

## git_notes2.txt - notes on git 2 course: ##

* `git rebase -i BRANCH` (interactive rebase, including `pick`, `edit` and `squash`)
*`git stash save "save message"` (save a stash without committing, so you can checkout another branch)
* `git stash apply stash@{0}` (apply stash of that name to current branch)
* `git stash drop stash@{0}` (drop stash of that name from the stash stack)
* `git stash pop stash@{0}` (pop that stash into current working branch)
* `git stash save --keep-index` (only stash unstaged files - not added ones)
* `git stash save --include-untracked` (include untracked files)
* `git stash save --keep-index --include-untracked` (do both of above)
* You can run the commit you want after the `git stash save --keep-index`
* With a stash conflict: `git reset --hard HEAD` and then reapply stash
* `git stash list --stat` (give summary of the changes in the stash)
* `git stash show stash@{0}` (show details on that specific stash)
* `git stash branch BRANCH_NAME stash@{0}` (create a new branch, apply stash, drop stash)
* `git stash clear` (empty the stash stack).

#### Purging history: ####

* `git clone repo_name copy_name` (back up the repo first)
* `git filter-branch --tree-filter 'shell command'` (Go through every commit and apply the shell command - this is slower. `rm -f` so it doesn't fail)
* `git filter-branch --index-filter 'git command including --ignore-unmatch'` (Only looks at staged files, so quicker)
* Second `filter-branch` requires `-f`
* `git filter-branch -f --prune-empty -- --all` (delete all empty commits)

#### Cherry-picking: ####

* `git checkout BRANCH_YOU_WANT_CODE_IN` (step 1 get on branch)
* `git cherry-pick SHAHASH_FOR_COMMIT_YOU_WANT` (step 2 grab commit from other branch)
* `git cherry-pick --edit SHAHASH` (edit commit message)
* `git cherry-pick --no-commit SHAHASH1 SHAHASH2` (stage but do not commit the commits, so you can combine into a single one yourself)
* `git cherry-pick -x SHAHASH` (keep reference to where commit is from)
* `git cherry-pick --signoff SHAHASH` (keep reference of who cherry-picked the commit)

#### Submodules: ####

* To make a submodule:
 * `git submodule add git@example.com:submodule_name.git` (add submodule directory if making it)
 * `git add --all` (stage stuff in submodule you want to add)
 * `git commit -m "Add submodule stuff"`
 * `git push` (now submodule is remotely available)
 * `cd ..` (go to parent repo)
 * `git add submodule_name`
 * `git commit -m "Update parent commit too)
 * `git push`
* Obtaining a submodule:
 * `git clone git@example.com:project.git` (clone whole project)
 * `git submodule init` (make submodule directories)
 * `git submodule update` (pull down submodule contents)
 * `git checkout BRANCH` (by default submodules start you on no branch)
* If you forget to checkout a branch for the submodule, and commit, it becomes and orphan. To fix:
 * `git checkout BRANCH_YOU_WANT_COMMIT_ON`
 * `git merge SHAHASH_OF_ORPHAN_COMMIT`
* `git push --recurse-submodules=check` (check no submodules have been forgotten when pushing parent)
* `git push --recurse-submodules=on-demand` (force submodules to be pushed if forgotten)

#### Reflog: ####

* Reflog contains everything, including deletes and deleted commits.
* `git reflog` or more detailed `git log --walk-reflogs`
* For deleted commit, get SHA hash, then:
 * `git reset --hard SHAHASH`
* For deleted branch:
* `git branch NEW_BRANCH_NAME SHAHASH_DELETED_BRANCH_LAST_COMMIT`

## githubnotes.txt: ##

* Configuration, forking, cloning, pull requests.
* Single repository workflows, collaborative practices.
* Release tags, release branches,