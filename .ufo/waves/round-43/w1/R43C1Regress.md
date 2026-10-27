# R43C1Regress — round-42 C2 tooling regression at the round-43 control-time baseline

**Verdict: CONFIRMED (C2 exact) / DEFECTS FOUND (C1 — the counter's own `projection_ok` clause is unreachable under the round-43 reserved-inputs rule; the divergence is bounded to that one clause and is a routing defect, not a tooling defect).**

Seat: `R43C1Regress` (leaf, wave 1). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Base `6b9e64fe7e0de202d9383baad5792fbfe039a743`. Freeze `d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b`.
L1: `KaidokuR43`. Nothing frozen yet; this output feeds the freeze. The L1 integrates and commits; this seat did not.

---

## 0. What this seat was asked to prove, and what it found

| Item | Asked | Result |
|---|---|---|
| C2 counter at `eb8215ac` | re-score to the committed stop receipt, field by field | **EXACT.** Receipt reproduced byte-for-byte on every field except `argv`. |
| C1 counter at `eb8215ac` | re-score to `.ufo/waves/round-42/l1/scores/c1-at-eb8215ac.json` | **DEFECT FOUND.** 22 of 23 per-carrier clauses reproduce exactly; `projection_ok` cannot be executed by a seat — it is an extractor run on published-carrier carve bytes, which the round-43 reserved-inputs rule forbids. See §4. |

The single divergence found is a **routing defect** in the round-43 seat contract, not a regression of the
round-42 tooling. §5 states it as a routed defect candidate for the lesson.

---

## 1. C2 — the round-42 C2 counter still scores exactly its committed stop receipt

### 1.1 The command (as dispatched)

```
S=/fast/scratch/hyaku/kaidoku-r43/w1-R43C1Regress
cd "$S"; export TMPDIR="$S" HYAKU_SCRATCH=/fast/scratch/hyaku
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    show 6b9e64fe7e0de202d9383baad5792fbfe039a743:tools/round-42/c2-counter.py > "$S/c2-counter.py"
python3 -I -B "$S/c2-counter.py" \
    --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --rev   eb8215ac87860f0e52745a4f842485bf8a6fe3b8 \
    --freeze d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b \
    --json-out "$S/regress-c2.json"
```

Exit code **1** — the honest stop, matching the committed receipt's `exit_code: 1`.

The counter bytes are the frozen ones, not a working-tree copy:
`git show 6b9e64fe:tools/round-42/c2-counter.py | sha256sum` =
`f108916713b38d860acdd60d78dd1d1a541b9feccb1bd1979742dd8dd952cb59`, identical to
`counter_sha256` **and** `counter_sha256_at_freeze` in the committed receipt, and identical at
`d1681696`, `eb8215ac` and `6b9e64fe`.

### 1.2 Field-by-field diff against `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json`

The committed receipt and the re-run receipt have **identical key sets** (66 top-level keys; no key added,
removed or renamed). Exactly **one** key differs:

| Key | Committed | Re-run | Verdict |
|---|---|---|---|
| `argv` | `["tools/round-42/c2-counter.py", …, "--json-out", ".ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json"]` | `["/fast/scratch/…/c2-counter.py", …, "--json-out", "/fast/scratch/…/regress-c2.json"]` | **Benign.** The counter records its own invocation; the scratch path and the out-path necessarily differ. Not a scoring field. |

Every other key is **bit-identical** — including all nested structures (35 `bindings`, 78 per-carrier
records, 21 `claim_bindings`, 14 `instrument_bindings`, the `table`, `decision_pairs`, `declared_features`,
`real_receipts`, `combo_unseen_majority`, `frozen_units`, `lookup`, `generator`, `writer_scope`):

- `matched` = **78**, `n` = **78** — same.
- `exit_code` = **1**, `met_target` = **false**, `met_target_consistent` = **true**, `met_target_formula` identical.
- `bindings_ok` = **false**; `bindings_false` = **`["observed_features_match_declared"]`** — the same single false binding.
- All **35** `bindings` entries identical, true for 34 and false for `observed_features_match_declared` — including
  `v4_block_identical`, `v4_block_present`, `v4_block_columns`, `generator_sha_matches_freeze`,
  `regenerated_seed_matches_freeze`, `carriers_regenerated`, `carriers_committed`, `manifest_after_freeze`,
  `manifest_before_envelopes`, `envelopes_valid`, `evaluator_covers_all`, `lookup_control_identical`,
  `combo_unseen_majority`, `real_receipts_depth_limited`, `legacy_*`, `handler_families_exercised`.
- `bindings_declared_unset` = `[]`, `bindings_undeclared` = `[]`, `actions_undeclared` = `[]`,
  `evaluator_missing` = `[]`, `evaluator_extra` = `[]`, `pair_mismatches` = `[]`, `frozen_paths_changed` = `[]`.
- **`combo_unseen_majority` identical**: `n_combos` 24, `need` 12, `unseen` = the same 19 ids
  (`C01,C02,C04,C05,C06,C08,C09,C10,C11,C14,C15,C17,C18,C19,C20,C21,C22,C23,C24`), `seen_in_dev` = the same 5
  (`C03,C07,C12,C13,C16`), `dev_named_tuples` 39, `source` the same path.
- `table` identical (the v4 rule block as the counter parsed it), `counter_sha256` =
  `counter_sha256_at_freeze` = `f1089167…cb59`, `materialised_files` = 68, `distinct_rows` 15,
  `distinct_decisions` 16, `manifest_first_add` = `d5e22b51…`, `revision`/`freeze`/`freeze_arg` identical.
- All 78 per-carrier records identical, including the 24 combo rows' `features_checked`, `features_match`,
  `declared_features`, `regen_ok`, `digest_ok`, `pair_match`, `row`.

**No divergence.** The round-42 C2 tooling still scores exactly its committed stop receipt.

### 1.3 The stop binding re-derived from committed bytes (independent of the counter)

`bindings_false = ["observed_features_match_declared"]` was re-derived by hand from the committed tree:

```
# declared (manifest, carriers[].declared_features, the ONE key contract R41-CL1)
jq '.carriers[]|select(.id=="C02").declared_features' corpus/evidence/round-42/c2/heldout/manifest.json
  -> gap_kinds = ["extractor-failure","unpublished-entry"]
     handler_set = ["squashfs_v4_be"], be_argv = "yes", gap_dependencies = [],
     symlink_removed = false, published = "nonzero"

# observed (the committed C02 REA envelope's own gap records)
grep -c '"depth-limited"'  corpus/evidence/round-42/c2/heldout/C02/envelope.json   -> 1
grep -c '"extractor-failure"' …/C02/envelope.json                                  -> 1
grep -c '"unpublished-entry"'  …/C02/envelope.json                                -> 1
```

The counter's own `declared_features.mismatch` entry agrees exactly:

```json
{"id":"C02","class":"combo","differ":["gap_kinds"],
 "declared":{"gap_kinds":["extractor-failure","unpublished-entry"], …},
 "observed":{"gap_kinds":["depth-limited","extractor-failure","unpublished-entry"], …}}
```

`"depth-limited"` is a **genuine** observed gap on C02 (the committed envelope carries a `depth-limited`
gap record next to the failing chunk at `max_depth: 1`), and the manifest's declared set omits it. Every
other class — all 27 named classes, `by_class` all `"match"` except `"combo": "mismatch"` — agrees.
The round-42 stop was honest and remains honest at the base. **This is exactly the defect R43-C1 targets
(routed R42-CL1 / mistake M42-2), and it is still live and still reproducible at the base.**

### 1.4 The C2 counter is genuinely network-free and lane-mutating-free (dev-mode requirement)

Re-run with **all** network routed to a dead proxy (`http_proxy=https_proxy=HTTP_PROXY=HTTPS_PROXY=http://127.0.0.1:9`,
`no_proxy=`):

```
exit 1;  matched 78;  n 78;  bindings_false ["observed_features_match_declared"]
differing vs the normal run: ['argv']   (nothing else)
```

So the counter needs **no network** — the fixtures it regenerates from are the committed in-lane copies under
`corpus/evidence/round-42/c2/fixtures/` (materialised via `KAIDOKU_FIXTURES`), and `urllib` is only reached
behind the generator's `--fetch` flag, which the counter does not pass. `git status --porcelain` after all
runs shows no lane mutation attributable to this seat.

### 1.5 C2 counter at the base revision and at the freeze (controls)

- **At the base `6b9e64fe`** (same counter bytes): exit **1**, `matched` 78/78, `bindings_false`
  `["observed_features_match_declared"]`, `combo_unseen_majority` identical, `v4_block_identical` true.
  The only differing keys vs the committed `eb8215ac` receipt are `argv`, `revision`, `revision_arg`, and
  `skill_block_commits_scanned` (**0 → 1**). That last one is explained and benign: commit `46486e7a`
  ("round-42: lesson, QUALITY 85, SCORECARD Round 42 + …, block-21 citation (command A), end census") is the
  one commit in `d1681696..6b9e64fe` that touches `SKILL.md`. The counter scans every such commit and
  re-checks the v4 block at each (`skill_block_drift`): `skill_block_drift_commits` is **empty** and
  `v4_block_identical` stays **true** — the citation commit added a *reference* to the block, it did not move
  a byte of the table. Independently confirmed with the counter's own `rule_block()` extractor on all three
  revisions: v4 block sha256 `92540586b8c03dcde511652c0d76ba93cbde8e5f4e79e0b94509192c19b101f2`,
  length 13851 — **byte-identical at `d1681696`, `eb8215ac` and `6b9e64fe`**.
- **At the freeze `d1681696`** (do-nothing control): exit **2**, `unevaluable: "no_manifest_at_rev"`,
  `frozen_paths_changed: []`. The frozen tooling still refuses to score a revision that has no manifest.
- **C2 counter selftest**: `{"selftest":"c2-counter r42 (v4)","cases":79,"green":18,"red":61,"pass":79,"fail":0}` — exit 0.

---

## 2. C1 — the round-42 C1 counter against its committed receipt

### 2.1 The counter and the receipt

`git show 6b9e64fe:tools/round-42/c1-counter.py | sha256sum` =
`0f5052f99a976cfdd391d3e8330b644ca403b146095ca73e14f3859ab9d1483c`, identical at `d1681696`,
`eb8215ac` and `6b9e64fe`, and identical to `counter_sha256` in the committed receipt.
`--verify-receipt` on the committed receipt: `{"ok": true, "detail": "ok"}`, exit 0.

### 2.2 What the counter does, and the block it hits

The counter's `CLAUSES` are 23 per-carrier predicates. 22 of them read only **lane bytes** (git objects,
the committed `after.json` envelopes, the committed oracle/nonregular TSVs, the committed fetch receipts) or
**reader-only probes** of the carrier bytes (sha256 + a pure superblock decode). The 23rd, `projection_ok`,
is different in kind: the counter's `rerun` clause re-runs **REA 6.5.0 `extract-firmware`** on the carrier
bytes and compares the fresh envelope's projection against the committed one.

