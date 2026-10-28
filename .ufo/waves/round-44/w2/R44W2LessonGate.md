# R44W2LessonGate — round-44 lesson audited against the frontier-step contract

**Seat:** `R44W2LessonGate` (audit only; no claim, counter, rubric, frozen byte or production doc touched).
**Lane:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · **base** `c29360e3ba5381a5ab69e372d0d9577970f85018` ·
**freeze** `c48f8a4bfd449300c975668e59aae5b5538b6a84` · **measured** `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac` ·
**lane tip at audit** `8bb1090a` (== tip at dispatch `c86ea508` for every frozen path).
**Target of the audit:** `corpus/lessons/round-44.md` (102 lines, committed at `8bb1090a`).
**Contract source for the audit:** the wave-2 assignment's frontier-step checklist (Mistakes schema + fix-shown-able-to-fail; Gate URL/date/≤25-word located quote per new row + ≥1 admit/≥1 reject; carried-debt re-listing against `.ufo/waves/round-44/w1/R44Debt.md`; census before→after with command and exit codes).
**Receipts:** `.ufo/waves/round-44/w2/artifacts/R44W2LessonGate/probe-receipts.json` (28 probes: seat, exact argv, cwd, exit, wall s, stdout bytes + sha256, stderr bytes + sha256) plus the two reproduced preflight JSONs. Every probe below is named `P<n>` and resolves in that file.

## Verdict in one screen

| checklist item | verdict |
|---|---|
| `## Mistakes`: class · evidence pointer · captured-by · fix, both rows | **5 cells each — pass on shape**; content defects below |
| M44-1 fix *shown able to fail* | **FAIL** — no fix mechanism exists; the red/green pair demonstrates the *defect*, and the remediation sits in the `captured-by` cell (D3) |
| M44-2 fix *shown able to fail* | **PASS, verified** — preflight reproduces byte-identically: RED exit 1 / 8 paths at `c86ea508`, GREEN exit 0 at `55bcce69`; both counters at tip exit 2 with the same 8 paths (P1, P2, P26); A/D/restore cases also red in a throwaway fixture. Wiring limits in D7 |
| `## Gate`: URL + access date + ≤25-word located quote, S138 + S139 | **partial** — both URLs correct; S138's cited manifest digest is wrong (D1) and its "12 words" is 10 (D5); S139 has no located quote and no receipt/timestamp although a committed receipt holds both (D4) |
| `## Gate`: ≥1 admit + ≥1 reject with reasons | **PASS** — admit S138/S139 (binding `opened_source_rows == ["S138","S139"]` is true in the C1 score receipt; the entry cites both); reject the assimilation package with per-row reasons and the slice digest `7383a90e…28e6a` matching `w1/R44Quarantine.md:5` |
| `## Carried debt`: every still-open id vs the 28 D-ids | **28/28 present, none dropped**; D-27 wrongly closed (D2); two carried-open prior ids dropped and one prior-id range inflated (D11) |
| census before→after, command + exit codes | **numbers verified** (137→139; 13→14 W04); **record defective** — no exit codes, round-end receipt untracked, start claim unsupported (D6) |

R44-C1's honest stop and R44-C2's calibration are **not re-argued here** (other wave-2 seats own them). Everything below is about whether *the record says what happened*.

---

## 1. `## Mistakes`

Table at `corpus/lessons/round-44.md:13-16`, header + two rows; every row parses to exactly 5 cells (`awk -F'|'` → `fields=5`).

| row | class | evidence pointer | captured-by | fix | fix shown able to fail |
|---|---|---|---|---|---|
| M44-1 (`:15`) | `stale-premise` | l1 probe-404 receipt + reproduced 404/200 pair — **all four artifacts exist, digests match** (P15); red receipt committed at freeze (`git cat-file -e c48f8a4:.ufo/waves/round-44/l1/probe-fixture-404.txt` → present) | holds the *remediation* ("the frozen-URL convention") | holds the *demonstration* ("the red/green pair above…") | **no** — see D3 |
| M44-2 (`:16`) | `freeze-violation` | `git log --oneline c48f8a4..main -- tools/round-44/` → only `c86ea508` (P13); preflight red receipt 8 paths; counters' `frozen_path_changed` lists are byte-identical to each other and to the preflight's `blob_changed` (P26, P1) | holds the rule quote + "none — … no commit-time gate existed" | holds `tools/round-45/frozen-path-preflight.py` + red/green receipts | **yes, reproduced** (P1/P2) |

