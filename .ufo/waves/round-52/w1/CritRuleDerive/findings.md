# CritRuleDerive — round 52 wave 1: attack on the R52-C1 law encoding as amended

Seat: `CritRuleDerive` (critic; leaf member — no dispatch, no subagents).
Scope: verify the r51 amendments F1–F11 as they land in `plans/round-52-claims.md`, and hunt
new holes in the law's *encoding* (the rule shape, the shape clause, the control battery).
All measurements are over **committed** lane bytes: the four round-50 envelopes, the four frozen
round-50 census tables, the frozen round-50 rule, and the r51 wave-1 draft counter (evidence
only — the r51 instruments never landed). No REA run, no network, no lane write.

**Verdict: the law's *statement* is sound on the measured width, but its *encoding* has three
holes the freeze must close, and one of them (F-3) makes the freeze's own kill rule
undecidable.** The two amendments that were supposed to make the law checkable — F3's
`allowed[device]=[]` shape and F4's `law_shape_ok` clause — together leave a rule that passes
every named control while contradicting the law in two distinct ways. Severity: **2 critical,
3 high, 2 medium, 1 low**.

Method note: the disposition engine under test is the **committed** `tools/round-50/c1-counter.py`
(`disposition_check`, `gap_rule_model`, `subject_root`, `diagnostics`, `gaps`,
`nonregular_published`), imported read-only; the rule under test is reconstructed from the
claims' own wording. Every number below is reproduced by the probes in this seat directory.

---

## F-1 (critical) — `removed.kinds` is a third disposition channel the law's shape clause never constrains

**The hole.** The claims define `law_shape_ok` (R52-C1 predicate) as: *"the frozen rule lists no
char-device/fifo/socket/block detail under `removed.silent` and `allowed` for those kinds is the
empty list"*, plus (F3) `required['char-device'] = false`. That is **two** of the rule's three
disposition channels. The third — `removed.kinds` — is never constrained by either the claims'
wording or the r51 draft's implementation
(`.ufo/waves/round-51/l1/drafts/c1-counter.py:2665-2680`).

