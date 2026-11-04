# ScribeRows — round-76 W1 seat report

Seat: ScribeRows (scribe), 2026-11-04. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
HEAD `201df797d555d324ee2eb5e3c4b9bbe4fb77d85a`. The seat spec's target — the three source
rows S286 `shlex.split`, S287 `argparse`, S288 `sh(1)` reject — is drafted, located and
mechanically checked under `.ufo/waves/round-76/w1/ScribeRows/`. `corpus/SOURCES.md` was not
edited (read-only), per the spec and the lane bounds.

## Behaviour

- One content GET per frozen URL. `shlex.html` 200 / 66 497 B / `4c1f8bf6…`;
  `argparse.html` 200 / 334 994 B / `14d33eea…`; `man1/sh.1.html` **404** / 196 B /
  `80c3fe2a…`.
- Three rows drafted in the 11-cell grammar, no literal or escaped pipe, ids S286-S288,
  `opened` 2026-11-04, mined / mined / rejected, tier A / A / C.
- Quotes located in the pinned bytes: `shlex.split` entry line 229, 7 words, composite
  (`<em>s</em>`); `ArgumentParser.error` prose lines 2417-2418, 21 words, composite
  (`<em>message</em>`, `<a>sys.stderr</a>`); 404 body line 6, 9 words.
- The reject carries `REJECTED: … . Flip: …` (the shell the gate refuses to invoke; flip is a
  consumer `shell=True` occurrence or a claim about shell semantics) and the required
  consumer search. `grep -c 'shell=True' tools/round-76/plan-command.py` prints `0`
  (grep exit 1); the consumer parses with `shlex.split` at line 107 and calls
  `subprocess.run(argv, …)` at line 162, and declares `--rev`/`--work` required at lines
  333/340 — the consumer the two admits name.

## Gates run (all read-only)

| gate | result |
|---|---|
| row checker (cell grammar, enums, quote contiguity, word counts, digest/locator pins) | `FAILURES: 0` |
| standing census on a scratch fixture from `HEAD:corpus/SOURCES.md` + these rows | rc 0, 24 W04 warnings, no E-finding |
| standing census on a scratch fixture from the worktree registry + these rows | rc 1, `E03` S286/S287/S288 duplicate id |
| independent digest cross-check against `.ufo/waves/round-76/l1/sources/` | shlex and argparse byte-identical; that seat carries `bash.1.html` instead of the 404 `sh(1)` |

## Findings (reported, not resolved)

1. **Id collision with uncommitted work.** The worktree already carries three uncommitted
   rows under S286/S287/S288 (`git blame` = Not Committed Yet; `M corpus/SOURCES.md`,
   sha256 `dde75e6e…`): S286 shlex (mined), S287 argparse (mined), S288 `bash(1)` (rejected).
   These drafts use the frozen ids, so appending them yields `E03` ×3 (mechanical proof in
   `ScribeRows/census-worktree-diff.txt`). Only one row set may land per id.
2. **S288 source substitution.** The frozen spec names
   `https://man7.org/linux/man-pages/man1/sh.1.html`; the uncommitted row rejects
   `bash(1)` at `man1/bash.1.html` (497 852 B, `e35fa296…`) with the note that the plan's
   `sh(1)` 404s. Both reject for the same reason; the draft keeps the frozen URL and records
   the 404 as its disposition.
3. **Uncommitted S286 anchor names the wrong tag.** It says the word `s` sits in a `<var>`
   tag; the served byte at line 229 is `<em>s</em>`.
4. **Uncommitted S287 quote is a mid-sentence fragment** (line 2418 only); this draft quotes
   the full sentence across 2417-2418 so the subject and `sys.stderr` are inside it.
5. **Cadence difference on the rejected row:** uncommitted `180d` vs `on-release` here
   (round-75 rejected-row convention). Both pass E09; a landing choice.

## Touched surfaces

Only `.ufo/waves/round-76/w1/ScribeRows/` (new evidence dir) and this report. No production
file, registry row, script, receipt of another round, or fleet-root path was written; no
`git` write was issued. Scratch `/fast/scratch/hyaku/kaidoku-r76/ScribeRows/` is deleted.

## Out of scope

Landing the rows (L1), the round-76 lesson `## Gate` write (lesson seat), the census over the
real lane, and adjudication of the S288 `sh(1)`-versus-`bash(1)` choice. No claim is made
about `sh(1)` being undocumented elsewhere, and the POSIX `sh.1p.html` page was not screened.

## Artifacts

`.ufo/waves/round-76/w1/ScribeRows/`: `rows.md` (drafts + located quotes + Gate rows +
conflicts), `rows-draft.md` (the three rows verbatim), `receipt.json` (digests, quote-to-line
mapping, gate results), `shlex.html`, `argparse.html`, `sh1.html`, `sha256sums.txt`,
`consumer-search.txt`, `check-rows.txt`, `check-rows.py`, `run-census.sh`, and the five
census outputs with `census-e03.txt` / `census-exits.txt`.
