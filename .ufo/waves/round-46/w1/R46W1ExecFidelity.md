# R46W1ExecFidelity — round-46 wave 1: frozen-counter fidelity and selftest audit

Seat `R46W1ExecFidelity`, lane `kaidoku`, round 46, wave 1. Read-only on the lane tree: every
write is under `.ufo/waves/round-46/w1/R46W1ExecFidelity/` (this report, `receipt.tsv`,
`receipts/`). Nothing was installed (no pacman, uv, npm or PATH write). Nothing was committed,
staged or stashed.

- **Stated freeze (prompt, contract):** `31820472784284727546808acc31b3ea1e73919b`.
- **Lane state at report time:** `21b55a8feb2e13f757a423428b7de585b9552968`.
- **The lane moved during this session** (seven commits between `16:56Z` and `17:04Z`:
  `7bf33e31`, `17a72375`, `781e19ae`, `0425224`, `1e32827b`, `49e6cac4`, `21b55a8f`). Every
  receipt below records the `rev` the counter itself resolved, and the ledger's UTC is the
  receipt file's mtime; where a run used `--rev HEAD` the resolved object id is in the receipt
  and in the ledger comment. The two r45 fidelity receipts use fixed historical revisions and
  are unaffected by the movement.

## 1. The freeze bytes

Extracted with `git show 3182047:<path>` into scratch (originals never touched). sha256 is over
the extracted bytes; blob is `git ls-tree`.

| path | blob | sha256 of bytes at 3182047 |
|---|---|---|
| `tools/round-46/attest.py` | `25883520b425` | `dd1e7df1682c5b63ed9f5f75a3aff26c7914e6d41885e5e2da717aa91165d0fb` |
| `tools/round-46/gate.py` | `d7cd9aace310` | `64626cca85b2de25d495155318493b3b9eab73c6f31ad7b78f4e76c4344d772e` |
| `tools/round-46/registry.py` | `6581c1b2acb8` | `307506d51f04bb1212aedc34619b675adc378ec8cfeb1ea5d15ac53582b7a449` |
| `tools/round-46/census.py` | `17c4ad5a4a23` | `960c516d3b5cb1bb0306bf7f44f848a76b9c795c5319328954b5021b234c1fd5` |
| `tools/round-46/census.json` | `cf8c8d3e863a` | `573ec008fc3f9173da04589c013484485758e9cf1c901a254bf1d6286d62133e` |
| `plans/round-46-claims.md` | `f60fb6310662` | `a09564e0a2e200c46f6c1fc56991813ad13c5b67f1b5e70721ab3ceee7afad01` |

The claims file is **byte-identical at every commit from 3182047 to HEAD** (all five hashes
`a09564e0…`). Only `tools/round-46/` moved: `50862e4a`, `65678df0`, `0425224`.

## 2. Selftests, run from the freeze bytes

```
python3 -I -B $S/frozen/attest.py   --root <lane> --freeze 3182047… --rev 3182047… --selftest
python3 -I -B $S/frozen/registry.py --root <lane> --freeze 3182047… --rev 3182047… --selftest
```

| counter | exit | banner line | stdout sha256 |
|---|---|---|---|
| `attest.py` (freeze bytes) | 0 | `ATTEST_SELFTEST: cases=15 failures=0` | `ac22e9c7acb4bb6fc66b98bdb203190dc64f18bb7121e686f02fa195810e8ddb` |
| `registry.py` (freeze bytes) | 0 | `REGISTRY_SELFTEST: cases=12 failures=0` | `0fa8c31a6419905fcb1971cb32631862be682014339a9e390634d360fd11872e` |

- Both selftests are green from the freeze bytes, so the freeze is **not** a crash-on-import.
- **Discrepancy 1.** The frozen claims file states `registry.py --selftest` prints
  `cases=11 failures=0` (`plans/round-46-claims.md:194`). The freeze bytes print **12** cases
  (the twelve `case(...)` calls at `registry.py:507-524`, including `red-v1-accepts-fenced`).
  The same count 12 is printed by the F4 bytes. The claims file is frozen, so this record error
  stands; it is an understatement, not a false pass.
