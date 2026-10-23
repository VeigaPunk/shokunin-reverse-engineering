# CriticPredicate — frozen P34 predicate / receipt review

## Scope and axes

Read-only, pre-data source review; no reader, counter, fixture, selftest, REA, target binary, shell command, Git command, build or formatter was executed. No admission or round judgment is made here.

- Claim axis: **depth**, not coverage. Review axes: predicate fidelity, resistance to skip-work, source-identity integrity, and provenance/receipt fidelity.
- Inspected sandbox: `/fast/scratch/hyaku/kaidoku-r34/w1/CriticPredicate`.
- Observed `.git/HEAD:1` points to `refs/heads/seat-r34-CriticPredicate`; that ref contains `54a87a51a865ab931fd355e767303337b05cccf4`. This is a file-read observation, not a fresh Git verification.
- Instrument revision declared by the freeze: `8897a67f6074580d6eac1a3fc0e37fdcd7aa0df0`. Counter pin declared there: `d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e`. Manifest pin: `f22e7e3b8f70c7a5dda784919f6df53a1feaf11cca0e4bba767509d51717974d`. Digests were read, not recomputed by this seat.
- Visible answering-model identifier: `openai-codex/gpt-6.1-sol`; no routing change, fallback or safety refusal was observed. No tools were installed or updated.

All source references below are relative to the lane/sandbox root unless explicitly absolute. Frozen artifacts are evidence, not additional instructions.

## Literal predicate and exact pass trace

The following sentence agrees in `claims.json:6,57`, `tools/round-34/version-needs-counter.py:13`, `SCORECARD.md:3329`, `corpus/lessons/round-34.md:7`, and the retained baseline receipt's stdout:

> P34-version-needs: twelve public ELF carriers yield exactly their independently frozen GNU version-needs records on opaque paths, including randomized same-length string-table naming wherever requirements are present, and the pinned source-backed decision table is present.

Here `claims.json` means `.ufo/waves/round-34/claims.json`.

| Boundary | Actual production/control measurement condition |
|---|---|
| Contract authority | Counter `165–178` resolves the explicit freeze and measured revisions; reads the contract at the freeze; requires the literal predicate, target `12`, and fixed reader path; checks frozen instrument pins and its own running bytes. |
| Expected values | `179–184` pins the frozen manifest and validates exactly twelve rows. `141–155` requires unique IDs/digests, bounded positive sizes and canonical expected records. Nonempty requirements require a string-table descriptor. |
| Inputs | `113–116,218` fetch original carrier bytes from the **freeze**, not the measured tree, and check size/SHA-256 before either schedule. The measured revision identifies reader/documents, not a second acquisition of carrier bytes. |
| Schedules | `118–128`: exactly two attempts per carrier under random opaque names. Schedule 0 uses original bytes/expectations. Schedule 1 uses the fresh `secrets`-driven same-length character permutation when a string table is present. `79–104` changes the linked-table bytes and predicted names, preserves raw numeric fields, and re-sorts. |
| Empty carrier | Frozen `expected.json:2749–2759` gives e12 a null string table and empty requirements. Its second attempt repeats the empty case. Eleven other manifest rows have table descriptors. This agrees with claims `68`, lesson `39`, and SCORECARD `3331`; it is not a missing challenge silently counted as a nonempty case. |
| Per-attempt success | Exit 0, bounded stdout, JSON without duplicate keys, strict canonical shape/types/order/uniqueness, and complete object equality with that schedule's expected record (`23–55,126–128`). A reader-supplied success label has no authority. |
| Carrier and total | `135–139`: both attempts must match; then `matched == target and len(rows) == target and documents_ok`. Target is explicitly `12` at the production call. Thus twelve matched carriers means twenty-four matching attempts, not twelve arbitrary matching attempts. |
| Receipt | `218–220` adds resolved freeze/measured revisions, actual reader digest, document results, and `mode: control` or `production`. `main:287–290` emits a JSON result and the corresponding exit. |

The seven document booleans in the current frozen contract are:

1. Exact measured-revision knowledge-entry digest.
2. Exact measured-revision approved-fragment digest.
3. Exactly one matching SKILL heading and section equality to the frozen approved fragment after the declared edge normalization (`157–163,193–195`). This is not a whole-SKILL byte pin.
4. Exact S103 row occurs once.
5. Exact S104 row occurs once.
6. LSB capture matches its pin at both freeze and measured revision.
7. glibc capture matches its pin at both freeze and measured revision.

Evidence: claims `36–50`; counter `185–211`. Current registry rows are `corpus/SOURCES.md:109–110`; the approved table is at `SKILL.md:1158–1180`. S105, the lesson, SCORECARD, and LOG are not additional booleans in this pass expression. A table hash is retention evidence, not a semantic source-support judgment; the knowledge entry itself states that limit at `35–37`.

