#!/usr/bin/env bash
# Round-52 ScoutMergeThemes scan receipts.
S=/fast/scratch/hyaku/kaidoku-r52/w1-ScoutMergeThemes
PKG=/home/vgpnk/Projects/shokuknow/merge/kaidoku
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
OUT=$S/receipts.jsonl
: > "$OUT"
run() { # id, description, command...
  local id="$1"; shift
  local desc="$1"; shift
  local cmd="$*"
  local so="$S/$id.stdout" se="$S/$id.stderr"
  local t0 t1 rc
  t0=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  ( cd "$S" && eval "$cmd" ) >"$so" 2>"$se"; rc=$?
  t1=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  python3 - "$id" "$desc" "$cmd" "$rc" "$t0" "$t1" "$so" "$se" >>"$OUT" <<'PY'
import hashlib,json,sys
id_,desc,cmd,rc,t0,t1,so,se=sys.argv[1:9]
def h(p):
    try: return hashlib.sha256(open(p,'rb').read()).hexdigest()
    except OSError: return None
print(json.dumps({"receipt_id":id_,"description":desc,"command":cmd,"exit_code":int(rc),
 "utc_start":t0,"utc_end":t1,"stdout_sha256":h(so),"stderr_sha256":h(se),
 "stdout_bytes":len(open(so,'rb').read()),"stderr_bytes":len(open(se,'rb').read())}))
PY
}
run R1 "package knowledge-entry inventory + theme classification" "python3 $S/scan.py"
run R2 "device-node / mknod / fifo / socket ground present in package?" "grep -rniE 'mknod|CAP_MKNOD|char[ -]?device|247:0|dev/led|device node|\\\\bfifo\\\\b|\\\\bsocket\\\\b' $PKG/knowledge $PKG/SOURCES.append.md | wc -l"
run R3 "padding / nopad / no-pad ground present in package?" "grep -rniE 'nopad|no-pad|padding' $PKG/knowledge $PKG/SOURCES.append.md | wc -l"
run R4 "ddwrt ground in package (row-level count)" "grep -rniE 'ddwrt|dd-wrt' $PKG/knowledge $PKG/SOURCES.append.md | wc -l"
run R5 "lane already holds the unblob format-matrix document (rows naming unblob.org/formats)" "grep -cE 'unblob.org/formats' $LANE/corpus/SOURCES.md"
run R6 "lane already holds the Freetz AVM-BE format note (AVM-BE-format.txt)" "grep -cE 'AVM-BE-format.txt' $LANE/corpus/SOURCES.md"
run R7 "lane already holds Freetz-NG docs/make/README.md (AVM-LE package doc)" "grep -cE 'docs/make/README' $LANE/corpus/SOURCES.md"
run R8 "lane mentions 6590 anywhere (AVM-LE device scope)" "grep -rc '6590' $LANE/corpus/SOURCES.md $LANE/corpus/knowledge/*.md | grep -v ':0' | wc -l"
run R9 "lane SOURCES max id" "grep -oE '^\\| S[0-9]+' $LANE/corpus/SOURCES.md | tr -d '| ' | sort -n | tail -1"
run R10 "id-collision: package rows vs lane rows" "python3 $S/idcheck.py"
run R11 "lane holds the 1970-fingerprint claim?" "grep -rn '1970' $LANE/corpus/knowledge/ | wc -l"
run R12 "lane holds NMI-gap / TI-checksum claim?" "grep -rniE 'NMI vector|TI checksum' $LANE/corpus/knowledge/ | wc -l"
run R13 "package entry count vs MERGE-REPORT stated count" "ls $PKG/knowledge/corpus/knowledge/*.md | wc -l"
run R14 "considerthese/ exists in this lane?" "ls -d $LANE/considerthese 2>&1 | wc -l"
run R15 "lane SOURCES row count" "grep -cE '^\\| S[0-9]+' $LANE/corpus/SOURCES.md"
