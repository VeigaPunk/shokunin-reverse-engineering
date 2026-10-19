set -u
TOOL=/var/tmp/ex26/tool-after-7cd19c3c.py
B=/var/tmp/ex26/behavior
rm -rf $B/fx; mkdir -p $B/fx/live $B/fx/rec
echo "== tool sha256 =="; sha256sum $TOOL
echo
echo "== F1: cleanly-absent, receipt-vs-live (expect MATCH exit 0) =="
$TOOL capture --out $B/fx/rec/absent.txt --paths $B/fx/live/gone.txt --label "ex26-absent" ; echo "capture rc=$?"
$TOOL verify $B/fx/rec/absent.txt --live; echo "verify rc=$?"
echo
echo "== F2: control — file now exists, ref absent (expect ABSENT exit 13) =="
printf 'now here\n' > $B/fx/live/gone.txt
$TOOL verify $B/fx/rec/absent.txt --live; echo "verify rc=$?"
rm -f $B/fx/live/gone.txt
echo
echo "== F3: cleanly-absent, receipt-vs-receipt (expect MATCH exit 0) =="
$TOOL capture --out $B/fx/rec/absent-b.txt --paths $B/fx/live/gone.txt --label "ex26-absent-b" >/dev/null; echo "capture rc=$?"
$TOOL verify $B/fx/rec/absent.txt $B/fx/rec/absent-b.txt; echo "verify rc=$?"
echo
echo "== F4: error-carrying (READ-ERROR), receipt-vs-live (expect UNEVALUABLE exit 14) =="
printf 'secret\n' > $B/fx/live/locked.txt; chmod 000 $B/fx/live/locked.txt
$TOOL capture --out $B/fx/rec/uneval.txt --paths $B/fx/live/locked.txt --label "ex26-uneval"; echo "capture rc=$?"
$TOOL verify $B/fx/rec/uneval.txt --live; echo "verify rc=$?"
echo
echo "== F5: error-carrying one side only (ref=READ-ERROR, cand=readable) (expect UNEVALUABLE 14) =="
chmod 644 $B/fx/live/locked.txt
$TOOL verify $B/fx/rec/uneval.txt --live; echo "verify rc=$?"
echo
echo "== F6: error-carrying one side only (ref=readable, cand=READ-ERROR) (expect UNEVALUABLE 14) =="
$TOOL capture --out $B/fx/rec/readable.txt --paths $B/fx/live/locked.txt --label "ex26-readable" >/dev/null
chmod 000 $B/fx/live/locked.txt
$TOOL verify $B/fx/rec/readable.txt --live; echo "verify rc=$?"
echo
echo "== F7: receipt-vs-receipt, one side error-carrying (expect UNEVALUABLE 14) =="
$TOOL verify $B/fx/rec/readable.txt $B/fx/rec/uneval.txt; echo "verify rc=$?"
chmod 644 $B/fx/live/locked.txt
