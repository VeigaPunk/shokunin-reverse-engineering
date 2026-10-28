# Round 46 lesson draft — Mistakes and Gate (seat `R46W1ScribeLesson`, wave 1)

Seat draft for the L1 to land in `corpus/lessons/round-46.md`. Every number below is a
receipt in `.ufo/waves/round-46/w1/R46W1ScribeLesson/` with its exact command, exit code,
UTC stamp and stdout sha256 (`receipts.tsv`). Revs used: declared freeze
`31820472784284727546808acc31b3ea1e73919b` (dispatch and
`plans/round-46-claims.md`'s own re-derivation), measured freeze
`65678df0f1666e83cdeea7233bfb31ffe73ec709`, landed-section rev
`781e19ae674225b6be0b5de56ee8574679bac0b6`, post-F4 rev
`0425224756791b414454df28a9abf93dcdf154ce`. Frozen counter bytes are read as
`git show 65678df0:tools/round-46/<f>` into scratch copies; the lane tree was never written.

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M46-1 | `control-named-a-measurement-that-cannot-exist-at-the-freeze` — the plan names four control receipts "at the freeze"; the C1 v1-profile control's subject (the nine forged copies of **block 23**) does not exist at the freeze, so its stated value cannot exist there either. At the declared freeze the artefact is absent; at the measured freeze the battery runs but the receipt is red for a second reason (the battery's *genuine* arm is scored with `--profile v2` whatever `--profile` says). | `plans/round-46-claims.md` R46-C1 "Before" bullet 2 ("`controls/ctl-c1-1-v1-profile.json`: … scored with `--profile v1` at the freeze, exit 0 with `forgeries_total 9`, `v1_green 9`") and R46-C2 "Before" (`ctl-c2-1-v1-profile.json`, `ctl-c2-2-ghost-tool.json`). Measured: **R13** `attest.py --profile v1 --freeze 3182047 --rev 3182047` → exit 1, `block_present 0`, `marker_occurrences 0`, `rule_blocks 22 < 23`, battery `skipped`; **R3** `--profile v1 --freeze 65678df0 --rev 65678df0` → exit 1, `failing ["battery genuine_green 0 != 1"]` with `forgeries_total 9`, `v1_green 9`. The named files are absent: `.ufo/waves/round-46/controls/` holds five receipts and none is `ctl-c1-1-v1-profile.json`; the present `ctl-c2-1-v1-scope.json` is `counter: round-45-c2`, `scope_size 6` (the round-45 counter, not a v1-profile run of the seven C2 forgery classes); `ctl-c2-2-ghost-tool.json` is absent. | the satisfiability preflight, which asked *"can the instrument compute this clause"* and never *"at which revision does this value exist"* — and never *"does the named control file exist"* | the v1-gap receipt is produced **post-landing** and the plan says so: `l1/scores/c1-v1-genuine-A2.json` (v1 profile, post-landing rev, exit 0) plus the battery block inside `c1-at-A2/A3.json` (`v1_green 9`). Shown able to fail: the same battery is red on the frozen C2 bytes (R12, `v1_green 0`) and green only after F4 (R5/R10/R11, `v1_green 7`), so "the v1 profile accepts every forgery" is not an assumption the receipt can carry |
| M46-2 | `plan-contradicted-its-own-instrument` — R46-C2 clause 6 requires `battery.v1_green == 7` ("the v1 clause set scores all seven forgery classes green"), and the plan's own frozen `registry.py` computes **0**: the v1 branch switches only the marker/fence parse, while `strict_cell`, `strict_exit` and `presence` are gated on the *spec* alone, so the "ported" v1 clause set keeps the v2 checks and rejects all seven forgeries. The claim is unsatisfiable at the bytes it froze, and its own frozen verdict says so. | **R12** (frozen `registry.py`, sha256 `db5adc02…`) `--root <lane> --freeze 65678df0 --rev 781e19ae` → exit 1, `failing ["battery v1_green 0 != 7"]`, all seven fixtures `v1_exit 1`. This is the L1's own `l1/scores/c2-at-781e19ae.json` (mtime 2026-10-28T16:59:26Z) reproduced exactly, not a seat artefact. Code read: `if spec["strict_cell"]` / `spec["strict_exit"]` / `spec["presence"]` at `db5adc02` vs `if hard and …` after F4 `0425224`. | `none` in the instrument — each battery asserts its own v1 numbers; neither compares the profile's clause set with the round-45 counter's, and `--fidelity` compares **values** (45/6), never the clause set | F4 (`0425224`) makes the three checks v2-only → **R5/R10/R11** exit 0, `v1_green 7`, identical stdout sha256 `116cebac…` in three invocations (scratch cwd, lane cwd with absolute root, lane cwd with `--root .`), while **R12** on the replaced bytes stays exit 1 — the fix is shown able to fail on what it replaced. Consequence: under the plan's own freeze rule nothing may change in `tools/round-46/` after the freeze, so F4 necessarily converts every later score into exit 2 — **R14** `--freeze 65678df0 --rev 0425224` → exit 2, `frozen_path_changed ["tools/round-46/", "tools/round-46/registry.py"]` |
| M46-3 | `claim-text-not-computed-by-its-own-clause-set` — three sentences of the frozen plan are stronger than the clause the counter computes, and one narrowing is the reverse. Each is measured, not read. | (a) "every row's trigger names a routed `R45-CL<n>` id" (Landed surface) vs clause 4 (thirteen ids appear in *some* row): **P1**, a 14th row `\| scratch note, no routed id \| nothing routed \| pin \| 0 \|` appended to the landed block → frozen `attest.py` exit 0, `met_target true`, `rows 14`, battery `9/9/0/1/0` = true. (b) "at least six citations carry a line selector and resolve" vs clause 5's `refs >= 6` counted per occurrence: **P2**, Refs paragraph cut to one citation repeated six times → `refs 7`, `met_target true`, exit 0. (c) the Freeze-integrity rule's "`restored` names a path the history arm saw and the blob arm finds clean": the blob arm reports the frozen **directory** while the history arm reports files, so every touched file is reported `restored` although modified — **R1** (`blob_changed ["tools/round-46/"]`, `restored` = the three touched files) and **R14** (`blob_changed ["tools/round-46/"]`, `restored ["tools/round-46/registry.py"]`). (d) R46-C2 clause 4 says the cell "enumerates `0=`, `1=`, `2=`"; `EXITMAP = \b([012])\s*[=:]` also accepts `0:` (code read, no receipt). | `none` for (a)–(c): the counters check clause values, not the sentences that describe them, and the battery only mutates the artefact *toward* each named defect class, never away from an unstated one | every row's cell 0 must carry a routed id (`re.search(r"R45-CL\d+", r[0])` per row, not on the union) and citations must be counted as `len(cited)`, a distinct-path set; the `restored` list must be computed after normalising both arms to the same granularity. Shown able to fail: P1 and P2 already are the red cases the current selftests lack |

