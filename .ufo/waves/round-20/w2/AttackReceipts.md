HOLDS — C3’s counted-receipt criterion at measured source S: all 19 run receipts validate with `--require-mid-maps`.

## Observations

- Exported `.ufo/waves/round-20/runs` and `.ufo/waves/round-17/tools` from commit `5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9` using `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin archive 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 -- .ufo/waves/round-20/runs .ufo/waves/round-17/tools | tar -x -C /tmp/a3receipts.Lj3Ru8` (exit 0). The S archive contained 19 `receipt.json` files; the label inventory is in `runs/run-log.txt:2-58` (the `t1246-link` entry at :34 was explicitly excluded before run).
- Invoked once per receipt: `python3 -I -B /tmp/a3receipts.Lj3Ru8/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/a3receipts.Lj3Ru8/.ufo/waves/round-20/runs/<label>/receipt.json`. Each returned exit 0, `status=valid`, zero findings:

| Label | Exit | Checks performed | Findings |
|---|---:|---:|---:|
| `t1246-addr2line` | 0 | 366 | none |
| `t1246-asm` | 0 | 372 | none |
| `t1246-buildid` | 0 | 366 | none |
| `t1246-cgo` | 0 | 372 | none |
| `t1246-compile` | 0 | 390 | none |
| `t1246-covdata` | 0 | 378 | none |
| `t1246-cover` | 0 | 372 | none |
| `t1246-doc` | 0 | 372 | none |
| `t1246-fix` | 0 | 366 | none |
| `t1246-go` | 0 | 378 | none |
| `t1246-gofmt` | 0 | 366 | none |
| `t1246-nm` | 0 | 366 | none |
| `t1246-objdump` | 0 | 372 | none |
| `t1246-pack` | 0 | 366 | none |
| `t1246-pprof` | 0 | 384 | none |
| `t1246-preprofile` | 0 | 372 | none |
| `t1246-test2json` | 0 | 366 | none |
| `t1246-trace` | 0 | 378 | none |
| `t1246-vet` | 0 | 372 | none |

- S validator selftest: `python3 -I -B /tmp/a3receipts.Lj3Ru8/.ufo/waves/round-17/tools/receipt-validate.py --selftest` (exit 0; `SELFTEST: CLEAN cases=28`). Its cases assert missing mid-map rejection with the flag and acceptance without it (`receipt-validate.py:978-1004`), absent analyze checks rejection (`:1029-1045`), and map checks on a non-analyze list step rejection (`:1071-1104`).
- Independent scratch mutation (copy of S `t1246-addr2line/receipt.json` in a `mkdtemp` directory; removed `map_path` and `map_sha256` from the analyze check): `python3 -I -B /tmp/a3receipts.Lj3Ru8/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/a3-missing-map-484ekw_f/receipt.json` returned exit 1, `status=invalid`, finding `mid_map_missing` at `$.steps.analyze.pin_checks[0]`.

## Assessment and residual risk

- **Inference:** C3’s falsifier condition at `claims.json:33-39` (“any counted receipt fails receipt-validate --require-mid-maps”) is not met at S. This agrees with the author-side result at `corpus/lessons/round-20.md:122-129`.
- The validator requires map files and recomputes their digest/verdict, and authenticates the analyze step (`receipt-validate.py:490-560`; `:502-509`). Its documented limit remains: it validates bytes present now and trusts the receipt’s pins for the run-window state (`:49-52`); it cannot rule out modification followed by restoration.
- This result is receipt-only, not evidence for first-failure comparisons. The retained run log records original `compare=2` statuses (`runs/run-log.txt:2-58`); the lesson describes the later comparison rerun at `corpus/lessons/round-20.md:105`. No comparison finding is made here.