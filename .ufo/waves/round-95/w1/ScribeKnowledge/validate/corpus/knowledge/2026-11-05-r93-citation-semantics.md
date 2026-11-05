# A criterion citation that resolves can still mis-state its rule: craft block 31 row 3 cited QUALITY 169 for the intact-input branch, and every resolving counter stayed green (round 93, R93-C2 depth)

source: S318, S317 — UPX 5.2.0 `src/p_unix.cpp` `PackUnix::unpackExtent` (p_unix.cpp:476, bound at :496) and `PackUnix::unpack` (p_unix.cpp:609, bound at :681), and `src/p_lx_elf.cpp` `PackLinuxElf64::unpack` (p_lx_elf.cpp:7755) with its end-of-file trailer check at :8065. S318 is the row this round opens and supersedes S313's over-broad caller wording; S313 is named here as prose context only and is not a citation of this entry.
verified-at: 92a240521bd1bf2213b75d18d9b176a8dafdc67c (checker `tools/round-93/craft-citation-semantic.py`, sha256 `34cf6579d7d0614336add1710912877492c68517331736fa5e4021ffedf05340`; the after-state is measured at the landing commit named in SCORECARD round 93); base `0a2a23da5eb50410a8a0df90c031d9f4fdadb024`.
recheck: 180d, and on any revision of `corpus/QUALITY.md` or `SKILL.md`'s craft section. The counting command and the receipts are named under Measured; the checker's own selftest is `python3 -I -B tools/round-93/craft-citation-semantic.py --selftest --work <scratch>`.

## The miscite

Craft block 31 in `SKILL.md` (`<!-- stop-boundary-refusal-table v1 -->`, the round-91 block) states a stop-boundary tamper is refused, not repaired. Its third table row reads:

> | intact input refused by mistake | `rc 0`, output byte-identical, `upx -t` green (four of four intact carriers) | never refuse an intact input: the refusal follows the packer's verdict, not the geometry | QUALITY 169 |

The **criterion cell** cites `corpus/QUALITY.md` row 169. Row 169 is:

> **Row 169 (a superseding instrument inherits its predecessor's guards and refusal contract, not only its logic).**

Row 169 states guard *inheritance* for a superseding instrument. It says nothing about never refusing an intact input, and it does not contain the phrase the row's own guard column asserts. The citation resolves — the pointer names a real row of a real file — and it mis-states the rule the row asserts. This is defect **D-91-3**, first named by the round-91 non-author spot-check at `corpus/lessons/round-91-verifier-spotcheck.md` §5, line 169:

> **D-91-3 (carried from the lane's own disclosure).** Block 31's third row cites QUALITY 169, but 169 is "a superseding instrument inherits its predecessor's guards and refusal contract" — not "never refuse an intact input".

It was consciously deferred at round 92 (`corpus/lessons/round-92.md` line 47: "**not fixed this round, on purpose.** A correction needs a new craft-block revision or a superseding criterion row, with the frozen-predicate discipline preserved") and stayed on the routed queue (`corpus/lessons/round-92-verifier-spotcheck.md` §6 item 5, line 74). It was also recorded as this round's own mistake M93-a in `corpus/lessons/round-93.md`.

**Observation.** The row 169 text was read directly out of the committed `corpus/QUALITY.md` at base by this seat: the row's full text is quoted above and contains neither "never refuse an intact input" nor "packer's verdict". Its title names "a superseding instrument inherits its predecessor's guards and refusal contract".

## Why every resolving counter missed it

The round-88 depth counter `tools/round-88/depth-blocks.py` and its successors `tools/round-89/depth-blocks-v2.py` and `tools/round-91/depth-blocks-v3.py` resolve a block's citations by **path and shape only**. All three carry the same `PATTERN`:

```
corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?
```

— they read `corpus/knowledge/` entries and check that the cited file and line range exist. The word/backtick floor (`shape()`: `words >= 25`, `spans >= 2`) and the v3 counter's table-shape clause (a header, a separator and at least three body rows) are structural. **No counter ever opens `corpus/QUALITY.md`.** Verified by reading all three instruments: `tools/round-88/depth-blocks.py` mentions "QUALITY" zero times; `tools/round-89/depth-blocks-v2.py` mentions it twice, both in prose (the docstring citing row 157 and the error message "could-not-evaluate: --expect-blocks N is required (QUALITY 157)"); `tools/round-91/depth-blocks-v3.py` mentions it seven times, all in the docstring, in two selftest fixtures (`QUALITY 1`, `QUALITY 2`, `QUALITY 3`), and in one error message. The string `QUALITY.md` occurs **zero** times in all three. No code path reads a criterion row's text.

**Observation:** a miscite inside a criterion cell is therefore invisible to every frozen depth counter, because the criterion cell's content is never read — only the block's citations to `corpus/knowledge/` entries, the block's word count, and its table shape. The defect class is *not* "the counter could not resolve the pointer"; the pointer resolved. The defect class is that resolution was the only thing checked.

This is the same shape as the earlier QUALITY rows that the depth counter already carries: row 175 ("a block-count predicate does not entail the block's shape") and row 180 (the v3 table-shape clause with a prose control). R93-C2 adds the *semantic* dimension: the cited criterion's text must state the rule the row asserts.

## The semantic atom

`tools/round-93/craft-citation-semantic.py` checks one craft block against one frozen manifest. For each manifest row it locates the table row whose first cell contains the frozen `row_snippet`, requires that exactly one such row exists, parses the criterion cell's `QUALITY (\d+)` citation, requires **exactly one** such citation in the cell, opens that row of `corpus/QUALITY.md`, and requires every frozen `keyword` to occur in the row's text. A missing keyword is a failure naming the row and the row number. Three structural atoms also apply: `block_present`, `marker` (the block carries the frozen marker string) and `shape` (at least four table rows, a header of at least four cells, at least three body rows each of at least four cells). The checker exits 1 on an atom failure and 2 when it cannot evaluate (malformed manifest, unknown revision).

The frozen before-manifest `.ufo/waves/round-93/manifests/block31-before.json` names block 31 with the marker `stop-boundary-refusal-table v1` and three rows; the after-manifest `.ufo/waves/round-93/manifests/block32-after.json` names block 32 with the marker `stop-boundary-supersedes-citation v1` and four rows. The keyword atoms are frozen before the data.

### The before measurement

`.ufo/waves/round-93/pre/r93-c2-block31-before.json` — exit 1, `ok: false`, one failing atom:

```
row 'intact input refused by mistake': QUALITY 169 lacks ['never refuse an intact input', "packer's verdict"]
```

The receipt's `checked` array shows the other two rows passing (cited 176, cited 167, `missing_keywords: []`) and the third failing with `cited: 169` and the two named missing keywords. **Re-derived by this seat** at the base revision, byte-identical in substance:

```sh
python3 -I -B tools/round-93/craft-citation-semantic.py --root . \
  --manifest .ufo/waves/round-93/manifests/block31-before.json --block 31 \
  --rev 0a2a23da5eb50410a8a0df90c031d9f4fdadb024 --json-out <receipt>
```

→ exit 1; receipt at `.ufo/waves/round-93/w1/ScribeKnowledge/receipts/r93-c2-block31-before-repro.json`; `failing` is the single string above and `atoms` are `block_present: true`, `marker: true`, `shape: true`.

The checker's own selftest is 10 fixture cases: `python3 -I -B tools/round-93/craft-citation-semantic.py --selftest --work "$S/work/selftest-c2"` → `SELFTEST cases=10 failures=0`, exit 0 (run by this seat at the declaration commit). The cases are `green` (0), `keyword-miss` (1), `cited-row-missing` (1), `row-not-found` (1), `block-missing` (1), `marker-missing` (1), `shape` (1), `no-citation-form` (2), `malformed` (2), `unknown-rev` (2). The `keyword-miss` case is the prose control the claim names: a fixture whose criterion cites a row whose text does not carry the keywords fails the atom.

## The fix: block 32 and QUALITY row 188

**Craft block 32** (`SKILL.md`, marker `stop-boundary-supersedes-citation v1`) is an **append**: block 31 stays as history, never rewritten. It carries a four-row decision table whose criterion column names a criterion that states each rule — QUALITY 176 (fall-through contract), QUALITY 178 (typed refusal + intact branch), QUALITY 184 (the one-green window rule) and QUALITY 188 (the new citation-semantics criterion). Its fourth row is the new class itself:

> | citation resolves but mis-states the rule | row 3 of block 31 cites row 169; row 169 states guard inheritance, not the intact-input branch | a craft row's criterion citation names a criterion whose text states the rule the row asserts, checked by the frozen keyword atoms | QUALITY 188 |

**QUALITY row 188** states the criterion in the lane's own bar:

> **Row 188 (a craft row's criterion citation names a criterion whose text states the rule the row asserts).** A citation that resolves to the right document can still mis-state the rule: craft block 31 row 3 cited QUALITY 169 for the intact-input branch, and row 169 states guard inheritance for superseding instruments — no sentence of it says an intact input must never be refused. Every depth counter that resolved paths stayed green, so the miscite was invisible to the instruments until the round-92 non-author spot-check named it (D-91-3). The semantic atom freezes, per row, the keywords the cited criterion must contain; a wrong citation fails the atom even though the pointer resolves. The fix is a new block (32) whose criterion column cites criteria that state each rule; the misciting block is history, never rewritten.

Row 188 is a **new row**, appended; row 169 is not edited. This is the append-only discipline the lane's corrections rule requires (`corpus/README.md` / `LEARNING.md` "Files the path writes": "Criteria are superseded by new rows that name the row they replace, never rewritten").

### The drafts, validated

The L1's drafts at `.ufo/waves/round-93/l1/drafts/` (`block32-draft.md`, `row188-draft.md`) were applied in this seat's scratch clone and scored with the frozen checker. **The drafts are green on the semantic atom:**

```sh
python3 -I -B tools/round-93/craft-citation-semantic.py --root . \
  --manifest .ufo/waves/round-93/manifests/block32-after.json --block 32 \
  --rev worktree --json-out <receipt>
```

→ exit 0, `ok: true`, `failing: []`, `atoms: {block_present: true, marker: true, shape: true}`, and the `checked` array resolves all four rows (cited 176, 178, 184, 188, each `missing_keywords: []`). Receipt: `.ufo/waves/round-93/w1/ScribeKnowledge/receipts/r93-c2-block32-after-drafts.json`.

Block 31 stays red at the same tree — the before-manifest still fails, exit 1, with the identical atom string (`…/receipts/r93-c2-block31-before-at-drafts.json`), which is the point of appending rather than rewriting.

## Measured

| claim | before | after | receipt |
|---|---|---|---|
| before-manifest on block 31 | exit 1, `ok: false`, atom `row 'intact input refused by mistake': QUALITY 169 lacks ['never refuse an intact input', "packer's verdict"]` | unchanged at the measured revision (block 31 is history) | `.ufo/waves/round-93/pre/r93-c2-block31-before.json`; `…/w1/ScribeKnowledge/receipts/r93-c2-block31-before-repro.json`; `…/receipts/r93-c2-block31-before-at-drafts.json` |
| after-manifest on block 32 | block 32 does not exist at base | exit 0, `ok: true`, `failing: []` on the L1's drafts | `…/w1/ScribeKnowledge/receipts/r93-c2-block32-after-drafts.json` |
| checker's selftest | — | `SELFTEST cases=10 failures=0`, exit 0 | run by this seat; no receipt file is written by `--selftest` |

### Counting command

```sh
python3 -I -B tools/round-93/craft-citation-semantic.py --root . \
  --manifest .ufo/waves/round-93/manifests/block32-after.json --block 32 \
  --rev <measured> --json-out <receipt>
```

Exit 0 means the after-manifest is ok at the measured revision.

## Limits (measured where stated; none is closed here)

1. **The atom is keyword-based, so it can be satisfied by a keyword in the wrong sense.** The checker requires the cited row's text to *contain* each frozen keyword string; it does not parse the row's meaning. A row that contains "never refuse an intact input" only in a sentence that negates it would pass. The frozen keyword atoms are narrow enough that this is not reachable for the four rows measured here (176, 178, 184, 188 each carry the phrase in its asserting sentence), but the check is a containment test, not a semantic proof. This is the honest limit of the instrument's name.
2. **Only the criterion cell is read.** The checker's `row[-1]` is the criterion cell. A row's *guard* cell — the column that actually states the rule in prose — is not read, and a row whose criterion cell is right but whose guard cell mis-states the rule is not caught. The defect D-91-3 was visible in the guard column, not the criterion column; the instrument reads the column where the citation lives.
3. **The check does not cover the whole craft section.** It scores one `--block` per run, so a second miscite in another block would need its own manifest and run. Only block 31 and block 32 were examined here.
4. **The depth counters still do not read QUALITY.** The semantic atom is a separate instrument, not a change to `depth-blocks-v2.py` or `depth-blocks-v3.py`. A block can still be green to the depth counters while its criterion citation mis-states — the depth counters' `unresolved` list is about *citation resolution*, never about citation semantics.
5. **The S318 draft's `unpackExtent` call-site list is incomplete.** The draft at `.ufo/waves/round-93/l1/drafts/s318-draft.md` lists eight call sites in `p_lx_elf.cpp`; `grep -n 'unpackExtent('` over the fetched file (HTTP 200, 373743 bytes, sha256 `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc`) returns **ten**: the draft's eight plus **7102** and **7305**, the `un_shlib_1` header peeks. The draft's prose names `un_shlib_1` as a caller family, so the omission makes the enumeration incomplete rather than the prose false. Reported, not edited — the S318 row is the L1's to land. The same observation is recorded in the companion fresh-pack entry.
6. **Not examined.** This seat did not check craft blocks 1–30 or 33+ for further miscites; did not measure whether any *other* criterion cell in the lane mis-states its rule; did not verify the round-88 counter `tools/round-88/depth-blocks.py` at any revision beyond a worktree run against the L1's drafts (`blocks 32, met_target true, resolved 32`, exit 0); and did not re-run the depth regression counters at the measured revision (they were run against the L1's drafts in the scratch clone, see the report).
