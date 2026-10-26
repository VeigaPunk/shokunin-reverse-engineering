# Reference-probe control suite (fixture freeze, six carriers, K5/K6 metadata FIXTURES)

probe: `_harness/receipt_probe_NOT_COUNTER.py` (receipt-only reference; NOT the round-39 counter)
fixture freeze: `39e7eedb72f726801679259951e54c20da57b616` (scratch clone of the lane at `a2f64e1` + fake K5/K6 metadata; K5 in-tree symlink, K6 escaping symlink)

| control | counter exit | expected | carriers_matched | failing bindings |
|---|---|---|---|---|
| CTL-C1-0 | 1 | 1 | 0 | K1:after_present; K2:after_present; K3:after_present; K4:after_present; K5:after_present; K6:after_present |
| CTL-C1-1 | 1 | 1 | 4 | K5:after_present; K6:after_present |
| CTL-C1-2 | 1 | 1 | 0 | K1:after_evidence_id_ok; K2:after_evidence_id_ok; K3:after_evidence_id_ok; K4:after_evidence_id_ok; K5:after_evidence_id_ok; K6:after_evidence_id_ok |
| CTL-C1-3 | 0 | 0 | 6 | - |
| CTL-C1-4 | 1 | 1 | 4 | K2:after_gaps_exact; K5:after_gaps_exact |
| CTL-C1-5 | 1 | 1 | 0 | K1:first_add_strict_descendant; K2:first_add_strict_descendant; K3:first_add_strict_descendant; K4:first_add_strict_descendant; K5:first_add_strict_descendant; K6:first_add_strict_descendant |
| CTL-C1-6 | 1 | 1 | 4 | K2:after_gaps_exact; K5:after_gaps_exact |
| CTL-C1-7 | 1 | 1 | 4 | K1:after_gaps_exact; K6:after_gaps_exact |
| CTL-C1-8 | 1 | 1 | 0 | K1:after_gaps_exact; K2:after_gaps_exact; K3:after_gaps_exact; K4:after_gaps_exact; K5:after_gaps_exact; K6:after_gaps_exact |
| CTL-C1-9 | 1 | 1 | 0 | K1:after_no_failed_chunk; K2:after_no_failed_chunk; K3:after_no_failed_chunk; K4:after_no_failed_chunk; K5:after_no_failed_chunk; K6:after_no_failed_chunk |

- CTL-C1-3 is the only control the receipt-only probe scores green (exit 0, 6/6). Its receipts were produced by `_harness/fabricate_receipts.py` with no REA process.
- Every other control is refused, each by the binding named in its `control.json`.
