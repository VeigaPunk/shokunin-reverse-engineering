# SentSecrets — credential / vendor-URL inheritance scan (round 52, w1)

Seat `SentSecrets`. Read-only; nothing written outside
`.ufo/waves/round-52/w1/SentSecrets/` and this file. No REA run, no download, no git mutation.
Tooling: the lane's own calibrated scanner
`.ufo/waves/round-50/w3/SentReceipts/credscan.py` (read-only) + the fleet's
`scripts/sources-census.sh validate --file`. **No tool installed** (no pacman/`uv`/`npx`
transaction; the pacman guard was never engaged).

**Verdict: PASS on the credential question.** Zero credential material, zero `op://` refs, zero
`Set-Cookie` values, zero credentialed URLs across the round-51 inheritance surface and the merge
package. One carried L0 restated (unchanged, nothing re-appended). One non-credential defect was
found in a sibling's draft, reported, **fixed by the owning seat, and independently re-verified
here as closed**.

## The three assigned questions

1. **Round-51 wave tree + `l1/drafts/` (310 files) — credential material a port could copy into
   `tools/round-52/`?** **None.** 12-class scan: `live_hits 0`, `placeholder_hits 0`,
   `synthetic_fixture_hits 0`. All 447 credential-*word* hits are lexical or prose, tabulated with
   `file:line` in `receipts/r51-credential-words-by-line.tsv`; the eight port candidates carry 60
   hits, **0 flagged** (all `token` = the frontier-note/action-vocabulary lexeme). The `op://`
   hits are only the round-51 sentinel's own report *naming* the class; there is no vault ref.
   `Set-Cookie` appears only in the prohibition text and in the fetch driver's own header scrub
   (`grep -iE '^(content-type|content-length|last-modified|etag):'`, cookies dropped).
2. **Merge package `/home/vgpnk/Projects/shokuknow/merge/kaidoku/` (80 files) — credential material
   or `op://` refs in the squashfs/AVM-adjacent staged entries?** **None.** `credscan` over the
   whole package and over the 11 AVM/squashfs entries: `live_hits 0` both. `grep 'op://'` → exit 1
   (0 hits); `Set-Cookie` → 0; `PRIVATE KEY` → 0; URL userinfo → 0; base64/hex blob ≥300/200 chars
   → 0. **CORPUS rule 6 (`CORPUS.md:129`) holds.** The 22 credential-word hits are all prose or
   citations: the adb AUTH handshake described by upstream AOSP (mechanism, no key bytes), the
   product name "1Password" in a byte-count table, "session" in ordinary English.
3. **The four vendor URLs in `carriers.json` — credentials embedded?** **No.** All four are
   `https://download.avm.de/…` with **no userinfo, no query string, no fragment, no port**
   (`urlsplit`-parsed). The `http_etag`/`http_last_modified` notes are response metadata, not
   cookies. Across every `carriers.json` in the lane: 0 credentialed URLs.

## Findings the L1 should act on

