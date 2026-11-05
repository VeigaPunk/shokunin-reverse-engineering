# ScribeKnowledge — round 96 attempt 1, lane kaidoku

Seat: ScribeKnowledge (scribe). Item: draft the knowledge entry, the S321 registry row
and the lesson drafts. **No lane file was edited** except this seat's own directory and
this report.

Axes named: **coverage** (the knowledge entry now names the kill-rule blind-spot class
and the fresh-source arm's second source), **depth** (each published number is traced to
a committed byte and a named command), **calibration** (every number the drafts publish
is a measurement, and the draft says explicitly where a claim is *supplementary* rather
than part of the frozen label), **freshness** (the entry opens with the provenance trio
and a `recheck:` command this seat actually executed).

## What this seat wrote (all under `.ufo/waves/round-96/w1/ScribeKnowledge/`)

| file | what it is | lands as |
|---|---|---|
| `knowledge.md` | the draft of `corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md` | the knowledge entry, at the landing commit |
| `sources-row.md` | the draft of the **S321** row for `corpus/SOURCES.md`, with a field-by-field justification and the row-change log | the appended registry row |
| `lesson-gate.md` | the draft of the `## Gate` section for `corpus/lessons/round-96.md` | the lesson's Gate section |
| `corrections.md` | the draft of the **R95-VD-2** correction entry (append-only) for `corpus/lessons/round-96.md`, plus one reported observation | the lesson's Corrections section |
| `verify.md` | the seat's verification evidence (every command, exit code and receipt path) | not landed; the L1's audit trail |

Plus this report, `.ufo/waves/round-96/w1/ScribeKnowledge.md`.

## The four drafts, in brief

**1. knowledge.md** — opens with the provenance trio (`source:` / `verified-at:` /
`recheck:`) as its first three lines. `source:` cites **S321** (`/usr/bin/printf`,
sha256 `b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7`, measured by
`tools/round-96/fresh-source2-check.py`, receipt
`.ufo/waves/round-96/pre/s321-fresh-source2-at-base.json`) **and** the wave evidence for
the kill-rule closure (the three before receipts and the three after receipts).
`verified-at:` names 2026-11-05 and the landing-commit placeholder `<landing-commit>`,
plus the four instrument digests (all four are the committed
`.ufo/waves/round-96/pins.sha256` values). `recheck:` is `sha256sum /usr/bin/printf`
plus a `fresh-source2-check` rerun — **executed by this seat**, see §"Recheck" below.

Sections: (a) the kill-rule blind-spot class (M95-h, the five survivors M2/M3/M4/M6/M10
and *why* the frozen rule could not see each, then the seven named checks of
`kill-rule-v2` with their **measured** kill attribution); (b) the unbound fields (M95-g,
the six forgeries with their typed reasons, the `counts-missing-key`/`counts-type`
typed schema, the downward met binding, the mandatory `--json-out`, and the red
fail-closed evidence); (c) the probe's own write escape (M95-i) and its closure; (d)
the second fresh source S321, with its measured label and the explicit statement that
it is **supplementary, not part of the frozen label**; (e) the six named limits carried
from the declaration, plus the unchanged PE/Mach-O gap.

**2. sources-row.md** — the S321 row in the exact 11-column format of the registry
table, in the `|`-delimited single-line shape the fleet census parses. Field-by-field
justification for every column; the landing requirement (the row, the knowledge entry
and the lesson file must land **in one commit**, else the census's `E11` fires against
S321 alone); the row-change log (**S321 appended; no existing row edited**; registry
225 → 226).

**3. lesson-gate.md** — the `## Gate` section: the S321 record row (source path,
sha256, access date 2026-11-05, the ≤25-word located measurement line
`fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1 met True`, and the
receipt path); the **admit** (S321) and one explicit **non-admission** from the same
measurement family (`/usr/bin/head`'s supplementary run — recorded in
`.ufo/waves/round-96/w1/ExecFreshSource.md` step 4, **not** admitted as a row, with the
flip condition stated: admit it as S322 only if a later claim rests on the held-out
arm being a property of **at least three** distinct host binaries rather than two); the
row-change log.

