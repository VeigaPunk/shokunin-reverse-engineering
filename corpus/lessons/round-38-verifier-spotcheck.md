author: hyaku closure (non-author integrator, @m_opus)

# kaidoku round 38 — verifier spot-check (non-author closure)

Scope: lane-round kaidoku r38 (attempt 2 landed; attempt 1 died without a report). Pre-round lane HEAD `676328449adf1abe411ee86d994baa81c9d06729` → after `7e97951460647e4fc39542b7a4f0255b5bf1af17` (branch `main`).
Report: `.ufo/reports/round-38/kaidoku.md` (fleet repo). Prompt: `.ufo/prompts/kaidoku-round-38.md`.
The report's own base is `77091b49…`, the lane's round-37 commit. `676328449` is its only child, and it adds only `corpus/lessons/round-37-verifier-spotcheck.md` (`git diff --stat 77091b49 676328449` → 1 file, +87). So both bases score the same surfaces.

Driver digest (copied from mutable `.ufo/watchdog.log`):

```
2026-10-26T03:00:01-03:00 launch kaidoku round=38 pgid=415193 driver=hyaku-inline attempt=1
2026-10-26T03:37:05-03:00 lane-dead-no-report kaidoku round=38; retry same round (hyaku-inline attempt=1: L1 KaidokuR38 exited without a landed round: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-38/kaidoku.md)
2026-10-26T03:37:07-03:00 launch kaidoku round=38 pgid=1293607 driver=hyaku-inline attempt=2
2026-10-26T04:21:00-03:00 complete kaidoku round=38; hyaku-inline attempt=2
```

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H %ci' -- .ufo/reports/round-38/kaidoku.md` | `kaidoku-shokunin <kaidoku@shokunin.local> e6fbc27830247170f379531a04ffc5e901066c8d 2026-10-26 04:20:15 -0300`. That is after the lane tip (04:19:42) and before `complete` (04:21:00) | ok |
| SHONEN heading, one line per box | read report §SHONEN | 4 lines: box 1 `[ ]`, box 2 `[~]`, box 3 `[ ]`, box 4 `[~]`, each with a pointer or reason | ok |
| cited commits exist and are ancestors of the branch | `git rev-parse --verify <h>^{commit}` and `git merge-base --is-ancestor <h> main` for `67632844 77091b49 e059ca93 efd5c47a 79f69347 f1010f67 3b960fe5 0fc61133 e265533e 7a1ac7fe 7e979514` | all resolve, all exit 0 | ok |
| commits in round | `git log 676328449..7e979514` | 13 commits, all authored by `kaidoku-shokunin`: attempt 1 `e059ca93`…`077e212b` (8), attempt 2 `3b960fe5`…`7e979514` (5) | ok |
| pushed | `scripts/hyaku/jj-lane.sh state …` | `branch=main local=7e979514… remote=7e979514… ahead=0 behind=0 head=detached tracked=0 untracked=0` | ok |
| leftovers | `git -C <lane> status --porcelain` | empty. The R36-CL1 stamp is now committed (`e059ca93`), so that leftover is closed | ok |
| fleet misroots | `ls /home/vgpnk/Projects/shokunin/unblob.log <lane>/paths_raw.txt /fast/scratch/hyaku/kaidoku-r38` | all absent. `paths_raw.txt` is tracked under `.ufo/waves/round-38/w2/artifacts/_misroot/`. Fleet `git status` holds operator-side `.ufo/state/kaidoku.report-baseline` plus intent-to-add files from other campaigns; none of them is round-38 kaidoku work | ok |
| prompt carries template contract | `diff <(sed -n 1,140p .ufo/prompts/kaidoku-round-38.md) templates/round-prompt.md` | only `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitutions differ in §1–§5. §6 is the hyaku addendum and §7 is scratch discipline. The route map quoted in §6 is the operator's run-8 global role map (model aliases). `MISSION.md` names only abstract buckets, and no contradiction was found | ok |
| waves dispatched | `ls .ufo/waves/round-38/w{1,2}.ready.dispatched`; `jq '.seats\|length, .results\|length' r38-w{1,2}-results.json` | both stamps are tracked. Seats 40/40 and 44/44; reports `ls w1/*.md \| wc -l` → 40, `w2` → 44 | ok |
| marker vs report | 13 commits, 2 knowledge entries, 6 SOURCES rows, receipts | a real report, not a marker | status `ok` |

## 2. Claims

The lane's counters and gates were not executed (§Gate standard, Closure consequence). Every number below is either a plain measurement over committed bytes or a read of committed gate evidence.

### R38-C1 — coverage, standard BE SquashFS v4 Frontier → Core (author: honest stop)

Re-measured:

- **Freeze bytes shipped at the measured revision.**
  - `sha256sum tools/round-38/c1-counter.py` → `a7a62b09…16db8`, which equals `git show e059ca93:tools/round-38/c1-counter.py | sha256sum`.
  - The same holds for `c2-counter.py` (`7f137b66…b0f7`).
  - `git diff e059ca93 7e979514 -- plans/round-38-claims.md tools/round-38/c{1,2}-counter.py` → empty.
- **Per-carrier predicate**, recomputed by `jq` over `corpus/evidence/round-38/c1/K*/after.json` against `corpus/evidence/round-37/c1/K*/oracle.tsv` (sha256 plus relative-path suffix):

| carrier | handler | gaps | oracle rows matched | carrier pin (`carriers.json`) |
|---|---|---|---|---|
| K1 | `squashfs_v4_be` | 0 | 5/5 | ok |
| K2 | `squashfs_v4_be` | **1** `unpublished-entry` (`firmware.bin_extract/var/lib/run-link` → `../../a/run.sh`, symlink) | 3/3 | ok |
| K3 | `squashfs_v4_be` | 0 | 4/4 | ok (`9c7c523c…97c0`) |
| K4 | `squashfs_v4_be` | 0 | 4/4 | ok (`a29ddc15…56ed`) |

- The predicate needs "no extraction gap", so the count is 3 of 4 carriers. Independently of that, `grep -n 'Round-38 additions to Core' PROVINCE.md` → nothing, so the predicate's Core-row binding is also unmet.
- **Before, re-measured:**
  - `git show efd5c47a:.ufo/waves/round-38/controls/ctl-c1-0-do-nothing.json` → `carriers_matched 0`, `met_target false`.
  - The before receipts read `missing-extractor-dependency [sasquatch-v4be]`, 0 files, on all of K1–K4.
- **Committed score evidence agrees:** `c1-v1-at-3b960fe5.json` and `c1-v1-at-final.json` (revision `7a1ac7fe`) give `carriers_matched 3`, `met_target false`. The informational v3 receipt gives 4 carriers but also `met_target false`.
- **Verdict: does not verify; honest stop. Agree.** The lane judged by the first freeze, not by the attempt-1 amendment. The cross-check in w2 `R38W2C1RuleChoice.md` was dispatched by the lane, so it is not outside evidence. This re-measurement is.

### R38-C2 — calibration, self-assessment surfaces vs repo state (author: met by counter; counter non-discriminating)

Re-measured:

- **The pointer repair:**
  - Base `PROVINCE.md:44` reads "doctor outputs in `evidence/doctor/`". `git cat-file -t 77091b49:evidence/doctor` → fatal, the path does not exist.
  - Final `:44` reads "doctor outputs in `.ufo/waves/round-19/evidence/doctor/` (doctor-6.5.0.txt, doctor-6.7.0.txt)". `git ls-tree` lists both files at base and at final.
- **Intended document:** the round-19 commit `4f6c73f8` introduced the doctor outputs at exactly `.ufo/waves/round-19/evidence/doctor/` and cited that path in PROVINCE. The next commit, `279e8b19`, shortened it to `evidence/doctor/`. The repair therefore restores the original document, not a substitute.
- **Counts:** command A's observable was recomputed in shell (`git ls-tree` over `corpus/knowledge` vs `2026-10-NN-*` stems in README `## Coverage map`).
  - Base: knowledge=124, mapped=124, and SCORECARD says "124/124".
  - Final: knowledge=126, mapped=126, and SCORECARD says "126/126" (`SCORECARD.md:23`).
  - The two added files are the two round-38 entries.
