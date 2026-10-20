# Round 15 — AttackAdmission (critic: admission, independence, inflation, numeric provenance, frontier)

Seat: `KaidokuR15.AttackAdmission`. This is an author-side critic seat with no subagents. It is **not** an independent reviewer: all 32 members of `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/swarm-registry.json` are `KaidokuR15.*` spawns.

Methods: read-only source and inventory commands only. I did not run any gate, selftest, `measure.py`, `snapshot-inventory.py`, build or provider. I read installed bytes once, in a Python cell, to test one counterexample (A3). That read is critic evidence, not the admitted measurement. Access date: 2026-10-20. No tools were installed or updated.

Abbreviations:
- L = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- INST = `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang`
- S003 = installed `Base-src.zip`. Its SHA-256 is `f00d29c2…a8d804`, which matches the registry pin; I re-hashed it.

## Verdict

Both claims can be admitted, but only in narrower form than `L/.ufo/waves/round-15/claims.json` states:

- **C1 (depth): admissible only on new content.** Credit applies only to pinned digests, per-minor patch coverage, the "all"-key finding that the OS/arch branch is vacuous, and log signatures. A file existing (0→1) proves nothing. As worded, claims.json:6 also overstates one of the discriminators (A3).
- **C2 (calibration): admissible only as a bounded correction.** It is a mandated conformance duty (A1), not a capability, and not a second discernment event.
- **Calibration and discernment verdicts stay pending** until a non-author closure samples them. No r15 seat can provide that sample.

## Findings

### A1 — C2 counts a mandated, status-neutral duty as axis improvement (high; impacts calibration)

**Counterexample.** C2 claims "calibration" for closing both routed defects.
- The round prompt makes this mandatory. `/home/vgpnk/Projects/shokunin/.ufo/prompts/kaidoku-round-15.md` §5 item 5 says: turn every routed defect "into a lesson-backed `QUALITY.md` criterion or fix, or say in the report why not."
- The closure labels both defects **status-neutral**: `L/corpus/lessons/round-14-verifier-spotcheck.md:171-172`.
- The same closure already credited **discernment improved** for this outside sample (`:167`). r14's own critic recorded that one event must not be counted twice: `L/.ufo/waves/round-14/w1/AttackTrends.md:77`.

**What is still legitimate.** Two statements were actively wrong, and superseding them is a real calibration fix:
- QUALITY #16 says "does not grade", but the code grades raw substrings at `L/.ufo/waves/round-14/tools/quote-fidelity.py:256-257`.
- Lesson Gate row 1 still cites the flawed advisory as support: `L/corpus/lessons/round-14.md:18`.

**Smallest safe correction.** Record C2 as "required duty discharged; calibration improved only by superseding two active misstatements."
- No capability row.
- No reset of the stagnation interval. Compare r14 `SCORECARD.md:2225-2228`, where a demonstrated capability did reset it.
- No new discernment credit for the same outside findings.
- Numeric proxy: 10.0→10.0, delta 0.

### A2 — C1 "before 0 → after 1" is true by construction; r14 seats already held the listing (high; impacts depth)

**Counterexample.** claims.json:6 says "Before no round15 inventory/decision record; after one". `L/.ufo/waves/round-15/measure.py:91-92` measures only whether `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md` and the tool file exist. At baseline `9719dd2`, a file named `r15` cannot exist, so the "before" value is fixed at 0.

The installed listing itself is old. r14 author-side artifacts already recorded it:
- `L/.ufo/waves/round-14/w1/AttackNovelty.md:38,107-108`: 11 base files, 0 `go1.2[56]` diffs.
- `L/.ufo/waves/round-14/w1/ReviewGoInference.md:32,56`: S003p, `go1.26.0.json` absent.
- `L/.ufo/waves/round-14/w1/GoEntryDraft.candidate.md:43,89`: 11 / 0 / 123 / 0 / 9.
- `L/.ufo/waves/round-14/w1/SnapshotBootstrap.md:26,180`.

None of these reached the admitted entry. The r14 entry only asks for this evidence, at `:76-77` ("Pin installed data…", "Distinguish absent base file from OS/architecture exclusion").

**Numeric-provenance trap.** r14 seats disagree on the diff count: SnapshotBootstrap.md:26 says "89 diffs", while GoEntryDraft.candidate.md:43 says 123. The r15 entry must cite only the fresh inventory output, never r14 seat counts.

