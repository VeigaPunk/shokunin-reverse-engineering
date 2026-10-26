# R38W2Sentinel — seam integrity, round 38 attempt 2 wave 2

**Verdict: DEFECTS FOUND.** Six of the five seam checks are clean (secrets, pacman, permissions,
symlinks, read-only repos, REA version discipline); the write-containment check and the
provenance check both fail, one of them *while I measured it*.

- Measured window: 2026-10-26T03:59:39−03:00 → 04:06:43−03:00. Lane HEAD moved `0fc61133` →
  `e265533e` during the window (that commit adds only `w2-spec.json`, `w2-gen.py`,
  `w2-dispatch.json`; it is not the corpus drift below). Everything cited is timestamped.
- Read-only throughout. No lane file edited, nothing moved or deleted, no VCS mutation, no
  subagents, no background jobs. Tooling ledger: **nothing installed or upgraded**.
- I attacked only the seam. I did **not** re-run or re-judge the C1/C2 counters; the verdicts
  themselves are other seats' surface.

---

## 1. Findings, by severity

### F1 — HIGH — seats wrote into both repo roots; the wave-1 remediation for this exact leak was not adopted and it recurred three times

| # | path | size | mtime | owner (from content) | state at 04:06:43 |
|---|---|---|---|---|---|
| a | `/home/vgpnk/Projects/shokunin/unblob.log` (**fleet repo root**) | 2652 B, sha256 `2d651a4a…f16299` | 03:56:04 | `R38W2SymlinkUnblob` | **still present, untracked, not ignored** |
| b | `kaidoku-shokunin/unblob.log` (**lane root**) | 2076 B, sha256 `b44810f5…f33eae` | 04:03:33 | `R38W2AvmProbe` | removed by another party between 04:05 and 04:06:43 (bytes preserved in my artifacts) |
| c | `kaidoku-shokunin/paths_raw.txt` (**lane root**) | 2770 B, 86 lines | 04:01:59 | unattributed | still present, untracked |

Wave-1 precedent, same file, lane root: `R38SentinelBounds.md:22,157` — 3617 B, mtime 03:24:32,
seat `R38ExecBeforeArmRecheck`, "removed by 03:26:53". That report published the remediation
(`cd "$S" && unblob …`, optionally `.gitignore` + a clean-tree assertion). **Nothing adopted it**:
`kaidoku-shokunin/.gitignore` is still `__pycache__/` + `*.pyc`; the fleet-root `.gitignore`
(`*-shokunin/`, `.ufo/waves/*/*-scratch/`, …) does not cover it; `git check-ignore -v unblob.log`
at the fleet root → **rc=1**; no pre-filing clean-tree assertion exists in `tools/round-38/`.

**Exploit path (mechanism, not speculation).** unblob logs to `./unblob.log` and installs its own
Landlock rule for the logfile at a **relative** path. Leaked line 4 of (a):

```
Activated FS access restrictions; rules=[Read("/"), ReadWrite("/dev/shm"),
  ReadWrite("/fast/scratch/hyaku/kaidoku-r38/R38W2SymlinkUnblob/direct/P5"), …,
  ReadWrite("unblob.log")], status=FullyEnforced pid=2896387
```

and line 1: `Logging configured extract_root=.`. So the sandbox *authorises* a write to
`./unblob.log` in whatever directory the process was launched from: the seat chose the CWD, the
sandbox then guaranteed the write succeeds there. Content of (a) names
`…/R38W2SymlinkUnblob/P5.sqsh`; content of (b) names `…/R38W2AvmProbe/input/k4-avm.bin`. REA's
`extract-firmware` inherits CWD, so `npx rea-agents …` launched from a repo root produces the same
file as a direct `unblob` call.

