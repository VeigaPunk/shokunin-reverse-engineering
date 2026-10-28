#!/bin/bash
# R44ScoutSkill drift checks — read-only over the lane tree.
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
OUT=/fast/scratch/hyaku/kaidoku-r44/probe-R44ScoutSkill
mkdir -p "$OUT"
run() {
  local name="$1"; shift
  local t0=$(date +%s%N)
  "$@" > "$OUT/$name.stdout" 2> "$OUT/$name.stderr"
  local rc=$?
  local t1=$(date +%s%N)
  local sha=$(sha256sum "$OUT/$name.stdout" | cut -d' ' -f1)
  echo "{\"check\":\"$name\",\"cmd\":$(printf '%s' "$*" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))'),\"exit\":$rc,\"stdout_sha256\":\"$sha\",\"wall_ms\":$(( (t1-t0)/1000000 ))}"
}
cd "$LANE"
# 1. v4 table row count (rows between marker and end of table)
run v4_table_rows bash -c "awk '/sqfs-triage-table v4/,0' SKILL.md | grep -c '^| \`' || true"
# 2. legacy handler coverage in v4 cells/prose
run v4_legacy_cells bash -c "awk '/sqfs-triage-table v4/,/^\$/' SKILL.md | grep -c 'squashfs_v\\[123\\]\\*' ; awk '/triage v4 \\(round 42\\)/,/Status — unscored/' SKILL.md | grep -o 'squashfs_v2_nonstandard' | head -1"
# 3. registry: last registry heading + unregistered tool dirs
run registry_coverage bash -c "grep -nE '^#{2,4} .*registry' SKILL.md | tail -1 ; for n in 41 42 43; do ls -d tools/round-\$n 2>/dev/null; done"
# 4. v4 status line vs r43 score
run v4_status bash -c "grep -n 'round 43 re-scores' SKILL.md ; python3 -c \"import json;d=json.load(open('.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json'));print('r43-c1 met_target',d['met_target'],'exit',d['exit_code'],'matched',d['matched'])\""
# 5. PROVINCE frontier: squashfs mentions inside ## Frontier section vs file-wide
run province_frontier bash -c "awk '/^## Frontier/,/^## Adjacent/' PROVINCE.md | grep -ci 'squashfs\|sasquatch' ; grep -n 'Still Frontier\|stay Frontier\|stays here' PROVINCE.md"
# 6. SKILL/PROVINCE identical at base vs worktree
run files_vs_base bash -c "git diff c29360e3 HEAD -- SKILL.md PROVINCE.md | wc -l ; git diff c29360e3 -- SKILL.md PROVINCE.md | wc -l"
# 7. carrier fixture presence at base
run carriers_at_base bash -c "for f in v1-le--squashfs_v1.0_le v1-be--squashfs_v1.0_be v2-le--squashfs_v2.0_le v2-be--squashfs_v2.0_be; do git cat-file -e c29360e3:corpus/evidence/round-42/c2/fixtures/\$f.bin && echo \$f OK; done"
# 8. registry tool-file existence (tools/ entries only, existing at base)
run tool_existence bash -c "for p in tools/round-42/c1-counter.py tools/round-42/sqfs-triage-v4.py tools/round-42/indep-eval-v4.py tools/round-42/fixtures.json tools/round-40/sqfs-triage-v2.py tools/round-40/c1-counter.py tools/round-39/sqfs-triage.py tools/round-39/c1-counter.py tools/round-39/gen-squashfs.py; do git cat-file -e c29360e3:\$p 2>/dev/null && echo \"\$p OK\" || echo \"\$p MISSING\"; done"
# 9. dangling pointers in registry
run dangling_pointers bash -c "git cat-file -e c29360e3:tools/selftest.py 2>/dev/null && echo 'tools/selftest.py exists' || echo 'tools/selftest.py MISSING (SKILL.md:1002 r24 row)'; git cat-file -e c29360e3:.ufo/waves/hyaku/kaidoku25-prerequisite/parent-after-process.json 2>/dev/null && echo 'hyaku path exists' || echo '.ufo/waves/hyaku/... MISSING (SKILL.md:1100)'"
# 10. selftest count spot-check: r40 sqfs-triage-v2 declares 45
run selftest_count_spot bash -c "grep -cE 'def case_|@_?case' tools/round-40/sqfs-triage-v2.py"
# 11. oracle identity
run oracle_version bash -c "unsquashfs -version 2>&1 | head -1; command -v unsquashfs"
# 12. v4 interpreter exists (unregistered round-42 tool used by scored r43 receipt)
run v4_interpreter bash -c "ls -l tools/round-42/sqfs-triage-v4.py tools/round-42/indep-eval-v4.py tools/round-43/c1-counter.py 2>&1 | awk '{print \$NF, \$5}'"
