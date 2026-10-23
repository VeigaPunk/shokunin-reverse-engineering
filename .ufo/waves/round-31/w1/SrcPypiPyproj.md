# Round 31 source row draft — S093

## Behavior and touched surfaces

Drafted the SOURCES registry row and source Gate records for PyPI's `pyproj` releases 3.4.1, 3.5.0, 3.6.1, 3.7.0 and 3.7.1. The lane's `corpus/SOURCES.md` was read only and was not edited; this report is the only lane file written. Downloaded snapshots are under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPypiPyproj/`.

Read-only contract/source surfaces: `/home/vgpnk/Projects/shokunin/CORPUS.md` (SOURCES contract), `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`, `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, and `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-31/c1/carriers.tsv`. The contract and census script permit `dataset`; the existing registry uses the same 11-column Markdown row shape.

## Draft SOURCES.md row

```markdown
| S093 | PyPI release records for pyproj 3.4.1, 3.5.0, 3.6.1, 3.7.0, and 3.7.1 — https://pypi.org/pypi/pyproj/3.4.1/json; https://pypi.org/pypi/pyproj/3.5.0/json; https://pypi.org/pypi/pyproj/3.6.1/json; https://pypi.org/pypi/pyproj/3.7.0/json; https://pypi.org/pypi/pyproj/3.7.1/json | dataset | A | Official filename and SHA-256 metadata for the five pyproj CPython 3.10 manylinux x86_64 wheel containers referenced by `corpus/evidence/round-31/c1/carriers.tsv`; not the extracted database bytes or REA behavior | PyPI JSON records fetched 2026-10-23; served JSON SHA-256: 3.4.1 `e2209485625e12441c5d5e8321cfcc0eff13780dc62937764699a1d4273756ca`, 3.5.0 `b652ced79ac8554f09b4f2544c05d0eaea8622e3d367009e89aa18fdab0d0e7c`, 3.6.1 `4eb7b680f90e15a34a0d55af0cddcb9f0730d1516b3831bfadb0e1c2b108d134`, 3.7.0 `b28551bf19cc04ccfe15e51bf404eadc7a296ba7c60dc714a5ed2b43a8a0e0f4`, 3.7.1 `2ad9561af74a4e9214333cc952909bbd3e64822d51c74cf4336c853ebdadb1b7`; `.urls[]` `filename` / `digests.sha256` (line 1): `pyproj-3.4.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` — `5a53acbde511a7a9e1873c7f93c68f35b8c3653467b77195fe18e847555dcb7a`; `pyproj-3.5.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` — `cd5e2b6aa255023c4acd0b977590f1f7cc801ba21b4d806fcf6dfac3474ebb83`; `pyproj-3.6.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` — `80fafd1f3eb421694857f254a9bdbacd1eb22fc6c24ca74b136679f376f97d35`; `pyproj-3.7.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` — `ee60895f60cbd1a9c903ab2bc22adea63004296a1c28b8775a11cf50905cf085`; `pyproj-3.7.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` — `1e47c4e93b88d99dd118875ee3ca0171932444cdc0b52d493371b5d98d0f30ee` | The official release records bind each named wheel archive to its declared SHA-256, supporting wheel-level carrier provenance; they do not verify the embedded `proj.db` bytes or REA behavior. | mined | 2026-10-23 | on-release | corpus/knowledge/2026-10-23-r31-sqlite-positive.md |
```

## Gate — opened PyPI records

Access date for each source: **2026-10-23**. Each document is one line. Quotes below are the exact wheel filename from line 1, under 25 words; the 3.7.1 quote is the requested manylinux x86_64 filename.

- URL `https://pypi.org/pypi/pyproj/3.4.1/json`; SHA-256 `e2209485625e12441c5d5e8321cfcc0eff13780dc62937764699a1d4273756ca`; 60,252 bytes; line 1 quote: `pyproj-3.4.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`.
- URL `https://pypi.org/pypi/pyproj/3.5.0/json`; SHA-256 `b652ced79ac8554f09b4f2544c05d0eaea8622e3d367009e89aa18fdab0d0e7c`; 60,655 bytes; line 1 quote: `pyproj-3.5.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`.
- URL `https://pypi.org/pypi/pyproj/3.6.1/json`; SHA-256 `4eb7b680f90e15a34a0d55af0cddcb9f0730d1516b3831bfadb0e1c2b108d134`; 56,089 bytes; line 1 quote: `pyproj-3.6.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`.
- URL `https://pypi.org/pypi/pyproj/3.7.0/json`; SHA-256 `b28551bf19cc04ccfe15e51bf404eadc7a296ba7c60dc714a5ed2b43a8a0e0f4`; 54,523 bytes; line 1 quote: `pyproj-3.7.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`.
- URL `https://pypi.org/pypi/pyproj/3.7.1/json`; SHA-256 `2ad9561af74a4e9214333cc952909bbd3e64822d51c74cf4336c853ebdadb1b7`; 61,822 bytes; line 1 quote: `pyproj-3.7.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl`.

### Fetch commands and outcomes

Each exact command below ran with exit code **0** and no reported output:

