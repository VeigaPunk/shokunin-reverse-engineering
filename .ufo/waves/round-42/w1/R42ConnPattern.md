# R42ConnPattern — cross-tool pattern scan of tools/round-38..41 at c4a38ea2

**Verdict: DEFECTS FOUND.** Non-segment-bounded path matching and trailing-slash aliasing live in the round-41 C1 counter's exact-path logic (closure D5), the C2 generator/counter declared-tuple key mismatch is confirmed live with a second consumer (CTL-C2-7 builder) that must be ported in lock-step, all four round-41 score receipts still carry no counter digest (closure D4), and the /tmp pattern is clean in rounds 38–41 (historical hits sit in rounds 28–34 and are not inherited by any round-42 port).

## Method

Static scan of `tools/round-38..41` at the base (`git show c4a38ea2:<path>` matches the working tree; all citations are to the base bytes) for the four patterns, plus live re-probes of pure functions extracted verbatim from the base file lines (artifacts) and reads of committed receipt/manifest bytes. No REA/unblob/sasquatch/unsquashfs/7z run, no VCS mutation, no installs (tooling record: none; `git show`/`grep`/`python3` only, host python 3.14). Failing inputs are deterministic and reproduced.

## Pattern 1 — path prefix tests not segment-bounded (closure D5)

| hit | file:line | round-42 port | inherited | failing input |
|---|---|---|---|---|
| 1a `diagnostic_rel` matches the root segment run at ANY position in the diagnostic link, never anchored to the receipt's `parameters.output_directory` | `tools/round-41/c1-counter.py:899-919` (loop 914-918) | `c1-counter` v4 port | yes, unless the port adds the output-dir prefix anchor (draft says "segment-bounded … D5" but the anchored-prefix requirement is the actual fix) | link `/…/decoy/firmware.bin_extract/bin/link` with CR `firmware.bin_extract` ⇒ `bin/link`; a foreign-directory removal satisfies the symlink-removal obligation (R41W2C1PathRule scenario 05b; live probe `artifacts/R42ConnPattern/pathrule-probes.txt` §1a) |
| 1b `path_parts` drops `''`/`.` so trailing-slash and `/./` spellings alias regular-table rows; `strip_rel` never strips a trailing slash (asymmetric) | `tools/round-41/c1-counter.py:780-791`, `951-959`, `962-966` | `c1-counter` v4 port | yes | candidate `firmware.bin_extract/var/info.txt/` ≡ oracle row `var/info.txt` (live probe §1b); a directory-like file spelling passes with the oracle file's sha (PathRule 06a/06e) |
| 1c same receipt string normalizes differently by helper: `strip_output` strips one `$output/`, `path_parts` strips repeatedly | `tools/round-41/c1-counter.py:829-840` vs `780-791` | `c1-counter` v4 port | yes | derivation child `$output/$output/x` keeps a literal sigil after one strip (rejects, 04a) while the file path `$output/$output/x` fully strips (accepts, 04b) |

Segment-bounded prefix tests in the same window that are NOT defects (checked): `mk-carriers.py:61-62` (r39) and `mk-carriers.py:62` (r40) use `base + os.sep`; `local-source-gate.py:170` uses `root + os.sep`; `ledger-status.py:94` uses `root_name + "/"`; `c1-counter.py:1970` uses `old_root + '/'`; `absence-sweep.py:99` uses `k.rstrip(os.sep) + os.sep`. So the defect is concentrated in the two functions above, not systemic.

## Pattern 2 — writer/reader key mismatches