- **Pointer sweep:** my own extractor, broader than the lane's, took backticked tokens in SCORECARD `## Owned axes` and `## Capabilities`, SHONEN, and PROVINCE `## Core` and `## Frontier`, and resolved them at each revision.
  - Base: 65 tokens, 9 unresolved. Final: 69 tokens, 8 unresolved.
  - The one real lane pointer among the base set was `evidence/doctor/`, and it is fixed. The other 8 are context-relative bare names whose prefix sits in the same sentence (`A2Capability14.md` → `.ufo/waves/round-32/a2audit/`, `FallbackReaders.md` → `.ufo/waves/round-19/w1/`), or host or fleet paths (`support/analyzeHeadless`, `AXES.md`, `result.json` under `evidence/round-1-…`). They are the same at base and final, so nothing regressed.
- **Evidence-verified, not executed:**
  - `l1/scores/c2-at-0fc61133.json` and `c2-final.json` (rev `7a1ac7fe`): `mismatches 0`, `guards_ok true`, `met_target true`.
  - The controls at `efd5c47a` all give `met_target false`.
  - `l1/intended-doc/{base,landed-0fc61133,final,shortcut-s2}.json`: `not-bound`, `bound`, `bound`, `not-bound`.
  - Self-test tallies (`w1/R38ExecSelftests.md`): c1 15 cases (1 green, 14 red, `failures []`), c2 14 cases (1/13), both exit 0 at the frozen digest.
