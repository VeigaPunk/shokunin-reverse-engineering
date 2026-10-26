# Round-40 counter checklist — from the lane's counter-failure history

Seat R40C1CounterLessons, wave 1, 2026-10-26. Inputs: `corpus/QUALITY.md` (rows 1–82),
`corpus/lessons/round-35…39-verifier-spotcheck.md`, `tools/round-39/c1-counter.py`
(blob `182308e4…`, 969 lines), `tools/round-39/c2-counter.py` (blob `bc20933b…`, 783 lines),
`tools/round-39/sqfs-triage.py` v1, `tools/round-39/heldout-gen.py`, round-39 mutant reports
(`w2/R39W2{C1,C2}Mutants.md`, `w2/R39W2TriageMutants.md`), `plans/round-40-claims.md` (DRAFT).
All line numbers below are against the round-39 tip files as read this wave.

Every item is phrased so the round-40 counter author can turn it into a clause plus a selftest
case. Part A = failure classes with the check and a one-line test. Part B/C = clause-by-clause
review of the two round-39 counters and what the round-40 successor must change. Part D = the
pre-freeze ordering gate. Part E = named red-case minimum for each successor selftest.

---

## Part A — Failure classes → check → one-line test

### A1. Non-discriminating counter: accepts the thing it was written to refuse
- Class: counter green on forged/copied/decoy inputs (round-36 A1–A6 shadow rows and decoys,
  round-36 F1 re-hashed envelope, round-38 M38-6 stub-at-path; QUALITY 77, 78, 81).
- Check: every acceptance predicate is demonstrated red on the specific forgery it exists to
  refuse, before data; a green case for the *legitimate look-alike* (QUALITY 40) accompanies it.
- Test: score the counter on the forged input class it claims to refuse — exit must be 1 with
  the named clause false, while the legitimate look-alike stays exit 0.

### A2. Receipt integrity ≠ provenance (R39-CL5, the routed C1 defect)
- Class: stored-evidence-id recompute proves only that the author holds the producer's digest
  code; a fabricated envelope re-minted with the real rule passes every integrity clause
  (`w2/R39W2C1Fabricate.md`; QUALITY 78; `plans/round-39-claims.md:79` disclosed it).
- Check: provenance comes from an **independent re-run at scoring time by the counter itself**,
  compared as a semantic projection — never from re-hashing the committed envelope.
- Test: build the exact fabrication the lane demonstrated (oracle-derived files + re-minted
  evidence id + self-consistent provenance path) — counter must exit 1 on projection mismatch.

### A3. Post-scoring amendment / freeze drift (M38-1, M38-2; QUALITY 79, 80; R38-CL4)
- Class: counters, claims, generators or control inputs change between the first freeze and the
  score; a "pre-scoring" fix is claimed after any seat has produced claim data.
- Check: history-based drift check over every frozen path (claims doc, counter, runner, oracle,
  carriers, generator, gap rule, projection-field list, control inputs) — `git log FREEZE..REV`,
  not blob comparison — exit 2 `frozen_path_changed`, never `met_target`; a later restore does
  not un-block.
- Test: freeze → edit a frozen path → restore → measure: still exit 2 (history, not bytes).

### A4. Control inputs landing after the freeze (R39-CL4; QUALITY 80, 34)
- Class: kill-control generators/receipts first committed after the freeze, so the controls
  certify bytes the freeze never held (`CTL-C2-5/6` `.formatfix` inputs at `72359309`).
- Check: every control input + generator is committed and format-validated **in the freeze
  commit**; each control replays at the freeze revision to its recorded verdict.
- Test: `git log FREEZE..REV -- <control paths>` is empty and the replay exit equals the
  receipt's recorded verdict.

### A5. Missing exit codes / unbound receipts (R39-CL6; QUALITY 73)
- Class: score receipts carry no exit code; a receipt without argv/revision/instant cannot be
  re-audited (`l1/scores/*.json` had no exit-code field in round 39).
