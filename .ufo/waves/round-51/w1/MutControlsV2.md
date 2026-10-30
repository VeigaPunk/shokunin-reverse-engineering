# MutControlsV2 — round-51 control designs: dead-control attack (wave 1)

**Verdict: the round-51 control sets are NOT ready to freeze. Three of the named controls are
dead (they pass while the claim is false), one mutation the claim names is green rather than red,
and the sibling's control draft currently scores a usage error as a full green battery.**

No REA run, no data run, no network, no vendor bytes, no lane-tree writes. All measurement ran in
`/fast/scratch/hyaku/kaidoku-r51/w1-MutControlsV2` on a `git clone --shared` fixture at base
`f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab` with the r51 carriers table + law rule committed on top.

## The three findings that change what the L1 freezes

1. **The C1 rule-shape claim is unwitnessed by the control mode the controls use.** The claim
   insists the rule is the law "not a detail whitelist", but `--controls` scores only the
   disposition verdict (`gaps_ok` + `nonregular_unpublished_ok`), under which the law rule and
   the **all-thirteen whitelist are extensionally identical** over the four carriers. Measured,
   all of these score `4/4, exit 0` with **byte-identical stdout** (`78001ef8bad7…`): the law
   rule, the all-13 whitelist, a strict subset of 13, and `allowed[char-device]=[unpublished-entry]`.
   Only the counter's `law_shape_ok` binding separates them — and `--controls` **never evaluates
   bindings**. A round could freeze a thirteen-detail whitelist and every named control would
   still pass. **A rule-shape control is mandatory before the freeze.**

2. **The claim's own strict-subset mutation is green, not red.** "whitelisting a strict subset of
   the thirteen stays red (the M50 partial-widening trap)" holds only on a `required=true` base
   (measured: 2/4, exit 1). On the **law base** (`required[char-device]=false`) the whitelist is
   never consulted — the counter's `required.get(kind, …)` lookup skips the disposition check
   for a non-required kind — so any subset is a **no-op** (4/4, exit 0). The claim's wording and
   the sibling's draft (`ExecControls/c1-controls.py`, `strict-subset-NN` built on the `new` base)
   both use the law base, so **the M50 partial-widening trap the claim names is not being tested**.

3. **No wrong-carrier-set control, and the mode has no target check.** `--controls` exits 0 iff
   every carrier it *scored* is clean; it never checks `carriers_scored == 4` or the expected id
   set. Measured: a carriers table listing **only c6430+c6490** (the two Cable-class carriers,
   which are clean under the **old** rule too) gives `carriers_scored 2, dispositions_matched 2,
   exit 0` — **green**. The two FRITZ!Box carriers that motivate the entire round can be absent
   and CTL-NEW still passes.

## The sibling's control draft currently scores a usage error as a green battery

`ExecControls/c1-controls.py` omits `--rev` (the mode requires `--root --rev`), reads
`doc['carriers_matched']` while the mode emits `dispositions_matched`/`carriers_scored` (so
`observed_count` is always `None`), and accepts exit 1 **or** 2 for every mutation arm. Measured
with the draft's own command line: the counter prints `usage: --controls requires --root --rev`
and exits **2** for all 19 arms; the draft then reports CTL-OLD/CTL-NEW/CTL-JUNK as
`misbehaved` (a field-name artefact) and **all twelve `MUT-STRICT-SUBSET-NN` arms as
`expected`** — a green mutation battery earned on a usage error.

Also measured: **exit 1 is overloaded** — an uncaught exception in the counter exits 1,
indistinguishable from a deliberate "not met", so every arm accepting exit 1 as red also accepts
a broken instrument.

## Redundant controls

- **CTL-JUNK (C1) / junk table (C2) / v5's committed junk table** — three arms of the same shape;
  C2's is carried over unchanged from v5 (126 → 126, per MutTriV6).
- **CTL-OLD (C1) vs the committed r50 after-receipt** — re-measures
  `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` (`carriers_matched 2`); its only new value
  is a port regression check, not evidence for the law.
- **MUT require-char-device + 247:0 (C1) vs CTL-OLD** — the same red, measured twice
  (identical stdout sha256 `4546ebc4b937…`).

## C2-specific findings

- **Both guard-deleted arms are green-by-omission as specified.** Deleting the new row flips the
  *pair* detector but leaves the *audit* at 0 (the body falls to `preserve-failure`, which
  prescribes no cross-read); deleting the audit code or the census check reports "0 violations /
  0 outside" and goes green unless the instrument **fails closed**. MutTriV6 measured this; the
  control set needs a detector-fail-closed arm (guard deleted → exit 2, refused).
- **The frozen expectations move.** MutTriV6 measured the do-nothing count **19 → 20** and
  action-swapped **51 → 52** under the v6 evaluator — freeze 20 and 52, not the v5 numbers.