`disposition_check` (`tools/round-50/c1-counter.py:1458-1569`) has three families: a
**path-resolved gap**, a **structural gap**, and a **removal**. The removal family is gated by
`removed.kinds`: a diagnostic whose `__typename__` matches `removed.diagnostic` must resolve to
exactly one census row **whose kind is in `removed.kinds`**. So a rule with
`removed.kinds = ["symlink", "char-device", …]` makes a *device row* an admissible removal
target — a device entry carrying a disposition, which the law says cannot exist ("a
char-device/fifo/socket oracle entry carries **no disposition at all**", R52-C1 law paragraph).

**Measured** (probe11 / probe13, against the committed g7581 envelope and census):

| rule | `law_shape_ok` (r51 draft semantics) | CTL-NEW | device-row removal diagnostic |
|---|---|---|---|
| the law (R52-C1) | **True** | 4/4 | **RED** — `removal at 'dev/led' names a 'char-device' entry; removed.kinds is ['symlink']` |
| `removed.kinds` + `char-device` | **True** | **4/4** | **GREEN** — `637 gaps (1 structural), 4 removals, 0 silent` |

So a rule that lets a device row carry a removal disposition passes the shape clause *and* the
whole control battery. The law's sentence and the rule's behaviour diverge, silently.

**Why this is new.** r51's F3/F4 fixed the *gap* channel (`allowed[device]=[]`) and the
*silent* channel (`removed.silent` empty). The removal channel was never examined; no r51
finding names `removed.kinds`.

**Smallest safe correction.** Add one clause to `law_shape_ok` and one to the mutation set:
- `law_shape_ok` must also require that `removed.kinds` contains **no** device kind (the
  claims' own vocabulary already exists: `DEVICE_KINDS = ('char-device','block-device','fifo','socket')`
  in the r51 draft, `:447`).
- Add **M5** to the frozen mutation set: the law rule with `removed.kinds` widened to name
  `char-device` → must be **RED** (by `law_shape_ok`, and by the disposition clause if the
  counter refuses a device-row removal outright).
- Cheaper and stronger still: make `disposition_check` **fail closed** on a removal diagnostic
  that resolves to a device row, regardless of `removed.kinds` (one extra condition next to
  the existing `entry_kind not in removal_kinds` check at `:1516-1519`). Then the escape closes
  even for a rule the shape clause would wave through.

---

## F-2 (critical) — CTL-NEW does not distinguish the law from a rule that ignores device rows entirely

**The question asked.** *"Is CTL-NEW (4/4 over round-50 envelopes) a real derivation
consistency check, or does it pass for any rule that ignores device rows entirely (then it
cannot distinguish the law from a no-device-check rule — name what does)?"*

**Answer: CTL-NEW passes for any rule that ignores device rows entirely, and also for the
opposite error — a rule that *tolerates* device gaps.** It distinguishes nothing about the
device accounting. Named, it does not separate the law from a device-blind rule.

**Measured** (probe2 / probe7, the four committed envelopes and the committed census tables):

| rule | CTL-NEW (dispositions green) | M2 fixture (14th device) |
|---|---|---|
| the law (R52-C1) | **4/4** | GREEN |
| **device-blind**: device kinds absent from `allowed` **and** `required` | **4/4** | GREEN |
| **device-tolerant**: `allowed['char-device'] = ['unpublished-entry']` | **4/4** | GREEN |
| the all-thirteen whitelist (M1) | **4/4** | RED |

So over the committed corpus the device accounting is **unobservable**: the corpus contains
**no** device gap and **no** device disposition of any kind on any of the 28 device rows
(probe5), so every rule that does not *require* a device disposition scores 4/4. CTL-NEW
therefore measures *"the rule tolerates the twelve unaccounted FRITZ!Box device rows"*, which
is a **regression** control against the round-50 miss — **not** a derivation-consistency check.

**The name.** What separates the law from the device-blind rule is **`law_shape_ok`** (F3/F4) —
and, for the whitelist family, **M2**. But `law_shape_ok` is a **rule-shape** check, not a
derivation check: it inspects the rule *text*, never the envelopes. So the honest description
is:

> CTL-NEW = the **round-50-miss regression** control (2/4 → 4/4);
> `law_shape_ok` = the **rule-shape** control (separates the law from a whitelist *by text*);
> M2 = the **derivation-consistency** control (the only arm that shows the rule's verdict
> depends on the *census*, not on a frozen detail list).

**Smallest safe correction.** Rename CTL-NEW in the claims to what it measures (the
"round-50-miss regression control"), and state explicitly in the predicate that the derivation
consistency property is carried by M2 + `law_shape_ok`, not by CTL-NEW. Then make the kill
rule say which arm is load-bearing: `CTL-NEW red, CTL-OLD yielding 4, or any mutant green that
should be red → stop` is currently decidable, but a reader cannot tell that CTL-NEW alone would
not catch a device-blind rule. **Note the M2 arm is currently the only one that does.**

---

## F-3 (critical) — the kill rule is undecidable as written: M1 is red only by a clause the controls path never evaluates

This is the **carried-over** r51 defect that F1–F11 did **not** answer, and it is the one that
can sink the round.

**The hole.** The R52 claims require M1 (the all-thirteen whitelist) to be **RED**, and say so
twice: *"must be **RED** — red by the frozen rule-shape clause `law_shape_ok`"* (rule mutations)
and the kill rule *"any mutant green that should be red → stop before the data run"*. But the
same claims scope the controls to *"the frozen **disposition verdict** (`gaps_ok` ∧
`nonregular_unpublished_ok`)"*. The r51 wave-1 draft implements exactly that scoping:
`controls_mode` (`.ufo/waves/round-51/l1/drafts/c1-counter.py:2706-2803`) evaluates
`gaps_ok` and `nonregular_unpublished_ok` and returns `0 if matched == len(per) else 1` — and
contains **zero** occurrences of `law_shape_ok` (measured).

**Measured** (probe3, the committed counter's own `disposition_check` over the committed
envelopes — the exact function `controls_mode` calls):

