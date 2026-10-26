# R36ScribeLessonMistakes — draft `## Mistakes` rows for `corpus/lessons/round-36.md`

Seat `R36ScribeLessonMistakes` (scribe, leaf). 2026-10-26. Advisory draft only: this report is the
only file written. `corpus/lessons/round-36.md` does not exist at HEAD `d2e46ef5`, so the block below
is paste-ready text for the L1, not a landed edit.

Lane state when read: HEAD `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be` (2026-10-26 01:27:16, "round-36:
R36-C2 self-assessment repairs"), on top of `3310d8fa` / `6a870b92` / `790561d4`. Base `cab59f22`.
Nothing installed or updated; no scratch directory created (no clone, download, fixture or REA run);
no lane counter, gate or selftest executed — every number below comes from read-only `git`
(`show`, `log -S`, `ls-tree`, `rev-parse`, `grep`, `sed`) and from already-committed receipts.

Row ids: round 35 used `M35-1..M35-4`, so this block proposes `M36-5..M36-7`. If a sibling scribe
seat lands the round-35 closure defects (`R35-D1..D5`) as `M36-1..M36-4`, the L1 must renumber one
block so ids stay unique and sequential; the rows themselves do not refer to each other by id.

---

## Draft block (paste into `corpus/lessons/round-36.md`)

```markdown
## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M36-5 | stale packaging-route premise carried as prose | `PROVINCE.md:149-150` ("unblob's squashfs recursion extractor (AUR-only)") and `corpus/README.md:227` ("sasquatch (AUR) — …") entered in the round-4 commit `999ce123` (2026-10-13 14:17:42 -0300) and were still byte-identical at base `cab59f22` and at HEAD `d2e46ef5`; `git log -S'AUR-only' -- PROVINCE.md` and `git log -S'sasquatch (AUR)' -- corpus/README.md` each return that one commit and no other. The Debian route existed before the sentence: onekey-sec publishes `sasquatch_1.0_amd64.deb` since tag `v1.0` (2022-02-26) and amd64/arm64/armhf + dbgsym since `sasquatch-v4.5.1-6` (2026-01-27) — `/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/sasquatch-prebuilt-package-inventory.md`, re-checked 2026-10-26 in `.ufo/waves/round-36/w1/R36ScoutPrebuiltInventory.md` (API `jq length` = 8; newest tag 6 assets; deb control `Version: 1.0`; installed binary reports `unsquashfs version 4.5.1`). The lane held no source row for the project at all: `git show cab59f22:corpus/SOURCES.md \| grep -cE '(sasquatch\|onekey-sec)'` = 0 (exit 1; max lane id `S106`), and the merge-KB `S130` is that KB's numbering, not the lane's | the round-36 inventory and unblob-README scouts (`.ufo/waves/round-36/w1/R36ScoutPrebuiltInventory.md`, `R36ScoutUnblobReadme.md:45,53,59` — the latter marks the "(AUR)" wording as lane-side and not checked by either upstream README); no lane rule existed to catch it | New QUALITY row: an operator-facing availability/packaging sentence names a channel only when an admitted `corpus/SOURCES.md` row opens the distributor's own release/asset listing, quotes the asset matrix, and carries `opened` + `recheck` dates; each round's doc sweep re-derives such sentences from that row instead of carrying them forward. Fails when the project has no admitted row (base: 0 rows, grep exit 1), when the quoted matrix contradicts a scope word (`only`, `missing`, `blocked`, `AUR-only`), or when the row is past its recheck interval. Able to fail: red at base on committed bytes — `PROVINCE.md:149` + `corpus/README.md:227` assert a channel while the SOURCES grep exits 1; the binding discipline is code-defined red in the frozen C1 selftest (`tools/round-36/c1-counter.py:321-324`, cases `S-id substring S1070`, `source row opened earlier`, `used-by lacks entry`, `coverage map lacks stem`, each expected exit 1) but **no selftest output is committed at HEAD** (`.ufo/waves/round-36/controls/` holds only the seven control receipts from `6a870b92`), so that half of the receipt is owed |
| M36-6 | present-tense scorecard count measured at a pinned revision | `SCORECARD.md:23` at base states `116/116 knowledge files mapped at c369242f…`; the C2 base receipt `.ufo/waves/round-36/controls/ctl-c2-0-do-nothing.json` (committed `6a870b92`) records `stated [116,116]` vs `observed [122,122]`, `mismatches: 3`, `met_target: false`, and `.out` ends `ctl-c2-0-do-nothing exit=1`. The pinned revision is honest (`git ls-tree -r --name-only c369242f \| grep -c '^corpus/knowledge/2026'` = 116) but the row was already two behind at its own commit `1288285e` (same command = **118**), and six entries landed between `c369242f` and `cab59f22` (`0007731e` +2, `bb0af56c` +1, `d7076120` +1, `8897a67f` +1, `66b84027` +1), so rounds 31-35 carried a number one `grep -c` could have corrected. The row's own history text had already recorded the class: "78/78 at `3395b6d` (luna-round-7; the row kept that revision until round 26)" | the round-36 C2 counter at the base (`tools/round-36/c2-counter.py:197`, check `O1 coverage mapped/files`); first instrument in the lane to compare a stated pair with an observed pair | State a current count recomputed at the tip beside the dated history, and run the existing one-line recipe-A recompute in the filing step so a mismatch stops the filing. Able to fail: committed reds `ctl-c2-0-do-nothing.json`/`.out` (116 vs 122, 3 mismatches, exit 1) and `ctl-c2-1-junk-count.json`/`.out` (999 vs 122, exit 1), both at `6a870b92`; code-level reds at `tools/round-36/c2-counter.py:287` (`junk count`), `:288` (`count deleted`), `:296` (`calibration count wrong`). Limit read from code: `stated()` uses `re.search` on the cell (`c2-counter.py:192-197`), so the **first** `N/N knowledge files mapped` decides; history must stay after the current count or the counter reads the old number and emits a false red |
| M36-7 | round filed before the lane tip it describes | fleet commit `33be25b89c2ac4633e5bf62a586008ca7b4e1a54` ("round-35: kaidoku report", 2026-10-25 16:20:58 -0300) precedes the lane's last round commit `3ca5a80f` ("round-35: land w1 results, dispatch and remaining wave artifacts", 16:43:52 -0300) and the closure `3b1ab3c9` (17:29:52); `git log -1 --format=%ct` gives 1792956058 vs 1792957432, so a `lane_tip <= report_commit` test exits 1. The report says so itself: `.ufo/reports/round-35/kaidoku.md:56` "Round-35 wave has not settled at filing cutoff, so the seat-result ledger and independent non-author claim closure remain outstanding", and it carries no `prefile` line at all (`grep -c prefile` = 0) although `corpus/QUALITY.md:57` (row 47) requires `tools/round-29/prefile-check.sh` to exit 0 immediately before the report commit **with its output in the report**. Round-35 wave artifacts were still arriving when the report landed: 76 round-35 files are tracked at `3ca5a80f`, and 14 remained untracked per `corpus/lessons/round-35-verifier-spotcheck.md` | round-35 outside verifier, defect `R35-D5` (`corpus/lessons/round-35-verifier-spotcheck.md`, closure commit `3b1ab3c9`); QUALITY row 47 existed and was unmet | The report names `lane_tip` (40 hex); a step that runs **after** the report commit asserts `git -C LANE rev-parse HEAD` equals it, `git -C LANE status --porcelain` is empty and no new `.ufo/waves/round-N/` path appeared; a late artifact is appended as an erratum with its own cutoff (R35-D5), never folded into the filed report. Able to fail: the r35 pair is the committed red instance (`33be25b8` vs `3ca5a80f`, ordering test exit 1, reproducible from the two hashes above). `tools/round-29/prefile-check.sh` cannot cover it — it checks only tree cleanliness and the two freeze ledgers at HEAD, and it runs before the report commit. This rule has no committed instrument receipt yet; the lane's own standard for gate credibility (`prefile-gate-at-filings.txt`, r26/r27/r28 filings exit 1) is a real red receipt, so this rule should ship with one |
```

---

## Evidence docket

### (a) `sasquatch (AUR-only)` — rounds 4→36, no admitted source row

```
$ git log --format='%h %ci %s' -S'AUR-only' -- PROVINCE.md
999ce123 2026-10-13 14:17:42 -0300 kaidoku r4+r4u: audit r3 (10 errata) + expansion + unlock wave integrated
$ git log --format='%h %ci %s' -S'sasquatch (AUR)' -- corpus/README.md
999ce123 2026-10-13 14:17:42 -0300 kaidoku r4+r4u: ...
$ git show cab59f22:PROVINCE.md | grep -n 'AUR-only'
149:- **sasquatch** — unblob's squashfs recursion extractor (AUR-only); 7z fallback
$ git show cab59f22:corpus/README.md | grep -n 'sasquatch (AUR)'
227:- sasquatch (AUR) — unblob squashfs recursion; 7z fallback covers today.
$ git show HEAD:PROVINCE.md | sed -n '149,150p'      # HEAD = d2e46ef5
- **sasquatch** — unblob's squashfs recursion extractor (AUR-only); 7z fallback
  covers the carved-image path today.
$ git show cab59f22:corpus/SOURCES.md | grep -cE '(sasquatch|onekey-sec)'
0            # exit 1
$ git show cab59f22:corpus/SOURCES.md | grep -oE '^\| S[0-9]{3} ' | sort -V | tail -1
| S106
```

`-S` returning exactly one commit is the counting evidence that the string's occurrence count never
changed from `999ce123` through HEAD: no later round edited the sentence, including the round-36 C2
repair commit `d2e46ef5`, which touched `SCORECARD.md` only. The packaging fact is upstream-dated, not
lane-derived: tag `v1.0` (2022-02-26, `sasquatch_1.0_amd64.deb`), tag `sasquatch-v4.5.1-6`
(2026-01-27, six assets), re-verified live on 2026-10-26 by the wave-1 scout (`jq length` = 8, per-tag
asset counts, deb control `Version: 1.0`, payload `./usr/bin/sasquatch`, `-version` →
`unsquashfs version 4.5.1 (2022/03/17)`). Round 36's own install (`3310d8fa`, sasquatch 4.5.1 from
the official deb into `~/.local/bin`) is the first use of that route in the lane.

