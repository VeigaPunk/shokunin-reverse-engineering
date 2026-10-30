# MutGapRule — R52 gap-rule mutation battery (wave r52-w1)

**Verdict: PASS.** The gap-rule mutation battery is frozen and every mutant's
expected-verdict matrix is measured from the committed lane bytes. All five
checks green (receipt: `receipt.json`; matrix: `matrix.md`; script:
`gap-rule-mutants.py`).

## What this seat did

Table math only, as briefed: **no counter run, no REA, no carrier bytes, no
network**. The clause math is a faithful port of the three-family disposition
check in `tools/round-50/c1-counter.py` (`disposition_check`, `gap_rule_model`,
`parse_nonregular`, `extract_rel`, `strip_rel`, `diagnostic_rel`,
`silent_detail_matches`), run over an arbitrary rule text against the
**committed** round-50 inputs (`tools/round-50/gap-rule.json`, the four
`tools/round-50/oracle/<id>.nonregular.tsv`, the four
`corpus/evidence/round-50/c1/<id>/after.json`).

### Two independent anchors (the battery is not self-confirming)

1. **Anchor against the committed receipt.** The ported math applied to the
   frozen round-50 rule reproduces
   `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` **exactly**: same
   `gaps_ok` (`true, true, false, false`) and **byte-identical `gaps_note`** on
   all four carriers (`568 gaps (1 structural), 1 removals, 1 silent, on 824
   non-regular entries` … and the `dev/pts/0`…`dev/pts/7` missing-disposition
   note on g7581/g7582). A baseline failure would have made every mutant
   verdict inconclusive; it did not fail.
2. **Cross-validation against the frozen counter itself.** The frozen
   `c1-counter.py` was imported as a module and its own `disposition_check` run
   over **every mutant x carrier pair (40 rows)**: all agree, including
   byte-identical notes.

## The frozen expected-verdict matrix

`shape` = `law_shape_ok` (the claims' rule-shape clause: no
char-device/fifo/socket/block detail under `removed.silent`, and `allowed` for
those kinds is the empty list). `clauses` = every clause that makes the rule
red.

| mutant | rule | shape | c6430 | c6490 | g7581 | g7582 | red clauses | overall |
|---|---|---|---|---|---|---|---|---|
| **M6** | r52 law (`required char-device=false`, device kinds empty in `allowed`) | green | green | green | green | green | – | **green** |
| **M1** | `required char-device=true`, silent `247:0` only | **red** | green | green | **red** | **red** | shape, R | **red** |
| **M1b** | `required char-device=true`, no silent allowance | green | red | red | red | red | R | **red** |
| **M2** | whitelist all thirteen details | **red** | green | green | green | green | **shape only** | **red** |
| **M3** | strict subset `247:0` + `136:0-136:7` | **red** | green | green | **red** | **red** | shape, R | **red** |
| **M3b** | strict subset `136:0-136:7` only (247:0 dropped) | **red** | red | red | red | red | shape, R | **red** |
| **M4** | symlink removal diagnostic dropped | green | red | red | red | red | R | **red** |
| **M5** | `removed.kinds` no longer admits a symlink | green | red | red | red | red | F3, R | **red** |
| **M5b** | no gap kind allowed for a symlink row | green | red | red | red | red | F1, R | **red** |
| **R50-FROZEN** | the committed round-50 rule (CTL-OLD) | red | green | green | red | red | shape, R | **red** |

### The cross-check the brief demanded (M2 / M6 vs `law_shape_ok`)

**M2 (the all-thirteen whitelist) is red BY `law_shape_ok`, not by
disposition.** Its per-carrier disposition is **green on all four carriers**
(every device row now has a disposition), so a disposition-only check would
have scored it green and let a detail whitelist pass. It is killed solely by
the rule-shape clause. **M6 (the law rule) is green on both** — shape green,
disposition green on 4/4. The shape clause is therefore *load-bearing*: it is
the only thing separating the law from an extensionally-identical whitelist
over the measured corpus, exactly as the claims state.

### Two probes (the corpus cannot measure them)