**Impact.** (i) The fleet repo is a git repo whose working tree carried 157 intent-to-add entries
at 03:59; a whole-subtree `git add -A` / `jj file track` sweep pulls a foreign lane's log into an
immutable commit, carrying absolute scratch paths (`/fast/scratch/hyaku/kaidoku-r38/…`) that do
not exist after scratch removal — un-reproducible path evidence in history. (ii) `R38W2SymlinkUnblob.md:12-14,196`
asserts "**No lane writes outside this report and …/artifacts/R38W2SymlinkUnblob/**" and leaves
the fleet-repo write undisclosed; a reader checking only the lane would rate containment green.
(iii) It is the fourth occurrence in two waves, so the containment claim in any wave report is a
per-seat assertion with no gate behind it.

**Smallest remediation.** `rm /home/vgpnk/Projects/shokunin/unblob.log` and
`rm kaidoku-shokunin/paths_raw.txt` before integrating; add `unblob.log` to both `.gitignore`s;
make the unblob call sites `cd "$S" && …` (or pass `--log-file "$S/unblob.log"`); add the
clean-tree assertion to the filing gate (QUALITY 47 already demands an empty `git status
--porcelain` at filing; round 38 has no `prefile-check.sh`, so nothing enforces it).

### F2 — HIGH — the landed corpus was rewritten mid-wave, uncommitted, and the rewrite relabels committed bytes as a "draft"

At 04:06:43, versus HEAD `e265533e`, four tracked files are modified. HEAD-relative diffs are in
`artifacts/R38W2Sentinel/`; against the *landing* commits the counts are 7/18/5 lines
(`…recursion.md` / `…unblob-format-matrix.md` / `round-38.md`) and QUALITY `+1` row.

1. `corpus/knowledge/2026-10-26-unblob-format-matrix.md` (04:01:06) **reverses a correction that
   is committed in `3b960fe5`**: the committed text said the staged "42 vendor-attributed entries"
   was "a count of the word `Vendor` (42 occurrences), not a per-handler attribution count"; the
   worktree now says "42 of the 97 sections carry one `Vendor:` field, and one of the 42 values is
   the literal `unknown`", plus new tallies "89 Fully supported, 8 Partially supported".
2. `corpus/lessons/round-38.md` (04:01:25) repeats the reversal and then writes: *"An attempt-2
   draft wrongly called it a word count; wave-2 seat `R38W2SrcS116` caught that before the final
   landing (M38-5)."*
3. `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` (04:01:25) hedges the very
   mechanism sentence R38-C1's verdict narrates (K2's `unpublished-entry` gap now holds only "in
   which `sasquatch-v4be` extracts the image").

Two distinct defects here, and they must not be conflated:

- **The content is evidence-backed.** `R38W2SrcS116.md` (03:56:00) recount is explicit: "42
  occurrences of the word `Vendor`, all as `Vendor:</strong>`; 42 sections carry a vendor field",
  "Counter {Fully:89, Partially:8}", one value `unknown` on `squashfs-v3-non-standard`. So the
  reversal is *correct*, and the landing's original correction was wrong.
- **The provenance wording is false.** The mislabeled "attempt-2 draft" is committed content — it
  is in both `3b960fe5` and `0fc61133` (`git show 0fc61133:corpus/lessons/round-38.md` line 48 =
  "Two corrections: …"). There was no draft: it landed, was scored, and is now being relabelled
  after the fact. "Before the final landing" is not true of an amendment made at 04:01 against a
  landing made at ~03:4x. This is the exact failure mode QUALITY 79 exists to catch (an amendment
  that calls itself pre-scoring), committed in the round that authored that rule.
- **`M38-5` has no definition.** `grep -n 'M38-5'` repo-wide → one hit, the sentence above, in the
  worktree lesson. The lesson's own table defines `M38-1..M38-4`; `corpus/QUALITY.md` cites
  `M38-1`, `M38-2`, `M38-6`. A mistake id cited with no row is not a recorded mistake.

