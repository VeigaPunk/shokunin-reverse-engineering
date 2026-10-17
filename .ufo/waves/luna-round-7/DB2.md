## CLAIM
Entry 2 content-audit: every substantive claim in E2D's proposed `inspect_rust_binary` entry (E2D.md:10-17) is derivable from the two leg-4 receipts; four fixable gaps block clean admission as drafted.

## METHOD
Read-only claim-by-claim mapping of E2D.md against `.ufo/waves/luna-round-6/receipts/leg-4.md` (43 lines) and `receipts-B/leg-4.md` (71 lines), plus SC2.md, `corpus/QUALITY.md:11-25`, `/home/vgpnk/.kimi-code/skills/shokunin/protocol/CORPUS.md:17`, `SCORECARD.md:100-105`, M1.md, K3.md, F8.md, P0.md. `git ls-tree -r HEAD` lists both receipts (durable). No live probe, network, or tracked-file change; only this file written.

## FINDINGS
- Derivable, with exact support: both carrier paths+SHAs, Evidence IDs, provider `rust-auditable` v1, RESULT — A: `leg-4.md:7,9,12,21,28,43`; B: `receipts-B/leg-4.md:6,12,14,17,47,71`. `auditable_metadata:null` and no `.dep-v0`: A:28, B:47; inferred rustc `da80ed…` offset 2287779 (A:28) vs no `/rustc/` path/null (B:47); bounds 256 MiB input / 1 MiB section / 8 MiB report (both :28/:47). "No runtime behavior was tested" — no receipt line records executing either target (only `file(1)`, sha256sum, MCP); consistent with the tool limitation. Ruling (c) held: E2D.md:12 pairs each SHA with its own Evidence ID; no merged-artifact claim.
- Citation gap: the class word `RESULT` appears only at `leg-4.md:43` and `receipts-B:71` — outside E2D's cited ranges (:27-29, :46-53); append `:43` / `:71`.
- Format gaps: E2D.md:10-17 lacks the mandatory `source:`/`verified-at:`/`recheck:` opening (`CORPUS.md:17`; parent ruling d). Derivably correct header: `source: .ufo/waves/luna-round-6/receipts/leg-4.md:7-13,27-29,43; receipts-B/leg-4.md:11-18,46-53,67-71`. The Admission bullet E2D.md:17 is unlabeled (`QUALITY.md:15`); F8.md:10's pointer "(E2V:16)" does not carry that claim (E2V.md:16 is that report's own verdict line).
- Entry-2 rows still use underscore stems (M1.md:12, K3.md:9) while the landing name is hyphenated (E2D.md:2, P0.md:8); the scan allows only `[a-z0-9-]+` (`SCORECARD.md:102`).

## THREATS
Derivability rests on retained HEAD-tracked receipts, not re-execution; historical run truth is unverified. If underscored row tokens integrate as drafted, `C3.md:13` simulates mapped=72, missing=6, dangling=6 — contradicting the 78/78 landing claim. Prior-72 byte identity and post-integration Command A are parent checks, not verified here.

## VERDICT
FINDING: Entry 2 content is fully receipt-derivable; before admission add its `source:/verified-at:/recheck:` header, widen RESULT-class citations to leg-4.md:43 / receipts-B:71, label the Admission bullet, and hyphenate the entry-2 row stems.
