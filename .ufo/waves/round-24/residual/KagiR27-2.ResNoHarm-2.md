# KagiR27-2.ResNoHarm-2 — no-harm / residual check at kaidoku round 24, commit 69e82c48

Scope: read-only falsification of the no-harm claims for lane commit
`69e82c48be5614ce96f7c1c32445fe61c4870630` against base
`fe10219ec6e92c32b7eb40d83fbcac888756c6c1` in
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (branch `main`).
Clone used for all Git-object reads: `/fast/scratch/kaidoku-r24/seats/ResNoHarm-2/lane`
(`git clone --no-hardlinks` of the lane at 69e82c48) plus
`/fast/scratch/kaidoku-r24/seats/ResNoHarm-2/baseclone` at `fe10219e`.
No lane file was written by this seat; all mutations were performed in
throwaway clones under `/fast/scratch/kaidoku-r24/seats/ResNoHarm-2/mut*`.
No tool was installed (nothing needed installing; TShark 4.6.9 was already
present at `/home/vgpnk/.local/opt/wireshark-4.6.9/bin/`, digests matched
`.ufo/waves/round-24/tool-pins.json`).

## Verdict

**No-harm is not established.** The five state facts the assignment asks
about are all *true at commit 69e82c48* — I reproduced each one — but three
of the five are true only as manual inspection, not as a machine-checked
property of the committed tree, and the committed instruments do not cover
the whole no-harm surface the round claims in
`.ufo/waves/round-24/claims.json:46-51`. The two committed instruments
(`count-c1.py`, `freeze-gate.py`) do fail when they should (red paths
exercised), but they also stay green across post-freeze edits and deletions
of the artifacts the no-harm list names. The round is not verified here; this
is a falsification report, not an admission.

## Findings

### Passing observations (all at 69e82c48 unless stated)

- **O1 — prior knowledge blobs byte-identical.** 107 pre-existing files
  under `corpus/knowledge/` at base; git blob digest comparison base→head:
  **0 mismatched**, 1 file added (the new round-24 entry). Independently at
  the working tree: 0 mismatched.
  (`git ls-tree -r <rev> corpus/knowledge/` + per-file sha256.)
- **O2 — SOURCES rows S001–S063 byte-identical.** Parsed all `| S… |` rows
  at both revisions: 63 common rows, **0 changed**, 5 added
  (S064–S068), 0 removed. The S001–S063 slice hashes identically:
  `2c67f4defc01ae684a097a8378f25c201cbefede6c7828e8a1076cc91e4b0ef0` at both
  revisions. Working tree: still 0 changed prior rows (S069–S071 added).
- **O3 — LOG/SCORECARD unchanged so far.** `git diff --stat fe10219e
  69e82c48 -- LOG.md SCORECARD.md` is **empty**; the two files are
  byte-identical to base at the reviewed commit (both files still contain
  no round-24 section at 69e82c48). In the *working tree* both have an
  appended round-24 section and the prefix property holds
  (working-tree bytes start with the committed bytes).
- **O4 — R23 count-c1 still 4/6.** `python3 -I -B
  .ufo/waves/round-23/tools/count-c1.py --root . --rev 69e82c48` →
  `t1_exercised_count 4 / t1_total 6`, `finding c1_incomplete`, exit 1 —
  identical exercised set to base (4/6, exit 1).
- **O5 — R22 counters 1/6 and 14/14.**
  `.ufo/waves/round-22/tools/count-c1.py --rev 69e82c48` → 1/6, exit 1;
  `count-c2.py --rev 69e82c48` → `accounted_count 14`, `mismatched []`,
  `foreign_rows []`, exit 0. Same values at base.
- **O6 — census exits 0.** `.ufo/gates/c1-census-v10.py --root .` → exit 0,
  `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)` at base,
  at head and at the working tree; `--selftest` → `SELFTEST: CLEAN cases=3`,
  exit 0; two consecutive `--json` runs byte-identical (deterministic).
  The gate file is **unchanged** base→head.
- **O7 — source census exit 0, same four W04.**
  `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate
  --today 2026-10-21 --root /home/vgpnk/Projects/shokunin kaidoku` → exit 0
  with W04 on S033, S047, S054, S062 — byte-identical to the base run
  (same four ids, same `ok` line). The script's sha256
  `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30` equals
  the digest r23 recorded in `.ufo/waves/round-23/verify/final/census-tool.json`,
  i.e. the census instrument did not change under the round.