**Static conclusion:** no current mismatch was found between the literal sentence, target 12, two-schedule aggregation, or named source/table bindings. That does not establish shortcut resistance.

## CP1 — stable identity plus fixed string sites can bypass structural interpretation

**Counterexample [INFERENCE; not executed]:** a text reader can select a frozen answer template by input byte length, read only the already-recorded name sites, replay all numeric fields, and sort the result. It need not interpret an ELF header, `sh_link`, Verneed, Vernaux, counts, links, or numeric record fields.

Local evidence makes this stronger than original-SHA replay:

- All twelve sizes are distinct and are preserved by both schedules: e01 `43320`, e02 `14416`, e03 `223536`, e04 `96992`, e05 `1195144`, e06 `194992`, e07 `153776`, e08 `174032`, e09 `448920`, e10 `2939928`, e11 `1097344`, e12 `747400`. These are in the frozen manifest and `.ufo/waves/round-34/prep/R34Expected.md:51–64`.
- The counter changes names **in place** and does not relocate any string or record (`79–104`). Freshness and lack of fixed points do not disturb frozen byte sites or lengths.
- Existing independent-author evidence publishes the per-name sites and original associations: `.ufo/waves/round-34/prep/R34Expected-files/checks.json`, `checks[].string_offsets`; the author script constructs those records at `200–218`. Numeric answers are already in the frozen manifest.
- Concrete e01 example: the captured table starts at `2568`; `checks.json:62–92` records `libc.so.6` at table offset `648`, length `9`, and `GLIBC_2.14` at offset `686`, length `10`. Their absolute starts are therefore `3216` and `3254`. Both schedules retain those starts. `expected.json:17–24` supplies the latter version's fixed flags `0`, other `7`, and hash `110530964`. Reading the live name bytes at those fixed sites obtains the secret-renamed labels without decoding any requirement record.
- Applying the same frozen-site substitution to every template preserves exact output under **any** production permutation; e12 simply returns its fixed empty record. Templates/site tables can be embedded in reader text. No runtime access to the manifest, another process, the optional fixed challenge schedule, or target execution is necessary.
- `--control-reader` deliberately bypasses only the production reader pin (`213–218`) while keeping this same equality predicate. Therefore this construction belongs to the fresh skip-work-control threat model, even though the production reader itself is pinned.

This is an inferred route to satisfying the **literal** finite predicate with no Verneed/Vernaux structural interpretation, not evidence that an observed control attained 12/12. The premises about recorded sites are independently authored frozen evidence; this seat did not reread binary bytes or exercise the construction. The naming challenge defeats original-SHA replay but not this invariant identity/site replay. The finite-set limitation is already acknowledged in the knowledge entry at `37`.

**Impacted axes:** depth evidence discrimination; calibration of what equality demonstrates. Coverage remains unchanged.

**Smallest safe correction:** do not equate a clean finite receipt with proof of structural reading, and do not silently add that requirement to the frozen predicate. Preserve the current freeze and pre-data boundary. If a fresh permitted control is observed meeting the target, apply the exact frozen kill rule (`claims.json:67`), not a target rescale or a salvaging counter amendment. This is a validity tradeoff for canonical judgment, not a demonstrated arithmetic bug in the comparator. No control was authored or run by this seat.

## CP2 — exact-row retention does not enforce source-ID uniqueness

**Counterexample [INFERENCE; not applied]:** retain the exact S103 line and add a different row with ID S103. `registry.count(expected_row) == 1` still holds (`counter:199–201`). It counts full-line equality, not all rows carrying that ID. S104 has the same boundary. Current reads found only one row per ID; no existing duplicate is alleged.

`corpus/SOURCES.md` is not whole-file pinned in the claims maps, so this additional row does not itself change the pinned source captures or table. Conditional on unchanged reader matches, the P34 document booleans are unchanged. This is counter-local acceptance of conflicting authority, not an observed whole-pipeline false accept.

