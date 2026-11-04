# MutCounter — four mutants of the R67-C1 counter (round 67, w1)

Mutation-test `tools/round-67/avm-le-counter.py` in scratch copies only. Nothing under `tools/`,
`corpus/`, `plans/` or another seat's directory was written; the lane's counter was never edited
(measured before and after, see Restoration). Scratch `/fast/scratch/hyaku/kaidoku-r67/MutCounter`,
deleted before this seat yielded.

## The instrument moved twice while this seat ran

| state | sha256 of `avm-le-counter.py` | where | score path online? |
|---|---|---|---|
| **A** — as dispatched to this seat | `f78ed365…` | blob at `39a91a99`; the worktree bytes at 21:49 | no: exit 2 `gap-rule.json absent at freeze` |
| **B** — correction 1 | `55decb51…` | blob at `3663e6b2` (= `HEAD` until 22:01) | partially: the rule read passes, exit 2 on the r42 REA lock digest |
| **C** — correction 2, live at seat end | `e44cacf5…` | blob at `66389549` (`HEAD`), from 22:01:48 | yes: the REA re-pin (`ecc4de0e`) + the receipts committed (`454071dd`) |
| **D** — in flight while this seat closed | `107211b5…` → `aa73e0da…` (moving) | worktree only, 22:03:53–22:04:15, uncommitted, another actor | unknown; the docstring now says "five things", keeps `carrier_fresh_ok` and `removed.silent`, and the file still carried the placeholder `RULE_V2_PIN = "RULE2PIN"` when last read |

Every verdict below is taken on **C**. The A and B measurements are kept because they document the
two corrections this seat independently hit (`baseline/score-superseded-pin-f78ed365.json`,
`baseline/score-shipped-unevaluable.json`, and the B-lineage A/B under `M1/lineage-b-receipt.json`,
`M4/lineage-b-receipt.json`, `fixtures/`). State D is recorded only as an observation: it was being
written while this seat ran, it is not committed, and it is not the instrument these mutants were
measured against. If D lands, **M1 becomes inapplicable** — a state that keeps the engine's clause
set whole has no `DROPPED_CLAUSES` constant to empty — which is the correct response to F1.

Shared pins: engine `tools/round-50/c1-counter.py` `9820811b…` (unchanged, loaded by path under
`ENGINE_PIN`); gap rule v2 `e66ba022…` (unchanged); carriers table unchanged; red fixture rule
`52b98181…` = rule v2 with `required.char-device` false→true and nothing else.

## Detectors

`D-control` — `--control`: exit code, `control_ok`, `gaps_ok_round67` (4 = the class rule admits
all four frozen envelopes), `gaps_ok_round50` (2), `red_controls`.

`D-score` — `--score` at `--rev 663895493ad24de423b4f9f35ad74ec1f700101f --freeze 3663e6b21dccf…`,
**without `--carrier-cache`**: the four committed after-arm receipts are read, the six
cache-dependent clauses (`carrier_present`, `carrier_pin_ok`, `carve_ok`, `layout_ok`,
`oracle_rederived_ok`, `projection_ok`) fail for want of carrier bytes and every other clause is
decided. That is the cheap, honest baseline for the clauses a mutant can move; with a cache the run
would also perform the REA re-extraction and the unsquashfs re-derivation, which is the L1's data
procedure.

## Baselines

**C-control** (`baseline/control-pristine.json`, counter `e44cacf5…`):

```
exit 0  control_ok True  gaps_ok_round67 4  gaps_ok_round50 2  rule e66ba022
red_controls: dropped_symlink_gap=bin/adsl  round67_rule_still_fails=True
              junk_rule_would_pass=True  publication_check_names_it=True  published=dev/led
```