- **O8 — the routed r23 README-separator defect is repaired.**
  `corpus/README.md` had 3 h2-adjacency violations at base (before
  `## Knowledge`, `## Lessons`, `## Frontier` — base lines 73, 160, 177);
  at head: **0**. Exactly those 3 changed repo-wide (206 → 203 h2
  violations across all tracked `.md`).
- **O9 — before-records reproduce.** `count-c1.py --rev fe10219e` at head
  produces stdout **identical** to the stored
  `.ufo/waves/round-24/measure/before-c1.json` (`0/4` held,
  `catalog_zero_count 16`); the head run gives `4/4` and
  `catalog_zero_count 12`, matching the SCORECARD wording "16 → 12".
- **O10 — repro negative control still bites.** Re-running
  `repro/fetch-inputs.py` with a manifest whose sha256 is 64 zeros →
  `match:false`, summary `exit 1`. (I did not re-download the six
  positive inputs — 1.28 GB — so the 6/6 positive claim rests on the
  stored `repro/run-1.jsonl`, which I read but did not re-execute.)
- **O11 — the freeze gate can go red.** Mutating
  `.ufo/waves/round-24/tools/count-c1.py` after the freeze →
  round-24 `INSTRUMENT_REVISED`, `required_failed ['round-24']`, gate exit 1.
  Removing the `instrument_supersessions` entry from the current
  `claims.json` → gate exit 1. The r23 rows reproduce the routed defect
  (`round-23 INSTRUMENT_ABSENT,INSTRUMENT_REVISED`).

### Defects

- **F1 (High) — the no-harm list in `claims.json` is wider than any
  committed check, and the two instruments miss most of it.**
  `.ufo/waves/round-24/claims.json:46-51` promises five no-harm properties:
  prior knowledge + source rows unchanged; LOG/SCORECARD prefixes
  preserved; R23 4/6 and R22 1/6 + 14/14; map integrity and blank-line
  separators restored; source census exit 0. What `count-c1.py` actually
  enforces is only: catalog bytes, `LEGACY_SHA256`, the round-22/23
  evidence trees, prior `corpus/knowledge/` blob digests, and a **prefix
  comparison of parsed S-rows** (`count-c1.py:129-132`); `freeze-gate.py`
  enforces the instrument freeze and the disclosure ledger only. Neither
  instrument reads `LOG.md`, `SCORECARD.md`, `corpus/README.md` or
  `corpus/lessons/` (`grep -c` on both tools → 0 hits for README/LOG/
  SCORECARD).
  Observed, by mutation in throwaway clones (all mutations exit **0** for
  both C1 and C2, i.e. undetected):
  - tamper a pre-existing `corpus/README.md` map row → `count-c1.py` exit 0,
    `freeze-gate.py` exit 0;
  - tamper a pre-round `LOG.md` line → both exit 0;
  - tamper `corpus/lessons/round-23.md` → `count-c1.py` exit 0;
  - delete `corpus/lessons/round-23.md` → `count-c1.py` exit 0;
  - tamper a pre-round **non-S-row** line of `corpus/SOURCES.md` (the
    `S024 → S026 → …` chain bullet at `corpus/SOURCES.md:80`) → exit 0.
  Inference: the round's stated no-harm surface is currently *true* (O1–O3)
  but is enforced by nothing in the commit; a later round can silently
  rewrite the README map, a prior lesson, or SOURCES prose and both gates
  will still report green.
- **F2 (High) — `freeze-gate.py` reports round-24 `CLEAN` across
  post-freeze edits to the claims file it is supposed to police.**
  `freeze-gate.py:82-91` reads the *frozen* `claims.json` for `instruments`
  and `claims`, and the *current* one only for `instrument_supersessions`,
  keyed on `(path, commit)` — the disclosed `sha256` field is never
  compared with anything.
  Observed (gate still `round-24: CLEAN`, exit 0 in every case):
  - `instrument_supersessions[0].sha256` replaced with 64 zeros → CLEAN,
    exit 0;
  - current `claims.json` `instruments[".ufo/waves/round-24/tools/count-c1.py"]`
    replaced with 64 zeros → CLEAN, exit 0;
  - post-freeze edit of the claim's own thresholds
    (`claims[0].before` 0 → 4 and `claims[0].target` rewritten) → CLEAN,
    exit 0.
  Observation: QUALITY33 (`corpus/QUALITY.md` row 33) reads "an undisclosed
  post-freeze change … is a finding, never a clean freeze", and lesson
  M24-1 (`corpus/lessons/round-24.md:56`) claims the fix is "instruments
  committed before the claims file and pinned there by sha256". Inference:
  the freeze currently binds *instrument bytes at the freeze commit* only;
  the claims file's own content and its visible pin map are not freeze-bound,
  so C2's `round-24 CLEAN` verdict does not mean "the measurement plan as
  written is the plan that was frozen". This is a gap in the axis C2 claims
  to move (calibration).
