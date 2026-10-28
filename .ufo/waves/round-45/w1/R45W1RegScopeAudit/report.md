# R45W1RegScopeAudit — registry-scope vs the two claim files

Seat: scout, read-only. Freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`. No frozen path was edited. No package was installed. `tools/round-45/c2-counter.py` was **not run**.

## Question

Is `tools/round-45/registry-scope.json` (six paths) honestly "the instruments the two frozen claim files name"?

## Axes

1. Path coverage: every `tools/round-N/...` string in the two claim blobs.
2. Class: instrument (program that carries a 0/1/2 verdict) vs data/fixture vs helper.
3. Description honesty: scope `paths` vs that classification, without treating the scope list inside round-45 as independent evidence of itself.

## Blobs (freeze, not HEAD)

HEAD at audit was `faa875bc0eb839d15b83c4afa6078819e5a7b381`. Freeze is an ancestor (`git merge-base --is-ancestor`, exit 0). These three paths are byte-identical to the freeze.

Command: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --exit-code f762b7273e3f6ca3c710bb37d5de92a4a4417aec -- plans/round-44-claims.md plans/round-45-claims.md tools/round-45/registry-scope.json`

Exit: 0. Stdout: empty. UTC: 2026-10-28T15:41:00Z (same invocation as the ls-tree receipt).

| path | blob at freeze |
|---|---|
| `plans/round-44-claims.md` | `db6e066499312dac0f7bad1a2dd2a9fb6a94d6d4` |
| `plans/round-45-claims.md` | `f93df4c3bd4069a0cd576d9649f1157609b6a5d5` |
| `tools/round-45/registry-scope.json` | `4855e97e497e329737f00076bdf686bf71b0827d` |

Scope file text (working tree = freeze blob):

- `scope`: "the instruments named as instruments by the round-44 and round-45 frozen claim files"
- `paths`: the six listed below
- `why`: claims round-44 names `c1-counter.py`, `c1-run.sh`, `c2-counter.py`, and round-45 names `frozen-path-preflight.py`, `c1-counter.py`, `c2-counter.py`

`plans/round-45-claims.md:91-100` repeats that same six and calls it "the instrument set named by" the two claim files. That block is the scope file restated. It is not a second witness.

## Classifier

**Instrument** = a program the claim names by a `tools/round-N/...` path, whose own contract exits 0 met / 1 not-met / 2 could-not-evaluate. Git mode `100755` is evidence, not the definition (`tools/round-42/c1-counter.py` is mode `100644` and is still a counter).

**Data/fixture** = JSON, planted trees, or a directory/glob freeze, with no verdict of its own.

**Helper** = a named program that does not emit a claim met/not-met verdict.

Round-44 claims contains the word `instrument` **zero** times (`grep instrument plans/round-44-claims.md`, no matches). Round-45 is the only file that uses the word.

## Every `tools/round-N/...` path the claim files name

### `plans/round-44-claims.md` at the freeze

