# ReviewerRepair — round 87, R87-C1 review (read-only)

Reviewed at `b5c7a49e20647bb73117ed1ffb4f68dd69916cd8`:
- `tools/round-87/upx-magic-repair.py` sha256 `f4ebd152…9723` (matches the frozen pin; the working tree is identical)
- `tools/round-87/upx-tamper-battery.py` sha256 `0f2d2bd8…4b0` (matches `claims.json`; the working tree is identical)
- `plans/round-87-claims.md` (frozen)

LSP: not used. Both files are Python scripts with no cross-file callers, so references were checked by reading them in full. Nothing below depends on a semantic index.

## Verdict: **sound-with-limits**

The repair meets the kill-rule provenance clause, and every counter arm computes what the frozen predicate sentence says. All non-REA arms pass 8/8 and all three controls hold. REA on jq's restored bytes reports 167. Nothing I found lets a case be recovered falsely. The limits are about calibration and scope (F1–F3), not correctness.

## Evidence (this seat)

| Item | Result |
|---|---|
| `counter-norea.json` (counter `--no-rea`, committed repair, scratch `--work`) | `repair_rc0`, `windows_only`, `test_ok` and `identity` true in **8/8** cases. `rea_recover` is false in all cases only because REA was disabled (`--no-rea`), so the receipt reads `recovered 0 of 8`, exit 1, as designed. Controls: N1 4/4 refused (rc 2), N2 0/4 recovered, N3 4/4 identical. `tool_sha256 0f2d2bd8…`, `repair_sha256 f4ebd152…` |
| `rea-jq-restored.json` | jq T1-zero → repair → `upx -t` OK → `upx -d` gives sha256 `e8156675…7806` (the pin) → REA 6.5.0 analyze rc 0: `procedure_count 167` (declared 167), segments 30, strings 190, evidence_id `ev_14f9d92f…d328`. REA `package.json` sha256 matches the pin |
| Selftests | counter `SELFTEST cases=8 failures=0`; repair `SELFTEST cases=9 failures=0` |
| `probe-out-of-population.txt` | Probe only, not a score: 24/27 ID across {jq, libz, dinit} × {--best, --lzma, -1} × {t1, ff, per-word random}. The 3 misses are libz --lzma, which the repair refuses (F2) |

## Kill-rule clause (provenance): PASS

- Imports are `argparse`, `json`, `struct` and `sys` only (repair:37-40). There is no `os`, `subprocess`, `hashlib` or `shutil`.
- The only file I/O is `open(a.inp, "rb")` (repair:225) and `open(a.out, "wb")` (repair:232). The CLI accepts only `--in`, `--out`, `--json` and `--selftest` (repair:215-218).
- No carrier path, pin or sha256 appears anywhere. The packer is never invoked; "UPX v5.2.0" appears only in the docstring.
- Anchors are found structurally: a checksum-validated PackHeader (repair:56-72), an l_info/p_info matched by `p_filesize == u_file_size` plus version/format (repair:126-142), and a b_info chain walk to the sentinel (repair:106-123). The tampered value is never used to find anything.
- Each byte the repair writes is the original value: libz/dinit repaired outputs are byte-identical to the untampered packed file (`repaired_equals_packed: true`). jq/xxd differ from it only at a word the repair never touches (F4).

## Arm and control check (counter)

| Arm / control | Lines | Computes the sentence? | Can it pass vacuously? |
|---|---|---|---|
| precondition `upx -t` ≠ 0 | 254-256 | yes (else exit 2) | no |
| `repair_rc0` | 263 | yes (rc 0 and output exists) | no |
| `windows_only` | 125-138, 271 | yes: same length; every differing byte sits in a window that now reads `UPX!` | yes, for a no-op (identity control). It limits what changes within each window, not how many windows change or where they are (F7) |
| `test_ok` | 274-277 | yes | no |
| `identity` | 278-284 | yes: `upx -d` sha256 == carrier pin | no; this is the strong arm |
| `rea_recover` | 285-292 | yes, literally | **entailed by `identity`** (F1) |
| N1 refuse-plain | 235-237, 321 | yes | counts rc `None` (timeout/OSError) as refused (F6) |
| N2 corrupt-payload | 301-318, 322 | yes | **vacuous with respect to the repair**: it holds through upx's own adler check (F3) |
| N3 intact-idempotent | 239-243, 323 | yes | passes for the do-nothing control |
| met / exit | 319-333, 379-389 | 0 met / 1 not met / 2 unevaluable | an uncaught exception also exits 1 (F5) |

T2 tamper-value absence check (248-249): correct. TARGET = 8 (87, selftest 355).

## Findings (by severity)

### F1 — MEDIUM (calibration) — the `rea_recover` arm is implied by `identity` and adds no evidence about the repair
- **Where:** counter:285-290. The arm runs only when `identity` holds (282), and `identity` means the bytes REA analyzes are byte-identical to the pinned original carrier.
- **Evidence:** REA analyzes `un`, whose sha256 equals `c["sha256"]`. So `procedure_count` depends only on the pin and REA's determinism, not on the repair. My jq run gives 167, the same number REA gives for the original pinned jq.
- **Effect:** the claim reads "REA 6.5.0 analyze of the restored bytes reports the declared original procedure count" as if it were a separate RE-level arm. In practice it checks that the REA pin is consistent. It cannot fail when `identity` holds unless REA itself drifts.
- **Suggested fix (future rounds; frozen files unchanged):** state this in the closure and the knowledge entry. For an RE-level before/after signal, add REA on the *tampered packed* file (expect the packed-stub count) next to REA on the restored bytes. The do-nothing control cannot reach the restored arm at all.