- Check: every score receipt embeds `exit_code`, `argv`, `rev`, `freeze`, and names anything it
  merely echoes as `caller_asserted`.
- Test: `jq -e '.exit_code != null and .argv != null' <each score receipt>` passes.

### A6. Substring / token-boundary defects (R35-D3 D-3 `S106` ⊂ `S1060`; r39 C1 mutant
`sid-bounds` survivor)
- Class: id matching without boundary lookarounds, or substring-anywhere text checks.
- Check: every id/surface token is matched with explicit boundaries (`S\d{3,}` with
  non-alphanumeric lookarounds); keep c1-counter's `SID_RE` pattern (c1-counter.py:79) — its
  removal is a live survivor.
- Test: registry holding only `S1060` → counter does not credit `S106`.

### A7. Placement: substring-anywhere section checks (R35-D4; QUALITY 54)
- Class: PROVINCE/README/SKILL checks that pass when the row sits under the wrong heading or in
  prose.
- Check: section-scoped parsing — extract the named section (`## Round-40 additions to Core`,
  `## Queue-drain craft` up to next `## `), then match rows inside it (c1-counter.py:150
  `section()` is the pattern).
- Test: the exact accepting sentence placed under `## Frontier` or in a prose paragraph → exit 1.

### A8. Shadow rows, duplicates, decoy documents (M36-3; QUALITY 77)
- Class: a second contradictory row/box, a later duplicate key, or a same-basename decoy file
  satisfies the counter while the scored surface says something else.
- Check: enumerate **every** occurrence (`findall`, not first `search`); keep duplicates as
  separate units; assert the counted population is bounded below at the base; bind a repaired
  pointer to the intended document named in the freeze (path **and** git object), not any
  same-basename file.
- Test: append a contradictory second row / drop in a decoy basename document → exit 1, with
  the decoy-materialised control recorded before data.

### A9. False absence claims (R38-CL1; QUALITY 82; M39-1)
- Class: "absent / exists nowhere on this host" argued from a sweep rooted at the wrong base.
- Check: any negative-existence clause names its sweep root(s) at the base the cited relative
  path is relative to; use `tools/round-39/absence-sweep.py` (18-case selftest) rather than an
  ad-hoc `find`.
- Test: fleet-root-only sweep exits 0 ABSENT while the item exists under the shokuknow root →
  corrected tool exits 1 PRESENT.

### A10. Unregistered instrument, no outer-CLI selftest (R38-CL2; QUALITY 61, 33, 68)
- Class: a gate/counter bound into admission has no SKILL registry row (entry command, verdict
  map, selftest spelling, pinned-value path) or is tested only through helpers.
- Check: register each round-40 instrument in SKILL.md with its verdict map; the selftest
  invokes the tool's **outer CLI** (`--selftest` through `main()`) and asserts exit code plus
  stable findings on green and red fixtures.
- Test: `grep <tool> SKILL.md@REV` finds the row; `python3 <tool> --selftest` exits 0 and prints
  the registered tally.

### A11. Mutant survivors = missing tests (r36: C1 2/10, C2 7/14; r39: C1 7 survivors + 1
equivalent, C2 9 genuine + 5 equivalent, interpreter 18/39 survivors)
- Class: the selftest/held-out set pins a narrower slice than the predicate leans on.
- Check: a mutant suite over every decision-bearing clause; each mutant scored on the triple
  `(exit, verdict, over-set name)` (QUALITY 71); every survivor triaged as either *missing test*
  (→ add the differential fixture **before the freeze**) or *equivalent* (→ recorded proof).
- Test: for each prior survivor class from `w2/R39W2*Mutants.md`, the successor's selftest has a
  named case that flips it; the mutant report lists zero untriaged survivors.

### A12. Self-reported verdicts trusted (M38-3 overstatement; QUALITY 72)
- Class: `met_target` decoupled from the counter's own numbers; a gate echoes the counter's flag.
- Check: the counter recomputes `met_target == (matched == target AND all bindings true)` inside
  itself (c2-counter.py has `met_target_consistent`; **c1-counter.py does not** — copy it), and
  any outer gate cross-checks it and drops rows whose reader crashed.