| path | lines | class | in scope? |
|---|---|---|---|
| `tools/round-43/c1-counter.py` | 28, 121, 308 | **instrument** (R43-C1 counter: exit 0 target met, 1 not met, 2 unevaluable, file lines 99-102). Claim label: "Freeze-walk port source" and "audit-only port sources". Mode `100755`. | **no** |
| `tools/round-42/c1-counter.py` | 120, 308 | **instrument** (R42-C1 counter: "Exit: 0 target met, 1 target not met, 2 unevaluable", file lines 366-367). Claim label: "a port of" and "audit-only port sources". Mode `100644`. | **no** |
| `tools/round-27/xpin-attribute.mjs` | 55 | **helper**, not a claim instrument. Header: exit 0 success, 2 unreadable input; no exit 1. Attributes an evidence id. Mode `100755`. | no (correct under this class) |
| `tools/round-44/` | 56, 83, 241, 277, 307 | directory freeze pathspec, not a file instrument | n/a |
| `tools/round-44/carriers.json` | 105 | data (carrier pins) | no (correct) |
| `tools/round-44/c1-counter.py` | 120, 159 | **instrument**. Predicate P44-C1. File: "Exit: 0 target met, 1 target not met, 2 unevaluable" (lines 213-214). Mode `100755`. | yes |
| `tools/round-44/c1-run.sh` | 161-162 | **instrument of the data procedure, not of the predicate**. Claim calls it "Data procedure". Script lines 30-31: exit 0 every carrier produced a receipt, 1 at least one failed, 2 could-not-evaluate. It `exec`s `c1-run.py`. Mode `100755`. | yes |
| `tools/round-44/control-fixtures/c1/` | 169 | fixture | no (correct) |
| `tools/round-44/control-fixtures/c2/` | 170 | fixture | no (correct) |
| `tools/round-44/control-fixtures/c3/` | 172 | fixture | no (correct) |
| `tools/round-44/control-fixtures/c4/` | 174 | fixture | no (correct) |
| `tools/round-44/c2-counter.py` | 249 | **instrument**. Predicate P44-C2. File lines 20-23: exit 0 iff mismatches == 0, 1 on a mismatch, 2 could-not-evaluate. Mode `100755`. | yes |
| `tools/round-44/c2-rubric.json` | 255 | data. The counter runs it. Its 80 checks are inline `python3 -c` (`check_contract.script_pinning`); they are not separate `tools/round-N` files. | no (correct) |
| `tools/round-42/fixtures.json` | 307 | data | no (correct) |
| `tools/round-44/control-fixtures/**` | 311 | fixture glob (covers `c5/` and `pos/`, which the claim does not name individually) | no (correct) |

Bare names in the same amendment sentence (lines 55-56), **not** written as `tools/round-N/...`, so not in the path census: `rea-pkg.json`, `prior-pins.json`. The parenthetical "vendored into tools/round-44/" is attached to `xpin-attribute.mjs`. At the freeze, `git ls-tree -r --name-only f762b727 -- tools/round-44 | grep -c xpin` printed `0`. `tools/round-44/` also has no `rea-pkg.json` and no `prior-pins.json`. The counter looks for `tools/round-44/rea-pkg.json` then falls back to `tools/round-42/rea-pkg.json` (`c1-counter.py` lines 261-263). That is a claim-text vs tree gap, not a scope-path class.

### `plans/round-45-claims.md` at the freeze

| path | lines | class | in scope? |
|---|---|---|---|
| `tools/round-45/` | 7, 11, 135 | directory freeze pathspec | n/a |
| `tools/round-45` | 136 (`--freeze-path`) | same directory | n/a |
| `tools/round-45/frozen-path-preflight.py` | 22, 32, 54, and 98 (the scope restatement) | **instrument**. File lines 22-23: "Exit codes: 0 clean; 1 violation; 2 could-not-evaluate". Line 32 calls it "the only instrument" of the *prior* freeze-integrity gate, not of the whole round. Mode `100755`. | yes |
| `tools/round-45/c1-counter.py` | 46, 65, and 99 (restatement) | **instrument**. File lines 13-14: 0 met, 1 not met, 2 could-not-evaluate. | yes |
| `tools/round-45/c2-counter.py` | 102, 116, and 100 (restatement) | **instrument**. File lines 11-12: 0 met, 1 not met, 2 could-not-evaluate. It trusts `registry-scope.json`; it does not re-parse the claim files. | yes |
| `tools/round-45/registry-scope.json` | 91 | data (this file) | no (correct) |
| `tools/round-44/c1-counter.py` | 95 (restatement only) | instrument; also named operationally by round-44 | yes |
| `tools/round-44/c1-run.sh` | 96 (restatement only) | data-procedure instrument; also named by round-44 line 162 | yes |
| `tools/round-44/c2-counter.py` | 97 (restatement only) | instrument; also named by round-44 line 249 | yes |

## (a) Instruments named by either claim file that the scope omits

Two:

1. `tools/round-42/c1-counter.py` — named at round-44 lines 120 and 308. Carries the R42-C1 verdict (0/1/2). Scope omits it.
2. `tools/round-43/c1-counter.py` — named at round-44 lines 28, 121, and 308. Carries the R43-C1 verdict (0/1/2). Scope omits it.

Round-44's own label for both, line 308, is "audit-only port sources". They do not score R44-C1, R44-C2, R45-C1, or R45-C2. Under a "claim-carrying scorer of these two rounds" reading they are out on purpose. Under the assignment's binary (named path + program + carries a verdict) they are omitted instruments. Both readings are in the text; the scope file's `why` uses the narrower one and does not mention these two paths.

