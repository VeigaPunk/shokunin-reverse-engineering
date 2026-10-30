# R52 / wave 1 / seat `ScribeReadme` — `corpus/README.md` bindings for R52-C1

**Verdict: the README drafts are ready for the L1** — a paste-ready 3-cell coverage-map row (with a
measured-not-promoted fallback), the matching `## Knowledge` index row, the dated frontier-note edit
in two variants (append-only vs supersede + in-place removal), and the **141 → 142** map-count
arithmetic with the command-A counting command. Every shape gate I could run offline passes (66
checks, 0 failures, two variants). Nothing was written into the lane tree outside my seat
directory; no REA run was made; no git mutation was performed; no tool was installed.

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · README read at lane HEAD
`1842addcef3458515859b928b92d9bbd0a46c5d5` (blob `b8a266ea52ed63dad8089294da964c6da107f87a`,
worktree sha256 `aad0c5907483f38fc0fcf82cb66f63d0b15a6554c3ad2d0d6d85c6a60b5da5db`, 303 lines) ·
the README blob is **byte-identical** at the round-start base `c525de54…`, at the claims draft
`ab0eafe…` and at HEAD (measured).

## Behaviour delivered

| # | artifact | what it gives the L1 |
|---|---|---|
| 1 | `coverage-map-row.md` §1 | the 3-cell coverage-map row for `2026-10-30-r52-avm-le-squashfs-core`, inserted after the round-51 coverage row (base L107) |
| 2 | `coverage-map-row.md` §2 | the **fallback** row (*measured, not promoted*) for the miss case — 3 cells, same shape |
| 3 | `coverage-map-row.md` §3 | the optional 4-cell `## Knowledge` index row (round-50/round-51 house style), with the two things the L1 must settle (the `S252` citation, the `verified-at` value) |
| 4 | `coverage-map-row.md` §4 | the conditionality matrix (which text lands on counter exit 0 / 1 / 2) |
| 5 | `frontier-note.md` §1–§3 | the old lines quoted verbatim (L97, L106, L274, L275, L282, L283, L303), the new dated bullet (last bullet of `## Frontier`) and the new dated trailing note (end of file) |
| 6 | `frontier-note.md` §4 | the **option A / option B** choice, with the seven exact old→new string pairs for option B |
| 7 | `map-count.md` | the **141 → 142** arithmetic, the command-A counting command, its semantics, and the two failure modes the same-commit landing prevents |
| 8 | `receipts/` | the re-runnable checker (`patch_readme.py`), its log, both patched README copies and both unified diffs, and a receipts table (command, exit code, stdout sha256, UTC) |

## The three findings the L1 should act on

### F1 — `S252` does not exist yet, so the coverage/Knowledge rows would be a false citation if they landed first

`corpus/SOURCES.md` at the base revision holds **158** rows and its highest id is **S251**; `S252`
(man7 `mknod(2)`, the CAP_MKNOD ground for the device law) is **drafted this round** by the
`ScribeSources` seat (`w1/ScribeSources/rows.md`, `used-by` = the round-52 entry stem, opened
2026-10-30) and is **not yet in the registry** (measured: `grep -c '^| S[0-9]'` = 158, zero hits for
`S252`). The claims require the entry to cite S252 and the round-50/51 rows cite their S-ids in the
coverage row, so my drafted rows carry `S252` — **but the SOURCES row and the README rows must land
in the same commit.** If the L1 lands the README rows first, the coverage row cites a source id
that does not exist (a false citation) and the counter's `sourced` binding
(`c1-counter.py:2464-2477`, requiring an S-id whose row is opened in `OPENED_DATES` and whose
`used-by` names the entry) stays false. Mitigation: land `SOURCES.md` + `corpus/README.md` + the
entry in **one** commit, or drop `S252` from the two cells and cite only S243/S244/S245/S249/S250/
S251 — but note those older rows' `used-by` cells currently name the **round-50/round-51** entries,
not the round-52 one, so they must also be extended if the entry cites them.

