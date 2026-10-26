# R41W2Sibling — cross-lane pattern check: do sibling counters share the two round-41 defect classes, and who guards?

**Verdict: DONE.** I attacked the cross-lane pattern question for the two round-41
defect classes: (1) **generator/counter declared-key mismatch** (counter reads a
declared field under a different key than the generator writes → silent false
binding) and (2) **commit helper skipping large evidence files**. Findings:
**class 2 is fleet-wide by construction** — the only commit writer in every lane
(`scripts/hyaku/jj-lane.sh`) silently drops new files > 1 MiB inside a *named
directory* commit (post-hoc stderr warning only), with confirmed incidents in
kaidoku (V4 `after.json`), kama (round 26, round 35) and mado (round 33/34).
**Class 1's exact key family exists only in kaidoku** (zero sibling hits for
`class_expected`/`declared_features`/`declared`), but a pattern-level instance is
documented and guarded in tameshi; the strongest sibling *mechanical* guards are
kama's `instrument-agreement.py` (undeclared volatility = disagreement), chousa's
drift baseline, and kotodama/souji fail-closed schemas. No sibling lane prevents
class 2 in the helper itself; guards are detection-only (kaidoku
`evidence-tracked.py` M41-3, mori `mori-unlanded-check.py`).

---

## 0. Axes (report-scoped)

- **coverage** — how many lanes/counters were actually examined for each defect class.
- **depth** — path:line precision for instances and guards; distinguishing detection vs prevention.
- **calibration** — no overclaiming: instances vs guards vs not-inspected are kept apart; negative evidence (grep zero hits) is reported as such.

## 1. The two defect classes, pinned from the kaidoku landing

### 1.1 Class 1 — declared-key mismatch (silent false binding)

Canonical instance (the C2 honest stop):

- Writer `tools/round-41/heldout-gen-v3.py` puts the six-field binding tuple under manifest key **`declared`** for every carrier: named classes at line 1372 (`'declared': declared_tuple(features)`), combos at line 1464; combos explicitly get `'class_expected': None` (lines 1467–1475: "A combo has no class label … so this field is null by design").
- Reader `tools/round-41/c2-counter.py` lines 1486–1506 looks for the tuple under `class_expected.features`, then `features`, then `declared_features`, then manifest-level maps (`class_features`, `classes_features`, `feature_tuples`, `features_by_class`, `class_tuples`) — **never under `declared`**. Combos therefore land in `feat_missing` → `observed_features_match_declared = false` with `declared_features.missing` = the 12 combos (score receipt `l1/scores/c2-at-e9a24d07.json`; `bindings_false: ["observed_features_match_declared"]`).
- Calibration note: the counter's own selftest red case for this binding (`c2-counter.py:2364–2366`, `combo_feat_mismatch`) mutates the *reader's own keys*, never the generator's actual emitted shape, so the suite could not catch the interface drift.
- Guard present in kaidoku (ad hoc, planner-side): `l1/mistakes/declared-keys.py` (M41-1) exits 1 on any carrier whose declared tuple sits under no key the frozen counter reads — i.e. it *detects* exactly this class. It is not wired into the counter; the C2 landing keeps the honest stop.

### 1.2 Class 2 — commit helper skipping large evidence files

- Fleet helper `scripts/hyaku/jj-lane.sh` is the only writer in every lane. Commit logic:
  - Named file > 10 MiB without `--allow-large` → hard error, exit 1 (lines 638–639).
  - **Named directory** is tracked "like `git add <dir>`"; `--include-ignored` admits files over `snapshot.max-new-file-size` only for named *files* (lines 654–656). New files in a named directory above the jj snapshot cap (~1 MiB) are **silently dropped**; afterwards only a stderr warning lists them (lines 718–722: `warn: jj refused to track (ignored or over size limit), not committed: …`). Commit proceeds.
  - Rule text: `scripts/hyaku/lane-addendum.md:272–276` ("new files over 1 MiB inside it are skipped with a warning — name them as files"); identical contract in every per-round prompt (e.g. `chousa-round-41.md:304–307`).
- Confirmed incidents:
  - **kaidoku**: commit `5ca6941b` skipped `corpus/evidence/round-41/c1/V4/after.json` (2,852,279 B) via a directory commit; repaired at `e9a24d07` — commit message itself: "skipped by the directory commit's 1 MiB rule at 5ca6941b, named as a file here". `ls-tree` at `e9a24d07` confirms all four V3/V4/L3/L4 receipt sets present.
  - **kama**: `corpus/lessons/round-26.md:89–91` ("1.4 MB log over the 1 MiB new-file limit was skipped by that directory commit and committed by name at 7e5ff9b5"); `round-35-verifier-spotcheck.md:37–41` (two `1066624`-byte fetch files, "Helper skip matches the report"); `round-36.md:27` (`helper-skipped` token).
  - **mado**: fleet `.ufo/l0-questions.md:151` (round-34 L0): round-33 K2 receipts could not be committed — "the helper skips files over 1 MiB inside a named directory" — kept out-of-lane with an ORIGIN.md; 473 MiB clones flagged as hygiene defect.

## 2. Sibling-lane scan (tools/ read-only)

Lane inventory: only kaidoku has `tools/round-*` dirs (round-25..41); all other lanes keep flat `tools/` (chousa 7 py, kama 54, kotodama 46, mado 13, mori 31, souji 19, tameshi 28, tsukuroi 64; audio/game-dev/kagi/kake/kasegi/kengaku/kotoba/kumitate/lore/revenger/tabi have no tools).

