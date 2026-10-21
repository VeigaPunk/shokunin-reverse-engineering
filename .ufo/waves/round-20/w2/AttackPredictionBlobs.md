HOLDS — for all 19 labels, `first_failure` equals the corresponding `first_failure.h1` at both freeze F and measured source S; `SHA256SUMS` verifies.

**Observation.** F = `808cbb31a1e24656da5ba4967497e602fbca7415`; S = `5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9`. Revision-scoped `git show` reads parsed each prediction and swiss blob at each ref; all 38 comparisons matched. Every prediction and swiss blob was byte-identical F↔S, and the checked working-tree files matched S. The manifests cover exactly 40 files (19 prediction blobs, 19 swiss blobs, carriers table, decision rule); checksum checks passed at F, S, and in the working tree. Manifest anchors: `.ufo/waves/round-20/predictions/SHA256SUMS:1-40`. Prediction/h1 line anchors below are relative to `.ufo/waves/round-20/`; both F and S have these same lines and values.

| Label | prediction `first_failure` | swiss `first_failure.h1` | F and S |
|---|---|---|---|
| `t1246-addr2line` | `predictions/t1246-addr2line.prediction.json:8` | `predictions/swiss-misread-v2/t1246-addr2line.json:37` | equal |
| `t1246-asm` | `predictions/t1246-asm.prediction.json:8` | `predictions/swiss-misread-v2/t1246-asm.json:30` | equal |
| `t1246-buildid` | `predictions/t1246-buildid.prediction.json:8` | `predictions/swiss-misread-v2/t1246-buildid.json:30` | equal |
| `t1246-cgo` | `predictions/t1246-cgo.prediction.json:8` | `predictions/swiss-misread-v2/t1246-cgo.json:30` | equal |
| `t1246-compile` | `predictions/t1246-compile.prediction.json:8` | `predictions/swiss-misread-v2/t1246-compile.json:55` | equal |
| `t1246-covdata` | `predictions/t1246-covdata.prediction.json:8` | `predictions/swiss-misread-v2/t1246-covdata.json:30` | equal |
| `t1246-cover` | `predictions/t1246-cover.prediction.json:8` | `predictions/swiss-misread-v2/t1246-cover.json:30` | equal |
| `t1246-doc` | `predictions/t1246-doc.prediction.json:8` | `predictions/swiss-misread-v2/t1246-doc.json:30` | equal |
| `t1246-fix` | `predictions/t1246-fix.prediction.json:8` | `predictions/swiss-misread-v2/t1246-fix.json:30` | equal |
| `t1246-go` | `predictions/t1246-go.prediction.json:8` | `predictions/swiss-misread-v2/t1246-go.json:61` | equal |
| `t1246-gofmt` | `predictions/t1246-gofmt.prediction.json:8` | `predictions/swiss-misread-v2/t1246-gofmt.json:30` | equal |
| `t1246-nm` | `predictions/t1246-nm.prediction.json:8` | `predictions/swiss-misread-v2/t1246-nm.json:37` | equal |
| `t1246-objdump` | `predictions/t1246-objdump.prediction.json:8` | `predictions/swiss-misread-v2/t1246-objdump.json:37` | equal |
| `t1246-pack` | `predictions/t1246-pack.prediction.json:8` | `predictions/swiss-misread-v2/t1246-pack.json:30` | equal |
| `t1246-pprof` | `predictions/t1246-pprof.prediction.json:8` | `predictions/swiss-misread-v2/t1246-pprof.json:43` | equal |
| `t1246-preprofile` | `predictions/t1246-preprofile.prediction.json:8` | `predictions/swiss-misread-v2/t1246-preprofile.json:30` | equal |
| `t1246-test2json` | `predictions/t1246-test2json.prediction.json:8` | `predictions/swiss-misread-v2/t1246-test2json.json:30` | equal |
| `t1246-trace` | `predictions/t1246-trace.prediction.json:8` | `predictions/swiss-misread-v2/t1246-trace.json:49` | equal |
| `t1246-vet` | `predictions/t1246-vet.prediction.json:8` | `predictions/swiss-misread-v2/t1246-vet.json:37` | equal |

**Commands and exit codes.**
- From `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20`: `sha256sum -c predictions/SHA256SUMS >/dev/null` → **0** (working tree).
- From `/home/vgpnk/Projects/shokunin`: `python3 -I -B /tmp/kr20-predblobs.CDCDfj/verify.py /tmp/kr20-predblobs.CDCDfj` → **0**; output: F and S `git ls-tree -r --name-only <REV> -- .ufo/waves/round-20/predictions` each **0**; each `git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show <REV>:.ufo/waves/round-20/predictions/<path>` succeeded; extracted F and S `sha256sum -c predictions/SHA256SUMS` each **0**, 40 entries; 19 prediction labels and 19 swiss labels, all comparisons true, `ERRORS=0`.

**Inference and residual scope.** This falsification check finds no mismatch in the specified revision-scoped blob identity/value contract; it does not test receipt binding, analyzer runtime results, or prediction correctness. The C3 statement and comparator shape are at `claims.json:33-39` and `contract.md:76-81`.