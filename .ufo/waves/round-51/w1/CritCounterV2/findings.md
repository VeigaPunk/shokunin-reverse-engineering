# CritCounterV2 — R51-C1 counter v2 design: pre-freeze findings

Seat: CritCounterV2 (critic, round 51 wave 1). Scope: attack the R51-C1 **v2 counter**
design against `{LANE}/plans/round-51-claims.md` §R51-C1 and the frozen round-50
instrument `{LANE}/tools/round-50/c1-counter.py` (4836 lines) plus the round-50
counter draft `.ufo/waves/round-51/w1/ExecCounterV2/c1-counter.py` (244 KB, a
byte-copy with edited constants).

All findings below are **measured**, not argued. Every probe is an offline
re-derivation against the committed round-50 receipts and oracle tables; **no REA
run, no network, no lane mutation**. Probe sources: `/fast/scratch/hyaku/kaidoku-r51/
w1-CritCounterV2/probe*.py` (removed at yield, per contract).

Axis impact: **coverage** (R51-C1's axis) for F1–F6, **calibration** for F7–F9.

> **Re-scope notice (2026-10-30, after concurrent amendment).** While this seat
> was probing, `plans/round-51-claims.md` was amended in the working tree
> (`git diff` shows +148/−36; the amendment record lists **CritRuleDerive F1–F11**,
> a *different* seat's attack round). This file was re-read against the amended
> text at 02:18. **F3, F6 and F7 below are now absorbed** by that amendment
> (the control input is now `after.json`, the drift gate is now stated as
> already present in v1, and `re_scored_pins` is now an explicit frozen
> allow-list). They are kept because the L1 must see the *measurements* that
> justify the amendment. **F2 survives in amended but weakened form and is restated
> as F2′** (the amended M1 mutant is green under the amended control verdict).
> **F13 is new** and is the most serious finding in this file: it is a defect in the
> *amended* text. F1, F4, F5, F8, F9, F10, F11, F12 are unaffected by the
> amendment and stand as written.

---

## F1 — The `247:0` allowance is not a Cable-class artefact: `dev/led 247:0` is on **all four** carriers, so the class distinction the derivation rests on is count-only (1 vs 13) over a **shared** node. (Severity: low after the amendment.)

**Claims text** (pre-amendment `plans/round-51-claims.md` §R51-C1): the round-50
rule's `removed.silent.char-device: ["247:0"]` "was generalised from the Cable class
(one char-device, `dev/led 247:0`) and leaves the FRITZ!Box class's twelve other
char-devices (`dev/pts/0-7 136:0-7`, `dev/tiatm 230:0`, `dev/ttyp0-2 3:0-2`) with
neither a matching gap nor a removal".

**Status after the amendment:** the phrase "generalised from the Cable class" has
been **removed** from the working-tree claims (verified: the string no longer
occurs), so the false attribution is fixed. The residual, still true and still
worth the L1's attention: the class split the derivation leans on is **count-only
(1 vs 13) over a shared node**, not a difference in which device details appear.

**Measured** (`probe2.py`, `probe3.py`; oracle tables `tools/round-50/oracle/*.nonregular.tsv`):

| carrier | char-devices in the frozen oracle | contains `dev/led 247:0` |
|---|---|---|
| c6430 (Cable) | **1** | yes |
| c6490 (Cable) | **1** | yes |
| g7581 (FRITZ!Box) | **13** | yes |
| g7582 (FRITZ!Box) | **13** | yes |

`dev/led 247:0` is present in **all four** carriers, so the round-50 rule's silent
allowance covers it everywhere. The FRITZ!Box unaccounted set is therefore the
other **twelve** — `dev/pts/0-7`, `dev/tiatm`, `dev/ttyp0-2` — exactly as the
claims enumerate. The claims' *enumeration* is right; **the claims' framing of the
`247:0` entry as "generalised from the Cable class" is false**: `247:0` is not a
Cable-class artefact at all, it is the one device node present in every carrier
(measured: all four tables contain `dev/led char-device 247:0`). This matters
because the claims make the *class distinction* the stated ground of the
re-derivation ("the class distinction is a property of the carriers' device
census, not of the rule"), and the measured census shows the classes differ by
**count only** (1 vs 13) with a **shared** device node, not by a Cable-specific
detail. A rule author who reads "generalised from the Cable class" may legitimately
conclude the R50 rule was *right* about `247:0` and only needs the other twelve
added — i.e. exactly the "all-thirteen whitelist" the claims themselves call a
cheat (they cite `MutC1Counter` F10 for it).

**Demand:** the claims' derivation paragraph must say that `dev/led 247:0` is
present on **all four** carriers and that the FRITZ!Box/Cable difference is a
count difference (13 vs 1) over a shared node; and the frozen rule must be derived
from the *producer's* behaviour (the law), not from either class's census.

---

## F2′ (restated against the amended claims) — **The amended M1 mutant is GREEN under the amended control verdict: the kill rule fires on a correct implementation.**

The amendment (CritRuleDerive F3/F4) fixed the *rule shape* — `allowed` for
device kinds is now the empty list and `required['char-device']` is now `false` —
and added a `law_shape_ok` clause plus a mutation set M1–M4. That is the right
shape. **But the amended control verdict is `(gaps_ok ∧ nonregular_unpublished_ok)`,
and `law_shape_ok` is in the *predicate*, not in the control verdict.** Measured
(`probe11.py`, the four committed round-50 envelopes, the amended rule shapes):

| mutant | amended claims require | `gaps_ok ∧ nonregular_unpublished_ok` | `law_shape_ok` |
|---|---|---|---|
| LAW (frozen round-51 rule) | green | **green** | True |
| **M1 all-thirteen whitelist** | **RED** | **GREEN** | False |
| M4a LAW + strict-subset whitelist | RED | **GREEN** | False |
| M4b `required=true` + strict subset | RED | RED | False |
| M3 `required=true` + `247:0` only | RED | RED | False |

**M1 is green on the amended control verdict** (measured: `gaps_ok` true on all
four carriers under the all-thirteen whitelist — the whitelist admits every
device row silently, so nothing is unaccounted). The claims' kill rule reads "any
mutant green that should be red → stop before the data run; report as a miss", so
a **correct** implementation, scored exactly as the claims' control verdict
specifies, **stops the round**. The same holds for **M4a**: the claims' M4 is
written as "a strict-subset whitelist stays red", but measured, the strict-subset
whitelist is green whenever `required` stays `false` — the whitelist is only
load-bearing when `required` is `true`.

The fix is one line of text: **the control verdict must include the shape
clause**, i.e. the controls score `(gaps_ok ∧ nonregular_unpublished_ok ∧
law_shape_ok)`, and M1/M4a must be stated as `required=true` + partial whitelist
(M4b/M3 shapes) or as "LAW + whitelist" with the whitelist's inertness stated
explicitly. Measured: `law_shape_ok` itself is well-defined and does separate the
law from the whitelist (it reads only the frozen rule: `silent[char-device]`
must be empty and `allowed[char-device]` must be the empty list) — it simply is
not in the verdict the claims say the controls score.

**Original F2 text (still true, and the amendment does not address it):** under
`required['char-device'] = False` the `removed.silent` whitelist is **unreachable
dead code** (`disposition_check` computes `need` and `continue`s before the
silent lookup, `tools/round-50/c1-counter.py:1552-1560`), so on the committed
corpus the law rule, `required=false + allowed=['unpublished-entry']` and
`required=true + silent=all-13` are **all green on all four carriers** — no
receipt gives any char-device a disposition (measured: the only path-bearing gap
kind across all four carriers is `unpublished-entry`, and every gap resolves to a
symlink). Only the new `law_shape_ok` clause and the new M2 fixture
(a fourteenth, unlisted device) separate them — **both are therefore load-bearing
and must be in the verdict**, which is exactly what F13 demands.

## F2 (original, now partly absorbed) — **The law-derived rule makes the claims' two required red mutations inert.** A counter that cannot go red on the specified mutants does not test the law.

The claims require these rule mutations to be **red**:

> "requiring char-device dispositions (`required.char-device=true`) and whitelisting
> only `247:0` reproduces the round-50 miss (red); whitelisting a strict subset of
> the thirteen stays red (the M50 partial-widening trap, `MutC1Counter` F10)."

**Measured** (`probe10.py`, against the real g7581 receipt, no fabricated data):

| rule | `gaps_ok` | claims require |
|---|---|---|
| LAW (required=false, allowed=[]) | **True** | green |
| LAW + strict-subset whitelist (`247:0`,`136:0`) | **True** | **RED** |
| LAW + whitelist only `247:0` | **True** | **RED** |

**Why:** `disposition_check` computes `need = required.get(kind, bool(allowed.get(kind)))`
and `continue`s when `need` is false — **before** the `removed.silent` lookup is ever
reached (`tools/round-50/c1-counter.py:1552-1560`). Under the law shape
(`required['char-device'] = False`) the `removed.silent.char-device` whitelist is
**unreachable dead code**: adding, narrowing, or deleting it cannot change
`gaps_ok`. Both specified red mutations are therefore **green**, and the claims'
kill rule ("any mutation green that should be red → stop") would fire on a
*correct* rule.

**This is the sharpest finding in the review: the claims' own mutation battery
certifies a rule that cannot distinguish the law from a cheat.** Measured
discriminability (`probe4.py`, `probe7.py`) — three rule shapes, all green on the
committed corpus:

| shape | g7581 gaps_ok | verdict |
|---|---|---|
| LAW `required=false, allowed=[]` | True | intended |
| CHEAT `required=false, allowed=['unpublished-entry']` | True | **indistinguishable** |
| CHEAT `required=true, silent=all-13` | True | **indistinguishable** |

The corpus cannot tell the law from the cheats because **no receipt in the corpus
gives any char-device a disposition** (measured: the only path-bearing gap kind
across all four carriers is `unpublished-entry`, and every gap resolves to a
symlink; `probe6.py`). The law is only falsifiable by a **synthetic fixture** in
which a char-device *does* carry a disposition — which the claims never mention.

**Demand (all three):**
1. The claims' mutation battery must be **rewritten against the law's actual
   shape**: the two "strict-subset whitelist" mutations must become mutations that
   put a char-device *back under a required kind* (i.e. `required['char-device']
   = true` with a *narrow* `silent` list) — that is the only shape in which the
   whitelist is live and can go red. Under the current text the battery cannot be
   satisfied by any law-shaped rule.
2. The counter's selftest must add a **discriminating fixture**: a receipt whose
   oracle contains a char-device **with** an `unpublished-entry` gap, asserting
   `gaps_ok == False` under the law rule. Without it the counter cannot
   distinguish the law from either cheat (measured above) and the claim's
   "law, not a detail whitelist" language is unfalsifiable by the instrument.
3. The frozen rule must keep `allowed['char-device']` as a **present key with an
   empty list**, not delete it: `gap_rule_ok` computes
   `uncovered = kinds_seen - set(model['allowed'])` and the carriers' kinds are
   `{char-device, dir, symlink}` (measured, `probe6.py`), so deleting the key makes
   `gap_rule_ok` **False** and the claim exits 1 on a binding, not on a gap.

---

## F3 — **ABSORBED by the amendment** (the control input is now `after.json`; the measurement below is the justification). **The claims' control design scored the wrong artefact.** The named receipts (`run.json`) are harness metadata, not REA envelopes; the counter reads `after.json`.

The claims name the control input as `corpus/evidence/round-50/c1/<id>/run.json`
(§R51-C1 "Pre-freeze controls": "scored with the v2 counter against
`corpus/evidence/round-50/c1/<id>/run.json` receipts and the round-50 oracle
tables"; and the predicate command's `--receipts corpus/evidence/round-51/c1`).

**Measured** (`probe9.py`): `run.json` has **no** `subject`, **no**
`normalized_result`, **no** `evidence_id`. The REA envelope the counter consumes is
`after.json` (the `data` object). Every receipt-derived clause
(`evidence_envelope_ok`, `subject_pin_ok`, `operation_ok`, `handler_ok`,
`chunks_ok`, `oracle_hits_ok`, `gaps_ok`, `evidence_id_ok`) reads the envelope's
`data` object — pointing the counter at `run.json` makes all of them fail and
`carriers_matched` 0, i.e. **CTL-NEW would be red for a file-shape reason, not a
rule reason**, and the kill rule ("CTL-NEW red … → stop") would stop the round.

**Demand:** the claims' control paragraph must name `after.json` (or "the REA
envelope `<id>/after.json`", never `run.json`), and the counter's `--receipts`
mode must state that it reads `<dir>/<id>/after.json`.

---

## F4 — **The frozen-walk is mis-scoped in the round-51 draft: the oracle producers and the round-50 tree are not frozen, and `tools/round-50/` is only half-frozen.**

The seat brief asks specifically: *should `tools/round-41/sqfs-list.py` and the
round-27 oracle producers be in the walk? the oracle tables were produced by them.*

**Measured** (`tools/round-50/c1-counter.py:413-425` vs the round-51 draft
`.ufo/waves/round-51/w1/ExecCounterV2/c1-counter.py:413-419`):

| frozen input | v1 (round-50) | draft (round-51) |
|---|---|---|
| `tools/round-41/sqfs-list.py` (2nd reader) | **frozen** | **DROPPED** |
| `tools/round-41/fetch-vendor.py` (fetcher) | **frozen** | **DROPPED** |
| `tools/round-27/xpin-attribute.mjs` (`XPIN`) | **frozen** | **DROPPED** |
| `tools/round-42/prior-pins.json` | **frozen** | **DROPPED** |
| `tools/round-42/rea-pkg.json` | **frozen** | **DROPPED** |
| `plans/round-50-claims.md` | frozen | replaced by round-51 ✓ |
| `tools/round-50/` prefix | **whole prefix** | **only `tools/round-50/oracle/`** |

The draft's `FROZEN_PATHS` is `('plans/round-51-claims.md', 'tools/round-50/carriers.json',
'tools/round-50/gap-rule.json')` and `FROZEN_PREFIXES = ('tools/round-51/', 'tools/round-50/oracle/')`.

**Why it matters, three measured consequences:**
- `tools/round-41/sqfs-list.py` is the **producer of the frozen oracle tables**
  (the round-50 run harness's `oracle` arm invokes it; the tables in
  `tools/round-50/oracle/` are its output). If it is not frozen, the counter
  verifies a *table* whose **producer is mutable** — the v1 selftest already had a
  case for this ("carried-over second reader edited after the freeze" → exit 2,
  `tools/round-50/c1-counter.py:4258`). The draft drops that protection.
- `tools/round-27/xpin-attribute.mjs` (`XPIN`) is **read at the freeze** by
  `evidence_ids()` to recompute every receipt's evidence id
  (`tools/round-50/c1-counter.py:669-670`) — an unfrozen `XPIN` means the
  evidence-id check reads a mutable tool. (`XPIN` is still *named* in the draft's
  constants, so it is read — just not frozen.)
- The draft's `tools/round-50/` freeze is **partial**: `tools/round-50/carriers.json`
  and `gap-rule.json` are named, but `tools/round-50/c1-counter.py` (the round-50
  counter the claims' before-arm cites) and `tools/round-50/c1-run.sh` are not, and
  the `tools/round-50/` **prefix** is gone, so any *new* file under it is not drift.

**Demand:** the round-51 frozen path set must carry the v1 carried-over inputs
(`tools/round-41/sqfs-list.py`, `tools/round-41/fetch-vendor.py`,
`tools/round-27/xpin-attribute.mjs`, `tools/round-42/prior-pins.json`,
`tools/round-42/rea-pkg.json`) **and** the whole `tools/round-50/` prefix
(the round-50 counter and run harness are the before-arm's instruments and the
carrier table's producer), plus `tools/round-41/fetch-vendor.py` for the new
`tools/round-51/fetch-vendor.py` it ports. Also freeze
`tools/round-50/c1-counter.py` explicitly: the claims' before-arm is that file's
round-50 receipt.

**Note (not a finding against the claims, a correction):** the claims never
mention the oracle producers. The frozen-walk choice is therefore unspecified, and
the draft resolved it by omission. This finding closes that gap.

---

## F5 — **PARTLY ABSORBED** (the amendment adds `--provenance-base`/`--receipt-fresh-base`, fixing the round-50/round-51 tree confusion; the path-traversal half is OPEN). **The `--receipts` directory parameter is an unauthenticated substitution channel: the wrong-tree confusion between the round-50 and round-51 evidence trees is uncaught, and a path-traversal is unguarded.**

The claims' predicate is `--receipts corpus/evidence/round-51/c1` (a
**directory**, relative to the CWD), and the controls score "the committed
round-50 receipts". Two distinct trees.

**Measured problems:**

1. **Wrong-tree confusion is structurally uncaught.** The v1 counter reads receipts
   from the **git tree at REV** (`show(root, rev, rpath)`,
   `tools/round-50/c1-counter.py:2302`) — a *repo-relative* path resolved inside the
   lane. A v2 that takes `--receipts <dir>` from the command line and reads it from
   the **filesystem** breaks that binding: the receipts would come from wherever the
   operator pointed, not from the committed tree at REV. Nothing in the v1 design
   checks that the receipt file read is the one committed at REV.

2. **Path traversal is unguarded.** `--receipts` with no normalisation accepts
   `--receipts ../../etc`, `--receipts /abs/path`, or a symlinked directory. The v1
   helpers `under_root` / `path_shape_ok` exist for *receipt paths inside a receipt*;
   the new **directory** parameter bypasses them entirely.

3. **The provenance prefix makes the confusion silently fatal.** Measured
   (`probe9.py`): every round-50 receipt's `parameters.output_directory` begins
   `/fast/scratch/hyaku/kaidoku-r50/`, but the round-51 `PROV_BASE` is
   `/fast/scratch/hyaku/kaidoku-r51/` → `run_provenance_ok` is **False** for all
   four round-50 receipts under a round-51 counter. So pointing a round-51 counter
   at the round-50 tree does not fail loudly at the tree level — it fails on a
   clause that also fails for the *right* tree (the fresh round-51 receipts are
   made under `kaidoku-r51/`), so the two failure modes are indistinguishable in the
   receipt.

**Demand:**
- `--receipts` must be a **lane-relative** path, normalised with `realpath`/
  `os.path.normpath`, **rejected** if it is absolute, contains `..`, or resolves
  outside the lane root; and the counter must require it to be exactly the tree
  named by the frozen `carriers.json` receipt paths (or a declared control tree).
- The receipt must record the **resolved absolute** receipts tree plus each
  receipt's sha256, so a run against the round-50 tree is distinguishable in the
  receipt from a run against round-51.
- The controls must pin which tree each control reads, and the two must differ
  **only** in the rule (CTL-OLD vs CTL-NEW), not in the provenance prefix — i.e.
  the round-51 counter must accept the round-50 provenance prefix *in control mode
  only*, and say so in the receipt.

---

## F6 — **ABSORBED by the amendment** (the claims now state that v1 already exits 2 on `frozen_path_changed`; the measurement below is the justification). **The freeze-drift gate already exists and already fails closed; the claims mis-describe v1 and the draft's selftest requirement is satisfiable only with a real fixture clone.**

The claims say: "the v1 counter **only reported drift**; a selftest case must
demonstrate exit 2 on a fixture clone with a mutated frozen byte". The routed
defect (`plans/round-51-claims.md`, "Freeze-drift gating") frames the same as new
work.

**Measured** (`driftclone` fixture, `git clone --shared` at
`f04b51dd…`, mutated `tools/round-50/gap-rule.json`, then added
`tools/round-51/extra.py`):
- `frozen_drift(freeze, freeze)` → `[]`;
- after mutating a frozen path → `['tools/round-50/gap-rule.json']`;
- after adding a file under the `tools/round-51/` prefix →
  `['tools/round-50/gap-rule.json', 'tools/round-51/extra.py']`;
- `measure()` on the drifted tree raises `Unevaluable` with
  `reason='frozen_path_changed'` → the CLI path returns **exit 2** with
  `frozen_path_changed` naming the path
  (`tools/round-50/c1-counter.py:2199-2202`, `2571-2577`).

So **the v1 counter already fails closed with exit 2** and already names the path;
the claims' "only reported drift" is **false as written** (v1 both reports *and*
gates). The genuinely missing piece is only the **selftest case**.

**Demand:** correct the claims' description (v1 already gates at exit 2; the
routed defect is *unverified*, not *absent*), and keep the selftest requirement —
but make it specific: the fixture clone must mutate **one byte of one frozen path
under the round-51 prefix** and assert exit 2 **and** that `frozen_path_changed`
names that exact path. Also assert the **negative**: mutating a **non**-frozen path
must **not** trip the gate (the v1 selftest lacks this direction — measured: the
draft's walk freezes `tools/round-51/` wholesale, so *any* file added there is
drift, including a harmless one).

**Drift-vs-do-nothing confusion (the seat brief's question):** the claims' CTL-DN
says "the v2 counter against a do-nothing fixture tree (no receipts) exits 1 or 2,
never 0". Exit 2 is the **could-not-evaluate** code (contract: "0 met/clean, 1
not met/violation, 2 could-not-evaluate") — and exit 2 is **also** what the drift
gate returns. So a control harness that reads only the exit code cannot tell
"drift detected (violation)" from "cannot evaluate (environment)". **Demand:** the
drift receipt must be distinguishable by **content** (`reason: frozen_path_changed`
plus a non-empty `frozen_path_changed`), and the controls must assert on that
field, not on the exit code alone; and CTL-DN's expectation should be pinned to
**exit 1** (a measured semantic red) with exit 2 allowed only for the drift
control, so a drift cannot be scored as a do-nothing red.

---

## F7 — **ABSORBED by the amendment** (a frozen `re_scored_pins` allow-list now exists; the measurement below is the justification). **`carrier_fresh_ok` collides with the claim: the four round-51 pins are the four round-50 pins, so the freshness clause is a self-inflicted zero unless the claim states the exemption.**

The claims re-run **the same four carriers** (the pins are identical — measured:
`tools/round-50/carriers.json` pins == the round-50 receipt's carriers). The v1
clause `carrier_fresh_ok` says: "the pin is not one a previous C1 freeze already
scored" (docstring `tools/round-50/c1-counter.py:119-122`), and the sources it
reads are `PRIOR_CARRIER_TABLES` + `PRIOR_PIN_CANDIDATES`
(`tools/round-50/c1-counter.py:386-390`).

**Measured** (`probe9.py`): the round-50 receipt's `prior_pins` (18 pins) contains
**none** of the four round-50/51 pins, and `prior_pin_sources` were
`.ufo/waves/round-41/c1/carriers.json`, `tools/round-49/carriers.json`,
`tools/round-42/prior-pins.json` — the round-50 carriers table was **not** among
them, because round 50 was the freeze that first scored them.

**The trap:** the honest round-51 walk must add `tools/round-50/carriers.json` to
`PRIOR_CARRIER_TABLES` (it is a previous C1 freeze's carrier table — the v1 code
reads exactly this kind of file for rounds 41 and 49). Doing so makes **all four
round-51 pins prior** → `carrier_fresh_ok` False on every carrier →
`carriers_matched` 0 → **the claim's target of 4 is unreachable**. Not adding it
means the freshness clause is silently defeated for the one round where it is
most meaningful (a re-freeze of the same carriers).

**Demand:** the claims must state explicitly that R51-C1 is a **re-freeze of the
same four already-scored pins** and that `carrier_fresh_ok` is therefore
**exempted for these four ids by name** (or the clause is redefined as
"not scored by a *different* C1 freeze under a *different* rule"), and the counter
must implement the exemption **by carrier id**, not by silently omitting the
round-50 table. A receipt that shows `carrier_fresh_ok` green against an
unspecified prior set is not evidence.

---

## F8 — **ABSORBED by the amendment** (the parser now accepts `{R50-C1, R51-C1}`; the measurement below is the justification). **The claim-label constant is a tripwire: the frozen rule and carriers table must keep `"claim": "R50-C1"` or the counter's own model rejects them.**

The draft's `gap_rule_model` and `carriers_spec` both test the literal `'R50-C1'`
(draft lines 786-787 and 869-870; unchanged from v1). **Measured** (`probe9.py`
and the rule-model probe): a rule labelled `"claim": "R51-C1"` yields
`probs = ["claim 'R51-C1' != R50-C1"]` → **`gap_rule_ok` False** → the counter
exits 1 on a *binding* with the carriers matched. Likewise `carriers_spec` returns
`["claim 'R51-C1' != R50-C1"]` → `carriers_spec_ok` False → exit 1.

So the frozen round-51 rule and carriers table are forced to carry
`"claim": "R50-C1"` — a **false provenance stamp** on round-51 artefacts (the same
trap the claims' own `frontier_note`/`sourced` binding machinery exists to
prevent), *or* the counter must be edited to accept `R51-C1`, in which case the
claim-label string is a **binding** that must be stated in the claims.

**Demand:** the counter must accept the round-51 label and the claims must name
the label as part of the frozen constant set (`claim: "R51-C1"`), with the
round-50 label kept accepted only for the round-50 tables. If the label stays
`'R50-C1'`, the round-51 artefacts carry a false provenance stamp and the
`gap_rule_ok` binding is measuring a string, not the rule.

---

## F9 — **The `sourced` binding cannot check the claims' required citations: `OPENED_DATES` excludes S243/S244/S245/S249, and the binding is existential (any one S-id), not the required set.**

The claims require the entry to "cite S243/S244/S245/S249 **and** the round-51
SOURCES row(s) opened this round". The draft sets `OPENED_DATES = ('2026-10-30',)`.

**Measured** (`probe9.py` + `corpus/SOURCES.md`): S243, S244, S245 and S249 are all
**opened 2026-10-28** — *not* in the round-51 window. The v1 `sourced` binding
requires `c[8] in OPENED_DATES` (`tools/round-50/c1-counter.py:2475`), so those
four rows can **never** satisfy it. Two further defects in the same binding:
- it is **existential** (`b['sourced'] = bool(ok_ids)`) — the entry citing **one**
  qualifying row satisfies it; the claims require a **set** of four;
- it checks the SOURCES row's `used-by` contains the entry, but **not** that the
  entry's `source:` lines cite **those specific** ids — so an entry citing an
  unrelated 2026-10-30 row passes while omitting S243/S244/S245/S249 entirely.

**Demand:** the round-51 `sourced` binding must (a) accept the round-50-window
rows the claims require (S243/S244/S245/S249, opened 2026-10-28) **and** the
round-51 rows, and (b) check the **required id set** is present in the entry's
`source:` lines — not merely that one qualifying id exists.

---

## F10 — **The selftest list has a hole that lets a broken counter pass: no selftest case exercises the `char-device` kind at all.**

The v1 selftest has **154** `add(...)` cases (measured) — but the fixture oracle
rows use the kind **`'device'`** (`tools/round-50/c1-counter.py:2919`, `2945`,
`3818`, `3996`), while the **real** oracle tables use **`char-device`**
(measured: 28 `char-device` rows across the four tables; the string
`'char-device'` appears only twice in the whole counter file). The v1 selftest
therefore **never** exercises the real kind name, the real `removed.silent` detail
matching (`247:0`), or the real `required`/`allowed` shape for device nodes.

**Demand — the missing selftest cases the v2 must add (each named by what it
kills):**
1. **`char-device` kind present** (the real vocabulary) — kills a counter whose
   kind handling works only for `'device'`.
2. **a char-device with a disposition** → `gaps_ok` False under the law rule —
   kills the F2 cheats (the discriminating fixture).
3. **`gap_rule_ok` with `char-device` key deleted from `allowed`** → binding False —
   kills the "delete the key" reading of the law.
4. **rule labelled `claim: "R51-C1"`** → accepted, `gap_rule_ok` True — kills F8.
5. **drift on a fixture clone** (mutate one byte under the round-51 prefix) →
   exit 2 **and** `frozen_path_changed` names that path — kills F6.
6. **a non-frozen path mutated** → exit 0 (no false drift) — kills the over-broad
   walk (the draft's whole-`tools/round-51/` prefix).
7. **`--receipts` path traversal / absolute / outside-lane** → rejected, non-zero —
   kills F5.
8. **`carrier_fresh_ok` exemption** for the four round-51 ids against the round-50
   prior table → green **and** an unrelated id → red — kills F7.
9. **`sourced` with the required id set** → green; with one id missing → red —
   kills F9.
10. **`gaps_ok` on a `fifo`/`socket`** — the corpus never contains them (measured:
    the only kinds present are `char-device`, `dir`, `symlink`), so the law's
    `fifo`/`socket` clause is **untested** by the corpus and must be tested by a
    fixture or the claim must not assert it (see F11).

**Status against the amendment.** The amendment (CritRuleDerive F4/F10) adds the
M1–M4 mutants and the drift selftest case, which cover demands 5 and (partly) 2
of the list above. **Eight demands remain uncovered**, and one *new* gap is
created by the amendment's own M2:

> **M2 is not the case this seat demanded.** M2 ("a fixture carrier whose
> non-regular census carries a fourteenth, unlisted device … must be GREEN under
> the law rule and RED under any detail whitelist") is a **census** case: the
> fourteenth device row is *unaccounted* under a whitelist and *silently admitted*
> under the law (measured: `need=false → continue`). It therefore **does**
> discriminate the law from a whitelist — good — but it tests only the law's
> *"a device row needs no disposition"* half. It does **not** test the law's
> other half, which the amendment itself states: "a gap landing on a device row
> is a violation of the law … a future extractor that starts emitting a device gap
> turns the rule **red** (fail closed)". That case needs a **receipt whose gap
> names a device row** — measured **red** under the law rule (`allowed[char-device]
> = []`) and **green** under the permissive cheat (`allowed[char-device] =
> ['unpublished-entry']`), i.e. it is the only construction that separates the law
> from the *permissive* rule the amendment's own `law_shape_ok` clause would
> also reject. **It is not in the amended mutation set.** Add it as M5.

The eight still-uncovered demands, restated as the amended selftest list:
**(a)** a fixture using the **real** kind vocabulary `char-device` (the v1
fixtures use the fictional `'device'`, so nothing tests the production kind);
**(b)** M5 — a receipt whose gap names a device row → red under the law rule and
green under `allowed[char-device]=['unpublished-entry']`; **(c)**
`gap_rule_ok` with the `char-device` key **deleted** from `allowed` → binding
false (measured: `uncovered=['char-device']`); **(d)** a **non-frozen** path
mutated → **no** drift (the draft's whole-`tools/round-51/` prefix makes any
added file there drift); **(e)** `--receipts` absolute / `..` / outside-lane →
rejected non-zero; **(f)** the `re_scored_pins` exemption: the four round-51 ids
green against the round-50 prior table, an unrelated id red; **(g)** `sourced`
with the required id set → green, one id missing → red; **(h)** a `fifo`/`socket`
device row → the law's arm exercised.

---

## F11 — **ABSORBED by the amendment** (the law is now stated to the measured width). **The law's scope exceeded the corpus: `fifo`, `socket` and `block-device` never occur, so the rule's arms for them are unfalsified; and the claims assert a producer property the counter cannot observe.**

The claims' law: "a char-device/fifo/socket oracle entry is expected to carry no
disposition at all". **Measured** (`probe10.py`): the non-regular kinds present
across all four carriers are exactly **{char-device, dir, symlink}** — `fifo`,
`socket` and `block-device` occur **nowhere**. Two consequences:
- a rule that *allowed* `fifo`/`socket` dispositions would score green on all four
  carriers (no fixture can distinguish it) — the law's arms for those kinds are
  **unfalsified by the corpus**;
- the claims also assert the law's *ground* ("the extraction producer creates no
  device nodes … an unprivileged extraction cannot `mknod`") — a property of REA /
  unblob, not of the counter's data. The counter observes only the **absence of a
  disposition**, which is consistent with the law but also with an extractor that
  silently dropped a device node it should have reported.

**Demand:** the claims must scope the counter-verified claim to the kinds the
corpus exercises (char-device) and attribute the producer-property half to the
cited source rows (S243/S245/S249), naming the counter's role as *testing the
rule, not the producer*. Any `fifo`/`socket` arm must be either backed by a
fixture or explicitly marked not-measured.

---

## F12 — Minor: the claims' before-arm command and the round-51 predicate are not the same measurement, and the "before" receipt is a round-50 file the L1 cannot re-measure.

The claims' counting command is "the predicate command, run once at the landing REV
(after) with the committed fresh receipts; the before-arm is the committed round-50
receipt named above plus CTL-OLD". The committed round-50 receipt is
`.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` (measured: `exit_code 1`,
`carriers_matched 2`, `failing = ['g7581:gaps_ok','g7581:projection_ok','g7582:gaps_ok']`).
That file records the round-50 counter's argv, which included `--pkg65` and
`--carrier-cache` — arguments the round-51 predicate command does **not** carry
(the claims' predicate is `… --root --rev --freeze --receipts --json-out`). The
before-arm and the after-arm therefore differ in **more** than the rule.

**Demand:** the claims must state that the before/after arms differ in the rule
(and in the receipts tree), and that the before-arm is the *committed* round-50
receipt (not a re-measurement this round) — or the difference must be enumerated
explicitly so the comparison is honest.

---

## F13 — **The amended control verdict does not contain the clause the amended mutation set depends on: M1 (the all-thirteen whitelist) is GREEN under `(gaps_ok ∧ nonregular_unpublished_ok)`, so the kill rule fires on a correct implementation.** (See F2′ for the measurement; this finding is the demand.)

**Measured** (`probe11.py`, the four committed round-50 envelopes, the amended
rule shapes): the amended M1 mutant — `required['char-device'] = true` with
`removed.silent.char-device` naming all thirteen observed details — has
`gaps_ok` **true on all four carriers** (the whitelist admits every device row
silently, so nothing is unaccounted) and `nonregular_unpublished_ok` true, hence
**green** under the amended control verdict. `law_shape_ok` is **false** for M1
(measured: it reads `silent['char-device']` and finds all thirteen details). The
claims put `law_shape_ok` in the **predicate** ("`law_shape_ok true` … wave-1
amendment F4"), not in the **control verdict** ("the two rule controls evaluate
the frozen **disposition verdict** (`gaps_ok` ∧ `nonregular_unpublished_ok`)").
The kill rule — "any mutant green that should be red → stop before the data run;
report as a miss" — is applied to the control verdict.

**Consequence:** a counter that implements the amended rules exactly will score
M1 green on the control verdict, the kill rule fires, and the round stops as a
miss — **for a correct implementation**. The measurement is symmetric and
decisive: the *only* clause that separates the law from the all-thirteen
whitelist is `law_shape_ok`, so it must be inside the verdict the mutants are
scored by.

**Demand (the smallest safe correction):**
1. the control verdict becomes `(gaps_ok ∧ nonregular_unpublished_ok ∧
   law_shape_ok)` — or, equivalently, the mutants are scored by the **predicate's**
   clause set, not a narrower one; and
2. the amended M4 must be stated as `required=true` + strict-subset whitelist
   (M4b, measured red) or as "LAW + whitelist", in which case the amendment
   must say the whitelist is **inert** under `required=false` and that its
   redness comes from `law_shape_ok` alone; and
3. the M2 fixture the amendment added (a fourteenth, unlisted device) is
   **load-bearing** and must be asserted in the frozen control fixtures, because
   measured, it is the only construction on which the law and a detail whitelist
   differ *by data* rather than by rule shape.

---

## F14 — **The amendment's `--gap-rule` override breaks the receipt's rule provenance: the receipt can report `gap_rule_unchanged true` and `gap_rule_ok true` while the disposition verdict came from an unpinned rule file.**

The amendment mandates four round-sensitive flags on the v2 counter:
`--gap-rule`, `--receipts`, `--provenance-base`, `--receipt-fresh-base`
(`plans/round-51-claims.md` §R51-C1, "Pre-freeze controls"). `--gap-rule` is
needed because CTL-OLD scores the round-50 rule and CTL-NEW the round-51 rule.

**Measured** (`probe12.py`, reading the v1 `measure()` body): in v1 the rule comes
from the **frozen path**, never from a scored file —
`plan_raw = show(root, freeze, GAPRULE)`; `model, plan_probs = gap_rule_model(plan_raw)`;
`res['gap_rule_unchanged'] = show(root, rev, GAPRULE) == plan_raw`. So:

- `gap_rule_unchanged` compares the **frozen path's** bytes at rev vs freeze — it
  says nothing about the file the override actually used;
- the `gap_rule_ok` **binding** is computed from `uncovered = kinds_seen -
  set(model['allowed'])` where `model` is parsed from the **frozen** rule, not the
  override;
- the receipt carries **no** rule-file sha256 (measured: the counter's receipt
  keys contain no `gap_rule_sha256`/`gap_rule_path`; `counter_sha256` covers the
  *counter* file only).

So under `--gap-rule <file>` the receipt can carry `gap_rule_unchanged: true` and
`gap_rule_ok: true` — both statements about the **frozen** rule — while the
**disposition verdict** (`gaps_ok`) came from a file that was never pinned,
hashed, or recorded. A control driver that scores the disposition verdict cannot
tell from the receipt which rule produced it.

**Demand:** the v2 receipt must name the rule file it actually applied and its
sha256 (`gap_rule_path`, `gap_rule_sha256`), the `--gap-rule` override must be
**rejected unless** the path is inside the lane and the file's bytes are
recorded, and `gap_rule_unchanged` / `gap_rule_ok` must be computed against **the
rule that was applied** (not the frozen path's) whenever an override is in
force. This is the seat brief's "rule-override masking a stale rule bytes pin"
question, answered: **yes, it can go unnoticed today.**

## F15 — **Three of the claims' landing bindings have no v1-shaped check at all, and the Frontier → Core promotion itself is unverified: the v1 `frontier_note` binding cannot distinguish "promoted" from "not promoted".**

The claims' R51-C1 "Landing bindings" list requires (all true at the landing REV,
"each re-derivable by the counter"): the entry exists; cites S243/S244/S245/S249
**and** the round-51 SOURCES rows; **names the fresh receipts**; `PROVINCE.md`
carries `## Round-51 additions to Core` with the LE members row and an updated
frontier note (**LE `hsqs` leaves the Frontier list**); the README coverage map
row; SOURCES `used-by`; the **SCORECARD coverage head names 141/141**; a **LOG
entry**.

**Measured** against the v1 binding set (9 bindings: `province_core_section`,
`province_core_row`, `frontier_note`, `entry_present`, `sourced`,
`coverage_map_row`, `carriers_spec_ok`, `gap_rule_ok`, `frozen_tables_valid`):

| claims' landing binding | v1 binding that checks it |
|---|---|
| entry exists | `entry_present` ✓ |
| cites S243/S244/S245/S249 **and** the round-51 rows | `sourced` — **existential, and the window excludes the four ids** (F9) |
| **names the fresh receipts** | **NONE** — no receipt-path check in the entry |
| `## Round-51 additions to Core` | `province_core_section` ✓ |
| the LE members row | `province_core_row` ✓ |
| **LE `hsqs` leaves the Frontier list** | `frontier_note` — **cannot check removal** (below) |
| README coverage map row | `coverage_map_row` ✓ |
| SOURCES `used-by` | `sourced` ✓ |
| **SCORECARD coverage head names 141/141** | **NONE** — `SCORECARD` referenced **0** times in the counter |
| **LOG entry** | **NONE** — `LOG.md` referenced **0** times in the counter |

**The promotion is the claim's substance and it is unverified.** Measured
(`probe13.py`): the v1 `frontier_note` predicate is
`any(FRONTIER_MARK in l and STEM in l and LE_AVM_RE.search(l.replace(STEM,'')) for l in prov_text.splitlines())`
— a note line existing **anywhere** in `PROVINCE.md`. Run against two
hypothetical `PROVINCE.md` texts that differ **only** in whether the Frontier
section still lists `- **LE AVM members (`hsqs`)** — still Frontier.`, the
binding returns **True for both** (measured). The counter never reads the
`## Frontier` section (measured: `"## Frontier"` occurs **0** times in the
counter). So a landing that adds the Core section and a frontier note while
**leaving the LE AVM members in the Frontier list** passes every binding — and
the claims assert the opposite ("LE `hsqs` leaves the Frontier list").

**Demand:**
1. a new binding that **reads the `## Frontier` section** and asserts the LE AVM
   members row is **absent** from it (the promotion is the claim; it must be
   checked, not asserted in prose);
2. a binding that the **entry names the fresh receipts** (the claims require it;
   the v1 binding set has no check);
3. a binding on the **SCORECARD coverage head** (141/141) and one on the **LOG
   entry** — or, if the L1 intends these to be verified outside the counter, the
   claims' phrase "each re-derivable by the counter" must be corrected to say
   which items are and are not counter-verified (the phrase as written promises
   all of them).

---

## Summary table (status against the working-tree claims at 02:18)

| # | finding | axis | severity | status | demanded fix |
|---|---|---|---|---|---|
| F1 | `247:0` is on **all four** carriers, not Cable-class; class difference is count-only (13 vs 1) | coverage | low | **absorbed** (the false attribution is removed); residual stands | state that the class split is count-only over a shared node |
| F2′ | the **amended** M1 mutant is GREEN under the amended control verdict; `law_shape_ok` is not in it | coverage | **critical** | **OPEN (new)** | put `law_shape_ok` in the control verdict; restate M4 as `required=true` + subset |
| F2 | under the law shape the `silent` whitelist is **unreachable**; the specified red mutations are **green**; law ≡ 2 cheats on the corpus | coverage | **critical** | partly absorbed (shape clause + M2 added); **inertness unexplained** | state the whitelist's inertness; add the char-device-with-disposition fixture |
| F3 | controls named `run.json` (harness metadata) instead of `after.json` (envelope) | coverage | **critical** | **absorbed** (amendment F2) | — |
| F4 | the draft's walk drops `sqfs-list.py`, `fetch-vendor.py`, `xpin-attribute.mjs`, `prior-pins.json`, `rea-pkg.json` and the `tools/round-50/` prefix | coverage | high | **OPEN** | carry the v1 carried-over inputs and the whole `tools/round-50/` prefix |
| F5 | `--receipts` dir unauthenticated; traversal unguarded; round-50 vs round-51 trees indistinguishable | coverage | high | **partly absorbed** (the flags `--provenance-base`/`--receipt-fresh-base` exist in the amendment; the tree-confusion half is fixed) — **traversal half OPEN** | lane-relative + normalised + rejected on escape; receipt records the resolved tree and receipt digests |
| F6 | v1 **already** gates drift at exit 2 (the claims said otherwise); exit 2 = could-not-evaluate **and** = drift | calibration | medium | **absorbed** (the claims now say v1 already exits 2) — residual: distinguish drift by receipt content | assert on `frozen_path_changed`, not the exit code |
| F7 | the four round-51 pins are the four round-50 pins; the honest prior table makes `carrier_fresh_ok` zero | coverage | **critical** | **absorbed** (amendment F1: explicit frozen `re_scored_pins` allow-list) | — (verify the allow-list is frozen and receipt-visible) |
| F8 | the `claim` label constant forces round-51 artefacts to stamp `"claim": "R50-C1"` | calibration | high | **absorbed** (amendment F10: the parser accepts `{R50-C1, R51-C1}`) | — |
| F9 | `OPENED_DATES` excludes S243/S244/S245/S249 (opened 2026-10-28); `sourced` is existential, not the required set | calibration | high | **OPEN** | widen the window and check the required id set in the entry's `source:` lines |
| F10 | 154 selftest cases, **none** exercising `char-device`; ten named missing cases | calibration | medium | **OPEN** | add the ten named cases |
| F11 | `fifo`/`socket`/`block-device` never occur → law arms unfalsified; producer property not observable by the counter | coverage | medium | **absorbed** (amendment F5: the law is stated to the measured width) | — |
| F12 | before-arm and after-arm differ in more than the rule | calibration | low | **OPEN** | enumerate the difference or state that the before-arm is the committed receipt |
| F13 | the amended control verdict omits the only clause that separates the law from the whitelist | coverage | **critical** | **OPEN (new)** | put `law_shape_ok` in the control verdict |
| F14 | the amendment's `--gap-rule` override lets the receipt report `gap_rule_unchanged`/`gap_rule_ok` about the **frozen** rule while the verdict came from an **unpinned** file; no rule sha256 in the receipt | coverage | **critical** | **OPEN (new)** | record `gap_rule_path`+`gap_rule_sha256`; compute both fields against the applied rule; reject out-of-lane overrides |
| F15 | three claims' landing bindings have **no** v1 check, and `frontier_note` **cannot distinguish "promoted" from "not promoted"** — the claim's substance is unverified | coverage | **critical** | **OPEN (new)** | a binding that reads `## Frontier` and asserts the LE AVM row is gone; bindings for the fresh receipts, the SCORECARD head and the LOG entry — or correct "each re-derivable by the counter" |

**Strongest counterexample (F2′/F13 — against the amended text):** the amended
M1 mutant (the all-thirteen whitelist) is **green** under the amended control
verdict `(gaps_ok ∧ nonregular_unpublished_ok)`, and the only clause that
separates it from the law — `law_shape_ok` — is in the predicate, not in the
verdict the mutants are scored by. The kill rule therefore fires on a correct
implementation. Measured on the four committed envelopes.

**Strongest surviving design defect (F4):** the round-51 draft's frozen walk drops
`tools/round-41/sqfs-list.py` — the **producer** of the frozen oracle tables — plus
`fetch-vendor.py`, `xpin-attribute.mjs` (read at the freeze to recompute every
receipt's evidence id), `prior-pins.json`, `rea-pkg.json`, and the whole
`tools/round-50/` prefix. The counter would verify a table whose producer is
mutable, and an evidence-id check whose tool is mutable.

**Strongest surviving calibration defect (F9):** `OPENED_DATES = ('2026-10-30',)`
excludes S243/S244/S245/S249 (measured: opened 2026-10-28), and the v1 `sourced`
binding is existential — so the claims' "cites S243/S244/S245/S249 **and** the
round-51 SOURCES row(s)" is not checked at all: an entry citing only an unrelated
2026-10-30 row passes, and the four required ids can never satisfy the binding.

**Not run / not claimed:** no REA run, no network fetch, no lane mutation, no
counter selftest executed (the drafts lack `--controls`/`--receipts`/`--gap-rule`).
All findings are static/offline re-derivations against committed bytes.
