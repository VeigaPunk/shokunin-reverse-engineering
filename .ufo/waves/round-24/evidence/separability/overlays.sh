#!/usr/bin/env bash
set -u
S=/fast/scratch/kaidoku-r24/seats/ResSeparability-2
L=$S/lane
T=$S/tools
OUT=$S/out
HEAD=69e82c48be5614ce96f7c1c32445fe61c4870630
ENTRY=corpus/knowledge/2026-10-21-r24-pcap-family-envelopes.md
EV=.ufo/waves/round-24/evidence/c1
rm -rf "$T" "$OUT"; mkdir -p "$T" "$OUT"
git -C "$L" show $HEAD:.ufo/waves/round-24/tools/count-c1.py > "$T/count-c1.py"
git -C "$L" show $HEAD:.ufo/waves/round-24/tools/freeze-gate.py > "$T/freeze-gate.py"
git -C "$L" show 97ade2e:.ufo/waves/round-24/tools/freeze-gate.py > "$T/freeze-gate-orig.py"
sha256sum "$T"/*.py
G() { git -C "$L" -c user.name=sep -c user.email=sep@invalid -c commit.gpgsign=false "$@"; }
c1() { python3 -I -B "$T/count-c1.py" --root "$L" --rev HEAD > "$OUT/$1.c1.json"; local e=$?
  python3 -c "import json,sys;d=json.load(open('$OUT/$1.c1.json'));print('C1 $1 exit=$e held=%s/%s err=%s'%(d.get('t2_held_count'),d.get('t2_total'),d.get('error')))"; }
c2() { local tag=$1; shift; python3 -I -B "${GATE:-$T/freeze-gate.py}" --root "$L" --rev HEAD "$@" > "$OUT/$tag.c2.json"; local e=$?
  python3 -c "
import json;d=json.load(open('$OUT/$tag.c2.json'))
f=[x for x in d.get('freezes',[]) if 'round-24/' in x['claims_file']]
print('C2 $tag exit=$e audited=%s disclosures=%s r24=%s err=%s'%(d.get('audited'),
 {k:d['disclosures'][k] for k in ('exact','of','missing','mismatched','stray')} if 'disclosures' in d else None,
 (f[0]['verdict'],[(x['finding'],x.get('path','').rsplit('/',1)[-1],x.get('commits')) for x in f[0]['findings']]) if f else None, d.get('error')))"; }
fresh() { G checkout -q -f --detach "$1" && G clean -qfdx; }
GA=(--require-clean round-24 --disclosures corpus/claim-freezes.tsv)
c1only_sources() {
  git -C "$L" show $HEAD:corpus/SOURCES.md | grep -v '^| S068 |' | grep -v '^- Instrument freeze before claims (round 24)' > "$L/corpus/SOURCES.md"; }

echo '== O0 HEAD'; fresh $HEAD; c1 O0; c2 O0 "${GA[@]}"

echo '== O1 C1-only on 74cd4e3 (frozen claims + envelopes, no gate revision, no ledger, no S068)'
fresh 74cd4e3; G checkout -q $HEAD -- $ENTRY; c1only_sources; G add -A; G commit -qm 'O1 C1 only'
c1 O1; c2 O1 "${GA[@]}"; c2 O1-noledger --require-clean round-24
GATE=$T/freeze-gate-orig.py c2 O1-origgate --require-clean round-24

echo '== O1b C1-only on 97ade2e (no claims.json at all)'
fresh 97ade2e; G checkout -q 74cd4e3 -- $EV; G checkout -q $HEAD -- $ENTRY; c1only_sources; G add -A; G commit -qm 'O1b'
c1 O1b

echo '== O2 C2-only on 9fb4eac with C1 envelopes removed (supersession hash preserved)'
fresh 9fb4eac; G rm -rq $EV; G checkout -q $HEAD -- .ufo/waves/round-24/claims.json corpus/claim-freezes.tsv; G commit -qm 'O2 C2 only'
c1 O2; c2 O2 "${GA[@]}"

echo '== O2b C2-only on 5dc49bf, gate revision re-applied (no C1 commit in ancestry)'
fresh 5dc49bf; G checkout -q 9fb4eac -- .ufo/waves/round-24/tools/freeze-gate.py; G commit -qm 'O2b gate revision'
X=$(git -C "$L" rev-parse HEAD)
G checkout -q $HEAD -- .ufo/waves/round-24/claims.json corpus/claim-freezes.tsv; G commit -qm 'O2b literal hash'
c2 O2b-literal "${GA[@]}"
sed -i "s/9fb4eacd23eb69ee9d659dd041e006e9ccd61480/$X/" "$L/.ufo/waves/round-24/claims.json"; G commit -qam 'O2b rewritten hash'
c1 O2b; c2 O2b-rewritten "${GA[@]}"

echo '== X1 HEAD + post-freeze edit to C1 instrument count-c1.py'
fresh $HEAD; echo '# r' >> "$L/.ufo/waves/round-24/tools/count-c1.py"; G commit -qam X1; c1 X1; c2 X1 "${GA[@]}"

echo '== X2 HEAD + C2 S068 row malformed as duplicate id S064'
fresh $HEAD; sed -i 's/^| S068 |/| S064 |/' "$L/corpus/SOURCES.md"; G commit -qam X2; c1 X2; c2 X2 "${GA[@]}"

echo '== X3 HEAD + R24-C1 claim text edited post-freeze (total 4->2, target)'
fresh $HEAD; python3 - "$L/.ufo/waves/round-24/claims.json" <<'P'
import json,sys;p=sys.argv[1];d=json.load(open(p));c=d['claims'][0];c['total']=2;c['target']='>=1/2';d['claims'][1]['target']='anything'
json.dump(d,open(p,'w'),indent=1)
P
G commit -qam X3; c1 X3; c2 X3 "${GA[@]}"

echo '== X4 HEAD - S068 row and path line'; fresh $HEAD; c1only_sources; G commit -qam X4; c1 X4; c2 X4 "${GA[@]}"
echo '== X5 HEAD - C1 knowledge entry and envelopes'; fresh $HEAD; G rm -rq $ENTRY $EV; G commit -qm X5; c1 X5; c2 X5 "${GA[@]}"
echo '== X6 HEAD - claim-freezes.tsv and QUALITY33'; fresh $HEAD; G rm -q corpus/claim-freezes.tsv; G checkout -q 9fb4eac -- corpus/QUALITY.md; G commit -qm X6; c1 X6; c2 X6 --require-clean round-24
echo '== X7 HEAD + post-freeze edit to producer run-rea.py'; fresh $HEAD; echo '# r' >> "$L/.ufo/waves/round-24/tools/run-rea.py"; G commit -qam X7; c1 X7; c2 X7 "${GA[@]}"
echo '== X8 HEAD + revert freeze-gate to frozen 97ade2e blob (C2 instrument revision undone)'; fresh $HEAD; G checkout -q 97ade2e -- .ufo/waves/round-24/tools/freeze-gate.py; G commit -qm X8; c1 X8; c2 X8 "${GA[@]}"
fresh $HEAD
