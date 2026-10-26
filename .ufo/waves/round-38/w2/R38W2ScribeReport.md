# R38W2ScribeReport — draft round-38 report body from committed bytes

**Verdict: DEFECTS FOUND.** The two author verdicts survive their own receipts (C1 `carriers_matched 3`, `met_target false`; C2 `mismatches 0`, `guards_ok true`), but four landed surfaces do not survive a byte read: the C2 receipt the SCORECARD and lesson cite does not exist, the C1 "before" receipt was generated under the third freeze, `PROVINCE.md:372` still calls `sasquatch-v4be` "unmeasured", and the round's end census is absent. The draft body records all of them rather than repeating the surfaces.

Draft delivered: `.ufo/waves/round-38/w2/artifacts/R38W2ScribeReport/report-body.md` (229 lines). Sections: `Work performed` (opens with R38-C1/coverage and R38-C2/calibration from the first-freeze claims doc, then one bullet per work item with commit or `path:line`), `Landed changes` (each item tied to `LOG.md:3128-3134` and to `3b960fe5f9a7f1dfa22819f98dc0fa983f4260a8` or `0fc6113376a156fddc3ec385386d71c3a4a9f690`), `Before → after measurements` (one row per claim: counting command, measured revision, values, verdict), plus eight receipt notes the integrator must not file around.

## What was executed (read-only)

No counter, no REA call, no web fetch, no subagent dispatch, no install or upgrade. Lane worktree read, never written; VCS read-only.

- `git log --oneline -12`; `git show --stat 3b960fe5…`; `git show --stat 0fc61133…`; `git show e265533e --stat`.
- `git ls-tree -r HEAD --name-only .ufo/waves/round-38/l1/`; `git ls-files .ufo/waves/round-38/l1/scores/`; `git cat-file -e HEAD:.ufo/waves/round-38/l1/scores/c2-final.json` → `fatal: path … does not exist in 'HEAD'`, exit 128.
- `git show e059ca93:tools/round-38/c1-counter.py | sha256sum` → `a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8`; same for `plans/round-38-claims.md` → `13ea8eba…09815`, and `c2-counter.py` at freeze and HEAD → `7f137b66…7b0f7` (identical; `git log --oneline e059ca93..HEAD -- tools/round-38/c2-counter.py` is empty, while the same log for `c1-counter.py` lists `f1010f67` and `79f69347`).
- `python3` (stdlib only) over the committed receipts: `corpus/evidence/round-38/c1/K{1..4}/{before,after}.json` (bindings, gaps, engine, evidence ids), `.ufo/waves/round-38/controls/*.json` (all seven: `exit`, `output.revision`, values), `.ufo/waves/round-38/l1/scores/*.json`, `.ufo/waves/round-38/l1/freeze-drift-*.json`.
- Independent coverage recount: `corpus/knowledge/*.md` = 126; every stem occurs in `corpus/README.md` `## Coverage map` (`:11-93`) → 126 mapped, 0 unmapped, 0 map-only stems; `grep -c .` on the four `oracle.tsv` → 5/3/4/4 = 16.
- `git diff 77091b49 3b960fe5 -- PROVINCE.md`; `git diff 77091b49 0fc61133 -- SCORECARD.md`; `git show 77091b49:PROVINCE.md | sed -n '372p'` vs `sed -n '372p' PROVINCE.md` (identical).
- `git status --porcelain`; `git diff --stat HEAD`; `ls .ufo/waves/round-38/w1/*.md | wc -l` → 40; `git ls-tree -r 3b960fe5 --name-only .ufo/waves/round-38/w1/ | grep -c artifacts/` → 443.

## Findings (each verified against committed bytes)

