# SB4 — sentinel: format (lane B, deepseek-v4.1-flash)

## CLAIM
Report-format sentinel, read-only at 20:12–20:14: on a frozen 64-file frame (`ls *.md | LC_ALL=C sort` minus the then-arrived lane-B reports `SB1.md`, `TB1.md`), the systematic every-4th sample of 16 reports is format-clean — 16/16 exact five-section sequence, 16/16 ≤400 words (max 347, `F8`), 16/16 verdict line matching `^(CLEAN|FINDING)` (11 FINDING, 5 CLEAN), 15/16 with `path:line` citations (`S4` uses the allowed exact-command+output form). The whole wave directory was 95/95 conforming at 20:14:13. Landing-format state, however: 16 files carry underscore-form stems (`…-inspect_go_binary`) that Command A's `[a-z0-9-]+` truncates to `2026-10-16-l7-01-inspect`; and only `E6D` of the six entry drafts carries the required `source:`/`verified-at:`/`recheck:` header. Baseline Command A re-run at 411175e: 72/72, missing/dangling `[]`, 9/9, 10.0/10.0.

## METHOD
Frame: `ls *.md | LC_ALL=C sort` at 20:12 minus `SB1.md`/`TB1.md`/`SB4.md` (64 files); sample = ranks 4,8,…,64: C4 C8 E2V E4V E6V F4 F8 G4 K3 M2 P1 Q3 RB7 S4 Z1 Z5. Checks per file: heading sequence `## CLAIM/METHOD/FINDINGS/THREATS/VERDICT`; whitespace word count; last non-blank line `^(CLEAN|FINDING)`; citation regex `\.md:\d+`. Stems: `grep -lE '2026-10-16-l7-0[0-9]-[a-z0-9-]*_[a-z0-9_]*' *.md`; python `re.findall(r'2026-10-\d{2}-[a-z0-9-]+')` on both stem forms; `ls corpus/knowledge | grep -c '_'` → 0. Header grep in E1D–E6D. No probes, MCP, or network.

## FINDINGS
- Sample re-read at 20:14:13 reproduced the 20:12 run: no heading, word-cap, or verdict-format defect; `S4.md` carries its executed python command and exact output block instead of `.md:line` refs.
- Underscore-form stems in 16 files at 20:14:13: C3, DB6, F2, F3, FB1, G1, K3, K4, M1, P1, Q1–Q4, QB2, T2 — including landing drafts: map rows `M1.md:11-13`, Knowledge rows `K3.md:8-10` and `K4.md:10-12`; `FB1.md:8` independently reports the same divergence. Hyphenated candidates match the regex fully; all 72 existing stems are underscore-free.
- Draft headers: `E6D.md:12-14` compliant; E1D–E5D contain none (`G3.md:10` flagged E3D).

## THREATS
Moving frame: `RB7.md` landed mid-check (in-frame by sort rule); directory grew 64→95 during the session; later lane-B arrivals are outside the sample. Checks are structural, not semantic; nothing is landed, so 78/78, the six entries' QUALITY compliance, and prior-72 byte-identity remain unverified here. Word cap measured by whitespace split, heading words included.

## VERDICT
FINDING: sampled reports and the whole present directory are format-clean, but landing names must be normalized — 16 files carry underscore stems that truncate under Command A's regex, and 5/6 entry drafts lack the house metadata header.
