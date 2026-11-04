# Round 73 — declared claims (frozen; no amendments after this file's container commit)

Base `05bf065684e52d72ea25aad95f7acb71fcd7874c` (the round-72 lane tip: the record commit, the
report and the non-author spot-check lesson; the lane tree is clean and pushed). Three claims on
three distinct axes, causally separable — each is scored by its own instrument and none reads
another's result. All three are capability acquisitions in the AXES sense: the instrument runs, its
output verifies, and its row enters the SCORECARD capabilities table in the same round.

**Lowest-axis obligation.** The lane's three owned axes sit at 10.0 behind different proxies; the
round-72 spot-check (routed defect 6) corrected the round-72 rationale: the stagnation nudge's
waiver condition was *not* met (capability rows entered in rounds 70 and 71 sit inside the
10-round window), and the obligation was satisfied by working coverage, tied-lowest at 10.0.
This round declares the same way: **`lowest-axis: coverage`** — R73-C1 works it — and claims no
waiver. `SCORECARD.md`'s round-73 section records the label (the audit's atom D6 reads it).

The round-72 non-author spot-check routed seven defects to this round
(`corpus/lessons/round-72-verifier-spotcheck.md` §6). This round's work is the lane's own queue
from that document and from `SCORECARD.md`'s round-72 `planned` list:
- planned item (a), MutReaders survivors a/b/c → **R73-C3**;
- planned item (c), "a producer-independent census for a hostile-wrapper class" → **R73-C1**;
- routed defects 1–5 (record/evidence mismatches) → **R73-C2**;
- routed defects 6 and 7 are prose discharges carried in the record (the lowest-axis label above;
  one named before receipt per claim row), not claim input — bookkeeping alone earns no claim slot.

## R73-C1 — coverage: the kernel's record joins the witness class (Frontier → Core)

**Type.** Capability acquisition. The round-72 knowledge entry
(`corpus/knowledge/2026-11-04-r72-checker-env-capsule.md`) records the forged-witness wrapper as a
*class boundary*: "a wrapper that forges both A11 witnesses" is not detected by the route, because
every A11 witness is a claim the child or the checker makes about itself. This round gives the
probe a witness the producer cannot forge and moves that boundary to Core for the measured route.

**Falsifiable before → after.** At the base the probe has eleven arms and **no channel that reads a
child's environment from the kernel side**: `grep -c '/proc/%d/environ' tools/round-72/seam-probe.py`
prints `0` against `3` in the round-73 probe. Its A11 witnesses are both producer-side — the shim's
own dump and the checker's own JSON — so a shim that writes a clean four-key dump while running
under the caller's 275-key environment passes every A11 clause. After the round the probe's A12
reads `/proc/<pid>/environ` for each shim process while it runs: the genuine run's kernel samples
show exactly HOME/LANG/PATH/TMPDIR with the canary absent, and the forged control — a producer that
inherits the caller environment, under shims that write a clean fabricated dump — is convicted by
the kernel witness while its child-side dumps still read clean.

**Predicate (one sentence, frozen).** R73-C1 is verified iff the frozen seam probe, run at the
measured revision as `python3 -I -B tools/round-73/seam-probe.py --root . --rev <measured> --tool
tools/round-73/packed-elf.py --battery tools/round-73/mutation-check.py --pkg <REA 6.5.0 root>
--work <scratch> --receipt <route receipt produced by tools/round-73/packed-elf.py>
--expect-upx <pinned copy> --nonce-commitment <pre-committed commitment> --json-out <receipt>`,
reports `arms_passed 12` of `target 12` with `A12_kernel_witness` true — the genuine run records
kernel samples for both `git` and `readelf` whose key sets are exactly HOME/LANG/PATH/TMPDIR with
`canary_present false`, the forged run's two child-side dumps read keys-exact and canary-free while
its kernel samples read dirty, and `verdict.forged_detected` is true — while the same probe at the
same revision against `--tool tools/round-72/packed-elf.py` reports 11 of 12 naming
`A12_kernel_witness` false (`--forger` absent: the round-72 probe has no kernel channel at all).

**Counting command.** The probe command above, plus
`grep -c '/proc/%d/environ' tools/round-72/seam-probe.py tools/round-73/seam-probe.py` → `0` and `3`.

**Kill rule.** Any arm false; a genuine kernel sample with a key set other than the allowlist or
carrying the canary; a forged run whose child-side dump is dirty (then there is no lie to detect) or
whose kernel samples read clean (then the witness is blind); a base arm true; a post-freeze
instrument edit → not verified, reported, never narrowed.

**Do-nothing control.** `tools/round-73/controls.py` arm `c1_no_kernel_channel` (the round-72 probe
at the same revision: 11 arms, no A12) and arm `c1_blind_witness` (a fixture whose kernel samples are
forced clean over a dirty world: `a12_verdict` returns ok false).

## R73-C2 — calibration: the record is re-derived from the receipts it cites

