#!/bin/bash
# Real-lane probes for R38W2CritGateBypass. Read-only git; writes only scratch.
set -u
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=/fast/scratch/hyaku/kaidoku-r38/R38W2CritGateBypass
PKG=/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
F=e059ca9391642d5b71b6662cabcbdce0d9308719
LAND=3b960fe5f9a7f1dfa22819f98dc0fa983f4260a8
TIP=0fc6113376a156fddc3ec385386d71c3a4a9f690
CTL=efd5c47a72a50b3a434783f82268fb4a96e636a1
V3=f1010f677a53ecf0e671952ce1bf4f44d51e151b
GD=tools/round-38/freeze-drift.py
cd "$L" || exit 9

fd() { python3 -I -B "$GD" "$@" | python3 -c 'import json,sys;d=json.load(sys.stdin);print("verdict="+d["verdict"],"commits="+str([c["commit"][:8] for c in d["drift"]]))'; }

echo "P1 QUALITY-79 command (default paths) at the control-receipts commit"
echo -n "   "; fd --root . --freeze $F --rev $CTL
echo "P2 same rev, generator path added"
echo -n "   "; python3 -I -B "$GD" --root . --freeze $F --rev $CTL tools/round-38/gen-controls.py | python3 -c 'import json,sys;d=json.load(sys.stdin);print("verdict="+d["verdict"],"commits="+str([c["commit"][:8] for c in d["drift"]]))'
echo "P3 default paths at the landing"
echo -n "   "; fd --root . --freeze $F --rev $LAND
echo "P4 default paths at the landing with the later commit f1010f67 offered as the freeze"
echo -n "   "; fd --root . --freeze $V3 --rev $LAND
echo "P5 default paths at the landing with a caller-chosen one-path list"
echo -n "   "; fd --root . --freeze $F --rev $LAND corpus/evidence/round-37/c1/K1/oracle.tsv
echo "P6 default paths at the harness-fix commit (matched pair)"
echo -n "   default : "; fd --root . --freeze $F --rev cb4326b2aa4c2024af0651fe6115b82d0c4de3df
echo -n "   harness : "; python3 -I -B "$GD" --root . --freeze $F --rev cb4326b2aa4c2024af0651fe6115b82d0c4de3df tools/round-38/c1-run.sh | python3 -c 'import json,sys;d=json.load(sys.stdin);print("verdict="+d["verdict"],"commits="+str([c["commit"][:8] for c in d["drift"]]))'
echo "P7 rule paths that differ between the freeze and the landing / tip"
for r in $CTL $LAND $TIP; do
  echo "   $r: $(git diff --name-only --no-renames $F $r -- plans/round-38-claims.md tools/round-38/c1-counter.py tools/round-38/c2-counter.py .ufo/waves/round-38/c1/carriers.json ':(glob)corpus/evidence/round-37/c1/*/oracle.tsv' ':(glob)corpus/evidence/round-37/c1/*/carrier.*' tools/round-38/gen-controls.py tools/round-38/c1-run.sh tools/round-27/xpin-attribute.mjs | tr '\n' ' ')"
done
echo "P8 first commit touching the claims doc (the derivable freeze)"
echo "   $(git log --reverse --format=%H -- plans/round-38-claims.md | head -1)"
echo "P9 frozen counter vs shipped counter on the same receipts at the landing"
git show $F:tools/round-38/c1-counter.py > "$S/c1-counter-frozen.py"
echo -n "   frozen (sha256 $(sha256sum "$S/c1-counter-frozen.py" | cut -c1-12)) : "
python3 -I -B "$S/c1-counter-frozen.py" --root . --rev $LAND --freeze $F --pkg65 $PKG | python3 -c 'import json,sys;d=json.load(sys.stdin);print("carriers_matched="+str(d["carriers_matched"]),"met_target="+str(d["met_target"]))'
echo -n "   shipped                                          : "
python3 -I -B tools/round-38/c1-counter.py --root . --rev $LAND --freeze $F --pkg65 $PKG | python3 -c 'import json,sys;d=json.load(sys.stdin);print("carriers_matched="+str(d["carriers_matched"]),"met_target="+str(d["met_target"]))'
echo "P10 shipped counter at the landed tip"
echo -n "   "; python3 -I -B tools/round-38/c1-counter.py --root . --rev $TIP --freeze $F --pkg65 $PKG | python3 -c 'import json,sys;d=json.load(sys.stdin);print("carriers_matched="+str(d["carriers_matched"]),"met_target="+str(d["met_target"]),"bindings false="+str([k for k,v in d["bindings"].items() if isinstance(v,bool) and not v]))'
echo "P11 the lesson's cited C2 receipt"
echo "   lesson line 11 cites .ufo/waves/round-38/l1/scores/c2-final.json -> $([ -e .ufo/waves/round-38/l1/scores/c2-final.json ] && echo present || echo ABSENT); committed: $(ls .ufo/waves/round-38/l1/scores/)"
echo "P12 freeze-drift.py at the freeze"
echo -n "   tools/round-38/freeze-drift.py: "; git cat-file -e $F:tools/round-38/freeze-drift.py 2>/dev/null && echo present || echo ABSENT
