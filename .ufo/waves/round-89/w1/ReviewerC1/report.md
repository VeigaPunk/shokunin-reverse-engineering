# ReviewerC1 — R89-C1 attack report (round 89, kaidoku, lane `kaidoku-shokunin`)

Scope: attack R89-C1 (coverage/capability, `b_info.sz_cpr` wrong-value class). R89-C2 was not in this seat's assignment; not judged here.
Axes named: coverage (does the frozen predicate reproduce), depth (does the counter test the derivation or only the bytes), calibration (do cheap rules score 4/4 and fail for the right reason).
Receipts: `receipts/` in this seat dir. Cheat sources with `SHA256SUMS`: `receipts/attacks/`. REA evidence: `receipts/rea/`.
Scratch `/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/` deleted before yield.

## Bottom line

1. **The frozen predicate reproduces at the declared repair bytes** (`332917f2…`): `recovered 4 of 4`, all four controls true, regression arm met, exit 0.
2. **The repair bytes changed mid-round, and the frozen kill rule's pin clause fires on the new bytes.** `tools/round-89/upx-field-value-repair.py` is `664b973a…` on disk and in the working tree (mtime 22:09:10, after my reproduction began). Committed HEAD and the index hold `332917f2…`. `claims.json` (committed `4ab027b27`, clean) still pins `332917f2…` at line 56. Its only `instrument_supersessions` entry (line 71) covers the depth counter. No repair supersession is recorded. The L1 states one is intended; it is not in the container. The `664b973a…` arm also meets the predicate (`recovered 4 of 4`, all controls true, regression met, exit 0), so the outcome holds at either byte set. The kill rule's pin clause does not.
3. **The counter certifies outcome bytes, not the derivation.** Two repairs that do not implement the chain-geometry law meet the entire frozen predicate with exit 0: a hybrid that reads the stored value and is gated by `upx -t`, and a brute-force packer oracle that uses the round-88 candidate locator. The "stored-value blind" and "chain-geometry" statements in the claim are untested by any arm.
4. **The kill rule has three unenforced clauses.** The isolation control records a pre-invocation listing only, so a repair that reads the pinned carrier `/usr/bin/jq` and writes into its box scores `met=True` (52 logged reads). The `repair_sha256` pin is recorded but never compared. The composed R87/R88 module pins are recorded but never compared.
5. **`field_only` binds correctly.** A one-byte flip outside the `sz_cpr` window is refused by `field_only` alone; the other four arms stay true.
6. **Calibration is weak.** Every tamper in the population has delta `-8` (receipt `c1-repro.json`, `cases[].tamper.delta`; true values 252/249/201/226). The `+8` branch is never exercised, so `stored + 8` is correct on all four carriers by construction.

## 1. Reproduction (frozen predicate, declared bytes)

Command (exit 0):
```
python3 -I -B tools/round-89/upx-field-battery.py --root <lane> \
  --repair-cmd tools/round-89/upx-field-value-repair.py --upx /usr/bin/upx \
  --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work <scratch>/work --json-out receipts/c1-repro.json \
  --evidence-dir receipts/rea --expect-recovered 4
```
Stdout verbatim: `recovered 4 of 4 controls_ok={'N1-refuse-plain': True, 'N2-corrupt-payload': True, 'N3-intact-idempotent': True, 'isolation': True} met=True exit=0`. Process exit 0 (`BATTERY_EXIT=0`).

Arms, per carrier (all five true on jq, xxd, libz, dinit): `repair_rc0`, `field_only`, `test_ok`, `identity`, `rea_recover`. REA procedure counts 167 / 99 / 184 / 1268 match `DECLARED_ORIG`. Repair output equals the packed input byte-for-byte on all four (`repaired_equals_packed: true`).