**Measured-bytes impact on the round's own invariant.** Several wave-2 seats verified
"worktree == landed bytes" for these entries (`R38W2SymlinkUnblob.md:11-12` at 03:59:04: "whose
bytes are identical to the working tree (`diff <(git show 3b960fe5:…)` → empty)"). That was true
when checked and is false from 04:01:06. Any seat that checks it after 04:01 gets the opposite
answer, and any integration that hashes the worktree rather than a revision is now scoring bytes
the freeze never held. The counters take `--rev`, so the C1/C2 receipts are unaffected — **but the
entry the verdict narrates is no longer the entry on disk.**

### F3 — HIGH — a new instrument, a new QUALITY row and an M38-6 citation landed at 04:05, after the freeze and after seats scored; its own receipts cannot satisfy its own "before data" clause

- `tools/round-38/intended-doc.py` — **new file**, mtime 04:05:07, 2776 B, untracked. Its docstring
  says it exists because "the frozen R38-C2 counter accepts any pointer whose path exists, so
  materialising a stub file … scores the same '1 -> 0 mismatches' as the real repair (wave-2 seat
  `R38W2C2Controls`, S2)".
- `corpus/QUALITY.md` row 81 added (04:05:36) and it demands: "**Before data**, the control suite
  carries a 'materialise the missing path' control; after data, `tools/round-38/intended-doc.py`
  … must print `bound`."
- The receipts for that control are `l1/intended-doc/{base,landed-0fc61133,shortcut-s2}.json`,
  all written **04:05:20–04:05:22** — i.e. after the data (`0fc61133`, ~03:4x) and after every
  wave-2 seat that scored C2. The rule's own before-data ordering is therefore unsatisfied by its
  own evidence, which is QUALITY 80's stated defect ("a generator fixed after the freeze makes the
  receipts certify bytes the freeze never held") applied to an instrument instead of a generator.
  The freeze `e059ca93` does not contain this tool, so QUALITY 79's drift gate — which walks the
  claim's kill-rule paths — has nothing to report unless the new path is added to the kill-rule set.
- `l1/intended-doc/shortcut-s2.json` records `"rev": "HEAD"`: a **floating** revision in a receipt
  that is meant to prove a bound. HEAD was `e265533e` at measurement and has moved twice today, so
  the receipt is not reproducible by pin. (`landed-0fc61133.json` is properly pinned and says
  `verdict: bound`; `base.json` says not-bound, which is the right polarity.)
- Row 81 cites `corpus/lessons/round-38.md` **M38-6**, and the worktree lesson contains
  `M38-6` **zero** times. Dangling cross-reference at measurement time.

Assessment: row 81's *substance* is a good rule and the under-test finding (frozen C2 counter is
gameable by a stub) is a legitimate wave-2 result. The defect is process: a post-freeze instrument
plus a post-freeze rule row, both uncommitted, with receipts dated after the scoring they are said
to precede, and a rule citing an undefined mistake id.

### F4 — LOW/MEDIUM — residue outside `$S` that nobody owns

