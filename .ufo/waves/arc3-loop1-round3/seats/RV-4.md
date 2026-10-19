# SEAT RV-4 | CHAIN c1 | ROLE reviewer

Task (seat line): verify the map-token patch is line-neutral on a scratch copy (line
count equal, token set 82->83, prior tokens byte-identical). Seat report.

**VERDICT: PASS** on all three named criteria, for both variants the producer drafted
and for one additional strictly-additive option built by this seat. Producer artifact:
`.ufo/waves/arc3-loop1-round3/claims/c1/records-drafts/map-token-patch.md` (SC-2, rev 1,
sha256 `333ca590716b27126fadd0ca9747dce5742e26c0a897d5090d7d7e6dcea11841`, 4069 B, mtime
2026-10-19 10:08:16 -0300). No corpus/README/SKILL/SCORECARD/LOG writes by this seat;
lane `corpus/README.md` was byte-identical (`6ac43e83…`) at every sample taken.

| variant (derived from the artifact's own fenced lines) | patch sha256 | after README sha256 | lines | tokens | prior 82 | seat criteria | strict r1 additive-only |
|---|---|---|---|---|---|---|---|
| PRIMARY | `022360897c6ca097…` | `016b632e46e5852a…` | 190→190 | 82→83 | identical | **PASS** | False (prose rewritten by design) |
| HONEST-STOP | `36e84521b5522072…` | `829245d5de4435bd…` | 190→190 | 82→83 | identical | **PASS** | False (prose rewritten by design) |
| caller option: strict additive (RV-4 build) | `ec684055d044ccc5…` | `a451ad1664cda0cb…` | 190→190 | 82→83 | identical | **PASS** | True |

## 1. Work performed (evidence pointers)

- **Baseline frozen and authenticated.** HEAD `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`;
  `corpus/README.md` 190 lines sha256 `6ac43e83…`, byte-identical to `git show
  HEAD:corpus/README.md`; byte copy frozen at `claims/c1/RV-4/README.before.md` (same
  sha256). Coverage map (`corpus/README.md:11-69`) = 84 token occurrences / 82 unique;
  mapped 82/82. Command A verbatim at HEAD →
  `claims/c1/RV-4/command-A-before.txt`: `{"citation_resolved_rules": 14, "coverage_score":
  10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82,
  "missing": [], "revision": "c07af80f…", "rule_blocks": 14}`. Independently corroborated
  by EX-14's before-state (`claims/c1/EX-14/before-state.txt`, `…/command-a-before-verbatim.md`)
  — same README sha, same 190 lines, same JSON.
- **Producer artifact located** by an own 60 s poller; its log is a byte copy at
  `claims/c1/RV-4/poll.log` (sha256 `a1799204…`), which carries the tick that first saw the
  artifact verbatim (`13:08:20Z`, `.ufo/waves/arc3-loop1-round3/claims/c1/records-drafts/map-token-patch.md`).
  Read-only: the artifact is SC-2's prose draft (no raw hunks — fenced verbatim lines + a
  substitution recipe).
- **Harness built + self-tested** (`claims/c1/RV-4/verify_map_token.py`, sha256
  `b771d643…`): extracts a fenced diff if present else takes the raw body; applies on a
  scratch copy (`git apply`, then `--unidiff-zero`, then GNU `patch`, with a disk-backed
  `TMPDIR`); measures line count, unique token set, prior-token set + occurrence order,
  hunk scope, files touched, additive-only shape. Self-test teeth:
  `selftest-positive.out` PASS; `selftest-negative-A-newline.out` (row inserted) FAIL on
  line neutrality; `…-B-rename.out` FAIL on prior-token identity; `…-C-drop.out` FAIL on
  removed token. Outputs copied under `claims/c1/RV-4/`.
- **Diffs built mechanically from the artifact's own bytes**
  (`claims/c1/RV-4/extract_and_build.py`, sha256 `2c767fcb…`): pulls the "Old line
  (:38, verbatim)" and the two "New line" blocks, asserts the old line matches the before
  README exactly once, emits `primary.patch` / `honest-stop.patch` + after-states. This
  re-derives SC-2's anchor claim `corpus/README.md:38` — match index `[37]` (0-based) =
  line 38, byte-exact.
- **Cross-tool application.** `git apply` clean (harness), and GNU `patch -p1` dry-run
  rc=0 / apply rc=0 with the same after-bytes (`016b632e…`, 190 lines).
