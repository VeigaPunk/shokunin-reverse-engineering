# Round 99 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

Lane-round: kaidoku round 99. Base `de098f51cd73d3b9b4a895840da8f2bb0a386db8` → lane HEAD
`37e5db9a7412e743da253a9f2ddc4ea85b6fe909`. Report `.ufo/reports/round-99/kaidoku.md` (fleet repo).
Driver digest (copied from the mutable `.ufo/watchdog.log`):
`2026-11-05T18:34:43-03:00 launch kaidoku round=99 pgid=1255880 driver=hyaku-inline attempt=1`;
`2026-11-05T19:31:17-03:00 complete kaidoku round=99; hyaku-inline attempt=1`.
All measurements below were run on 2026-11-05 by this closure session; no lane gate was executed.

## 1. Conformance (PROTOCOL §Round-robin closure step 1)

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H %cI' -- .ufo/reports/round-99/kaidoku.md` | `kaidoku-shokunin <kaidoku@shokunin.local> 63ff4480c1d587d8cf2917f7be077481e774f326 2026-11-05T19:30:18-03:00` (after the final lane commit at 19:28:54, before completion at 19:31:17) | ok |
| `SHONEN` heading, one line per box | read report §SHONEN; `git show 37e5db9a:SHONEN.md \| grep -nE '^\s*- \['` | 4 boxes in SHONEN.md, 4 lines in the report (`[~]`×3, `[ ]`×1) | ok |
| cited commits exist and are ancestors of `refs/heads/main` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> refs/heads/main` for 8fb5ac4f, 5f08a78f, 01c4b79c, 64cc3e10, c19d57cd, 09688de2, 37e5db9a (and base de098f51) | all `commit`, all ancestors | ok |
| pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state …/kaidoku-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/main` | `ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote `37e5db9a…` | ok |
| prompt carries the template contract | `diff <(sed -n '1,140p' .ufo/prompts/kaidoku-round-99.md) kimi-shokunin/templates/round-prompt.md` | differs only in filled placeholders (lane, round, fleet root, AXES = coverage + depth + calibration); §6 hyaku addendum present | ok |
| marker? | — | real report with 7 resolvable commits | not a marker |

## 2. Claims

### R99-C1 — calibration: self-assessment mismatches 17 → 0 (re-measured)

Plain re-derivation (python over `git ls-tree`/`git show`, no lane tool):
- Coverage-map section (`corpus/README.md` `## Coverage map` … `## Knowledge`) table rows naming each
  `corpus/knowledge/*.md` stem: base `de098f51` **176 of 182** (missing r93-citation-semantics,
  r93-fresh-pack-oracle, r94-receipt-path-json, r95-receipt-world-binding, r96-kill-rule-coverage,
  r97-receipt-byte-binding — the last is in the `## Knowledge` index only, line 278); `64cc3e10`
  **182 of 182**; `37e5db9a` **183 of 183**. Matches the reported A3 values.
- Coverage head (`SCORECARD.md` `| coverage |`): base cites 168/168 (stale; observed 176/182 = 9.67);
  final cites 183/183, true. A1/A2 match.
- Registry: `tools/round-9[789]/*.py` with a SKILL.md table row naming the path: base **0 of 9**,
  `64cc3e10` **14 of 14**, final **14 of 14**. sha256 pins in the rows for the six round-98/99 tools
  equal `git show 37e5db9a:<path> | sha256sum` (2fa1102d…, e732465b…, d4ed4430…, ac97598a…,
  685a3ab0…, cd0f8fab…).
- 2 + 6 + 9 = 17 base mismatches — equals the do-nothing receipt
  (`pre/c1-do-nothing-at-base.json`: `mismatches 17`, exit 1).
- Evidence-verified: receipts `l1/scores/c1-at-{64cc3e10,c19d57cd,09688de2}.json` carry `mismatches 0`,
  exit 0 and their own `rev`; `pre/c1-selftest.txt` `SELFTEST cases=9 failures=0`, `rc=0`.
- M99-i correction spot-read: the craft-citation-v2 row at final reads `SELFTEST cases=11`; the tool
  prints `cases={len(cases)}` (`craft-citation-v2.py:352`).
- **Verdict: calibration improved** (re-measured). The lane's named limit stands: the counter checks
  presence/shape, not truth.

### R99-C2 — coverage: truncated UPX PE refused (frontier → core; capability)

Evidence-verified: `l1/scores/c2-at-{01c4b79c,c19d57cd,09688de2}.json` all carry the frozen target label
(`… truncated 40 of 40 … effective 79 of 79`), exit 0, own `rev`; `pre/c2-controls-at-freeze.txt`
shows the r98 repair (`truncated 0 of 40; cli 0 of 3`), identity and g2–g8 all `rc=1`, committed at
5f08a78f before the candidate (01c4b79c, 3 s later).

Independent re-measurement on two carriers outside the pinned ten (upx 5.2.0, `--best`):
`freeglut64.vc10.dll` (94208 B packed) and `gle32.vc10.dll` (27648 B packed), cut by 0/1/100/513/half
bytes, both repairs read via `git show 37e5db9a:tools/round-9{8,9}/upx-pe-repair.py`:

| cells | `upx -t` | r98 repair | r99 repair |
|---|---|---|---|
| 2 untruncated | rc 0 | `ok intact` rc 0 | `ok intact` rc 0 |
| 6 cuts 1/100/513 B | rc 1 | `ok intact` rc 0 (false green) | `refused: truncated: file N bytes < aligned end of last section M` rc 2, no output |
| 2 half cuts | rc 1 | `packheader-candidates:0` rc 2 | `truncated` rc 2 |
| 2 random 777 B overlays | rc 0 | — | `ok intact` rc 0 |
| 2 zeroed `UPX!` tampers | rc 1 → rc 0 after repair | — | `ok magic@992`, `upx -d` output byte-equal to untampered unpack |

