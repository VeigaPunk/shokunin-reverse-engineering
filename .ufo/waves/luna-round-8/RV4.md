## CLAIM
Replay legs 9–10 on Kimi-pinned REA 6.4.0: the six 6.5-only verbs are absent from the advertised tools (L9); the jq control returns a result (L10).

## METHOD
From `/tmp`, ran `npx -y rea-agents@6.4.0 mcp`; in the same session requested `tools/list` and called `inspect_binary_layout` on `/usr/bin/jq`. Closed stdin and observed exit 0. Repeated L10 with `detail:"summary"` for the complete, compact stdout in `receipts/leg-10.md`. No config edits.

## FINDINGS
L9 `tools/list` returned 170 tools. Each of `inspect_go_binary`, `inspect_rust_binary`, `inspect_electron_fuses`, `inspect_sqlite_database`, `search_bytes`, and `inspect_with_objdump` was absent (six exact-name checks: `true`); matches.
L10 `inspect_binary_layout` returned Evidence `ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd` for `/usr/bin/jq` (SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`), class RESULT; matches. Summary replay linked `inspect_analysis_view` to parent `inspect_binary_layout`, with complete-within-view coverage 202/202. First combined session stdout: 2,127,950 bytes, SHA-256 `23e94d0ba95df1ce781d6d825f5431cba5fa3d8d6cc7b8bfce0983e8e6911799`.

## THREATS
The first session’s full `tools/list` schemas dominate its large stdout; the receipt records the full stdout of the successful summary repeat, not that catalog payload. No config-edit command was issued; npx may update its package cache. This is version differentiation only, not promotion.

## VERDICT
CLEAN
