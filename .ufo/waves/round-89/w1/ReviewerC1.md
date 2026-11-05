# ReviewerC1 — scoped findings (R89-C1)

Full evidence and pointers: `.ufo/waves/round-89/w1/ReviewerC1/report.md`. Receipts: `.ufo/waves/round-89/w1/ReviewerC1/receipts/`.

## Reproduction
- Frozen predicate at declared repair bytes `332917f2…`: `recovered 4 of 4 … met=True exit=0` (`receipts/c1-repro.json`).
- Current worktree bytes `664b973a…` (L1 revision, mtime 22:09:10): `recovered 4 of 4 … met=True exit=0` (`receipts/c1-current-worktree.json`).
- Pins re-hashed against committed HEAD blobs: all match `claims.json` except the repair, which is `664b973a…` on disk versus `332917f2…` at HEAD and in the container.

## Cheap rules (same counter)
| Rule | Label | met · exit | Stops at |
|---|---|---|---|
| M88-8 sibling copy | 0 of 4 | F · 1 | N3 false; box refuses (`no packed sibling`) |
| Packer oracle ±32, r87 locator | 4 of 4 | F · 1 | regression 0 of 4 |
| Packer oracle full range, r87 locator | 4 of 4 | F · 1 | regression 0 of 4 |
| Packer oracle full range, r88 candidate locator | 4 of 4 | **T · 0** | survivor |
| `stored + 8` | 4 of 4 | F · 1 | N3 false |
| `stored`-reading hybrid gated by `upx -t` | 4 of 4 | **T · 0** | survivor |
| `u_len` arithmetic | 0 of 4 | F · 1 | test_ok, identity, rea false |

## Defects
- **D1 high, isolation.** `tools/round-89/upx-field-battery.py:180` snapshots the box before invocation only; `:288`, `:369` judge on that. A carrier read of `/usr/bin/jq` (52 reads) plus a box write scored `met=True`.
- **D2 high, pin not enforced.** `tools/round-89/upx-field-battery.py:270` records `repair_sha256`; nothing compares it to `332917f2…`. Self-mutation probe shows the recorded pin is pre-run.
- **D3 medium, module pins not checked.** `tools/round-89/upx-field-battery.py:246-250`; repair `upx-field-value-repair.py:112-113`, `:125-126`.
- **D4 high, depth.** The counter does not test the chain-geometry derivation or stored-value blindness; the stored-reading hybrid and the r88-locator oracle both meet the predicate.
- **D5 calibration.** Population tamper is a single offset (`-8`): `tools/round-89/upx-field-battery.py:124-129`; every receipt delta is `-8`.
- **D6 medium.** The repair reads the stored value to classify (`upx-field-value-repair.py:147`, `:153`), contrary to the claim's wording.
- **D7 high, governance.** Repair changed mid-round without a container supersession; `claims.json` line 56 still pins `332917f2…`; no repair entry in `instrument_supersessions` (line 71 is depth-only). Under the frozen kill rule's pin clause the claim is killed at `664b973a…` until the supersession is recorded before the verdict.

## Field-only binding
Verified: a one-byte flip at `e_ident[9]` outside the `sz_cpr` window is refused by `field_only` alone (`tools/round-89/upx-field-battery.py:138`).

## Verification gaps
L1's three repair defects (traceback, FIFO, `/dev/zero`) not independently reproduced. R89-C2 not in scope. Full-oracle cost at real block sizes not measured.