Pattern scans over all lane tools (explicit paths; see `artifacts/R41W2Sibling/commands.log`):
- `class_expected` / `declared_features` / `"declared"` / `get("features")`: **zero hits outside kaidoku** — siblings do not share the exact round-41 key family.
- `git add` inside any lane's tools: **zero matches** — no lane-local commit helper; all commits flow through `jj-lane.sh`.
- `ls-tree|cat-file|committed|tracked` hits are the *guards* below.

### Per-lane table (evidence: `artifacts/R41W2Sibling/lanes-table.json`)

| lane | class 1 | class 2 | guard(s) |
|---|---|---|---|
| kaidoku | **instance** (C2: reader keys c2-counter.py:1486–1506 vs writer key `declared`, heldout-gen-v3.py:1372/1464) + detector `l1/mistakes/declared-keys.py` | **instance** (V4 after.json skipped at 5ca6941b) | detector `l1/mistakes/evidence-tracked.py` (M41-3; red at 5ca6941b, green at e9a24d07); counters read only committed blobs (`git show REV:path`, c1-counter.py:353–355,1581) so absence fails bindings |
| kama | none (round-38 audit repair note documents past key/path-lookup bug; now covered) | **instance** (round 26 log; round 35 pair) | counters read committed blobs only: append-only-audit.py:106,145–162; hexrun-census.py:124–193; gate-registry-check.py:108–141; release-recheck.py:197–213; pin-trigger-consumed.py:35; citation-provenance.py:41–44; `instrument-agreement.py:15–26` (undeclared volatile field = disagreement) |
| chousa | none | none found | research-gate.sh drift baseline (byte-compare normalized capture vs declared volatile contract; GATE_DRIFT on any undeclared difference, lines 761–766); undeclared source ids refused |
| kotodama | none | none found | assemble-culture-d4.py:23–33,296–314 fails closed on absent/undeclared blocks and collisions; check-gate-battery.py:22–28 validates declared input digests vs snapshot bytes |
| souji | none | none found | souji-cert-evidence.py:822–891 refuses missing artifacts/declared digests; souji-evidence-cache.py:29–32 refuses undeclared required dependencies; souji-registry-agreement.py declared-vs-observed over committed bytes |
| tameshi | **instance** (round-12 producer recorded `declaration.kind` from nonexistent nested `declared.kind`; frozen truth at top level; summary recorded null) — explicit, documented | none found | witness-metadata.py (docstring 5–20): pins all three declaration inputs, requires literal frozen top-level kind, preserves the historical null as non-authority; bash-witness-study.py selftest asserts "summary preserves top-level exposed declaration kind" (1680–1682); command-binding.py digest-pins bundles |
| mado | none | **instance** (L0: K2 receipts uncommittable) | refused silent sweep; ORIGIN.md + closure-named hygiene defect |
| mori | none | none found | mori-unlanded-check.py (round-48 fix: reports filed while evidence untracked; scans `git status --porcelain` for uncommitted round work under waves/corpus/tools); mori-evidence-loss.py audits copies vs recorded sha256 and named commit |
| tsukuroi | not inspected [INFERENCE] | not inspected [INFERENCE] | — (check-* auditors; update-safety gate is module-scoped) |

## 3. Calibration / second-order notes

1. **Class 2 is a fleet infrastructure property, not a per-lane one.** Every lane's evidence landing goes through `jj-lane.sh`; any lane that commits an evidence *directory* containing new files > 1 MiB silently drops them unless each file is named (or the file is ≤ the cap). Three lanes have already hit it (kaidoku, kama, mado). “Which already guard?” — the guards are **detection-only and post-hoc**:
   - kaidoku `evidence-tracked.py` (M41-3) runs per data step (not wired into counters; the counters happen to hard-fail on missing committed blobs).
   - mori `mori-unlanded-check.py` runs at report time (round 48's fix for exactly this hole).
   - No lane modifies the helper, and the helper's hard error path (jj-lane.sh:638–639) protects only *named* files > 10 MiB.
2. **Class 1's exact key family is kaidoku-only**, but the *pattern* is not: tameshi round 12 is a documented sibling instance (producer wrote a nonexistent nested key; the frozen summary records null). The difference is that tameshi's guard (`witness-metadata.py`) is a committed gate that surfaces and pins the historical corruption without rewriting it, whereas kaidoku's C2 counter still reads the wrong key at the measured revision, hence the honest NOT MET.
3. **Strongest mechanical guards against interface drift** (would make class-1-style silent false bindings fail loudly): kama's `instrument-agreement.py` (any undeclared volatile field between runs is a disagreement), chousa's gate drift baseline, kotodama/souji fail-closed schema validation. These are general guards, not defenses against the specific key family.
4. **Negative-result honesty**: the "zero hits" greps bound the claim to the scanned token set and lane tools directories; they do not prove absence of *other* key-mismatch shapes in sibling lanes. Deeper per-lane generator/counter pairing was not performed [INFERENCE]; nothing contradicts the top-level finding that the two round-41 classes are not shared in their exact form beyond the cited instances.

## 4. Bounds / hygiene

- Wrote only `.ufo/waves/round-41/w2/R41W2Sibling.md` and `.ufo/waves/round-41/w2/artifacts/R41W2Sibling/` (commands.log, lanes-table.json).
- No VCS mutation (git only read-only: log/ls-tree/cat-file/config); no jj; no REA/unblob; no network; no vendor bytes; no tool installs (none needed — recorded per RULES.md).
- Scratch `$S=/fast/scratch/hyaku/kaidoku-r41/R41W2Sibling` created empty and removed at finish.