- **Discrepancy 2.** The same paragraph says every predicate clause "was exercised before this
  freeze". Clause 7 (the C1 battery counts) has **no** selftest case in the freeze bytes: the
  `case()` helper takes no `battery` argument and the `green-with-battery` case was added later
  by F3. So clause 7 is unexercised at 3182047 — and, as §6 shows, would not pass there.
- Current instruments for context: `attest.py` at HEAD prints `cases=16 failures=0`
  (`0bf8f4c6…`), `registry.py` `cases=12 failures=0` (`0fa8c31a…`, same bytes as the freeze's
  registry selftest).

## 3. Fidelity receipts — the r45 port against round 45

Commands (freeze bytes; `--no-battery` because the r45 artefact has no r46 battery):

```
python3 -I -B $S/frozen/attest.py   --root <lane> --spec r45 --profile v1 --no-battery \
  --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec \
  --rev    f59565b782c18b0eb691bec12f52d2f80d9f5032
python3 -I -B $S/frozen/registry.py --root <lane> --spec r45 --profile v1 --no-battery \
  --freeze f762b727… --rev f59565b7…
```

| counter | exit | every receipt field | stdout sha256 |
|---|---|---|---|
| `attest.py --spec r45 --profile v1` | 0 | `rule_blocks 22`, `block_present 1`, `block_is_last true`, `marker_occurrences 1`, `header [trigger, arm, exit, receipt]`, `header_ok true`, `rows 10`, `refs 8`, `cited` = the five r45 paths, `unresolved_citations []`, `cites {S140 true, tools/round-45/frozen-path-preflight.py true}`, `frozen_derived [tools/round-45/, plans/round-45-claims.md]`, `touched 0`, `restored []`, `frozen_path_changed []`, `met_target true` | `419339114d48b3c2f1735c0be70f4044d9d507f1cad109c5633b6f183a47d6fc` |
| `registry.py --spec r45 --profile v1` | 0 | `scope_size 6`, `registry_rows 45`, `registered` = the six r44/r45 paths, `unregistered []`, `thin []`, `absent_at_rev []`, `header null` (r45 parse), `frozen_derived [tools/round-45/, plans/round-45-claims.md]`, `touched 0`, `frozen_path_changed []`, `met_target true` | `fab5a4110465f498caded3c480cdadd29f47037f4ab6d2aa1c207bab3fdc315c` |

Cross-check against round 45's **own** counters at the same two revisions (extracted from
`f59565b7` and run against the lane):

| round-45 counter | exit | values | sha256 |
|---|---|---|---|
| `tools/round-45/c1-counter.py` | 0 | `rule_blocks 22`, `block22_rows 10`, `block22_refs 8`, `block22_unresolved_citations []`, `block22_header_ok true`, `block22_cites {S140 true, interpreter true}`, `preflight_selftest {cases 11, failures 0, exit 0}`, `met_target true` | `90597e617067fe4f17399c7e114f36ff5ce7e7da24cb3ce7d06d3b43e57b6f18` |
| `tools/round-45/c2-counter.py` | 0 | `registry_rows 45`, `scope_size 6`, `registered` = six, `thin []`, `unregistered []`, `met_target true` | `a352f65c098e76f8a00dcb8a86725036f85fc26e86aef0d57db61061e42041d4` |

Field-level diffs (script comparison, common keys only):

- frozen `attest.py` r45 receipt vs `.ufo/waves/round-46/controls/ctl-c1-fidelity.json`:
  **no differing common key, no key present in one and not the other.**
- frozen `registry.py` r45 receipt vs `ctl-c2-fidelity.json`: **identical field-for-field.**

So the round-45 recorded values the seat names — `rule_blocks 22`, `block22_rows 10`,
`block22_refs 8`, `registry_rows 45`, `scope_size 6` — are reproduced exactly, by the frozen
port and by round 45's own instruments.

## 4. Is the v1 profile a faithful port or a straw man?

**For the declared fidelity receipt it is faithful, not a straw man.** `--spec r45 --profile v1`
returns the same verdict and the same numbers as the round-45 counters on the round-45 artefact,
and the two control receipts are field-identical.

