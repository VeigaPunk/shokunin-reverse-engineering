# FAttackCausalityFinal — round 16, wave 2 critic (author side, advisory)

Axes: **depth**, **calibration**. Target: the new entry, SKILL, lesson, LOG, README and SOURCES text must not claim (a) the old target's cause, (b) parity with the compiled provider, or (c) effective patched buckets for the current installed artifacts. I attacked the current worktree files. `selection.py` changed while I was reviewing it; line numbers below are from my second read (315 lines). Paths are relative to `kaidoku-shokunin/` unless absolute.

## Verdict

**(a) Old-target cause and (b) compiled-provider parity:** I found no overclaim (bounded no-finding; see below).

**(c) Effective patched buckets:** no current text claims them. One fixable assurance gap (F1). One counterexample against a sibling's proposed strengthening (F2).

Two calibration items that overlap with siblings, listed only so the record is complete:
- The "exercised 1.24.5" contrast and the missing `verification.json`. Already reported in `w2/FAttackNoveltyFinal.md:14-24`, `w2/FAttackProvenanceFinal.md:37-48,76-77` and `w2/FReportEvidence.md:70-74`. I agree with them and do not repeat their corrections.
- README guidance does not follow the new QUALITY #18 (F3).

## F1 — Fixable: nothing pins the "unpatched" bucket label (calibration, low–medium)

**Counterexample.** Change `selection.py:280` from `"base_matching_buckets_source": "unpatched_base_file"` to `"effective_patched"`, or delete the key. Every current fixture still passes:
- `selfcheck.py:89` forces only `patch_applied` and `evidence_class`.
- No case's `expected` mentions `base_matching_buckets_source`. A grep over `selection-fixtures.json` and `negative-fixtures.json` finds no hits. The diff-selected cases are `exact_diff` (:38-48), `lower_fallback` (:63-73) and `corrupt-diff-still-selected` (:231-240).

This key is the only machine-readable marker that the entry (`…r16-go-selection-preview.md`, table row `base_matching_buckets` and Limits "All bucket results are unpatched") and `SKILL.md:501` rely on when a diff is selected. `patch_applied:false` does not say what the bucket list was computed from.

**Smallest correction.** Add hand-written expectations only. Do not change `FORCED`, because `missing_base` legitimately emits `null`:
- `exact_diff`, `lower_fallback`, `corrupt-diff-still-selected`: add `"base_matching_buckets_source": "unpatched_base_file"`.
- `missing_base_despite_diff` (selection-fixtures.json:3): add `"base_matching_buckets_source": null`.

These are label values, not hashes.

## F2 — Counterexample to the proposed "bucket invariance" claim (depth, calibration)

`w2/FFrontierAudit.md:66-72` (F7) proposes to "assert the invariant as a source-model observation". The data part is sound, and I deepened it:

- **Path depth.** I parsed all `@` section headers in the 123 installed diffs: 82,579 sections in total. Path length is 3 (5,288), 4 (73,869), 5 (2,040) or 6 (1,382). There are no sections of length 0, 1 or 2.
- **Source law.** S003 `JsonPatchApplier.java:75-94,122-155`: `applySection` changes only `path[-1]` under `findParent(path[:-1])`. With length ≥3, neither a top-level bucket nor a bucket's direct children (`Funcs`/`Types`) can be added or removed.
- **Top-level keys.** For all 11 bases, every top-level key a same-minor diff names exists in the base.

So, **if** application succeeds, the effective top-level bucket names equal the base names for every installed diff ([INFERENCE FROM SOURCE + DATA]).

That conditional is exactly the gap. The repo's own fixture `negative-fixtures.json:223-241` (`corrupt-diff-still-selected`) is the counterexample. The preview reports `exact_diff` with `base_matching_buckets:["all"]`, but in source:
- `JsonPatch.read` throws `IOException("bad start of patch section")` (`JsonPatch.java:188-190`). It runs inside the derived-provider producer (`GoApiSnapshot.java:134-140`).
- `get` declares and propagates the exception (`:102-116`).
- `GoRttiMapper.java:174-187` catches only `CancelledException`.

