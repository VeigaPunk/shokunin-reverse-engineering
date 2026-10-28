# R44W2LessonGate — round-44 lesson audited against the frontier-step contract

**Seat:** `R44W2LessonGate` (audit only: no claim, counter, rubric, frozen byte or production doc touched).
**Lane:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
**Audit target (pinned):** `corpus/lessons/round-44.md` at commit `f370592b`, blob sha256
`2e4c22d24ba4187f7b725e848bdaa535eed2b3ad9f3e9e6dcc8c6a64e88dd379`, **150 lines**; lane tip `4503fb78` (adds one w2 artifact only).
**Revisions used by the lesson:** base `c29360e3ba5381a5ab69e372d0d9577970f85018`, freeze `c48f8a4bfd449300c975668e59aae5b5538b6a84`, measured `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`.
**Contract source:** the wave-2 assignment's frontier-step checklist — `## Mistakes` (class · evidence · captured-by · fix, every fix *shown able to fail*), `## Gate` (URL + access date + ≤25-word located quote per new row; ≥1 admit + ≥1 reject with reasons), `## Carried debt` (every still-open id vs the 28 in `w1/R44Debt.md`), census before→after with command **and exit codes**.
**Report revision:** this is the final text. The copy committed at `f370592b` is an earlier draft of the same
seat; the L1 should commit this worktree version.
**Receipts:** `.ufo/waves/round-44/w2/artifacts/R44W2LessonGate/probe-receipts.json` (28 probes: seat, exact argv, cwd, exit, wall s, stdout bytes + sha256, stderr bytes + sha256), `preflight-fixture-probes.json`, `supplementary-probes.json` (mtimes, replay flags, bindings), `final-tip-4503fb78-counters.json`, plus the reproduced preflight JSONs. Probes are cited below as `P<n>`.

> **Audit-target drift (recorded, not a defect by itself):** the lesson changed three times while this seat ran:
> `d48af63c` (as committed at `8bb1090a`, 102 lines) → `1d80844d` (at `923fa870`, 143 lines) → `2e4c22d2`
> (at `f370592b`, 150 lines). Every finding below was re-verified against `2e4c22d2`; two defects that the
> first snapshot had (`M44-2` "added/edited 8 files" — all eight were `M`; unsupported chronology) are fixed
> in the final bytes and are **not** reported.

## Verdict

| checklist item | verdict |
|---|---|
| `## Mistakes`: class · evidence · captured-by · fix, all rows | **shape pass** — 3 rows, 5 cells each (`awk -F'\|'` → 5); content defects D8, D9, D10, D11 |
| M44-1 fix *shown able to fail* | **weak** — the red/green pair demonstrates the defect (verified), but no fix mechanism exists to fail (D8, and D6 for the debt row) |
| M44-2 fix *shown able to fail* | **PASS, verified** — RED exit 1 / 8 paths at `c86ea508`, GREEN exit 0 at `55bcce69`, both JSON-identical to the committed receipts (P1, P2); the tool also reds `A` and delete+restore in a throwaway fixture; both counters exit 2 with the same 8 paths — as committed at `c86ea508` (`c1/c2-score-at-tip.json`, P26) and re-run at `4503fb78` (`final-tip-4503fb78-counters.json`) |
| M44-3 fix *shown able to fail* | **PASS, verified** — C2 at `8bb1090a` exit 2 with **9** paths incl. `SCORECARD.md` (I reproduced: stdout sha256 `0a81b8b2…`, matching `w2/artifacts/R44W2C1Satisfy/tip-timings.json`); at `923fa870` **8** paths, `SCORECARD.md` absent (reproduced; identical to `l1/c2-score-at-final-tip.json`, whose `revision` is `923fa870`), and the same 8 at `4503fb78` |
| `## Gate`: URL + access date + ≤25-word located quote, S138 + S139 | **FAIL** — S138's cited manifest digest matches no committed object (D1), its "opened" cell is a replay of subdirectory listings of a URL never fetched (D3), and its "12 words" is 10 (D4); S139 has no located quote and no capture pointer although both exist (D2) |
| `## Gate`: ≥1 admit + ≥1 reject with reasons | **pass on shape**; admit evidence over-claims an instrument (D5). Reject reasons and slice digest `7383a90e…28e6a` check out against `w1/R44Quarantine.md:5` |
| `## Carried debt`: 28 D-ids | **28/28 present, none dropped**; D-27 wrongly closed (D6); prior-round ids incomplete/inflated (D12) |
| census before→after, command + exit codes | **numbers verified** (137→139; 13→14 W04); **record defective** — no exit codes for the row counts and the round-start claim has no receipt (D7) |

