# R44W2C2Vacuity — the C2 score reproduces exactly; the rubric is not uniformly falsifiable (h1 and all three targets free-pass their own statement) and every frozen-file entry's detector is unreachable in the scoring mode

**Seat** R44W2C2Vacuity · lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · measured
`55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac` · freeze `c48f8a4bfd449300c975668e59aae5b5538b6a84`
· base `c29360e3ba5381a5ab69e372d0d9577970f85018` · dispatch tip `c86ea508` · lane HEAD
observed during this seat `8bb1090af3fef64477c4337855e4347472db2701` (lane `refs/heads/main`,
unchanged; no `refs/vacuity` ref exists in the lane).

**Answer.**

1. **The scored C2 result is confirmed, not falsified.** From an independent `git clone --shared`
   of the lane, the frozen counter returns exit `0`, `entries 80`, `entries_evaluated 80`,
   `mismatches []`, `frozen_path_changed []`, `rubric_sha256_at_freeze == rubric_sha256_at_rev`
   (`e8cc0ded…`), `counter_sha256 == counter_sha256_at_freeze` (`085192ea…`), `met_target true`
   in 4.5 s. No vacuity in the *arithmetic* of the score.
2. **Vacuity is present in the entries, and it lands on the claim's own subject.** Of the six
   picks (three classes), **two are free passes at the measured revision**: `C2-h1` stays green
   with its whole subject section (`corpus/README.md` `## Coverage map`) deleted from REV —
   because it derives from `HYAKU_FREEZE` and emits `observed := derived`, so no REV mutation can
   move it; and the three **target** entries `C2-a1/a2/a4` each stay green when the human
   statement they were landed to repair is mutated, because their checks replace the statement
   with the appended `c2-correction-value` block. Of the six picks, **two are `free-pass`-class**
   (`a1`, `h1`); of the claim's three targets, **all three** (`a1`, `a2`, `a4`) free-pass their
   own statement.
3. **The four kills are real but only observable in a non-scoring configuration.** Every
   `SCORECARD.md`/`SHONEN.md` mutation exits `2 frozen_path_changed` before any entry is
   evaluated (`entries_evaluated 0`, no failing id). The reds for `c01`, `g1`, `b1`, `d14` appear
   only when the freeze walk is bypassed with the counter's own `--pre-freeze` flag (80 entries
   evaluated, same frozen counter bytes, derivation still at the real freeze). A mutation that
   reaches a frozen entry's statement is, by construction, the same edit that trips the gate.
4. I changed no claim, counter, rubric, frozen byte or production doc. Findings are below as
   numbered defects with `path:line`, the command, the exit code and the observed value.

---

## 1. Method

One clone, one work dir, absolute paths, everything under
`/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C2Vacuity/` (deleted before yield).

```bash
S=/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C2Vacuity
mkdir -p "$S/work" "$S/out"
git clone --shared --no-checkout --quiet \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/clone"
git -C "$S/clone" rev-parse --show-toplevel      # -> $S/clone  (asserted before any mutation)
git -C "$S/clone" rev-parse --verify '55bcce69^{commit}'
git -C "$S/clone" rev-parse --verify 'c48f8a4^{commit}'
```

Fixed inputs, verified by hash:

| object | value |
|---|---|
| `tools/round-44/c2-counter.py` | `085192ea6c3f3f4d67c58ce459ef06e1febd0b668dc367ccfbdd12661736c277` (identical at freeze and at 55bcce69; never modified) |
| `tools/round-44/c2-rubric.json` | `e8cc0dedd6b4bbfb323983018806de4b6ad59b80b1aeee111aa2d8ebf55e755e` (identical at freeze and at 55bcce69) |
| python / git | `/usr/bin/python3` 3.14.8 · git 2.56.0 |
| no tooling installed | pacman PAUSED; nothing fetched or upgraded for this seat |

