# R39W2C1AxisFit — post-landing attack on R39-C1 as a *coverage* claim

**Verdict: DEFECTS FOUND.** The frozen predicate is met and I could not falsify it: I re-derived
`carriers_matched == 6`, every binding true, exit 0 at `6fdaf4f1` from a clean `--shared` clone, and I
independently re-ran REA 6.5.0 on **all six** committed carriers and reproduced every semantic clause of
the receipts. The defects are in what the landing *says moved*: (D1) the coverage move is not recorded
anywhere the lane scores it — **no round-39 commit touches `SCORECARD.md` or `LOG.md`**, and the
coverage row still reads `126/126` while the landing makes it `128/128`; (D2) the surface the claim
names as moved, `PROVINCE.md:156-157`, is **byte-identical** to the base — the supersession exists only
as a note 226 lines below it, so two live sentences in `PROVINCE.md` still assert BE v4 is Frontier;
(D3) the BE entry does not cite the lane's own prior holding for the symlink rule. No overclaim of AVM,
vendor-mangled or "every" survived the sweep. Claim-by-clause table and exact pointers below.

## 0. What I read and ran (all read-only; scratch removed)

- Frozen rule `git show 8fcda41c:plans/round-39-claims.md`; prompt §6 item 9;
  `git log a2f64e1d..main` (6 commits, tip `e40a25df` at the time of writing).
- Scratch `S=/fast/scratch/hyaku/kaidoku-r39/R39W2C1AxisFit`; `git clone -q --shared <lane> $S/clone`;
  a scratch clone is the only VCS object I wrote to, and I committed nothing anywhere.