R44-C1's stop and R44-C2's 80/80 are other seats' surfaces; this file only asks whether the record says what happened.

**Defect index, in document order:** D8 · D9 · D10 · D11 (`## Mistakes`) | D1 · D2 · D3 · D4 · D5 (`## Gate`) | D6 · D12 (carried debt) | D7 (census) | D13 (preflight wiring). Each is numbered once as a `###` block and cited from the table above.


---

## 1. `## Mistakes` (lines 17–19)

Header at `:15`, rows `M44-1`, `M44-2`, `M44-3`; all three parse to 5 cells.

| row | class | evidence pointer | captured-by | fix | fix shown able to fail |
|---|---|---|---|---|---|
| M44-1 (`:17`) | `stale-premise` | probe-404 receipt + reproduced pair — all four artifacts exist and hash as quoted except one attribution slip (D11); receipt present at `c48f8a4` (`git cat-file -e` exit 0; introduced at `2081dc06`, an ancestor) | holds the **remediation** ("the frozen-URL convention") | holds the **demonstration** ("the red/green pair above…") | **weak** (D8) |
| M44-2 (`:18`) | `freeze-violation` | `git show -s --format='%h %ad %cd' c86ea508 55bcce69` → author `09:57:16`, committer `10:43:43` (verified, P24); fixture mtimes `09:50:09`–`09:50:30` (verified: `supplementary-probes.json` probe 1, `stat -c '%y'` exit 0); preflight receipt 8 paths; counters agree (P26) | "none — … the only enforcement sat inside the scoring counter" | preflight + red/green receipts | **yes — reproduced (P1/P2)**; parenthetical defect D10 |
| M44-3 (`:19`) | `freeze-violation` (self-inflicted by the record) | `w2/R44W2C1Satisfy.md` D-3 + rubric note; 9-vs-8 path counts reproduced independently | rubric's own note | ledger moved to `LOG.md`; SCORECARD restored | **yes — 9→8 reproduced**; class-label defect D9 |

Verified positives, all re-derived here:

- RED `python3 tools/round-45/frozen-path-preflight.py --root <lane> --freeze c48f8a4… --rev c86ea508… --pathspec tools/round-44` → **exit 1**, `verdict frozen_path_changed`, `touched 8`, `blob_changed 8`, JSON **identical** to `.ufo/waves/round-44/l1/preflight-c86ea508.json` (P1).
- GREEN `--rev 55bcce69…` → **exit 0**, `verdict clean`, identical to `preflight-55bcce69.json` (P2).
- Both counters at `4503fb78`: C1 exit **2**, C2 exit **2**, each 8 `frozen_path_changed` paths, byte-identical lists; `SCORECARD.md` absent (committed tip receipts P26; re-run in `final-tip-4503fb78-counters.json`). "Admissible only at `55bcce69`" is therefore accurate.
- M44-3: C2 at `8bb1090a` → exit 2, **9** paths including `SCORECARD.md`, stdout sha256 `0a81b8b2…` (matches the seat receipt); at the restored tip → 8 paths without it. The remedy is real and observable.
- The 8 frozen paths at `55bcce69` equal their freeze blobs (`git rev-parse c48f8a4:<p>` == `55bcce69:<p>` for the control-fixture manifests tested), consistent with GREEN (P2).

### D8 — M44-1's `captured-by`/`fix` cells are swapped and the fix is not a mechanism

