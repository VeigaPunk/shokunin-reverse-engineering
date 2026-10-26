# R38CriticSourcedClaim — attack on the C1 sourced-claim link

Seat: critic (leaf). Round 38, wave 1. Lane `kaidoku-shokunin`, lane HEAD `9c9d496b73cf066b02639dc54647934a0ba4297a`,
freeze `e059ca9391642d5b71b6662cabcbdce0d9308719`, base `77091b492cc53f8743bd0701b1e7d5e66123dd84`.

Assignment: falsify the C1 binding *"the entry cites a `SOURCES.md` row opened 2026-10-26 whose used-by
lists the entry"* with the five named decoys, and verify that `S112+` ids are genuinely unused.
Advisory only: **no lane file was changed** except this report and
`.ufo/waves/round-38/w1/artifacts/R38CriticSourcedClaim/`; no VCS mutation; no REA run; no tool
installed; the frozen counter, predicate, carriers and oracle were not edited.

## 0. Instrument and method

- Instrument: `tools/round-38/c1-counter.py`, sha256 `a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8`
  (identical at the freeze `e059ca93` and at HEAD `9c9d496b`; `git log e059ca93..HEAD -- tools/round-38/c1-counter.py` is empty).
- Frozen selftest reproduced on those bytes: `{"cases": 15, "green_ok": 1, "red_ok": 14, "failures": []}`, exit 0
  (`artifacts/R38CriticSourcedClaim/frozen-counter-identity.txt`).
- Method: import the frozen module **unchanged** and drive `measure()` over fixture git repos built exactly the
  way its own selftest builds them (carriers/oracles/xpin/after-receipts from `tools/round-38/selftest/`,
  receipts minted with `tools/round-27/xpin-attribute.mjs`). Only `corpus/SOURCES.md` and the entry's
  `source:` lines vary. **31 fixtures**: 21 synthetic (`drivers/decoys.py`), 6 on the lane's own registry
  bytes from `git show 9c9d496b:corpus/SOURCES.md` (`drivers/decoys2.py`), 4 on the sibling scribe's real
  append block (`drivers/decoys3.py`). Carrier/receipt values are the counter's selftest fixtures; the
  carrier axis is **not** under test here.

## 1. Verdicts — the five assigned decoys

| # | decoy | fixtures | frozen-counter exit | verdict |
|---|---|---|---|---|
| 1 | source row opened **2026-10-25** | `C1` | 1 | **RED — as required** |
| 2 | used-by **lacks the entry** | `C2` | 1 | **RED — as required** |
| 3 | **S1120** substring | `C3` (entry `S1120`, row `S112`), `C4` (row `S1120`, entry `S112`) | 1, 1 | **RED — as required** (tokenizer is boundary-guarded both sides; `C5` with both rows present and entry `S112` → green, correctly) |
| 4 | row **outside the Registry table** | `C6` (synthetic `## Leads`), `C7` (synthetic `## Search log`), `R3` (real registry bytes), `S1` (scribe block after `## Leads`) | **0, 0, 0, 0** | **GREEN — KILL** |
| 5 | used-by lists a **different entry path** | `C8` (`…-other.md`) | 1 | **RED — as required** |
| — | `S112+` unused in the existing registry | `collision-check.txt` | — | **VERIFIED FREE** (see §6) |

Hardening of #5 (all red, all correct): `C9` `…-recursion.md.orig`, `C16` `…-recursion.md.`, `C19`
`./corpus/knowledge/…`, `C20` bare stem without `corpus/knowledge/` prefix. The comparison is exact
list-element equality after `split(',')` + `strip()`, so no prefix/suffix/substring route exists.

## 2. The kill: the counter does not care where the row lives

Frozen code, `c1-counter.py:221-229` — the scan walks **every line of the file**, with no section tracking:

```python
for line in reg.decode().splitlines():
    if not re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', line):
        continue
    c = cells(line)
    if len(c) != 11:
        continue
    used = [u.strip() for u in c[10].split(',')]
    if c[0] in src_ids and c[8] == OPENED and ENTRY in used:
        ok_ids.append(c[0])
```