### F2 — MEDIUM (scope of the Frontier→Core move) — the repair refuses mixed-method chains (libz.so `--lzma`)
- **Where:** repair:87-90 (`walk_chain` stops when a block's method differs from the first block's) and repair:118 (the resume scan accepts only the first block's method).
- **Evidence:** `probe-out-of-population.txt`. For libz `--lzma`, block 1 uses method 0x02 (NRV2B, 680→201) and the next blocks use 0x0e (LZMA). Repair rc 2 "b_info chain does not reach an end-of-chain sentinel" for t1/ff/rnd **and for the intact packed file**. It fails safe and emits no wrong bytes. jq and dinit `--lzma` repair fine.
- **Effect:** the frozen population (`--best`) never reaches this. The Core row should be scoped to the measured population (UPX 5.2.0 amd64 ELF, NRV `--best`, also `-1` by probe), not to "UPX magic-altered ELF" in general. Shared objects packed with `--lzma` remain Frontier.
- **Suggested fix (next round):** allow the method to vary per block within the set of known UPX methods, and drop the single-method requirement in the resume scan.

### F3 — LOW (control strength) — N2 does not test the repair
- **Where:** counter:301-318.
- **Evidence:** in `counter-norea.json` the repair returns **rc 0** on all 4 corrupted inputs, and N2 holds only because `upx -t`/`-d` reject the flipped payload byte. The do-nothing and naive-global pre-receipts also have N2 true (`.ufo/waves/round-87/pre/c1-control-*-at-base.json`).
- **Effect:** N2 shows that payload corruption is never laundered. Its only power against a repair is against one that emits known-good bytes, which is the "re-pack" provenance cheat named as a limit. It is not evidence that the repair detects corruption; it does not check `c_adler`/`u_adler`.
- **Suggested fix:** describe N2 as an upx-integrity guard. Optionally, a future repair could verify the PackHeader adlers and refuse.

### F4 — LOW (wording) — jq/xxd repaired files are not byte-identical to the original packed file
- **Where:** repair restores 3 anchors (repair:150); the packed jq/xxd files contain 4 `UPX!` words.
- **Evidence:** the 4th word is the immediate of a stub instruction `81 fa 55 50 58 21` = `cmp $0x21585055,%edx` (jq offset 10971, xxd offset 16499). It stays tampered, so `repaired_equals_packed: false` for jq/xxd. The repaired and tampered jq both run (`jq-1.8.2`), and so do xxd's. The predicate does not require that word, and `upx -d` still restores the pin.
- **Effect:** "restores the `UPX!` magic words" means the three structural markers, not every word. The knowledge entry should say so.

### F5 — LOW (counter exit contract) — uncaught exceptions collide with exit 1
- **Where:** counter:111-118 (`run()` catches only OSError/TimeoutExpired, with `text=True` decoding) and 379-384 (only `Unevaluable` is caught).
- **Effect:** a decoding error or other exception gives a Python traceback with rc 1, which reads as "not met", and no receipt is written. This did not occur in any run here. Suggested fix: catch `Exception` → exit 2 with a receipt.

### F6 — LOW — N1 counts a crash or timeout as a refusal
- **Where:** counter:236-237 (`n1["rc"] != 0` is true for rc `None`).
- **Effect:** a repair that hangs on plain ELFs would pass N1. The committed repair exits cleanly with rc 2 (receipt).

### F7 — LOW — `windows_only` does not limit how many windows change or where
- **Where:** counter:125-138.
- **Effect:** a repair that sprays `UPX!` into stub padding which `upx -d` ignores would pass `windows_only` and `identity`. The committed repair does not do this: its diff against the untampered packed file is empty (libz/dinit) or only the untouched stub word (jq/xxd). This is a counter limit, not a defect in this repair.

### F8 — INFO
- The REA pin is the sha256 of `package.json` only (counter:194-196); REA code files could drift under the same `package.json`.
- `/usr/bin/xxd` is a symlink to `/usr/bin/tinyxxd`. The counter follows it (`shutil.copy2`, sha pin on the target), so the pin is sound.
- Under T1 the sentinel test accepts any 12 zero bytes (repair:96-103). A false early sentinel would make the repair write `UPX!` in the wrong place, but `test_ok` would catch it, so there is no false recovery. It held on every probe.

## Residual risk / verification gaps
- I did not run the full counter with REA (the L1/executor seat owns that run). I ran REA on jq's restored bytes only, and it matched (167).
- The probe covers amd64 only; i386, arm, PE and Mach-O are not exercised. Entry-altered stubs are out of the claim's scope.
- `upx --best` packing determinism is not pinned. Per-case `packed_sha256` is recorded; jq here was `e8b6c9e7…268a`.

No tools were installed or upgraded.
