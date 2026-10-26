# R40AssimReject — assimilation-reject verdicts, AVM knowledge set (round 40, wave 1, pre-freeze)

**Verdict: DEFECTS FOUND** — 2 of the 3 re-tested entries are **REJECT** (`avm-firmware-image-unblob.md`,
`avm-le-variant-reachability.md`); 1 is **ADMIT-AFTER-REWRITE** (`avm-le-image-genuine-marker.md`).
The rejected mechanism is still standing after round 39 flagged it, it contradicts three sibling
entries and the lane's own shipped triage table, and it would become a scoring fault if the freeze
cites the entry or scores R40-C1's fifth kill control on the unblob process exit code.

Seat: critic/assimilation-reject (leaf). Nothing outside
`.ufo/waves/round-40/w1/R40AssimReject.md` and
`.ufo/waves/round-40/w1/artifacts/R40AssimReject/` was written. Shokuknow read-only (fixtures hashed
in place and copied to scratch). No REA call; no unreduced carrier touched; `unblob`,
`sasquatch`, `sasquatch-v4be` untouched and not reinstalled. No tool installed; no pacman
transaction. Read-only git only (none was needed).

---

## 0. The measured spine (this seat's own runs)

Everything below is rebuilt by `artifacts/R40AssimReject/repro.sh`; the probe is
`artifacts/R40AssimReject/probe.py` (pure stdlib, no unblob/sasquatch code).

| run | input (development fixture, not a carrier) | sha256 | AVM marker | unblob handler | child argv | files | unblob process exit | `Extract command failed` in log |
|---|---|---|---|---|---|---|---|---|
| A | `lanes/kaidoku/round11/work/avm-be.squashfs` (genuine AVM-BE) | `c7f74691…32d32` | **SET** 365==365 | `squashfs_v4_be` | `sasquatch-v4be -no-exit-code -f -d …` (**no `-be`**) | 4 | **0** | 0 |
| B | same bytes, superblock `8:12 := 1792847340` (4 bytes differ) | `7038aae4…31ce89` | not set | `squashfs_v4_be` | `sasquatch-v4be -be -no-exit-code -f -d …` | **0** | **0** | **1** |
| C | `lanes/kaidoku/round13/work/avm-le-genuine.squashfs` | `18d3ad05…afaee4` | **SET** 361==361 | `squashfs_v4_le` | `sasquatch -le -no-exit-code -f -d …` | 4 | 0 | 0 |

Direct extractor matrix (no unblob), same bytes: `sasquatch-v4be` no-flag on A → exit 0, 4 files;
`-be` on B → exit 1, 0 files, `FATAL ERROR: File system corruption detected`; no-flag on C → exit 1,
`FATAL ERROR: Block size too small.  File system is corrupt.`

**A single 4-byte superblock field decides the flag and the flag decides success**: marker on →
no `-be` → 4 files; marker off (everything else byte-identical) → `-be` → 0 files. The marker is
therefore not merely "noticed" by unblob; on the big-endian v4 path it is the one input that
selects a working extractor invocation.

Pinned source, unblob 26.6.4 (`unblob/handlers/filesystem/squashfs.py`, sha256
`2d7b901b…5599287`), quoted in `artifacts/R40AssimReject/handler-quote.txt`:

```
40:            case Endian.BIG, 4:
41:                executable = self.V4BE_EXECUTABLE
42:                struct_parser = StructParser(SquashFSv4LEHandler.C_DEFINITIONS)
44:                    header = struct_parser.parse(
45:                        SquashFSv4LEHandler.HEADER_STRUCT, f, Endian.BIG
47:                    # see …/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt
48:                    is_avm = header.bytes_used == header.mkfs_time
49:                    if not is_avm:
50:                        commands_args.append("-be")
53:            case Endian.LITTLE, _:
54:                commands_args.append("-le")
```

