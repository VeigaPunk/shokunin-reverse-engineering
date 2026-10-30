# SentCreds — credential and vendor-bytes scan (round 51, wave 1)

**Verdict: PASS.** The round-51 wave surface carries **no credential values** and **no vendor
firmware bytes**. The four largest files under `corpus/evidence/round-50/c1/` are JSON extraction
manifests, not images. One **carried** L0 (unredacted GitHub session cookies in *pushed history*,
already open at `plans/round-51-claims.md:250`) is re-measured and re-confirmed — the tips are
clean, three live blobs are still reachable from `origin/main`. Nothing new is added by this wave
and nothing was re-appended.

Full receipt with every command, exit code, stdout sha256 and UTC stamp:
`.ufo/waves/round-51/w1/SentCreds/scan.md` (+ `final-receipts.json`, `whole-tree-credscan.json`
beside it).

## The three findings that matter

1. **Round-51 surface is credential-clean (measured, not assumed).** The lane's own calibrated
   scanner (`tools/round-50/w3/SentReceipts/credscan.py`, 12 classes, values never reproduced)
   returns `live_hits 0`, `placeholder_hits 0` over `plans/round-51-claims.md` +
   `.ufo/waves/round-51/` (119 files), `corpus/evidence/round-50/c1/` and `tools/round-51/`.
   Every credential-*word* hit is itemised in the receipt as a false positive with `file:line`:
   `claims.md:250` (the L0 line itself), `gen-w1.py:21`/`:138` and `w1-spec.json`/`w1-dispatch.json`
   (the contract's own prohibition text), `c1-counter.py:583`/`:2446` (`sid_tokens`) and
   `sqfs-triage-v6.py:98-813` (the action-vocabulary tokenizer), plus **vendor firmware file paths
   inside the round-50 manifests** (`webuicookie.lua`, `cookie.js`, `sso_password.js`, `passwd`).
   Zero `op://`, private keys, `AKIA*`, `ghp_*`, JWTs.

2. **No AVM vendor bytes in the lane tree — working tree *and* full git history.** All 12 pinned
   sha256 values from `tools/round-50/carriers.json` (4 carriers + 4 vendor images + 4 tar
   members) were searched against every working-tree file ≥ 100 kB (1 019 hashed) and every history
   blob > 1 MiB (55 of 48 900 objects hashed): **NONE**. Every SquashFS in `corpus/` is a
   **non-AVM-marker** fixture (`mkfs_time != bytes_used`), so no AVM-written image is committed
   either. The `after.json` receipts are large because they are **manifests** (~4 556 file entries
   and ~637 gap entries per carrier: path, size, sha256, handler) — measured 0 base64 blobs ≥ 300
   chars, 0 control bytes, strict UTF-8 JSON, `file` → `JSON text data`. The round-51 fetcher
   draft's header handling is byte-identical to round-50's (no `getheaders()`, no `Set-Cookie`
   read); `c1-run.sh` copies only four text TSVs into the lane.

3. **Carried L0 re-confirmed with fresh measurement, and it is a *history* problem only.** At
   `HEAD` all 15 `set-cookie:` lines in the 64 `.hdr*` files are placeholders (`[redacted…]` /
   `<redacted>`). But three live blobs remain reachable from the pushed ref
   (`git rev-list origin/main --objects`): `ba6b0d6e…` (round-45 `f1.hdr`, `_gh_sess` 352 chars),
   `5f8478b4…` (round-49 `C1CarrierPins/receipts/tree.hdr`, 348), `815e2951…` (round-49
   `C1S138Reopen/receipts/top.hdr`, 364). This is the finding the round-50 sentinel recorded
   (`.ufo/waves/round-50/w1/C1SentinelFetch.md:30`, `.ufo/waves/round-50/w3/SentReceipts.md:64-65`)
   and the closure left open by decision; remediation needs a history rewrite + force-push or an
   operator-authorised rotation — both outside a wave seat's remit. **Impact low** (`logged_in=no`,
   anonymous GitHub session cookies).

## One hygiene item for the L1 (not a containment defect)

`git status --porcelain` shows `?? tools/round-51/` — a wave-1 draft
(`tools/round-51/c1-run.sh`, 46 142 B, mtime 2026-10-30 01:58) sitting in the lane's `tools/`
rather than under `.ufo/waves/round-51/w1/<seat>/`. `ScribeReadme.md:80-85` already reported it. I
did not touch it. It is credential-clean and vendor-byte-clean, so it is a **hygiene** question
only: whether it is moved into its owning seat's directory before the freeze, so the freeze stays
the single commit that adds the round-51 instruments.

## Scope and honesty notes

* No REA run, no `--data-run`, no vendor download, no lane or fleet mutation: read-only
  (`git log/show/ls-tree/rev-list/cat-file/merge-base`, `status`); no commit, push, stage or stash.
  The receipts examined are the **committed round-50** ones, not fresh data.
* The credential scan is **pattern-based** (12 classes); the whole-lane-tree sweep
  (47 715 files / 735 608 832 B) was the mitigation — its 9 live-class hits were each manually
  classified and are all synthetic (round-49 sentinel self-test fixtures, one placeholder whose
  own text says it is a demo value, one fictional hex token in a report *about* secret-file
  detection, and one coincidental substring inside a 10.7 MB binary patch). No literal value is
  reproduced in either deliverable.
* The vendor-byte check is **pin-based plus AVM-marker-based**: it proves the four pinned AVM
  images and their members are absent; a re-encoded or non-SquashFS vendor payload would not be
  caught by either test.
* The tree changed under the scan (siblings kept writing); the round-51 surface was re-scanned at
  2026-10-30T05:08:08Z after the last sibling write observed at that moment.
* **Tooling: none installed.** The lane's own round-50 scanner was reused read-only plus stdlib
  `hashlib`/`json`/`re`/`subprocess`. No pacman/`uv`/`npx` transaction, so the pacman guard was
  never engaged. Scratch `/fast/scratch/hyaku/kaidoku-r51/w1-SentCreds` was removed after the
  receipts were copied into the seat directory.
