# R38ReviewerPredicateIdentity — predicate-identity audit + falsifiers (wave 1)

Seat: reviewer, kaidoku round 38 wave 1. Judged on coverage, calibration.
Anchor: **frozen bytes** — claims+counters at freeze `e059ca9391642d5b71b6662cabcbdce0d9308719`, control receipts at `efd5c47a72a50b3a434783f82268fb4a96e636a1`, base `77091b492cc53f8743bd0701b1e7d5e66123dd84`. All counter runs below used `python3 -I -B` with `HYAKU_SCRATCH`/`TMPDIR` isolated to my seat scratch; every fixture repo was created with `git init` + `rev-parse --show-toplevel` verification; scratch was removed at the end. Nothing was written outside this report and `.ufo/waves/round-38/w1/artifacts/R38ReviewerPredicateIdentity/`. No VCS mutation in the lane; no REA run (no claim data exists yet — `corpus/evidence/round-38` is absent at HEAD, verified via `git ls-tree`).

**Headline: 10 green falsifiers.** The frozen C2 counter can be driven to `met_target=true, exit 0` by four claim-violating states (shadow duplicate row, decoy-document repair, shadow duplicate section, second contradictory count), and the frozen C1 counter by six (supersession-denying note, absent gaps field, forged provider version, duplicate S-id row, junk carrier bytes, duplicated oracle rows). Additionally the `frontier_note` binding is **already true at the base** — the do-nothing control itself proves it. Separately, the frozen `c1-counter.py` and `plans/round-38-claims.md` are being **edited live, uncommitted, mid-round** (§1), and the v2 rewrite's selftest currently fails its own green case.

Artifacts (all under `.ufo/waves/round-38/w1/artifacts/R38ReviewerPredicateIdentity/`): `c1-counter-at-freeze.py`, `c2-counter-at-freeze.py`, `gen-controls-at-freeze.py`, `c1-run-at-freeze.sh`, `instruments-at-freeze.json`, `claims-worktree-vs-freeze.diff`, `c1-counter-worktree-vs-freeze.diff`, `counter-run-outputs.txt`, `carrier-pin-check.json`, `c2-frontier-blindspot.json`, `c2-decoy-{base-sanity,A,A2,B,C,D}.json`, `c1-decoy-*.json`, `c1-decoy-summary.json`, `c2-decoys.sh`, `c2-decoyA2.sh`, `c1-decoys.py`, `c1-e9b.py`.

## 1. Freeze integrity — the frozen instruments are mutating mid-round (highest severity)

Observed states of `tools/round-38/c1-counter.py` within ~25 minutes (md5, lines):

| state | md5 | lines | when |
|---|---|---|---|
| freeze blob `e059ca9` | `ef0c65cbf32c…` | 395 | committed |
| working tree | `760a697a354d…` | 417 | at my first run (crashed) |
| working tree | `c596e8b3c25d…` | 427 | 03:27:33 -03 |
| working tree | `da425d210b44…` | 424 | at report time |

