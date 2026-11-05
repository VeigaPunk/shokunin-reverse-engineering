# CriticC2 — adversarial attack on R95-C2 (depth, craft block 34)

Frozen at 4bda1d1dd3788973f10e61212b70df18b3b14ea0. Pins matched (checker 34cf6579…05340; depth-v2 359f15e1…dcf18f; depth-v3 bcf6c4ea…aeb052f; after manifest cf5f265f…03ba8; junk manifest abcf7bda…a321). Full table: `.ufo/waves/round-95/w1/CriticC2/attacks.md`.

## Verdict

The claim's surface (a decision table whose criteria "state the rules the rows assert") is not certified by the frozen predicate. The keyword atoms are a containment test: a false, contradictory criterion that carries every frozen keyword exits 0 (A1, A9), and a true one exits 0 identically (A8). The junk control is itself a vocabulary test: it passes whenever the stub carries its three junk phrases (A2, exit 0). The claim's own named limit (vocabulary check, QUALITY 188) covers A1, A2, A8 and A9. It does not cover two further gaps:

- **A5 (miscite, exit 0):** the frozen predicate maps the revision and symlink rows to QUALITY 192; the checker never compares the cited number to that mapping, so all four rows citing QUALITY 191 pass while QUALITY 192 is unrelated.
- **A6/A7 (depth counters, exit 0):** depth-blocks-v2 and depth-blocks-v3 accept block 34 with three junk table rows (A6), and with rows naming the frozen snippets whose criteria carry no keywords (A7). Their floors are shape-only (word count, backtick spans, citation range, pipe-table shape). The plan names no residual for them.

## Predicate clauses satisfied by keyword presence alone

Checker (`tools/round-93/craft-citation-semantic.py`): block marker substring; row snippet substring in the first cell; `QUALITY N` count in the criterion cell (N not compared to the plan's mapping); QUALITY row N existence; every frozen keyword as a substring of the whole QUALITY bullet (any sentence, including negated or contradictory ones). The junk control exits 1 only when its junk phrases are absent.

Depth v2 / v3: block existence, citation range bounds, word and span floors, pipe-table shape. No criterion text is read.

## Plan wording on the residual (quoted)

`plans/round-95-claims.md` R95-C2 named limit: "The keyword atom is a vocabulary check (QUALITY 188 residual): a criterion that carries the keywords passes whether or not it states the rule. C2 does not claim more than the vocabulary check plus the junk-manifest control."

## Receipts and commands

- Stub built in `$S/clone` (commits 63a1a648… and 60361dea… for the `--rev` repeats); fixtures under scratch, deleted after copying. Receipts copied to `.ufo/waves/round-95/w1/CriticC2/receipts/`. Stub fragments: `.ufo/waves/round-95/w1/CriticC2/stubs/stub-fragments.md`.
- Base control reproduces the pre-receipts: checker exit 1 `block 34 missing (craft has 33 blocks)`; v2 exit 1 `blocks 33 resolved 33 expect 34`; v3 exit 1.
- Stub A1 (keywords in false sentences): checker `--worktree` exit 0 `ok`; junk manifest exit 1 (`lacks ['str() fallback']`, etc.); depth-v2 exit 0 `blocks 34 resolved 34`; depth-v3 exit 0 `required-shaped 1/1`.
- Junk-vocabulary stub (A2): junk manifest exit 0 `ok`.
- Junk table with no snippets (A6): checker exit 1 (`row not found` x3); depth-v2 exit 0; depth-v3 exit 0.
- Note on mode: the frozen commands use `--rev`. I ran `--worktree` on the clone and `--rev` (A9) on committed stubs; both gave the same exit codes.
- Tooling: nothing installed or upgraded. Host state: none changed. Lane: no files written; `git status` shows only other seats' untracked L1 files.

## Smallest safe correction (for the L1 at landing, not an edit to frozen files)

1. The landing knowledge entry must name A1, A2, A5, A6 and A7 as residuals, and must not describe the junk control as a rubber-stamp detector: it tests absence of its own vocabulary.
2. A fix for A5 and A7 needs a new frozen predicate (a row-to-number binding in the manifest and a criterion-text check), not an edit to `craft-citation-semantic.py` or the depth counters in this round.
3. Depth v2 / v3 should be cited only as structural floors in the landing receipt.

## Files written

- `.ufo/waves/round-95/w1/CriticC2/attacks.md`
- `.ufo/waves/round-95/w1/CriticC2/stubs/stub-fragments.md`
- `.ufo/waves/round-95/w1/CriticC2/receipts/*.json` (base controls, A1, A2, A3, A4, A5, A6, A7, A8, A9 `--rev` runs)
- `.ufo/waves/round-95/w1/CriticC2.md` (this report)
- Scratch `/fast/scratch/hyaku/kaidoku-r95/CriticC2` removed after copying.
