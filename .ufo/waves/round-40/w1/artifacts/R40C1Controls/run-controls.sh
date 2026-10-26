#!/bin/sh
# run-controls.sh -- driver for the P40-C1 pre-freeze control suite (R40C1Controls).
#
# Every control runs in its own throwaway clone, so no overlay can leak into another
# and the clone is never the lane: this script writes only under --work.
#
#   ./run-controls.sh --honest <clone> --base <OID> --freeze <OID> --counter <tool.py> \
#                     --work <dir> [--only ID] [--json-out results.json]
#
# <clone>    a clone of the lane containing the honest round-40 tree (its tip is the
#            scored revision). Used read-only (`git clone --shared`).
# <base>     the pre-round base commit (default fa6a8a3f); CTL-C1-0 scores it.
# <freeze>   the honest freeze commit; controls that rewrite the freeze build a new one
#            and pass its OID to the counter instead.
# <counter>  the round-40 C1 counter, called as
#              python3 -I -B <counter> --root R --rev V --freeze F --json-out J
#            exit 0 met_target, 1 not met, 2 unevaluable.
#
# Stages come from suite.json `commit_stage`:
#   base                 score the base commit
#   pre-freeze/in-freeze build a synthetic freeze = honest freeze tree + overlay, commit
#                        it, then restore the honest tip on top and score there
#   post-freeze          honest tip + overlay commit, scored against the honest freeze
#   refusal_class=audit  skipped: no control can refuse it (reported SKIP)
#
# One line per control: `<id> PASS|FAIL|SKIP ...`. suite.json's `expected` block is the
# authority; for a byte-only counter the `expected_byte_only` block applies when the
# counter reports `rerun_projection_ok: null`.
#
# POSIX sh; no git subcommand mutates <clone>. Fixture commits use -c user.name=fx.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
HONEST= FREEZE= COUNTER= WORK= ONLY= JSON= BASE=
while [ $# -gt 0 ]; do
    case $1 in
        --honest) HONEST=$2; shift 2 ;;
        --base) BASE=$2; shift 2 ;;
        --freeze) FREEZE=$2; shift 2 ;;
        --counter) COUNTER=$2; shift 2 ;;
        --work) WORK=$2; shift 2 ;;
        --only) ONLY=$2; shift 2 ;;
        --json-out) JSON=$2; shift 2 ;;
        *) echo "run-controls: unknown argument $1" >&2; exit 2 ;;
    esac
done
[ -n "$HONEST" ] && [ -n "$FREEZE" ] && [ -n "$COUNTER" ] && [ -n "$WORK" ] || {
    echo "run-controls: --honest --freeze --counter --work are required" >&2; exit 2; }
[ -n "$BASE" ] || BASE=fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f
mkdir -p "$WORK"
WORK=$(CDPATH= cd -- "$WORK" && pwd)
: "${TMPDIR:=$WORK}"; export TMPDIR
SPEC=.ufo/waves/round-40/c1/carriers.json
RESULTS=$WORK/results.txt
: > "$RESULTS"
CLONES=
HONEST_TIP=$(git -C "$HONEST" rev-parse --verify HEAD)

ctl() { python3 -I -B "$here/ctl-lib.py" "$@"; }
ctl_transform() { ctl --control "$1" --root "$2" --freeze "$3" --spec "$SPEC" --stage "$4"; }
commit_at() {                      # tolerates an empty commit (position-only controls)
    git -C "$1" add -A
    if [ -n "$(git -C "$1" status --porcelain)" ]; then
        git -C "$1" -c user.name=fx -c user.email=fx@fx commit -q -m "$2"
    fi
    git -C "$1" rev-parse HEAD
}
score() {
    set +e
    python3 -I -B "$COUNTER" --root "$1" --rev "$2" --freeze "$3" \
        --json-out "$1/score.json" > "$1/score.stdout" 2> "$1/score.stderr"
    rc=$?
    set -e
    echo "$rc"
}
field_of() {   # field_of <id> <commit_stage|overlay|refusal_class>
    python3 -I -B -c 'import json,sys
cs=json.load(open(sys.argv[1]))["controls"]
c=[x for x in cs if x["id"]==sys.argv[2]][0]
print(c.get(sys.argv[3]) or "")' "$here/suite.json" "$1" "$2"
}

report() {
    python3 -I -B - "$here/suite.json" "$1" "$2" "$3" "$RESULTS" <<'PY'
import json, sys
suite, cid, rc, score_path, out = sys.argv[1:6]
ctrl = [c for c in json.load(open(suite))['controls'] if c['id'] == cid][0]
exp = dict(ctrl['expected'])
try:
    got = json.load(open(score_path))
except Exception:
    got = {}
bindings = got.get('bindings') or {}
if bindings.get('rerun_projection_ok', 'absent') is None and 'expected_byte_only' in ctrl:
    exp = dict(ctrl['expected_byte_only'])
failing = sorted(k for k, v in bindings.items() if v is False)
problems = []
if int(rc) != exp['exit']:
    problems.append('exit %s != %s' % (rc, exp['exit']))
if 'met_target' in exp and bool(got.get('met_target')) != bool(exp['met_target']):
    problems.append('met_target %r != %r' % (got.get('met_target'), exp['met_target']))
for name in exp.get('must_fail') or []:
    if bindings.get(name) is not False:
        problems.append('%s should be false, is %r' % (name, bindings.get(name)))
for name in exp.get('must_pass') or []:
    if bindings.get(name) is not True:
        problems.append('%s should be true, is %r' % (name, bindings.get(name)))
verdict = 'PASS' if not problems else 'FAIL'
line = ('%s %s expected=exit,%s got=exit,%s failing=%s%s'
        % (cid, verdict, exp['exit'], rc, ','.join(failing) or '-',
           '' if not problems else ' :: ' + '; '.join(problems)))
print(line)
with open(out, 'a') as f:
    f.write(line + '\n')
PY
}

