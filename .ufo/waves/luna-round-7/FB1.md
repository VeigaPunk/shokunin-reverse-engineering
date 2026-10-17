## CLAIM
Format audit of round-7 entry drafts 1–2 (E1D `inspect_go_binary`, E2D `inspect_rust_binary`): destination/row names, metadata fields, heading and label conventions, checked against house style and sibling entries.

## METHOD
Read-only: E1D, E2D, E1V, E2V, siblings E3D–E6D, G1, row drafts M1/K3, `corpus/QUALITY.md`, `corpus/README.md` rows, `/home/vgpnk/.kimi-code/skills/shokunin/protocol/CORPUS.md:17`, all 72 `corpus/knowledge/*.md` (field counts), plus a python `[a-z0-9-]+` token simulation. HEAD 411175e; no probes, MCP, or network.

## FINDINGS
- **Name divergence (blocks the round claim).** The drafts define hyphenated destinations — `E1D.md:8` `corpus/knowledge/2026-10-16-l7-01-inspect-go-binary.md`, `E2D.md:2` `…l7-02-inspect-rust-binary.md` — but the rows that will land for them use underscore stems: `M1.md:11-12` (`knowledge/2026-10-16-l7-01-inspect_go_binary`, `…l7-02-inspect_rust_binary`) and `K3.md:8-9`. A `[a-z0-9-]+` extraction over those tokens yields only the truncated `2026-10-16-l7-01-inspect` (python check over the drafts), so landing M1/K3 verbatim breaks command A's mapped/missing/dangling. Underscore variants also at G1.md:2, P1.md, Q1.md, F5.md, C3.md, T2.md (Q2 mixed); N1/P0/TB1 already hyphenate. Ruling (a) ⇒ normalize all landed names at integration.
- **Fields.** E1D/E2D bodies lack `source:`/`verified-at:`/`recheck:` (CORPUS.md:17; sibling pattern E6D.md:12-14). FB4 audits this across all six; E1D already carries the material (`E1D.md:19,26`), so it is a label/prepend fix, not missing evidence.
- **House deltas (minor).** 72/72 corpus entries open with an HTML `<!-- corpus entry — … -->` header; no round-7 body I read has it (round-wide; parent decides). E1D's title (`E1D.md:13`) lacks the backticked verb/version that E2D:10 and E6D:10 use.
- **Cleared.** Hyphenated numbered destinations; map rows are 3-cell/4-pipe (`M1.md:11-12`) and Knowledge rows 4-cell/5-pipe (`K3.md:8-9`); observation/inference/unknown labels (`E1D.md:21-24`; `E2D.md:12-17`); RESULT-no-Core statements (`E1D.md:30`; `E2D.md:17`); entry 2 keeps lane-A/B carriers distinct (`E2D.md:12-13,20`), per ruling (c).
- **Side note.** `E1D.md:2`'s "E1V.md was not found" is not reproducible now: E1V.md exists (mtime 19:56:45; E1D written 19:57:51) — timing artifact plausible, and E1V's CLEAN verdict conflicts with no claim in E1D.

## THREATS
Command A was not run (not an in-repo script); its token behavior is simulated from the parent-stated `[a-z0-9-]+`. Drafts are untracked and lanes wrote concurrently. Not verified: post-landing counts, prior-entry byte identity, and rows for entries 3–6 (sibling seats' scope).

## VERDICT
FINDING: entries 1–2 bodies are format-clean apart from the missing house field block, but M1.md:11-12 and K3.md:8-9 must be normalized to the hyphenated stems before landing or command A's mapped=78 / dangling=[] cannot hold.
