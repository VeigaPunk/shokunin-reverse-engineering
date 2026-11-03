# Gate — S264 and S265 re-grounded (round 64, seat ScribeSources)

Access date for both sources: 2026-11-03. Fetches ran once each, into
`/fast/scratch/hyaku/kaidoku-r64/ScribeSources/` (scratch deleted after the seat); the bytes were hashed, not
retained. No release asset was downloaded. No file in the lane was edited.

## S264 — jsc2js README at the pinned commit

- URL: https://raw.githubusercontent.com/xqy2006/jsc2js/01fc264d22055865a460b322399a15d84b71f5aa/README.md
- Command: `curl -fsSL -o s264-README.md <URL>` — exit 0 (`-f` makes any 4xx/5xx exit 22, so the body is a 2xx).
- Fetch time: 2026-11-03T22:43:31Z (file mtime 2026-11-03 19:43:31 -0300).
- Bytes: 8996. sha256 `df85060f38fd9ba5a15df5c86b4fbc9aa988c4d6faab8d8aa8d8b91f9ffeade3`.
- Cross-check (same bytes at the pin, not just at the branch): the staged clone `/home/vgpnk/.local/share/kaidoku-jsc/jsc2js-src`
  has `rev-parse HEAD` = `01fc264d22055865a460b322399a15d84b71f5aa`, and
  `git -C <clone> show 01fc264d22055865a460b322399a15d84b71f5aa:README.md | sha256sum` returns the same
  `df85060f…eade3`; the working-tree copy `/home/vgpnk/.local/share/kaidoku-jsc/jsc2js-src/README.md` also hashes to it.
  So the network fetch, the committed blob at the pin and the staged copy are byte-identical.
- Located quote (English section; nearest heading `### 1. Get the matching d8`, line 128; quote on line 130).
  The exact fetched line 130 is:
  `Go to the Releases page and choose the V8 version that is **identical to** the one that produced your target `.jsc`. (Open an Issue if the version you need is missing.)`
  Quoted span: "Go to the Releases page and choose the V8 version that is identical to the one that produced your target `.jsc`."
  — 21 words; the two `**` bold markers around `identical to` are elided, every word is verbatim.
- Supporting lines in the same fetched bytes (not the quote): line 144 (the dump is "V8 Ignition bytecode disassembly"),
  line 139 (`./d8 -e "loadjsc('path/to/xxx.jsc')" > xxx.txt`), line 152 (`python view8.py --disassembled ../xxx.txt ../xxx.js`),
  line 157 ("this is a semantic approximation"), lines 175-176 (V8 5.1 lower bound), line 199 ("Always use a **matching** d8 build").
- Claim it teaches: the route is two host-side stages behind one version gate. The d8 build must carry the V8 version identical to
  the artifact producer's; stage 1 is a `loadjsc()` Ignition text dump; stage 2 is View8 reconstruction, described only as an
  approximation. It therefore grounds a per-cell `dump|view8|check` label as three documented stages and grounds the
  version-match requirement — it grounds nothing about a reconstruction being valid JavaScript, and nothing about any artifact.
- Decision: accept as S264, kind `docs`, tier A, status `mined`, opened 2026-11-03, recheck 90d. It is the lane-registry
  replacement (renumbered by document, the URL) for the shokuknow-staged `jsc-mapper-cli-contract` entry staged as S125.
- Limits: the README is bilingual; the quote is from the English section (lines 109-219). Line numbers are of the fetched 219-line
  bytes and would move if upstream edits the file. The README documents intent; the round's measured View8 output on the probe cell
  is 213 bytes of Ignition pseudo-code that `node --check` rejects, so the README's "approximate JavaScript" framing is the tool's
  claim of intent, not an observed output class — the row's scope excludes parseability for that reason.

## S265 — jsc2js releases page (the inventory)