Those carrier bytes are the four **published** third-party rootfs carves — OpenWrt Kamikaze 8.09.2 (BE),
OpenWrt Kamikaze 8.09 x86 (LE), DD-WRT v24 mega (LE) and DD-WRT v24 Fonera (BE) — and the round-43
reserved-inputs rule is explicit:

> *"Never run REA, unblob, sasquatch or any extractor on a PUBLISHED third-party firmware image
> (OpenWrt/DD-WRT/AVM downloads) **or anything carved from it** — readers only."*

The carrier cache **is** "anything carved from it". So the `projection_ok` clause is **not executable by a
seat in round 43**. (Round 42's wave-1 dispatch carried no such reserved-inputs clause — the round-42 seats
ran the extractor on the published carriers and the L1 scored them; round 43 adds the restriction. See §5.)

### 2.3 The reader-only probe: 22/23 clauses reproduce exactly

`artifacts/R43C1Regress/c1-readonly-probe.py` imports the **frozen** counter bytes and calls the counter's
own `measure()` through the counter's own `rerun` injection hook (the same hook `--selftest` uses), passing a
stub that **never starts an extractor**. Every other clause therefore evaluates over the **real published
carrier bytes**, using only readers.

The carrier cache was rebuilt with the **frozen** `tools/round-42/fetch-carrier.py`
(sha256 `54b03b6df6b72b67af3aef93f013dd3df2d53a08650039a970908bf8b8b64498` — identical to
`tool_sha256` in all four committed round-42 fetch receipts) and the **committed** `.ufo/waves/round-42/c1/fetch-spec.json`:

```
python3 -I -B fetch-carrier.py --spec fetch-spec.json --cache cache --image-cache imgcache --work work
exit 0;  all four carriers ok
  OW-A8092  pin 35f777eb…  DW-MEGA   pin 5d37063e…
  OW-X86FS  pin 12a2fd58…  DW-FONERA pin 02199832…
each cache entry's sha256 == its committed pin (re-hashed independently)
```

Readers-only confirmation that the published carriers are the expected images, with no extractor involved:
`7z l` on the two OpenWrt carves lists **586 files / 95 folders** (OW-A8092) and **570 files / 94 folders**
(OW-X86FS) — consistent with the committed oracle row counts (409 and 403 **regular** files; `7z` counts
directories and non-regulars too). The two DD-WRT carves are the vendor `hsqt`/`tqsh` variants and 7-Zip
26.04 does not read them, which is why the committed oracle for those two was built by a different reader.

The probe result (`artifacts/R43C1Regress/c1-readonly-probe-at-eb8215ac.json`) against the committed
`c1-at-eb8215ac.json`:

- **Per-carrier: 22 of 23 `CLAUSES` identical, and the differing one is `projection_ok` for all four
  carriers** — verified programmatically (`ALL carriers differ ONLY in projection_ok: True`).
- All 12 boolean `bindings` identical and **true**: `carrier_sources_ok`, `carriers_spec_ok`,
  `coverage_map_row`, `endianness_coverage`, `entry_present`, `extractor_bin_ok`, `frontier_note`,
  `frozen_tables_valid`, `gap_rule_ok`, `province_core_row`, `province_core_section`, `sourced`.