run_one() {
    id=$1
    stage=$(field_of "$id" commit_stage)
    cls=$(field_of "$id" refusal_class)
    d=$WORK/$id
    rm -rf "$d"
    if [ "$cls" = audit ]; then
        echo "$id SKIP refusal_class=audit" | tee -a "$RESULTS"
        return
    fi
    git clone -q --shared "$HONEST" "$d"
    case $stage in
    base)
        git -C "$d" checkout -q "$BASE"
        rev=$BASE; fz=$BASE ;;
    pre-freeze|in-freeze)
        git -C "$d" checkout -q "$BASE"
        git -C "$d" checkout "$FREEZE" -- .
        if [ "$id" = CTL-C1-16 ]; then
            rm -f "$d/.ufo/waves/round-40/c1/controls.json"
        else
            if ! ctl_transform "$id" "$d" "$FREEZE" freeze; then
                echo "$id MATERIALIZE-FAIL" | tee -a "$RESULTS"; rm -rf "$d"; return
            fi
        fi
        fz=$(commit_at "$d" "ctl: $id freeze")
        if [ "$id" = CTL-C1-16 ]; then
            git -C "$d" checkout "$FREEZE" -- .ufo/waves/round-40/c1/controls.json
        fi
        git -C "$d" checkout "$HONEST_TIP" -- .
        if ! ctl_transform "$id" "$d" "$FREEZE" tip; then
            echo "$id MATERIALIZE-FAIL" | tee -a "$RESULTS"; rm -rf "$d"; return
        fi
        rev=$(commit_at "$d" "ctl: $id tip") ;;
    post-freeze)
        git -C "$d" checkout -q "$HONEST_TIP"
        if ! ctl_transform "$id" "$d" "$FREEZE" all; then
            echo "$id MATERIALIZE-FAIL" | tee -a "$RESULTS"; rm -rf "$d"; return
        fi
        rev=$(commit_at "$d" "ctl: $id")
        fz=$FREEZE ;;
    *)
        echo "$id STAGE-UNKNOWN $stage" | tee -a "$RESULTS"; rm -rf "$d"; return ;;
    esac
    CLONES="$CLONES $d"
    rc=$(score "$d" "$rev" "$fz")
    if [ "$id" = CTL-C1-N2 ]; then
        mkdir -p "$WORK/tmp2"
        set +e
        TMPDIR=$WORK/tmp2 python3 -I -B "$COUNTER" --root "$d" --rev "$rev" \
            --freeze "$fz" --json-out "$d/score2.json" > "$d/score2.stdout" 2>&1
        set -e
        if ! python3 -I -B -c 'import json,sys
a=json.load(open(sys.argv[1])); b=json.load(open(sys.argv[2]))
ok = a.get("bindings")==b.get("bindings") and a.get("carriers_matched")==b.get("carriers_matched")
raise SystemExit(0 if ok else 1)' "$d/score.json" "$d/score2.json"; then
            echo "$id FAIL projection unstable across two scoring runs" | tee -a "$RESULTS"
            rm -rf "$d"; return
        fi
    fi
    report "$id" "$rc" "$d/score.json"
}

IDS=$(python3 -I -B -c 'import json,sys; print(" ".join(c["id"] for c in json.load(open(sys.argv[1]))["controls"]))' "$here/suite.json")
for id in $IDS; do
    if [ -n "$ONLY" ] && [ "$ONLY" != "$id" ]; then continue; fi
    run_one "$id"
done

if [ -n "$JSON" ]; then
    python3 -I -B - "$here/suite.json" "$RESULTS" "$JSON" <<'PY'
import json, sys
suite, results, out = sys.argv[1:4]
verdicts = {}
for line in open(results):
    parts = line.split()
    if len(parts) >= 2:
        verdicts[parts[0]] = parts[1]
doc = {'suite': suite,
       'controls': [{'id': c['id'], 'commit_stage': c.get('commit_stage'),
                     'refusal_class': c.get('refusal_class'),
                     'expected': c['expected'],
                     'observed': verdicts.get(c['id'], 'NOT RUN')}
                    for c in json.load(open(suite))['controls']]}
json.dump(doc, open(out, 'w'), indent=1, sort_keys=True)
PY
    echo "wrote $JSON"
fi

for d in $CLONES; do rm -rf "$d"; done
echo "results: $RESULTS"
