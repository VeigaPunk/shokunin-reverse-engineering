# R38CriticClaimsC1 — R38-C1 shortcut falsifiers (round 38, wave 1)

Seat: critic, advisory only. No lane mutation, no VCS write, no REA/extractor run, no tool
installs. Every score below was produced with committed counter bytes in a scratch fixture repo.

**Verdict: KILL — every freeze so far (v1, v2, v3).**
- **v1** (`e059ca93`, counter sha `a7a62b09…`): `met_target` is reached with four **fabricated
  after-receipts** (oracle file list + handler string, evidence ids minted by REA's own 6.5.0
  digest rule) and stub surface rows — no REA run, no carrier read (§3).
- **v2** (`79f69347`, counter `46c46601…`) and **v3** (`f1010f67`, counter `d9aa8b62…`, the
  current instrument): after amending P38-C1 to require a paired `before`-receipt, the **same
  fabrication with a fabricated before-receipt also reaches `met_target`** (exit 0,
  `carriers 4/4`), under both frozen v2 and v3 bytes — plus every relaxation (carrier bytes
  swapped, stem superstring, duplicate heading, reused SOURCES row, stub entry, provider
  version) (§5). The before-arm adds a second authored claim, not provenance.
- The kill-rule controls stay red, but under v2 `ctl-c1-1`/`ctl-c1-2` are red **vacuously**: the
  control generator was not updated for the new required `before.json`, so they are red because
  `before_present` is false, not because of "three carriers"/"wrong handler" (§5d).
- Independent binding defects: the `frontier_note` binding is already true at the freeze and is
  satisfied by text saying the opposite (§4); `e h j l m o s` in §2.

## 1. Score identity and method

| freeze | commit | counter sha256 | bytes | selftest |
|---|---|---|---|---|
| v1 | `e059ca93` | `a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8` | 17469 | 15 cases: green_ok 1, red_ok 14, exit 0 |
| v2 | `79f69347` | `46c466014ac8535de2b1e0baa63c0e463b12f0a3f1734c3a4cdf25690510d76d` | 19482 | 18 cases: green_ok 1, red_ok 17, exit 0 |
| v3 | `f1010f67` | `d9aa8b622086d3efab4cf59f189bc8f51b2eb07f2fe73e08ab4a0774065d0347` | 19603 | 18 cases: green_ok 1, red_ok 17, exit 0 |

- Both counters were extracted from their freeze commits (`git show <commit>:tools/round-38/
  c1-counter.py`) and kept as artifacts; the working tree was never used as the instrument.
- Fixture repos: `git -C LANE archive <freeze>` of the **14 paths the counter reads** (`xpin`,
  `selftest/dev-after.json`, round-38 `carriers.json`, `K1..K4` `oracle.tsv` + carrier bytes,
  `PROVINCE.md`, `corpus/SOURCES.md`, `corpus/README.md`), `git init`, toplevel verified equal to
  the fixture dir, committed as the fixture freeze; each variant is one commit on top. [INFERENCE]
  Decision-equivalence to the full lane at a revision: `measure()` reads only those paths plus
  git objects and never opens `carriers.json`'s `path` field (no `c['path']`, no file hashing in
  any counter). The fixture archive was taken at `e059ca93`; `git diff --stat e059ca93 f1010f67
  -- <these 14 paths>` is empty, so v1/v2/v3 are scored on byte-identical fixture inputs and
  differ only in the counter/claims bytes.
- Per-variant command (receipts carry argv):
  `python3 -I -B <frozen counter> --root fx --rev <variant> --freeze <fixture freeze>
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --json-out <receipt>`.
- The only subprocess the counter runs besides `git` is `node xpin-attribute.mjs` (envelope
  identity). No `npx`/REA/unblob/sasquatch process is started by counter or by my battery.

## 2. v1 falsifier matrix (exit 0 = met target = kill)