- **Precedence is load-bearing**: with the new row *above* `legacy-body-failure` the
  "glob broadened back" mutant is green (0/0) — the guard around it is dead.
- **The before-arm is blocked as written**: the v5 instrument refuses a non-ancestor freeze
  (measured exit 2: *"freeze 'f04b51dd…' is not an ancestor of '1aa27369…'"*), so the base arm must
  name a freeze that **is** an ancestor of the base rev.
- **Missing C2 controls**: detector-fail-closed; v6-label-preservation ("exactly one pair
  changed"); a reader-census binding (flipping the census disables the audit silently).

## Recommended before the freeze

1. **Make `--controls` evaluate `law_shape_ok`** (or add a separate shape arm) — otherwise the
   amended F4/M1 arm is unscoreable (measured: the clause is a binding, never reached).
2. **Make M2 mandatory and fix its base** — M2 separates the law from `required=true` whitelists
   (measured green 4/4 vs red 0/4) but not from `required=false` whitelists (measured green 4/4
   even with a 14th device). Both arms are needed.
3. **Fix the sibling's `new` base rule** — it names all 13 details under `removed.silent`
   (measured `law_shape_ok=False`), the shape the claim forbids.
4. **Fix the sibling's interface** (four measured breaks): pass `--rev`; read
   `dispositions_matched`/`carriers_scored`; write the rules inside the repo so `--gap-rule`
   resolves through git; require a parsing receipt with a named reason.
5. Add the **wrong-carrier-set control** and assert `carriers_scored == 4` + the expected ids.
6. Fix the **strict-subset mutation's base** — red only with `required=true` (measured 2/4); a
   no-op on the law base.
7. For C2: freeze the new expectations (20 / 52), pin the new row's precedence position, add the
   three missing arms, and name the before-arm's freeze.
8. Implement or amend the text for the `--provenance-base` / `--receipt-fresh-base` flags.

## Amendment check — the claims file was amended concurrently (wave-1 F1–F11)

The claims gained a `## Wave-1 amendment record` while this seat worked (F1 carrier set, F2
rule-scoped controls, F3 rule shape, F4 mutation set M1–M4, F9 CTL-OLD relabelled). I re-ran
every arm against the **current** counter bytes and re-read the amended text. **F3/F4 close the
design gap in principle, but the instrument and the control driver do not yet implement them:**

- **F3's `law_shape_ok` clause exists in the counter but is a *binding*, and `--controls` never
  evaluates bindings** (measured: `law_shape_ok`/`shape_notes`/`DEVICE_KINDS` are all absent from
  `controls_mode`). So **F4's M1 arm — "the all-thirteen whitelist must be RED" — is currently
  unscoreable** through the mode the controls use.
- **F4/M2 (the fourteenth, unlisted device) works — but only for `required=true` whitelists.**
  Measured with the census carrying `dev/ttyS0 4:64`: law **green 4/4**, every `required=true`
  whitelist **red 0/4**. A `required=false` whitelist — which is what the sibling draft's `new`
  base and all 12 of its subset mutants are — stays **green 4/4 even with the 14th device**,
  because `required=false` skips the disposition check for device rows entirely. So M2 as written
  does not discriminate the draft's own mutants; only `law_shape_ok` can.
- **The sibling's `new` base rule fails the law-shape clause it exists to witness**: it sets
  `required['char-device']=False` **and** `removed.silent['char-device'] = list(DETAILS_13)` —
  measured `law_shape_ok=False` ("names 13 detail(s)"). That is the shape F3 forbids; it is green
  under the disposition verdict and wrong under the shape verdict.
- **A fourth independent break in the sibling draft:** it writes rules to `--out` (outside the
  lane) and passes absolute paths, but the counter resolves `--gap-rule` through
  `git show <rev>:<path>` — measured: out-of-repo path → **exit 2 "rule absent"**; the same rule
  committed inside the repo → **exit 0**. Every arm of that draft exits 2 on the rule lookup.
- The amended text names `--provenance-base` / `--receipt-fresh-base` — **absent** from the
  counter today.

**Recommendation unchanged, with M2 promoted to mandatory and the shape clause moved into the
control path.**

## Evidence

`{W1}/MutControlsV2/findings.md` — the full dead-control table (per control: what it skips, what it
observes, how it passes while the claim is false) and the redundancy analysis.
`{W1}/MutControlsV2/probe/` — `measurements.tsv` (every arm: exit, scored, matched, stdout
sha256), `receipt.txt` (exact commands, exit codes, stdout sha256, stderr, UTC
2026-10-30T05:24:47Z, counter sha256 `028dde4ae38b…`, fixture rev `97b429f6ad68…`), the six
offline probe scripts, and the exact rule fixtures scored.

Tools installed: none. REA runs: none. Data runs: none. Network: none. Lane tree modified: no.

Report: `.ufo/waves/round-51/w1/MutControlsV2.md`
