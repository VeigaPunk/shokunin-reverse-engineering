# Round 47 / w1 — seat `C2Mismatch`: are the four C2 before-mismatches real?

Lane `kaidoku`, round 47, wave 1. Seat `C2Mismatch` (R47-C2 verification: re-derive the four
mismatches the counter reports at the base and say whether each is real).
Base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`; freeze `5017e1f7299c3a812e87e7950148f54313dd279e`
(`git diff-tree 5017e1f` = `A plans/round-47-claims.md`, `A tools/round-47/exact.py`,
`A tools/round-47/record.py`; `git diff --stat 13a9e9e 5017e1f -- corpus/ SKILL.md SCORECARD.md`
is empty, so the freeze moves no measured surface).

Lane tree read-only: this seat wrote nothing outside
`.ufo/waves/round-47/w1/C2Mismatch*`. No commits, no stages, no `jj`. No installs.
Scratch `/fast/scratch/hyaku/kaidoku-r47/C2Mismatch` removed after the receipts were copied.

## 1. The counting command and its receipt

```sh
HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r47/C2Mismatch \
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47/record.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev 13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5 \
  --json-out .ufo/waves/round-47/w1/C2Mismatch/receipt.json
```

| field | value |
|---|---|
| exit | **1** |
| run UTC | `2026-10-28T17:55:59Z` (`canonical.utc`) |
| stdout | 1769 B, sha256 `53d81a3d27a4c0c832b334f0cc69aa97e414339574dc6b458f730630fd4d7e36` (`canonical.stdout`, stderr empty) |
| `receipt.json` | sha256 `53d81a3d…4d7e36` (byte-identical to stdout) |
| `sections` | `["round-45", "round-46"]` |
| `atoms` / `verified` / `exempted` | 50 / 46 / 0 |
| `atoms_by_class` | `axes 2, path 12, rev 33, seats 2, window 1` |
| `corrections` / `corrections_bad` | 0 / `[]` |
| `failing` | `["mismatches 4 != 0", "corrections 0 < 2"]` |
| `battery` | `correction_forgeries 3`, `forgeries_green 0` — **all three fixtures report `error: "no corrections section"`**, i.e. no forgery was actually applied (see C2M-6) |
| `met_target` | `false` |

The four `mismatches` entries, verbatim:

| # | `class` | `key` | atom as written | counter's `derived` |
|---|---|---|---|---|
| 1 | `seats` | 45 | `Wave 1: 40 seats; wave 2: 32 seats` | claimed `[40,32]`, derived `[40,36]`, dispatch `[40,36]` |
| 2 | `window` | 46 | `0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every measurement above. | `reason: "unverifiable"` — the claimed window names no concrete `A..B` revisions |
| 3 | `axes` | coverage | `coverage 133/133 at the head of its Owned-axes row` | claimed `[133,133]`, derived `[138,138]` |
| 4 | `axes` | depth | `depth 20/20 at the head of its Owned-axes row` | claimed `[20,20]`, derived `[23,23]` |

## 2. My own derivation of each of the four — is the counter right?

Every row is a command I ran myself against committed state, not a re-read of the counter's
internals. Machine receipts: `derive/commands.tsv` (name, exit, stdout sha256, UTC, argv) and
`derive/<name>.out` / `.err`.

