# R45W1C1HeaderBoundary — block-22 parse boundaries of the frozen C1 counter

Seat `R45W1C1HeaderBoundary`, round 45 wave 1, lane `kaidoku`, 2026-10-28T15:43Z.
Scope: the parse boundaries of the **frozen** `tools/round-45/c1-counter.py` block-22 checks,
exercised on scratch fixtures only. No lane file was written outside this seat directory.

## 0. Frozen provenance (verified, not assumed)

| what | value | how |
|---|---|---|
| counter under test | `sha256 2cfc5a4853585879b0924f4c002ed4581dced02f061068d325c2cd3da130a509` | `sha256sum` of the scratch copy and of `kaidoku-shokunin/tools/round-45/c1-counter.py`; identical |
| freeze commit | `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` | `git log --format=%H -1 -- plans/round-45-claims.md` |
| frozen bytes unchanged at HEAD | empty diff | `git -C kaidoku-shokunin diff --stat f762b72..HEAD -- plans/round-45-claims.md tools/round-45/` → exit 0, no output, 2026-10-28T15:41:57Z |
| lane HEAD when graded | `faa875bc0eb839d15b83c4afa6078819e5a7b381` | `--rev HEAD` resolved inside the receipt |

Scratch: `/fast/scratch/hyaku/kaidoku-r45/R45W1C1HeaderBoundary` (`TMPDIR` set there, fixture repos under
`fx*/`, every git call `-C <fixture>`). Removed after the receipts were copied out.

## 1. What the instrument actually parses (read from the frozen body)

| step | code | behaviour |
|---|---|---|
| section | `craft_blocks`, l.59–61 | text after the literal `"## Queue-drain craft "` (**trailing space load-bearing**), terminated at the first `"\n## "` — fence-unaware |
| blocks | l.62 | `re.split(r"(?m)^- \*\*", section)[1:]` — only a column-0 `- **` line starts a block; the preamble before the first one is discarded |
| table | `block_table`, l.64–76 | the **first** ≥3 stripped lines starting with `\|`; header cells lowercased and backtick-stripped; separators matching `\|[\s:\|-]+\|` skipped; every other pipe line is a data row (l.75) |
| exit column | l.144 | `next(... if "exit" in h ...)` — first header cell **containing** `exit` |
| exit cell | l.146 | `row[exit_col].strip("\` ")` must be in `{"0","1","2"}`; a missing column flags every row |
| header | l.161 | each of `trigger`,`arm`,`exit`,`receipt` present as a **substring** of *some* cell |
| refs | `REF`, l.33 + `unresolved_refs`, l.78–93 | `(corpus/(knowledge\|lessons)\|plans)/<name>.md` with **optional** `:N` or `:N-M`; total counts occurrences |
| marker | l.136 | `len([b for b in blocks if MARKER in b])` — blocks, not occurrences |

## 2. The five required probes

Protocol per fixture: fresh `git init` repo (identity configured locally, toplevel asserted equal to the
fixture), commit 1 = freeze with a 21-block `SKILL.md` and a `PREFLIGHT_SELFTEST: cases=11 failures=0`
stub at `tools/round-45/frozen-path-preflight.py`, commit 2 = the mutated block 22; then
`python3 -I -B <scratch>/c1-counter.py --root <fixture> --freeze HEAD~1 --rev HEAD --json-out receipts/<id>.json`.

| # | fixture | expected by the claims text | observed | exit |
|---|---|---|---|---|
| **a1** | marker in **two different** blocks (`fx-a1`) | `block22_present == 1` fails → not met | `block22_present 2`, `rule_blocks 22`; `failing: ["block22_present 2 != 1", …]` | **1** |
| **a2** | marker **twice inside one** block (`fx-a2`) | claim says "exactly one *block* contains the marker" → met | `block22_present 1`, rows 8, refs 4, `met_target true` | **0** |
| **b1** | header reordered, `exit` 3rd (`fx-b`) | "header carries trigger, arm, exit, receipt" — order free → met | `block22_header_ok true`, `met_target true` | **0** |
| **b2** | header reordered, `exit` **first** (`fx3-b3`) | order free → met | `header_ok true`, `met_target true` | **0** |
| **b3** | header reordered, `exit` **last** (`fx3-b4`) | order free → met | `header_ok true`, `met_target true` | **0** |
| **c** | one exit cell `0/1`, 8 rows (`fx-c`) | "every row's exit cell is exactly one of 0,1,2" → not met | `failing: ["block22 exit cells outside {0,1,2}: 8"]` (all 8 rows carry the dual value) | **1** |
| **d** | `corpus/lessons/round-45.md:1`, file exists, **0 lines** (`fx-d`) | "every path:line … resolves at --rev" → not met | `block22_unresolved_citations ["corpus/lessons/round-45.md:1-1"]`; `refs 4` | **1** |
| **e** | citation **with no line number** `corpus/lessons/round-44.md` (`fx-e`) | located citations / `path:line` forms only → a bare path should not count | accepted, counted: `block22_refs 4`, `unresolved []`, `met_target true` | **0** |