| hit | file:line | round-42 port | inherited | failing input |
|---|---|---|---|---|
| 2a generator writes the declared tuple under `carriers[].declared`; frozen counter reads only `class_expected.features` ⇒ `features` ⇒ `declared_features` (M41-1 / R41-CL1) | writer `tools/round-41/heldout-gen-v3.py:1372,1464`; reader `tools/round-41/c2-counter.py:1496-1503` | `heldout-gen-v4` + `c2-counter` v4 | draft fixes with ONE key `declared_features`; but see coupling risk below | all 12 combos (`C01..C12`): `class_expected` None, `features`/`declared_features` absent ⇒ `observed_features_match_declared false`, exit 1 (receipts `c2-at-e9a24d07.json`, `c2-at-042b8769.json`; key census `artifacts/R42ConnPattern/manifest-keys.txt`) |
| 2b `c2-controls.py` builds CTL-C2-7 lookup rows from the OLD key `c['declared']` | `tools/round-41/c2-controls.py:84` | control builder (C2 frozen control tables) | inherited if not ported with the generator | after the v4 generator moves to `declared_features`, an unported `c2-controls.py` reads a key the manifest no longer carries ⇒ lookup rows empty/vacuous, the anti-enumeration control silently weakens (the exact property R41-CL1's refreeze must beat, claim line 99-100) |
| 2c manifest-level fallback key list is dead code that can mask a third key name | `tools/round-41/c2-counter.py:1486-1491` (`class_features`,`classes_features`,`feature_tuples`,`features_by_class`,`class_tuples`) | `c2-counter` v4 | keep in mind: the single-key port must drop or rewrite this fallback, not extend it | none today (no manifest carries any of the five names); a future generator writing a new manifest-level key without updating the counter recreates M41-1 |
| 2d `run.json` writers have no reader (M41-5): `c1-run.sh` writes `OUTDIR/run.json`, the counter never reads it — the ARG_MAX failure produced a missing `run.json` with zero binding effect | `tools/round-41/c1-run.sh:16-23` (contract), counter clauses read `after.json` only | `c1-run.sh` + `c1-counter` v4 | yes | any rootfs-sized run (like V4) where `jq --argjson` exceeds ARG_MAX: `run.json` absent and `run-harness-failure.log` present, yet the counter still scored 4/4 |

## Pattern 3 — receipts without the scorer's own digest (closure D4)

All four round-41 score receipts lack `counter_sha256`; the C1 receipts contain no counter digest of any name; C2 embeds it only as `frozen_units.COUNTER` (different key, inconsistent schema). Writer of the C1 receipt: `tools/round-41/c1-counter.py:1789-1797` (dumps `res` + `argv` + `exit_code`; no self-digest). The L1 wrapper `l1/score.sh` computes none either. Earlier rounds did record it (`round-22/23/32/34` receipts), so this is a regression in the L1 scoring harness.

- Inherited: the round-42 `c1-counter` port is the same writer; unless the port or `l1/score.sh` computes and records the counter file sha256, the freeze receipts will again be self-unverifiable (the draft claim line 19-20 requires it — an enforcement point is needed, and it must be named, since neither current writer does it).
- Verify: `artifacts/R42ConnPattern/receipt-sha-audit.txt`.

## Pattern 4 — hardcoded /tmp / TMPDIR-ignoring scratch

Clean in rounds 38–41: every tool honours `TMPDIR`/`HYAKU_SCRATCH` or a `--work`/`--scratch` argument (`c1-counter.py:1516`, `c2-counter.py:439`, `c1-run.sh:137,141` exports `TMPDIR=$scratch`, `heldout-gen-v3.py:2049-2050,2087`, `sqfs-triage-v3.py:1721`, `fetch-vendor.py:262`, `c1-extra.py:66,197`, `local-source-gate.py:471`). The hardcoded hits live in earlier rounds and are NOT in the port ancestry: round-30/31/32 `cwd="/tmp"` (REA subprocess spawns), round-34 `HOME="/tmp"`, round-28/29 hardcoded `TMP=` host paths, round-25 `ruler.py:90` `startswith(('/tmp','/dev/shm'))`. Round-42 ports derive from round-41 files, so nothing inherits. Residual guard: REA stages under system `/tmp/rea-firmware-*` and unblob writes `unblob.log` into cwd — the c1-run/fetch ports must keep `TMPDIR` exported and run from scratch, as round-41 already does.

## The move (one bounded proposal)

Port the C2 refreeze's single-key change to **all three consumers at once** and prove it before the freeze: `heldout-gen-v4` writes `declared_features`; `c2-counter` v4 reads exactly that key (drop the 5-name fallback); `c2-controls.py` v4 builds CTL-C2-7 rows from `declared_features`; and `c2-counter`'s own selftest fixtures include at least one combo whose ONLY tuple declaration is `declared_features` (today the selftest writes `features`/`class_expected.features`, so a green 70-case selftest would pass without ever exercising the new key). This is the smallest change that makes R41-CL1's refreeze (a) self-testing for the new key and (b) unable to silently weaken the lookup control that R41 w2 measured at 8/12. It does not harm coverage/depth/calibration: it only closes the exact two-seat interface gap that M41-1 froze.

Secondary (same move, accepted as part of the port): record `counter_sha256` inside the counter at receipt time (same process, the frozen bytes being run) so D4 is resolved without depending on `l1/score.sh`.

## Risks

- If `c2-controls.py` is frozen unported, CTL-C2-7 succeeds vacuously on combos (0/12 or an error), which would *weaken* the required anti-lookup evidence — the claim's "lookup control scores strictly fewer than half" needs the ported control, not the old one.
- Fixing `diagnostic_rel` by anchoring to `parameters.output_directory` changes gap disposition on any receipt whose diagnostic link is not under the output dir; the four real carriers must be re-run through the ported counter (their current links are under the trusted output dir, so the 4/4 score should stand — verify by rerun).
- Rejecting trailing slashes could fail a receipt that REA actually emits with one; the round-41 receipts do not contain any, so the strictness change is safe on real data but must be a red selftest, not a silent normalization change.

## Verification exercised

Live probes (verbatim function extraction) reproduced 1a/1b/1c; committed byte reads reproduced 2a (manifest census: `declared` on 52/52, `declared_features` on 0/52), 2b (controls builder reads `declared`), 3 (four receipts, no `counter_sha256`); static scan enumerated pattern 4. Everything cited is at the base `c4a38ea2`; no working file was modified.

## Bounds

Leaf seat: no subagents, no background jobs, no agent://all. Wrote only `.ufo/waves/round-42/w1/R42ConnPattern.md` and `.ufo/waves/round-42/w1/artifacts/R42ConnPattern/`. No git/jj mutation; no tool installs (nothing new on PATH); no vendor bytes; no scratch dirs created (all probes in-memory; no `/tmp` usage).
