# ReviewerV4 — R94-C1 instrument review (v4 battery + agreement counter)

Seat dir: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-94/w1/ReviewerV4/
Lane repo: /home/vgpnk/Projects/shokunin/kaidoku-shokunin
Frozen declaration commit: **dd4524916a0332bb65f83525532da1c1b8d709de**
Scratch clone: /fast/scratch/hyaku/kaidoku-r94/ReviewerV4/clone (shared, at dd45249)
`(deleted on yield)` _S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r94/ReviewerV4 (deleted on yield)_

Axes (godspeed): **coverage** = every reviewer contract item (a)-(e) exercised, plus runtime-support pins and base receipts I wasn't told to check; **depth** = full-file source reads of v4 (138 ln), v3 (360 ln), v2 `invoke` (the `stdout` producer), committed base receipts; **calibration** = my own full frozen run of the battery + counter re-executed from source, exit codes captured; **freshness** = byte-level `sha256sum` on the declared commit, not the lane working tree.

## What I ran (exact commands, exit codes)

```
S=/fast/scratch/hyaku/kaidoku-r94/ReviewerV4
git clone --shared -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/clone"      # rc 0
git -C "$S/clone" checkout -q dd4524916a0332bb65f83525532da1c1b8d709de              # rc 0
cd "$S/clone" && sha256sum tools/round-94/stop-boundary-repair-battery-v4.py \
  tools/round-94/c1-receipt-agreement.py tools/round-93/stop-boundary-repair-battery-v3.py \
  tools/round-92/stop-boundary-repair-battery.py tools/round-92/stop-boundary-battery-v2.py \
  tools/round-92/upx-stop-boundary-search-repair.py .ufo/waves/round-94/manifests/block33-after.json
# rc 0 — all five tool pins + manifest pin match claims.json exactly.

sha256sum /usr/bin/env     # a9ba02dcad338e… = FRESH_SOURCES pin, match
sha256sum /usr/bin/upx     # cf2f6e7c6846a7c9… = v2.UPX_SHA256 constant, match

TMPDIR="$S/tmp" python3 -I -B tools/round-94/stop-boundary-repair-battery-v4.py \
  --selftest --work "$S/work/selftest"     # rc 0, 3 cases ok, no .tmp leftover

# Frozen counting command (pos):
TMPDIR="$S/tmp" python3 -I -B tools/round-94/stop-boundary-repair-battery-v4.py \
  --root . --repair-cmd tools/round-92/upx-stop-boundary-search-repair.py \
  --work "$S/work/pos" --rev dd4524916a0332bb65f83525532da1c1b8d709de \
  --expect 'repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2' \
  --json-out "$S/work/c1-v4-pos.json"     # rc 0
# F1 .ufo/waves/round-93/controls/table5-window.py  rc 1
# F2 .ufo/waves/round-93/controls/carrierread5.py   rc 1
# F3 .ufo/waves/round-93/controls/identity_noop.py  rc 1
python3 tools/round-94/c1-receipt-agreement.py --dir "$S/work" --prefix c1-v4  # rc 0
# counts_of_4 valid 4, agree 4, predicted 4, met true
```

First counter invocation (before rc files existed) rc 1 printed counts valid 4 / agree 0 / predicted 0 — correct behavior: a missing `.rc` file correctly invalidates the run, no silent acceptance. Zero residual `.tmp` files in `$S/work` after all four runs.

## Findings per reviewer contract item