### F2 — the counter's `frontier_note` binding reads `PROVINCE.md`, not `corpus/README.md`, and it cannot distinguish "promoted" from "not promoted"

The round-52 counter draft (`w1/ExecCounterV2/c1-counter.py:2447-2450`, the port of the round-50
counter) computes `frontier_note` as

```python
b['frontier_note'] = any(FRONTIER_MARK in l and STEM in l
                         and LE_AVM_RE.search(l.replace(STEM, ''))
                         for l in prov_text.splitlines())
```

over **`PROVINCE.md`** — the README is never searched for it. Two consequences the L1 should decide
on, both raised independently in round 51 (`CritCounterV2` F15: "the v1 `frontier_note` binding
cannot distinguish *promoted* from *not promoted*; a binding that reads `## Frontier` and asserts
the LE AVM row is gone"):

1. The README's `## Frontier` section is where the class is still listed **as an item** in four
   dated still-frontier enumerations (L274, L275, L282, L283) and in the round-50 trailing note
   (L303). A counter binding that asserts "LE `hsqs` left the frontier list" has to read **the
   README** — the PROVINCE binding alone stays green whichever way the promotion goes.
2. The draft carries both variants so the L1 can choose:
   * **option A (append-only)** — the two new dated lines only; the historical enumerations keep
     naming the class (3 such lines remain after the patch, measured). A counter can then check
     "the newest dated frontier line names the promotion", but **not** "the clause is gone".
   * **option B (supersede + in-place removal)** — the two new dated lines **plus** seven in-place
     replacements that drop the `LE AVM members (`hsqs`)` clause from every still-frontier
     enumeration (each edited line gets a dated pointer, so the history stays truthful). After
     option B, **no** `## Frontier` still-frontier enumeration and **no** trailing note names the
     class as an item (measured: 0), and only three dated *descriptive* sentences still mention it
     (the two historical coverage-map rows, which now carry a pointer, and the new round-52 coverage
     row itself). **My recommendation: option B**, because it is the only variant a counter can
     check for an actual removal, and because the lane has done the same thing before
     (`corpus/README.md:268` prefixes the round-42 bullet with a dated supersession pointer).

   The pointer wording is deliberate: it says "the little-endian AVM members left this list",
   **not** "LE AVM members left this list", so a still-frontier enumeration that mentions the class
   in a pointer cannot be mis-read as one that lists it, and the `LE_AVM_RE` token
   (`LE[ _-]AVM|AVM[ _-]LE`) does not fire on the pointer.

### F3 — the map count is 141 → 142, and the coverage row + the entry must land in one commit

Measured at the base revision `c525de54…`: `corpus/knowledge/` holds **141** `.md` files (142
`ls-tree` entries, the 142nd being `corpus/knowledge/.gitkeep`), all **141** mapped in the
`## Coverage map` section — command A at that rev returns `knowledge_files: 141`, `mapped: 141`,
`missing: []`, `dangling: []`, `coverage_score: 10.0`, `citation_resolved_rules: 26`,
`rule_blocks: 26`, `depth_score: 10.0`. The round-52 entry is the **142nd** `.md` file (sorted, it
comes last: `2026-10-30-r52-avm-le-squashfs-core.md` after
`2026-10-30-r51-avm-le-squashfs-core.md`), so:

* the `SCORECARD.md` `## Owned axes` coverage row must read **`142/142 knowledge files mapped`**
  (atom **B1**, `tools/round-50/c2-record.py:496-517`, derives the number from
  `git ls-tree -r --name-only <rev> -- corpus/knowledge` and requires the row to state `N/N` with the
  same N — so the row's own wording must keep the literal `(\d+)/(\d+) knowledge files mapped`
  phrase);
* the numeric coverage **score does not move** (142/142 → 10.0), only the count in the head;
* the entry and the coverage row must land in the **same commit**: entry without row →
  `missing: ['2026-10-30-r52-avm-le-squashfs-core']`, `coverage_score` 9.93, atom B1 red; row
  without entry → `dangling: ['2026-10-30-r52-avm-le-squashfs-core']`. Both simulated on the patched
  tree (both come out `mapped: 142`, `missing: []`, `dangling: []`, `coverage_score: 10.0`).

## Shape gates I ran (offline; no REA, no lane write, no git mutation)

`receipts/check.log` — 66 checks, **0 failures**, both variants (script
`receipts/patch_readme.py`, re-runnable; scratch-only inputs).

| gate | result |
|---|---|
| the README blob is identical at base / claims draft / HEAD | True |
| the coverage-map section's rows are all 3 cells under the frozen `cells()` (`tools/round-50/c1-counter.py:585-586`) | 94 rows at base, **0** bad; 95 rows patched, **0** bad |
| the drafted coverage row is 3 cells, no `|` inside any cell | 3 / 3, True |
| the counter's own `coverage_map_row` expression (`c1-counter.py:2479-2482`, ported at `ExecCounterV2/c1-counter.py:2475-2476`) | True |
| `map_token` (`c2-record.py:490-493`) matches the row inside `## Coverage map` | True |
| `unique_section` for `## Coverage map` / `## Knowledge` / `## Frontier` | 1 / 1 / 1, before and after the patch |
| exactly one `## Knowledge` row for the stem, 4 cells | 1, 4 |
| the fallback row is 3 cells and says *measured, not promoted* / *stay Frontier* | True / True / True |
| frontier-note shape (mark `Round-52 frontier note` + stem + `LE AVM` token, stem removed) | 2 lines, both variants |
| neither new frontier line carries a `|` | True |
| the new bullet is the last `## Frontier` bullet, drops the LE-AVM-members clause, keeps the `~13k`-file clause, keeps AVM kernels / nested sub-images | True (both variants) |
| the trailing note is the last non-blank line of the file | True |
| option B: no `## Frontier` still-frontier enumeration and no trailing note names the class | 0 / 0 (option A: 3 historical enumerations remain — the documented difference between the variants) |
| option B: the `~13k`-file clause survives the in-place edits | True (base 1 → 3: the two new lines) |
| command A on the patched tree | `knowledge_files 142`, `mapped 142`, `missing []`, `dangling []`, `coverage_score 10.0`, both variants |
| the r51 stem stays mapped (no regression) | True |
| `S252` is **not** in the registry at the base revision | True (158 rows, highest id S251) — see F1 |
| draft text == verified text | the coverage row, the fallback row, the Knowledge row, the frontier bullet and the trailing note are byte-identical between the draft `.md` files and the checked constants |
| lane tree untouched | `git status --porcelain` over `corpus README.md SKILL.md PROVINCE.md SCORECARD.md LOG.md SHONEN.md tools plans corpus/SOURCES.md corpus/evidence corpus/knowledge` → empty |

**Not run:** the round-52 counter (it does not exist at the freeze yet; its scoring needs the
freeze and the L1's data run), the four-carrier data run, any REA invocation (forbidden this wave),
the `PROVINCE.md` twin edit (another seat's surface: `## Round-52 additions to Core` +
`Round-52 frontier note`), and the `SCORECARD.md` head edit (another seat's surface).

## An observation about a sibling's write (not mine, not touched)

`git status` shows one **tracked** modification in the lane tree:
`.ufo/waves/round-50/w3/ScribeEntryC1.md` (+30 lines, an "Addendum — the landing outcome" block
appended to a round-50 wave-3 seat report). It is not mine and I did not touch it; it is recorded
here only because the wave contract expects drafts under the current seat's directory. No
`corpus/`, `tools/`, `plans/`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `SHONEN.md`,
`corpus/SOURCES.md`, `corpus/evidence/` or `corpus/knowledge/` file is modified.

## Two details the L1 should check against the claims' own constants

* the claims' `frontier_mark` is **`Round-52 frontier note`** and the counter draft's `FRONTIER_MARK`
  is the same string (`ExecCounterV2/c1-counter.py:380`) — my README lines carry exactly that
  mark, so the shape is satisfied whether the binding reads the README or `PROVINCE.md`;
* the claims' `prov_base` is `/fast/scratch/hyaku/kaidoku-r52` **without** a trailing slash, while
  the counter's `PROV_BASE` is a *prefix test* (`output_directory.startswith(PROV_BASE)`) and the
  round-50/51 counters use `/fast/scratch/hyaku/kaidoku-r5N/` **with** one. Not my surface, but the
  counter seat should make the constant consistent with the prefix semantics (a trailing slash is
  what stops `/fast/scratch/hyaku/kaidoku-r52-evil/…` from passing the prefix test).

## Touched surfaces (mine) and out of scope

* **Written** (all under my seat directory): `.ufo/waves/round-52/w1/ScribeReadme.md` (this
  report), `.ufo/waves/round-52/w1/ScribeReadme/{coverage-map-row.md, frontier-note.md,
  map-count.md}`, `.ufo/waves/round-52/w1/ScribeReadme/receipts/{patch_readme.py, check.log,
  README.patched.A.md, README.patched.B.md, README.A.patch, README.B.patch, receipts.tsv}`.
* **Not touched:** `corpus/`, `tools/`, `plans/`, `SKILL.md`, `PROVINCE.md`, `LOG.md`,
  `SCORECARD.md`, `SHONEN.md`, `corpus/SOURCES.md`, `corpus/evidence/`, the fleet repo,
  `.ufo/state/`. No commit / stage / stash / jj command; no git mutation of any kind; no
  `npx rea-agents` / `rea` invocation; no download; scratch
  `/fast/scratch/hyaku/kaidoku-r52/w1-ScribeReadme` removed after the receipts were copied. **No
  tool was installed** this seat (no pacman / uv / npx install) — the task needed only read-only
  git, `python3` and `sha256sum`.

## Artifacts

* `.ufo/waves/round-52/w1/ScribeReadme/coverage-map-row.md` — coverage-map row (3 cells) +
  fallback row + optional Knowledge-index row (4 cells) + the conditionality matrix.
* `.ufo/waves/round-52/w1/ScribeReadme/frontier-note.md` — old lines quoted verbatim, the two new
  dated lines, the option A / option B choice with the seven exact old→new pairs, the ~13k-file
  clause warning, the conditionality.
* `.ufo/waves/round-52/w1/ScribeReadme/map-count.md` — the 141 → 142 arithmetic, the command-A
  counting command and its semantics, the two failure modes, the cross-seat dependencies.
* `.ufo/waves/round-52/w1/ScribeReadme/receipts/check.log` — the 66-check log (0 failures).
* `.ufo/waves/round-52/w1/ScribeReadme/receipts/patch_readme.py` — the re-runnable checker
  (reads the lane README, writes only into its output directory).
* `.ufo/waves/round-52/w1/ScribeReadme/receipts/README.patched.A.md` (sha256
  `106710f1d97e2960adc0d6f727d20136399e22b9826511e3eaa28bb79337a058`) and
  `README.patched.B.md` (sha256 `e51dd152ed90a818d9e258ce84f3fbf1d4f78a7d259be6e3bfa38884cb1ff574`)
  — the patched README copies (option A / option B).
* `.ufo/waves/round-52/w1/ScribeReadme/receipts/README.A.patch` and `README.B.patch` — the
  unified diffs against the base README.
* `.ufo/waves/round-52/w1/ScribeReadme/receipts/receipts.tsv` — command, exit code, stdout sha256,
  UTC time per receipt.
