# CR2 (critic) — C1b append-only purity: can the correction note be read as rewriting the lesson's historical claims?

Read-only seat (only repo write is this report). All commands run 2026-10-18 from
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD `4b806e14db22ea44cc57729f5fa3f7b46b616178`
(`git status --porcelain` → only `?? .ufo/waves/arc2-loop1-round1/`). Scratch namespace used:
`/tmp/arc2-l1r1-CR2/`. Overlap artifacts read, never modified: C1.md, CR5.md, E7.md, E8.md, E23.md, S2.md.

## 1. Verdict

**BYTE PURITY HOLDS — PROVEN BY DRY-RUN; the interpretive attack is real but closable.**
Appending either existing draft (E7.md:136-148 or E8.md:37-63) leaves the first 8568 bytes of
`corpus/lessons/2026-10-15-round-1.md` byte-identical (sha256 `71e003e8…`, blob `0cb945bd…`) and shifts no
downstream line citation. But **E8's block is not landable verbatim**: its sentence "Read the :152
pointer against HEAD as `PROVINCE.md:114-116`" (E8.md:58) is an imperative that substitutes a new
referent for the historical text, and the block carries no no-rewrite clause. E7's block is landable
but lacks the byte-identity evidence (sha256 `78f40919…`, quoted refusal text). The merged block in
§5 was dry-run appended and passes all purity checks; land it (or E7) — not E8 as drafted.
One instrument conflict found (wave-live, see §3-C5): an earlier E23 revision's census command
(`grep -n '107-109'` expecting 1→0) was unsatisfiable by construction; the E23.md revision current at
this report's final read (13:43, 21150 B, `:145`) already carries a corrected instrument
(`grep -c "PROVINCE.md:114-116" …` → 0→≥1), which matches my re-scoped instrument. The 1→0 form, if
anywhere still planned, must be dropped.

## 2. The strongest objection (steelman)

**O1 — Imperative substitution edits truth-conditions without touching bytes.** The historical
sentence at `corpus/lessons/2026-10-15-round-1.md:152` asserts a boundary at `PROVINCE.md:107-109`.
A reader at the lesson's own revision resolves that to the refusal bullet; a post-append reader is
instructed by E8's block to resolve the same words to different province bytes. Byte-append purity
is intact, but the claim's *meaning* has been re-indexed by a dispositive instruction. If "append-only"
means "the historical text keeps meaning what it meant", E8's imperative violates it on the face of
the file, and its missing self-limiting clause leaves the violation unrepaired.