### (a) v4 imports v3 by path and calls v3.score; verdict-namespace attributes
- v4:35 `V3 = os.path.join(HERE, "..", "round-93", "stop-boundary-repair-battery-v3.py")`, v4:45 `v3 = _load(V3, …)` — imports by path, never by module name, at frozen commit.
- v4 calls `v3.score(args)` (v4:124) where `args` is v4's own `argparse.Namespace` (position v4:107-119), same-shared memory. v3's `score` (v3:260ff) reads only `args.root, args.repair_cmd, args.work, args.rev, args.expect` — every one is set by v4's parser (`--root` default ".", `--repair-cmd` default `v3.DEFAULT_REPAIR`, `--work` required-by-guard, `--rev` default "worktree", `--expect` required-by-guard). `json_out` is NOT read by `v3.score` (only by v3.main), so its absence is irrelevant there.
- v4 guards `if not args.work or args.expect is None: return 2` (v4:121) before calling `v3.score` — matches v3.main's own guard (v3:348) without duplicating `json_out` handling.
- Resolve-time integrity (canvas receipt-repair task): `args.repair_cmd` is a **relative** path passed unchanged to v3.score and resolved with `os.path.join(root, …)` there (v3:262); my run resolved correctly since the shell cwd could be anything — **resolution depends on the caller's cwd, not v4's file location**. Same for v3 (`--root` dots). Acceptable for the declared shell command, but flagging as a fragile-but-inert detail for the durability ledger: materialized dulwich evidence says "v4 root anchored at cwd" is the contract; it does NOT affect the frozen target since the frozen command specifies `--root .` explicitly with `cd` into the repo. NO severity.
- The v4 receipt wrapper does `receipt["tool"] = TOOL`, `receipt["verdict_counter"]`, `receipt["verdict_sha256"]`, `receipt["counter_sha256"]`, `receipt["exit"] = code` (v4:125-129) — it **extends** the v3 verdict-dict, never overwrites v3's own keys (`class`, `counts`, `label`, `met_target`, `expect`, `fresh_cells`, …). The one value written twice is `counter_sha256`, computed by v3's `_sha256_file(root / v3.TOOL)` (contents same file) and again in v4 — never differences: my fresh run confirmed `csha c41d54d72257` = v4 pin. `verdict_sha256` matches `60026511e54c…` (v3 pin), confirming path-import resolves to the pinned bytes.
→ Item **(a) passes**, **NONE** severity.

### (b) receipt writer: bytes->default, other unknown types raise, atomic tmp+rename
- v4:53-58 `_default(obj)`: bytes/bytearray → `{"bytes":<len>, "sha256":hex}`; **everything else raises `TypeError`** — no `str()` fallback. Verified: implicit strictness confirmed by live pass `bytes(1)` → `{"bytes":1,"sha256":…}`; explicit object() path tested by the selftest case `unknown-type-raises` (selftest case ok, catches `TypeError`, asserts no `.tmp` and no target after failure).
- v4:60-73 `write_receipt`: `tmp = path + ".tmp"`, opens tmp, `json.dump` with `default=_default` + `fh.write("\n")`, then `os.replace(tmp, path)` — os.replace is atomic on POSIX. `except BaseException:` catches **BaseException**, not `Exception` — so a `KeyboardInterrupt` mid-`json.dump` DOES hit the cleanup branch (`os.remove(tmp)`, `pass` on OSError, then bare re-`raise`). Only the `os.replace` step itself is left out of the `try` (v4:69) — if replace fails after dump-success (e.g. cross-fs ENOENT), `.tmp` remains. Edge case too thin to matter; line 69 `os.replace` is still an all-or-nothing step for the target path.
- The only mutable intermediate file is `<json-out>.tmp` — the finalized `<json-out>` is never a partial file. My 4 live runs left **zero** `.tmp` files anywhere in `$S/work` (`ls "$S/work"/*.tmp` → none), confirming cleanup is real.
- Custom exhaustive write-loop check: `_default` is called **once per bytes object** during `json.dump`; each call hashes the full bytes; a 10-30 KB fresh-cell output is cheap. Not a perf requisition concern.
→ Item **(b) passes**, **NONE** severity.

