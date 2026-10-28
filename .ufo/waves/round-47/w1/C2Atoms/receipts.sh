#!/usr/bin/env bash
# C2Atoms receipt capture: one line per independently re-derived atom value.
set -u
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
B=13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5
H=e856beb552080c03ede6000b96f1b58bde44c421
cd "$L" || exit 1
printf 'label\tcommand\texit\tstdout_sha256\tstdout\n'
rc() {
  local label="$1"; shift
  local out code
  out=$("$@" 2>&1); code=$?
  printf '%s\t%s\t%s\t%s\t%s\n' "$label" "$*" "$code" \
    "$(printf '%s' "$out" | sha256sum | cut -d' ' -f1)" \
    "$(printf '%s' "$out" | tr '\n' '|' | cut -c1-300)"
}
rc seats-r45-w1 python3 -c "import json;print(json.load(open('/dev/stdin'))['counts']['spawn'])" < <(git show $B:.ufo/waves/round-45/w1-dispatch.json)
rc seats-r45-w2 python3 -c "import json;print(json.load(open('/dev/stdin'))['counts']['spawn'])" < <(git show $B:.ufo/waves/round-45/w2-dispatch.json)
rc seats-r46-w1 python3 -c "import json;print(json.load(open('/dev/stdin'))['counts']['spawn'])" < <(git show $B:.ufo/waves/round-46/w1-dispatch.json)
rc seats-r46-w2 python3 -c "import json;print(json.load(open('/dev/stdin'))['counts']['spawn'])" < <(git show $B:.ufo/waves/round-46/w2-dispatch.json)
rc window-claims-in-scope grep -c 'is empty' < <(git show $B:SCORECARD.md)
rc window-real-range-nonempty git log --name-status --format= 0425224..$B -- tools/round-46 plans/round-46-claims.md
rc window-claim-as-written-nonempty git log --name-status --format= 0425224..$H -- tools/round-46 plans/round-46-claims.md
rc window-correction-range-empty git log --name-status --format= 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md
rc path-dir-tree git cat-file -t $B:.ufo/waves/round-45/
rc path-file git cat-file -e $B:.ufo/waves/round-46/controls/ctl-c2-1-v1-scope.json
rc rev-5382acc8 git rev-parse --verify 5382acc85f9d8617fe242fc116819b8055dfc4c7^{commit}
rc rev-5382acc8-ancestor git merge-base --is-ancestor 5382acc85f9d8617fe242fc116819b8055dfc4c7 $B
rc rev-50862e4a git rev-parse --verify 50862e4a^{commit}
rc rev-50862e4a-ancestor git merge-base --is-ancestor 50862e4a $B
rc rev-landing-not-ancestor-of-base git merge-base --is-ancestor $H $B
rc coverage-total-base git ls-tree -r --name-only $B -- corpus/knowledge
rc coverage-total-landing git ls-tree -r --name-only $H -- corpus/knowledge
rc depth-blocks-base python3 -c "
import re,subprocess
s=subprocess.run(['git','show','13a9e9e1:SKILL.md'],capture_output=True,text=True).stdout
c=s.split('## Queue-drain craft ',1)[1].split('\n## ',1)[0]
print(len(re.split(r'(?m)^- \*\*',c)[1:]))"
rc depth-blocks-landing python3 -c "
import re,subprocess
s=subprocess.run(['git','show','e856beb5:SKILL.md'],capture_output=True,text=True).stdout
c=s.split('## Queue-drain craft ',1)[1].split('\n## ',1)[0]
print(len(re.split(r'(?m)^- \*\*',c)[1:]))"
rc counter-at-base python3 -I -B tools/round-47/record.py --root "$L" --rev $B --no-battery
rc counter-at-landing python3 -I -B tools/round-47/record.py --root "$L" --rev $H
rc counter-record-sha-at-freeze sh -c "git show 5017e1f:tools/round-47/record.py | sha256sum"
rc counter-record-sha-at-head sh -c "git show HEAD:tools/round-47/record.py | sha256sum"
rc counter-frozen-check-shape grep -c frozen_path_changed tools/round-47/record.py || true