**For the batteries the claim actually requires, the frozen v1 arm was not the round-45 clause
set at all — it was accidentally *stricter*, so the claimed battery values were unattainable.**
Measured from the freeze bytes:

- C1 clause 7 (`v1_green == 9`): with the frozen file's dead name rebound in memory only
  (`probe_battery.py`, originals untouched), the frozen battery returns `forgeries_total 9`,
  `v1_green 1`, `v2_green 0`, `genuine_green 1`, counter exit **1** with
  `failing ["battery v1_green 1 != 9"]`. Only `header-substring` is v1-green; the other eight
  forgeries are rejected by the v1 arm because the frozen v1 header test looks for round-45
  tokens (`receipt`) in an r46 header and the row floor is 13.
- C2 clause 6 (`v1_green == 7`): a fixture repo holding the L1's drafted registry section
  (`l1/registry-section.md`, 38 rows × 7 cells) plus the frozen census scores structural v2
  **green** (38/38 registered, 0 thin, 0 absent) but the battery returns `v1_green 5` — exit 1
  with `failing ["battery v1_green 5 != 7"]`. `substring-cell` and `prose-exit` are rejected by
  the v1 arm because `strict_cell` and `strict_exit` are not gated by `hard` in `score()`.

The lane has since repaired exactly this, in two post-freeze commits: F3 `65678df0` (attest) and
F4 `0425224` (registry). With the current bytes the same measurements give C1 `v1_green 9`
(all nine forgery fixtures `v1_exit 0`, `v2_exit 1`) and C2 `v1_green 7` (all seven `v1_exit 0`,
`v2_exit 1`). `corpus/lessons/round-46.md:19` (M46-3) already records the freeze series; the
numbers above are the independent measurement of the two v1 arms, which M46-3 does not quantify.

Residual divergence of the v1 port from the round-45 predicate, read from source (not
hypothetical): round 45 required (a) the interpreter's own `--selftest` green at `--rev`,
(b) the interpreter present at `--rev`, (c) the marker block count *exactly* 1. The v1 port has
none of (a)/(b) and uses `>= 1` for (c) — all weaker on the artefact, so v1 cannot inflate the
v2 improvement. It also shares the hardened freeze arms (`gate.freeze_state`), which are
*stricter* than round 45's `git log --name-only`. Net: faithful in the measured direction.

## 5. The freeze is a series, and the stated freeze cannot score

The frozen claims file says the freeze is "the commit that first contains this file and
`tools/round-46/`", that nothing in either changes after it, and that "a change makes both
counters exit 2 `frozen_path_changed`". The first such commit is `3182047`. Three later commits
touch `tools/round-46/`:

| commit | UTC | change |
|---|---|---|
| `50862e4a041499dd2ce0da68d10301b765bb9997` | 13:51:57 | `gate.main_guard` returns a tuple; battery runs only after the structural clauses pass |
| `65678df0f1666e83cdeea7233bfb31ffe73ec709` | 13:55:07 | attest battery's dead `REF`; v1 header/row-floor/selector; a battery selftest case |
| `0425224756791b414454df28a9abf93dcdf154ce` | 14:00:46 | registry v1 profile applies its own loose checks |

Measured, at `--freeze 3182047`:

| run | rev resolved | exit | reason |
|---|---|---|---|
| frozen `attest.py` | `e3dfdbad` | 2 | `frozen_path_changed`; `touched`/`restored` = attest.py, gate.py, registry.py; `blob_changed ["tools/round-46/"]` |
| frozen `registry.py` | `e3dfdbad` | 2 | same |
| HEAD `attest.py` | `49e6cac4` | 2 | same |
| HEAD `registry.py` | `49e6cac4` | 2 | same |
| HEAD `attest.py` | `21b55a8f` | 2 | same |
| HEAD `registry.py` | `21b55a8f` | 2 | same |

So **every** artefact revision after the stated freeze — including the landed block 23 and the
landed registry — is inadmissible against the prompt's freeze. The lane in fact scores at
`freeze = rev = 0425224` (`l1/scores/c1-at-F4.json`, `c2-at-F4.json`), where `FREEZE..REV` is
empty and the frozen-path arm is vacuous by construction. Re-run at that freeze against the
current HEAD, both are green:

