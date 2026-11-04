# Sources opened — ScribeLesson, round 69 w1

Access date 2026-11-03 (-03; re-open instants at 2026-11-04T02:34-02:42Z). Every entry was opened by
this seat; nothing is quoted from a peer without its path.

## Live URLs (curl -fsSL, bytes and sha256 measured by this seat)

| url | http | bytes | sha256 |
|---|---|---|---|
| https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx.1 | 200 | 40 077 | `09552b3cf4e9073c288060b8f50ed1c1dde3dca89dcaf1230367b6c3e15d4e25` |
| https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx-doc.txt | 200 | 37 208 | `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42` |
| https://github.com/upx/upx/releases/tag/v5.2.0 | 200 | 162 743 | `d9770b01652949f0fcf667d985767d1b0f7fbff9847c66342e2c10454296fad1` |
| https://man.archlinux.org/man/upx.1.en | 200 | 47 791 | `aed1c12a62e54bbe04f718e9184b3c912dbf254fc98233771809e8536143ea04` |

Locators measured inside the fetched bytes: `upx.1` line 164
(`\&\fB\-\-version\fR: print the version of \fBUPX\fR`), checksum sentence 112-114;
`upx-doc.txt` line 99 (byte offset 3 653), literal quote, 6 words; `grep -c 'print the version'` = 0 in
the release page, 1 in the Arch mirror.

## Lane files read (read/bash/git, all read-only)

- `corpus/lessons/round-68.md` (full), `corpus/lessons/round-68-verifier-spotcheck.md` (full),
  `corpus/lessons/round-67.md` (full).
- `plans/round-69-claims.md` (full), `.ufo/waves/round-69/claims.json` (full).
- `.ufo/waves/round-69/l1/census-start.txt` (full: 19 W04 + `ok`).
- `.ufo/waves/round-69/l1/pre/c1-at-base.json`, `c2-at-base.json`, `c3-at-base.json` (raw),
  `controls-at-base.json` — parsed with python3 `json`; c3 required stripping its first line.
- `.ufo/waves/round-68/l1/scores/c2-at-landing.json` (keys, carrier key list, arms, counts,
  `rev`, `instrument`, `packer`).
- `tools/round-69/packed-elf.py` (lines 60-173, 259-333, 454-543), `tools/round-69/mutation-check.py`
  (patch sets, validate, kill logic), `tools/round-69/contract-probe.py` (`validate`).
- `tools/round-68/packed-elf.py` (sha256 only), the four round-69 tool sha256s.
- `corpus/SOURCES.md` (rows 180-187; row counts at base/declaration/freeze via `git show`).
- working-tree diffs: `corpus/SOURCES.md` (+S270), `corpus/README.md`, `PROVINCE.md`,
  `corpus/knowledge/2026-11-03-r68-packed-elf-route.md`; untracked
  `corpus/lessons/round-69.md` (56 lines, full) and
  `corpus/knowledge/2026-11-03-r69-packed-route-contract.md` (head).
- `git` read-only: `log`, `show`, `diff`, `status`, `rev-parse` on the lane; the freeze commit
  re-derived with `--diff-filter=A`.
- `scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kaidoku` (read-only; 177 rows
  in the uncommitted tree, 176 at every committed round-69 revision).

## Peer drafts opened (not claim input; cited by path)

- `.ufo/waves/round-69/w1/ReviewerGates/attacks.json`, `review.md`, `freeze-integrity.json`, and the
  attack fixtures (`missing-identity-arm`, `one-carrier-no-arms`, `nan-ratio`, `boundary-075`,
  `boundary-over075`, `explicit-false-arm`, `foreign-instrument-receipt`, `mutation-invented-kills`,
  `probe-invented-arms`).
- `.ufo/waves/round-69/w1/ExecC3/c3-at-landing-exec3.json` (head), `w1/ExecC3.md` (existence).
- `.ufo/waves/round-69/w1/SentinelScope/audit.md` §1.1-1.2 (head), plus mtimes of the tracked files.
- `.ufo/waves/round-69/w1/ExecRepairs/evidence/` (listing + the four `r24-gate-*.json` rev fields).

## Not available at writing

- `.ufo/waves/round-69/w1/ScoutSource/` — empty, no `sources.md` (measured `ls`).
- `.ufo/waves/round-69/l1/scores/` — empty, no after receipt (measured `ls`, 2026-11-04T02:37Z).
