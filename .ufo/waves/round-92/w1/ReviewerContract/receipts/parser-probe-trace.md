# parser-probe-trace.md — v2 `typed_refusal` probe (ReviewerContract, R92-C2 review)

v2 module imported from the declaration-commit clone
(`/fast/scratch/hyaku/kaidoku-r92/ReviewerContract/clone/tools/round-92/stop-boundary-battery-v2.py`).
Probe code imported the module and called `typed_refusal(stdout)` directly for each shape.

| case | stdout shape | typed_refusal | last line parses as dict | note |
|---|---|---|---|---|
| plain | `{"tool": "t", "class": "c", "refused": "because"}` | True | True | round-91 print contract |
| pretty-multi | pretty-printed multi-line refusal body | False | False | round-91 never emits this |
| trailing-brace | `{...} trailing` | False | False | not round-91 shape |
| refused-null | `{"refused": null, "x": 1}` | True | True | residual: key-presence probe |
| refused-bool | `{"refused": false}` | True | True | residual: key-presence probe |
| extra-json-line | typed JSON then an afterthought JSON line | False | True (second line) | parser uses LAST line only |
| json-array | `[{"refused": true}]` | False | False | not a dict |
| quoted | refusal JSON inside prose | False | False | not raw JSON |

rc gate: `score_cell` sets `typed = (rc == 2) and typed_refusal(...)` (v2:169) — rc 1 or any
other nonzero rc can never be typed regardless of stdout shape. Verified in receipt
`c2-counterfeit-C-v2.json` (all 10 cells rc 1, typed false) and the live rerun
`receipt-c.json` (same).

Host: /usr/bin/upx sha256 `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`
(matches v2 pin).