**4. corrections.md** — the **R95-VD-2** correction, append-only, naming both
superseded r95 texts verbatim (`corpus/lessons/round-95.md:19` and
`corpus/knowledge/2026-11-05-r95-receipt-world-binding.md:41`): the tag-stripped
`open(2)` page states `O_NOFOLLOW` **six** times, not five, with the counting command.
The correction names the occurrence the round-95 enumeration missed (the `HISTORY`
section's own `O_NOFOLLOW` / `POSIX.1-2008` entry), lists all six with their page
locations, and states what the correction does **not** change (the admit/reject
decision, the S320 row, the registry). It also carries one **reported, not corrected**,
observation — the M6 kill-attribution divergence (see below).

## Commands this seat ran, with exit codes

Every command below was run by this seat; none is quoted from another seat's report
except where explicitly attributed.

| # | command | exit | result |
|---|---|---|---|
| 1 | `sha256sum /usr/bin/printf` | 0 | `b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7  /usr/bin/printf` — matches the committed pin |
| 2 | `python3 -I -B tools/round-96/fresh-source2-check.py --root . --work $S/recheck/work --rev 3baac2ef4b9b2830d299125b8184ca06d9e6584d --json-out $S/recheck/receipt.json` (in the scratch clone) | **0** | stdout `fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1 met True exit 0`; receipt equals the committed base receipt **except `revision`** |
| 3 | `bash scripts/sources-census.sh validate --file corpus/SOURCES.md --root . --today 2026-11-05` — **arm A**, S321 row appended, consumer absent | **1** | `file E11 S321 missing used-by corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md` |
| 4 | same — **arm B**, consumer present | **0** | no E-code against S321; 32 `W04`, identical to the lane baseline's 32 |
| 5 | `bash scripts/sources-census.sh census …` baseline vs with-row | 0 | rows 225 → **226**; tier.A 205 → **206**; status.mined 201 → **202**; invalid 0 |
| 6 | `python3 -c "…tag-strip…" > /tmp/s320-stripped.txt && grep -o 'O_NOFOLLOW' /tmp/s320-stripped.txt \| wc -l` | 0 | **6** |
| 7 | `grep -o 'O_NOFOLLOW' .ufo/waves/round-95/l1/scores/s320-open2-fetch1.html \| wc -l` | 0 | **6** (same count before and after tag-stripping) |
| 8 | `upx --version` / `python3 --version` | 0 | `upx 5.2.0` (UCL 1.03, zlib 1.3.1.1-motley) / `Python 3.14.8` |
| 9 | programmatic read of `.ufo/waves/round-96/l1/scores/c1-at-decl-worktree.json` for the per-mutant kill attribution | 0 | the measured attribution table in `verify.md` §5 |
| 10 | programmatic read of `.ufo/waves/round-96/mutants.json` (`forgery_reasons`, `kills_via`) | 0 | the six intended reasons; the declared attribution |

**No tool was installed or upgraded by this seat**, so the operator tooling directive in
`/home/vgpnk/.omp/agent/RULES.md` has nothing to record beyond "no install performed".

## Findings

**F1 — the round-95 prose count of `O_NOFOLLOW` is six, not five (this is R95-VD-2).**
The committed round-95 fetch `.ufo/waves/round-95/l1/scores/s320-open2-fetch1.html`
(76 506 B, sha256 `d665489c…`) carries the flag **six** times — the file-creation-flag
list, the `O_NOFOLLOW` description, the two `O_PATH` occurrences, the `ERRORS` entry,
and, the one the round-95 enumeration missed, the `HISTORY` section's own
`O_NOFOLLOW` / `POSIX.1-2008` entry. The count is 6 both before and after tag-stripping
(every occurrence is the bare token; none is split across a tag boundary). The round-95
lesson (`corpus/lessons/round-95.md:19`) and the round-95 knowledge entry
(`corpus/knowledge/2026-11-05-r95-receipt-world-binding.md:41`) both say "five times".
The correction entry with the counting command is drafted in `corrections.md`; the
round-95 files are **not** edited (they are historical; the correction is append-only in
the round-96 lesson). The admit/reject decision is unaffected — only occurrence 2
carries the rule, and only that one is admitted.

**F2 — the mutant table's declared kill attribution for M6 diverges from the measured
one (reported, not corrected).** `.ufo/waves/round-96/mutants.json` declares M6
(the removed `revision-not-bound` branch) to be killed by "K-dmain shortrev"; the
measured receipt shows **M6 is killed by K-selftest**, because the v6 counter's selftest
carries a `verify-catches-wrong-revision` case that trips first, while K-dmain's
`shortrev` scenario still exits non-zero for other reasons and reads `ok: true`.
**M6 is killed either way**, so the frozen label, the kill rule and the mutant table
are unaffected; only the attribution differs. The knowledge draft reports the measured
attribution and names the divergence; the frozen mutant table is not edited. The L1 may
carry this as a lesson mistake row (*class · evidence pointer · captured-by · fix*;
evidence pointer: `.ufo/waves/round-96/mutants.json` and
`.ufo/waves/round-96/l1/scores/c1-at-decl-worktree.json`).

**F3 — the S321 row has a landing-order requirement, and it is E11-exact.** The census
fires `E11` against a `mined` row whose `used-by` path is absent from disk. At the
declaration neither `corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md` nor
`corpus/lessons/round-96.md` exists. Measured both arms in the scratch clone: with the
row and no consumer the validator exits **1** with `E11 S321 missing used-by
corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md`; with both present it exits
**0** with no E-code against S321 and the same 32 `W04` as the untouched baseline. The
row, the knowledge entry and the lesson file must land in **one commit**.

**F4 — the `recheck:` command the entry publishes is executable and reproduces the
committed measurement.** The knowledge draft's `recheck:` line names
`sha256sum /usr/bin/printf` plus a `fresh-source2-check` rerun; this seat ran both.
The rerun's receipt equals the committed base receipt field-for-field **except**
`revision` (the revision the run was invoked at) — `label`, `counts`, `deterministic`,
`collides_public_packed`, `intact_identity`, `blocks`, `packed_sha256`, `source`,
`source_sha256`, `exit`, `met_target` and all four cell records are equal.

**F5 — the honest arm's K-probe row reads `followed-symlink`, and that is correct.**
In the after receipt the honest arm's K-probe row reads `verdict "followed-symlink"`,
`victim_intact false`, `receipt_valid true`, `met false` — because K-probe is pointed
at the round-94 v4 writer, which does follow a planted link, and K-probe scores
*consistency*, not hardness. The hardened leg is the separate public probe run
(`.ufo/waves/round-96/l1/scores/c1-symlink-v6-at-decl.json`: `verdict "hardened"`,
`victim_intact true`, `receipt_valid true`, `tmp_is_symlink true`, `tmp_left true`).
The knowledge draft states this so a later reader does not read the honest arm's
`followed-symlink` as a failure.

**F6 — the red fail-closed evidence is a process exit 1, and the receipt's own `exit`
field reads 0.** `honest-pos-red-head-not-bound.json` records `head null` and no
`selfverify` key; the `.stdout` reads `selfverify ok=False reasons=1` and the label
line ending `met True exit 1`; the `.stderr` reads `selfverify reason:
head-not-bound`; the `.rc` file reads **1**. The receipt JSON's own `exit: 0` is the
*battery's* inner exit, which was fine. The draft distinguishes the two so the red
evidence is not misread.

## Out of scope (and why)

- **R96-C2's craft block 35, QUALITY 193/194 and the SKILL.md registry rows.** Those
  are the craft-block seat's (`ScribeBlock35`). This seat's drafts touch only the
  knowledge entry, the S321 row and the lesson's Gate / Corrections sections; the
  knowledge draft names the craft block only as the C2 claim's subject and asserts
  nothing about its content.
- **R95-VD-1 (landing-revision receipts)** and **R95-VD-3 (registry rows for the four
  round-95 instruments)**. VD-1 is discharged by the round's own after-side receipts
  naming the landing revision; VD-3 is the R96-C2 registry work. Neither is drafted
  here — `corrections.md` says so explicitly rather than silently omitting them.
- **The frozen counting commands were not re-run.** The seat's item is drafting; the
  reproduction seats are `ExecRepro` and `ExecFreshSource`. Every number the drafts
  publish comes from a committed receipt, so nothing depends on a fresh run of the kill
  rule, the battery or the probe.
- **No lane file, host state, `~/.local/bin` path or fleet-root file was written.** The
  scratch tree `/fast/scratch/hyaku/kaidoku-r96/ScribeKnowledge/` held one
  `git clone --shared` clone and the recheck receipt and was removed before finishing.

## Bounds observed

- Read-only on the lane repo: the only lane writes are this seat's directory
  (`.ufo/waves/round-96/w1/ScribeKnowledge/`) and this report
  (`.ufo/waves/round-96/w1/ScribeKnowledge.md`). No lane file was edited, created,
  deleted, staged or committed; no mutating git/jj command was run anywhere.
- Scratch: one `git clone --shared` clone under
  `/fast/scratch/hyaku/kaidoku-r96/ScribeKnowledge/clone`, removed before finishing.
  The clone's `git rev-parse --show-toplevel` was asserted to print the clone path
  before any use of it.
- No subagent spawns, no background jobs beyond this seat's own commands, no
  `agent://all` message, no `.ufo/state/`, `MANIFEST.json`, `templates/`, `scripts/` or
  sibling-lane write, no `/home/vgpnk/Projects/shokuknow` access.
- No host mutation: no sysctl, no `/proc/sys` write, no service or namespace change,
  no pacman transaction, no install or upgrade.
