## CLAIM
The census must be fail-closed: exact ten-leg inventory, fixed denominator 10, locked per-leg predictions, and before/after host-state comparisons. A glob plus self-reported PASS labels is gameable.

## METHOD
Read-only at `f0e8cdecb216d71cf7df974675c0f6b16ba4f82f`. Reviewed round-5 census precedent (`.ufo/waves/luna-round-5/receipts/census-pre.sh:34-40`), round-2 package inventory (`.ufo/waves/luna-round-2/receipts/l12-catalog-digest.txt:16-38`), `PROVINCE.md:15-31`, and `git status --porcelain=v1 -uall` (pre-existing untracked `.ufo/interactive-sessions/` and prior wave files). No probes or repo changes.

## FINDINGS
- Inventory gate: require exactly `leg-1.md` … `leg-10.md`; reject missing, extra `leg-*`, symlink, non-regular, or empty receipts. Hash each complete receipt and verify the recorded SHA-256 of exact stdout bytes. Keep denominator 10 even when missing; missing/invalid legs are mismatches, not dropped rows. Suggested final inventory command (after battery):
  `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -c 'from pathlib import Path; import hashlib; d=Path(".ufo/waves/luna-round-6/receipts"); want={f"leg-{i}.md" for i in range(1,11)}; ps=list(d.glob("leg-*.md")); assert {p.name for p in ps}==want and all(p.is_file() and not p.is_symlink() and p.stat().st_size for p in ps); print("\n".join(f"{p.name} {hashlib.sha256(p.read_bytes()).hexdigest()}" for p in sorted(ps)))'`
- Score only against frozen predictions: L1 must be exact `6.5.0`/exit 0 and L2 exactly 207 parsed `tools/list` entries; generic RESULT labels would wrongly pass incorrect exact answers. L3–8 RESULT, L9–10 TYPED-REFUSAL; independently inspect the raw output because a receipt’s declared class can lie. Round-2 package/catalog inventory is not proof of a current running process (`PROVINCE.md:28-31`).
- “Zero mutations outside /tmp” literally conflicts with mandated repo-local receipts/report. Explicitly exempt only `.ufo/waves/luna-round-6/{CA6.md,receipts/leg-*.md}`. Compare pre/post filesystem state; current pre-existing untracked files mean a final `git status` alone cannot attribute changes. `/tmp` cwd does not contain npm writes: PROVINCE records the cache under `~/.npm/_npx` (`:19-22`); force npm cache/TMPDIR under `/tmp`. Hash the Devin/OMP/Kimi config paths before/after (`PROVINCE.md:16-18`) and fail on missing/unreadable baseline.

## THREATS
Receipt/hash checks prove byte integrity, not truth or that every process terminated. Snapshot comparison misses transient writes/deletes and concurrent actors; require write tracing or narrow the claim to detectable post-state. Census output must cite the prereg hash and snapshot hashes.

## VERDICT
FINDING: literal zero-outside-`/tmp` is unsatisfiable with required repo-local writes; define the evidence-path exception and bind exact outputs, predictions, and pre/post snapshots before scoring N/10.