| counter (current bytes) | freeze | rev | exit | values |
|---|---|---|---|---|
| `attest.py` | `0425224` | `21b55a8f` | 0 | `rule_blocks 23`, `rows 13`, `refs 9`, `pin e6c44d2d… == expected`, `battery 9/9/0/1`, `failing []` |
| `registry.py` | `0425224` | `21b55a8f` | 0 | `scope_size 38`, `registry_rows 38`, `unregistered [] thin [] absent_at_rev []`, `battery 7/7/0/1`, `failing []` |

Those two receipts match `l1/scores/c1-at-F4.json` and `c2-at-F4.json` field-for-field except
`rev` (the lane's are recorded at rev `0425224`; mine at rev `21b55a8f`, whose `tools/` and
`SKILL.md` blobs are unchanged — `git diff 49e6cac4 21b55a8f` touches only the lesson).

Pin coherence: block 23 pins `sha256:e6c44d2d57dbbc65ed8d14b642a6101eea264b05faf68c25606525b8fe532346`,
which is the sha256 of `attest.py` from F3 onward; the 3182047 bytes are `dd1e7df1…`. Clause 6
("equal to the sha256 of `tools/round-46/attest.py` at the measured revision") therefore holds
only for a measured revision at or after F3.

## 6. Defects in the frozen (3182047) bytes — reported, not fixed

Each line names the exact command shape and differs only in value from what the claims file
asserts. None of these were repaired by this seat.

**D1 — an unhandled exception exits 1 with a traceback, not 2.**
`python3 -I -B $S/frozen/attest.py --root <lane> --freeze 65678df0 --rev HEAD` →
`{"reason": "unhandled NameError: name 'REF' is not defined"}` followed by
`TypeError: cannot unpack non-iterable int object`, exit **1** (sha `7d900cb2…`).
Cause: frozen `gate.main_guard` returns the int `2`, while both counters unpack
`code, receipt = gate.main_guard(...)`. The file's own contract says "An unhandled exception is
a defect, never a verdict: every entry point catches it and returns 2", and `R45-CL13 (f)`
required exit 2 with a reason. The freeze bytes violate it; F3/`50862e4a` fix it.

**D2 — the frozen registry battery runs before the structural verdict.**
`python3 -I -B $S/frozen/registry.py --root <lane> --freeze 3182047 --rev 3182047` →
`{"reason": "unhandled AttributeError: 'NoneType' object has no attribute 'splitlines'"}` then
the same `TypeError`, exit **1** (sha `40f46c32…`). With `--no-battery` the same command returns
a proper receipt: exit 1, `markers: 0 open, 0 close`, `header null`, `unregistered: 38 of 38`
(sha `d89e522f…`). The registered control `ctl-c2-0-do-nothing.json` carries
`freeze 50862e4a` and `battery {"skipped": …}`, so **that control cannot be produced by the
freeze bytes** — it was produced by the post-freeze fix.

**D3 — the C1 do-nothing control's stated exit is not what the freeze bytes return.**
`... --freeze 3182047 --rev 3182047` (default battery) → exit **2**,
`"battery: cannot build a battery: marker blocks 0"` (sha `f44d667d…`). The claims' "Before"
says "at the freeze, exit 1 — `block_present 0`, `rows 0`, `marker_occurrences 0`", which the
freeze bytes return only with `--no-battery` (exit 1, sha `547507e6…`). A 2 never counts toward
a target, so the freeze cannot demonstrate even the do-nothing arm without a flag the counting
command does not carry.

**D4 — C1 clause 7 is unattainable from the freeze bytes.** `v1_green 1 != 9` (exit 1), measured
with the dead `REF` rebound in memory only (sha `856373a7…`). Per-forgery v1 exits: `garbage-rows`,
`thin-rows`, `lineless-refs`, `two-markers`, `stub-pin`, `self-refs`, `missing-routed-id`,
`no-vocab-arm` = 1; `header-substring` = 0; every v2 exit = 1; `genuine_exit 0`.