| rule scored by the disposition verdict | dispositions green | M1 requires |
|---|---|---|
| round-50 rule (CTL-OLD) | 2/4 | — |
| the law (CTL-NEW) | 4/4 | — |
| **M1 (all-thirteen whitelist)** | **4/4** | **RED** |

M1 is disposition-**green** — measured, directly, with the committed engine. It is red *only*
through `law_shape_ok`, and `law_shape_ok` is not in the controls path. So on the claims' own
scoping, **M1 comes out green and the kill rule fires on a correct rule**, i.e. the round stops
itself before the data run for the wrong reason. (r51's `MutGapRule` seat measured the same
thing end-to-end against the r51 counter's `--controls` mode and reported it; the r51
amendment record F2/F4 changed the *claim text* but did not change the *scoping*, and the r52
claims repeat that scoping verbatim — `plans/round-52-claims.md:115-117`.)

**Smallest safe correction.** Two lines in the claims:
1. State that the **control verdict is `gaps_ok ∧ nonregular_unpublished_ok ∧ law_shape_ok`**,
   and that `law_shape_ok` is evaluated **on the named rule inside the controls path** (the
   control receipt must carry `law_shape_ok` and its shape notes, so the kill rule is decidable
   from the receipt alone).
2. Say so in the mutation paragraph: *"M1 is red by `law_shape_ok`; the control verdict
   therefore includes `law_shape_ok`, and the control receipt carries it."*

This is also what makes F-1's fix enforceable: a shape clause that is never evaluated cannot
police `removed.kinds` either.

---

## F-4 (high) — M2 is **not** vacuous, but it discriminates less than the claims state

The task asks: *"does the law rule actually score it GREEN while a whitelist scores RED, or
does required=false make M2 vacuous (both score green)? If vacuous, M2 tests nothing."*

**Answer: M2 is NOT vacuous — but it is narrower than the claims claim.** Measured (probe7):

| rule (all scored on the same 14th-device fixture `dev/ttyS0 4:64`) | verdict |
|---|---|
| the law | **GREEN** |
| whitelist with `required['char-device']=true` + the thirteen details silent | **RED** (`required entry with no disposition … on ['dev/ttyS0']`) |
| whitelist with `required['char-device']=false` + the thirteen details silent | **GREEN** |

So M2 as written (*"RED under any detail whitelist"*) is **false for the `required=false`
whitelist shape**, which is a legal shape under the law (required=false is the law's own
setting for the kind). r51's `MutGapRule` seat flagged exactly this and the r51 amendment
record's F4 wording still says *"red under any whitelist"* — carried into r52 unchanged.

This is not fatal (the `required=false` whitelist is caught by `law_shape_ok`, since
`removed.silent['char-device']` names device details), but the frozen expectation table must be
written against the **measured** verdicts, not the claims' prose, or the mutation battery will
report a false "misbehaved" arm.

**Smallest safe correction.** Restate M2 as: *"GREEN under the law rule; RED under a whitelist
that **requires** a device disposition (`required['char-device']=true`); a whitelist that only
lists the details under `removed.silent` (leaving `required=false`) stays GREEN here and is
caught by `law_shape_ok`."* And freeze the expectation table with those three rows
explicitly.

---

## F-5 (high) — F8's remedy records a constant, not a limit: the receipt cannot say which subtree was not descended into

**The claim.** F8 / R52-C1: *"the v2 counter records the `depth-limited` gap's `input_path` and
`continuation_id` in its receipt so the limit stays visible"* and the predicate requires
`depth_gap_recorded true`.

**Measured** (probe5 / probe8, the four committed envelopes):

- the `depth-limited` gap's `input_path` is **`$output/firmware.bin_extract`** on all four
  carriers — the **chunk root**, not the path the limit stopped at;
- its `continuation_id` is **identical across all four carriers**
  (`3b54e297653ef5bd5afa64e607b809946398c269f862657ab0544192b7b442ab`) — one distinct value
  for four different carriers. It is the "rerun with a higher max_depth" continuation, keyed
  to the root path, so it cannot distinguish *which* subtree was skipped;