| # | variant | construction | exit | met | deciding clause |
|---|---|---|---|---|---|
| a | `a-do-nothing` | fixture freeze only | 1 | no | all false except `frontier_note` (§4) |
| base | `base-do-nothing` | real lane, `--rev 77091b49`, `--freeze e059ca93` | 1 | no | `carriers_matched 0`, `carriers_unchanged false` |
| b | `b-receipts-only` | fabricated 4 after-receipts only | 1 | no | `carriers 4`, every surface binding false |
| **c** | `c-full-shortcut` | b + stub entry + new SOURCES row + README row + Core row | **0** | **YES** | all true, carriers 5/3/4/4 |
| d | `d-row-wrong-section` | c, Core row under `## Round-36 additions to Core`; round-38 heading empty | 1 | no | `province_core_row false` — **holds** |
| **e** | `e-row-decoy-duplicate-heading` | c, row in a duplicate `## Round-38 additions to Core` near the top; intended EOF section empty | **0** | **YES** | `section()` first match (v1:62) |
| f | `f-entry-same-basename-other-dir` | c, entry at `corpus/knowledge/archive/<STEM>.md`, rows cite it | 1 | no | `entry_present false` — **holds** |
| g | `g-source-opened-earlier` | c, SOURCES row `opened 2026-10-25` | 1 | no | `sourced false` — **holds** |
| **h** | `h-reuse-existing-today-row` | c, append entry pointer to existing `S110` (already `opened 2026-10-26`, SOURCES.md:113) | **0** | **YES** | `sourced true`, `opened_source_rows ["S110"]` |
| i | `i-entry-cites-S1120` | c, entry `source: S1120`, registry has `S112` only | 1 | no | `sourced false` — **holds** (boundary-exact `sid_tokens`) |
| **j** | `j-readme-stem-prefix` | c, coverage row names `<STEM>-draft` (different stem, STEM as prefix) | **0** | **YES** | `STEM in l` substring (v1:234) |
| k | `k-readme-other-stem` | c, coverage row names `2026-10-26-r38-other` | 1 | no | `coverage_map_row false` — **holds** |
| **l** | `l-carrier-bytes-swapped` | c, `K1/carrier.sqsh` = text, `K3/carrier.bin` = empty | **0** | **YES** | `carriers_unchanged` compares JSON only (v1:152); pins never recomputed over bytes |
| **m** | `m-entry-stub-no-claim-text` | c, entry body is one line `source: S112` | **0** | **YES** | `entry_present` only checks the path (v1:211) |
| **o** | `o-provider-version-unchecked` | c, receipts claim `{"id":"unblob","name":"NotUnblob at all","version":"0.0.1"}` | **0** | **YES** | only `provider.id` read (v1:176) |
| **s** | `same-commit-freeze` | receipts + surface edits in the commit used as both `--rev` and `--freeze` | **0** | **YES** | no freeze/claim temporal separation |

v1 controls (frozen `gen-controls.py` + frozen counter, re-generated in my scratch):
`c1-0` on the real lane at `e059ca93` → exit 1, bindings identical to the committed receipt;
`c1-1` → exit 1, carriers 3; `c1-2` → exit 1, carriers 0. **No ctl-c1-* is green.**

## 3. The loud kill (v1) — paste receipt (QUALITY 78 on the frozen instrument)

`c-full-shortcut`: exit 0, `carriers_matched 4`, `met_target true`, built as follows and with
**no extractor and no carrier read** (four receipts minted in ~1 s by `run_variants.py`):

- copy the freeze-committed `tools/round-38/selftest/dev-after.json`;
- set `subject.digest.sha256` = the `carriers.json` pin; `normalized_result.files` = the
  `oracle.tsv` rows; one chunk `handler: "squashfs_v4_be"`; `extraction_gaps: []`;
- mint `evidence_id` with `node tools/round-27/xpin-attribute.mjs --pkg65 <rea-agents 6.5.0>`;
- add a one-line entry (`source: S112`), one stub SOURCES row (`S112`, `opened 2026-10-26`,
  used-by = entry), one README coverage row, one Core row in a new round-38 section.

