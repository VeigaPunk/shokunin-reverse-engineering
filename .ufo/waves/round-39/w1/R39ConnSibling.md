# R39ConnSibling — sibling-overlap scan for R39-C1 / R39-C2 (round 39 wave 1, pre-freeze)

**Verdict: CONFIRMED** — no sibling lane under `/home/vgpnk/Projects/shokunin/*-shokunin` duplicates
R39-C1's Core ground (standard big-endian SquashFS v4 Frontier→Core) or R39-C2's (a SquashFS
`extract-firmware` outcome-triage instrument). Both claims move kaidoku-local ground only. One live
adjacency finding (revenger firmware row, ADJ-06 open) and five reusable held-out/seed instrument
patterns found; none is a seed-from-freeze-commit counter, so R39-C2's `heldout-gen.py`
seed = freeze-hash design is novel fleet-wide [INFERENCE from the greps below].

Seat: `R39ConnSibling` (leaf, connector, godspeed). Date: 2026-10-26. Lane root:
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. This scan is read-only; the only write is this
report. No tools installed (nothing needed; pacman pause respected). No git mutation.

---

## 1. Method

Targeted greps over all 20 sibling lanes (`audio, chousa, game-dev-2d, game-dev-3d, kagi, kake,
kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi,
tameshi, tsukuroi`) for four pattern families, then close reads of every hit that looked like
ground (not a seat log):

1. `squashfs|sasquatch|unblob` (substrate)
2. `extract-firmware|rea-agents|extract_firmware` (REA receipts)
3. `triage|decision.table|held.?out|seed.*freeze` (instruments)
4. `unsquashfs|mksquashfs|sqfs|\.sqsh|avm` (carriers/oracles/AVM marker)

Plus: `seed.{0,40}(commit|freeze)` over every lane's `plans/` + `tools/`; PROVINCE/SKILL/corpus
reads of revenger (nearest REA sibling), souji (fixture-vault hits), tameshi (verification craft);
fleet `.ufo/l0-questions.md`; the shokuknow merge mirror (read-only). Exact commands in §7.

## 2. What kaidoku itself already holds (the surfaces R39 moves)

- `PROVINCE.md:156-157` — Round-4 Frontier bullet **sasquatch** ("big-endian/AVM stays here").
- `PROVINCE.md` Round-36 Core row + `:372/:376` notes — LE v4 promoted (r36); standard BE v4
  measured through `sasquatch-v4be` in r38 and **not** promoted (R38-C1 honest stop on K2's
  `unpublished-entry` symlink gap). R39-C1 re-runs this promotion with the symlink rule stated
  before data and six carriers.
- `SKILL.md:1231-1243` — round-36 LE-only decision table (signal→meaning→action, prose recall).
  R39-C2 replaces/deepens it with a machine-readable triage table + held-out seeded counter.
- `plans/round-39-claims.md` — the DRAFT this scan feeds.

## 3. Sibling ground, surface by surface

### 3.1 SquashFS / unblob / sasquatch / firmware-extraction substrate