- **Path:line:** `corpus/lessons/round-44.md:17` (cells 4–5); `.ufo/waves/round-44/w1/R44Debt.md:76` ("enforced by **seat discipline**, not by the tooling").
- **Command / exit:** `ls tools/round-45/` → only `frozen-path-preflight.py`; no URL linter anywhere under `tools/round-44` or `tools/round-45`.
- **Observed:** the `captured-by` cell carries the remediation ("the frozen-URL convention: a URL is pinned only after a successful open of its listing, never guessed"); the `fix (shown able to fail)` cell carries the demonstration (`grep -c 'squashfs_v2.0_be.expected'` = 0 in the 200 page, exit 1, P16).
- **Impact:** the fifth column contains no remediation for the row, and the only thing "shown able to fail" is the original error. A future guessed URL meets no instrument.
- **Smallest remediation:** move the convention into the `fix` cell and label it "process only, no executable arm (D-27 open)", or land a URL-cell linter with one red control (which would also close D-27).

### D9 — M44-3's `freeze-violation` label contradicts the claim's frozen-path list, and the remedy is a restore the rule forbids

- **Path:line:** `corpus/lessons/round-44.md:19`; `plans/round-44-claims.md:311-320`; the claims' freeze-integrity rule in `plans/round-44-claims.md` ("a later restore does not un-block (exit 2 `frozen_path_changed`, never `met_target`)").
- **Command / exit:** `sed -n '318p' plans/round-44-claims.md` → "`SCORECARD.md`, `SHONEN.md`, `corpus/README.md`, …" under the heading **"NOT frozen — BASE-pinned in the C2 rubric"**; `git show HEAD:SCORECARD.md | sha256sum` == `git show 55bcce69:SCORECARD.md | sha256sum` (`5828347b…`); C2 at the tip lists 8 paths, `SCORECARD.md` absent (`final-tip-4503fb78-counters.json`).
- **Observed:** the breach was of `tools/round-44/c2-rubric.json` `expected_edits["SCORECARD.md"]` (a rubric-bound 7-line append + blank separator = the 8-line diff), not of a byte-frozen path; and the remedy ("restored to the `55bcce69` blob") is exactly the "later restore" the frozen rule says must not un-block. The C2 counter *did* un-block on the restore.
- **Impact:** the class label overstates the violation (SCORECARD is not frozen by the claim), while the remedy normalises a restore the claim text forbids — two different rules are being conflated, and the next round cannot tell which one binds.
- **Smallest remediation:** label M44-3 `rubric-bound-edit` (not `freeze-violation`), and state that the restore un-blocks only under the C2 counter's blob-equality tolerance, which contradicts the claim's restore rule (route that contradiction as a defect).

### D10 — M44-2's "graded surface was already non-frozen while `55bcce69` scored"

- **Path:line:** `corpus/lessons/round-44.md:18`.
- **Command / exit:** preflight at `55bcce69` → **exit 0**, `blob_changed []` (P2); `git rev-parse c48f8a4:<p>` vs `55bcce69:<p>` for control-fixture manifests → identical.
- **Observed:** the *graded revision* was frozen; what was dirty from 09:50 onward was the **worktree**. Counters read commits (`--rev`), so the score cannot be contaminated by worktree dirt.
- **Impact:** the parenthetical invites the opposite inference — that the admissible score itself is tainted — which is the one claim a reader must not be left to guess about.
- **Smallest remediation:** "the worktree was already dirty from 09:50; the graded commit tree was not (`preflight-55bcce69.json`, exit 0)".

### D11 — M44-1 attaches one digest to a two-file group, and its frozen red arm is not self-describing

- **Path:line:** `corpus/lessons/round-44.md:17`.
- **Command / exit:** `sha256sum` on the three artifacts (P15): `guessed-expected-404.body d5558cd4…512ed`, `tree-200.html e3ea23b9…2f46`, `member-names.txt 99232795…0176`; `git show HEAD:…/probe-fixture-404.txt | xxd` → 14 bytes, `404: Not Found`, no URL/argv/exit/digest.
- **Impact:** the parenthetical digest covers only the HTML; and the frozen receipt cannot tie itself to the URL it is supposed to evidence — authenticity rests on the later wave-1 reproduction.
- **Smallest remediation:** one digest per file, plus a metadata sidecar (URL, argv, exit, digest, timestamp) or an explicit note that the l1 file is a body-only copy.

---

## 2. `## Gate` (lines 25–28)