- **Probe 14th device** (the claims' mutation M2): a synthetic `dev/ttyS0 4:64`
  row added to the committed g7581 census. **M6 (law) stays GREEN; M1, M1b, M2
  and M3 all go RED.** The committed corpus has no fourteenth device, so this
  arm is a fixture probe, not a claim about the measured carriers — the L1 must
  land it as a fixture carrier with a 14th device for the frozen control.
- **Probe device-gap fail-closed**: a synthetic `unpublished-entry` gap
  injected on the committed c6430 device row `dev/led`. The **law rule goes
  RED** (`gap kind 'unpublished-entry' not allowed for 'char-device' entry
  'dev/led' (allowed [])`) while the **round-50 rule tolerates it** (its
  `allowed['char-device']` lists `unpublished-entry`). This is the claims'
  "a future extractor that starts emitting a device gap turns the rule red
  (fail closed)" property, demonstrated — and it is a property the round-50
  rule does **not** have.

## Findings for the L1

1. **`law_shape_ok` must be in the frozen counter's clause set, or M2 survives.**
   The disposition check alone cannot distinguish the law from the all-thirteen
   whitelist over the measured corpus (both are 4/4 green). The claims already
   name `law_shape_ok` as a predicate clause; this battery shows it is the
   *only* thing that kills M2.
2. **The claims' wording of `law_shape_ok` has a hole: it does not test
   `required`.** As written ("lists no char-device/fifo/socket/block detail
   under `removed.silent` and `allowed` for those kinds is the empty list"),
   **M1b** (`required char-device=true`, no silent allowance) **PASSES** the
   shape clause. It is still red overall, but by the disposition clause (R),
   not by shape. The claims' F3 amendment says the law is
   `required['char-device'] = false` — that fact is currently only enforced
   *indirectly*, through the disposition of a corpus where the other twelve
   devices exist. The battery reports both `law_shape_ok` and a
   `law_shape_ok_strict` (shape **plus** `required[device] == false`); under
   the strict variant M1b is red by shape as well. **Recommendation: freeze the
   strict variant** (or add `required[device] == false` to the frozen shape
   clause) so the shape clause alone enforces the whole law.
3. **The r52 law rule as specified (`required char-device=false`, device kinds
   empty in `allowed`) is sufficient to make all four carriers green** (M6: 4/4
   disposition green, shape green) — no silent allowance for device kinds is
   needed, and none should be added (the `removed.silent` device detail is
   precisely what makes the round-50 rule fail the shape clause).
4. **The claims' own mutation labels are renumbered relative to the seat
   brief.** The brief's M2 == the claims' M1 (all-thirteen whitelist); the
   brief's M3 == the claims' M4 (strict-subset whitelist); the claims' M2 (the
   14th-device fixture) is the synthetic probe above. The battery carries both
   namings in the script so the L1 does not have to reconcile them by hand.
5. **The removal family (F3) and the "both gapped and removed" exclusivity
   check are load-bearing and independently exercised** (M5 red by F3+R; M5b red
   by F1+R; M4 red by R). A rule that drops the symlink removal diagnostic
   (M4) leaves the removed symlink row with no disposition — red at 0/4.

## Mutation discipline / restoration

The lane tree was **read-only**: every input file's sha256 was taken before and
after the run and is identical (`battery.json` → `restoration.identical=true`;
11 files listed in `matrix.md`). All mutant rule texts and the harness live in
this seat's directory and in scratch; nothing under `tools/`, `plans/`,
`corpus/`, `SKILL.md`, `PROVINCE.md`, `LOG.md`, `SCORECARD.md` or the fleet
repo was written. No git/jj mutation of any kind was run.

## Not run (and why)

- No counter run — `tools/round-52/c1-counter.py` does not exist yet (the L1
  builds it); the rule-scoped control is computed from the committed envelopes
  instead, per the claims' F2 pre-freeze-controls clause.
- No REA invocation — the wave contract reserves REA for the L1.
- No carrier re-fetch and no live census re-derivation — the round-50 carrier
  cache was swept and vendor bytes are out of scope for this seat.
- No live re-run of the round-50 counter — its carrier bytes no longer exist;
  the anchor uses the committed envelopes and the committed verdict receipt.

## Files

- `.ufo/waves/round-52/w1/MutGapRule/gap-rule-mutants.py` — the harness
  (clause port + anchor + cross-validation + probes + battery; exit 0 iff the
  computed matrix equals the independently derived `EXPECTED` matrix).
- `.ufo/waves/round-52/w1/MutGapRule/battery.json` — the full machine output
  (anchor rows, cross-validation rows, matrix, probes, restoration hashes).
- `.ufo/waves/round-52/w1/MutGapRule/matrix.md` — the readable matrix.
- `.ufo/waves/round-52/w1/MutGapRule/receipt.json` — command, exit code, stdout
  sha256, UTC time, check results, artifact hashes, not-run list.

**Tools installed: none** (no `pacman`, no `uv tool`, no `npx` install; the
battery uses only the python3 standard library, and the frozen counter is read
from the lane tree, not executed as a program).
