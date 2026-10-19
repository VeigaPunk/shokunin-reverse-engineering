# EX-22 — frozen-run stability (chain c2, arc3-loop1-round2)

Seat EX-22 | chain c2 | role executor | 2026-10-19 | repo HEAD `14b1682`
(round-1 records; work commit `fbbbd45`).

Task: recover the PRE-round census (`git show HEAD:.ufo/gates/c1-census-v10.py`,
sha256 `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b`) to
scratch, re-run it on the pre-edit tree so its verdicts match round-1's recorded
readings, then run the same script on the post-edit tree and show that only the
new H1/H3 classes may differ.

One seat-artifact caveat up front (rule #14 discipline): the real target moved
several times inside this seat's window. Every reading below is labelled with
the instrument revision that produced it; the closing revision is recorded in
§6 and re-verified at close. Scratch: `/var/tmp/ex22` (never `/tmp`). Writes:
this directory + `seats/EX-22.md` only; the real target was read-only to me.

## 1. Identity — trees and instruments

| item | sha256 |
|---|---|
| pre-round instrument (HEAD blob) | `6f1d19ff…` (490 lines; == worktree at seat start) |
| pre-edit tree snapshot `tree-pre` | PROVINCE `d075a3c67e17ae…` (162 l), SKILL `483b0eba27458c…` (371 l), SCORECARD `a7c72950094eca…` (1417 l) — identical to the worktree |
| round-1 work tree `tree-r1work` (`fbbbd45`) | PROVINCE `d075a3c6…`, SKILL `483b0eba…`, SCORECARD `30129a98d6f3f3…` (1336 l) |
| round-1 pre-work tree `tree-r1pre` (`e845c2b`) | PROVINCE `d075a3c6…`, SKILL `5c93c7c1bf45c7…`, SCORECARD `30129a98…` |
| round-1 recorded capture | `claims/cross/VZ-4/c3-census-after.txt` = `3b677b8ee47eccb217616eba641fc0b66f72e53634a5ae51a92f8b04e2a22418` |

Rebuild recipe and all fixture/instrument hashes: `evidence/fixtures.md`.
Custody paths were only hashed/stat'ed, before and after (`evidence/custody-readonly.txt`):
5/5 sha256 identical, `.kimi-code/config.toml` inode/ctime unchanged.

## 2. Pre-edit tree — the pre-round instrument reproduces round-1's readings

| run (`evidence/runs/`) | tree | exit | verdict | stdout sha256 |
|---|---|---|---|---|
| `v10-r1work` | round-1 work tree | 0 | PASS 0/0/0/0 | `3b677b8e…` — **byte-identical to the recorded capture** (`cmp` clean) |
| `v10-r1pre` | round-1 pre-work tree | 0 | PASS 0/0/0/0 | `3b677b8e…` (the r1 work edit moved no census byte) |
| `v10-pretree` | pre-edit tree at HEAD | 0 | PASS 0/0/0/0 | `d3da7509…` (records-commit reading; SCORECARD 1336 → 1417 l, loci 9 unchanged) |
| `v10-pretree-rerun` / `-cwdroot` / `-hs0` / `-hs1` | pre-edit tree | 0 | PASS | `d3da7509…` ×4 — rerun, `cwd=/`, `PYTHONHASHSEED=0/1` all byte-identical |

So the pre-round instrument's verdicts match round-1's recorded readings both
(a) exactly, at the r1 tree where a recorded digest exists, and (b) in verdict
and 0/0/0/0 counts at the current HEAD tree.

## 3. Post-edit tree — only the new classes differ

2×2 (v10 = pre-round instrument, v11 = landed post-edit instrument):

| instrument × tree | exit | verdict | stdout sha256 |
|---|---|---|---|
| v10 × pre-edit tree | 0 | PASS 0/0/0/0 | `d3da7509…` |
| v10 × post-edit tree (snapshot and real root, `v10-postedit-*`) | 0 | PASS 0/0/0/0 | `d3da7509…` — the instrument edit is invisible to the pre-round script |
| v11 × pre-edit tree (`v11final-pretree`, `v11final-worktree`) | 0 | PASS 0/0/0/0 | `1db2ec31…` |
| v11 × round-1 work tree (`v11final-r1work`) | 0 | PASS 0/0/0/0 | `30a06521…` |

Deltas are exactly the new declarations (`evidence/diffs/final-clean.v10-vs-final.diff`,
`…/final-r1work.recorded-vs-final.diff`): two added lines (`UNREADABLE
(could-not-evaluate): []`, `DECLARED FAIL CLASSES: []`) and the extended G2 line.
Every pre-existing reading line — live anchors, per-file `lines=`, per-file
`loci=`, all locus sections, SCOPE-ERRORS, G7, G11, VERDICT — is byte-identical.

Injection matrix (deltas confined to the declared classes; all FAILs exit 1):

| injection (fixture) | v10 | v11 |
|---|---|---|
| SKILL.md absent | PASS `5256fe24…` (silent `lines=0 loci=0`) | FAIL `fcf6e725…` `UNREADABLE ['SKILL.md: FileNotFoundError']` |
| SKILL.md zero-byte | PASS `5256fe24…` (silent) | FAIL `975ab64f…` `['SKILL.md: 0 lines < declared max 20 (rows beyond EOF)']` |
| SKILL.md first 10 lines | PASS (same class) | FAIL `bb5f0024…` `['SKILL.md: 10 lines < declared max 20 …']` |
| SKILL.md is a directory | PASS (same class) | FAIL `097de4dc…` `['SKILL.md: IsADirectoryError']` |
| SKILL.md EACCES | PASS (same class) | FAIL `6b2cc430…` `['SKILL.md: PermissionError']` |
| PROVINCE.md absent | FAIL `7b47ada6…` (marker scope-errors) | FAIL `545f23ff…` (same scope-errors **plus** `['PROVINCE.md: FileNotFoundError']`) |
| PROVINCE.md 130 lines (max end − 1) | — | FAIL `6126066e…` `['PROVINCE.md: 130 lines < declared max 131 …']` |
| PROVINCE.md 131 lines (max end) | — | PASS `913ca95e…` |
| all three needles neutered | PASS `c831970f…` (`loci=0`, G2 "ok") | FAIL `b7049482…` `DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']` |
| SKILL.md needle-free, 371 lines (nullskill) | PASS `d6cb0bde…` | FAIL `d6c74651…` `['BLIND-INSTRUMENT']` (per-file current-ok: PROVINCE 17 / SCORECARD 14 / SKILL 0) |
| PIN alone neutered (partial) | PASS `17c5144b…` | PASS `91c31ea2…` — residual, see §4 |
| rogue non-live value inside a DATED range (t5b) | PASS `4d25ddd3…` | PASS `4ee4d86b…` (same locus `:45 … -> historical (dated scope)`, delta = the new lines only) |

JSON mode declares the causes on the same runs: `unreadable`,
`declared_fail_classes`, `g2_floor: "1/readable-file"`, `current_ok_per_file`
(`runs/v11final-*.json`, `v11landed-absent-skill.json`). Exit codes stay 0/1;
no new exit-2 path was introduced. `--quiet` keeps the same verdict
(`v11final-pretree-quiet`).

## 4. Attacks / refutations attempted

1. "The pre-round census reading is environment-dependent" → **REFUTED**:
   rerun, `cwd=/`, `PYTHONHASHSEED=0/1` all byte-identical (`d3da7509…`, `1db2ec31…`).
2. "The records-commit append moves the census verdict" → **PARTIALLY REFUTED**:
   verdict and `loci` unchanged; only the SCORECARD `lines=` count moves
   (1336 → 1417), because the appended section is locus-free by construction.
3. "RV-11's H1 patch text alone closes the absent-file hole" → **CONFIRMED for
   OSError, REFUTED for zero-byte/truncated**: the verbatim patch-text preview
   (`a81893fc…`) reads **PASS** on the zero-byte fixture (`v11prev-empty-skill`,
   `8c16ec6d…`). The landed code closes zero-byte/truncated/directory/EACCES via
   the declared-max-EOF rule (five fixtures, above).
4. "The per-file floor false-FAILs an ordinary run" → **CONFIRMED on an
   intermediate revision**: `c95a5cf3…` (per-file floor counted current-ok
   *blocks*) reads `VERDICT: FAIL … SKILL.md=0` on the clean pre-edit tree
   (`v11r2probe-pretree`, `d4ed70b9…`; diff `diffs/final-vs-blockfloor.diff`).
   EX-14's map predicted this in the block unit; the revision that landed next
   counted assertions instead. The final revision's per-file counts at HEAD are
   17/14/3, all above the floor.
5. "The H3 floor is vacuous on real-shaped trees" → **REFUTED** at the class
   boundary: nullskill (readable, gate-clean, zero loci) reads PASS before and
   FAIL after — the global floor would not see it.
6. "Partial blindness is closed" → **REFUTED, by design**: PIN-only neutering
   still reads PASS (`91c31ea2…`), matching the landed header's named H4 /
   self-certification residual ("a token floor is not a coverage floor").
7. "The post-edit instrument changed ordinary readings on the real tree" →
   **REFUTED**: §3's diff is exactly the three new declaration lines; the same is
   true against the round-1 recorded capture.
8. "The landing's own after-hash is fresh" → **REFUTED at close**: EX-16's
   `receipts/after/after-sha256.txt` names `df9ffdf9…`, but the file was revised
   twice more inside the window (doc-only; see §6). The receipt needs a
   re-derivation to the closing hash. (Flagged, not a stability defect —
   behaviour is byte-identical, §6.)

## 5. Residuals / gaps (named, not weaponized)

- Partial (per-needle) blindness stays open by design (attack 6); only the
  external locus-count + scope-diff audit sees it. My seat's own evidence is
  exactly such an audit, but it is not machine-enforced in the census.
- The H1 rule keys on the declared max end: a legitimately shrinking scope file
  below its declared bound FAILs until the SCOPE row is re-keyed. That is the
  intended semantics (rows past EOF are unevaluable), pinned at both sides of
  the boundary (130 FAIL / 131 PASS). It also means any future *removal* of a
  scope row must lower `max_end`, or the file may fail the floor.
- My post-edit readings are certified on the closing revision `d0772ce8…`
  (610 lines): the full matrix (16 runs) re-ran byte-identical to `df9ffdf9…`.
  If a further code revision lands after this seat's close, §3's matrix must be
  re-run on the new bytes; the fixture set and `evidence/fixtures.md` rebuild
  it in seconds.
- Cross-seat note for the parent: several round-2 seats pinned their verdicts
  to the superseded `82fb807e…` (e.g. RV-4, EX-18, EX-23 seat texts). Those
  verdicts are about the same behaviour class as the final revision, but their
  named hash is not the closing one.

## 6. Revision history of the real target observed in-window

| time (-03) | sha256 | behaviour |
|---|---|---|
| 09:05:05 | `7b5a0e88…` | header-only; behaviour `d3da7509…` |
| ~09:07 | `1431620f…` | header-only |
| ~09:10 | `076bd621…` | H1+H3 code landed (global floor) |
| ~09:11 | `82fb807e…` | first terraced "landed" state; clean `a9cd6886…`, blindall FAIL, blindpin PASS |
| 09:11–09:12 | `c95a5cf3…` | per-file floor in the block unit — ordinary-run false-FAIL (attack 4) |
| 09:12–09:15 | `df9ffdf9…` | per-file floor in the assertion unit (EX-16's "r9 final" receipt) |
| 09:15 | `2fa3023b…` | doc-only self-description fixes |
| 09:17 | `a4c16763…` | doc-only; all 14 certified run digests identical to `df9ffdf9…` |
| 09:19–09:20 (close) | `d0772ce8…` | doc-only (G20 unit note: block floors refuted by CR-2/CR-3 evidence); **16/16 matrix digests identical** to `df9ffdf9…` |

Closing state of the real target: `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`
(610 lines), captured in `evidence/instrument-closing.sha256` and the frozen
copies `evidence/instr-final3-*.py`. Every certified reading in §2–§3 is
reproduced byte-for-byte on these bytes.

## 7. Evidence index

`evidence/manifest.sha256` — sha256 of every capture, exit code, diff,
instrument and doc in this directory. Key files:
`evidence/runs/*.out|.exit|.json` (labelled `<instrument>-<tree>`),
`evidence/diffs/*.diff`, `evidence/fixtures.md` (rebuild recipe),
`evidence/custody-readonly.txt`, `evidence/landed.diff` (EX-16's r1 landing),
`evidence/instr-*.py` (blind variants kept frozen).