- Counter, from that clone (`TMPDIR=$S`):

  ```
  python3 -I -B tools/round-39/c1-counter.py --root $S/clone \
    --rev 6fdaf4f162aff156fcef0e52998a5469c64fd6f0 \
    --freeze 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b \
    --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
    --json-out $S/c1-at-6fdaf4f1.json        # exit 0, carriers_matched 6, met_target true, frozen_path_changed []
  ```

  same call with `--rev 8fcda41c…` → exit **1**, `carriers_matched 0`, `met_target false`, and
  `coverage_map_row/entry_present/frontier_note/province_core_*` all false (the claim's "command that
  shows it unmoved" reproduces). `--selftest --pkg65 …` → exit 0,
  `cases 33, green_ok 1, red_ok 32, failures []`.
- **Independent provenance (the counter cannot do this, and the freeze says so):** six fresh
  `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output <committed carrier> <fresh outdir>`
  runs under `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob`, outdirs under `$S/reaout/<K>`. Exit 0 for all
  six; stderr empty. Result: handler `squashfs_v4_be`, 0 failed chunks, published file set **and sha256**
  identical to the committed `after.json` **and** to the frozen `oracle.tsv` (5/3/4/4/10/8 rows, 0
  mismatches), gap sets identical, subject digest identical to the `carriers.json` pin
  (`artifacts/…/six-carrier-rerun.md`, per-carrier `K*-rerun.json`). Evidence ids differ from the
  receipts only because `parameters.output_directory` is inside the hashed projection — expected, and the
  same property that makes a byte-copied receipt un-recomputable.
- Byte checks: all six carriers start `73 71 73 68` (the big-endian `sqsh` magic); superblock
  compression id (offset 20, big-endian) = 1 (gzip) for K1–K5, **4 (xz) for K6**, and K6's bytes hold **4** xz
  stream magics `fd 37 7a 58 5a 00` — the xz leg is real decoding, not a relabelled LZMA2 (M39-7's
  failure mode).
- Local producer source `…/uv/tools/unblob/…/handlers/filesystem/squashfs.py:40-48`: `case Endian.BIG, 4:`
  sets `executable = "sasquatch-v4be"` and appends `-be` **only** when `not (bytes_used == mkfs_time)`.
  The Core row's "`sasquatch-v4be -be` … (AVM marker excepted)" is exact, not a shortcut.
- `~/.local/bin/unblob` is a symlink to `…/uv/tools/unblob/bin/unblob` (same sha256
  `0ce7b624…1d09`, both `26.6.4`), so the row's `REA_UNBLOB_COMMAND=~/.local/bin/unblob` and the run
  records' uv-tools path name the same binary. Not a defect.

## 1. Did the landing move PROVINCE ground Frontier → Core?

Mechanically yes, in the lane's established append-only form: `6fdaf4f1` adds 8 lines at
`PROVINCE.md:378-384` — `## Round-39 additions to Core` with one `squashfs_v4_be` row (`:382`) and a
`Round-39 frontier note` (`:384`); `corpus/README.md` gains a coverage-map row (`:93`, **Core**), a
knowledge-index row (`:203`) and a Frontier bullet (`:245`, "standard big-endian v4 is **Core** …
superseding the round-38 line above").

**Counterexample (D2).** The claim's own sentence, "Surface moved: … bullet **sasquatch**
(`PROVINCE.md:156-157`)", is false at the measured revision: `PROVINCE.md:156-158` hashes identically at
`a2f64e1d` and `52b0eb29` (`sha256 d9ddd81e…a04b2`, `artifacts/…/province-identity.txt`), and so does the
round-38 note at `:376` (`6b686a4d…082f`) whose last sentence is still "**Big-endian SquashFS stays
Frontier.**" A reader at `### Round-4 frontier (post-unlock)` therefore still reads "big-endian/AVM stays
here … Round 38: … not promoted"; the only supersession is at `:384`, after the Core table, and it is
what points *back* at `:156-157`. Rounds 36 and 38 each edited that same bullet inline (its bracketed
`[2026-10-26: …]` text is theirs), and the round-38 closure credited freshness precisely because the note
landed at **`:157` and `:376`**, not only at the file's end. Round 39 annotated neither. The claim's
predicate asks only for "a round-39 frontier note [that] supersedes the big-endian part", so the claim
passes as frozen — but the coverage *surface statement* overstates what the landing did, and `PROVINCE.md`
now carries two live falsified sentences with no forward pointer at their site. `corpus/README.md` got
this right (inline bullet at `:245`), which makes the PROVINCE omission an inconsistency inside one
commit, not a convention.

Not defects, checked: the round-36 row at `:372` still says `sasquatch-v4be` "… unmeasured" — that stale
aside was already superseded by the dated note at `:376` in round 38 and the new note re-supersedes it;
the row text is not rewritten by convention (same as rounds 31/32). The note at `:384` names the bullet by
line, which is the R36-CL2 repair standard.

## 2. Is anything the round-38 closure required still missing?

Nothing on the routed list, and the two Q gates now exist:

| routed | round-39 discharge | my check |
|---|---|---|
| R38-CL1 false absence sweep | QUALITY 82 + `tools/round-39/absence-sweep.py` (gate, `--selftest` 18 cases) + lesson `## Corrections to round 38` (both tsvs re-stated with size/sha256) | `corpus/QUALITY.md:88` present; correction text names the true paths |
| R38-CL2 unregistered gates | `SKILL.md:1327+` `### Round-35/37/38/39 instrument registry`, incl. rows for `round-38/{freeze-drift,intended-doc,registry-immutable}` and all round-39 tools; `--selftest` added to the three round-38 tools | ran all three in the clone: 8/8, 9/9, 5/5 PASS, exit 0 (`artifacts/…/r38-gate-selftests.txt`) |
| R38-CL3 overstatement | report-level, not a lane file; nothing to check here | — |
| R38-CL4 "which verdict blocks a score" | `plans/round-39-claims.md` §Freeze-integrity rule: any touch of a frozen path in `FREEZE..REV` → counter exit 2, restore does not un-block | counter implements it (`frozen_path_changed`), and my run shows `[]` for `8fcda41c..6fdaf4f1` on plans/counters/carriers/oracles; the only changed frozen-listed paths are the six `corpus/evidence/round-39/c1/K*/{after,run}.json`, which are the receipts the predicate *requires* to be added after the freeze |

**Missing, but from the round contract rather than the r38 spot-check (D1):** prompt §2 item 5 requires
per-claim "score delta, evidence pointer, counting command, and measured commit" in `SCORECARD.md` and the
motivating evidence appended to `LOG.md`.

```
git log --oneline a2f64e1d..main -- SCORECARD.md LOG.md      # → empty, exit 0
grep -c 'Round 39\|round-39\|Round-39' SCORECARD.md          # → 0
grep -c 'round-39\|Round 39\|Round-39' LOG.md                # → 0
```

So the coverage axis move has no SCORECARD round section at all (every other measured round has one;
`:3385` round 36, `:3399` round 38), and the coverage row (`SCORECARD.md:23`) still reads "**126/126**
knowledge files mapped after the round-38 landing". Re-derived with the lane's own observable
(knowledge `.md` files vs backticked `2026-10-XX*` stems in `corpus/README.md`):
`a2f64e1d → 126/126`, `6fdaf4f1 → 128/128`, `52b0eb29 → 128/128`, `unmapped []`
(`artifacts/…/coverage-proxy.txt`). The landing moved that proxy by two and recorded neither the delta nor
the commit; a closure reading `SCORECARD.md` alone cannot see a coverage change this round. The frozen
predicate has no SCORECARD clause, so this is a landing/bookkeeping defect, not a predicate miss — but it
is the one omission that makes the round's *axis* claim unreadable in the lane's own scorecard.

## 3. Is the claim re-scoring a rule the lane already held (prompt §6 item 9)?

**Partly yes, in attribution; no, in the axis label.** The label is right: item 9's own test — "a coverage
claim names the surface it moves (frontier → core …) and the command that would show it unmoved" — is met
verbatim, and the round-38 closure used the same unit ("no Frontier → Core move" was why coverage did not
move). The warning clause bites only on *content*, and the freeze does bind new content: the six-carrier
spec, the xz leg (K6, superblock id 4), and symlink cardinality (one carrier with two in-tree links).

The residual is the **rule**, not the carriers. "`unpublished-entry` gaps on symlinks are not extraction
failure; the right test is gaps == in-tree link set" was already held by this lane in two places before
round 39: `SKILL.md:1267` (round-36 LE craft table: symlinks "retained as metadata only … **Not** a
sasquatch failure and **not** blocked recursion") and the round-38 BE entry's §Symlinks. The round-39 BE
entry (`corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md:32-35`) credits only "round 38's stop" and
cites S122; it does **not** name `SKILL.md:1267` (**D3**). That is an attribution gap, not a false
sentence — and wave-1's proposed disclosure sentence (`w1/R39C1AxisFit.md` (a), "the in-tree-symlink
retention is the lane's prior holding") was **not** adopted into the freeze, which is allowed after the
freeze but should be visible somewhere in the round's prose. The honest reading of the coverage delta is
therefore: **1 new map row + 2 genuinely new carriers (xz; UTF-8/space names; two in-tree links at once);
4 of 6 scored carriers are the round-38 set re-measured under a corrected rule** — which the claims file
does disclose ("K1–K4 = the round-38 carriers"). Modest, real, not a re-score of a held *rule*.

## 4. Overclaim sweep (AVM / vendor-mangled / "every")

| statement | where | bounded? |
|---|---|---|
| "publishes **every** oracle regular file on six frozen BE v4 carriers (5,3,4,4,10,8)" | README `:93`, PROVINCE `:382` | yes — enumerates per carrier and bounds to the oracle |
| "on six frozen carriers **every** regular file of an independent oracle is published" | entry `:9-10` | yes — carrier count named, oracle named |
| "gaps exactly one `unpublished-entry` per in-tree symlink … escaping links removed" | README `:93`, PROVINCE `:382` | yes — verified (4 in-tree, 4 escaping; 0 escaping published, 0 escaping gap) |
| "(AVM marker excepted)" / "AVM-BE bodies and vendor-mangled images stay Frontier" | PROVINCE `:382,:384`, README `:93,:245`, entry `## Limits` | yes, and the producer source confirms the exception |
| "no failed chunk" | PROVINCE `:382` | yes — 0 failing chunks on all six, re-run |

No AVM body, vendor-mangled image, extracted program or LE claim rides on the new Core row. Two
presentation nits only: the Core row does not pin the `sasquatch-v4be` binary by sha256 (round-36's LE row
pins `ad02d27a…`), and S121 (sasquatch source, opened this round) is not cited by the entry, so the BE
binary's identity rests on a path+version string.

## 5. Counter reachability (reproduced, then closed)

The freeze's disclosed limit is real and I reproduced it: `controls/ctl-c1-3.json` —
`carriers_matched 6`, `met_target false`, false bindings `["frontier_note"]`, `counter_exit 1`,
`verdict "unexpected-exit"`. A receipt set fabricated and re-minted under the 6.5.0 rule therefore clears
every receipt-only clause and fails only on documentation. That limit is now **closed for the six
committed carriers** by §0's six independent re-runs, which is the provenance duty the freeze assigns to
wave 2 — not a counter result.

## 6. Impacted axes

- **coverage:** claim predicate met (6/6, all bindings, provenance re-derived for all six); the move is
  real but unrecorded in `SCORECARD.md`/`LOG.md` and under-edited in `PROVINCE.md`. Net: improved, thin,
  and not auditable from the scorecard until D1 is fixed.
- **depth:** untouched by C1 (C2's surface). No harm.
- **calibration:** **harmed** in the narrow sense that the lane's self-assessment surfaces now understate
  observed state (`SCORECARD.md:23` says 126/126, observed 128/128), which is exactly what QUALITY 81 /
  the round-38 pointer claim exist to prevent. Fixable without a new claim.
- **freshness/legibility:** `PROVINCE.md:156-158` and `:376` carry falsified sentences with no inline
  supersession; `corpus/README.md` does not.

## 7. Smallest safe corrections (do not change the frozen predicate)

1. **D1** — add `## Round 39` to `SCORECARD.md` (coverage row restated `126/126 → 128/128`, per claim:
   score delta, `c1-at-6fdaf4f1.json` pointer, the counting command, measured commit `6fdaf4f1`) and one
   `LOG.md` entry naming the landed surface. This is prompt §2 item 5 work that was skipped, not a claim
   change.
2. **D2** — append to the `- **sasquatch** —` bullet at `PROVINCE.md:156-158`, in the style rounds 36/38
   already used there: `[2026-10-26 Round 39: standard BE v4 is Core — see ## Round-39 additions to Core
   (2026-10-26-r39-be-squashfs-v4-core); AVM-BE and vendor-mangled stay here.]`, and add
   `(superseded round 39)` to the last sentence of `:376`. Until that lands, a reader of the Frontier
   section gets the round-38 verdict and no pointer.
3. **D3** — in the BE entry's `**Symlink rule.**` paragraph, add "(prior holding for LE: `SKILL.md:1267`;
   round-38 BE entry §Symlinks)" so the rule is attributed to the craft table it came from.
4. Optional, cheap: pin `sasquatch-v4be`'s sha256 in the Core row's Ports/keys cell (as round 36 did for
   the LE binary) and cite S121 in the entry for `-be`.

## 8. Artifacts (`.ufo/waves/round-39/w2/artifacts/R39W2C1AxisFit/`)

| file | what it proves |
|---|---|
| `c1-at-6fdaf4f1.json`, `c1-at-freeze.json` | my own counter receipts: 6/6 met at the landing, 0/6 exit 1 at the freeze |
| `c1-selftest.txt` | `cases 33, green_ok 1, red_ok 32, failures []`, exit 0 |
| `six-carrier-rerun.md`, `K{1..6}-rerun.json` | independent REA 6.5.0 re-runs of all six committed carriers: handler, 0 failed chunks, file set+sha256, gaps, subject digest all reproduce |
| `escaping-not-published.txt` | per symlink row from `symlinks.tsv`: escaping → not published, no gap; in-tree → gap, not published (8/8 rows OK) |
| `province-identity.txt` | `PROVINCE.md:156-158`, `:372`, `:374`, `:376` hash-identical base vs `52b0eb29`; `:378-384` differ |
| `coverage-proxy.txt` | 126/126 → 128/128 mapped, `unmapped []`, vs the stale SCORECARD row |
| `scorecard-log.txt` | `git log a2f64e1d..main -- SCORECARD.md LOG.md` empty; 0 mentions of round 39 in either |
| `r38-gate-selftests.txt` | round-38 gate self-tests 8/8, 9/9, 5/5, exit 0 (R38-CL2 discharge) |

## 9. Limits of this report

- My re-runs use this host's unblob 26.6.4 / `sasquatch-v4be` 4.5.1 / REA 6.5.0 and the committed
  carriers. They prove each receipt is a real run's output over those bytes; they do not prove the run
  happened before the freeze commit — only commit order and the hashed `parameters` can speak to that.
- I did not dispatch, message peers, or run C2's tools; C1 only.
- Tool installs: none (all binaries already present; `npx -y rea-agents@6.5.0` resolved the cached
  package). SEAT ↔ seat name: `R39W2C1AxisFit`.
- Scratch `/fast/scratch/hyaku/kaidoku-r39/R39W2C1AxisFit` removed after the artifacts were copied.
