#!/usr/bin/env bash
# R45W2RevSweepPath reproduction harness: every attack as one recorded call.
set -u
S=/fast/scratch/hyaku/kaidoku-r45/R45W2RevSweepPath
H=/home/vgpnk/Projects/shokunin/scripts/hyaku
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
PF=$LANE/tools/round-45/frozen-path-preflight.py
mkdir -p "$S/out"
: > "$S/receipts.tsv"
rec(){ # label -- cmd...
  local label=$1; shift; local out rc ts sha
  out=$("$@" 2>&1); rc=$?
  ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  printf '%s\n' "$out" > "$S/out/$label.out"
  sha=$(printf '%s' "$out" | sha256sum | cut -d' ' -f1)
  printf '%s\t%s\t%s\t%s\t%s\n' "$label" "$ts" "$rc" "$sha" "$*" >> "$S/receipts.tsv"
  printf '%-38s rc=%-3s sha=%s\n' "$label" "$rc" "${sha:0:16}"
}

rec r01-no-git-commit-in-fleet  bash -c "grep -rn -E '(^|[^a-z])git (commit|add)' $H/*.sh $H/*.py /home/vgpnk/Projects/shokunin/scripts/shokunin-watchdog.sh | grep -v selftest || echo NONE-OUTSIDE-SELFTEST"
rec r02-no-no-verify             bash -c "grep -rn -- '--no-verify' $H /home/vgpnk/Projects/shokunin/scripts/shokunin-watchdog.sh || echo NONE"
rec r03-no-gate-wiring            bash -c "grep -rn 'frozen-path-preflight' $H /home/vgpnk/Projects/shokunin/scripts/shokunin-watchdog.sh || echo NONE"
rec r04-commit-callers           bash -c "grep -rn -E 'fleet-commit\\.sh|jj-lane\\.sh commit' $H/*.sh | grep -v selftest"
rec r05-jj-version               jj --version
rec r06-lane-side-probes         bash -c "sed -n '153,178p' $H/inline.sh"

# fx1: git control — a lane-side pre-commit hook is live under git commit
D=$S/fx1-git; rm -rf "$D"; git init -q "$D"
cd "$D" || exit 9
[ "$(git rev-parse --show-toplevel)" = "$D" ] || exit 9
mkdir -p .git/hooks
printf '#!/bin/sh\necho ran >> %s/h1.log\nexit 1\n' "$S" > .git/hooks/pre-commit; chmod +x .git/hooks/pre-commit
echo a > a.txt; git add a.txt
rec r07-fx1-git-pre-commit-blocks git -c user.name=u -c user.email=u@x commit -m one
rec r08-fx1-hook-log             bash -c "wc -l < $S/h1.log 2>/dev/null || echo none"
rec r09-fx1-commit-count         bash -c "git -C $D rev-list --count HEAD 2>/dev/null || echo 0"

# fx2: the exact fleet-commit.sh jj sequence with the same blocking hook
D=$S/fx2-jj; rm -rf "$D"; git init -q "$D"; cd "$D" || exit 9
[ "$(git rev-parse --show-toplevel)" = "$D" ] || exit 9
git -c user.name=u -c user.email=u@x commit -qm initial --allow-empty
jj git init --colocate >/dev/null 2>&1
printf '#!/bin/sh\necho ran >> %s/h2.log\nexit 1\n' "$S" > .git/hooks/pre-commit; chmod +x .git/hooks/pre-commit
echo b > b.txt
rec r10-fx2-jj-track  jj --config 'snapshot.auto-track="none()"' --config user.name=k --config user.email=k@y file track -- 'root:"b.txt"'
rec r11-fx2-jj-commit jj --config 'snapshot.auto-track="none()"' --config user.name=k --config user.email=k@y commit -m fleet-seq -- 'root:"b.txt"'
rec r12-fx2-hook-log  bash -c "wc -l < $S/h2.log 2>/dev/null || echo none"
mkdir -p dir/sub; echo 1 > dir/a.json; echo 2 > dir/sub/b.json
jj --config 'snapshot.auto-track="none()"' --config user.name=k --config user.email=k@y file track -- 'root:"dir"' >/dev/null 2>&1
rec r13-fx2b-dirpathspec-commit jj --config 'snapshot.auto-track="none()"' --config user.name=k --config user.email=k@y commit -m dirsweep -- 'root:"dir"'
rec r14-fx2b-committed-paths    bash -c "git -C $D show --name-only --format= HEAD"
rec r15-fx2b-hook-still-silent  bash -c "wc -l < $S/h2.log 2>/dev/null || echo none"

