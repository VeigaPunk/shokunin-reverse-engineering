# R39C2Counter — R39-C2 counting instrument (pre-freeze build)

**Verdict: DONE** — `c2-counter.py` implements every check the P39-C2 draft names, exits
0/1/2 on the specified map, carries 27 isolated git-fixture selftest cases (27/27 green),
and passes two end-to-end checks against the *real* generator, image writer and triage
interpreter bytes as published in this wave.

## Deliverable

`artifacts/R39C2Counter/c2-counter.py` (783 lines, stdlib only) — L1 copies it verbatim to
`tools/round-39/c2-counter.py` **at the freeze commit** (its own path is one of the four
frozen paths, so any later edit is `exit 2 frozen_path_changed`).

```
python3 -I -B c2-counter.py --root LANE --rev REV --freeze FREEZE [--json-out PATH]
python3 -I -B c2-counter.py --selftest
```

Exit map: **0** `met_target` · **1** computed, target not met · **2** unevaluable
(`unknown_revision:<r>`, `freeze_not_ancestor_of_rev`, `frozen_path_changed`,
`no_manifest_at_rev`, `manifest_unparsable`, `generator_absent_at_freeze`,
`generator_failed`, `generator_wrote_no_manifest`, `regenerated_manifest_unparsable`,
`interpreter_failed`, `met_target_inconsistent`). Unevaluable runs still write the receipt,
including `frozen_paths_changed`, `interpreter_exit` and a stderr tail.

Every input is read with `git show`/`git cat-file`/`git log` only. Regenerated carriers,
materialised tools and envelope copies live in a private `mkdtemp` under
`$HYAKU_SCRATCH/kaidoku-r39`, removed in a `finally`. `--rev`/`--freeze` are resolved to full
hashes first; the manifest seed is compared to the **resolved full freeze hash**.

## Predicate → binding map (20 bindings, all must be `true`)

| Draft clause | Binding |
|---|---|
| manifest seed == freeze | `seed_matches_freeze` |
| manifest names the frozen generator | `manifest_generator_path`, `generator_sha_matches_freeze` |
| classes list sane and 2 each | `classes_unique`, `classes_two_each`, `n_equals_twice_classes` |
| carrier ids/arms/paths sane | `ids_unique`, `arms_valid`, `carrier_paths_unique`, `envelope_paths_unique` |
| table present at REV | `triage_table_present` |
| table block byte-identical at FREEZE and REV | `triage_table_identical` |
| interpreter exists at FREEZE | `interpreter_present_at_freeze` |
| recorded writer agrees with the writer git serves | `writer_matches_manifest` |
| regeneration seed is the freeze hash | `regenerated_seed_matches_freeze` |
| every carrier regenerates byte-identically and equals the committed bytes | `carriers_regenerated`, `carriers_committed` |
| envelope subject digest == carrier sha256 and `operation == extract_firmware` | `envelopes_valid` |
| manifest strictly after FREEZE | `manifest_after_freeze` |
| manifest ancestor-or-equal of every envelope first-add | `manifest_before_envelopes` |

`matched` = carriers whose interpreter label equals the generator's label (manifest `label`
when present, else `class`). `N = len(carriers)`. The receipt asserts the equality
literally: `met_target == (matched == N and all(bindings))` is recomputed independently and
recorded as `met_target_consistent`; a false comparison raises `met_target_inconsistent`
(exit 2) rather than publishing a verdict. The receipt also carries `bindings_false`,
per-carrier `committed_sha256`/`regenerated_sha256`/`label`/`expected_label`/`digest_ok`/
`operation_ok`/`first_add`, `table`, `writer`, `generator`, `manifest_first_add`, `argv`.

The table block is extracted exactly as the interpreter defines it: first line containing
`<!-- sqfs-triage-table v1 -->` inside the `## Queue-drain craft` section (heading
case-insensitive, to the next `## ` heading), through the last consecutive `|` row — marker
line included, so comment lines between marker and table are covered by the freeze
comparison.

