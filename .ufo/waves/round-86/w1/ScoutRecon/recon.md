# ScoutRecon — round 86 (kaidoku) recon for R86-C1 / R86-C2

Seat: ScoutRecon (scout, read-only). BASE `2cf0b7ff93c698809bed321f7338276a22d6beb9`.
Lane tip at recon: `0864a7bdbf185583773d1a3f3416de76e9cab137`.
No production file was edited. All fixtures lived under
`/fast/scratch/hyaku/kaidoku-r86/ScoutRecon/` and were removed after the receipts
below were copied.

---

## 0. TL;DR for the next seat

| # | Finding | Effect |
|---|---|---|
| F1 | **A3 needs exactly ONE `\| coverage \|` row in the whole `SCORECARD.md`, not one in `## Owned axes`.** BASE has **23**. | The counter's `rows[0]`/`len(rows)!=1` check fails on the count before it ever reaches the pointer check. A3 is unreachable until the 22 historical rows are renamed out of the `\| coverage \|` prefix. |
| F2 | **A1's count clause lives in the `teaches` cell (index 6), not the `anchor` cell (index 5).** | The BASE S303 row puts "five scopes" in its *anchor* cell; the counter reads `cells[6]`. The new superseding row must carry `count N (ids)` in its **teaches** cell. |
| F3 | **A3's receipt must be a blob at `--rev` whose JSON has a 40-hex `rev`, and its round must be ≥ the row's own round.** The row's own round is `85`; no round-85 receipt exists at BASE. | The new receipt must be committed **before** the measured revision, at a round ≥ 85 (round-86 works). |
| F4 | **`tools/round-84/mutation-closure.py` is pinned in `claims.json` (`target_instruments` + `loaded_by_counter`) with sha256 `e5cfd2ed…`.** A2 requires editing its docstring → the pin breaks. | `tools/round-84/freeze-precheck.py` then reports `COUNTER_PIN_MISMATCH:tools/round-84/mutation-closure.py` and the round-86 container goes **FLAGGED**. The pin must be re-issued by the L1 after the edit. |
| F5 | **`gate-registry.py` executes the tool from the `--root` WORKING TREE, not from `--rev` and not from `--worktree`.** | The row's self-test cell must name a command that works from the lane root; the observed exit reflects the working tree's tool bytes. |
| F6 | The registry row format is strict: `cells[0]` must be **exactly** `` `tools/round-85/predicate-bind.py` `` (backticked), `>= 7` cells, verdict cell must literally contain `0=`, `1=`, `2=`. | A near-miss row (unquoted path, `0=clean` only, 6 cells) silently drops out of `registry_rows` → `G1` fails with `rows: 0`. |
| F7 | `SKILL.md` at BASE has **zero** occurrences of `predicate-bind`; the registry section has 140 `tools/`-prefixed rows. | The insertion point is line 1930 (immediately before `<!-- /instrument-registry -->` at line 1930; last tool row is line 1929). |

---

## 1. R85-3 — S303's supersession count (A1)

### Command and observed output

```
$ git show 2cf0b7ff93c698809bed321f7338276a22d6beb9:corpus/SOURCES.md | grep -n 'rea-agents-6.5.0.tgz'
```

Rows whose **source cell** (column index 1) carries `rea-agents-6.5.0.tgz` — parsed with the
counter's own `split_row` / `parse_registry` (`tools/round-86/record-agreement.py:78-95`):

```
total registry rows: 209
rows whose SOURCE cell (cells[1]) carries rea-agents-6.5.0.tgz: 8
  line 85 S079
  line 86 S080
  line 89 S083
  line 96 S090
  line 98 S092
  line 125 S119
  line 129 S123
  line 219 S303
ids: ['S079', 'S080', 'S083', 'S090', 'S092', 'S119', 'S123', 'S303']
excluding S303: 7 ['S079', 'S080', 'S083', 'S090', 'S092', 'S119', 'S123']
```