Host-applicability caveat, so the fix is not oversold: on this Arch host the AUR is the
package-manager-native route and `dpkg` is absent (`R36ScoutUnblobReadme.md:45`), so "AUR-only" was
wrong as a claim about upstream publication, not as a claim about this host's package manager. The
gate above tests the publication claim (asset matrix), which is what the sentence asserted.

### (b) `116/116` vs `122/122`

```
$ cat .ufo/waves/round-36/controls/ctl-c2-0-do-nothing.json
 "assertion_mismatches": [{"check": "O1 coverage mapped/files", "observed": [122,122], "stated": [116,116]}]
 "mismatches": 3, "guards_ok": false, "met_target": false, "revision": "cab59f22..."
$ cat .ufo/waves/round-36/controls/ctl-c2-0-do-nothing.out
{"assertion_mismatches": [... "observed": [122,122], "stated": [116,116] ...], "mismatches": 3, "met_target": false, ...}
ctl-c2-0-do-nothing exit=1
$ git ls-tree -r --name-only c369242f | grep -c '^corpus/knowledge/2026'
116
$ git ls-tree -r --name-only 1288285e | grep -c '^corpus/knowledge/2026'      # the row's own commit
118
$ git ls-tree -r --name-only cab59f22   | grep -c '^corpus/knowledge/2026'
122
$ git log --diff-filter=A --format='%h %ci %s' --name-only c369242f..cab59f22 -- corpus/knowledge/
0007731e ... round-31: entries (C1 positive, C2 refusals) ...      corpus/knowledge/2026-10-23-r31-sqlite-{positive,refusals}.md
bb0af56c ... round-32: bounded ARM64X ...                          corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md
d7076120 ... round-33: stop safety-held claim ...                  corpus/knowledge/2026-10-23-r33-chpe-structural-profile.md
8897a67f ... round-34: source-backed ELF reader ...                corpus/knowledge/2026-10-23-r34-elf-version-needs.md
66b84027 ... round-34: land the stopped claim's record ...          corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md
```

