# ScoutPinmapSites — R17-PINMAP site census

Baseline `9011581d84527ba34c675f9cf912e54d2e72d470`. Read-only: this file only.
Question: every lane text site at the baseline stating that mid-run pin maps are retained,
plus the accurate replacement wording, grounded in `.ufo/waves/round-17/tools/carrier-run.py`.

Worktree at the cited tracked files is byte-identical to the baseline
(`git diff --stat 9011581d -- corpus SCORECARD.md LOG.md SKILL.md` → empty, exit 0), so
working-tree line numbers equal baseline line numbers.

## 1. Observation — what the producer actually retains

`.ufo/waves/round-17/tools/carrier-run.py:481-487` (mid-run, throttled `PIN_CHECK_S`):

```json
rec.setdefault("pin_checks", []).append({
    "taken_at_utc": mid["taken_at_utc"],
    "equal": cmp_mid["equal"],
    "entries": len(mid["entries"]),
    "changed": cmp_mid["changed"],
    "missing": cmp_mid["missing"],
})
```

- `entries` is an **integer path count**, not the map. `equal` is `pins.compare(pins_pre, mid)`
  (`:480`) — a verdict relative to the retained **pre** map (`pins.py:75-106`).
- No per-path map, no map digest, no `pins/mid-*.json` write exists at this revision
  (`grep -n "mid-" carrier-run.py` → no match).
- Pre/post maps **are** retained in full: `receipt["pins_pre"]` at `carrier-run.py:336-337` and
  `receipt["pins_post"]` at `:385-387`; each snapshot is
  `{entries:{path:{sha256,size,mtime_ns}}, taken_at_utc, monotonic_ns}` (`pins.py:56-71`).
- Adjacent precision gap: `pins.compare` also returns `errors` (`pins.py:103`), but both retention
  sites drop it (`carrier-run.py:485-486`, `:489-491`). `[INFERENCE]` An unreadable mid-check path
  therefore yields `equal:false` with `changed:[]`/`missing:[]` — a failure with no named path.
- Receipt aggregate (8 HEAD receipts): `pin_checks` count per analyze step ∈ {2,3,4,8}; every
  entry has exactly the five keys above, `equal:true`, `entries:146`; `pins_pre`/`pins_post` each
  146 paths.

## 2. Sites that overstate (mid-run *maps* asserted)

| # | anchor | exact overstated phrase | why it is false |
|---|---|---|---|
| 1 | `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:30-32` | "each pin map is retained with its UTC instant: pre, every 30 s during analyze (2–8 checks per run, `steps.analyze.pin_checks`), and post. All maps are equal." | The universal "each pin map" includes the mid-run instants; only pre/post maps exist. Mid instants keep verdict+count (`carrier-run.py:481-487`). "2–8 checks per run" and "all equal" are themselves verified correct. |
| 2 | `SCORECARD.md:2374` | "and carries pre/mid/post pin maps with instants" | Same: mid-run carries no map. |
| 3 | `corpus/lessons/round-17.md:90` | "the entry states identical bytes at those instants only" (full clause: "Every mid-run check is retained with its instant (second pass: 2–8 per run, all equal); the entry states identical bytes at those instants only; ...") | First clause is accurate ("check ... with its instant"; 2–8 verified). Second clause vouches for a correction that did not happen while site 1 still says each map is retained. This site is **not** listed in `round-17-verifier-spotcheck.md:137` — it is an additional site. |

### Accurate replacements

**Site 1 (reword, keeps the verified numbers):**

```text
  frozen prediction, and all 143 installed Go data files. In the second pass
  the per-path maps are retained for pre and post only; each mid-run check
  retains its UTC instant and the comparator verdict against the retained pre
  map (`{taken_at_utc, equal, entries:int, changed, missing}`,
  `steps.analyze.pin_checks`, `carrier-run.py:481-487`), not its own map.
  Every recorded verdict compares equal (2–8 checks per run; 8/8 receipts).
  They show identical bytes **at those instants** only (QUALITY #19). The
  first-pass receipts kept only pre/post maps.
```

**Site 1 (append-only correction line, the r16 form — see §4):**

```text
- R17-PINMAP: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:30-32` mid-run instants retain the comparator verdict against the retained pre map and a path count, not a per-path map; per-path maps (146 paths, sha256+size) are retained pre and post only (`carrier-run.py:481-487`).
```

**Site 2:** replace "and carries pre/mid/post pin maps with instants" with
"and carries pre and post per-path pin maps with instants (146 paths each, sha256+size) plus mid-run
instants that retain the comparator verdict against the pre map (`pin_checks`)".

**Site 3:** replace "the entry states identical bytes at those instants only" with
"the entry states the pre/post maps equal and the mid-run verdicts equal at those instants, and does
not claim a mid-run map". (Or, once site 1 is corrected, cite the corrected anchor.)

## 3. Criterion vs observation — `corpus/QUALITY.md:29`

`QUALITY #19` is a **standing requirement**, not a claim about r17:
"the producing tool keeps each pin map (per-path SHA-256 and size) with its UTC timestamp and the
comparison verdict, including mid-run checks, plus a retained red run in which a mutated path is
named and the comparison fails."