Verified positives for M44-2 that the row claims, all re-derived by this seat:

- RED: `python3 tools/round-45/frozen-path-preflight.py --root <lane> --freeze c48f8a4… --rev c86ea508… --pathspec tools/round-44` → **exit 1**, `verdict frozen_path_changed`, `touched 8`, `blob_changed 8`; the emitted JSON is **identical** to the committed `.ufo/waves/round-44/l1/preflight-c86ea508.json` (P1).
- GREEN: same with `--rev 55bcce69…` → **exit 0**, `verdict clean`; identical to `.ufo/waves/round-44/l1/preflight-55bcce69.json` (P2).
- Both counters at the tip: `c1-score-at-tip.json` exit **2**, `c2-score-at-tip.json` exit **2**, each with the same 8 `frozen_path_changed` paths (P26). The claim "the frozen-path list is byte-identical in both counters" is true.
- The tool is not vacuous on this round's evidence: it accepts `A` as well as `M/D/R/T/U/C`, detects an add under a frozen directory, and stays red after a delete+restore of identical bytes in a throwaway fixture (`$D=$(mktemp -d)` under my scratch, `git -C $D rev-parse --show-toplevel` asserted equal to `$D`; results in `probe-receipts.json` under my fixture run notes).

### D3 — M44-1's fix is not a fix, and the row's columns are swapped

- **Path:line:** `corpus/lessons/round-44.md:15` (cells 4 and 5); corroborating `.ufo/waves/round-44/w1/R44Debt.md:76` ("enforced by **seat discipline**, not by the tooling").
- **Command / exit:** `sed -n '15p' corpus/lessons/round-44.md` (read, no exit semantics); `ls tools/round-45/` → only `frozen-path-preflight.py`.
- **Observed:** the `captured-by` cell contains the remediation ("the frozen-URL convention: a URL is pinned only after a successful open of its listing, never guessed"); the `fix (shown able to fail)` cell contains the red/green demonstration of the *error* (`grep -c 'squashfs_v2.0_be.expected'` = 0 in the 200 page). No artifact anywhere in the lane refuses a URL cell without a committed 200 listing receipt.
- **Impact:** the contract requires each fix to be *shown able to fail*. For M44-1 the only thing shown able to fail is the defect. A future round can repeat the URL guess with no instrument reddening (see D2).
- **Smallest remediation:** put the remediation in the fix cell and mark it "process only — no executable arm, tracked as D-27 open", or land a URL-cell linter with one red control.

---

## 2. `## Gate`

Rows at `corpus/lessons/round-44.md:22-25`.

| requirement | S138 (`:24`) | S139 (`:25`) |
|---|---|---|
| URL | correct, matches `corpus/SOURCES.md:144` | correct, matches `corpus/SOURCES.md:145` |
| access date | `2026-10-28T11:10:29Z–11:12:37Z` — start matches the earliest committed listing `fetched_at` 11:10:29Z, all 10 listings HTTP 200 (P17 context; listings scan) | `2026-10-28` only — **no time, no receipt pointer** (D4) |
| ≤25-word quote | 10 words, labelled **12** (D5); sentence is `manifest.source.grounds` in the *repo*, not the opened URL | 11 tokens, but the page-derived element is only the bare tag `4.7.5`; the rest is `/usr/bin/unsquashfs` output — **not located in the page** (D4) |
| content addressing | manifest sha256 `4bc53dbb…c1a13` — **matches no committed object** (D1) | `/usr/bin/unsquashfs` sha256 `461e1fd9…b1677c` — **correct**, equals `carriers.json.toolchain.unsquashfs` and the live binary (P23) |
| admit/reject reason | admit — `bindings.opened_source_rows == ["S138","S139"]` is true in `c1-score-at-55bcce69.json`; the entry cites both rows (`corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:12-13`) | same |
| reject | assimilation package rejected with named per-row reasons (S150 fabrication-class, S113/S136/S147 anchor caveats, S117 unverifiable), slice digest `7383a90e…28e6a` = `w1/R44Quarantine.md:5` | — |

Only two rows are *new* this round: `git diff c29360e3..HEAD -- corpus/SOURCES.md` is `3 0` (S138 + S139 + one blank), so the "every new row" scope is complete.

### D1 — HIGH: the S138 Gate row cites a manifest sha256 that exists nowhere

