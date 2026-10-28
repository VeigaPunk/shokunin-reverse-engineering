# R45-W1 — C1 selftest from the freeze, and an attack on both claim predicates

Seat `R45W1C1SelftestFromFreeze`. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`. Run window `2026-10-28T15:38Z`–`2026-10-28T15:42Z`.
Python `3.14.8`. No installs, no upgrades (nothing needed).
Receipts: `.ufo/waves/round-45/w1/R45W1C1SelftestFromFreeze/receipts/` (14 files including `SHA256SUMS`, all verifying);
this file is mirrored at `.ufo/waves/round-45/w1/R45W1C1SelftestFromFreeze.md`. Scratch `/fast/scratch/hyaku/kaidoku-r45/R45W1C1SelftestFromFreeze`, removed after copy.

## Verdict

| item | result |
|---|---|
| three frozen instruments, freeze bytes, `--selftest` | **all exit 0, `failures=0`** |
| frozen outputs vs the freeze's own `controls/*-selftest.txt` | **byte-identical (3/3)** |
| frozen-path diff `FREEZE..HEAD` | **empty** (`diff --stat` lines = 0) |
| worktree vs freeze bytes, 5 frozen files | **5/5 identical** |
| R45-C1 / R45-C2 counters at `1f4b27f8` and at `HEAD` | **exit 0, `met_target true`, `failing []`** |
| S140 / S141 sources re-opened | **HTTP 200, exact recorded byte counts and sha256** |
| predicate clauses defeated by mutation | **6** (C1 c1, C1 c4, C2 c1, C2 c2 ×2 modes, C2 c3) |

The instruments are sound as *executed*: deterministic, self-consistent with their own frozen receipts, and they score the landed tree met at two revisions. The instrument *predicate text* is weaker than the claims file says in six places (below). None of those gaps was exploited by the actual landing — I verified the landed artifact against the text predicate as well as the counter. So this is a hardening list for wave 2, not a wave-1 failure.

## 1. Frozen state at run time

```
head=faa875bc0eb839d15b83c4afa6078819e5a7b381
freeze_first_commit=f762b7273e3f6ca3c710bb37d5de92a4a4417aec   (git log -1 -- plans/round-45-claims.md)
freeze_is_ancestor=yes    commits_freeze_to_head=5

git diff --stat f762b727..HEAD -- tools/round-45/ plans/round-45-claims.md
(no output)
diff_stat_exit=0   diff_stat_lines=0
```

Byte identity, `git show <freeze>:<p> | sha256sum` vs `sha256sum <p>`:

| path | sha256 (freeze = worktree) |
|---|---|
| `tools/round-45/frozen-path-preflight.py` | `633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b` |
| `tools/round-45/c1-counter.py` | `2cfc5a4853585879b0924f4c002ed4581dced02f061068d325c2cd3da130a509` |
| `tools/round-45/c2-counter.py` | `50212d0f456107edb6e36c48b51988ac24ec58b84b16197abe13572d2111b025` |
| `tools/round-45/registry-scope.json` | `6e2dda713a474dd6479a0af1430af9f38013d058a7cf9d2cc3fe293b9bd8dff9` |
| `plans/round-45-claims.md` | `56bacf3143e904ae1c9683c61f0d3f30900257c6fd90d38965d735c7c50b915e` |

Receipt: `receipts/receipts-frozen-state.txt`. `SKILL.md` advanced 5 commits past the freeze, as designed — it is the graded surface and is not frozen.

## 2. `--selftest` from the freeze bytes

Each copy extracted with `git show f762b727:tools/round-45/<f>` into `freeze/`, then
`python3 -I -B <copy> --selftest` with `TMPDIR=$S/tmp`.

| instrument | exit | final line | stdout sha256 | wall |
|---|---|---|---|---|
| `frozen-path-preflight.py` | 0 | `PREFLIGHT_SELFTEST: cases=11 failures=0` | `9f03df6538de49b733ecc71415bbb192a30aa428b82953f4ea064342389ec06c` | 0.244 s |
| `c1-counter.py` | 0 | `C1_SELFTEST: cases=9 failures=0` | `296734f224877a86e8d216bcde5382bbe0f18ff1dadddb1d18099f3754fdac6d` | 0.356 s |
| `c2-counter.py` | 0 | `C2_SELFTEST: cases=7 failures=0` | `aea7e363e5661efcc038df11f2e88380c11815b480d9458f9cc26370b40b0f2d` | 0.168 s |

stderr empty (sha `e3b0c442…` = empty string) on all three. Wall times from a second
timestamped pass; stdout sha identical across both passes, so the instruments are
deterministic here.

**Reproduction of the freeze's own control receipts** — `diff` against
`.ufo/waves/round-45/controls/{preflight,c1,c2}-selftest.txt`:

```
preflight-selftest   frozen=9f03df6538de49b7  mine=9f03df6538de49b7  IDENTICAL
c1-selftest          frozen=296734f224877a86  mine=296734f224877a86  IDENTICAL
c2-selftest          frozen=aea7e363e5661efc  mine=aea7e363e5661efc  IDENTICAL
```

All eleven named red cases are present in the preflight set (touched, restored, dirty,
pathspec-required, unknown-freeze, non-ancestor, bulk-sweep, plus four green arms).

Note on clause 6's `cases >= 11`: the preflight reports **exactly 11**, no margin — losing
any one case drops the claim. That is intended (each case is a required red arm), but it
means a future deletion is a silent claim break unless the case list is pinned elsewhere.

## 3. Counters against the real lane

`python3 -I -B freeze/<c>-counter.py --root <lane> --freeze f762b727 --rev <rev> --json-out …`

| rev | counter | exit | `met_target` | key values |
|---|---|---|---|---|
| `1f4b27f8` | c1 | 0 | true | `rule_blocks 22`, `block22_present 1`, `block22_rows 10`, `block22_refs 7`, `unresolved []`, `cites {S140:true, interpreter:true}`, `preflight_selftest {cases:11, failures:0, ok:true}` |
| `1f4b27f8` | c2 | 0 | true | `scope_size 6`, `registered` = the six scope paths, `unregistered []`, `thin []` |
| `faa875bc` | c1 | 0 | true | same, `failing []` |
| `faa875bc` | c2 | 0 | true | same, `failing []` |

Receipts: `receipts/c1-counter-1f4b27f8.json`, `c2-counter-1f4b27f8.json`,
`c1-counter-faa875bc.json`, `c2-counter-faa875bc.json` (sha256 in `receipts/` directory
listing below). Both claims therefore hold at the measured revision **and** still hold at
the wave-2 spec tip, so nothing landed after the score moved the goalposts.

## 4. Attack on the predicates — 15 mutations

Method: load the **freeze-extracted** counter modules with `importlib`, reuse their own
fixture helpers (`make_repo`, `skill_with`, `good_block`, `GOOD_ROW`, `HEAD`, `good_rows`)
so the mutation is exactly the counter's own idea of a passing surface plus one change, and
run `evaluate` on the fixture repo. Harness: `attack.py` (scratch), results
`receipts/attacks.json`, `receipts/attacks.stdout` (sha `62e542e1e7264430…`).

### Landed (counter exits 0 where the claims text implies a rejection)

| # | mutation | clause | text says | counter |
|---|---|---|---|---|
| A1 | 21 real blocks, one block whose body contains a top-level `- **sub-note**` line | C1 **1** (`rule_blocks == 22`) | 22 rule blocks | **0** — `rule_blocks 22`, counts the split fragment as a block |
| A2 | pass block adds `SKILL.md:99999` and `tools/round-45/does-not-exist.py:7` | C1 **4** ("every `path:line` … resolves") | unresolved ≠ [] | **0** — `block22_refs 4`, `unresolved []` |
| A2′ | same with `corpus/SOURCES.md:9999`, `LOG.md:9999` | C1 **4** | unresolved ≠ [] | **0** (and when forced to be the 4th ref it reports `refs 3 < 4`, never the bad line) |
| A3 | six registry-shaped rows under `## Repository files (not the instrument registry)` | C2 **2** ("some SKILL.md *registry* row") | unregistered = 6 | **0** — all six registered |
| A4 | first cell `` see `tools/round-44/a.py` (legacy) `` | C2 **2** ("first cell is **exactly** that path") | unregistered = 6 | **0** — `re.search`, not equality |
| A5 | scope file with 6 entries, `…/y.py` listed twice | C2 **1** (`scope_size == 6`) | distinct six | **0** — `scope_size 6` |
| A6 | exit cell `mean latency 0.5 / 1.2` | C2 **3** ("names `0`, `1` and `2`") | thin | **0** — `\b0\b`, `\b1\b`, `\b2\b` all hit |

Root causes, exactly:

- **C1 clause 1** — `craft_blocks()` splits the section on `^- \*\*` (MULTILINE), so any
  top-level `- **bold**` line inside a block body manufactures an extra "rule block". The
  count is a formatting proxy, not a rule count. The block's own disclosed limit
  (`SKILL.md:587-589`) covers structurally-valid-but-empty rows; it does **not** cover this.
- **C1 clause 4** — `REF = re.compile(r"((?:corpus/(?:knowledge|lessons)|plans)/[A-Za-z0-9._-]+\.md)(?::(\d+)(?:-(\d+))?)?")`.
  Only `corpus/knowledge/**`, `corpus/lessons/**` and `plans/**.md` are counted or
  validated. `SKILL.md:…`, `tools/…:…`, `LOG.md:…`, `SCORECARD.md:…` and
  `corpus/SOURCES.md:…` are invisible to both the `>= 4` count and the resolution arm —
  even though the block itself cites S140, whose home is `corpus/SOURCES.md`.
- **C2 clause 1** — `len(scope)`, with no `set()`; duplicates inflate the size.
- **C2 clause 2** — `parse_rows()` scans **every** `|` line in `SKILL.md` for a
  `len(cells) >= 3` row whose `cells[0]` `re.search`es a backticked tool path. Heading,
  section and cell fidelity are unconstrained, so "registry row" is not what is measured,
  and "first cell is exactly that path" is not what is tested.
- **C2 clause 3** — `\b0\b`/`\b1\b`/`\b2\b` anywhere in the third cell. Any sentence with
  the digits 0, 1 and 2 passes regardless of whether it states exit semantics.

### Held (counter rejects correctly)

| # | mutation | exit | reason |
|---|---|---|---|
| H1 | every exit cell `0/1/2` | 1 | `exit cells outside {0,1,2}: 8` |
| H2 | exit cell `10` | 1 | same (word-boundary/equality is strict) |
| H3 | two blocks carry the marker | 1 | `block22_present 2 != 1` |
| H4 | 8 rows that are one row repeated | 1 | `block22_rows 1 < 8` |
| H5 | first cell `vendor/tools/round-44/a.py` | 1 | `unregistered` all six — the substring is genuinely absent |
| H6 | exit cell `non-zero means trouble` | 1 | `thin` named |
| H7 | exit cell `latency 0.5s / 1.2s` | 1 | `thin` — incidental: `2` abuts `s`, so `\b2\b` misses |
| H8 | 4th ref replaced by `corpus/SOURCES.md:9999` | 1 | but for the **wrong** reason: `refs 3 < 4`, `unresolved []` |

**Calibration of the campaign:** 6 distinct clauses fall, 7 controls hold, 1 holds for the
wrong reason. The counters are not decorative — the strict arms (exit-cell equality,
marker uniqueness, row count, path-substring, thin-cell) genuinely bite.

### The landing did not exploit any of this

I checked the landed artifact against the **text** predicate, not just the counter:

- Block 22 is real: `SKILL.md:547` `- **22. Freeze integrity is an instrument, and every
  arm has a red case.**`, marker at `:567`, 10 data rows with **10 distinct** triggers
  (`awk`-counted), header `trigger | arm | exit | receipt` at `:568`, exit cells
  `1,1,1,1,2,1,2,2,0,0`, all in `{0,1,2}`.
- It cites `S141` (`:560`, `:570`), `S140` (`:573`) and the interpreter
  `tools/round-45/frozen-path-preflight.py` (`:553`) inside the block.
- Its 7 refs are all `corpus/**`/`plans/**` and all resolve at `--rev`; the two
  refs I spot-read, `corpus/lessons/round-45.md:12-17` and
  `plans/round-45-claims.md:132-147`, exist and say what is claimed.
- C2: six rows at `SKILL.md:1636-1641`, each first cell **exactly** the backticked scope
  path, each third cell carrying `0`/`1`/`2`, all inside `### Round-44/45 instrument
  registry` (`:1623`). Scope file's six paths are distinct.

## 5. Sources opened

Both fetched live this run; **both match the recorded page hash and byte count exactly**.

| id | URL | HTTP | bytes recorded = fetched | sha256 recorded = fetched |
|---|---|---|---|---|
| S140 | `https://git-scm.com/docs/git-status` | 200 | 99,934 | `903e31c527d443ab4051f7b4e0225058efd96a45d0400538f6ba19b5c9c59ad9` |
| S141 | `https://git-scm.com/docs/git-diff-tree` | 200 | 256,810 | `f81c1e3141b2e8e2cfc5790b8923881862f964ae5e3f85c157299b71f80c9640` |

Raw bytes retained: `receipts/git-status.html`, `receipts/git-diff-tree.html`.

Quote verification (HTML stripped, entities unescaped, whitespace collapsed):

- S140, `corpus/lessons/round-45.md:25` — "guaranteed not to change in a
  backwards-incompatible way between Git versions or based on user configuration … ideal
  for parsing by scripts": **both fragments FOUND**, in one paragraph under the
  `Porcelain Format Version 1` anchor, which is also present. The `-z` paragraph is
  present ("Terminate entries with NUL … This implies the `--porcelain=v1` output format").
- S141, `corpus/lessons/round-45.md:26` — "When --raw, --numstat, --name-only or
  --name-status has been given, do not munge pathnames and use NULs as output field
  terminators.": the **second half is verbatim**; the first half is a *whitespace-normalised
  transcription* — the page renders each option in its own `<code>` span, so the raw text
  reads `When --raw , --numstat , --name-only or --name-status has been given`. A
  re-verifier doing exact substring matching on extracted text gets a **miss on the
  sentence as quoted**. Every token is present and the meaning is exactly right; this is a
  transcription convention issue, not a misquote. Recommend quoting it with the span
  spacing elided (`When --raw, --numstat, --name-only or --name-status … do not munge
  pathnames …`) or noting "code-span spacing normalised" alongside the sha.

## 6. Findings, ranked

1. **C1 clause 1 is a formatting count, not a rule count** (A1). Defeats
   `rule_blocks == 22` with 20 real blocks plus one nested bold bullet. Fix: count only
   lines matching `^- \*\*\d+\.` and/or require distinct block numbers `1..22`.
2. **C1 clause 4's citation arm has a narrowed scope** (A2/A2′). The claims text says
   *every* `path:line` resolves; the regex validates only three prefixes. `SKILL.md`,
   `tools/`, `LOG.md`, `SCORECARD.md`, `corpus/SOURCES.md` are unchecked — including the
   home of the very source the block cites. Fix: broaden `REF` to any
   `[A-Za-z0-9._/-]+\.(md|py|sh|json|txt)` and fail on unreadable paths.
3. **C2 clause 2 accepts any table row in `SKILL.md`** (A3) and **a first cell containing
   the path rather than equal to it** (A4). The block's own prose at `SKILL.md:1629`
   ("a row satisfies a scope path only when its first cell is that exact backticked path")
   is **false of the implementation** — a calibration assertion the instrument contradicts.
   Fix: restrict to rows under the registry heading and compare `cells[0].strip("`")`.
4. **C2 clause 1 does not de-duplicate** (A5). Fix: `len(set(scope))` plus a
   `duplicates` field.
5. **C2 clause 3 accepts incidental digits** (A6). A cell reading "mean latency 0.5 / 1.2"
   is "naming 0, 1, 2". Fix: require the tokens as *exit codes*, e.g.
   `{0,1,2} ⊆ set(re.findall(r"(?<![.\d])[012](?![.\d])", cell))` and reject cells with a
   decimal or unit inside the match, or require the cell to be a delimited list.
6. **S141 quote whitespace normalisation** (§5). Documentation nit for `corpus/lessons/round-45.md:26`.

None of 1–5 changes today's score: the landed artifact satisfies the strict reading too.
They matter for wave 2, where the falsification spec must not be satisfiable by formatting.

## 7. Landing-evidence draft (for the L1)

Rows/values the L1 can cite directly, all re-derived this run:

- **Claim C1** — `tools/round-45/c1-counter.py` at `--rev 1f4b27f8…`, exit 0,
  `met_target true`, `failing []`; receipt
  `.ufo/waves/round-45/w1/R45W1C1SelftestFromFreeze/receipts/c1-counter-1f4b27f8.json`
  (sha256 `da9d99b4d1388e8274ef49e0735a38622308b5b411bc344f370ab8df417936de`).
  Still exit 0 at `HEAD faa875bc` (receipt sha256 `427bf895…`).
- **Claim C2** — `c2-counter.py` same pair, exit 0, `met_target true`, `failing []`;
  receipt sha256 `0daf63d3d13068a376af8adce4e37c9830f312d21cdaf2649d98478bf3c0abb9`
  (`1f4b27f8`) and `042ff4dd…` (`HEAD`).
- **Frozen integrity** — diff empty, 5/5 blobs identical, freeze is an ancestor of both
  revs; `receipts/receipts-frozen-state.txt`.
- **Instrument selftests** — three green receipts, byte-identical to the freeze's own
  `controls/*-selftest.txt`; `receipts/*-selftest.stdout`.
- **Sources** — S140/S141 opened, exact hash+size match, quotes located; §5 and
  `receipts/git-*.html`. Suggested SOURCES note for S141: "quote normalises code-span
  spacing; raw page renders `When --raw , --numstat , …`".
- **Registry** — `SKILL.md:1636-1641` verified as six exact-path rows inside
  `### Round-44/45 instrument registry`, exit cells carrying `0`/`1`/`2`.

## 8. Not run / limits

- Did not execute the counters' *live* `frozen_path_changed` arm against the real lane —
  that needs a post-freeze commit touching a frozen path, which the contract forbids me
  from making. The arm is covered by each counter's own selftest (`red-frozen-touched…`,
  exit 2) and by `frozen-path-preflight` case `red-touched`/`red-restored`.
- Did not score C1's `--selftest` red cases from a *mutated copy* of `c1-counter.py` itself
  (self-instrument mutation) — out of scope for this seat; wave 2 can do it.
- No `pacman`/`uv`/`npm` installs were made or needed; no `/tmp` writes (all scratch under
  `$TMPDIR=$S/tmp`, removed).
- Lane tree untouched: only `.ufo/waves/round-45/w1/R45W1C1SelftestFromFreeze/` written.