Two asymmetries the corpus must not flatten: handler **selection** is marker-independent (magic +
endianness only), the **extractor argv** is marker-dependent on the `Endian.BIG, 4` arm only
(`:48-50`); the `Endian.LITTLE` arm (`:53-54`) has no marker test, which is why the LE entries'
"invisible" observation reproduces and the BE entry's generalisation does not. The same arm is
also reached by `SquashFSv4BroadcomHandler` (`:548-553`, extractor constructed at `:553` with the
BE magic), so the test belongs to every big-endian v4 handler, not to AVM support. `[INFERENCE for
Broadcom: read from construction sites, not measured.]`

**Exit code is not an outcome witness.** `ExtractCommandFailedReport.severity = Severity.WARNING`
(`unblob/report.py:91-98`) and the CLI maps `WARNING → 0`, `ERROR → 1`
(`unblob/cli.py:464-475`), so run B — total extraction failure, 0 published files, extractor exit 1
— ends with **unblob exit 0**. Quoted in `artifacts/R40AssimReject/exit-policy-quote.txt`.

**The falsified sentence is also visible inside committed evidence** (no rerun needed):
`corpus/evidence/round-39/c2/heldout/H13/envelope.json` logs
`command='sasquatch-v4be -no-exit-code -f -d …'` (class `avm-marker-be-dropped`, marker read, `-be`
omitted) while `H15/envelope.json` logs `command='sasquatch-v4be -be -no-exit-code -f -d …'`
(class `body-extractor-failure`). Table in `artifacts/R40AssimReject/envelope-argv.tsv`.

---

## 1. `avm-firmware-image-unblob.md` — **REJECT**

**Weakest claim.** `:16` "…**unblob handles it with the ordinary little-endian and big-endian
SquashFS handlers** — it never notices the AVM marker at all", developed at `:75-77` "The AVM
marker is **invisible to unblob**: it selects a handler on the magic and the endianness, never on
the marker, so an AVM_LE image and a plain LE image of the same size and compression take the same
path."

**Counterexample, four independent directions.**

1. **The pinned handler reads the marker and acts on it** — `squashfs.py:48-50` above, with the
   comment at `:47` citing Freetz's `AVM-BE-format.txt`. The sentence names the marker as the
   decision input and names the source in the same block.
2. **The entry contradicts its own table.** `:67` prints the BE member's argv as
   `sasquatch-v4be -no-exit-code -f -d {outdir} {inpath}` — the **absent `-be` is the marker being
   noticed**. The observation reproduces; the causal sentence beside it does not.
3. **The entry contradicts three sibling entries.** `sasquatch-unblob-avm-branch.md:16-18`
   ("appends `-be` only when `header.bytes_used == header.mkfs_time` is **false**. The AVM case is
   therefore signalled by the **absence** of a flag"), measured there as a true/false pair at
   `:27-31` ("unblob's own parser confirms … `is_avm` = true … **the `-be` is gone**").
   `avm-le-variant-reachability.md:25` likewise speaks of "its v4-BE AVM branch", and
   `avm-image-extraction.md` / `avm-image-build-blocker.md` carry `image_is_avm` rows. So the
   corpus already holds the correct mechanism three times over, with no pointer from `:75-79`,
   and the set would admit mutually exclusive authorities.
4. **The lane's shipped artefact already states the opposite.** `SKILL.md:339` (triage table v1,
   label `avm-marker-be-dropped`): "mkfs_time equals bytes_used, unblob read the AVM marker and
   omitted -be", sourced to the same `S112 lines 44-50`. The deployable skill and the knowledge
   entry disagree today.

Measured: runs A/B above (marker flip on a *genuine* AVM-BE body, not only on a doctored standard-BE
probe) and the committed H13/H15 argv pair. Round 39 reached the same conclusion
(`.ufo/waves/round-39/w1/R39AssimAvmCritic.md`, E4); the sentence is **unchanged two waves later**,
so this is a standing claim, not an oversight.

