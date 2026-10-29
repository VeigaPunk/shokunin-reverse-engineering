# ScribeLogDraft — round 50 attempt 2, wave 3 (build)

Seat: `ScribeLogDraft` (scribe). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, read-only on the lane
tree; the only writes are this seat's directory and this report. Base revision
`f890bbead20ca2c549487167f56876ae47f1e1a4` (attempt-2 claims commit). No REA run, no network fetch, no git
mutation, no tool installed.

## Verdict

**The LOG.md attempt-2 entry is drafted and ready to land, with three items the L1 must settle before
landing.** The draft is at `.ufo/waves/round-50/w3/ScribeLogDraft/log.md` (sha256 `8d122e3c…`, 7527 bytes);
it carries every bullet the seat spec asked for, each naming a path or a command, and each
landing-dependent value left as an explicit `FILLED-AT-LANDING` marker rather than an invented number.
The three items are: (1) the L1's own receipt `.ufo/waves/round-50/l1/frozen-unchanged-attempt2.txt` does
not exist yet, so the resume bullet currently cites a receipt that is not on disk; (2) the dispatched
wave-3 seat count is **35**, not the 37 the seat prompt states — three independent lane files agree on
35; (3) the C3 claim's "no independent reader" wording for `squashfs_v3_broadcom` contradicts the
round-49 entry it cites, and the `legacy-body-failure` row has two distinct mis-actions, not one.

## Findings