| # | my command | my value | counter's value | verdict |
|---|---|---|---|---|
| 1 | `git show 13a9e9e:.ufo/waves/round-45/w{1,2}-dispatch.json` → `counts.spawn`; `git show 13a9e9e:.ufo/waves/round-45/r45-w{1,2}-results.json` → `seats`, `len(results)`; `git ls-tree 13a9e9e -- .ufo/waves/round-45/w3-dispatch.json` | w1 spawn **40**, w2 spawn **36**; w1 results `seats 40 / 40`; w2 results `seats 36 / 36`; no w3 dispatch | `[40,36]` | **counter RIGHT — the record is false.** `32` matches neither its own cited source (`r45-w2-results.json` says 36) nor the dispatch. The number `32` is `policy.waveMinLanes` in the same dispatch file (`m1-w2-dispatch.out`), i.e. the band minimum, not a count. Independent corroboration already committed: `.ufo/waves/round-45/r45-w2-results.json` seats `R45W2Waves` V5 and `R45W2SweepAudit` both falsify "32" with the same 36. |
| 2 | `git show 13a9e9e:SCORECARD.md` line 3635; `git log --name-status --format= 0425224..13a9e9e -- tools/round-46 plans/round-46-claims.md`; same over `0425224..58eb04b6`, `0425224..7bf33e31`, `332f4884..13a9e9e`, `332f4884..58eb04b6` | line 3635 contains the literal `<tip>`; `0425224..13a9e9e` prints **`M tools/round-46/attest.py` + `M tools/round-46/gate.py`** (commit `332f4884`); `0425224..58eb04b6` non-empty; `0425224..7bf33e31` empty; `332f4884..13a9e9e` and `332f4884..58eb04b6` empty | `unverifiable` | **counter RIGHT, and the claim is worse than unverifiable: it is false.** The section's own F5/A4/B1 amendment declares `332f4884` the measured freeze, and that commit sits inside the claimed window and edits `tools/round-46/`. So "empty at every measurement above" is false at both of the section's measurement tips. The counter catches it only as a shape defect (no concrete pair). |
| 3 | `git ls-tree -r --name-only 13a9e9e -- corpus/knowledge \| grep -c '\.md$'`; same at `e1c83313`; coverage-map tokens of `corpus/README.md` `## Coverage map` at `13a9e9e` | **138** files at `13a9e9e`; **133** at `e1c83313`; map: 143 token occurrences, 138 unique, `mapped_intersection 138`, `dangling []`, `missing []` → **138/138** | `[138,138]` | **counter RIGHT at `--rev`.** `133/133` is true at its own cited revision (`command A at e1c83313`, round 41), so the defect is staleness, not a lie — but the card then carries two incompatible current values: row head `133/133` vs the round-45 and round-46 sections' `knowledge_files 138 / mapped 138`. |
| 4 | craft-section split on `^- \*\*` of `SKILL.md` at `13a9e9e` plus an independent resolution pass over every `corpus/|plans/|tools/` citation (file present at rev, `1 <= start <= end <= line count`); same block count at `e1c83313` | **23** blocks, **23/23** resolve; **20** blocks at `e1c83313` | `[23,23]` | **counter RIGHT at `--rev`**, and the same staleness class as #3: `20/20` was true at `e1c83313`. |

**No false mismatches.** All four are real under the frozen predicate; #1 and #2 are substantively
false statements, #3 and #4 are stale leading values that the frozen clause reads as current.

Two measurement notes that matter for how the repair is written:

- the coverage fraction is a **set** count (138 files ∩ 138 unique map tokens). The map carries 143
  token occurrences for 138 files (five cross-references, e.g. `2026-10-18-arc2-r7-pe-wall` appears
  in three rows). Not a defect, but "mapped" counts files, never rows — do not write 143 anywhere.
- `133/133` and `20/20` were true when written. A correction that calls them false without saying
  "stale at the head" overstates the defect.

## 3. Findings against the FROZEN C2 clause (attack, not repair)

Each finding has a runnable probe, the exact command, the differing value and a fixture path.
All probes import the frozen `tools/round-47/record.py` and call `record.evaluate_text(...)` on
mutated *text* (or an overridden `files()` accessor) — the frozen bytes are never edited and the
lane tree is never written. `probe*.out` carry the full JSON; `.utc` the run time.

### C2M-1 (HIGH) — the documented `axes` correction is unparseable; two landed `corrects` lines are dead text

`record.py:50` `CORR = re.compile(r"^- corrects (seats|window|path|rev) (\S+):\s*(.+)$")` omits
`axes`, although `corrects()` implements an `axes` branch (`CORR_AXES`, `"an axes correction must
state '<resolved>/<total>'"`) and the claims file says "a … `axes` correction must state
`<resolved>/<total>`". Consequence: an `axes` correction line is silently dropped — it neither
exempts, nor counts, nor can ever be `corrections_bad`.

- base card, depth row stale at `20/20`, the only repair being `- corrects axes depth: 20/20`
  (`probe2.py`, case `B2-axes-correction-dropped`, `probe2.out`, sha256 `1a530174…a3bb33`):
  exit **1**, `mismatches [["axes","depth 20/20 …"]]`, `corrections 2` (the line is not counted).
- at the landing revision `f54b3b6d` (`probe6.out`, sha256 `0c002006…fd7713`): the card has
  four `- corrects` lines, `lines_matching_CORR 2`, `corrections_parsed 2`, exit **0**; the two
  dropped lines are `- corrects axes coverage: 138/138 …` and `- corrects axes depth: 24/24 …`.
  Appending `- corrects axes depth: 99/99 — fabricated` leaves exit **0** (`corrections 2`).

So the SCORECARD sentence "each `corrects` line below … is itself re-derived by the counter at the
measured revision" is false for two of the four lines as committed. Two honest repairs, both
available to the L1: (a) drop the two `axes` lines and say the rows were corrected in place —
the counter needs nothing from them; or (b) freeze-permitting, widen `CORR` to include `axes`
(that changes frozen bytes, so it needs a new freeze, not an edit).

