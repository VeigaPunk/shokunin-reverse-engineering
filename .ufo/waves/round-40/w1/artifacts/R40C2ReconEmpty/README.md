# R40C2ReconEmpty artifacts — zero-regular-file SquashFS v4 outcomes (BE + LE)

All inputs are **development** carriers: six trees authored in scratch and built with
`tools/round-39/gen-squashfs.py`. No C1 carrier (V1/V2/L1/L2) and no C2 held-out carrier was
built or run here.

| path | what |
|---|---|
| `build.sh` | reproduces trees → carriers → 26 REA runs → feature table → v1 labels → v2 probe; `usage: ./build.sh WORKDIR` on an empty workdir (sets `TMPDIR`/`R40_WORK`; nothing goes to `/tmp`) |
| `trees.json` | the six tree shapes (`directories` / `regular_files` / `symlinks`) |
| `carriers/`, `carriers.sha256` | 23 dev carriers + digests (146–511 B each; `NOTSQFS-gzip.bin` is the no-chunk control) |
| `envelopes/` | 26 full REA `{ok,data,meta}` envelopes (`.full.json`, 13–17 KB each) + `.run.json` (exit code, argv, arm, duration) + `runs.json` |
| `features.json`, `features.tsv` | v1 feature vector plus `operation`, `provider.id`, `chunks[].extraction_failed`, `unpublished_entries[]`, `diagnostics[].report`, `derivations[]` |
| `v1-labels.tsv` | `tools/round-39/sqfs-triage.py` label + matched rule for each envelope |
| `probe-v2-labels.tsv` | the candidate v2 table applied by `probe-v2-rows.py` to the 26 real + 4 synthetic envelopes |
| `candidate-triage-v2.md` | CANDIDATE v2 table (12 columns, marker, actions line) — recon proposal, not the frozen SKILL.md block |
| `probe-v2-rows.py` | recon probe implementing the L1 v2 grammar (not the frozen interpreter) |
| `fixtures/` | malformed/control tables (`bad-dup-label.md`, `bad-cell.md`, `bad-action.md`, `nodomain.md`) and `fixtures/synthetic/` domain-guard envelopes |
| `oracle/` | `sqfs-list.py` per carrier: `.files.tsv`, `.symlinks.tsv`, `.inspect.json`, `.err` (T4 both fail `zero-length metadata block at 130`) |
| `logs/sqfs-list.txt`, `logs/direct-reads.txt` | independent-reader log and direct `sasquatch(-v4be)` reads with exit codes |

Everything here was produced on 2026-10-26 (scratch since removed). Tool versions: REA 6.5.0
(`npx`), unblob 26.6.4 (engine sha256 `0ce7b624…1d09`), sasquatch / sasquatch-v4be 4.5.1.