- **F3 (Medium) — the README-separator fix has no executable check, and
  the lesson asserts one.** `corpus/lessons/round-24.md:57` (M24-2) states
  the fix as "blank lines restored before `## Knowledge`, `## Lessons`,
  `## Frontier`; **the final no-harm check counts a blank line immediately
  before each `## ` heading**". No such check exists in the committed tree:
  `grep -rn "blank line immediately|blank separator|## heading" --include='*.py'`
  over the whole repo returns only the wave-1 task prompt text in
  `.ufo/waves/round-24/gen-wave1.py:17,116,145,149`; `.ufo/waves/round-24/tools/`
  and `.ufo/gates/` contain none; `tools/selftest.py` has 0 README mentions;
  round-23's `verify.py:147-149` checks only *non-empty-line order*
  preservation, which is exactly the check that failed to notice the r23
  regression. The wave-1 seat `CritNoHarm`
  (`gen-wave1.py:116`) was supposed to produce "an executable check for
  each" but the 85-seat BUILD wave was refused 20/20
  (`.ufo/waves/round-24/wave1-refusals.jsonl`) and no BUILD seat ran.
  Observation: the state is repaired (O8); inference: nothing prevents the
  next round from removing those blank lines again, and the round's own
  record overstates what is enforced.
- **F4 (Medium) — the no-harm evidence for the reviewed commit is
  untracked, and the selftest oracle is unpinned.** At 69e82c48 the paths
  `.ufo/waves/round-24/tools/selftest.py`, `measure/no-harm-r22c1-…json`,
  `measure/no-harm-r22c2-…json`, `measure/no-harm-r23c1-…json`,
  `measure/selftest-69e82c48.jsonl`, `measure/start-census.json` and
  `residual/` are all absent from the commit (`git status` shows them
  untracked; `git cat-file -e 69e82c48:<path>` fails). `selftest.py` is
  also not in `claims.json`'s `instruments` map, so its own digest
  (sha256 `4d7cf12d30f5f39802e7c8c4d7f6fbfa65135f789cee044c6ba7908f93baf6f4`)
  is bound by nothing. I ran it against 69e82c48 and it reports 17/17,
  exit 0 — but that result is not reproducible from the commit alone, and
  the working-tree lesson (`corpus/lessons/round-24.md:131-135`) itself
  discloses the selftest was written *after* the candidate with
  expectations chosen after observing it, i.e. a post-hoc oracle.
- **F5 (Medium) — the committed lesson omits three disclosures the
  working tree makes.** The committed `corpus/lessons/round-24.md` at
  69e82c48 is 71 lines; the working-tree file is 149 lines. The added
  paragraphs include "**Selftest disclosure**" (line 131), "**Timestamp
  error**" (line 136: `claims.json` says `declared_at 16:50:00Z` but the
  freeze commit finalized at 16:44:44Z) and "**Census defect**" (line 139:
  "no live start census was taken before source edits").
  `measure/start-census.json` (untracked) is explicit:
  "the live start census was not taken before SOURCES.md changed (disclosed
  conformance defect)". I reproduced the reconstruction myself
  (`census-base-root` at base → exit 0, same four W04) and it does hold at
  base, so the *numbers* survive; but the defect disclosure for the census
  and the post-hoc-selftest disclosure live only in uncommitted files at the
  reviewed revision.
