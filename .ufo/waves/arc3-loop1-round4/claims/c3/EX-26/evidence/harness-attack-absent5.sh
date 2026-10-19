set -u
TOOL=/var/tmp/ex26/tool-after-7cd19c3c.py
B=/var/tmp/ex26/behavior
rm -rf $B/fx5; mkdir -p $B/fx5
echo "== A1: five cleanly-absent stanzas, --require-paths 5, --live =="
$TOOL capture --out $B/fx5/absent5.txt --paths $B/fx5/p1 $B/fx5/p2 $B/fx5/p3 $B/fx5/p4 $B/fx5/p5 --label "ex26-absent5"; echo "capture rc=$?"
$TOOL verify $B/fx5/absent5.txt --live --require-paths 5; echo "verify rc=$?"
echo
echo "== A2: same receipt, receipt-vs-receipt (self) =="
$TOOL verify $B/fx5/absent5.txt $B/fx5/absent5.txt --require-paths 5; echo "verify rc=$?"