| Lane | What exists | Path | Relation to R39 |
|---|---|---|---|
| **revenger** | Firmware *province claim* and one held C07 row: a **manual byte readout** of an authored 2048-byte fixture against a saved `inspect_firmware_regions` record; scope sentence explicitly excludes the `extract_firmware` route | `PROVINCE.md:3-5`; `corpus/README.md:43`; `corpus/knowledge/round-64-firmware-region-byte-evidence.md` (header + scope) | Adjacent, **not duplicating**. No SquashFS anywhere in the lane. |
| **revenger** | unblob external-dependency census: `unblob --show-external-dependencies` → 15 names, 5 present / 10 missing incl. `sasquatch`, `sasquatch-v4be` (probe 2026-10-25); assimilation drafts + gate re-derivations | `.ufo/waves/round-70/w1/R70W1AssimUnblob.md:61-89`; `w2/R70W2AssimGateA.md:50-53`, `R70W2AssimGateB.md:30-36`; mirrored at `shokuknow/merge/revenger/knowledge/corpus/knowledge/firmware-extractor-dependency-degradation-2026-10-23.md` | Host-tooling census only; supports kaidoku's provider story, owns no BE ground. |
| **revenger** | Round-63/64 connector fences: "must not run `extract-firmware` or any payload"; "does not absorb kaidoku Core live `inspect-firmware-regions`/`extract-firmware`" | `.ufo/waves/round-63/build/R63ConnectorOverlap.md:36-42`; `round-64/R64ConnectorOverlap.md:14-16,45`; `corpus/knowledge/round-64-firmware-region-byte-evidence.md:203` | Explicit non-absorption; ADJ-06 arbitration still open at fleet `.ufo/l0-questions.md:42` (tsukuroi r1: "arbitrate the kaidoku/revenger shipped-artifact overlap before an ADJ-06 analysis is routed"; no L0 answer on that entry). |
| **souji** | No own ground. The only sasquatch hits are copies of a `Frontier-Queue.md` inside census *test vaults* | `census/round-26/waves/assimilation/validate/tests/vault/fixture-src-*/atlas-dir-*/Frontier-Queue.md:7` ("sasquatch build (AUR) → unblob squashfs recursion") | Test-fixture text, not lane knowledge; grep of souji `PROVINCE.md`/`SKILL.md`/`corpus/knowledge`/`corpus/lessons` = zero hits. |
| **game-dev-3d** | REA provider census (jadx 1.5.6 / binwalk 3.1.0 / unblob 26.6.4 present; Ghidra/pwntools absent) and REA `inspect-artifact` receipts on authored GLB/ZIP carriers | `corpus/knowledge/rea.md:37-56`; `corpus/lessons/r9-glb-review.md`, `r10-zip-review.md`, `r10-rea-zip-carrier.md` | REA-adjacent tooling note; verb is `inspect-artifact`, no firmware, no SquashFS. |
| **kengaku** | One connector scan noting kaidoku's sasquatch Frontier line as **unrelated** to its domain | `.ufo/waves/round-26/build/ConnRosterScan.md:16` | Negative evidence of overlap. |
| **kake / kama / kagi** | REA MCP registration only, disabled / attested | `kake-shokunin/.ufo/waves/round-50/w1/SentinelWriteScope.md:109-111`; `kama-shokunin/.ufo/waves/round-29/w2/MisrootSweep.md:178`; `kagi-shokunin/.ufo/waves/round-20/pane-attestation.json:42-46` | Config debris, not ground. |
| **audio, chousa, game-dev-2d, kasegi, kotoba, kotodama, kumitate, lore, mado, mori, tabi, tameshi, tsukuroi** | No `squashfs`/`sasquatch` ground (`tsukuroi` owns driver/firmware *health* only and filed ADJ-06) | e.g. `tsukuroi-shokunin/PROVINCE.md:3-4,51` | None. |

Carrier/oracle shapes (`unsquashfs`, `mksquashfs`, `.sqsh`, `avm`): zero lane hits (only ffmpeg
`avm2` and tmp-path noise in audio/game-dev-2d). The AVM-marker BE body is kaidoku-unique in the
fleet.

### 3.2 REA `extract-firmware` receipts

No sibling holds a committed `extract-firmware` receipt. `extract-firmware` strings appear only in:
revenger's quoted REA guide snapshots (`.ufo/waves/round-63/source-snapshots/rea-firmware-guide.md:89-92`,
`round-64/...:56-59`) — documentation of the verb's CLI shape, not receipts; revenger's fence
sentences; and kaidoku's own material. Kaidoku remains the only lane that has ever run the verb
(r36 LE carriers; r38 BE probe envelopes under kaidoku `.ufo/waves/round-38/w2/artifacts/R38W2AvmProbe/`).

### 3.3 Outcome-triage / decision-table instruments

No sibling holds an extraction-outcome triage table. Decision-table *craft* exists but in other
domains: audio's threshold/calibration tables (`audio-shokunin/corpus/knowledge/2026-10-12-threshold-calibration.md`;
scribe drafts `reports/round-10..r23/r*-scribe.md`) and kotodama's verification triage protocol
(`tools/gates/frozen/provenance-audit/*/to-verify-triage-protocol.md`) — neither touches REA or
firmware. Kaidoku's round-36 table (`SKILL.md:1231-1243`) is the only extract-firmware outcome
table in the fleet, and R39-C2 explicitly supersedes it.

## 4. Held-out / seed counter designs — reusable?

The fleet has five held-out/seed instrument families worth mining for C2's design (none keyed to a
freeze commit hash):

