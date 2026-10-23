# Round 31 W1 source evidence — S095

## Behavior

Prepared the requested S095 `corpus/SOURCES.md` row as a draft only. No source catalog, knowledge entry, carrier, tool, or other lane file was edited. The only lane write by this seat is this report. PyPI's release JSON and linked source distribution were downloaded by `curl` into the seat scratch directory; five fixture members were extracted there and hashed against the frozen carrier manifest. No REA command was run and no tool was installed.

## Gate

- **URL:** https://pypi.org/pypi/pyogrio/0.11.1/json
- **Access date:** 2026-10-23
- **Served JSON:** SHA-256 `5b286ab2a9c4bf86b7ca46fb0a17e4b92669b76f98c9b5acece09fe776707162`; 32,351 bytes.
- **Located quote, raw JSON line 1:** `"filename":"pyogrio-0.11.1.tar.gz"` (quote is under 25 contiguous words; the JSON is one physical line).
- **Named sdist:** `https://files.pythonhosted.org/packages/bf/1d/ae0340237207664e2da1b77f2cdbcb5f81fd0fc9f3200a48ca993a5e12ef/pyogrio-0.11.1.tar.gz`; PyPI JSON reports size `287267` and SHA-256 `e1441dc9c866f10d8e6ae7ea9249a10c1f57ea921b1f19a5b0977ab91ef8082c`.

## Findings

- **[OBSERVATION] Metadata and curl gates passed.** The exact JSON curl command was `timeout 300 curl -fsSL https://pypi.org/pypi/pyogrio/0.11.1/json -o /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPyogrio/pyogrio-0.11.1.json`; its recorded stdout was `exit=0`. The saved JSON file mtime was `2026-10-23T04:09:55.009666189Z` (UTC), size 32,351 bytes. From the fetched JSON `.urls[]` record for `pyogrio-0.11.1.tar.gz`, the observed fields were the filename, the sdist URL above, size `287267`, and sha256 `e1441dc9c866f10d8e6ae7ea9249a10c1f57ea921b1f19a5b0977ab91ef8082c`. The filename quote is located on JSON line 1.
- **[OBSERVATION] Downloaded archive matches its published digest and the carrier manifest.** Exact curl command: `timeout 300 curl -fsSL https://files.pythonhosted.org/packages/bf/1d/ae0340237207664e2da1b77f2cdbcb5f81fd0fc9f3200a48ca993a5e12ef/pyogrio-0.11.1.tar.gz -o /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPyogrio/pyogrio-0.11.1.tar.gz`; recorded stdout `exit=0`. Saved archive mtime `2026-10-23T04:10:03.323661125Z` (UTC), size 287,267 bytes. `sha256sum` output was `e1441dc9c866f10d8e6ae7ea9249a10c1f57ea921b1f19a5b0977ab91ef8082c` for the archive, equal to the digest in the JSON and to each of the five `container_sha256` cells for `gpkg-*` rows 9–13 of `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-31/c1/carriers.tsv`.
- **[OBSERVATION] All five archived fixtures match their pinned carrier bytes.** Extraction command (exit `0`): `timeout 300 sh -c 'mkdir -p /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPyogrio/extracted && tar -xzf /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPyogrio/pyogrio-0.11.1.tar.gz -C /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPyogrio/extracted pyogrio-0.11.1/pyogrio/tests/fixtures/curve.gpkg pyogrio-0.11.1/pyogrio/tests/fixtures/curvepolygon.gpkg pyogrio-0.11.1/pyogrio/tests/fixtures/line_zm.gpkg pyogrio-0.11.1/pyogrio/tests/fixtures/multisurface.gpkg pyogrio-0.11.1/pyogrio/tests/fixtures/test_gpkg_nulls.gpkg'`. `sha256sum` output (each equals its manifest `sha256` cell):

  | Carrier | Sdist member | SHA-256 |
  |---|---|---|
  | `gpkg-curve` | `curve.gpkg` | `03a9c5904fd3075c61ba96e5bf0aac381721d43799db23c06634a0c56e04f302` |
  | `gpkg-curvepolygon` | `curvepolygon.gpkg` | `00a1309ab0f29f97a4c5f6cb9cd3bde27143fc936712d5101767f60f0c96bac7` |
  | `gpkg-line-zm` | `line_zm.gpkg` | `9563e513b064476ee7ab8c66858f3f434307ca554f7495652d09674d2747c70c` |
  | `gpkg-multisurface` | `multisurface.gpkg` | `898a238bc119f051622c22de973899f501466a33a6a6c0cc405122802c6d648d` |
  | `gpkg-test-gpkg-nulls` | `test_gpkg_nulls.gpkg` | `4281d3c55f2042e2174ab9a13c5c5a06d13841071c1aa3ea2cc131afaf71e1d8` |

  The manifest records 98,304 bytes for each carrier; `stat` on each extracted member also returned 98,304 bytes. The hash command completed successfully with all five hashes printed (exit 0).