- The uncommitted edit **rewrites the frozen predicate docstring**: v1 "run with stock unblob 26.6.4; no external extractor dependency" → v2 "run with `sasquatch-v4be` available, as unblob 26.6.4's `SquashFSExtractor` requires" **plus a new paired before-receipt clause** ("publishes none of them and names `sasquatch-v4be` as a missing extractor dependency"). This reverses the v1 claim's own "Not claimed / corrected premise" sentence (which explicitly said the round-37 before-arm "does not reproduce" and that "sasquatch-v4be is required" is not claimed). Full diff: `c1-counter-worktree-vs-freeze.diff`.
- `plans/round-38-claims.md` is **also modified uncommitted** ("freeze v2"): the v1 sentence "Both claims below are scored only by the counter, predicate and kill rule frozen in this file's commit; frozen controls are scored with each counter before any claimed data" is **deleted**, a "Freeze v2 note (pre-scoring amendment)" added (citing R38CrossToolK1's measurement that the v1 probe never actually stripped `~/.local/bin` from PATH), the predicate restated with before-receipts, selftest count 15→18, and the harness's oracle-mode sentence dropped. Diff: `claims-worktree-vs-freeze.diff`.
- **No new freeze commit exists.** At HEAD the committed claims/counters still say v1; the working tree says v2. Three-site identity (claim ↔ counter ↔ receipt) is broken live, and any scoring run performed now would use edited bytes, violating the instrument map's "scores happen only with these bytes, never with edited copies".
- The v2 (in-flight) counter **fails its own selftest green case**: `{"cases": 18, "green_ok": 0, "red_ok": 17, "failures": ["green: want 0 got 1"]}` (observed twice, md5 `80d2413f`/`da425d21`). An intermediate state also crashed with `AttributeError: 'NoneType' object has no attribute 'get'` on the base run and selftest (`chunk_handlers(envs.get(...))` without a None guard; later states added `if not env: return []` guards). I did not repair any of this — reported only.
- `tools/round-38/c1-run.sh` was edited by a **commit after the freeze** (`efd5c47a..HEAD`, riding the w1-dispatch commit): `mkdir -p "$OUT"` → `rm -rf "$OUT"`. The freeze's harness could not run the after-mode at all (REA refuses an existing extraction root, which `mkdir -p` creates). A listed instrument (`c1_harness`) changed post-freeze.
- `tools/round-38/gen-controls.py` was edited **between the freeze and the controls commit** (`e059ca9..efd5c47a`): the freeze copy mapped control kinds via `a.kind.split('-')[1]` → `'1'/'2'/'3'`, which falls into the green-fixture `else` branch — at the freeze commit, all three c2 defect controls would have been built as GREEN fixtures (control meets target → kill). The committed control receipts were generated with the fixed copy. The freeze shipped a broken control generator.
- The untracked `.ufo/waves/round-38/w1.ready.dispatched` stamp repeats the exact R36-CL1 defect class the claims file says was "landed as fixes".

## 2. Site 1↔2 — claim sentence ↔ frozen counter code (v1 bytes)

### 2a. C1 (`plans/round-38-claims.md` Predicate P38-C1 ↔ `c1-counter.py` at freeze)

Faithful (verified, not just plausible):

| claim sentence | code | verdict |
|---|---|---|
| "publishes every regular file of the frozen independent oracle (same relative-path suffix, same sha256)" | `matched()` c1:136-143; `after_oracle_hits == oracle_files` c1:190 | ✓ implemented as stated |
| "names the `squashfs_v4_be` handler" | `after_handler_ok` c1:177 | ✓ (any chunk; see D9 for the row-side strictness) |
| "recomputes to its stored evidence id under the rea-agents 6.5.0 rule" | `after_evidence_id_ok` c1:185 = xpin col2(stored) == col3(id under 6.5.0) and `ev_`-prefixed — confirmed against `xpin-attribute.mjs` output spec (`path, stored, id65, id67, verdict`) | ✓ meaningful (not the vacuous id65==id67 reading) |
| receipt identity = subject digest (R36-CL6) | `after_subject_ok` c1:174 vs carriers.json pin | ✓ |
| oracle/carriers unchanged after freeze | blob equality c1:152,167 | ✓ (but see D4) |
| "the counter below at the base exits non-zero" | measured: exit 1 at `--rev 77091b49` and at `--rev e059ca9` | ✓ |
| selftest 15 cases (1 green, 14 red) | measured: `cases 15, green_ok 1, red_ok 14, failures []`, exit 0 | ✓ |
| dev inputs are the round-36 selftest fixture envelopes, never a carrier | `tools/round-38/selftest/*` sha256-identical to `tools/round-36/selftest/*` (4/4 files) | ✓ |
| "SOURCES.md row opened 2026-10-26 whose used-by lists that entry" | registry scan c1:219-233 (11 cells, `c[8]==OPENED`, `ENTRY in used`) | ✓ shape |

Divergences (sentence vs code), each with a live falsifier unless noted:

- **D1 — "the round-38 frontier note supersedes the big-endian Frontier bullet" is not implemented, and is pre-satisfied at the base.** Code: `frontier_note` = any line in the whole file containing `big-endian` AND `superseded` (c1:208-209) — no Frontier-section scope, no round-38 anchor, no check that the bullet itself is marked. At the base/freeze this is already true from round-36 text: `PROVINCE.md:157` ("[2026-10-26: superseded for LE SquashFS v4 …; big-endian/AVM stays here.]") and `PROVINCE.md:374` ("… is superseded for little-endian SquashFS v4 … Big-endian/AVM and vendor-mangled images stay Frontier.") — the latter **asserts big-endian stays Frontier**, the opposite of the binding's intent. Evidence: ctl-c1-0 records `frontier_note: true` at the freeze with zero round-38 work. Falsifier **E1 GREEN**: a fixture whose only triggering line is "- the big-endian Frontier bullet is not superseded; big-endian ground stays Frontier." scores `met_target=true` (`c1-decoy-E1-note-denial.json`). The frozen selftest's own green note sits under `## Next`, not Frontier — placement was never checked.
- **D2 — "run with stock unblob 26.6.4" is unchecked.** Code checks `provider.id == 'unblob'` only; the envelope schema carries `provider.version` (dev-after.json: `"version": "26.6.4"`), never compared. Falsifier **E3 GREEN**: `provider.version = "9.9.9"` → `met_target=true` (`c1-decoy-E3-provider-version-forged.json`).
- **D3 — "carries no extraction gap" passes when the receipt omits the field entirely.** `gaps(env) == []` treats a missing `extraction_gaps` key as zero gaps (c1:131-134). Falsifier **E2 GREEN**: key deleted → `met_target=true` (`c1-decoy-E2-gaps-field-absent.json`). The claim's wording asserts the receipt *carries* no gap; the counter accepts a receipt that says nothing.
- **D4 — carrier bytes are never hashed; "sha256 pins frozen" is checked only against the receipt's self-reported subject digest.** The counter reads carriers.json, oracle.tsv and after.json — never `corpus/evidence/round-37/c1/K*/carrier.*`. Falsifier **E8 GREEN**: junk bytes at all four pinned carrier paths → `met_target=true` (`c1-decoy-E8-carrier-bytes-junk.json`). For the record I verified the pins themselves are correct: sha256 of all four carrier blobs at the base matches the pins (`carrier-pin-check.json`; K1 9780 B, K2 1606 B, K3 4096 B, K4 307 B).
- **D5 — duplicate oracle rows are not separate units.** `matched()` counts satisfied oracle *rows*; two identical rows are both satisfied by the **same single published file**. Falsifier **E9b GREEN**: oracle.tsv with each row duplicated (frozen in both commits) → `oracle_files=4, after_oracle_hits=4, met_target=true` with only 2 distinct published files (`c1-decoy-E9b.json`).
- **D6 — duplicate S-id registry rows accepted.** The sourced binding accepts *any* row with the cited id; id uniqueness is unchecked, so a shadow duplicate row (opened 2026-10-26, used-by listing the entry) satisfies the binding while the row the entry actually cites is opened 2026-10-25. Falsifier **E4 GREEN** (`c1-decoy-E4-duplicate-sid.json`).
- **D7 — `section()` is first-match on headings (c1:62-71).** A row placed under a *second* `## Round-38 additions to Core` heading is invisible → false negative (E5: `province_core_row=false`, exit 1). Blind spot, not a green.
- **D8 — registry rows with ≠11 cells are silently skipped (c1:224).** A valid-cited row with an extra column is invisible → false negative (E10: `sourced=false`, exit 1).
- **D9 — the Core row must carry the handler in its FIRST cell (c1:205-207); the claim says only "naming `squashfs_v4_be`".** Stricter than the claim → false-negative risk for a legitimate row with the handler in another cell. No falsifier needed (code cite).
- **D10 — `ENTRY in r` is a substring test over the whole row** — a row mentioning the entry path anywhere (even in a non-citation cell) passes "cites". Weaker than "cites" but bounded by the sourced chain; noted, no falsifier.

### 2b. C2 (Predicate P38-C2 ↔ `c2-counter.py`, frozen bytes == working tree)

Faithful:

| claim sentence | code | verdict (measured at base) |
|---|---|---|
| "every backticked lane-repo pointer in them resolves (path exists, line range inside the file)" | `pointers()` c2:100-111 (findall over backticked tokens, LANE allowlist) + `resolves()` c2:113-123 | ✓ 48 pointers scanned, 1 unresolved = `evidence/doctor/` in `prov_core:REA MCP server` — exactly the claim's Before |
| "the four stated counts equal command A / command B" | O1-O4 c2:203-215; `command_a`/`command_b` c2:125-150 match the SCORECARD "Measurement recipes" code-shape (stems, coverage-map split, `- **` rule blocks, knowledge refs with ranges; obligations aligned/total) | ✓ observed 124/124, 17/17, 9/9 (command B), SHONEN box1 17/17 |
| "the three stated section ranges equal the observed heading-to-last-non-blank-line ranges" | R1-R3 c2:209-211 vs `heading_range` c2:152-163 | ✓ observed craft [81,314], adjacent [97,125] |
| "no unit removed / no fewer pointers" | `missing_units`, `pointers_not_fewer` c2:229-235 | ✓ |
| selftest 14 cases | measured: `cases 14, green_ok 1, red_ok 13, failures []`, exit 0 | ✓ |
| do-nothing at base exits 1 with exactly 1 mismatch | measured + ctl-c2-0 | ✓ |
| separability (C2 never touches C1 receipts/carriers; C1 reads none of SCORECARD/SHONEN) | code read-set | ✓ |

Divergences:

- **D11 — duplicate rows/boxes are NOT separate units: a later key overwrites an earlier one.** `units()` keys every row by first cell / box text into a dict (c2:73, 86, 92) — precisely what QUALITY 77 ("keeps duplicate rows/boxes as separate units instead of letting a later key overwrite an earlier one", from R36 M36-3) forbids. Falsifier **decoy-A2 GREEN**: on the real base bytes, append a duplicate `| REA MCP server | … |` row to `## Core` with the pointer repaired (compensating one blank line so the Adjacent range is unchanged) → `mismatches=0, guards_ok=true, met_target=true, exit 0` while the **original row still carries the unresolved `evidence/doctor/` pointer** (`c2-decoy-A2.json`; the receipt's own `base_unresolved` shows the counter knew the pointer was bad at base). The plain decoy-A (without compensation) was *defeated* by R3 — the line insertion shifted the Adjacent range 97-125→98-126 and the range check caught it (`c2-decoy-A.json`) — that part of the counter works.
- **D12 — `stated()` is `re.search` (first match), not `findall` (c2:200-202)** — QUALITY 77's exact prohibition. Falsifier **decoy-D GREEN**: the real coverage row with a second, contradictory `999/999 knowledge files mapped` appended in the same row → first match (124/124) is checked, the junk statement is invisible → `met_target=true, exit 0` (`c2-decoy-D.json`).
- **D13 — `section()` is first-match on headings (c2:31-39): shadow sections are invisible.** Falsifier **decoy-C GREEN**: a second `## Owned axes` section appended to the real SCORECARD with `| coverage | 10 | 999/999 knowledge files mapped | … |` → the shadow row is never a unit, its count never compared → `met_target=true, exit 0` (`c2-decoy-C.json`).
- **D14 — "repaired by a resolving pointer to the same document" is implemented as a suffix match (c2:226-231: `p2 == path or p2.endswith('/'+path)`), not the intended document named in the freeze** (`.ufo/waves/round-19/evidence/doctor/`, claims-file Before note; QUALITY 77: "not any same-basename file"). Falsifier **decoy-B GREEN**: repair pointer `corpus/evidence/doctor/` backed by a **decoy document I created** → suffix matches → `mismatches=0, guards_ok=true, met_target=true, exit 0` (`c2-decoy-B.json`).
- **D15 — the PROVINCE `## Frontier` rows are never scanned at all.** `units()` collects only `|`-rows; the real Frontier section is a bullet list → zero `prov_frontier` units. The Frontier bullets carry 6 backticked lane-repo pointers (measured, `c2-frontier-blindspot.json`); none is checked. All 6 resolve at the base today, so this is latent — but any future unresolved pointer in a Frontier bullet is invisible to the counter, i.e. the claim's "the PROVINCE.md `## Core` and `## Frontier` rows carry zero mismatches" is enforced on half its surface.
- **D16 (minor)** — PROVINCE table *header* rows become units (`prov_core:Surface`), adding noise units; harmless at base (present in both rev and base sets).
- **D17 (observation)** — the round-36 sasquatch Core row (the very surface C1 moves, `PROVINCE.md:372`) lives under `## Round-36 additions to Core`, a separate `##` section outside `## Core`; C2 therefore never scans it. This matches the claim's literal "## Core and ## Frontier rows" wording, but means the claim's calibration surface excludes the dated round-section rows entirely.

### 2c. Cross-cutting corpus criteria

- **QUALITY 68** (predicate byte-identical across claim/config/counter/receipt; counting command reads the predicate from the claim file and re-hashes pins): not met by the frozen v1 bytes. The counter docstring de-backticks and re-wraps the sentence (backticks around `squashfs_v4_be`, `PROVINCE.md`, `SOURCES.md`, `corpus/README.md` dropped); the receipt carries only the label `"predicate": "P38-C1"`/`"P38-C2"`, never the sentence; neither counter reads `plans/round-38-claims.md`; neither hashes the carrier pins (D4).
- **QUALITY 77**: three of its four clauses are violated by the frozen C2 counter (first-match `stated()` D12; dict-collapse units D11; suffix-match repair D14), each with a green falsifier.
- **QUALITY 78** (receipt integrity ≠ provenance): the C1 evidence-id check is integrity-only by design; anyone with the producer's digest code can mint a passing envelope (my E-decoys did exactly that, via the counter's own xpin). Provenance must come from the independent non-author re-run the wave owes; the counter cannot supply it.
- **QUALITY 45** is not triggered (C1's claim does not name a specific `claim_row` id), but D6 shows the same *class* of weakness the row was written for.

## 3. Site 3 — control receipts (`.ufo/waves/round-38/controls/`)

- **Labels:** 7 receipts, `control` fields `c1-0, c1-1, c1-2, c2-0, c2-1, c2-2, c2-3` ↔ claim's CTL-C1-0..2 / CTL-C2-0..3. **No scored receipt carries a label not in the claim.** ✓
- **All 7 exit 1** ✓ — the kill rule holds; no control met the target.
- **ctl-c1-0** ran at `--rev e059ca9` (the freeze), not "at the base" as the claim's kill-rule sentence says; its output also records `frontier_note: true` — the pre-satisfaction evidence of D1. (At the true base the frozen counter exits 1 via `carriers_unchanged=false` — measured; the claim's "unevaluable/exit non-zero" wording covers both.)
- **ctl-c2-2 "delete the bad pointer" does not delete the bad pointer.** `gen-controls.py` `c2_fixture(defect='delete')` empties the *Capabilities* row's pointer (`x.md` — not a lane pointer, so deleting it is a no-op for the counter) while the rev tree's PROVINCE row substitutes the bad pointer with `docs/x.md`. Exit 1 comes from the **unrepaired wrong-document guard**, not from a deletion.
- **ctl-c2-3 "substitute other resolving documents"** substitutes the Capabilities row's non-pointer `x.md` with resolving `d/y.md` **and** the bad pointer with `docs/x.md`; exit 1 via the **same unrepaired guard as ctl-c2-2** — the two controls are mechanism-identical, so the four C2 controls exercise three distinct failure modes, not four, and neither c2-2 nor c2-3 exercises its labeled mechanism.
- Control receipts record argv + counter exit + the counter's stdout summary, but **omit the guards detail** (`unrepaired`/`missing_units` lists), so the firing guard is not recoverable from the receipt alone (QUALITY 73 gap). This matches the v2 claims file's own wave-1 disclosure (R38ExecSelftests: "several red cases fail via `guards_ok` rather than the named clause"); my independent reading adds that c2-2/c2-3 are the same mechanism and that neither matches its label.

## 4. Instrument map (R36-CL4) vs committed instruments

`.ufo/waves/round-38/instruments.json` is committed at the freeze ✓, but:

- **`"frozen_at_commit": "{{FREEZE}}"` is a literal, unsubstituted template placeholder** in the committed blob (`instruments-at-freeze.json`) — the frozen map does not name its own freeze commit.
- Its note "Every instrument below is committed at the freeze commit" is **false for three entries**: `c1_receipts` (`corpus/evidence/round-38/c1/K*/after.json` — `corpus/evidence/round-38` is absent at the freeze, by design claim data), `controls_dir` (landed one commit later, `efd5c47a`), and `census_script` (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` — a fleet-repo path; the lane has no `scripts/` at the freeze).
- `tools/round-38/gen-controls.py` — the tool that built and scored the control fixtures — is committed at the freeze but **not listed** in the map, despite being edited between freeze and controls commit (§1).
- The map is already stale vs the in-flight v2: v2 adds `K*/before.json` receipts; the map's `c1_receipts` glob lists only `after.json`.

## 5. Falsifier ledger

| id | counter | variant (on real base bytes unless noted) | result | claim sentence violated |
|---|---|---|---|---|
| decoy-A2 | C2 (frozen) | duplicate `REA MCP server` row shadows the unresolved-pointer original | **exit 0, met_target** | "every … pointer … resolves"; QUALITY 77 duplicate-units |
| decoy-B | C2 (frozen) | bad pointer repaired by decoy document `corpus/evidence/doctor/` | **exit 0, met_target** | "repaired … to the same document"; QUALITY 77 intended-document |
| decoy-C | C2 (frozen) | second `## Owned axes` section with junk count | **exit 0, met_target** | "zero mismatches" over Owned-axes rows; QUALITY 77 every-occurrence |
| decoy-D | C2 (frozen) | second contradictory count in the same coverage row | **exit 0, met_target** | "the four stated counts equal …"; QUALITY 77 findall |
| E1 | C1 (frozen) | only triggering line *denies* the supersession | **exit 0, met_target** | "the round-38 frontier note supersedes the big-endian Frontier bullet" |
| E2 | C1 (frozen) | after-receipt omits `extraction_gaps` | **exit 0, met_target** | "carries no extraction gap" |
| E3 | C1 (frozen) | `provider.version = "9.9.9"` | **exit 0, met_target** | "run with stock unblob 26.6.4" |
| E4 | C1 (frozen) | duplicate S-id row (cited row opened 2026-10-25) | **exit 0, met_target** | "cites a SOURCES.md row opened 2026-10-26" |
| E8 | C1 (frozen) | junk bytes at all four pinned carrier paths | **exit 0, met_target** | "sha256 pins frozen" (pins never checked against bytes) |
| E9b | C1 (frozen) | duplicated oracle rows satisfied by one published file | **exit 0, met_target** | duplicate rows as separate units |
| (pre-satisfied) | C1 (frozen) | `frontier_note=true` at base and freeze with zero round-38 work | ctl-c1-0 | D1 |
| E5 | C1 (frozen) | row under a second round-38 heading | exit 1 (false negative) | blind spot |
| E10 | C1 (frozen) | registry row with 12 cells | exit 1 (false negative) | blind spot |
| decoy-A | C2 (frozen) | duplicate row without range compensation | exit 1 — **R3 range check caught the line shift** | (counter working as intended) |

Fixture bases: C2 decoys on a full `git archive` of the real base tree (base snapshot `3df29da2…`, decoy revs in the JSON argv); C1 E-decoys on the frozen selftest fixture machinery (green-sanity first, exit 0, validating the harness). All scripts and JSON receipts are in the artifacts dir.

## 6. Residual risks and verification gaps

- **Receipt provenance (QUALITY 78):** every green falsifier mints envelopes with the counter's own xpin — the counters verify integrity, never provenance. The wave's independent non-author re-run comparing semantic payloads remains the only provenance mechanism; nothing in this audit substitutes for it.
- I did not re-measure the v2 note's premise (unblob 26.6.4 `SquashFSExtractor` requiring `sasquatch-v4be` for BE v4; the v1 probe's `grep -v sasquatch` PATH flaw) — that is R38CrossToolK1's cited measurement; I audited identity, not the extractor behavior, and ran no REA.
- The v2 counter/claims are a moving target: all v2 statements here are timestamped observations of an uncommitted working tree (4 md5 states recorded), not an audit of committed bytes. Once v2 is committed, every finding in §2 must be re-checked against the v2 bytes; from the v2 diff, the binding code (frontier_note, sourced, province_core_row, coverage_map_row, matched, gaps semantics) is unchanged, so D1-D10 are expected to persist, and D11-D15 (C2) are untouched by v2.
- ctl-c1-1/c1-2 were scored on scratch fixture commits (`801e2019…`, `9f5b5b6f…`) that no longer exist; the receipts' argv is recorded but the fixture trees are gone (acceptable for controls, noted for reproducibility).
- I did not audit the census/reports/SCORECARD-integration surfaces (other seats' scope); `considerthese/` verified absent (the claim's one report line holds).

## 7. Tooling record

No tools installed or upgraded (operator authorization 2026-10-19 unused): only preinstalled `python3`, `node v26.12.0`, `git`, coreutils. No pacman transactions, no host services touched, no background jobs, no subagents. Scratch `/fast/scratch/hyaku/kaidoku-r38/R38ReviewerPredicateIdentity` (fixtures, frozen-blob extracts, counter scratch) removed after the report was written; all cited bytes are preserved under the artifacts dir.
