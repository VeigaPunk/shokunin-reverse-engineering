# ExecGrammar — R52 wave 1

Verdict: settled. Files are isolated to `.ufo/waves/round-52/w1/ExecGrammar/`.

- `grammar.md` records the exact normalized envelope paths and distinguishes the harness `run.json` wrapper from the committed `after.json` data envelope. It documents wrapper receipt pointers and the published files, gaps, diagnostic link mapping, subject SHA-256 and handlers used by v2 controls.
- `disposition-witness.py` performs the requested offline comparison on the four committed envelopes and their frozen nonregular oracle rows. No REA invocation, vendor fetch, or data run occurred.
- Retained output: `ExecGrammar/disposition-witness.stdout`; command `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ExecGrammar/disposition-witness.py`; exit 0; UTC `2026-10-30T10:48:47Z`; stdout SHA-256 `1444e90dbc24a658195cc5dbcfb283a61ff8db2b1775ada4fbaa3cf771f32ac5`. Output counts/results: c6430 568 gaps/1 removal/824 nonregular R50 PASS and law PASS; c6490 613/1/914 PASS/PASS; g7581 637/3/1001 FAIL with 12 missing under R50, PASS under law; g7582 same. Thus CTL-OLD disposition is 2/4 and law disposition 4/4.
- The script's exit 0 means the comparison completed; verdicts are explicitly printed per arm. Its scope reproduces the disposition check's three classes, not full counter predicates or byte-dependent checks.
- Status record: `ExecGrammar/status.json`. No tools installed; no checks beyond the recorded offline witness were run. Risks: the witness is standalone and deliberately limited to the disposition clause; the L1's integrated counter controls remain authoritative.

Report path: `.ufo/waves/round-52/w1/ExecGrammar.md`.
