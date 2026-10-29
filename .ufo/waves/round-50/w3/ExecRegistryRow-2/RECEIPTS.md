# ExecRegistryRow-2 — receipt index

Every receipt carries the exact command, its exit code and the sha256 of its stdout.

| receipt | command | exit | stdout sha256 |
|---|---|---|---|
| `receipt-validate-peer-row.json` | `python3 -I -B validate-peer-row.py` (script sha256 `1eb1a2a2c25022d616ea69ab4bf2c1df060778c7ccca254b93a04cb95339e2f8`) | 0 | `2442343246c885c3eda75cc343b0d1012038aa7b86c1e5f8ba992b7f724687e0` |
| `receipt-drift-extension.json` | `python3 -I -B drift-extension.py` (script sha256 `2a92d1c4c3b38c6f51258545c02ea574df02ca49d453aa11e29c6a1921182a38`) | 0 | the file is the stdout of the run (5 JSONL cases + the JSON array) |
| `receipt-final-landing.json` | `python3 -I -B final-landing.py` (script sha256 `199438e226edb90cf0009aa27a768e61cf8ca23c1e1f65a8abcd896a4ca479fe`) | 0 | the file is the stdout of the run (2 JSONL cases + the JSON array) |
| `receipt-registry-couplings.json` | `python3 -I -B registry-couplings.py` (script sha256 `b7c1a5bbeb3f826fb2a95002100d83e14b4c3e2613bf46bff652e45ebf1361ef`) | 0 | the file is the stdout of the run |

Receipt-file digests (as copied into this seat directory):

| file | sha256 |
|---|---|
| `receipt-validate-peer-row.json` | `83e6a28fb90b7e57b8088ace8061cf5774717f6c6d12256708dbd6f89a457955` |
| `receipt-drift-extension.json` | `5bb1a1730e691d2af32fd217b58c97a202e1938d476d6ca1e5278dd2b54b6f81` |
| `receipt-final-landing.json` | `1d084587a88fea1be6b128704f146ad1277fdd0700dd73b9e1ed818d8fb280a0` |
| `receipt-registry-couplings.json` | `8cb1c4ded64b03e719c1c44592876cd2dddf183eb945a5bb1c93c30c824570f8` |
| `receipt-landed-row.json` | `python3 -I -B verify-landed-row.py` — re-reads the **landed** `SKILL.md` row and re-applies every frozen predicate to the landed bytes (13/13 PASS) | 0 | `9d7df95bc893c21e729e28738a6322d0b79d0a3a70e11e92150663fbf9dffe49` |

| `receipt-attribution.txt` | `efc060462c23d7f45d6919a09853f6117db27100670b4df3e5b32a29c6b52c3a` |
| `receipt-step-isolation.txt` | `d7a3a6e81317bcd8c1b26161b77cb21d3195d83437546691282e7a88771ea0d0` |
| `receipt-landed-row.json` | see the table above |

The last two are the provenance receipts for the stray-stub question:

| receipt | command | exit |
|---|---|---|
| `receipt-attribution.txt` | `python3 -I -B attribution.py` (script sha256 `1eb1a2a2…` for `validate-peer-row.py`; this script's own digest is in the seat dir) | 0 |
| `receipt-step-isolation.txt` | `python3 -I -B step-isolation.py` — replays `final-landing.py`'s eight subprocess steps one at a time, recording the lane file's (sha256, size, mtime) after each | 0 |


UTC times of the runs are inside each receipt (the fixture clone revs are recorded there, and
the git commit timestamps are in the clone history).

Environment: `TMPDIR=/fast/scratch/hyaku/kaidoku-r50/w3-ExecRegistryRow-2`; lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; base revision
`f890bbead20ca2c549487167f56876ae47f1e1a4`; C1/C2 freeze `435d41fd4ad9211d1579fc447936fb33d2b74467`.
