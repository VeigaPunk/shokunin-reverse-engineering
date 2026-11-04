# ExecC2 — independent R73-C2 re-derivation

Base `05bf065684e52d72ea25aad95f7acb71fcd7874c` and declaration `da6c17c1eb8dec0b780e276c7f1cb8d9b4fa4d4b` both yield audit rc 1, **6 mismatches**, rows `[false,false,false,false,false,false,true]`. Independently extracted committed inputs reproduce the predicates, but **D7 is already false-green**: existing before receipts resolve while the report/SCORECARD cross-document selection disagreement is never checked. Other atoms also contain identified syntactic false-green paths and stricter-than-routed repair requirements.

All seven own-word defect facts, exact committed evidence, atom comparisons, false-green analysis and limits: [ExecC2/Report.md](ExecC2/Report.md). Receipts: `ExecC2/committed-evidence.json`, `independent-comparison.json`, `base-audit.json`, `declaration-audit.json`, `audit-execution.json`.

No landing evaluated; zero landing mismatches not established. Report-side discrepancy is sourced to the committed non-author spotcheck, not a direct out-of-lane report read. Only assigned audits executed; no implementation edits, installs or general tests. Scratch deleted in `finally` after retaining receipts.

Report: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-73/w1/ExecC2/Report.md
