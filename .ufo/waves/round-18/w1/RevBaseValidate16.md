# RevBaseValidate16 — R17-VALIDATE16 baseline premise (B = 9011581d84527ba34c675f9cf912e54d2e72d470)

**Verdict: OPEN.** The C1 premise holds at B. Both 16-receipt assertions survive unqualified, and the
only retained validator runs cover 8 receipts. One supporting clause in the lesson is **mis-stated**:
remedy (a), "retain the validator run over `git show da64646:…/receipt.json`", is not executable with
the shipped validator against B's tree — I ran it and got 8/8 invalid, exit 1. The live remedy is (b)
correct the count to 8 (or add path rebinding to the validator). The R18 contract's closure check is
simultaneously too weak (it would accept the failing run) and too strong (it forbids remedy (b) and a
stronger 16-entry summary).

## Observation vs inference

Observations are Git-object or file reads plus one executed tool run (receipt-validate.py, read-only,
receipts extracted to `/tmp/r18-val16.taJuQQ`; the executed tool's sha256 equals B's blob,
`618448829ba6c5d743ef10c5b686b9f4e09a3ae09f2da0aa5d0e50e3d239126f`). Inferences are labelled.

| # | Claim at B | Anchor | Label |
|---|---|---|---|
| 1 | Lesson routes R17-VALIDATE16 at line 138 exactly as quoted: 16-claim at `SCORECARD.md:2364` and `round-17.md:122`, `verification.json` retains 8 `receipt-validate-*` runs, all on A receipts | `corpus/lessons/round-17-verifier-spotcheck.md:138` (same bytes at B) | observation |
| 2 | SCORECARD still asserts "all 16 receipts `receipt-validate.py` exit 0" | `SCORECARD.md:2364` at B | observation |
| 3 | The r17 report still asserts "All 16 receipts pass the final validator (verification pass)" | `corpus/lessons/round-17.md:122` at B | observation |
| 4 | `verification.json`: 79 commands, 8 labels starting `receipt-validate-` (+1 `selftest-receipt-validate`, not a receipt run); every argv targets `.ufo/waves/round-17/runs/<label>/receipt.json`; exit 0, expected 0; run 14:47:32–34Z | `.ufo/waves/round-17/verification.json` (top level + commands) | observation |
| 5 | Rev binding: commands carry no per-command rev. The only binding is `source_revision = d0ab299…` (S), `baseline_revision = b563c79…`; receipt targets are worktree paths at S | same file | observation |
| 6 | Receipt blobs: `da64646` has 8, A (`de6c721…`) has 8; A = S = B (identical blobs); A ∪ `da64646` = 16 distinct. So the 8 runs cover exactly the A/S/B set and zero of the `da64646` set | `git ls-tree`/`git rev-parse` over both revs | observation |
| 7 | No retained invocation targets `da64646` objects. The only pass-1 mention is the w2 finding that the *old* validator rejected every producer receipt (`unrecognized_shape`) | `git grep -n R17-VALIDATE16 B -- .`; `corpus/lessons/round-17.md:88` at B; `LOG.md:2076` at B | observation |
| 8 | B's own measured LOG says "8/8 `receipt-validate` exit 0", and SCORECARD's capability row says "`receipt-validate.py` exit 0 ×8 in `verification.json`" — B is internally inconsistent; the 16 claim is the outlier | `LOG.md:2106`, `SCORECARD.md:2374` at B | observation |
| 9 | No correction/qualification line exists at B: `R17-VALIDATE16` appears only inside the verifier lesson itself, not in SCORECARD or LOG | `git grep` at B | observation |
| 10 | The contract's closure evidence is absent at B: `.ufo/waves/round-18/evidence/validate16/summary.json` does not exist (`git cat-file -e` exit 128); it is also absent in the current worktree | `git cat-file`; `ls` | observation |

## Executed counterfactual: remedy (a) is not satisfiable at B

```
mktemp -d /tmp/r18-val16.XXXXXX; for each of the 8 da64646 runs/*/receipt.json: git show da64646:<p> > $T/<p>
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py $T/.../receipt.json
  -> exit 1; {"invalid": 8, "unreadable": 0, "valid": 0}; emitted "exit": 1
  findings per receipt: binding_mismatch ($.bound_sessions, logfile_ok/md5_ok/target_ok false);
  missing_file for runs/<label>/logs/rea-ghidra-<pass1-suffix>/ghidra.log and script.log;
  pro-aether: sha256_mismatch at $.steps.analyze.stdout (expected 2de6d60f…, actual a3db9af2…)

control: python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py <8 receipts tracked at B>
  -> exit 0; {"invalid": 0, "valid": 8}
```