**Type.** Capability acquisition. The lane's self-assessment (SCORECARD claim rows, the knowledge
entries' provenance, the record gate's disclosures) is checked against committed bytes by a frozen
atom table derived from an **outside** document — the non-author spot-check's routed-defect list —
never from the table it audits (QUALITY #111).

**Falsifiable before → after.** At the base the audit reports `mismatch_count 6` of 7 atoms: the
round-72 C2 row cites a target sha (`39a2193e…`) that is not the receipt's (`602b305d…`), the
mutation receipt's pin is vacuous (`expect null`), `gate-at-record.json` carries no `disclosures`
block and the freeze ledger carries no round-72 row, the lying-receipt checker receipt records
`rc null` where the record says "exits 1", the round-72 knowledge entry's provenance trio sits at
lines 66–68 instead of its open, and no round-73 section declares a lowest axis. After the round the
same audit at the landing revision exits 0 with `mismatch_count 0`.

**Predicate (one sentence, frozen).** R73-C2 is verified iff the frozen record audit, run at the
measured revision as `python3 -I -B tools/round-73/record-audit.py --root . --rev <measured>
--json-out <receipt>`, exits 0 with `mismatch_count 0` over its 7 atoms and every atom row `ok true`
— while the same command at base `05bf0656` exits 1 with `mismatch_count 6`, naming exactly
`D1_c2_evidence_hash`, `D2_c2_pin_conjunct`, `D3_record_gate_disclosures`, `D4_c3_exit_code`,
`D5_provenance_trio_open` and `D6_nudge_rationale`, with `D7_before_pointer` already true.

**Counting command.** The audit command above; `mismatch_count` is the counter.

**Kill rule.** An atom true at the base for a reason the routed defect names (then the atom does not
bind the defect); an atom false at the landing; a `--validate` defect on the receipt; an atom added,
removed or re-worded after the freeze → not verified, reported.

**Do-nothing control.** `tools/round-73/controls.py` arm `c2_do_nothing` (the base record with the
landing receipts absent: 6 mismatches) and arm `c2_lying_receipt` (an audit receipt whose atom rows
say `ok true` over a base tree is rejected by `--validate`'s derived-count agreement).

## R73-C3 — operability: the three reader-seam survivors die by named cases

**Type.** Capability acquisition. The round-72 wave's mutation probe reported three selftest
survivors (`MutReaders` a/b/c: the git reader's env threading, the checker's readelf env threading,
the implicit-capsule derivation) that only a hand-built behavioral fixture killed. This round makes
the seams testable and binds each survivor to a named selftest case, so the battery kills them.

**Falsifiable before → after.** At the base `tools/round-72/packed-elf.py` has no case that exercises
those three seams; the same three defect classes applied to its bytes survive `--selftest`
(`--patch-set r73base` → `survivor_count 3`). After the round the route exposes `readelf_header()`
and `implicit_capsule()` as seams and its selftest carries `git-reader-allowlisted-exec`,
`checker-readelf-allowlisted-exec` and `implicit-capsule-polluted-raw-log`; the same three defect
classes applied to the round-73 bytes are each killed by their named case (`--patch-set r73` →
`survivor_count 0`).

**Predicate (one sentence, frozen).** R73-C3 is verified iff the frozen mutation battery, run at the
measured revision as `python3 -I -B tools/round-73/mutation-check.py --root . --rev <measured>
--tool tools/round-73/packed-elf.py --patch-set r73 --work <scratch> --min-pristine-cases 38
--expect-target-sha256 <the route blob's sha256 at the measured revision> --json-out <receipt>`,
exits 0 with `survivor_count 0`, every mutant `killed` with `expect_case` in its `failed` list,
pristine `cases 38` green and `target_pin.matched` true — while the same battery with `--patch-set
r73base --tool tools/round-72/packed-elf.py` reports `survivor_count 3` and survivors
`["git_reader_env_dropped", "readelf_env_dropped", "implicit_capsule_dropped"]`.

**Counting command.** The battery command above; `survivor_count` is the counter.

**Kill rule.** A survivor; a mutant killed by a case other than its declared one; a pristine selftest
not green or short of 38 cases; an unpinned target; a base arm that cannot apply a patch site (then
the class is not the same class) → not verified, reported.

**Do-nothing control.** `tools/round-73/controls.py` arm `c3_base_world` (patch set `r73base`
against the round-72 route: three survivors) and arm `c3_no_case` (the same patch set against the
round-73 route with the three cases deleted from the registry: three survivors, so the cases, not
the patch text, are what kills).

## Frontier step (inside the claim cap, no extra claim)

- **SOURCES.md.** One row opened this round: the Linux man-pages `proc_pid_cmdline(5)` page, which
  grounds the mechanism A12 uses to find the shim process (the kernel exposes each process's argv).
  It is cited by the round-73 knowledge entry and the C1 receipt's `channels` block.
- **Census.** `sources-census.sh validate --root … kaidoku` at round start (exit 0, 183 rows) and at
  round end (exit 0, 184 rows).
- **Mistake mined.** Round 72's A11 measured a *child-side* witness and called the boundary
  unfalsifiable without giving the observer a channel; the lesson's `## Mistakes` records it with
  the criterion that should have caught it (a witness claim names its channel, and a producer-side
  witness is a claim).
- **Assimilation.** The `merge/kaidoku/` package does not serve these claims → `Assimilation: none`.
  `considerthese/` is absent in this lane (no directory).
- **Sourced claim.** R73-C1 cites the new row through the knowledge entry.

## Waves

One v1 wave `r73-w1`, 16 seats: 6 executor, 3 scribe, 2 reviewer, 2 mutation-tester, 1 critic,
1 sentinel, 1 scout, 1 connector. Attack roles (reviewer/critic/mutation-tester) 5 of 16 = 31%.
The L1 holds the planner seat. No residual call.