| # | Sev | What was checked | Exact command | Exit | stdout sha256 / value |
|---|---|---|---|---|---|
| 1 | info | C1 frozen bytes unchanged between the attempt-1 freeze and the attempt-2 base | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --stat 435d41fd4ad9211d1579fc447936fb33d2b74467 f890bbead20ca2c549487167f56876ae47f1e1a4 -- tools/round-50/ plans/round-50-claims.md tools/round-41/sqfs-list.py tools/round-27/xpin-attribute.mjs` | 0 | stdout empty (0 bytes), sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; receipt `.ufo/waves/round-50/w3/ScribeLogDraft/frozen-unchanged-receipt.txt` (sha `b21bd47d…`) |
| 2 | info | What changed between the freeze and the base | same `git diff --stat` with `plans/round-50-attempt2-claims.md` added to the pathspec | 0 | `plans/round-50-attempt2-claims.md | 134 ++++…` — one file, 134 insertions, no other change |
| 3 | info | The frozen C1 counter's offline selftest is green at the attempt-2 base | `HYAKU_SCRATCH=$S TMPDIR=$S python3 -I -B tools/round-50/c1-counter.py --selftest` (cwd = lane) | 0 | stdout sha256 `e698eb09f7f1083d319c819e54e271af6fc91edf766a1beb48711923a02c16a5` (13457 B); JSON `{"selftest":"c1-counter","cases":169,"green_ok":17,"red_ok":152,"path_probes":6,"path_probes_discriminating":3,"root_probes":8,"spec_probes":43,"failures":[]}`; copy `.ufo/waves/round-50/w3/ScribeLogDraft/c1-counter-selftest-attempt2.json`, receipt `…/c1-counter-selftest-receipt.txt` (sha `b1e7226a…`) |
| 4 | **HIGH** | The L1's own "frozen unchanged" receipt does not exist | `cat /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/l1/frozen-unchanged-attempt2.txt` | 1 | `No such file or directory` — the resume bullet in the draft cites this path; the L1 must write it (or amend the draft to cite only the receipt that exists) before landing |
| 5 | **MED** | The dispatched wave-3 seat count | `python3 -c` over `.ufo/waves/round-50/w3-dispatch.json` (`counts.spawn`), `w3-spec.json` (`items`), `w3/swarm-registry.json` (`members`) | 0 | **35** in all three (dispatch `spawn 35`; spec 35 items; registry 35 members, all `kind: spawn`). Role mix identical in all three: `executor 10, scribe 7, scout 5, critic 4, reviewer 4, connector 2, mutation-tester 1, revenger 1, sentinel 1`; attack roles (reviewer+critic+mutation-tester) 9/35 = 25.7%. The seat prompt's "37 seats" is not the dispatched number — the draft says 35 |
| 6 | **MED** | The C3 claim's reader census vs the entry it cites | `sed -n '100,106p' corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`; `grep -n "squashfs_v3_broadcom\|partial reader" …` | 0 | `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md:103`: `squashfs_v3_broadcom` — `unsquashfs` 4.7.5 refuses the magic (exit 1), `7z` 26.04 **does** list the committed LE fixture (exit 0, 2 files, 13 B; receipt `v3-readers`), "A partial reader therefore exists". `plans/round-50-attempt2-claims.md` §R50-C3 calls all three families "no independent reader (… per the round-49 entry's reader census)". The claim's own cited source denies that for broadcom; the v5 table must branch per family |
| 7 | **MED** | The `legacy-body-failure` row has two mis-action branches, not one | `sed -n '536p' SKILL.md` | 0 | the row's cause reads: "if the independent readers fail where sasquatch failed the body is damaged and the failure stands; **if either lists the tree the fault is the sasquatch build or its argv, so reinstall the extractor and rerun** before touching the image". For a healthy v2ns/v3_nonstandard body (both readers refuse) the row declares the body damaged; for a healthy broadcom body (7z lists) it prescribes reinstalling the extractor. The v5 rule must cover both, or state which families each branch serves — the draft's C3 bullet says so |
| 8 | info | The four v2ns `_ddefault` envelopes named by F2 exist, and the held-out dir size | `ls .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/ \| wc -l`; `… \| grep -i ddefault` | 0 | 126 envelopes in the dir; exactly four `squashfs_v2_nonstandard_*_ddefault` (`squashfs_v2.0_{be,le}`, `squashfs_v2.1_{be,le}`), each with `envelope.json`; the other `_ddefault` entries belong to the reader-backed families (`squashfs_v1`, `squashfs_v2`, `squashfs_v3`, `squashfs_v3_ddwrt`, `squashfs_v3_adaptive`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`) and must keep their v4 rows |
| 9 | info | The v4 table rows the C3 claim moves | `grep -n "legacy-body-failure\|^  | clean \|" SKILL.md` | 0 | `SKILL.md:526` marker `<!-- sqfs-triage-table v4 -->`, `:527` the actions comment, `:536` the `legacy-body-failure` row (glob `squashfs_v[123]*`, action `cross-read-legacy`), `:543` the `clean` row (gap kinds `none`, published files `>0`, action `none`, "match files to the oracle by exact relative path and sha256"). The draft cites these line anchors |
| 10 | info | The C3 instrument does not exist yet at the base (expected — it is this wave's build) | `ls tools/round-50/` | 0 | `c1-controls.py, c1-counter.py, c1-run.sh, c2-record.py, carriers.json, control-fixtures/, fetch-vendor.py, gap-rule.json, oracle/, selftest-r49-c2.expected.json, selftest-r49-c2.py`; no `sqfs-triage-v5.py` (the C3 freeze adds it) |
| 11 | info | The C1 freeze record and the attempt-1 controls the resume bullet cites | `cat .ufo/waves/round-50/l1/FREEZE`; `ls .ufo/waves/round-50/controls-attempt1/` | 0 | `FREEZE` = `435d41fd4ad9211d1579fc447936fb33d2b74467`; attempt-1 controls dir holds `c0 c1 c2 c3 c4 pos summary.json score.out.txt` |
| 12 | low | Dispatcher race on `w3.ready.partial` | `ls .ufo/waves/round-50/` then `cat .ufo/waves/round-50/w3.ready.partial` | 1 on the second call | the file existed at the first listing (`Oct 29 17:32`) and was gone seconds later; `w3.ready` is present and names the dispatch file and the L1. Informational only |

## What the draft contains (and where it is conservative)

- Resume decision: attempt 1's release without advance (attempt-1 controls: CTL-C1-0/1 as expected,
  CTL-C1-2/-3/-4/POS `could_not_evaluate` on `provider_timeout` at load 95–176, no data run), C1 resumed
  under the SAME freeze `435d41fd…` with no amendment, the empty `git diff --stat` proving the bytes, the
  attempt-2 declaration as the only addition, and the frozen counter's offline selftest green at the base.
