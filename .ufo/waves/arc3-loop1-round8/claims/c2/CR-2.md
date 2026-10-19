# CR-2 — C2 live pin re-anchor

**Scope:** C2 evidence and patch text only. No PROVINCE, gate, custody, or other tracked source file was modified. The receipt is prepared under this seat's permitted evidence directory; same-commit landing with C1 remains an integration duty, not something this seat can attest.

## Verdicts

- **CORRECTED — PROVINCE locator.** First-hand read of `PROVINCE.md:18` shows `~/.kimi-code/config.toml:3546`. A targeted live search finds the sole `rea-agents@` match at line 4126, with `rea-agents@6.7.0`; therefore the current pointer should change from `:3546` to `:4126`.
- **VERIFIED — match and bounds.** `grep -cF` returned one match; `wc -l` returned 4,150. The target line is within the current file, and the unique matching pin is at 4126.
- **REPRODUCED — line content digest.** The targeted line's UTF-8 bytes excluding its LF terminator hash to `eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1`. The grep-emitted record including LF hashes to `eb1c7da74fc5f870d7c6537e87beeaf043491b5cdd00ee7a2f65e426d9f2b675`. See the seat receipt at `claims/c2/CR-2/receipt.txt`.
- **DISCREPANCY — receipt chronology in current row.** `date -u` at capture returned `2026-10-19T17:55:09Z`, while `PROVINCE.md:18` calls the `17:55:49Z` receipt historical. At measurement time that cited stamp was 40 seconds in the future. The patch below leaves this unrelated timestamp prose untouched; the operator/integrator should resolve or explicitly carry this chronology discrepancy.
- **UNVERIFIABLE — same-commit landing.** This seat may only write its own wave artifact directory. It cannot land the PROVINCE edit, C1 gate extension, or final receipt path together; the combined commit must be verified by the integrator.

## Re-derived command evidence

Capture time:

```text
$ date -u +%FT%TZ
2026-10-19T17:55:09Z
```

Targeted live pin search, count, and line-count:

```text
$ grep -nF 'rea-agents@' /home/vgpnk/.kimi-code/config.toml
4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
$ grep -cF 'rea-agents@' /home/vgpnk/.kimi-code/config.toml
1
$ wc -l /home/vgpnk/.kimi-code/config.toml
4150 /home/vgpnk/.kimi-code/config.toml
```

Line hashes (the first hashes the matched text without LF; the second hashes grep's record including LF):

```text
$ grep -F 'rea-agents@' /home/vgpnk/.kimi-code/config.toml | tr -d '\n' | sha256sum
eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1  -
$ grep -F 'rea-agents@' /home/vgpnk/.kimi-code/config.toml | sha256sum
eb1c7da74fc5f870d7c6537e87beeaf043491b5cdd00ee7a2f65e426d9f2b675  -
```

Measured repository revision: `git rev-parse HEAD` → `904b724258fc9396a016bd9952b5cd40225fb7d8`. `git diff --check -- PROVINCE.md; git diff --numstat -- PROVINCE.md; git status --short -- PROVINCE.md` emitted no output, confirming this seat did not alter the target source. The older R7 adjudication's re-receipt-first rationale is at `.ufo/waves/arc3-loop1-round7/claims/c1/C1-ADJUDICATION.md:48-62`; it is context only, not evidence for the current line or hash.

## PROVINCE patch text — not applied

This replaces one pointer token on the existing physical line; it is line-count neutral. The rest of the dated-row text remains byte-for-byte unchanged.

```diff
diff --git a/PROVINCE.md b/PROVINCE.md
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -17,3 +17,3 @@
 `rea-agents@6.5.0` (`/home/vgpnk/.omp/agent/mcp.json:8`), and Kimi
-`rea-agents@6.7.0` (`~/.kimi-code/config.toml:3546` at the 2026-10-19 re-read; the 17:55:49Z receipt's pointer :3298, and earlier :2940 [16:57:35Z] and :3227 [17:32Z], are historical). Cache/catalog
+`rea-agents@6.7.0` (`~/.kimi-code/config.toml:4126` at the 2026-10-19 re-read; the 17:55:49Z receipt's pointer :3298, and earlier :2940 [16:57:35Z] and :3227 [17:32Z], are historical). Cache/catalog
 identities (re-read 2026-10-18): 6.7.0 at `/home/vgpnk/.npm/_npx/a1722018f28f9df2` — 153 CLI
```

Patch check: extracting this fenced diff and piping it to `git apply --check -` exited 0. An independent in-memory replacement reported `pointer_occurrences_before 1 after 1 line_counts 162 162`.

## Receipt and integration handoff

Receipt bytes are in `claims/c2/CR-2/receipt.txt` (within the only permitted write scope); its re-derived file identity is 646 bytes, SHA-256 `f5c928146707483e097119c8b260ac41a516fda67549bfe39faf4fcbf1086398`. Suggested canonical landing path (not written by this seat): `.ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt`. Integrator must land the receipt, PROVINCE patch, and C1 extension in the same commit; if the receipt bytes or line are re-captured at landing, recompute both hashes and update the receipt before sealing the instrument anchor. No whole-config contents or whole-config digest were captured by this seat.