- **Coupling rehearsal** (`claims/c1/RV-4/coupling-rehearsal.sh` + `.out`): scratch clone
  seeded from HEAD **Git objects**, then primary map token + a stub entry file named for
  the token stem; command A at three revisions (below).
- **Citation-drift probe rehearsal** (read-only, no `--snapshot-dir`; the probe never
  writes outside a snapshot dir). A full-tree scratch clone of HEAD (81 MB) was probed
  twice: first against the table as it stood mid-round (31 entries, `738b3a56…` +
  `ff47bfd6…`) — `claims/c1/RV-4/probe-rehearsal.txt` — and again after C3's implementer
  had extended it (57 entries, `bfc42f1b…` + `d97dd60a…`) —
  `claims/c1/RV-4/probe-rehearsal-v2.txt` (sha256 `1c2daca7…`). Both runs: before /
  primary-after / honest-stop-after × default+strict = `findings=0 exit=0`, twelve runs in
  total. Gate files re-hashed after every run: unchanged by this seat.
- **Identity record** (`claims/c1/RV-4/artifact-identity.txt`) plus a machine-derived
  summary (`claims/c1/RV-4/measurements.json`, produced by `summarize.py` — no
  hand-transcribed numbers). The producer artifact's sha256 was re-derived at four read
  points (last at 13:13Z) and did not churn during this seat's run.

## 2. Proposed changes

**none** (reviewer seat; no corpus/README edit authored by this seat). Caller options,
all fully measured, live in `claims/c1/RV-4/` as derived patch text:
`primary.patch`, `honest-stop.patch`, and `caller-option-strict-additive.patch`
(token appended, row prose untouched — the only form for which the r1 additive-only
instrument also reads True). If the parent prefers to land SC-2's recipe rather than a
diff, the substitution is equivalent: both appliers reproduce the same after-bytes.

## 3. Before→after measurement for the chain's claim (c1: line-neutral map token, 82→83)