**Counterexample (real bytes, not a synthetic straw man).** Take the sibling scribe's five-row block
(`.ufo/waves/round-38/w1/artifacts/R38ScribeSOURCES/append-block.md`, ids S112–S116, `opened` 2026-10-26,
`used-by` = the round-38 entry) and place it after `## Leads (unopened)` instead of at the end of the
Registry table:

```
S0 block inside ## Registry   → counter exit 0, sourced true, opened_source_rows [S112,S113,S114,S115,S116]
S1 block after ## Leads       → counter exit 0, sourced true, opened_source_rows [S112,S113,S114,S115,S116]
```

Identical bytes under the lane's own registry contract (`scripts/sources-census.sh validate --file`):

```
S0 (inside Registry):  E12 = 0   (only +1 W04: S112 shares S108's URL, distinct scopes)
S1 (after ## Leads):   E12 = 5   file E12 S112 … S116 row outside Registry section
```

So the two authorities on the same surface disagree: **C1 green, census error.** `E12` is
SOURCES-CONTRACT-v1's own rule (`sources-census.sh:30`), and the frozen claims doc makes a passing
scratch-mirror census a precondition of the append (`plans/round-38-claims.md` §Frontier step). A green
C1 that rests on an out-of-registry row would therefore claim a *registered* source that the registry's
own contract refuses to count — false provenance, not a formatting quibble.

The same route fires in the synthetic fixtures at two independent placements (`C6` `## Leads`, `C7`
`## Search log`). The frozen selftest has **no** placement case, so this surface was never falsified:
the 14 red cases are `do-nothing, K2 receipt missing, wrong handler, gap present, oracle changed,
carriers changed, Core row outside section, row without handler, row absent, frontier note absent,
S1120, opened earlier, used-by lacks entry, coverage-map stem`.

## 3. Three further untested routes (green where the frozen predicate reads as "no")

| fixture | route | counter | note |
|---|---|---|---|
| `C11` (synthetic), `R4` (real bytes), `S2` (**scribe block, entry cites only S115**) | row with `status = rejected`, `opened` 2026-10-26, used-by = entry | **exit 0, sourced true** | the frozen counter never reads the status column: `grep -n 'status' c1-counter.py` matches only the selftest's fixture header. An entry whose only "born-today" source is a **refused** document scores green. This is exactly the shape the round's own Gate produces (S105, S100, S028 are retained rejections; the scribe drafts S115 as the 7-Zip rejection *with* the entry in used-by) |
| `C13` | two rows share id `S112`; one opened 10-25 with another entry, one 10-26 with the entry | exit 0 | duplicate-id acceptance; census `E03` would flag it, the counter cannot |
| `C17` | entry's `source:` line appears **only inside a fenced code block** (e.g. quoting the format) | exit 0 | lowest severity of the three, but it means "cites" is satisfied by didactic text |

## 4. Honest routes verified green (the target is reachable)

| fixture | edit | counter |
|---|---|---|
| `R0` | registry unchanged, entry cites S108 (opened 2026-10-26, `mined`, used-by = the round-36 entry) | exit 1 — the `used-by` append is required |
| `R1` | S108's `used-by` += the round-38 entry | exit 0, `sourced` true |
| `R2` | new `S112` row at the end of the Registry table | exit 0, `sourced` true |
| `S0` | the scribe's real S112–S116 block appended in the Registry table | exit 0, all five rows qualify; census: 0 E01–E12, 1 new W04 |

Note the interaction with §3: the scribe's block keeps the entry path in **both** a `mined` row (S112) and
the `rejected` S115 row, so a *citation list* is fine; the exposure is only if the entry's `source:` lines
rest on a rejected row alone (`S2`).

## 5. False-red conventions the honest path must respect

All of these are red under the frozen counter and are avoidable formatting, not defects: backticked
used-by path (`C10`), `Source:` capitalised (`C14`), 12-cell row (`C15`), 4-space-indented row (`C12`),
trailing period (`C16`), `./` prefix (`C19`), bare stem (`C20`). The real registry's convention is
unbackticked, comma-separated, full relative paths, and the scribe's block complies.

## 6. `S112+` collision check (as assigned)

