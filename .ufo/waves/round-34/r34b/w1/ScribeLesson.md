# ScribeLesson — R34-C2 lesson append (draft only)

Seat: `L1Kaidoku34-2.ScribeLesson`. Leaf member, no dispatch. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, frozen revision `c79bbe7b0959132b9873ff3431cf5eb313b58b33`.
Observed window: 2026-10-25T07:18:59Z → 2026-10-25T07:22:29Z (UTC; all timestamps below are UTC).
Scratch: `/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeLesson/` (clone `lane/`, defect copies `lane-permute-loud/`, `lane-permute-silent/`, `lane-nopayload/`, receipts `receipts-mine/`).
Python: `/usr/bin/python3` = 3.14.8. No tool installs; no network; no lane VCS mutation; no ELF carrier, fixture or reader executed as a program of interest (readers invoked only as python by the counters; fixtures only read as bytes, mode 0644).

Axes I moved: (1) evidentiary fidelity — every claim below is tied to a local command or a pinned file; (2) required-section completeness — `## Claim R34-C2`, `## Mistakes`, `## Gate` present, append labelled; (3) depth — each mined mistake carries a reproduced failure and the criterion that catches it, not just a name; (4) contract/path safety — one report file, scratch-only writes.

---

## 1. What I ran (exact, with exits)

| # | command | exit | UTC | result |
|---|---|---|---|---|
| 1 | `git clone -q <lane> lane && git checkout -q c79bbe7b…` (scratch) | 0 | 07:19:07Z | `rev-parse HEAD` = `c79bbe7b0959132b9873ff3431cf5eb313b58b33`; `git status --porcelain` empty |
| 2 | `python3 -I -B tools/round-34/replay-gate.py --root . --selftest --json-out ../receipts-mine/gate-selftest.json` (cwd=clone) | 0 | 07:19:11Z | `{"cases": 12, "failed": [], "failures": 0, "mutants": 3, "mutants_killed": 3, "selftest": "replay-gate"}`; **no json-out file is written in selftest mode** (observed) |
| 3 | `… --root . --config tools/round-34/gate-config-mini.json --json-out ../receipts-mine/gate-green.json` | 0 | 07:19:13Z | `REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=-`; receipt sha256 `7cadb7e70e411d7f17c1ca82e6230f5bef7a8198569ab05acab3efb4cf29076f` |
| 4 | `… --root . --config tools/round-34/gate-config-naive.json --json-out ../receipts-mine/gate-red.json` | 2 | 07:19:14Z | `REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=6 shortcuts_over_target=label-memorization`; receipt sha256 `14ae2986a4d5a94d00f5da346ff44ddfce50ea925083069ada422db987061a9e` |
| 5 | `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root <clone> --rev c79bbe7b… --json-out mine-c2.json` | 0 | 07:21:59Z | `GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-`; receipt sha256 `da78f44419ecf83935e1fe6b1cd72f611c5a0e7e03029e97580d515a0796f3e9`, **byte-identical to `.ufo/waves/round-34/r34b/after/c2-at-instruments.json`** (`diff` on sorted JSON: no difference) |
| 6 | `… c2-shortcut-gate-counter.py --root <clone> --rev c79bbe7b… --gate tools/round-34/absent-gate.py` | 2 | 07:21:45Z | `GATE_COUNTER_UNEVALUABLE finding=gate_absent measured_revision=c79bbe7b… gate_path=tools/round-34/absent-gate.py` — reproduces the do-nothing control |
| 7 | green config on `lane-permute-loud` (one-hop map, `new_offset[name_off]`), absolute root | 3 | 07:22:10Z | `REPLAY_GATE_UNEVALUABLE finding=positive_control_below_target shortcuts_below_target=7 shortcuts_over_target=-`; receipt `b651d228…` |
| 8 | green config on `lane-permute-silent` (`new_offset.get(name_off, 0)`), absolute root | 3 | 07:22:12Z | identical line; receipt `c5df84cf…` |
| 9 | mini-counter direct on `lane-permute-loud` | 0 (payload) | 07:20:22Z | `{"finding":"records_mismatch","matched":2,"met_target":false}` — only `beta.mrec` and `epsilon.mrec` decode; all six multi-record fixtures fail |
| 10 | pinned c2 counter with payload capture removed (`payload = None`) | 1 | 07:19:59Z, re-run 07:21:5xZ | `GATE_COUNTER_MISS … clauses_failed=green_clean,green_positive_meets_target,mutants_killed,red_refused,selftest_clean`; receipt sha256 `77e0663cda63f3c79a6da991f724ee84a6acf6db1e92f010e946c2df97476182` (identical on re-run) |
| 11 | pristine green config, **relative** `--root lane`, then **absolute** `--root $PWD/lane` | 3, then 0 | 07:22:28Z / 07:22:29Z | relative: `REPLAY_GATE_UNEVALUABLE finding=counter_receipt_fields`; absolute: `REPLAY_GATE_CLEAN … shortcuts_below_target=7` |
| 12 | permute audit: pinned `permute()` × 20 seeds × 8 fixtures (160 permutations) | — | 07:19–07:20Z | 159/160 satisfy size=512, decode-equals-expected, sha differs, pool multiset preserved; the single failure is `beta.mrec` seed 18 (`sha_differs=false`). Over 2000 seeds, `beta` is byte-identical to pristine at seeds `18, 1415` (2/2000 = 1/474) |