Cause (observation): the validator recomputes digests of the files each receipt names at their recorded
**absolute** paths and has no `--root`/`--rev`/path-map option (`receipt-validate.py:2-6` docstring,
`:718-727` argparse). The pass-1 log paths exist only in the `da64646` tree; at B those paths hold pass-2
logs under different `rea-ghidra-*` suffixes, and `pro-aether/analyze.json` was overwritten.

Inference: no moment existed when the *fixed* validator and live pass-1 bytes coexisted in the worktree —
the fix landed at/after `95e34db`/S, by which time pass 2 had replaced `runs/`. The sentence "All 16
receipts pass the final validator" can therefore only be an inference from shape acceptance, not a run
over the committed pass-1 artifacts. This is the mis-statement: the defect is real, but the first stated
remedy cannot be executed as written against B.

## Minimal objective test

For revision R:

- `claim(R)` = largest unqualified "all N receipts" count in the r17 claim sites (N = 16 at B).
- `covered(R)` = number of **distinct receipt blob ids** for which a committed invocation record at R
  names that receipt, records `exit == 0`, and the invocation target resolves to that blob.
- `corrected(R)` = a named line qualifies the 16 claim to the covered count.

`OPEN(R) := claim(R) > covered(R) and not corrected(R)`; `CLOSED(R) := covered(R) == 16 with all exits 0,
or claim(R) == covered(R) with the claim text corrected`.

At B: `claim = 16`, `covered = 8` (one invocation per A-set label, all exit 0, target blobs = A = S = B),
`corrected = false` ⇒ **OPEN**. The deciding comparison is `16 > 8`; it needs only Git blob ids plus the
command records, no tool execution. The stronger form — `covered` over the union of both pass sets — is
also what a correct closure must show: 8 + 8 distinct blobs, each with a retained exit 0.

## Comparison with the R18 contract (`.ufo/waves/round-18/contract.md:33-35`)

Contract check: `evidence/validate16/summary.json` parses, `rev == da64646…`, `receipts` exactly 8 entries
each with an int `exit`; SCORECARD and LOG each have a line containing `R17-VALIDATE16`. Per
`contract.md:28`, a defect is closed only if all checks pass.

**Too weak — it does not test the defect it names.**
1. `int exit` is not `exit == 0`. The run I obtained (8/8 invalid, exit 1) would satisfy it: the checker
   can close the defect precisely when the claim is falsified.
2. No blob binding: entries need no label, receipt sha, argv/stdout, or `tool` field. Eight arbitrary
   entries plus a `rev` string pass.
3. Token-presence is not text truth: `SCORECARD.md:2364` could remain verbatim while a separate line names
   `R17-VALIDATE16`; the same for LOG. A check that never reads the claim cannot detect a claim/evidence
   mismatch.
4. It never requires the A/S side (the only side actually retained) in the summary, so
   `SCORECARD.md:2374`'s "×8 in `verification.json`" pointer can stay false after a pass.

**Too strong — it excludes the two closures that would actually discharge the defect.**
1. It rejects the lesson's explicit alternative "or correct the count to 8": a truthful text correction
   with no `summary.json` stays open forever.
2. It requires exactly 8 entries, so a 16-entry summary over both revisions — the strongest closure and
   the only one that supports the original 16 claim — fails the check.
3. It mandates a new W18 file instead of repairing the r17 record's own pointer, leaving the r17 artifact
   internally inconsistent even on pass.
4. The mandated route is infeasible at B (above): only a failure record can be produced, which point 1
   of "too weak" then accepts.

Net: too weak on truth-tracking and too strong on remedy shape. The contract should check the claim text
(count corrected or qualified) **and** `exit == 0` **and** receipt-blob coverage — or accept 8/16-entry
summaries bound to the blob set — rather than token presence plus int entries.

## Residual risk / verification gaps

- [INFERENCE] "Could not have been produced" assumes the validator's absolute-path semantics and that no
  external (non-Git) copy of the pass-1 logs existed; Git alone cannot disprove the latter.
- The lesson's "have only w2 seat prose" is imprecise: the 8 `da64646` receipts are committed blobs, and
  the w2 prose records a **red** old-validator run (`corpus/lessons/round-17.md:88`), not a green one. The
  operative claim — zero retained runs over them — is true.
- "A receipts" resolves exactly: A = `de6c721be61bf6e8b4001021f09a9cdea38166dd`, whose receipt blobs are
  identical to S (`d0ab299…`) and B, and disjoint from `da64646`'s.
- No installs or upgrades. Read-only: only this report was written; the validator run read lane bytes and
  wrote only under `/tmp`. No REA/Ghidra/carrier execution.