- Test: a mutant that forces `met_target true` with `matched < target` → `met_target_consistent`
  false → exit 2, recorded as a red selftest case.

### A13. In-place mutation of shared frozen inputs (M30-2; QUALITY 49, 51)
- Class: a tool rewrites a carrier/mutant it was handed; regeneration silently repairs it.
- Check: counters re-hash every input on each run (c1 `carrier_pin_ok` does); instruments that
  regenerate run only on private copies; exactly one seat may run a regenerating counter.
- Test: corrupt a carrier copy → counter exits 1 on the pin clause (c2 `carrier_corrupt` case),
  not a silent regeneration success.

### A14. Severability (R35-D3 D-1)
- Class: a claim's evidence is coupled to a sibling claim's data (C2 D-1 waited on C1's SOURCES
  change), so one stop cascades.
- Check: each counter is evaluable on its own inputs at a revision that holds only its own data.
- Test: run each counter at a rev with the other claim's data absent → evaluable (exit 0/1), not
  exit 2 `unevaluable`.

### A15. Domain guard (R39-CL1; planned item (b))
- Class: the interpreter labels envelopes outside its domain (non-`extract-firmware`, non-unblob)
  because it never reads `operation`/`provider.id`.
- Check: v2 interpreter applies the guard **before** row matching: non-matching
  operation/provider → `unclassified`, unconditionally; the counter scores that as a real
  decision class.
- Test: envelope with `operation: analyze` on a SquashFS carrier → `unclassified` even against a
  table whose only row would otherwise match.

### A16. Row coverage vs measured outcomes (R39-CL2, R39-CL3)
- Class: rows exclude real outcomes (mixed-symlink images K5/K6 get an action that contradicts
  their own gaps; P>0 damage and P=0 empty images have no row); the scored column is unscored.
- Check: v2 table has the mixed-symlinks row **ahead of** the escaping row; every held-out class
  (incl. partial-body-failure P>0, clean-empty P=0) has a row; the `action` cell is scored
  together with the label; labels unique per row.
- Test: interpreter on a both-link-kinds envelope → `mixed-symlinks` (not `escaping-symlink-
  removed`); a table with a right label but wrong action → counter exit 1.

### A17. Replicate diversity / shortcut population (draft v2; QUALITY 69, 67, 77)
- Class: N envelopes collapse to fewer real decisions; a memoriser or key built from surviving
  invariants reproduces expectations.
- Check: the generator makes the two replicates of a class differ in **non-decision** features
  (endian, comp, names, command text, where the `MaliciousSymlinkRemoved` typename is recorded);
  the counter reports `distinct_decisions`; fresh per-run content with the expectation derived
  from the generation is preferred (seed = freeze hash).
- Test: two replicates of one class have different carrier bytes but the same (label, action);
  the score receipt prints the distinct-decision count and a collapsed-replicate control is red.

### A18. Carrier screening before freeze (R28 case; QUALITY 43)
- Class: a frozen carrier list holds a carrier the tool refuses on input format, so the target is
  unreachable before any run.
- Check: every C1 carrier is screened before the freeze with the same input check the consumer
  applies — here the independent oracle's superblock/AVM-marker/LE-metadata parse — and the
  screen output is committed with the freeze.
- Test: the committed screen file covers all 4 carriers and each shows marker + LE metadata
  decode; a failing screen blocks the carrier from the frozen list.

### A19. Per-call tool pins (QUALITY 39; QUALITY 8/10)
- Class: a tool pin carried by the frozen invocation alone; receipts from a differently-versioned
  producer accepted.
- Check: the rerun receipt records resolved package version + that package's own `package.json`
  sha256 (rea-agents 6.5.0), unblob 26.6.4 command, sasquatch-v4be 4.5.1 digest on the child
  PATH; the counter rejects a run whose recorded pins differ.