1. **The C2 receipt cited by the scored surfaces is phantom.** `SCORECARD.md:3406` and `corpus/lessons/round-38.md:11` cite `.ufo/waves/round-38/l1/scores/c2-final.json`; it exists in neither `HEAD`, `0fc61133`, nor the worktree. The receipt actually produced is `.ufo/waves/round-38/l1/scores/c2-at-0fc61133.json`, untracked. `LOG.md:3130` is silent on the name. This contradicts the round's own R37-CL1 closure (`corpus/lessons/round-38.md:85-87`, "every receipt this round cites is committed … `.ufo/waves/round-38/l1/scores/`").
2. **The C1 "before" receipt is not a first-freeze run.** `SCORECARD.md:3405` describes `controls/ctl-c1-0-do-nothing.json` as "exit 1 at the freeze", but the receipt's `argv` records `--rev f1010f67… --freeze f1010f67…` (freeze v3). Its `output.carriers_matched 0` is consistent with the do-nothing arm (no receipts, no entry), but the receipt does not evidence the first-freeze arm it is offered for.
3. **The `frontier_note` binding was green before the round.** `c1-counter.py:208-209` at `e059ca93` tests any PROVINCE line containing both `big-endian` and `superseded`; `PROVINCE.md:157` already held both at base `77091b49`, and the committed control receipt shows `frontier_note: true` with `entry_present: false`. Consistent with wave-1 `w1/R38CriticClaimsC1.md` §4; it does not change the stop, which the carrier count and both Core bindings already force.
4. **`PROVINCE.md:372` still says `sasquatch-v4be` is "unmeasured"** — byte-identical at base and HEAD — while the landed entry, `corpus/README.md:239` and four before/after receipts measure it. The C2 counter cannot see prose, so this survives `mismatches 0`.
5. **The frozen predicate's premise contradicts its own receipts**: "run with stock unblob 26.6.4; no external extractor dependency" (`c1-counter.py:5-7` at `e059ca93`) vs before-arm `missing-extractor-dependency` [`sasquatch-v4be`] on all four carriers and after-arm publishing only with the binary reachable (M38-3). The counter scores receipts, not the premise, so C1's stop stands.
6. **The L1 C1 receipt names a scratch counter** (`/fast/scratch/hyaku/kaidoku-r38/l1/c1-counter-v1.py`) and stores no digest; identity rests on `SCORECARD.md:3405`'s `a7a62b09…`, which I verified equals the frozen blob. Whether the scratch copy held exactly those bytes is not recoverable from committed bytes [INFERENCE limit].
7. **No end census**: `corpus/lessons/round-38.md:66` promises it "in the report"; only `.ufo/waves/round-38/census-start.txt` exists.
8. **Live worktree drift during drafting**: three tracked corpus files modified after HEAD (`corpus/lessons/round-38.md`, the two round-38 knowledge entries; `git diff --stat HEAD` = 17 insertions / 13 deletions) and untracked `paths_raw.txt` at lane root. The `Vendor:` statistic is stated two incompatible ways (HEAD: "42 occurrences of the word"; worktree: "42 of 97 sections carry one `Vendor:` field"), and the worktree lesson cites an `M38-5` that has no table row (`grep -c '^| M38-'` → 4 at both revisions). Not repaired by me; line numbers in the draft are HEAD's and shift with that commit.

Consistent with the receipts as read (not re-measured): C1's `carriers_matched 3` with K2's single `unpublished-entry` gap (`firmware.bin_extract/var/lib/run-link`, symlink target `../../a/run.sh`) and both Core bindings false; C2's `mismatches 0`, `guards_ok true`, `pointers 52` vs `base_pointers 48`, command A 126/126 and 17/17, command B `[9,9]`, ranges `[81,314]`/`[97,125]` at `0fc61133`.

## Bounds and writes

- Files written: `.ufo/waves/round-38/w2/R38W2ScribeReport.md` (this report) and `.ufo/waves/round-38/w2/artifacts/R38W2ScribeReport/report-body.md`. Nothing under `corpus/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `tools/`, no VCS mutation, no sibling lane, no `shokuknow`.
- **Disclosure:** my first `write` used a path relative to the workspace root, which created `/home/vgpnk/Projects/shokunin/.ufo/waves/round-38/w2/artifacts/R38W2ScribeReport/report-body.md` outside the lane. I detected it in the next read, copied the file into the lane, and removed the stray tree I had created (`rm -rf /home/vgpnk/Projects/shokunin/.ufo/waves/round-38`; the pre-existing `.ufo/waves` and its siblings were untouched — verified `ls: cannot access … round-38: No such file or directory`, and the lane copy is the one edited afterwards).
- Scratch: none created (`/fast/scratch/hyaku/kaidoku-r38/R38W2ScribeReport` unused); no `/tmp` files.
- Tools installed or updated: none. No pacman, no npx, no uv, no subagents, no `agent://all`.

## Out of scope / not done

Report status line, `Sources & frontier`, `Trend verdicts`, `SHONEN`, end census and any `corpus/` repair belong to the L1 (`KaidokuR38a2`). I did not re-run either counter, open any web source, re-open S116, or re-derive the REA receipts; the draft is a reading of committed bytes, and every place that could not be settled from them is marked in the artifact.
