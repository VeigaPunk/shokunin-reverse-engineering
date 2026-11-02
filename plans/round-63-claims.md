# Round 63 — plans (declared before any claim data lands)

Lane kaidoku, round 63, L1-inline on the Windows host. Round base
`4ce1d64ed62f4dff42ceab43aba085ad0fc1fed7` (the r62 non-author verifier
spot-check commit, which verified R62-C1 **improved** with no routed
defects; the outside decision is recorded in LOG per QUALITY #34 BEFORE
this round's claims are measured). The work program is the r62 record's
`planned` field, executed verbatim: "the edge-numstat grammar's base
analog (edge claims whose receipts bind both edge endpoints could gain a
base-edge re-derivation the r61 gate does not attempt [corpus-wide]; a
new instrument and its own freeze per the r60 rule)".

Fresh-start binding honored (the prompt's §7): r50/r51/r52 re-read and
spot-checked with fresh probes at this round's base; the seven ruled-out
items are receipted in `.ufo/waves/round-63/l1/scores/freshstart-spotcheck.txt`
at the freeze.

## Claim — R63-C1 (depth, capability acquisition)

**The corpus-wide numstat-edge claim sweep.** New instrument
`tools/round-63/edge-numstat-sweep.py` (committed BEFORE this plans+claims
pair is frozen — the QUALITY #33 order): one `git ls-tree -r --name-only
REV -- .ufo/waves` listing filtered to the lane's committed receipt corpus
exactly as the r60/r62 sweeps filter it; each enumerated receipt audited
by the FROZEN single-receipt gate `tools/round-61/numstat-edge-audit.py`
(sha-pinned via `--expect-sha256`, refused exit 2 on a pin mismatch), one
argv subprocess per receipt (sys.executable -X utf8 -I -B, no shell, and
NEVER a `--name` override fleet-wide — the receipt-own bindings are the
r61 gate's own resolution, so per-receipt context is the receipt's, not
the caller's); the inventory computed ONLY from the gate's own JSON
bodies (the sweep itself never reads receipt bytes — a stricter rule than
the r62 sweep's reporting-only mirror: here there is nothing to mirror);
rc 2 routes on the gate's own reason ("no edge claim" = the normal
unevaluable, anything else = invocation error, fail-closed); a body
naming another receipt than the sweep passed is an invocation error;
finding keys keep the r60 `receipt:line:class` format;
`--dispositions` TSV coverage/orphan check identical to the r60/r62
sweeps; `--only PATH` restricts to named enumerated receipts (recorded in
the inventory).

**What was never checkable before this round:** the frozen r61 gate is
single-receipt and every application since r61 was hand-aimed (six
demonstrations over named receipts). No instrument ever enumerated the
receipt corpus for edge-claim-bearing receipts, so the answer to "which
receipts carry claims in the r61 grammar, and do their edges re-derive?"
existed nowhere on the record. Before-arms (receipted at the freeze,
`scores/c1-before.txt`): instrument absent rc=128 at the base; 0 SKILL
rows; 0 SCORECARD rows; 0 `records/edgesweep-` receipts; the r62 sweep's
inventory JSON carries no edge fields (`grep -c '"edge_inventory"'` → 0 —
the behavior token, not the mention); the r61 demos carry no
`receipts_total` inventory (`grep -c` → 0); the composed gate is frozen
and present at the base (rc 0) — the sweep composes those bytes, never
re-implements them.

**Falsifiable before→after** (each verifiable without any other claim —
single claim, so trivially causally separable):

- before: no corpus-wide edge inventory exists at the base; the three
  claim-bearing receipts' corpus-wide state (which receipts carry the 7
  edge-claim instances; which bind both edge endpoints; which fire
  fail-closed) is nowhere recorded.
- after: the instrument registered (SKILL row 7 cells pipe-free with the
  neighbor recounted; SCORECARD capability row, first-working round 63);
  selftest 53 cases 0 failures; the FIRST corpus-wide edge inventory at
  the base: 258 receipts enumerated, 0 invocation errors, 3 receipts with
  edge claims (7 claim instances), 2 receipts binding all endpoints from
  their own bytes, 1 receipt with unresolvable quote-prose names, 255
  receipts without edge claims, 4 findings named
  (1 NUMSTAT_EDGE_MISMATCH — the standing D60-1 — and 3
  NUMSTAT_NAME_UNRESOLVED — the r61 before-arm's quote-prose); red exit 1
  without dispositions; green exit 0 with the r63 disposition TSV (4
  findings all dispositioned, each citing its standing disclosure; a
  green sweep never claims the defects erased); the `--only` arm over the
  three claim-bearing receipts reproduces the same 4 keys (the r61
  recorded classes); the pin fail-closed arm exits 2 before any
  enumeration.

**Counting commands** (all run on THIS host against committed bytes):

- `python -X utf8 -I -B tools/round-63/edge-numstat-sweep.py --selftest`
- the fleet sweep at `--rev <base>` / `--rev <record>` (JSON inventory:
  receipts_total, counts, edge_inventory, finding_keys)
- before-arm greps pasted in `scores/c1-before.txt`
- after-arm greps pasted in `scores/c1-after.txt` (SKILL row count,
  capability row count, `records/edgesweep-` receipt count)

**Sourced claim:** S263 — the Python `hashlib` module documentation
(docs.python.org/3/library/hashlib.html), opened this round, snapshot
pinned at `.ufo/waves/round-63/l1/s263/`. C1's composition trust anchor
rests on it: the sweep never audits with unpinned checker bytes — the
`--expect-sha256` pin check hashes the composed gate's worktree bytes
with hashlib's SHA-256 (the FIPS 180-4 family, per the pinned page) and
refuses a mismatch before any enumeration. The same digest discipline
pins all nine instruments in the claims container.

**Lowest-axis rule:** coverage/depth/calibration all 10.0 (tied) — every
owned axis is a lowest axis; the claim works depth. Stagnation nudge not
fired (window N=10; capabilities entered r60, r61, r62; r63 = 3/10).

**§9 sizing / do-nothing control:** at the base the instrument is absent
(rc 128), zero rows, zero receipts, and no corpus-wide edge inventory
exists anywhere in the record — a do-nothing control cannot produce the
instrument, the first inventory, the registration, or the threading
statistics. The r62 planned field names the candidate; the round executes
it.

**QUALITY #44 note (pre-freeze probes):** the live dry run of the sweep
against the base ran BEFORE this declaration was committed (the M62-1
rule: end-to-end, production seam). Probe times are recorded in the
receipts the freeze carries; the freeze commit lands after the probes.
The demonstration receipts land with the freeze, from committed
declaration bytes (hash-verified worktree-vs-blob identical at the
declaration).
