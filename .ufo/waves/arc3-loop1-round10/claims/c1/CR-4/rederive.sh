#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SEAT="$ROOT/.ufo/waves/arc3-loop1-round10/claims/c1/CR-4"
EVIDENCE="$SEAT/evidence"
SOURCE="$ROOT/.ufo/waves/arc3-loop1-round8/claims/c3/EX-8/evidence/K8.vy"
VYPER="$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper"
RUN="$(mktemp -d /var/tmp/kaidoku-cr4-r10.XXXXXX)"

mkdir -p "$RUN/tmp" "$RUN/compile" "$RUN/probe" "$EVIDENCE/compile" "$EVIDENCE/probe"
cp "$SOURCE" "$EVIDENCE/K8.vy"

{
  printf 'measurement_utc='
  date -u +%Y-%m-%dT%H:%M:%SZ
  printf 'repo_head='
  git rev-parse HEAD
  printf 'work_commit='
  git rev-parse eb5a2c4
  printf 'source_path=%s\n' "$SOURCE"
  sha256sum "$SOURCE" "$EVIDENCE/K8.vy"
  printf 'compiler_path=%s\n' "$VYPER"
  sha256sum "$VYPER"
  "$VYPER" --version
  printf 'scratch=%s\nTMPDIR=%s\n' "$RUN" "$RUN/tmp"
  printf 'REA=' 
  env TMPDIR="$RUN/tmp" npx -y rea-agents@6.7.0 --version
} > "$EVIDENCE/identity.txt"

for target in london prague; do
  for pass in 1 2; do
    env TMPDIR="$RUN/tmp" "$VYPER" --evm-version "$target" -f bytecode_runtime "$EVIDENCE/K8.vy" > "$RUN/compile/$target.$pass.runtime.hex"
  done
  cmp "$RUN/compile/$target.1.runtime.hex" "$RUN/compile/$target.2.runtime.hex"
  cp "$RUN/compile/$target.1.runtime.hex" "$EVIDENCE/compile/$target.runtime.hex"
  env TMPDIR="$RUN/tmp" "$VYPER" --evm-version "$target" -f abi "$EVIDENCE/K8.vy" > "$EVIDENCE/compile/$target.abi.json"
  env TMPDIR="$RUN/tmp" "$VYPER" --evm-version "$target" -f method_identifiers "$EVIDENCE/K8.vy" > "$EVIDENCE/compile/$target.methodids.json"
  env TMPDIR="$RUN/tmp" "$VYPER" --evm-version "$target" -f settings "$EVIDENCE/K8.vy" > "$EVIDENCE/compile/$target.settings.json"
  env TMPDIR="$RUN/tmp" "$VYPER" --evm-version "$target" -f opcodes_runtime "$EVIDENCE/K8.vy" > "$EVIDENCE/compile/$target.opcodes.txt"
  env TMPDIR="$RUN/tmp" npx -y rea-agents@6.7.0 inspect-evm-interface "$EVIDENCE/compile/$target.runtime.hex" hex --format json > "$RUN/probe/$target.json" 2> "$RUN/probe/$target.stderr"
  cp "$RUN/probe/$target.json" "$EVIDENCE/probe/$target.json"
  cp "$RUN/probe/$target.stderr" "$EVIDENCE/probe/$target.stderr"
done

python3 "$SEAT/measure.py" "$EVIDENCE/compile" "$EVIDENCE/probe" > "$EVIDENCE/measure.txt"

python3 - HEAD eb5a2c4 <<'PY' > "$EVIDENCE/command-a.txt"
import json, pathlib, re, subprocess, sys

def get(rev, path):
    return subprocess.check_output(['git', 'show', f'{rev}:{path}'], text=True)

for rev in sys.argv[1:]:
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', rev,
                                     '--', 'corpus/knowledge'], text=True).splitlines()
    files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')}
    section = get(rev, 'corpus/README.md').split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
    mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
    craft = get(rev, 'SKILL.md').split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
    rules = re.split(r'(?m)^- \*\*', craft)[1:]
    pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
    resolved = 0
    for rule in rules:
        refs = re.findall(pattern, rule)
        valid = bool(refs)
        for name, first, last in refs:
            try:
                count = len(get(rev, 'corpus/knowledge/' + name).splitlines())
                start, end = int(first or 1), int(last or first or 1)
                valid = valid and 1 <= start <= end <= count
            except subprocess.CalledProcessError:
                valid = False
        resolved += valid
    print(json.dumps({'revision': subprocess.check_output(['git', 'rev-parse', rev], text=True).strip(),
        'mapped': len(files & mapped), 'knowledge_files': len(files),
        'missing': sorted(files - mapped), 'dangling': sorted(mapped - files),
        'citation_resolved_rules': resolved, 'rule_blocks': len(rules),
        'coverage_score': round(10 * len(files & mapped) / len(files), 2),
        'depth_score': round(10 * resolved / len(rules), 2)}, sort_keys=True))
PY

printf 'scratch=%s\n' "$RUN" > "$EVIDENCE/reproduction.txt"
printf 'Compile each EVM target twice, compare bytes, then run REA 6.7.0 inspect-evm-interface on each compiled runtime. All compiler/probe TMPDIR scratch was under /var/tmp.\n' >> "$EVIDENCE/reproduction.txt"
printf 'Command A used the frozen SCORECARD.md:88-124 recipe at HEAD and at work commit eb5a2c4; it measures baseline only because this seat creates a draft, not a corpus/map change.\n' >> "$EVIDENCE/reproduction.txt"
