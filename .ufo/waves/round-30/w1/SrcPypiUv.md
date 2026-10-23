# R30-C1 PyPI provenance — S091 draft

## Behavior and scope
Fetched the official PyPI release JSON for `uv` 0.13.0 and compared it with the retained lane copy. This is publication-provenance evidence only; it is not evidence of REA behavior or a live carrier/mutant run. The draft row below was not inserted into `corpus/SOURCES.md`.

## Draft SOURCES row

| S091 | PyPI release record for uv 0.13.0 — https://pypi.org/pypi/uv/0.13.0/json | registry | A | Official wheel filenames and sha256 digests for the seven wheels referenced by `corpus/evidence/round-30/c1/carriers.tsv`; used by R30-C1 and R30-C2. Does not establish wheel-member contents or REA behavior | Served JSON SHA256 `2eaed6c87b935f909946768885051f65341552f6d94e4fc23612a6d72e284b4c`; `.urls[]` filename / `digests.sha256` (line 1): `uv-0.13.0-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` — `52c7da0fd9056d9551124777ec77de53f0df7017daf8f98a19e947b7837416ed`; `uv-0.13.0-py3-none-manylinux_2_28_aarch64.whl` — `f840e640fe16591f6d71a94e8863707b7ba43c5786d1fe662868a9fb44c53e50`; `uv-0.13.0-py3-none-manylinux_2_31_riscv64.whl` — `78187f23c0b51d1be824096ec8a656c417acca312f5451ba1e2ee057ec5a6e87`; `uv-0.13.0-py3-none-win_amd64.whl` — `0367b4e0ae4dcef32da4aa2ad2f3853b6ad81d50c187abe50d343d892b8fea21`; `uv-0.13.0-py3-none-win_arm64.whl` — `286d5976bffe3ed0c62601c0393adb3748f0d88aa24f38cd80ebab773f5b5f74`; `uv-0.13.0-py3-none-macosx_10_12_x86_64.whl` — `93265932cb2efd1486d4d182211281b3f0b31637e2fc160c4c8d7b15294188d1`; `uv-0.13.0-py3-none-macosx_11_0_arm64.whl` — `a5f93ae362b751737cecef0bbc0294624be68a843ff9b32d86e6862a26101630` | The release record names the official wheel archives and their digests. Those are the wheel-level provenance values used by the carrier list; they do not independently establish carrier member hashes or analyzer outcomes. | mined | 2026-10-23 | on-release | R30-C1, R30-C2 |

## Gate note
Served JSON, line 1, SHA256 `2eaed6c87b935f909946768885051f65341552f6d94e4fc23612a6d72e284b4c`; located quote (one JSON string value, under 25 words/tokens): `"filename":"uv-0.13.0-py3-none-macosx_10_12_x86_64.whl"`. This supports the official filename provenance for the cited wheel; the row's digest mappings are scoped to the PyPI release metadata.

## Findings and evidence

- **Fetch:** command `timeout 120 curl --fail --silent --show-error --location https://pypi.org/pypi/uv/0.13.0/json --output /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcPypiUv/pypi-uv-0.13.0.json`; no stdout/stderr, exit 0. The fetched file mtime was `2026-10-22 23:42:28.714508984 -0300` = `2026-10-23T02:42:28.714508984Z` (UTC conversion from the displayed -0300 offset). Access date: 2026-10-23.
- **Whole-file hashes:** command `timeout 20 sha256sum /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcPypiUv/pypi-uv-0.13.0.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/pypi-uv-0.13.0.json`; exact stdout:
  ```
  2eaed6c87b935f909946768885051f65341552f6d94e4fc23612a6d72e284b4c  /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcPypiUv/pypi-uv-0.13.0.json
  2eaed6c87b935f909946768885051f65341552f6d94e4fc23612a6d72e284b4c  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/pypi-uv-0.13.0.json
  ```
  Exit 0. The exact UTC second of this command was not captured; it completed after the fetched file mtime and before the timestamped tuple-diff command below (2026-10-23T02:42:53Z). The matching hashes establish byte identity of the served and retained JSON.
- **Filename/digest diff:** command `timeout 120 bash -c 'date -u "+%Y-%m-%dT%H:%M:%SZ"; diff -u <(jq -r ".urls[] | [.filename,.digests.sha256] | @tsv" /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcPypiUv/pypi-uv-0.13.0.json | sort) <(jq -r ".urls[] | [.filename,.digests.sha256] | @tsv" /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/pypi-uv-0.13.0.json | sort); rc=$?; printf "DIFF_EXIT=%s\\n" "$rc"; exit "$rc"'`; exact stdout `2026-10-23T02:42:53Z\nDIFF_EXIT=0`; exit 0, with no diff hunks. The sorted complete `.urls[]` filename/sha256 tuples match.
- **Release tuple extraction:** command `timeout 30 jq -r '.urls[] | [.filename,.digests.sha256] | @tsv' /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcPypiUv/pypi-uv-0.13.0.json`; exit 0. Its output included all 19 release URL records; the seven listed in S091 match the seven unique wheel / `wheel_sha256` pairs in `carriers.tsv`. This extraction's exact UTC second was not captured.

## Gates and touched surfaces
The S091 row is a draft only; no R30 counter or REA command was run, no carrier or mutant was executed, and no frozen target line was evaluated. Read `corpus/evidence/round-30/c1/carriers.tsv` and the retained PyPI JSON; wrote only this scoped report in the lane. `corpus/SOURCES.md` and all other lane content remain unchanged. No tool was installed.

## Out of scope and limits
No wheel was downloaded or unpacked. The PyPI record supports published archive filename/digest provenance, not the contents of wheel members, member hashes, carrier execution, or `inspect_rust_binary` behavior.

## Artifact
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcPypiUv/pypi-uv-0.13.0.json` — SHA256 `2eaed6c87b935f909946768885051f65341552f6d94e4fc23612a6d72e284b4c`.

## Findings
- **Observation:** local frozen and fetched PyPI JSON have identical SHA256; producing command and full output above; exit 0; exact command time was not captured (completed before the timestamped `diff` at 2026-10-23T02:42:53Z).
- **Observation:** sorted complete `.urls[]` filename/sha256 tuple sets are identical; producing `diff` command and output above; exit 0; 2026-10-23T02:42:53Z.
- **Observation:** seven carrier wheel names and hashes in the draft are present in the served release's `.urls[]`; producing `jq` extraction and carrier TSV read; exit 0; the exact `jq` command time was not captured.