- Test: rerun receipt with unblob ≠ 26.6.4 → clause false, exit 1.

### A20. Scratch-path identity vs byte identity (R36-CL6)
- Class: receipts point `subject.local_path`/`parameters.output_directory` into deleted scratch;
  path fields read as identity.
- Check: identity is `subject.digest.sha256` only; path fields are consistency clauses, never
  match keys; the projection comparison must exclude absolute paths and per-run fields.
- Test: same digest at a different path → matched; projection equality holds across two runs
  with different output directories.

### A21. Predicate/pin single source (QUALITY 68, 33; M34-5/6)
- Class: predicate sentence or pins differ between claims file, configs, counter constant and
  receipt; instrument map absent/malformed → vacuous CLEAN (QUALITY 66).
- Check: the freeze ships the instrument map in the claims file's `instruments` container; the
  counting command re-hashes pins from the claims file at each run; the freeze-integrity gate
  rejects absent/empty/malformed maps with a non-CLEAN verdict.
- Test: paraphrase the predicate in the counter constant → defect; map-free run → exit 3 /
  unevaluable, never CLEAN.

### A22. Negative controls scored before data (QUALITY 48, 50, 58; r36 skip controls left green)
- Class: a control that meets the target is discovered after data, forcing either a rule change
  (forbidden) or a dishonest pass.
- Check: do-nothing, round-39-receipts-copied, re-minted fabrication, marker-only relabel,
  marker-stripped body, receipts-in-freeze-commit (C1); base SKILL, v1-transcribed, catch-all,
  label-right/action-wrong, table+`*` default row (C2) — all scored by the frozen counters
  before the first data commit, receipts committed.
- Test: each control receipt exists at/under the freeze revision with its recorded exit ≠ 0
  (or forced redesign documented before data).

### A23. Carrier/vendor provenance registered (R37-CL2; QUALITY 1, 12)
- Class: third-party bytes (vendor images, Freetz notes) relied on without a provenance chain.
- Check: vendor members carry URL → image sha256 → member path/offset → member sha256 in the
  frozen spec; lane-built carriers name generator + seed + commit; external format notes get a
  SOURCES row before any claim rests on them.
- Test: spec entry with an empty provenance chain for a vendor-derived carrier → binding false.

### A24. Gate schema strictness (QUALITY 66; M34-2)
- Class: an integrity gate reports CLEAN when its input map is absent/empty/malformed.
- Check: the successor's map schema rejects missing keys, wrong shapes and empty lists with a
  distinct exit (3) and an unevaluable verdict — never vacuous CLEAN.
- Test: run the gate on the round-36-style mapless claims → exit 3 `instruments_missing`.

---

## Part B — `tools/round-39/c1-counter.py` review → clauses the round-40 successor must change

Keep (proven in round 39, reuse as-is):
- History-based `frozen_drift` (c1-counter.py:337) with exit 2 `frozen_path_changed`; restore
  does not un-block. Extend `FROZEN_PATHS` (:72) to the round-40 set (claims, counter, runner,
  `carriers.json`, oracles, symlinks, **gap-rule file, projection-field list**).
- `carriers_unchanged` (frozen vs rev bytes) in `met_target`.
- Section-scoped PROVINCE/README/SOURCES checks (:150, :504-537) with boundary-regex S-ids and
  the `opened` date + `used-by` bindings — with their red cases (province-row-outside-section,
  S1120, opened-earlier, used-by-lacks-entry, coverage-map-lacks-stem).
- Non-vacuity binding pattern (`symlink_coverage`, `xz_leg`, `carriers_spec_ok`) — extend, don't
  drop (see B3).
- Receipt `receipt_fresh` = first add is a strict descendant of the freeze and ≠ freeze
  (receipts added in the freeze commit fail — draft kill control).
- External read-only tooling through git objects; scratch under `HYAKU_SCRATCH` (`scratch_root()`
  :143) — keep, and add `--work`/TMPDIR honouring for the new REA re-run child.