**C-score** (`baseline/score-real-receipts-baseline.json`): exit 1, `carriers_matched 0`, 24
`failing` entries = exactly the six cache-dependent clauses × 4 carriers. Everything receipt-derived
is green on all four: `receipt_present`, `receipt_fresh`, `evidence_envelope_ok`, `subject_pin_ok`,
`operation_ok`, `handler_ok`, `chunks_ok`, `oracle_hits_ok`, `gaps_ok` (**4/4** under the class
rule), `nonregular_unpublished_ok`, `path_shape_ok`, `run_provenance_ok`, `parameters_ok`,
`evidence_id_ok`; `carrier_fresh_ok` true ×4. Bindings: `carriers_spec_ok`, `gap_rule_ok`,
`frozen_tables_valid` true; `province_core_section`, `province_core_row`, `frontier_note`,
`entry_present`, `sourced`, `coverage_map_row` false — the round-67 prose/entry does not exist at
this rev yet, so `met_target` cannot hold until the documentation lands (not this seat's subject,
but it is the other half of the score).

**B-score** (`fixtures/score-baseline.json`, fixture `ff26dcbb…`): the same A/B before the receipts
were committed, using `AFTERDIR → corpus/evidence/round-50/c1` and an `evidence_ids` stub. Verdicts
agree with C; it is kept as corroboration, not as the primary record.

## Verdicts

| mutant | mutation | bytes | detector | baseline | mutant | verdict |
|---|---|---|---|---|---|---|
| **M1** | `DROPPED_CLAUSES ("carrier_fresh_ok",)` → `()` | `c7c2e2f5…` | `D-score` | exit 1, 24 failing | exit 1, **24 identical** failing | **survived — equivalent mutant** |
| **M2** | rule `required.char-device` false→true | rule `52b98181…` + driver `a6a8549e…` | `D-control` | exit 0, `control_ok` true, `gaps_ok_round67` 4 | exit 1, `control_ok` false, `gaps_ok_round67` 0 | **killed** (control field + exit code) |
| **M3** | `control_ok` conjunction → `ok = True` | `4fea96fa…` (base `ee1f816c…`) | `D-control` on the red rule | exit 1, `control_ok` false | exit 0, `control_ok` true | **killed on the red fixture** (control field + exit code); invisible on the green control |
| **M4** | `PROV_BASE …kaidoku-r67/` → `…kaidoku-r50/` | `72031bd8…` | `D-score` | `run_provenance_ok` true ×4 | `run_provenance_ok` **false ×4** | **killed** (receipt field; exit code unchanged only because the cache is absent) |

One survivor, three kills.

---

## M1 — `patch_engine` keeps `carrier_fresh_ok`

```diff
-DROPPED_CLAUSES = ("carrier_fresh_ok",)
+DROPPED_CLAUSES = ()
```

`M1/counter.py` = live bytes + that line, sha256
`c7c2e2f5a40adb768801295b60efcbdd962a82e75a3a0b57c1d32dbd74283a38`. Command `M1/run.txt`; receipt
`M1/receipt.json`, exit **1**.

Against the C baseline, leaf by leaf: `patches.clauses` 22 → 23 (the clause is re-inserted at index
2), `patches.dropped_clauses` `["carrier_fresh_ok"]` → `[]`, and the counter sha it echoes about
itself. **Zero behavioural leaves** — `failing` identical (24 entries), every per-carrier clause
value identical, every `matched` flag identical, `bindings_false` identical.

Why it cannot be anything else — `M1/prior.out`, calling the pinned engine's own `prior_pins()` at
the freeze `3663e6b2`:

```
prior_sources ['.ufo/waves/round-41/c1/carriers.json', 'tools/round-49/carriers.json',
               'tools/round-42/prior-pins.json']
prior_pin_count 18
g7581 pin_in_prior=False => carrier_fresh_ok = True
g7582 pin_in_prior=False => carrier_fresh_ok = True
c6490 pin_in_prior=False => carrier_fresh_ok = True
c6430 pin_in_prior=False => carrier_fresh_ok = True
```

`carrier_fresh_ok` is **true 4/4**, so restoring it to `CLAUSES` cannot move `carriers_matched`. The
declared patch 5 of the "six disclosed patches" is a **no-op**, and its stated reason — "freshness
cannot hold by construction" — is false against the pinned prior tables. It is harmless as a patch
and misleading as a rationale: the drop does not carry the claim, and it could not have rescued the
claim had a prior table listed the four pins (the clause would then be false with or without the
drop). `w1/CriticClaims.md` §2 reached the same conclusion by a different route.