**Flip condition.** The verdict reverses only if the pinned handler contains no comparison of
`mkfs_time` with `bytes_used` (it does, `:48`) **or** a marker flip leaves both the child argv and
the extraction outcome unchanged (measured: argv `-no-exit-code` ↔ `-be`, 4 files ↔ 0 files, on
bytes that differ in exactly 4 positions). Either observation would restore the "invisible" reading.

**Impacted axes.** *coverage* — this is the entry a `## Round-40 additions to Core` row would cite
for the AVM layout; citing it as written imports the false mechanism into the frozen row.
*depth* — the entry suppresses the one fact R40-C1's carriers depend on (the marker is load-bearing
on the BE path). *calibration* — its `recheck:` line (`:11`, `grep -c` for a superblock shape) cannot
detect the false claim, so the 180-day recheck will keep passing a falsified sentence.

**Smallest safe correction (no measurement is lost).**

- `:14-16` → "…carries **both** AVM filesystem formats at once, and unblob takes each one with the
  handler it uses for plain SquashFS — the marker does not change *handler selection*, but on the
  big-endian path it changes the *extractor command*."
- `:75-79` → "**The point, and the limit.** The marker is invisible to handler selection: unblob
  picks `squashfs_v4_be` on the magic and the endianness alone. It is **not** invisible to the
  extractor: `SquashFSExtractor.extract` parses the big-endian v4 superblock, sets
  `is_avm = bytes_used == mkfs_time` and omits `-be` exactly when the marker holds
  (`squashfs.py:40-50`). The BE member's argv in the table above *is* the marker being read: with
  the marker stripped from the same bytes, unblob adds `-be` and the extractor fails."
- Add one line: "A marker-stripped copy of a genuine AVM-BE body is indistinguishable from body
  damage at the *symptom* level; the discriminator is the child argv, not the exit code."
- Replace the `recheck:` line with one that can fail: `grep -c 'is_avm = header.bytes_used ==
  header.mkfs_time' <pinned squashfs.py>` → 1, plus `grep -c ' -be ' <BE member argv>` → 0.

---

## 2. `avm-le-variant-reachability.md` — **REJECT**

