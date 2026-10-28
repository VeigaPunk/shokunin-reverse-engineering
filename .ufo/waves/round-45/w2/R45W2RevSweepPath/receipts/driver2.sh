#!/usr/bin/env bash
set -u
S=/fast/scratch/hyaku/kaidoku-r45/R45W2RevSweepPath
H=/home/vgpnk/Projects/shokunin/scripts/hyaku
say(){ printf '\n### %s\n' "$*"; }
run(){ printf '$ %s\n' "$*"; "$@"; printf 'rc=%s\n' "$?"; }

say "fx3-control: a real git pre-push hook blocks git push"
D=$S/fx3-git; rm -rf "$D" "$S/origin3.git"; git init -q "$D"; cd "$D" || exit 9
[ "$(git rev-parse --show-toplevel)" = "$D" ] && echo toplevel_ok
git init -q --bare "$S/origin3.git"; git remote add origin "$S/origin3.git"
echo x > x.txt; git add x.txt; git -c user.name=u -c user.email=u@x commit -qm one
printf '#!/bin/sh\necho "pre-push ran" >> %s/hooks3push.log\nexit 1\n' "$S" > .git/hooks/pre-push; chmod +x .git/hooks/pre-push
run git push -q origin HEAD:refs/heads/ctl
echo "hooks3push.log: $([ -f "$S/hooks3push.log" ] && wc -l < "$S/hooks3push.log" || echo none)"

say "fx4: the REAL fleet-commit.sh, lane-side blocking pre-commit hook present"
D=$S/fx4-fleet; rm -rf "$D" "$S/origin4.git" "$S/state4"; git init -q "$D"; cd "$D" || exit 9
[ "$(git rev-parse --show-toplevel)" = "$D" ] && echo toplevel_ok
echo base > base.txt; git add base.txt; git -c user.name=u -c user.email=u@x commit -qm base
jj git init --colocate >/dev/null 2>&1; echo "jj_rc=$? .jj=$([ -d .jj ] && echo yes||echo no)"
git init -q --bare "$S/origin4.git"; git remote add origin "$S/origin4.git"
jj --ignore-working-copy bookmark create master -r '@-' >/dev/null 2>&1; echo "bm_master=$?"
jj --ignore-working-copy bookmark create main -r '@-' >/dev/null 2>&1; echo "bm_main=$?"
printf '#!/bin/sh\necho "pre-commit ran" >> %s/hooks4.log\nexit 1\n' "$S" > .git/hooks/pre-commit; chmod +x .git/hooks/pre-commit
echo report > fleet-report.md
run env SHOKUNIN_ROOT="$D" HYAKU_STATE="$S/state4" FLEET_REMOTE=origin FLEET_BRANCH=master FLEET_MIRROR=main FLEET_PUSH_BACKOFF=0 \
  bash "$H/fleet-commit.sh" --as kaidoku -m "round-99: kaidoku report (hyaku sweep)" -- fleet-report.md
echo "hooks4.log: $([ -f "$S/hooks4.log" ] && wc -l < "$S/hooks4.log" || echo none)"
echo "fleet tip:"; git log --oneline -2 --format='%h %s'; echo "committed paths:"; git show --name-only --format= HEAD

say "fx5: the REAL jj-lane.sh commit, hook present, bulk DIRECTORY pathspec"
D=$S/fx5-lane; rm -rf "$D" "$S/origin5.git"; git init -q "$D"; cd "$D" || exit 9
[ "$(git rev-parse --show-toplevel)" = "$D" ] && echo toplevel_ok
git init -q --bare "$S/origin5.git"; git remote add origin "$S/origin5.git"
mkdir -p .ufo/waves/round-44 controls tools/round-44/control-fixtures
echo a > .ufo/waves/round-44/a.json; echo b > .ufo/waves/round-44/b.json
echo c > tools/round-44/control-fixtures/keep.json; echo d > tools/round-44/control-fixtures/touch.json; echo e > unrelated.txt
git add -A; git -c user.name=u -c user.email=u@x commit -qm base; git branch -M main; git push -q -u origin main
echo "branch=$(git rev-parse --abbrev-ref HEAD)"
run bash "$H/jj-lane.sh" init "$D" fxlane
printf '#!/bin/sh\necho "pre-commit ran" >> %s/hooks5.log\nexit 1\n' "$S" > .git/hooks/pre-commit; chmod +x .git/hooks/pre-commit
echo changed >> tools/round-44/control-fixtures/touch.json; echo more >> .ufo/waves/round-44/a.json; echo stray > unrelated.txt
say "fx5a: a bare '.' pathspec"
run bash "$H/jj-lane.sh" commit "$D" --as fxlane -m "bulk" -- .
say "fx5b: directory pathspecs covering a frozen tools dir (the M45-1 shape)"
run bash "$H/jj-lane.sh" commit "$D" --as fxlane -m "bulk dirs" -- .ufo/waves/round-44 tools/round-44
echo "hooks5.log: $([ -f "$S/hooks5.log" ] && wc -l < "$S/hooks5.log" || echo none)"
echo "lanetip paths:"; git show --name-status --format= refs/heads/main | head -10