There is no `captured-by: none`→`QUALITY.md` question pending here: (a) and (b) are caught
by a probe that the battery's own method can run, so the fix is a case, not a criterion.

## Gate

### Sources opened this round (2026-10-28)

| row | URL | opened | located quote (≤25 words) |
|---|---|---|---|
| S142 | https://git-scm.com/docs/git-log | 2026-10-28T17:05:32Z, HTTP 200, 375,834 bytes, page sha256 `0a73e33b235368af3021b6dc7dbca11ca4b513157ac651acf548d94e1a5c4a1a`; anchors `--diff-merges=<format>` and value `first-parent` | "Show full diff with respect to first parent. This is the same format as --patch produces for non-merge commits." (19 words) |

The fetch above is the seat's own (recorded as HTTP status, byte count and page sha256;
the 375 KB body is not retained, since the page is re-fetchable and the digest is the identity):
it reproduced the S142 row's recorded digest **byte for byte**, so the page is
byte-stable across at least two fetches and a page sha256 is usable identity here — unlike
S138's `github.com` page (`R45-CL12`), where two fetches differed in 667 bytes. The row is
cited by the round's R46-C1 landing: `tools/round-46/gate.py`'s history arm passes
`--diff-merges=first-parent` precisely so a merge's own resolution edit is visible, the arm
`R45-CL6` found missing.

### Admission and rejection

- **Admit** S142 as a registry row (`docs`, tier A, `mined`, recheck `on-release`,
  `used-by corpus/lessons/round-46.md`): opened this round and cited by R46-C1's instrument.
- **Assimilation: none.** The round lands a *measure*, not a domain claim; `considerthese/`
  is absent in this lane, S142 cites no staged row, and no `merge/kaidoku/` theme proposal
  applies. The round-44 quarantine refusals stand unchanged (S150 fabrication-class;
  S113/S136/S147 anchor caveats; S117 unverifiable), so no row is appended from the staged
  set.
- **Census before → after:** `corpus/SOURCES.md` rows **141 → 142**
  (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`; 141 measured at
  `227d6982^`, 142 now). Round-start census `<L1 fills>` (round 45 closed at `kaidoku ok`,
  exit 0, 14 `W04`); round-end measured: `kaidoku ok`, exit 0, **15 `W04`** — S142 adds
  warning #15 because its URL duplicates this lane's own `S074`
  (`git-scm.com/docs/git-log`: 1 occurrence before `227d6982`, 2 after). The Gate must state
  that delta; it cannot repeat round 45's "adds no new `W04`" line. No `status` / `recheck` /
  `used-by` cell of an existing row was changed.

## Reconciliation with the landed draft

`corpus/lessons/round-46.md` was already committed while this seat ran (`227d6982`,
`49e6cac4`, `21b55a8f`). Mapping, so the L1 merges rather than duplicates:

- Landed **M46-1** is this draft's M46-1 (same class). This draft adds R13/R3 and the two
  absent C2 control names; the landed row's fix names a `c1-v1-gap` path that does not exist
  in `l1/scores/` (`c1-v1-genuine-A2.json` does).
- Landed **M46-2** (`plan-froze-a-number-the-code-does-not-fix`, routed as R46-CL4) is a
  different defect. If the id is kept, this draft's M46-2 becomes **M46-5**.
- Landed **M46-3** (`freeze-moved-four-times`) is this draft's M46-2 *consequence*; the pair
  reads best as cause (mine) and effect (landed). Mine names the contradiction that forced
  F4; the landed row counts the four freeze commits.
- Landed **M46-4** (`proxy-harm-recurrence`, command A 22/23 → 23/23) was **not run** by this
  seat; no confirmation or refutation is offered.
- Landed **R46-CL3** already states this draft's M46-3(a) as a wording defect; **P1** upgrades
  it from a code read to an artefact that scores `met_target true` with the full battery
  green. Landed **R46-CL2** (arm-vocabulary substring) is confirmed by code read
  (`any(t in r[arm_col].lower() for t in ARMS)`), not new.

## Receipts

`receipts.tsv` (R1–R14), `probe.out` (P1/P2), `census.out`, `F5-outpath-refusal.out`, and one
JSON per run, all in this seat directory. The driver (`driver.sh`) and the probe (`probe.py`) are copied here too, so
every value can be re-derived: `git show 65678df0:tools/round-46/{attest,registry,gate}.py`
into a scratch copy, `--freeze/--rev` as recorded, `--json-out` **inside the measured root**.
