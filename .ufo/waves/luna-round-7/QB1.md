## CLAIM
Final QUALITY gate for entry 1: Z1's recommended `inspect_go_binary` text passes criteria 1-15; its only landing blocker is the missing house metadata header.

## METHOD
Read Z1.md:11-23 (recommended text), E1D.md, G1.md, E1V.md, corpus/QUALITY.md:11-25, CORPUS.md:17-19. Verified each citation against the two leg-3 receipts and SC1. Durability: `git ls-tree -r HEAD --name-only .ufo/waves/luna-round-6/` lists both leg-3 receipts; `git status --short .ufo/waves/luna-round-6/SC1.md` → `?? .ufo/waves/luna-round-6/SC1.md`. No probes, MCP, network, or writes.

## FINDINGS
Per criterion, PASS/FAIL:
1 PASS — sources resolve; both leg-3 receipts HEAD-tracked; SC1 untracked but auxiliary (receipts-B/leg-3.md:17-18 carries path+hash).
2 PASS — falsifiable: pinned hash, evidence id, offsets, settings.
3 PASS — domain-specific: Go build-info inspection.
4 PASS — `/usr/bin/docker` + SHA-256 `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9`.
5 PASS — labels: two Observations (captured description vs tested RESULT), Inference, Unknown/limitations (Z1.md:18-21).
6 PASS — Evidence ID `ev_671861638ed7fe544cce229c3d4a9258766337a5e72dcf79f107af713b596a4b` plus exact call `{"path":"/usr/bin/docker"}` (Z1.md:16).
7 PASS — unexamined named: PE/Mach-O, missing-metadata/rejected inputs, functions/source/types/decompilation.
8 PASS — pins rea-agents@6.5.0, server 6.5.0, provider `go-build-info` v1; claim source distinguished (captured description vs tested).
9 PASS — no runtime claim; explicitly excluded.
10 PASS — real carrier exercised; RESULT-class; "Round-6 call" states provenance; no Core promotion.
11 PASS — "complete module text/no unparsed lines" is parsed-and-complete (receipts/leg-3.md:164-166: `unparsed_lines:[]`, `complete:true`).
12 PASS (n/a) — real carrier, nothing synthesized.
13 PASS (n/a) — no occurrence counts.
14-15 PASS (n/a) — id cited, no identity-domain claim; keep it so (a cross-lane same-id claim would need the f(content,path,params) domain, QUALITY.md:24-25).

Gap outside 1-15: Z1's text lacks `source:`/`verified-at:`/`recheck:` — required by CORPUS.md:17-19 and parent ruling (d), the same catch G3/Z3 made for entry 3. Land as `corpus/knowledge/2026-10-16-l7-01-inspect-go-binary.md` (E1D.md:8; hyphenated, ruling (a)); G1's underscore name would break the map-token regex.

## THREATS
No re-execution under the no-probe rule; gate rests on retained receipts. SC1 is untracked and must not be the sole anchor (it is not). Criterion 10's "this round" spans round-6 exercise → round-7 landing; the text's "Round-6 call" makes that explicit. The metadata header must be added at landing; this seat cannot write corpus files.

## VERDICT
FINDING: criteria 1-15 all PASS; prepend `source:`/`verified-at:`/`recheck:` before landing as `2026-10-16-l7-01-inspect-go-binary.md`.