The clause's value is computed unconditionally per carrier (`d['carrier_fresh_ok'] = pin is not None
and pin not in prior`, engine line 2250) and `failing_lists()` names any `CLAUSES` entry not `True`,
so a *false* `carrier_fresh_ok` — the only way this clause can bite — would surface in `failing` and
in `carriers_matched`. The survivor is inert, not undetected.

## M2 — the rule's `required.char-device` back to true

`M2/rule-mutation.diff` (the rule is the mutant; the counter copy is a pointer holder):

```diff
  "required": {
   "symlink": true,
-  "char-device": false,
+  "char-device": true,
   "block-device": false,
```

Mutant rule sha256 `52b981819948a21160c8d2f94d1676dedb8ed8035d4fb7ac006f2743c8adabb7`; driver
`M2/driver.py` sha256 `a6a8549ec6ad72f581d9b1f85a80d888ebc56179eb8c7080511eea6af09c78a3` = live bytes
with `RULE_V2` pointing at a scratch rule slot (the control path reads the rule from the filesystem,
so the lane is untouched). Command `M2/run.txt`.

| field | green rule `M2/m2_green.json` | mutated rule `M2/m2_red.json` |
|---|---|---|
| exit | 0 | **1** |
| `control_ok` | true | **false** |
| `gaps_ok_round67` | 4 | **0** |
| `gaps_ok_round50` | 2 | 2 |
| `red_controls.junk_rule_would_pass` | true | **false** |
| `red_controls.publication_check_names_it` | true | true |
| `rule_problems` | all empty | all empty |

Killed by the control field and the exit code, and the green run with the same driver exits 0, so
the kill is attributable to the rule. `gaps_ok_round67` lands at **0**, not round 50's 2: see F2 —
v2 also dropped `removed.silent.char-device = ["247:0"]`, so with `required.char-device` restored
the two Cable carriers (one char device each) fail as well. `gaps_ok_round50` stays 2 because that
model still carries the silent block.

## M3 — the `--control` `control_ok` expression forced true

`M3/mutation.diff` (`M3/base-counter.py` → `M3/counter.py`, identical except this hunk):

```diff
-    ok = (doc["gaps_ok_round67"] == TARGET and doc["gaps_ok_round50"] == 2
-          and doc["red_controls"]["round67_rule_still_fails"] is True
-          and doc["red_controls"]["publication_check_names_it"] is True)
+    ok = True
     doc["control_ok"] = ok
     doc["exit_code"] = 0 if ok else 1
```

Mutant sha256 `4fea96facf253e41f169139b5a1b0ca0c6f6b19d50c91696e71988d659d4ceee`; unmutated driver
`ee1f816cedef1532fa9d5c1c50bf26709c2fc99b84f7aa73e91cacd68b6f5d2d`. A forced-true control is only
visible where the honest expression is false, so the detector is the red rule (M2's rule), same
driver pair:

| fixture | base driver | M3 |
|---|---|---|
| green rule | exit 0, `control_ok` true, `gaps_ok_round67` 4 | exit 0, `control_ok` true, 4 |
| red rule | exit **1**, `control_ok` **false**, `gaps_ok_round67` 0 | exit **0**, `control_ok` **true**, `gaps_ok_round67` 0 |

Killed by the control field and the exit code on the red fixture: the mutant certifies a rule whose
own `gaps_ok_round67` is 0 and whose junk-rule red fixture no longer discriminates
(`junk_rule_would_pass false` in both columns). On the green control the mutant is invisible — a
forced-true flag and a true flag agree — so the wave's red-fixture battery is what makes it
detectable at all.

## M4 — `PROV_BASE` left at the r50 prefix

```diff
-PROV_BASE = "/fast/scratch/hyaku/kaidoku-r67/"
+PROV_BASE = "/fast/scratch/hyaku/kaidoku-r50/"
```

`M4/counter.py` sha256 `72031bd8b9e58c619c0dd9c1b0cdd04133732ae2224ccbb67ea465c9774f1ff8`. Command
`M4/run.txt`; receipt `M4/receipt.json`, exit 1.

Against the C baseline, the complete delta is exactly four additions and nothing else:

```
+ c6430:run_provenance_ok
+ c6490:run_provenance_ok
+ g7581:run_provenance_ok
+ g7582:run_provenance_ok
failing 24 -> 28;  carriers_matched 0 -> 0 (cache absent on both sides)
carriers/*/run_provenance_ok: true x4 -> false x4
patches/prov_base: /fast/scratch/hyaku/kaidoku-r67/ -> /fast/scratch/hyaku/kaidoku-r50/
```

`run_provenance_ok` is a pure function of the receipt's `parameters.output_directory` and
`PROV_BASE`; it takes no data. The four committed after-arm receipts sit under
`/fast/scratch/hyaku/kaidoku-r67/`, so under M4 they fail **whatever the carrier cache supplies**:
the six cache-dependent clauses can be satisfied by a data run, this one cannot. `carriers_matched`
is therefore 0 and the exit is 1 instead of 0 — a data run would not rescue it.

`M4/provenance-probe.txt` measures the same clause through the engine's own `provenance_ok()`, both
directions, so the inversion is not an artefact of the missing cache:

| `parameters.output_directory` | base `PROV_BASE` r67 | M4 `PROV_BASE` r50 |
|---|---|---|
| `/fast/scratch/hyaku/kaidoku-r67/c1-run.ABC123/extract` (real `c1-run.sh` shape) | true | **false** |
| `/fast/scratch/hyaku/kaidoku-r67/counter/x` | true | **false** |
| `/fast/scratch/hyaku/kaidoku-r50/c1-run.uVY6Hs/extract` (frozen envelope) | false | **true** |

Verdict **killed by receipt field**. Note that M4 leaves `PROV_SEGMENT = "/kaidoku-r67/"` alone, so
the receipt's `patches` echo carries the inconsistent pair (`prov_base …r50/`, `prov_segment
/kaidoku-r67/`) — this mutant is visible to a reader of its own receipt without any run.

## Findings beyond the four verdicts

**F1 — one of the six declared patches is a no-op and its stated reason is false** (M1). Harmless
patch, false rationale; corroborated by `w1/CriticClaims.md` §2.

**F2 — the v2 rule's `removed` block is not "unchanged from round-50"** as the counter docstring
(item 1) and the wave description state: `removed.silent.char-device = ["247:0"]` is gone
(`baseline/rule-delta-vs-r50.diff`; the only other delta is `required.char-device`). Inert while a
char device is not required; load-bearing the moment one is — M2's red rule lands at 0 of 4, not
round 50's 2 of 4. Prose that says the class rule changed in exactly one field is off by one.

**F3 — the REA package pin drifted, and the correction widens the patched surface.** At 21:59 the
shipped `--score` exited 2 before any clause: `baseline/score-shipped-unevaluable.json`,
`unevaluable "rea package does not match the freeze: package-lock.json sha256 815c18f1… != frozen
d42d56f0…"`. The npx `rea-agents` 6.5.0 tree kept the frozen `package.json` (`a5003023…`); only the
npm-written lock differed, and no `package-lock.json` with the frozen digest exists under
`/home/vgpnk` or `/fast/scratch` (`find … -name package-lock.json`, every file hashed, depth 8).
The lane re-pinned at `ecc4de0e` (atom **A11**), which restores the run. Two residues a reviewer
should weigh: (i) `patch_engine` now also patches `mod.rea_package_problems`, so the engine's own
frozen `rea-pkg` document (read at the freeze through `REA_PKG_CANDIDATES`) is no longer consulted —
the REA identity is now bound by a wrapper constant (version + `package.json` sha + the host's lock);
(ii) frozen atom **A4 still says** "the patched names are exactly GAPRULE, AFTERDIR, ENTRY, STEM,
CORE_HEADING, FRONTIER_MARK, OPENED_DATES, PROV_BASE, PROV_SEGMENT, WORK_OVERRIDE and CLAUSES", and
the docstring still says "patching exactly six things" / "The six disclosed patches", while there
are now seven engine bindings patched. The receipt does disclose it (`patches.rea_pkg`), so it is
not hidden — but A4 and the docstring are false as written.

**F4 — the instrument's bytes moved twice during the wave**: `f78ed365…` (dispatch) → `55decb51…`
(correction 1, `1e7fe7b7`, worktree restored at 21:57:31) → `e44cacf5…` (correction 2, `ecc4de0e` /
`66389549`). A seat that hashes `tools/round-67/avm-le-counter.py` gets different answers before
21:57:31, between 21:57:31 and 22:01:48, and after; any receipt written in an earlier window names
the earlier sha.

**F5 — the A-state bytes fail exactly where A10 says.** `baseline/score-superseded-pin-f78ed365.json`:
`f78ed365…` at `--rev 3663e6b2 --freeze 3663e6b2` (= the freeze, where the rule file certainly
exists) returns exit 2 `gap-rule.json absent at freeze`, because `patch_engine` passed an absolute
path and the engine reads `GAPRULE` through `git show <rev>:<path>`. The B and C bytes pass that
point. Cosmetic residue on C: `patches.gap_rule` still echoes the absolute path while the engine
receives the lane-relative name.

**F6 — the documentation bindings are the other half of the score.** On C, with the data receipts
committed, the only failing clauses are the six cache-dependent ones; but six of the nine bindings
(`province_core_section`, `province_core_row`, `frontier_note`, `entry_present`, `sourced`,
`coverage_map_row`) are false at `66389549`. `met_target` needs both, so a cache-backed run cannot
reach 4/4 until the entry and the PROVINCE/README/SOURCES rows land.

## Reproduction

```
S=/fast/scratch/hyaku/kaidoku-r67/MutCounter     # deleted before this seat yielded
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
git -C $L show HEAD:tools/round-67/avm-le-counter.py > $S/c.py     # = e44cacf5 at seat end
$L/tools/round-67/avm-le-counter.py --control --root $L --rev a7a4ce69… --work $S/w --out ctl.json
$L/tools/round-67/avm-le-counter.py --score --root $L \
    --rev 663895493ad24de423b4f9f35ad74ec1f700101f --freeze 3663e6b21dccf4c4957f459301156664d8b151d6 \
    --pkg65 ~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
    --claims $L/.ufo/waves/round-67/claims.json --work $S/w --out score.json
```

`--score` without `--carrier-cache` needs no extraction and finishes in under a second; it reads the
four committed receipts and decides every clause except the six that need the carrier bytes.

## Restoration and provenance

- No write to `tools/`, `corpus/`, `plans/` or any sibling directory. Every mutant is a scratch
  copy; the two rule mutations live in scratch `rule.json` slots the driver points at.
- Counter sha at seat start: `f78ed365…` (the dispatch pin). At 22:02 it was `e44cacf5…` = `git show
  HEAD:tools/round-67/avm-le-counter.py`, with `git status -- tools/` clean. Both of those changes
  are the lane's disclosed corrections (A10, A11), not mine. At 22:03:53–22:04:15, while this seat
  was writing up, `tools/round-67/avm-le-counter.py` and `tools/round-67/gap-rule-v2.json` were
  modified again by another actor and left uncommitted (state D above; the rule reached
  `b55d5e87…`, the counter passed through `107211b5…` and `aa73e0da…`). Those bytes are not mine,
  not tested here, and not stable at the time of writing; the wave must re-hash before it scores.
- One bytecode cache entry (`tools/round-67/__pycache__/avm-le-counter.cpython-314.pyc`, created
  when this seat's probe imported the counter) was removed; a sibling's
  `mutation-battery.cpython-314.pyc` was left untouched. `__pycache__/` is gitignored.
- Scratch tree deleted; no evidence lives under `/tmp`.