**Smallest safe correction.** The depth verdict cites content deltas, not file presence. `KaidokuR15.AttackNovelty` reached the same set independently (`L/.ufo/waves/round-15/w1/AttackNovelty.md:66-108`, N1–N7); it is also an author seat. The admissible deltas are:
- full per-file SHA-256 values;
- per-minor patch coverage and fallback targets;
- the "all"-key finding (A3);
- the log signature that separates missing from present base;
- `-cgo` keys that are never selected.

Without these, C1 repackages r14.

### A3 — "Discriminates OS/architecture applicability" is false as a live alternative on this host (high; impacts calibration and depth)

**Counterexample** (source anchors plus the critic's installed read):
- S003 `GoApiSnapshot.java:108-109`: the search order is always `[goOS-goArch, goOS, unix|"", goArch, "all"]`.
- `:216-224` keeps every listed key that is present.
- `:503-505`: `isInvalid()` is `arches.isEmpty()`.
- Installed bytes: all 11 `INST/go1.*.0.json` files have a top-level `"all"` dict (`dict`, 2 members).
- All 123 `INST/patchverdiffs/*.diff` files have zero `@` paths of length ≤1. The first path element counts are `all` 58,666, `darwin` 5,046, and so on.
- For `go1.25.0.json`, `runtime.moduledata` appears only under `all` (all other 26 top-level keys: False).

**Consequence [INFERENCE: not executed].** For every GOOS/GOARCH, a present installed base yields a non-empty `arches`, so the snapshot is valid. On Ghidra 12.1.4 as installed, an invalid snapshot comes only from a missing base file. The r14 entry's sentence at `L/corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md:51-54` is a general source possibility, but it cannot be reached on this host.

**Limit.** This holds for these bytes only. I did not read the `JsonPatchApplier` semantics.

**Smallest safe correction.**
- Reword C1 to "missing base vs present base (plus patch-fallback level); OS/arch exclusion checked and vacuous here."
- Add a bounded, append-only qualification of r14 `:51-54` in the r15 entry.

### A4 — Lookup-scope and inventory facts rest partly on unregistered bytes; used-by cells point at files that do not exist (medium; impacts calibration)

1. **Lookup scope uses an unregistered source.** "INST is the only lookup root" depends on Generic `Application.java:954-963`: `getModuleDataFile` resolves against the calling class's module and then `findModuleFile(DATA_DIRNAME + …)` at `:355-367`. That archive (`…/Ghidra/Framework/Generic/lib/Generic-src.zip`, SHA-256 `391951647be9c4244053034791679457a99728383d94dbcd33bf1708734e9de0`) is not in `corpus/SOURCES.md`.
   - I also checked that the only installed `data/typeinfo/golang` directory is INST.
   - The one user extension, `~/.config/ghidra/ghidra_12.1.4_PUBLIC/Extensions/ghidra-emotionengine-reloaded`, has no `typeinfo`.
   - Either L1 opens a row, or the entry marks this scope fact as an unregistered observation.
2. **S023 covers one file only.** The uncommitted S023 row in the worktree registers only `go1.25.0.json`; its digest `54d10162…6252` matches. Inventory facts about the other 10 bases, the 123 diffs and the 9 GDTs have no registry row. Either cover them with the inventory output's digests plus an explicit "observed installed data" label, or scope the claims to S023.
3. **Dangling used-by cells.** The S003, S007 and S023 used-by cells now name `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md` and `corpus/lessons/round-15.md`. Neither file exists at the time of this read.
4. **Obligations from the round prompt** (`kaidoku-round-15.md` §2 item 1):
   - a lesson `## Gate` row for S023;
   - old→new logs for the two used-by changes.
   - S023's locator is a JSON path. The value at `all.Types.runtime.moduledata.Fields[1]` = `{"Name":"pcHeader","DataType":"*runtime.pcHeader"}` matches the row (verified). Under QUALITY #17 this needs a manual check, not a `quote-fidelity` submission.

### A5 — Integration came before the candidate seats; the before-record states a status it cannot show (medium; impacts calibration and provenance)

Observed mtimes (`stat -c %y`):

| Time (−03:00) | Event |
|---|---|
| 03:54:21 | `claims.json` written |
| 03:55:10 | `corpus/QUALITY.md` (#17), `corpus/lessons/round-14.md` and the r14 entry correction edited, 49 s after claims |
| 03:55:55 | `sources-before.json` written |
| 03:56:15 | `swarm-registry.json` written |
| 03:58:18 | `corpus/SOURCES.md` S023 added |
| 03:58:40 | `ReviewSources.md` written |
| 03:59:08 | `AdvisoryCorrection.candidate.md` written |
| 03:59:35 | `CriterionDraft.candidate.md` written |

- The landed C2 text came before every seat output and before the registry. The candidate seats therefore review text that had already landed; they did not draft it. L1 must not cite them as its origin or as pre-integration review.
- `L/.ufo/waves/round-15/sources-before.json` says "Executed at round start … before changes; initial git status empty", but it was written 45 s after the corpus edits and carries no execution timestamp.
- SOURCES.md stayed at baseline until 03:58:18, so the validator verdict is plausibly a valid baseline result [INFERENCE]. The "status empty" clause cannot be verified from the bytes.
- **Correction:** record the actual execution time and pre-change status, or narrow the wording to "SOURCES.md unmodified at execution".

### A6 — No r15 seat is outside evidence (high; governance)

- `swarm-registry.json`: 32/32 agentIds are `KaidokuR15.*`. That includes the 6 reviewers, 4 critics (this seat among them), 2 sentinels and 2 revengers.
- The precedent is r14 `SCORECARD.md:2222-2223` ("No author-side seat counts as the current round's independent reviewer") and the round prompt's "independent non-author verification remains required".
- The r14 closure's agree/disagree sample belongs to r14. It must not be reused as r15's sample.

**Correction:** r15 reports calibration as author-side and closure as pending, and makes no discernment claim from its own seats. Convergence between seats (for example AttackNovelty and this report on A3) is author-side corroboration, not independence.

### A7 — Frontier step: the planned real-carrier move was replaced, and the stated blocker is inaccurate (medium; impacts depth and calibration)

- r14 `SCORECARD.md:2230-2233` planned "one depth/capability claim to discriminate bootstrap failure on a caller-selected real Go carrier with retained analyzer diagnostics". r15 C1 is a source/installed-data inventory instead.
- The candidate carrier bytes are present locally: `/var/cache/pacman/pkg/1password-cli-2.40.0-2-x86_64.pkg.tar.zst`, 14,543,312 bytes, pinned by r14 `ReviewGoInference.md:35`. The ClaimSeparation seat's framing ("missing caller-selected target") is therefore inaccurate.
- The actual blockers are:
  - (a) this wave's contract forbids target/provider execution;
  - (b) there is no operator/caller selection or authorization for that run.

**Correction.** Record the plan as **deferred, not done**, and name the blockers.
- C1 is a preparatory depth step. Its log signature (missing base emits neither `Falling back…` nor `Using Go API snapshot for…`, per `GoApiSnapshot.java:111,122-126,158-164`) sharpens a future retained-log run.
- C1 does not discharge the planned frontier move.

### A8 — The lowest-axis tie has no stated tie-break (low; impacts calibration)

- claims.json:12 says "three owned proxies tie at 10; calibration worked" but names no tie-break.
- Lane precedent is the most-falsifiable-next-claim tie-break: `SCORECARD.md:1342-1343,1423`.
- Coverage has not been worked as a claim in r13 (`:2144`), r14 (`:2191`) or r15.

**Correction:** state the tie-break and why depth and calibration win over coverage.

### A9 — C2 text and measurement gaps (medium)

1. **Correction text skips the first hop.**
   - The landed correction (`L/corpus/lessons/round-14.md`, appended `## Round-15 correction — virtual-dispatch advisory`; entry `:108-117`) cites only `GoRttiMapper.java:380-386` and `GoTypeManager.java:405-455`.
   - The step from `registerStructures` to `getType` is DataTypeMapper `:207-210` → `:172-176` (`getType(structNames, Structure.class)`) → `:310-313` (the List overload calls `getType(String, Class)` virtually).
   - I verified the full chain in S003, including `GoTypeManager.java:449` `apiSnapshot.getTypeDef`.
   - Fix: add the DataTypeMapper anchors in the r15 lesson or LOG.
2. **Line range.** The flawed advisory lines are `ReviewGoInference.md:57-58` plus the support claim at `:61`. Line 56 is a correct installed observation and `:59` is an honest UNKNOWN. The corpus text follows the closure's "57–61", which is acceptable; FrontierScribe's "56-58" would wrongly mark `:56` as flawed.
3. **Correction placement.** The inline pointers at `round-14.md:18,76` are byte-identical to baseline, so the correction is append-only and separate from them. That is the most the append-only rule allows. The closure also asks for a **LOG** correction (spotcheck `:171`); none exists yet.
4. **`measure.py` weaknesses:**
   - `:96` uses substring `C2_MARKER in lesson`; it should anchor `^## ` plus the marker.
   - `:92` measures that the tool exists, not that the inventory is reproducible.
   - It does not check that gate/fixture pins are unchanged, although the claim asserts "no quote gate implementation change".
   - It does not check that `ReviewGoInference.md` bytes are unchanged.
5. **QUALITY #17 over-narrows exit 2.** It says "Exit 2 denotes the documented malformed/tampered inputs". Exit 2 also comes from:
   - the internal-exception catch-all at `quote-fidelity.py:828-832`, reported as `invalid_manifest ident=gate`;
   - argparse usage errors (`SystemExit`, not caught).

   Separately, a rendered-origin quote whose text happens to occur raw would grade exit 0 (`:256`). "May return exit 1" is honest, but #17 should say that a green result on a non-raw representation is not evidence. Low severity.
6. **Boundary fixture: static prediction holds.**
   - `raw-source.md` SHA-256 `2e80083b…8270` matches the manifest pin.
   - The rendered quote `Use raw bytes.` is absent from the raw text, so `:256-257` gives `quote_not_contiguous@rendered-text`, exit 1.
   - The extra top-level `provenance` key is tolerated: `parse_manifest` uses `.get` at `:173-181`.
   - No frozen expectation pins these fixtures. The r14 frozen run pins explicit paths only (`:300-347`), so it is unaffected; but the r15 expected outcome currently lives only in prose.

## Numeric provenance (critic observations; L1 must re-derive)

| Item | Value | How observed |
|---|---|---|
| HEAD / baseline | `9719dd2…` (closure commit by protocol-shokunin) | `git rev-parse HEAD`; `git show --stat` |
| Worktree corpus diff at read time | QUALITY +1; SOURCES +5/−2 (S003/S007 used-by, S023, search log); lesson r14 +17; r14 entry +11 | `git diff --stat` |
| Base JSON / diffs | 11 / 123; 1.25 diffs 0; 1.24 max `.6` | `ls INST`, `ls INST/patchverdiffs` |
| `"all"` dict present in bases | 11/11 | Python `json.load` (critic) |
| Top-level-only diff paths | 0 of 123 files | Python parse of `@ ` lines (critic) |
| Source rows | 22 at baseline → 23 if S023 lands (A tier +1) | registry diff; registry growth, not an axis score |
| Owned proxies | 10.0 / 10.0 / 10.0; delta 0 | `SCORECARD.md:2189-2191` |

## Proposed L1 checks (not run by this seat)

1. Run `python3 L/.ufo/waves/round-15/measure.py 9719dd232687f5ee78a4ed323b37f8810e833d10` and again on the after revision. Report booleans as presence only, never as axis deltas.
2. Run `python3 -I L/.ufo/waves/round-15/snapshot-inventory.py` twice. Commit the stdout and confirm the SHA-256 of the two runs is byte-equal. Spot-check against `sha256sum INST/go1.*.0.json`.
3. Confirm the A3 claims from the inventory output: every base has an `all` container. Grep the diffs for top-level-only paths: `grep -h '^@ \["[^"]*"\]$' INST/patchverdiffs/*.diff | wc -l` should be 0.
4. Check that gate pins are unchanged:
   - `git -C L diff --quiet 9719dd2 <after> -- .ufo/waves/round-14/tools .ufo/waves/round-14/fixtures .ufo/waves/round-14/measure.py .ufo/waves/round-14/w1/ReviewGoInference.md`
   - `git -C L diff --quiet 9719dd2 <after> -- corpus/lessons/round-14-verifier-spotcheck.md`
5. Check append-only edits: `git -C L diff --numstat 9719dd2 <after> -- corpus/QUALITY.md corpus/lessons/round-14.md corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` should show 0 deletions. For SOURCES.md, only the used-by cell deltas should appear, logged old→new in `corpus/lessons/round-15.md`.
6. Confirm `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md` and `corpus/lessons/round-15.md` exist and are mapped in the README coverage map (missing/dangling empty). Then run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`, expecting exit 0.
7. Run the boundary fixtures and record argv/exit/stdout in a round-15 verification record. Expected: raw exit 0; rendered exit 1 `quote_not_contiguous@rendered-text`. Also run the existing `--selftest` and `--frozen L/.ufo/waves/round-14/fixtures/expected.json`.
8. Grep the r15 SCORECARD/report text for any capability row, stagnation reset, discernment credit from r15 seats, or wording that "OS/arch" is a live cause. Each must be absent.
9. Confirm a LOG append names the correction, the DataTypeMapper `:176,310-313` anchors, and the A7 deferral with its blockers.