# fx3: pre-push — git push runs the hook (control); jj git push does not
D=$S/fx3-git; rm -rf "$D" "$S/o3.git"; git init -q "$D"; cd "$D" || exit 9
[ "$(git rev-parse --show-toplevel)" = "$D" ] || exit 9
git init -q --bare "$S/o3.git"; git remote add origin "$S/o3.git"
echo x > x.txt; git add x.txt; git -c user.name=u -c user.email=u@x commit -qm one
printf '#!/bin/sh\necho ran >> %s/h3.log\nexit 1\n' "$S" > .git/hooks/pre-push; chmod +x .git/hooks/pre-push
rec r16-fx3-git-push-blocked bash -c "git -C $D push -q origin HEAD:refs/heads/ctl"
rec r17-fx3-hook-log         bash -c "wc -l < $S/h3.log 2>/dev/null || echo none"
cd "$S/fx2-jj" || exit 9
jj --ignore-working-copy bookmark create master -r '@-' >/dev/null 2>&1
printf '#!/bin/sh\necho ran >> %s/h2push.log\nexit 1\n' "$S" > .git/hooks/pre-push; chmod +x .git/hooks/pre-push
git init -q --bare "$S/o2.git"; git remote add origin "$S/o2.git" 2>/dev/null || git remote set-url origin "$S/o2.git"
rec r18-fx3-jj-push-unblocked jj --ignore-working-copy git push --remote origin --bookmark master
rec r19-fx3-jj-push-hook-log  bash -c "wc -l < $S/h2push.log 2>/dev/null || echo none"

# fx4: the REAL fleet-commit.sh with a blocking lane-side pre-commit hook
D=$S/fx4-fleet; rm -rf "$D" "$S/o4.git" "$S/state4"; git init -q "$D"; cd "$D" || exit 9
[ "$(git rev-parse --show-toplevel)" = "$D" ] || exit 9
echo base > base.txt; git add base.txt; git -c user.name=u -c user.email=u@x commit -qm base
jj git init --colocate >/dev/null 2>&1
git init -q --bare "$S/o4.git"; git remote add origin "$S/o4.git"
jj --ignore-working-copy bookmark create master -r '@-' >/dev/null 2>&1
jj --ignore-working-copy bookmark create main -r '@-' >/dev/null 2>&1
printf '#!/bin/sh\necho ran >> %s/h4.log\nexit 1\n' "$S" > .git/hooks/pre-commit; chmod +x .git/hooks/pre-commit
echo report > fleet-report.md
rec r20-fx4-real-fleet-commit env SHOKUNIN_ROOT="$D" HYAKU_STATE="$S/state4" FLEET_REMOTE=origin FLEET_BRANCH=master FLEET_MIRROR=main FLEET_PUSH_BACKOFF=0 bash "$H/fleet-commit.sh" --as kaidoku -m "round-99: kaidoku report (hyaku sweep)" -- fleet-report.md
rec r21-fx4-hook-log          bash -c "wc -l < $S/h4.log 2>/dev/null || echo none"
rec r22-fx4-committed-paths   bash -c "git -C $D show --name-only --format= HEAD"