**8 rows / 7 prior** — matches the expectation in the seat brief. Note the set is **not**
`S083/S090/S092/S119/S123` (what S303's own cell claims): `S079` and `S080` also carry the
tarball URL in their source cell.

### The BASE S303 row, cell by cell (11 cells)

```
cell0: S303
cell1: npm tarball `rea-agents-6.5.0.tgz` as authority for the extraction-gap taxonomy — https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz
cell2: code
cell3: A
cell4: Curation candidate: the packed package as an authority for gap-kind semantics
cell5: Opened 2026-11-04; the registry already holds this URL in five scopes (S083/S090/S092/S119/S123) and the packed bytes expose no stable anchor
cell6: REJECTED: a tarball is not an anchored document and the URL is already in scope; S302 is the anchored authority; flip: a published REA documentation URL that anchors the gap taxonomy
cell7: rejected
cell8: 2026-11-04
cell9: on-release
cell10: corpus/lessons/round-84.md
```

**Where "five scopes" actually sits: cell5 (the `anchor` cell).** The counter reads
`r["cells"][6]` (the `teaches` cell) — see `record-agreement.py:100-115`:

```python
sup = [r for r in rows if len(r["cells"]) > 6 and r["cells"][6].startswith("supersedes S303")]
row = sup[-1]
teaches = row["cells"][6]
m = re.search(r"count\s+(\d{1,3})(.*)$", teaches)
prior = [i for i in url_rows if i not in (row["id"], "S303")]
declared = int(m.group(1))
ids = [i for i in re.findall(r"\bS\d{3,}\b", m.group(2)) if i != row["id"]]
ok = declared == len(prior) and sorted(set(ids)) == sorted(set(prior))
```

So the **new** superseding row must satisfy all of:

1. It is a row in `corpus/SOURCES.md` with **11** cells (the registry header is
   `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`).
2. Its **cell 6** (`teaches`) **starts with** the literal string `supersedes S303`
   (`startswith`, so a leading space or a different verb like "replaces S303" fails).
3. Its cell 6 contains `count <N>` where **N = 7**.
4. The ids listed **after** the `count N` clause are exactly
   `S079 S080 S083 S090 S092 S119 S123` — set-equal, order-free.
5. It is the **last** such row in the file (`sup[-1]`), so only one superseding row should exist.

### Verified fix (fixture, then removed)

```
$ python3 -I -B tools/round-86/record-agreement.py --root . \
    --worktree <fixture> --json-out <receipt>
agreed 3 / 3 mismatches []
A1-s303-supersede-count True {"declared_count": 7,
  "declared_ids": ["S079","S080","S083","S090","S092","S119","S123"],
  "prior_rows":   ["S079","S080","S083","S090","S092","S119","S123"],
  "superseding_row": "S305", "url_rows_total": 9}
```

Working cell 6 (the `teaches` cell) used:

```
supersedes S303 — corrected prior-row count 7 (S079/S080/S083/S090/S092/S119/S123); the packed package is not an anchored document
```

### Grammar traps (measured, not guessed)

| Trap | Observed behaviour |
|---|---|
| `count N` placed in the **anchor** cell (index 5) | `why: "superseding row states no 'count N' clause"` — the counter never sees it. |
| `account 7` instead of `count 7` | `re.search(r"count\s+(\d{1,3})")` **matches** `account 7` (substring, no word boundary) → declared = 7. Silent, but do not rely on it. |
| `S303` appearing **after** the `count` clause | `ids` collects it → `S303` is in `declared_ids` but not in `prior` → **mismatch**. |
| `count 17` | `(\d{1,3})` accepts 3 digits → declared = 17 ≠ 7 → mismatch. |
| A superseding row whose **source cell** carries the URL | `url_rows_total` becomes 9, but `prior` excludes the superseding row id, so `prior` stays 7. Safe either way — confirmed in the fixture (`url_rows_total: 9`, `prior_rows` = 7 ids). |

### Census interaction

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <fixture-SOURCES.md> --root /home/vgpnk/Projects/shokunin`
→ **0** `E0` findings on the fixture that adds the superseding row (same as BASE: 0).

`E04` (duplicate URL+scope) is **exempted** when the row's `teaches` matches
`/supersedes S[0-9]{3}/` (`sources-census.sh:648`). The superseding row's `teaches` must
therefore keep the literal `supersedes S303` string — which the counter requires anyway.
`W04` (same URL across scopes) stays a warning and does not change lane status.

`E11` (used-by path missing on disk) applies: the new row's `used-by` cell must name a path
that **exists on disk**. A `corpus/lessons/round-86.md` that does not yet exist is an E11
error at census time.

---

## 2. R85-5 — the `mutation-closure.py` docstring (A2)

### The docstring sentence, with line numbers (BASE)

```
$ git show 2cf0b7ff93c698809bed321f7338276a22d6beb9:tools/round-84/mutation-closure.py | sed -n '2,22p'
```

```
line  8: present in the target's own output; an absent declared case is inconclusive, never a pass).
line 12:                 declared case is absent from the pristine inventory (QUALITY 138: an absent
line 13:                 detector is a survivor, never a pass)
```

The single sentence that names an absent declared case is, verbatim, at **line 8**:

> `an absent declared case is inconclusive, never a pass).`

### The status the code assigns in the `not case_present` branch

```
$ git show 2cf0b7ff93c698809bed321f7338276a22d6beb9:tools/round-84/mutation-closure.py | grep -n 'case_present'
195:        case_present = mutant["declared_case"] in pristine_inventory
197:                      "declared_case_present": case_present})
202:        elif not case_present:
```

The counter's own extraction (`record-agreement.py:117-141`) confirms the branch's label:

```
A2-docstring-status False {"code_status": "survived",
  "conflicting_words": ["inconclusive"],
  "sentence": "an absent declared case is inconclusive, never a pass)."}
```

→ the code assigns **`survived`**; the docstring says **`inconclusive`**. That is the drift.

### The counter's exact rule

```python
label = None
for i, line in enumerate(lines):
    if re.match(r"\s*(?:el)?if not case_present:\s*$", line):
        for follow in lines[i + 1:i + 6]:
            m = re.search(r'entry\["status"\]\s*=\s*"([a-z_]+)"', follow)
            if m: label = m.group(1); break
        break
...
sentences = [s for s in re.split(r"(?<=[.;:])\s+", doc) if "absent declared case" in s]
if len(sentences) != 1: -> fail
stem = label[:5]                       # "survi"
others = [w for w in STATUS_WORDS if w[:5] != stem and re.search(rf"\b{w}", sentence)]
ok = stem in sentence and not others
```

Consequences for the fix sentence:

- The sentence must contain `surviv` (the 5-char stem `survi` of `survived`) — the word
  `survivor` also satisfies it.
- The sentence must **not** contain `inconclusive` or `killed` (`STATUS_WORDS` minus those
  sharing the `survi` stem — i.e. `inconclusive` and `killed`; `survivor` is *not* in the
  conflict set because `survivor`[:5] == `survi`).
- **Exactly one** sentence in the whole module docstring may contain the phrase
  `absent declared case`. The docstring's second mention of absence is at lines 12-13
  ("the declared case is absent from the pristine inventory … an absent detector is a
  survivor") — that phrasing does **not** contain the literal phrase `absent declared case`,
  so it does not create a second sentence. Verified: BASE produces exactly one.
- Note the counter splits sentences on `(?<=[.;:])` — a trailing `)` stays attached to the
  sentence, which is why the observed sentence ends `pass).`

### Verified fix (fixture)

Replacing `an absent declared case is inconclusive, never a pass` with
`an absent declared case is a survivor, never a pass` yields:

```
A2-docstring-status True {"code_status": "survived", "conflicting_words": [],
  "sentence": "an absent declared case is a survivor, never a pass)."}