The fabricated receipt is internally contradictory and still green: `raw_result` still describes
the round-36 LE fixture (`/tmp/rea-firmware-6TQbeD/extracted/firmware.bin_extract/a.txt`,
`provider_id 157887:1`) while `normalized_result.files` claims BE oracle paths/hashes. The counter
never cross-checks `raw_result` against `normalized_result`, never binds the extractor identity or
version, and never checks that the receipt postdates the freeze.

Structural, not a corner case: the oracle file list is public at the base, so the observable
(published path+sha) is copyable, and the only integrity gate (`after_evidence_id_ok`, v1:185)
recomputes a digest over data the claimant authored.

## 4. Inherited `frontier_note` (v1, v2 and v3 unchanged)

`b['frontier_note'] = any('big-endian' in l and 'superseded' in l for l in PROVINCE)`
(v1:208-209; v2:226-227). Two pre-existing lines satisfy it at the freeze, both saying the
opposite of the claim:

- `PROVINCE.md:157`: `… [2026-10-26: superseded for LE SquashFS v4 — see ## Round-36 additions to
  Core; big-endian/AVM stays here.]`
- `PROVINCE.md:374`: `Frontier note, 2026-10-26: … superseded for little-endian SquashFS v4 …
  Big-endian/AVM and vendor-mangled images stay Frontier.`

`a-do-nothing`, `v2-do-nothing` and the committed `ctl-c1-0` all report `frontier_note: true`.
The clause “the round-38 frontier note supersedes the big-endian Frontier bullet” is **not
measured** in any freeze: it is green with the note absent and the old bullet intact.

## 5. Freeze v2/v3 (committed `79f69347` / `f1010f67`) — paired-receipt restatement does not close the kill

### 5a. What v2 changed

The claims note says v1's “does not reproduce” premise was falsified by R38CrossToolK1 (unblob
26.6.4's `SquashFSExtractor` needs `sasquatch-v4be` on PATH for BE v4), and restates P38-C1: after
receipt must publish the oracle with the `squashfs_v4_be` handler and no gap; **paired before
receipt** must publish none and name `sasquatch-v4be` as `missing-extractor-dependency`. The
counter adds `before_present`, `before_subject_ok`, `before_operation_ok`,
`before_missing_extractor_gap`, `before_oracle_hits == 0` (v2:176-205). It still reads only
envelope fields; from the freeze commit it reads only `XPIN`, `CARRIERS` and the oracles
(v2:88,157,171) — **`before.json` is never checked to exist at the freeze**, so “frozen with the
claim” is unmeasured. All §2 binding expressions are unchanged (row/heading `223-225`, entry
`229-232`, source row `246`, stem `252`). **v3** changes one carrier clause only:
`after_gaps_empty` becomes `after_no_missing_extractor_gap` (reject only
`kind == "missing-extractor-dependency"`; other gap kinds pass). The v3 commit did **not** amend
`plans/round-38-claims.md`: the frozen predicate text still says “freeze v2” and “carries no
extraction gap”, so the frozen words and the frozen counter now disagree (calibration defect:
the predicate sentence no longer describes the scored bytes).

### 5b. Frozen v2 and v3 counters green on fabricated paired receipts

Fabricated `before.json`: a copy of the same `dev-after.json` template with `files: []`,
`extraction_gaps: [{"kind":"missing-extractor-dependency","handler":"squashfs_v4_be",
"dependencies":["sasquatch-v4be"]}]`, `coverage: partial`, `published_bytes: 0`, subject = the
carrier pin, re-minted. Fabricated `after.json`: §3. Scored with committed v2 bytes
(`46c46601…`, selftest 18/18):