Change:

1. **`run_provenance_ok` (:219) — replace, don't patch.** A self-declared substring
   (`/kaidoku-r39/`) inside a hashed envelope is claim, not provenance (A2); its mutants
   `prov-isabs` survives the selftest. Round 40 adds the **rerun binding**: the counter executes
   REA 6.5.0 itself (`cd "$S"`, `REA_UNBLOB_COMMAND` absolute, fresh outdir under its own
   scratch, sasquatch-v4be 4.5.1 on the child PATH), extracts the fixed semantic projection from
   the fresh run, and compares it with the committed receipt per carrier:
   projection = sorted (path-suffix, sha256) publication set + gap multiset (kind, path-suffix) +
   chunk-handler set + per-chunk `extraction_failed` flags. State in the counter docstring that
   evidence **ids are never compared across runs** — `parameters.output_directory` is inside the
   hashed 6.5.0 projection, so a fresh run's id necessarily differs (QUALITY 14/15); the
   committed id stays checked by the existing xpin recompute (:172) as *integrity only*.
   The clause list keeps `run_provenance_ok` only as a consistency hint, demoted to non-gating,
   or drops it.
2. **`first_add` (:313) — wrong direction.** It takes `git log --diff-filter=A … | tail -1`
   without `--reverse`; a receipt added pre-freeze, deleted and re-added post-freeze passes
   `receipt_fresh`. c2-counter.py:71 already does it right (`--reverse`, first line). Fix to
   `--reverse` + first entry, and add the red case (add→delete→re-add across the freeze).
3. **Non-vacuity bindings must encode the AVM layout, not just the marker (draft predicate).**
   Per carrier: `sqsh` magic + v4.0 + `mkfs_time == bytes_used` (BE reads) **and** the first
   metadata block length decodes as little-endian; the two decodes must differ, so the frozen
   generator/writer must emit a first metadata length ≥ 256 — otherwise the marker-only
   `gen-squashfs.py --endian avm` body (standard BE) satisfies the binding and kill control 4 is
   vacuous. Bind `avm_marker_all` + `le_metadata_all` over **every** carrier (not `any` — the
   r39 `xz_leg` uses `any`, whose version-check mutant survives, A11), plus distinct pins and
   gzip+xz legs. Add the missing-selftest fixtures for the survivors: non-v4 superblock must
   fail the leg binding (`xz-ver`), duplicate-gap and wrong-kind-gap receipts must fail
   (`gaps-set`, `gaps-kind`), wrong-content publication at an oracle path must fail
   (`oracle-nosha`), a relative `output_directory` must fail if the clause is kept (`prov-isabs`),
   and S-id-in-longer-token must not match (`sid-bounds`).
4. **Gap rule from a frozen artifact, not code.** The r39 rule is hardcoded
   (`gaps_ok` :285, kind `unpublished-entry` per in-tree link). Round 40's gap rule is fixed in
   the freeze "from development recon, never from carrier runs" — so it must be a frozen file
   (kinds + allowance) the counter reads at the freeze revision, listed in FROZEN_PATHS; the
   counter fails closed on an absent/malformed rule (A24 pattern). The rule file's provenance
   (development-image receipts it was derived from) is cited in the claims, not re-derived by
   the counter.
5. **`met_target` consistency check missing (A12).** Copy c2's `met_target_consistent`
   recomputation and its selftest cases; a C1 mutant that flips `met_target` without flipping
   `carriers_matched` must exit 2/1, never 0.
6. **`oracle_hits` (:276) duplicate-row and suffix-collision behaviour.** Two oracle rows with
   identical (rel, sha) let one published file score twice; `same_rel` (:229) endswith matching
   is fine but the spec should assert oracle rows unique (id, rel, sha) — add a
   `carriers_spec_ok` sub-check plus fixture.
