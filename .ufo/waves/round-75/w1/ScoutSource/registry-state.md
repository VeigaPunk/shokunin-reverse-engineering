# registry-state — the id binding for the two round-75 pages (final state)

Recorded by ScoutSource (leaf scout) on 2026-11-04. The wave wrote the registry while this seat was
reading it, so this receipt keeps the **timeline** and ends at the state it can pin to a revision.
Every statement names the revision it was measured at.

Revisions, in landing order after the freeze `ec149dc4`:

```
bfdf03dd  the lesson, the sourced entry, the registry rows and the two criteria
ad53c1e1  the base receipt binds the runner that executed
4e0329a4  the runner disclosure and the re-taken pre receipts
6864a780  the landing receipts and the four selftest inventories
1f2f7062  the landing record, the tip receipts and the corrected source ledger
b5f4196d  the tip re-runs, the landing controls and the record gate
23893e23  (later tip; SOURCES.md unchanged since 1f2f7062)
```

## 1. The frozen container, and its errata

At the freeze `ec149dc4`, `.ufo/waves/round-75/claims.json:57` read:

```
"sources_rows_opened": "S283 proc_pid_cmdline(5) admitted; S284 environ(7) rejected"
```

and `plans/round-75-claims.md:105-110` said the same in prose, with line 117 "R75-C1 cites S283
through `corpus/knowledge/2026-11-04-r75-a12-case-independence.md`".

At `1f2f7062` the field was **corrected under a declared erratum** (the predicate sentences,
counters and kill rules untouched):

```
"sources_rows_opened": "S284 os.path.commonpath admitted (mined); S285 environ(7) rejected; S283 (re.fullmatch) withdrawn as a duplicate of S143"
"errata": [{"field": "frontier.sources_rows_opened",
            "why": "the planned row ids moved when S283 (re.fullmatch) was withdrawn as a duplicate of the existing S143; ...",
            "recorded": "2026-11-04, round 75 landing"}]
```

## 2. What the registry binds, per revision

| id | at `bfdf03dd` | at `1f2f7062` (= `23893e23`) |
|---|---|---|
| S277 (line 194) | `proc_pid_cmdline(5)`, `man5/proc_pid_cmdline.5.html`, mined (round 73), digest `1fc68168…a91f15`, 7 918 B | unchanged |
| S275 (line 192) | `proc_pid_environ(5)`, mined (round 72) | unchanged |
| S283 | `re.fullmatch`, Python docs | **row withdrawn and deleted** (duplicate of S143, "Python `re` documentation … the exact-match primitive, `re.fullmatch`", line 149) |
| S284 | `os.path.commonpath`, Python docs | same row; becomes the entry's primary source |
| S285 | `environ(7)`, `man7/environ.7.html`, **rejected**, digest `f209ca23…af5455`, 21 810 B | unchanged |

Row count: 189 at base `3c15a156` → **192** at `bfdf03dd` → **191** at `1f2f7062` and after
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`).

`corpus/knowledge/2026-11-04-r75-a12-case-independence.md:3` now opens
`source: S284 — … os.path.commonpath …` and carries the argv half on **S277** (its own sentence: the
argv-as-claim half rests on S277, with S278 for the read gate).

## 3. Live drift that the correction did not reach

`corpus/SOURCES.md:230` (the round-75 search log, unchanged since `bfdf03dd`) still ends its
scope sentence with:

> Identified 2, screened 2, included 1 (**S283**), excluded 1 (**S284**).

At `23893e23` S283 does not exist (withdrawn) and S284 is `os.path.commonpath`; the included page is
**S277** and the excluded page is **S285**. The *substance* of the sentence matches this seat's
independent open exactly (two GETs, 7 918 B and 21 810 B, `grep -c cmdline` on the environ snapshot
→ 0), so this is an id reference-drift only, not a false search claim.

Also still standing in `corpus/lessons/round-75.md`, Gate table:

- S277's located quote is counted "16 words"; whitespace split gives **15**.
- S284's located quote is counted "13 words"; whitespace split gives **12**.
- S143's row reuses the registry's *anchor cell* (`Page fetched 2026-10-28 (HTTP 200, 257,706 bytes,
  sha256 f169ed06…); anchor re.fullmatch(pattern, string, flags=0)`) in the "located quote
  (≤25 words)" column — that is a registry cell, not a source excerpt. The row is honest about
  what it is ("the row's own anchor cell"), but the column then carries no page quote for S143.

All three are inside the ≤25-word limit or are labelling issues, not gate failures.

## 4. Census — closed

| claim | state |
|---|---|
| `.ufo/waves/round-75/l1/census-end.txt` cited by `corpus/lessons/round-75.md:37` | **exists at `1f2f7062`** (23 W04 lines, `kaidoku ok` last line) |
| "191 rows" at the round end | **matches** the tree at `1f2f7062` and after |
| W04 count | 23 at round start (`l1/census-start.txt`) and 23 at the end (the 24th warning seen mid-wave was S283's `re.html` duplicate, withdrawn with the row) |

An earlier read by this seat, at `6864a780`, saw 192 rows, 24 W04 and no `census-end.txt`; the
`1f2f7062` correction closed all three. This receipt records that history rather than restating the
mid-wave numbers as final.

## 5. Commands (all read-only)

```
git -C <lane> log --oneline ec149dc4..HEAD
git -C <lane> show 1f2f7062 -- .ufo/waves/round-75/claims.json
git -C <lane> show 1f2f7062 -- corpus/SOURCES.md
git -C <lane> show HEAD:corpus/SOURCES.md | grep -nE '^\| ?S(275|277|283|284|285) '
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
grep -c W04 .ufo/waves/round-75/l1/census-start.txt .ufo/waves/round-75/l1/census-end.txt
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
```
