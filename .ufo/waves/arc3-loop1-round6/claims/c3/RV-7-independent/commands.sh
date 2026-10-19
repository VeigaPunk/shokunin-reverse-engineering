#!/usr/bin/env bash
# Reproducing RV-7-independent's measurements. Read-only on the repo; scratch under /var/tmp.
set -euo pipefail
cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"   # repo root
REV=c625d5d
# 1. command A (verbatim from SCORECARD.md:88-124), for REV in c625d5d 58c3db7
python3 - "$REV" <<'PY'
import json, pathlib, re, subprocess, sys
rev = sys.argv[1]
def get(path):
    return subprocess.check_output(['git', 'show', f'{rev}:{path}'], text=True)
paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', rev, '--', 'corpus/knowledge'], text=True).splitlines()
files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')}
section = get('corpus/README.md').split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
craft = get('SKILL.md').split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
rules = re.split(r'(?m)^- \*\*', craft)[1:]
pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
resolved = 0
for rule in rules:
    refs = re.findall(pattern, rule); valid = bool(refs)
    for name, first, last in refs:
        try:
            count = len(get('corpus/knowledge/' + name).splitlines())
            start, end = int(first or 1), int(last or first or 1)
            valid = valid and 1 <= start <= end <= count
        except subprocess.CalledProcessError:
            valid = False
    resolved += valid
print(json.dumps({'revision': rev, 'mapped': len(files & mapped), 'knowledge_files': len(files),
 'missing': sorted(files - mapped), 'dangling': sorted(mapped - files),
 'citation_resolved_rules': resolved, 'rule_blocks': len(rules),
 'coverage_score': round(10*len(files & mapped)/len(files), 2),
 'depth_score': round(10*resolved/len(rules), 2)}, sort_keys=True))
PY
# 2. draft bytes: the fenced block in claims/c3/SC-3.md section 4
#    python3 - <<'PY' ... re.search(r'```markdown\n(.*?)```', t, re.S) ...
# 3. scratch landing: insert rule15-sc3.txt after the unique anchor "never a carried-over number.\n"
#    in `git show 58c3db7:SKILL.md`, then re-run command A's split/citation logic on the simulated file.
# 4. live probes (carrier paths absolute; disk-backed TMPDIR):
#    TMPDIR=/var/tmp/rv7-verify/probe npx -y rea-agents@6.4.0 inspect-evm-interface \
#      "$PWD/.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/creation.hex" hex --format json
#    TMPDIR=/var/tmp/rv7-verify/probe npx -y rea-agents@6.4.0 inspect-evm-interface \
#      "$PWD/.ufo/waves/arc3-loop1-round1/claims/c1/EX-02/smoke/out/Smoke_sol_Smoke.bin" hex --format json
