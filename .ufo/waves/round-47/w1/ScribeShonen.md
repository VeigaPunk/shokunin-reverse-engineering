# ScribeShonen — round 47: SHONEN section draft + stated-cell audit

Seat: `ScribeShonen` (leaf; no subagents). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scratch `/fast/scratch/hyaku/kaidoku-r47/ScribeShonen` (removed at exit). Anchor: the round's
declared freeze **A4 `1e2c3102952dc636650095643c1963c833859019`** (`git log -1 --format=%H` at
2026-10-28T17:55Z), base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`. All work read-only on the
lane; no counter was "fixed", no frozen byte touched, no git mutation anywhere.

Deliverable: `.ufo/waves/round-47/w1/ScribeShonen/shonen.md` — four lines, one per box, with the
evidence pointer that would justify `[~]` at A4, the `[x]` verifier status, and eight stale
stated cells checked against the repo (S1–S8). **No `[x]` is awarded and none is justified**: no
named non-author verifier exists for any box as a whole; the nearest non-author artefacts are
listed per box (round-43/39/40 wave-2 lane seats and the round-46 outside spot-check).

## 1. SHONEN lines (summary of the draft)

| box | `[~]` pointer that survives a repo check at A4 | `[x]` verifier |
|---|---|---|
| SKILL.md real tables, cited sources | craft `SKILL.md:81-642`, **24** blocks; block 24 at `:632-641`, marker once, header `trigger \| v2 hole \| v3 arm \| exit`, 4 rows, arms exactly `symbol/once/digest/order`, both pins equal the bytes; v4 region `92540586…` (13 856 B) equal at `d1681696..A4`; command A `rule_blocks 24`, `citation_resolved_rules 23`, `mapped 138/138` | none; named non-author lane seat `R43W2Skill` (regions byte-identical, command A 21/21) and outside spot-check §2 (block 23 re-derived) — the box's "no promotion verifier" is stale |
| end-to-end task logged | `LOG.md:3174-3183` (round 42, 4 carriers, `corpus/evidence/round-42/c1/*` present at A4), `:3184-3197` (round 43, 78/78), `:3164-3173`, `:3153-3163`, `:3137-3152` | none outside; lane re-runs exist for rounds 39/40/41 only — `.ufo/waves/round-42/w2/` does not exist |
| executable without oral context | `sqfs-triage.py --selftest` 35/35, `c2-counter.py --selftest` 27/27, `sqfs-triage-v2.py --selftest` 45/45 (my runs, committed blobs); round-39 20/20, round-40 26/26 receipts; recipes = command A + command B only | none outside; lane seats `R39W2TriageMutants` (35/35), `R39W2C2Mutants` (27/27), `R40W2C2IndepEval` |
| no cross-domain bleed | `PROVINCE.md:97-125` sha256 `f1a5cfc6…78b4` identical at `52b0eb29` and A4 (`diff` empty); appends `:378-384`, `:386-394`, **and the uncited `:396` (r41), `:410` (r42), `:424` (r44)**; file unmodified since round 44 | none; lane finding `R39W2C1AxisFit` D2 (repaired); spot-check §5 covers round 46 only |

## 2. Findings

### F1 (HIGH) — the depth head `24/24` is false under the published command A, and `record.py` greens it with a different count

The card (`SCORECARD.md` `## Owned axes` depth row, the `## Record corrections — round 47` line
`- corrects axes depth: 24/24 … citation_resolved_rules 24`, and the pending `## Round 47` section
line "`citation_resolved_rules 24/24`") asserts the depth proxy reads 24 of 24. The published
recipe (`SCORECARD.md:86-143`, command A, `corpus/knowledge/([a-z0-9-]+\.md)` only) reads **23 of
24** at A4, at the landing `e856beb5`, and at `62e33f7d`:

```sh
# (a) command A verbatim at the freeze: aggregate count (receipt commandA-at-A4.json)
#     → {"mapped":138,"knowledge_files":138,"citation_resolved_rules":23,"rule_blocks":24,"depth_score":9.58}
# (b) the failing block, isolated — block 24 carries zero command-A citations, block 23 carries one:
git show 1e2c3102:SKILL.md | sed -n '/^- \*\*24\. /,/^## Config custody/p' \
  | grep -oE 'corpus/knowledge/[a-z0-9-]+\.md' | wc -l          # 0
git show 1e2c3102:SKILL.md | sed -n '630p' | grep -oE 'corpus/knowledge/[a-z0-9-]+\.md' | wc -l   # 1
# (c) the counter that greens the false head:
python3 -I -B tools/round-47/record.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev 1e2c3102952dc636650095643c1963c833859019 \
  --json-out .ufo/waves/round-47/w1/ScribeShonen/receipts/record-head2.json      # → rc 0, mismatches [], failing []
```

Receipts: `receipts/commandA-at-A4.json`, `receipts/commandA-multirev.json`
(`e856beb5 24/23`, `1e2c3102 24/23`, `5017e1f7 23/23`, `77d196c6 21/21`, `eb8215ac 21/20`,
`52b0eb29 18/18`, `4d62ee5a 19/19`, `e1c83313 20/20`), `receipts/record-head2.json`.

Cause, read from the frozen counter: `depth_pair()` (`tools/round-47/record.py`, `"""Resolved
craft rule blocks over the total, exactly as command A reads them."""`) scans `HARD_REF =
re.compile(r"((?:corpus|plans|tools)/[A-Za-z0-9._/-]+)(?::(\d+)(?:-(\d+))?)?")`, not command A's
`corpus/knowledge/…` pattern. Block 24 (`SKILL.md:632-641`) cites `corpus/lessons/round-46.md`,
`plans/round-47-claims.md` and `https://docs.python.org/…` — **zero** `corpus/knowledge/*.md`
tokens (block 23 has one at `SKILL.md:630`). So `HARD_REF` resolves it (24/24) while command A does
not (23/24): the docstring's "exactly as command A reads them" is false, and the `axes` class of
R47-C2 is re-derived under a definition the claims file does not name ("command A's
citation-resolution count over `## Queue-drain craft `").

Consequence for R47-C2: the two exempted `axes` atoms (`coverage 138/138`, `depth 24/24`) are
green only through the private pattern; under the named recipe the `depth` atom is a mismatch
(claimed 24/24, observed 23/24) and the card's `corrects axes depth` line fails R47-C2 clause 3
("a correction line must itself re-derive") — the correction states a command-A result the command
does not produce. Also note the same defect class at `eb8215ac` (round 42): `unresolved_blocks [21]`
— block 21 was never resolvable by command A either, so this is a recurrence, not a new accident.
Honest depth score under the recipe at A4: `round(10*23/24, 2) = 9.58`.

The clean fix is a property of the artefact, not of the counter: add one resolvable
`corpus/knowledge/<entry>.md:<start>-<end>` citation to block 24 (out of this seat's write scope —
recorded, not applied).

### F2 (HIGH) — the frozen file declares a two-freeze series; the lane landed four amendments, two of them after data, and C1 is green only at an undeclared freeze

- `grep -c 'Freeze amendment' plans/round-47-claims.md` → **2** (A1, A2). A1's own text: "the freeze
  is a series of two, disclosed"; A2's text: "Every clause, threshold and kill rule is
  byte-identical to A1". Neither A3 nor A4 has a paragraph in the frozen file.
- `git log --oneline 5017e1f7..HEAD -- tools/round-47` → four commits: `9018c53b` (A1), `62e33f7d`
  (A2), `2e4ae434` (A3, `record.py` +11/−2), `1e2c3102` (A4, `record.py` +3/−1). The frozen file's
  rule is explicit: "Nothing in this file or in `tools/round-47/` changes after the freeze: a change
  makes both counters exit 2 `frozen_path_changed`." All four are such changes.
- `exact.py --rev HEAD` at each declared freeze: `5017e1f7` → rc 2 `frozen_path_changed`
  (`plans/round-47-claims.md`, `tools/round-47/`, `tools/round-47/record.py`); `9018c53b` → rc 2
  same; `62e33f7d` → rc 2 `frozen_path_changed` with `touched ["tools/round-47/record.py"]` (A3).
  Receipts `receipts/exact-head-<freeze>.{json,stdout}`.
- The only green C1 receipt is `.ufo/waves/round-47/l1/scores/c1-at-A4.json`
  (`freeze == rev == 1e2c310295…`, `met_target true`, `failing []`, `frozen_path_changed []`,
  battery `forgeries_total 4 / v2_green 4 / v3_green 0 / genuine_green 1 / crash 0`, `refs 8`) —
  i.e. the claim is met at `--freeze 1e2c3102`, a commit the frozen claims file never names.
- Timeline: the landing `e856beb5` (data) precedes A3/A4. "All before any claim verdict" (the
  SCORECARD sentence) is true; "series of two" and "nothing changes after the freeze" are not.

I am reporting the mismatch, not adjudicating it: whether re-declaring the freeze in the record is
admissible is the canonical judge's call. What is checkable is that the frozen file's own text and
the round's freeze series disagree by two amendments, and that the claim's green exists only at the
later one.

### F3 (HIGH) — `record.py` cannot exit 2 `frozen_path_changed`; the frozen sentence is unimplementable for C2

`tools/round-47/record.py` contains **zero** occurrences of `freeze` (case-sensitive; `grep -c
freeze tools/round-47/record.py` → 0) and its CLI takes only `--root --rev --no-battery --selftest
--json-out` (`record.py:467-472`); its counting command in the claims file
(`python3 -I -B tools/round-47/record.py --root … --rev … --json-out …`) has no freeze argument.
Yet the frozen file says "a change makes **both** counters exit 2 `frozen_path_changed`", and
`record.py` exits 0 at A4 while `tools/round-47/record.py` itself changed three times after
`5017e1f7` — the counter cannot detect that its own interpreter moved. This is a frozen-clause
defect (an enforcement sentence one of the two instruments cannot satisfy), independent of F2.

### F4 (MEDIUM) — the worktree is dirty on frozen paths mid-wave; counter runs observe it and report `frozen_worktree_dirty`

At 17:52:31Z and 17:53:04Z `exact.py` reported `dirty: ["tools/round-47/record.py"]` and rc 2
`frozen_worktree_dirty` (A3 was uncommitted at the first observation, re-dirtied by a sibling at
the second); at 17:55:16Z `SCORECARD.md` was ` M` in the worktree (the round-47 section being
written) while `tools/round-47`, `plans/round-47-claims.md`, `SKILL.md`, `PROVINCE.md` and
`SHONEN.md` were clean. `restored` in the receipts is a classification, not a write
(`gate.py:172`: `restored = [p for p in touched if …]`), so no seat's edit was clobbered by this
seat. Any C1 run taken while a sibling holds `tools/round-47/record.py` open returns 2 for a reason
that has nothing to do with the claim.

### F5 (LOW) — the SHONEN stated cells are stale by four rounds, and R46-V6's SHONEN half does not resolve

S1–S8 in `shonen.md`; the load-bearing ones: `SKILL.md:81-449` / "20/20" (round-41 values; A4 is
`81-642` / 24 blocks / 23 resolved); "no promotion verifier" (superseded by the round-46 outside
spot-check); PROVINCE appends cited only through round 40 while `:396`, `:410`, `:424` exist;
SHONEN's last change is `8de80f1d` (round 43), so rounds 44–47 have no asserted cell at all.
R46-V6 ("`SHONEN` box 3 … say `cases=16`") does not describe any revision of the file:
`git log -S 'cases=16' -- SHONEN.md` is empty, the file has no `attest.py`/`cases=` token, and its
last edit predates the round-46 counter. Only the SKILL-registry half of R46-V6 can be checked
against `SKILL.md` (not this seat's surface, untouched by me).

## 3. Checks run (exact command, exit code, stdout sha256, UTC)

| # | command (from the lane root) | rc | stdout sha256 | UTC |
|---|---|---|---|---|
| 1 | `python3 -I -B tools/round-47/exact.py --root <lane> --freeze 5017e1f7299c3a812e87e7950148f54313dd279e --rev HEAD --json-out .ufo/waves/round-47/w1/ScribeShonen/receipts/exact-head-5017e1f…json` | 2 | `26487ed01e133681400bc7b0ed11a81d5ac93d1e0e1d53c9d2b1dfd2265b13f0` | 17:52:31Z |
| 2 | same with `--freeze 9018c53b16503c8d06d398b75503406508119946` | 2 | `c973732701193fce0c295f7d0283d3af7c12fb97b488cd52659d890ac5573e22` | 17:52:31Z |
| 3 | same with `--freeze 62e33f7dd75c8e3285967b26419842c106f6c965` | 2 | `b976b39631a66635c01ee62dde7d23c8575e5628a04a78bfa5938159254ef6b7` | 17:52:50Z |
| 4 | same with `--freeze 2e4ae43463aabdae707f8c8a4daa41441ad67a71` | 2 | `cfb5eac54eb1a3c823d9908de6cfb19385dfb4db2df1713105f86ad38711133c` | 17:53:04Z |
| 5 | `python3 -I -B tools/round-47/record.py --root <lane> --rev HEAD --json-out …/record-head.json` | 0 | `7ba2c7b8b277ba356afe6f1c733d1209685727aa97b45e473e904ff70c90c080` | 17:52:33Z |
| 6 | same, `--rev HEAD` at A4 → `receipts/record-head2.json` | 0 | `c609b3e1c8ac00d03f8b80c9313d96b25466e53116b40121422f43e94224209d` | 17:53:22Z |
| 7 | command A (verbatim recipe) at A4 → `receipts/commandA-at-A4.json` | 0 | `ff125a5185114610fe5cb1e6484a5fd5595cce30f7baf94d38dff957ded1e87e` | 17:54:40Z |
| 8 | command A at 8 revisions → `receipts/commandA-multirev.json` | 0 | `d7c8e05a1792c69ea6bd98b73a8dcaf3418300f0a9fdc83ddd69aff3ffdadb22` | 17:55Z |
| 9 | `tools/round-39/sqfs-triage.py --selftest` (scratch copy) | 0 | `cases=35 pass=35 fail=0` (stdout not retained) | ~17:49Z |
| 10 | `tools/round-39/c2-counter.py --selftest` (scratch copy) | 0 | `{"cases":27,"pass":27,"fail":0}` (stdout not retained) | ~17:49Z |
| 11 | `tools/round-40/sqfs-triage-v2.py --selftest` (scratch copy) | 0 | `cases=45 pass=45 fail=0` (stdout not retained) | ~17:50Z |
| 12 | v4-region sha256 at `d1681696/eb8215ac/77d196c6/5017e1f7/A4` via `c1-counter.py:rule_block` | 0 | `92540586…1b101f2`, 13 856 B, all five equal | ~17:47Z |

Rows 9–12 are "ran green, stdout not retained as a file"; their times are approximate to the minute — the tallies above are the observed
strings, and rows 1–8 are the graded receipts. Verified-not-executed: `.ufo/waves/round-47/l1/scores/c1-at-A4.json`
(L1 receipt, read in place), `c2-at-A4.json`, round-42/43 LOG entries and score receipts,
`corpus/evidence/round-42/c1/*` existence, `PROVINCE.md` line ranges and byte-identity,
`.ufo/waves/round-{39,40,41,42,43}/` seat layouts.

## 4. Not run / out of scope

- No SHONEN.md edit, no SCORECARD/SKILL/LOG/PROVINCE edit, no commit, stage, stash, checkout or
  any VCS mutation; no counter "repair".
- The two counters were run as black boxes at HEAD under the declared freezes; their
  forgery batteries' semantics (`--selftest`, the four/three fixtures) were not otherwise attacked —
  other wave seats own that, and the frozen bytes are theirs to score.
- Exit code 2 never counted as a pass anywhere above; F2's "green" is quoted from the L1 receipt.
- Installs: **none** (no `uv`, `npx`, `pacman` or `~/.local/bin` write). Guaranteed by the host's
  paused-package state and not needed by this seat.

## 5. Touched surfaces

Written, all inside the seat dir: `.ufo/waves/round-47/w1/ScribeShonen.md`,
`.ufo/waves/round-47/w1/ScribeShonen/shonen.md`, `.ufo/waves/round-47/w1/ScribeShonen/receipts/`
(`commandA-at-A4.json`, `commandA-multirev.json`, `exact-head-{5017e1f,9018c53b,A2,A3}.{json,stdout}`,
`record-head{,2}.{json,stdout}`). Scratch `/fast/scratch/hyaku/kaidoku-r47/ScribeShonen` removed
before yield. Nothing else in the lane or the fleet repo was written.
