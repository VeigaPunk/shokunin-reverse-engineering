# Round 93 — claims declaration (frozen before candidate scoring)

Lane `kaidoku`, round 93, attempt 1. Base `0a2a23da5eb50410a8a0df90c031d9f4fdadb024`
(branch `main` tip at round start, remote-verified `ahead=0 behind=0`).
Machine-readable twin: `.ufo/waves/round-93/claims.json`.

Round shape: ONE v1 wave (`r93-w1`) under `/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json`
(band 8–16), sized to the two claims plus the frontier step. The L1 holds the
planner seat; the wave validator refuses `planner`.

Lowest-axis note: all four owned axes sit at 10.0 on finite proxies (SCORECARD
`## Owned axes`), saturation line 10.0, stagnation window 10. The last capability
entered round 92, so the stagnation nudge is not invoked; both claims land on
routed round-92 defects (M92-d/CHEAT-D/CHEAT-E → C1; D-91-3 → C2), which are
the calibration and depth surfaces.

## R93-C1 — calibration (measured overreach): the fresh-pack held-out arm

- **Surface.** The round-92 repair label admits forgeries that derive nothing:
  a five-carrier pinned-image table (M92-d, round-92 critic `c1-table-repair-5`)
  and a five-carrier carrier-read repair (round-92 CHEAT-D) both pass
  `repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10`.
  The round-92 named limits asked for a fresh-pack oracle.
- **Before (do-nothing controls, scored at base with the frozen round-92
  battery, receipts committed pre-freeze):**
  - `.ufo/waves/round-93/pre/r93-do-nothing-r92label-F1.json` — label met True,
    exit 0 (admitted);
  - `.ufo/waves/round-93/pre/r93-do-nothing-r92label-F2.json` — label met True,
    exit 0 (admitted);
  - `.ufo/waves/round-93/pre/r93-negative-control-identity-r92label.json` — met
    False, exit 1 (negative control: the old label does not admit a no-op);
  - `.ufo/waves/round-93/pre/r93-positive-r92repair-r92label.json` — met True,
    exit 0 (the honest repair stays admitted).
- **Counter (candidate = the counter).** `tools/round-93/stop-boundary-repair-battery-v3.py`:
  the round-92 public battery unchanged (imported by path) plus a fresh-pack
  held-out arm — a nonce-marked sha-pinned source (`/usr/bin/env`,
  `a9ba02dc…d202301`) packed fresh at measure time (twice, byte-deterministic),
  its last block tampered ±7 near and ±40 far plus an intact control; a repaired
  fresh cell must round-trip (`upx -d`) to the mutated source bytes; provenance
  atoms (marker present/absent, determinism, no collision with public packed
  images) are required; refusal typing is strict (`refused` a non-empty string
  — the round-92 ReviewerContract key-presence hole closed in this instrument).
- **Frozen label (after):** `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6;
  far-refused 12 of 12; fresh-roundtrip 2 of 2` for the honest repair.
- **Frozen target:** after-state receipts at the round's measured revision:
  - positive control (round-92 repair under v3) met_target true, exit 0;
  - F1 (`.ufo/waves/round-93/controls/table5-window.py`) met_target false with
    both fresh near cells not repaired;
  - F2 (`.ufo/waves/round-93/controls/carrierread5.py`) met_target false with
    both fresh near cells not repaired;
  - F3 (`identity_noop.py`) met_target false.
- **Kill rule:** the positive control not met at the measured revision; any of
  F1/F2 admitted (met_target true) by v3; any receipt missing; v3's or an
  import's sha256 differing from the pins in `claims.json`.
- **Capability row** (rides this claim's demonstration): `fresh-pack held-out
  arm battery (nonce-marked source, roundtrip oracle, strict typed parsing)` —
  enters the SCORECARD capabilities table this round.

## R93-C2 — depth: a craft row's criterion citation states the rule it asserts

- **Surface.** Craft block 31 row 3 cites `corpus/QUALITY.md` row 169 (guard
  inheritance) for the intact-input rule; the citation resolves but mis-states
  (D-91-3, `corpus/lessons/round-92-verifier-spotcheck.md` §5 item 3). Every
  frozen depth counter only resolved paths, so the miscite stayed invisible.
- **Before (scored at base pre-freeze):**
  `.ufo/waves/round-93/pre/r93-c2-block31-before.json` — exit 1, the named
  atom `row 'intact input refused by mistake': QUALITY 169 lacks ['never refuse
  an intact input', "packer's verdict"]`; the checker's selftest is 10 cases,
  0 failures (`tools/round-93/craft-citation-semantic.py --selftest`).
- **Candidate.** (a) craft **block 32** (append-only; block 31 stays as
  history) with a corrected criterion column citing rows that state each rule
  (176 fall-through contract, 178 typed refusal + intact branch, 184 one-green
  window rule, 188 the new citation-semantics criterion); (b) **QUALITY row
  188**: a craft row's criterion citation names a criterion whose text states
  the rule the row asserts, with the semantic atom as the guard.
- **Counter.** `tools/round-93/craft-citation-semantic.py` with two frozen
  manifests (`.ufo/waves/round-93/manifests/block31-before.json`,
  `block32-after.json`); keyword atoms and the marker/shape atoms are frozen
  before data.
- **Frozen target (after, at the measured revision):**
  - after-manifest on block 32 exit 0 (`ok`);
  - before-manifest on block 31 exit 1 at base (committed above) and exit 1 at
    the measured revision (block 31 is history, not rewritten);
  - a prose control is killed: a fixture block whose criterion cites a
    non-stating row fails the atom (selftest case `keyword-miss`, and the
    before-manifest is the real-fixture proof);
  - no depth regression: `tools/round-89/depth-blocks-v2.py` at the measured
    revision reports 32 blocks, resolved 32; `tools/round-91/depth-blocks-v3.py`
    with `--expect-blocks 32` met (shape clause holds at the new boundary).
- **Kill rule:** the after-manifest not ok at the measured revision; the
  before-manifest green at base; any depth regression counter unmet; the
  checker's sha256 differing from the pin in `claims.json`.

## Frontier step and honest-stop

Sourced claim: R93-C1's knowledge entry cites `S318` (new row opened this
round) and re-opened rows `S271`, `S313`, `S316`, `S317`. Assimilation:
`merge/kaidoku/` absent, lane has no `considerthese/` → `Assimilation: none`.
No universal clauses; both targets are single-commit byte-level predicates a
closure can re-derive with one command. Never narrowed after landing; a miss
is an honest stop.
