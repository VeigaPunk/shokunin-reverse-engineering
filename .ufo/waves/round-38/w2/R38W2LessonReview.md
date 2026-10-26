# R38W2LessonReview — falsification pass on `corpus/lessons/round-38.md` @ `0fc6113376a156fddc3ec385386d71c3a4a9f690`

**Verdict: DEFECTS FOUND** — the Mistakes rows, their able-to-fail fixes (re-executed), the Gate rows, the registry old→new log, R37-CL2/CL3 and R36-CL1 all verify against the landing commit, but the **R38-C2 verdict cites a receipt that does not exist at `0fc6113`** (line 11), which in turn makes the **R37-CL1 closure statement false** (lines 85–88); one bare host-path citation (line 80) fails lane resolution while its factual claim is true.

All git operations below were read-only (`show`, `cat-file -e`, `ls-tree`, `log`, `diff`, `grep <rev>`, `merge-base`) against the lane at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Lane HEAD during review: `e265533ea3a7cd4d9a75a24ef737c2ff0e98e95f` (= `main`); every check was run against the judged commit `0fc6113`, not the worktree.

## Defects

### D1 (HIGH) — line 11: the R38-C2 receipt cited does not exist at the landing commit

Line 10–11: "**R38-C2** is measured at the landing commit (`.ufo/waves/round-38/l1/scores/c2-final.json`)."

- `git cat-file -e 0fc6113:.ufo/waves/round-38/l1/scores/c2-final.json` → fails.
- `git ls-tree -r --name-only 0fc6113 -- .ufo/waves/round-38/l1/scores/` → exactly two files: `c1-v1-at-3b960fe5.json`, `c1-v3-at-3b960fe5-NOT-THE-RULE.json`.
- Tree-wide search at `0fc6113` for `c2-final`: the only hit in the whole lane tree is `.ufo/waves/round-36/after/c2-final.json` (round 36, a different claim). Same at HEAD `e265533`.
- Tree-wide `git grep 0fc6113376a156fddc3ec385386d71c3a4a9f690 0fc6113 -- .ufo/waves/round-38 corpus` → **no hits**: no committed file at the landing commit records a C2 counter run at rev `0fc6113` under any name. The only committed C2 counter receipts in round-38 are wave-1 recounts (`w1/artifacts/R38ExecRecountBase/c2-at-{base,tip}.json`, both `mismatches: 1`, pre-repair).