- URL: https://github.com/xqy2006/jsc2js/releases
- Command: `curl -fsSL -o s265-releases.html <URL>` — exit 0. No asset URL was requested.
- Fetch time: 2026-11-03T22:43:32Z (file mtime 2026-11-03 19:43:32 -0300).
- Bytes: 328667. sha256 `4aeaed401d1cff230a2ba7e9031a53a591906e607965bb93345467f20a13654b`.
- Located quote (page h1 `Releases: xqy2006/jsc2js`, line 444; entry heading `15.6.75.25`, line 785; body on line 972):
  "Patched d8 for V8 15.6.75.25 (includes d8 + snapshot_blob.bin)." — 10 tokens counting the `+`.
- Structure read from the same bytes: the page title is `Releases · xqy2006/jsc2js · GitHub` (line 111); the list heading is
  `Release list` (line 480); the first page carries 10 unique `/releases/tag/` links (lines 488-614) and a
  `Next` link to `?page=2` (line 630), so the page alone does not state a total.
- Count: 10 unique tag links on the fetched page; API total 679 releases and 679 tags (commands and outputs in `counts.txt`).
- Independent corroboration already in the lane (read, not re-run by this seat): `corpus/knowledge/jsc-mapper-release-inventory.md`
  derives 679 distinct tags from seven `releases?per_page=100&page=N` responses, and records the staged entry's earlier 677 as stale.
  The `per_page=1` Link `rel="last"` derivation in `counts.txt` agrees at 679.
- Claim it teaches: build selection is by exact V8 version tag. Each release is the patched d8 for one V8 version string plus
  `snapshot_blob.bin`; the latest is `15.6.75.25`; and the three builds R64-C1 pins (`14.8.178.14`, `14.8.178.1`, `14.7.173`) are
  each present as a release tag with `d8-<version>-linux.tar.gz` and `d8-<version>-windows.zip` assets, all published 2026-08-11.
- Decision: accept as S265, kind `docs`, tier A, status `mined`, opened 2026-11-03, recheck 90d. It is the lane-registry
  replacement (renumbered by document, the URL) for the shokuknow-staged entry staged as S129.
- Limits: the 10-tag count is page one only; 679 is the API pagination total, and the page markup (labels, "Latest" badge) can change
  without any release changing, so the row cites the API command for the count. No asset bytes were fetched, so no asset digest is
  re-grounded here; the round's d8 pins are the tool's own, and the plan's claim that they match the API `digest` fields was not
  re-run by this seat. The README's "369 tags" and "57 exact failed tags" (S264 lines 182-198) count upstream V8 source tags covered
  by the patch, not jsc2js releases — they must not be read as a release count. The API `digest` fields are per-asset archive digests
  (e.g. `d8-14.8.178.14-linux.tar.gz` sha256 `9326e285…`), while the instrument's `PINS` are per-file digests (d8, snapshot_blob.bin,
  icudtl.dat); the two sets are not directly comparable, so no pin-vs-API digest match is claimed here.

## Cross-checks and findings (reported, nothing edited)

1. Registry path: the seat brief names `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/CORPUS.md` for the 11-column schema, but no
   such file exists in the lane; the header `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`
   is at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md:5`, whose last row before this seat was S263. The rows in
   `rows.md` follow that header and continue the numbering at S264/S265.
2. Frozen instrument citation: `tools/round-64/jsc-route-matrix.py` line 4 cites "S125 README, S129 release inventory". In the lane
   registry S125 is the AVM FRITZ!Box 6490 download directory and S129 is the binwalk v2 README, so the citation reads as a
   lane-registry reference to unrelated rows. `plans/round-64-claims.md` (`## Assimilation`) shows the ids are the shokuknow staging
   ids, re-pointed by document to S264/S265. The instrument is frozen; this is a wording finding for the round record, not an edit.
3. Instrument integrity (read-only check): `sha256sum tools/round-64/jsc-route-matrix.py` =
   `29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb`, equal to the pin in the seat brief.
4. No numeric release count appears anywhere in the frozen instrument text (`grep -n "679|369|57 "` on it returns nothing), so the
   inventory total reported here is the measured API total, 679, and is not attributed to the instrument.