S326 re-opened (see §3): the refusal rule is the packer's. ExecHeldOut's 432-cell run
(`w1/ExecHeldOut.md:35-45`) is lane evidence, consistent with the above.
- **Verdict: coverage improved** (re-measured on held-out carriers plus evidence-verified battery).
  Named limits (CriticC2 fa/fb/fg, 15 mutation blind spots, PackHeader always at 992 in my cells) stand.

### Harm check (owned axes coverage, depth, calibration; freshness read)

- `git diff de098f51 37e5db9a -- SCORECARD.md`: one in-place change (the coverage head, now true),
  one capability row, an appended round-99 section; no other axis row edited.
  `git diff --numstat` deletions: SCORECARD 1 (that head), SOURCES 1 (S324 `used-by`, logged in the lesson).
- depth: `coverage-selfcheck-at-{de098f51,09688de2}.json` `recipe_a.citation_resolved_rules 36` at both,
  `depth_score 10.0` — **unchanged** (evidence-verified).
- Observation, not harm: recipe A's legacy `coverage_score` 7.8 → 7.76 (mapped 142 of 182 → 142 of 183) —
  the pre-round-85 recipe-A mapping disclosed in the old head; the new head no longer restates it.
- freshness: no receipt-corpus change; not re-measured by the lane or by me — **unchanged** (not an owned
  claim axis this round).

## 3. Discernment spot-check (LEARNING.md)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S326 UPX 5.2.0 `src/packer.cpp` | admit (tier A, mined) | `curl https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packer.cpp` → 44586 B, sha256 `ab274d67…e040` (equal to row and copy); line 433 `throw OverlayException("invalid overlay size; file is possibly corrupt");` under the `(int) overlay < 0` test at 432 | agree | primary source for the exact refusal; quote is 8 words, located correctly; the caller arithmetic is at `pefile.cpp` 3046-3049 (re-opened: `ALIGN_UP(isection[iobjs - 1].rawdataptr + isection[iobjs - 1].size, ih.filealign); checkOverlay(overlay);`) |
| S327 candidate (ScoutSources draft, `w1/ScoutSources/draft-s327-candidate-rejection.md`) | reject (no row; would duplicate S326) | GitHub search API `repo:upx/upx "invalid overlay size"` → `total_count 0`; `"overlay size"` → 4 hits today (seat saw 2), titles about PAR::Packer, DOS header, .NET ratio, `p_mac.cpp` datatype — none on truncation; `doc/upx-doc.txt` v5.2.0 sha256 `4dc547ed…8c42` equal, `grep -c invalid` → 0 | agree | no tracker/doc source states the behaviour; the packer source already admitted is the authority |
| S326 row quote (new SOURCES row, ≤25 words) | — | same fetch | ok | quote 8 words, line 433, revision tag `v5.2.0` named |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → exit 0,
`kaidoku ok`, 33 W04 warnings (start receipt 32): the new one is
`S326 duplicate url raw.githubusercontent.com/upx/upx/v5.2.0/src/packer.cpp across scopes` (S310 already
registers that URL for the header-sanity scope). Scoped rows are allowed; the report's "only the W04
warnings already there" is inaccurate (defect 2 below).

## 4. Axis verdicts and trends

| axis | verdict | basis |
|---|---|---|
| calibration | improved | re-measured (§2 C1) |
| coverage | improved | re-measured on held-out carriers + evidence-verified battery (§2 C2) |
| depth | unchanged | evidence-verified 36 → 36 |

- **expansion: improved** — new admitted entry `2026-11-05-r99-pe-upx-truncation-refusal.md` on ground the
  Round-98 frontier note held as Frontier, `source:` S326 (mined), coverage-map row line 141; one capability row.
- **quality: improved** — the round-98 repair's exit-0 false green on truncated packs is superseded; I
  reproduced the false green (6/6 small cuts) and its fix on two non-pinned DLLs; no admitted entry failed re-check.
- **discernment: improved** — this spot-check agrees with the sampled admit and reject; the lane caught and
  corrected its own three false registry rows (M99-i) in-round. Caveat: defect 1.

## 5. Routed defects (lane must fix next round)

1. `corpus/lessons/round-99.md` `## Gate` records no rejection; the S327 rejection drafted by ScoutSources and
   the GitHub/docs sweep never reached the Gate table or `corpus/SOURCES.md` `## Search log` (no round-99
   search-log note was appended; CORPUS.md SOURCES rule 5). Append both next round.
2. Report §Sources and lesson census line say the end census has only pre-existing W04 warnings; S326 adds a new
   W04 (URL shared with S310). Record a correction and say whether S326/S310 scope split is deliberate.
3. M99-k: SCORECARD head at `64cc3e10`/`c19d57cd` cited receipts first committed at `09688de2` — commit cited
   receipts in the same commit that cites them.
4. M99-j: the C1 forgery-control fixture revision `e2502c3d…` is not in the lane; commit fixture bytes, not only the diff.
5. Coverage head no longer states recipe A's current mapped fraction (142 of 183, `coverage_score 7.76`); restate
   or retire recipe A explicitly.
6. Carried: round-99 named limits (lesson `## Named limits` 1–3) and round-97 routed defects 2–5, 7 remain open.

## 6. Operator note (promotion is operator-owned)

SHONEN boxes 1–3 are backed by committed artifacts a non-author can check (registry rows with pinned shas,
LOG round-99 end-to-end task, re-runnable frozen commands); this closure re-ran the C2 domain task on
held-out carriers from committed bytes only. Box 4 untouched. No `[x]` written here.