## 3. Extra probes on the same axes (cheap, all receipted)

| fixture | mutation | observed | exit | reads as |
|---|---|---|---|---|
| `fx2-d2` | bare path to the **0-line** file | unresolved `corpus/lessons/round-45.md:1-1` | 1 | existence is still checked for bare paths |
| `fx2-d3` | `corpus/lessons/round-45.md:0-0` (0-line file) | unresolved `…:0-0` | 1 | 1-based; consistent |
| `fx-g` | `plans/round-45-claims.md:99` (file has 10 lines) | unresolved `…:99-99` | 1 | consistent |
| `fx2-e3` | bare path to a **missing** file | unresolved `corpus/lessons/does-not-exist.md` | 1 | consistent |
| `fx2-f2` | 4 valid refs **+** `corpus/lessons/no/such.md:1` | `refs 4`, `unresolved []`, met | 0 | **unresolvable nested path invisible** |
| `fx2-f4` | 4 valid refs + `notes/nowhere.md:2` | `refs 5`, met | 0 | out-of-scope path invisible |
| `fx2-f3` | 4 valid refs + `tools/round-45/frozen-path-preflight.py:9999` | `refs 4`, met | 0 | interpreter line never resolved |
| `fx-e2` | the **same** `path:line` 4× | `refs 4`, met | 0 | duplicates satisfy the quota |
| `fx-b2` | header `triggers \| arms \| exit-code \| receipts` | `header_ok true`, met | 0 | substring match |
| `fx2-b5` | header `trigger \| exit-cause \| arm \| exit \| receipt`, valid exits in col 3 | 8 rows flagged | 1 | **first** `exit`-containing column wins |
| `fx-i` | a 3-line sample table above the decision table | `rows 10`, `header_ok false` | 1 | first table wins |
| `fx4-l1` | 7 rules + repeated header line | `rows 8` but the header row's exit cell is `exit` | 1 | row count inflated, still caught |
| `fx4-l2` | 7 real rules only | `rows 7` | 1 | consistent |
| `fx4-l3` | 7 rules + `\| \| \| 1 \| \|` | `met_target true` | 0 | **filler row counts as a rule row** |
| `fx4-l4` | 7 rules + empty exit cell | 1 row flagged | 1 | consistent |
| `fx4-l5` | 7 rules + `\| a \| \| 2 \| \|` | met | 0 | blank trigger/arm/receipt accepted |
| `fx4-c4` | exit cell `"1"` (quoted) | 8 flagged | 1 | consistent ("exactly") |
| `fx2-c2` | exit cell `0 (met)` | 8 flagged | 1 | consistent |
| `fx2-c3` | exit cell `0+1` | 8 flagged | 1 | consistent |
| `fx-h` | exit cell `` `1` `` | met | 0 | backticks stripped — tolerance |
| `fx2-a3` | marker between blocks 21 and 22 | `present 1` but the marked block is **21**: rows 0, header false | 1 | marker binds to a block, not to an ordinal |
| `fx2-a4` | marker in the section preamble (before block 1) | `present 0` | 1 | preamble is discarded by the split |
| `fx5-a6` | marker on **block 5 of 22**, green table there | `rule_blocks 22`, `present 1`, `met_target true` | **0** | **the "22" is never verified** |
| `fx3-h2` | heading `## Queue-drain craft` **without** trailing space | `IndexError` l.60; stdout **0 bytes**, **no receipt written** | 1 | crash presented as "not met" |
| `fx3-h3` | ```-fence containing a line `## not a heading` in the section | `rule_blocks 0` | 1 | fence-unaware section end |
| `fx-j` | preflight stub prints `cases=10 failures=0` | `preflight_selftest {ok:false, cases:10}` | 1 | consistent with `cases >= 11` |
| `fx-k` | unmodified green block | `met_target true` | 0 | control |

## 4. Where the instrument diverges from `plans/round-45-claims.md`

### LOOSER — accepts what the claim words would refuse