- Every other per-carrier field identical, including the **full `layout` superblock decode** (`ok`,
  `magic`, `endianness`, `major`/`minor`, `block_size`, `bytes_used`, all four table offsets,
  `compression_signatures`, `meta_signal`), `carve_ok`, `compression` = `lzma` on all four,
  `endianness` = be/le/le/be, `oracle_hits_ok` (409/403/447/569 = 100 % oracle hits, zero extra published),
  `gaps_ok` (the `unpublished-entry` per symlink and the one `depth-limited`),
  `nonregular_unpublished_ok` (272/261/265/250 non-regular entries for OW-A8092/OW-X86FS/DW-MEGA/DW-FONERA,
  zero published non-regulars), `path_shape_ok`,
  `run_provenance_ok`, `subject_pin_ok`, `evidence_envelope_ok`, `extract_env_ok`, `handler_ok`,
  `chunks_ok`, `operation_ok`, `evidence_id_ok`, `receipt_fresh`, `fetch_receipt_ok`.
- The only remaining per-carrier differences are `projection_ok` (true → false, by construction),
  `projection_diff` (`[]` → null), `projection_error` (null → the stub's refusal record), `matched`
  (true → false, because `matched` requires all 23 clauses), and `carrier_cache` (the scratch cache path,
  a provenance field).

**Top-level divergence: `carriers_matched` 4 → 0, `met_target` true → false, `exit_code` 0 → 1** — and
that divergence is *entirely* the arithmetic of one clause (`matched` requires all 23), not a second defect.
`carrier_ids`, `prior_pins`, `prior_pin_sources`, `evidence_digests`, `projection_profile`,
`frozen_path_changed`, `frozen_tables_valid`, `gap_rule_problems`, `carriers_spec_problems`,
`carriers_unchanged`, `gap_rule_unchanged` are all identical.

### 2.4 The tooling's own self-checks

- **C1 selftest** (offline, simulated REA): `{"selftest":"c1-counter","cases":121,"green_ok":14,"red_ok":107,…}` — exit 0, 121/121.
- **C1 `--selftest-rea`** on an **MIT unblob 26.6.4 fixture** (`corpus/evidence/round-42/c2/fixtures/v3-le--squashfs_v3_le.bin`
  — an explicitly permitted development input): exit **0**, `"selftest_rea": "ok"`, `handler: squashfs_v3`,
  `endianness: le`, `compression: gzip`, real REA 6.5.0 runs, and the fabrication arm correctly reds.
  This proves the counter's **live** REA path (REA 6.5.0 + unblob 26.6.4 + sasquatch 4.5.1 + the xpin
  evidence-id recomputation) is functional on this host — the machinery the `projection_ok` clause uses is
  alive; only the *input class* (published carrier bytes) is off-limits.
