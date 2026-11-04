source: S272 — Python subprocess environment contract, https://docs.python.org/3/library/subprocess.html#subprocess.Popen (env parameter); own-work evidence: the six `tools/round-70/` instruments pinned by `.ufo/waves/round-70/claims.json` at the freeze below, and `plans/round-70-claims.md`.
verified-at: 4737a542ae3b1b910d8fe43efbd572bc578b07c6 (frozen contract provenance, not this scribe's execution verdict).
recheck: `python3 -I -B tools/round-70/packed-elf.py --check-receipt .ufo/waves/round-70/l1/scores/c3-at-landing.json --root . --rev "$MEASURED_REV"`; use the frozen plan's full forged-receipts and seam-probe commands for R70-C1/C2, with explicit REA package and seat-owned scratch roots; `python3 -I -B tools/round-70/packed-elf.py --selftest` checks the registered pure cases, not the end-to-end claims.
Source locator: S272 draft `.ufo/waves/round-70/w1/ScoutSource/sources.md`; retained `subprocess.html:881-885`, under `#subprocess.Popen`. ScoutSource records HTTP 200, 208648 bytes, sha256 `4b88b8316a05baadaa7b2dd254c320a40b5406d8158a57f2a50b55b4d872a2c7`, fetched 2026-11-04T04:17:30Z, Python 3.15.2 documentation. Located quote (14 words): “these are used instead of the default behavior of inheriting the current process’ environment”. This grounds R70-C2 A3/A6, not measured outcomes or the other seam arms. S260 covers a different scope on the same live URL; retain this snapshot pin because its bytes differ.
Companion located clause (composite, 19 words; raw lines 881–883, bytes 88438–88591): “If env is not None, it must be a mapping that defines the environment variables for the new process”. Read together with the separately quoted 14-word clause, this states mapping substitution rather than merely the inheritance default; the full 33-word sentence is not presented as a single bounded quote. The adjacent self-sufficiency note (composite, 13 words; raw lines 888–890) says: “If specified, env must provide any variables required for the program to execute”.

# Round 70 — provenance-bound receipts, a safe packer seam, and one static carrier

MANIFEST: target=corpus/knowledge/2026-11-04-r70-provenance-bound-receipts.md; operation=create; this line is draft routing metadata, remove when landing.

## Evidence status and axes

Calibration (R70-C1), operability (R70-C2) and coverage (R70-C3) are independent declared capability-acquisition contracts. This entry records the frozen contracts and their declared measurement constants. It is not an execution receipt and does not independently admit any claim. The L1 must integrate genuine measured-revision receipts and attack findings before landing promotion language.

Base: `5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d`; operative declaration: `8b82516182a269482f3a7dc96b50cd2ac349f3a6`; operative freeze: `4737a542ae3b1b910d8fe43efbd572bc578b07c6`. Round-69's later provenance gate did not repair its frozen false-green receipt readers retroactively; round 70 introduces a new freeze.

Own-work producer `tools/round-70/packed-elf.py` has frozen sha256 `1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880`. The container also pins `contract-probe.py`, `mutation-check.py`, `seam-probe.py`, `forged-receipts.py` and `controls.py`; its top-level `instruments` map is distinct from the predicates in `claims` (the round-29 gate's container contract, repairing M69-1).

## Calibration: reader clauses bind the receipt to its producer

`packed-elf.py --check-receipt` requires `--root` and `--rev`. Its admission clauses compare receipt revision to the supplied measured revision and instrument path/hash to the producer blob resolved at that revision. Carrier rows are bound to the frozen `CARRIERS` registry: exact ids, source paths, pins, kinds and ceilings; original procedure counts are bound to `DECLARED_ORIG`. The ratio must equal `round(ceiling / original_procedures, 4)` and must not exceed 0.75; packed procedures must not exceed the carrier ceiling. The reader checks the row/id set, target and matched count (four), true control and met fields, empty failing list, each row's `ok`, required arm presence and arm truth. These are structural/declared-value checks, not a cryptographic attestation that all recorded subprocesses actually ran.

The ten declared forgery clauses are F1 `rev`, F2 `instrument.sha256`, F3 `source`, F4 `before_ceiling_ratio`, F5 `orig_procedures`, F6 `packed`, F7 `carrier rows`, F8 `arm identity_ok missing`, F9 `unknown carrier id`, F10 `instrument absent`. R70-C1 requires every shape to pass the base checker and fail the new checker naming that clause. Identity shapes F1/F2/F3/F9/F10 must also make hardened contract-probe arms `A5_carrier_record` and `A6_packer_pin` false while passing the designated base probe. Genuine receipts must pass both new readers.

The shapes must be cut from the three-carrier round-69 receipt, not the four-carrier round-70 receipt: otherwise the base rejects `target 4 != 3` and the claimed before-arm is false. The frozen battery's wrong-world selftest guards that distinction. The mutation battery separately enforces its target hash, pristine floor and unique per-run `work_dir`; the declared negative floor is 24 against the 23-case registry. Its `--validate` must reject a constant receipt without mutant rows. These are acceptance requirements, not results inferred from this prose.

## Operability: the safe packer seam

The producer hashes caller-supplied `--upx` bytes and compares the pin before executing `--version`. An impostor printing `upx 5.2.0` must be refused without executing. The validated path, not the module default, is threaded through pack/list/unpack/negative-control calls. The frozen pin is UPX 5.2.0 sha256 `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`; packing mode is `upx --best`.

S272 grounds why an explicit `env` mapping is needed: otherwise subprocesses inherit the parent's environment. `build_child_env` constructs exactly `HOME`, `LANG`, `PATH`, `TMPDIR`; LANG is `C`, PATH comes from the parent or `/usr/bin`, HOME and TMPDIR derive from the work root, not a system temporary-directory fallback. This is a key allowlist, not proof that inherited PATH contents are trusted. The committed registry includes `child-env-allowlist`, `child-env-home-in-work`, `child-env-no-tmp`, plus `case-inventory`; the declared green selftest must match all 23 registered cases.

Missing prerequisites and unusable work roots have typed exit-2 refusals; a broken node is `broken_tool`, and an unexecutable packer is `packer_mismatch` rather than a traceback. Producer scratch uses a fresh `mkdtemp` under the supplied work root and is removed in `finally`; the mutation battery must similarly isolate each run. The declared seven seam arms are `A1_hash_before_exec`, `A2_threaded_path`, `A3_child_env_allowlist`, `A4_broken_node_typed`, `A5_packer_exec_format`, `A6_home_no_tmp`, `A7_per_run_work`. Admission requires 7/7 at the measured revision and 0/7 at the base, with A2's receipt bound to its producer before argv records are trusted. REA node invocations retain their existing inherited environment: this is not global child-process sanitization.

## Coverage: a static-exe carrier, with a class-specific ceiling

Declared constants (inventories are procedures / segments / strings, not semantic equivalence):

| carrier | kind | original inventory | packed inventory | packed procedure ceiling | ceiling/original |
|---|---|---|---|---|---|
| `/usr/bin/jq` | executable | 167 / 30 / 190 | 3 / 3 / 3 | 10 | 0.0599 |
| `/usr/bin/xxd` | executable | 99 / 29 / 103 | 3 / 3 / 3 | 10 | 0.1010 |
| `/usr/lib/libz.so.1.3.2` | shared-object | 184 / 29 / 199 | 98 / 6 / 136 | 120 | 0.6522 |
| `/usr/bin/docker-init` (`dinit`) | static-exe | 1268 / 29 / 1111 | 3 / 3 / 5 | 10 | 0.0079 |

The static carrier pin is `0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115`. Its ceiling is 10/1268, not its observed 3/1268 stub ratio. The shared-object ceiling is 120, not the executable ceiling of 10; no universal three-procedure stub is claimed. The frozen registry contains all four full carrier pins, paths and original procedure counts.

The route detects packed bytes with `upx -l` plus zero ELF section headers, requires unpacked sha256 identity against the original carrier pin, and compares recovered procedure/segment/string inventory counts. R70-C3 requires `target 4`, `carriers_matched 4`, `control_ok true`, `failing []` and a true checker verdict. The old round-69 receipt must be rejected on producer binding and `target 3 != 4`; its earlier green verdict cannot establish the new capability.

REA is pinned at 6.5.0 with package.json sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`; the cache-level lock is recorded, not pinned. Reported limits retain REA's 120-second per-verb boundary.

## Limits

Only the pinned Linux x86-64 ELF carriers, UPX 5.2.0 with the exact packer hash and `--best`, and REA 6.5.0 are covered. No other packer, anti-UPX stub with changed magic/entry, PE/Mach-O, or static binary other than the pinned docker-init is promoted. Inventory-count recovery is not semantic equality, source recovery or runtime behavior. Packer child-environment allowlisting does not change the REA node environment. Producer identity and registry agreement alone do not authenticate arbitrary attacker-authored raw execution records; do not generalize the ten-shape battery to rejection of every possible fabrication.
