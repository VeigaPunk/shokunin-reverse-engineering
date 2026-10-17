# YB4 — /tmp litter attribution audit

## CLAIM
Per-artifact attribution to kaidoku rounds is provable two ways: receipt+hash (path cited in a kaidoku wave receipt; recomputed sha256 equals the record) — 9 artifacts verified — and content self-identification (repo paths/copies) — 37 of 152 top-level entries. The remainder cannot be provably separated from sibling sessions by name/mtime alone. No deletion performed.

## METHOD
Read-only. `findmnt -T /tmp` → tmpfs born 2026-10-16 18:47:46, so all litter is post-boot and older cited scratch (`/tmp/r3-asar-list.txt`, `/tmp/r4u`, `/tmp/r10-02-scratch`, `/tmp/r9-*`) is absent. Inventory `ls -la`; `rg -l 'kaidoku'` plus commit-hash (`a280e07|411175e|3395b6d|6e2ee8f`) and sibling-repo searches; recomputed sha256 of receipt-claimed artifacts; read rounds 6–9 receipts.

## FINDINGS
Tier 1 — recomputed hash equals receipt record: `xb1-r8/census.py` a0fc12ef = census-laneB-pre.txt:18; `rea-cb5/census2.py` f52e6d20 = CB5.md:5; `zb3-broken-sim.md` d641e3d3 = QB1.md:9 / census-pre.txt:97; `kaidoku-luna-round-8-leg-3-mcp.stdout` 5c682099 = receipts/leg-3.md:6; `luna-round-8-ex7-run/mcp.stdout` 866f8b58 = DB2.md:11; `kaidoku-luna-round8-rv1/leg1.stdout` 3754366908ac = PB0.md:9; `kaidoku-luna-round-8-leg10.stdout` 23e94d0b = CB8.md:9; `rb8-knowledge-manifest.txt` 694f8ed3 = RB8.md:14; `tb1-r7/run{1,2}.out` 77b10639 = (round-7) TB1.md:14.

Tier 2 — content self-ID: five `kaidoku-luna-*` entries (one cited by tracked `corpus/knowledge/2026-10-16-l7-01-inspect-go-binary.md:5`); `bb2-sim`, `cb3-sim`, `rb5-sim`, `qb2-sim` contain repo copies (`.git/config`).

Tier 3 — name/mtime only (~90 entries): `tb1-r8`, `vb*`, `zb3-*`, `cb2-*`, `hb2-*`, `rea-bb*/cc*`, `m*.log`.

Non-kaidoku: steam/`sdk165`/`dumps/`, `t_*.log`, `arms-rum-preload.cjs`.

Live: 157 entries; `sb4r9-*`, `gb2-*`, `pb1-r9` written 21:58–22:00 mid-audit.

## THREATS
Receipts are lane-authored, mutable, unsigned; a hash proves custody, not authorship. Round 9 reuses round-8 seat codes (HB2.md, CB4.md landed 21:55–22:00), so prefixes span rounds. No sibling-session /tmp records are inspectable from this repo → tier-3 separation is unprovable here. Seven root-only dirs unread; inventory drifted mid-audit.

## VERDICT
FINDING: attribution is provable only per-artifact (9 receipt+hash, ~37 self-ID); the majority cannot be separated from sibling sessions by name/time; recommend no unilateral cleanup — freeze wave, then an operator-owned manifest (hash, receipt pointer, tier) before any deletion.
