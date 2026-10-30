# R51 v1-counter audit — dead weight the v2 port must drop

Seat: SimpV1Audit · scope: `tools/round-50/c1-counter.py` (4836 ln) and
`tools/round-50/c1-controls.py` (1817 ln).

Method: read both files end to end; static AST reachability scan (no undefined
name); then **offline probes** against the *committed* round-50 receipts and
oracle tables. No REA was run (no `npx rea-agents`, no package invocation, no
network). All probe scripts and receipts are under
`/fast/scratch/hyaku/kaidoku-r51/w1-SimpV1Audit/` (removed at the end).

**Verdict: the v1 counter's core disposition machinery is exactly what the
round-51 law needs — keep it. Almost everything that must change is in the
*constants and the flags*, not the algorithms.** Concretely: 6 items to DROP,
9 to RE-POINT, 5 to KEEP-with-question, and **3 defects the port must not
inherit** (below, "DO NOT INHERIT").

---

## A. DROP — provably dead or provably round-50-only in the v2 port

| # | file:line | item | evidence | recommendation |
|---|---|---|---|---|
| A1 | `c1-counter.py:396` | `PROV_SEGMENT = '/kaidoku-r50/'` | **zero uses in the counter.** `grep -n PROV_SEGMENT c1-counter.py` → only the definition. The controls read it only as a *fallback* in `consts()` (`c1-controls.py:271`: `PROV_BASE or PROV_PREFIX or PROV_SEGMENT`), and `PROV_BASE` is always present, so the fallback is never taken. | **DROP.** It is round-50 path text with no consumer. |
| A2 | `c1-counter.py:1321-1326` (`same_rel`) | `same_rel()` | **no call site in the production path.** Its only caller is the selftest probe at `c1-counter.py:3659`. The production path compares via `extract_rel`/`strip_rel` (`1325` is inside `same_rel` itself; the live call sites are `1380`, `1409`, `1423`, `1432`, `1496`, `1511`). | **DROP from the port's production path; keep only if the selftest probe is ported.** It is a selftest-only helper that duplicates `extract_rel`+`strip_rel`. If the v2 selftest keeps the exact-vs-legacy discriminator, keep `same_rel` *in the selftest* and delete it from the module top level. **KEEP-with-question** — the selftest probe (`3659`) needs a name; see B7. |
| A3 | `c1-counter.py:1328-1333` (`legacy_same_rel`) | the round-40 suffix matcher | selftest-only by design (docstring: "Selftest only"). It exists to *prove* the exact matcher discriminates from the defective round-40 rule. | **KEEP** (it is the falsification witness for R40-CL1). Do not drop: it is provenance, not weight. |
| A4 | `c1-counter.py:386-392` | `PRIOR_PIN_CANDIDATES` entries `tools/round-50/prior-pins.json`, `tools/round-49/prior-pins.json` | **Neither file has ever existed in git** (`git log --all --diff-filter=A -- 'tools/round-50/prior-pins.json' 'tools/round-49/prior-pins.json'` → empty; `ls` → MISSING). Only `tools/round-42/prior-pins.json` exists, and it is the only one that has ever resolved. | **DROP the two never-existing paths**; keep `tools/round-42/prior-pins.json` (live) and add the round-51 file the port actually freezes. *(`tools/round-50/carriers.json` in `PRIOR_CARRIER_TABLES` is different — that file exists and the port needs it per F1.)* |
| A5 | `c1-counter.py:391-392` (`REA_PKG_CANDIDATES`) | `tools/round-50/rea-pkg.json`, `tools/round-49/rea-pkg.json` | same finding: **neither has ever existed** (`git log --all --diff-filter=A` over those two paths → empty). At the round-50 freeze the tree held only `tools/round-42/rea-pkg.json` (verified with `git ls-tree -r 435d41fd`). The round-50 counter therefore *silently* resolved to the **round-42** pin. | **DROP the two dead candidates.** More important: the port must land a real `tools/round-51/rea-pkg.json` (or knowingly reuse round-42's) — otherwise the candidate list resolves to round-42 by accident, exactly as round 50 did. **Note: the draft v2 already lists `tools/round-51/rea-pkg.json` first, but that file does not exist yet (see D4).** |
| A6 | `c1-controls.py:73-74`, `439-461` | `REA_ATTEMPTS = 5`, `LAST_ATTEMPTS`, the `capture_real` retry loop with `time.sleep(15)` | This is the **attempt-1 timeout workaround**: a round-50 host-load flake policy (REA 6.5.0's fixed 120 s deadline) baked into the *controls driver*. The counter has its own, different policy: `MAX_REA_ATTEMPTS = 3` with **no sleep** (`c1-counter.py:1923`, `2053-2076`). Two divergent retry policies for the same flake is the "second convention" the role forbids. | **DROP the controls' own retry/sleep policy**; the port's counter-side retry (`MAX_REA_ATTEMPTS=3`) is the one to keep and extend (amendment F6 already asks for the ENOENT case to join it). If the v2 controls keep a live-capture path at all, it must call the counter's policy, not a second one. |
| A7 | `c1-controls.py:837-889` (`spec_c1b`), `1095-1157` (`spec_c2x`) | the BE-carrier arm and the attack arm | Both are **"EXTRA ARM (not in the default set)"** by their own docstrings and are absent from `ALL_CONTROLS` (`:77`). `spec_c1b` reads `corpus/evidence/round-41/c1/L3` (a round-41 BE carrier) — a body the round-51 LE-only claim has no use for. `spec_c2x` is "outside the plan" by its own note and the round-50 summary already treats it as `informational_c2x`. | **DROP both** from the v2 controls unless the L1 explicitly wants a BE arm. They are the largest single blocks of round-50-specific surface (≈120 ln together) and are unreachable from the default control set. |

---

## B. RE-POINT — the constant/flag is round-50-specific and must move, but the
## mechanism is load-bearing (do not delete the mechanism)

| # | file:line | item | v2 value / action |
|---|---|---|---|
| B1 | `c1-counter.py:374-380`, `404` | `CARRIERS`, `GAPRULE`, `AFTERDIR`, `ENTRY`, `STEM`, `CORE_HEADING`, `FRONTIER_MARK`, `COUNTER_PATH` | → `tools/round-51/…`, `corpus/evidence/round-51/c1`, the `2026-10-30-r51-…` entry, `## Round-51 additions to Core`, `Round-51 frontier note`, `tools/round-51/c1-counter.py`. |
| B2 | `c1-counter.py:393` | `OPENED_DATES = ('2026-10-28','2026-10-29')` | → `('2026-10-30',)` (a **single** day: the round-51 window). Note the v1 value was a *two-day* window; the `sourced` binding (`:2475`) tests `c[8] in OPENED_DATES`. **Measured**: S243/S244/S245/S249 are all opened `2026-10-28`, so the round-51 entry needs its **own** opened row(s) — the v1 window cannot be widened to cover both. |
| B3 | `c1-counter.py:396-397` | `PROV_BASE` | → `/fast/scratch/hyaku/kaidoku-r51/`. **BUT see D1** — this breaks the round-50 receipts the controls score. |
| B4 | `c1-counter.py:425` | `FROZEN_PREFIXES = ('tools/round-50/',)` | → `('tools/round-51/', 'tools/round-50/oracle/')` — the round-50 **oracle** tables are read by the v2 counter (as the oracle for the four re-scored carriers) so they must stay frozen, while the round-50 *instruments* must not be a frozen family. |
| B5 | `c1-counter.py:413-424` (`FROZEN_PATHS`) | freezes `plans/round-50-claims.md`, `tools/round-41/{fetch-vendor,sqfs-list}.py`, `tools/round-42/{prior-pins,rea-pkg}.json` | → `plans/round-51-claims.md`; keep the round-41/42 entries that still exist; the round-50 `carriers.json`/`gap-rule.json` join **only if** they are the frozen inputs (they are, per F1/F2). |
| B6 | `c1-counter.py:792`, `875` | `claim != 'R50-C1'` checks | → accept `('R50-C1','R51-C1')`: CTL-OLD scores the **round-50** rule and must parse. The draft v2 already does this (`:839`, `:922`). |
| B7 | `c1-counter.py:2514-2531` | the CLI surface | `--root/--rev/--freeze/--pkg65/--json-out/--unblob/--work/--carrier-cache/--rea-timeout/--no-rerun/--selftest/--selftest-rea/--dev-image/--verify-receipt` | **KEEP** all. `--no-rerun` is *not* dead weight: it is the documented "the predicate binds a fresh rerun" refusal, and `main()` returns exit 2 with a receipt for it. **ADD** `--gap-rule`, `--receipts` (already in the draft), and the `--controls` rule-scoped mode. |
| B8 | `c1-counter.py:2049-2076` | the counter's own retry (`MAX_REA_ATTEMPTS = 3`, no sleep) | **KEEP** — and per amendment F6 **extend** it to the REA `execution_failure`/ENOENT-inside-tree case. This is the one retry policy the port should have. |
| B9 | `c1-controls.py:67-109`, `368-461` | the controls' round-50 constants (`DEFAULT_BASE_REV` `:67`, `DEFAULT_FIXTURES` `:68`, `FOREIGN_SOURCES` `:106`, `K1_PATH` `:108`, `TEMPLATE_RECEIPT` `:109`, `LAST_ATTEMPTS` `:74`, `unblob_path` `:368`, `path_dirs` `:372`, `stripped_path` `:380`) | → re-point to round-51 paths. **But see D3**: most of the *live-capture* machinery (`capture_real` `:413`, `real_receipt` `:503`, `stripped_path` `:380`, `unblob_path` `:368`, the `npx` invocation at `:432`) exists to build real REA receipts — which the round-51 controls **no longer need**, because F2 makes the controls rule-scoped over *committed* envelopes. **That is a whole subsystem to drop.** |

---

## C. KEEP — load-bearing, do not drop

| # | file:line | item | why it must survive |
|---|---|---|---|
| C1 | `c1-counter.py:1458-1568` (`disposition_check`) | the three-family disposition check | **This is the whole round-51 mechanism.** **Measured** on the four committed round-50 envelopes (`tools/round-50/oracle/<id>.nonregular.tsv` + `corpus/evidence/round-50/c1/<id>/after.json`), with the v1 code *unmodified*: the round-50 frozen rule → `gaps_ok` **False** on g7581/g7582, **True** on c6490/c6430 (2 of 4 — the committed miss, reproduced). A law-shaped rule (`allowed[char-device/block-device/fifo/socket] = []`, `required['char-device'] = false`) → **4 of 4**. A 12-of-13 whitelist → still **red** on g7581/g7582 (the M50 partial-widening trap holds). The v1 `disposition_check` needs **no change** to express the law. |
| C2 | `c1-counter.py:1440-1456` (`silent_detail_matches`) | the per-detail silent matcher | KEEP — it is what makes the M50 partial-widening trap red, and the law-shaped rule makes it *unreachable* (no device detail listed) while leaving the `empty-target` symlink case intact. |
| C3 | `c1-counter.py:1572-1596` (`all_adds`, `is_ancestor`) | the receipt-freshness walk | KEEP, but see **D2**: it is the clause the round-50 receipts fail, by construction. |
| C4 | `c1-counter.py:1661-1725` (`frozen_drift`) + `448` (`FrozenPathChanged`) + `2576-2584` | freeze-drift detection and the **exit-2 gate** | KEEP — and the routed defect 3 ("v1 only reported drift") is **already satisfied**: **measured** by mutating `tools/round-50/gap-rule.json` after the freeze in a scratch fixture clone: `main()` exits **2** with `reason: frozen_path_changed` and `frozen_path_changed: ["tools/round-50/gap-rule.json"]`. The v1 counter already fails closed with a path-naming receipt. The port must **keep** this and add the selftest case the claim asks for. |
| C5 | `c1-counter.py:2094-2145` (`rederive_oracle`) + `992-1058` (`layout_probe`) + `1061-1068` (`provenance_ok`) + `1289-1333` | the byte-dependent clause helpers | KEEP — they are the *evidence* half of the counter. Note `provenance_ok` is the clause that breaks under the round-51 prefix (D1). |
| C6 | `c1-counter.py:1061-1068` + `:106-142` | `provenance_ok` / `trusted_run_root` | KEEP as the clause; see D1 for the porting conflict. |

---

## D. DO NOT INHERIT — three defects the v2 port must not carry over

These are the highest-value findings. Each is measured, not inferred.

### D1 (critical) — the round-51 provenance prefix makes every committed round-50 receipt fail `run_provenance_ok`

The v1 `PROV_BASE` (`:397`) is `/fast/scratch/hyaku/kaidoku-r50/`; the port's is
`/fast/scratch/hyaku/kaidoku-r51/` (B3). The four committed round-50 envelopes
carry `parameters.output_directory` under **kaidoku-r50**:

```
g7581 /fast/scratch/hyaku/kaidoku-r50/c1-run.uVY6Hs/extract   v1_base_ok=True  r51_base_ok=False
g7582 /fast/scratch/hyaku/kaidoku-r50/c1-run.GNUccw/extract   v1_base_ok=True  r51_base_ok=False
c6490 /fast/scratch/hyaku/kaidoku-r50/c1-run.GpkDyU/extract   v1_base_ok=True  r51_base_ok=False
c6430 /fast/scratch/hyaku/kaidoku-r50/c1-run.NqjdN2/extract   v1_base_ok=True  r51_base_ok=False
```

(measured by calling the v1 `provenance_ok` on each receipt's recorded
`output_directory` under both prefixes.)

The claim already names this — "the committed round-50 receipts fail
`run_provenance_ok` (round-50 provenance prefix)" — and answers it by making the
controls **rule-scoped** (F2), which evaluates *only* the disposition verdict.
**That answer is correct and the port's `--controls` mode implements it
(measured: LAW → exit 0, 4/4; the round-50 rule → exit 1, 2/4).** The trap for
the L1 is elsewhere:

> **The `--controls` mode must not evaluate the full predicate.** A single
> `PROV_BASE` constant cannot serve both the round-50 receipts (controls) and
> the round-51 receipts (data run). The claims' F2 text proposes `--provenance-base`
> and `--receipt-fresh-base` as flags (claims:126) — **the draft v2 does not
> implement either flag**; it avoids the problem by scoping the mode down
> instead. **Either is a valid answer; what is invalid is a `--controls` mode
> that runs the full predicate**, because it will report 0/4 for both rules and
> the kill rule ("CTL-NEW red … stop before the data run") would fire on a
> *measurement artefact* and kill a correct claim. **Recommendation: keep the
> draft v2's rule-scoped design, and make the rule-scope explicit in the
> receipt** (it already is: `disposition_ok`, `dispositions_matched`).

### D2 (critical) — `receipt_fresh` is false for the committed round-50 receipts, and the claim's counting command omits `--pkg65`

Measured with the v1 `all_adds` at the base rev `f04b51dd`:

```
g7581 all_adds = ['646d29c9df4ef77499248f95589cb9526c6dea19']
  is_ancestor(base, 646d29c9) = False      # the receipt was added BEFORE the freeze
  receipt_fresh computed by v1 = False
```

So under the v1 semantics the round-50 receipts are **not fresh** relative to
any round-51 freeze — they were added at `646d29c9`, an ancestor of the base.
`646d29c9` is exactly the commit the routed-defect list (claims:234) says was
never cited in LOG.md. **Consequence: any "score the committed round-50
receipts" control that evaluates `receipt_fresh` is red by construction.** The
rule-scoped `--controls` mode is the correct escape (it does not evaluate
freshness); the port must **not** try to make `receipt_fresh` true for them.

**Second, sharper finding on the same clause:** the claims' stated predicate
command (claims:87-88) is

```
python3 -I -B tools/round-51/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> \
  --receipts corpus/evidence/round-51/c1 --json-out <OUT>
```

— **no `--pkg65`** — while the draft v2's `main()` (`:2871`) still requires
`--pkg65` and exits 2 with `usage: --root --rev --freeze --pkg65 required`.
**Either the claim's command gains `--pkg65`, or the port makes `--pkg65`
optional (defaulting to `find_rea_pkg()`).** This is a one-line divergence
between the claim text and the instrument; the L1 must reconcile it **before the
freeze**, because the claim's predicate sentence and the counter's docstring are
required to be the same sentence.

Note also that `--receipts` (claims:87) is honoured **only** in the draft v2's
`--controls` mode (`:2861`); the main `measure()` path still resolves receipts
from the per-carrier `receipt` key or `AFTERDIR` (`:2353`). If the claim's
predicate command really intends `--receipts` to steer the main path, the port
must wire it there too. **KEEP-with-question for the L1.**

### D3 (high) — the round-50 controls driver is built around live REA capture; the round-51 controls are rule-scoped over committed bytes

The v1 controls driver's whole spine is *capture real REA receipts*:
`capture_real` (`:413`, `npx -y rea-agents@6.5.0` at `:432`), `real_receipt`
(`:503`), `stripped_path` (`:380`), `unblob_path` (`:368`), `path_dirs` (`:372`),
`mint_ids` (`:472`), `import_receipt` (`:981`), plus the whole `spec_c0..spec_c4`
/`spec_pos` builder family (`:788-1094`) whose fixtures are *planted sandbox
trees* (`make_sandbox` `:176`, `plant_and_commit` `:194`, `write_fixtures`
`:1159`, `load_fixtures` `:1192`, `stage_cache` `:1443`). Amendment F2 replaces
that with **rule-scoped verdicts over committed envelopes** — a different shape
of control entirely.

**Consequence for the port:** the v2 controls driver should be a much smaller
program — read a carriers table, read one named rule, read the committed
envelopes, evaluate the disposition verdict, exit 0/1/2 — and the
`capture_real`/`real_receipt`/`npx`/`stripped_path`/`import_receipt`/
`mint_ids`/`spec_c*` machinery **should not be ported**. Note the draft v2 has
**no** `tools/round-51/c1-controls.py` yet (`ls tools/round-51/` → `c1-counter.py`,
`c1-run.sh` only), so this decision is still open and is worth making
explicitly rather than by default.

**Caveat, stated honestly:** the claims still name `CTL-DN` ("the v2 counter
against a do-nothing fixture tree (no receipts) exits 1 or 2, never 0") and
`CTL-JUNK` ("scores 0 of 4, exit 1"). A *fixture tree* implies some planting
machinery survives. The minimal shape that satisfies both the rule-scoped
controls and CTL-DN is: the same `--controls` mode pointed at an **empty
receipts directory** (CTL-DN → nothing to score → not 0) and at a **junk rule**
(CTL-JUNK → the disposition check fails on every carrier). **No sandbox cloning,
no fixture planting, no REA.** Recommend that shape; it drops roughly half the
v1 controls driver.

### D4 (high) — `tools/round-51/carriers.json` does not exist, yet the claim and the draft both read it

`ls tools/round-51/` → `c1-counter.py`, `c1-run.sh`, `__pycache__/` — **no
`carriers.json`, no `gap-rule.json`, no `rea-pkg.json`, no `prior-pins.json`.**
But the draft v2's `CARRIERS = 'tools/round-51/carriers.json'` (`:409`) and
`GAPRULE = 'tools/round-51/gap-rule.json'` (`:410`), and `controls_mode` reads
`CARRIERS` at `rev` (`:2721`) and the rule at `rev` (`:2731`).

**Measured**: with the draft v2's `controls_mode` pointed at a scratch clone
that *lacks* `tools/round-51/carriers.json`, every invocation exits **2**
("carriers table tools/round-51/carriers.json absent"). After adding a
round-51 carriers table to the scratch clone, the same three rules scored
LAW → exit 0 (4/4), M1-13-whitelist → exit 0 (4/4), round-50 rule → exit 1
(2/4) as expected.

**Two things follow, and the second is a live defect:**

1. The four round-51 instruments the claim names must be *frozen* — the
   carriers table, the gap rule, the rea-pkg pin, the prior-pins document — and
   three of them do not exist yet. If they are not landed, the port cannot be
   frozen and the claim cannot be met.

2. **The M1 mutant (the all-thirteen whitelist) currently scores GREEN in the
   draft v2's `--controls` mode** (measured: `dispositions_matched: 4`, exit 0).
   The claim requires M1 to be **RED**, "red by the frozen rule-shape clause
   `law_shape_ok`". The draft v2 *does* implement `law_shape_ok` — but only in
   the `measure()` **bindings** path (`tools/round-51/c1-counter.py:2662-2678`,
   with `DEVICE_KINDS` at `:447` and the binding registered in `BINDINGS` at
   `:478`). **`controls_mode` (`:2703-2795`) never computes it**: the only
   clauses it evaluates are `receipt_present`, `gaps_ok`, `gaps_note`,
   `nonregular_unpublished_ok` and the derived `disposition_ok`
   (`:2762-2780`) — `grep -n "law_shape_ok"` returns **no hit inside
   `controls_mode`**. Since M1 is *intentionally* extensionally identical to the
   law over the measured data (C1 above: a 13-detail whitelist is green under
   `gaps_ok`), **the rule-shape clause is the only thing that can separate M1
   from the law — and the control mode does not evaluate it.**
   **This must be fixed before the freeze**: `controls_mode` must also require
   `law_shape_ok` (or the equivalent shape check) for its exit-0 verdict.
   *This is a finding about the draft, not the v1 — but it is the single most
   consequential thing in this audit, because the kill rule reads
   "any mutant green that should be red → stop before the data run".*

---

## E. KEEP-with-question — uncertain; flagged, not decided

| # | item | question for the L1 |
|---|---|---|
| E1 | `c1-counter.py:4630-4836` (`selftest_rea`, `lane_le_avm_image`) | A **real-REA** end-to-end selftest that builds a lane SquashFS with `mksquashfs`. Round-50-specific in that it asserts the round-50 provenance prefix. It is *not* reachable from `--selftest` (a separate `--selftest-rea` flag). **KEEP-with-question**: the wave forbids REA runs, so it cannot be exercised here — but it should not be silently dropped, because it is the only check that the *real* runner still agrees with the receipt. **I did not run it** (no REA permitted). |
| E2 | `c1-counter.py:1061-1068` `provenance_ok` + the `PROV_BASE` constant | Does the port need **two** accepted prefixes (round-50 for the controls' inputs, round-51 for the data run), or is the rule-scoped mode sufficient? The claim says the latter; the draft implements the latter. **Confirm.** |
| E3 | `c1-counter.py:2316-2317` (`receipt_fresh`) | Keep the clause as-is for the round-51 data run (the fresh receipts *are* added after the freeze), and rely on the rule-scoped mode for the round-50 inputs? Or add a `--receipt-fresh-base` flag (claims:126)? The draft does neither — it scopes the mode. **Confirm.** |
| E4 | `c1-controls.py:209-228` (`scrape`), `230-291` (`consts`) | The controls scrape the counter's constants **by AST, never importing**. This is deliberate and good (it lets one driver score several counters) — but it also means every **renamed** constant silently changes the controls' behaviour (`consts()` has round-50-specific fallbacks at `:243` (`2026-10-28`), `:245` (the `2026-10-28-r50-…` entry path), `:255` (`## Round-50 additions to Core`), `:256` (`Round-50 frontier note`)). **Those fallbacks must be re-pointed or removed** — a stale fallback would make the controls score the wrong paths and report a false green. |
| E5 | `c1-controls.py:1288-1381` (`judge`) + `:1256-1286` (`summarize`) | The expectation vocabulary (`exit`, `matched`, `doc_bindings_all_false`, `every_slot_fails`, `slot_fails_exactly`, `accept_refusal`, …) is tuned to the v1 control set. If the v2 controls are rule-scoped (D3), most of it is dead. **Keep only what the new control set uses** — but the shape (`expect` → `ok/why/diag`, fail-closed on an unknown clause) is worth keeping: it is why an unnamed clause can never read as a pass. |

---

## F. What the v1 counter's selftest already covers (so the port need not re-derive it)

The v1 selftest is ~1700 lines with ~150 cases and is **green** (the controls
selftest was run here: 20/20 pass, exit 0). Its cases that the round-51 port
must carry over, by name:

* **freeze drift** — `4222-4279`: `carrier bytes changed after freeze`,
  `oracle changed after freeze`, `nonregular table changed after freeze`,
  `carriers.json changed after freeze`, `gap-rule.json changed after freeze`,
  `gap-rule.json touched then restored`, `counter edited after freeze`,
  `claims edited after freeze`, `a new file under tools/round-50 after the
  freeze`, `rea-pkg pin edited after the freeze`, the two carried-over readers,
  `xpin tool edited after the freeze`, `oracle table first committed after the
  freeze is not frozen`, and the three merge-aware cases (`evil merge`, side
  branch, clean merge). **This is the routed-defect-3 selftest the claim asks
  for — it already exists in v1 and already passes** (C4).
* **the exact-vs-legacy path discriminator** — `3646-3690`, with
  `legacy_same_rel` (A3) as the falsification witness.
* **the structural-gap family** — `4310-4336`.
* **the projection-profile refusals** — `4339-4355`.
* **the provenance refusals** — `3311-3367` (`/kaidoku-r39/`, `..` climb,
  substring-only, the previous round's scratch, a relative path).

**Recommendation: port the v1 selftest as the v2 selftest and *edit* it, not
rewrite it** — then add the round-51-only cases the claim names (M1 red, the
M2 fourteenth-device green, the M3 partial whitelist red, and the freeze-drift
exit-2 case).

---

## G. Evidence index (all offline, no REA, no network)

| probe | what it established | where |
|---|---|---|
| `probe.py` | the v1 `disposition_check` unmodified → round-50 rule 2/4, law rule 4/4, 12-of-13 whitelist red | `S/probe.py` (run output in this report) |
| `probe2.py` | v1 `main()` exits **2** with `frozen_path_changed` on a mutated frozen path; `provenance_ok` false for all four round-50 receipts under a round-51 prefix | `S/probe2.py` |
| `probe3.py` | `run.json` has no `normalized_result`/`operation`/`provider`/`subject`/`parameters` — it is a **harness** receipt, not the envelope. The control input must be `after.json` (the claim says so at claims:113; confirmed here) | `S/probe3.py` |
| `probe4.py` | the v1 counter, measured at the base rev against the committed round-50 receipts: `receipt_fresh` **False** for all four (added at `646d29c9`, an ancestor of base) | `S/probe4.py` |
| draft-v2 `controls_mode` in a scratch clone | LAW → exit 0 (4/4); M1 13-whitelist → exit 0 (4/4) ← **defect D4.2**; round-50 rule → exit 1 (2/4) | `S/clone` (scratch only) |
| `git log --all --diff-filter=A` over `tools/round-4{9,50}/{prior-pins,rea-pkg}.json` | those four files **never existed** (A4, A5) | — |
| `git ls-tree -r 435d41fd -- tools/` | only `tools/round-42/rea-pkg.json` existed at the round-50 freeze (A5) | — |
| `awk` over `corpus/SOURCES.md` | S243/S244/S245/S249 all opened `2026-10-28` (B2) | — |

**Honest limits.** (i) I did **not** run the v1 counter's `--selftest` or
`--selftest-rea` (the latter needs REA, forbidden this wave; the former needs
`--pkg65` and executes the frozen `xpin` tool against the REA package, which
the no-REA rule forbids). The v1 selftest's greenness is therefore taken from
the committed round-50 receipts, not re-measured here. (ii) The v2 draft in
`tools/round-51/c1-counter.py` is a **sibling seat's uncommitted draft** — I
read it but changed nothing. (iii) Every change I recommend to the *lane tree*
is a recommendation to the L1; **this seat wrote nothing outside
`.ufo/waves/round-51/w1/SimpV1Audit/`**.

## H. Scratch cleanup

`/fast/scratch/hyaku/kaidoku-r51/w1-SimpV1Audit/` (probe scripts, the scratch
`git clone --shared`, the scratch rules and the `lane_le_avm_image` helpers)
was removed after the receipts above were recorded. The lane tree is unchanged:
`git status --porcelain` shows only the pre-existing `?? .ufo/waves/round-51/`
and the siblings' drafts — nothing this seat wrote.