- **Toolchain digests match the committed receipt exactly**:
  `unblob` `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09` (26.6.4),
  `sasquatch` `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754` (4.5.1),
  `sasquatch-v4be` `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`.
- **rea-agents 6.5.0**: materialised at exactly the frozen `rea-pkg.json` package root
  `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`; `package.json` sha256
  `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c` and `package-lock.json` sha256
  `d42d56f0f4f8baf3ecc24f2bd24f9f09e3c99b83592ef85201f74df255e0c6ca` — **both equal the frozen pins**, so
  the counter's `rea_package_problems` gate passes.
- **C1 counter at `eb8215ac` without a carrier cache**: exit 1, and its receipt is **byte-identical to the
  same run at the base `6b9e64fe`** except `argv` and `revision` — the counter's non-carrier half is
  revision-stable.

---

## 3. Frozen-byte state at the base (material to the freeze the L1 is about to take)

| Frozen artefact | `d1681696` | `eb8215ac` | `6b9e64fe` (base) | Verdict |
|---|---|---|---|---|
| `tools/round-42/c2-counter.py` | `f1089167…cb59` | `f1089167…cb59` | `f1089167…cb59` | identical |
| `tools/round-42/c1-counter.py` | `0f5052f9…1483c` | `0f5052f9…1483c` | `0f5052f9…1483c` | identical |
| `tools/round-42/sqfs-triage-v4.py` | `497bab67…` | `497bab67…` | `497bab67…` | identical |
| `tools/round-42/indep-eval-v4.py` | `7a135dd3…` | `7a135dd3…` | `7a135dd3…` | identical |
| `tools/round-42/heldout-gen-v4.py` | `c2b1641a…` | `c2b1641a…` | `c2b1641a…` | identical |
| `tools/round-42/fixtures.json` | `9f957663…` | `9f957663…` | `9f957663…` | identical |
| SKILL.md v4 rule block (`rule_block()`) | `92540586…b101f2` (13851 B) | `92540586…b101f2` | `92540586…b101f2` | **byte-identical** |
| `corpus/evidence/round-42/c2/fixtures/` tree | `6aaadcea…` | `6aaadcea…` | `6aaadcea…` | identical |
| `corpus/evidence/round-42/c2/heldout/` tree | (absent) | `53665235…` | `53665235…` | identical at the two revisions that have it |

`git log d1681696..6b9e64fe -- tools/round-42 …` shows **no modification** of any frozen path in the C2
counter's sense (`frozen_paths_changed: []`); the only `SKILL.md`-touching commit is `46486e7a`, and the
counter re-verified the v4 block at it (no drift). The round-42 C2 stop receipt stays byte-committed at
`.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json`.

**Durability re-check after the L1's concurrent wave-1 commits.** The lane HEAD advanced from the base
`6b9e64fe` to `1ede187d` ("round-43: wave-1 attack findings folded into draft …") while this seat was
working. Re-verified at that HEAD: `tools/round-42/{c2-counter,c1-counter,sqfs-triage-v4,indep-eval-v4}.py`
are **still byte-identical** to the base and the freeze (`f1089167…`, `0f5052f9…`, `497bab67…`, `7a135dd3…`),
and the SKILL.md v4 rule block is **still** `92540586b8c03dcde511652c…` at `d1681696`, `6b9e64fe` and the new
HEAD. The baseline this seat measured is therefore not invalidated by the draft edits, and the round-43
freeze can still take the round-42 tooling bytes as frozen.

---

## 4. The divergence, stated exactly

**One divergence, one cause.** The C1 counter's `projection_ok` clause is defined as *a fresh REA 6.5.0
`extract-firmware` run on the carrier bytes*. The carrier bytes for the round-42 C1 claim are **carves of
published third-party firmware images**. The round-43 reserved-inputs rule forbids a seat from running any
extractor on a published image **or anything carved from it**. The clause and the rule are in direct
conflict, so the clause cannot be executed from a seat.

Measured consequence: `projection_ok` false on 4/4 carriers → `matched` false on 4/4 → `carriers_matched`
4 → 0 → `met_target` true → false → `exit_code` 0 → 1. The other 22 clauses and all 12 top-level bindings
reproduce exactly.

