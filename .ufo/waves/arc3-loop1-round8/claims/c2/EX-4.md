# EX-4 — C2 PROVINCE pin re-anchor

Claim: freshness — re-anchor the Kimi `rea-agents` pointer from the stale config line to the measured live line and provide a content-hash receipt. Scope is the EX-4 handoff artifact only; no source/config/gate/LOG file was edited.

## Re-derived evidence and verdicts

1. **`PROVINCE.md:18` points at `:3546` — REPRODUCED.** `git show HEAD:PROVINCE.md | python3 -c 'import sys; lines=sys.stdin.read().splitlines(); print(f"HEAD:PROVINCE.md line_count={len(lines)}"); print(f"HEAD:PROVINCE.md:18: {lines[17]}")'` returned `HEAD:PROVINCE.md line_count=162` and line 18 containing ``~/.kimi-code/config.toml:3546``. `git status --short -- PROVINCE.md .ufo/waves/arc3-loop1-round8` returned only `?? .ufo/waves/arc3-loop1-round8/`, so the tracked PROVINCE source was clean at measurement.

2. **Current live pin — VERIFIED.** A fresh dedicated search for `rea-agents@` in `/home/vgpnk/.kimi-code/config.toml` returned exactly:
   ```text
   /home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
   ```
   This establishes the live locator and the pin/version from the observed matching line; no other config contents are reproduced here.

3. **Candidate re-anchor is line-neutral — VERIFIED.** On the immutable HEAD snapshot, an in-memory one-occurrence substitution of `` `~/.kimi-code/config.toml:3546` `` with `` `~/.kimi-code/config.toml:4126` `` produced:
   ```text
   old_pointer_occurrences=1 new_pointer_occurrences=1 old_pointer_remaining=0 line_count_before=162 line_count_after=162 changed_line=18 line18_same_position=True
   ```
   The patch below changes only four digits on existing line 18, within the dated PROVINCE row; it adds or removes no lines. I extracted this exact diff from the artifact and ran `patch --batch --dry-run -p1` followed by a scratch-only application against a HEAD copy under `/dev/shm`:
   ```text
   PATCH_DRY_RUN_RC=0
   checking file PROVINCE.md
   PATCH_SCRATCH_APPLY_RC=0
   patching file PROVINCE.md
   SCRATCH_DIFF_EXACT=True
   LINES_BEFORE=162 LINES_AFTER=162
   ```
   Scratch verification confirms the delivered hunk applies and makes exactly the intended pointer substitution; the tracked source remains untouched.

4. **Live line content receipt — VERIFIED (captured 2026-10-19T17:55:23Z).** Hash contract: SHA-256 over the UTF-8 bytes of the exact observed `args` line, excluding its terminating LF. The executed `printf '%s' 'args = [ "-y", "rea-agents@6.7.0", "mcp" ]' | sha256sum` output was:
   ```text
   eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1  -
   ```
   For newline-inclusive reproducibility, `printf '%s\n' 'args = [ "-y", "rea-agents@6.7.0", "mcp" ]' | sha256sum` returned `eb1c7da74fc5f870d7c6537e87beeaf043491b5cdd00ee7a2f65e426d9f2b675`.

5. **Same-commit co-landing with C1 — UNVERIFIABLE by this seat.** This seat is authorized to deliver patch text and receipt only, not to edit tracked source or create the landing commit. The integrator must apply this pointer update in the same commit as C1's gate extension and re-derive the live locator/hash at that landing point; this receipt is time-bound to the capture above.

## Proposed patch text (not applied)

```diff
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -18,1 +18,1 @@
-`rea-agents@6.7.0` (`~/.kimi-code/config.toml:3546` at the 2026-10-19 re-read; the 17:55:49Z receipt's pointer :3298, and earlier :2940 [16:57:35Z] and :3227 [17:32Z], are historical). Cache/catalog
+`rea-agents@6.7.0` (`~/.kimi-code/config.toml:4126` at the 2026-10-19 re-read; the 17:55:49Z receipt's pointer :3298, and earlier :2940 [16:57:35Z] and :3227 [17:32Z], are historical). Cache/catalog
```

This is the exact full line read at `PROVINCE.md:18`; only the pointer digits change. Historical receipt references are retained as context, not asserted as current measurements.

## Revision identity

Read-only Git checks independently returned HEAD `904b724258fc9396a016bd9952b5cd40225fb7d8` and the resolvable work commit `7deeb36045209f3fbeb4460edd7aef5b5270af22`; HEAD summary: `arc3-loop1-round7: records — SCORECARD round section, LOG entry, round report (measured at work commit 7deeb36; C1 adjudicated-partial)`. Measurements above are against the current HEAD/live pin observation, not carried forward from the prior round.