- **Path:line:** `corpus/lessons/round-44.md:24` — "manifest `corpus/evidence/round-44/oracle/manifest.json` sha256 `4bc53dbb…c1a13`".
- **Command / exit:** `git -C <lane> show {c48f8a4,55bcce69,HEAD}:corpus/evidence/round-44/oracle/manifest.json | sha256sum` → **exit 0 each**, all three print `06a72dd5b660c79adae943917abf40c24ab16554ec6c2f14985958799a78f5fe` (P6); worktree `sha256sum` prints the same.
- **Observed:** no committed or worktree object hashes to `4bc53dbb…`; the only other occurrence of that prefix in the lane is the wave-1 draft it was copied from, `.ufo/waves/round-44/w1/R44EntryDraft.md:101`. The manifest is absent at that seat's HEAD `fc5eb54a` (`git cat-file -e` exit 1) and was committed once, at `c1ff9e89`, already as `06a72dd5…`.
- **Impact:** the S138 row's only content-addressed anchor is false; a reviewer cannot tie the Gate to the oracle bytes, and the mistake the round mines (guessing an object instead of opening it) is repeated in the record itself at one remove.
- **Smallest remediation:** replace with `06a72dd5…f5fe` (freeze blob) and note the supersession; do not carry a seat-reported digest into a Gate row unverified.

### D4 — S139's Gate row omits the located quote and the capture that exist

- **Path:line:** `corpus/lessons/round-44.md:25`.
- **Command / exit:** `python3 -c "json.load(open('.ufo/waves/round-44/w1/R44SrcOracle/receipts/s139-releases-page.json'))"` → `started_at 2026-10-28T11:13:04Z`, `exit 0`, `stdout_sha256 86434136…` (P18); `grep -o 'title="Squashfs tools 4.7.5"' …/s139-releases-page.stdout.txt` → **exit 0**, one hit (P19); the same stdout records `HTTP 200 bytes 398943` and page sha256 `d08749f4…` (P18/P19 context).
- **Observed:** the row's "opened" cell is a bare date with no pointer, and its "located quote" cell contains no page text or anchor (no `$.tag_name`, no title, no line), mixing `/usr/bin/unsquashfs` output instead. Both the timestamp and a 4-word located quote are available in the committed receipt.
- **Impact:** S139's access/quote cells cannot be traced to any capture; "access date" is unverifiable and the "located quote" requirement is unmet — while the round's own S139 receipt would satisfy it.
- **Smallest remediation:** cite `w1/R44SrcOracle/receipts/s139-releases-page.json` (2026-10-28T11:13:04Z, page sha256 `d08749f4…`) and quote `title="Squashfs tools 4.7.5"` (4 words).

### D5 — S138's quote is repo-side and its word count is wrong

- **Path:line:** `corpus/lessons/round-44.md:24` — `"NOT handler code, NOT extractor behaviour, NOT a C1 carrier" (manifest source.grounds, 12 words)`.
- **Command / exit:** `python3` word split of the quoted string → 10 tokens (P-receipt note); `grep -c 'squashfs_v2.0_be.bin_extract' w1/R44SrcOracle/listings/squashfs_v2__big_endian__output__.json` → **exit 0**, `1` (P17).
- **Observed:** 10 words, not 12; and the sentence is from the committed manifest, not from the opened URL. The only URL-derived element is the 1-token member name `squashfs_v2.0_be.bin_extract` (verified in the 200 listing JSON).
- **Impact:** the Gate cell reads as a page quote when it is a repo quote with a mis-stated length; a ≤25-word *located* quote is met only by a token.
- **Smallest remediation:** label the member token as the located artifact (path + `entries[]` index) and state 10 words for the manifest sentence, or quote the listing entry verbatim with its JSON location.

### Verified in this section (no defect)

- `S138` URL resolves to the same source as `corpus/SOURCES.md:144`; the capture's 10 listings are all `http_status 200`, `failures: []`, 22 members (manifest `counts`), matching the row's "10 listings + 22 members".
- Admit binding is real, not asserted: `c1-score-at-55bcce69.json` → `bindings.opened_source_rows = ["S138","S139"]`; both rows are cited at `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:12-13`.
- Reject has reasons and a digest that matches the seat report.
- Census's duplicate claim is accurate: 14 `W04` lines at the end, the 14th is S138 (P10), and the same unblob tree URL already sits on `corpus/SOURCES.md:136` (S130) — "a within-scope URL also present at another row's evidence pointer" is true.

---

## 3. `## Carried debt` (`:85-101`)