**Mutant construction (no branch, index or work tree of the lane is touched).** For each probe I
read the target blob at REV (`git show 55bcce69:<path>`), applied exactly one textual mutation
(the driver asserts the occurrence count), then built a child commit with git plumbing only —
`read-tree` into a throwaway `GIT_INDEX_FILE`, `hash-object -w`, `update-index --cacheinfo`,
`write-tree`, `commit-tree -p 55bcce69`, `update-ref refs/vacuity/<name>` — inside `$S/clone`.
`git commit`, `git add`, `checkout`, `reset`, `stash` were not run anywhere; the lane has no
`refs/vacuity` and its HEAD is unchanged. The eleven mutant refs exist only in the scratch clone.

**Three run modes, same frozen counter bytes:**

| mode | argv | purpose |
|---|---|---|
| A — scored | `--rev <M> --freeze c48f8a4` | the claim's configuration (freeze walk enforced) |
| B — isolation | `--rev <M> --freeze c48f8a4 --pre-freeze` | the counter's own documented bypass: freeze violations are reported, not enforced; entries are still evaluated with `HYAKU_FREEZE=c48f8a4` and `HYAKU_REV=<M>` |
| F — rubric's fitness harness | `--rev <M> --freeze <M>` | `rev = freeze = the mutated commit` (the mode the rubric's `fitness.harness` declares) |

Baseline command (mode A with `M = 55bcce69`):

```bash
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c2-counter.py \
  --root "$S/clone" --rev 55bcce69 --freeze c48f8a4 \
  --work "$S/work" --json-out "$S/out/baseline.json"
# exit 0
```

## 2. Baseline reproduction at 55bcce69

| field | value |
|---|---|
| exit code | `0` |
| `entries` / `entries_evaluated` | `80` / `80` |
| `mismatches` / `mismatches_count` | `[]` / `0` |
| `frozen_path_changed` | `[]` |
| `rubric_source` | `freeze` |
| `rubric_sha256_at_freeze` = `…_at_rev` | `e8cc0dedd6b4bbfb323983018806de4b6ad59b80b1aeee111aa2d8ebf55e755e` |
| `counter_sha256` = `…_at_freeze` | `085192ea6c3f3f4d67c58ce459ef06e1febd0b668dc367ccfbdd12661736c277` |
| `met_target` / `claim_score` / `usable_as_claim_score` | `true` / `true` / `true` |
| wall / stdout sha256 | 4.61 s / `dd7c529bb6340c364854093937bce3d90ec980ebdea951263bb38dc52316a9b3` (receipt `artifacts/R44W2C2Vacuity/baseline.json`) |

`C2`'s recorded numbers are exact. Nothing in this report changes them.

## 3. The 6×2 grid (six picks, ≥3 classes)

Pick set: two count checks (`a1`, `h1`, `b1` — count over a correction block, a derived
invariant, a historical pin), one pointer check (`c01`), one append/expected-value check (`g1`),
one contains/cited-range check (`d14`). `a1` and `h1` carry a second mutation because the first
locates the value the check reads and the second locates the value the claim *names*.

**Mutation → result.** "Failing id" is the id in `mismatches` of that run.

