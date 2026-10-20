# C3 binding review — `t1250-vet`

## Findings (severity order)

### No actionable binding defect found; exact-read prediction mismatch is reported below

**Observation — frozen identity and carrier binding.** `producer.json` records label `t1250-vet` and branch tip `a1140e76fffdc1be032d9d813dbb686157803bbc` (`.ufo/waves/round-19/runs/t1250-vet/producer.json:2-5`). The frozen prediction names `/home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/vet` and SHA-256 `9b9d776e7569c910de714790a1b9bab1287b49fdc210973158f3076cee683bf7` (`.ufo/waves/round-19/predictions/t1250-vet.prediction.json:34-36`). Independently hashing the live carrier produced that same digest; the receipt records the same `sha256_pre` and `sha256_post` (`.ufo/waves/round-19/runs/t1250-vet/receipt.json:5-9`). The frozen `SHA256SUMS` entry for this prediction is `b49702371a57bf97746669b3cda26b1a642ae04bf99604bc8f656d0b73fbf38a`; the working prediction hashes to that value and `git diff` against the freeze commit is empty.

**Observation — one bound runtime and retained log.** The receipt has one `bound_sessions` entry (`receipt.json:2-3`). Its retained-log record binds `logs/rea-ghidra-CSKBVG/ghidra.log`, size 37,973 bytes, SHA-256 `a5de762231722468bcf265d5cd13ad9669f3a6d59a2746c73373e18a1a1a79c2` (`receipt.json:1955-1962`). Independent `sha256sum` and `wc -c` returned the same digest and size. `observation.json` binds that same path, size and digest (`observation.json:78-81`). The literal log contains the Go 1.25.0 snapshot route and analyzer failure at lines 180-186, and `Caused by: java.io.EOFException: Invalid index: 13902080` at line 229 (`logs/rea-ghidra-CSKBVG/ghidra.log`). The observation records one invalid-index read, `13902080`, and no EOF reads (`observation.json:73-75`, `:10`).

**Observation — pin maps.** There are exactly two standalone mid maps, `pins/mid-1.json` and `pins/mid-2.json`; each has 152 entries. The receipt embeds 152-entry `pins_pre` and `pins_post` maps, with `pins_compare.equal: true` and empty changed/errors/missing lists (`receipt.json:348-354`; map sections begin at `:356` and `:1122`). Independent canonicalization of the four `.entries` objects yielded the same SHA-256, `3838353e9b5da82bb8172ceff35701d95f89085c5760427a02f99a69870c65dd`. Independently hashed mid-map file digests match the receipt’s `pin_checks`: mid-1 `712f80696c35556953dceaa790ce8d173b65a00f07436fef5615920781c8a2c6`, mid-2 `abd0d119e26f38845662b3388f82e565b1028ab05a4ce20e5f46b892a14247d6`; both checks report 152 entries, `equal: true`, and empty changed/missing lists (`receipt.json:1934-1952`). Both mid maps also record the frozen prediction digest above (`pins/mid-1.json:758-761`, `pins/mid-2.json:758-761`).

The retained validator evidence records exit 0, one valid receipt, 366 checks, no findings, pins available, and `require_mid_maps: true` (`evidence/receipt-validation/t1250-vet.json:2-22`). This is retained evidence; I did not rewrite the receipt or rerun validation.

**Observation — comparison and frozen decision.** `compare.json` has `all_match: false`; its only mismatch is `extra.invalid_index_reads`: observed `[13902080]`, predicted `[13902080, 852107777, 1801722468838924630]` (`compare.json:1-2, 51-60`). The frozen rule explicitly says compare exit is reported per label while the mechanism verdict comes from the bound log; a D label is confirmed when its bound log reports a failure containing at least one H1-only index and no index outside the frozen H1 list (`predictions/decision-rule.json:3-6`). The frozen H1-only values for vet are `{13902080, 852107777}` (`decision-rule.json:21-25`). Thus the observed index is H1-only, with no additional observed index outside the frozen H1 list. **Inference:** this bound D-label log satisfies the frozen H1-confirming criterion despite the exact-list compare mismatch; it is not a full-list prediction match. `compare.exit` is 1 and `carrier-run.exit` and `observation.exit` are 0. Do not report `all_match` as true. This one-label review does not establish the required silence of the seven non-D labels.

### Expected validator digest change — not a finding