### C2M-2 (HIGH) — deleting a claim is a valid "repair"; the `axes` class needs one atom, not two

`collect_axes` emits one atom per `coverage`/`depth` row; the `classes` clause only fails when an
entire class has zero atoms. Removing the `| coverage |` row removes its atom instead of correcting
it, and the card scores **met** (`probe2.py`, case `C2-coverage-row-deleted-green`): exit **0**,
`axes 1`, `failing []`. A round can therefore repair a false axis figure by deleting the row. Only
the `exempted <= 3` cap and a human reviewer stand against it.

### C2M-3 (HIGH) — a `window` atom can be made green by a pathspec no commit touches, or by a reversed window

`window_empty` runs `git log base..tip -- <pathspec>`; git exits 0 with empty output for an unknown
path and for a non-ancestor base, and both score the atom green.

- `probe.py` case `D-pathspec-typo` (`probe.out`, sha256 `7033124e…464280`): the claim
  `0425224..13a9e9e -- tools/round-46x plans/round-46-claims.md` is empty → exit **0**, although
  `tools/round-46` changed inside that window.
- `probe.py` case `E-reversed-window`: `13a9e9e..7bf33e31 -- tools/round-46 plans/round-46-claims.md`
  → exit **0** (a descendant..ancestor window is always empty).

The three-forgery battery does not carry either case.

### C2M-4 (MEDIUM) — a `path` correction's statement is never read, so two fabricated lines satisfy `corrections >= 2`

`corrects()` for `path` returns `files(key) is not None` and discards `stmt` entirely. Two true-by-
construction `- corrects path <atom> …` lines therefore clear `CORR_MIN` while exempting nothing:
`probe4.py` case `D4-inert-corrections-real-keys` (`probe4.out`, sha256 `96eb9802…8ee9a1`) → exit
**0**, `corrections 2`, `corrections_bad []`, `exempted []` on a card whose real repairs were
in-place edits. At the landing revision the same holds with a fabricated statement
(`probe6.py` case `fabricated-path-statement`): exit **0**, `corrections 3`. By contrast a
fabricated `seats` total is caught (`fabricated-seats-total` → exit 1, `claimed [9,999]` vs
`derived [1,75]`), so the weakness is class-specific, not general.

### C2M-5 (MEDIUM) — the `seats` pair shape binds waves 1 and 2 only; a third wave is invisible

`SEATS_PAIR` is `Wave 1: A seats; wave 2: B seats`. With a synthetic
`.ufo/waves/round-45/w3-dispatch.json` (`counts.spawn 9`), the pair claim stays green and no atom
mentions the third wave, while the sum shape counts it: `Waves: 40 + 36 = 85 seats` is green
(derived `[40,36,85]`) and `Waves: 40 + 36 = 76 seats` is red (`probe4.out` case
`sum-counts-wave3`, `probe5.out` sha256 `6ec1cc65…d34f26`). At `13a9e9e` no round has three
dispatches (`m1-third-wave` is empty), so this is latent, not live.

### C2M-6 (MEDIUM) — the before-state battery "passes" by erroring, not by discriminating

`run_battery` increments `correction_forgeries` and adds `forgeries_green += 0` when the card has no
corrections section (`error: "no corrections section"`). The recorded before receipt therefore shows
`correction_forgeries 3 / forgeries_green 0` with **zero mutations applied** — exactly what
`receipt.json` shows (`probe2.out` case `G2-battery-on-before`). Clause 6's numbers in the before
cell are not evidence that the forgery classes are detected; only the post-landing run is.

### C2M-7 (INFO) — a placeholder window is exempted by any empty window, including one unrelated to the tip

`exempt()` returns `True` for a `pair is None` window atom under *any* window correction, and the
correction's own pair only has to be empty somewhere (`probe.py` case `F-placeholder-window-invisible`,
exit **0**). Combined with C2M-3 this means the `<tip>` defect can be "repaired" by naming an empty
window that does not cover the measurement. The window the L1 actually landed
(`332f4884..58eb04b6`) is sound and I verified it empty; the hole is in the predicate, not in the
landed text.

### Also verified as sound (no finding)

- `rev` atoms: 33 at the base, all resolve and are ancestors (`verified 46` overall).
- `path` atoms: 12, all present at the base.
- the historical-correction clause (a `seats`/`window` correction for a round older than the
  last-two window is not a ghost) does what the record needs — otherwise the round-45 seats
  correction would become `corrections_bad` the moment a `## Round 47` section lands
  (I probed that shape while looking for C2M-1).

