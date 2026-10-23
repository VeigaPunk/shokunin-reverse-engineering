# RevCarrierProvenance — do the 16 frozen carriers match official PyPI provenance?

Seat: `KaidokuR30.RevCarrierProvenance` (reviewer). Round 30 wave 1. All work
under `/fast/scratch/hyaku/kaidoku-r30/seats/w1/RevCarrierProvenance/`.
Timestamps UTC 2026-10-23T02:42:05Z–02:42:50Z. No carrier or mutant was executed
(bytes read only); no lane file was modified.

## Method

1. Read `corpus/evidence/round-30/c1/carriers.tsv` (16 rows, 7 wheels) and the
   committed `corpus/evidence/round-30/c1/pypi-uv-0.13.0.json`.
2. Fetched `https://pypi.org/pypi/uv/0.13.0/json` fresh via `curl` (HTTP 200,
   29 777 bytes) at 2026-10-23T02:42:05Z into the seat dir.
3. Compared the two JSON documents byte-for-byte (`cmp`) and per-wheel via the
   served `urls[].digests.sha256` fields.
4. Downloaded the 7 wheels named in the TSV from the `urls[].url` links in the
   fresh JSON (`xargs -P7 curl -sSO`), verified each file's sha256.
5. Extracted the TSV-named member from each wheel with Python `zipfile`
   (CRC-checked `z.read`), sha256'd it, compared with the TSV `sha256`/`size`
   columns and with the staged file `/fast/scratch/hyaku/kaidoku-r30/carriers/<id>`.
6. Checked the 16 extracted members for duplicate bytes (hash multiset).

## PyPI JSON diff result (observation)

- `sha256(committed pypi-uv-0.13.0.json)` = `2eaed6c87b935f909946768885051f65341552f6d94e4fc23612a6d72e284b4c`
- `sha256(fresh fetch 2026-10-23T02:42:05Z)` = `2eaed6c87b935f909946768885051f65341552f6d94e4fc23612a6d72e284b4c`
- `cmp` exit 0 → **byte-identical; zero diff.** The served document reports
  `info.version = 0.13.0`, `urls` = 19 files (the TSV uses 7 of them).
- Located quote from the served bytes (one-line JSON), the manylinux x86_64
  wheel's digest object:
  `"digests":{"blake2b_256":"c3751901383808ba0d421f32060ba0e9884169b685a722e1af5d87fdd4225ba6","md5":"043b663343ea39e31bafcb9e5dda8f38","sha256":"52c7da0fd9056d9551124777ec77de53f0df7017daf8f98a19e947b7837416ed"}`
- Source record: URL `https://pypi.org/pypi/uv/0.13.0/json`, accessed
  2026-10-23, sha256 of served bytes `2eaed6c8…b4c` (above). The wheel bytes
  themselves were fetched from the `urls[].url` values in that document
  (files.pythonhosted.org links), accessed 2026-10-23T02:42:21Z; per-wheel
  sha256 below.

## Wheel verification (observation)

All 7 downloaded wheels' sha256 match both the fresh-PyPI `digests.sha256` and
the TSV `wheel_sha256` column:

| wheel | sha256 (first 12) | PyPI digest match | TSV match |
|---|---|---|---|
| manylinux_2_17_x86_64 | `52c7da0fd905` | OK | OK |
| manylinux_2_28_aarch64 | `f840e640fe16` | OK | OK |
| manylinux_2_31_riscv64 | `78187f23c0b5` | OK | OK |
| win_amd64 | `0367b4e0ae4d` | OK | OK |
| win_arm64 | `286d5976bffe` | OK | OK |
| macosx_10_12_x86_64 | `93265932cb2e` | OK | OK |
| macosx_11_0_arm64 | `a5f93ae362b7` | OK | OK |

## 16-row carrier table (observation)

"wheel sha ok" = downloaded wheel bytes sha256 == PyPI digest == TSV
`wheel_sha256`; "member sha ok" = extracted member sha256 == TSV `sha256`
(and member byte length == TSV `size`, checked and OK on all rows);
"file sha ok" = `sha256(/fast/scratch/hyaku/kaidoku-r30/carriers/<id>)` ==
TSV `sha256` == extracted member sha256.