The row's stated pair is reproducible at its pinned revision (116), so this is not a fabricated
number — it is a present-tense axis score carrying a five-round-old measurement. The repair landed in
`d2e46ef5` (`SCORECARD.md:23` now reads `122/122 … at cab59f22`, with `116/116 at c369242f` and
`109/109 at ebe2cb4a` kept as dated history).

### (c) report before tip

```
$ (lane)  git log --format='%h %ci %s' -1 3ca5a80f
3ca5a80f 2026-10-25 16:43:52 -0300 round-35: land w1 results, dispatch and remaining wave artifacts
$ (fleet) git log --format='%h %ci %s' -1 33be25b8
33be25b8 2026-10-25 16:20:58 -0300 round-35: kaidoku report
$ grep -n 'not settled' /home/vgpnk/Projects/shokunin/.ufo/reports/round-35/kaidoku.md
56:... Round-35 wave has not settled at filing cutoff, so the seat-result ledger and independent
   non-author claim closure remain outstanding. ...
$ grep -c 'prefile' /home/vgpnk/Projects/shokunin/.ufo/reports/round-35/kaidoku.md
0
$ lt=$(git log -1 --format=%ct 3ca5a80f); rt=$(git -C .../shokunin log -1 --format=%ct 33be25b8)
lane_tip=1792957432 fleet_report=1792956058 ; [ "$lt" -le "$rt" ] -> exit 1
```