```

and the tool's own selftest stays green after the docstring edit:

```
$ python3 -I -B <fixture>/tools/round-84/mutation-closure.py --selftest
SELFTEST cases=10 failures=0
```

(The round-84 mutant table `.ufo/waves/round-84/mutants.json` targets only
`tools/round-82/printed-command.py` (8), `tools/round-82/conjunction-gate.py` (3) and
`tools/round-83/source-bind.py` (2) — **no** mutant targets `mutation-closure.py`, so the
docstring edit does not perturb the round-84 mutation battery.)

### ⚠ F4 — the pin conflict (must be reported to the L1)

`tools/round-84/mutation-closure.py` is pinned in `.ufo/waves/round-86/claims.json`:

```json
"target_instruments": { "tools/round-84/mutation-closure.py": "e5cfd2ededbdfa7af4b6d2a40cfc23685edc58828f971efd4a5739a07904f6ad" },
"loaded_by_counter":  { "tools/round-84/mutation-closure.py": "e5cfd2ededbdfa7af4b6d2a40cfc23685edc58828f971efd4a5739a07904f6ad" }
```

That digest is the BASE blob's sha256 (verified: `git show 2cf0b7ff…:tools/round-84/mutation-closure.py | sha256sum`
→ `e5cfd2ededbdfa7af4b6d2a40cfc23685edc58828f971efd4a5739a07904f6ad`).

Editing the docstring changes that blob, and `tools/round-84/freeze-precheck.py`
(`PIN_KEYS = ("instruments", "loaded_by_counter", "producers_not_counters")`) then reports,
on a fixture where only the docstring was edited:

```
"findings": ["COUNTER_PIN_MISMATCH:tools/round-84/mutation-closure.py"],
"verdict": "FLAGGED", "met": false
```

So the L1 must **re-issue the pin** for `tools/round-84/mutation-closure.py` in
`.ufo/waves/round-86/claims.json` after the A2 edit lands, or the round-86 container
self-check goes FLAGGED. (The pre-freeze receipt
`.ufo/waves/round-86/pre/freeze-precheck-at-declaration.json` shows the container is
currently **CLEAN** at rev `ec9963eb9…`.)

---

## 3. R85-6 — the SCORECARD `| coverage |` receipt pointer (A3)

### 3a. The row's own round vs the receipts it names

```
$ grep -n '^| coverage |' SCORECARD.base.md   # 23 hits, first at line 23
```

The **first** `| coverage |` row (line 23, inside `## Owned axes`, heading at line 19) has
5 cells; the last cell (the row's own round) is:

```
cell4: 85 (self-assessment fraction re-derived at the round-85 record; score unchanged)
```

`re.match(r"\s*(\d{1,3})\b", round_cell)` → **claim_round = 85**.

Receipts named **in that row**:

```
.ufo/waves/round-84/l1/scores/coverage-selfcheck.json
.ufo/waves/round-76/l1/scores/coverage-selfcheck-at-record.json
.ufo/waves/round-75/l1/scores/coverage-selfcheck-at-record.json
.ufo/waves/round-68/l1/scores/coverage-selfcheck-at-record.json
.ufo/waves/round-67/l1/scores/coverage-selfcheck-at-record.json
```

Newest named round = **84 < 85** → `why: "named receipt predates the row's own round"`.

**Does a round-85 receipt exist at `2cf0b7ff`?**

```
$ git ls-tree -r --name-only 2cf0b7ff93c698809bed321f7338276a22d6beb9 -- .ufo/waves/round-85/l1/scores/
(no output — the directory does not exist)
$ git ls-tree -r --name-only 2cf0b7ff… -- .ufo/waves/round-85/ | head
.ufo/waves/round-85/c1/literal-none-predicate-bind.json
.ufo/waves/round-85/c1/variant-predicate-bind.json
.ufo/waves/round-85/c2/after-21row.json
.ufo/waves/round-85/c2/after-frozen13-regression.json
.ufo/waves/round-85/claims.json
.ufo/waves/round-85/l1/sources/FirmwarePublication.rea-agents-6.5.0.js
.ufo/waves/round-85/l1/sweep/tokens-red-before.txt
.ufo/waves/round-85/mutants.json
.ufo/waves/round-85/pre/…
.ufo/waves/round-85/r85-w1-*.json
.ufo/waves/round-85/w1-briefs/…
.ufo/waves/round-85/w1/…
```

**No round-85 `l1/scores/` receipt exists at BASE.** The nearest existing receipts are
round-84 (and older).

The existing round-84 receipt is a valid A3 target — it is a blob at BASE and its `rev`
field is 40-hex:

```
$ git show 2cf0b7ff…:.ufo/waves/round-84/l1/scores/coverage-selfcheck.json | python3 -c "…"
rev= '26f4e1ba85e0ca85921ea99f3fdd02a619373b78'
40hex? True
keys= ['atoms','exit','mismatches','ok','predicate','recipe_a','recipe_a_block_sha256','recipe_a_diffs','recipe_a_equivalent','recipe_a_hidden','recipe_a_hidden_count','rev','stem','stem_score','tool']
```

(Note the receipt's `rev` (`26f4e1ba…`) is the *measured* revision; it is **not** an ancestor
of the commit that added the receipt file (`8ae9c8ee…`) — `git merge-base --is-ancestor`
returns non-zero. The counter only requires the field to be 40-hex, not to be an ancestor.)

### 3b. ⚠ F1 — the counter demands EXACTLY ONE `| coverage |` row in the whole file

This is the single most important thing the next seat must not miss. The counter
(`record-agreement.py:154-158`) does **not** scope to `## Owned axes`:

```python
rows = [line for line in card.splitlines() if line.startswith("| coverage |")]
if len(rows) != 1:
    return False, {"why": f"expected exactly one `| coverage |` row, found {len(rows)}"}
```

BASE has **23** such rows (line 23, then 179, 258, 317, 363, 404, 450, 492, 522, 551, 605,
736, 797, 961, 1059, 1535, 2243, 2301, 2359, 2417, 2506, 2948, 3409 — each in a different
historical round section). The BASE receipt shows the counter **failing on the count**:

```
"id": "A3-receipt-pointer", "ok": false,
"detail": {"why": "expected exactly one `| coverage |` row, found 23"}
```

The pointer check is never reached at BASE. On a fixture where the 22 historical rows were
renamed to `| coverage_hist |` (leaving only the `## Owned axes` row), the counter proceeds
and reports the *second*, distinct defect:

```
A3-receipt-pointer False {"claim_round": 85,
  "receipt": ".ufo/waves/round-84/l1/scores/coverage-selfcheck.json",
  "receipt_round": 84,
  "why": "named receipt predates the row's own round"}
```

So **two independent edits** are needed for A3, and the second is invisible until the first
is done:

- **A3-i** — the file must contain exactly one line starting with `| coverage |`.
- **A3-ii** — that row's last cell must lead with a round `R`, and a receipt path
  `.ufo/waves/round-M/l1/scores/<name>.json` with `M >= R` must be named **in that same
  row**, must be a blob at `--rev`, and its JSON must carry a 40-hex `rev` field.

Also note `rows[0]` — the paths are collected from **the first** matching line only
(`re.findall(..., rows[0])`), so the receipt path must appear in the surviving row, not
elsewhere in the file.

### 3c. What A3 looks like when it passes (verified)

Fixture: one `| coverage |` row (the `## Owned axes` one, last cell still leading with `85`),
its evidence cell naming `.ufo/waves/round-86/l1/scores/coverage-selfcheck.json`, and that
receipt committed with `"rev": "0000…0"` (40 hex):

```
A3-receipt-pointer True {"claim_round": 85,
  "receipt": ".ufo/waves/round-86/l1/scores/coverage-selfcheck.json",
  "receipt_round": 86, "receipt_rev": "0000000000000000000000000000000000000000"}
```

⇒ **round-86 ≥ 85 works.** The receipt's `rev` need not be the measured revision, only
40-hex — but the receipt **file** must be a blob at the measured `--rev`, so it must be
committed before the measurement.

### 3d. Renaming the 22 historical rows — consumer impact (measured)

The rename needed for A3-i is `| coverage |` → something else, for the 22 rows **outside**
`## Owned axes`. I checked every consumer of the `| coverage |` prefix in the lane:

| Tool | How it reads the row | Effect of renaming the 22 historical rows |
|---|---|---|
| `tools/round-25/a2/c1-calibration.py:76` | `next((ln for ln in score.splitlines() if ln.startswith("| coverage |")), "")` — **first** match, unscoped | **Unaffected** — line 23 is still the first match. (Its I4 atom needs `(\d+)/(\d+) knowledge files mapped` in that row; the row keeps it.) |
| `tools/round-26/c2-calibration.py:157-199` | `owned_axes_rows()` — scoped to `## Owned axes`, and requires exactly one `\| coverage \|` row **inside** it | **Unaffected** — the scoped row is unchanged. Its `decoy-outside-owned-axes` selftest case builds its own fixture, not the lane's card. |
| `tools/round-66/coverage-selfcheck.py:219-227` | `coverage_row()` — scoped `AXES_HEAD = "## Owned axes"` / `AXES_END = "\n## "` | **Unaffected.** Measured: `--selfcheck` on the renamed fixture → `"stem": {"knowledge_files": 168, "mapped": 168, "mismatches": 0, "missing": [], "dangling": []}`, `recipe_a_hidden_count: 26`, exit 0. |
| `tools/round-53/r53-record.py:503-514` | `owned_row()` — **first** match, unscoped | **Unaffected** — line 23 still first. |
| `tools/round-36/c2-counter.py:66`, `tools/round-38/c2-counter.py:70` | `section(sc, '## Owned axes')` | **Unaffected** (scoped). |
| `tools/round-47/record.py:174-176`, `tools/round-50/c2-record.py:498-503` | scoped to `## Owned axes`; round-50 wants exactly 1 coverage row there | **Unaffected.** |
| `tools/round-73/74/75/76/record-audit.py` | read `## Capabilities`, not the axes rows | **Unaffected** — all four ran green on the renamed fixture (`"defects": []`). |

**Measured on the renamed fixture** (`git init` clone of the lane at BASE with 22 rows
renamed, then `tools/round-66/coverage-selfcheck.py --selfcheck`):
`missing []`, `dangling []`, `mismatches 0`, `stem.coverage_score 10.0`, exit 0; and
round-73/74/75/76 record-audits all returned `"defects": []`.

**Caveat for the L1**: renaming the historical rows is a **production SCORECARD edit that
rewrites historical sections**. Two smaller alternatives exist and were considered:
(i) leave the historical rows alone and instead make the *counter* tolerant — **forbidden**
(the counter's bytes are pinned in `claims.json` `instruments` and the atom rules are
frozen); (ii) move the `## Owned axes` row so it is the only `| coverage |` row — same edit
cost. The rename is the only route that leaves the counter byte-identical. If the L1 judges
rewriting 22 historical rows too invasive, **A3 cannot be reached this round** and the
honest outcome is a partial claim — that is a decision for the L1, not for me.

---

## 4. R85-2 — the SKILL.md instrument-registry row (C2)

### 4a. BASE state

```
$ grep -c 'predicate-bind' SKILL.base.md
0
$ grep -n 'instrument-registry' SKILL.base.md
1780:<!-- instrument-registry v2 -->
1930:<!-- /instrument-registry -->
```

`grep -c 'predicate-bind' SKILL.md` at BASE = **0** — the tool is entirely unregistered.
The registry section spans **lines 1780–1930** of `SKILL.md` (1988 lines total) and holds
**140** `tools/`-prefixed rows.

### 4b. Exact marker lines and the insertion point

| What | Line | Content |
|---|---|---|
| Section open marker | **1780** | `<!-- instrument-registry v2 -->` |
| Section header row | **1782** | `\| tool \| gate or probe - purpose \| verdict map (exit codes) \| self-test command \| pinned-value path \| write scope \| owner \|` |
| Header separator | **1783** | `\|---\|---\|---\|---\|---\|---\|---\|` |
| First tool row | 1784 | `\| \`tools/round-41/c1-counter.py\` \| …` |
| **Last tool row (BASE)** | **1929** | `\| \`tools/round-84/nested-sqfs.py\` \| …` |
| **Section close marker** | **1930** | `<!-- /instrument-registry -->` |

**Insertion point: immediately before line 1930** — i.e. append the new row after the
`tools/round-84/nested-sqfs.py` row and before `<!-- /instrument-registry -->`. The new row
becomes **line 1930** and the close marker moves to **1931**.

(The counter's `registry_rows()` splits the section on `REGISTRY_OPEN = "<!-- instrument-registry"`
and `REGISTRY_CLOSE = "<!-- /instrument-registry -->"`, so the row must sit **inside** that
span. A row placed after the close marker is invisible to `G1`.)

### 4c. The three most recent rows' cell style (BASE, lines 1927-1929)

| Line | cell0 | cell2 (verdict map) | cell3 (self-test command) | cell6 (owner) |
|---|---|---|---|---|
| 1927 | `` `tools/round-84/freeze-precheck.py` `` | `0=each container's verdict equals its \`--expect\` (or is CLEAN) with the \`instruments-only\` control accepting the defective container; 1=any mismatch or a FLAGGED container without an expectation; 2=a container that cannot be read` | `` `python3 -I -B tools/round-84/freeze-precheck.py --root . --rev <rev> --container … --json-out <receipt>` `` | `kaidoku-r84` |
| 1928 | `` `tools/round-84/mutation-closure.py` `` | `0=every mutant killed, no inconclusive, every pristine green; 1=any survivor, inconclusive or red pristine; 2=target or table unreadable` | `` `python3 -I -B tools/round-84/mutation-closure.py --root . --rev <rev> --mutants .ufo/waves/round-84/mutants.json --work <scratch> --json-out <receipt>`; selftest 10 cases `` | `kaidoku-r84` |
| 1929 | `` `tools/round-84/nested-sqfs.py` `` | `0=all nine arms true and the control fires; 1=any arm false or control silent; 2=could-not-evaluate` | `` `python3 -I -B tools/round-84/nested-sqfs.py --rev <rev> --work <scratch> --json-out <receipt>`; selftest 9 cases `` | `kaidoku-r84` |

House style for the self-test cell, in order: a **backticked** `python3 -I -B <tool path> …`
command, then a `— ` separator, then the case count / date. Rows that carry an `exit N`
declaration spell it as `exit 0 on <date>` (e.g. line 1825's
`python3 -I -B tools/round-48/meanings.py --selftest — 18 cases, exit 0 on 2026-10-28`).

**The exit-N spelling is load-bearing.** `declared_command_exit()` searches the **whole**
self-test cell for `re.search(r"\bexit\s+(\d)\b", cell)` — so the `exit N` must appear
**after** the `— ` separator, but it may sit anywhere in the cell. Meanwhile
`command_argv()` takes `cell.split(" — ", 1)[0]` — **only the text before the first ` — `**
is the command. So the cell must be exactly:

```
`python3 -I -B tools/round-85/predicate-bind.py --selftest` — <N> cases, exit 0 on <date>
```

with the command first, then ` — `, then the `exit N`.

### 4d. The five atoms, exactly as the counter reads them

`tools/round-86/gate-registry.py`:

- **G1** — `find_row()` matches `r[0] == "`tools/round-85/predicate-bind.py`"`. The cell 0
  must be the path **in backticks, exactly**, with no extra text. `registry_rows()` also
  requires `len(cells) >= 7` **and** `cells[0].startswith("`tools/")`.
- **G2** — `row[2]` must contain the literals `0=`, `1=` **and** `2=`; and the **observed**
  `--selftest` exit must equal `0`.
- **G3** — `row[3]` must name a `python3` command on the tool path and an `exit N`; the
  command's argv is executed **with no shell** in `--root` under a **four-key** child env
  (`PATH`, `HOME`, `TMPDIR`, `LANG`) and the observed exit must equal the declared one.
- **G4** — `row[4]` must name at least one `.ufo/waves/round-<N>/claims.json` that is a
  blob at `--rev` (the regex is `\.ufo/waves/round-\d+/claims\.json`).
- **G5** — `row[6]` must match `kaidoku-r(\d+)$` with the same `N` as the tool's own
  `tools/round-<N>/` directory → **`kaidoku-r85`**.

### 4e. Verified passing row (fixture, 5/5)

```
| `tools/round-85/predicate-bind.py` | gate — R85-C1 calibration: the round-85 literal-none predicate binding | 0=met; 1=not met; 2=could-not-evaluate | `python3 -I -B tools/round-85/predicate-bind.py --selftest` — 21 cases, exit 0 on 2026-11-04 | `.ufo/waves/round-85/claims.json` | only the explicit `--json-out` path | kaidoku-r85 |
```

```
$ python3 -I -B tools/round-86/gate-registry.py --root . --worktree <fixture> --work <scratch> --json-out <receipt>
GATE_REGISTRY agreed=5/5 mismatches=[]
G1-row-present         True {"rows": 1, "tool": "tools/round-85/predicate-bind.py"}
G2-exit-map-observed   True {"declared_map_complete": true, "observed_selftest_exit": 0, "declared_success_exit": 0}
G3-self-invocation     True {"argv": ["-B","tools/round-85/predicate-bind.py","--selftest"], "declared_exit": 0, "observed_exit": 0, "last_line": "SELFTEST cases=21 failures=0"}
G4-pinned-blob         True {"declared_pins": [".ufo/waves/round-85/claims.json"], "blobs_at_rev": [".ufo/waves/round-85/claims.json"]}
G5-owner-round         True {"owner": "kaidoku-r85", "tool_round": "85"}
```

The tool's own selftest is green at BASE:

```
$ python3 -I -B tools/round-85/predicate-bind.py --selftest
SELFTEST cases=21 failures=0
```

### 4f. ⚠ F5 — where the counter actually executes the tool

`run_selftest()` and the G3 exec both use `cwd=str(root)` and the **relative** path
`tools/round-85/predicate-bind.py`:

```python
proc = subprocess.run([sys.executable, "-I", "-B", TOOL, "--selftest"],
                      cwd=str(root), env=env, capture_output=True, text=True, timeout=600)
```

So the bytes executed are **`--root`'s working-tree copy** — *not* the `--rev` blob and
*not* the `--worktree` copy. Measured, with `--root R --worktree W` where `R`'s tool exits 1
and `W`'s tool exits 0:

```
"last_line": "ROOT_TOOL_RAN", "observed_exit": 1
```

⇒ the **root** copy ran, not the worktree copy. Two consequences:
- the row's self-test cell must name a command that works from the **lane root**;
- the observed exit reflects the **working tree's** `tools/round-85/predicate-bind.py` bytes,
  so the lane's working tree must hold the same tool the row describes.

(The `--worktree` mode is therefore only a **read** mode: SKILL.md and the pinned
`claims.json` are read from the worktree, while the tool executes from `--root`.)

### 4g. Format traps (measured against the counter's own source)

| Trap | Observed |
|---|---|
| cell 0 without backticks (`tools/round-85/predicate-bind.py`) | `registry_rows()` skips it (`cells[0].startswith("`tools/")` is false) → `G1` `rows: 0` |
| a row with only 6 cells | skipped by `len(cells) >= 7` → `G1` `rows: 0` |
| verdict cell missing `2=` | `G2` `declared_map_complete: false` |
| `exit 0` placed **before** the ` — ` | `command_argv()` would then take only that fragment as the command → argv parse failure or a wrong argv → `G3` red |
| `exit 10` (two digits) | `re.search(r"\bexit\s+(\d)\b")` matches only the single digit `\d` → `declared_exit` would be `1` |
| owner `kaidoku-r85 (round 85)` | `re.search(r"kaidoku-r(\d+)$", owner.strip())` is `$`-anchored → **no match** → `G5` red |
| owner `kaidoku-r84` | `G5` red (round mismatch with `tools/round-85/`) |
| pinned cell naming only a non-`claims.json` path | `G4` `declared_pins: []` → red (the regex demands `round-<N>/claims.json`) |

---

## 5. S255 (`git-show` documentation) — current record and re-openability

The row, cell by cell (BASE `corpus/SOURCES.md` line 172):

| Field | Value |
|---|---|
| cell0 (id) | `S255` |
| cell1 (source) | `git-show documentation — https://git-scm.com/docs/git-show (plain HTML; snapshot bytes and sha256 in \`.ufo/waves/round-55/l1/s255/\`)` |
| cell2 (kind) | `docs` |
| cell3 (tier) | **`A`** |
| cell4 (scope) | `The official semantics of the revision-pinned blob read the round-55 instruments use: \`git show REV:path\` reads an object's bytes from the repository, never from a mutable worktree` |
| cell5 (anchor) | `DESCRIPTION "For plain blobs, it shows the plain contents." (8 words); fetched 2026-11-01, snapshot sha256 \`0a95cbcd8868054d851eedb192864798092c597592851989f5d1bb392730168a\`` |
| cell6 (teaches) | `Grounds the object-model discipline of \`tools/round-55/corrections-pin.py\` and \`tools/round-55/v6-block-digest.py\`: a ledger or table digest is computed over the bytes at a named revision, so the verdict names the revision it was measured against; tool documentation, not an REA surface, and no git internals were modified.` |
| cell7 (status) | **`mined`** |
| cell8 (opened) | **`2026-11-01`** |
| cell9 (recheck) | **`on-release`** |
| cell10 (used-by) | `plans/round-55-claims.md, tools/round-55/corrections-pin.py, corpus/lessons/round-55.md, corpus/knowledge/2026-11-04-r81-registry-and-record-boundary.md, corpus/lessons/round-81.md, corpus/knowledge/2026-11-04-r83-positive-source-attribution.md, corpus/lessons/round-83.md` |

### Is the row openable again this round?

**Yes.** Evidence:

1. **Precedent — it was re-opened before.** `corpus/lessons/round-83.md:19`:
   `Registry delta: zero new rows; S255 status mined→mined and recheck on-release→on-release
   unchanged. Only used-by changes: …` and `corpus/knowledge/2026-11-04-r83-positive-source-attribution.md:1`
   carries `source: S255 — https://git-scm.com/docs/git-show#_description; reopened 2026-11-04; …`.
   So the round-83 wave re-opened S255 and **changed only `used-by`** — no new row, no tier
   change, no status change.
2. **The append-only rule permits it.** `tools/round-38/registry-immutable.sh` (SKILL.md
   line 1713): "SOURCES append-only, CORPUS rule 2: a row present at BASE may differ at REV
   only in status, recheck and used-by". Adding S255 to the round-86 knowledge entry's
   `used-by` cell is exactly the allowed edit.
3. **Census-wise it is clean.** `sources-census.sh validate` on BASE gives **0** `E0`
   findings for this lane (only `W04` warnings), so re-opening S255 introduces no new
   error class. `E11` requires the added `used-by` path to exist on disk.
4. **The tier/status are already right.** Tier A, status `mined`, recheck `on-release` —
   the round-75 search-log convention (`corpus/SOURCES.md:251`) says the `opened` cell is
   the date the source was **first** opened by this lane, so a re-open does **not** rewrite
   `opened`. Leave `opened` at `2026-11-01`; record the re-open in the `## Search log`
   section and add the round-86 lesson/knowledge path to `used-by`.

**Caveat.** The round-85 lesson already shows the *pattern* the C1 work needs:
`corpus/lessons/round-85-verifier-spotcheck.md:241` — "SOURCES rule 2 requires a new row
whose `teaches` opens `supersedes S303 —`, preserving the old row". S255's re-open and
S303's supersession are **two different rows**; S255 is the *source* for the C1 knowledge
entry, S303/S305 is the *registry* correction. Do not merge them.

---

## 6. Can both counters be driven from a fixture tree?

### `tools/round-86/record-agreement.py --worktree <fixture>` — **YES**

```
$ grep -n 'add_argument' tools/round-86/record-agreement.py
395:    ap.add_argument("--root", default=".")
396:    ap.add_argument("--rev")
397:    ap.add_argument("--worktree")
398:    ap.add_argument("--control", choices=["substring-only"])
399:    ap.add_argument("--selftest", action="store_true")
400:    ap.add_argument("--json-out")
```

With `--worktree`, the read function becomes
`def read(path): return (work_root / path).read_text()` and `rev` becomes the string
`worktree:<path>`. **Every file the counter needs must exist in the fixture tree**:
`corpus/SOURCES.md`, `tools/round-84/mutation-closure.py`, `SCORECARD.md`, plus any
`.ufo/waves/round-M/l1/scores/*.json` the A3 atom names (read from the worktree, not from
git, in worktree mode). Measured: a fixture tree with those four files and the three
corrections applied yields `agreed 3/3 mismatches []`.

Caveat: in `--worktree` mode the receipt read for A3 comes from the **worktree**, so a
worktree fixture cannot prove "is a blob at `--rev`" — only the `--rev` mode can. Use
`--rev` for the real measurement.

### `tools/round-86/gate-registry.py --worktree <fixture>` — **YES, with a caveat**

```
$ grep -n 'add_argument' tools/round-86/gate-registry.py
335:    ap.add_argument("--root", default=".")
336:    ap.add_argument("--rev")
337:    ap.add_argument("--worktree")
338:    ap.add_argument("--work")
339:    ap.add_argument("--control", choices=["file-exists"])
340:    ap.add_argument("--selftest", action="store_true")
341:    ap.add_argument("--json-out")
```

The worktree supplies `SKILL.md` and the pinned `.ufo/waves/round-<N>/claims.json`
(read function → `work_root / path`), but **the tool is executed from `--root`'s working
tree** (see §4f). Measured: `--root .` (lane root, where
`tools/round-85/predicate-bind.py` exists and is green) with `--worktree <fixture>` →
`agreed=5/5 mismatches=[]`.

**Caveat:** the worktree copy of the tool is ignored, so a fixture that wants to prove a
*different* tool behaviour must put that tool in `--root`. `--work` (the scratch dir) is
where the counter creates `home/` and `tmp/` for the four-key child env.

Both counters also have `--selftest` (self-contained, no fixture needed) and
`--control {substring-only|file-exists}` (the declared false-green controls).

---

## 7. Assumptions a later seat must NOT make

1. **Do not assume A3 is one edit.** The counter needs *exactly one* `| coverage |` line in
   the whole `SCORECARD.md` (BASE: 23) **and** a round-≥R receipt. Both must land.
2. **Do not assume the `## Owned axes` scope is enough.** Unlike round-26/round-66, the
   round-86 counter scans the **whole file** (`line.startswith("| coverage |")`, no section
   split).
3. **Do not assume `count N` may live in the anchor cell.** The counter reads `cells[6]`
   (the `teaches` cell). BASE S303's "five scopes" is in `cells[5]` (anchor) — the
   superseding row's `teaches` must carry `count 7 (S079/S080/S083/S090/S092/S119/S123)`.
4. **Do not assume the id list is the 5 ids in S303's cell.** The correct set is **7**:
   `S079 S080 S083 S090 S092 S119 S123`. `S079` and `S080` also carry the URL.
5. **Do not assume the count is "five scopes" or "8 rows".** The counter's `prior` set
   excludes both `S303` and the superseding row → **7**.
6. **Do not assume `| S303 |` may be edited in place.** `tools/round-38/registry-immutable.sh`
   allows only `status`, `recheck`, `used-by` to change on an existing row — the
   `teaches`/`anchor` cells are frozen. The correction **must** be a new row.
7. **Do not assume a row id.** The next free id at BASE is **`S305`** (BASE max is `S304`);
   the counter does not check the id, but the census's `E03` forbids a duplicate.
8. **Do not assume the `supersedes` verb is free-form.** It must be the literal
   `supersedes S303` at the **start** of the `teaches` cell (`startswith`), and it also
   satisfies the census's `E04` exemption.
9. **Do not assume the docstring may keep `inconclusive` anywhere in that sentence.** The
   sentence must contain `survi` and must not contain `inconclusive` or `killed`.
10. **Do not assume the docstring edit is free.** It breaks the
    `loaded_by_counter` / `target_instruments` pin on `tools/round-84/mutation-closure.py`
    → `freeze-precheck` reports `COUNTER_PIN_MISMATCH` and the round-86 container goes
    FLAGGED. The pin must be re-issued.
11. **Do not assume a round-85 receipt exists.** `.ufo/waves/round-85/l1/scores/` does not
    exist at BASE. The new receipt must be committed at a round ≥ 85 **before** the
    measured revision, with a 40-hex `rev` field.
12. **Do not assume the receipt's `rev` must be an ancestor.** Only the 40-hex format is
    checked (the round-84 receipt's `rev` is *not* an ancestor of its own commit).
13. **Do not assume 7 registry columns is a formality.** `registry_rows()` requires
    `len(cells) >= 7`; a 6-cell row is invisible. And `cells[0]` must be the **backticked**
    path, exactly.
14. **Do not assume the verdict cell may use prose.** It must contain the literal
    `0=`, `1=`, `2=`.
15. **Do not assume `exit N` may be placed before the ` — `.** `command_argv()` takes only
    the text before the first ` — `; the `exit N` is matched anywhere in the cell but must
    describe the command that actually runs.
16. **Do not assume a 2-digit exit works.** `declared_command_exit()` matches a single
    digit (`\d`), so `exit 10` declares `1`.
17. **Do not assume the owner cell may carry a suffix.** `kaidoku-r(\d+)$` is `$`-anchored.
18. **Do not assume the counter runs the tool at `--rev`.** It runs `--root`'s working-tree
    copy (§4f). The lane working tree must hold the tool the row describes.
19. **Do not assume `--worktree` proves blob-at-rev.** In worktree mode every read comes
    from the fixture tree; only `--rev` exercises the `git show` path.
20. **Do not assume the S255 re-open rewrites `opened`.** The round-75 convention fixes
    `opened` at the first-open date; a re-open changes `used-by` (and the search log).
21. **Do not assume renaming the 22 historical `| coverage |` rows breaks the lane.** It
    does not — measured against round-25, round-26, round-53, round-66, round-73/74/75/76.
    But it **is** a rewrite of historical SCORECARD sections; the L1 owns that decision.
22. **Do not assume the census tolerates a dangling `used-by`.** `E11` requires the path to
    exist on disk.

---

## 8. Commands run (all read-only, all reproducible)

```
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD
git -C … log --oneline -8
git -C … show 2cf0b7ff93c698809bed321f7338276a22d6beb9:corpus/SOURCES.md
git -C … show 2cf0b7ff93c698809bed321f7338276a22d6beb9:SKILL.md
git -C … show 2cf0b7ff93c698809bed321f7338276a22d6beb9:SCORECARD.md
git -C … show 2cf0b7ff…:tools/round-84/mutation-closure.py
git -C … ls-tree -r --name-only 2cf0b7ff… -- .ufo/waves/round-85/
git -C … ls-tree -r --name-only 2cf0b7ff… -- .ufo/waves/round-85/l1/scores/
python3 -I -B tools/round-86/record-agreement.py --root . --rev <rev> --json-out <r>
python3 -I -B tools/round-86/record-agreement.py --root . --worktree <fixture> --json-out <r>
python3 -I -B tools/round-86/gate-registry.py  --root . --worktree <fixture> --work <scratch> --json-out <r>
python3 -I -B tools/round-85/predicate-bind.py --selftest
python3 -I -B tools/round-84/mutation-closure.py --selftest
python3 -I -B tools/round-66/coverage-selfcheck.py --root <fixture> --rev <rev> --selfcheck
python3 -I -B tools/round-73/74/75/76/record-audit.py --root <fixture> --rev <rev>
python3 -I -B tools/round-84/freeze-precheck.py --root <fixture> --rev <rev> --container .ufo/waves/round-86/claims.json --expect .ufo/waves/round-86/claims.json=CLEAN
python3 -I -B tools/round-68/registry-conformance.py --root . --rev 2cf0b7ff…
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <fixture-SOURCES.md> --root /home/vgpnk/Projects/shokunin
```

Fixture repos were created with `D=$(mktemp -d …) && git -C "$D" init -q` and every later
call named `-C "$D"` (or `--root "$D"`); `git rev-parse --show-toplevel` was asserted to
equal the fixture dir before any commit. **No commit, push, fetch, checkout, reset, stash,
add or other mutating git/jj command was run against the lane.** The only `git add`/`commit`
calls were inside throwaway `mktemp -d` fixture repos under the scratch dir.

## 9. LIVE VERIFICATION AGAINST THE L1's INTEGRATION COMMIT

The L1 landed `4cc03025e6d4f6f1e00b5e402fcc0180e6e730bc` ("round-86: integrate A2 docstring
repair (R85-5), S305 supersession row and S255 re-open (R85-3), knowledge entry, SKILL
registry rows for predicate-bind and the round-86 counters (R85-2), coverage-map and index
rows") while this recon was being written. **Every finding above is confirmed against that
commit**, and the remaining work is now precisely bounded.

### 9a. Current counter status at `4cc03025e`

```
$ python3 -I -B tools/round-86/record-agreement.py --root . --rev 4cc03025e…
RECORD_AGREEMENT agreed=2/3 mismatches=['A3-receipt-pointer']
  A1-s303-supersede-count True {"declared_count": 7, "declared_ids": ["S079","S080","S083","S090","S092","S119","S123"], "prior_rows": [same 7], "superseding_row": "S305", "url_rows_total": 8}
  A2-docstring-status     True {"code_status": "survived", "conflicting_words": [], "sentence": "an absent declared case scores survived, never a pass)."}
  A3-receipt-pointer     False {"why": "expected exactly one `| coverage |` row, found 23"}

$ python3 -I -B tools/round-86/gate-registry.py --root . --rev 4cc03025e… --work <scratch>
GATE_REGISTRY agreed=5/5 mismatches=[]
```

**C2 (R86-C2) is already GREEN — 5/5.** The L1's registry row satisfies every atom
(G1 `rows: 1`; G2 `observed_selftest_exit: 0`; G3 `observed_exit: 0` matching
`declared_exit: 0`; G4 pin `.ufo/waves/round-85/claims.json` present; G5
`kaidoku-r85` ↔ `tools/round-85/`). No further work is needed for C2.

**A1 and A2 are GREEN.** A1 landed with exactly the seven ids I derived
(`declared_count: 7`, `superseding_row: S305`). A2 landed as
`an absent declared case scores survived, never a pass` — the word `surviv` is present and
`inconclusive`/`killed` are not, which satisfies the stem rule.

**A3 is the only remaining atom**, and it is red for **exactly the reason I predicted**
(F1/F3): the file still holds **23** `| coverage |` rows, and the row still names only the
round-84 receipt.

```
$ git show 4cc03025e:SCORECARD.md | grep '^| coverage |' | head -1
last cell: 85 (self-assessment fraction re-derived at the round-85 record; score unchanged)
receipts named: [('84','coverage-selfcheck.json'), ('76',…), ('75',…), ('68',…), ('67',…)]

$ git ls-tree -r --name-only 4cc03025e -- .ufo/waves/round-86/l1/
(no output — no round-86 receipt committed yet)
```

So A3 needs **both** remaining edits:

- **A3-i** — rename the 22 historical `| coverage |` rows (all outside `## Owned axes`) so
  exactly one remains.
- **A3-ii** — name a round-≥85 receipt in that row's evidence cell and commit it (the
  round-86 directory does not exist yet at HEAD).

### 9b. Verified: A3-i + A3-ii together take C1 to 3/3

Applied to a **full `git checkout` of `4cc03025e`** (not a partial copy), with exactly two
edits — the 22-row rename, and a new `.ufo/waves/round-86/l1/scores/coverage-selfcheck.json`
carrying a 40-hex `rev` plus the row's evidence cell naming it:

```
$ python3 -I -B tools/round-86/record-agreement.py --root <fixture> --rev <fixture-rev>
RECORD_AGREEMENT agreed=3/3 mismatches=[]
  A3-receipt-pointer True {"claim_round": 85,
    "receipt": ".ufo/waves/round-86/l1/scores/coverage-selfcheck.json",
    "receipt_rev": "4cc03025e6d4f6f1e00b5e402fcc0180e6e730bc", "receipt_round": 86}
```

### 9c. The A3 edits break no lane consumer (measured, with a control)

I first got a misleading reading from a **partial** fixture (a `cp -r` subset missing
`LOG.md`/`PROVINCE.md`/…), which showed extra record-audit mismatches. I rebuilt the test as
a full checkout and ran a **zero-edit control** to separate the two effects:

| Audit | control (HEAD, 0 edits) | HEAD + A3-i + A3-ii | delta |
|---|---|---|---|
| `tools/round-73/record-audit.py` | `[]` | `[]` | none |
| `tools/round-74/record-audit.py` | `[]` | `[]` | none |
| `tools/round-75/record-audit.py` | `['D20_grammar_reds']` | `['D20_grammar_reds']` | none |
| `tools/round-76/record-audit.py` | `['D24_capability_rows']` | `['D24_capability_rows']` | none |

**The A3 edits introduce zero new mismatches.** `D20_grammar_reds` and
`D24_capability_rows` are **pre-existing at `4cc03025e`** and are not caused by the rename —
they are the L1's own landing state and are outside this claim's scope.

`tools/round-66/coverage-selfcheck.py --selfcheck` on the same fixture:
`stem: 169/169 missing [] dangling [] mismatches 0`, `recipe_a_hidden_count: 27` — green.

`bash scripts/sources-census.sh validate --file <fixture>/corpus/SOURCES.md --root <fixture>`
→ **0** `E0` findings.

### 9d. ⚠ F4 is live at HEAD — the pin must be re-issued

```
$ python3 -I -B tools/round-84/freeze-precheck.py --root . --rev 4cc03025e… \
    --container .ufo/waves/round-86/claims.json --expect .ufo/waves/round-86/claims.json=CLEAN
"findings": ["COUNTER_PIN_MISMATCH:tools/round-84/mutation-closure.py"], "verdict": "FLAGGED"
```

Exactly the conflict predicted in §2: the A2 docstring repair changed the blob, so the
`loaded_by_counter` / `target_instruments` pins in `.ufo/waves/round-86/claims.json` are stale.
Re-issuing both pins to the new blob digest restores it — verified on the fixture:

```
$ python3 -I -B tools/round-84/freeze-precheck.py --root <fixture> --rev <fixture-rev> \
    --container .ufo/waves/round-83/claims.json --expect .ufo/waves/round-83/claims.json=FLAGGED \
    --container .ufo/waves/round-86/claims.json --expect .ufo/waves/round-86/claims.json=CLEAN
"verdict": "FLAGGED" (round-83, expected) / "findings": [] "verdict": "CLEAN" (round-86)
"met": true, "refused_expected": 1, "accepted_expected": 1
```

**This is the L1's next required step and it is independent of A3** — it can be done in
either order.

### 9e. Remaining work for the L1, itemised

1. **Re-issue the pin** for `tools/round-84/mutation-closure.py` in
   `.ufo/waves/round-86/claims.json` (both `loaded_by_counter` and `target_instruments`)
   to the post-repair blob digest. → unblocks `freeze-precheck` (currently FLAGGED).
2. **A3-i** — rename the 22 historical `| coverage |` rows in `SCORECARD.md` (all outside
   `## Owned axes`). Verified consumer-neutral.
3. **A3-ii** — commit `.ufo/waves/round-86/l1/scores/coverage-selfcheck.json` with a
   40-hex `rev`, and name that path in the surviving `| coverage |` row's evidence cell.
4. Re-run both counters at the measured revision: C1 → `agreed 3/3 mismatches []`,
   C2 → `agreed 5/5 mismatches []` (C2 is already green at `4cc03025e`).

No counter byte, atom rule, plan file, `claims.json` atom text or `.ufo/waves/round-86/pre/`
receipt needs to change for any of this.

---

## 10. Scratch

`/fast/scratch/hyaku/kaidoku-r86/ScoutRecon/` (fixtures `fx/`, `fx2/`, `fxc2/`, `consumer.*`,
`fpc.*`, `rootfx.*`, `root2.*`, `wt2.*`, `exec.*` and the JSON receipts `exp-*.json`) was
deleted after this report was written. Nothing under `/tmp` was used as evidence.