Log of rows 7–10 with patch digests: `receipts-mine/defect-repro.log` sha256 `2f3c09a80f4655a358e3808be32616e7d1d835dc61a9d6ae81961bbec6d27b43`. Patched instrument digests: `lane-permute-loud/…/mini-counter.py` `d063f7f3…`, `lane-permute-silent/…/mini-counter.py` `4f6c8e73…`, `lane-nopayload/…/c2-shortcut-gate-counter.py` `d2cdac7c…`.

Reading anchors used below (lane files, read-only): `tools/round-34/replay-gate.py` (31, 39, 58, 67, 71-74, 76-84, 104-131, 156-171, 174-190), `tools/round-34/c2-shortcut-gate-counter.py` (28, 41-59, 73, 93-120), `tools/round-34/mini-fix/mini-counter.py` (34-49, 51-53, 57-81), configs `gate-config-mini.json` / `gate-config-naive.json`.

---

## 2. DRAFT — append for `corpus/lessons/round-34.md`

> Everything between the BEGIN/END markers is draft text for the L1 to land. It is written to be appended after the existing file; the first attempt's sections (`## Claim and order`, `## Mistakes`, `## Gate`, `## Claim verdict`, and the trailing limits) are not amended by it.

=== BEGIN DRAFT ===

---

## Round 34, attempt 2 — append (R34-C2)

*This section is appended after the first attempt's lesson; the R34-C1 sections above stay intact. R34-C1 remains frozen and stopped (`claim-stop.json`): its production reader and twelve carriers were not executed, re-scored or relabelled, and nothing here reopens it.*

## Claim R34-C2

**What was frozen, and when.** A pre-freeze, structure-blind shortcut-replay gate, declared in `.ufo/waves/round-34/r34b/claims.json` (`declared_at_utc` 2026-10-25T07:11:52Z, file mtime 07:13:04Z) and committed as `c79bbe7b0959132b9873ff3431cf5eb313b58b33` (author/committer date 2026-10-25T04:13:11-03:00 = 07:13:11Z). The instrument files predate the declaration (`replay-gate.py` mtime 07:09:52Z, `c2-shortcut-gate-counter.py` 07:11:41Z), and the production measurement follows the commit (before receipt 07:13:21Z at base `ec3125ad`, after receipt `.ufo/waves/round-34/r34b/after/c2-at-instruments.json` mtime 07:13:24Z). Order observed: instruments → claim text → freeze commit → before → after.

