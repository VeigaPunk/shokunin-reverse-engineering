# R38W2C2Rescore — re-score of the frozen R38-C2 counter at the landing commit

**Verdict: DEFECTS FOUND.** The frozen counter's verdict reproduces exactly — at
`REV=0fc6113376a156fddc3ec385386d71c3a4a9f690` it prints `mismatches 0`, `guards_ok true`,
`met_target true`, exit **0**, and the on-disk receipt
`.ufo/waves/round-38/l1/scores/c2-at-0fc61133.json` is reproduced field-for-field. What the landing
does **not** survive is its own provenance: the SCORECARD R38-C2 row and the round-38 lesson cite
`.ufo/waves/round-38/l1/scores/c2-final.json`, which exists at no revision, in no commit and on no
disk; the receipt that does reproduce is **untracked**. Both defects sit exactly in the blind spot
the frozen predicate excludes, so the counter's green is not evidence against them.

Seat `R38W2C2Rescore` (leaf, wave 2). Claim attacked: `plans/round-38-claims.md` R38-C2 / P38-C2 at
the first freeze `e059ca9391642d5b71b6662cabcbdce0d9308719`; counter
`tools/round-38/c2-counter.py`; base `77091b492cc53f8743bd0701b1e7d5e66123dd84`; controls
`efd5c47a72a50b3a434783f82268fb4a96e636a1`. Nothing in the lane was modified; no VCS mutation; no
tool installed or upgraded; scratch removed at exit.

## 1. Instrument identity — the counter bytes are the frozen bytes, everywhere that matters

| revision | `git show <rev>:tools/round-38/c2-counter.py \| sha256sum` |
|---|---|
| `e059ca93` (first freeze) | `7f137b664984595e4d63068a7fa0be2c74a7c57fe5cd5e3a0b794918d2a7b0f7` |
| `3b960fe5` (C1 landing) | `7f137b66…d2a7b0f7` (identical) |
| `0fc61133` (C2 landing) | `7f137b66…d2a7b0f7` (identical) |
| work tree `tools/round-38/c2-counter.py` | `7f137b66…d2a7b0f7` (identical — no uncommitted drift) |
| `77091b49` (base) | absent (`git show` fatal; introducing commit is the freeze `e059ca93`) |

