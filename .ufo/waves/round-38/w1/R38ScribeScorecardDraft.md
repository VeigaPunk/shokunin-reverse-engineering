# R38ScribeScorecardDraft — draft SCORECARD round-38 section + LOG.md entry

Seat: `R38ScribeScorecardDraft` (leaf scribe, round-38 wave 1). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. L1 = `KaidokuR38`. Advisory only: no lane
surface edited, no VCS mutation, no REA run, no install/upgrade, no subagent, no background job,
no `agent://all`.

Inputs read: `plans/round-38-claims.md`; `corpus/lessons/round-37-verifier-spotcheck.md`;
`SCORECARD.md` (round-36 section, `## Owned axes`, `## Capabilities`); `LOG.md` tail; `SHONEN.md`;
`PROVINCE.md` (Core/Frontier/round-36 Core section); `tools/round-38/{c1-counter.py,c2-counter.py}`;
`.ufo/waves/round-38/{c1/carriers.json,controls/*.json}`; wave-1 seat artifacts (see §4).

## 0. Behavior, gates, touched surfaces

**Behavior.** Drafted the round-38 SCORECARD section and LOG entry, measured the pre-claim state
and the wave-1 draft receipts with read-only commands, and surfaced the conflicts that make a
verdict premature. No claim value was upgraded: every after value and every verdict is `[L1-FILL]`.

**Gates.**
- Claim gates (target not met yet, by design of this seat): C1 `carriers_matched == 4` and every
  binding true; C2 `mismatches == 0` and `guards_ok`.
- Freeze gates: the counter/predicate/carriers/oracle must stay byte-identical after `e059ca93`;
  **this gate is currently broken** — see D7.
- Draft gate for the capability row: only if the C1 landing stands and states the `sasquatch-v4be`
  dependency.
- No gate was reported as passed on the strength of a draft receipt.

