# R45W1SrcGitDiffTree — S141 live open, registry row, Gate block, quote proof

Seat `R45W1SrcGitDiffTree` (scribe), round 45 wave 1, lane `kaidoku`. Leaf member: no subagent
dispatch. Markers at issue: `w1`, evidence drafting for the landing, sources opened before data.

## Behavior

1. Opened source S141 live: `https://git-scm.com/docs/git-diff-tree` → HTTP **200**, **256,810**
   bytes, sha256 `f81c1e3141b2e8e2cfc5790b8923881862f964ae5e3f85c157299b71f80c9640`, curl exit 0,
   UTC **2026-10-28T15:38:50Z**. Saved copy kept under the seat dir and re-hashed in place.
2. Located **both** statements the assignment names, with `<dt>`/`<h2>` anchors and raw line
   locators of the saved copy:
   - `--name-status` + `-z`: anchor `Documentation/git-diff-tree.txt--z` (raw 3644), sentence at
     raw 3646-3647 — *"When --raw, --numstat, --name-only or --name-status has been given, do not
     munge pathnames and use NULs as output field terminators."* (**20 words**).
   - raw-diff format: anchor `_raw_output_format` (raw 5369), field list from raw 5418; separator
     lines 5453 (`a tab or a NUL when -z option is used.`), 5459 (`…; only exists for C or R.`,
     **16 words**), terminator 5465 (`an LF or a NUL … to terminate the record.`).
3. Wrote the 11-column registry row (used-by `corpus/lessons/round-45.md`) and a two-row Gate
   block into `row.md`, and proved both quotes are substrings of the **saved** copy (tag-strip +
   whitespace-normalise + `in` test, exit 0, `prove.json` hashed).
4. Audited the already-landed row and found no drift: `corpus/SOURCES.md:147` at HEAD
   `faa875bc0eb839d15b83c4afa6078819e5a7b381` (landed by `e715263cb51b713c342ab992d527fe9d61d6f8ff`)
   carries exactly 11 cells, the same URL, HTTP code, byte count and sha256 I measured, and
   `used-by corpus/lessons/round-45.md`. `S1xx` rows went 40 (freeze `f762b72`) → 42 (HEAD).
5. Registry acceptance re-run read-only: `scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin kaidoku` → exit **0**, `kaidoku ok`, no `S141` line, 14 `W04`.
6. Cross-checked the instrument that the S141 justification names, and receipted the documented
   framing empirically on scratch fixtures with git 2.56.0.

## Gates

| gate | command | exit | stdout sha256 | UTC |
|---|---|---|---|---|
| live open | `curl -sS -L --max-time 60 -o s141.html -w '%{http_code}\n' https://git-scm.com/docs/git-diff-tree` | 0 (HTTP 200) | file `f81c1e31…` | 15:38:50Z |
| quote proof | `python3 -I -B prove.py …/s141-git-diff-tree.html` | 0 | `aaf83dca1c70…` | 15:40:17Z |
| semantic receipt (name-status ± `-z`) | `./fixture_receipts.sh "$S"` | 0 | `8823a38b4a1c…` | 15:40:49Z |
| raw format `-z` | `git -C "$R" diff-tree -r -M --raw --no-commit-id -z "$C" \| od -c` | 0 | `397180684930…` | 15:40:55Z |
| preflight's own invocation | `git -C "$R" log -m --diff-merges=first-parent --name-status --format=%x00%H -1 "$C"` | 0 | `0179ac749dfc…` | 15:41:14Z |
| registry census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | 0 | `9f32a8a84ef1…` | 15:41:58Z |

`0` = met/clean on every line above. No gate in this seat exits 2: every value was evaluable.

## Touched surfaces

Written (inside the seat dir only):
`row.md`, seat report copy `report.md`, `s141-git-diff-tree.html`, `prove.py`, `prove.json`,
`prove.exit`, `utc_prove`, `fixture_receipts.sh`, `fixture-transcript.txt`, `fixture.exit`,
`utc_fixture`, `raw-transcript.txt`, `raw.exit`, `utc_raw`, `log-transcript.txt`, `log.exit`,
`utc_log`, `census.out`.
Plus the instructed trailer file `.ufo/waves/round-45/w1/R45W1SrcGitDiffTree.md` (this file).

Read-only: `plans/round-45-claims.md`, `corpus/SOURCES.md`, `corpus/lessons/round-45.md`,
`tools/round-45/{frozen-path-preflight.py,c1-counter.py,c2-counter.py}`,
`scripts/sources-census.sh`, plus `git log/show/rev-parse/status` on the lane.

Not touched: `SKILL.md`, `plans/`, `tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`, `.ufo/state/`,
`.ufo/watchdog.log`, `.scratch/`, any sibling lane dir, the fleet repo. No `git add/commit/
checkout/reset/switch/pull/push`, no `jj` mutation, no network write, no package install.