# fx5: the REAL jj-lane.sh — '.' rejected, directory pathspecs land the M45-1 shape
D=$S/fx5-lane; rm -rf "$D" "$S/o5.git"; git init -q "$D"; cd "$D" || exit 9
[ "$(git rev-parse --show-toplevel)" = "$D" ] || exit 9
git init -q --bare "$S/o5.git"; git remote add origin "$S/o5.git"
mkdir -p .ufo/waves/round-44 tools/round-44/control-fixtures
echo a > .ufo/waves/round-44/a.json; echo c > tools/round-44/control-fixtures/keep.json
echo d > tools/round-44/control-fixtures/touch.json; echo e > unrelated.txt
git add -A; git -c user.name=u -c user.email=u@x commit -qm base; git branch -M main; git push -q -u origin main
bash "$H/jj-lane.sh" init "$D" fxlane >/dev/null 2>&1
printf '#!/bin/sh\necho ran >> %s/h5.log\nexit 1\n' "$S" > .git/hooks/pre-commit; chmod +x .git/hooks/pre-commit
echo changed >> tools/round-44/control-fixtures/touch.json; echo more >> .ufo/waves/round-44/a.json; echo stray > unrelated.txt
rec r23-fx5-dot-pathspec-refused bash "$H/jj-lane.sh" commit "$D" --as fxlane -m bulk -- .
rec r24-fx5-dirpathspecs-landed bash "$H/jj-lane.sh" commit "$D" --as fxlane -m "bulk dirs" -- .ufo/waves/round-44 tools/round-44
rec r25-fx5-lane-tip-paths      bash -c "git -C $D show --name-status --format= refs/heads/main"
rec r26-fx5-hook-log            bash -c "wc -l < $S/h5.log 2>/dev/null || echo none"

# fx6: the dirty arm's scope boundary, with --json-out receipts
D=$S/fx6-scope; rm -rf "$D"; git init -q "$D"; cd "$D" || exit 9
[ "$(git rev-parse --show-toplevel)" = "$D" ] || exit 9
mkdir -p tools/round-45 other
echo one > tools/round-45/frozen.txt; echo base > other/base.txt
git add -A; git -c user.name=u -c user.email=u@x commit -qm base; FZ=$(git rev-parse HEAD)
echo two > other/later.txt; git add -A; git -c user.name=u -c user.email=u@x commit -qm later; REV=$(git rev-parse HEAD)
echo dirty >> tools/round-45/frozen.txt
rec r27-fx6a-dirty-in-scope python3 -I -B "$PF" --root "$D" --freeze "$FZ" --rev "$REV" --pathspec tools/round-45/ --freeze-path tools/round-45 --check-dirty --json-out "$S/out/fx6a.json"
git checkout -- tools/round-45/frozen.txt
echo dirty > other/uncommitted.txt
rec r28-fx6b-dirty-outside-scope python3 -I -B "$PF" --root "$D" --freeze "$FZ" --rev "$REV" --pathspec tools/round-45/ --freeze-path tools/round-45 --check-dirty --json-out "$S/out/fx6b.json"
rec r29-fx6b-other-dirtypathspec python3 -I -B "$PF" --root "$D" --freeze "$FZ" --rev "$REV" --pathspec tools/round-45/ --freeze-path tools/round-45 --check-dirty --dirty-pathspec other/ --json-out "$S/out/fx6b-other.json"
rec r30-fx6c-no-dirty-arm       python3 -I -B "$PF" --root "$D" --freeze "$FZ" --rev "$REV" --pathspec tools/round-45/ --freeze-path tools/round-45 --json-out "$S/out/fx6c.json"

# fx7: the real lane, read-only
rec r31-real-gate-measured python3 -I -B "$PF" --root "$LANE" --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec --rev e715263cb51b713c342ab992d527fe9d61d6f8ff --pathspec tools/round-45/ --freeze-path tools/round-45 --check-dirty
rec r32-real-gate-tip      python3 -I -B "$PF" --root "$LANE" --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec --rev "$(git -C "$LANE" rev-parse HEAD)" --pathspec tools/round-45/ --freeze-path tools/round-45 --check-dirty
rec r33-c86-paths        bash -c "git -C $LANE show --name-only --format= c86ea508 | awk -F/ '{print \$1\"/\"\$2}' | sort | uniq -c | sort -rn"
rec r34-c86-identity     bash -c "git -C $LANE log -1 --format='%an <%ae> | %cn <%ce>' c86ea508"