| Lane | Instrument | Path | Reusable idea for R39-C2 |
|---|---|---|---|
| **tameshi** | Sealed held-out runner-copy set + replay-as-selftest-seeds: round-32 held-out mutants (`HeldOutPrintf-1/2`, `HeldOutGuard-1/2`, `HeldOutTallyArms-01/02`, `HeldOutLoop-1`, `HeldOutRefactor-a3/a4/k1`) defeat a tally counter; sealed copies at `.ufo/evidence/round-32/heldout/` | `tools/tally-audit-v2.py:12-28,363,615-628`; `tools/tally-audit-v3.py:44-48`; witness freeze at `tools/bash-witness-study.py:1745` | Class-per-vector labeling + sealed evidence replay — the closest structural match to "held-out envelopes scored against a frozen interpreter". |
| **chousa** | Pre-registered held-out inventory (33 quotes, sha256-pinned `held-out.tsv`) built before wave 2; controls CtlAlwaysAbsent / CtlRawGrep; "void-before-data" rule and "refreeze a replacement design using source-backed held-out positives" | `.ufo/waves/round-29/build/ScoutGateQuotes/held-out.tsv`; `controls/CtlAlwaysAbsent/report.md:73-74`; `controls/CtlRawGrep/report.md:99-102` | Pre-registration discipline: manifest hash published before data exists; freeze-void kill language kaidoku can mirror in the C2 kill rule. |
| **audio** | Named non-author verifier classifies 13 held-out allowed/refused/uncertain cases before a box is checked | `LOG.md:415-428`; `reports/round-24/r24-verifier.md:5-60` | Held-out *evaluation* owned by a non-author seat — matches C2's "generator assigns labels before any REA run". |
| **mori** | `mori-silence-cases.sh`: Fisher-Yates shuffle of 28 case ids via xorshift32 **seeded from a pinned env seed** (`MORI_SHUFFLE_SEED`), same seed ⇒ same order | `tools/mori-silence-cases.sh:81-82` | Deterministic pinned-seed selection; C2's `seed = freeze commit hash` is the strictly stronger commit-anchored version. |
| **kama / kengaku** | Seeded randomized offline fixture audits (`round41-pinwatch-audit.py:28`, `round42-digest-audit.py:47`, "CASES randomized offline fixture cases (seeded)"); seeded-mutant kill selftest where "every seeded mutant must be killed" | `kama-shokunin/tools/round41-pinwatch-audit.py:28`; `kengaku-shokunin/plans/parser_policy_compare.py:354,574` | Seeded fixtures + mandatory-mutant-kill selftests for the counter itself. |

`grep -rn -i -E "seed.{0,40}(commit|freeze)|freeze.{0,40}seed|seeded" <all-lane plans/ tools/>`
returned **no sibling hit keyed to a freeze commit**; the only `seed = freeze` match in the fleet
is kaidoku's own `plans/round-39-claims.md:65`. So: R39-C2's seed-from-freeze held-out generator
has no sibling design to absorb; tameshi/chousa are the best craft references. Kaidoku's own
round-34 (`tools/round-34/mini-fix/build.py`, deterministic rebuild from `spec.json`) is the
in-lane precedent for deterministic fixture regeneration.

## 5. Answers to the seat questions

1. **Which siblings hold the ground?** Only **revenger** holds REA firmware ground (C07 held row,
   r70 unblob dependency census), and it is *reported-not-absorbed* against kaidoku with fences
   against running `extract-firmware` — see §3. game-dev-3d holds REA `inspect-artifact` craft;
   souji holds nothing (vault copies only); every other lane's hits are config debris or
   connector notes. Paths in §3.1–3.3.
2. **Do R39-C1/C2 duplicate a sibling's Core ground?** **No.** R39-C1 (BE SquashFS v4 promotion)
   duplicates nothing — no sibling has SquashFS carriers, oracles, or BE extraction receipts;
   revenger's firmware row is an authored-fixture region readout that excludes the extract route
   and stays on its side of the open ADJ-06 (`fleet .ufo/l0-questions.md:42`). R39-C2's triage
   table duplicates nothing — the only extract-firmware outcome table is kaidoku's own r36 LE
   table. **Adjacency axis (report, do not absorb):** revenger's PROVINCE still names
   "archives, firmware" and its README C07 row is `held`; kaidoku should keep the C1 promotion
   scoped exactly to "standard big-endian SquashFS v4" (as the draft claims do) and should not
   cite revenger's fixture row as either supporting or conflicting evidence. Tsukuroi's ADJ-06
   arbitration request remains the operator-owned route for the domain overlap; nothing in R39
   presumes its outcome.