Not (a), recorded so they are not mistaken for omissions:

- `tools/round-27/xpin-attribute.mjs` is named and is mode `100755`, but it has no not-met exit. Helper.
- Data/fixture paths above are named and correctly absent from `paths`.
- These programs exist under `tools/round-44/` at the freeze (mode `100755`) and are **not named** by either claim file, so they are not (a): `c1-controls.py`, `c1-oracle.py`, `c1-run.py` (the process `c1-run.sh` execs; its lines 85-90 are the 0/1/2 the shell documents), `c2-controls.py`. `c1-oracle.py`'s full exit contract was not read; it is an oracle builder with a `--selftest`, not a named path.

## (b) Scope paths not named by a claim file

None. Each of the six is a path string in at least one claim file, and each is also named outside round-45's self-restatement at lines 95-100:

| scope path | named outside the six-item list |
|---|---|
| `tools/round-44/c1-counter.py` | round-44 lines 120, 159 |
| `tools/round-44/c1-run.sh` | round-44 line 162 |
| `tools/round-44/c2-counter.py` | round-44 line 249 |
| `tools/round-45/frozen-path-preflight.py` | round-45 lines 22, 32, 54 |
| `tools/round-45/c1-counter.py` | round-45 lines 46, 65 |
| `tools/round-45/c2-counter.py` | round-45 lines 102, 116 |

## (c) Is the six-path scope honestly "the instruments the two frozen claim files name"?

**No, not as an exhaustive extraction. Yes, as the set round-45 stipulates.**

- The six paths are exactly the list `plans/round-45-claims.md:95-100` and `registry-scope.json` `paths`. Those two texts cannot disagree; they were written as one list. Every scope path is named by a claim file ((b) is empty).
- The scope string "named **as instruments** by the round-44 **and** round-45" claim files over-attributes the word. Round-44 never says "instrument". Only round-45 does, and it does so by declaring this same six.
- The `why` sentence is true and incomplete. Round-44 does name those three round-44 programs. It also names `tools/round-42/c1-counter.py` and `tools/round-43/c1-counter.py`, which are counters. The sentence does not say "only", but "the whole claim-carrying instrument set" is the claim being audited, and those two names are the hole in an exhaustive reading.
- `c1-run.sh` is inside the six. Round-44 does not call it an instrument; it calls it the data procedure. It does carry 0/1/2 for "receipts produced", which is not P44-C1 (`c1-counter.py` is). Including it matches round-45's list and is wider than "predicate counters only". The unnamed body is `c1-run.py`.
- Data the claims name (`carriers.json`, `c2-rubric.json`, `control-fixtures/**`, `fixtures.json`, `registry-scope.json`, the two directory pathspecs) is correctly not in `paths`.

Nothing here is a proposal to edit the frozen file.

## Not run

- `tools/round-45/c2-counter.py` (the counter that consumes this scope). Not this question.
- Full exit-path read of `tools/round-44/c1-oracle.py`.

## Receipt

`ls-tree` of `tools/round-27/xpin-attribute.mjs`, `tools/round-44`, `tools/round-45` at the freeze.

- Command: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-tree -r f762b7273e3f6ca3c710bb37d5de92a4a4417aec -- tools/round-27/xpin-attribute.mjs tools/round-44 tools/round-45` (wrapped with a utc header; see the file)
- Exit: 0
- Stdout sha256 (file including the utc header line): `9361d5fecbfa39988329eb0936ffb2f6d88990dc128f56ad9c3daacd70c56507`
- UTC: `2026-10-28T15:41:00Z`
- Copy: `.ufo/waves/round-45/w1/R45W1RegScopeAudit/ls-tree.txt`
- Scratch `/fast/scratch/hyaku/kaidoku-r45/R45W1RegScopeAudit` removed after the copy.

## Confidence

High on the path inventory and on (b). High that the two omitted counters carry 0/1/2 verdicts and that round-44 labels them audit-only port sources. The (c) split (exhaustive vs stipulated) is the reading of those two wordings; it is not a guess about author intent beyond the files.
