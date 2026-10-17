# XB1 — lane B census runner 2: independent Command A + receipts census

## CLAIM
Command A reproduces exactly at the briefed round-9 records HEAD and at the actual current HEAD; the receipts store is 80 files (43 tracked / 37 untracked), all 43 tracked hashes recompute, and the sole MANIFEST.txt deviation is the disclosed round-8 leg-10 append supersession.

## METHOD
Read-only from repo root; no probes/network. `git rev-parse HEAD` → `c343939236d95f6027a67db6034920d06c83ac25`; the briefed `6e83a20` is no longer HEAD (`git diff --stat 6e83a20 c343939` = LOG +16, SCORECARD +12, zero deletions). Ran the `SCORECARD.md:92-123` recipe verbatim at REV=`6e83a2079385fc1ecbd5a854e772b77714362dfe` and REV=`c343939236d95f6027a67db6034920d06c83ac25`. Census: `find .ufo/waves/luna-round-N -path '*receipts*' -type f`; `git ls-files` over the r6/r8 receipt dirs; `git diff --quiet HEAD -- <those dirs>`; python sha256 recompute of C2.md's 43-row table and of all three MANIFEST.txt files; `head -n 59 .ufo/waves/luna-round-8/receipts/leg-10.md | sha256sum`.

## FINDINGS
- Command A, both revisions: `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "rule_blocks": 9}` — only `revision` differs; C1/A2 values reproduced.
- Receipts by round: r2 27, r4 1, r5 4, r6 26 (receipts 14 + receipts-B 12), r7 3, r8 17, r9 2; r1/r3 none; total 80. Tracked 43 (all of r6/r8; `git ls-files` = 43, `git diff --quiet HEAD` exit 0). Untracked 37 (r2 27, r4 1, r5 4, r7 3, r9 2).
- C2.md's 43-row hash table: 43/43 exact, 0 mismatch (includes r6 `census-laneB-pre.txt`=`320ee5a2…`, corroborating round-6 XB1; C2's 26/17 split matches).
- MANIFEST.txt: r6 lane-A 1/1 (L1 only; LOG.md:805-806 discloses this); r6 lane-B 10/10; r8 9/10 — `leg-10.md` row `c89eea7a…` vs current `6cd389e9…` (40,401 B); my `head -n 59 | sha256sum` = `c89eea7a…` (27,655 B): disclosed append supersession reproduced. Caveat: "MANIFEST annotated" (LOG.md:855) resolves to `receipts/census-laneB-pre.txt:266` (APPEND-SUPERSEDED), not an annotation inside MANIFEST.txt.
- Also reproduced D5: r2 `L7-mcp-tools-6.5.0.txt`=`dc740c46…`, `L5-help.txt`=`224965ba…`; B2.md:10's `a910c6…` ≠ the named receipt.
- Freeze fingerprints (sha256 of sorted `hash␣␣path` lines): untracked-37 `0f781ea28c8d1b41d8b40ab49dabd2f7c1974f1d48d52fd71dee733c2d7e5b32`; all-80 `6ead431d60e1a426f76f6bb3966222f5489b8aac89f5fdcdf6569302e4bbf673`.

## THREATS
Command A values were known from lane-A reports before my run (reproduction, not blind). Hashes attest bytes, not provenance; untracked receipts lack Git durability — the fingerprints above freeze them at `c343939`. Round-10 has no receipts dir; this seat wrote only this file.

## VERDICT
CLEAN — Command A reproduces at both HEADs; 43/43 tracked receipt hashes recompute; the one MANIFEST deviation is a reproduced, previously disclosed append.