## Selftest — 27 cases, 27 pass, 0 fail

One shared fixture builder, three commits each (base / FREEZE / claim data), identity set
only with `-c user.name=fx -c user.email=fx@fx` inside the fixture, toplevel verified before
the first commit. Stub generator writes a real-shaped manifest (recipe `class` + `label`);
stub interpreter implements the marker/table grammar so table edits change labels only when
the table says so.

Green: all bindings and labels · generator object with matching sha · envelope path omitted,
sibling inferred · full CLI envelope `{ok,data,meta}` · lane-root-relative carrier/envelope
paths. Red (exit 1): table removed after freeze · seed != freeze · manifest before freeze ·
envelope before manifest · table edited after freeze · carrier not regenerable · subject
digest mismatch · envelope operation wrong · missing envelope · 3 carriers in one class ·
two carriers share one carrier path · one mislabel · catch-all table · unclassified ·
labels right with a false binding (consistency path). Exit 2: do-nothing (no manifest) ·
interpreter edited after freeze · generator edited after freeze · claims edited after
freeze · counter edited after freeze. Plus a direct unit check of the
`met_target`/`matched` consistency detector over all five truth combinations.

## End-to-end evidence (real bytes published in this wave)

| Check | Inputs | Result |
|---|---|---|
| selftest | fixtures | `SELFTEST cases=27 pass=27 fail=0`, exit 0 |
| base run | `--rev --freeze a2f64e1d` | exit 2 `no_manifest_at_rev` (kill-rule "do-nothing at base" is non-zero) |
| real generator + real writer | `artifacts/R39C2HeldoutGen/heldout-gen.py`, `tools/round-37/gen-squashfs.py` (stub interpreter, fixture-only `stub_class`) | exit 0, `matched 16/16`, `bindings_false []`, generator deterministic across two runs, `writer.sha256` matched |
| real interpreter + TableDraft block | `artifacts/R39C2Triage/sqfs-triage.py`, `artifacts/R39C2TableDraft/skill-craft-block.md`, real generator/writer | exit 0, `matched 16/16`, per-class labels all correct (8 recipe classes, `clean-be`/`clean-le` → `clean`) |
| ReconDep candidate rows | `artifacts/R39C2ReconDep/candidate-triage-rows.md` | exit **2** `interpreter_failed`: `line 16: cause -> action cell has no "->" separator` |
| shortcut controls | `artifacts/R39C2Shortcuts/*.md` | CTL-1 catch-all 4/16→1 · CTL-2 gap-count-only 6/16→1 · CTL-3 gap-kind-only 10/16→1 · CTL-4 published-only 6/16→1 · CTL-5 round36-LE, CTL-6 no-be-no-sr, BOUND, FEASIBILITY-full-table → exit **2** `interpreter_failed` (same missing `->`) |

No REA run, no held-out seed, no held-out carrier was built or touched. The real-byte checks
use fixture repos whose freeze hash is a fresh fixture commit; carriers are regenerated from
that hash.

## Integration contract for the freeze (L1)

1. Freeze commit contains **final** bytes of `tools/round-39/c2-counter.py`,
   `tools/round-39/sqfs-triage.py`, `tools/round-39/heldout-gen.py`,
   `plans/round-39-claims.md`. Never touch those four afterwards — results go to
   `LOG.md`/receipts, not into the claims file.
2. `SKILL.md` carries the craft-section block with the marker. The rest of `SKILL.md` may
   change after the freeze; the block may not.
3. Held-out set: `python3 tools/round-39/heldout-gen.py --seed <FREEZE> --out <dir> --run`,
   then commit `manifest.json` + `<id>/carrier.sqsh` + `<id>/envelope.json` under
   `corpus/evidence/round-39/c2/heldout/`. Add an `envelope` field per carrier or leave the
   envelopes as `<id>/envelope.json` siblings — both resolve.