**This is a limitation of the seat contract, not evidence of tooling drift.** Supporting measurements:
the counter's *live* REA arm works (2.3, `--selftest-rea` green on an MIT fixture); the toolchain digests
equal the committed receipt's; the counter bytes are identical at three revisions; and the committed receipt
itself verifies (`--verify-receipt` ok).

**Routed defect candidate (for the L1 / the lesson).** Suggested identifier: **R43-CL1a** (companion to the
claim-side R43-C1 and to the already-routed R42-CL1). Statement: *the round-43 seat dispatch binds every
seat with a "never run an extractor on a published third-party image or anything carved from it" rule, while
the round-42 C1 counter's `projection_ok` clause is by construction such an extractor run on published
carrier carves; no seat can therefore reproduce `.ufo/waves/round-42/l1/scores/c1-at-eb8215ac.json`, and the
C1 half of the "control-time baseline" cannot be closed from a seat.* Proposed resolutions, in order of
preference: (a) the L1 runs the C1 re-score itself (the L1 alone runs the post-freeze data procedure, and
round 42's L1 already scored this arm — precedent in `tools/round-42/c1-run.sh`); (b) the rule gains an
explicit carve-out for *reproducing an already-committed score* as opposed to *producing new evidence*; or
(c) the C1 arm is re-grounded on development inputs (the MIT unblob 26.6.4 fixtures), which changes the
claim and must be recorded as such. **[INFERENCE]** — the routing itself is the L1's call; the measurement
above is what this seat can attest.

Note the same constraint does **not** affect R43-C1 itself: the round-43 C1 claim scores the frozen v4
triage table on a fresh held-out set built from the **MIT unblob 26.6.4 fixtures** (explicitly permitted),
and the round-42 C2 tooling that carries that score reproduces exactly with no network and no published
image.

---

## 5. The C02 root cause, and why R43-C1's refusal rule is the right fix

Re-derived from committed bytes (§1.3): the round-42 generator declared a six-field tuple for combo C02 that
its own REA run did not observe — `depth-limited` was observed but not declared. The label/action decision
was nevertheless identical on both sides (`partial-body-failure`), which is why the table scored 78/78 while
the manifest still failed `observed_features_match_declared`. The round stopped on that binding and the
stop was honest.

The round-43 fix (`heldout-gen-v4r43.py` refuses to write a manifest whose declared tuple differs from the
tuple its own run observed) targets exactly this. Two calibration notes for the L1, both grounded in what I
measured:

1. **`depth-limited` on a combo is a real, structural REA-6.5.0 behaviour at the depth ceiling**, not a
   generator slip: the committed C02 envelope carries the `depth-limited` gap record itself, at
   `max_depth: 1`, next to the failing chunk. A refusal rule keyed on the *observed* tuple will therefore
   see `depth-limited` on every combo that sits at the ceiling, and the new manifest must declare it.
2. **The frozen generator is deterministic and its committed output is reproducible at the base**:
   `carriers_regenerated` true, `regenerated_seed_matches_freeze` true, all 78 carriers regenerate
   byte-identically from the seed in ~2 s with no network. The round-43 port therefore has a working
   reference point for its own `regenerated_*` bindings.

---

## 6. Tooling installed/updated

Per the operator directive (2026-10-19) and the round-43 pacman guard (**all** pacman transactions are
paused host-wide):

| Tool | Version | Channel | Reason |
|---|---|---|---|
| `rea-agents` (npm) | 6.5.0 | `npx -y rea-agents@6.5.0` (official npm registry) | The frozen `tools/round-42/rea-pkg.json` pins the package root `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` and its two file digests; the C1 counter's `rea_package_problems` gate refuses a package whose bytes differ. Materialised to exactly that root; **both frozen digests match**. No PATH directory and no `~/.local/bin` entry was created or modified. |

No other tool was installed, upgraded, moved or removed. `unblob` 26.6.4, `sasquatch` 4.5.1 and
`sasquatch-v4be` were used **as found**; their digests equal the committed receipt's `extractor_bin_detail`
(§2.4). `pacman` was not invoked at all.

---

## 7. Commands and limits

**Executed (all read-only against the lane; scratch only):**

```
git show 6b9e64fe:tools/round-42/c2-counter.py > $S/c2-counter.py
python3 -I -B $S/c2-counter.py --root <lane> --rev eb8215ac --freeze d1681696 --json-out $S/regress-c2.json      # exit 1
python3 -I -B $S/c2-counter.py --root <lane> --rev 6b9e64fe --freeze d1681696 --json-out $S/regress-c2-at-base.json # exit 1
python3 -I -B $S/c2-counter.py --root <lane> --rev d1681696 --freeze d1681696 --json-out $S/c2-at-freeze.json     # exit 2
python3 -I -B $S/c2-counter.py --selftest                                                            # exit 0, 79/79
python3 -I -B $S/tree/tools/round-42/c1-counter.py --selftest --pkg65 <rea-agents root>                    # exit 0, 121/121
python3 -I -B $S/tree/tools/round-42/c1-counter.py --selftest-rea --pkg65 <root> \
    --dev-carrier <lane>/corpus/evidence/round-42/c2/fixtures/v3-le--squashfs_v3_le.bin \
    --unblob /home/vgpnk/.local/bin/unblob                                                            # exit 0, selftest_rea ok
python3 -I -B $S/fetch-carrier.py --spec $S/fetch-spec.json --cache $S/cache --image-cache $S/imgcache --work $S/work  # exit 0, 4/4
python3 -I -B <lane>/.ufo/waves/round-43/w1/artifacts/R43C1Regress/c1-readonly-probe.py \
    --counter $S/tree/tools/round-42/c1-counter.py --root <lane> --rev eb8215ac --freeze d1681696 \
    --pkg65 <rea-agents root> --carrier-cache $S/cache --out $S/c1-readonly-eb.json                        # exit 1 (22/23 clauses exact)
python3 -I -B $S/c2-counter.py ... with http_proxy/https_proxy/HTTP_PROXY/HTTPS_PROXY=http://127.0.0.1:9, no_proxy=  # exit 1, only argv differs
7z l <each fetched carrier>                                                                            # readers only
```

**Limits and boundaries observed.**

- **No extractor was run on any published third-party firmware image or on anything carved from one.**
  The `projection_ok` arm was executed with a stub that starts no extractor; the published carriers were
  touched only by the frozen fetch tool (HTTP GET + sha256 + a byte-range carve) and by readers (`7z l`,
  the counter's own pure superblock probe). The real REA arm was exercised on an **MIT unblob 26.6.4
  fixture** only.
- **No third-party firmware image or file extracted from one was copied into the lane.** The four fetched
  carves live only in scratch and are removed with it; they are cited here by URL + sha256 + rebuild command
  (`tools/round-42/fetch-carrier.py --spec .ufo/waves/round-42/c1/fetch-spec.json --cache <dir>`), never by
  lane path. Artifacts in this seat's directory are receipts and reports only, all under 150 KB.
- **No VCS mutation.** Only read-only git (`show`, `log`, `ls-tree`, `rev-parse`, `cat-file`, `diff`,
  `status`) was used, each call naming `-C` explicitly. The lane's `plans/round-43-claims.md` is modified in
  the working tree and `HEAD` has advanced to `1ed29de2` — **the L1's own concurrent work, not this seat's**;
  this seat wrote only inside `.ufo/waves/round-43/w1/artifacts/R43C1Regress/` and this report.
- **Scratch**: `S=/fast/scratch/hyaku/kaidoku-r43/w1-R43C1Regress`, `TMPDIR=$S`, `HYAKU_SCRATCH=/fast/scratch/hyaku`;
  removed on completion. No `find`/`du` sweep under `/fast/scratch`; no `/tmp` path is cited as evidence.
- **Tool identity**: every receipt cited above was produced by the **frozen** counter bytes, verified by
  sha256 against the committed receipt's `counter_sha256` and by the counters' own `--verify-receipt`.
- **[INFERENCE]** where marked is a judgement about routing, not a measurement. Everything else is a recorded
  command output or exit code.

---

## 8. Artifacts

Under `.ufo/waves/round-43/w1/artifacts/R43C1Regress/`:

| File | What it is |
|---|---|
| `c2-regression-at-eb8215ac.json` | C2 counter re-run at `eb8215ac` — the reproduction of the committed stop receipt |
| `c2-regression-at-base-6b9e64fe.json` | C2 counter re-run at the base |
| `c2-regression-network-isolated.json` | the same run with all network routed to a dead proxy (proves dev-mode network-freedom) |
| `c2-counter-at-freeze-control.json` | do-nothing control: exit 2 `no_manifest_at_rev` |
| `c2-selftest.out` | C2 counter selftest, 79/79 |
| `c1-readonly-probe.py` | the reader-only probe (imports the frozen counter; its own `rerun` hook; starts no extractor) |
| `c1-readonly-probe-at-eb8215ac.json` | probe result — 22/23 clauses identical per carrier, all 12 bindings true |
| `c1-counter-nocache-at-eb8215ac.json` | C1 counter at `eb8215ac` with no carrier cache (non-carrier half) |
| `c1-counter-nocache-at-base-6b9e64fe.json` | the same at the base — byte-identical to the above but for `argv`/`revision` |
| `c1-selftest.out` | C1 counter selftest, 121/121 |
| `c1-selftest-rea-fixture.out` | real-REA selftest on the MIT unblob 26.6.4 v3 fixture — `selftest_rea: ok` |
| `c1-carrier-fetch-receipt.json` | frozen fetch tool's receipt for the four published carriers (pins, bytes, digests) |
| `fetch-carrier-frozen.py` | the frozen fetch tool's bytes (sha256 `54b03b6d…`), for the rebuild command |

**Rebuild commands** (scratch paths are not evidence; every artefact above is reproducible from the lane):

```
C2 re-run:
  git show 6b9e64fe:tools/round-42/c2-counter.py > c2-counter.py
  python3 -I -B c2-counter.py --root <LANE> --rev eb8215ac --freeze d1681696 --json-out regress-c2.json
C1 reader-only probe:
  git show 6b9e64fe:tools/round-42/c1-counter.py > tree/tools/round-42/c1-counter.py
  git show 6b9e64fe:tools/round-27/xpin-attribute.mjs > tree/tools/round-27/xpin-attribute.mjs
  git show 6b9e64fe:tools/round-42/fetch-carrier.py > fetch-carrier.py
  git show eb8215ac:.ufo/waves/round-42/c1/fetch-spec.json > fetch-spec.json
  python3 -I -B fetch-carrier.py --spec fetch-spec.json --cache cache --image-cache imgcache --work work
  python3 -I -B <LANE>/.ufo/waves/round-43/w1/artifacts/R43C1Regress/c1-readonly-probe.py \
      --counter tree/tools/round-42/c1-counter.py --root <LANE> --rev eb8215ac --freeze d1681696 \
      --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
      --carrier-cache cache --out c1-readonly-eb.json
```

---

## 9. Summary for the L1

1. **The round-42 C2 tooling still scores exactly its committed stop receipt at `eb8215ac`** — one key
   (`argv`) differs, every scoring field is bit-identical, `matched` 78/78, exit 1, the single false binding
   `observed_features_match_declared`. Also confirmed at the base and network-isolated, and at the freeze it
   still exits 2 `no_manifest_at_rev`. **The control-time baseline for R43-C1 holds.**
2. **The stop binding is still live and still reproducible from committed bytes**: combo C02's committed
   envelope carries a `depth-limited` gap the manifest does not declare. R43-C1's refusal rule addresses the
   right defect.
3. **The frozen v4 table, the frozen interpreter, the frozen evaluator, the frozen generator, the frozen
   fixtures and both frozen counters are byte-identical at `d1681696`, `eb8215ac` and the base.** The one
   `SKILL.md`-touching commit in range (`46486e7a`) added a *citation* to block 21 and moved no byte of the
   table; the counter re-verified this itself (`skill_block_drift_commits` empty).
4. **One routed defect found (R43-CL1a candidate)**: the round-43 reserved-inputs rule forbids a seat from
   running any extractor on a published third-party image *or anything carved from it*, which makes the
   round-42 C1 counter's `projection_ok` clause — and therefore the C1 half of the control-time baseline —
   unreachable from a seat. The measurement is in §2.3 (22/23 clauses per carrier exact, all 12 bindings
   true) and the measurement that it is *not* tooling drift is in §2.4 (live REA arm green on an MIT fixture;
   toolchain and package digests equal the committed receipt's; counter bytes identical at three revisions;
   committed receipt verifies). The routing decision is yours.
5. **No lane mutation, no published image touched by an extractor, no third-party bytes copied into the
   lane, no VCS mutation, one tool installed (rea-agents 6.5.0 via npx, digests matching the frozen pins).**

Report: `.ufo/waves/round-43/w1/R43C1Regress.md`