Only two rows are new: `git diff c29360e3..HEAD -- corpus/SOURCES.md` is `3 0` (S138, S139, blank).

| requirement | S138 (`:27`) | S139 (`:28`) |
|---|---|---|
| URL | matches `corpus/SOURCES.md:144` | matches `corpus/SOURCES.md:145` |
| access date | `2026-10-28T11:10:29Z–11:12:37Z` — but see D3 (replay + subdirectory listings; the cited URL itself never fetched) | `2026-10-28` only — no time, no receipt pointer (D2) |
| ≤25-word located quote | 10 words labelled **12** (D4); the prose quoted is `manifest.source.grounds` in the repo, not page text | 11 tokens; the page-derived element is the bare tag, no anchor; the rest is `/usr/bin/unsquashfs` output (D2) |
| content address | manifest sha256 `4bc53dbb…c1a13` — **matches no committed object** (D1) | `/usr/bin/unsquashfs` sha256 `461e1fd9…b1677c` — **correct**: equals `carriers.json.toolchain.unsquashfs` and the live binary (P23) |
| admit / reject | admit (see D5 for the over-claim); reject with per-row reasons and slice digest matching `w1/R44Quarantine.md:5` | same |

### D1 — HIGH: the S138 Gate row cites a manifest sha256 that exists nowhere

- **Path:line:** `corpus/lessons/round-44.md:27` — "manifest `corpus/evidence/round-44/oracle/manifest.json` sha256 `4bc53dbb…c1a13`".
- **Command / exit:** `git -C <lane> show {c48f8a4,55bcce69,HEAD}:corpus/evidence/round-44/oracle/manifest.json | sha256sum` → **exit 0 each**, all print `06a72dd5b660c79adae943917abf40c24ab16554ec6c2f14985958799a78f5fe` (P6); worktree `sha256sum` prints the same.
- **Observed:** no committed or worktree object hashes to `4bc53dbb…`; the only other in-lane occurrence is the wave-1 draft it was copied from, `.ufo/waves/round-44/w1/R44EntryDraft.md:101`. The manifest is absent at that seat's HEAD `fc5eb54a` (`git cat-file -e` exit 1) and entered the repo once, at `c1ff9e89`, already as `06a72dd5…`.
- **Impact:** the S138 row's only content-addressed anchor is false; a reviewer cannot tie the Gate to the oracle bytes, and the mistake the round mines (pinning an object never opened) is repeated inside the record.
- **Smallest remediation:** replace with `06a72dd5…f5fe` (the freeze blob) and record the supersession.

### D2 — S139's Gate row omits the located quote and the capture that exist

- **Path:line:** `corpus/lessons/round-44.md:28`.
- **Command / exit:** `python3 -c "json.load(open('.ufo/waves/round-44/w1/R44SrcOracle/receipts/s139-releases-page.json'))"` → `started_at 2026-10-28T11:13:04Z`, `exit 0`, `stdout_sha256 86434136…` (P18); `grep -o 'title="Squashfs tools 4.7.5"' …/s139-releases-page.stdout.txt` → **exit 0**, one hit (P19); the same stdout records `HTTP 200 bytes 398943` and page sha256 `d08749f4…`.
- **Observed:** "opened" is a bare date with no pointer; "located quote" has no page anchor and mixes local tool output. A 4-word page quote and a timestamped capture both exist in the repo.
- **Impact:** S139's access/quote cells cannot be traced to any capture; the located-quote requirement is unmet while the evidence to meet it is committed.
- **Smallest remediation:** cite `w1/R44SrcOracle/receipts/s139-releases-page.json` (2026-10-28T11:13:04Z, page `d08749f4…`) and quote `title="Squashfs tools 4.7.5"` (4 words).

### D3 — S138's "opened" cell is a replay of subdirectory listings; the cited URL itself was never fetched

