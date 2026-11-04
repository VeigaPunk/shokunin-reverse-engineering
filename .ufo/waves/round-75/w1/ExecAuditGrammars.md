# ExecAuditGrammars — round 75, wave 1

Seat: ExecAuditGrammars (executor, leaf). Target: `tools/round-75/record-audit.py`
(read-only) and `.ufo/waves/round-75/w1/ExecAuditGrammars/`.

## Assignment

Attack the four strengthened grammars (D9′–D12′) with COSMETIC fixtures that a
token-presence predicate would accept, and show the exact grammar rejects each.
Call the parsers directly in-process (module import) AND through the committed
`--selftest` case names. Probe two ACCEPT fixtures to show the grammar is not
rejecting everything. Any cosmetic fixture that passes is a BLOCKING defect.

## Method

- Instrument `tools/round-75/record-audit.py` imported in-process via
  `importlib.util.spec_from_file_location`; parsers `parse_used_by`,
  `parse_search_note`, `parse_rejected_row`, `parse_census_erratum` called
  directly. No lane file modified (receipt records
  `instrument_sha256 = bba8b8cd0e724b19083a90a567c80c239a78410dad9bb78bfe4025b5e4e5bb6e`,
  lane HEAD at run `98825979922eafea5aa49322761a43dd0e6ddd16`).
- Committed selftest executed as `python3 -I -B tools/round-75/record-audit.py
  --selftest` from the lane root: exit 0, 10 cases, `failures: []`; every
  committed case covering a fixture family is green.
- Driver ran in the seat scratch dir `/fast/scratch/hyaku/kaidoku-r75/ExecAuditGrammars/`
  (deleted on exit); the receipt was written first to this w1 seat dir.

## Results

### Cosmetic fixtures (must each return ≥1 defect naming the failed shape)

| # | Fixture input | Token-presence predicate accepts because… | Exact-grammar defects |
|---|---------------|--------------------------------------------|-----------------------|
| 1 | used-by cell: `corpus/knowledge/x.md, not corpus/knowledge/y.md` | both comma tokens are `corpus/knowledge` paths | `negated path token: not corpus/knowledge/y.md` (affirmative first token kept) |
| 2 | used-by cell: `x.md` | a `.md` token is present | `token is not an exact corpus path: x.md`; `no affirmative path token` |
| 3 | search note: `round 75 Question: Where searched: Identified screened included excluded Stop: no candidates kept` | names `round 75`, `Question:`, `Where searched:`, all four field words, `Stop:` | `missing integer count: Identified/screened/included/excluded` (all four) |
| 4a | teaches cell: `REJECTED: short` (status `rejected`, 11 cells) | carries `REJECTED:` plus a reason token | `teaches does not carry REJECTED: <reason>; flip: <condition>` |
| 4b | teaches cell: `REJECTED: short; flip: never` | carries `REJECTED:`, a reason, and a `flip:` clause | `rejection reason is fewer than three words`; `flip condition is fewer than three words` |
| 5 | `census erratum: W04 lines 23 and 24 rows`, measured row count 25 | names W04, a lines clause, and row counts | `erratum does not name the measured 25 rows` (numbers present are 23, 24; 25 absent) |

All six cosmetic fixtures are REJECTED by the exact grammar, each with at least
one defect naming the failed shape. Zero cosmetic passes → **no blocking
defect**.

### Accept fixtures (must each return no defects)

| # | Fixture input | Defects |
|---|---------------|---------|
| A1 | well-formed used-by cell: `corpus/knowledge/x.md, corpus/lessons/round-1.md` | none (both paths kept) |
| A2 | complete rejected row: `REJECTED: a real reason here; flip: when the page carries it` | none |

Both accepts are clean — the grammar is exact, not indiscriminate.

## Committed `--selftest` corroboration

`python3 -I -B tools/round-75/record-audit.py --selftest` → exit 0, 10 cases,
`failures: []`. Case names: `d9-negated-path-red`, `d9-token-grammar-red`,
`d10-token-only-red`, `d11-empty-flip-red`, `d12-reversed-values-red` (the red
arms matching fixture families 1–5), `d9-exact-path-accepts`,
`d10-counts-required-red`, `d11-complete-accepts`, `d12-bound-values-accepts`,
`receipt-defects-red`. Every fixture family's covering committed case is green
in the same receipt, so the in-process results and the committed selftest agree.

## Acceptance verdict

- Each cosmetic fixture returns ≥1 defect with a reason naming the failed
  shape: PASS (6/6).
- Each accept fixture returns none: PASS (2/2).
- Cosmetic fixture that passes would be a BLOCKING defect: none occurred
  (`summary.blocking_defects: []`).

Receipt: `.ufo/waves/round-75/w1/ExecAuditGrammars/receipt.json` (`ok: true`).

## Risks

- The attack covers the five assignment-shaped cosmetics plus the two named
  accepts; it does not mutate the instrument, so later waves re-running the
  committed selftest reproduce these arms unchanged.
- No environment values were written anywhere (key-shape discipline kept; the
  driver only read the instrument bytes and the receipt path).