* **F1 (CLOSED — non-credential; found, reported, fixed by the owning seat, re-verified here).** The
  sibling's `ScribeMergeAdopt` rows S253–S260 initially failed `sources-census.sh validate` with
  **8 × `E09`** ("invalid recheck"): the recheck cell held prose (`180d — recheck run 2026-10-30,
  exit 0, count 1 (command in the entry's recheck line and \`## Gate\`)`) and the rule is
  `recheck !~ /^[0-9]+d$/ && !symbolic(recheck)`. The owning seat applied the fix (bare cadence
  `180d` in the cell; run detail moved to the entry's `recheck:` header / `## Gate`). **Independently
  re-verified here on a fresh scratch mirror: exit 0, `ok` + 19 `W04`, 0 error codes.** The seat
  also surfaced a second placement rule I had measured independently: an **EOF append raises 8 ×
  `E12`** ("row outside Registry section") — the rows must go **after the last registry row**.
  **Two landing rules for the L1: (a) insert after the last registry row; (b) keep the `recheck`
  cell a bare cadence.** Both are recorded in the sibling's `plan.md` §5–§6. Credential re-scan of
  the sibling's 10 files after the fix: `live_hits 0`. Final re-gate against the seat's delivered
  `sources-rows.md` (sha256 prefix `beb6c67d703ab0da`): **exit 0, 0 error codes**; all 8 rows carry
  exactly 12 pipes, `recheck` = `180d`; and the two own-work rows' pinned campaign artefacts were
  digest-verified against the bytes on disk (`lead2-avm-le-genuine.tsv` 940 B
  `523637c885bb50c6…` ✓, `lead2-stale-build.tsv` 964 B `4c962bacd24af813…` ✓ — both cited files
  exist at `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work/`).
* **F2 (Medium, latent — applies to any *bulk* append from the merge package; not a round-52
  blocker).** The package's own 132 staged rows carry the same defect in stronger form: **44 ×
  `E01`** (a literal `\|` inside a cell — the validator's `gawk -F'|'` does **not** honour
  backslash escapes, proved by fixture), **88 × `E09`** (prose recheck in every row), **132 ×
  `E11`** (used-by names files that exist only in the package's knowledge tree). Measured
  remediation in scratch — normalise the recheck cell to a bare cadence, remove literal `|`
  characters, copy the knowledge entries in — the mirror validates with **0 `E`-codes on the merged
  range**. The package's own ids `S106–S237` collide with the lane's `S001–S251`; the document
  renumber map (S106→S252 … S237→S383) is in `receipts/merge-renumber-map.tsv` (`E03` = **0**
  after renumbering). **The round-52 adoption does not append those rows** — it lands 8
  re-grounded rows (S253–S260) written from pinned upstream documents, and those are clean (§F1).
  Keep the two normalisation rules on file for any later bulk append.
* **F3 (Low, carried L0, unchanged).** The open L0 "unredacted session cookies in pushed history"
  is still live in three blobs reachable from `origin/main` (`ba6b0d6e…` round-45 `f1.hdr`,
  `5f8478b4…` round-49 `tree.hdr`, `815e2951…` round-49 `top.hdr`; `_gh_sess` 348–364 chars,
  `_octo` 26–27, `logged_in` 2 ⇒ `no`, anonymous). The tip tree is clean (all redaction
  placeholders). This wave re-appends nothing; remediation needs operator-authorised rotation or a
  history rewrite, both out of a wave seat's remit.
* **F4 (Informational).** Two tracked lane-top-level strays, `kaidoku-r26/seats/EntryCorrection/final-report.md`
  and `kaidoku-r51/w1-MutGapRule/amended-law-battery.py` (misrooted wave artefacts). Credential-clean,
  but they belong under `.ufo/waves/`. Also: the merge package's staged rows cite the *other* lane's
  `lanes/kaidoku/roundN/work/…` paths, which do not exist here (this lane has no `lanes/`
  directory) — a citation-hygiene issue for any row adopted verbatim.

## Headline measurements

| measurement | value |
|---|---|
| credential-class hits, round-51 surface (310 files / 5 776 021 B) | **live 0**, placeholder 0, synthetic 0 |
| credential-class hits, merge package (80 files) | **live 0**, placeholder 0, synthetic 0 |
| credential-class hits, round-52 wave tree (280 files) | **live 0** |
| `op://` refs, merge package / round-51 surface | **0** / 0 (only the class name in prose) |
| credentialed URLs (userinfo) anywhere in the three surfaces | **0** |
| `carriers.json` URLs with userinfo / query / fragment | **0 / 0 / 0** |
| `sources-census.sh validate` on the lane registry (baseline) | **exit 0** (`ok` + 19 `W04`) |
| same, with the sibling's rows S253–S260 **before** the fix | exit 1 — 8 × `E09` |
| same, with the sibling's rows S253–S260 **after** the fix (re-verified here) | **exit 0** — `ok` + 19 `W04`, 0 error codes |
| same, with the sibling's rows appended at EOF | exit 1 — 8 × `E12` (the placement rule) |
| same, with the package's 132 rows added | exit 1 — 44 `E01`, 88 `E09`, 132 `E11` (0 after normalisation) |

Full receipts (argv, cwd, UTC, exit code, stdout/stderr sha256) for all 35 commands:
`.ufo/waves/round-52/w1/SentSecrets/receipts/receipts.json`. Scratch
`/fast/scratch/hyaku/kaidoku-r52/w1-SentSecrets` was removed after the receipts were copied in.

**Report:** `.ufo/waves/round-52/w1/SentSecrets/scan.md` (full scan, file:line tables, fixtures).