3. **Held-out / seed-from-freeze design to reuse?** No sibling has a seed-from-freeze counter.
   Reusable craft (not absorption): tameshi's sealed held-out replay set (`tally-audit-v2/v3.py`),
   chousa's pre-registered held-out manifest + void-before-data kill (`round-29` controls),
   audio's non-author held-out classification (`r24-verifier`), mori's pinned-seed shuffle
   (`mori-silence-cases.sh:81-82`). Suggested non-binding borrow for the L1: have the frozen
   `heldout-gen.py` print its seed derivation (freeze hash → PRNG) like mori's pin line, and pin
   the held-out manifest sha256 in the freeze commit like chousa's `held-out.tsv`.

## 6. Risks / notes for the L1

- ADJ-06 is open; if the C1 freeze commit lands revenger-adjacent language beyond "standard
  big-endian SquashFS v4", tsukuroi's question escalates. The draft claims' "Not claimed" line
  already fences this — keep it.
- Revenger's r70 census records `sasquatch`/`sasquatch-v4be` as *missing* on the host on
  2026-10-25; kaidoku's r38/r39 work uses both from `~/.local/bin`. That is a host-state
  divergence across lanes' notes, worth one sentence in the C1 knowledge entry so a fleet reader
  does not mistake revenger's apt-line census for kaidoku's runtime PATH.
- Shokuknow mirrors both lanes (`merge/kaidoku/knowledge/.../sasquatch-unblob-dependency.md`,
  `merge/revenger/knowledge/.../firmware-extractor-dependency-degradation-2026-10-23.md`) — mirrors
  are downstream of lane knowledge, not independent evidence.

## 7. Evidence appendix (commands; all read-only)

```sh
# lane listing
ls -d /home/vgpnk/Projects/shokunin/*-shokunin          # 21 lanes incl. kaidoku
# substrate / REA / instrument sweeps (grep tool, 20 sibling lanes, patterns in §1)
# -> hits summarized in §3; zero .sqsh/unsquashfs/avm-carrier hits
grep -rn -i -E "squashfs|sasquatch|unblob|extract-firmware" \
  /home/vgpnk/Projects/shokunin/{revenger,souji,game-dev-3d}-shokunin/{PROVINCE.md,SKILL.md,corpus}
# revenger C07 row + scope sentence
sed -n '1,20p' revenger-shokunin/PROVINCE.md
grep -n -E "C0[4-8]|firmware" revenger-shokunin/corpus/README.md   # C07 = held, r64 entry
sed -n '1,60p' revenger-shokunin/corpus/knowledge/round-64-firmware-region-byte-evidence.md
# ADJ-06 open question
sed -n '38,46p' /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md   # :42 tsukuroi r1, no answer
# held-out/seed designs
grep -rn -i -E "freeze|held.?out" tameshi-shokunin/tools/ | head
grep -n "seed" mori-shokunin/tools/mori-silence-cases.sh    # :81-82 xorshift32, MORI_SHUFFLE_SEED
grep -rn -i -E "seed.{0,40}(commit|freeze)" /home/vgpnk/Projects/shokunin/*/plans/ /home/vgpnk/Projects/shokunin/*/tools/ \
  | grep -v kaidoku-shokunin   # -> no freeze-seeded sibling design
# kaidoku own surfaces
sed -n '139-163p' kaidoku-shokunin/PROVINCE.md     # frontier bullet :156-157
sed -n '365-380p' kaidoku-shokunin/PROVINCE.md     # r36 row + r38 note :372/:376
sed -n '1220-1265p' kaidoku-shokunin/SKILL.md      # r36 LE decision table 1231-1243
# shokuknow mirrors (read-only)
ls /home/vgpnk/Projects/shokuknow/merge/{kaidoku,revenger}/knowledge/corpus/knowledge/ | grep -iE "sasquatch|unblob|firmware"
```

Tooling record: no installs/upgrades this seat (read-only scan; pacman transactions remain paused
per operator directive; nothing fetched).
