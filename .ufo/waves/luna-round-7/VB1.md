## CLAIM
All cited values for evidence items 1–2 re-verify by recomputation: SC1/SC2 carrier SHA-256s, lane-A leg-3/leg-4 receipt digests, and (bonus) lane-B leg-3/leg-4 cited digests. No mismatch found.

## METHOD
Read-only at HEAD 411175e; no probes, no network. Commands: `sha256sum /usr/bin/docker /usr/bin/rg` and `file` on both; `sha256sum` over `/tmp/cc3-luna6/stdout3.raw`, `/tmp/rea-cc4/stdout-node.raw`, `/tmp/rea-bb3/*`, `/tmp/rea-bb4/*`; byte-equality via awk-extraction + `cmp` of receipts/leg-4.md:27-28 and leg-3.md:208; reconstruction and hashing of lane-B raw server stdout/stderr from receipts-B/leg-3.md:41-42,48.

## FINDINGS
- SC1 `/usr/bin/docker` = `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9` = SC1.md:11; `file` BuildID `9e64db63…` matches SC1.md:10.
- SC2 `/usr/bin/rg` = `d006acfe51619144af4709e85945fe3b5a6f05038d356c4d8f752a33b4ecae42` = SC2.md:10; BuildID `9c4ccf92…` matches.
- Leg-3 lane A: cited `fb47bd53…` (receipts/leg-3.md:221) = sha256 of `/tmp/cc3-luna6/stdout3.raw` (3,099,964 B; three frames: id=1 rea 6.5.0 initialize, id=2 tools/list, id=3 docker result with `ev_67186163…`, `70f68a77…`). leg-3.md:208 is byte-identical to that file's line 3 (`cmp`).
- Leg-4 lane A: cited `bc4902f7…` (receipts/leg-4.md:39) = sha256 of the 8,113 B block at leg-4.md:27-28, byte-identical to `/tmp/rea-cc4/stdout-node.raw` (contains `ev_0618e7a5…`, `inspect_rust_binary`, bytes 24944200).
- Lane-B leg-3 cited digests all recompute: `75b83edf` (leg-3.stdout, 12,904 B), `af23888b` (server stdout, 11,977 B, reconstructed), `2772e913` (server stderr, 181 B, reconstructed), `93b1cbb9` (probe-leg3.mjs) — receipts-B/leg-3.md:45,50,59,95. Lane-B leg-4: `84d489f7`, `15564e67`, `568cb4c3`, `9b40bde4` all recompute over /tmp/rea-bb4 files (receipts-B/leg-4.md:21-24,31,43-44).
- Retained receipt-file anchors: receipts/leg-3.md `01063004…`, leg-4.md `99a1c690…`; receipts-B/leg-3.md `97855851…` (= /tmp/rea-bb3/leg-3.reconstructed.md), receipts-B/leg-4.md `162b4831…`.

## THREATS
Lane-A receipts do not name their capture paths; the /tmp copies postdate receipt creation (19:03–19:06 vs 18:19–18:25), consistent with copied/re-run deterministic output — provenance beyond hash + content identity is not provable from the repo. /tmp is volatile, so this check is re-runnable only while those files persist (record them). Digests bind bytes, not tool correctness.

## VERDICT
CLEAN — every cited hash for items 1–2 recomputes exactly; none contradicted.
