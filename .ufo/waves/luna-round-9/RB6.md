# RB6 — invariants verifier (E2 + G2/G3 closure)

## CLAIM
At fixed HEAD `a280e07` the four round-9 landing texts are not yet applied; command A 79/79 + 9/9 (10.0/10.0) holds, the tracked tree is byte-identical to HEAD with zero deletions, PROVINCE is untouched, and a 550 s watch saw no tracked change. The finalized landing texts (`RB1.md:15-25`, `RB2.md:13-27`, `RB4.md:11`) are command-A- and byte-neutral under exact-text simulation; the one-pass post-integration battery is pinned below.

## METHOD
- Snapshot 22:02–22:08: `git status --porcelain=v1 --untracked-files=no` empty; `git diff --quiet HEAD --` exit 0; `git diff --name-status --diff-filter=D HEAD --` empty; tree `9e509118913e…`; 170 tracked files; watcher (10 s polls) → `NO-TRACKED-CHANGE in 550s window; last check 2026-10-16T22:08:21-03:00`.
- Command A verbatim (`SCORECARD.md:93-123`, `REV=a280e07`) → `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "rule_blocks": 9}`; worktree-adapted variant (same regexes, disk reads) → identical counts.
- Simulation (in-memory, no writes, no `/tmp`): baseline blobs + RB1 block at r4-16 EOF + RB2 text at SCORECARD EOF + RB4 note at r2 EOF; item 3 has no tracked edit (`RB3.md:9`) → identical JSON.
- Anchors: PROVINCE `fe7f3f61…`/blob `8a1cec88…`; r4-16 `622e3661…` (925 L); r2 `541f3499…` (242 L); r3 `697804b5…` (137 L); SCORECARD `0c722936…` (559 L); README `f6fb46d6…`; SKILL `1e22c289…`.

## FINDINGS
- No landing present (corroborates `PB0.md:10`, `TB1.md:14`, `SB2.md:4`); r4-16 grep `output_directory|provider_blob_id|four sites` → 0 hits; r2 bleed loci `:12,:217,:236-237` unchanged. E2's absence finding still holds at 22:08; G3's integration check remains open.
- Neutrality is structural, not only simulated: EOF appends only grow cited line counts; the README coverage map (79 unique tokens; digest `bd70aa5f…b79750c4`, LF-terminated — G3:24's string is a 63-hex truncation; `TB1.md:11` concurs) and SKILL's 9 rules are untouched by every final text.
- Battery for integration: changed set ⊆ {r4-16, r2-jq-shadow, SCORECARD.md, LOG.md} (+r3-jq-provenance.md only if item 4 extends); `git diff --numstat HEAD --` deletions = 0; PROVINCE/README/SKILL blobs unchanged; rerun command A + token digest. Break vectors (new corpus/knowledge file; README/SKILL edit) are absent from all four dispositions.

## THREATS
Pre-integration snapshot: landed bytes were never observed; neutrality rests on simulation plus the structural argument. No probes/network. "7 values" not re-derived; cold-cache untested (out of scope). If integration lands different wording or placement, re-run the battery before recording 79/79.

## VERDICT
FINDING: no landing applied at snapshot; invariants hold and the three finalized texts are command-A/byte-neutral under simulation — post-integration re-run required.