The effective outcome is therefore a mapper-construction failure, not an empty snapshot and not those buckets. The same happens if `findParent` throws at depth ≥2 (`JsonPatchApplier.java:149-158`). A derived-cache entry keyed by base FSRL plus the requested `go%s.json` name (`GoApiSnapshot.java:133-135`), not by diff identity, could also serve bytes from another diff ([INFERENCE]; the entry's cache limit already covers this).

`selection.py` never parses diffs (`:240-245` only hashes them), so it cannot emit the invariant per run.

**Smallest safe correction.** Keep the current "unpatched / effective content unknown" wording (entry Limits; `SKILL.md:501`; lesson `round-16.md:20`). Do not relabel `base_matching_buckets` as effective or "presence-invariant" in tool output. If L1 wants the corpus fact, record it as a dated observation about the installed diff files, with:
- the producing argv retained under QUALITY #18;
- an explicit "only if application succeeds; not observed in Ghidra" condition.

Otherwise leave it out this round. Small wording fix: `lessons/round-16.md:20` says S003 "actually applies" a diff. The evidence is a source reading, so "source defines a derived provider that applies" is more accurate. Same for the `selection.py` docstring phrase "would be merged at runtime (134-144)": "patched by `JsonPatchApplier` per source".

## F3 — README recheck spelling vs new QUALITY #18 (calibration, low)

`corpus/README.md:36` gives `python3 -I .ufo/waves/round-16/selection.py --root <installed-golang-dir> …`. That is a relative path plus a placeholder. The exercised spelling to be retained is the absolute argv in `SKILL.md:506`, and QUALITY #18 (`corpus/QUALITY.md:28`) requires guidance to match it "or explicitly name an unexercised variant".

**Fix.** Either use the SKILL argv, or add "(unexercised template; recorded argv: SKILL go-selection-preview row)". The row's `verification.json` reference is pending; see the siblings above.

## Bounded no-finding

**Old target cause.** No new text links a selection result to the historical `op` failure:
- the entry's `UNKNOWN` paragraph (:11);
- `SKILL.md:489-507` (no causal text);
- `LOG.md:1936-1938` ("no … historical-cause proof");
- the lesson's reject row (`round-16.md:22`);
- `SOURCES.md:47`;
- the r14 correction (`2026-10-14-r14-02-final-sweep.md:197-207`) and the r15 correction (`…r15-go-snapshot-inventory.md:76-91`).

No fixture or note mentions 1.26 or `op`. w1 `AttackCausality.md`'s point that selection is not recovery still holds and is reflected in the text.

**Compiled-provider parity.** Every new document says "source model". The entry discloses that `Base-src.zip` is not authenticated against the loaded classes, plus the single-root, derived-cache and parser-strictness limits. I spot-checked two parity edges against source outside S003 (`Ghidra/Framework/Generic/lib/Generic-src.zip`, `ghidra/framework/Application.java`; **not a registered source**, so do not cite it in the corpus without a row):
- **Directory named like a diff or base.** `getDataFileInModule` throws `FileNotFoundException` for directories (`:369-372`), so Java returns null and probes a lower patch. Python's `is_file()` is false, so it also continues lower. They agree.
- **Module scope.** `getModuleDataFile(String)` resolves only the caller's own module (`:954-962`), so user Extensions are not consulted ([INFERENCE]: the caller's module is Base). On this host, `find` shows exactly one `typeinfo/golang` tree in the install tree and none under `~/.config/ghidra`. The one installed extension has no `typeinfo`. So the single-root limit is benign today. It is not a runtime claim.

S003 anchors used by the entry are correct: `:108-111`, `:122-126`, `:128-131`, `:148-166` (warn at :158-160), `:168-178`, `:180-181`, `:183-192`, `:230-232` and `:239`. `GoVer.toString`/`prevPatch`/`withPatch` (`GoVer.java:134-140,155-159`) keep the major and minor version fixed and emit `M.m.p`, which supports the canonical filename regex.

## Commands and limits

All read-only. I did not run `selection.py`, `selfcheck.py`, `controls.py` or `measure.py`, or any build, test or linter.
- `unzip -p` reads of `Base-src.zip` members (`GoApiSnapshot`, `JsonPatch`, `JsonPatchApplier`, `GoVer`, `GoRttiMapper`) and of `Generic-src.zip` `Application.java`.
- `ls`/`find`/`grep` over the installed golang data and `~/.config/ghidra`.
- Two one-off `python3 -I -c` parses of installed data:
  - for each base, top-level keys vs. the first path element of every same-minor diff section;
  - a tally of all diff section path lengths.

  These were not retained as a producer. F2's numbers need a QUALITY #18 receipt before they enter the corpus.

No target or Ghidra execution, and no edits to implementation or corpus. No installs or updates. Only this report was written.