- **Path:line:** `corpus/lessons/round-44.md:27`.
- **Command / exit:** `supplementary-probes.json` probes 3–4 (both **exit 0**): the committed manifest has `started_at == finished_at == 11:12:37Z`, `all(replayed_from_saved_receipt) == True`, and its `fetched_at` set is `11:10:29Z`–`11:10:43Z`; the scan of `w1/R44SrcOracle/listings/*.json` for `repo_path == tests/integration/filesystem/squashfs` prints `[]` — every entry is a `__output__` (or `.bin_extract`) descendant.
- **Observed:** the cell reads "opened 11:10:29Z–11:12:37Z (contents API, 10 listings + 22 members, HTTP 200)", i.e. the original fetch timestamps plus a replay pass, over descendants of the named URL. Nothing in the repo records an open of `…/tests/integration/filesystem/squashfs` itself.
- **Impact:** the access evidence and the URL cell do not intersect; under the round's own M44-1 convention ("a URL is pinned only after a successful open of its listing") this row's URL is pinned without one.
- **Smallest remediation:** list the subdirectory URLs actually opened (with the receipt path/timestamp), or fetch the cited tree URL and commit that receipt.

### D4 — S138's quote is repo-side and the word count is wrong

- **Path:line:** `corpus/lessons/round-44.md:27` — `"NOT handler code, NOT extractor behaviour, NOT a C1 carrier" (manifest source.grounds, 12 words)`.
- **Command / exit:** `python3` word split → 10 tokens; `grep -c 'squashfs_v2.0_be.bin_extract' w1/R44SrcOracle/listings/squashfs_v2__big_endian__output__.json` → **exit 0**, `1` (P17).
- **Observed:** 10 words, not 12; and the sentence is committed manifest text, not page text. The only URL-derived element is a 1-token member name.
- **Impact:** the cell reads as a page quote with a mis-stated length; the "located quote" requirement is met only by a token.
- **Smallest remediation:** label the member token as the located artifact (listing path + `entries[]`) and state 10 words, or quote the listing entry verbatim with its JSON location.

### D5 — "were re-opened in-round (the C1 counter's `opened_source_rows` binding is true)" over-reads the binding

- **Path:line:** `corpus/lessons/round-44.md:32-36`; binding implementation `tools/round-44/c1-counter.py:2172-2185` (`OPENED = '2026-10-28'` at `:251`).
- **Command / exit:** read the implementation; run `python3 -c` over `corpus/SOURCES.md` S138 → 11 cells, `cells[8] = '2026-10-28'`, `cells[10] = corpus/knowledge/…-core.md`.
- **Observed:** `opened_source_rows` requires (a) the row id to appear in the entry's `source:` lines, (b) `cells[8] == '2026-10-28'` — a **self-declared date cell** — and (c) `used-by` naming the entry. It reads no HTTP receipt.
- **Impact:** the sentence's stated warrant cannot establish "re-opened"; S139 does have a real 11:13:04Z page receipt, S138 does not (D3). The record cites an instrument for a fact the instrument does not compute.
- **Smallest remediation:** cite the actual capture for each row (S139 receipt; S138 listing receipts), and stop citing `opened_source_rows` as open evidence.

---

## 3. `## Carried debt` (lines 125–141)

**D-id vector:** all **28/28** ids from `.ufo/waves/round-44/w1/R44Debt.md:23-76` appear exactly once (`dropped = []`, `extra = []`, re-derived from the pinned blob). The header at `:125` says "still open".

### D6 — D-27 is marked closed on an unmet exit condition, inside a "still open" section

- **Path:line:** `corpus/lessons/round-44.md:138-139` ("D-27 `stale-premise` fix (**now closed** by the committed 404 receipt, `## Mistakes` M44-1)") vs `:125` header, vs `.ufo/waves/round-44/w1/R44Debt.md:76`.
- **Command / exit:** `ls tools/round-45/` → only `frozen-path-preflight.py`; `grep -rn "local-source-gate" tools/round-45` → nothing.
- **Observed:** the exit condition is a conjunction: "the local-source gate (or an equivalent linter) refuses a URL cell without a committed 200 listing receipt, with a red control showing a guessed URL fails; **and** the 404 probe receipt is committed". Only the receipt conjunct is met; R44Debt itself records the enforcement as seat discipline.
- **Impact:** a reader believes `stale-premise` is mechanically gated; the next round's guessed URL reddens nothing.
- **Smallest remediation:** keep D-27 open and split it — "receipt conjunct closed (`l1/probe-fixture-404.txt`, `2081dc06`); gate conjunct open — no URL linter" — or land the linter with a red control and then close.