7. **Rerun mechanics for the selftest.** The selftest cannot run real REA; factor the runner
   (`--rea-command` argv injection like the existing `--pkg65` xpin injection) so selftest
   fixtures drive a stub runner, and carry (a) green: stub projection equals committed receipt;
   (b) red: stub differs in one file sha / one gap kind → rerun binding false. Also keep the
   legitimate-look-alike green: two carriers sharing byte-identical oracle content both match
   (QUALITY 40).
8. **Receipt contract (A5, A19).** The score receipt the counter writes must include
   `exit_code` (0/1/2 + reason), `argv`, `rev`, `freeze`, per-run pins (rea-agents version +
   `package.json` sha256, unblob command + version, sasquatch-v4be sha256), and
   `caller_asserted` markers for anything echoed. R39-CL6.
9. **Registration.** SKILL.md registry row (entry command, verdict map `0/1/2`, selftest
   spelling, pinned-value path) — R38-CL2; `--selftest` already runs through `main()` (outer
   CLI, QUALITY 61) — keep.

## Part C — `tools/round-39/c2-counter.py` review → clauses the round-40 successor must change

Keep:
- Seed = freeze hash; byte-identical regeneration via the frozen generator (`carriers_regenerated`)
  **plus** committed-bytes equality (`carriers_committed`) — the pair that makes regeneration
  reproducibility, not tamper detection (QUALITY 51).
- `met_target_consistent` recomputation + its selftest cases (A12) — this is the counter c1
  should copy.
- `manifest_after_freeze` + `manifest_before_envelopes` (c2-counter.py:71 `first_add` with
  `--reverse` is the correct primitive — see B2).
- Writer sha binding (`writer_matches_manifest` :232) for the generator's writer dependency.
- Path resolution hygiene (`resolve()` :220 rejects absolute/`..`), envelope sibling inference,
  full-CLI `{ok,data,meta}` acceptance, lane-relative paths — all have selftest cases; port them.

Change:

1. **`envelopes_valid` (:~330) requires `operation == 'extract_firmware'` for every envelope —
   this contradicts the v2 out-of-domain class by design.** Change to: `digest_ok` (subject
   digest == carrier sha) required for all; `operation` recorded per envelope; the out-of-domain
   class expects `unclassified` **and** its envelope keeps a non-extract operation. Add the red
   case: all envelopes non-extract → their expected labels are `unclassified` and a table that
   labels them otherwise fails; an envelope with extract operation in the out-of-domain class
   also fails (class/arm consistency).
2. **Score (label, action), not label (R39-CL3).** The frozen generator assigns the pair before
   any REA run; the v2 interpreter prints both; expected = pair; the receipt reports
   `distinct_decisions` and the per-class expected pairs. Unique labels per row: the table
   parser must reject two rows with the same label (exit 2, malformed table) — that makes
   "label ⇒ row decision" true and kills the catch-all-plus-duplicate control.
3. **Marker uniqueness / shadow block (A8).** `table_block` (:87) reads the first v2 marker in
   the craft section. Add binding `v2_marker_unique` (exactly one marker occurrence in the
   section — `findall`), plus `v1_block_unchanged` (draft: block 18 byte-identical at rev vs
   freeze) so v2 work cannot silently rewrite v1. Red cases: two v2 markers with different
   tables → exit 1/2; v1 block edited after freeze → exit 1.
4. **Domain guard + action are interpreter features the counter must pin:** held-out classes
   `mixed-symlinks`, `clean-empty` (P=0), `partial-body-failure` (P>0), `body-extractor-failure`
   (P=0), `out-of-domain` — each with a row or the explicit `unclassified` fall-through. Use the
   replicate variation to pin the 18 surviving interpreter sites where real variation can
   (A17): one replicate carrying `MaliciousSymlinkRemoved` only in diagnostics vs only in
   `raw_result` (SR-raw-only); `-be` in a non-first command (BE-first-cmd-only); a
   `sasquatch`-substring basename that is not `sasquatch` (SQ-substring/no-basename); a
   non-squashfs handler in the chunk list (H-no-filter); two-gap envelope for G/D unions;
   P=0 vs P>0 vs P=2 for the published-files cells (RM-gt0-loose, RM-zero-loose, P-bool,
   P-plus-unpublished). The rest are interpreter-`--selftest`-only cases; both detectors are
   reported per mutant on `(exit, verdict)` triples (A11).
