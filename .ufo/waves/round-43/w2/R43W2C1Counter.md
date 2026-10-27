# R43W2C1Counter — C1 counter review

**Evaluated revision:** `77d196c66f4fea00d7d543728b190ebdfaf6d0f0` (the C1 receipt's measured revision).  
**Freeze:** `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c`.  
**Lane tip observed:** `5856614ac4bf7f2363bbcd1956644474a82108e5`.

Scope was the frozen P43-C1 counter and committed score/control evidence. I used only committed Git blobs for the rechecks below. No C1 generator or REA run was performed. C2 was read only for the required receipt context; its result is not assessed here.

## Findings, by severity

### High — P43-C1's S135 license-row condition is not a binding

The frozen plan requires `corpus/SOURCES.md` to carry row S135 naming the unblob 26.6.4 LICENSE at its pinned URL with its committed digest (plan, `## R43-C1`, predicate). The counter's `CLAIM_BINDINGS` (`tools/round-43/c1-counter.py:235-251`) contains no S135/SOURCES-content binding. `SOURCES` appears in `FROZEN_PATHS` (`:177-183`) and is used by the post-freeze drift walk, so this only establishes that the file was not changed after the freeze. `fixtures_pinned` (`:1574-1583`) derives from the `tools/round-42/fixtures.json` pin bytes, committed fixture copies, and the fixture license field; it does not parse or validate S135. The counter's runtime receipt therefore can mark `bindings_complete` and `met_target` without deriving the required row's URL or digest.

The row is in fact correct in the measured blob: S135 names `https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/LICENSE`, reports 1068 bytes and SHA-256 `67303bbde385e13f69e8019f6f8bc77d4ebfce58c2a409952645e3fe4f4d922e`. This is a missing predicate check, not evidence that the current row is wrong. The receipt reports `fixtures_pinned: true`, `bindings_false: []`, `matched/n: 78/78`, `met_target: true`, `exit_code: 0`; no S135-derived field appears in it. The current true row does not make the counter's absent check auditable or prevent a bad row already present at FREEZE from passing.

### Medium — run.json evidence is not fully represented in the score receipt

The counter checks all loaded `run.json` records in its loop (`:1880-1921`), but serializes only `run_rows[:40]` (`:1922`). The held-out set is 78 carriers; the C1 receipt has no `runjson.rows_total`, no rows for the other 38 carriers, and no SHA-256 of the raw `run.json` blobs. Thus `runjson_digests: true` is an internal all-record result, not an independently reconstructible per-carrier receipt. The score's `digest_matches_carrier` value is also read from each record and required to be literal `true` (`:1908-1910`), rather than computed as a field; the actual subject-hash equality is separately checkable against the carrier bytes.

Independent H01 check passed: committed carrier SHA-256 and `run.json.subject_sha256` both equal `0d8ba23bed1a882343495375022be98e6e6b2b7e4cf4baea8f03b9638950cc1c`; `digest_matches_carrier` is true; run summary `gap_kinds` and `handlers` match the counter's envelope extraction. The raw H01 `run.json` SHA-256 is `14f518ec034b559f613b4cd3d2d1e30fce17a02359173f151ecc92ade2424a51`, a value not stored by the score receipt. This is a receipt completeness/derivation gap; this single-row recheck does not falsify the counter's internal 78-row loop.

### Low — stale lookup clause in the counter docstring contradicts the frozen claim

The docstring's predicate prose at `tools/round-43/c1-counter.py:20-22` says the lookup control “scores strictly fewer than half.” The frozen plan explicitly amended that clause to report-only because the known score is 19/24 (`plans/round-43-claims.md`, `## R43-C1` and `## Wave-1 amendments`, item 2). The implementation and receipt correctly do not bind it: `CLAIM_BINDINGS` omits `lookup_combo_below_half`; receipt `lookup` says `score: 19`, `below_half: false`, `binding: false`, “reported, not bound.” This is stale counter documentation, not a scoring failure, but it contradicts the plan's statement that the docstring clause list is the full predicate text.

## Clause review and read-only reproductions

- Score identity: the committed C1 receipt at measured revision `77d196c66f4fea00d7d543728b190ebdfaf6d0f0` reports `exit_code=0`, `matched=78`, `n=78`, `met_target=true`, `bindings_false=[]`. Its `counter_sha256` and `counter_sha256_at_freeze` both equal `3a23e93ee95f4b0d69a2f4d03ed2592c9f0b81dbb6188cb6818a18a8f4f33c79`.
- Frozen table / code identity: the receipt reports the table region SHA-256 `92540586b8c03dcde511652c0d76ba93cbde8e5f4e79e0b94509192c19b101f2` and no changed frozen paths. I independently recomputed full-file freeze-to-REV drift for `SKILL.md` and `tools/round-43/c1-counter.py` from Git objects: merge-aware `git log` yielded no commit output for either path (exit 0); both freeze and REV blob IDs matched (`SKILL.md` `3268fe77d27272b89d75b8f88f75c24c24158407`; counter `e9335c03c6ad5bb7487be7197c0e6ce31c9c9803`). This does not independently re-extract the table-region hash.
- C02 tuple: independently read committed C02 envelope and manifest, called the frozen counter's `observed_features` and `declared_features`, and compared all six required fields. All six matched (full values in `artifacts/R43W2C1Counter/rechecks.txt`); envelope SHA-256 is `9ada75f5082fa6ebe8a6b3e440de5fb19607872c2bc26beb8190bb796577a18b`. The counter receipt reports `observed_features_match_declared=true` and generator tuple check all equal; this C02 reproduction supports those values for this carrier only.
- For the remaining P43-C1 groups, the receipt reports true for the listed seed/path/regeneration and committed-carrier checks; table/anchor/interpreter/evaluator identity; evaluator pairs; tuple/extras checks; fixture pins; legacy/dev-arm and round-42 control reproduction; combo unseen majority; and real receipts. These groups were not independently rerun in this seat. In particular `combo_unseen_majority` reports 21 unseen of 24 against a threshold of 12. Lookup is intentionally report-only, as above.
- C1 control receipt summary says `ok=true`, `controls_at_target=[]`, `kill_rule_fires=false`; CTL-C1-2 records red exit 3 for the round-42 C02 mismatch and green exit 0; CTL-C1-4 records its manifest-only hand edit as `observed_features_match_declared=false`, counter exit 1. These are committed claims, not rerun here.
- C2 context only: committed `c2-at-77d196c6.json` reports `exit_code=1` and `checks_ok=false` despite gate exit 0 and copy-audit exit 0 / 136 checks / 0 failures. No C2 diagnosis is made in this C1 seat.

## Residual risk and verification gaps

- **C1 remains incompletely enforced by its counter** until the required S135 row content is made a binding (or otherwise incorporated into the scored predicate implementation). Current source bytes happen to satisfy that clause.
- The run.json loop's all-78 verification can be read in code, but its serialized receipt omits 38 per-carrier rows and raw run.json hashes; independent audit of the complete runjson evidence therefore requires the committed inputs and counter logic.
- No LSP device/status interface was exposed by the available tool inventory. I used `grep`/`read` as literal fallback for code locations; those results are not semantic caller/reference evidence. No caller/reference graph was available.
- No tests, formatter, linter, whole-repo check, generator, extractor, REA, unblob, or sasquatch run was made. No disk-heavy probe or installation was needed. No scratch was created; nothing required cleanup. The initial exploratory Python probe exited 1 on a missing manifest `envelope` key; manifest carrier paths do not contain that key, so the successful recheck used `C02/envelope.json`. No repository bytes were modified by that probe.

## Paths and hashes examined

SHA-256 values below were computed over committed blob bytes with `git show` unless the entry is a Git blob object ID. Score/control files are from the observed lane tip; content score is explicitly for REV `77d...`.

| Path | Revision | SHA-256 |
|---|---|---|
| `plans/round-43-claims.md` | FREEZE | `0326dff974d48df575486256dbd5a0b36593dbc84155d0d40560b64d3c20d83e` |
| `tools/round-43/c1-counter.py` | FREEZE and REV | `3a23e93ee95f4b0d69a2f4d03ed2592c9f0b81dbb6188cb6818a18a8f4f33c79` |
| `SKILL.md` | FREEZE and REV | `32fb1a265da04c07c958cf04a4f4552bdec94fb527ef863cf1e08e313c03b724` |
| `corpus/SOURCES.md` | REV | `251ec4a72ee3dcf1f0f5e45debc001be2333c0340b661e616ebceaaedb62c68c` |
| `corpus/evidence/round-43/c1/heldout/manifest.json` | REV | `980eafa59ca3890bf45945a02a6e608da511435d972d1ec978a38fd068ef2555` |
| `corpus/evidence/round-43/c1/heldout/C02/envelope.json` | REV | `9ada75f5082fa6ebe8a6b3e440de5fb19607872c2bc26beb8190bb796577a18b` |
| `corpus/evidence/round-43/c1/heldout/H01/carrier.sqsh` | REV | `0d8ba23bed1a882343495375022be98e6e6b2b7e4cf4baea8f03b9638950cc1c` |
| `corpus/evidence/round-43/c1/heldout/H01/run.json` | REV | `14f518ec034b559f613b4cd3d2d1e30fce17a02359173f151ecc92ade2424a51` |
| `.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json` | lane tip | `13a495dbb6862d6cfbdd1f41e4a09460740f86bf93e8bb08e313b06d92b8a55c` |
| `.ufo/waves/round-43/controls/c1/summary.json` | lane tip | `143d4c38412c8d4af785243ffdabc5e8735d0237818643ce1bb151e4db624e5d` |
| `.ufo/waves/round-43/controls/c1/receipts/CTL-C1-2.json` | lane tip | `84a6d0dd8333028fcb0da29b8e33fbe814309257a5a0f264789a29e62a78706c` |
| `.ufo/waves/round-43/controls/c1/receipts/CTL-C1-4.json` | lane tip | `ed41a5e1da2b20cfc006d1c4dd8dc855a954646807b1874171880c5e5327b919` |
| `.ufo/waves/round-43/l1/scores/c2-at-77d196c6.json` | lane tip | `42f592aec7d6ffe082a257dba1142b1790857c53ddaab17b1bae1c8db09b76e6` |
| `.ufo/waves/round-43/controls/c2/ctl-c2-2-summary.txt` | lane tip | `4d1ae7eb4b902a2a6fa3e26c5e61f4dc9be521075ea23cdefa256109f387a1eb` |

## Commands / outputs / exit codes

- `git -C <LANE> rev-parse HEAD` → `5856614ac4bf7f2363bbcd1956644474a82108e5` (0).
- `git -C <LANE> log --oneline -15` → lane history showed score/evidence commit `5856614a`, held-out commit `77d196c6`, and freeze `f3f8db38` (0).
- Python read-only recheck used `git show <REV>:<path>` for the manifest, C02 envelope, H01 carrier, H01 run.json, H01 envelope; each Git subprocess returned 0. Python observation and digest comparisons completed successfully. Exact outputs are in `artifacts/R43W2C1Counter/rechecks.txt`.
- For freeze drift, `git -C <LANE> log --format=@@%H --name-status --no-renames -m --diff-merges=first-parent <FREEZE>..<REV> -- <path>` returned 0 with empty output for `SKILL.md` and `tools/round-43/c1-counter.py`; `git rev-parse <FREEZE>:<path>` and `<REV>:<path>` returned 0 and identical object IDs as listed above.
- Hash inventory used `git show <REV-or-tip>:<path>` followed by Python `hashlib.sha256`; all listed blobs returned 0.
- LSP was unavailable (no LSP tool/status route in this session); no semantic references/definition/diagnostics queries were possible.

Report: `.ufo/waves/round-43/w2/R43W2C1Counter.md`