Command shape (0–3 leading spaces, the round-35/36 guard):
`grep -oE '^ {0,3}\| *S[0-9]{3,} *\|' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -u`

| check | result |
|---|---|
| registry ids | **111**, range `S001`…`S111`, **0 duplicates**, **0 gaps** in S001–S111 |
| registry ids ≥ `S112` | **0** |
| `comm -12` registry × probe `S112`…`S130` | **0 collisions** |
| all 111 registry rows sit inside `## Registry` | yes (no row anywhere else in the file) |

Namespace caveat (read-only `shokuknow/merge/kaidoku/SOURCES.append.md`): the staged package holds **132**
ids `S106`…`S237`, **126** of them ≥ `S112`, so `S112` is *not* free in the staged namespace. Verbatim
copy cannot satisfy the frozen binding anyway: staged `opened` values are `2026-10-23` (51) and
`2026-10-24` (78) — **none is 2026-10-26** — and 44/132 staged rows do not have 11 cells (35×12, 9×13;
3 rows even carry `mined` in the `opened` slot). Renumber by document, as S110/S111 already did.
Lane-prose collision to avoid: `corpus/lessons/round-35.md:21` and `round-36.md:48` already use **S113**
for the adb reference and S117/S125/S129/S136/S147/S150/S184/S186 for staged documents — adopting those
staged ids verbatim would give two documents the same lane id in reviewable text.

## 7. Boundary condition: the frozen instrument and claims doc are being rewritten in the worktree

Observed passively, no edits by me. Two surfaces drifted after the freeze:

**(a) `tools/round-38/c1-counter.py`** — three snapshots:

| time | sha256 of the worktree copy | state |
|---|---|---|
| first attack run | `f27f982bb4c8dbedb8b7ef1bcadad3bd02df8d2fb7af6a7f78a43ce3093e83fa` | `SyntaxError: expected 'except' or 'finally' block` (line 173) — the counter was unrunnable |
| `2026-10-26T03:2x` | `733be0168527fec193f70441752ef561e1f402789e6b67fd280547357a312967` | own selftest dies: `UnboundLocalError: … 'be_before'` |
| `2026-10-26T03:26:27-03:00` | `1b6a8d1064767164290375ce1d2819f69a9748818bcd8bb3c88feef9b51facd8` | 36+/21− vs HEAD |

The uncommitted diff changes the **predicate sentence itself** (drops "stock unblob 26.6.4; no external
extractor dependency", requires `sasquatch-v4be` available, adds a paired before-receipt that must publish
none of them and name `squashfs-v4be` as a missing dependency) and adds a before/after arm in `measure()`.

**(b) `plans/round-38-claims.md`** — worktree `320f2f081d311a702409e0459bbd66d6d887d0775a554ba3279dd19a12c6f767`
vs HEAD `13ea8eba917f487e0b1e876d2846f77c0c259dd0ba6066d31906284608109815` (48+/35−). The draft titles
itself "frozen claims (freeze v2)" and discloses the reason (wave-1 measurement refutes the v1
"no external extractor dependency" premise; v1 probes filtered PATH *component names* instead of stripping
`~/.local/bin`). It is a self-described **pre-scoring amendment**, and no claim has been scored under v1.

Relevant to this seat, the v2 draft: keeps the sourced sentence **verbatim** (`…cites a SOURCES.md row
opened 2026-10-26 whose used-by lists that entry`, only re-wrapped); raises the C1 selftest to 18 cases but
adds only before-arm cases (`missing before/after receipt`, `after carrying the dependency gap`, `before
without the gap`, `before := after`) — **no placement case, no rejected-status case, no duplicate-id case,
no fenced-citation case**. Every finding in §2 and §3 therefore survives v2 as drafted.

**None of this moves a verdict in this report.** No hunk of either captured diff touches the sourced block
(`grep -E '^[-+].*(src_ids|OPENED|ENTRY in used)'` over the counter diff is empty), and every verdict above
was produced with the frozen bytes `a7a62b…` restored from git into scratch. The drift is reported because
(a) a green/reject verdict must name the bytes it used, (b) if v2 lands, the sourced battery should be
re-run against the v2 bytes (`drivers/decoys.py` takes `C1_COUNTER` for exactly this), and (c) peer report
`w1/R38ExecAfterK1.md:119-121` already records the worktree/freeze divergence.