5. **`expected_label` fallback (:~305 `label if isinstance(label,str) and label else class`).**
   With unique labels required, drop the fallback: a manifest row without an explicit expected
   label is a malformed manifest (exit 2), not silently graded by class name — otherwise a
   class-rename relabel passes.
6. **Controls in the freeze (A4).** The kill-control inputs (base SKILL, v1-transcribed,
   catch-all, label-right/action-wrong, table+`*` row) plus their generators are committed in
   the freeze commit and format-validated there (a `--validate-controls` mode); each replays at
   the freeze revision to its recorded verdict. R39-CL4.
7. **Generator erratum.** The `corruption_bad_minor` docstring erratum in `heldout-gen.py` is
   frozen bytes — the round-40 generator must fix it **before** its freeze (afterwards it is
   disclosure-only, QUALITY 79 pattern).
8. **Receipt contract** as B8 (exit codes, argv, pins; R39-CL6).

## Part D — Pre-freeze ordering gate (both counters)

In the freeze commit itself (verified by a gate, exit 0 required before any data commit):
1. claims file with `instruments` map (QUALITY 68) and predicate sentence byte-identical across
   claim/config/counter constants (QUALITY 68, A21);
2. both counters + runner + v2 interpreter + generator + writer + gap rule + projection-field
   list, format-valid (QUALITY 33/38: instrument committed before data, refuses pre-instrument
   data);
3. C1 carriers + oracles + symlinks + pins; AVM screen output for every carrier (A18);
4. C2 control inputs + generators, format-validated (A4);
5. selftest red/green receipts for both counters at the freeze bytes (QUALITY 61);
6. SKILL registry rows for every instrument (A10);
7. before-receipts / do-nothing control receipts (scored before data; QUALITY 48/50).

After the freeze: data commits only (receipts, envelopes, manifest, held-out carriers) — any
touch of the above is exit 2 forever (A3).

## Part E — Minimum named red cases per successor selftest

C1 (beyond porting the 32 r39 red cases):
1. re-minted fabrication (oracle-derived) → rerun projection mismatch, exit 1 (A2 — the case the
   r39 counter demonstrably lacks);
2. receipt add → delete → re-add across freeze → `receipt_fresh` false (B2);
3. stub rerun differing by one file sha / one gap kind → rerun binding false (B7);
4. marker-only standard-BE carrier relabelled as AVM → `le_metadata_all` false (B3);
5. genuine AVM body with marker stripped → `avm_marker_all` false (draft kill control);
6. non-v4 superblock satisfying leg binding → `xz_leg`/leg binding false (`xz-ver` survivor);
7. duplicate gap kind / wrong-kind gap with real path / wrong sha at oracle path /
   relative output dir / S-id in longer token (the five r39 survivors' fixtures);
8. `met_target` forced true with matched < target → `met_target_consistent` false (A12);
9. legitimate look-alike green: two carriers with identical oracle rows (QUALITY 40).

C2 (beyond porting the r39 set):
1. out-of-domain envelope labelled by a row → exit 1 (A15);
2. right label, wrong action → exit 1 (A16);
3. duplicate row label in table → interpreter exit 2 (C2);
4. second v2 marker / edited v1 block → exit 1/2 (C3);
5. collapsed replicates (both replicates identical bytes) → `distinct_decisions`/diversity
   binding false (A17);
6. catch-all row and table+`*` default row → out-of-domain envelope mislabelled → exit 1;
7. manifest without explicit expected label → exit 2 (C5);
8. control input committed after freeze → exit 2 `frozen_path_changed` (A4);
9. per-replicate feature-site fixtures for the SR/BE/SQ/H/G/D/P interpreter survivors (C4).
