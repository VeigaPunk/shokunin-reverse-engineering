# CriticClaim — adversarial review of R87-C1 (round 87, kaidoku)

Role: critic, read-only on production files. Scratch `/fast/scratch/hyaku/kaidoku-r87/CriticClaim/`
(deleted at yield; receipts copied into `receipts/` here). All commands cited reproduce from the
receipts; no packed/tampered binary is committed.

## Headline verdict

**R87-C1 survives as a predicate; its declared difficulty rationale is falsified by measurement.**
A ~60-line chain-walk-free repair (`v4`) scores the frozen predicate exactly as the committed tool:
`recovered 8 of 8`, `controls_ok` all true, `met=True exit=0` — **with REA enabled**
(`receipts/cheap-v4-checksum-lite-rea.json`), and its 8 outputs are **byte-identical to
`tools/round-87/upx-magic-repair.py`'s outputs** on this population. The frozen plan's supporting
sentence — "The target is therefore failable by the cheap rule: it needs the zeroed class, which
only a structural repair reaches" — is wrong as a discriminant: the zeroed class is reached by a
cheap rule the counter cannot separate from the committed tool.

## Attacks (cheap repairs scored with the frozen counter)

All runs: `python3 -I -B tools/round-87/upx-tamper-battery.py --root . --repair-cmd
<variant> --upx /usr/bin/upx --work <scratch>/work-<n> --json-out <receipt>` from the lane root;
carriers/packer pins passed preflight (upx 5.2.0 sha256 cf2f6e7c…c969; carrier sha256 match).
`--no-rea` receipts record `recovered 0 of 8` by construction (see Finding F4); the per-attack
column is **non-REA-recovered**, counted from per-case arms `repair_rc0, windows_only, test_ok,
identity`.

| # | Cheap repair (script in scratch `var/`) | non-REA | N1 | N2 | N3 | Receipt | Verdict |
|---|---|---|---|---|---|---|---|
| A1 | v1 fixed offsets learned from jq ({556, len-3065, len-44, len-36}) | 2/8 | false (rc 0 ×4) | true | true | `receipts/cheap-v1-fixed-offsets-no-rea.json` | claim survives |
| A2 | v2 every window == word at len-36 except zero-runs >12 / >24 | 4/8 / 4/8 | false | true | true | `receipts/cheap-v2-thresh12-no-rea.json`, `receipts/cheap-v2-thresh24-no-rea.json` | claim survives |
| A3 | v3 last two windows before EOF only | 0/8 | false | true | true | `receipts/cheap-v3-lasttwo-no-rea.json` | claim survives |
| A4 | v4 checksum-PH + version/format l_info + zero-surround sentinel (no b_info walk) | **8/8** | **true** | true | true | `receipts/cheap-v4-checksum-lite-no-rea.json`, **full REA: `receipts/cheap-v4-checksum-lite-rea.json`** | **target not failable enough — WEAKENED** |

Why the failures fail: A1 restores wrong anchors on xxd/libz/dinit (layout not universal: l_info at
556/556/9284/556; sentinel at len-44/len-44/len-1859/len-46) and cannot refuse plain originals
(N1 false — no structural test at all). A2 rewrites 162 zero windows on jq T1 (payload/stub zeros)
→ `windows_only` true but `upx -t` fails. A3 restores a pad window and misses libz's sentinel
(1859 bytes from EOF) and every l_info. N1 is the only control any of A1–A3 fails, and N1 is
satisfiable by one checksum scan (A4 does exactly that).

### A4 detail (the falsifying counterexample)

- Rule: refuse non-LE-ELF; intact passthrough if `d[-36:-32] == UPX!` (N3); else scan the tail 512
  bytes for a 32-byte window validating the PackHeader checksum (which excludes the magic, so it
  validates under T1/T2); restore `UPX!` at that offset; restore at the first offset whose bytes
  `+6/+7` equal the PackHeader version/format and whose u32 at `+16` equals `u_file_size` (l_info);
  restore at the first tamper-value window with four zeros either side wholly before the PackHeader
  (sentinel). No `b_info` chain walk, no block plausibility, no first-matching-chain semantics.
- Full-REA receipt: `recovered 8 of 8`, controls true, exit 0; per-case REA counts 167/99/184/1268
  — identical to the committed tool's declared counts (cross-checked against
  `.ufo/waves/round-87/l1/scores/rea-candidate/*.json`, same deterministic `evidence_id`s).
- Byte-identity to the committed tool: all 8 repaired outputs hash equal
  (reproduced in scratch `cmp/`; my packing equals the battery's packing on all 8 —
  `packed_sha256` match — so this is one population, one set of bytes).