- **F6 (Medium) — the SCORECARD row points at a measured revision that the
  final section does not name.** The working-tree round-24 table header
  (`SCORECARD.md:2894`) says "Before → after (counting command, **measured
  revision in the final section below**)"; the Round 24 section
  (`SCORECARD.md:2885-2910`) is the last section in the file and names no
  revision — `grep -c 69e82c48 SCORECARD.md` → 0, and there is no
  `Measured at …` line. Round 23's section does carry one
  (`SCORECARD.md` "### Round-23 initial committed measurements — Measured
  source V=`6615aea…`"), so this is a regression in the record format, not
  the house style. The round-24 LOG entry has the same gap. Inference: the
  "after" numbers in the table cannot be tied to a revision by a reader.
- **F7 (Low) — the C2 before/after pair spans two denominators.**
  `claims.json` R24-C2 `before` = "0/10 retained claim freezes disclosed";
  at base the gate audits 10 freezes and discloses 0; at head it audits 11
  (round-24 joins the audited set) and discloses 11/11 — `freeze-gate.py`
  output `{"audited": 11, "clean": 1, "disclosures": {"exact": 11, "of": 11}}`.
  The claim text itself states "r14..r24", so the intent is disclosed, but
  "0/10 → 11/11" in `SCORECARD.md:2897` reads as a like-for-like ratio over
  a set that grew by one. Ledger rows were checked row-by-row against the
  gate's own findings: all 11 match exactly (verdict + finding set).
- **F8 (Low) — the census instrument is unpinned by this round.**
  Round 24 records no digest for `scripts/sources-census.sh`
  (`measure/start-census.json` has no `sha256` field; there is no
  round-24 `census-tool.json`). It happens to be unchanged (O7), but the
  "source census exit 0" no-harm item is not bound to a specific script
  revision by any committed artifact.

## Residual risk / verification gaps

- The six repro inputs were **not** re-downloaded here (1.28 GB, and the
  root disk was at 98 %); the 6/6 positive claim is read from
  `repro/run-1.jsonl` and `repro/receipt.json`, not re-executed. The
  negative control *was* re-executed and still fails correctly (O10).
- `count-c1.py` is Git-object-only and unauthenticated by design; the
  producer `.run.json` records (argv, exit 0, stdout byte-equal to the
  envelope) were re-checked independently for all five envelopes and match
  (`stdout_identical True`, `meta.command` equals the verb, argv names
  `rea-agents@6.5.0`), and the three committed capture files hash equal to
  the `subject.digest.sha256` in their envelopes — but no producer record is
  signed, so "the producer really ran REA" is still an assumption.
- Lane state moved during this review: the working tree gained
  `corpus/SOURCES.md` rows S069–S071, a rewritten first line of the
  round-24 knowledge entry, a re-pointed `tool-pins.json`, an expanded
  lesson and a new `sources/capinfos-4.6.9.adoc` after 69e82c48. All
  findings above are stated against the commit; the working-tree no-harm
  state was re-checked and still holds (0 changed prior S-rows, 0 changed
  prior knowledge blobs, 0 changed prior lessons), but the commit under
  review is now behind the working tree.

## Recommended L1 action

1. **Extend `freeze-gate.py` to bind the claims file's own content**, not
   only instrument bytes: compare the current `claims.json` against the
   freeze-commit copy and raise a finding when any of `claims[*].before`,
   `claims[*].target`, `falsifiers`, `instruments` or
   `instrument_supersessions[*].sha256` differs; verify each disclosed
   supersession's `sha256` against the blob at the disclosed commit
   (`blob_sha256(root, commit, path)`) instead of keying disclosure on
   `(path, commit)` alone. Rationale: F2 shows the current gate reports
   `CLEAN` for three distinct post-freeze edits.
2. **Land the missing no-harm checks as committed instruments** and add
   them to `selftest.py`: (a) prior `corpus/README.md` non-empty lines and
   a blank line immediately before every `## ` heading (F3, the exact check
   M24-2 already claims); (b) pre-round `LOG.md`/`SCORECARD.md` prefix
   preservation; (c) prior `corpus/lessons/*` blob identity; (d) a
   whole-file (not prefix-of-parsed-rows) comparison of `corpus/SOURCES.md`
   so non-S-row prose is covered (F1). Each needs a red case.
3. **Commit the no-harm evidence with the round** — `tools/selftest.py`,
   the `measure/no-harm-*.json` records, `measure/start-census.json` and a
   `census-tool.json` carrying the census script's sha256 — and pin
   `selftest.py` by digest in `claims.json` `instruments` (F4, F8).
4. **Fold the three working-tree disclosures into the committed lesson**
   (selftest disclosure, timestamp error, census defect) before the round
   closes, or state explicitly that they are uncommitted (F5).
5. **Name the measured revision in the round-24 SCORECARD section** and
   fix the table header's "measured revision in the final section below"
   pointer (F6); keep the C2 before/after denominators separate in the row
   text (F7).
6. **Do not treat this seat's report as verification.** The round's state
   at 69e82c48 passes the seven state facts the assignment enumerated
   (O1–O8), but the round-level claims R24-C1/R24-C2 are a separate
   question and remain outside this seat's scope; re-run the L1 gate after
   fixes 1–3 land, since adding the checks above will change both tools'
   digests and therefore require a new freeze/supersession record.
