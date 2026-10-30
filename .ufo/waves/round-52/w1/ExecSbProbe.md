# ExecSbProbe — round 52 wave 1

Verdict: settled; drafted standalone probe at `.ufo/waves/round-52/w1/ExecSbProbe/sb-probe.py`.

- It follows the round-50 embedded summary layout (offsets/endianness/version/compression/marker) and emits the requested JSON fields, adding `bytes_used_le_file_size` as a separate safety check. Exit 0 requires LE `hsqs`, v4.0, compression 4, AVM marker, and bytes_used within file size; invalid format exits 1. `--allow-nonavm` exits 0 only with an explicit JSON waiver.
- Synthetic plain-tree `mksquashfs` xz image was accepted after fixture-only setting `mkfs_time=bytes_used`: exit 0, stdout SHA-256 `bc58094affd4398e41c02d9b9427dd2daf5b787f243e3408f463d85932b8b756`, UTC `2026-10-30T10:46:40Z`. Non-SquashFS fixture refused: exit 1, stdout SHA-256 `ab674ba798618359b4c55ab8000714138b19c941fe90f9cde8bf31d573d8d986`, same UTC. Exact commands and captured output are in `ExecSbProbe/fixture-receipt.json`.
- Fixture was a plain tree; no FIFO added. No network, REA run, package installation, or lane-tree edits performed. `sqfs-list.py --inspect` semantics were not independently exercised; summary fields were taken from c1-run.sh's embedded reader.

Risks/blockers: probe output's invalid magic is decoded with replacement semantics; malformed/truncated files are refused. `--allow-nonavm` is intentionally a control-only explicit waiver; caller must constrain its use.

Status: `.ufo/waves/round-52/w1/ExecSbProbe/status.json`. Checks not run: no full harness/build/test (parent owns integration verification).