- `/tmp`: 9 files naming r38/kaidoku, mode 644, mtimes 01:08:42–03:56:34 —
  `r38sec.md` (3663 B, unprepublished round-report prose), `r38scribe-xpin.txt` (1168 B, scratch
  paths + `ev_` hashes), `r38uf-tree.json` (1 522 052 B), `r38readme.md` (74 854 B upstream copy),
  `r38f` + `r38-fixtures.txt` (identical 1785 B pair), `r38w2score_seat.txt`, and
  `tsk-r38-{census,live}-before.txt` (01:08, tsukuroi's, not this lane). `/tmp` is 3% used now, so
  no pressure, but the bounds require cleanup and these are world-readable.
- `/fast/scratch/hyaku/kaidoku-r38/mint.wrapped.json` (11 246 B, 03:58:05) sits in the **shared
  parent**, not a seat `$S`; its payload references `/fast/scratch/hyaku/kaidoku-r36/…`, so it is a
  round-36 envelope copied in as a fixture. [INFERENCE] written by a wave-2 seat rather than the L1.
- Six zero-byte dirs from attempt 1 still present: `controls-c1-{1,2}`, `controls-c2-{1,2,3}`,
  `R38W2RevFreezeDrift`, `R38W2ScorecardAccuracy` (empty parent dirs, harmless, but the
  attempt-1 inventory `l1/attempt1-scratch-leftovers.txt` lists them and was not acted on).
- The 22 seat dirs with content belong to seats that are still running; not residue.

### F5 — LOW — a pre-written fleet-repo report stub

`.ufo/reports/round-38/kaidoku.md` (fleet repo, untracked, 85 B, 03:55:05) contains exactly
`# kaidoku — round 38 report (attempt 2)` + `DRAFT — completed after wave 2 settles.` It is the one
untracked fleet-root file whose content names kaidoku/round-38 besides the leak. Being a stub it
fabricates nothing — but it sits at the path the fleet-level report is read from, and it was
created before any wave-2 seat filed. It must be filled or deleted before the round is called
closed; an empty-but-present report is the cheapest way to over-report a round.

---

## 2. Check-by-check results

**(1) Fleet-root untracked files naming kaidoku / round-38 / R38.** `git -C …/shokunin status
--porcelain` → 180 entries (157 ` A` intent-to-add, 19 ` M`, 3 `??`). Files whose *content* hits
the pattern: `.ufo/reports/round-38/kaidoku.md` (85 B, §F5) and `unblob.log` (2652 B, §F1a — it
names `R38W2SymlinkUnblob`). Also ` M .ufo/state/kaidoku.report-baseline` (harness state, not
content). Nothing moved or deleted.

**(2) Scratch / tmp residue.** §F4. All `/fast/scratch/hyaku/kaidoku-r38/*` seat dirs with content
are live seats; `controls-*` empties and `mint.wrapped.json` are attempt-1/round-36 residue. No
orphaned extractor processes: `ps -eo pid,etimes,cmd | grep -E 'unblob|sasquatch|rea-agents'` →
only three `npm exec rea-agents@6.7.0 mcp` (elapsed 7734 s, started 01:55:44–01:56:10, i.e.
**before** wave 1; §3). No `lsof +D` handles held on any seat scratch dir.

**(3) Secrets.** Zero. Patterns `sk-…`, `ghp_`/`gho_`, `AKIA…`, `BEGIN * PRIVATE KEY`, `op://`,
`xox[baprs]-`, `Bearer <20+>`, `password=…` over `.ufo/waves/round-38/w1/` (41 reports + all
artifacts), `.ufo/waves/round-38/w2/`, and **every committed** round-38 path
(`git ls-tree -r HEAD | grep -i round-38`, content scanned via `git show`) → no matches. The
64-hex strings that look like keys are sha256 file digests (verified in context:
`03b1153c…  c2-at-tip.json` in `R38ExecRecountBase.md:200`) and 21 `ev_` evidence ids.

**(4) Lane writes outside `w1/` + `w2/artifacts/`.** At 04:03: `git status --porcelain -uall`
= 220 entries; 211 fall inside an allowed prefix, 9 outside. Of the 9, three are the §F2 corpus
edits (real, and the only ones that are tracked-content changes) and six are integration-side
files: `l1/attempt1-scratch-leftovers.txt`, `l1/scores/c2-at-0fc61133.json`, `l1/intended-doc/*.json`,
`r38-w1-results.json`, `w2.ready`, `w2.ready.dispatched`, `w2/swarm-registry.json` (mode 600 — correct
for a registry). Those six are outside the *seat* prefix set but are L1/dispatcher own-work, not a
seat leak; I flag them only so the L1 states which prefixes it claims. Plus `paths_raw.txt` at the
lane root (§F1c) and, at 04:03:33, a lane-root `unblob.log` (§F1b). **No seat wrote into
`corpus/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md` or `tools/` as a seat**; the
`corpus/` + `tools/round-38/intended-doc.py` writes are L1-side and are the subject of §F2–F3.

**(5) pacman.** **Zero transactions.** 28 textual mentions across both waves; a strict scan
`pacman[[:space:]]+-{1,2}(S|Sy|Syu|Su|U|R|Q…)` yields one hit, inside
`artifacts/R38ExecReadmePatch/README.patched.md:43` — historical corpus prose about a round-r4
`pacman -Q` rescan, not an invocation. Every other mention is a negative assertion ("pacman
untouched", "no pacman transaction"). No `-Sy`, no `-U`, no service restart anywhere. Consistent
with the host-wide pause.

---

## 3. What I checked that held (so the green is calibrated)

- **Symlinks in the round-38 tree:** 0 (`find .ufo/waves/round-38 corpus/evidence/round-38 -type l`
  → empty). No artifact link can traverse out of the lane.
- **Permissions:** no world-writable file under `.ufo/waves/round-38`; scripts 755, reports 644,
  registries 600; the `extract-K*` trees at 600 are stricter than needed, not looser.
- **Read-only package:** `/home/vgpnk/Projects/shokuknow` — no file newer than 03:50
  (`find … -newermt '2026-10-26 03:50'` → empty); `merge/kaidoku` newest mtime 2026-10-24 23:33.
  The repo's many ` M` entries under `lanes/chousa/…` are pre-existing and not from this round. No
  campaign tool was run there.
- **Sibling lanes:** the only recent writes under `/home/vgpnk/Projects/shokunin/*-shokunin/` are
  `kasegi-shokunin/.git/objects/*` — that lane's own round, not this one.
- **REA version discipline:** every wave-1/wave-2 receipt cites `rea-agents@6.5.0` (22 + 17
  citations); zero uses of an `xd://mcp__rea_*` device. The three resident
  `npm exec rea-agents@6.7.0 mcp` servers are the editor's MCP clients (`~/.local/share/fnm/node-
  versions/v24.21.0/.../rea-agents`, package 6.7.0), started 01:55:44–01:56:10, and wave-1
  `R38ExecProvincePatch.md:25` already documents that host configs pin 6.7.0. **Not a defect** —
  recorded here because it is the one live trap that would have silently broken the pin.
- **Committed round-38 bytes are unmodified for every tracked file except §F2's four** — so no
  wave-2 seat retro-edited carriers, oracles, counters or controls.

---

## 4. Limits

- The lane was being written by other actors throughout my window (corpus at 04:01, `QUALITY.md` +
  `intended-doc.py` at 04:05, lane-root `unblob.log` removed between 04:05 and 04:06:43). Every
  statement above is tied to a measured timestamp; §F2/F3 may be *completed* by the L1 after I
  filed, which would answer the dangling-id half of them and not the provenance-wording half.
- Attribution in §F1 is read from the leaked bytes (scratch path + pid), not from process
  accounting: the writing processes had exited. Writer identity for `paths_raw.txt` and
  `mint.wrapped.json` is unknown; I did not guess.
- I did not verify the *arithmetic* of `89/8` or `42 of 97` myself — I checked that a seat report
  with a live fetch receipts them, which is the seam question, not the counting question.
- Advisory only: I changed no predicate, counter, carrier, oracle or landing byte, and I judge no
  author verdict.

## 5. Evidence artifacts (`artifacts/R38W2Sentinel/`)

`leaked-unblob.log.fleet-root.txt` (sha256 `2d651a4a…`), `leaked-unblob.log.lane-root.avmprobe.txt`
(sha256 `b44810f5…`), `leaked-paths_raw.txt.lane-root.txt`, `lane-status-at-0403.txt`,
`fleet-root-status-relevant.txt`, `corpus-worktree-vs-HEAD.diff`,
`{recursion,unblob-format-matrix,round-38}.md.vs-3b960fe5.diff`,
`round-38.md.vs-0fc61133.diff`, `QUALITY-81-worktree.diff`, `QUALITY-row-81.txt`,
`lesson-line50-M38-5.txt`, `new-instrument-intended-doc.py.snapshot`,
`intended-doc-receipts/{base,landed-0fc61133,shortcut-s2}.json`, `state-snapshot-0406.txt`.

Scratch `S=/fast/scratch/hyaku/kaidoku-r38/R38W2Sentinel` created and removed; nothing cited here
lived there.
