# R25-A3-W1 — Integrity of the saved C2 evidence (round-25 a2)

Seat `KaidokuR25a3.EvidenceIntegrity` (leaf executor, no delegation). Target
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-25/a2/c2`. Audit window
2026-10-22T10:36Z–10:47Z. Lane read-only: only this report was written in the lane; no git write, no jj,
no network fetch.

## Verdict summary

- A1 response sha256 vs its `db/manifest.json` entry — **holds**, 138/138 match, 0 mismatch.
- A2 manifest URL vs the file's database and selector (and page) — **holds**, 138/138, 0 mismatch.
- A3 response body actually answers the requested selector (extra check) — **holds**, 138/138, 0 mismatch.
- A4 `rea-run.txt` `sha256=` vs sha256 of `envelope.json` bytes — **holds**, 6/6, 0 mismatch.
- A5 `rea-run.txt` `carrier_sha256=` vs sha256 of the carrier hex file — **holds**, 6/6, 0 mismatch.
- A6 every `carriers.tsv` path exists in the lane — **holds**, 12/12 (6 hex + 6 ABI) exist.
- A7 manifest lists only existing files; no extra files on disk — **holds**, 0 missing, 0 extra.
- A8 saved a2 evidence reproduces the committed a3 tally — **holds**, byte-identical.

**No mismatch was found in any check; every mismatch list is empty.**

## Counts checked

- Manifest entries across 6 carriers' `db/manifest.json`: **138** (carrierb 16, carrierv 30, kdxtoken 12, rv2token 10, stewardtoken 44, vaultb-opt200 26). Response files on disk: **138** (144 JSON files under the six `db/` dirs, minus 6 manifests). `rea-run.txt` files 6; `carriers.tsv` data rows 6 (2 paths each).
- Name patterns: 69 `4byte-<8hex>-p0.json`, 69 `openchain-<8hex>.json`. Every 4byte file is page 0, so the fetch loop never followed a `next` link (observation, not a defect).
- Selectors covered: **69** (5+6+13+8+22+15), each with exactly one 4byte and one openchain response; the envelope selector set equals the db selector set for all six carriers.

## Evidence per check

**A1 — response sha256 vs manifest sha256.** Command `python3 -I -B /fast/scratch/hyaku/kaidoku-r25-a3/seats/EvidenceIntegrity/verify_evidence.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --json …/verify-report.json` (exit 0, 10:40Z; re-run at 10:47Z, exit 0, identical summary). Stderr summary line, verbatim: `SUMMARY checked=138 manifest_entries, 138 response_files, sha256_ok=138, url_ok=138, body_ok=138, rea_runs=6, rea_sha256_ok=6, rea_carrier_sha_ok=6, carrier_paths_exist=12, carrier_paths_missing=0, mismatches=0`. Mismatches: none.

**A2 — manifest URL vs file database/selector.** Rule per file: `4byte-<sel>-p<page>.json` ⇒ URL has `4byte.directory` **and** `hex_signature=0x<sel>` (plus `page=<page>` iff page > 0, no `page=` when page = 0); `openchain-<sel>.json` ⇒ URL has `openchain.xyz` **and** `function=0x<sel>`. Result `url_ok=138, url_bad=0`. Example rv2token: `4byte-095ea7b3-p0.json` ↔ `https://www.4byte.directory/api/v1/signatures/?hex_signature=0x095ea7b3`, `openchain-095ea7b3.json` ↔ `https://api.openchain.xyz/signature-database/v1/lookup?function=0x095ea7b3&filter=false`. Mismatches: none.

**A3 — body answers the requested selector (beyond assigned scope, cheap and decisive).** For each 4byte body every `results[].text_signature` was keccak-256 hashed with the lane's own `tools/round-25/a2/resolve-selectors.py` keccak and must equal the filename selector: 69/69 files clean, 0 keccak-mismatch candidates. For each openchain body the `result.function` map must contain `0x<sel>`: 69/69 present. `body_ok=138, body_bad=0`, agreeing with the committed a3 tally (`keccak_mismatch_candidates: 0`).

**A4 — `rea-run.txt` sha256 vs `envelope.json` bytes.** sha256 recomputed over the raw bytes of each `envelope.json`, compared with the `sha256=` field: 6/6 equal, 0 mismatch. Examples: rv2token stated `ed4a1118dfc7a180fac794541371019ce8bc2272908860bc1fd4bf99ad2cbf50` = actual; stewardtoken stated `1de20e9604885579649a6486306518a906c1aac6c4961a818e53d3cdd82b642a` = actual.

**A5 — `rea-run.txt` carrier_sha256 vs the carrier hex file.** sha256 recomputed over each `carriers.tsv` hex path in the lane and compared with `carrier_sha256=`: 6/6 equal, 0 mismatch. The same digest equals the envelope `subject.digest.sha256` in all six cases, and `envelope.subject.local_path` equals the `carriers.tsv` hex path in all six cases (0 mismatch).