## 4. Landing evidence the L1 needs (numbers and traps, measured)

Frozen bytes are not mine to change; these are measurements of what the landed card has to say.

1. **Depth must read 24/24 at the landing revision, and block 24 must be a list bullet.**
   At `13a9e9e` the craft section has 23 blocks and 23/23 resolve (`m4-block-count`,
   `m4-citation-resolution`). Appending a synthetic 24th block whose citation cannot resolve at
   that rev yields `derived [23,24]` (`probe3.out` case `E3-block24-depth`, exit 1) — so the
   denominator moves the instant the block lands. Format sensitivity, measured
   (same probe, three variants):

   | block 24 written as | derived pair | effect on the depth atom |
   |---|---|---|
   | `- **24. Title.** …` | `(24,24)` if every citation resolves, else `(23,24)` | counted; this is the only correct form |
   | `### 24. Title.` | `(23,23)` | invisible — the round's depth move cannot be read |
   | `**24. Title.**` (no list marker) | `(22,23)` | folds into block 23 and breaks *block 23's* resolution |

2. **Coverage stays 138/138** — round 47 adds no `corpus/knowledge` file
   (`git diff --stat 13a9e9e 5017e1f -- corpus/` empty).
3. **The two corrections the counter can read must be the two I verified true**: `2 waves, 76 seats
   total` (dispatch `[40,36]`) and `empty in 332f4884..58eb04b6 -- tools/round-46
   plans/round-46-claims.md` (0 bytes). Both are what the current landing text says.
4. **The axes rows must be edited in place** — an `- corrects axes …` line does not parse (C2M-1).
5. **Do not delete an axis row** as the repair (C2M-2).

## 5. Advisory on the landing state (read-only, rev moves under us)

HEAD was `3186f69b`, `07d2894e`, `04469ee8`, `f54b3b6d` at successive reads during this wave.
At `f54b3b6d` (`probe6.out`) the counter exits **0**, `met_target true`, `sections ["round-46",
"round-47"]`, `atoms 41`, `mismatches []`, `corrections 2`, `corrections_bad []`, battery `3/0`
with all three forgeries red for the right reason. The only defect visible in that state is C2M-1:
four `corrects` lines, two parsed. The L1 should either drop the two `axes` lines from the
corrections section or stop claiming that every line in it is re-derived.

## 6. Receipts

| file | what | sha256 (short) |
|---|---|---|
| `receipt.json` | canonical base run (exit 1) | `53d81a3d…4d7e36` |
| `canonical.stdout` / `.stderr` / `.utc` | 1769 B / 0 B / `2026-10-28T17:55:59Z` | `53d81a3d…4d7e36` / `e3b0c442…` |
| `derive/commands.tsv` + `derive/<name>.out|.err` | 17 independent derivations, each with exit, stdout sha256 and UTC | `df313649…` |
| `probe.py` / `probe.out` | pathspec-typo, reversed-window, placeholder-exemption, wave-3 seats | `7033124e…464280` |
| `probe2.py` / `probe2.out` | green baseline, unparseable `axes` correction, deleted coverage row, inert corrections, battery on before-state | `1a530174…a3bb33` |
| `probe3.py` / `probe3.out` | block-24 depth sensitivity, sum-vs-pair seats | `d9c85319…f2c82e` |
| `probe4.py` / `probe4.out` | inert corrections with real keys; three-wave seats sum | `96eb9802…8ee9a1` |
| `probe5.py` / `probe5.out` | historical-window corrections, three-wave seats | `6ec1cc65…d34f26` |
| `probe6.py` / `probe6.out` | landing state at `f54b3b6d`: 4 `corrects` lines, 2 parsed, fabricated lines | `0c002006…fd7713` |
| `at-head.json` | counter run at `07d2894e` (exit 0) | `d366b080…f4e4c2` |

## 7. Risks and not-run

- **Not run:** `tools/round-47/exact.py` and every R47-C1 clause — another seat's scope. I did not
  re-measure the counter at the final landing revision; §5 is a snapshot of a moving HEAD.
- The probe harness calls `record.evaluate_text` in-process. That is the frozen predicate itself,
  but it bypasses `gate.main_guard`/`out_path`; the CLI path is covered by the canonical run and by
  `at-head.json`.
- `--json-out` must resolve inside the lane root (`gate.out_path` rejects scratch paths, exit 2
  `{"reason": "--json-out outside the lane root: …"}` — reproduced, `at-head.stdout` first run).
- No installs, no network, nothing written outside this seat's directory.