Controls: N1 refuse-plain rc 1 on all four; N2 corrupt-payload `recovered: false` with `repair_rc: 0` on all four (flip at len//2); N3 intact idempotent `identical: true` on all four; isolation `n1_box: ["in"]` on all four.

Regression arm (round-88 counter, same repair): `recovered 4 of 4 … met=True exit=0`.

Selftests (exit 0): repair at 332917f2 `SELFTEST cases=16 failures=0`; battery `SELFTEST cases=9 failures=0`. Repair at 664b973a: `SELFTEST cases=22 failures=0`, exit 0.

### Pins (re-hashed against committed HEAD blobs via `git show HEAD:<path> | sha256sum`, read-only)

| Pin | Expected (claims.json) | Committed HEAD blob | On disk |
|---|---|---|---|
| `tools/round-89/upx-field-value-repair.py` | 332917f2…070 | 332917f2…070 ✔ | **664b973a…2285c37 ✘ (changed 22:09:10)** |
| `tools/round-89/upx-field-battery.py` | f6f5ed61…720 | f6f5ed61…720 ✔ | f6f5ed61…720 ✔ |
| `tools/round-89/depth-blocks-v2.py` | 359f15e1…dcf18f | 359f15e1…dcf18f ✔ | 359f15e1…dcf18f ✔ |
| `tools/round-88/upx-chain-battery.py` | a01ed622…160 | a01ed622…160 ✔ | a01ed622…160 ✔ |
| `tools/round-88/upx-chain-repair.py` | 59ee51b0…b46 | 59ee51b0…b46 ✔ | 59ee51b0…b46 ✔ |
| `tools/round-87/upx-magic-repair.py` | 96da7d8e…4 | 96da7d8e…4 ✔ | 96da7d8e…4 ✔ |
| `/usr/bin/upx` | cf2f6e7c…969 | — | cf2f6e7c…969 ✔ |
| REA `package.json` | a5003023…6a | — | a5003023…6a ✔ |
| carrier jq | e8156675…806 | — | e8156675…806 ✔ |
| carrier xxd | 7b1e5d0c…e65 | — | 7b1e5d0c…e65 ✔ |
| carrier libz.so.1.3.2 | 6c78c5e5…ca9 | — | 6c78c5e5…ca9 ✔ |
| carrier docker-init | 0bd49c8d…115 | — | 0bd49c8d…115 ✔ |

Note: the seat brief named the repair pin `048e2c8e…`. No committed artifact carries that value. `claims.json` and the plan both say `332917f2…`, which matches HEAD. I used `332917f2…`.

Repair receipt pins: `c1-repro.json` `repair_sha256 332917f2…`; `c1-current-worktree.json` `repair_sha256 664b973a…`.

### Reproduction at the current bytes (superseded-candidate arm)

Same command, `--json-out receipts/c1-current-worktree.json`. Stdout verbatim: `recovered 4 of 4 controls_ok={'N1-refuse-plain': True, 'N2-corrupt-payload': True, 'N3-intact-idempotent': True, 'isolation': True} met=True exit=0`. Process exit 0 (`CUR_BATTERY_EXIT=0`, wall 190.9 s). Regression arm met, 4 of 4, rc 0.

Arm provenance: `cheat-field-flip.py` and `cheat-carrier-read.py` load the frozen repair from the lane path; both ran at ~21:54, before the 22:09 change, so they exercised `332917f2…`. The other cheats do not load the repair file.

Pre-freeze receipts (read, not rerun): `pre/c1-base-r88-repair.json` `recovered 0 of 4`, controls N1/N2/N3/isolation all true, exit 1. `pre/c1-control-identity.json` and `pre/c1-control-naive.json`: `N1-refuse-plain: false`, exit 1. These match the declared red arms.

## 2. Cheap-rule table (same frozen counter, same population)

Rules run as `--repair-cmd` scripts under the frozen battery. "met" is the frozen `met_target`; the failing-arm column names what stopped it.

| # | Rule (source in `receipts/attacks/`) | Label | N1 / N2 / N3 / iso | Regression (r88) | met · exit | Failing arm and verbatim evidence |
|---|---|---|---|---|---|---|
| a | **M88-8 sibling copy** (`cheat-sibling.py`) | recovered 0 of 4 | T / T / **F** / T | 0 of 4 | F · 1 | `repair_rc0: rc 3 ['refused: no packed sibling in the input directory']`. Isolation is *true*: the isolated box holds only `in`, so there is nothing to copy. The box defeats the cheat; N3 flags it. Isolation did not detect it. |
| b1 | **Packer oracle, ±32 window, r87 anchor** (`cheat-oracle.py`) | recovered 4 of 4 | T / T / T / T | **0 of 4** | F · 1 | Regression fails: the r88 zeroed class leaves `find_linfo` refusing. Oracle meets T4 only. |
| b2 | **Packer oracle, full range [1, sz_unc0], r87 locator** (`cheat-oracle-full.py`) | recovered 4 of 4 | T / T / T / T | **0 of 4** | F · 1 | Regression: same locator refusal. Direct probe on zeroed jq: `refused: p_info is not followed by a plausible b_info` (exit 3). |
| b3 | **Packer oracle, full range, r88 candidate locator** (`cheat-oracle-full2.py`) | recovered 4 of 4 | T / T / T / T | 4 of 4 | **T · 0** | **Survivor.** No chain geometry, no u_len accounting, no stored-value read in the value search. Direct probe: zeroed-class jq repaired in 0.55 s, output `cmp`-identical to the clean packed file. |
| c1 | **`stored + 8`, blind** (`cheat-plus8.py`) | recovered 4 of 4 | T / T / **F** / T | 0 of 4 | F · 1 | N3 false: an intact file is corrupted. The class is `stored − 8` on every carrier, so `+8` is the correct value on the population by construction. |
| c2 | **Stored-reading hybrid, `upx -t`-gated** (`cheat-hybrid.py`): identity if `upx -t` accepts; else try `stored+8`, `stored−8` gated by `upx -t`; else delegate to r88 | recovered 4 of 4 | T / T / T / T | 4 of 4 | **T · 0** | **Survivor.** Reads `stored`, violates the declared stored-value-blind law, meets the full predicate. The counter cannot tell it apart from the derivation. |
| d | **`u_len` arithmetic** `ph_off − (b0+12)` (`cheat-arith.py`) | recovered 0 of 4 | T / T / **F** / T | 0 of 4 | F · 1 | `test_ok: rc 1 [... compressed data violation]`, `identity: rc 1 sha None`, `rea_recover` skipped. |
| e | **Self-mutating repair** (`cheat-selfmutate.py`, appends to its own source) | recovered 4 of 4 | T / T / **F** / T | 0 of 4 | F · 1 | Met only through N3. Receipt `repair_sha256 0f62e088…` is the pre-run hash; the archived file, which is post-run, is `f6b2027b…`. The pin does not bind the bytes that ran. |
| f | **Field flip outside window** (`cheat-field-flip.py`: frozen repair, then `e_ident[9] ^= 1`) | recovered 0 of 4 | T / T / F / T | — | F · 1 | `field_only: byte 9 changed outside the sz_cpr window 580-584` (jq, xxd, dinit); `…9308-9312` (libz). The other four arms are true on all four carriers. `field_only` is the sole binding arm. |
| g | **Carrier read** (`cheat-carrier-read.py`: frozen repair plus `open('/usr/bin/jq')` + sha256 each call, plus write `carrier-read.marker` into the invocation box) | recovered 4 of 4 | T / T / T / T | 4 of 4 | **T · 0** | **Survivor.** `markers/carrier-read.log`: 52 `read /usr/bin/jq sha256=e815667…806` lines. The box write goes undetected (D1). |
| ref | Identity / naive-global (pre-freeze) | recovered 0 of 4 | **F** / T / T / T | 0 | F · 1 | Pre-freeze controls, read not rerun. |

Survivors (met=True, exit 0): **b3** (r88-locator full-range oracle), **c2** (stored-reading gated hybrid), **g** (carrier-read probe). Plus the frozen repair itself, at both byte sets.

Interpretation. Survivors b3 and c2 both reach the predicate's outcome by a route the claim excludes (a stored-value read, the locator). The claim is a capability claim, so an alternative route to the same bytes is not itself a cheat. But the claim also states the derivation law, and the counter does not test it. Survivor g is a kill-rule hole: the counter cannot see a non-input read.

## 3. Attacks on the kill rule

**Does `field_only` bind the changed byte to the window?** Yes, verified by probe f. The check is `field_only` at `tools/round-89/upx-field-battery.py:138` (`lo, hi = b0 + 4, b0 + 8`; every differing index must lie in `[lo, hi)`), and it fires alone.

**Can a repair score 4 of 4 while naming, reading or hashing a carrier path or pin?** Yes: survivor g. The repair reads `/usr/bin/jq` and hashes it on every call, then scores `met=True exit=0`. The counter's only isolation evidence is a listing taken before invocation (D1).

**Does the receipt pin the repair bytes?** No. `repair_sha256` is recorded (battery `:270`) and never compared to any pin. Nothing in `tools/round-89/` compares the value to `332917f2…`. The composed R87/R88 module hashes are returned in `preflight` (`:246-250`) and recorded, never compared to `claims.json`. Probe e shows the pin records a pre-run hash, not the post-run bytes.

**Does the isolation control catch the sibling cheat?** No. Probe a is refused because the box has nothing to copy. The isolation control is true for a. It is a precondition, and it cannot flag a cheat that refuses on its own.

**Does the regression arm discriminate?** Partly. It rejects every locator-dependent repair (b1, b2 score 0 of 4). It does not reject a repair that uses the r88 candidate locator (b3) or a stored-reading gate (c2), because those reach the same bytes on the zeroed class.

## 4. Defects (with file:line)

Line numbers are for the files as named. `upx-field-battery.py` is the frozen `f6f5ed61…` version. `upx-field-value-repair.py` at HEAD (`332917f2…`) and at the current `664b973a…` version carry the same statements at the same lines for every pointer below.

**D1 — high, kill-rule gap (isolation).** `tools/round-89/upx-field-battery.py:180` takes `before = sorted(os.listdir(box))` before the invocation and never re-lists the box after it. `:288` and `:369` judge isolation on that pre-run snapshot. Probe g wrote `carrier-read.marker` into the box and read `/usr/bin/jq` 52 times; isolation stayed true and `met=True`. The docstring (`upx-field-battery.py:26-29`) says the receipt "records the directory listing each invocation saw"; the code records only the pre-run listing. The kill rule's "a repair invocation that saw anything but its single input file" is not what is measured. The r88 counter names this limit (`tools/round-88/upx-chain-battery.py:52-53`: "the counter scores bytes, not provenance"); the r89 counter does not carry it forward.

**D2 — high, kill-rule gap (repair pin not enforced).** `tools/round-89/upx-field-battery.py:270` computes `repair_sha = sha256_file(repair)` once, before the case loop. No comparison to `332917f2…` exists anywhere in the counter. The kill-rule clause "receipt's `repair_sha256` differs from the frozen pin" is therefore not enforced by the counter, and the bytes that run are not re-hashed after the run (probe e).

**D3 — medium, pins recorded but not checked.** `tools/round-89/upx-field-battery.py:246-250` returns `r87_module_sha256`, `r88_module_sha256`, `r88_counter_sha256` without comparing them to `claims.json` (`96da7d8e…`, `59ee51b0…`, `a01ed622…`). The repair records the same digests at `upx-field-value-repair.py:112-113` and `:125-126` (`digest87`, `digest88`), also uncompared. A change to the composed R87 or R88 modules runs silently.

**D4 — high, depth: the counter does not test the derivation or stored-blindness.** Survivors b3 and c2 meet the full predicate. The claim's "stored-value blind" law and "chain-geometry" derivation are not an arm.

**D5 — calibration: population has one tamper offset.** `tools/round-89/upx-field-battery.py:124-129` (`tamper_field`) uses `wrong = sz_cpr - 8` (or `+8`, `:129`). Every receipt shows delta `-8`. Any repair that tries `stored ± 8` (c1, c2) reaches the true value on the population. The `+8` branch is never exercised. This lets cheap local-search rules score 4/4 on the class.

**D6 — medium, the repair reads the stored value for its classification.** `upx-field-value-repair.py:147` `if info["stored_sz_cpr"] == derived:` and `:153` `info["class"] = "chain-geometry" if info["stored_sz_cpr"] == 0 else "field-value"` (same lines at HEAD `332917f2…`). The claim says "the round-89 repair never reads the stored value". The derivation (`derive`, `:68`; stored unpacked at `:76`, recorded only; key `(total <= u_len, total, -derived)` at `:100`) is stored-blind. The output bytes are stored-blind in effect (both branches write the same bytes). The classification is not, and the claim's wording overstates it.

**D7 — high, governance: instrument change mid-round without a supersession.** `tools/round-89/upx-field-value-repair.py` changed on disk at 22:09:10 (`664b973a…`, 13654 B) after my reproduction began. `git status --porcelain` shows ` M` on it. Read-only `git diff` shows the change: new `tempfile` and `stat` imports, a `repair()` wrapper that converts upstream `Refused` (its docstring), and docstring changes. Committed HEAD and the index hold `332917f2…`. HEAD moved `8bbb40cc` → `1cacbf7bd` during the session. `claims.json` (committed `4ab027b27`, clean) has no repair supersession entry. The L1 states the revision was made on purpose to fix three defects (an unconverted `Refused` traceback giving rc 1, a FIFO `--in` blocking, `/dev/zero` raising `MemoryError`) and that it is recorded as an `instrument_supersessions` entry with a re-taken before record. I did not verify those three defects. The kill rule says "receipt's `repair_sha256` differs from the frozen pin", so the claim is killed on that clause at `664b973a…` until the supersession is recorded before the verdict. At `664b973a…` the claim's outcome arms all hold (§1).

**D8 — low, input discrepancy (not a lane defect).** The seat brief gave the repair pin as `048e2c8e…`. No artifact carries it; the committed and claimed pin is `332917f2…`.

**D9 — low, docstring vs code.** `upx-field-value-repair.py:69` (`derive` docstring) says "the stored value taken out of the gate"; the classifier at `:147` and `:153` reads it back. Same substance as D6; listed for the docstring.

## 5. Verification gaps and limits

- Not verified: the L1's three repair defects (traceback, FIFO, `/dev/zero`). I read the L1 message and did not reproduce them.
- Not measured: cost of the full-range oracle (b3) on large blocks. It is O(sz_unc0) `upx -t` calls (~4 ms each on these carriers). Cost at real block sizes is untested.
- Not run: R89-C2 (depth). Out of this seat's assignment.
- Survivors b3, c2 and g are my probes; I did not modify the lane or the frozen counter.

## 6. Tooling

No tools installed or upgraded. Used existing `/usr/bin/upx` (5.2.0, pinned), `node` (REA 6.5.0), `python3`, `git` (read-only). No pacman. No writes outside the seat dir and scratch (deleted).

## 7. Recommendations (for the L1)

1. Record the repair supersession in `claims.json` (`instrument_supersessions`) with the `664b973a…` sha and a before record, before any verdict. Until then the frozen pin clause is live and fires.
2. Either narrow R89-C1's label to outcome recovery ("bytes equal the pinned carriers under upx -t and REA"), or add a stored-blind arm: a second wrong value outside `±8` (e.g. `stored + 37`, in range) must produce the same bytes. Probes c2 and b1 fail that arm. b3 passes it, so it must be cost-bounded or accepted as an outcome-equivalent route.
3. Fix the counter's isolation: re-list the box after each invocation (`upx-field-battery.py:180`, consumers at `:288` and `:369`) and record the post-run listing. A box listing cannot see carrier reads; the kill rule should say so, or the counter should run the repair under a read-restricted sandbox.
4. Enforce the pins: compare the post-run `repair_sha256` to the frozen pin (`:270`); compare the R87/R88 module shas to `claims.json` in `preflight` (`:246-250`).
5. Add a second tamper offset (or a `+8` carrier) to the population, so local-search rules cannot reach 4/4 on a single delta.
6. Correct the stored-value wording in the repair (`:147`, `:153`) or the claim.