- **[INFERENCE]** The published release record plus matching archive digest and fixture hashes supports provenance of the five R31-C1 fixture inputs to this official sdist. It does not establish Pyogrio runtime behavior, fixture semantics, or any REA outcome.
- **[OBSERVATION / LIMIT]** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r31-sqlite-positive.md` was not found on two direct reads (the later check completed by 2026-10-23T04:11:30Z). The requested draft carries `status=mined` and that used-by path, but the row must not be appended as mined until that knowledge entry exists, per the SOURCES contract.
- **[UNKNOWN]** The shell tool did not expose UTC start times for the extraction/hash calls. Their output and exit status are recorded above; the latest terminal clock sample during artifact timestamp recording was `2026-10-23T04:13:19Z`. The downloaded files' exact UTC mtimes are recorded above. No unsupported execution timestamp is inferred.

## Draft SOURCES.md row

Exact proposed row (status and used-by as assigned):

```markdown
| S095 | PyPI release record for pyogrio 0.11.1 — https://pypi.org/pypi/pyogrio/0.11.1/json (sdist https://files.pythonhosted.org/packages/bf/1d/ae0340237207664e2da1b77f2cdbcb5f81fd0fc9f3200a48ca993a5e12ef/pyogrio-0.11.1.tar.gz) | dataset | A | The official source-distribution identity and five GeoPackage fixtures used as R31-C1 inputs; not Pyogrio runtime behavior or REA outcomes | Served JSON SHA-256 `5b286ab2a9c4bf86b7ca46fb0a17e4b92669b76f98c9b5acece09fe776707162` (32,351 bytes); `.urls[]` filename `pyogrio-0.11.1.tar.gz`, size `287267`, SHA-256 `e1441dc9c866f10d8e6ae7ea9249a10c1f57ea921b1f19a5b0977ab91ef8082c` (line 1); downloaded sdist SHA-256 `e1441dc9c866f10d8e6ae7ea9249a10c1f57ea921b1f19a5b0977ab91ef8082c` (287,267 bytes), equal to all five `gpkg-*` `container_sha256` cells in `corpus/evidence/round-31/c1/carriers.tsv`; the five members `pyogrio-0.11.1/pyogrio/tests/fixtures/{curve.gpkg,curvepolygon.gpkg,line_zm.gpkg,multisurface.gpkg,test_gpkg_nulls.gpkg}` hash to their respective carrier `sha256` cells (carriers.tsv:9-13) | The PyPI record and matching archive digest establish that R31-C1's five pinned GeoPackage fixtures are members of the official pyogrio 0.11.1 sdist; they do not establish REA reader semantics or success. | mined | 2026-10-23 | on-release | corpus/knowledge/2026-10-23-r31-sqlite-positive.md |
```

## Touched surfaces and artifacts

- **Lane surface:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-31/w1/SrcPyogrio.md` only. `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md` was read but not modified.
- **Scratch root:** `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPyogrio/`. SHA-256 for each file artifact:
  - `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPyogrio/pyogrio-0.11.1.json` — `5b286ab2a9c4bf86b7ca46fb0a17e4b92669b76f98c9b5acece09fe776707162`
  - `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPyogrio/pyogrio-0.11.1.tar.gz` — `e1441dc9c866f10d8e6ae7ea9249a10c1f57ea921b1f19a5b0977ab91ef8082c`
  - `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPyogrio/extracted/pyogrio-0.11.1/pyogrio/tests/fixtures/curve.gpkg` — `03a9c5904fd3075c61ba96e5bf0aac381721d43799db23c06634a0c56e04f302`
  - `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPyogrio/extracted/pyogrio-0.11.1/pyogrio/tests/fixtures/curvepolygon.gpkg` — `00a1309ab0f29f97a4c5f6cb9cd3bde27143fc936712d5101767f60f0c96bac7`
  - `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPyogrio/extracted/pyogrio-0.11.1/pyogrio/tests/fixtures/line_zm.gpkg` — `9563e513b064476ee7ab8c66858f3f434307ca554f7495652d09674d2747c70c`
  - `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPyogrio/extracted/pyogrio-0.11.1/pyogrio/tests/fixtures/multisurface.gpkg` — `898a238bc119f051622c22de973899f501466a33a6a6c0cc405122802c6d648d`
  - `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPyogrio/extracted/pyogrio-0.11.1/pyogrio/tests/fixtures/test_gpkg_nulls.gpkg` — `4281d3c55f2042e2174ab9a13c5c5a06d13841071c1aa3ea2cc131afaf71e1d8`
  - `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPyogrio/S095-row.md` — `9fd2db502ef2947ef5cc53d30fb96fcfc9521f8c1ba7eb2c9e12a0b354b896d8`

## Out of scope

No edit to the lane's SOURCES registry, no REA run on any carrier or mutant, no tests/builds, no package/tool installation, no Git/jj mutation, and no assertion that the round's behavioral target passed. The source distribution and its members were read/extracted only in the seat scratch directory.

Report: .ufo/waves/round-31/w1/SrcPyogrio.md