| # | pick (entry) | class | mutation (one edit, at REV) | mode A (scored) | mode B (isolation) | verdict |
|---|---|---|---|---|---|---|
| 1a | `C2-a1-owned-coverage-count` | count / correction block | `SCORECARD.md` `c2-correction-value: 137/137` → `137/998` | exit **2**, `frozen_path_changed ["SCORECARD.md"]`, 0 entries evaluated — **no failing id** | exit **1**, failing id `C2-a1-owned-coverage-count`, `observed UNSUPPORTED:137/998` | killed (entry-level), unreachable in the scored mode |
| 1b | `C2-a1-owned-coverage-count` | count / human statement | `SCORECARD.md` `137/137 knowledge files mapped` → `137/998 knowledge files mapped` (the appended prose declaration) | exit **2**, `frozen_path_changed ["SCORECARD.md"]` | exit **0**, `mismatches []`, `observed 137/137` | **free-pass** |
| 2a | `C2-h1-readme-coverage-map-complete` | count / derived invariant | `corpus/README.md`: delete one coverage-map stem (`` `2026-10-13-asar-surface`, ``) | exit **0**, `mismatches []`, `frozen_path_changed []` | exit **0**, `mismatches []`, `observed 137/137; missing=[]; dangling=[]` | **free-pass** |
| 2b | `C2-h1-readme-coverage-map-complete` | count / derived invariant | `corpus/README.md`: delete the whole `## Coverage map` section | exit **0**, `mismatches []` | exit **0**, `mismatches []`, `observed 137/137; missing=[]; dangling=[]` | **free-pass** (subject destroyed, counter green) |
| 3 | `C2-c01-cap-pointer` | pointer | `SCORECARD.md` `.ufo/waves/luna-round-6/receipts/` → `…/-missing` | exit **2**, `frozen_path_changed ["SCORECARD.md"]` | exit **1**, failing id `C2-c01-cap-pointer`, `observed UNSUPPORTED:unresolved:.ufo/waves/luna-round-6/receipts/-missing` | killed (entry-level) |
| 4 | `C2-g1-planned-r34-to-35` | append / expected value | round-35 planned row: `after a steer` → `as first written` | exit **2**, `frozen_path_changed ["SCORECARD.md"]` | exit **1**, failing id `C2-g1-planned-r34-to-35`, `observed token-found` | killed (entry-level) |
| 5 | `C2-b1-owned-coverage-count-pin` | count / historical pin | `SCORECARD.md` `133/133 knowledge files mapped` → `133/997 knowledge files mapped` | exit **2**, `frozen_path_changed ["SCORECARD.md"]` | exit **1**, failing id `C2-b1-owned-coverage-count-pin`, `observed UNSUPPORTED:133/997` | killed — but see **D4**: the kill rests on reading the *REV* statement against a *pinned* derivation |
| 6 | `C2-d14-province-round39-core-row` | contains / cited range | `SHONEN.md` `` `PROVINCE.md:378-384` `` → `` `PROVINCE.md:378-999` `` | exit **2**, `frozen_path_changed ["SHONEN.md"]` | exit **1**, failing id `C2-d14-province-round39-core-row`, `observed UNSUPPORTED:range-out-of-file` | killed (entry-level) |

Mutant commits and hashes (source blob → mutant blob; mode-A and mode-B stdout):

| mutation | mutant | blob at REV → mutant | mode-A stdout sha256 | mode-B stdout sha256 |
|---|---|---|---|---|
| `a1-correction-value` | `c7a29d99b374` | `5828347b…6793` → `a69916bf…6dcf` | `15e792da…5b7d` (exit 2) | `84d2e5a5…8f50` (exit 1) |
| `a1-prose-value` | `86cf282c9603` | `5828347b…6793` → `fd201a4a…4a34` | `890157da…64bc` (exit 2) | `416a2e30…5125` (exit 0) |
| `h1-readme-map-stem` | `63b26e832d72` | `8d2ea86b…8dbd` → `bd97e643…530b` | `dcd37fd0…a0eb` (exit 0) | `f0a6d259…5fe6` (exit 0) |
| `h1-subject-section-deleted` | `90bd4ba9886a` | `9c65c258…5a7f` → `4f4d7aa0…9f31` | `b9915af7…71b7` (exit 0) | `d3ad21aa…6640` (exit 0) |
| `c01-pointer` | `cfd77fdeb478` | `5828347b…6793` → `9d61ea58…93ef` | `665670b6…bd74` (exit 2) | `39330a76…e01c` (exit 1) |
| `g1-planned-marker` | `0e828da7bde7` | `5828347b…6793` → `86067b17…603f` | `2e8034da…c168` (exit 2) | `47876791…627d` (exit 1) |
| `b1-pinned-occurrence` | `6b9d25c7ecc6` | `5828347b…6793` → `f6b1e29a…b81b` | `3926e158…b1fd` (exit 2) | `a6cda95c…3c89` (exit 1) |
| `d14-contains-range` | `4f7801c74ce4` | `3fc0bc67…4c43` → `ee031e52…c689` | `323be391…5d90` (exit 2) | `c53c8700…b3ff` (exit 1) |

Full 64-hex values are in `artifacts/R44W2C2Vacuity/grid.json` and `probes.json`.

**Grid reading, stated plainly.**