```text
timeout 300 curl -fsSL https://pypi.org/pypi/pyproj/3.4.1/json -o /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPypiPyproj/pyproj-3.4.1.json
timeout 300 curl -fsSL https://pypi.org/pypi/pyproj/3.5.0/json -o /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPypiPyproj/pyproj-3.5.0.json
timeout 300 curl -fsSL https://pypi.org/pypi/pyproj/3.6.1/json -o /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPypiPyproj/pyproj-3.6.1.json
timeout 300 curl -fsSL https://pypi.org/pypi/pyproj/3.7.0/json -o /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPypiPyproj/pyproj-3.7.0.json
timeout 300 curl -fsSL https://pypi.org/pypi/pyproj/3.7.1/json -o /fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPypiPyproj/pyproj-3.7.1.json
```

## Findings and provenance

- **Observation — downloaded snapshots equal the lane-pinned copies.** The producing command was:

  ```text
  timeout 30 bash -c 'for v in 3.4.1 3.5.0 3.6.1 3.7.0 3.7.1; do local=/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPypiPyproj/pyproj-$v.json; pinned=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-31/c1/pypi-pyproj-$v.json; printf "%s scratch=" "$v"; sha256sum "$local"; printf "%s scratch_bytes=" "$v"; wc -c < "$local"; printf "%s pinned=" "$v"; sha256sum "$pinned"; printf "%s pinned_bytes=" "$v"; wc -c < "$pinned"; if cmp -s "$local" "$pinned"; then printf "%s byte_identical=yes cmp_exit=0\\n" "$v"; else rc=$?; printf "%s byte_identical=no cmp_exit=%s\\n" "$v" "$rc"; fi; done'
  ```

  Overall command exit code: **0**. Exact output excerpt: `3.4.1 byte_identical=yes cmp_exit=0`; `3.5.0 byte_identical=yes cmp_exit=0`; `3.6.1 byte_identical=yes cmp_exit=0`; `3.7.0 byte_identical=yes cmp_exit=0`; `3.7.1 byte_identical=yes cmp_exit=0`. For each version the scratch and pinned SHA-256 and byte size are the corresponding Gate values above.
- **Observation — wheel archive digests match the frozen carrier list.** I read each release record's `.urls[]` entry selected by its exact CPython 3.10 manylinux x86_64 filename, reading `filename` and `digests.sha256`; the returned filename/digest pairs are reproduced in the draft row. Comparing those values with the five `container` / `container_sha256` cells in `corpus/evidence/round-31/c1/carriers.tsv` gives five exact matches: 3.4.1 `5a53acbde511a7a9e1873c7f93c68f35b8c3653467b77195fe18e847555dcb7a`; 3.5.0 `cd5e2b6aa255023c4acd0b977590f1f7cc801ba21b4d806fcf6dfac3474ebb83`; 3.6.1 `80fafd1f3eb421694857f254a9bdbacd1eb22fc6c24ca74b136679f376f97d35`; 3.7.0 `ee60895f60cbd1a9c903ab2bc22adea63004296a1c28b8775a11cf50905cf085`; 3.7.1 `1e47c4e93b88d99dd118875ee3ca0171932444cdc0b52d493371b5d98d0f30ee`. This is wheel-level identity only, not independent verification of extracted `proj.db` contents or analyzer behavior.
- **Observation — requested used-by target was absent when checked.** A read of `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r31-sqlite-positive.md` returned `Path ... not found`. The row is drafted with the user's exact requested status `mined` and used-by path, but the target's existence/citation remains an integration gate; do not treat it as verified from this report.

UTC timing: access date is observed as 2026-10-23. Individual curl start times were not captured. A subsequent line-count/timestamp command returned `2026-10-23T04:11:05Z`; all five downloaded JSON files reported one line. No exact fetch-time claim is made.

## Gates, limits, and out of scope

- Gate passed: all five curl requests exited 0; each downloaded JSON is byte-identical to its pinned evidence copy; all five metadata wheel SHA-256 values match `carriers.tsv`.
- Integration gate outstanding: verify the used-by knowledge entry exists and cites S093 before admitting this row as mined into the registry.
- No lane product files were edited; no REA or carrier analysis was run; immutable carriers were not touched; no packages/tools were installed; no tests, build, lint, or formatter were run.

## Artifacts

Downloaded source snapshots, with SHA-256 (and byte length):

- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPypiPyproj/pyproj-3.4.1.json` — `e2209485625e12441c5d5e8321cfcc0eff13780dc62937764699a1d4273756ca`, 60,252 bytes.
- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPypiPyproj/pyproj-3.5.0.json` — `b652ced79ac8554f09b4f2544c05d0eaea8622e3d367009e89aa18fdab0d0e7c`, 60,655 bytes.
- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPypiPyproj/pyproj-3.6.1.json` — `4eb7b680f90e15a34a0d55af0cddcb9f0730d1516b3831bfadb0e1c2b108d134`, 56,089 bytes.
- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPypiPyproj/pyproj-3.7.0.json` — `b28551bf19cc04ccfe15e51bf404eadc7a296ba7c60dc714a5ed2b43a8a0e0f4`, 54,523 bytes.
- `/fast/scratch/hyaku/kaidoku-r31/seats/w1/SrcPypiPyproj/pyproj-3.7.1.json` — `2ad9561af74a4e9214333cc952909bbd3e64822d51c74cf4336c853ebdadb1b7`, 61,822 bytes.

Report path: `.ufo/waves/round-31/w1/SrcPypiPyproj.md`.
