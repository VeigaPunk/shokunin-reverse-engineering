#!/usr/bin/env bash
# score-controls.sh - score R41-C2 control tables against one evaluator and one
# envelope set.
#
#   score-controls.sh --interp PATH --eval PATH --envelopes DIR [--envelopes DIR]...
#                     [--controls DIR] [--control NAME=PATH]... [--detail]
#
# --interp    the triage interpreter (v2/v3 CLI: --skill SKILL --json ENV...)
# --eval      the independent evaluator, called once as: eval ENVELOPE...
#             (TSV `path<TAB>label<TAB>action`, a JSON list of
#             {path,label,action}, or a JSON object with a `results` list)
# --envelopes a directory of *.json envelopes, or of class subdirectories each
#             holding envelope.json; repeatable, lists are concatenated
# --controls  directory scanned for *.skill.md (default: this script's directory)
# --control   one extra control as NAME=PATH (repeatable; scored first)
#
# Prints one line per control: NAME, matched/n, interpreter exit code.  With
# --detail it also prints every mismatched envelope, expected -> observed.
# Exit 0 scored; 2 usage/IO/parse error (never a control verdict).
set -u

here=$(cd -- "$(dirname -- "$0")" && pwd)
interp=
evalr=
envdirs=()
controls=$here
detail=0
declared=()

usage() {
  sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'
}

while [ $# -gt 0 ]; do
  case $1 in
    --interp) interp=${2-}; shift 2 ;;
    --eval) evalr=${2-}; shift 2 ;;
    --envelopes) envdirs+=("${2-}"); shift 2 ;;
    --controls) controls=${2-}; shift 2 ;;
    --control) declared+=("${2-}"); shift 2 ;;
    --detail) detail=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'score-controls: unknown argument %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
done