**Predicate (frozen wording).** P34-shortcut-replay: a finite structural-decoding counter is frozen only after registered structure-blind shortcut readers are scored under the counter's own predicate and none meets the target, while a registered structural reader does. The C2 counter carries a second, operational sentence as its `PREDICATE` and in the receipt `predicate` field; both `predicate` strings are quoted verbatim in the wave report, since `claims.json`'s `predicate_identity` asserts a single sentence across three carriers that the files do not bear out (see M34-10).

**Six clauses, all of which must hold.** `selftest_clean`, `mutants_killed` (=3), `red_refused` (`REPLAY_GATE_REFUSED`, exit 2, `label-memorization` over target), `green_clean` (`REPLAY_GATE_CLEAN`, exit 0), `green_positive_meets_target` (=8), `gate_present`. Kill rule: any false clause is a miss and stops; no target, counter, predicate or label may be changed afterwards, and no shortcut class may be dropped to reach CLEAN.

**Red surface (shape-only counter refused).** `gate-config-naive.json` drives `mini-fix/naive-counter.py`; observed `REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=6 shortcuts_over_target=label-memorization`, exit 2. The red case is a purpose-built shape-only counter, not the stopped R34-C1 production reader.

**Green surface (identity-defeating counter clears).** `gate-config-mini.json` drives `mini-fix/mini-counter.py` over eight author-built 512-byte `MREC` record-chain fixtures, with seven registered shortcut classes (`all-false`, `size-keyed`, `fixed-slice`, `digest-keyed`, `string-scan`, `record-order-replay`, `label-memorization`) and the `structural` positive control; observed `REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=-`, exit 0, `green_positive_matched=8`.

**Gate self-test.** 12 cases, 3 mutants, 0 failures: six outcome cases (clean, red-one, red-two, boundary-below, positive-below, counter-garbage), three refusal cases (two-shortcut floor, duplicate class, absent positive control) and three branch mutants (`if over:` → `if False:`, the positive-control check, the shortcut floor).

**Independent reproduction.** A fresh clone at `c79bbe7b` re-ran all three surfaces and the pinned C2 counter on 2026-10-25T07:19:11–07:21:59Z; the C2 receipt is byte-identical to the production receipt (`da78f444…`). The do-nothing control reproduces as `GATE_COUNTER_UNEVALUABLE finding=gate_absent`, exit 2.

**Pins (sha256, from `claims.json`).** `replay-gate.py` `8fa94b23…`, `c2-shortcut-gate-counter.py` `41d59703…`, `gate-config-mini.json` `4483f385…`, `gate-config-naive.json` `72b12941…`, `mini-fix/mini-counter.py` `43ef669f…`, `mini-fix/build.py` `c6718051…`; eight fixtures and eight readers pinned separately. All five control receipts are under `r34b/controls/` (do-nothing `gate_absent` exit 2; four gate mutants MISS, each naming its failed clause).

