# R35ReviewerC2 — C2 counter D-1..D-4 false accepts / false rejects

Seat: `R35ReviewerC2` (wave 1, review lane; leaf member, no delegation). Item: review
`tools/round-35/c2-calibration-counter.py` D-1..D-4 for false accepts/rejects; build evidence and
first falsifications. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Measured HEAD:
`ee0c865c878492c26fb43aa1c0beaee7b6388f63`; base `aa04633a686d49756763b1feed4be6830d5bb479`;
freeze `2323d197456f1328459d9420aff025cffbcb3e27`.

Report: `.ufo/waves/round-35/w1/R35ReviewerC2.md`

## Method and limits

- Read the frozen counter (pinned bytes), canonical claims file, round-34 verifier spot-check
  (defect definitions), and the live D1-D4 target artifacts at HEAD.
- Falsifications ran in throwaway sandbox git repos under `/tmp` (`tempfile.mkdtemp`, same pattern
  as the counter's own `--selftest`); each repo was deleted after its run. No `/fast/scratch`
  access, no lane write, no VCS/index/jj mutation, no nested delegation, nothing installed.
- The lane counter itself was run once, read-only, without `--json-out`:
  `python3 -I -B tools/round-35/c2-calibration-counter.py --root . --base aa04633a… --freeze 2323d197… --rev HEAD` → `C2_FAIL: …` (11 ids below), `EXIT=1`.
- Limits: sandbox fixtures, not lane bytes; the S1060 substring case for D-3 was already shown by
  `.ufo/waves/round-35/w1/R35CriticClaims.md` (lesson M35-2) and was cited, not re-run.

## Instrument integrity checks (pass)

| check | command/evidence | result |
|---|---|---|
| predicate byte-identity | AST-extract `PREDICATE` from counter; compare to `claims-canonical.json` C2 `predicate` | byte-identical |
| counter pin | sha256 of worktree file and of `HEAD:tools/round-35/c2-calibration-counter.py` | both `576c14dd95c0a54b…` = canonical `instruments` pin |
| frozen census digest | sha256 of `HEAD:.ufo/waves/round-35/assimilation/census-start.txt` | `b6ce2b17…` = canonical `frozen_inputs` digest |
| read-only property | counter uses `git show`/`git log` only; no worktree reads, no writes without `--json-out` | holds |
| exit contract | 12 sandbox runs: green→0, mutated→1, and missing-args→2 per argparse | holds |

Lane state at HEAD (all honest mid-round): `D1_no_sources_change_after_base`;
`D2_r34w2_correction_missing`; `D2_settle_missing:w1-settle.json`; `D2_settle_missing:w2-settle.json`;
`D2_lesson_seat_line_missing`; `D3_source_missing`; `D3_verified_at_missing`; `D3_recheck_missing`;
`D3_source_not_s106`; `D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4`;
`D4_section_missing:### Round-34 run-6 instrument registry`. `w1-settle.json`/`w2-settle.json` are
absent at HEAD; the lesson carries no `31/32`, no `AAdjacencyCite`, no seat line; the r34b entry has
no `^source:/^verified-at:/^recheck:` lines.

## Findings by severity

### FA-1 (high, false accept, D-1 content): the "9 W04 warnings" count is not enforced; all content checks are substrings

`check()` tests `"rows=106" in census`, `"EXIT=0" in census`, `"W04" in census`. Demonstrated:

- FA1: census with **2** W04 lines (predicate demands 9) → `C2_CLEAN`, exit 0.
- FA2: `rows=1060` → substring `rows=106` matches → exit 0.
- FA9: pure fabrication `rows=106 EXIT=0 W04 warnings: none, census skipped` → exit 0.

The r34 D-1 defect's decisive detail was a wrong warning count (report said 8, base blob yields 9);
this counter repeats that exact blind spot. The counter's own frozen green selftest fixture writes
`"rows=106 EXIT=0 W04 warnings\n"` — no count, no 9 — so the frozen instrument never exercises the
number its predicate states. (Corroborates M35-2; extends it with FA1/FA2.)

### FA-2 (high, false accept, D-1 timing): same-commit census passes; r34's actual defect shape would pass verbatim

`parse_iso(ct) > parse_iso(fc)` fails only when the census commit is strictly *after* the first
`corpus/SOURCES.md` change. Equal timestamps pass. FA3: census absent at base, added in the **same
commit** as the first SOURCES change → exit 0. But r34 D-1 was precisely "census committed by
`66b84027` — the same commit that added S106". The frozen canonical predicate says "committed
**before** the first corpus/SOURCES.md change"; the counter implements "not after", i.e. the weaker
plan wording ("no later than"). A byte-level repeat of the routed defect passes this counter.
Also: ordering rests on committer times (`%cI`), which are unauthenticated and rebasable — FR2
shows a true-first census *rejected* after a committer-time inversion (e.g. rebase timestamp bump):
exit 1 `D1_census_after_first_sources_change`.

### FA-3 (high, false accept, D-2): correction check is two substrings; the opposite assertion passes

`"AAdjacencyCite" in lesson and "31/32" in lesson`. FA4: lesson states *"The 31/32 figure was
itself a miscount; all 32 reported; AAdjacencyCite settled."* — the exact contradiction of the r34
correction (AAdjacencyCite was the unreported seat) — → exit 0. Additional D-2 gaps:

- FA5: `{"spawned": true, …}` in `w1-settle.json` — `isinstance(True, int)` is True, so a boolean
  counts as 1; totals computed with the bool → exit 0. Negative ints likewise accepted.
- `SETTLE_FILES` is the fixed pair w1/w2; a `w3-settle.json` would be silently excluded from
  "wave seat totals" (code-level observation; no w3 exists today).
- The counter compares lesson ↔ receipts only. r34 D-2's root class — receipts disagreeing with
  reports on disk (32 in map, 31 files) — is outside the frozen predicate, so consistent-but-wrong
  receipts + a lesson copying them pass. Residual, by predicate design, but worth naming.

### FA-4 (medium, false accept, D-3): presence-only trio; empty values pass; "appended" is unverifiable

Checks are `(?m)^source\s*:`, `^verified-at\s*:`, `^recheck\s*:`, `^source\s*:.*S106`. FA6:
`source: S106` + **empty** `verified-at:` and `recheck:` lines → exit 0. A trio inside a fenced
code-block example would pass equally; nothing distinguishes an appended block from a rewritten
entry (the r34 routing said "append … do not rewrite"), and nothing pins the pre-image. The S106
match is substring (`S1060` accepted) — already demonstrated by M35-2, cited here.

### FA-5 (medium, false accept, D-4): content-blind and first-match-only section scan

- FA7: all data rows replaced with `| | | | | | | | |` (8 empty cells) → exit 0. The check counts
  pipes; cells may be empty or arbitrary.
- FA8: a **second** `### Round-32 instrument registry` section appended with 5-cell rows → exit 0;
  the lookup `break`s at the first header match, so duplicates are unchecked.
- Scope: `EIGHT_CELL_SECTIONS` names two sections, but SKILL.md has three registry sections; the
  middle `## Round-34 instrument registry` (SKILL.md:1182) is never examined. Today all its rows
  are 8-cell (checked at HEAD, lines 1184-1199), so the gap is benign now — but the r34 D-4
  routing covered "the new SKILL.md registry section (and the two that precede it)" (three). The
  frozen predicate itself names only round-32 and run-6, so this is predicate-scope narrowing at
  authoring time, matched by the counter — an observation, not a counter bug.

### FR-1 (medium, false rejects / unpassable-as-frozen, D-4): the frozen sections do not match the repository they measure

The two live D-4 failures are both frozen-check-vs-reality artifacts:

- Real heading at SKILL.md:1209 is `### Round-34 run-6 instrument registry — the shortcut-replay
  gate (stopped capability)`; the exact-match `l.rstrip() == sec` can never match it →
  `D4_section_missing` forever, regardless of row health.
- The Round-32 section contains an archived 4-cell "Residual witness registry" (SKILL.md:1081-1084)
  predating the 8-cell standard → `D4_not_eight_cells:…line1081:cells=4`.

D-4 as frozen cannot distinguish "defect closed" from "defect present" on this repo: any pass
requires rewriting archived layout. This corroborates M35-3 with exact ids/lines; kill-rule stop is
the honest outcome (as recorded). Additionally FR1: a valid 8-cell GFM row whose cell contains an
escaped pipe (`\|`) is counted as 9 cells → false reject of a well-formed row.

### M-1 (medium, freeze-record integrity): canonical `instrument_supersessions` is stale relative to its own pins

The canonical file names `a85ca674` as superseding both counters ("finalized freeze-read path and
green/red selftest"). Measured blobs: C2 at `a85ca674` = `3a23f3eb…`, C1 at `a85ca674` =
`018e96d0…` — neither is the pin; the pinned bytes (`576c14dd…`, `e28792c7…`) first appear at
`2323d197` — **the same commit that adds `claims-canonical.json` itself**. `e4ca43dd` (first add of
`claims-frozen.json`) pinned the older `c0f37d21`/`d49ff16a` bytes, and `freeze-integrity` failed at
`f1ea3a6d` (`FAIL pins=4 changed=2`), disclosed in `freeze-status.md` and lesson M35-4. Mitigation:
both post-`13d7a815` counter diffs are claims-path relocations (`claims-frozen.json` →
`plans/round-35-freeze.json` → `claims-canonical.json`) plus selftest alignment; the D1-D4 `check()`
logic did not change after first add. But the canonical snapshot's supersession metadata asserts a
finalization state its named commit does not contain, and "instruments committed before
`claims.json`" holds only in the letter (first-add of a *draft*), not for the canonical pair.

### Positives (verified, not assumed)

Predicate byte-identity holds across counter/canonical; pin = HEAD blob = worktree; the frozen
census receipt at HEAD hashes exactly to `frozen_inputs`; the counter reads only immutable git
objects; the do-nothing/junk behaviors are real (lane run exits 1 with named ids; selftest red path
kills a mismatched lesson line); exit codes 0/1/2 behaved per contract in all runs.

## Residual risks and verification gaps

- Commit-time ordering (D-1) is trust-in-committer-metadata; jj/git rewrites can invert or collapse
  it (FR2 shown). `git log` history simplification for merge commits untested.
- D-2 receipts↔disk and any wave-3 receipts are outside the frozen predicate — closable defects the
  counter cannot see.
- D-3 appendedness/rewrite detection absent; value emptiness unenforced.
- D-4 pipe-counting is a markdown-rendering approximation; escaped pipes misclassify (FR1).
- C1 counter and its predicate are out of this item's scope; not reviewed.
- No lane state was mutated by this seat; the lane counter run wrote no receipt.

## Suggested next-round instrument notes (advisory, non-frozen)

Typed exact parsing for the census (`rows=(\d+)\b`, `(\d+) × W04`), digest-pinning the census
against `frozen_inputs` inside the counter, anchoring the seat-accounting line (`^` + per-wave
breakdown), requiring non-empty `verified-at:`/`recheck:` values, exact-section enumeration with a
section count guard, and GFM-aware cell splitting (unescape `\|` before counting).