**D5 — C2 clause 6 is unattainable from the freeze bytes (and from the pre-F4 bytes).** With the
L1's drafted section in a fixture: `registry_rows 38`, `unregistered 0`, `thin 0`,
`absent_at_rev 0`, but `v1_green 5 != 7`, exit 1 (sha `c298256b…`; the pre-F4 HEAD bytes return
the byte-identical receipt). Per-mutation v1 exits (frozen registry, `probe_v1_gap.py`,
sha `46147e07…`): `fenced 0`, `off-section 0`, `substring-cell 1` (`unregistered: 38 of 38`),
`prose-exit 1` (`thin verdict-map cells: 1`), `html-comment 0`, `first-wins-shadow 0`,
`no-header 0`; all seven v2 exits 1. With F4 bytes the same fixture is exit 0,
`forgeries_total 7 / v1_green 7 / v2_green 0 / genuine_green 1` (sha `bc6ab7e2…`).

**D6 — the frozen claims file's selftest count is wrong** (`cases=11` at
`plans/round-46-claims.md:194`; the bytes print 12). It is an understatement; no clause depends
on it, but the frozen record is inaccurate and the file is byte-frozen.

**D7 — three named control receipts are absent.** The frozen claims file names six control
receipts; `controls/` (as of `21b55a8f`) holds five files: three match a claimed name, two
(`ctl-c2-0-do-nothing.json`, `ctl-c2-1-v1-scope.json`) are not named in the claims, and three
claimed names have no file:

| claims line | named receipt | present? |
|---|---|---|
| `plans/round-46-claims.md:94` | `controls/ctl-c1-0-do-nothing.json` | yes, but its `freeze` field is `50862e4a`, and the freeze bytes cannot produce it (D3) |
| `plans/round-46-claims.md:96` | `controls/ctl-c1-1-v1-profile.json` | **no** |
| `plans/round-46-claims.md:102` | `controls/ctl-c1-fidelity.json` | yes, field-identical to my re-run |
| `plans/round-46-claims.md:158` | `controls/ctl-c2-1-v1-profile.json` | **no** (a `ctl-c2-1-v1-scope.json` exists; different receipt) |
| `plans/round-46-claims.md:159` | `controls/ctl-c2-2-ghost-tool.json` | **no** |
| `plans/round-46-claims.md:160` | `controls/ctl-c2-fidelity.json` | yes, field-identical to my re-run |

Reconstructed from the F3/F4 bytes: `--profile v1 --freeze 0425224 --rev <HEAD>` → exit 0,
`battery 9/9/0/1` (sha `7541ce89…` at rev `49e6cac4`), so the C1 v1-profile control is
reproducible but was never written. The "ghost-tool" and C2 v1-profile controls remain
unreproduced here because they need the forged section the claims describe; that is wave 2's
data, not this seat's.

**D8 — two residual v2 non-discriminations in `attest.score` (still present at HEAD).**
1. Arm vocabulary is matched by **substring**: `any(t in r[arm_col].lower() for t in ARMS)`.
   An arm cell `uncommitted` passes; only `zzz` fails.
2. The per-row trigger requirement is not enforced: clause 4 is computed as the **union** of
   `R45-CL\d+` over cell 0 (`finditer(r"R45-CL\d+", r[0])` + `missing`), so a fourteenth row
   whose trigger names no routed id passes as long as the thirteen ids appear elsewhere.

   Probe (HEAD bytes, `l1`-independent): a block with the 13 genuine rows plus
   `| a trigger naming no routed id | off topic | commit | 0 |` → exit **0**;
   plus `| R45-CL2 | ghost | uncommitted | 0 |` → exit **0**; the `zzz` control → exit **1**
   (`arm cells outside the vocabulary: 1`). sha `608a66e1…`, identical at the freeze bytes and at
   HEAD. The claim's landed-surface prose says "every row's trigger names a routed `R45-CL<n>`
   id" and clause 4 says "every arm cell is in the vocabulary"; the measure is weaker than both,
   and neither forgery class is in the nine-fixture battery. This is the same class as the
   round-45 header-substring defect, in a new column.