- the receipt's own `depth_limited_paths` is likewise `["$output/firmware.bin_extract"]` and
  `coverage` is `"partial"`.

So F8's two recorded fields are **carrier-invariant constants**. Recording them satisfies
`depth_gap_recorded` while leaving the limit exactly as invisible as before.

**And the underlying reach question is worse than the claims' "reached" caveat states.**
Measured reach test (probe4 / probe12): the extractor's *own* records (published files ∪
path-resolved gaps ∪ `unpublished_entries` ∪ diagnostics), by top-level directory:

- `g7581` / `g7582`: `dev` has exactly **3** extractor-side records (`dev/kdsld_misc`,
  `dev/log`, `dev/new_led` — all symlinks). **`dev/pts/` has ZERO records of any kind.**
  Eight of the thirteen device rows (`dev/pts/0-7`) live in `dev/pts/`.
- `c6490` / `c6430`: `dev` has 2–3 records; the single device row `dev/led` sits in `dev/`.

So **8 of the 13 FRITZ!Box device rows sit in a directory the extractor left no trace of in
any channel.** The law's measurement ("28 of 28 rows carry no extraction gap and no published
path") is true but **vacuous for those 8 rows**: an extractor that never visited `dev/pts/`
and one that visited it and stayed silent are indistinguishable in the receipt. The claims'
caveat ("a device-only subtree never descended into cannot be distinguished from one reached
and correctly produced no gap") names the problem; F8 does not solve it.

Also note the depth-limit is real but *global*, not per-subtree: `max_depth=1` in every
committed receipt's parameters, yet all 4556 oracle regular files were published at relative
depths 1–8 (`probe12`), i.e. the extractor descended the whole tree for regular files. The
device rows are invisible for a different reason.

**Smallest safe correction.** Two options; pick one and say which:
- (a) **Scope the law's device claim to the 12 rows the extractor demonstrably reached**
  (`dev/led`, `dev/tiatm`, `dev/ttyp0-2` on each FRITZ!Box carrier, `dev/led` on each Cable
  carrier — 5+5+1+1 = 12 of 28), and state the 16 `dev/pts/*` rows as **not measured**. The
  law then says what the receipt supports. This is the honest, cheap fix.
- (b) Add a **reach clause** the counter can actually evaluate: for each device row, require
  that the extractor produced *some* record under the row's parent directory (or that the row's
  parent directory is absent from the extraction tree entirely, which the census can tell).
  Under (b), `dev/pts/*` would fail the reach clause on the current receipts — so (b) requires
  a fresh extraction at a higher depth, i.e. it is a data-run change, not a freeze change.

Either way, **`depth_gap_recorded` as specified (input_path + continuation_id) is not evidence
of anything and should not be presented as the F8 remedy.** It must be renamed (e.g.
`depth_gap_fields_present`) or replaced by (a)/(b).

---

## F-6 (high) — the law sentence re-admits the inference the lane's own round-51 corpus **rejected**: fifo/socket do not disappear

**The hole.** The R52-C1 law paragraph says: *"it creates **no device nodes, fifos or sockets** —
an unprivileged extraction cannot `mknod` a device — and it emits **no gap record for them**"*,
and grounds it on S250. The rule encodes that for **four** kinds:
`allowed['char-device'] = allowed['block-device'] = allowed['fifo'] = allowed['socket'] = []`.

**But the lane's own committed round-51 corpus says exactly the opposite** about two of those
four kinds, and says it was *deliberately rejected*:

- `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md:16-25` (committed):
  *"FIFO (`:1328`) and socket (`:1349`) creation call `mknod` **outside this root test**. Thus the
  proposed explanation 'an unprivileged extraction cannot mknod, so char-device/fifo/socket rows
  all disappear' is **rejected**. The source does not prove those two kinds disappear. The lane
  must distinguish the mechanisms and observe the operative extractor before assigning a
  disposition to an untested kind."*