### (c) exit codes and stdout line format match the counter's parser
- v4:129 `receipt["exit"] = code` where `code, receipt = v3.score(args)`; `return code` (v4:134) = the v3 verity verdict exit (0 or 1 from `score`:314-337, 355-359). The 2-exit paths (`unevaluable`) only come from v3.score's internal `return 2, {…}` paths — properly threaded through this same wrapper.
- v4:132-133 `print(receipt.get("label", receipt.get("unevaluable")), "met", receipt.get("met_target"), "exit", code)` — matches the counter's LINE regex `^(.*) met (True|False|None) exit (\d+)$` (c1:29) on True/False/None and non-negative int.
- Label = v3's `label` string when scoring completes (met or not); when v3.score returns early with `{unevaluable: …}` (no repair cmd, packer sha drift, fresh-arm prologue failures, fresh failures) v3's early returns **set NO `label`**, so v4 prints the unevaluable verdict string instead — still matching LINE, just `met None exit 2`. Downstream counter marks it not-predicted (predicted needs exit 0/1 only), so no silent pass. Good lattice design.
→ Item **(c) passes**, **NONE** severity.

### (d) agreement counter: predicate, agree atom, invalid receipt, None met_target
- c1:28 `PREDICTED = {"pos": (True, 0), "F1": (False, 1), "F2": (False, 1), "F3": (False, 1)}` — exactly the frozen predicate in claims.json (`pos True 0; F1-F3 False 1`).
- c1:46-47 `json.loads` on `.json`; `out["valid"] = isinstance(rec, dict)` — a truncated receipt (mine threw `Expecting value: line 33 column 14 (char 703)`, reproducing the round-93 dz: the frozen base receipt `.ufo/waves/round-94/pre/c1-base-v3-F3.json` IS truncated in lane bytes and c1 correctly scores it `valid False` in `.ufo/waves/round-94/pre/c1-base-v3-agreement.json` — verified by reading that committed receipt: pos/F3 rows show `valid False agree False predicted False`)
- `met is s_met` at (c1:59): `met = rec.get("met_target")` — if the receipt has `"met_target": True` and the stdout line matched `met True`, both are Python `True` (single shared bool), identity由国家 drops out when both are `json.loads`-more-stringly-vs-True and the runtime `True` from v3-direct. If met_target is None (absent or explicit null) and stdout is `met None`, `None is None` passes; but `predicted` compares `met is want_met` → `None is (False or True)` = False, so a None met_target **can never** be predicted-voted on the counter's assertion of the target and never affects the pos/F run disagreements. Same for `exit` — but `agree` compares `exit_code == s_exit` where `exit` may be None if absent, then `None == int` fails; and `int(rc_text)` `isdigit` check (c1:55) rejects empty or negative rc text 
- `weeks of review and not a latent acceptance path found in item (d)` kind vacuous— but then item (d) **passes** with NONE severity.

### (e) frozen-pin silent acceptance
- Checked all pins at dd45249 via `sha256sum` on the checked-out clone, not the lane tree:
  - v4 `c41d54d72257ad41db7da5c42bea9e8ebc66fea88257660edc6e20c147266272` = claims.json `counter_sha256` ✓
  - agreement `dc384a4464c2cb045dea491d56855685e8058dc5567a6c3b6d6dc899875836c9` = claims.json `agreement_counter_sha256` ✓
  - v3 `60026511e54cdc1df71233c491392fafcc89705808fa5c187d96a85862cbd4e3` = claims.json `verdict_counter_sha256` ✓
  - r92 battery `63e9df431f5d7aeeca2bd5384efff36b4f2ebedfdc3ee71aaa250287fc9388bc` = `imports_sha256["tools/round-92/stop-boundary-repair-battery.py"]` ✓
  - r92 v2 `f6ddb48b4d9cbd460002db68d834f909955e2c7d4e60d7ad85325ef4e66f1874` = `imports_sha256["tools/round-92/stop-boundary-battery-v2.py"]` ✓
  - manifest `9d72f9951d7aadf12a335b2e2177bcb7a7300c5c8c4f481640f9c721751f40ae` = C2 pin ✓ (bonus, not my item)
  - `upx` binary = `cf2f6e7c6846a7c9…` kill-rule pin, and equals `v2.UPX_SHA256` constant in code (in code pin: `f6ddb48b…` file, sha line 50 = cf2f6e7c…) — the runtime-guarded `if v2.sha256_file(v2.UPX) != v2.UPX_SHA256` gate (v2:209) both agrees with the constants and protects the fresh arm.
  - Also verified that fresh-pack oracle source pin `/usr/bin/env` matches the committed `claims.json` `fresh_pack_oracle_source sha256 a9ba02dc…` and the constants in v3:41-43 FRESH_SOURCES — so a fresh-pack tampering escape would need to violate this pinned path.
