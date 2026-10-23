# A2FreezeBytes — round-32 freeze-pin and predicate/executable audit

utc: 2026-10-23T06:58Z (checks 06:4x–06:58Z). Seat: KaidokuR32A2.A2FreezeBytes.
Scope: recompute sha256 pins of `.ufo/waves/round-32/claims*.json` instrument/input maps at each
freeze and at main; verify no post-freeze changes and data-not-committed; compare each frozen
claim sentence against the executable clauses of its pinned counter. Read-only git/hash only; no
counter, no carrier binary, no REA run was executed.
Sandbox: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2FreezeBytes/` (`lane/`, `fleet/` clones,
`counters/` extracts), GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset, `git -C` absolute everywhere.

## Result summary

All pins recompute. No post-freeze change to any pinned object or claims file; main tip **is**
the v3 freeze commit. No data (committed envelopes, entry, PROVINCE/SCORECARD repair) committed.
Predicate↔executable alignment verified for all four frozen claims; findings below are all LOW.

## Revisions (exercised)

- `git -C lane rev-parse --verify`: `9a73680a`→`9a73680af21b002e3b99956c89234b2bbde2a71b`,
  `9d54070b`→`9d54070bebceff77401b25a1bb12e19107b3ab67`,
  `f382e3b7`→`f382e3b7978e6091a19ca93277c15a75c0016b43`, `main`→`f382e3b7…6b43` (rc 0 all).
- `git log --format=%H %cI %s -18 main`: tip `f382e3b7` = the v3 freeze commit itself
  (2026-10-23T03:10:01-03:00); parents `9d54070b`, `9a73680a`, base `283aad7f`.
- First-add (`git log --diff-filter=A -- <file>`): claims.json added at `9a73680a` (v1 freeze);
  claims-v2.json at `9d54070b`; claims-v3.json at `f382e3b7`. Consistent with each file's
  freeze_rule "first commit that adds it is the freeze commit".
- Fleet clone (`/home/vgpnk/Projects/shokunin`, default branch master, tip `575bceda`):
  `cef00867ab3279ac2c2d10421e3e62c0e5d693f3` exists ("hyaku phase-4: chunk ruling; kaidoku r31
  and chousa r31 admitted; r32 dispatches") and is an ancestor of HEAD (`merge-base --is-ancestor` rc 0).

## Pin recomputation (exercised; sha256 of `git show <rev>:<path>` blobs and worktree bytes)

Every pin in all three claims maps equals the pinned digest at its own freeze, at main, and in
the lane worktree:

| file | pin tail | at own freeze | main | worktree |
|---|---|---|---|---|
| c1-arm64x-positive.py | …0800f1a | 9a73680a ✓ | ✓ | ✓ |
| arm64x_oracle.py | …936686 | 9a73680a ✓ | ✓ | ✓ |
| c2-capability-calibration.py (v1) | …bc4446 | 9a73680a ✓ | ✓ | ✓ |
| build-arm64x-carriers.sh | …737ba3 | 9a73680a ✓ | ✓ | ✓ |
| c1/carriers.tsv | …bf3d16e | 9a73680a ✓ | ✓ | ✓ |
| c1/predictions.tsv | …737c56b | 9a73680a ✓ | ✓ | ✓ |
| inputs/loadconfig-arm64.s | …864ba2d | 9a73680a ✓ | ✓ | ✓ |
| inputs/loadconfig-arm64ec.s | …32c0d4 | 9a73680a ✓ | ✓ | ✓ |
| c2-capability-calibration-v2.py | …a8d36a | 9d54070b ✓ (absent at 9a73680a, correct) | ✓ | ✓ |
| c2-capability-calibration-v3.py | …cab2f9f | f382e3b7 ✓ (absent earlier, correct) | ✓ | ✓ |
| freeze-integrity.py | …1804cd | 9d54070b & f382e3b7 ✓ | ✓ | ✓ |

Claims files byte-identical worktree = main blob = freeze blob
(claims.json `8aa0672c…`, claims-v2.json `805a0514…`, claims-v3.json `a3be7e40…`; sha256sum
vs `git show` vs `git show <freeze>:…`).

Frozen binary pins: all 12 carriers in `/fast/scratch/hyaku/kaidoku-r32/carriers/` hash to
`carriers.tsv` sha256s (worktree `sha256sum` vs tsv, 12/12) and carry `chattr +i`
(`lsattr`: `----i--` on all). Probe `/fast/scratch/hyaku/kaidoku-r32/probe/x.dll`
sha256 `424777cb…dc` equals `before/probe/x.dll.sha256` committed at the freeze.

## No post-freeze changes (exercised)

- `git diff --stat 9a73680a..f382e3b7` touches only: claims-v2/v3, the two control receipts,
  `before/c2v{2,3}-*.txt`, and the three new tools — i.e., only the two supersession freezes.
- `git log 9a73680a..main -- SCORECARD.md PROVINCE.md corpus/knowledge corpus/evidence/round-32`:
  empty.
- `git ls-tree -r main -- .ufo/waves/round-32`: only `before/*`, `claims{,-v2,-v3}.json`,
  `controls/l1-c2-v{1,2}-*-receipt.txt` — the two pre-data control receipts, as claims-v3
  `supersedes.reason` records.
- Worktree bytes of SCORECARD.md (`bba9f55d…`) and PROVINCE.md (`c167827a…`) equal their main
  blobs — no uncommitted edits to the two files the counters read at REV.

## Data not committed (exercised)

- `corpus/evidence/round-32/c1/` at main (and v1 freeze): only `carriers.tsv`, `predictions.tsv`,
  `inputs/` — no `envelopes/`, no `runs.tsv`; `git log --diff-filter=A` for
  `corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md`: no commits.
- `git grep -n ARM64X main -- PROVINCE.md`: still only :83 "Reserve: ARM64X hybrids…" under
  `## Frontier` (:73); `git show 283aad7f:PROVINCE.md | grep -n ARM64X` — same single line at :83,
  unmoved command's expected output reproduced.
- `## Capabilities` section at main (SCORECARD.md:615–623): still 5 rows; the only hyaku-closed
  round credited is round 27 (row :623); rounds 13/14/17 absent — matches the `surface` sentence
  "credits 1 of the 4 outside-recorded capabilities".
- `git log 283aad7f..main -- SCORECARD.md PROVINCE.md corpus/knowledge`: only `9a73680a` appears,
  and only because it added frozen inputs under `corpus/evidence/`; no repair commit exists.

## Statement-set and anchors (exercised)

- `git show cef00867…:MANIFEST.json` (1,242,275 bytes): exactly 4 kaidoku `capabilities_added`
  items (rounds 13, 14, 17, 27) — `statements=4` as frozen. Each item matches exactly its
  `key_list` pattern; closure set (`admitted` non-null) = rounds 12–31.
- Recomputed `anchors_at_freeze` independently (same `REL_PATH_RE`/`TICK_RE`/outside-row rules on
  `283aad7f:SCORECARD.md` + the 4 MANIFEST items): all four entries **match the frozen map
  exactly**; every anchor resolves at base (`git cat-file -e` rc 0). Outside-section capability
  rows at base: 3 (round 27's anchor comes from the MANIFEST item alone).

## Claim sentence vs executable clauses

Verified clause-by-clause by reading the pin-matched sources extracted to
`counters/` (hashes recorded above). Exercised = source read + cross-checks; no execution.

**C1 (`P1-pass`)** — all clauses implemented in `judge`/`measure`: oracle classify (machine
0xAA64 + ARM64+ARM64EC kinds, oracle.py:104–109); exit 0 + `ok===true` + `operation` +
subject-digest vs frozen sha (counter:72–80); field projection via `comparable`
(oracle:128–135) vs `expected` (112–125) incl. ordered `segments` list and `segment_count`;
`procedure_count` vs `predictions.tsv` (`predictions.tsv` recomputed consistent:
`procedure_count` = `native_exports`, `document` = `target-<sha12>.dll`, 12/12 rows);
committed-envelope clause `added_ct > freeze_ct` + `strip_meta` equality + `evidence_id`
substring in entry (109–126); doc gates `entry_ok`/`province_ok` (129–150); exit semantics
`0 iff pass==12 and e_ok and p_ok`, write-mode prints WRITE-MODE, no target line, exit 3
(211–218, 221–223).

**C2v3 (`P2-match`, live claim)** — statement construction, section bounds, per-row conditions
(distinct rows via `used`, single-key first cell, `ROUND_RE` exactly-one-round, backticked anchor
paths resolving at REV via `ls-tree`, ≥5 shared words with anchored description) and the closed
statement set (key-list coverage, non-empty anchors → exit 2) all implemented
(c2-v3.py:68–211). The frozen `anchors_at_freeze` map equals the counter's own derivation
(recomputed above).

### Findings (all LOW)

1. **LOW — frozen prose inaccuracy, not an executable mismatch.** `claims.json`
   `pre_freeze_probe` says the 12 carriers separate count rules "on 6 carriers (native != EC
   count)". `carriers.tsv` at the freeze shows **7** (k04 4/1, k05 1/4, k07 6/2, k08 2/6,
   k09 7/3, k10 3/7, k12 1/2; recomputed with DictReader). Understated, non-amendable per
   freeze_rule; the separation claim itself remains true.
2. **LOW — C2v3 word tokenizer vs sentence.** Predicate: words = "letters, length >= 4,
   case-folded". Code: `re.findall(r"[A-Za-z][A-Za-z-]{3,}")` admits interior hyphens
   (c2-v3.py:126), so `evidence-ID`-type tokens count as one code-word but up to two
   sentence-words; code is the stricter rule and can only flip a ≥5 boundary verdict to
   mismatch. No flip demonstrated (receipted base row shares 16).
3. **LOW — C1 "first added after the freeze commit" is implemented as a committer-timestamp
   comparison** (`first_added` %ct vs min ctime of the claims-file add commit, counter:103–116),
   not DAG ancestry. An envelope reachable only post-freeze but carrying a ctime ≤ the freeze
   commit's (skew/rewrite) would satisfy the clause while violating the sentence's intent.
4. **LOW — `province_ok` exclusion regex case-sensitive.** `re.search(r"Frontier|Adjacent|
   exclusion", heading)` (counter:147) would accept a row under e.g. "## Core exclusion"
   (lowercase "exclusion" is covered; "ADJACENT"/"frontier" are not) — slightly narrower
   exclusion than the sentence's "not Frontier/Adjacent/exclusion".
5. **LOW (superseded artifacts only).** v1 reverse check flags only *unused* rows naming a
   closed round (v1 code:100–103); its docstring's stricter form ("names that round … a
   mismatch") is under-enforced for used rows — unreachable defect for v1 since v1 has no
   exactly-one-round forward gate; v2/v3 close it via `rounds_named(cells[-1]) != {n}`.
   v2 `evidence_ok` requires `/` in the backticked span (v2:93), narrower than the sentence's
   "backticked lane path" for bare `file.md` spans.

### Noted ambiguities (sentence silent, code picks a reasonable branch — not defects)

- Envelope `format`/`architecture` are read from `data.subject`, `document`/`segments`/counts
  from `data.normalized_result` (oracle:128–135); the sentence does not name envelope paths.
- Segment equality is whole-dict equality — an envelope segment carrying an extra key fails;
  the sentence's 6-key list is thus enforced exactly.
- `strip_meta` removes top-level `meta` only; nested `meta` keys would still compare.
- MANIFEST duplicate kaidoku entries for rounds 12–14 exist (admitted=None carry
  `capabilities_added`; later entries carry closures) — code iterates all round entries,
  consistent with the sentence.

## Verification gaps

- No counter, oracle, REA run, or carrier binary executed (per assignment); executable-clause
  evidence is pin-matched source reading plus read-only git/hash recomputation.
- Probe x.dll interior (2 native / 2 EC exports) not re-parsed; only its sha256 verified.
- Worktree verified only over the pinned paths, claims files, SCORECARD.md, PROVINCE.md; a full
  `git status` on the lane was intentionally not run (git confined to the scratch clone).
- claims*.json of other waves (rounds 14–31) observed via glob but out of this seat's scope.

Report: .ufo/waves/round-32/a2audit/A2FreezeBytes.md