- C3 declaration: depth; F1 and F2 from `.ufo/waves/round-49/w2/W2Skill.md`; the exact SKILL line anchors;
  the table-v5 / `tools/round-50/sqfs-triage-v5.py` landing surface; plus the broadcom wording sub-bullet
  (finding 6) so the record carries the open question rather than a settled fact.
- Wave-3 shape: 35 seats and the measured role mix, from the three dispatch files, with the no-REA-in-this-
  wave rule and the reason (attempt 1's lost window).
- C3 freeze, controls, data run and landing: `FILLED-AT-LANDING` markers, each naming the exact command
  or path the L1 must substitute a measured value into (C3 freeze commit + registry row; C1 controls
  `c1-controls.py gen`/`score` under `.ufo/waves/round-50/controls-attempt2/`; C3's four controls before
  the table lands; `c1-run.sh after --id <id> --carrier <CACHE>/<pin>.bin --data-run`; the C1 entry /
  PROVINCE / README / SOURCES S243-S245+S249 / SCORECARD `140/140` set; the C2 re-measure at the final REV).

## Limits of this seat

- Nothing was landed: `LOG.md` is untouched, `plans/`, `tools/`, `corpus/`, `SKILL.md`, `PROVINCE.md`,
  `SCORECARD.md`, `SHONEN.md` and the fleet repo were read only. No commit, no stage, no stash.
- No REA invocation, no `--data-run`, no vendor download; the C1 carriers were never fetched, so the
  draft's data-run and landing bullets stay placeholders.
- The C3 instrument was not built or scored by this seat: `tools/round-50/sqfs-triage-v5.py` does not
  exist at the base, so finding 6/7 are text-level findings against the committed `SKILL.md` table and the
  committed round-49 entry, not a score.
- The C1 counter was exercised only through its offline `--selftest` (the counter's own docstring states
  `--selftest` is offline and deterministic); no scoring run at any revision was made by this seat.
- The 35-vs-37 seat-count discrepancy is reported, not reconciled: the L1 owns the wave-shape record.
- Tree check after the draft: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain` lists only untracked wave artifacts (`.ufo/waves/round-50/…` produced by the L1 and the dispatcher, plus this seat's own files) — no tracked file is modified by this seat.

## Tooling

No tool was installed (no pacman, no `uv tool`, no `~/.local/bin` write). Every command used the host's
`python3` (`python3 -I -B`), `git` (read-only subcommands: `log`, `rev-parse`, `cat-file`, `diff --stat`,
`ls-tree`, `show`) and coreutils. Host guard checked before the heavy pass:
`bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` (exit 0; `/fast/scratch/hyaku`
showed 237.8 M under `kaidoku-r50` and 1.9 G under `souji-r42`).

## Artifacts

- `.ufo/waves/round-50/w3/ScribeLogDraft/log.md` — the LOG.md attempt-2 entry draft (sha256 `8d122e3c…`).
- `.ufo/waves/round-50/w3/ScribeLogDraft/frozen-unchanged-receipt.txt` — the frozen-bytes receipt (sha256 `b21bd47d…`).
- `.ufo/waves/round-50/w3/ScribeLogDraft/c1-counter-selftest-receipt.txt` — the selftest receipt (sha256 `b1e7226a…`).
- `.ufo/waves/round-50/w3/ScribeLogDraft/c1-counter-selftest-attempt2.json` — the raw selftest stdout (sha256 `e698eb09…`).
- Scratch `/fast/scratch/hyaku/kaidoku-r50/w3-ScribeLogDraft` removed after the receipts were copied here.