### D12 — prior-round debt: two open ids dropped, one range inflated, one alias unnamed

- **Path:line:** `corpus/lessons/round-44.md:140-141`.
- **Commands / exits:** `grep -rn 'R40-CL7\|round-40 D2' .ufo/waves/round-44 corpus/lessons/round-44.md | wc -l` → **0** (P21); `.ufo/waves/round-43/w1/R43ConnRouted.md:53-54` records both as **open — reason: operator-owned policy**; `grep -rn 'R43-CL2\|R43-CL3\|R43-CL4' . | grep -v .git | wc -l` → **0** (P20); `grep -rhoE 'R43-CL[0-9]a?' .ufo/waves/round-43 corpus/lessons/round-43*.md | sort -u` → **`R43-CL1a`** only (P22); `R42-CL3` exists at `corpus/lessons/round-42.md:77` and is unnamed.
- **Impact:** two still-open operator-policy exposures (vendor-terms and the AVM blobs at `7fce3086`) vanish from the round-44 record; "R43-CL1..CL4" cites four ids of which the lane holds one candidate; `R42-CL3`'s carry of R41-CL3 is silent.
- **Smallest remediation:** add `R40-CL7` and `round-40 D2` with their status and the round-43 pointer; replace `R43-CL1..CL4` with `R43-CL1a`; write `R42-CL3 (= R41-CL3)`.

*(Observation, not a defect: the 28 D rows are re-listed as ids with short labels, not the ledger's own text; the ledger's "re-list … verbatim" is met at id level only.)*

---

## 4. Census before → after (lines 47–53)

Numbers re-derived by this seat:

| probe | command | exit | observed |
|---|---|---|---|
| P7 | `git show c29360e3:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` | **0** | `137` |
| P8 | `grep -cE … corpus/SOURCES.md` | **0** | `139` |
| P9 | `grep -c W04 …/l1/sources-census-start-replay.txt` | **0** | `13` |
| P10 | `grep -c W04 …/l1/sources-census-end.txt` | **0** | `14` |

Both census artifacts are now committed (`git ls-tree HEAD .ufo/waves/round-44/l1/` shows both; they came in at `923fa870`), so the "untracked receipt" defect from the first snapshot is **fixed**.

### D7 — no exit codes for the row counts, and the "round-start" claim has no supporting receipt

- **Path:line:** `corpus/lessons/round-44.md:47-53`.
- **Commands / exits:** `git status --porcelain` on the two census files → empty (committed); `sed -n '1p;$p' .ufo/waves/round-44/l1/sources-census-start-replay.txt` → **exit 0**: first line `ERROR: config not found: /fast/scratch/hyaku/kaidoku-r44/l1/shokunin.conf`, last line `baseclone<TAB>ok<TAB>/fast/scratch/…/l1/baseclone/corpus/SOURCES.md` (P12); `grep -c W04` on the same file → 13 (P9) — the 14 belong to the **end** receipt (P10).
- **Observed:** the lesson attributes "`kaidoku ok`, exit 0, 14 W04" to the round start, but the only start artifact is a **base-clone replay** that opens with an `ERROR:` line, is scoped `baseclone`, and reports 13 W04. Neither row-count invocation carries an exit code.
- **Impact:** the "before" side is not re-derivable from the committed record, and the sentence borrows the end receipt's numbers for the start; the contract's "command and exit codes" is met for one command only.
- **Smallest remediation:** record `grep` exit 0 for each side, cite the start artifact by path and say it is `baseclone` scope with its `ERROR:` line, or re-run the start validate at lane scope and commit that receipt.

---

## 5. Remaining defect on the M44-2 fix's wiring

### D13 — two measured traps remain undisclosed; the docstring over-promises

