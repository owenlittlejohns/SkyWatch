# Notes on git courses from Code School

#
# git_notes1.txt: git Real:

Basic commands

* `git add` (add files to the staging area)
* `git commit` (commit changes)
* `git log` (see history of commits)
* `git status` (see what has changed and which branch you are on)
* `git init` (make a new repo in the directory you are within)
* `git diff` (see what has changed since the last commit)
* `git diff --stages` (see changes in staged files)
* `git checkout -- FILENAME` (revert `FILENAME` to last commit)
* `git reset (--soft HEAD^, --hard HEAD^)` (undo commit, `--soft` puts back in staging, `--hard` undoes commit and deletes changes. One carrot per commit to be undone)

Remote repos:

* `git remote add REPO_NAME URL_TO_REPOSITORY` (add remote to local machine)
* `git remove -v` (list remotes)
* `git push` (push to remote)
* `git pull` (pull from remote)
* `git remote rm` (Delete remote)
* `git clone URL_TO_REPO.git LOCAL_NAME` (clone a remote repo locally)

Branching and tags:

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
** `git tag -a tag_name -m` "Commit message for new tag name)
** `git push --tags` (push tag name to current commit)
* `git checkout old_tag_name` (revert code to previously tagged version)

Rebasing:

* To make cleaner history for repos:
** `get fetch` (pull remote repo, but don't merge it)
** `git rebase` (hopefully sorted)
* If conflicts occur:
** Edit conflicts in file
** `git add FILENAME` (add the new changes)
** `git rebase --continue` (finish the rebase)
* Alternatively, undo the rebase:
* `git rebase --abort` (undo progress on rebase)
* Local rebasing:
** `git checkout branch_name` (switch to branch)
** `git rebase repo_branch_is_from` (add commits from original repo to new branch)
** `git checkout repo_branch_is_from` (switch to original repo)
** `git merge branch_name` (do a fast-forward merge of branch into original)