The sha256 both assignments name (`7f137b66…`) holds at the freeze **and** at the landing commit:
the C1/C2 counter was not amended between freeze and landing (the attempt-1 amendments touched the
C1 predicate/counter only, per `plans/round-38-claims.md` C2's "no counter change after this commit").

## 2. Selftest — green on the frozen bytes

```
python3 -I -B tools/round-38/c2-counter.py --selftest
{"selftest": "c2-counter", "cases": 14, "green_ok": 1, "red_ok": 13, "failures": []}   exit 0
```
Run twice (once `TMPDIR`-only, once with `HYAKU_SCRATCH` pinned into my scratch): identical, exit 0.
Fixture repos are the counter's own `mkdtemp` + `git -C "$d" init -q` with a toplevel check before
the first commit; nothing was written outside scratch.

## 3. The scored run at `REV=0fc61133` — reproduced, exit 0

```
python3 -I -B tools/round-38/c2-counter.py --root <lane> \
  --rev 0fc6113376a156fddc3ec385386d71c3a4a9f690 \
  --base 77091b492cc53f8743bd0701b1e7d5e66123dd84 --json-out <OUT>
{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0,
 "revision": "0fc611337…", "unresolved": []}                                     exit 0
```

Full receipt (`artifacts/R38W2C2Rescore/c2-at-0fc61133-repro.json`):

| field | value |
|---|---|
| `mismatches` | **0** |
| `unresolved` | `[]` |
| `assertion_mismatches` | `[]` (**7** assertions evaluated, all match) |
| `guards.missing_units` | `[]` |
| `guards.base_pointers` / `pointers` | 48 → **52** (`pointers_not_fewer: true`) |
| `guards.base_unresolved` | `[["prov_core:REA MCP server", "evidence/doctor/"]]` |
| `guards.unrepaired` | `[]` |
| `guards_ok` / `met_target` | **true / true** |
| `observed.command_a` | `{"knowledge_files": 126, "mapped": 126, "resolved_rules": 17, "rule_blocks": 17}` |
| `observed.command_b` | `[9, 9]` |
| `observed.craft_range` / `adjacent_range` | `[81, 314]` / `[97, 125]` |

**Receipt reproduction:** compared with the receipt on disk
(`.ufo/waves/round-38/l1/scores/c2-at-0fc61133.json`, sha256
`d467d2d6a33bbf58989e6f9c8bc4353734fe530ab2868926c970721634dc88ab`), the JSON is **equal for every
field except `argv`** (my `--json-out` path differs). So yes — the receipt is reproduced.

## 4. Controls and neighbouring revisions (all re-derived, not copied)

| run | exit | numbers |
|---|---|---|
| do-nothing: `--rev base --base base` | **1** | `mismatches 1`, `unresolved [["prov_core:REA MCP server","evidence/doctor/"]]`, `guards_ok false`, `assertion_mismatches []` |
| `--rev e059ca93` (first freeze, repairs not landed) | **1** | same single unresolved pointer as the base |
| `--rev 3b960fe5` (C1/receipts landed, coverage row not re-stated) | **1** | `assertion_mismatches [{"check":"O1 coverage mapped/files","stated":[124,124],"observed":[126,126]}]`, `guards_ok true` |
| `--rev 0fc61133` (the landing) | **0** | `mismatches 0`, `guards_ok true` |
| `--rev e265533e` (current tip) | **0** | `mismatches 0`, `guards_ok true` |
| off-lane: scratch clone, `--rev 0fc61133` | **0** | identical to the lane run except the echoed `base` string (short vs full sha) |

Two calibration consequences, both benign but worth stating: (a) C2 was **not** met at the C1
commit — the coverage row still said 124/124 while 126 files existed — so the "met" verdict exists
only from `0fc61133`, which is exactly the revision the row names ("the commit that lands this
section"); (b) the counter is `git show`-addressed, so an untracked/dirty work tree cannot change
its verdict — proved by re-running against a clone.

The frozen controls `ctl-c2-0…3` are committed receipts
(`.ufo/waves/round-38/controls/ctl-c2-{0,1,2,3}-*.json`), all `exit 1`; `ctl-c2-0`'s embedded
`output` block matches my do-nothing re-run field-for-field. The selftest's 13 red cases are the
frozen control set for the mutate-class attacks (do-nothing, junk count, deleted count, deleted
pointer, substitution by another document, unresolved province pointer kept, box removed, craft
off-by-one, Adjacent wrong, range beyond file, new unresolved pointer, wrong calibration count,
wrong SHONEN count).

## 5. Independent re-derivation (different code path, same numbers)

`artifacts/R38W2C2Rescore/audit.py` re-enumerates the four predicate surfaces from `git show`
without importing the counter and resolves every backticked lane pointer with a tree-aware resolver:

```
C2-scope units                : 52 pointers, 52 resolved, 7 resolved as trees, 0 unresolved
SCORECARD '## Round 38'       : 12 pointers, 10 resolved, 2 unresolved   <- see §6
```

Independent numbers for the seven assertions: 126 knowledge files (my own `ls-tree` count) and —
under the counter's "stem named anywhere in `## Coverage map`" rule, not my stricter read (see note
2 below) — 126 mapped stems; queue-drain rule blocks 17, resolvable
17, zero bad `corpus/knowledge/…:range` citations; obligations 9/9 `aligned` at the row's own
`measured_revision` `c265db9bd3c0883fbaf4487f839559c85a736826`; craft section `SKILL.md:81-314`;
`## Adjacent` `PROVINCE.md:97-125`. Every stated value in SCORECARD/SHONEN equals the observed one,
so the seven assertion checks are genuinely two-sided and not tautological.

Three measure-semantics notes I had to reconcile before I could trust the count (all disclosed,
none a defect of this landing):

1. **Directory pointers.** 7 of the 52 pointers are directories (e.g.
   `.ufo/waves/round-19/evidence/doctor/`, `corpus/evidence/round-36/c1/`). The counter's `exists()`
   uses `git cat-file -e`, which accepts a tree; a blob-only resolver reports those 7 as
   unresolved. The predicate says "path exists", so the counter's reading is the defensible one —
   but a reader who assumes "pointer = file" will over-count failures by 7.
2. **`mapped` is stem-mention, not row binding.** The counter regexes stems inside the whole
   `## Coverage map` section. A backtick-anchored, row-cell-only extraction yields 91 of 126, not
   126 — so 35 stems are "mapped" only via mentions outside a row's first cell. It does not change
   this landing's claim (both round-38 entries do have real rows, `corpus/README.md:91-92`), but the
   proxy is weaker than the wording "mapped" suggests.
3. **Section-range stop rule.** `adjacent_range` stops at the next heading **of any level**, hence
   97-125; a `##`-only stop gives 97-374 because the `### Round-4…`/`### Round-36…` subsections
   follow `## Adjacent`. Stated 97-125 matches the counter's rule, so R3 passes — the predicate's
   "heading-to-last-non-blank-line" is under-specified and the counter is what fixes it.

## 6. DEFECT A — the landing cites a receipt that does not exist (SCORECARD + lesson)

* `SCORECARD.md:3406` (R38-C2 row, "after" cell): "0 mismatches, `guards_ok`, exit 0
  (`.ufo/waves/round-38/l1/scores/c2-final.json`, revision in its `revision` field)".
* `corpus/lessons/round-38.md:11`: "**R38-C2** is measured at the landing commit
  (`.ufo/waves/round-38/l1/scores/c2-final.json`)."

Evidence:
```
git cat-file -t 0fc61133:.ufo/waves/round-38/l1/scores/c2-final.json -> fatal: does not exist
git cat-file -t e265533e:.ufo/waves/round-38/l1/scores/c2-final.json -> fatal: does not exist
find <lane> -name c2-final.json -> ./.ufo/waves/round-36/after/c2-final.json   (round 36 only)
git log --all --oneline -- '*c2-final.json' -> round-36 commits only (018ae628, 6286d38f, …)
git ls-tree -r --name-only 0fc61133 | grep round-38/l1/scores ->
  …/c1-v1-at-3b960fe5.json, …/c1-v3-at-3b960fe5-NOT-THE-RULE.json     (no c2 receipt at all)
```
The predicate is satisfied, but two landed self-assessment surfaces point at a path that never
existed. This is the class the lane already routed as R37-CL1 ("commit every receipt the report
cites; cite only what is committed") and it is invisible to P38-C2 by construction: the predicate
enumerates `## Owned axes`, `## Capabilities`, SHONEN boxes and PROVINCE `## Core`/`## Frontier` —
round sections and lessons are out of scope, as the wave-1 critic's K-series predicted
(`.ufo/waves/round-38/w1/R38CriticClaimsC2.md`). `LOG.md`'s C2 bullet is fine (it says "Final
receipt in `.ufo/waves/round-38/l1/scores/`", a directory that resolves); the pointer audit of the
`## Round 38` section flags only two, and `evidence/doctor/` is a legitimate verbatim quotation of
the base's broken pointer. Lesson audit: 26 pointers, 24 resolve, `c2-final.json` and the quoted
`considerthese/` absence are the two misses.

## 7. DEFECT B — the receipt that does reproduce is untracked

```
git status --porcelain -- .ufo/waves/round-38/l1/scores/
?? .ufo/waves/round-38/l1/scores/c2-at-0fc61133.json
git ls-files .ufo/waves/round-38/l1/scores/  -> only the two c1 receipts
```
So the C2 verdict's only real evidence lives in the working tree and would vanish on a clean
checkout. Combined with §6 this is a provenance defect, not a counter defect: the numbers are true,
the artefacts the landing rests on are not in the repository. (Note for the L1, advisory only:
either commit `c2-at-0fc61133.json` and re-aim the two citations at it, or write/commit the file the
citations already name.)

## 8. What this seat did **not** establish

- Not checked: R38-C1's honest-stop numbers (another seat's lane; I only observed that C2 was red at
  `3b960fe5` for the coverage-count reason above). Not judged: whether the wave-1 critic's K1-K8
  shortcut payloads were *attempted* on this landing — I only verified the landing avoids the four
  concrete ones: at `0fc61133` exactly one `## Core`, one `## Frontier`, one `## Owned axes`, one
  `## Capabilities`, and one occurrence of each audited SHONEN box (`grep -c` = 1 for all six) — no
  shadow-duplicate unit; no forged `evidence/doctor/` basename copy
  (`git cat-file -t 0fc61133:evidence/doctor` fatal; the repair targets
  `.ufo/waves/round-19/evidence/doctor/`, a tree holding `doctor-6.5.0.txt` and `doctor-6.7.0.txt`),
  and `evidence/round-1-2026-10-15/result.json` is **byte-unchanged** base→landing (`git diff --stat`
  empty), so command B was not rewritten.
- `[INFERENCE]` The two `c2-final.json` citations are a naming slip for the receipt the L1 actually
  produced (`c2-at-0fc61133.json`): same round, same directory, same `revision` field, and the
  receipt's numbers are what the row states. I did not ask the L1 and did not repair anything.

## 9. Bounds, tooling, reproduction

- Wrote only this report and `artifacts/R38W2C2Rescore/` (six run receipts, `pointer-audit-at-0fc61133.json`,
  `independent-rederivation.json`, `receipts.txt` with every command/output/exit code, `audit.py`,
  `indep.py`). No writes to `corpus/`, `PROVINCE.md`,
  `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `tools/`, no sibling lane, no `/home/vgpnk/Projects/shokuknow`.
- Read-only git throughout (`show`, `cat-file`, `ls-tree`, `ls-files`, `diff`, `log`, `rev-parse`,
  `merge-base --is-ancestor`, `status --porcelain`) plus one `git clone` **into scratch**. No
  add/commit/checkout/reset/stash/pull/push; no jj.
- Scratch `S=/fast/scratch/hyaku/kaidoku-r38/R38W2C2Rescore` (`TMPDIR`, `HYAKU_SCRATCH`) with
  `trap 'rm -rf -- "$S"' EXIT`; clone, fixtures and receipts all under it; removed at exit.
- No tool installed or upgraded (stock `python3`, system `git`); pacman untouched; REA not invoked —
  this seat's subject is a frozen local counter.
- Exact commands and outputs: `artifacts/R38W2C2Rescore/receipts.txt`; per-run JSON:
  `c2-at-{0fc61133-repro,0fc61133-clone,base-repro,freeze-e059ca93,3b960fe5,HEAD}.json`;
  `pointer-audit-at-0fc61133.json`; `independent-rederivation.json`.