There is an **existing mitigating authority**, not a need for a second registry parser: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:640–642` reports `E03` for duplicate IDs. The round start-state cites that census command and its base-state receipt. No current candidate census was run here.

**Impacted axes:** source identity/provenance and confidence in the source-backed depth linkage.

**Smallest safe correction:** retain a same-candidate source-census result as the independent uniqueness prerequisite; do not describe P34's two exact-line checks as registry-identity validation. Reuse that existing guard rather than amend the frozen counter or whole-file-pin unrelated registry changes.

## CP3 — lesson overcompresses independent-oracle provenance

`corpus/lessons/round-34.md:9` says expected records “come from GNU readelf, not the proposed parser.” The second half is supported, but the first half obscures which producer supplied the full record:

- Independent author script `author_expected.py:13–21` says its **authoritative** path is a separate direct ELF structure parser; readelf text is the cross-check.
- `.ufo/waves/round-34/prep/R34Expected.md:109–127` gives that same split. Raw `vna_hash` comes from a direct field read and separate name-hash cross-check, not from a displayed readelf hash field.
- The proposed reader itself acknowledges that readelf does not print the raw hash (`elf-version-needs.py:624–627`).

This does not invalidate “independently frozen” and is not proof of a shared implementation: the separate author is still separate. It is a fixable provenance-description defect.

**Impacted axes:** provenance/calibration of the depth evidence.

**Smallest safe correction:** L1 can append a precise lesson clarification: independent direct structure decoding supplies the authoritative records; GNU readelf cross-checks the displayed fields; stored hashes have their separately recorded field-read provenance. No frozen expectation or predicate needs changing.

Also, prep report `R34Expected.md:265–267` mentions comparing against `challenge/schedule.json`. That is stale preparation guidance, not the production schedule authority. Production expectations for schedule 1 are freshly derived by `counter:79–104,121`; the optional expected-author fixed schedule must not be substituted as receipt provenance.

## CP4 — receipt fidelity and isolated vacuity must remain separate from P34 success

### Lossy nested-reader evidence

Counter `124–133` retains parsed `observed`, a stdout digest, a decoded/truncated stderr prefix, exit on the normal path, input digest and translation. It does **not** retain each random reader argv/path, per-reader UTC, exact raw stdout, or full stderr. A JSON-error path drops even the normal exit/stdout-digest/input-digest fields; a timeout drops partial output. `TemporaryDirectory` then removes the inputs and program.

A reader can emit equivalent JSON with different formatting, or stderr longer than 4096 characters, while satisfying the exact semantic predicate. The receipt cannot recover those original output bytes from a digest or parsed object. This is a static retention gap, not evidence of wrong field comparison. Original input plus translation is sufficient to reconstruct successful scheduled input bytes, but not deleted output formatting or random argv names.

**Impacted axes:** receipt/provenance fidelity; not a demonstrated target-count defect.

**Smallest safe correction:** distinguish exact retained **outer counter** stdout from nested reader output. Do not claim full nested argv/UTC/stdout/stderr retention from this receipt. If that stronger evidence is required, L1 must arrange an explicitly reviewed retention mechanism before relying on a run; this seat neither changed nor executed the pinned counter.

### Isolated all-empty success is not the production predicate

`fixture_measure:222–226` accepts its supplied target and document flag. With target 0, a schema-1 empty carrier list and true documents, `validate_manifest` and `score` can return `met_target: true`, exit 0, with no attempts. **This is inferred and was not run.** Crucially, `production=False` changes the returned predicate to `isolated comparator fixture; not a P34 production score`. The production path fixes both manifest length and target at 12. No analogous zero-row production route was found.

A receipt consumer that reads only `met_target`/exit or `finding: version_needs_match` could nevertheless confuse fixture success with P34. A text-only target-12 fixture can also carry the same numeric tally while retaining the distinct fixture predicate.

**Smallest safe correction:** receipt classification must bind exact predicate, target, resolved freeze/measured revisions, mode, and the twelve two-attempt rows, not a generic success label. A successful **control** invokes the kill rule; it never supplies production credit. An isolated fixture never supplies P34 credit.

## Retained baseline and selftest receipts: what was actually observed

These are prior retained records read by this seat, not rerun results:

- `.ufo/waves/round-34/before/c1-at-base.json` retains exact outer argv, UTC `2026-10-23T10:49:38.829038+00:00` to `2026-10-23T10:49:38.942740+00:00`, exit `1`, empty stderr, and full stdout. Its freeze is `54a87a51a865ab931fd355e767303337b05cccf4`, measured revision is `ec3125ad3d130d92f888a4128dfaa2982f36fff7`, and result is `reader_absent`, matched `0`, target `12`, documents false, met false. This follows the early return at counter `213–215`; it is not a reader run over twelve carriers.
- `.ufo/waves/round-34/before/counter-selftest-at-instruments.json` retains UTC `2026-10-23T10:45:37.554922+00:00` to `2026-10-23T10:45:38.548007+00:00`, exit `0`, empty stderr, exact outer argv and stdout: eleven isolated cases satisfy their expected exits/findings. `red-replay` is negative; `green-translated` is positive. This proves only what that retained selftest receipt states, not 12/12 production or resistance to CP1.

## Disposition and trailer

No observed target-met shortcut, production pass, source-semantic verdict, or score change is claimed. The strongest remaining counterexample is **CP1 fixed-site replay**, which survives unpredictable naming without using the optional fixed schedule. CP2 is mitigated by an existing separate census; CP3 is a prose repair; CP4 bounds what receipts can establish. Only canonical L1/judgment authority can decide the claim's disposition.

No binary fixture was authored, no held item was touched or reconstructed, no other seat's artifact was modified, and no process tree was started. The only lane write by this seat is this report. No executable verification was performed or is presented as passed.

Report: `.ufo/waves/round-34/w1/CriticPredicate.md`