**Scope held.** The eight fixtures are author-built synthetic bytes, never domain evidence; no ELF carrier, no R34-C1 reader, no production reader is executed, and the readers are invoked only as python by the counters. Fixtures stay static bytes, mode 0644. The predicate is an instrument property (a counter may not be frozen while a registered shortcut meets it), not a claim about any binary's semantics. No depth/coverage/calibration score moves; the three owned proxies stay tied at 10.

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M34-6 | offset map keyed in the wrong domain (permute) | frozen two-hop map `mini-counter.py:62-66,72-74,81`; scratch reproductions of both one-hop forms (`new_offset[name_off]` sha `d063f7f3…`, `new_offset.get(name_off,0)` sha `4f6c8e73…`) turn the green surface into `REPLAY_GATE_UNEVALUABLE finding=positive_control_below_target`, exit 3, `matched=2/8` (only the two single-record fixtures decode) | the pre-freeze green run and the C2 clause `green_positive_meets_target == 8`; the 12-case gate selftest alone would not catch it (it substitutes a synthetic counter) | frozen instruments already carry the two-hop map; no edit. Lesson: a green set whose fixtures all have one record cannot expose this — at least one fixture with ≥2 distinct names is required |
| M34-7 | clause computed from the printed verdict line instead of the gate payload | `c2-shortcut-gate-counter.py:41-59` (payload parse) and `:93-120` (clauses read `verdict`, `classes_over_target`, `rows`, `failures`, `mutants_killed`); scratch variant with payload capture removed: `GATE_COUNTER_MISS`, exit 1, `clauses_failed=green_clean,green_positive_meets_target,mutants_killed,red_refused,selftest_clean` while both verdict lines remained `REPLAY_GATE_REFUSED`/`REPLAY_GATE_CLEAN`; receipt sha `77e0663c…` | any clause that reads only a human line is unfalsifiable; here the failure direction is a false miss | none needed; frozen. Lesson: a verdict word is not evidence; every clause must be numeric/structured from the payload |
| M34-8 | transform envelope leaks into the string pool | `mini-counter.py:60-70` parses `pool = data[names_off:]` to the end of the 512-byte buffer, so 473 NUL padding bytes become empty strings: `beta.mrec` pool = 488 bytes / 474 parsed strings / 1 non-empty; `permute()` returns bytes identical to pristine at seeds 18 and 1415 of 2000 (1/474); 20-seed audit 159/160, the miss being `beta` seed 18 | nothing frozen requires the permuted copy to differ; `transformed_sha256` is recorded but never compared with the input digest | not applied (frozen). Routed limit: seed-dependent identity on single-name fixtures; an 8/8 target needs all eight to collide, so no CLEAN result is currently explainable this way |
| M34-9 | input resolution depends on path spelling | `replay-gate.py:71-74` prefixes a possibly relative root, `:76-84` runs the counter with `cwd=root`, so the reader argument is re-prefixed; pristine clone: `--root lane` → `REPLAY_GATE_UNEVALUABLE finding=counter_receipt_fields` exit 3, `--root $PWD/lane` → `REPLAY_GATE_CLEAN` exit 0 | the selftest always uses an absolute temporary root (`:174-190`), so the relative form is untested | none (frozen). The production receipt used an absolute root and reproduces byte-identically; a seat that runs with a relative root will see a false UNEVALUABLE and must not report it as a counter defect |
| M34-10 | identity asserted in prose, not held in the files | `claims.json` `predicate_identity` says one sentence is the config field, the counter constant and the receipt label; byte comparison shows **two** sentences: claims/config carry the “finite structural-decoding counter is frozen only after…” text, the C2 `PREDICATE` and the receipt carry the “…refuses the shape-only counter whose label-keyed memorization meets its target…” text; `replay-gate.py` never reads `config["predicate"]` | a text-equality check across the three carriers at freeze time; no instrument performs one | report only; the L1 decides whether the freeze wording or the receipts stand. No instrument edited, no predicate changed |

## Gate

Opened-source candidate for this attempt: S106, proposed row, not yet in `corpus/SOURCES.md`.