**A6 — `carriers.tsv` paths exist in the lane.** All 12 listed paths exist as regular files under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/` (6 runtime hex under `.ufo/waves/arc3-loop1-round1|3|4/…`, 6 compiler ABI files). 0 missing.

**A7 — manifest/file set agreement.** 0 manifest entries without a file on disk; 0 db files missing from the manifest. Each carrier's `fetch.txt` count equals its manifest length (16/30/12/10/44/26 = 138).

**A8 — end-to-end reproduction of the committed a3 tally.** Command `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-25/a3/tally-resolution.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --out /fast/scratch/hyaku/kaidoku-r25-a3/seats/EvidenceIntegrity/tally-rerun` (exit 0, 10:42Z). The regenerated `tally.json` and all six per-carrier analyze files are **byte-identical** to the committed `corpus/evidence/round-25/a3/c2/analyze/*.json` (`cmp` clean; tally sha256 `479bc13ea4c2139289808a54c47321c83c3daafffaad5de4b06c00ac840b40dc` on both sides): the saved a2 evidence is exactly the input that produced the committed a3 numbers.

## Supporting cross-checks (observation)

- `git status --porcelain -- corpus/evidence/round-25/a2/c2` is empty: all 163 tracked files (138 responses +
  6 manifests + 6 envelopes + 6 `rea-run.txt` + 6 `fetch.txt` + `carriers.tsv`) are committed and unmodified in
  the working tree (`git ls-files` = 163).
- The attempt-3 REA replay envelopes in `corpus/evidence/round-25/a3/c2/rea-replay/*.json` have the **same sha256**
  as the attempt-2 saved `a2/c2/<carrier>/envelope.json` bytes for all six carriers (rv2token `ed4a1118…`, kdxtoken
  `1bc65b6f…`, vaultb-opt200 `506c9101…`, carrierb `95e86017…`, stewardtoken `1de20e96…`, carrierv `a2e7ba7b…`) —
  independent confirmation that the saved envelopes are genuine REA 6.5.0 output, not hand-written. Fetch
  timestamps span 2026-10-22T08:28:09Z–08:31:37Z and the REA runs precede them (08:27:59Z–08:28:04Z).

## Artifacts (outside the lane; the L1 integrates)

Under `/fast/scratch/hyaku/kaidoku-r25-a3/seats/EvidenceIntegrity/`:

```
verify_evidence.py 247a7ecaacf1eb80ea3ff604c3afdb1265f48f2f2ec9c0acd29aac2596687c83   verify-report.json c4c6f160f1458f57410468f75aab556f03652bd7c3f2a7e43f08203162bfac3a
verify-stdout.json 1aad56311917e5c8c224461aa11f8b7f0594b20bcfd815e59fe43928f830ed37   verify-summary.txt e1f921aec09297463cc03ce11b7a4850cf066e00ebaf7d173a75582b4bbfb6bc
rerun-tally.json 7e02dbbe048da684b217b5c535423db41938c41a9b4767d5f13359fb628ca2b7   rerun-tally.err (empty stderr) e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
tally-rerun/tally.json 479bc13ea4c2139289808a54c47321c83c3daafffaad5de4b06c00ac840b40dc   tally-rerun/rv2token.json 76edb9ecbaacbc680d636afc7e5a2afb18717047595421863d7696bf736cc2b1
tally-rerun/kdxtoken.json 233f1260115766dde6818a88eb102a8e427badfc10c783b0079693d46aff2f8b   tally-rerun/vaultb-opt200.json 7be57d1a9c0985437ee1bfdc47d897de31598a4689c1984134904d7e569ad040
tally-rerun/carrierb.json 6b5b13288b232d5b4a564769785e4b90243e1611215e715865bb8fb317b059cc   tally-rerun/stewardtoken.json 8874ecbefe24b50368319e36ae96030c7e0a5b3dc6a89800e12966d24b202e63
tally-rerun/carrierv.json bbcf5f83ed0773acef528e0c34b9cf20b9d1a46ca7c5681f9bd6395c0c9bb187
```

`verify_evidence.py` is read-only: it opens the lane for reading only and writes nothing there; its keccak-256 is imported
from the lane's own `tools/round-25/a2/resolve-selectors.py`, so the audit inherits the lane's hashing definition.

## Tooling

No tool was installed, upgraded or removed; everything needed (python3 3.14.8 stdlib, git read-only, coreutils) was
already present, so the host-wide pacman pause was untouched.

## Risks, limits, unknown

- A manifest sha256 proves the file on disk is the file hashed at fetch time; it cannot by itself prove the body
  was served by the remote API rather than hand-written. The independent REA replay (identical envelope bytes)
  and the live re-fetch by other wave seats are the external corroboration; this seat performed no network
  fetch, so provenance of the HTTP bodies rests on those peers.
- openchain bodies were checked for the presence of the requested selector key, not for the keccak of the
  returned names (third-party text; the resolver's own `keccak-mismatch` label covers it and the committed tally
  reports 0 such rows).
- Because no 4byte response had a `next` link, no page ≥ 1 file exists; the URL rule for pages > 0 was implemented
  but exercised by zero files, so that branch is untested by this evidence set (inference, not an observed
  failure). The lane's Git index and jj state were not touched; the lane was only read.

Report: `.ufo/waves/round-25/a3/w1/EvidenceIntegrity.md`
