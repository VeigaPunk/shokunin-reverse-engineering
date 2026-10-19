# CR-1 — C2 PROVINCE pointer re-anchor

## Verdicts

- **PROVINCE preimage — VERIFIED.** `PROVINCE.md:18` currently points Kimi's `rea-agents@6.7.0` pin at `~/.kimi-code/config.toml:3546`.
- **Live pin — VERIFIED.** First-hand `Grep` output places `[mcp_servers.rea]` at line 4124 and `args = [ "-y", "rea-agents@6.7.0", "mcp" ]` at line 4126.
- **Correction — CORRECTED (patch prepared, not applied).** The patch below changes only `3546` to `4126`, a same-line / line-count-neutral edit.
- **Durable receipt registration and same-commit landing — UNVERIFIABLE from this seat.** Write scope is limited to this seat artifact; neither `PROVINCE.md` nor a shared receipt path was edited. The captured receipt is attached below for the integrator to land alongside C1.

## First-hand evidence

- `git rev-parse HEAD` → `904b724258fc9396a016bd9952b5cd40225fb7d8`.
- `Read(PROVINCE.md, line_offset=14, n_lines=20)` → line 18 contains `~/.kimi-code/config.toml:3546`.
- `Grep(pattern="rea-agents@", path="/home/vgpnk/.kimi-code/config.toml")` → `/home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]`.
- `Grep(pattern="^\\[mcp_servers\\.rea\\]$", path="/home/vgpnk/.kimi-code/config.toml")` → `/home/vgpnk/.kimi-code/config.toml:4124:[mcp_servers.rea]`.
- Capture time: `2026-10-19T17:54:14Z`; content hash and its exact byte scope are in `CR-1/evidence/live-config-receipt.txt`.
- `.ufo/receipts/` is absent in this checkout; the receipt is therefore retained only under this seat's permitted evidence directory. Integrator must place it in the project's durable receipt path as part of landing.

## Proposed patch text — NOT APPLIED

```diff
diff --git a/PROVINCE.md b/PROVINCE.md
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -18 +18 @@
-`rea-agents@6.7.0` (`~/.kimi-code/config.toml:3546` at the 2026-10-19 re-read; the 17:55:49Z receipt's pointer :3298, and earlier :2940 [16:57:35Z] and :3227 [17:32Z], are historical). Cache/catalog
+`rea-agents@6.7.0` (`~/.kimi-code/config.toml:4126` at the 2026-10-19 re-read; the 17:55:49Z receipt's pointer :3298, and earlier :2940 [16:57:35Z] and :3227 [17:32Z], are historical). Cache/catalog
```

The stable locator is stanza `[mcp_servers.rea]` + key `args`; the numeric line is recorded only as this capture's coordinate. Receipt SHA-256 covers the exact `args` line as UTF-8 without a line terminator.