- **Verdict: verifies.** Calibration **improved**: the mismatch count went 1 → 0 on an independent re-derivation, and the score stays 10 (saturated proxy). The lane's disclosure that the frozen counter accepts a stub (M38-6) is correct. This re-derivation does not depend on that counter.

### Harm check

- `git diff 676328449 7e979514 -- SCORECARD.md`: one coverage row restated (124/124 → 126/126) and an appended `## Round 38` section. Depth and calibration rows are byte-unchanged, and no score moved.
- `SKILL.md`, `SHONEN.md`: no diff.
- PROVINCE: three edits (the `:44` pointer, the dated note at `:157`, the note at `:376`). Adjacent `:97-125` is unchanged.
- SOURCES S001–S111 are byte-identical between base and final (`diff` of the row sets → empty). Rows 111 → 117, appends only. The `3b960fe5` S110 edit is reverted.
- No owned axis harmed.

| axis | verdict | reason |
|---|---|---|
| coverage | unchanged | C1 honest stop. Map proxy 124 → 126, but no Frontier → Core move and score 10 → 10 |
| depth | unchanged | row byte-identical, `SKILL.md` no diff |
| calibration | improved | C2 re-derived: 1 → 0 mismatches. Pointer bound to the original round-19 document; counts 126/126 observed |
| operability | unchanged | `SKILL.md` no diff. The new round tools are unregistered (R38-CL2) |
| freshness | unchanged | not claimed. The stale "unmeasured" aside was superseded by a dated note, counted under the quality trend |
| adjacency | unchanged | `PROVINCE.md:97-125` unchanged |

Not every claim verifies, because C1 stopped, and no axis is harmed. Verdict: **rejected-honest-stop**.

## 3. Discernment spot-check (`corpus/lessons/round-38.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S112 unblob `squashfs.py` @26.6.4 | admit | `curl raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py`, HTTP 200; `git ls-remote … refs/tags/26.6.4` | agree | sha256 `2d7b901b…9287`. Tag = `1fcc7a0a584a70a96c31f5a276c20944d199a089`. Line 26 `V4BE_EXECUTABLE = "sasquatch-v4be"`, lines 40-41 `case Endian.BIG, 4:` / `executable = self.V4BE_EXECUTABLE`, lines 68-69 `get_dependencies` returns both. The anchor joins lines 40-41, as the lesson discloses |
| S113 BE v4 fixtures | admit | raw LFS pointers for `squashfs_v4_be/__input__/squashfs_v4{.nopad,}.bin` @26.6.4 | agree | `oid sha256:a29ddc15…56ed size 307` and `oid sha256:9c7c523c…97c0 size 4096` equal the `sha256sum` of the committed K4 and K3 carriers |
| S116 unblob.org/formats | admit (assimilated) | `curl https://unblob.org/formats/` | agree | HTTP 200, 216890 B, sha256 `8f8c29af…bbc5` (byte-identical to the row). 97 `<h2 id=`; "more than 30 different archive, compression, and file-system formats" ×3; `id="squashfs-v4-be"` "SquashFS (v4-BE)". Counted per section: 89 Fully / 8 Partially, and 42 `Vendor:`, which matches the entry and confirms the M38-5 reversal |
| S117 README @26.6.4 | admit (assimilated) | `curl …/26.6.4/README.md` | agree | sha256 `6544d60f…3716`. Line 5 "unblob parses unknown binary blobs for **78+ archive, compression, and file-system formats**" and line 22 "**78+ supported formats**" are verbatim |
| S115 7-Zip 26.04 BE v4 refusal | reject (as oracle) | `7z l` on K1–K4 (7-Zip 26.04 x64); LE controls `corpus/evidence/round-36/c1/fixtures/k{1,2}-*.sqsh` | agree | K1–K4 each exit 2 with "Cannot open the file as archive". The LE controls exit 0. A refusal is not an extraction oracle, and it is BE-specific |
| REFUSE `sasquatch-unblob-compatibility-precondition` | reject | `find /home/vgpnk/Projects/shokunin /home/vgpnk/Projects/shokuknow -name r7-local-measurements.tsv` | **agree with the decision, disagree with one stated reason** | The lesson (`:80-82`) says the source "exists nowhere on this host", citing a `find` rooted at the fleet root only. The file exists at `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round7/work/r7-local-measurements.tsv` (1204 B, 2026-10-24), and `lanes/…` is relative to the shokuknow root. Its row M5 reads "sasquatch is absent from PATH and unblob is not importable on this host". That was true when measured and is false since the round-36 install of `~/.local/bin/sasquatch{,-v4be}`. The refusal stands on the host-state and lane-bytes grounds (D1/D2), not on provenance (R38-CL1) |
| REFUSE `sasquatch-unblob-avm-branch` | reject | `ls /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round9/work/lead2-avm-branch.tsv`; `curl -o /dev/null -w %{http_code} https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/` | agree with the decision, disagree with one stated reason | The tsv exists (1177 B, 2026-10-24), even though the lesson (`:96-97`) says S190/S191 "exist nowhere on this host". The other grounds hold: an unpinned `unblob/main` reference, the closing premise falsified (the AVM URL returns HTTP 200), and the branch mechanics reproduced on lane bytes. Same defect class (R38-CL1) |
| quarantine staged S150 (zenn.dev) | refuse (fabrication class) | `curl -L https://zenn.dev/yasu01/articles/7370bd5d414ec4` | agree | HTTP 200, 174088 B. `grep -c 'シンボルがない場合のヒント'` → 0. The real H2 list has no such heading |