- **S106 admitted, scope bounded.** binutils-gdb `binutils/readelf.c` at tag `binutils-2_47` (sourceware tag list capture `tags.html`, sha256 `3411ce75b07bcafafd14d5a98b81967e8cf31adc21922f18be9fa01ffb1e7a38`; tag page `tag22.html`, sha256 `82729c74141887ee3ce7114bf2e9730e669ca60e4c4c5771fd30e985bfa81485`; tag `version.m4` gives `BFD_VERSION 2.47`, sha256 `ac049860…`), fetched 2026-10-25T07:18Z. Capture `readelf-2_47.c`, 689,644 bytes, sha256 `7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff`; holds release notes “Changes in 2.47:”. The captured source's record walk is at `process_version_sections` (line 13859), gated by the section-header type (`case SHT_GNU_verneed`, line 14020), with the bound “if (vstart + sizeof (*entry) > endbuf) break;” (14067-14068), the Verneed field order at 14072-14076 (`vn_version, vn_cnt, vn_file, vn_aux, vn_next`), the overflow break at 14089-14090, the Vernaux field order at 14102-14106 (`vna_hash, vna_flags, vna_other, vna_name, vna_next`), and name resolution through `valid_dynamic_name`/`get_dynamic_name` (467-479) applied at 14108-14113. **Flip:** an opened revision that resolves names from anywhere but the linked dynamic string table, or whose record walk is not section-type gated.
- **S106 refusal branches located.** “Invalid vna_next field of %lx” (14121), “Missing Version Needs auxiliary information” (14134), the `vn_next` analogue “Invalid vn_next field of %lx” (14139), and “Missing Version Needs information” (14149), each reached by a bound or offset check at 14067-14068, 14089-14090, 14098-14099, 14127-14128 and 14143-14144 rather than by trusting the counts.
- **What S106 does not support.** Nothing about the eight synthetic `MREC` fixtures, the gate's target, loader acceptance, or any R34-C1 carrier. It grounds the legitimate-reader shape the structural control emulates at fixture scale: section-type gate, record walk bounded by `sh_size`, string resolution through a linked table, and refusal on truncated links. GitHub API tag discovery was rate-limited (`tags.json` holds the API error body) and the 2.44/2.45/2.46 raw requests returned `404: Not Found` (14 bytes each), so 2.47 is the only release tag behind this capture; the exact request URL is recorded in the S106 scout report, not here.

=== END DRAFT ===

---

## 3. Evidence pointers per draft claim

| draft claim | pointer |
|---|---|
| freeze chronology | `claims.json` `declared_at_utc` 2026-10-25T07:11:52Z, sha256 `de3afbfb61d70fee177392b256719bb665ad07d999303999381442120facd828`; `git show -s c79bbe7b` author/committer `2026-10-25T04:13:11-03:00`; `stat` mtimes gate 07:09:52Z, counter 07:11:41Z, claims 07:13:04Z, before 07:13:21Z, after 07:13:24Z |
| six clauses + target | `claims.json.claims[0].target`, `.kill_rule`; `c2-shortcut-gate-counter.py:112-120` |
| green / red / selftest lines | my clone receipts `receipts-mine/gate-green.json` (`7cadb7e7…`), `gate-red.json` (`14ae2986…`), selftest stdout (row 2) |
| production receipt, reproduced | `after/c2-at-instruments.json` sha256 `da78f444…`; my `mine-c2.json` same sha, sorted-JSON `diff` empty |
| before / do-nothing | `before/c2-at-base.txt` sha256 `b512cfc25d401c31a16dd4a4dd977a19c7252fd6b4a4d26f56af2de73bc19c2b`; `controls/do-nothing.txt` sha256 `dc9cde99…`; my run row 6 |
| four gate mutants | `controls/gate-*.py.txt` — always-clean MISS `red_refused,selftest_clean`; junk-clean MISS `red_refused`; no-positive-check MISS `mutants_killed,selftest_clean`; vacuous-no-floor MISS `selftest_clean` |
| M34-6 | `mini-counter.py:57-81`; patched copies + `receipts-mine/lane-permute-*.green.json`; `matched=2` payload row 9 |
| M34-7 | `c2-shortcut-gate-counter.py:41-59,93-120`; `nopayload2.json` sha `77e0663c…`; stdout row 10 |
| M34-8 | `mini-counter.py:60-70`; audit 20/2000 seeds; `expected.json` unchanged |
| M34-9 | `replay-gate.py:71-74,76-84,174-190`; rows 11 (relative vs absolute root) |
| M34-10 | verbatim §4 below; `grep -n predicate` over gate/counter shows `config["predicate"]` is never read |
| S106 | captures under `/fast/scratch/hyaku/kaidoku-r34b/w1/ScoutReadelfSource/` (sha256s in the draft); line numbers verified with `grep -n`/`sed -n` on `readelf-2_47.c` |