- Falsifies: plans/round-87-claims.md, cheap-rule control paragraph: "…needs the zeroed class,
  which only a structural repair reaches." The frozen counter does not force the structural work
  (chain walk); it forces only checksum validation + anchor heuristics.
- Does NOT falsify: the predicate itself (the committed repair passes it; the kill rules — recovered
  <8, controls, window discipline, provenance clause — all still pass; v4 takes only `--in/--out`
  and names no pin, so even the provenance clause is not what separates them).

## Out-of-population tampers (limits, not changes — jq, committed repair)

| Tamper | pre `upx -t` | repair | `upx -t` after | `upx -d` → pin | Limit exposed |
|---|---|---|---|---|---|
| T3 per-anchor values (l_info→AAAA, sentinel→BBBB, PH→CCCC) | FAIL | rc 0, 3 anchors | PASS | PIN-MATCH | repair generalizes past the two frozen values — population narrower than tool |
| T4 only l_info → 00000000 | FAIL | rc 0, 1 anchor | PASS | PIN-MATCH | single-anchor tamper is detectable AND repairable, but outside the frozen population (population tampers hit every magic word) |
| T5 T2 + p_info.p_filesize zeroed | FAIL | rc 0, 3 anchors | **FAIL** | **rc 1** | one adjacent field defeats the tool; the repair locates p_info (find_linfo uses it) but never repairs it |
| T6 `$Info: This file is packed with the UPX…` string removed | **PASS** | rc 0 "intact" | PASS | PIN-MATCH | tamper ineffective against -t/-d, so the population's own precondition (`upx -t` non-zero) excludes this class; only `-l` banner output would notice |

Scratch transcript of this table was produced by the commands in `oop/`; receipt-equivalent evidence
is the pinned jq sha256 `e815667…7806` match / mismatch recorded above (paths deleted with scratch;
values are reproducible from the commands and pins).

## Axis-fit judgment (part 3)

- **Coverage is the right axis.** This is a Frontier→Core surface move demonstrated by an
  end-to-end capability (tamper → repair → `upx -d` → pinned bytes → REA count), on a frozen,
  pinned population. Not quality dressed as coverage.
- **The predicate is free of unenumerated universals.** The frozen sentence enumerates its five
  arms and "controls_ok all true" maps to exactly the three named controls; the kill rule
  enumerates its clauses. No "always/never" clause beyond the enumeration.
- **Weakened discriminative power, not axis misfit.** F4/F5 below mean the counter saturates at
  8/8 for anything past naive-global; the coverage signal lives almost entirely in N1 (refusal)
  plus the do-nothing/naive controls. A future round could freeze one saturating-cheap-rule control
  (e.g. A4) to restore signal — a finding, not a change I may make.

## Findings (numbered)

- **F1 (weakened, falsified rationale):** the counter cannot distinguish the committed structural
  repair from a chain-walk-free cheap rule; both score 8/8 with byte-identical outputs. The plan's
  "only a structural repair reaches the zeroed class" is false as stated. Predicate unaffected.
- **F2 (limit):** out-of-population robustness is broader than frozen (T3, T4 recovered) but
  one-field-adjacent corruption (T5) and banner-only tampering (T6) are unrepaired/unreachable.
  Declared now as limits; the frozen population need not change.
- **F3 (limit, already declared in plan):** provenance is unscored; A4 re-confirms it (a cheap rule
  with no provenance and no chain walk passes even the review-enforced `--in/--out` clause).
- **F4 (counter quirk):** under `--no-rea` the receipt label always reads "recovered 0 of 8"
  (`rea_recover` pinned false, `recovered = all(arms)`); non-REA pre-checks must read per-case
  arms. Misleading label, no effect on the frozen predicate (which runs with REA).
- **F5 (REA arm is not a repair discriminator):** `rea_recover` is fully determined by `identity`
  (restored bytes are pinned-identical → identical `evidence_id`/counts, shown by the 12 committed
  evidence files where T1/T2 rows for a carrier share one `evidence_id`). It verifies the
  end-to-end unpack (capability evidence) but cannot separate repairs.
- **F6 (positive):** controls N1/N2/N3 each exclude real degenerate classes (identity, naive-global,
  offset/word heuristics A1–A3 all fail at least N1 or an arm); packing is deterministic (my
  scratch packing == battery packing on all 8), and the counter is selftest-clean
  (`.ufo/waves/round-87/pre/c1-counter-selftest.txt`).

## Smallest safe correction

None available to me (frozen files may not change). Recommended to the L1, as findings only:
freeze A4 as a second cheap-rule control in a future counter revision, and reword the plan's
"only a structural repair reaches" sentence if the round is re-declared.

## Tooling authorization record

No tool installed or upgraded (upx 5.2.0, python3, node all present and pinned — pacman untouched).