New SOURCES row quote check: S117 (`corpus/SOURCES.md:123`). The row's quote "unblob parses unknown binary blobs for **78+ archive, compression, and file-system formats**" has 12 words, within the 25-word limit. It sits at README line 5 at the pinned tag, and the bytes re-open identically. **ok.** S112 and S116 quotes were also re-opened above; both ok.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → exit 0, `kaidoku ok`, 11× W04. The S112 and S117 warnings are disclosed cross-scope URL reuse. Output is identical to the committed `.ufo/waves/round-38/census-end.txt`, except that the file adds a trailing `exit 0` line. Rows `grep -cE '^ {0,3}\| S[0-9]{3}'` → 111 → 117, matching the report.

## 4. Trend verdicts

- **expansion: improved.** Two admitted entries cover ground the base map did not hold: measured BE v4 behaviour, and the producer format matrix naming `v4-BE`. Both are mapped (126/126), and each `source:` cites mined rows opened this round: S112–S114 and S116–S117, with `used-by` naming the entry.
- **quality: improved.** The stale PROVINCE "unmeasured" aside is superseded by dated notes (`:157`, `:376`). The new entries re-verify on re-open: 97 sections, "more than 30" ×3, 89/8, 42, and "78+". The false M38-5 correction was reversed. No admitted entry failed a re-check.
- **discernment: improved.** At the decision level the spot-check agrees on 4 admits and 4 rejects. The lane refused the post-scoring amendment, measured by the first freeze, and disclosed its own non-discriminating counter. One disagreement is on a supporting reason: two false absence claims in refusal provenance. It is routed as R38-CL1, and it must become a lesson and criterion next round, or this trend reads harmed.

## 5. Routed defects (lane fixes next round; status-neutral)

- **R38-CL1 (false absence sweep).** `corpus/lessons/round-38.md:80-82,96-97` and `w2/R38W2AssimRejects.md` state that `r7-local-measurements.tsv` and `lead2-avm-branch.tsv` "exist nowhere on this host", but the `find` was rooted at `/home/vgpnk/Projects/shokunin` only. Both files exist under `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round{7,9}/work/`. Append a correction to the lesson record. Add a QUALITY criterion: a negative existence claim must root its sweep at the base that the staged path is relative to. Re-state each refusal on its surviving grounds.
- **R38-CL2 (unregistered gates).** `tools/round-38/freeze-drift.py`, `intended-doc.py` and `registry-immutable.sh` are bound into admission by QUALITY 79/81. None has a self-test mode (`grep -c selftest` → 0 in each), and SKILL.md has no round-38 registry row (`grep -c round-38 SKILL.md` → 0). The c1/c2 counters are also unregistered. Under §Gate standard they grade as unregistered probes. Register each with entry command, verdict map, self-test and pinned-value path, or name them probes.
- **R38-CL3 (overstatement).** Report §Trend "discernment" says the v3 amendment "would have turned C1 green (v3: 4/4)". `c1-v3-at-3b960fe5-NOT-THE-RULE.json` has `carriers_matched 4` but `met_target false`, because no Core row exists. Say "carrier-green".
- **R38-CL4 (gate redness noted).** `freeze-drift.py --freeze e059ca93 --rev 7a1ac7fe` is red (exit 1, three drift commits) while `ships_freeze_bytes true`. That is correct history disclosure, but the round-39 freeze must define which verdict blocks a score.
- R36-CL1 is closed (stamp committed in `e059ca93`). R37-CL1..CL3 are addressed by S113/S114, the S115 rejected row, a `## Gate` section, and committed receipts.

SHONEN: no `[x]` written. For the operator: box 2 (an end-to-end domain task) looks checkable by a non-author. The REA `extract-firmware` before/after receipts on K1–K4 re-derive from committed bytes (§2), and the trigger → action → outcome entry is at `LOG.md:3126-3135`. Boxes 1, 3 and 4 are not checkable from this round's evidence.
