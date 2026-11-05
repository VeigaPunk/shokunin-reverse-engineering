# CriticC2 — attacks on R95-C2 (depth, craft block 34)

Frozen at 4bda1d1dd3788973f10e61212b70df18b3b14ea0. Checker `tools/round-93/craft-citation-semantic.py` sha256 34cf6579…05340 (pinned, matched); `tools/round-89/depth-blocks-v2.py` 359f15e1…dcf18f (matched); `tools/round-91/depth-blocks-v3.py` bcf6c4ea…aeb052f (matched); `block34-after.json` cf5f265f…03ba8 (matched); `block34-junk.json` abcf7bda…a321 (matched).

Columns: `after` = frozen manifest block34-after.json on the stub; `junk` = frozen manifest block34-junk.json; `v2` / `v3` = depth-blocks-v2 / v3 with `--expect-blocks 34` (v3 also `--shape-from 34`). Exit codes are the process exit codes. Runs were `--worktree` in the clone and `--root <variant>` for the variants; A1 and A2 were repeated with `--rev` on committed stubs (rows A9).

Stub: block 34 (marker `receipt-world-binding v1`, four rows named by the frozen snippets, criterion cells `QUALITY 191` / `QUALITY 192`, `Refs: corpus/knowledge/2026-11-05-r93-citation-semantics.md:1-3`) appended before `## Config custody`. QUALITY.md ends at row 190 at base, so rows 191-192 were appended as bullets. Fragments of every variant: `stubs/stub-fragments.md`.

| # | attack | after | junk | v2 | v3 | covered-by-named-limit |
|---|---|---|---|---|---|---|
| A0 | control: unmodified base 4bda1d1d (block 34 absent) | 1 | 1 | 1 | 1 | n/a (control) |
| A1 | every frozen keyword in a FALSE or contradictory sentence: "A receipt is never bound to the frozen expect label", "...correct even when met_target is true", "A counter is never required to recompute the label from its own counts", "...a planted link is correct, because a unique temporary name is never needed" (QUALITY 191, 192) — clone worktree | 0 | 1 (3 atoms missing) | 0 | 0 | yes — plans `## R95-C2` named limit ("keyword atom is a vocabulary check ... a criterion that carries the keywords passes whether or not it states the rule"); QUALITY 188 residual; knowledge `2026-11-05-r93-citation-semantics.md` limit 1 (containment test, not semantic proof) |
| A2 | A1 plus the three junk keywords (`str() fallback`, `complete JSON or absent`, `helper-only selftest`) carried in false sentences | 0 | **0** (control defeated) | 0 | 0 | yes — same vocabulary limit. The junk control detects only absence of its own vocabulary, not rubber-stamping; the plan's wording "a checker that passed it would be a rubber stamp" overstates it |
| A3 | keywords only in the SKILL.md block-34 prose; QUALITY 191/192 keyword-free | 1 (lacks 6 atoms) | 1 | 0 | 0 | n/a for the checker (control: it reads only the cited criterion text). Depth counters accept it: no (see A6) |
| A4 | control: A1 with `planted` removed from row 192 | 1 (`lacks ['planted']`) | 1 | 0 | 0 | n/a (control: a missing atom is caught) |
| A5 | miscite: all four rows cite `QUALITY 191` (false keyword sentences), `QUALITY 192` is an unrelated row | **0** | 1 | 0 | 0 | **no** — the frozen predicate maps the revision and symlink rows to QUALITY 192 (plans, frozen predicate); the checker never compares the cited number to that mapping, and no named limit mentions it |
| A6 | junk decision table: prose ~35 words with 2 backticked spans and a valid knowledge citation, plus three junk rows `| x | y | z | w |` with no row snippets and no QUALITY citation | 1 (row not found x3) | 1 | **0** | **0** | checker: n/a (rejects it). Depth counters: **no** — v2 and v3 accept three junk rows; the claim's frozen depth commands 2 and 3 pass on it; the named limit covers only the keyword atom |
| A7 | rows name the four frozen snippets and cite 191/192, but QUALITY 191/192 carry no keywords (`Row 191 (empty)`) | 1 | 1 | **0** | **0** | checker: n/a (rejected). Depth counters: **no** — as A6, v2/v3 cannot see the criterion text |
| A8 | positive control: TRUE rule text carrying the same keywords (`... checked only when met_target is true; ...must recompute the label from its own counts`; `... checked against git rev-parse ... under a unique temporary name, so no planted link is followed`) | 0 | 1 | 0 | 0 | yes — A1 and A8 get identical exit codes, so the checker is indifferent to truth; the same named vocabulary limit |
| A9 | repeat of A1 and A2 with `--rev` on committed stubs (63a1a648… and 60361dea…), the frozen command's mode | A1: 0 / A2: 0 | A1: 1 / A2: **0** | A1: 0 / A2: 0 | A1: 0 / A2: 0 | yes (same as A1, A2) |

Receipts: `receipts/*.json` (checker `--json-out`, depth `--json-out`); base control `receipts/base-*.json`; A1 `receipts/clone-stubfalse-*`; A9 receipts are the `--rev` runs (stdout only, reproduced in the report). Negative controls A3/A4 show the checker reads the cited QUALITY text and not the SKILL.md block.

## Predicate clauses satisfied by keyword presence alone (checker, 34cf6579…)

1. Marker `receipt-world-binding v1` present anywhere in the block (prose or comment): presence.
2. `row_snippet` appears once in the first cell of a body row: presence (no link to the criterion's meaning).
3. Criterion cell names exactly one `QUALITY N`: presence; N is not compared to the plan's row-to-number mapping (A5).
4. QUALITY row N exists (bullet `- **Row N (` or table `| N |`): presence.
5. Every frozen keyword is a substring of that bullet (whole bullet text, any sentence, negated or contradictory): presence (A1, A8).
6. The junk manifest exits 1 only if its vocabulary is absent (A2): absence of junk vocabulary is the only thing it tests.
7. Shape (header + separator + >=3 body rows of >=4 cells): structural (A6).

Depth v2 / v3 read block N, its `corpus/knowledge/` citations and range bounds, word and backtick-span counts, and the pipe-table shape. They read no QUALITY text and no criterion meaning (A3, A6, A7).

## Named residual (quoted)

- `plans/round-95-claims.md`, R95-C2 named limit: "The keyword atom is a vocabulary check (QUALITY 188 residual): a criterion that carries the keywords passes whether or not it states the rule. C2 does not claim more than the vocabulary check plus the junk-manifest control."
- QUALITY row 188: "It is a vocabulary check: it does not prove the criterion states the rule, so a criterion that merely repeats the keywords passes (named limit, `corpus/lessons/round-93.md` M93-a and limits)."
- `corpus/knowledge/2026-11-05-r93-citation-semantics.md` limit 1: "The checker requires the cited row's text to *contain* each frozen keyword string; it does not parse the row's meaning. A row that contains 'never refuse an intact input' only in a sentence that negates it would pass."

The named limits cover A1, A2, A8, A9 (vocabulary). They do not cover A5 (number mapping) or A6/A7 (depth counters accept junk tables and empty criteria); the plan names no residual for v2/v3 content.
