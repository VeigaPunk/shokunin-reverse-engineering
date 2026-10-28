# R45W2Scorecard — attack on the `SCORECARD.md` `## Round 45` record

Seat: `R45W2Scorecard` (leaf, no dispatch). Lane `kaidoku`, round 45, wave 2.
Target of this seat: **the record**, not the landing — every number in the round-45 claim table,
every commit hash the section cites, and the section's own record-level sentences.

Read-only on the lane tree: nothing under `SKILL.md`, `plans/`, `tools/`, `corpus/`, `LOG.md`,
`SCORECARD.md` was written, staged, committed or stashed. All fixtures and receipts lived in
`/fast/scratch/hyaku/kaidoku-r45/R45W2Scorecard` (removed before yielding); the receipts are copied
into this directory. `git status --porcelain` over tracked files is empty after the seat's run.

Revision attacked: the section as committed at the lane tip **`a63d109f`** (identical to
`main`'s `SCORECARD.md`; `git diff --stat a63d109f main -- SCORECARD.md` empty), whose numbers are
the ones `abfeda50`, `14340d41`, `1d04c6af` and `a63d109f` left in place.

---

## 1. Verdict per number in the claim table

Every command below was run from outside the lane (cwd `/`), `python3 -I -B`, `TMPDIR` inside the
scratch dir. `--root` = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

| # | number as recorded | re-derived value | instrument | verdict |
|---|---|---|---|---|
| 1 | `rule_blocks 22` (C1 after, `1f4b27f8`) | **22** | `c1-counter.py` exit 0 (`c1-A1.json`, stdout sha256 `d30817c5…`) + independent `^- \*\*` split of `## Queue-drain craft` from `git show <rev>:SKILL.md` = 22 at `e715263c`, `1f4b27f8` and `f59565b7` + command A `rule_blocks 22` at `1f4b27f8`/`f59565b7` | **holds** |
| 2 | `block22_rows 10` | **10** | counter `block22_rows 10` at `1f4b27f8`; independent extraction of the marker block = 12 table lines = header + separator + **10 data rows**; exit cells `1,1,1,1,2,1,2,2,0,0` all in `{0,1,2}`; header is `trigger \| arm \| exit \| receipt` | **holds** |
| 3 | `block22_refs 7` (measured at `1f4b27f8`) | **7** at `1f4b27f8` | counter `block22_refs 7`; independent `findall` of `corpus/(knowledge\|lessons)/…` + `plans/…` refs in the block = 7; lane receipt `l1/scores/c1-at-1f4b27f8.json` also 7. All 8 refs at A3 resolve inside their files | **holds at its stated revision** (but stale vs A3 — see F5) |
| 4 | `preflight_selftest cases 11 failures 0` | **11 / 0, exit 0** | counter field at `1f4b27f8`, A2, A3, tip; **independent** run of the interpreter bytes taken from `f59565b7` (`sha256 633ebc05…`, byte-identical to the `f762b727` blob) → 11 case lines, `PREFLIGHT_SELFTEST: cases=11 failures=0`, exit 0 | **holds** |
| 5 | `unregistered 6 → 0` | **6 at the freeze → 0 at `1f4b27f8`/A2/A3** | `c1/c2`-counter: freeze exit 1 `unregistered` = the six scope paths, `registered []`; A1/A2/A3 exit 0 `unregistered []`. Independent parser over `git show f59565b7:SKILL.md`: each of the six `registry-scope.json` paths has exactly one row whose **first cell** is path-equal | **holds** |
| 6 | `thin []` | **`[]`** at freeze, `1f4b27f8`, A2, A3 | counter; independent: every one of the six matched rows' exit cell names `0`, `1` and `2` (e.g. `` `0` met; `1` not met; `2` could-not-evaluate ``) | **holds** |
| 7 | `scope_size 6` | **6** | counter `scope_size 6`; `tools/round-45/registry-scope.json` `paths` length = 6 (file is frozen: `git diff --stat f762b727..a63d109f -- tools/round-45/` empty) | **holds** |
| 8 | command A `138/138` | **138 / 138** | recipe A at `1f4b27f8`: `knowledge_files 138`, `mapped 138`, `missing []`, `dangling []`, `coverage_score 10.0`; independent: `git ls-tree` `.md` count = 138 and distinct `2026-10-NN-*` stems in `## Coverage map` = 138. `10 → 10` is real: at the freeze also 138/138, `coverage_score 10.0` (`cmdA-freeze`) | **holds** |
| 9 | command A `22/22` (`rule_blocks` / `citation_resolved_rules`) | **22 / 22** at `1f4b27f8` and A3 | recipe A: `rule_blocks 22`, `citation_resolved_rules 22`, `depth_score 10.0`; at the **landing** `e715263c`: `rule_blocks 22`, `citation_resolved_rules 21`, `depth_score 9.55` — which is exactly the A1 narrative ("would have scored 21/22, the round measured that and repaired it before claiming") | **holds** (and the A1 narrative is confirmed) |

Also re-derived and holding: freeze `f762b727` really is
`git log --format=%H -1 -- plans/round-45-claims.md`; `f762b727^ == 149133d4` (base); the frozen
bytes are untouched through A3 and the tip (`git diff --stat f762b727..f59565b7 -- plans/round-45-claims.md tools/round-45/` and `…f762b727..a63d109f…` both empty; frozen preflight exit 0 `clean`
at `faa875bc`, A2, A3 and `a63d109f` over both frozen pathspecs); wave 1's `40 seats`
(`r45-w1-results.json` `seats 40`, 40 results, present at `main`); both counters' selftests carry **no**
`red-restored` case (c1: 9 cases, c2: 7 cases — so "only the preflight carries an explicit
`red-restored` test case" holds).

---

## 2. Findings (severity order)

### F1 — HIGH — "the values are identical" across four revisions is false (the record contradicts its own receipts)

- **Attacked sentence:** `SCORECARD.md:3590-3591`
  ("**The measured revision for the round is A3**; the values are identical at `e715263c`,
  `1f4b27f8`, `fedd11bf` and A3") and the same class at `SCORECARD.md:3581`
  ("`1f4b27f8` is the first met measurement, and every value is identical at both" [A2]).
- **Exact input:** the round's own counting command
  `python3 -I -B tools/round-45/c1-counter.py --root <LANE> --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec --rev <REV>`
  at `REV ∈ {e715263c, 1f4b27f8, fedd11bf, f59565b7}`.
- **Observed `block22_refs`:** **6** at `e715263c` → **7** at `1f4b27f8` → **8** at `fedd11bf` → **8**
  at `f59565b7` (exit 0, `met_target true` at all four; every other predicate constant:
  `rule_blocks 22`, `block22_rows 10`, `preflight_selftest 11/0`, `unresolved []`).
  The difference is real and intended — A1 adds the `corpus/knowledge/…r34b…` citation (refs 7),
  A2 adds the bare `plans/round-45-claims.md` reference (refs 8).
- **The lane's own receipts already say so:** `l1/scores/c1-at-e715263c.json` → `"block22_refs": 6`;
  `c1-at-1f4b27f8.json` → `7`; `c1-at-A2.json` → `8`; `c1-at-A3.json` → `8`. The sentence contradicts
  four artifacts committed in the same round. Independently, command A's depth proxy also differs at
  the landing (`citation_resolved_rules 21`, `depth_score 9.55`) vs the later revisions (`22`, `10.0`).
- **Fix:** append-only correction replacing the identity clause with the measured series
  (`block22_refs 6 → 7 → 8 → 8`; every other predicate identical), and the same for the A2 sentence
  (`block22_refs` 7 vs 8). Do not delete the A2/A3 text — correct it in place with an erratum.

### F2 — HIGH — "wave 2: 32 seats" is not from the file it cites, and the file does not exist

- **Attacked sentence:** `SCORECARD.md:3527-3528`
  ("Wave 1: 40 seats; wave 2: 32 seats (counts from `.ufo/waves/round-45/{r45-w1,r45-w2}-results.json`)").
- **Exact input:** `git log --all --diff-filter=A -- .ufo/waves/round-45/r45-w2-results.json` → **no
  commit ever added it**; `git cat-file -e main:.ufo/waves/round-45/r45-w2-results.json` → absent;
  also absent at `a63d109f` and on disk.
- **Observed instead:** `.ufo/waves/round-45/w2-dispatch.json` `counts = {"spawn": 36, "resume": 0,
  "total": 36}`; `w2-spec.json` at `faa875bc`, `a63d109f` and `0ee50aaf` carries **36** named items;
  the only `32` in the dispatch is `policy.waveMinLanes = 32` (the band minimum of
  `scripts/hyaku/ufo-wave-policy.json`, band 32–64).
- **Consequence:** the recorded seat count is 4 below the dispatched wave and is sourced to a
  non-existent artifact; a wave-2 results ledger has to be written at settlement for the citation to
  become true. The `40` for wave 1 is correct (`r45-w1-results.json` `seats 40`, 40 results).
- **Fix:** `wave 2: 36 seats dispatched (w2-dispatch.json counts.spawn=36)` now, and cite
  `r45-w2-results.json` only once settlement writes it (then state the settled count, not `waveMinLanes`).

### F3 — MEDIUM — the C2 "base" before-state names a reason the counter cannot produce under the round's freeze

- **Attacked cell:** `SCORECARD.md:3533`, before-column: "at the base exit 2 `scope file absent at rev`
  (`.ufo/waves/round-45/controls/ctl-c2-0-base-unevaluable.json`)".
- **Exact input:** `c2-counter.py --root <LANE> --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec --rev 149133d47aa7e90796f96047afe6d251a3e65b2c`.
- **Observed:** exit **2** with `{"reason": "freeze is not an ancestor of rev"}` — the ancestry guard
  is `c2-counter.py:77`, the scope-file check is `:84-86`, so the later branch is unreachable for this
  pair. The cited receipt *does* say `scope file absent at rev`; I reproduced it byte-for-byte only
  with **`--freeze 149133d4 --rev 149133d4`** (self-freeze; `c2-base-selffreeze`, exit 2), an input the
  record never states. Same provenance issue for `ctl-c1-0-base.json`, whose `freeze` field is
  `149133d4`; with the round's freeze, `c1-counter.py` at the base also exits 2
  (`freeze is not an ancestor of rev`, `c1-base.json`), not "the same values" as the freeze control.
- **What survives:** the exit code `2` (could-not-evaluate) and the claim's semantics ("the base is not
  a measurable before") — the base is genuinely unevaluable under the round's freeze. Only the **named
  reason** is falsified, plus the receipt's unstated input.
- **Fix:** record the receipt's actual inputs (`--freeze <base> --rev <base>`) and the round-freeze
  observable (`exit 2, freeze is not an ancestor of rev`); the claims file is frozen, so route this as
  an append-only erratum in `SCORECARD.md`/`LOG.md` rather than editing `plans/round-45-claims.md`.

### F4 — MEDIUM — the A2 gate is cited to a receipt whose range stops one commit before A2 (and no receipt gates A3)

- **Attacked sentence:** `SCORECARD.md:3579-3580` — "The gate over both frozen pathspecs from the
  freeze to A2 is `clean`, exit 0 (`…/l1/preflight-round45-frozen-both.json`)."
- **Exact input:** read the cited receipt: `rev: faa875bc0eb839d15b83c4afa6078819e5a7b381`
  (`git merge-base --is-ancestor faa875bc fedd11bf` → 0, i.e. it is A2's ancestor, not A2).
- **Observed:** the sentence's *substantive* claim is true — I ran the frozen preflight over both
  pathspecs (`--pathspec tools/round-45/ --pathspec plans/round-45-claims.md --freeze-path tools/round-45 --freeze-path plans/round-45-claims.md`) at A2: `verdict clean`, exit 0 (`pf-A2`, sha256
  `93e1da23…`) — and the lane already holds the correct artifact, `l1/preflight-at-A2-both.json`
  (`rev: fedd11bf…`, `verdict clean`), which the section does **not** cite. There is likewise **no**
  receipt gating the freeze to A3, the declared final measured revision; I ran it (`pf-A3`, `clean`,
  exit 0, sha256 `565f7251…`).
- **Fix:** point the A2 sentence at `preflight-at-A2-both.json`, and add the A3 gate receipt
  (`pf-A3`) beside `c1-at-A3.json`/`c2-at-A3.json`.

### F5 — MEDIUM — the C1 table row and the header are stale relative to the section's own final measured revision

- **Attacked cells:** `SCORECARD.md:3527` ("measured revision `1f4b27f8`") and `:3532` (C1 after-cell
  `block22_refs 7`, measured-at column `1f4b27f8`), while `:3590` declares "**The measured revision for
  the round is A3**" and `:3589` records `block22_refs 8` at A3.
- **Exact input:** the C1 counting command at `1f4b27f8` (7 — correct) and at `f59565b7` (8).
- **Consequence:** the table's numbers are individually true at the revision they name, so this is not a
  false number, but the table no longer describes the round's declared measurement, and the header
  names a revision the section itself supersedes. A reader who stops at the table gets `7`, a reader
  who stops at the A3 paragraph gets `8`.
- **Fix:** state the A3 values in the row (or mark the row "superseded by A3; `block22_refs 8`") and
  make the header say A3 with `1f4b27f8` as the first met measurement.

### F6 — LOW — "the round-44 counters' `frozen_path_changed` list" is plural by mistake

- **Attacked sentence:** `SCORECARD.md:3557-3558` — "Appending this section to `SCORECARD.md` also adds
  that path to the round-44 counters' `frozen_path_changed` list at any post-round-45 tip."
- **Exact input:** the two round-44 counters' frozen sets. `tools/round-44/c2-counter.py:134`
  `C2_DEFAULT_FROZEN = ('SCORECARD.md', 'SHONEN.md', 'SKILL.md')` → yes for C2.
  `tools/round-44/c1-counter.py:270-286` `FROZEN_PATHS` (claims file, round-44/round-42/round-39 tools,
  carriers, xpin) plus `FROZEN_PREFIXES = ('tools/round-44/', 'corpus/evidence/round-44/oracle/')` →
  `SCORECARD.md` is **not** frozen there, and `frozen_drift` (`:1629-1641`) only adds paths from
  `FROZEN_PATHS`, carrier paths and output trees.
- **Verdict:** true for the round-44 **C2** counter, false for the round-44 **C1** counter; the plural
  overstates. (`[INFERENCE]` for r44/C2's *runtime* behaviour — I did not execute that counter, whose
  rubric runs external checks; the frozen-set membership itself is read exactly from source.)
- **Fix:** "the round-44 C2 counter's `frozen_path_changed` list".

---

## 3. Every commit hash the section cites — ancestry of `main`

Extracted mechanically from the `## Round 45` section (10 hex tokens, 6 distinct commits), each
resolved with `git rev-parse --verify <t>^{commit}` and tested with
`git merge-base --is-ancestor <h> main`.

| token | commit | ancestor of `main` |
|---|---|---|
| `149133d47aa7e90796f96047afe6d251a3e65b2c` | `149133d47aa7` | **YES** |
| `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` / `f762b727` | `f762b7273e3f` | **YES** |
| `e715263cb51b713c342ab992d527fe9d61d6f8ff` / `e715263c` | `e715263cb51b` | **YES** |
| `1f4b27f82353d6544dc0c8048b3cfdadd8525d12` / `1f4b27f8` | `1f4b27f82353` | **YES** |
| `fedd11bf5ff9fe42d061169f78d77df59af4eca1` / `fedd11bf` | `fedd11bf5ff9` | **YES** |
| `f59565b782c18b0eb691bec12f52d2f80d9f5032` | `f59565b782c1` | **YES** |

No cited hash is unknown or off-`main`. (`a63d109f` is the tip the section sits on; `main` is one
commit further, `0ee50aaf`, which adds wave-1 record only — `git rev-list --count a63d109f..main` = 1,
`main..a63d109f` = 0.)

---

## 4. Receipts (exact command, exit, stdout sha256, UTC)

All stdout files and JSON receipts are in `receipts/` beside this report. Runner: `receipts/run.py`
(cwd `/`, `TMPDIR`/`HYAKU_SCRATCH` = scratch, bytes captured verbatim). Times are UTC, 2026-10-28.

| label | what | exit | stdout sha256 | time |
|---|---|---|---|---|
| `c1-A1` | c1-counter `--rev 1f4b27f8` | 0 | `d30817c559e0949ab8500a9f04e5349db79cac5d2bb8df2d8f88f6732463a32b` | 16:00:09Z |
| `c1-A2` | c1-counter `--rev fedd11bf` | 0 | `5bbfa17f1ea8c695f3105ec3532d6f6cec2869539d1b59c983098814e159480f` | 16:00:35Z |
| `c1-A3` | c1-counter `--rev f59565b7` | 0 | `90597e617067fe4f17399c7e114f36ff5ce7e7da24cb3ce7d06d3b43e57b6f18` | 16:00:35Z |
| `c1-land` | c1-counter `--rev e715263c` (refs **6**) | 0 | `cb869305df9b64d68e106ce1acfa326dd6d73c8b15f18b07d7546b898c5cc95f` | 16:00:35Z |
| `c1-tip` | c1-counter `--rev a63d109f` | 0 | `854b9ebec0a7c58edd7ced632fad42bc8545082d7ea1f0eda913bacc04799129` | 16:00:36Z |
| `c1-freeze` | c1-counter `--rev f762b727` (before) | 1 | `e2731609959b489750a703fc12a5605ad4538395c5f808424e142dfff41fb4e1` | 16:00:17Z |
| `c1-base` | c1-counter `--freeze f762b727 --rev 149133d4` | 2 | `2ad451743ac05872bfaad8c1e1a88d91055a0e3e0b770116c4f2f003e6c24ea6` | 16:01:30Z |
| `c2-A1` | c2-counter `--rev 1f4b27f8` | 0 | `2b401a9ae5a6e562178561fba15b2ae2199f019e9b1059b0b6f65175d5e4d1ca` | 16:00:09Z |
| `c2-A2` | c2-counter `--rev fedd11bf` | 0 | `1d4276779b3655f5c300f05cdbdde1ec4747ecceebe24f6cd9255c00ef1bd8ac` | 16:00:35Z |
| `c2-A3` | c2-counter `--rev f59565b7` | 0 | `a352f65c098e76f8a00dcb8a86725036f85fc26e86aef0d57db61061e42041d4` | 16:00:35Z |
| `c2-freeze` | c2-counter `--rev f762b727` (before) | 1 | `d6e202aac80ee78d9a6fbd1113ea5b62fb51b27503faccb38dec8afdb9216dd0` | 16:00:17Z |
| `c2-base` | c2-counter `--freeze f762b727 --rev 149133d4` → `freeze is not an ancestor of rev` | 2 | `c1b9db741fabb5e758958cbff3172c9280589cc972b826d84379129bbf3efe59` | 16:00:17Z |
| `c2-base-selffreeze` | c2-counter `--freeze 149133d4 --rev 149133d4` → `scope file absent at rev` | 2 | `ab4227f82c5ece647630d9d1d65a5eb497bb80d22ed68a54ee942e6284d9f254` | 16:00:35Z |
| `cmdA-freeze` | recipe A at `f762b727` (138/138, 21/21, 10.0/10.0) | 0 | `4a1bfae34d8fa32963e50438f01d09c63e0c0fa52597ceb523b14601dd1859a6` | 16:03:22Z |
| `cmdA-A1` | recipe A at `1f4b27f8` (138/138, 22/22, 10.0/10.0) | 0 | `b8f35e3e9f2be3aaf37f30a5f49136010ef0a310e55d705b00ad959e86c97f9a` | 16:00:58Z |
| `cmdA-land` | recipe A at `e715263c` (138/138, **21**/22, 10.0/9.55) | 0 | `bbbf9e61726c07405c6eb000b306843b06a1f7285fb11890abb2c0d7dc15ae94` | 16:00:58Z |
| `cmdA-A3` | recipe A at `f59565b7` (138/138, 22/22, 10.0/10.0) | 0 | `ea7c9d876ae05de7203a143a10d6c14888f7aaf94d1562786746aa2d6df3bbb9` | 16:00:58Z |
| `pf-faa` | frozen preflight, freeze→`faa875bc`, both pathspecs | 0 | `4b5a685dc4274637efd76b2349acd384bfb817ec70b8203ca891c69c6b20c658` | 16:03:07Z |
| `pf-A2` | frozen preflight, freeze→`fedd11bf`, both pathspecs | 0 | `93e1da236849ab4354a8633a0e23bb6ac44e824d40993d2b4c53f8582369fc4f` | 16:03:07Z |
| `pf-A3` | frozen preflight, freeze→`f59565b7`, both pathspecs | 0 | `565f72513f20c7737a59da495e62062c33cd68f95a75d59348ddf18392d1ea7d` | 16:03:07Z |
| `pf-tip` | frozen preflight, freeze→`a63d109f`, both pathspecs | 0 | `f8f32cb42126cf6c3bd686c1b593d05e1e3bdd2ec2b5dcf3d9397b9cbc10b62d` | 16:03:07Z |

By-hand checks with no receipt file (read-only, `git`/`grep`/`python3 -c` only):
freeze derivation, `f762b727^` = base, the four-revision `block22_refs` series, the 10-row/22-block
independent extraction, the 6-row registry parse, 138/138 independent coverage count, per-citation
line-range resolution at A3, the per-token ancestry sweep, `sha256sum` of the A3 preflight bytes vs
the freeze blob (`633ebc05…` both), and `--selftest` on the extracted bytes (11/0, exit 0).

---

## 5. Residual risk and what was not run

- **F6 is static** for the round-44 C2 counter: I read its frozen set (`C2_DEFAULT_FROZEN`) and its
  rubric binding, but did not execute it (its rubric drives external checks). The round-44 C1
  counter's exclusion of `SCORECARD.md` is exact from source.
- **Not exercised:** the section's non-numeric statements — "quality improved", "discernment improved",
  "expansion unchanged", "the four r44/r45 counters' exit maps were read from source by one seat each",
  "the S138 `opened` over-claim is corrected append-only with a live fetch". They have no numeric
  observable and no named receipt in the section, so they are neither verified nor falsified here.
- **Reconciliation note for the L1:** F1, F3, F5 are one family — the record was amended by appending
  new paragraphs while leaving the earlier table/header values in place, and the appended paragraphs
  then asserted equality across revisions that the round's own receipts contradict. F2 is a different
  family (a count attributed to a file that settlement has not yet written). F4 and F6 are citation
  defects where the substantive fact survives.
- Everything in §1 that "holds" was re-derived with the round's own instruments **and** at least one
  independent mechanism (regex split, `grep -c`, `ls-tree`, or a hand parser), so a coincidence of the
  counter with itself is not the only support.