- `corpus/lessons/round-51.md:45` (committed): the shared char/FIFO/socket `mknod` premise is
  recorded as **rejected**, not admitted.
- `SKILL.md:573-578` (committed, the round-51 source correction): *"S250 distinguishes
  root-gated char/block-device creation from the non-root-gated FIFO/socket branches …
  an absent char-device cannot be presumed to have an `unpublished-entry` gap."*

The R52 claims cite S250 for the *opposite* conclusion, and the r51 amendment F5 "fixed the
width" by *marking the generalisation unexercised* while the law **sentence** and the **rule
shape** keep asserting it. The R52 claims' own width paragraph even says *"the generalisation
to fifo/socket/block rests on the source ground"* — but the source ground **rejects** it for
fifo/socket.

**Measured consequence** (probe7): with a synthetic fifo row `dev/pipe0` and the
`unpublished-entry` gap an extractor that *does* create a fifo would emit, the R52 law rule
scores **RED** (`gap kind 'unpublished-entry' not allowed for 'fifo' entry 'dev/pipe0'`),
while the round-50 rule tolerated it. Under the r51 knowledge entry's own reading (fifo/socket
creation is *not* root-gated, so an unprivileged extractor **can** create them and **does**
report them), the R52 rule is **wrong** about two of its four kinds — and the freeze would
promote that wrongness to Core.