| v2 variant (identical under v3) | exit | met | carriers |
|---|---|---|---|
| `v2-do-nothing` | 1 | no | 0 |
| `v2-receipts-only` (paired fabricated receipts) | 1 | no | 4 |
| **`v2-full`** (paired receipts + surface rows) | **0** | **YES** | 4 |
| **`v2-carrier-bytes-swapped`** (K1 text, K3 empty) | **0** | **YES** | 4 |
| **`v2-readme-stem-prefix`** (`<STEM>-draft`) | **0** | **YES** | 4 |
| **`v2-row-decoy-duplicate-heading`** | **0** | **YES** | 4 |
| **`v2-reuse-existing-today-row`** (S110) | **0** | **YES** | 4 |
| **`v2-entry-stub-no-claim-text`** | **0** | **YES** | 4 |
| **`v2-provider-version-unchecked`** (name/version) | **0** | **YES** | 4 |
| `v2-after-carries-gap` (my negative control) | 1 | no | 3 |
| `v2-before-carries-no-gap` (my negative control) | 1 | no | 3 |

Re-run with the v3 bytes (`d9aa8b62…`) and the identical fabricated inputs, every verdict above
reproduces exactly (`v3-freeze-falsifiers.json`); v3's relaxation does not affect them because the
fabricated after receipts already carry `gaps: []`. So the amended predicate is satisfied by two
authored envelopes per carrier; the before receipt
is fabricated with an empty file list and a gap object — nothing was extracted, nothing was
refused by an extractor, no carrier byte was read. The v2 selftest adds “K2 before missing”,
“before carries no gap”, “before := after”, “after carries gap” and these do discriminate *shape*;
none of them can distinguish a claimant-authored shape from a runner-produced one.

### 5c. Transient state (for the record)

While the v2 draft was in the working tree, the 03:27:58 snapshot (`122fb982…`) was not scorable:
`per[k] = d` was absent so `res['carriers']` was `{}` for every input, and its selftest reported
18 cases with `green_ok 0`, `failures: ["green: want 0 got 1"]` (artifact
`v2-selftest-122fb982-broken.json`). The committed v2 restored `per[k]` (v2:195) and greens 18/18.
Peer artifacts record the sequence (`R38SentinelBounds/c1-counter.py.snapshot-{0322,0323,0324}`,
`R38ExecSelftests/lane-drift-c1-counter.diff`).

### 5d. v2/v3 controls are red but vacuous

`3b0da5dd` re-scored the c1 controls under v2 and `077e212b` re-scored c1-0 under v3. `tools/round-38/gen-controls.py` still writes only
`after.json` (`gen-controls.py:72`; no `before.json`), so under v2/v3 every fixture fails
`before_present`:
- `ctl-c1-1-three-carriers`: exit 1, `carriers_matched **0**` (v1 receipt: 3);
- `ctl-c1-2-wrong-handler`: exit 1, `carriers_matched 0`;
- `ctl-c1-0-do-nothing`: exit 1, as before.
The kill rule is therefore satisfied, but the v2 receipts no longer demonstrate “three carriers
only” or “wrong handler”; both are red because the required before-arm is absent. The controls
must be regenerated for v2 with paired fixtures to keep their named discriminating power.

## 6. Impacted axes

- **coverage** — in both freezes the target is reachable without the extraction work; in v2 the
  paired before-arm is equally forgeable. `carriers_matched == 4` does not evidence REA published
  anything from any carrier. C1 cannot be credited on counter-met alone.
- **calibration** — v2's amended selftest discriminates receipt shape but not provenance; its c1
  kill controls are vacuous (§5d); the v1 red set lacks fabricated-receipt, carrier-swap,
  duplicate-heading, stem-superstring, reused-row, provider-version and same-commit cases.
- **depth** — untouched (C1 reads no SCORECARD/SHONEN). No other axis moved.

## 7. Smallest safe correction (advisory)

