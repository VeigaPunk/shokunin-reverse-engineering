# CriticClaim — round 83 attribution calibration

Axes: calibration accuracy; causal relevance to committed evidence; provenance/identity preservation; resistance to fixture gaming; scope honesty. Author-side review only: no admission, integration, or canonical judgment.

## Actual mismatch, not merely house style

Read-only `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 650344bc37ca303fb9487c1174192057af499b9b:corpus/knowledge/2026-11-04-r82-conjunction-and-printed-commands.md` exposes this actual first line:

> source: S286 — https://docs.python.org/3/library/shlex.html#shlex.split; reopened 2026-11-04; retained snapshot .ufo/waves/round-82/l1/sources/shlex.html:227-234; duplicate S299 withdrawn in-round

The final paragraph also explicitly says S299 duplicates S286 and was withdrawn. Thus S299's positive attribution is contradicted by the actual historical entry, independently of the newly specified comma-list grammar. S286 remains positively attributed. There are two real query cases over ONE real document, not two independent real documents.

The committed legacy receipt was also read with `git show` at that BASE. `.ufo/waves/round-82/l1/scores/c2-at-landing.json:137-146` retains `entry_cites_row:true`, but `row_mined:false`, `met:false`, and `SOURCED_ROW_UNMET`; overall `ok:false`. Do not recast this as a formerly accepted C2 claim. The narrow correction is that its true attribution subfield meant lexical presence, not positive attribution. Keep the original receipt unchanged.

`tools/round-82/printed-command.py:257-261` returns membership in `re.findall(r"\bS[0-9]+\b", line)` on the first `source:` line. It therefore includes S299 from the withdrawal commentary. The preexisting `.ufo/waves/round-83/pre/legacy.json` records three mismatches: `real-withdrawn`, `commentary-only`, and `withdrawn-head`; its subject SHA-256 equals the historical receipt's instrument SHA-256, `88b1dff2385547e1bdb2ecf802d667c38eabe929747075c27ae88f0c5c061487`. These are inspected existing measurements, not independently rerun results. The existing refuse-everything receipt records three mismatches, including `real-primary`; mere blanket refusal is insufficient.

## Strongest counterexample: finite success need not implement the grammar

Frozen `.ufo/waves/round-83/attribution-cases.json:2-9` uses only S286 and S299; S286 is queried positively once. A self-contained shortcut can satisfy all eight expected booleans without implementing attribution parsing:

```python
def entry_cites(text, sid):
    return sid == 'S286' or (sid == 'S299' and (
        text.startswith('source: S299 —') or
        text.startswith('source: S286, S299 —')))
```

[INFERENCE, static case-by-case derivation; not executed] This yields true for real-primary, plain-positive, and multi-positive, and false for the other five frozen inputs. Yet `entry_cites('no source field', 'S286')` is true. It also ignores duplicate fields, line-window constraints, most valid ids, and general list parsing. An exact `(text, sid)` lookup table can do the same; fixture case ids need not be passed to the function. A constant scalar cannot pass because the expected population mixes true and false, but a constant map can.

Impacted axes: calibration and generalization, not the literal eight-case predicate. The declared finite predicate can remain honestly satisfied by a bad general parser; the fixed population cannot distinguish these implementations. Smallest safe correction: leave predicate, counter, fixtures, and freeze untouched; manually inspect candidate source for an actual id-independent parser and explicitly retain the finite-coverage limit. A claim of general grammar enforcement would require a separately scoped future declaration, not an in-round reinterpretation. This review does not issue the canonical judgment on that tradeoff.

## AST extraction: authentic function bytes, limited execution claim

The declaration-pinned `tools/round-83/attribution-audit.py` was read directly using `git show de4e58b2c22bf4376dc81bd32dfe0b9ac605e17e:tools/round-83/attribution-audit.py`; it matches the inspected extraction structure:

- Lines 21-30 parse the committed subject, require exactly one synchronous top-level `entry_cites`, compile only that function AST, and provide `re`. Ordinary module-level CLI statements and other helper definitions are excluded. The legacy function is actually exercised, not reimplemented.
- Lines 34-39 pass the actual BASE document for both real cases and require `type(value) is bool` plus expected equality. Lines 43-56 read fixtures from `--freeze`, target from resolved `--rev`, and the actual entry from fixed BASE, recording all three byte hashes.
- Full subject-file hashing identifies the containing bytes; it does not establish that its CLI or all module behavior executed. The measured unit is the extracted function. Avoid calling this an end-to-end historical script repair.
- AST selection is not a sandbox or an enforced purity proof: the retained function can contain imports, defaults, decorators, nested definitions, mutable state, or builtin access. Python `exec` supplies builtins; providing only `re` explicitly does not prove the function uses only `re`. Thus fixture-reading or state/order shortcuts remain possible in principle. No exploit was executed, and no candidate is accused of using one.

Impacted axes: provenance and resistance to gaming. Smallest safe correction: describe the function-level measurement precisely and source-review self-containedness; do not claim runtime isolation, CLI coverage, or adversarial authenticity. Altering the frozen extractor is outside this review.

## What the eight cases do not establish

The plan already limits itself to a bounded house grammar and does not claim universal natural-language interpretation or historical migration. Preserve that wording. The real example establishes a substantive lexical-versus-positive mismatch; the six synthetic cases extend coverage but do not prove the entire grammar. No frozen case exercises duplicate source fields, the twelve-line cutoff, fewer-than-three-digit identifiers, a different queried id, or many malformed-list variants. The `embedded-id` case does distinguish S299 from S2999. These are coverage limits, not grounds to silently add fixtures or change acceptance.

After the initial report, ExecCandidate supplied `.ufo/waves/round-83/w1/ExecCandidate/candidates/source-bind.py`. Read-only inspection of lines 37-46 finds an id-independent implementation: first twelve lines, exactly one line-start source field in that window, a fullmatch over ASCII-digit comma-separated ids and the em-dash separator, then exact id membership. No constant map, S286/S299 special case, stateful sequence, decorator, default expression, or builtin escape appears in that function. Thus the shortcut counterexample identifies a frozen-test limitation, not an observed defect in this supplied implementation. This is static source inspection, not an execution result. CLI execution remains outside the frozen extracted-function measurement.

## Execution and boundaries

Only read-only inspection was performed. No builds, linters, formatters, executable probes, clone, installation, git/jj mutation, production edit, sibling write, or runtime invocation. A read-only git call initially used the prescribed but nonexistent scratch cwd and failed before execution; subsequent calls used the existing fleet cwd and absolute `git -C` paths. No scratch directory or files were created, so no scratch cleanup was necessary. No tool installs/updates to record.

Self-evaluation: accuracy 4/5 (pinned source/receipt and supplied candidate inspected, attack behavior statically derived rather than executed); completeness 4/5 (all assigned evidence surfaces covered, no runtime results claimed); clarity 4/5 (findings separate real defect from finite-coverage tradeoff, report intentionally detailed); actionability 4/5 (specific source-review and wording corrections without moving freeze); conciseness 4/5 (provenance and boundary details add length). Overall 4.0/5. Highest-impact improvement is to preserve these limits in L1's final assessment rather than treating a finite pass as comprehensive grammar enforcement. The user should agree this is bounded author-side evidence, not admission.
