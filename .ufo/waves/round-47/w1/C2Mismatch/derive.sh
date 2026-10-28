#!/usr/bin/env bash
# C2Mismatch independent derivation of the four before-mismatches.
# Every command is read-only on the lane; each row prints cmd / exit / stdout sha256 / UTC.
set -u
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
REV=13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5
out=${1:?usage: derive.sh OUTDIR}
mkdir -p "$out"
cd "$out" || exit 1

rec() { # name, then the command argv
  local name=$1; shift
  local utc; utc=$(date -u +%FT%TZ)
  "$@" > "$name.out" 2> "$name.err"
  local rc=$?
  printf '%s\t%s\t%s\t%s\t%s\n' "$name" "$rc" \
    "$(sha256sum "$name.out" | cut -d' ' -f1)" "$utc" \
    "$(printf '%s ' "$@" | tr '\n' ' ')" >> commands.tsv
  echo "== $name rc=$rc sha=$(sha256sum "$name.out" | cut -d' ' -f1) utc=$utc"
}

: > commands.tsv

# --- M1 round-45 wave-2 seats -------------------------------------------------
rec m1-w1-dispatch git -C "$R" show "$REV:.ufo/waves/round-45/w1-dispatch.json"
rec m1-w2-dispatch git -C "$R" show "$REV:.ufo/waves/round-45/w2-dispatch.json"
rec m1-w2-results git -C "$R" show "$REV:.ufo/waves/round-45/r45-w2-results.json"
rec m1-seat-count python3 -c "
import json,subprocess
R='$R'; REV='$REV'
for p in ('.ufo/waves/round-45/w1-dispatch.json','.ufo/waves/round-45/w2-dispatch.json'):
    d=json.loads(subprocess.run(['git','-C',R,'show',REV+':'+p],capture_output=True,text=True).stdout)
    print(p,'counts.spawn',d['counts']['spawn'])
for p in ('.ufo/waves/round-45/r45-w1-results.json','.ufo/waves/round-45/r45-w2-results.json'):
    d=json.loads(subprocess.run(['git','-C',R,'show',REV+':'+p],capture_output=True,text=True).stdout)
    print(p,'seats',d['seats'],'len(results)',len(d['results']))
sed=subprocess.run(['git','-C',R,'show',REV+':SCORECARD.md'],capture_output=True,text=True).stdout.splitlines()
print('SCORECARD:3527',sed[3526])
print('SCORECARD:3528',sed[3527])
"
rec m1-third-wave git -C "$R" ls-tree -r --name-only "$REV" -- .ufo/waves/round-45/w3-dispatch.json

# --- M2 round-46 window -------------------------------------------------------
rec m2-line python3 -c "
import subprocess
R='$R'; REV='$REV'
t=subprocess.run(['git','-C',R,'show',REV+':SCORECARD.md'],capture_output=True,text=True).stdout.splitlines()
print('SCORECARD:3635',t[3634])
"
rec m2-window-at-base git -C "$R" log --name-status --format= "$REV".."$REV" -- tools/round-46 plans/round-46-claims.md
rec m2-window-0425224-to-base git -C "$R" log --name-status --format= 0425224.."$REV" -- tools/round-46 plans/round-46-claims.md
rec m2-window-332f4884-to-base git -C "$R" log --name-status --format= 332f4884.."$REV" -- tools/round-46 plans/round-46-claims.md
rec m2-window-0425224-to-7bf33e31 git -C "$R" log --name-status --format= 0425224..7bf33e31 -- tools/round-46 plans/round-46-claims.md
rec m2-window-332f4884-to-58eb04b6 git -C "$R" log --name-status --format= 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md

# --- M3 coverage ---------------------------------------------------------------
rec m3-knowledge-count-at-base sh -c "git -C $R ls-tree -r --name-only $REV -- corpus/knowledge | grep -c '\.md$'"
rec m3-knowledge-count-at-e1c83313 sh -c "git -C $R ls-tree -r --name-only e1c83313 -- corpus/knowledge | grep -c '\.md$'"
rec m3-coverage-pair python3 -c "
import re,subprocess,os
R='$R'; REV='$REV'
paths=[p for p in subprocess.run(['git','-C',R,'ls-tree','-r','--name-only',REV,'--','corpus/knowledge'],capture_output=True,text=True).stdout.splitlines() if p.endswith('.md')]
stems={os.path.basename(p)[:-3] for p in paths}
t=subprocess.run(['git','-C',R,'show',REV+':corpus/README.md'],capture_output=True,text=True).stdout
sec=t.split('## Coverage map\n',1)[1].split('\n## ',1)[0]
toks=re.findall(r'2026-10-\d{2}-[a-z0-9-]+',sec)
ms=set(toks)
print('knowledge_files',len(stems),'map_token_occurrences',len(toks),'map_unique',len(ms))
print('mapped_intersection',len(stems&ms),'dangling',sorted(ms-stems),'missing',sorted(stems-ms))
"
# --- M4 depth ------------------------------------------------------------------
rec m4-block-count python3 -c "
import re,subprocess
R='$R'; REV='$REV'
skill=subprocess.run(['git','-C',R,'show',REV+':SKILL.md'],capture_output=True,text=True).stdout
craft=skill.split('## Queue-drain craft (',1)[1].split('\n## ',1)[0]
blocks=re.split(r'(?m)^- \*\*',craft)[1:]
print('rule_blocks',len(blocks))
"
rec m4-citation-resolution python3 -c "
import re,subprocess
R='$R'; REV='$REV'
def show(p):
    r=subprocess.run(['git','-C',R,'show',REV+':'+p],capture_output=True,text=True)
    return r.stdout if r.returncode==0 else None
skill=show('SKILL.md')
craft=skill.split('## Queue-drain craft (',1)[1].split('\n## ',1)[0]
blocks=re.split(r'(?m)^- \*\*',craft)[1:]
REF=re.compile(r'((?:corpus|plans|tools)/[A-Za-z0-9._/-]+)(?::(\d+)(?:-(\d+))?)?')
ok=0
for b in blocks:
    refs=REF.findall(b); good=bool(refs)
    for name,first,last in refs:
        body=show(name)
        if body is None: good=False; break
        n=len(body.splitlines()); s=int(first or 1); e=int(last or first or 1)
        if not (1<=s<=e<=n): good=False; break
    ok+=good
print('citation_resolved_rules %d/%d' % (ok,len(blocks)))
"
rec m4-block-count-at-e1c83313 python3 -c "
import re,subprocess
R='$R'
skill=subprocess.run(['git','-C',R,'show','e1c83313:SKILL.md'],capture_output=True,text=True).stdout
craft=skill.split('## Queue-drain craft (',1)[1].split('\n## ',1)[0]
print('rule_blocks_at_e1c83313',len(re.split(r'(?m)^- \*\*',craft)[1:]))
"
echo "--- commands.tsv ---"
cat commands.tsv