`tools/round-29/prefile-check.sh` header (read, not run) states its three steps: `git status
--porcelain` empty, round-24 freeze gate `--disclosures corpus/claim-freezes.tsv` at HEAD, round-29
gate on `corpus/claim-freezes-v2.tsv` when present — no clause about commit ordering or about the
report's own repository, so the r35 failure was outside its reach even had it been run and recorded.

---

## Status of the round-36 `## Mistakes` requirement

- The three requested rows are drafted above with class, evidence, capture and fix as separate cells
  in the round-34/35 table shape.
- Able-to-fail status: (b) and (c) each carry a committed red (a control receipt and a hash pair
  respectively); (a) carries a red that is reproducible from committed bytes but no committed
  instrument receipt, and its nearest code-level reds are the frozen C1 selftest cases whose output
  is not yet committed. All three fixes are therefore honestly split into "red receipt exists" and
  "red receipt owed", not blanket-claimed.

## Additional candidate rows / findings for the L1 (not in the draft block)

1. **Declared surface ≠ scored surface (candidate M36-8).** `plans/round-36-claims.md` R36-C1 names
   the frozen surface as the `PROVINCE.md` Frontier bullet and the `corpus/README.md` Firmware row,
   but the frozen bindings (`tools/round-36/c1-counter.py:199-230`) score only
   `province_core_section`, `province_core_row` (a new `## Round-36 additions to Core` row naming
   `sasquatch` and the entry), `entry_present`, `sourced` (a `corpus/SOURCES.md` row opened
   `2026-10-26` whose used-by lists the entry) and `coverage_map_row`. Nothing reads the Frontier
   bullet or the Firmware row, so C1 can reach `met_target` while `PROVINCE.md:149` still says
   "(AUR-only)" — which it does at HEAD. The predicate is frozen and must not be changed; the row is
   for the next round's claim design (an assertion that a surface moved needs that surface's diff,
   the same shape as QUALITY 65 for "unchanged").
2. **Row-format is load-bearing for the count check.** `c2-counter.py:192-197` takes the first
   `(\d+)/(\d+) knowledge files mapped` in the `Owned axes` coverage cell. Any future edit that puts
   history before the current count flips O1 to a false red; a future counter should select by the
   revision token it scores, not by prose order.
3. **Registry split.** The merge-KB row `S130` (`sasquatch-prebuilt-package-inventory`) has no lane
   counterpart: the lane's registry stops at `S106` at base and holds zero sasquatch/onekey rows.
   Round 36's C1 requires a lane row opened 2026-10-26, so the merge row and the lane row will carry
   different ids for the same upstream page; the lesson should say which registry a citation resolves
   in, or a reader will check the wrong one.
4. **The merge entry is already known-defective as written.** `R36ScoutPrebuiltInventory.md` refuses
   it on two packaging claims (asset generality "each carrying a Debian package per architecture" is
   false for `v1.0`, amd64-only; the `4.5.1`/`1.0` split is not in the release body) and recommends
   "admit only after correction". If the round admits the corrected row, the correction — not the
   original — is what the new QUALITY row should bind to.

## Out of scope

- No re-run of C1/C2 counters, selftests, `c1-run.sh`, `prefile-check.sh`, `freeze-gate.py` or any REA
  command; no claim, counter, carrier, oracle, predicate or QUORUM value touched.
- No edit to `corpus/lessons/round-36.md` (does not exist), `SCORECARD.md`, `PROVINCE.md`,
  `corpus/README.md`, `corpus/SOURCES.md` or `corpus/QUALITY.md`; no VCS operation.
- Not asserted: whether the r36 entry will cite the corrected merge row; whether `sasquatch 4.5.1`
  satisfies unblob 26.6.4 (C1 sibling seats own that); anything about AVM/big-endian SquashFS or 7z
  fallback.

## Artifact paths

- This report: `.ufo/waves/round-36/w1/R36ScribeLessonMistakes.md` (untracked at HEAD; the whole
  `.ufo/waves/round-36/w1/` tree is `??` in `git status --porcelain`).
- Committed receipts cited: `.ufo/waves/round-36/controls/ctl-c2-0-do-nothing.{json,out}` and
  `ctl-c2-1-junk-count.{json,out}` at `6a870b92`; `corpus/lessons/round-35-verifier-spotcheck.md`
  (closure `3b1ab3c9`); fleet `.ufo/reports/round-35/kaidoku.md` at `33be25b8`.
- Read-only external input: `/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/sasquatch-prebuilt-package-inventory.md`.
- No scratch directory was created, so none was left to remove.
