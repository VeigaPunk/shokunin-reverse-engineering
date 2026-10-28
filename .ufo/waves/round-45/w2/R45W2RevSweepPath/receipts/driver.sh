#!/usr/bin/env bash
set -u
S=/fast/scratch/hyaku/kaidoku-r45/R45W2RevSweepPath
H=/home/vgpnk/Projects/shokunin/scripts/hyaku
say(){ printf '\n### %s\n' "$*"; }
run(){ printf '$ %s\n' "$*"; "$@"; printf 'rc=%s\n' "$?"; }

say "fx1 control: a lane-side .git/hooks/pre-commit DOES run under git commit"
D=$S/fx1-git; rm -rf "$D"; git init -q "$D"; cd "$D" || exit 9
tl=$(git rev-parse --show-toplevel); [ "$tl" = "$D" ] && echo "toplevel_ok=$tl"
mkdir -p .git/hooks
printf '#!/bin/sh\necho "pre-commit ran $(date -u +%%H:%%M:%%SZ)" >> %s/hooks1.log\nexit 1\n' "$S" > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
echo a > a.txt; git add a.txt
run git -c user.name=u -c user.email=u@x commit -m one
echo "hooks1.log exists: $([ -f "$S/hooks1.log" ] && wc -l < "$S/hooks1.log" || echo none)"
echo "commits: $(git rev-list --count HEAD 2>/dev/null || echo 0)"

say "fx2 jj: the same hook, the exact fleet-commit.sh jj sequence"
D=$S/fx2-jj; rm -rf "$D"; git init -q "$D"; cd "$D" || exit 9
tl=$(git rev-parse --show-toplevel); [ "$tl" = "$D" ] && echo "toplevel_ok=$tl"
git -c user.name=u -c user.email=u@x commit -qm initial --allow-empty
jj git init --colocate >/dev/null 2>&1; echo "jj_init_rc=$? .jj=$([ -d .jj ] && echo yes)"
printf '#!/bin/sh\necho "pre-commit ran" >> %s/hooks2.log\nexit 1\n' "$S" > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
echo b > b.txt
run jj --config 'snapshot.auto-track="none()"' --config user.name=k --config user.email=k@y file track -- 'root:"b.txt"'
run jj --config 'snapshot.auto-track="none()"' --config user.name=k --config user.email=k@y diff --summary -- 'root:"b.txt"'
run jj --config 'snapshot.auto-track="none()"' --config user.name=k --config user.email=k@y metaedit --update-author
run jj --config 'snapshot.auto-track="none()"' --config user.name=k --config user.email=k@y commit -m fleet-seq -- 'root:"b.txt"'
echo "hooks2.log exists: $([ -f "$S/hooks2.log" ] && wc -l < "$S/hooks2.log" || echo none)"
echo "jj log:"; jj --ignore-working-copy log --no-graph -r '::@-' -T 'commit_id.short() ++ " " ++ description.first_line() ++ "\n"' 2>&1 | head -4

say "fx2b: one directory pathspec commits every nested file (the M45-1 shape)"
mkdir -p dir/sub; echo 1 > dir/a.json; echo 2 > dir/sub/b.json
run jj --config 'snapshot.auto-track="none()"' --config user.name=k --config user.email=k@y file track -- 'root:"dir"'
run jj --config 'snapshot.auto-track="none()"' --config user.name=k --config user.email=k@y metaedit --update-author
run jj --config 'snapshot.auto-track="none()"' --config user.name=k --config user.email=k@y commit -m dirsweep -- 'root:"dir"'
echo "committed paths:"; git show --name-only --format= HEAD 2>/dev/null

say "fx3: pre-push hook — git push runs it (control); jj git push must not"
O=$S/origin1.git; rm -rf "$O"; git init -q --bare "$O"
cd "$S/fx1-git" || exit 9
printf '#!/bin/sh\necho "pre-push ran" >> %s/hooks1push.log\nexit 1\n' "$S" > .git/hooks/pre-push; chmod +x .git/hooks/pre-push
git remote add origin "$O" 2>/dev/null || git remote set-url origin "$O"
run git -c user.name=u -c user.email=u@x commit -qm two --allow-empty
run git push -q origin HEAD:refs/heads/ctl
echo "hooks1push.log exists: $([ -f "$S/hooks1push.log" ] && wc -l < "$S/hooks1push.log" || echo none)"

O2=$S/origin2.git; rm -rf "$O2"; git init -q --bare "$O2"
cd "$S/fx2-jj" || exit 9
jj --ignore-working-copy bookmark create master -r '@-' >/dev/null 2>&1; echo "bm_master_rc=$?"
jj --ignore-working-copy bookmark create main -r '@-' >/dev/null 2>&1; echo "bm_main_rc=$?"
printf '#!/bin/sh\necho "pre-push ran" >> %s/hooks2push.log\nexit 1\n' "$S" > .git/hooks/pre-push; chmod +x .git/hooks/pre-push
git remote add origin "$O2" 2>/dev/null || git remote set-url origin "$O2"
run jj --ignore-working-copy git push --remote origin --bookmark master
echo "hooks2push.log exists: $([ -f "$S/hooks2push.log" ] && wc -l < "$S/hooks2push.log" || echo none)"