- **L1 (high).** A citation with **no line number** counts as a located citation and resolves
  (`fx-e`, exit 0, `refs 4`). `REF` l.33 makes the `:N` group optional, and `unresolved_refs` l.88–91
  substitutes line 1. The claim says "located citations (four or more, all resolving at the measured
  revision)" and "every `path:line` or `path:first-last` reference resolves". A block of four bare paths
  scores `block22_refs 4` with zero located citations.
- **L2 (medium).** Citations the regex cannot see are neither counted nor reported: `corpus/lessons/no/such.md:1`
  (`fx2-f2`, exit 0), `notes/nowhere.md:2` (`fx2-f4`, exit 0). The claim says **every** such reference
  resolves; an unresolvable nested path passes silently.
- **L3 (medium).** The interpreter citation is checked only for **presence as a substring**
  (`cites["interpreter"] = PREFLIGHT in block`, l.150). `tools/round-45/frozen-path-preflight.py:9999`
  is not a `REF` target (only `.md` under three prefixes) and is not resolved (`fx2-f3`, exit 0).
- **L4 (low).** Four copies of one `path:line` satisfy `refs >= 4` (`fx-e2`, exit 0). The instrument
  counts occurrences, never distinct citations.
- **L5 (low).** Header words are matched as **substrings** (l.161): `triggers | arms | exit-code | receipts`
  is accepted (`fx-b2`, exit 0). The claim says the header "carries `trigger`, `arm`, `exit`, `receipt`".
- **L6 (medium vs the surface, zero vs the predicate).** Row **content** is never checked: `| | | 1 | |`
  and `| a | | 2 | |` count as rows (`fx4-l3`, `fx4-l5`, exit 0), so seven real rules + one filler row
  meets `block22_rows >= 8`. The predicate says `block22_rows >= 8`; the surface says "at least eight
  **rule** rows". The instrument follows the predicate — the divergence is between the two sentences.