**Contract deviation, self-corrected.** One receipt capture ran without `cd "$S"`, so four files
(`log-transcript.txt`, `log.err`, `log.exit`, `utc_log`) landed in the fleet root
`/home/vgpnk/Projects/shokunin/` at 12:41 local. They were moved into the seat dir immediately and
the fleet root was re-listed to confirm they are gone (`ls` → "No such file or directory" for all
four). Residual fleet-root changes in `git status` (`.ufo/l0-questions.md`, `.scratch/*`, `o.bin`)
pre-date this seat and were not touched.

## Findings

- **F1 (depth, landing evidence).** The drafted Gate row cites only quote A. The preflight's rename
  arm handles a record with two pathnames, which is exactly what the raw-format C/R sentence
  (raw 5459) licenses. Two-row Gate block supplied in `row.md` §4.
- **F2 (calibration defect in the drafted lesson).** `corpus/lessons/round-45.md` `## Gate` labels
  the S141 quote "(23 words)". Measured 20 by `wc -w` and by `prove.py`. Over-stated by 3; the ≤25
  bound is met either way; no counter reads the cell.
- **F3 (instrument/source mismatch, no predicate effect).** `tools/round-45/frozen-path-preflight.py:32`
  says "with --name-status, `-z` terminates fields with NUL", but line 93 invokes
  `git log … --name-status` **without** `-z` and lines 99-107 split on `"\t"`;
  `tools/round-45/c1-counter.py:53` runs `git log --name-only --format=` without `-z` too.
  Receipt D shows that invocation returns C-quoted pathnames (`"\303\251.txt"`, `"tab\there.txt"`).
  Verdict-neutral for the frozen ASCII paths (`plans/round-45-claims.md`, `tools/round-45/`) because
  the `ls-tree --name-only` side is quoted the same way and `ok = not touched and not
  blob_changed and not restored and not dirty` never cross-compares representations. The sentence
  is stronger than the code; the repair (`-z` + `\x00` splitting) was **not** applied — the
  instrument is frozen and this seat reports, never fixes.
- **F4 (coverage of the instrument's own claim).** The preflight's 11 selftest cases contain no
  case exercising a pathname that git would munge (`grep` for `quotePath|quote|nonascii|munged` →
  none). `cases >= 11` (C1 clause 6) is met at exactly 11.
- **F5 (recorded value, not an asserted defect).** The lesson claims the round-end census prints
  16 `W04` warnings; measured at HEAD: exit 0, `kaidoku ok`, **14** `W04`, no S141 line. `W04` is a
  cross-scope duplicate class, so other lanes' registries can move it.

## Empirical receipts worth citing

`git diff-tree -r -M --name-status --no-commit-id -z <C>` on a fixture that renames `old.txt` →
`new.txt` and modifies `é.txt` and a tab-containing name:

```
R   1   0   0  \0   o   l   d   .   t   x   t  \0   n   e   w   .   t   x   t  \0
M  \0   t   a   b  \t   h   e   r   e   .   t   x   t  \0   M  \0 303 251   .   t   x   t  \0
```

7 NULs = 3 (rename) + 2 (tab path) + 2 (`é` path): one NUL terminator per field, raw bytes in the
pathname, status and pathname as separate fields. Without `-z` the same commit prints
`M\t"tab\there.txt"` and `M\t"\303\251.txt"` — quoted, C-escaped, i.e. munged. This is the direct
evidence for statement A and the reason a gate must not parse the un-`-z` form for path equality.

## Out of scope / not run

- The C1 and C2 counters and the preflight `--selftest` were **not** run here (other wave-1 seats
  own them); no `failing == []` or `met_target` value is claimed by this seat.
- No claim predicate was edited, no SKILL block drafted, no lesson row appended, nothing committed.
- No installs, so no tooling record beyond versions observed: curl 8.23.0, git 2.56.0, python 3.14.8.

## Artifacts

- `.ufo/waves/round-45/w1/R45W1SrcGitDiffTree/row.md` — 11-column row, two-row Gate block, §2
  locators, §5 proof table, §6 receipts, §7 findings, §8 receipt hashes.
- `.ufo/waves/round-45/w1/R45W1SrcGitDiffTree/s141-git-diff-tree.html` — saved copy, sha256
  `f81c1e3141b2e8e2cfc5790b8923881862f964ae5e3f85c157299b71f80c9640`.
- `.ufo/waves/round-45/w1/R45W1SrcGitDiffTree/{prove.py,prove.json,prove.exit,utc_prove}`.
- `.ufo/waves/round-45/w1/R45W1SrcGitDiffTree/{fixture_receipts.sh,fixture-transcript.txt,fixture.exit,utc_fixture}`.
- `.ufo/waves/round-45/w1/R45W1SrcGitDiffTree/{raw-transcript.txt,raw.exit,utc_raw}`.
- `.ufo/waves/round-45/w1/R45W1SrcGitDiffTree/{log-transcript.txt,log.exit,utc_log}`.
- `.ufo/waves/round-45/w1/R45W1SrcGitDiffTree/census.out`.
- `row.md` §8 is the hash/time inventory for every file above.

Scratch `S=/fast/scratch/hyaku/kaidoku-r45/R45W1SrcGitDiffTree` is removed after the receipts were
copied; nothing under `/tmp` was used or cited.
