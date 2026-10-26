# R40C2ActionReview — action vocabulary and causes for SquashFS triage table v2, against measured evidence

VERDICT: **DEFECTS FOUND** — all 13 draft labels are supportable and every proposed action token is
grounded in a measured round-39 run (proposal: `w1/artifacts/R40C2ActionReview/actions.md`), but
(1) `avm-marker-be-dropped`'s correct action is **not decidable from envelope fields alone** without a
stated standard-BE-body assumption the draft does not carry, (2) the v1 causes carry six measured
defects (D3/D4a/D4b/D5b/D6/D7) that v2 must fix or it re-freezes false mechanism stories, (3) the
`wrapper-be-then-remove` delivery mechanism remains untested through REA `[INFERENCE]`, and (4) the
v2 counter must score the `(label, action)` pair — v1 scored actions 0% (nonsense-cause mutant 20/20),
so an unscored column would repeat that. Nothing was frozen, nothing outside my two files was written.

Seat: leaf (R40C2ActionReview), no subagents, no background jobs. Axes (godspeed): **depth** primary
(the action column becomes a scored decision surface: v1 carried 9 distinct decisions over 20
envelopes; the v2 draft's unique labels + two `unclassified` action variants give 14); **coverage**
secondary (11-token closed vocabulary over 13 classes + guard + fallback); **calibration** (the two
non-decidable flags prevent false confidence at label level).

## Method

Read the draft claims (`plans/round-40-claims.md`, R40-C2 class list), the v1 table
(`SKILL.md:333-343`) and its rule block, the knowledge entry
(`corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md`), both wave-2 reviews
(`R39W2C2TableReview.md`, `R39W2C2AxisFit.md`), the AVM critic (`R39AssimAvmCritic.md`) and the
routed defects (`corpus/lessons/round-39-verifier-spotcheck.md` §5). Then verified the load-bearing
vectors from committed bytes myself rather than trusting the reviews: K5/K6 `after.json`
(`G=[unpublished-entry] SR=yes P=10/8` — the mixed-symlink shape), H01 envelope
(`provider.id == "unblob"` exactly, `operation == "extract_firmware"`, `subject.local_path` present),
the round-39 held-out manifest (label collisions: `clean-be`/`clean-le` → `clean`,
`version-minor-mismatch` → `body-extractor-failure`), the v1 counter's label-only compare
(`tools/round-39/c2-counter.py:389-390`), the prose domain guard at `SKILL.md:1270`, and that no
round-38/39 artifact exercises the `-be` PATH wrapper (grep over `.ufo/waves/round-3{8,9}/`:
only draft notes marking it `[INFERENCE]`). No REA/unblob run, no carrier built (frozen-carrier
discipline). Tooling: nothing installed or changed.

## Findings (severity-ordered)

1. **HIGH — `avm-marker-be-dropped`: action not decidable from envelope fields alone without a stated
   assumption.** The vector (H=`squashfs_v4_be`, G={extractor-failure}, D=∅, BE=no, P=0) is produced
   both by a marker-only standard-BE body (action: force `-be`; measured exit 1→0 in the critic's
   sasquatch matrix) and by a genuine AVM-layout body failing for an unrelated reason (action: `-be`
   does not fix it; damage triage — S121:4389-4395 forces the wrong reading). R40-C2's "Not claimed"
   list excludes genuine AVM-layout outcomes, so within the claim the row is decidable — but the v2
   row/prose must carry that assumption explicitly, or adopt the critic's carrier-byte disambiguator
   (metadata block-length endianness at `inode_table_start`; exact only on ≤4096-B fixtures) and
   declare that the interpreter reads carrier bytes. Silence here is a guess. Never key on the stderr
   "different endianess" sentence (printed by succeeding and failing runs alike).
2. **HIGH — the v2 counter must score `(label, action)`, not label only.** Round 39 measured the
   failure mode: `c2-counter.py:389-390` compares `label == expected_label`; replacing all eight v1
   cause cells with nonsense scored 20/20 (AxisFit §3c). The draft's "scored together" is the fix;
   the counter design must compare the pair and report distinct row decisions (14 under my
   vocabulary), else the new column is decorative again.
3. **MEDIUM — six measured cause defects in v1 must not be re-frozen in v2.** D3 (escaping row omits
   the symlink-loop branch of `MaliciousSymlinkRemoved`, S118:58-63 — action happens to stay correct);
   D4a (`unpublished-entry` fires for `special` entries too, S119 `firmwareAnalysis.js:137-141` —
   action survives, cause must say "non-file entry"); D4b (absolute targets kept by re-root, not
   "resolve inside"); D5b (a leftover `sasquatch-v4be` wrapper re-adds `-be` exactly when unblob omits
   it, so genuine AVM-BE runs fail and get mislabeled `body-extractor-failure` — both rows' causes need
   the stale-wrapper note, and the action token is `wrapper-be-then-remove`, remove mandatory); D6
   (body-failure cause must restore "or the extractor build"); D7 (dep rows' source cells must cite
   REA as the minter of `missing-extractor-dependency`). All demonstrated or source-cited in
   `R39W2C2TableReview.md` §4.
4. **MEDIUM — `wrapper-be-then-remove` is the only token whose delivery mechanism has no measured run.**
   The flag fix is measured (sasquatch direct matrix); the REA-through-PATH-wrapper path is not —
   wave-1 recorded it `[INFERENCE]` (`w1/R39C2TableDraft.md:144`) and no artifact since exercises it.
   The v2 table must either keep that `[INFERENCE]` marker in the row's source cell or measure it in
   development recon before the freeze (development inputs only).
5. **MEDIUM — `keep-evidence-match-published` (partial-body-failure) is half-measured.** The P>0 shape
   is measured (`full-be1-xz`, exactly one extractor-failure gap, P=6, `w1/R39C2ReconDep.md` §2); the
   "match the published subset to the oracle" half is `[INFERENCE]` — no measured partial run was
   oracle-compared. Marked in the artifact.
6. **LOW — mixed-symlinks needs cell pins AND row order, not either alone.** K5/K6 (re-verified:
   `G=[unpublished-entry] SR=yes`, P=10/8) must hit the mixed row; a v1-style `G=*` escaping cell
   decides by order alone. Pin escaping's `G=∅` and place mixed ahead of it.
7. **LOW — fallback `unclassified` needs action `none`, and the domain guard needs its own action.**
   Out-of-domain → `(unclassified, not-comparable)` (restores the prose guard at `SKILL.md:1270`,
   fixes AxisFit C2 / R39-CL1); no-row-match → `(unclassified, none)` — the table says "action not
   derivable" instead of borrowing a look-alike row's action. Collapsing both to a bare label would
   re-open the silent-mislabel path at action level.
8. **LOW — kill-control interaction.** A trailing `*` default row is inert on the claimed set (every
   class row fires first), so the draft's "best table + `*` default row" control cannot fail unless
   scored with at least one out-of-set envelope. Flagged for whoever owns the control table.

## Residual risk and verification gaps

- I did not run REA or unblob (bounds): all "measured" attributions rest on the round-39 corpus,
  wave reports and committed receipts; I re-verified the vectors I rely on (K5/K6, H01, manifest,
  counter compare) but not the underlying extractor behaviour.
- The timeout corner (`ExtractorTimedOut` records `cmd`, not `command`, so BE reads `n/a`,
  S120 `report.py:125-131`) and compound multi-chunk masking (dep-miss hidden behind a second chunk's
  `SR=yes`; a marker-only chunk inside a publishing container losing the `-be` hint to the partial
  row) are outside the claimed single-chunk family; the v2 block prose must state them as limits.
- `partial-body-failure`'s BE cell: only BE=yes is measured; I propose `*` (nothing else carries P>0
  with an extractor-failure gap, so it shadows nothing), but the v2 generator's actual class emission
  decides the pin.
- Whether the L1 wants clean-empty to share `match-oracle` or take a dedicated token is editorial:
  the scored pair distinguishes via the label either way.

Full proposal with per-label signatures, tokens, evidence and decidable-status:
`w1/artifacts/R40C2ActionReview/actions.md`.