if [ -z "$interp" ] || [ -z "$evalr" ] || [ ${#envdirs[@]} -eq 0 ]; then
  printf 'score-controls: --interp, --eval and --envelopes are required\n' >&2
  exit 2
fi
for f in "$interp" "$evalr"; do
  [ -r "$f" ] || { printf 'score-controls: cannot read %s\n' "$f" >&2; exit 2; }
done
# ---- envelopes -------------------------------------------------------------
envs=()
for envdir in "${envdirs[@]}"; do
  [ -d "$envdir" ] || { printf 'score-controls: %s is not a directory\n' "$envdir" >&2; exit 2; }
  found=0
  if compgen -G "$envdir/*/envelope.json" >/dev/null; then
    while IFS= read -r f; do envs+=("$f"); found=1; done \
      < <(printf '%s\n' "$envdir"/*/envelope.json | sort)
  elif compgen -G "$envdir/*.json" >/dev/null; then
    while IFS= read -r f; do envs+=("$f"); found=1; done \
      < <(printf '%s\n' "$envdir"/*.json | sort)
  fi
  if [ "$found" -eq 0 ]; then
    printf 'score-controls: no *.json or */envelope.json under %s\n' "$envdir" >&2
    exit 2
  fi
done

# ---- controls --------------------------------------------------------------
names=()
paths=()
if [ ${#declared[@]} -gt 0 ]; then
  for spec in "${declared[@]}"; do
    names+=("${spec%%=*}")
    paths+=("${spec#*=}")
  done
fi
if [ -d "$controls" ] && compgen -G "$controls/*.skill.md" >/dev/null; then
  while IFS= read -r f; do
    names+=("$(basename "$f" .skill.md)")
    paths+=("$f")
  done < <(printf '%s\n' "$controls"/*.skill.md | sort)
fi
if [ ${#names[@]} -eq 0 ]; then
  printf 'score-controls: no control tables found\n' >&2
  exit 2
fi

# ---- score -----------------------------------------------------------------
python3 -I -B - "$interp" "$evalr" "$detail" \
  "${names[@]}" -- "${paths[@]}" -- "${envs[@]}" <<'PY'
import json
import os
import subprocess
import sys


def die(msg):
    sys.stderr.write('score-controls: %s\n' % msg)
    raise SystemExit(2)


args = sys.argv[1:]
if args.count('--') != 2:
    die('internal: expected two -- separators')
if len(args) < 4:
    die('internal: short argument vector')
interp, evalr, detail_flag = args[0], args[1], args[2]
cut1 = args.index('--')
cut2 = args.index('--', cut1 + 1)
names = args[3:cut1]
paths = args[cut1 + 1:cut2]
envs = args[cut2 + 1:]
if len(names) != len(paths):
    die('internal: %d names, %d paths' % (len(names), len(paths)))
if not envs:
    die('internal: no envelope argument')
detail = detail_flag == '1'


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def pairs_from(text):
    """Return {path: (label, action)} from TSV or JSON output."""
    stripped = text.strip()
    out = {}
    if not stripped:
        return out
    if stripped[0] in '{[':
        try:
            obj = json.loads(stripped)
        except ValueError:
            return out
        rows = obj.get('results') if isinstance(obj, dict) else obj
        if not isinstance(rows, list):
            return out
        for row in rows:
            if isinstance(row, dict) and isinstance(row.get('path'), str) \
                    and isinstance(row.get('label'), str):
                out[row['path']] = (row['label'], row.get('action'))
        return out
    for line in stripped.splitlines():
        parts = line.rsplit('\t', 2)
        if len(parts) == 3:
            out[parts[0]] = (parts[1], parts[2])
            continue
        parts = line.rsplit(None, 2)
        if len(parts) == 3:
            out[parts[0]] = (parts[1], parts[2])
    return out


def ident(path):
    parent = os.path.basename(os.path.dirname(path))
    return parent or os.path.basename(path)


# ---- expected --------------------------------------------------------------
res = run(['python3', '-I', '-B', evalr] + envs)
expected = pairs_from(res.stdout) if res.returncode == 0 else {}
if not expected:
    expected = {}
    for env in envs:
        one = run(['python3', '-I', '-B', evalr, env])
        got = pairs_from(one.stdout) if one.returncode == 0 else {}
        if not got:
            die('evaluator failed on %s (exit %d): %s'
                % (env, one.returncode, (one.stderr or '').strip()[:200]))
        expected.update(got)
missing = [e for e in envs if e not in expected]
if missing:
    die('evaluator returned no pair for %s' % missing[0])

# ---- observed --------------------------------------------------------------
rows = []
for name, path in zip(names, paths):
    if not os.access(path, os.R_OK):
        die('cannot read control %s' % path)
    res = run(['python3', '-I', '-B', interp, '--skill', path, '--json'] + envs)
    if res.returncode != 0:
        rows.append((name, 0, len(envs), res.returncode,
                     [(ident(e), expected[e], None) for e in envs]))
        continue
    observed = pairs_from(res.stdout)
    hits = 0
    misses = []
    for env in envs:
        got = observed.get(env)
        if got == expected[env]:
            hits += 1
        else:
            misses.append((ident(env), expected[env], got))
    rows.append((name, hits, len(envs), 0, misses))

width = max([len(r[0]) for r in rows] + [7])
print('%-*s  %9s  %s' % (width, 'control', 'matched/n', 'interp exit'))
for name, hits, total, code, _misses in rows:
    print('%-*s  %9s  %11d' % (width, name, '%d/%d' % (hits, total), code))
print('# controls=%d envelopes=%d evaluator=%s interp=%s'
      % (len(rows), len(envs), os.path.basename(evalr), os.path.basename(interp)))
if detail:
    for name, hits, total, code, misses in rows:
        print('\n## %s  %d/%d  exit=%d' % (name, hits, total, code))
        if code != 0:
            print('   interpreter refused the table; no envelope was labelled')
            continue
        if not misses:
            print('   no mismatch')
        for this, want, got in misses:
            print('   %-22s want %s/%s  got %s'
                  % (this, want[0], want[1],
                     ('%s/%s' % got) if got else '<abstain/unmatched>'))
PY
exit $?