**Smallest safe correction.** Narrow the law's device kinds to the two the source actually
grounds — **char-device and block-device** — and either
- drop `fifo`/`socket` from the `allowed` map entirely (the counter's `gap_rule_ok` binding
  already requires every census kind to be covered — `kinds_seen - set(model['allowed'])` at
  the r51 draft `:2663` — so **the kinds must be listed**; listing them with
  `allowed['fifo'] = ['unpublished-entry']` and `required=false` restores the round-50
  behaviour and the disposition clause's tolerance), and mark the fifo/socket disposition
  **unobserved** in the claims; or
- keep `[]` but state the rule as *"no gap record for a char-device/block-device row; the
  fifo/socket disposition is unobserved and the rule does not decide it"* — which then
  contradicts `allowed['fifo'] = []` and so must be fixed too.

Either way, **the r51 rejected premise must not be re-admitted as measured law in the R52
freeze**, and the fix belongs in the `## Wave-1 amendment record` (which is still empty).

---

## F-7 (medium) — the `unpublished_entries` channel is a disposition channel the rule-scoped controls never read

**Measured** (probe6 / probe5): `disposition_check` does **not** read
`normalized_result.unpublished_entries[]` (verified by source inspection: the string
`unpublished` does not appear in its body; the counter reads it only in `receipt_paths` and in
`projection`). The claims' control scope is `gaps_ok ∧ nonregular_unpublished_ok`, and
`nonregular_unpublished_ok` is about **published** paths colliding with census rows — not about
`unpublished_entries`.

Consequence, measured: a receipt that reports a **device row in `unpublished_entries[]`**
(a char-device entry kept as metadata) scores **GREEN** under the law rule, and
`nonregular_published` stays empty. The device row then carries a disposition the law says it
cannot carry — and the rule-scoped controls cannot see it. (In the committed corpus the two
channels happen to be the same 636/636/612/567 symlink rows — probe12: the path-resolved gap set
and the `unpublished_entries` set are **identical** for all four carriers — so the corpus never
separates them. A future extractor that reports a device through `unpublished_entries` only
would be invisible.)

**Smallest safe correction.** Either extend the law's scope sentence to say the law governs the
**gap** channel only (and say so explicitly), or add a third family to the disposition check:
a census row of a device kind must appear in **no** channel — no gap, no removal, no
`unpublished_entries` entry, no published path. The second is what the law sentence actually
claims; it is one extra check over a list the counter already parses.

---

## F-8 (medium) — F10 names one grammar site; the counter has **two**

**Measured.** `tools/round-50/c1-counter.py` has two independent `claim`-label checks:
`gap_rule_model` (`:793`) and `carriers_spec` (`:876`). The R52 claims' F10 grammar bullet names
only the first: *"the v2 `gap_rule_model` accepts the claim labels `{R50-C1, R52-C1}`"*. The
r51 draft fixed **both** sites (`:839` and `:922`). The frozen carrier tables carry per-round
labels (`R41-C1`, `R49-C1`, `R50-C1` — measured), so the round-52 carrier table's own `claim`
label is a live second site.

**Smallest safe correction.** Widen F10 to: *"the v2 counter accepts the claim labels
`{R50-C1, R52-C1}` at **both** grammar sites — the rule parser and the carrier-table parser
(the committed counter checks the label in two places, `c1-counter.py:793` and `:876`); the
frozen round-52 rule and the frozen round-52 carrier table both carry `"claim": "R52-C1"`."*
Without this, a v2 counter that widens only the rule parser scores the round-52 carrier table
`carriers_spec_ok false` — an honest miss that *looks* like a success (every other binding
true, exit 1), exactly the failure r51's `MutGapRule` seat documented.

---

## F-9 (low) — F7's census re-derivation names `unsquashfs -lln`, which cannot produce the frozen table's rows

**Measured** (probe10 / probe11). F7 requires the v2 counter to re-derive the **non-regular**
census at score time *"with the frozen reader/`unsquashfs -lln`"* and compare the row sets in
both directions. `unsquashfs -lln` on a synthetic little-endian image containing a char-device,
a fifo and a socket emits a **mode-character listing**:

```
crw------- 0/0                 247,  0 2023-11-14 19:13 squashfs-root/dev/led
prw-r--r-- 0/0                       0 2023-11-14 19:13 squashfs-root/run/pipe0
srw-r--r-- 0/0                       0 2023-11-14 19:13 squashfs-root/run/sock0
```

The frozen table's format is `relpath TAB kind TAB detail` with `detail` = `major:minor`
(`247:0`) and **no** `squashfs-root/` prefix. `-lln` therefore yields **no comparable
(rel, kind, detail) tuples** without a bespoke parser, and it prints `247,  0` (comma) where
the table has `247:0` (colon). The r51 draft's F7 implementation uses the correct reader —
`tools/round-41/sqfs-list.py --layout auto` (the producer of the frozen tables, per
`tools/round-50/c1-run.sh:319-321`) — and the round-41 `c1-extra.py` registry row already
pins that re-derivation pattern.

**Smallest safe correction.** Change F7's reader name to the one that actually produces the
frozen table, and keep `-lln` only as a *cross-check* if desired:
*"the non-regular census is re-derived at score time by the frozen reader
`tools/round-41/sqfs-list.py --layout auto` — the producer of the frozen tables — and must
equal the frozen `*.nonregular.tsv` row sets in both directions; a reader that cannot run is
exit 2 (`oracle_env_error`), never a green."* (The r51 draft's `census_rederived` implementation
at `.ufo/waves/round-51/l1/drafts/c1-counter.py:2219-2250` is exactly this and can be ported.)

---

## What I verified as sound (no finding)

- **F3's rule shape on the gap channel works.** A gap landing on a device row is RED under the
  law: measured `gap kind 'unpublished-entry' not allowed for 'char-device' entry 'dev/pts/0'`
  (probe2). A *renamed* gap kind (`device-node`) is also RED. A gap on a path that maps to no
  oracle row is RED (`matches 0 non-regular entries`). The `required` semantics are as F3
  states: `required['char-device']=true` with no silent list scores **0/4**; with
  `silent={'char-device':['247:0']}` it scores **2/4** (reproducing the round-50 miss exactly).
- **CTL-OLD = 2/4, CTL-NEW = 4/4, CTL-JUNK = 0/4** — all three reproduced against the
  committed envelopes and tables with the committed engine (probe2/probe9). The committed miss
  receipt agrees: `carriers_matched 2`, `exit_code 1`, `g7581` and `g7582` with
  `gaps_ok false` (probe9). CTL-DN: with no receipts the disposition check fails closed
  (`no extract root: paths cannot be resolved`), so the control is red, not green.
