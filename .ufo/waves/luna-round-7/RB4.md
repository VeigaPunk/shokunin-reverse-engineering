## CLAIM
Append-only audit: the landing's exact diff is seven paths — six new `corpus/knowledge/` notes plus `corpus/README.md` (+12/−0) — and nothing else; with hyphenated stems the unmodified Command A reaches the claimed 78/78.

## METHOD
Read the plan set (E1D–E6D/E1V–E6V, G1–G6, Z1–Z6, M1/M2, K3/K4, P0–P2, N1/N2) at HEAD `411175e` via `git show`/`git ls-tree`. Reproduced N2's two baseline digests. Inserted six hyphenated 3-cell map rows after `corpus/README.md:61` and six 4-cell Knowledge rows before `:141` in memory only, then ran the `SCORECARD.md:92-123` recipe verbatim. No tracked writes.

## FINDINGS
Exact expected diff:

```text
A corpus/knowledge/2026-10-16-l7-01-inspect-go-binary.md
A corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md
A corpus/knowledge/2026-10-16-l7-03-inspect-electron-fuses.md
A corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md
A corpus/knowledge/2026-10-16-l7-05-search-bytes.md
A corpus/knowledge/2026-10-16-l7-06-inspect-with-objdump.md
M corpus/README.md (+12/-0)
```

- Simulated Command A output: `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 78, "mapped": 78, "missing": [], "rule_blocks": 9}`. Hyphenation alone suffices; no SCORECARD.md/SKILL.md edit (K4's regex-widening alternative is unnecessary).
- Baselines independently reproduced: token digest `c538284b…` (`\n`.join(sorted(set)) + `\n`), 72-blob digest `3adf3bc2…` (`\n`.join(`<stem> <blob-sha256>`) + `\n`); HEAD census 72 .md + `.gitkeep`, 72 unique tokens = stems, Knowledge table 73 rows (72 + `lessons/round-13-distillation`).
- Drafts that must not enter the landing as written: `M1.md:11-13` and `K3.md:8-10` row tokens still underscore (`inspect_go_binary`); landed verbatim they give mapped=72, coverage 9.23 (C3/S1). `P2.md:2` drafts LOG.md + SCORECARD.md content — records-stage only (round-6 precedent: work `bc91424`, records `411175e`), outside the authorized diff. No other plan file proposes a tracked edit.

## THREATS
- Scouts SC1–SC6 are untracked at HEAD (`git status` → `?? .ufo/waves/luna-round-6/SC4.md`); legs 3–8 receipts (12 files) are tracked and unchanged, so receipt citations are durable and SC citations resolve worktree-only. Landing scouts would enlarge the diff (F8).
- The simulation is in-memory; post-landing Command A, QUALITY admission, and the 72-blob byte-identity gate remain unmeasured. Normalizing M1/M2/K3/K4 row text must apply the content rulings (E4 B-only per G4/E4V; E2 carriers distinct).

## VERDICT
FINDING: scope is exactly 7 paths under hyphenated stems; M1/K3 underscore row tokens and P2's LOG/SCORECARD drafts must not ride in the landing commit as written.
