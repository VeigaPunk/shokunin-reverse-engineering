# EX-3 — C2 PROVINCE pin re-anchor

**Scope:** C2 freshness evidence and proposed pointer edit only. No tracked source or operator-owned config was changed. The receipt is stored in this seat's evidence directory.

## First-hand re-derivation

- `git rev-parse HEAD` returned `904b724258fc9396a016bd9952b5cd40225fb7d8`.
- `Read(PROVINCE.md, lines 15–18)` returned line 18 as:

  ```text
  18  `rea-agents@6.7.0` (`~/.kimi-code/config.toml:3546` at the 2026-10-19 re-read; the 17:55:49Z receipt's pointer :3298, and earlier :2940 [16:57:35Z] and :3227 [17:32Z], are historical). Cache/catalog
  ```

- A fresh Grep for `rea-agents@` in `/home/vgpnk/.kimi-code/config.toml` returned the live match:

  ```text
  /home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
  ```

  The only matching pin line returned is at `:4126`; this re-derives the current locator and pin version independently of the earlier wave artifacts.
- I computed the SHA-256 over the exact matched line text (UTF-8, excluding the line terminator), and also over that text plus LF. Command output:

  ```text
  line_content_sha256_no_terminator=eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1
  line_record_sha256_with_LF=eb1c7da74fc5f870d7c6537e87beeaf043491b5cdd00ee7a2f65e426d9f2b675
  2026-10-19T17:53:54Z
  ```

  The matching line and both digests are recorded in [the receipt](EX-3/receipt.txt). The hash scope is explicit: it binds the pin line content, not the entire mutable config file.

## Per-item verdicts

- **VERIFIED — live pin:** the Kimi config search locates `rea-agents@6.7.0` at line 4126.
- **CORRECTED — PROVINCE pointer:** the current `PROVINCE.md:18` points to `:3546`; the live pin search points to `:4126`. The patch below changes only those four digits on the existing line, so it is line-neutral.
- **UNVERIFIABLE — same-commit landing:** the seat is restricted to artifact paths and cannot edit `PROVINCE.md` or land C1's gate change. The required same-commit relationship remains for the integrator to establish when applying both changes.

## Proposed patch text — not applied

```diff
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -18 +18 @@
-`rea-agents@6.7.0` (`~/.kimi-code/config.toml:3546` at the 2026-10-19 re-read; the 17:55:49Z receipt's pointer :3298, and earlier :2940 [16:57:35Z] and :3227 [17:32Z], are historical). Cache/catalog
+`rea-agents@6.7.0` (`~/.kimi-code/config.toml:4126` at the 2026-10-19 re-read; the 17:55:49Z receipt's pointer :3298, and earlier :2940 [16:57:35Z] and :3227 [17:32Z], are historical). Cache/catalog
```

This artifact supplies a current line-content receipt and patch proposal; it does not itself assert that either has been landed.
