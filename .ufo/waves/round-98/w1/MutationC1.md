# MutationC1 — mutation test of tools/round-98/upx-pe-repair.py (R98-C1 battery)

Seat: MutationC1 (mutation-tester), lane kaidoku round 98 w1, 2026-11-05.
Clone: `git clone --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin $S/clone`,
`checkout --detach 72346895a35a74af18151b125934fa0c09fe1e3c`;
`git rev-parse HEAD` = 72346895a35a74af18151b125934fa0c09fe1e3c; `rev-parse --show-toplevel`
= $S/clone (asserted before any write). Scratch $S=/fast/scratch/hyaku/kaidoku-r98/MutationC1
(503G free at start), deleted at end. No mutating git command anywhere; lane untouched except
this seat's receipt dir and this report. No tool installs needed (upx 5.2.0 already at
/usr/bin/upx; battery preflight accepted it).

## Detector and protocol
Frozen battery, run from $S/clone with TMPDIR=$S/tmp:
`python3 -I -B tools/round-98/pe-upx-tamper-battery.py --repair-cmd <repair> --work $S/work/<tag> --json-out <receipt> --rev 72346895a35a74af18151b125934fa0c09fe1e3c`
Kill rule: mutant killed iff battery label differs from
`recovered 18 of 18; intact 6 of 6; refused 2 of 2; effective 18 of 18` or battery exit != 0.
Pristine repair sha256 2fa1102d320acd8016a05721763c9d57f15a6b92894a67821187d8c825a1dfa4
(clone file; never modified — mutants were applied to copies in $S/mut/, one `edit` each,
diff vs pristine = exactly the one intended line, hashes in mutants.json).
Detector ran on pristine (baseline), each mutated copy, and the restored (unchanged) clone.

## Baseline (pristine) — passed, verdicts conclusive
`--repair-cmd tools/round-98/upx-pe-repair.py` -> EXIT=0,
label `recovered 18 of 18; intact 6 of 6; refused 2 of 2; effective 18 of 18`, met True.
Receipt: .ufo/waves/round-98/w1/MutationC1/pristine-baseline.json

## Mutants (12 single-point), exact labels as printed by the battery
| id | point | change | exit | label | verdict |
|----|-------|--------|------|-------|---------|
| m01 | checksum range | sum(h[4:31]) -> sum(h[4:32]) | 1 | recovered 0 of 18; intact 0 of 6; refused 2 of 2; effective 18 of 18 | killed |
| m02 | checksum modulus | % 251 -> % 255 | 1 | recovered 0 of 18; intact 0 of 6; refused 2 of 2; effective 18 of 18 | killed |
| m03 | format set | PE_FORMATS drops 36 win64/pep | 1 | recovered 9 of 18; intact 3 of 6; refused 2 of 2; effective 18 of 18 | killed |
| m04 | version range | 10..14 -> 10..13 | 0 | frozen target label | SURVIVED |
| m05 | window start | rptr - 64 -> rptr | 1 | recovered 0 of 18; intact 0 of 6; refused 2 of 2; effective 18 of 18 | killed |
| m06 | window length | 1024 -> 512 | 0 | frozen target label | SURVIVED |
| m07 | uniqueness | len(found) != 1 -> < 1 | 0 | frozen target label | SURVIVED |
| m08 | name prefix | startswith(b"UPX") -> startswith(b"UP") | 0 | frozen target label | SURVIVED |
| m09 | .rsrc/UPX2 choice | ternary branches swapped | 0 | frozen target label | SURVIVED |
| m10 | magic write skipped | if ... != MAGIC -> if False and ... | 1 | recovered 6 of 18; intact 6 of 6; refused 2 of 2; effective 18 of 18 | killed |
| m11 | refusal exit code | return 2 -> return 0 | 1 | recovered 18 of 18; intact 6 of 6; refused 0 of 2; effective 18 of 18 | killed |
| m12 | output write skipped | os.replace(tmp, out) -> if False: ... | 1 | recovered 0 of 18; intact 0 of 6; refused 2 of 2; effective 18 of 18 | killed |

Score: 7 of 12 killed; 5 survived (m04 m06 m07 m08 m09).
Cross-checks: all five survivors produced repair output byte-identical to pristine on every
cell (0 differing cells/arms vs pristine-baseline.json); m01/m02/m05 sample cell
(t32,magic) = rc 2 `refused: packheader-candidates:0`; m03 kills exactly the win64/pep
carriers (t64/magic rc 2 refused, t32/magic rc 0 ok); m10 keeps intact arm 6/6 and recovers
only the names-only cells (magic-bearing cells unrepaired).

## Survivor classification (0 equivalent, 5 battery blind spots)
- m04 (version range 10..13): blind spot, not equivalent. UPX 5.2.0 packs version byte 13 on
  all six carriers, so the narrowed range is observationally identical here, but a genuine
  v14 header would newly be refused. The battery never probes version-byte boundaries.
- m06 (window 512): blind spot, near-equivalent in domain. The PackHeader sits at window
  origin for every UPX-packed PE (rptr-64; fallback rptr), so the 1024-byte reach that
  mirrors readPackHeader(1024) is never distinguished from 512.
- m07 (uniqueness < 1): blind spot, not equivalent — the most material finding. The corpus
  always yields exactly one candidate, so the multi-candidate refusal path is untested; the
  mutant would call set.pop() on a multi-element set and may repair at an arbitrary wrong
  anchor (corrupting output) where pristine safely refuses. A decoy-header cell would kill it.
- m08 (prefix "UP"): blind spot, not equivalent. T2 only writes .text/.data/.rdata; a tamper
  leaving an UP-prefixed non-UPX name (e.g. UPDAT) would be skipped by the mutant and lose
  recovery, but no such cell exists.
- m09 (.rsrc/UPX2 flip): dead branch under the battery, not equivalent in general. The
  pristine run emits `name2` zero times: all six carriers keep section-2 name `.rsrc` through
  every tamper (T2 leaves non-UPX-prefixed names alone), so neither the UPX2 path nor the
  rsrc_rva-placement decision is ever exercised. A resource-less carrier (section 2 = UPX2
  after packing) would kill it.

## Restoration evidence
Mutants never touched the clone file (applied to $S/mut/mXX.py copies). After all runs the
restored-bytes detector re-run (restored.json) gave EXIT=0, frozen target label, met True,
and `sha256sum` of clone tools/round-98/upx-pe-repair.py = 2fa1102d320acd8016a05721763c9d57f15a6b92894a67821187d8c825a1dfa4
= pre-run hash of $S/pristine.py. Detector verdicts therefore rest on a passing baseline.

## Receipts (all under .ufo/waves/round-98/w1/MutationC1/)
pristine-baseline.json, m01..m12.json (battery receipts, incl. repair_sha256 per run),
restored.json, mutants.json (mutant list: point, change, mutant sha256, exit, label,
verdict, classification), m01..m12.py (mutant sources, hash-pinned). L1 receipts in
.ufo/waves/round-98/l1/ were not read-modified.

## Bounds and limits
Battery score uses upx 5.2.0 at /usr/bin/upx (preflight-checked each run); carriers
sha256-pinned by the battery itself (no pin mismatches seen — exit never 2). Single rev (L)
in scope; controls at B belong to other seats. Verdict line:

MutationC1: upx-pe-repair.py @7234689 under frozen C1 battery — 12 single-point mutants, 7 killed, 5 survived (m04 version-range, m06 window-reach, m07 multi-candidate-uniqueness, m08 partial-prefix-name, m09 rsrc/UPX2-branch), all 5 battery blind spots, none equivalent; baseline and restored bytes both pass, clone hash unchanged.