**Touched surfaces (all outside the lane's scored files):**
`.ufo/waves/round-38/w1/R38ScribeScorecardDraft.md` (this report) and
`.ufo/waves/round-38/w1/artifacts/R38ScribeScorecardDraft/{scorecard-section.md,draft-carrier-clauses.tsv,draft-clauses.py,xpin-recompute-drafts.txt,xpin-recompute-drafts.err}`.
Nothing else written; no VCS mutation (the one modified tracked file, `tools/round-38/c1-counter.py`,
was already modified by another actor — D7).

## 1. Deliverable

**Draft text (this seat's only product):**
`.ufo/waves/round-38/w1/artifacts/R38ScribeScorecardDraft/scorecard-section.md`
(sha256 `f0166b3b7f6ce6b01311f0322075676e3aecde3efccf30d42381a2cf311cf0a3`, 120 lines)

It contains, as drop-in text:
- the SCORECARD section `## Round 38 — standard big-endian SquashFS v4 to Core, and self-assessment
  mismatch to zero`, with claim rows R38-C1/R38-C2 (axis/surface, before → after, exact counting
  command, `[L1-FILL]` measured-at, `[L1-FILL]` verdict);
- owned-scores restatement (coverage/depth/calibration 10 → 10, proxy counts named);
- a conditional `## Capabilities` row for BE-v4 SquashFS recursion with its entry rule;
- a LOG entry opening `## 2026-10-26 — round 38 (relaunch of round 37): …`;
- §C verdict placeholder table (inputs → command); §D limits.

Supporting artifacts in the same directory:

| file | sha256 | what it is |
|---|---|---|
| `draft-carrier-clauses.tsv` | `119876d261d2fecaf1d0dab879a218e7fb1de920d1fb4c22ae5504139c4bb754` | per-receipt clause table (subject pin, handler, gaps, oracle hits, coverage) for the 10 wave-1 draft envelopes |
| `draft-clauses.py` | `f6220a4d8e3c35d6a2079a4649e3cfe7fc6f8da2dc35571547889f3a96cf23cf` | read-only script that produced the table |
| `xpin-recompute-drafts.txt` | `4a5e572e560319d8f70b430c2dbb6b76ff7dab4a2634b8db13c87b708fa95309` | evidence-id recomputation for the same 10 envelopes |
| `xpin-recompute-drafts.err` | empty (sha256 of empty file) | stderr |

The draft marks every `measured at` and every verdict `[L1-FILL]`; no after value is written as
observed claim data, because no after receipt is committed under `corpus/evidence/round-38/` and no
landing revision exists.

## 2. Commands this seat ran (all read-only; exit codes as observed)

```
$ git ls-tree -r --name-only HEAD corpus/knowledge | grep -c '\.md$'
124
$ python3  (map/stem intersection over corpus/README.md '## Coverage map' vs corpus/knowledge/*.md)
map_stems 124 mapped 124 files 124
$ python3  (SKILL.md '## Queue-drain craft' rule blocks; citation resolution per counter rule)
rules 17 resolved 17
$ python3  (evidence/round-1-2026-10-15/result.json obligations)
command_b 9 / 9
$ grep -c '^|' corpus/SOURCES.md
113        # 111 data rows + header + separator
$ python3 -I -B .ufo/waves/round-38/w1/artifacts/R38ScribeScorecardDraft/draft-clauses.py --root .
carrier	variant	receipt	subject_ok	handler_ok	gaps	oracle_hits	oracle_rows	published	coverage
K1	seat	…/R38ExecAfterK1/after.json	yes	yes	1	0	5	0	partial
K1	seat-onpath	…/R38ExecAfterK1/after.sasquatch-on-path.json	yes	yes	0	5	5	5	partial
K1	patch	…/R38ExecProvincePatch/after-K1.json	yes	yes	0	5	5	5	partial
K2	seat	…/R38ExecAfterK2/after.json	yes	yes	1	3	3	3	partial
K2	patch	…/R38ExecProvincePatch/after-K2.json	yes	yes	1	3	3	3	partial
K3	seat	…/R38ExecAfterK3/after.json	yes	yes	1	0	4	0	partial
K3	seat-onpath	…/R38ExecAfterK3/diagnostic-after-with-declared-extractor.json	yes	yes	0	4	4	4	complete
K3	patch	…/R38ExecProvincePatch/after-K3.json	yes	yes	0	4	4	4	complete
K4	seat	…/R38ExecAfterK4/after.json	yes	yes	0	4	4	4	complete
K4	patch	…/R38ExecProvincePatch/after-K4.json	yes	yes	0	4	4	4	complete
exit=0        # receipt paths elided to "…"; full paths are in draft-carrier-clauses.tsv
$ node tools/round-27/xpin-attribute.mjs --pkg65 <rea-agents 6.5.0 root> --pkg67 <same> <10 wrapped envelopes>
exit=0; all 10 lines: stored = 6.5.0 = 6.7.0 = "both"
```

`scorecard-section.md` cites the base/freeze/tip counter receipts produced by seat
`R38ExecRecountBase` (`c1-at-base.json`, `c1-at-freeze.json`, `c1-at-tip.json`, `c2-at-base.json`,
`c2-at-tip.json`) — those are that seat's runs, not re-run here; the selftest counts in the LOG
draft are attributed to that seat's §3. The clause table and xpin run above are this seat's
measurement of *draft* envelopes only.

No install or upgrade was performed; nothing to add to the tooling ledger.

## 3. Before values written into the draft (provenance)

- C1 base `77091b49`: `carriers_matched 0`, `carriers_unchanged false` (only because
  `carriers.json` is absent at the base), `met_target false`, bindings all false except
  `frontier_note true`, exit 1 — `.ufo/waves/round-38/w1/artifacts/R38ExecRecountBase/c1-at-base.json`.
- C1 freeze `e059ca93`: same but `carriers_unchanged true`, exit 1 — `c1-at-freeze.json`; identical
  in every compared key to control `ctl-c1-0-do-nothing.json` (exit 1).
- C2 base: `mismatches 1`, `guards_ok false`, unresolved `[["prov_core:REA MCP server",
  "evidence/doctor/"]]`, 48 pointers, `missing_units []`, `pointers_not_fewer true`, 7/7 assertions
  agree; `observed`: command A `{knowledge_files 124, mapped 124, rule_blocks 17, resolved_rules 17}`,
  command B `[9,9]`, craft `[81,314]`, Adjacent `[97,125]`, exit 1 — `c2-at-base.json`.
- Controls: all seven receipts carry `"exit": 1`; C1 `carriers_matched` 0/3/0; C2 `mismatches` 1.
- Freeze `e059ca9391642d5b71b6662cabcbdce0d9308719` and controls commit
  `efd5c47a72a50b3a434783f82268fb4a96e636a1` are the values named in `plans/round-38-claims.md`
  and in the control `argv` blocks.

## 4. Findings — conflicts that block a verdict (reported, not repaired)

**D1 — K2 cannot satisfy `after_gaps_empty` as the carrier is constituted.** Both K2 draft
receipts (`R38ExecAfterK2/after.json`, `R38ExecProvincePatch/after-K2.json`) publish exactly the
3 oracle regular files, name `squashfs_v4_be`, and carry recomputing ids — and one
`extraction_gaps` entry:

```json
{"kind":"unpublished-entry","input_path":"$output/firmware.bin_extract/var/lib/run-link",
 "relative_path":"firmware.bin_extract/var/lib/run-link","handler":null,"provider_id":null,
 "range":null,"root_file_range":null,"dependencies":[],"continuation_id":"602c674b…"}
```

The frozen clause is `after_gaps_empty = gaps(env) == []` (`tools/round-38/c1-counter.py:177`), so
K2 `matched` is false and `carriers_matched` cannot reach 4 on these receipts. Seat report
`R38ExecAfterK2.md` reaches the same conclusion in its own words ("Under P38-C1 as frozen, K2 does
not match"). `[INFERENCE]` the gap is the committed symlink; the oracle lists only regular files,
so the counter does not distinguish "structural gap" from "lost member".

**D2 — the predicate's "no external extractor dependency" premise is falsified on these
carriers.** `R38ExecAfterK3.md` §2-3 (verbatim, condensed): arm A — clean `PATH` (no
`sasquatch`/`sasquatch-v4be`) — exit 0, handler `squashfs_v4_be`, `files []`, `coverage partial`,
1 gap `missing-extractor-dependency` `dependencies=["sasquatch-v4be"]`, **0/4** oracle files; arm C
— clean `PATH` plus a shim exposing **only** `sasquatch-v4be` — exit 0, `coverage complete`, 4
files, `gaps []`, **4/4**. K1 shows the same shape: `R38ExecAfterK1/after.json` (clean `PATH`) has
0/5 and a gap; `after.sasquatch-on-path.json` has 5/5 and no gap. K4's dep-probe shows
`env-nosasq-gap.json` (0 files, gap) vs `env-v4beonly-ok.json` (4/4, no gap). So stock unblob
26.6.4 does **not** decode BE v4 without the external binary, while the counter only inspects
`extraction_gaps`. A met verdict produced from on-`PATH` receipts would be true to the counter and
false to the sentence `plans/round-38-claims.md` freezes ("no external extractor dependency").
That decision belongs to the L1/closure; this draft writes neither met nor honest-stop.

**D3 — which file is "the" after receipt is unsettled for K1 and K3.** The seats' files named
`after.json` are the clean-`PATH` failing arms; the passing arms are siblings
(`R38ExecAfterK1/after.sasquatch-on-path.json`,
`R38ExecAfterK3/diagnostic-after-with-declared-extractor.json`,
`diagnostic-after-shim-only-extractor.json`, `harness-after-mode-post-fix-ok.json`). The
`R38ExecProvincePatch` directory holds a third complete quad (K1 5/5, K2 3/3 + gap, K3 4/4, K4 4/4,
all ids recompute). If the landing commits only `after.json` per carrier, `carriers_matched` is 0;
if it commits the on-`PATH` envelopes, K1/K3/K4 match and K2 still does not. Routed defect R37-CL1
("commit every receipt the report cites") makes this choice auditable but does not resolve it.

**D4 — the frozen harness could not produce an after receipt at freeze time.** At `e059ca93` and
`9c9d496b`, `tools/round-38/c1-run.sh` `after` mode ran `mkdir -p "$OUT"`; REA rejects an existing
output root (`"Extraction output root already exists"`, exit 1). Reproduced by
`R38ExecAfterK3.md` §5 (`harness-after-mode-failure.txt`), then fixed by the L1 in `cb4326b2`
during wave 1 (`rm -rf "$OUT"`), after which the fixed harness ran exit 0 with an ambient `PATH`.
The after receipts in wave 1 were therefore produced outside the frozen harness; the harness at the
freeze is not the harness that can be pointed at as the claim's procedure.

**D5 — carried counter blind spots confirmed at the freeze (from `R38ExecRecountBase.md` §4, not
re-measured here).** (a) `frontier_note` is a whole-file scan for a line containing `big-endian`
and `superseded`; `PROVINCE.md:156-157` already carries such a line whose clause says big-endian
"stays here", so the binding is green pre-claim and discriminates nothing. (b) `measure()` never
reads `c['path']`; carrier bytes are never hashed at `--rev`, so the receipt's self-declared
`subject.digest` is the only carrier tie (material is honest: the seat re-hashed all four committed
carriers against the pins, all match). (c) `carriers_unchanged false` at the base means "absent",
not "modified". These belong in the C1 verdict as disclosed limits, in the same class as the
carried R36-CL3/R36-CL5 blind spots.

**D6 — round 37 has no LOG.md or SCORECARD section.** `grep -n 'round 37\|round-37' LOG.md` →
no matches; the last SCORECARD round section is round 36 (`SCORECARD.md:3385`). The draft LOG
entry therefore introduces round 37 to `LOG.md` only through the verifier's spot-check file, and
says so. The `[L1-FILL]` census line stays because this seat did not read the census output.

**D7 — the frozen C1 counter is modified in the worktree during wave 1, repeatedly.** Observed
after the freeze `e059ca93` while this seat was running:

```
$ git status --porcelain
 M tools/round-38/c1-counter.py      # only modified tracked file
$ git diff --numstat
38	20	tools/round-38/c1-counter.py
$ git show e059ca93:tools/round-38/c1-counter.py | sha256sum
a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8  -
$ sha256sum tools/round-38/c1-counter.py     # 03:23:27 -03:00
211059785dc2a17a10f90d24505abdad5f85f671cbd0ff422e2dc8db1b8acf1e  tools/round-38/c1-counter.py
$ sha256sum tools/round-38/c1-counter.py     # minutes later, same seat
733be0168527fec193f70441752ef561e1f402789e6b67fd280547357a312967  tools/round-38/c1-counter.py
```

Peer seats recorded the same drift independently: `R38ExecSelftests.md` §4 "Live drift in the
frozen c1 counter (disclosed, not repaired)" with a timeline (`03:22:04` → `f27f982b…`), and
`R38MutC1/uncommitted-counter-diff-vs-HEAD.diff` / `uncommitted-counter-diff-snapshot2.diff`.
`R38ExecSelftests/selftest-runs.json` pins the frozen sha and runs a scratch mirror, precisely so
the selftest does not depend on the worktree.

The diff rewrites the predicate separator sentence ("stock unblob 26.6.4; no external extractor
dependency" → "sasquatch-v4be available, as unblob 26.6.4's `SquashFSExtractor` requires"), adds a
paired committed `before.json` per carrier that must publish none of the oracle and name
`sasquatch-v4be` as a missing extractor dependency, and moves the handler/gap checks onto the after
envelope. `plans/round-38-claims.md` says "the counter, predicate, carriers and oracle are never
changed after this commit"; the frozen blob is not what the path now executes, and the path does not
hold one stable value across the wave. A landing scored by running `tools/round-38/c1-counter.py`
today would score a predicate the freeze does not contain, with the exact code depending on when it
ran. Reported, not reverted (VCS mutation is outside this seat) and not run (neither version). The
draft §A0 instructs the L1 to either score the frozen blob or re-freeze the amended claim in a new
commit and say so.

## 5. Draft decisions the L1 must make before integrating

1. C1 verdict: met-under-frozen-rule (on-`PATH` receipts) vs honest stop (premise falsified) vs
   honest stop (K2 gap + receipt ambiguity). The counter itself can only return 0 or 1; the
   predicate's prose cannot be made true on these carriers by any receipt.
2. Whether the capability row is entered at all. The draft row states the `sasquatch-v4be`
   dependency explicitly, unlike the round-36 LE row; it must not be entered if C1 is an honest
   stop.
3. Which receipts are committed under `corpus/evidence/round-38/c1/` (R37-CL1) and whether their
   `output_directory`/`local_path` values (scratch paths) are acceptable as landed bytes — they
   recompute, but they name `/fast/scratch/...`.
4. Whether the owned coverage row is re-stated 124/124 → 125/125 in the same landing as the entry
   (the C2 counter's O1 assertion reads the stated pair; a stale 124/124 after the entry lands is a
   mismatch of the C2 class).
5. LOG bullet on routed defects (R37-CL1..CL3, R36-CL1..CL6) — the draft keeps it with
   `[L1-FILL: verify each landed fix against the freeze commit]` because this seat verified none of
   them.
6. Freeze-drift resolution (D7): score the frozen blob `e059ca93:tools/round-38/c1-counter.py`
   (sha256 `a7a62b09…`) or re-freeze the amended predicate/receipt shape in a new commit and cite
   the new freeze. The draft supports either, but not a silent mix.

## 6. Out of scope / not done

- No edits to `SCORECARD.md`, `LOG.md`, `PROVINCE.md`, `corpus/**`, `SHONEN.md`, `SKILL.md`,
  `plans/**`, `tools/**`.
- No commit, push, checkout, reset, stash, jj mutation; no `git add`.
- No REA invocation, no network fetch, no tool install.
- No counter run at a landing revision (none exists); no attempt to fill `[L1-FILL]` values.
- No verdict was upgraded: the clause table and id recomputation are labelled draft-stage inputs.

## 7. Scratch

`S=/fast/scratch/hyaku/kaidoku-r38/R38ScribeScorecardDraft` was created for the wrapped envelopes
and `TMPDIR`, and removed before this report (`ls` → "No such file or directory"). Cited values
live in lane artifacts only.
