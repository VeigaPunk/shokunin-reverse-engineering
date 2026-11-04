# ScribeSources — round 78, wave 1

**Seat.** ScribeSources (scribe). **Observed at** 2026-11-04T09:10:38-03:00 from
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD
`ffcb47d13f0340f88397af6c8d2707a9554abab3`. **Report:** `.ufo/waves/round-78/w1/ScribeSources.md`.
No lane file was edited by this seat; every write is under `.ufo/waves/round-78/w1/ScribeSources/`.

## Behaviour

- Measured the three committed snapshots at `.ufo/waves/round-78/l1/sources/` from the HEAD blobs:
  `stdtypes.html` 814 496 B / `16f072e19fed1d1a…acf1`, `tomllib.html` 34 923 B /
  `d98e62f75b3a673e…d53a`, `re.html` 257 722 B / `24ef5ff00f937cee…28a6`.
- Located one contiguous quote per snapshot with `grep -n`: stdtypes line 440-441 (8 words), tomllib
  lines 221-223 (17 tokens incl. the ellipsis), re line 283 (13 words).
- Ran the seat-named id scan and the three URL greps. No id collides (HEAD: 197 ids, highest S291;
  working tree: 200 ids, highest S294, no duplicates). No URL collides for stdtypes or tomllib; the
  `re.html` URL is already **S143**'s (`corpus/SOURCES.md:149`).
- Ran the census read-only: exit 0, 23 W04 warnings (the round-77 count), none naming S292, S293,
  S294, `gnupg` or `re.html`.
- Drafted `rows.md` (the two mined rows, pinned; the S294 conflict with both candidates),
  `gate-block.md` (four decision rows, census, plan reconciliation), `shots.txt` (every command and
  output) and `report.json`.

## Registry state found (concurrent landing)

The working tree already carries S292 (`stdtypes`, mined), S293 (`tomllib`, mined) and **S294 = the
GnuPG handbook, rejected** — not the frozen plan's `re.html`. The `re.html` snapshot is deleted in the
working tree (uncommitted; still committed at HEAD). The L1's `l1/pre-append-url-check.txt` records the
duplicate-URL check that saw S143 (re) and S263 (hashlib) before that landing. This seat did not touch
any of it.

## Gates

- **Access date** 2026-11-04 on every drafted row. **HTTP 200** is the landing's recorded fetch status;
  this seat re-measured bytes and digests only and did not re-fetch.
- **Quote discipline**: each quote is a literal contiguous `grep -n` excerpt, ≤25 words/tokens; the
  landed S292/S293 anchor cells cite one line where the sentence spans two or three, and the drafts
  correct the span (reported as a note, not as an edit).
- **used-by**: S292 → `corpus/knowledge/2026-11-04-r78-attack-gate.md`; S293 →
  `corpus/knowledge/2026-11-04-r78-surface-recheck.md`; the reject row (either candidate) → `—`.
  Both cited entries exist in the working tree, are untracked, and cite their row at line 1.
- **No duplicate URL is registered**: `re.html` is withheld (S283 precedent, round-75 lesson), not a
  second row.

## Touched surfaces

Writes (all under the evidence dir):
`.ufo/waves/round-78/w1/ScribeSources/{rows.md,gate-block.md,shots.txt,report.json}` and this report.
Reads: the three snapshots (and the HEAD blob of `re.html` through `git show`), `corpus/SOURCES.md`,
`plans/round-78-claims.md`, the two round-78 knowledge entries, `corpus/lessons/round-75.md`,
`tools/round-77/prefile-receipt.py`, `tools/round-78/{attack-gate.py,surface-recheck.py}`, the round-78
`l1/` receipts, and read-only `git`.

## Out of scope (not done)

- No lane edit: the SOURCES rows, the lesson, `PROVINCE.md` and the knowledge entries are the L1's to
  land.
- No re-fetch of any URL; no network source was opened.
- No execution of the round-78 instruments; their measured arms belong to the executor/reviewer seats.
- No decision on the S294 conflict: `rows.md` §3 states the two admissible outcomes.

## Findings

1. S292's landed anchor cites line 441; the quoted sentence starts on 440. S293's cites line 221; the
   span is 221-223. Drafts carry the corrected spans.
2. The frozen plan says "S294 `re.html`, rejected"; the registry instead rejects the GnuPG handbook at
   S294. Both are defensible; only one can hold, and the lesson's Gate block must match the registry.
   If the plan's letter must hold, the GnuPG row moves to S295 **before** the landing commit, because
   committed ids are never reused.
3. `re.html` cannot be a new row: its URL duplicates S143, which already mines `re.fullmatch`; the
   round-75 lesson withdrew S283 on exactly this ground.
4. The GnuPG row's `used-by` is `-` where S291 uses `—`, and its anchor states 12 words for an 11-word
   quote. Cosmetic, both under the 25-word cap.
5. The re.html snapshot exists only in git right now (working-tree deletion is uncommitted).
6. The two `used-by` targets are untracked; a landing commit that omits them leaves dangling cells.

## Artifacts

- `.ufo/waves/round-78/w1/ScribeSources/rows.md` — the two mined rows verbatim-ready, the S294
  candidates, the collision evidence, the resolution options.
- `.ufo/waves/round-78/w1/ScribeSources/gate-block.md` — the lesson `## Gate` text.
- `.ufo/waves/round-78/w1/ScribeSources/shots.txt` — commands and outputs.
- `.ufo/waves/round-78/w1/ScribeSources/report.json` — machine-readable findings.
- This report.

## Tooling

No installs or upgrades. `git`, `grep`, `sha256sum`, `wc`, `awk` and the lane's read-only census script
were used; scratch `/fast/scratch/hyaku/kaidoku-r78/ScribeSources/` was removed before yield.