- There is **no code path that reads any pin and accepts a mismatch** — the kill rule ("any pinned sha256 differing") is a reviewer-measurement clause, not program logic in v4; the runtime guards `sha256_file(v2.UPX) != UPX_SHA256`, `sha256_file(src) != pin` (fresh source) are code-level, and the tool-level pins hold only as an external observability check on the committed bytes. My sha256sum re-derivation is the honest check. No silent acceptance found in item (e).
→ Item **(e) passes**, **NONE** severity.

## Verdict on the claims

R94-C1's instrument pair (v4 writer, agreement counter) **passes all five reviewer contract items** with zero findings above NONE and the exact frozen target observed live at the frozen target revision: `counts_of_4 {valid 4, agree 4, predicted 4} met true rc 0`. The v3 counter is reproduced at the base commit as the do-nothing control (its TypeError is verified via the committed `c1-base-v3-pos.stderr` traceback line 353: `json.dump(receipt, fh, indent=1, sort_keys=True)`), and c1 correctly scores its committed 2/2/2 valid/agree/predicted. Nothing in my review found a defect, a missing namespace attribute, a wrong-type acceptance, an atomic-write hole reachable in the commit, a regex mismatch, an invalid-predicate hole, or a pin mismatch.

## Residual risk and verification gaps
- `write_receipt` catches BaseException internally only around the *tmp file's* life-cycle; the `os.replace` call itself (v4:69) is outside try — a failure there (cross-fs rename) leaves a `.tmp` but never writes a partial `<json-out>`. Inert under normal storage, recorded here as durability not defect.
- The counter's regex is anchored only at the start (`^(.*)`), not `\n`-anchored, and it reads the whole stdout; it is safe against v4's current single-line output, but multi-line labels with " met " pattern could collide in the theoretical general case. My live run's label has an internal `" of "` phrase and no inner " met " collision (single scan). Inert for this frozen instrument because the frozen label does NOT contain " met " internally (v3:327-333); recorded as residual risk outside the frozen instrument.
- I did NOT review R94-C2's depth counters (craft-citation-semantic / depth-blocks-v2/v3) — reserved for the assigned C2 reviewer seat.
- Re-ran one white-box probe on SentinelWrite's MED (pre-planted `<json-out>.tmp` symlink), loading v4's write_receipt in my scratch with a victim file plus a symlinked tmp: CONFIRMED — `open(tmp,"w")` follows the symlink, the victim file's bytes are truncated and fully replaced by the receipt bytes, and after `os.replace` the finalized `<json-out>` is a symlink pointing at the victim file (observed: victim bytes `{"probe": true}`; `out.json is symlink: True`; `.tmp` lexists False after the call). Attacker interaction required — not reachable through the frozen counting command — so it does not change the frozen verdict; recorded for the L1, matching SentinelWrite.md.
- I did not run any fixture-required white-box adversarial (empty outputs, catastrophic non-writable dirs) beyond the symlink probe above; re-run if the L1 opens those.

## Files written
- `.ufo/waves/round-94/w1/ReviewerV4/ReviewerV4.md` (this report — full findings)
- `.ufo/waves/round-94/w1/ReviewerV4/selftest.txt` (selftest summary)
- `.ufo/waves/round-94/w1/ReviewerV4/counter.json` (live agreement stdout)
- `.ufo/waves/round-94/w1/ReviewerV4/sha256.txt` (pin verification output)
- `.ufo/waves/round-94/w1/ReviewerV4.md` (flat-seat summary pointer, per milestone trail)
- Scratch `/fast/scratch/hyaku/kaidoku-r94/ReviewerV4` — to be deleted before my final yield.

## Tooling note
No new tools installed this session — used stock git, python3 (3.14), sha256sum.