4. Commit the manifest **strictly after** the freeze and **together with or before** the
   envelopes (same commit is fine: ancestor-or-equal).
5. Keep `tools/round-37/gen-squashfs.py` at the measured revision byte-equal to the writer
   the generator recorded (`generator.writer.sha256`); the counter materialises that file
   from git and hands it to the generator via `KAIDOKU_GEN_SQUASHFS` (argv stays exactly
   `--seed/--out`).
6. Default classes are the eight recipes → 16 carriers; `clean-be` and `clean-le` share the
   label `clean`, so a label-only count would be 7 labels. The draft's "2 per class" is
   scored on the recipe `class`.

## Findings the freeze must absorb

- **F1 — manifest shape.** The real generator writes
  `generator: {name, version, sha256, writer:{...}}`, carriers with `class` (recipe) *and*
  `label`, and no `envelope`. The counter accepts both that shape and the task's simplified
  shape (string generator path; label = class; explicit envelope), verifying the generator
  self-sha and the writer sha when declared. [INFERENCE] The L1 will commit the generator
  manifest verbatim; the counter is built for exactly that.
- **F2 — generator `--out` refusal.** It refuses an existing `manifest.json`; the counter
  always regenerates into a fresh scratch directory.
- **F3 — writer location.** The generator resolves `gen-squashfs.py` relative to its own
  `__file__` or `KAIDOKU_GEN_SQUASHFS`; run from scratch, only the env var works. Covered.
- **F4 — control tables are malformed under the frozen grammar.** Four shortcut controls
  (CTL-5, CTL-6, BOUND, FEASIBILITY-full-table) and the ReconDep candidate rows fail the
  interpreter's `cause -> action` cell rule (no literal `->`), so the counter reports exit 2
  `interpreter_failed`, not exit 1. That still satisfies "must not meet the target", but if
  the L1 wants them scored as *measured misses* rather than *unevaluable controls*, the cause
  cells need `->` before the freeze. The TableDraft block parses cleanly (7 rules) and is the
  one verified end-to-end.
- **F5 — frozen claims file.** `plans/round-39-claims.md` is in the frozen set: appending
  results there after the freeze is `exit 2` by construction.
- **F6 — interpreter exit 2 is contagious by design.** The interpreter makes a malformed cell
  fatal; the counter mirrors that (unevaluable) instead of any silent non-match.

## Risks / limits

- Provenance is digest + determinism + first-add order. A hand-written envelope that carries
  the right subject digest, `operation`, and plausible features would label correctly; the
  counter cannot prove the REA run happened on that carrier (same limit class as the
  round-36 registry note). The committed envelopes must stay unedited pre-freeze.
- The counter verifies the *committed* generator/writer/interpreter bytes, not that the L1
  used the same generator to produce the claim set; determinism at the freeze hash is what
  ties them.
- Regeneration assumes the generator is byte-deterministic across the loop/`lzma` build in
  use; the real generator was verified deterministic here (two runs, manifest and all 16
  carrier bytes equal) [observed].
- Selftest interpreter/generator are stubs (real artifacts are published separately); the
  real-interpreter behaviour is covered by the two end-to-end checks above, whose synthetic
  envelopes are feature-typed, not REA-produced.

## Files

- `artifacts/R39C2Counter/c2-counter.py` — the instrument.
- `artifacts/R39C2Counter/interface-check.py` — real-generator/writer fixture check.
- `artifacts/R39C2Counter/real-triage-check.py` — real-interpreter/table/control checker.
- `artifacts/R39C2Counter/evidence/` — selftest output, base receipt, both end-to-end
  summaries + counter receipts, ReconDep rejection, `controls/summary.tsv` and eight control
  receipts.

No packages installed or updated. Scratch `/fast/scratch/hyaku/kaidoku-r39/R39C2Counter`
removed at exit.