So the sentence "R38-C2 is measured at the landing commit" is backed by a citation to a receipt that was never committed. The `0fc6113` commit message itself says "C1 first-freeze scores" — only C1 scores landed. Cross-seat note: `SCORECARD.md` line 3406 cites the same missing path (scorecard reviewer's scope).

### D2 (HIGH) — lines 85–88: the R37-CL1 closure statement is false as written

Line 85: "- **R37-CL1** (cite only committed receipts): every receipt this round cites is committed: …"

The three enumerated path groups (`corpus/evidence/round-38/c1/K*/{before,after}.json`, `.ufo/waves/round-38/l1/scores/`, wave-1 artifacts) are all committed and resolve — but the universal claim is falsified by the lesson's own line 11: `c2-final.json` is a receipt this round cites and it is not committed at `0fc6113` (evidence under D1). R37-CL1 is closed with a false universal statement.

### D3 (MINOR) — line 80: bare `HOST-CONTRACT.md` does not resolve at `0fc6113`

Line 80: "- **S147 adopt-with-anchor** — `HOST-CONTRACT.md` line 41; the heading names in the row are wrong."

- `git cat-file -e 0fc6113:HOST-CONTRACT.md` → fails; not in the lane tree or worktree.
- It resolves only as a host file: `/home/vgpnk/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md` (byte-identical copy, sha256 `ab36b310…`, also installed under `~/.zcode/skills/...`). The staged S147 row (shokuknow `SOURCES.append.md`) says "resolves under `$HOME`", so the reference is grounded — but the lesson cites it bare, which reads as a lane path and fails the mandated `cat-file -e` resolution.
- The factual claims around it are **true**: line 41 is `- REA release: \`rea-agents@6.7.0\`, skill v42, 207 tools.`; the staged row's named headings (§ "REA release", § "Expected doctor output") do not exist as headings — actual headings are `## State as of this writing` (L39) and `## Expected \`doctor\` output on this host` (L46). "The heading names in the row are wrong" verifies.

## Mandated checks that PASS

### 1. Backticked paths resolve at `0fc6113` (`git cat-file -e`)

All 100 unique backticked tokens extracted (`git show 0fc6113:corpus/lessons/round-38.md | grep -oE '\`[^\`]*\`' | sort -u`). Every lane-relative path resolves after brace/glob expansion — 8× `K*/{before,after}.json`, 3 knowledge entries, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `.ufo/waves/round-36/w2.ready.dispatched`, `.ufo/waves/round-37/probes/avm.txt`, 4× `.ufo/waves/round-38/assimilation/*`, 3× `l1/freeze-drift-*.json`, `l1/scores/` + the `c1-v{1,3}` glob (→ the two committed score files), 9× `w1/R38*.md`, 5× `w1/artifacts/...` (incl. `R38ExecAfterK3/harness-after-mode-{failure.txt,post-fix-ok.json}`), `w1.ready.dispatched`, `tools/round-38/{freeze-drift,c1-counter,gen-controls}.py`, `plans/round-38-claims.md`. External/staged references verified where claimed: staged `S106`=unblob README and `S122`=unblob.org/formats in shokuknow `SOURCES.append.md`; `avm-image-extraction.md` exists at `shokuknow/merge/kaidoku/knowledge/corpus/knowledge/`; `lanes/kaidoku/round{7,9}/work/*.tsv` exist in the shokuknow repo and are not lane-retained (as the lesson states). `considerthese/` absent from tree and worktree — the lesson's "absent" claim is the correct result of its own resolution failure. Two misses: D1 and D3.

### 2. `## Mistakes` rows complete (class · evidence · captured-by · fix)

All four rows (lines 17–20) parse to 5 non-empty cells: id, class, evidence, captured-by, fix. M38-1/M38-3/M38-4 captured-by = QUALITY 55 / none / none with reasons; M38-2 captured-by = "none (no rule required control generators inside the freeze)".

### 3. Fixes SHOWN able to fail — cited commands executed

- **M38-1 / M38-2 fix — freeze-drift exits** (committed `tools/round-38/freeze-drift.py` extracted to scratch, run read-only against the lane):
  - `--freeze e059ca93 --rev 077e212b` (default kill-rule paths) → **exit 1**, drift = [`f1010f67` 03:32:55, `79f69347` 03:30:33] — byte-equal to committed `.ufo/waves/round-38/l1/freeze-drift-077e212b.json`.
  - `--rev cb4326b2` → **exit 0**, drift `[]`, verdict clean — equal to `freeze-drift-cb4326b2.json`.
  - `--rev 077e212b tools/round-38/gen-controls.py` → **exit 1** listing `efd5c47a` (03:09:14) — equal to `freeze-drift-gen-controls.json`.
  - `--rev 77091b4` (base, not a descendant) → **exit 2** ("freeze is not an ancestor"), as the fix text claims.
- **M38-2's F1 mechanism reproduced live**: ran the *frozen* `gen-controls.py` (e059ca93) `c2-1` in scratch → counter exit **0** (the `else` branch of `c2_fixture` mints the repaired fixture — `prov_ptr='`+doctor path, i.e. green, `met_target true`), while the *fixed* generator (efd5c47a) → counter exit **1** (red defect fixture). Frozen `gen-controls.py:199` passes `a.kind.split('-')[1]` = `'1'/'2'/'3'` into `c2_fixture`, which branches only on `junk/delete/substitute`; `:217` `return 0 if res.get('exit') != 1 else 1` masks the green control as success. Exactly as the lesson states.
- **M38-3 fix — before/after receipts**: all 8 committed receipts inspected at `0fc6113`. Every `K*/before.json`: `normalized_result.files == []` and contains `missing-extractor-dependency` with `sasquatch-v4be`; every `K*/after.json`: published `files` with sha256s. "Red or green depending only on the arm" holds in the committed record. (REA arms not re-executed — receipts are the cited evidence.)
- **M38-4 fix**: `git diff 9c9d496b cb4326b2 -- tools/round-38/c1-run.sh` shows `mkdir -p "$OUT"` → `rm -rf "$OUT"`; `harness-after-mode-failure.txt` records exit 1 at HEAD `9c9d496b` with REA's "Extraction output root already exists"; `harness-after-mode-post-fix-ok.json` is a completed extract_firmware envelope. The harness is indeed outside the kill-rule set (freeze-drift DEFAULT paths), so "not an M38-1 class amendment" is correct — note `79f69347` also touched `c1-run.sh`, consistent with the harness being out-of-set.

### 4. Quotes ≤ 25 words

All double-quoted and 「」-quoted strings word-counted: max 17 words (S114's Freetz opening line). None exceeds 25.

### 5. Gate decisions carry reason + flip

S112–S116 rows (lines 28–32): all five have non-empty reason and flip cells (S115 = **reject** with reason and flip). The three assimilation decisions each carry reason + flip; the `sasquatch-unblob-compatibility-precondition` REFUSE carries "Flip: none; this is a superseded host snapshot" — a flip field is present but degenerate (no falsifiable condition); noted, not counted a defect.

### 6. Registry old→new logged

`git diff e059ca93 0fc6113 -- corpus/SOURCES.md`: exactly one modified row (S110) + five appended (S112–S116). S110 cell-by-cell: only cell 4 (scope, exactly the old→new strings quoted on line 34) and cell 10 (used-by: `…unblob-sasquatch-dependency.md` → that plus `…unblob-format-matrix.md`) differ; status/recheck cells unchanged — "No status or recheck cell changed" verifies. Row counts: 111 S-rows at freeze → 116 at landing ("Rows 111 → 116"). S115 status cell = `rejected` (R37-CL3's rejected row exists).

### 7. Routed defects

- **R37-CL1**: **FALSE** — see D2. (The enumerated groups themselves are committed; the universal claim is not.)
- **R37-CL2**: TRUE — S113 (BE fixtures) and S114 (Freetz note) are registered provenance rows; digests re-verified: `.ufo/waves/round-37/probes/be-squashfs_v4.nopad.bin` sha256 = `a29ddc15f5a6abca…` (= S113's LFS oid), `avm.txt` sha256 = `c1c43f6f97d7477d…a9a5d5` (matches the lesson's `c1c43f6f…a5d5`).
- **R37-CL3**: TRUE — Gate decisions filed in this section; S115 is a rejected row; the 7-Zip quote "Cannot open the file as archive" is present in the committed `R38CrossToolK4/7z-refusal.txt`.
- **R36-CL1**: TRUE — `.ufo/waves/round-36/w2.ready.dispatched` shows `A` in `e059ca93`'s name-status; `.ufo/waves/round-38/w1.ready.dispatched` shows `A` at `3b960fe5`.

## Additional verifications (spot-checks beyond the mandated list)

- **C1 verdict bytes** (line 9–10): `c1-v1-at-3b960fe5.json` = `carriers_matched 3`, `met_target false`, target 4, freeze `e059ca93`, rev `3b960fe5`; K2's `after.json` has exactly **one** `extraction_gap`, kind `unpublished-entry` (`var/lib/run-link`) — "K2 fails on one unpublished-entry gap" is precise. `c1-v3` = 4/4 matched (`met_target` still false on province bindings) — "3/4 → 4/4" is accurate and the v3 file is honestly named `NOT-THE-RULE`.
- **M38-1 timeline**: R38ExecAfterK1 §2e exists; its counter runs are timestamped 03:17:22–03:18:23, before `79f69347` (03:30:33) and `f1010f67` (03:32:55) — "before both" verifies. Frozen counter sha `a7a62b09…` = sha256 of `c1-counter.py` at `e059ca93` (recomputed). `f1010f67` touched only `c1-counter.py`; `79f69347` touched claims doc + counter (+ harness). Cited `git log e059ca93..077e212b -- …` reproduces both commits with the stated times.
- **M38-2**: c2-counter sha256 `7f137b664984…` at the freeze, blob `04a0bc63` identical through `main` (`e265533`) — "unchanged throughout" verifies; fix-before-dispatch 03:09:14 vs 03:15:59 verifies; all 7 committed control receipts record exit 1; R38ReviewerControlReplay F1/F2/F3 present and match.
- **S110 live re-pin**: fetched `unblob/26.6.4/README.md` → sha256 `6544d60f22f7b521f8705b3bba5d47a50e428ccbd3359542708dbd009ccf3716` (exact match to the row), 235 lines, line 5 and line 22 both carry "78+", line 49 is the sasquatch install sentence — the S110 scope edit's "78+" sentence (lines 5, 22) is live-true.
- **S112**: retained round-36 handler scout confirms lines 24–26 with line 26 `V4BE_EXECUTABLE = "sasquatch-v4be"`; S108 digest `2d7b901b…9287` matches the S108 row.
- **S116 / format-matrix entry**: committed entry contains 97-section count, "more than 30" ×3, `v4-BE`, the `v4-broadcom` correction, "Does not support encrypted ZIP files", "78+" — matching the lesson's reproduction claims.
- **Assimilation artifacts**: `reg-ids` 111 lines (S001–S111), `staged-ids` 132 (S106–S237), `collisions` exactly S106–S111 (6) — line 38–39 verifies; `guard-proof.txt` shows the indented `  | S002 |` fixture proof.
- **Quarantine slice**: 5 kaidoku rows (S150, S113staged, S117, S136, S147) as claimed. **S150 live-verified**: zenn article fetched, 174,088 B exactly, heading 「シンボルがない場合のヒント」 occurs **0** times — the fabrication-class call is true. **S113staged**: staged row does say "17 locales"; the lesson's correction (21 + `x-default`) is a correction of it, consistent. **S136**: lane file line 8 carries the "2 of 24 verbs" answer — anchor true. **S147**: line 41 anchor true; "heading names in the row are wrong" true (see D3 for the citation form).
- **40 seats** (line 6): `w1-dispatch.json` `counts = {spawn: 40, resume: 0, total: 40}`; `w1-spec.json` has 40 items.
- **Freeze contents** (lines 3–4): `e059ca93` tree holds `plans/round-38-claims.md`, both counters + `selftest/` + `c1-run.sh` under `tools/round-38/`, `.ufo/waves/round-38/c1/carriers.json`, `instruments.json`, `census-start.txt`.

## Residual risk / not re-verified

- **"died at 03:37:05"** (line 6): no committed file in the round-38 tree mentions 03:37 (`git grep 03:37 0fc6113 -- .ufo/waves/round-38` → no hits; `swarm-registry.json` has no such timestamp). Plausible from attempt-1's handoff record outside what I searched — [INFERENCE], unevidenced in the lane tree.
- **S117's "IEEE Xplore HTTP 202 with an empty body"** half not re-run; the Crossref half verified live (paper title resolves).
- **S116 live refetch** not repeated (flip condition is refetch-based; counts taken from the committed entry and registry row).
- **REA before/after arms** not re-executed; the committed receipts were inspected instead (the cited evidence).
- **D1's root cause** (was `c2-final.json` ever produced?) is outside this seat: the C2-at-landing measurement itself is another seat's target; my finding is that the lesson cites a receipt absent from the committed record.

## Tooling

No tools installed or upgraded (none needed); no pacman transactions; sasquatch binaries untouched.

## Scratch

`/fast/scratch/hyaku/kaidoku-r38/R38W2LessonReview` removed after this report was written; all cited values are quoted inline above.