**D9 — the shared gate's frozen set is not self-protecting (still present at HEAD).**
`gate.frozen_set` derives the frozen paths from the claims file **at `rev`**. If a post-freeze
commit edits the claims file and *drops its own entry* from `## Frozen paths (exact)`, neither
the history arm nor the blob arm sees the claims change: the derived set becomes
`["tools/round-46/"]` and the tool bytes are untouched. Fixture probe (frozen and HEAD `gate.py`
give the identical receipt, sha `01aa0c00…`):

| probe | exit | derived set |
|---|---|---|
| tool edited, claims intact | 2 | both entries |
| claims edited, both entries intact | 2 | — |
| **claims edited, its own entry dropped** | **0** | `["tools/round-46/"]` |
| tool edited and `tools/round-46/` line dropped | 2 | `["plans/round-46-claims.md"]` |

The one-file commit that rewrites the rule text while leaving the tools alone is clean. `R45-CL18`
closed the *scope-difference* hole; this is the *self-reference* hole and it is not in block 23's
rows. The 3182047 prose already bounds a different limit honestly (`R45-CL19` squash), so the
table could carry this one too — but the frozen bytes do not compute it.

## 7. What the current tree actually is

- `SKILL.md` block 23 landed at `227d6982`, re-pinned at `6e018068`, cites a knowledge entry from
  A3 `7bf33e31`; at the current bytes C1 is green.
- The registry landed at `781e19ae`; C2 is green at the current bytes (38 of 38, 0 thin, 0
  absent, battery 7/7/0/1). Before that, at rev `17a72375` my registry run was red
  (`markers: 0 open, 0 close`, `header null`, `unregistered: 38 of 38`, sha `464fc655…`).
- The only admissible scoring range for either claim today is a freeze at or after F4
  (`0425224`); at the prompt's `3182047` both counters exit 2.
- The lane's own record already says this: `corpus/lessons/round-46.md:19` M46-3
  `freeze-moved-four-times`. My receipts independently reproduce M46-3's claims and add the two
  battery shortfalls (`v1_green 1`, `v1_green 5`), the exact crash modes, the selftest-count
  error, the missing control, D8 and D9.

## 8. Limits of this seat

- Not run: a merge fixture for the `-m --diff-merges=first-parent` history arm (the selftest has
  no merge case; `R45-CL6` is source-read here, only the non-merge touch case is exercised).
  Not run: `--json-out` refusal and scratch-refusal probes through the counter CLI (both are
  source-read; the selftest does not cover them).
- The `--profile v1` battery numbers for the freeze bytes depend on the in-memory `REF` rebound
  in `probe_battery.py`; without it the frozen bytes crash (D1). The patch is stated in the
  probe's docstring and the frozen files were never modified.
- `receipts/` holds every stdout cited, the probe scripts, the fixture builder and its
  `fixture.json`; `receipt.tsv` carries UTC, exact command, exit and stdout sha256 per receipt.
- Installs/upgrades: **none**. No mutation of the lane tree, no git write, no PATH write.

## 9. For the L1, in priority order

1. **Do not score either claim at `3182047`.** Both exit 2; the admissible freeze is `0425224`
   (or any later commit that leaves `tools/round-46/` untouched). The wave report should cite
   the freeze it actually used, per claim, and the `frozen_path_changed` receipts for the
   stated one.
2. **D8 is a live non-discrimination hole in a green instrument.** Either add two forgery
   classes (`arm-substring`, `row-without-routed-id`) to the battery or tighten `attest.score`
   to token equality on the arm cell and a per-row id requirement — but not in this freeze; it
   is a next-round instrument change with its own freeze.
3. **D9 is a gate defect, not an artefact defect.** The frozen set should include the claims
   file unconditionally (round 45 hard-coded `FROZEN = [CLAIMS, "tools/round-45"]`; the
   derivation lost that guarantee). Route it with the round-47 freeze core.
4. **Correct the record, not the frozen file:** `cases=11` → 12, and the missing
   `ctl-c1-1-v1-profile.json` should be written (my reconstruction shows it is green) or the
   claims' pointer amended in a later claims file.
5. M46-3/M46-4 already stand; my receipts are the evidence file for them. No new lesson row is
   needed from this seat.
