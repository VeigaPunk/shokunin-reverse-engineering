#!/bin/bash
# W2Chronology receipts: every command below was run; output sha256 and exit code recorded in receipts.tsv
set -u
export GIT_NO_REPLACE_OBJECTS=1
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
F=decc5697bfd4ec1e9de4a762ad199d9bd9c4230d
D=4aabb0b4bf716fb564c8406509c40b0a67457800
L=29883d4ec35a31a8393c4ffb220888c44c0bb022
A=.ufo/waves/round-49/w2/W2Chronology
OUT=$LANE/$A
cd "$LANE"
set +u
run() { local name="$1"; shift; local t; t=$(date -u +%FT%TZ); "$@" > "$OUT/$name.out" 2> "$OUT/$name.err"; local rc=$?; printf '%s\t%s\texit=%s\tstdout_sha256=%s\tcmd=%s\n' "$name" "$t" "$rc" "$(sha256sum < "$OUT/$name.out" | cut -c1-64)" "$*" >> "$OUT/receipts.tsv"; }
: > "$OUT/receipts.tsv"
run log-freeze-landing git log --format='%H %ad %cd %s' --date=iso e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9..$L
run ancestry-freeze-in-data git merge-base --is-ancestor $F $D
run ancestry-data-in-landing git merge-base --is-ancestor $D $L
run ancestry-freeze-in-landing git merge-base --is-ancestor $F $L
run add-c1-receipts git log --diff-filter=A --format=%H%x20%ad -- corpus/evidence/round-49/c1
run add-after-json-any-path git log --diff-filter=A --format=%h%x20%ad%x20%s --date=iso -- '*round-49/c1/*after.json'
run commits-touching-tools-r49 git log --format='%h %ad %s' --date=iso -- tools/round-49 plans/round-49-claims.md
run frozen-paths-freeze-to-landing git diff --name-only $F $L -- plans/round-49-claims.md tools/round-49 tools/round-42 tools/round-39 tools/round-27 corpus/evidence/round-44
run commits-touching-frozen-after-freeze git log --format=%h $F..$L -- plans tools/round-49 tools/round-42 tools/round-39 tools/round-27 corpus/evidence/round-44/oracle corpus/evidence/round-44/carriers
run tree-status-tracked-mods git status --porcelain --untracked-files=no
run freeze-blobs-sha sh -c "for f in tools/round-49/c1-counter.py tools/round-49/c2-mismatch.py tools/round-49/c1-controls.py tools/round-49/c1-run.py tools/round-49/c1-run.sh plans/round-49-claims.md; do git show $F:\$f | sha256sum | sed \"s#-#\$f#\"; done"
run freeze-vs-landing-blob-counter sh -c "git rev-parse $L:tools/round-49/c1-counter.py $F:tools/round-49/c1-counter.py"
run control-rev-and-counter-sha sh -c "grep -h -o -E '\"rev\": \"[0-9a-f]{40}\"|\"exit_code\": [0-9]+' .ufo/waves/round-49/controls/c0/receipt.json .ufo/waves/round-49/controls/ctl-c2-0-do-nothing.json"
run l1-scores-cited-exist sh -c "for p in .ufo/waves/round-49/l1/scores/c1-final.json .ufo/waves/round-49/l1/scores/c2-final.json; do if git cat-file -e $L:\$p 2>/dev/null; then echo \"TRACKED \$p\"; elif [ -e \$p ]; then echo \"WORKTREE \$p\"; else echo \"MISSING \$p\"; fi; done"
run w1-report-mtimes-latest sh -c "find .ufo/waves/round-49/w1 -type f -printf '%TY-%Tm-%TdT%TH:%TM:%TS %p\n' | sort | tail -5"
run w1-files-after-freeze sh -c "find .ufo/waves/round-49/w1 -type f -newermt @1793225512 | wc -l"
run draft-mtimes-tools sh -c "find .ufo/waves/round-49/draft/tools/round-49 .ufo/waves/round-49/draft/plans -maxdepth 1 -type f -printf '%TY-%Tm-%TdT%TH:%TM:%TS %p\n' | sort"
run wave1-hash-records sh -c "grep -h -E '^[0-9a-f]{64}  ' .ufo/waves/round-49/w1/C1CounterMut/draft-sha256.txt"
run entry-draft-r49-sha sh -c "sha256sum .ufo/waves/round-49/w1/artifacts/R49EntryDraft/corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md .ufo/waves/round-49/w1/C1ScribeEntry/entry.md; wc -l .ufo/waves/round-49/w1/artifacts/R49EntryDraft/corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md .ufo/waves/round-49/w1/C1ScribeEntry/entry.md"
run wave1-seat-count sh -c "python3 -c \"import json;r=json.load(open('.ufo/waves/round-49/w1/swarm-registry.json'));print(len(r['members']))\"; ls .ufo/waves/round-49/w1/*.md | wc -l"
run c2-seat-no-report sh -c "python3 -c \"import json;r=json.load(open('.ufo/waves/round-49/r49-w1-results.json'));x=[y for y in r['results'] if y['name']=='C2SourcesReopen'][0];print(x['output'][:200])\""
run mutant-vs-frozen-counter sh -c "for m in .ufo/waves/round-49/w1/C1CounterMut/mutants/M36-provenance-substring-only.py .ufo/waves/round-49/w1/C1CounterMut/mutants/M50-freeze-walk-empty.py; do diff /fast/scratch/hyaku/kaidoku-r49/W2Chronology/frozen-c1-counter.py \$m | grep -c '^[<>]'; done"
run blob-scan-attacked-drafts python3 $LANE/$A/scan_blobs.py /fast/scratch/hyaku/kaidoku-r49/W2Chronology/blobs-all.txt
run landing-score-files sh -c "for f in c1-at-data-4aabb0b4 c1-at-landing c2-at-landing; do python3 -c \"import json,sys;d=json.load(open('.ufo/waves/round-49/l1/scores/'+sys.argv[1]+'.json'));print(sys.argv[1], d.get('rev'), d.get('exit_code'))\" \$f; done"
