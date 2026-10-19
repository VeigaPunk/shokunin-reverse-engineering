# EX-6 — C2 PROVINCE pin re-anchor and receipt

## Result

- **Live pin line — VERIFIED.** Fresh lookup placed `[mcp_servers.rea]` at config line 4124 and its `args` at line 4126; the exact live line names `rea-agents@6.7.0`.
- **PROVINCE pointer — VERIFIED stale; CORRECTED in patch text only.** `PROVINCE.md:18` currently cites `~/.kimi-code/config.toml:3546`; the freshly observed pin line is `:4126`.
- **Line neutrality — VERIFIED.** Replacing only the pointer preserves the file's 162-line count and the changed row's 198 UTF-8 bytes (198 before and after). No source edit was applied.
- **Receipt — VERIFIED for the exact line text.** The line-content SHA-256 below is over its 42 UTF-8 bytes, excluding the line ending.
- **Same-commit landing — UNVERIFIABLE from this seat.** The source patch and receipt need to be integrated in the same commit as C1's gate extension; this artifact-only seat did not make that commit or write a central receipt.

## First-hand measurements

Fresh pin lookup:

```text
/home/vgpnk/.kimi-code/config.toml:4124:[mcp_servers.rea]
/home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
```

`PROVINCE.md:18` currently contains:

```text
`rea-agents@6.7.0` (`~/.kimi-code/config.toml:3546` at the 2026-10-19 re-read; the 17:55:49Z receipt's pointer :3298, and earlier :2940 [16:57:35Z] and :3227 [17:32Z], are historical). Cache/catalog
```

The `:3546` token is the stale pointer being replaced; the other historical text is preserved unchanged, not re-adjudicated here. The row is inside the dated PROVINCE entry (lines 15–26).

## Patch text (not applied)

This is the measured, one-token replacement on line 18; all other row content remains unchanged:

```diff
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -18 +18 @@
-`rea-agents@6.7.0` (`~/.kimi-code/config.toml:3546` at the 2026-10-19 re-read; the 17:55:49Z receipt's pointer :3298, and earlier :2940 [16:57:35Z] and :3227 [17:32Z], are historical). Cache/catalog
+`rea-agents@6.7.0` (`~/.kimi-code/config.toml:4126` at the 2026-10-19 re-read; the 17:55:49Z receipt's pointer :3298, and earlier :2940 [16:57:35Z] and :3227 [17:32Z], are historical). Cache/catalog
```

Measurement output from the in-memory replacement check:

```text
old_line_occurrences=1
whole_file_line_count_before_after=162/162
changed_line_utf8_bytes_before_after=198/198
```

## Receipt draft for integration

Captured immediately after the fresh Grep result at `2026-10-19T17:55:24Z` (UTC). The line number is locator metadata; the stable identity is the stanza/key plus content digest.

```json
{
  "captured_at": "2026-10-19T17:55:24Z",
  "source": "~/.kimi-code/config.toml",
  "stanza": "[mcp_servers.rea]",
  "key": "args",
  "line": 4126,
  "line_text": "args = [ \"-y\", \"rea-agents@6.7.0\", \"mcp\" ]",
  "line_text_encoding": "UTF-8",
  "line_ending_in_hash": false,
  "line_content_bytes": 42,
  "line_content_sha256": "eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1"
}
```

The receipt field `line_content_sha256` is SHA-256 of the displayed `line_text` exactly, without a trailing LF. For clarity, the separately computed LF-terminated variant is `eb1c7da74fc5f870d7c6537e87beeaf043491b5cdd00ee7a2f65e426d9f2b675`; that is **not** the receipt hash above.

## Scope and status evidence

At measurement, `git diff -- PROVINCE.md` and `git status --short -- PROVINCE.md` produced no output. Only this seat artifact was written. Integrator action remains: place the receipt under `.ufo/receipts/` or the established receipts path and apply the line-18 replacement in the same commit as C1. `LOG.md` and all source/custody paths were left untouched under the frozen seat write scope.