1. Bind the proof to an artifact the claimant cannot author: have the counter (or the frozen
   harness, whose receipt it validates against a freeze-committed nonce) run `c1-run.sh
   before|after` itself at the measured revision. A second authored envelope (v2's before) is not
   a substitute.
2. If a counter-only check is kept, at minimum: (a) recompute each carrier file's sha256 from
   `c['path']` at `rev` against the pin; (b) require both receipts absent at the freeze commit;
   (c) require `raw_result` to carry the tool invocation and agree with `normalized_result`;
   (d) require `provider.version` 26.6.4 for both arms. (a) kills `l`; (b) kills `s` and makes
   v2's “frozen with the claim” real; (c) kills `c`/`o`; (d) kills `o`.
3. Tighten text bindings: exact stem equality (v2:252; kills `j`), one round-38 heading (kills
   `e`), old bullet text absent *and* note inside the round-38 section (kills the inherited
   `frontier_note`), a new SOURCES id rather than a used-by append (kills `h`), an entry body
   naming the handler/claim (kills `m`).
4. Regenerate the v2 controls with paired fixtures so ctl-c1-1/2 test what they claim; add red
   cases for §2/§5b.
5. No binding over claimant data can make “receipt fabricated from the oracle” red; only (1)
   closes it.

## 8. Limits

- Fixture = the 14 counter-read paths at the freeze; [INFERENCE] decision-equivalent per §1.
- I did not run REA/unblob/sasquatch: findings concern the counters' decision functions, not
  whether real BE-v4 extraction succeeds. I make **no** claim about the provenance of the
  untracked `corpus/evidence/round-38/c1/K{1..4}/{before,after}.json` now present in the lane; I
  did not use them as evidence. The point is that a fabricated set scores identically.
- `e h j l m o s` are relaxations of the otherwise-green `c`/`v2-full`; each isolates one binding;
  not a prediction that the wave report will use them.
- The wave committed v1 → v2 → v3 inside this session; `f1010f67` (counter `d9aa8b62…`) is the
  newest freeze I scored, and HEAD may move again. The finding is design-level: every scored
  clause reads claimant-authored envelope fields, so a further textual freeze that keeps that
  shape will keep reproducing it. The 03:27:58 transient is recorded in §5c.
- Scratch `/fast/scratch/hyaku/kaidoku-r38/R38CriticClaimsC1` removed; cited receipts copied to
  `.ufo/waves/round-38/w1/artifacts/R38CriticClaimsC1/`.

## Artifacts

`w1/artifacts/R38CriticClaimsC1/`:
- v1: `falsifier-matrix.json`; receipts `a-do-nothing.json` … `m-entry-stub-no-claim-text.json`,
  `o-provider-version.json`, `same-commit-freeze.json`, `base-do-nothing.json`,
  `ctl-c1-{0,1,2}-rerun.json`; score bytes `c1-counter-frozen.py` (`a7a62b09…`).
- v2: `v2-counter-46c46601-snapshot.py` (`46c46601…`), `v2-counter-122fb982-snapshot.py` (broken
  transient), `v2-selftest-46c46601.json` (18/18), `v2-selftest-122fb982-broken.json`,
  `v2-claims-diff.txt`, `v2-draft-falsifiers.json`, `v2-full.json` / `v2-full-committed.json`,
  `v2-receipts-only.json`, `v2-carrier-bytes-swapped.json`, `v2-provider-version-unchecked.json`.
- v3: `v3-counter-d9aa8b62-snapshot.py`, `v3-selftest.json`, `v3-freeze-falsifiers.json`, `v3-full.json`,
  `v3-carrier-bytes-swapped.json`, `v3-readme-stem-prefix.json`,
  `v3-row-decoy-duplicate-heading.json`, `v3-reuse-existing-today-row.json`,
  `v3-entry-stub-no-claim-text.json`, `v3-provider-version-unchecked.json`,
  `v3-after-carries-gap.json`, `v3-before-carries-no-gap.json`.
- Drift snapshots: `wt-counter-0326-snapshot.py` (`1b4dc730…`), `wt-counter-latest.py`.
- Battery sources: `run_variants.py`, `run_variants_v2.py` (show no REA/npx call).

Report: `.ufo/waves/round-38/w1/R38CriticClaimsC1.md`