**D-id vector:** all **28/28** ids from `.ufo/waves/round-44/w1/R44Debt.md` (`:23-76`) appear exactly once in the lesson; `dropped = []`, `extra = []` (regex over the ledger's `| D-nn |` rows vs the lesson body). Id-level preservation passes.

Two residues:

### D2 — D-27 is marked closed against an exit condition that is not met (and contradicts the section's own header)

- **Path:line:** `corpus/lessons/round-44.md:98-99` ("D-27 `stale-premise` fix (**now closed** by the committed 404 receipt, `## Mistakes` M44-1)") vs the section header `:85` ("## Carried debt (still open; `w1/R44Debt.md`)"), and the exit condition at `.ufo/waves/round-44/w1/R44Debt.md:76`:
  > "The frozen-URL convention is mechanical: the local-source gate (or an equivalent linter) refuses a URL cell without a committed 200 listing receipt, with a red control showing a guessed URL fails; **and** the 404 probe receipt is committed before the freeze…"
- **Command / exit:** `ls tools/round-45/` → only `frozen-path-preflight.py`; `grep -rn "URL" tools/round-44 tools/round-45` finds no URL gate; `hash` of the probe receipt exists (D3 evidence).
- **Observed:** the receipt conjunct is satisfied (`probe-fixture-404.txt` present at `c48f8a4`); the gate conjunct is not — no linter, no red control. R44Debt itself records the enforcement as seat discipline, i.e. not mechanical. The ledger's own rule (`R44Debt.md:146`) lets only the landing round close a row, and only "with the pointer" to the exit evidence; the lesson points only at the receipt.
- **Impact:** a reader believes `stale-premise` is mechanically gated; the next round's guessed URL will be accepted by every instrument. The row is also simultaneously declared open (header) and closed (body).
- **Smallest remediation:** keep D-27 open and split it in words: "receipt conjunct closed (`l1/probe-fixture-404.txt`, commit `2081dc06`); gate conjunct open — no URL linter exists", or land the linter with a red control and then close.

### D11 — prior-round debt: two open ids dropped, one range inflated, one alias unnamed

- **Path:line:** `corpus/lessons/round-44.md:100-101` ("Prior-round open ids unchanged: R36-CL5, R40-CL2, R41-CL3, R42-CL1, R42-CL2 …, R43-CL1..CL4").
- **Commands / exits:**
  - `grep -rn 'R40-CL7\|round-40 D2' .ufo/waves/round-44 corpus/lessons/round-44.md | wc -l` → **0** (P21);
  - `.ufo/waves/round-43/w1/R43ConnRouted.md:53-54` records both as **open — reason: operator-owned policy** at round-43 base (vendor-terms exposure and the AVM blobs at `7fce3086`, "history not rewritten");
  - `grep -rn 'R43-CL2\|R43-CL3\|R43-CL4' . | grep -v .git | wc -l` → **0** (P20); `grep -rhoE 'R43-CL[0-9]a?' .ufo/waves/round-43 corpus/lessons/round-43*.md | sort -u` → **`R43-CL1a`** only (P22);
  - `R42-CL3` exists as a routed id (`corpus/lessons/round-42.md:77`) and is not named in round 44.
- **Observed:** two still-open, operator-owned ids vanish from the record; "R43-CL1..CL4" cites four ids of which the lane holds one candidate id; `R42-CL3` (which explicitly carries `R41-CL3`) is folded silently into `R41-CL3`.
- **Impact:** the carried-debt list is not a faithful "every still-open id" vector: two operator-policy exposures are no longer re-disclosed anywhere in the round-44 record, and an inflated id range reads as four tracked items.
- **Smallest remediation:** add `R40-CL7` and `round-40 D2` with their operator-owned status and the round-43 pointer; replace `R43-CL1..CL4` with `R43-CL1a`; write `R42-CL3` (= R41-CL3) explicitly or say it is folded.

**Observation (not a defect):** the 28 D-ids are re-listed as ids with 2–8-word labels, not the ledger's own text; the ledger's "re-list … verbatim" is met at id level only. If verbatim means the row text, the section under-delivers, but no id is lost.

---

## 4. Census before → after

Line `:44-49` claims `corpus/SOURCES.md` **137 → 139 rows**, command `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`, round-start `sources-census.sh validate …` → `kaidoku ok`, exit 0, 14 W04 warnings, round-end receipt `.ufo/waves/round-44/l1/sources-census-end.txt`.

Re-derived by this seat:

| probe | command | exit | observed |
|---|---|---|---|
| P7 | `git show c29360e3:corpus/SOURCES.md \| grep -cE …` | **0** | `137` |
| P8 | `grep -cE … corpus/SOURCES.md` | **0** | `139` |
| P9 | `grep -c W04 .ufo/waves/round-44/l1/sources-census-start-replay.txt` | **0** | `13` |
| P10 | `grep -c W04 .ufo/waves/round-44/l1/sources-census-end.txt` | **0** | `14` |

### D6 — the census record is not re-derivable: no exit codes, untracked receipts, an error-line start artifact

- **Path:line:** `corpus/lessons/round-44.md:44-49`.
- **Commands / exits:**
  - `git status --porcelain .ufo/waves/round-44/l1/sources-census-end.txt .ufo/waves/round-44/l1/sources-census-start-replay.txt` → **exit 0**, both `??` (P11) — the cited "round-end receipt" is **not committed** at `8bb1090a`;
  - `sed -n '1p;$p' .ufo/waves/round-44/l1/sources-census-start-replay.txt` → **exit 0**: first line `ERROR: config not found: /fast/scratch/hyaku/kaidoku-r44/l1/shokunin.conf`, last line `baseclone<TAB>ok<TAB>/fast/scratch/…/l1/baseclone/corpus/SOURCES.md` (P12) — the only start artifact is a base-clone replay with an error line, not the lane-scope `kaidoku ok` the lesson cites;
  - the lesson records **no** exit code for either row-count invocation and **no** exit code for the round-end validate.
- **Impact:** the "before" side of the census has no committed receipt and no exit code; the "after" side's receipt exists only in the worktree and records no exit status. The numbers themselves are right — but the contract asked for command **and exit codes**, and the committed record cannot reproduce the comparison.
- **Smallest remediation:** commit both census artifacts, record `grep` exit 0 for each side, record the validate exit code in the receipt (or in the lesson), and either re-run the start validate at lane scope or restate the start as `baseclone ok` with its `ERROR:` line disclosed.

---

## 5. Remaining defects on the M44-2 row and its fix

### D7 — the preflight is only as good as the caller-supplied pathspec; the round's frozen set is wider than the demonstrated one

- **Path:line:** `corpus/lessons/round-44.md:16` (fix cell) and `:57` (R44-CL1: "wire it into the round's commit sequence").
- **Commands / exits (P3/P4, tool unchanged, read-only):**
  - `frozen-path-preflight.py --freeze c48f8a4… --rev c86ea508… --pathspec tools/round-45` → **exit 0**, `verdict clean` — a **false green at the violating commit**;
  - `… --rev 55bcce69…` + the C2 counter's own frozen set (`SCORECARD.md SHONEN.md SKILL.md tools/round-44/c2-counter.py tools/round-44/c2-rubric.json tools/round-44`) → **exit 1**, `blob_changed ["SCORECARD.md"]` — a **false red at the measured rev**, because the C2 counter tolerates that bound edit (`c2-score-at-55bcce69.json.freeze_notes[0].state == bound_edit_applied`, receipt exit 0);
  - `… --rev c86ea508…` with **no** pathspec → exit 1 with 542 `touched` paths (every path in the range), i.e. no-pathspec is noise, not a safe default.
  - `tools/round-45/frozen-path-preflight.py:2` docstring says "red **before** a commit that touches a claim's frozen paths", but the tool only accepts `rev` commits (`rev-parse --verify <rev>^{commit}`, `:35`/`:39`); it cannot read the index, so it cannot run pre-commit.
- **Impact:** the fix is real for the M44-2 instance, but wiring it per R44-CL1 with a single pathspec leaves every other frozen path (claims file, SOURCES, SKILL.md, carriers, oracle trees, held-out receipts) ungated; wiring it with the full set turns the round's own legitimate bound edit red. And the docstring promises a pre-commit gate the code cannot provide.
- **Smallest remediation:** give the tool the claim's frozen set (or read it from `carriers.json`/the counter receipt), add an explicit allow-list mode for `expected_append` bound edits, and either implement an index mode (`--staged`) or state the gate is candidate-commit, post-commit/pre-push.

### D8 — M44-2's chronology is unsupported by any surviving receipt

- **Path:line:** `corpus/lessons/round-44.md:16` — "`c86ea508` added/edited 8 files … **after both counters had already scored at `55bcce69`**".
- **Commands / exits:** `git log -1 --format='%h %cI'` for `55bcce69` → `2026-10-28T09:57:16-03:00`, `c86ea508` → `2026-10-28T10:43:43-03:00` (P24); `stat -c '%y'` on the two score receipts → `c1 11:13:02`, `c2 11:12:46` local (P25).
- **Observed:** the only receipts at `55bcce69` postdate the violating commit by ~29 minutes; no committed artifact evidences a scoring run before `10:43`. (Attempt 1 could have scored between `09:57` and `10:43`, but then its receipt did not survive — it is not in `.ufo/waves/round-44/l1/`.)
- **Impact:** the row reads as a verified sequence ("scored, then violated, then re-run") but the ordering rests on nothing committed; a reader cannot tell whether the frozen-path violation was present while the admissible score was taken.
- **Smallest remediation:** drop the ordering clause, or commit the attempt-1 score receipt (or its mtime) and cite it.

### D9 — "added/edited 8 files": zero additions

- **Path:line:** `corpus/lessons/round-44.md:16`.
- **Command / exit:** `git show --name-status c86ea508 -- tools/round-44/` → **exit 0**, 8 lines, **all `M`** (P13); `git ls-tree -r --name-only c48f8a4 tools/round-44/control-fixtures/ | wc -l` → **exit 0**, `38` (P14) — the eight paths already existed at freeze.
- **Impact:** small but exact: the violation is a *modification* of eight frozen regular files inside a frozen directory, not an addition. "Added" would matter for whether the directory-freeze rule or a file-level freeze was breached.
- **Smallest remediation:** "modified 8 frozen files under `tools/round-44/control-fixtures/`".

### D10 — M44-1's artifact digests are misattributed and the committed red arm is not self-describing

- **Path:line:** `corpus/lessons/round-44.md:15` — "`tree-200.html` + `member-names.txt` (200, sha256 `e3ea23b9…3d2f46`)".
- **Commands / exits:** `sha256sum` on the three artifacts → `guessed-expected-404.body d5558cd4…512ed`, `tree-200.html e3ea23b9…2f46`, `member-names.txt 99232795…0176` (P15); `cat .ufo/waves/round-44/l1/probe-fixture-404.txt` → **14 bytes**, body `404: Not Found`, no URL/argv/exit/digest.
- **Impact:** one sha256 is attached to a two-file group (only the HTML hashes to `e3ea23b9…`), and the frozen red receipt cannot tie itself to the guessed URL — its authenticity rests on the *later* wave-1 reproduction, not on the frozen byte.
- **Smallest remediation:** one digest per artifact; either commit a metadata sidecar (URL, argv, exit, digest, timestamp) beside `probe-fixture-404.txt` or cite `w1/artifacts/R44MistakeHunt/` as the self-describing arm and mark the l1 file as the body-only copy.

---

## 6. What holds (verified, no defect)

1. `## Mistakes` has both rows with all five columns, and M44-2's fix reproduces byte-identically (P1/P2) with counter parity at the tip (P26).
2. `## Gate` has one admit (S138 + S139, binding true in the frozen counter output, cited by the entry) and one reject with per-row reasons and a matching slice digest.
3. All 28 R44Debt ids are re-listed; none dropped.
4. Census numbers: 137 → 139 rows, 13 → 14 W04, S138 is the 14th and duplicates S130's tree URL; SOURCES diff base→HEAD is `3 0` (additive only, so "no existing row cell was changed" holds).
5. `tools/round-45/frozen-path-preflight.py` is committed at `8bb1090a` and is outside the round-44 frozen pathspec, so adding it cannot itself violate the freeze.
6. The preflight's claims about `A`, `D` and delete-then-restore hold in a throwaway fixture (red on `A`; still red after a same-bytes restore, `blob_changed []`, `touched [A,D,M,A]`).

## 7. Limits, tooling, scratch

- **Read-only.** No mutating git/jj command was run in the lane; the only fixture repo was created under my scratch with `git -C "$D" rev-parse --show-toplevel` asserted equal to `$D`.
- **Writes:** this file and `.ufo/waves/round-44/w2/artifacts/R44W2LessonGate/` only (`probe-receipts.json`, the two reproduced preflight JSONs).
- **Tool installs/upgrades:** none. No package manager was invoked (pacman is paused host-wide); the audit needed only `python3`, `git`, `grep`, `sha256sum`, `stat`.
- **Scratch:** `/fast/scratch/hyaku/kaidoku-r44/R44W2LessonGate/` — deleted before yielding (see terminal note in the seat result; no `/tmp` path is cited as evidence).
- **Not re-derived here (other seats' surfaces):** R44-C1's counter verdict, R44-C2's 80-entry rubric, and the QUALITY number in M44-2's closing parenthesis. This audit only asks whether the lesson's frontier-step cells match committed bytes.