- **Path:line:** `corpus/lessons/round-44.md:18` (fix cell) and `:63-69` (R44-CL1); tool `tools/round-45/frozen-path-preflight.py:2` (docstring) and `:35`/`:39` (`rev-parse --verify <rev>^{commit}`).
- **Commands / exits (P3/P4/P5, read-only):**
  - `--freeze c48f8a4… --rev c86ea508… --pathspec tools/round-45` → **exit 0**, `verdict clean` — **false green at the violating commit**, because the pathspec is caller-supplied;
  - `--rev 55bcce69…` + the C2 counter's own frozen set (`SCORECARD.md SHONEN.md SKILL.md tools/round-44/c2-counter.py tools/round-44/c2-rubric.json tools/round-44`) → **exit 1**, `blob_changed ["SCORECARD.md"]` — **false red at the measured rev**, on the bound edit the C2 counter tolerates (`freeze_notes[0].state == bound_edit_applied`, receipt exit 0);
  - no pathspec → exit 1 with 542 `touched` (every path in the range), i.e. noise, not a safe default.
- **Observed:** R44-CL1 now names a dirty-tree arm, "a mandatory pathspec for a directory freeze", and fleet-sweep placement — but a *mandatory* pathspec does not make it *correct*, and the bound-edit allow-list is named nowhere. The docstring says the gate runs "before a commit", while the tool only accepts commit revisions and cannot read the index.
- **Impact:** wiring the gate per R44-CL1 can still be green on a real violation or red on the round's own legitimate landing, and the pre-commit promise cannot be kept by the code.
- **Smallest remediation:** derive the pathspec from the claim/`carriers.json`, add an allow-list mode for `expected_append` bound edits, and either add a `--staged` mode or restate the gate as candidate-commit (pre-push).

---

## 6. What holds (verified, no defect)

1. Three mistake rows, five cells each; M44-2's and M44-3's fixes are **shown able to fail** by reproducible counter runs (P1, P2, `final-tip-4503fb78-counters.json`).
2. Both counters at the tip (`4503fb78`) exit 2 with the same 8 `frozen_path_changed` paths and no `SCORECARD.md`; "admissible only at `55bcce69`" is accurate, and the C2 admissible score is 80/80 with `mismatches []` (receipt present; not re-argued here).
3. `## Gate` has one admit (S138 + S139) and one reject with per-row reasons; the quarantine slice digest `7383a90e…28e6a` matches `w1/R44Quarantine.md:5`.
4. All 28 R44Debt ids are re-listed; none dropped.
5. Census numbers: 137 → 139 rows, 13 → 14 W04, S138 is the 14th and duplicates S130's tree URL; `git diff c29360e3..HEAD -- corpus/SOURCES.md` is `3 0` (additive only), so "no existing row cell was changed" holds.
6. `tools/round-45/frozen-path-preflight.py` sits outside the round-44 frozen pathspec, so adding it did not re-violate the freeze.
7. S139's binary digest in the Gate row is correct (`461e1fd9…` == `carriers.json.toolchain.unsquashfs` == `sha256sum /usr/bin/unsquashfs`, P23).

## 7. Limits, tooling, scratch

- **Read-only against the lane.** No mutating git/jj command in the lane. The only clone is `/fast/scratch/hyaku/kaidoku-r44/R44W2LessonGate/lane` (`git clone --shared`, `rev-parse --show-toplevel` verified); the only fixture repo was created under my scratch with `git -C "$D" rev-parse --show-toplevel` asserted equal to `$D`. Never ran `c1-run.sh`, REA, or any data procedure.
- **Writes:** this file and `.ufo/waves/round-44/w2/artifacts/R44W2LessonGate/` only.
- **Tool installs/upgrades:** none; no package manager invoked (pacman is paused host-wide). Tooling used: `python3`, `git` (read-only), `grep`, `sha256sum`, `stat`, `xxd`.
- **Scratch:** `/fast/scratch/hyaku/kaidoku-r44/R44W2LessonGate/` is deleted before this seat yields; no `/tmp` path is cited as evidence.
- **Not re-derived here (other seats' surfaces):** R44-C1's verdict and the C2 rubric's entry-level truth. This audit asks only whether the frontier-step cells match committed bytes — and notes that the lesson's own `R44-CL2` text now correctly reports that the C2 counter's red at `55bcce69` is the three withdrawn documentation bindings, not provenance (`c1-score-at-55bcce69.json`: exit 1, `carriers_matched 4`, `met_target false`, `bindings_false = ["province_core_section", "province_core_row", "frontier_note"]` — `supplementary-probes.json` probe 2, exit 0).