**Weakest claim.** `:10-13` "…with the correct value the tool still does not produce an AVM image,
because the AVM marker … is not set on that path", restated at `:21-25` and closed at `:30-33`
("**What would close the variant.** The `AVM_FORMAT_AS_OPTION` build … or a genuine AVM_LE firmware
image").

**Counterexample.** Both halves are falsified by bytes the lane retains, and by a sibling entry in
the same set.

- `lanes/kaidoku/round13/work/avm-le-plain550.squashfs` was built by a **clean** rebuild of the
  plain Freetz 23-patch recipe with `-DTARGET_FORMAT=AVM_LE` **only** and **no** `-no-mkfs-time`
  (`build-avmle2.sh:32-37`); it carries the marker (`mkfs_time` 361 == `bytes_used` 361, probe
  output in `probe-output.txt`).
- It is **byte-identical** to `avm-le-genuine.squashfs` (sha256 `18d3ad05…afaee4` for both,
  `cmp -s` exit 0) — the image entry 3 built with `AVM_FORMAT_AS_OPTION` **plus** `-no-mkfs-time`
  (`build-avmle.sh:22-36`). So the option is not needed and the two recipes converge on the same
  bytes: `artifacts/R40AssimReject/sha-identities.txt`.
- `avm-le-image-genuine-marker.md:40-42` states the same reversal in words ("the round-12 conclusion
  — 'the AVM marker needs the `AVM_FORMAT_AS_OPTION` build' — is **wrong on both counts**"), and
  names it as the round-12 finding without naming this file. Two entries, same `verified-at`, no
  pointer in either direction: a duplicate authority with opposite answers.
- The entry's own measurement reproduces exactly and is therefore *not* the defect: the image it
  measured is `lanes/kaidoku/round12/work/avm-le.squashfs`, sha256 `afeb55a4…a5299`, `mkfs_time`
  `1792847340` — the number printed verbatim at `:23` — i.e. the stale-binary image whose
  `bytes_used` is 365, not the 361 of the clean rebuilds. The bytes are right; the causal reading of
  them is wrong.

**Flip condition.** The verdict reverses if `avm-le-plain550.squashfs` shows `mkfs_time ≠
bytes_used`, i.e. if a clean plain-Freetz build with the correct define does *not* set the marker.
It shows 361 == 361.

**Impacted axes.** *coverage* — the entry as titled ("not reachable") is a standing negative that
the lane's own bytes overturn; a Core row or a Gate admission that carries it re-teaches the wrong
route. *depth* — the salvageable half (the name-versus-value correction, `:15-19`) is exactly the
mistake that caused the stale build, so it must be kept and the conclusion removed. *calibration* —
its `recheck:` (`:7`, `grep -c 'handler=squashfs_v4_le'`) tests an incidental observation that is
true under both readings.

**Smallest safe correction.** Retitle to the surviving fact — "The second AVM variant's
`TARGET_FORMAT` value is `AVM_LE`, not `AVM_BE_AVM_LE`" — keep `:4-5` sources, `:15-19` and the
caveat at `:35-39`; delete `:12-13`; replace `:21-28` with the stale-build fact plus the two shas
(`afeb55a4…` stale vs `18d3ad05…` clean) and a reversal pointer to
`avm-le-image-genuine-marker.md`; delete `:30-33` (the variant is closed, per that entry). Add the
retained-image digests, which neither entry carries today.

---

## 3. `avm-le-image-genuine-marker.md` — **ADMIT-AFTER-REWRITE**

**Central claim confirmed, three ways.** The retained image is `hsqs`, XZ, `mkfs_time` 361 ==
`bytes_used` 361 (my probe); the clean rebuilds reproduce the marker in two recipes
(`lead2-stale-build.tsv` rows `clean_rebuild_plain_freetz_550_define_AVM_LE`,
`clean_rebuild_avm_format_as_option_with_no_mkfs_time`, both consistent with the bytes I hashed);
and my run C reproduces the recorded unblob behaviour byte for byte — handler `squashfs_v4_le`,
argv `sasquatch -le -no-exit-code -f -d …`, 4 files, no `Extract command failed`. The recorded
`FATAL ERROR: Block size too small.  File system is corrupt.` from `sasquatch-v4be` also
reproduces (exit 1, 0 files). What the entry says about the **LE** path — that the marker does not
change unblob's handling — is correct and source-backed (`squashfs.py:53-54` has no marker test).

**Why not admit as-is.** Three sentences overreach in the direction the round-40 C1 claim cannot
afford:

1. `:30` "…unblob, and the marker is invisible to it." True for the LE arm only; the same sentence
   in the BE entry (`:75`) is the falsified one, and this wording is what the false generalisation
   is built from. It must be scoped: "invisible to the LE path, which never tests the marker".
2. `:55-56` "it does not say unblob *recognises* the AVM marker" is now known false on the BE path
   (`:48-50`); as a caveat it under-claims in the opposite direction and will keep the corpus from
   recording the mechanism it has measured.
3. It records an extraction success without recording that unblob's own exit code is **0 for a
   total extraction failure** (`report.py:94`, `cli.py:466-467`; measured in run B). A reader who
   adopts "4 files extracted" as the witness is one step from adopting exit codes as witnesses.

**Rewrite (four additions, no deletions of measurement).** (a) scope `:30` to the LE path and name
`squashfs.py:53-54`; (b) replace `:55-56` with "on the big-endian v4 path the marker *is* read and
it removes `-be`; this entry measures only the LE path"; (c) add the image digest `18d3ad05…`, the
tool pins (unblob 26.6.4, handler sha `2d7b901b…`, sasquatch/sasquatch-v4be 4.5.1) and the verbatim
argv; (d) add the reversal pointer to entry 2 (retitled) so the pair is navigable in both
directions.

**Flip condition.** Reverses if the retained `avm-le-genuine.squashfs` does not carry the marker or
if unblob's LE arm is shown to test the marker (neither holds: 361==361; `:53-54`).

**Impacted axes.** *coverage* — this is the entry a C1 "genuine AVM_LE" row could cite, and it is
the only one of the three that is safe after a bounded rewrite. *depth* — with (b)+(d) it becomes
the LE half of one consistent pair instead of a third voice. *calibration* — its own caveats are
narrower than its data.

---

## 4. What the freeze must change (ordered by blast radius)

1. **Do not cite `avm-firmware-image-unblob.md` as the basis of the round-40 AVM Core row** until
   `:16` and `:75-79` are rewritten. The R40-C1 claim's own mechanism sentence (unblob 26.6.4
   `squashfs_v4_be` chooses `sasquatch-v4be` without `-be` exactly when the marker holds) is
   **correct** — verified at `squashfs.py:40-54` and by runs A/B — so the *claim* is safe; the
   *entry it would cite* is not. A round-40 entry that inherits the "invisible" wording would put
   the contradiction inside the frozen Core row.
2. **R40-C1 kill control 5 must not be scored on the unblob process exit code.** The draft's "a
   genuine AVM body with the marker stripped (unblob adds `-be`, extraction fails)" *passes* if
   "fails" means exit ≠ 0: run B is exit 0 with 0 files, because the failure is a `WARNING`
   (`report.py:94`) and warnings map to 0 (`cli.py:466-467`). Smallest safe correction: score the
   kill as "0 published regular files **and** an `ExtractCommandFailedReport` in
   `normalized_result.diagnostics`" (or as "the `-be` token is present in the child argv"), and
   apply the same wording to the receipt binding "no failed chunk" — otherwise the kill control
   cannot fire and the re-minted-fabricated-receipt defect R39-CL5 survives in a new form.
3. **Keep the `-be in child argv` column in triage table v2.** `avm-marker-be-dropped` (H13) and
   `body-extractor-failure` (H15) are otherwise identical envelopes — exit 0, handler
   `squashfs_v4_be`, gap `extractor-failure`, 0 published files — and differ only in the logged
   extractor command. v1 already separates them by that column (`SKILL.md:334,339-340`;
   `sqfs-triage.py:43-47`); the v2 change list does not mention it, and dropping it in a rewrite
   would collapse two labels into one. (C2 seats own this; recorded here because the evidence came
   out of the AVM attack.)
4. **Add a reversal pointer between entries 2 and 3** (both directions) and give entry 2's removal
   of `:12-13` a dated line, so the corpus can show *when* the stale-build reading was retired
   (QUALITY #35/#36: a rejected decision must be locatable from the admitting row).

## 5. Limits of this review

- Two entries were assigned; `avm-le-image-genuine-marker.md` was read as the counterpart of entry 2
  and is verdicted above because entry 2 cannot be judged without it. `avm-image-extraction.md`,
  `avm-image-build-blocker.md`, `sasquatch-unblob-avm-branch.md` and
  `sasquatch-unblob-compatibility*.md` were **not** re-tested here; round 39's E1/E2 verdicts on
  the first three stand unreviewed by me, and `sasquatch-unblob-avm-branch.md:39` ("What is still
  open. A real AVM image.") is stale for the same reason round 39 recorded.
- No vendor image was downloaded this wave (V1 is a frozen carrier; the dev fixtures are the lane's
  retained 4096-byte images). The 9877-file vendor measurement is therefore **not** re-measured
  here; it is corroborated indirectly through the committed round-39 envelopes' argv, which is
  sufficient for the mechanism question and nothing more.
- The Broadcom-arm claim in §0 is source-read only, not measured.
- `[INFERENCE]` marks: Broadcom reachability of the marker branch; intent behind entry 2's stale
  build (the byte evidence is direct, the motive is not).