## 4. Conflicts reported verbatim (for the canonical judge)

`claims.json.claims[0].predicate_identity` states: “The same sentence is the gate config's `predicate` field, the C2 counter's PREDICATE constant and the receipt label”. Byte comparison returns two distinct texts:

1. carried by `claims.json` `predicate`, `gate-config-mini.json` `predicate`, `gate-config-naive.json` `predicate`:
   “P34-shortcut-replay: a finite structural-decoding counter is frozen only after registered structure-blind shortcut readers are scored under the counter's own predicate and none meets the target, while a registered structural reader does.”
2. carried by `c2-shortcut-gate-counter.py` `PREDICATE` and `after/c2-at-instruments.json` `predicate`:
   “P34-shortcut-replay: the committed replay gate refuses the shape-only counter whose label-keyed memorization meets its target, clears the identity-defeating counter on the same eight fixtures where every registered shortcut class stays below target, and its selftest kills every mutant of its own refusal, positive-control and shortcut-floor branches.”

`claims==mini: True`, `claims==naive: True`, `claims==const: False`, `const==after: True`. Not resolved here; the L1 decides.

**Second discrepancy, on the assignment's own phrasing.** The seat assignment says both author-side bugs were caught by “the gate selftest”. For M34-6 that cannot be the 12-case `replay-gate.py --selftest`: `replay-gate.py:174-190` writes its own synthetic `SELFTEST_COUNTER` and four stub readers into a temporary absolute root, so `mini-fix/mini-counter.py` and its `permute()` are never executed there (my run row 2 completed with the clone's mini-counter untouched). The reproductions in rows 7–9 show the observable catching surfaces for that defect class are (a) the green run's structural positive control falling below the 8/8 target and (b) the C2 clause `green_positive_meets_target == 8`; the draft says exactly that and does not attribute M34-6 to the gate selftest. For M34-7 the catching surface is the C2 counter's own clause set, which is a selftest of the counter, not of the gate. Whoever lands the lesson should keep the narrower wording or supply the pre-fix receipt I could not find (none exists in the freeze commit; `git show --stat c79bbe7b` adds 27 files with no earlier instrument revision).

## 5. Limits and unrun items

- **No retained pre-fix failing run.** The two author-side defects (M34-6, M34-7) were corrected before the freeze commit, so the round holds no failing receipt from before the correction. Rows 7–10 are **my** reproductions on patched scratch copies at `c79bbe7b`, not the author's original executions, and must not be cited as pre-freeze receipts.
- M34-8 and M34-9 are limits found this wave, not historical defects; neither was fixed (instruments frozen).
- I did not mutate any lane file, VCS, scorecard, LOG, lesson, corpus, SKILL or PROVINCE file; the draft above exists only here.
- Not run: the remaining four control gates through my own clone (their receipts exist and are cited, not re-executed); the ExecPermuteAudit seat's independent 20-seed audit (mine is separate); any S106 network re-fetch (no network used; stated URL form is inferred from the tag name and the 404 pattern of the neighbouring tags, pending the S106 scout report).
- The wave's attack seats were still running when this draft was written; the draft records the frozen surfaces and my reproduction and asserts **no** claim verdict and **no** score.

## 6. Verdict

`DRAFT_COMPLETE` — the append text for `corpus/lessons/round-34.md` is drafted above with `## Claim R34-C2`, `## Mistakes` (five mined mistakes: the two required author-side bugs plus three limits I reproduced or located), and `## Gate` sentences for a proposed S106; every claim carries a pointer, and the predicate-text conflict is reported verbatim rather than resolved. Unrun checks: four non-do-nothing controls not re-executed, S106 URL not re-fetched.