| id | wheel sha ok | member sha ok | file sha ok |
|---|---|---|---|
| elf-x86_64-uv | yes | yes | yes |
| elf-x86_64-uvx | yes | yes | yes |
| elf-aarch64-uv | yes | yes | yes |
| elf-aarch64-uvx | yes | yes | yes |
| elf-riscv64-uv | yes | yes | yes |
| elf-riscv64-uvx | yes | yes | yes |
| pe-x86_64-uv | yes | yes | yes |
| pe-x86_64-uvx | yes | yes | yes |
| pe-x86_64-uvw | yes | yes | yes |
| pe-arm64-uv | yes | yes | yes |
| pe-arm64-uvx | yes | yes | yes |
| pe-arm64-uvw | yes | yes | yes |
| macho-x86_64-uv | yes | yes | yes |
| macho-x86_64-uvx | yes | yes | yes |
| macho-arm64-uv | yes | yes | yes |
| macho-arm64-uvx | yes | yes | yes |

## Duplicate carrier bytes (observation)

None. The 16 extracted members have 16 distinct sha256 values
(`Counter` over member hashes: all counts = 1). The two `uvx`/`uvw` "shim"
carriers are real per-arch binaries, not copies — e.g. `pe-x86_64-uvx`
vs `pe-x86_64-uvw` are 347 440 vs 346 928 bytes with different hashes.

## Bonus observation (not in acceptance, sanity only)

`file` output on each staged carrier matches its TSV `format`/`arch` labels:
ELF aarch64/riscv64/x86-64, Mach-O arm64/x86_64, PE32+ ARM64/x86-64; `uvw`
files are the GUI-subsystem variants. Full `file` transcript captured in the
verification output; consistent with labels on all 16 rows.

## Evidence trail (commands)

- `curl -sS https://pypi.org/pypi/uv/0.13.0/json` → http=200, 29 777 bytes,
  exit 0, 2026-10-23T02:42:05Z.
- `cmp committed vs fresh` → no output, exit 0, `JSON_IDENTICAL`.
- `cut -f2 wheel-urls.txt | xargs -P7 -I{} curl -sSO {}` in `wheels/` → 7 files,
  exit 0, 2026-10-23T02:42:21Z.
- `sha256sum wheels/*.whl` → 7 hashes equal to TSV `wheel_sha256` (table above).
- Python `zipfile` extract + `hashlib.sha256` loop over 16 TSV rows → every row
  printed `member_sha:OK size:OK file_sha:OK`, exit 0, 2026-10-23T02:42:33Z.
- `Counter` over extracted member hashes → `duplicate member hashes: none`.

## Verdict

**Holds.** All 16 frozen carriers are byte-exact extractions of the named
members of the official uv 0.13.0 PyPI wheels, whose own bytes match the digests
currently served by PyPI; the committed PyPI JSON is byte-identical to what
PyPI serves today; no carrier bytes are duplicated. Provenance chain
PyPI digest → wheel file → zip member → staged carrier file is unbroken on
every row.

## Seat artifacts (/fast/scratch/hyaku/kaidoku-r30/seats/w1/RevCarrierProvenance/)

| path | sha256 |
|---|---|
| pypi-uv-0.13.0-fresh.json | 2eaed6c87b935f909946768885051f65341552f6d94e4fc23612a6d72e284b4c |
| wheel-urls.txt | 4d48925756e2b83fbee6a21eb91c171c9cbe8ca2a4c6219a249a5a8214b03220 |
| verify.py (reproduction script) | d5b6963d3b019c715fb12c31065022f4e85ef53e217c3606d82f14ba400a5c4a |
| artifact-hashes.txt (full list) | — (regenerable) |
| wheels/*.whl (7 files) | see wheel table — each equals its TSV `wheel_sha256` |
| members/<id> (16 files) | each equals its TSV `sha256` (and the staged carrier file) |

No tools installed (curl, python3, zipfile, hashlib, file already present —
no installs needed under the paused-pacman policy). No REA invocation (item is
provenance review, not REA). No git/jj writes; lane access read-only.
Report: .ufo/waves/round-30/w1/RevCarrierProvenance.md