- **The census measurement the law rests on is exact**: 28 device rows over the four carriers
  (13 + 13 + 1 + 1), **0** with a gap, **0** published, **0** in `unpublished_entries`
  (probe4/probe5).
- **The 636/636/612/567 path-resolved gap set and the `unpublished_entries` set are identical
  for every carrier** (probe12) — so the corpus never separates the two channels (see F-7).
- **F1/F2's carrier-set answer holds as stated** in the R52 claims: the four round-50 pins are
  re-scored under an explicit `re_scored_pins` allow-list, and no new carrier is claimed. I did
  not re-measure the `prior_pins`/`re_scored_pins` mechanics (they live in the un-landed r51
  draft); the claim text is explicit and self-consistent.
- **F10's labels** are correct for the rule parser; only the second grammar site is missing
  (F-8).

---

## Smallest safe correction — the whole set, in order

1. **Freeze-blocking (critical).** Extend `law_shape_ok` to police `removed.kinds`
   (no device kind) — F-1 — **and** make the control verdict
   `gaps_ok ∧ nonregular_unpublished_ok ∧ law_shape_ok`, with `law_shape_ok` and its shape
   notes carried in the control receipt — F-3. Without #2, #1 cannot be enforced and M1's
   required RED is unreachable.
2. **Freeze-blocking (critical).** Restate the M2 expectation against the **measured** three
   verdicts (law GREEN / required-whitelist RED / silent-only whitelist GREEN) — F-4 — and
   freeze that table.
3. **Freeze-blocking (high).** Narrow the device-kind scope of the law to the kinds the source
   grounds (char-device, block-device) and stop re-admitting the r51-rejected fifo/socket
   inference; list the fifo/socket disposition as unobserved — F-6 — and put it in the
   `## Wave-1 amendment record` (still empty).
4. **Freeze-blocking (high).** Either scope the law's device claim to the 12 rows the extractor
   demonstrably reached, or add a real reach clause and accept that it needs a deeper
   extraction — F-5 — and stop presenting `input_path`/`continuation_id` as the F8 remedy.
5. **Freeze-blocking (medium).** Widen F10 to both grammar sites and name the round-52 carrier
   table's label — F-8; point F7's reader at `sqfs-list.py --layout auto` — F-9.
6. **Freeze-blocking (medium).** Either scope the law to the gap channel or add the
   `unpublished_entries` family — F-7.
7. **Rename CTL-NEW** to the round-50-miss regression control and state that M2 + `law_shape_ok`
   carry the derivation-consistency property — F-2.

Every item is a text change in `plans/round-52-claims.md` (or in the rule-shape clause of the
v2 counter as it is drafted). None of them requires a new measurement, and none of them can be
fixed after the freeze.

---

## Scope and limits

- Read-only on the lane tree. Files written: this findings file, `receipts.txt`, the probe
  scripts, `status.json` — all under `.ufo/waves/round-52/w1/CritRuleDerive/`.
- **No REA run**, no `npx rea-agents`, no network, no download, no git/jj mutation, no write into
  `tools/`, `plans/`, `corpus/`, `SKILL.md`, `PROVINCE.md`, `LOG.md`, `SCORECARD.md`,
  `SHONEN.md` or the fleet repo.
- The r51 wave-1 draft counter was read as **evidence** (it never landed); the disposition
  engine under test is the **committed** `tools/round-50/c1-counter.py`.
- Scratch `/fast/scratch/hyaku/kaidoku-r52/w1-CritRuleDerive` was removed after the receipts
  were copied here.
- No tool was installed or upgraded this wave (none needed).
- One lane-tree stray observed, **not** touched (it is not this seat's surface): a
  `kaidoku-r51/w1-MutGapRule/amended-law-battery.py` copy sits at the **lane root**
  (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/kaidoku-r51/…`), untracked and *not*
  git-ignored (`git check-ignore` exit 1). It is the r51 misroot artifact named in that
  round's `MutGapRule` report. The fleet root is clean (`git status --porcelain` shows only
  `.scratch/` and `.ufo/l0-questions.md` modifications, both pre-existing). Reporting only.