- It is not itself an overstatement, and correcting it downward would remove the bar the round-17
  fix is measured against. Recommendation: leave #19 unchanged.
- It is **unmet** by the r17 producer for mid-run instants (observation §1). The knowledge entry
  cites "(QUALITY #19)" at `:33` as if met — that citation is part of site 1's overstatement.
- The round-18 C1 fix (`contract.md:128-131`: full mid map to `DIR/pins/mid-<n>.json` plus
  `map_path`/`map_sha256`, validator recompute) makes **future** runs satisfy it. It cannot
  retro-fix r17: `claims.json` non_goals include "no edit of round-17 retained receipts/logs".
  So r17 prose still needs the §2 corrections (or a revision-scoped qualifier such as "from the
  round-18 revision onward").

## 4. Discharge form (precedent)

The r16 routed defects were discharged by **append-only named corrections in the next round's
lesson file**, not by editing the filed bytes:
`corpus/lessons/round-17.md:94` heading `### R16-PROVENANCE named corrections (append-only; filed bytes unchanged)`,
one line per site at `:96-99`; `corpus/lessons/round-16.md:154` and the r16 entry `:95` still read
"remained unchanged during execution". The R17-PINMAP analog is a
`### R17-PINMAP named corrections (append-only; filed bytes unchanged)` block in
`corpus/lessons/round-18.md` with one line per site (1, 2, 3 above).

## 5. Checked and clean (not sites)

- `LOG.md:2086-2087` "every mid-run pin check retained, exit 1 on drift" — says *check*; accurate.
- `SKILL.md:537` "pins equal at every recorded instant" — accurate, no map claim.
- `SKILL.md:541` "mid-run-drift finding" — accurate.
- `.ufo/waves/round-17/contract.md:138-139` "mid-run pin check retained in `steps.<name>.pin_checks`" — accurate requirement.
- `corpus/lessons/round-17.md:106` "cites retained second-pass checks" — accurate.
- `corpus/lessons/round-17.md:81` "retaining every pin check with its instant" — accurate.
- `.ufo/waves/round-17/w2/draft-log-measured.md:47-52` — already states the truth and offers the alternative wording ("pre and post maps only; mid-run checks not retained").
- `.ufo/waves/round-17/w2/{CriticC1Admission.md:18-26, ReviewLessonMistakes.md:93-95, ReviewProvenanceCorrections.md:20-23, ReviewTrendVerdicts.md:84-102}` — these already *find* the defect; historical drafts, not claims to correct.
- `corpus/lessons/round-17-verifier-spotcheck.md:108,137` — correct as written; `:137` simply omits site 3.
- `.ufo/waves/round-17/w1/*` "pre/post pin maps" mentions (`ScoutCarrierPackages.md:100`, `ReviewCapabilityTable.md:103,123`, `SimplifyTools.md:151`) — pre/post only; accurate and advisory.

## 6. Remaining unknowns

- Whether L1 prefers the reword or the append-only correction line for site 1 (both given; the
  r16 precedent is append-only). `[INFERENCE]`
- Whether the round-18 mid-map write will also retain `errors` (not specified at
  `contract.md:128-131`); if not, the §1 unreadable-path gap survives the fix.
- First-pass (`da64646`) receipts were not opened for this question; the aggregate in §1 covers the
  8 HEAD receipts only. `[INFERENCE]` their pin fields match the `da64646` producer described at
  `round-17-verifier-spotcheck.md:137` (no `pin_checks`).

## 7. Commands exercised (argv, exit)

```text
git rev-parse HEAD                                         -> 9011581d84527ba34c675f9cf912e54d2e72d470, 0
git grep -n -i -E "pin maps?|maps are equal|pre/mid/post|each pin map" 9011581d -- '*.md' '*.txt'   -> matches listed above, 0
grep -n "pre/mid/post\|pin map\|pin_checks\|maps are equal\|mid-run check\|mid-run pin" SCORECARD.md LOG.md SKILL.md corpus/QUALITY.md corpus/lessons/round-17.md corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md -> 0
python3 (aggregate .ufo/waves/round-17/runs/*/receipt.json pin_checks/pins_pre/pins_post) -> 0
git status --porcelain -- corpus SCORECARD.md LOG.md SKILL.md .ufo/waves/round-17 -> empty, 0
git diff --stat 9011581d -- corpus SCORECARD.md LOG.md SKILL.md -> empty, 0
grep -n "snapshot(\|pins_pre\|pins_post\|mid-" .ufo/waves/round-17/tools/carrier-run.py -> 0 (no mid map write)
```

No installs or upgrades were performed. No REA/Ghidra analysis, no carrier execution, no jj/git write.