- **Map-token mechanics (my seat's slice).** Before 190 lines / 82 unique tokens / 84
  occurrences → after 190 lines / **83 unique tokens** / 85 occurrences, exactly one
  changed line (`:38`, inside coverage map lines 11-69), one file touched, all other 189
  lines byte-identical; prior 82 tokens identical as a set **and** in occurrence order;
  `added_content` carries exactly one new token
  `2026-10-19-arc3-r3-evm-optimizer-shapes`; `removed_lines: 0` prior tokens.
  Commands: `python3 verify_map_token.py <patch> README.before.md <scratch>`
  (outputs `primary-verification.out`, `honest-stop-verification.out`,
  `caller-option-strict-additive-verification.out`).
- **Command A coupling (scratch clone, real Git objects).** `82/82 → 83/83`, `missing []`,
  `dangling []`, rules `14/14`, scores `10.0/10.0` at the after revision; the control
  revision (token landed **without** the entry file) reads `knowledge_files 82, mapped 83,
  dangling ["2026-10-19-arc3-r3-evm-optimizer-shapes"]` — the entry/token coupling is real
  and mechanically detectable. `coupling-rehearsal.out`, plus the lane-repo guard line
  showing `corpus/README.md` still `6ac43e83…` after the rehearsal.
- **Freshness side-reading (not c1's claim, recorded as context).** Probe findings 0 in
  both modes before and after — the landing does not perturb the 7 table entries that
  touch `corpus/README.md` (5 line-anchored at `:22`/`:175`, which are stable because the
  change is line-neutral, and 2 SCORECARD→README line-number pointers at `:177`/`:72`
  whose target lines are untouched).

## 4. Attacks / refutations attempted (verdicts)

1. **"Line-neutral means only the token was added."** REFUTED as stated, benignly: both
   producer variants rewrite the row's state prose; the strict r1 additive-only shape
   reads False for them. Precedent evidence: r1's **landed** change
   (`git diff e845c2b HEAD -- corpus/README.md`, one line) is itself token-append **plus**
   prose rewrite, line-neutral — the frozen strictly-additive r1 patch
   (`.ufo/waves/arc3-loop1-round1/claims/c1/RV-4/map-token.frozen.patch`) was not what
   landed. Verdict: the prose-rewriting form is precedent-conforming; the strict form
   remains available as the caller option if the parent wants the additive instrument
   green.
2. **"The patch might sneak changes outside the map row."** REFUTED: one hunk, one
   changed line, hunk start 38 inside the coverage section (11-69), files touched
   `['corpus/README.md']`, whole-file token multiset delta exactly +1 occurrence of the new
   token (none removed) — same single-occurrence pattern as the r1 landed token.
3. **"Prior tokens could be silently re-ordered/renamed."** REFUTED: prior-token set
   identical **and** occurrence-sequence identical for all three variants; synthetic
   rename/drop negatives FAIL the harness as designed.
4. **"The new token could dangle at landing."** CONFIRMED as a real hazard, and shown to
   be detectable: the token equals the entry-file stem
   (`2026-10-19-arc3-r3-evm-optimizer-shapes`) and command A reports the dangling token
   if the entry file is absent. Stem agreement currently holds across every in-flight
   draft that names it (PL-1 plan, `records-drafts/knowledge-entry-draft.md`, SC-2, CR-2)
   — no r1-style stem divergence is live. Verdict: coupling requirement, satisfied in
   draft, to be re-measured by the parent at the records commit.
5. **"The landing could break existing citation-drift pins."** REFUTED by measurement,
   twice: findings 0 in default and strict modes at before, primary-after,
   honest-stop-after, on a full-tree scratch clone — both with the mid-round table
   (31 entries, `738b3a56…`: `probe-rehearsal.txt`) and with C3's extended table
   (57 entries, `bfc42f1b…` + `d97dd60a…`: `probe-rehearsal-v2.txt`). The 7 v1 entries
   touching `corpus/README.md` (5 line-anchored at `:22`/`:175`, 2 SCORECARD→README
   line-number pointers) are unperturbed because the change is line-neutral. Caveat: the
   table is still moving under C3, so the reading must be re-run at the round's commit
   and is bound to the two table shas named above.
6. **"The instrument itself might lie."** Attacked the harness twice: a
   `index A..0000000` header (my own generator defect) makes GNU `patch` exit 1 with
   "Not deleting file…" even though the bytes land — fixed to real blob hashes, after
   which `patch` and `git apply` agree byte-for-byte. Separately, an unresolvable `--rev`
   (`HEAD~2` after a checkout orphaned a scratch commit) makes the probe fail **closed**
   (`revision_unresolvable`, exit 2) rather than silently reporting 0 — recorded as an
   instrument property, and the affected reading was discarded and re-run with explicit
   SHAs.
7. **"Worktree contamination."** REFUTED: every edit ran under `/dev/shm/rv4r3/…`
   (never `/tmp`); the lane `corpus/README.md` sha is unchanged at every sample; the gate
   files were re-hashed after each probe run and changed only by C3's own implementer
   (31→57 entries), never by this seat.
8. **"The artifact's self-identity claims."** One nit, non-blocking: the draft states
   "Revision 1 (2026-10-19T~13:12Z)" while the file's own mtime is 13:08:16Z (epoch
   1792415296) and its sha256 has been stable since — the artifact cannot have been
   written at the later time it names. The draft elsewhere defers identity to the final
   revision, so this is a text nit, not a verified-false identity claim. Everything else
   the draft asserts about itself (target `:38`, old-line bytes, the line-neutral
   mechanic, the 190-line count) was re-derived here and holds.
9. **"The round's record drafts could overstate the map-token result."** Checked against
   the sibling drafts (`records-drafts.md` sha256 `f49aa9ee…`, `knowledge-entry-draft.md`
   sha256 `5c1818c7…`): the records draft restates exactly the mechanics measured here
   (`corpus/README.md:38`, 190 → 190, one line differs, command A 82/82 → 83/83, prior 82
   byte-identical, rules 14/14) and names `map-token-patch.md` as the token source with the
   stem-equality requirement. No divergence found; the round's C1 record set currently
   agrees with the independent measurement.

## 5. Blockers

None. Two landing notes the parent should carry:

- The producer artifact is **prose** (no raw diff), so it cannot be `git apply`ed as-is;
  the diffs in my claims dir are mechanical derivatives of its own fenced lines and are
  reproducible by re-running `extract_and_build.py` against the artifact bytes
  (sha256 `333ca590…`). If SC-2 revises the artifact, that sha and these measurements
  must be re-derived — this seat's verdict is bound to rev 1.
- Command A's `83` depends on the entry file landing with the exact stem the token names;
  this seat's after-state used a **stub** entry (stem coupling only), not the round's real
  entry content, which the EX seats own.