**Observation:** the producer and receipt pin the receipt validator at `70672eb3bd0c06e93ca439a31558f35ab7f76bd23aa74acd026290972553d145` (`producer.json:11`; `receipt.json:1103-1105` and `:1869-1872`). That is also the validator digest from the frozen commit. The current validator file hashes to `6afb7ef6600cdc7907d5eb4af1ac97b9dae1a10c648c50474d249fca2ac2c762`. **Inference:** this is the instructed post-run forward-fix mismatch, not evidence that the receipt’s historical pin is wrong. No receipt was rewritten.

**Observation:** independent `sha256sum` of the other producer-pinned tools—`carrier-run.py`, `pins.py`, `log-extract.py`, `compare.py`, `swiss-misread.py`, and `selection.py`—matched the digests recorded at `producer.json:7-10,12-13`. The validator is the sole producer-tool digest difference and is explained above.

## Residual risk and verification gaps

- The receipt itself discloses that retained logs are polling copies and lines written after the final poll but before REA deletes its runtime root can be missing (`receipt.json:24`). The retained log is internally hash-bound, but this capture limit remains.
- This scope covers only `t1250-vet`. The frozen cohort rule additionally requires checking the seven non-D labels for absence of Go analysis failures (`decision-rule.json:5-8`).
- No LSP device is mounted: `read xd://lsp` returned “No such tool”; the available-device list had no LSP route. This target is generated JSON/log evidence, so no caller/definition/diagnostics check was available. Literal log inspection is not semantic source proof.
- No carrier execution, REA analysis, build, broad suite, mutation test, or production edit was performed.

## Commands and observed exit codes

All paths below are under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` unless absolute.

```sh
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
R="$LANE/.ufo/waves/round-19/runs/t1250-vet"
sha256sum "$R/logs/rea-ghidra-CSKBVG/ghidra.log" "$R/pins/mid-1.json" "$R/pins/mid-2.json" "$R/carrier-run.stdout"
wc -c "$R/logs/rea-ghidra-CSKBVG/ghidra.log" "$R/carrier-run.stdout"
sha256sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/vet
# exit 0
```
Observed: log `a5de7622…a1a79c2` / 37,973 bytes; mid-1 `712f8069…1c8a2c6`; mid-2 `abd0d119…14247d6`; carrier `9b9d776e…e683bf7`.

```sh
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
R="$LANE/.ufo/waves/round-19/runs/t1250-vet"
find "$R/pins" -maxdepth 1 -type f -name 'mid-*.json' -printf '%f\n' | wc -l
jq '.pins_pre.entries|length' "$R/receipt.json"
jq '.pins_post.entries|length' "$R/receipt.json"
jq '.entries|length' "$R"/pins/mid-*.json
for x in pre post; do jq -S ".pins_${x}.entries" "$R/receipt.json" | sha256sum; done
for f in "$R"/pins/mid-*.json; do jq -S '.entries' "$f" | sha256sum; done
# exit 0
```
Observed: two mid files; all four maps contain 152 entries. Canonical SHA-256 of each map’s `.entries` object was `3838353e…870c65dd` (exit 0).

```sh
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
git -C "$LANE" --no-optional-locks show a1140e76fffdc1be032d9d813dbb686157803bbc:.ufo/waves/round-19/predictions/t1250-vet.prediction.json
# exit 0
sha256sum "$LANE/.ufo/waves/round-19/predictions/t1250-vet.prediction.json"
git -C "$LANE" --no-optional-locks diff --stat a1140e76fffdc1be032d9d813dbb686157803bbc -- .ufo/waves/round-19/predictions/
# exit 0; diff empty
```
The frozen sums file reports the prediction digest above (`predictions/SHA256SUMS:10`, as of the freeze commit). The working prediction digest matches it.

```sh
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
sha256sum "$LANE/.ufo/waves/round-17/tools/receipt-validate.py"
git -C "$LANE" --no-optional-locks show a1140e76fffdc1be032d9d813dbb686157803bbc:.ufo/waves/round-17/tools/receipt-validate.py | sha256sum
# exit 0
```
```sh
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
cd "$LANE"
sha256sum .ufo/waves/round-18/tools/swiss-misread.py .ufo/waves/round-17/tools/carrier-run.py .ufo/waves/round-17/tools/pins.py .ufo/waves/round-17/tools/log-extract.py .ufo/waves/round-17/tools/compare.py .ufo/waves/round-16/selection.py
# exit 0
```
Observed current validator digest `6afb7ef6…ac2c762`; frozen validator digest `70672eb3…2553d145`, matching the run’s historical pin.