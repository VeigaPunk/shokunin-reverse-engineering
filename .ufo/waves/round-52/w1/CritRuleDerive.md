# CritRuleDerive — round 52 wave 1 (attack on the R52-C1 law encoding as amended)

**Seat**: `CritRuleDerive` (critic; leaf member — no dispatch, no subagents).
**Verdict**: **the law's statement is sound on the measured width; its encoding is not.**
Nine findings — **3 critical, 3 high, 2 medium, 1 low** — all measured over **committed** lane
bytes (the four round-50 envelopes, the four frozen census tables, the frozen round-50 rule, and
the committed `tools/round-50/c1-counter.py` disposition engine). Three are freeze-blocking and
would either make the freeze's own **kill rule undecidable** or land a rule that contradicts the
lane's committed round-51 corpus.

**Full findings with evidence, exact counters and the smallest safe correction for each**:
`.ufo/waves/round-52/w1/CritRuleDerive/findings.md`
**Receipts** (exact commands, exit codes, stdout sha256, UTC):
`.ufo/waves/round-52/w1/CritRuleDerive/receipts.txt`
**Probes** (13 scripts, re-runnable): same directory, `probe.py` … `probe13.py`.

## The three that matter most

1. **F-1 (critical) — `removed.kinds` is a third disposition channel the shape clause never
   constrains.** `disposition_check` has three families (path-resolved gap, structural gap,
   **removal**); F3/F4 constrain `allowed` and `removed.silent` but never `removed.kinds`. A rule
   with `removed.kinds = ["symlink","char-device",…]` **passes `law_shape_ok` and scores CTL-NEW
   4/4**, yet accepts a *device-row removal diagnostic* as a legal disposition — a device entry
   carrying a disposition, which the law says cannot exist. Measured: under the law that
   diagnostic is **RED** (`removal at 'dev/led' names a 'char-device' entry`); under the widened
   rule it is **GREEN** (`4 removals`). Fix: constrain `removed.kinds` in `law_shape_ok`, add
   mutant M5, and/or make the disposition check refuse a device-row removal outright.

2. **F-3 (critical) — the kill rule is undecidable: M1 is red only by a clause the controls
   path never evaluates.** The claims scope the controls to `gaps_ok ∧ nonregular_unpublished_ok`
   and require M1 (all-thirteen whitelist) to be **RED** *by `law_shape_ok`*. But M1 is
   disposition-**green** — measured 4/4 with the committed engine — and `controls_mode` in the
   r51 draft contains **zero** occurrences of `law_shape_ok`. On the claims' own scoping M1 comes
   out green and **the round stops itself before the data run for the wrong reason**. Fix: the
   control verdict must be `gaps_ok ∧ nonregular_unpublished_ok ∧ law_shape_ok`, with
   `law_shape_ok` evaluated on the named rule inside the controls path and carried in the
   receipt. (This is r51's un-amended blocker, carried into r52 verbatim.)

3. **F-2 (critical) — CTL-NEW does not distinguish the law from a rule that ignores device rows
   entirely.** Measured over the committed corpus: the law, a **device-blind** rule (device kinds
   absent from `allowed` *and* `required`), and a **device-tolerant** rule
   (`allowed['char-device']=['unpublished-entry']`) **all score CTL-NEW 4/4**. The corpus has
   zero device dispositions on all 28 device rows, so CTL-NEW measures *"the rule tolerates the
   twelve unaccounted FRITZ!Box rows"* — a **regression** control — not derivation consistency.
   What separates the law is `law_shape_ok` (a rule-*text* check) and **M2** (the only arm whose
   verdict depends on the census). Fix: rename CTL-NEW to the round-50-miss regression control
   and say in the predicate that M2 + `law_shape_ok` carry derivation consistency.

## Also load-bearing

- **F-4 (high)**: M2 is **not** vacuous, but the claims overstate it — measured three verdicts:
  law GREEN / required-whitelist RED / **silent-only whitelist GREEN**. The claims' *"RED under
  any detail whitelist"* is false for the `required=false` shape; freeze the measured table.
- **F-5 (high)**: F8's remedy is a **carrier-invariant constant** — the `depth-limited` gap's
  `input_path` is the chunk root (`$output/firmware.bin_extract`) and its `continuation_id` is
  **identical on all four carriers**, so it localises nothing. Worse, **8 of the 13 FRITZ!Box
  device rows (`dev/pts/0-7`) sit in a directory with zero extractor-side records in any
  channel** — 12 of 28 rows are demonstrably reached, 16 are not measured at all. Fix: scope the
  law's device claim to the reached rows, or add a real reach clause.
- **F-6 (high)**: the law re-admits an inference the lane's **own committed** round-51 corpus
  **rejected** — `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md:16-25` and
  `corpus/lessons/round-51.md:45` say the FIFO/socket `mknod` calls are **not** root-gated, so
  "char-device/fifo/socket rows all disappear" is **rejected**. The R52 rule encodes
  `allowed['fifo']=allowed['socket']=[]` anyway; measured, that rule is **RED** on a fifo gap the
  r51 reading says an extractor would emit. Narrow the law to char/block-device.
- **F-7 (medium)**: `disposition_check` never reads `unpublished_entries[]`, so a device row
  reported there scores **GREEN** under the law rule and the controls cannot see it.
- **F-8 (medium)**: F10 names one grammar site; the counter has **two** (`c1-counter.py:793`
  rule parser, `:876` carrier table) — a v2 counter widening only the first scores
  `carriers_spec_ok false` with every other binding true.
- **F-9 (low)**: F7 names `unsquashfs -lln`, which emits a mode-char listing (`247,  0`,
  `squashfs-root/` prefix) — **no comparable (rel, kind, detail) tuples**; the reader that
  produced the frozen tables is `tools/round-41/sqfs-list.py --layout auto`.

## Verified sound (no finding)

F3's gap-channel shape works (device gap / renamed gap kind / unmapped path all RED);
CTL-OLD **2/4**, CTL-NEW **4/4**, CTL-JUNK **0/4** reproduced against committed bytes and the
committed miss receipt; the census measurement is exact (**28** device rows, **0** gap, **0**
published, **0** in `unpublished_entries`); F1/F2's carrier-set answer is self-consistent.

## What I did / did not do

Read-only on the lane tree. Files written: this report, `findings.md`, `receipts.txt`,
`status.json` and 13 probe scripts — all under `.ufo/waves/round-52/w1/CritRuleDerive/`. **No**
REA run, **no** `npx rea-agents`, **no** network/download, **no** git/jj mutation, **no** write
into `tools/`, `plans/`, `corpus/`, `SKILL.md`, `PROVINCE.md`, `LOG.md`, `SCORECARD.md`,
`SHONEN.md` or the fleet repo. Scratch `/fast/scratch/hyaku/kaidoku-r52/w1-CritRuleDerive`
removed after copying. No tool installed or upgraded (none needed). The r51 wave-1 draft counter
was read as **evidence only** (it never landed); the engine under test is the **committed**
`tools/round-50/c1-counter.py`.

**Reported, not touched**: a stray `kaidoku-r51/w1-MutGapRule/amended-law-battery.py` sits at the
**lane root**, untracked and **not** git-ignored (`git check-ignore` exit 1) — the r51 misroot
artifact. Fleet root is clean. Not this seat's surface; the L1's misroot sweep owns it.
