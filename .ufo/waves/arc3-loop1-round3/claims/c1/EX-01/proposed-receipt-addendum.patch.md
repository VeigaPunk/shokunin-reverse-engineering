# Proposed change (PATCH TEXT — not applied) — EX-01 / chain c1 / arc3-loop1-round3

Targets (choose at integration; this seat has no write access to either):
  A. `.ufo/waves/arc3-loop1-round1/claims/c1/EX-02/install-receipt.txt` — append §10.
  B. `.ufo/waves/arc3-loop1-round3/records/**` (parent-written) — cite the ledger for
     the three package.json/package-lock pins, per F1.

Why: the receipt pins exactly two files by hash (soljson.js, solc.js — lines 101/102).
The prefix `package.json`, `package-lock.json` and `node_modules/solc/package.json`
hashes exist only in `claims/c1/receipts/chain-ledger.draft.md:35` (+ EX-04 receipt
line 31). All re-derived and MATCH on 2026-10-19 (EX-01, `compiler-check.txt` §2), but
the receipt alone cannot support a "receipt re-verified" sentence for those files. The
addendum also lands the compiler-core pin, which no artifact carried before.

## Hunk A — append to EX-02/install-receipt.txt

```diff
--- a/.ufo/waves/arc3-loop1-round1/claims/c1/EX-02/install-receipt.txt
+++ b/.ufo/waves/arc3-loop1-round1/claims/c1/EX-02/install-receipt.txt
@@
 Seat report: .ufo/waves/arc3-loop1-round1/seats/EX-02.md
 ================================================================================
+
+10. ADDENDUM — RE-DERIVED BY arc3-loop1-round3 SEAT EX-01 (2026-10-19)
+--------------------------------------------------------------------------------
+  Reuse check for round 3 (no install; read-only hashing + compiles on scratch).
+  Evidence: .ufo/waves/arc3-loop1-round3/claims/c1/EX-01/compiler-check.txt
+
+  a) Pin-scope note: this receipt pins exactly two files by hash (§6). The three
+     other tree pins are recorded in claims/c1/receipts/chain-ledger.draft.md:35
+     (and node_modules/solc/package.json also in EX-04/compile-receipt.txt:31):
+       tools/solc-prefix/package.json            sha256 b4205b088e5cfa42851bd673ac3d6656599bb32eaf3de112132f8d0bf3b61225
+       tools/solc-prefix/package-lock.json       sha256 9f6dcab2bbb454040be487fced0c87efa6f3cc7e90cf7275c37305a47e3d470c
+       tools/solc-prefix/node_modules/solc/package.json  sha256 b3a90035cab4e8aa43068f33f01497dccfb77b294e1ea30c5fb32a9631e33491
+
+  b) All pins re-derived on disk this date — all MATCH, incl. tarball
+     sha256 0e1a1ab6…575a51 (6476046 B) and sha512 = registry integrity,
+     re-hashed from the npm cache content file named in §4; 0 files in the
+     prefix modified after the install minute; the tracked package.json /
+     package-lock.json blobs equal their git blobs ab95d628… / 9d9a7f28….
+     Whole tree re-attested against the cache tarballs, package by package:
+     8/8 IDENTICAL (script: arc3-loop1-round3/claims/c1/EX-01/attest-prefix-vs-cache.py).
+
+  c) Compiler CORE pin (new — the wasm module embedded in soljson.js; there is no
+     soljson.wasm on disk, and the version literals are absent from soljson.js /
+     solc.js / package.json text):
+       embedded module   22012583 bytes
+       sha256            df14c4e5ee58b27f06b6ce9966d6de6d6382dbe6b43e41a387c9812648afca1e
+       contains          "commit.f401782d.Emscripten.clang"; solidity_version()
+                         -> 0.8.37+commit.f401782d.Emscripten.clang
+       re-derive with    arc3-loop1-round3/claims/c1/EX-01/capture-embedded-wasm.js
+       ambient tree      byte-identical (same sha256) — the §6 cross-check extends
+                         from soljson.js/solc.js to the compiler core itself
+       deterministic     same size + sha256 across 3 captures
+
+  d) Operability re-run: solcjs --version -> 0.8.37+commit.f401782d.Emscripten.clang
+     (exit 0, by absolute path and via node solc.js); smoke source recompiled with
+     --bin --abi --optimize and with --optimize --optimize-runs 200 -> bin
+     530efc7b…6a5f (1370 hex chars) / abi 73441f84…081a, i.e. the §5 bytes exactly,
+     rerun-identical.
```

## Hunk B — one line for the round-3 records (parent discretion)

```diff
+Compiler (reused r1 prefix) — EX-01 re-derived every pin: receipt §6 pair MATCH;
+package.json / package-lock.json / solc's package.json pins live in the r1 chain
+ledger:35 (MATCH); tarball sha256 re-hashed from the npm cache content file; whole
+tree 8/8 identical to cache tarballs; NEW pin embedded wasm sha256 df14c4e5…afca1e
+(22012583 B); smoke recompiles byte-exact, rerun-identical; prefix node_modules/ is
+gitignored (compiler bytes on disk only). No install run.
```

## Not proposed

- No change to `corpus/`, `SCORECARD.md`, `LOG.md`, `README`, or the pointer table:
  this seat collected no evidence that any of them is wrong. The one wording risk is
  in `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:7` ("a `/tmp`-defaulted run
  fails EDQUOT … a disk-backed `TMPDIR` is required, not optional") — that statement is
  scoped to the rea-agents/EVMole probe, and it remains true for that probe; the seat's
  measurement (compiler-check.txt F4) shows only that /tmp accepts writes again now and
  that solcjs itself is fine either way. Reword only if a later round re-measures the
  probe's failure mode; not worth a patch on today's evidence.
- No `.gitignore` change: tracking `node_modules/` is a repo-level decision (F3 records
  the exposure and the zero-cost mitigation; the parent owns the call).