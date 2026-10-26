#!/usr/bin/env bash
# runrea.sh -- one REA 6.5.0 extract-firmware run on a development carrier.
#
# Usage: runrea.sh NAME ARM INPUT   (ARM = after | before)
#   after : PATH unchanged, sasquatch/sasquatch-v4be resolvable
#   before: $HOME/.local/bin stripped from the child PATH; REA_UNBLOB_COMMAND
#           stays absolute.
# Writes into $WORK/<NAME>-<ARM>/: stdout.json (raw CLI stdout), envelope.json
# (parsed JSON), run.json (argv, exit code, PATH arm), out/ (REA output dir).
# The caller owns WORK and TMPDIR.
set -u
NAME=$1; ARM=$2; INPUT=$3
WORK=${WORK:?WORK must be set}
BASE="$WORK/$NAME-$ARM"
rm -rf -- "$BASE"
mkdir -p "$BASE"
OUT="$BASE/out"
export REA_UNBLOB_COMMAND="$HOME/.local/bin/unblob"
if [ "$ARM" = before ]; then
  NEWPATH=$(printf '%s' "$PATH" | tr ':' '\n' | grep -v -x -F "$HOME/.local/bin" | paste -sd: -)
  export PATH="$NEWPATH"
fi
cd "$BASE" || exit 1
npx -y rea-agents@6.5.0 extract-firmware --format json --full-output "$INPUT" "$OUT" \
  > "$BASE/stdout.json" 2> "$BASE/stderr.txt"
RC=$?
python3 - "$BASE" "$NAME" "$ARM" "$INPUT" "$RC" <<'PY'
import json, os, shutil, sys
base, name, arm, inp, rc = sys.argv[1:6]
raw = open(os.path.join(base, 'stdout.json'), 'r', encoding='utf-8', errors='replace').read()
obj = None
try:
    obj = json.loads(raw)
except ValueError:
    start = raw.find('{')
    if start >= 0:
        try:
            obj = json.loads(raw[start:])
        except ValueError:
            obj = None
if obj is not None:
    with open(os.path.join(base, 'envelope.json'), 'w', encoding='utf-8') as fh:
        json.dump(obj, fh)
        fh.write('\n')
path_bin = os.path.join(os.path.expanduser('~'), '.local', 'bin')
real = os.path.realpath(path_bin)
record = {
    'name': name, 'arm': arm, 'input': inp, 'exit_code': int(rc),
    'rea_argv': ['npx', '-y', 'rea-agents@6.5.0', 'extract-firmware',
                 '--format', 'json', '--full-output', inp, '$out'],
    'parsed': obj is not None,
    'home_bin_on_path': any(p and os.path.realpath(p) == real
                            for p in os.environ.get('PATH', '').split(':')),
    'rea_unblob_command': os.environ.get('REA_UNBLOB_COMMAND'),
}
with open(os.path.join(base, 'run.json'), 'w', encoding='utf-8') as fh:
    json.dump(record, fh, indent=2, sort_keys=True)
    fh.write('\n')
print(name, arm, 'exit', rc, 'parsed', obj is not None,
      'home_bin_on_path', record['home_bin_on_path'])
PY
exit 0