- `h1` is green under *every* mutation of REV, including deletion of the section it is named
  after. Its check reads `corpus/README.md`, `corpus/knowledge/**` and `SKILL.md` **at
  `HYAKU_FREEZE`** and emits `derived` as both `observed` and `derived`; the rubric literal is
  the only other input. The measured revision is not an input. (Mode A returns `exit 0` and —
  because `frozen_path_changed` is empty — `met_target true` on a tree with no coverage map.)
- `a1`, `a2`, `a4` — the three claim targets — each free-pass a mutation of the statement they
  were landed to repair (measured for all three, below). Their check takes
  `stated = correction(STMT, EID)` whenever the appended block exists; the row is dead text.
- `c01`, `g1`, `b1`, `d14` genuinely detect their mutation, but only in mode B; in mode A the
  frozen-path gate returns before `for entry in entries:` (`tools/round-44/c2-counter.py:1199`
  vs `:1228`), so the entry is never executed. 77 of 80 entries live on the two frozen files
  (`SCORECARD.md` 55, `SHONEN.md` 22) and share that property.

## 4. Extra probes (target coverage, witness reproduction)

| probe | mutation | mode A | mode B | observed of the pick |
|---|---|---|---|---|
| `a2-prose-value` (target) | `SCORECARD.md` `20/20 queue-drain rule blocks` → `20/99 …` | exit 2, `frozen ["SCORECARD.md"]` | exit **1**, failing id **`C2-b2-owned-depth-count-pin`** (not a2) | `C2-a2` = `21/21` → **free-pass**; `C2-b2` = `UNSUPPORTED:20/99` |
| `a4-prose-value` (target) | `SCORECARD.md` `craft section `SKILL.md:81-449`` → `81-448` | exit 2, `frozen ["SCORECARD.md"]` | exit **1**, failing id **`C2-b9-owned-depth-craft-range-observable-pin`** (not a4) | `C2-a4` = `81-543` → **free-pass**; `C2-b9` = `UNSUPPORTED:…` |
| `h1-witness-delete-file` (the rubric's own h1 witness) | delete `corpus/knowledge/2026-10-13-asar-surface.md` | exit **1**, failing id **`C2-h2-readme-knowledge-entries-resolve`** | (run in mode F instead) | `C2-h1` = `137/137; missing=[]; dangling=[]` unchanged |
| same, mode F | `rev = freeze = mutant` | — | exit 1, ids `[C2-h1…, C2-h2…]` | `C2-h1` = `137/137; missing=[]; dangling=['2026-10-13-asar-surface']` — the witness reproduces **only** when the freeze is redefined to the mutant |

Receipts: `artifacts/R44W2C2Vacuity/{a2prose,extras,h1delete}.json`; mode-A/mode-B stdout sha256
for each row are in those files.

Also measured, for the fitness claim: running `C2-a1`'s own payload at the base census
(`REV=BASE`, `FREEZE=c48f8a4`) yields `observed "UNSUPPORTED:133/133"`, `derived "137/137"` —
i.e. the entry is **already mismatching before any mutation**. The rubric's recorded `a1`
witness (`observed UNSUPPORTED:133/999`) is therefore not evidence that the mutation caused the
failure; the entry fails identically without it.

## 5. Findings — numbered defects

**D1 — the frozen counter does not implement the claim's B2 clause, and 71/80 entries would be
exit 2 under it.** `plans/round-44-claims.md:213-216` makes B2 mandatory ("`asserted` must be a
byte substring of the BASE blob's `line_at_base` … else exit 2 `asserted_not_in_base_line`").
The frozen counter never reads `line_at_base` or `line_sha256` and has no such error path:
`grep -c "line_at_base\|line_sha256\|asserted_not_in_base_line" tools/round-44/c2-counter.py`
→ `0`; the entry parse at `tools/round-44/c2-counter.py:374-401` accepts `asserted` as any JSON
value. Measured over all 80 entries against the BASE blobs (line hashes recomputed with sha256
of the line bytes without the newline): `line_sha256` mismatches `0`, but
**`asserted`-not-substring-of-`line_at_base` = 71/80**, including all three targets —
`C2-a1` asserted `137/137` vs base line `133/133`; `C2-a2` `21/21` vs `20/20`; `C2-a4` `81-543`
vs `81-449` (`tools/round-44/c2-rubric.json:388`, `:438`, `:538`). Exact-command evidence:
`artifacts/R44W2C2Vacuity/` (B2 audit run from `python3` on `c2-rubric.json` + `git show
c29360e3:<file>`), exit `0`, observed `71` offending entries. The frozen claim text and the
frozen instrument describe different rubrics; the record should say so rather than present the
claim as the thing measured.

**D2 — the three target entries pass by not checking the statement they repair
(note-over-value).** `tools/round-44/c2-rubric.json:388` (`C2-a1`), `:438` (`C2-a2`), `:538`
(`C2-a4`): each check computes `stated` from the `## Owned axes` row and then overrides it with
`eff = correction(STMT, EID); if eff is not None: stated = eff` (payload text, copied verbatim
into `artifacts/R44W2C2Vacuity/cmd_C2-a1-owned-coverage-count.py` and `cmd_a4.py`). Mutation of
the row's number leaves the entry match (`137/137` observed after a mutated row; `21/21`;
`81-543`); only the appended `c2-correction-value` line is load-bearing. Measured: mode B exit
`0`, `mismatches []` for `a1-prose-value`; mode B failing id `C2-b2-…` (not `a2`) for
`a2-prose-value`; mode B failing id `C2-b9-…` (not `a4`) for `a4-prose-value`. This is stronger
than D-17 ("the old text stands"): the counter stops counting the statement that the claim's own
intro says C2 counts ("C2 counts self-assessment mismatches between the lane's own statements and
committed repo state", `plans/round-44-claims.md:11-13`).

**D3 — `C2-h1` is inert at the measured revision and is pinned contrary to the claim text.**
`tools/round-44/c2-rubric.json:4563` region: `"pin": "HYAKU_FREEZE"`, `asserted "137/137;
missing=[]; dangling=[]"`; its payload ends `A=command_a(REV2); derived="…"; emit(derived,
derived)` (`artifacts/…/cmd_C2-h1-readme-coverage-map-complete.py`), so `observed := derived`
always. `plans/round-44-claims.md:234-237` says README is not byte-frozen and "its checks
re-derive current rows at REV"; h1 does not. Measured: deleting the whole `## Coverage map`
section at REV yields exit `0`, `mismatches []` in **both** modes, `observed "137/137;
missing=[]; dangling=[]"`; the rubric's own witness (delete a knowledge file) is invisible to
h1 at REV (exit 0 for h1; h2 reds instead) and reproduces only with `rev = freeze = mutant`.
The asserted literal is also not in the subject (`137/137` occurs 0 times in
`corpus/README.md` at 55bcce69), which is why D1's clause cannot hold for this entry.

**D4 — pinned entries compare the REV statement against the pinned derivation, so a legitimate
future row refresh is a false red.** `C2-b1`'s payload reads `STMT = show('SCORECARD.md', REV)`
and derives at the literal `REV2 = 'e1c83313'`
(`artifacts/…/cmd_C2-b1-owned-coverage-count-pin.py`); `C2-b2`/`C2-b3`/`C2-b9` use the same
shape. `plans/round-44-claims.md:218-220` requires the opposite ("`evaluate_at = pin` for
historical count/receipt assertions … never compare a pinned historical value to the current
tree"). Measured: mutating the current coverage row reds `C2-b1` (`UNSUPPORTED:133/997`,
mode B); mutating the current depth row's craft range reds `C2-b9`
(`UNSUPPORTED:81-448`, mode B) while `C2-a4`, the entry that is supposed to be checked, stays
green. Today the rows happen to still equal their pins, so nothing reds; the first round that
refreshes `## Owned axes` turns every `b*` entry red on history that has not changed.

**D5 — the rubric's fitness claim (80/80 "fails_as_required") is measured in a mode that
redefines the freeze, and at 55bcce69 that mode is contaminated.** `tools/round-44/c2-rubric.json:213`
declares the harness as "rev = freeze = the mutated commit". Run that way against a child of
55bcce69, every one of the seven probes red two entries **unconditionally** —
`C2-a1-owned-coverage-count` and `C2-h1-readme-coverage-map-complete` — because
`HYAKU_FREEZE` then points at a tree that already contains C1's post-freeze knowledge entry
(138 files) while the rubric asserts the freeze-tree value 137 (`probes.json`, `fitness_mode`
for all seven). So the `a1` witness at the base is non-discriminating (D1's last paragraph,
measured `UNSUPPORTED:133/133` pre-mutation), and the same harness at the measured revision
cannot isolate the probe's effect. The fitness gate exists, but its recorded witness does not
show what it claims for the target entries or for h1.

**D6 — entry-level detection is unreachable in the scoring configuration (ordering, not
vacuity).** `tools/round-44/c2-counter.py:1199` returns `EXIT_CANT` on
`frozen_path_changed` before the entry loop at `:1228`. 77/80 entries name a frozen file
(`SCORECARD.md` 55, `SHONEN.md` 22; `frozen_paths` at `c2-rubric.json`), so **any** mutation of
their statement produces exit `2`, `entries_evaluated 0`, no failing id — measured for five
`SCORECARD.md` probes and one `SHONEN.md` probe. The entry reds this report records required
`--pre-freeze`. The only scored-configuration red I produced is `C2-h2` (knowledge-file
deletion), which reads REV. The claim's "fitness gate … mutate the asserted value → expect
mismatch" is thus satisfied only in a mode the score never uses; the record should state that,
and a round-45 design should either put the statement check on a non-frozen copy or drop the
per-entry fitness claim.

## 6. Verdict on R44-C2 as recorded

| recorded statement (lesson / rubric) | verdict |
|---|---|
| "`entries_evaluated 80`, `mismatches []`, `frozen_path_changed []`, exit 0" at 55bcce69 | **confirmed** (exact reproduction; §2) |
| rubric frozen and unmodified freeze→REV | **confirmed** (`e8cc0ded…` both sides) |
| "80 entries witnessed, 80 fails_as_required, not_demonstrated []" | **not established**: h1 cannot be falsified by any REV edit; the three targets are not falsified by mutating their statement; the witness mode carries unconditional collateral at 55bcce69 (D3, D5) |
| "calibration: zero mismatches over the rubric" | **true as counted**, but 3 of the 80 counted entries are target entries whose statement is no longer the checked object (D2), and the claim's mandatory B2 admissibility clause is not implemented (D1) |
| "C2 STOPS if the frozen census finds zero mismatches among the three named entries at BASE" | the base census does find mismatches (`a1` measured `UNSUPPORTED:133/133`; §4), so the stop was not triggered — consistent |

## 7. Limits of this seat

- One mutation per entry, on one scratch clone; I did not enumerate all 80 entries, so the count
  of free passes is a lower bound (measured: 2 of 6 picks, 3 of the 3 targets).
- `a2`/`a4`'s payloads share a1's shape by construction (identical `stated`/`eff` code); I
  measured all three statement mutations, so that part is not inference.
- The `--pre-freeze` mode is the counter's documented flag; I did not patch, re-freeze or
  re-author anything, so mode-B results are properties of the frozen bytes.
- No claim about C1, M44-2 or the frozen-path preflight; those belong to other wave-2 seats.
- Machine checks were run only as mutation probes; no build/lint/format pass was in scope.

## 8. Receipts, lane integrity, scratch

- Receipts: `artifacts/R44W2C2Vacuity/{baseline,probes,grid,extras,h1delete,a2prose}.json`
  (each carries `argv`, `exit_code`, `wall_seconds`, `stdout_sha256`, and per-entry `observed`),
  plus the seven extracted check payloads and the three drivers (`drive.py`, `drive2.py`,
  `drive3.py`).
- Lane integrity: lane HEAD `8bb1090af3fef64477c4337855e4347472db2701` = `refs/heads/main`
  before and after; `git for-each-ref refs/vacuity` in the lane → empty (the ten mutant refs
  live in `$S/clone` only); no lane index, work tree, claim, counter, rubric or frozen byte
  touched; no fleet-root file written.
- Scratch: `/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C2Vacuity/` (clone, work dirs, mutant
  trees) deleted before yield; no `/tmp` evidence path is cited.
- Tooling: none installed or upgraded (pacman paused; no `uv`/`npx` need arose).