## 8. Impacted axes

- **coverage (C1).** The sourced binding is satisfiable on the drafted block (`S0`, `R1`, `R2`), so the
  target is reachable as far as this link goes. But the binding cannot distinguish a registered row from
  an out-of-registry one (§2) and cannot distinguish an admitted source from a refused one (§3); a green
  C1 built on either would overstate coverage.
- **calibration (the instrument's own claim).** The frozen selftest's 14 red cases are exactly as the
  claims doc lists them, but the sourced predicate is **weaker than the lane's own SOURCES-CONTRACT-v1**:
  placement, status, duplicate-id and fenced-citation are untested. That gap should be disclosed against
  the successor counter (R36-CL3/CL5 style), not repaired post-freeze.

## 9. Smallest safe corrections (advisory; nothing in the lane was edited)

1. **Land the five rows at the end of the `## Registry` table** (as the scribe block is written), never
   after `## Paths` / `## Leads` / under a `##`-level heading. Verified green at `S0`, census-clean.
2. **Do not let the C1 entry's only born-today `source:` line be the `rejected` S115 row** — cite a
   `mined` row (S112 or S116) as well. The counter would not notice; the reader and the Gate would.
3. **Name the instrument bytes in the claim receipt** (`a7a62b…`), since the worktree copy diverges (§7).
4. **Record the four untested routes** (placement, rejected status, duplicate id, fenced citation) in the
   round's lesson as disclosed blind spots of P38-C1's sourced binding for the successor counter. The v2
   draft's 18-case selftest does not add any of them (§7); closing them by editing the frozen counter this
   round would break the freeze clause.
5. **Renumber, don't copy, staged rows**; `S112` is free in the registry and already used by a different
   document in the staged package (§6).

## 10. Limits

- 31 fixtures with the counter's own selftest carriers/receipts; no REA run, no relation to the carrier
  axis (`carriers_matched` is 4 in every fixture by construction).
- I did not adjudicate the before-arm question (§7); a peer seat measures it.
- The census `validate --file` runs used a scratch mirror, so every run reports `E11` mirror artefacts
  (used-by paths absent relative to the mirror). `E12` presence/absence is the discriminating signal and is
  taken from the same command. The real-lane `validate --root … kaidoku` run is clean (exit 0, 9× W04).
- [INFERENCE] Re-dating an old row's `opened` cell to 2026-10-26 and appending the entry would also satisfy
  the binding (code path identical to `R1`, only the date cell differs); not separately fixture-run.

## Artifacts and reproduction

`artifacts/R38CriticSourcedClaim/`: `decoy-results.json` (21), `decoy2-results.json` (6),
`decoy3-results.json` (4), `drivers/decoys{,2,3}.py`, `frozen-counter-identity.txt`,
`counter-worktree-drift.diff`, `counter-worktree-drift-latest.diff`, `counter-drift-snapshot2.txt`,
`claims-doc-drift.txt`, `collision-check.txt`, `census-receipts.txt`, `staged-package-shape.txt`.

```bash
S=/fast/scratch/hyaku/kaidoku-r38/R38CriticSourcedClaim; mkdir -p "$S"
export HYAKU_SCRATCH="$S" TMPDIR="$S"
git -C <lane> show e059ca93:tools/round-38/c1-counter.py > "$S/fz/tools/round-38/c1-counter.py"   # + selftest/ and ../round-27/xpin-attribute.mjs
export C1_COUNTER="$S/fz/tools/round-38/c1-counter.py"
python3 -I -B artifacts/R38CriticSourcedClaim/drivers/decoys.py    # 21 fixtures
python3 -I -B artifacts/R38CriticSourcedClaim/drivers/decoys2.py   # 6 on the real registry bytes
python3 -I -B artifacts/R38CriticSourcedClaim/drivers/decoys3.py   # 4 on the scribe block
```

Tooling: nothing installed; no `pacman`, no `uv`, no `npx` beyond the pre-existing rea-agents 6.5.0 path
(passed as `--pkg65`, never executed as a campaign tool). Scratch removed at exit.