**O2 — The `:7` convention-scope fork.** `corpus/lessons/2026-10-15-round-1.md:7` says "Line citations
to *pre-existing lane files* use baseline revision line numbers." If PROVINCE.md (a lane-definition
document, not a lane output) falls outside that phrase, the :152 pointer was not convention-conformant
but simply wrong at HEAD — and any note that calls it convention-following ("follows this file's
declared baseline-revision convention (:7)", E8.md:42) rewrites the record of what happened, converting
an error into a convention instance. The assessment status of the historical claim changes even though
its bytes do not.

**O3 — Re-affirmation creep.** Resolving :152 to the refusal at :114-116 necessarily asserts the
*current* province still carries the boundary the 2026-10-15 lesson invoked. If the boundary text had
moved or weakened, the note would silently revalidate an old assessment from inside a dated artifact.

**O4 — Artifact identity.** The append changes the lesson's blob (`0cb945bd…` → new), stale-ifying the
two wave-internal hash citations (V1.md:62, V6.md:10), and adds a new `##` heading at EOF where the file
previously ended `intact.` (`tail -c 40 | xxd` → `...intact..`). No corpus-pinned hash of this file
exists (corpus/README.md:163 is an index row with no size/hash), so this is wave-internal only.

## 3. The counter, with exact wording boundaries

**C0 — The dispositive facts make the attack closable at zero evidence cost.**
Prefix identity is proven (dry-run below); all 30+ observed range citations to this file (`:87-153`,
`:140-143`, `:145-155`, …; grep sweep §4.7) resolve unchanged because an EOF append shifts nothing;
and the corpus already accepts *stronger* interpretive moves on this exact file — the recovery
companion says "This entry supersedes the closure promises in `corpus/lessons/2026-10-15-round-1.md:140-143,154-160`"
(`corpus/lessons/2026-10-15-round-1-recovery.md:17-18`) with original bytes preserved
(`corpus/lessons/2026-10-15-round-1-admission-correction.md:11-13`: "their original bytes and full
historical outputs remain preserved"). A pointer refresh is strictly weaker than the accepted precedent.

**C1 (answers O1) — Boundary B1: describe, never command.** Landable: "Against the pre-append revision
`4b806e14…`, the :152 pointer resolves to `PROVINCE.md:114-116`" (descriptive, revision-indexed).
Not landable as-is: "Read the :152 pointer against HEAD as `PROVINCE.md:114-116`" (E8.md:58 —
imperative, and "HEAD" is a floating referent that goes stale). The r2 precedent keeps this boundary:
its note "Folded back to the recorded evidence, they assert only that …" and closes "This note
qualifies, and does not rewrite, the historical text." (`corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:244`).

**C2 (answers O2) — Boundary B2: fact-only core survives either fork.** The sentence "At baseline
`6645585` and at the landing commit `c265db9`, `:107-109` is the refusal bullet; at the pre-append
revision `4b806e14`, the refusal is at `:114-116`" is true under both readings and adjudicates nothing.
The stronger "follows this file's declared baseline-revision convention (:7)" is defensible if the
parent accepts the convention scope (support: the identical convention in SCORECARD.md:16-17; the twin
pointer introduced at the same commit `c265db9`; E21/P1 rulings) — E8's clause is at that boundary.
"Was correct as written" is one step beyond it (a verdict); "the pointer was wrong" is the opposite
overreach. The recommended block keeps E8's clause, drops the verdict.

**C3 (answers O3) — Boundary B3: revision-pin every citation; Boundary B4: mandatory self-limiting
clause.** The note must state the referent is byte-identical at both loci (sha256 `78f40919…` at
baseline :107-109 and pre-append :114-116 — verified) so that it moves an *address*, not a referent;
and it must carry the r2-precedent clause verbatim ("This note qualifies, and does not rewrite, the
historical text.") or E7's variant ("the historical citation is not rewritten", E7.md:146-147). E8's
block has neither the clause nor a statement that the note adds no current-validity claim — that is
the precise reason it fails this boundary while E7 passes.

**C4 (answers O4) — Boundary B5: heading label.** The lesson has no `## Errata` section
(`grep -n "Errata" corpus/lessons/2026-10-15-round-1.md` → rc=1), unlike the r2 file (`:221`), so a new
`##` heading is structurally required. "Pointer refresh" (recommended) frames the note as maintenance
consistent with its own claim that the citation was baseline-correct; "Correction note" (E8.md:38)
frames :152 as wrong. Either lands; the label is editable, the body citations are load-bearing.

**C5 — Instrument conflict (wave-live; resolved in the current E23 revision).** An earlier E23
revision's census (`grep -n '107-109' corpus/lessons/2026-10-15-round-1.md SCORECARD.md`, expecting
"lesson 1 → 0 live") is unsatisfiable by construction: append-only keeps the :152 line and any
drift-explaining note must name the token — dry-run returns **2**. Wave-live note: E23.md and S2.md
were rewritten by their seats during this report's run (observed: E23.md 11057→21150 B, mtime 13:43;
S2.md 9323→13797 B, mtime 13:41). The E23.md revision current at my final read (13:43) already
carries the corrected instrument at `:145` (`grep -c "PROVINCE.md:114-116" corpus/lessons/2026-10-15-round-1.md` → 0 → ≥1;
lesson `107-109` occurrences "1 → 1 historical"), and the current S2.md carries the same `:114-116`
instrument at `:102` — both match my re-scoped instrument, so no instrument fix is now needed. Re-scoped
instrument (all verified on the dry-run):
`head -160 <file> | grep -c 'PROVINCE.md:107-109'` → 1 (constant; historical body untouched);
`grep -c 'PROVINCE.md:114-116' <file>` → 0→1;
`head -c 8568 <file> | sha256sum` → `71e003e8…` (constant; prefix identity).

## 4. Evidence (commands run this session, with observed output)

**4.1 — File identity (pre-append).**
`git rev-parse HEAD:corpus/lessons/2026-10-15-round-1.md` → `0cb945bd0514f8b5e77710409ef7f98d33ced02a`;
`git hash-object corpus/lessons/2026-10-15-round-1.md` → same (worktree = HEAD);
`sha256sum` → `71e003e816895e1c819e4669e0e33ae14ca41673036c8d94344e32a4793a7442`; `wc -l -c` → 160 lines,
8568 bytes; `tail -c 40 | xxd` → `… intact.\n` (single trailing LF).

**4.2 — Pointer census.** `grep -n "PROVINCE" corpus/lessons/2026-10-15-round-1.md` → only
`152:the safety/trust boundary at \`PROVINCE.md:107-109\`; it remains correction debt,`.
`grep -c "PROVINCE.md:114-116"` → 0; `grep -c "PROVINCE.md:107-109"` → 1.

**4.3 — PROVINCE revision walk.**
`for c in 6645585 c265db9 75af886 7125dd4 HEAD; do git show $c:PROVINCE.md | grep -n "Quality/safety verdicts"; done`
→ `107 / 107 / 107 / 114 / 114`. `git show 7125dd4 -- PROVINCE.md | grep '^@@'` →
`@@ -29,8 +29,11 @@` (+3) and `@@ -61,7 +64,11 @@` (+4); `git show 75af886 -- PROVINCE.md | grep '^@@'` →
`-5,25 +5,25` and `-38,7 +38,7` (net 0); `git log --oneline 7125dd4..HEAD -- PROVINCE.md` → empty.

**4.4 — Byte identity of the moved block.**
`git show 6645585873c4e66372b15687c47000abf8d91978:PROVINCE.md | sed -n '107,109p' | sha256sum` =
`sed -n '114,116p' PROVINCE.md | sha256sum` = `78f40919e4dc1a882512b5bab6767a821c4fc9fc2bec1f8c5f14fa14c19200b3  -`.
HEAD `:107-109` observed = tail of the anti-trigger bullet + head of the installing-engines bullet
(the unrelated operator-scope text).

**4.5 — Precedent.** `git show 40162fc --numstat` → `2 0 corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md`
(insertions only). Note at `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:244` read verbatim;
closes "This note qualifies, and does not rewrite, the historical text." and cites `PROVINCE.md:114-116`.

**4.6 — Companion-file precedent.** `corpus/lessons/2026-10-15-round-1-recovery.md:17-18` ("This entry
supersedes the closure promises in `corpus/lessons/2026-10-15-round-1.md:140-143,154-160`") and
`corpus/lessons/2026-10-15-round-1-admission-correction.md:9-13` (original bytes preserved) — both read.

**4.7 — Downstream citations.** Repo-wide grep for `2026-10-15-round-1.md:<n>` → 30 distinct ranges
(e.g. `:7`, `:87-153`, `:140-143`, `:145-155`); all ≤160, none shifted by an EOF append.

**4.8 — Dry-run (namespace `/tmp/arc2-l1r1-CR2/`).**
`cp corpus/lessons/2026-10-15-round-1.md base.md`; appended E8-block, E7-block, and the §5 merged
block (each after one blank-line separator) to copies. For every variant:
`head -c 8568 <new> | cmp - base.md` → **PREFIX-IDENTICAL**; merged copy: 188 lines, 10027 bytes;
`head -c 8568 merged_full.md | sha256sum` → `71e003e8…` (unchanged). Post-append instruments:
`grep -c 'PROVINCE.md:107-109'` → **2** (original :152 + note); `grep -c 'PROVINCE.md:114-116'` → **1**;
within first 160 lines: 1 / 0. Quoted refusal block in the merged copy (`sed -n '178,180p'`) vs
`sed -n '114,116p' PROVINCE.md` → `cmp` **QUOTE-IDENTICAL**.

**4.9 — Frozen-cause pointers (resolve).** `SCORECARD.md:266-267` ("The 2026-10-15 reconciliation
table above stays frozen"); `SCORECARD.md:16-17` (baseline-revision convention); `LOG.md:883-886`
(carried debt: r3 `(:60,:136)`; stale pointers at `SCORECARD.md:79` "frozen reconciliation table —
untouchable" and the lesson "(historical)").

## 5. Verbatim block for the parent (land as-is; prefix-identity dry-run-verified)

Append at EOF after one blank-line separator (the file ends with a single LF; r2 `:243-244` separator
convention: blank line, then the note). Post-landing proof:
`head -c 8568 <file> | sha256sum` → `71e003e8…` (or `| git hash-object --stdin` → `0cb945bd…`).

````markdown
## Pointer refresh — refusal-locus drift (appended 2026-10-18, arc2-loop1-round1)

Append-only note; every byte above this section is unchanged. The
`PROVINCE.md:107-109` citation at :152 follows this file's declared
baseline-revision convention (:7) and resolves exactly at baseline
`6645585873c4e66372b15687c47000abf8d91978` and at this lesson's landing
commit `c265db9`. The refusal bullet later moved +7 lines, bytes unchanged,
in luna-round-5 (`7125dd4`; hunks +3 and +4) — luna-round-2 (`75af886`)
edited other lines same-line only and left the bullet at :107. The sha256
of the three-line refusal block (with terminating newline) is
`78f40919e4dc1a882512b5bab6767a821c4fc9fc2bec1f8c5f14fa14c19200b3` at both
the baseline locus (:107-109) and the pre-append-revision locus (:114-116).
Against the pre-append revision `4b806e14db22ea44cc57729f5fa3f7b46b616178`,
the :152 pointer resolves to `PROVINCE.md:114-116`; the refusal bullet reads:

```text
- **Quality/safety verdicts on findings** — the lane answers "what does this
  shipped artifact do, per evidence id X" — never "is it safe, trustworthy, or
  licensed for reuse" `(unowned)`.
```

The sibling occurrence at `SCORECARD.md:79` is adjudicated
NO-CHANGE-with-cause: it sits in the frozen 2026-10-15 assessment block
(`SCORECARD.md:266-267`) and resolves under that file's declared
baseline-revision convention (`SCORECARD.md:16-17`); it is carried at
`LOG.md:883-886`. This note qualifies, and does not rewrite, the historical
text.
````

Strict-purity fallback for B2 (if the parent rejects the :7 scope over PROVINCE.md): replace the first
sentence's "follows this file's declared baseline-revision convention (:7) and resolves exactly at" with
"resolves at": "…citation at :152 resolves at baseline `6645585…` and at this lesson's landing commit
`c265db9`, and against the pre-append revision `4b806e14…` resolves to `PROVINCE.md:114-116`." All other
clauses are invariant.

## 6. Conclusions, labeled

**Observations (ran/read this session):** §4.1–4.9 in full — file identity 160 lines / 8568 B / blob
`0cb945bd…` / sha256 `71e003e8…`; single pointer at :152; revision walk 107/107/107/114/114; hunks
+3/+4 solely `7125dd4`, `75af886` net-0, no later PROVINCE commits; block sha256 `78f40919…` identical
at both loci; r2 precedent insertion-only (`2 0`) with its self-limiting clause; recovery companion's
supersession language; 30+ downstream ranges; dry-run prefix identity for all three drafts; post-append
grep counts 2/1 (whole) and 1/0 (first 160); quote `cmp` identical; SCORECARD/LOG freeze pointers resolve.

**Inferences:** (1) Byte-level append-only purity is guaranteed for any of the three drafts — the attack
surface is purely interpretive. (2) E8's draft fails B1 (imperative substitution) and B4 (no no-rewrite
clause); E7's passes both but is under-evidenced; the §5 merged block is the recommended landing text.
(3) The O2 fork does not affect the note's factual core; only the convention-scope phrase is at stake,
and the strict-purity fallback removes even that. (4) The earlier 1→0 census form would have recorded a
false failure (2≠0) after a correct landing; the E23.md/S2.md revisions current at final read already
use the corrected instrument (§3-C5), so no action remains there.

**Unknowns:** (a) whether the parent accepts the `:7`/SCORECARD.md:16-17 convention scope over
PROVINCE.md (the O2 fork) — the recommended first sentence depends on it; fallback given. (b) which of
E7/E8/merged the parent lands (all three byte-pure; only merged is boundary-complete). (c) whether the
mandatory LOG entry (AGENTS.md) will also record the SCORECARD.md:79 NO-CHANGE-with-cause adjudication
— parent's integration choice. (d) whether the battery legs' receipts timing affects C1b (it does not:
C1b reads no battery artifact).
