# R44W2ScoutDebt — debt-ledger exit check (round 44, wave 2)

**Seat:** `R44W2ScoutDebt`. **Lane:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
**Ledger (not rewritten):** `.ufo/waves/round-44/w1/R44Debt.md` (28 rows, draft-era).
**Record under test:** `corpus/lessons/round-44.md:77-91` (carried-debt paragraph).
**Pins:** base `c29360e3ba5381a5ab69e372d0d9577970f85018`; freeze `c48f8a4bfd449300c975668e59aae5b5538b6a84`; measured rev `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`.

State rule used here (the L1 records exits; this file does not edit the ledger):

- `closed-this-round` — every conjunct of that row's `future-round-exit-condition` is evidenced by a committed artifact this round.
- `exercised` — at least one conjunct, or a frozen amendment/control aimed at the exit, is evidenced, and the exit as written did not fire. Do not close the row.
- `open` — no exit conjunct fired. Restating the limit in the lesson is not exercise.

Counts: **1 closed-this-round, 9 exercised, 18 open.** The lesson's carried-debt sentence is wrong on two ids (defects 1 and 2). It is right to leave the other 26 unclosed.

## Table

| id | state | evidence |
|---|---|---|
| D-01 | open | Exit wants a scored carrier with a directory, a multi-block member, and a duplicate pair. `tools/round-44/carriers.json` `carriers` is still `['v1le','v1be','v2le','v2be']`, member sizes `[6,7,7]`, `[6,7,7]`, `[7,7,7,7]`, `[7,7,7,7]`. `PROVINCE.md:424` is "measured, not promoted" on four fixtures; v1/v2 stay Frontier (`PROVINCE.md:430`). The until-then wording holds; the exit did not fire. |
| D-02 | open | No published image is in `carriers.json`. Claims `:189-190` and the knowledge entry still say the OpenWrt White Russian URL 404'd and the DD-WRT listing was empty *this round*. No committed 200-listing receipt plus a standing "no published v1/v2 carrier exists" close was found under `.ufo/waves/round-44/`. |
| D-03 | open | Claims `:191` and `PROVINCE.md:430` keep `squashfs_v2_nonstandard` Frontier. No producer-independent v2ns census. |
| D-04 | open | Same frontier sentence keeps `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, `squashfs_v4_broadcom` Frontier. No per-handler oracle pair was added. |
| D-05 | open | gzip v3 stays in that Frontier list. No gzip-v3 REA score. |
| D-06 | open | LE AVM, AVM kernels, and depth>1 stay in that Frontier list. No separate receipt for any of the three. |
| D-07 | exercised | Exit is an AND. Conjunct 2 fired: at the freeze, `git grep -c -e 'is uncompressed' -e 'oracle property' c48f8a4b -- plans/round-44-claims.md` prints nothing (no match). Claims `:37-43` bind `zlib(gzip)` from the inode-table block and say `file(1)` mislabels both BE images. Conjunct 1 did not: the four carriers are still the 6–7 byte members above; nothing with a multi-block member, a fragment-boundary file, and a duplicate pair was scored. Do not close. |
| D-08 | exercised | `tools/round-44/c1-counter.py:360-364` sets `structural['depth-limited']=0` and says the draft allowance is gone. No symlink or device carrier was scored (census sizes above are regular files only), and the replacement is not a row-identity binding to an oracle entry. The positive-witness half of the exit did not fire. |
| D-09 | open | `corpus/evidence/round-44/oracle/manifest.json` `source.grounds` still says the S138 trees are "NOT handler code, NOT extractor behaviour, NOT a C1 carrier" (unblob `26.6.4` commit `1fcc7a0a…`). The counter's oracle is the frozen unsquashfs census (`c1-counter.py:63-66`), not a demonstrated fixture-author distinct from sasquatch, and not a per-carrier `7z` oracle. Lesson `:82-83` correctly leaves this open. |
| D-10 | exercised | Scored ids are still four. The manifest has 8 `v2.1` file rows and **no** `unbound` key (`manifest_has_unbound_key False`; `git grep unbound` on the freeze blob prints nothing). Claims `:25-27` and `:155-156` and `c1-counter.py:913-914` exclude v2.1 in prose. The exit's artifact is `unbound: true` on the manifest, or a scored v2.1 carrier. Neither exists. Do not close. |
| D-11 | exercised | `file(1)` is not the probe: `layout_probe` (`c1-counter.py:1070-1168`) compares magic, `s_major`, `s_minor`, and compression class to the frozen carrier entry; compression comes from the inode-table metadata block (`0x78` zlib), and `:52` says `file(1)` is never a compression oracle. CTL-C1-5 reds bad magic / swapped `s_major` / swapped `s_minor` (`.ufo/waves/round-44/w1/artifacts/R44C1Controls/controls/c5/receipt.json`, title "mutated superbytes", `met_target false`). The exit also requires a live `unsquashfs -s` assertion and a mutated compression-id outside the frozen set. v1/v2 has no compression-id field, and the probe never calls `unsquashfs`. Do not close. |
| D-12 | exercised | CTL-C1-POS reached `met_target true`, `carriers_matched 4`, exit 0 on counter sha256 `9f2cc140e1fa7875bcd9dc80ce2ff5a1006e8ee73c7e1207580f88a97ffea993`, which equals `l1/c1-score-at-55bcce69.json` `counter_sha256`. That run's freeze field is sandbox `7883cacd`, not `c48f8a4b`, and the receipts are this round's scratch captures, not a prior round's frozen after-receipt. Claims `:161-164` still say the data procedure is after the freeze and seats never run `c1-run.sh`. The named exit did not fire. |
| D-13 | open | Claims `:193-194` now restate R40-CL2 / D-13 (projection, not authorship). That is the disclosure, not a provenance-bearing receipt and not a decision that provenance is out of scope. Lesson routed defect R44-CL3 says the same hole is not closed. |
| D-14 | open | Claims `:106` and `:195` still call the four bins round-42 held-out inputs and state the consequence. No fresh held-out set was designated. The "until then, no held-out language" constraint is still being breached by the frozen text; the exit did not fire. |
| D-15 | open | The frozen rubric scores 80 entries and drops 10 (`c2-rubric.json` `dropped` length 10). `scope.excluded_note` (`:108`) still says a mismatch on an excluded id is a lesson defect, not counter ground. No outside class was added to the scored set. |
| D-16 | exercised | Rubric rule `R4_two_sources` (`c2-rubric.json:161`) requires a second git-object source, and `mutation-witness.json` has 80/80 `fails-as-required`. There is no per-check "proves / does not prove" field, and no seeded control whose only job is the semantic arm the exit names (pointer contains the claim id; count from the named file set). Do not close. |
| D-17 | open | `R5_append_only_repair` and `expected_edits.SCORECARD.md` (`c2-rubric.json:162`, `:179-197`) are still an appended correction. The original owned-axes lines are not marked superseded in place. |
| D-18 | exercised | Branch 1 failed: the relaxation was not deleted (`expected_edits` still binds `SCORECARD.md`). Branch 2 is only partly met. `w1/artifacts/R44C2Rubric/receipts/control-seeded-in-place-edit.json` exits **2** with `frozen_path_changed ["SCORECARD.md"]` and `bound_edit_violation` / `not_append_only`, but `counter_sha256` is null, `rubric_source` is `file`, and its freeze field is the **base** `c29360e3`, not `c48f8a4b`. The measured-rev receipt does print the allowed scope: `l1/c2-score-at-55bcce69.json:6511-6516` `SCORECARD.md` `bound_edit_applied`, `appended_lines` 8. That is not yet "a frozen control". Do not close. |
| D-19 | closed-this-round | Exit shape is mismatches > 0 at BASE and 0 at REV on the frozen rubric. `w1/artifacts/R44C2Rubric/receipts/base-census-summary.json`: exit **1**, `entries_evaluated` 80, `mismatches` 3, ids `C2-a1-owned-coverage-count`, `C2-a2-owned-depth-count`, `C2-a4-owned-depth-craft-range`, `rubric_sha256` `e8cc0dedd6b4bbfb323983018806de4b6ad59b80b1aeee111aa2d8ebf55e755e`. `git show c48f8a4b:tools/round-44/c2-rubric.json \| sha256sum` prints that same digest. `l1/c2-score-at-55bcce69.json`: exit **0**, `mismatches` `[]`, `entries_evaluated` 80, `met_target` true, `rubric_sha256_at_freeze` the same digest, `pre_freeze` false. The vacuity stop did not fire; the predicate's non-vacuous landing did. The lesson still lists D-19 under "still open" — defect 2. |
| D-20 | open | The three repaired targets are a coverage count, a depth count, and a `SKILL.md` range (`expected_edits` append). None is a capability row re-derived from a receipt. C2's exit 0 is not evidence about coverage (C1 is `met_target` false). |
| D-21 | exercised | `c2-counter.py` argparse (`:1628-1642`) has `--pre-freeze`, `--selftest`, `--schema`, and no `--rubric-audit`. `git grep rubric-audit` on the freeze blobs of `c2-counter.py` and `c2-controls.py` prints nothing. What exists is the external witness: rubric `fitness.fails_as_required` 80, `not_demonstrated` `[]`, and `mutation-witness.json` 80/80 `fails-as-required`. The counter will still score an entry that has no red arm. Do not close. |
| D-22 | open | Planned-row checks (`C2-g*`, command text around `c2-rubric.json:4226`) still treat `steer` inside the marker as the hatch (`steered="steer" in marker.lower()`) and do not require the marker to cite a resolving receipt path. |
| D-23 | open | Category `(e)` checks `git show` a committed score JSON and compare fields (`c2-rubric.json` commands around `:1948`). They do not re-execute the cited counter. `git grep` of the rubric found no "lower evidence" grade. |
| D-24 | open | Exit wants each README map row bound to the knowledge stem's `source:` so a wrong-but-present row reds. `git grep -c 'source:' c48f8a4b -- tools/round-44/c2-rubric.json` prints nothing. `C2-h1` note (`c2-rubric.json:4569`) is still command A `mapped == files` with `missing`/`dangling` empty — the blind spot the debt named. Claims `:243-246` assert the opposite; that sentence is not exit evidence (defect 3). |
| D-25 | open | Lesson `:34-40`: `Assimilation: none`, five-row slice re-derived, no row appended. That is the carried re-check, not "slice closed, nothing adoptable". |
| D-26 | open | `test -d considerthese` exit **1** (absent). Lesson `:41` is the one-line absence report the debt already said is not the exit. No dated "later round must re-check rather than assume" note beyond the ordinary carried-debt list. |
| D-27 | exercised | The 404 path is now in the freeze. `git merge-base --is-ancestor 2081dc069e9f5a15a8f4dacf0e917399a468ffc7 c48f8a4b` exit **0**. Freeze blob `1becba2bb0a80e7b9b0a7715f15e56512a7e5f7e`, 14 bytes, sha256 `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed`, body `404: Not Found`. The other conjunct did not fire: no local-source gate or URL linter. `git grep rubric-audit` / lane `tools/round-44` has no URL gate, and `/home/vgpnk/Projects/shokunin/scripts` has no match for `listing receipt`, `http_status`, `200 listing`, or `guessed URL`. The lesson calls D-27 closed on the file alone — defect 1. |
| D-28 | open | `c2-rubric.json` `frozen_paths` is still `SCORECARD.md`, `SHONEN.md`, `SKILL.md` whole. No separate instrument-registry file, and citations are not re-resolved row ids at REV. |

## Defects the L1 must record

The ledger file stays as wave 1 wrote it. These are record defects, not claim edits.

### 1. D-27 is not closed

- Path: `corpus/lessons/round-44.md:90-91` ("D-27 `stale-premise` fix (now closed by the committed 404 receipt").
- Command: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin merge-base --is-ancestor 2081dc069e9f5a15a8f4dacf0e917399a468ffc7 c48f8a4bfd449300c975668e59aae5b5538b6a84`; exit **0**. `git cat-file -s c48f8a4b:.ufo/waves/round-44/l1/probe-fixture-404.txt` → **14**. sha256 **`d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed`**.
- Observed: the receipt conjunct of D-27's exit is met. The mechanical conjunct (a gate that refuses a URL cell with no committed 200 listing, plus a red control on a guessed URL) is absent. Closing D-27 on the 14-byte file drops half the exit.
- Required record: D-27 stays open (this seat's finer state: exercised). M44-1 may keep the file as its red arm; that is not the debt exit.

### 2. D-19's exit did fire; the lesson still lists it open

- Path: `corpus/lessons/round-44.md:87-88` (D-19 inside "Carried debt (still open)").
- Command / observed: `w1/artifacts/R44C2Rubric/receipts/base-census-summary.json` exit_code **1**, mismatches **3**, rubric sha256 **`e8cc0dedd6b4bbfb323983018806de4b6ad59b80b1aeee111aa2d8ebf55e755e`**. `git show c48f8a4b:tools/round-44/c2-rubric.json | sha256sum` → the same digest (match; the census is the frozen rubric bytes). `l1/c2-score-at-55bcce69.json` exit_code **0**, `mismatches` **[]**, `entries_evaluated` **80**, same rubric digest, `rubric_source` **freeze**.
- Required record: close D-19 this round. The vacuity stop was the debt; the round landed the only shape the exit accepts.

### 3. Do not close D-24 from the claims sentence

- Path: `plans/round-44-claims.md:243-246` (frozen; do not edit) asserts a content arm "binding each map row to its knowledge stem's `source:` (debt D-24 mitigation)".
- Command: `git grep -c 'source:' c48f8a4b -- tools/round-44/c2-rubric.json` → no match (exit 1, empty stdout).
- Observed: `C2-h1` (`c2-rubric.json:4569`) is still mapped-vs-files with empty missing/dangling. A present-but-wrong map row still cannot red on `source:`.
- Required record: D-24 stays open. The frozen sentence overstates the instrument; it is not exit evidence.

## Commands

Facts file: `.ufo/waves/round-44/w2/artifacts/R44W2ScoutDebt/facts.txt` (1529 bytes, sha256 `1b85cdfec9adeb7762e4d34d4aa9db36a4118c98107984efcebed5bda29a7727`). The shell was not separately timed (`wall_seconds` unmeasured). `facts_exit:0` is the extractor's exit. `git grep -c` sections in that file are empty because a no-match exits 1 and prints no count line (`|| true`).

| command | exit | observed |
|---|---|---|
| `git merge-base --is-ancestor 2081dc06… c48f8a4b` | 0 | 404 commit is an ancestor of the freeze |
| `git log -1 -- .ufo/waves/round-44/l1/probe-fixture-404.txt` | 0 | `2081dc06` 2026-10-28 08:59:08 -0300 |
| `git show c48f8a4b:tools/round-44/c2-rubric.json \| sha256sum` | 0 | `e8cc0ded…55e755e` |
| `git grep -c` uncompressed / `unbound` / `source:` / `rubric-audit` at the freeze paths named above | 1 (no match) | those strings are absent from the blobs searched |
| `test -d /home/vgpnk/Projects/shokunin/kaidoku-shokunin/considerthese` | 1 | directory absent |
| python extract over `carriers.json`, rubric, manifest, mutation witness, c1 score | 0 | four carriers; fitness 80/80; c1 `carriers_matched` 4, `met_target` false, exit 1; manifest has no `unbound` key; 8 v2.1 files |

Scratch `/fast/scratch/hyaku/kaidoku-r44/R44W2ScoutDebt` was created only as `TMPDIR` and removed (`test ! -e` exit 0). No clone. No tool installed. Ledger not rewritten.
