# SB2 — append-only pre-record (7 target files, HEAD=cfc84c2)

## CLAIM
Pre-record complete: tail-12-line sha256 pins for all 7 round-5 target files at HEAD (cfc84c2), plus full-blob sha256, line/byte counts, and last-line anchors. Working tree is byte-identical to HEAD for all 7 (hash-object == rev-parse HEAD:path), so a later append-only verifier can diff against either.

## METHOD
`git show HEAD:<f> | tail -12 | sha256sum` (tail pin); cross-checked via `sed -n 'N-11,Np'` — all 7 OK; full-blob `sha256sum`; `wc -l` / `wc -c`; identity check `git hash-object <f>` vs `git rev-parse HEAD:<f>`; final-byte check. `git status --porcelain` shows only untracked `.ufo/` paths — no tracked modifications. Read-only run; no tracked-file writes.

## FINDINGS
Format: path | lines | bytes | tail12 sha256 | full sha256
```
corpus/knowledge/2026-10-13-asar-surface.md | 91 | 11100 | 6281a096f9c778a30598964c6ef2e498c5a2e0dc79849ddc9c7fbe9f61c53dba | a55fc71cc009b6e33e04a9656c3f4df201b6835dad019818d4c25ff2beb6eec9
corpus/knowledge/2026-10-13-r4u-01-firmware-deep.md | 119 | 19470 | 113b27dd89c54aee9ecfcf987a43b8a12b8099ebd0e492a86d28799c2fdcc4a2 | d565f690dfb5d97f819a9489895736291ec8b6b0bd9d1986f0e0a66bafeca5ce
PROVINCE.md | 155 | 18038 | 7637dc55582ff686df2f2319898af05578a36f9e03ce5392aefe55164d67bcde | cd6c62292f09829fda76b396f9f791605d7cfcafbead15b348436f9d9c7bdca5
corpus/README.md | 173 | 37571 | 39d202f5fc34150670dd55bd32af28b97261fd4cf7ffb4c7edd5dcbe38f0f16c | 43a392ebe7361e51bc982ef6cdc5e789abd847b1ceefe71bf193660d0d9d30f4
corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md | 375 | 27727 | 351ae3a029a74ba6306839915de28ed29388b972e16f5b7a4f3c47b7ae7fc8b8 | 0e60215518c214f5a1e1ea4d7031269f1e8e24e84d504bfd2dd3f7f4a51e928d
corpus/knowledge/2026-10-13-r5-02-call-targets-jq.md | 194 | 12634 | cc9beb318bf9fe896426a02ba366513b461585f0a2662ca7b123f2d04925144a | 7387e01cc9cde9f06df0e9c1370d348d83b0d45667181ba77de3848c34138689
corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md | 108 | 23444 | 7f7f8106324d86c9a1b898926e4db892bb7daf83457ac41dd3a54cbbec965406 | 0a794bc13e8ab9cf635b882e39c9c6f06e3dedf31d22cd7760e43d93e89f5b80
```
Last-line anchors (append boundary): asar-surface → "  belongs to the r1-era asar sweep this entry summarizes."; r4u-01 → "  observations in this file remain true as written."; PROVINCE → "  (`HOPPER_LAUNCHER_PATH`), JEB."; README → "- Criterion-5 (observation/inference labels) is not uniformly applied"; r9-02 → "entry claims nothing outside lines 177–178."; r5-02 → "the 2 `jmp *…(%rip)` sites and any computed call lacking a reference e"; r12-01 → "  the defect there is queue-bookkeeping lag, per r12-02's ledger."

## THREATS
1. Tail-12 hash detects tail-region drift only, not mid-file edits — full-blob sha256 is recorded so a verifier can instead prove strict prefix-preservation (old blob bytes = exact prefix of new file).
2. Pins refer to HEAD cfc84c2; if HEAD moves they must be re-derived at that commit.
3. `tail -12` is newline-split; all 7 files end with LF (0x0a verified), and sed line-range cross-check matched all 7, so pins equal lines (N-11..N).

## VERDICT
CLEAN — all 7 baselines recorded, double-checked, and reproducible from frozen HEAD cfc84c2.