- **L7 (medium for the landing).** The marker need not sit on the 22nd block: with 22 blocks and the
  marker on block **5**, the counter exits 0 (`fx5-a6`). Predicate clause 2 ("exactly one block contains
  the marker") permits this by its letter; the surface calls the block "rule block 22", and the kill rule
  only names `red-relabelled-21-block` (21 blocks), so a relabelled 12th block with a green table scores.
- **L8 (low, likely intended).** Backticked exit cells are accepted (`fx-h`, exit 0; `strip("\` ")` l.146).
  "exactly one of `0`, `1`, `2`" read literally would reject `` `1` ``; the claim's own tables are
  backticked, so this tolerance is necessary — record it as a tolerance, not a defect.

### STRICTER / fragile — refuses or mis-reads what the claim words allow

- **S1 (medium).** `block_table` takes the **first** ≥3-line table in the block. A 3-line sample table
  above the decision table makes the counter grade the sample: `fx-i` → `rows 10`, `header_ok false`,
  exit 1, although the decision table beneath satisfies every clause.
- **S2 (low-medium).** The exit column is the **first** header cell containing `exit` (l.144). A decoy
  column `exit-cause` placed before `exit` hijacks it: `fx2-b5` rejects a table whose real exit cells are
  all valid. Column **order** is otherwise free (`fx3-b3`, `fx3-b4` exit 0).
- **S3 (low-medium).** The section ends at the first line starting `## ` **even inside a code fence**
  (`fx3-h3`: `rule_blocks 0`, exit 1). The frozen claims say nothing about fences; a fenced snippet in
  the landed block would silently truncate the craft section.
- **S4 (medium, semantics).** A heading `## Queue-drain craft` without the trailing space crashes at
  l.60 (`fx3-h2`): exit **1**, stdout **0 bytes** (sha256 of empty input, `e3b0c442…`), **no
  `--json-out` receipt**. Per the round contract exit 1 means "not met" and 2 means "could not
  evaluate"; a parse crash is the latter, and a receipt-less exit 1 is indistinguishable from a genuine
  red to any consumer that only reads the exit code.
- **S5 (cosmetic).** A single-line citation is echoed in `block22_unresolved_citations` as `path:1-1`
  (range-normalized). The value is correct; only the rendering differs from the input form.
- **S6 (informational).** The marker binds to whichever block contains it (`fx2-a3`): with the marker
  between blocks 21 and 22 it attaches to block 21, so every table/ref check then runs against block 21.
  Consistent with clause 2, but it means a mis-placed marker produces misleading sub-findings rather
  than a marker-specific one.

## 5. Landing risks for L1 (drawn from the above, ordered by blast radius)

1. Cite every reference as `path:line` or `path:first-last`; the counter will **not** catch a naked path
   (L1), so a reviewer must, or the depth evidence is thinner than the receipt says.
2. Keep the citations inside `corpus/{knowledge,lessons}/` or `plans/` with no subdirectory; nested
   targets are invisible in both directions (L2) and cannot serve as evidence.
3. Emit exit cells as bare `0`/`1`/`2` (backticks tolerated). `0/1`, `0 (met)`, `"1"`, `0+1` are red
   (`§2 c`, `§3`). One dual-valued cell makes all 8 rows fail.
4. Exactly **one** pipe table in the block, and no `exit`-containing column before the real exit column
   (S1, S2). Header order is otherwise free (b1–b3).
5. No line starting with `## ` anywhere in the block, fences included (S3).
6. The heading keeps its trailing space — `## Queue-drain craft ` — else the counter crashes as exit 1
   with an empty stdout (S4). Today's SKILL.md line 81 `## Queue-drain craft (rounds 5-12, distilled in
   round 13)` parses, so this is latent, not live.
7. Eight **content-bearing** rows still matter: the counter accepts filler rows (L6), so "eight rule
   rows" is a text requirement the instrument does not enforce.
8. Do not rely on the counter to prove the marker is on block 22 (L7); if the landing intends ordinal
   22, that is a human/reviewer check.

## 6. Lane datapoint (parse evidence only; no scoring decision)

The frozen counter at `--freeze f762b72… --rev HEAD` (= `faa875bc0eb839d15b83c4afa6078819e5a7b381`,
after `e715263c` landed block 22 and `1f4b27f8` amended its citations) returns **exit 0**:
`rule_blocks 22`, `block22_present 1`, `block22_rows 10`, `block22_refs 7`,
`block22_unresolved_citations []`, `block22_cites {S140:true, interpreter:true}`, `header_ok true`,
`preflight_selftest {cases:11, failures:0, exit:0, ok:true}`, `met_target true`.
Receipt: `receipts/lane-head-c1.json`. Read as "the landed block is on the parser's happy path", not as
"R45-C1 is scored" — the scoring seats own that call.

## 7. Receipts

`receipts/` beside this report holds 36 fixture receipts (the 37th sweep run, `fx3-h2`, wrote no receipt
by construction — that absence is the finding), the two `fx5` marker probes and `lane-head-c1.json`
(40 JSON files with `receipt-index.json`), the crash artefacts `fx3-h2-crash.stdout.txt` /
`fx3-h2-crash.stderr.txt`, and `receipt-index.json` with, per run: exact command, exit code, stdout
sha256, stdout/stderr byte counts, UTC time, and the observed receipt fields. Counter sha256 recorded in
the index. Index sha256 `dc4560d604a60209129537276c163431f5335c957d8d632e43c1d6e699583318` (written
2026-10-28T15:41:57Z; the two `fx5` probes and the lane run were added afterwards).

Selected stdout sha256 (first 12): `fx-a1 2380f23a812c`, `fx-a2 52a9d9cdd78b`, `fx-b ced32e0275f2`,
`fx-c 529449d3c324`, `fx-d 44272c6ce810`, `fx-e 7da04d2376b3`, `fx3-b3 81c5dabb15c3`,
`fx3-b4 81a5ec854e47`, `fx3-h2 e3b0c44298fc` (empty), `fx4-l3 f24f371f1f7e`, `fx5-a6 174bbce82c47`,
`lane-head 0c83a7b3fc34`.

## 8. Honest gaps

- Not run: `c1-counter.py --selftest` itself, `c2-counter.py`, `frozen-path-preflight.py --selftest`
  in isolation (the counter ran it from the fixture rev, and from lane HEAD, both `cases=11
  failures=0`). Seats `ExecSelftestSynthetic`, `RevC2Freeze` and `CritC1Witness` cover those; no
  duplication claimed.
- Not tested: `path:1-` (trailing dash), CRLF line endings, a marker inside a fenced block, tables whose
  separator uses `:` alignment (the separator regex permits it but no fixture exercises alignment), and
  `--rev` values that are not `HEAD`/`HEAD~1`.
- No tool installs; no package manager touched.
- Fixture repos were created and destroyed entirely under the scratch root; nothing under `/tmp` was used
  as evidence.

`Report: .ufo/waves/round-45/w1/R45W1C1HeaderBoundary/report.md`
