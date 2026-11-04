# ExecC3 — independent R72-C3 derivation

Axes: raw-byte fidelity, clause discrimination, receipt-reader differential. R72-C3 reproduced for the assigned seven shapes and two readers. No production instruments changed; no audit implementation imported by the independent cutter/derivation.

## Independent raw-witness facts

`ExecC3/independent-derivation.json` retains all 46 per-record key sets, canary-presence flags, lexical normalized HOME/TMPDIR containment flags, child classes, aggregate facts and comparisons with the unchanged genuine summary. Every record has exactly HOME, LANG, PATH, TMPDIR; canary absent; both directories contained under the declared original run root. Census: git=1, node=16, readelf=8, upx-pinned-copy=21. All seven aggregate comparisons match. SHA256: `77716010d1c64944b7786c2b5915d12158b344468aa022a97f7571832bc02dc8`.

## Own cutter and audit calls

`ExecC3/derive-c3.py` independently cuts each shape under the seat scratch, copies bytes into the retained directory, and invokes the CLI with `python3 -I -B`, explicit `--capsule`, and the genuine round-71 `--audit`. No built-in tamper battery or capsule_audit import is used. The digest shape appends one blank line; record-count drops the final record; key/canary/HOME/TMPDIR/child shapes change the first record only. HOME/TMPDIR use a sibling prefix (`<root>-outside`) to distinguish containment from naive string-prefix checking.

| Shape | rc | Named failures |
|---|---:|---|
| genuine | 0 | none |
| digest | 1 | log_sha256 |
| record count | 1 | log_sha256, records, children |
| extra key | 1 | log_sha256, keys |
| canary key | 1 | log_sha256, keys, canary |
| HOME escape | 1 | log_sha256, home_under_run |
| TMPDIR escape | 1 | log_sha256, tmpdir_under_run |
| child-class change | 1 | log_sha256, children |

All seven declared clauses were named. Exact commands, cwd, rc, stdout, stderr and parsed JSON: `ExecC3/audit-*.json`; compact matrix and shape hashes: `ExecC3/audit-results.json`. Retained capsule bytes: `genuine.jsonl`, `digest.jsonl`, `record-count.jsonl`, `extra-key.jsonl`, `canary-key.jsonl`, `home-escape.jsonl`, `tmpdir-escape.jsonl`, `child-class.jsonl`; unchanged summary: `genuine-summary.json`.

## Lying-receipt differential

Round-71 source: `.ufo/waves/round-71/w1/ExecC1/c1-route.json`; only `child_env_observed.log` is changed, pointing to the polluted retained capsule. Reader extracted with read-only `git show b827a8b5d54f2885ec9be7786389f356c59226ce:tools/round-71/packed-elf.py`; SHA256 `5cf95aaa0892c4e4f1b82edb60590b57e6667467ed607b15989bb867e7d8efe0`. Reader with that revision and commitment `20256a954f2613bef25019a6b8c260883cb5f852a624e3af7a5335005326822e` accepts: rc=0, met=true, failing=[]. Evidence: `ExecC3/reader-r71-supported-interface.json`, `receipt-r71-lying.json`, `round71-packed-elf.py`.

Interface caveat: the frozen round-71 reader does not support `--capsule`. The requested explicit-flag attempt is retained as `reader-r71-explicit-capsule.json` (rc=2, unrecognized argument), separately from its supported-interface acceptance. No compatibility shim or reader modification hides this limitation.

Round-72 source: `.ufo/waves/round-72/l1/pre/route-at-declaration.json`, with only the observed-log pointer changed to `r72-polluted.jsonl`. This polluted capsule is independently built from its own `env-at-declaration.jsonl`, adding the synthetic canary to the first record. Reader invoked with explicit `--capsule`, declaration revision and its own receipt commitment: rc=1, met=false; failures exactly `receipt_capsule: keys`, `receipt_capsule: canary`. Other reported clauses (child_env_observed, run_binding, run_nonce, run_root) remain true. Evidence: `ExecC3/reader-r72-explicit-capsule.json`, `receipt-r72-lying.json`, `r72-polluted.jsonl`.

## Bounds and limitations

All retained artifacts are under `.ufo/waves/round-72/w1/ExecC3/`; summary outcome `ExecC3/results.json`. The sole scratch directory `/fast/scratch/hyaku/kaidoku-r72/ExecC3` was removed by the driver's finally block before command return. Own UPX scratch copy matched the pinned SHA256 `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`; no packer execution was needed for reader experiments. No installs, git mutations, external-state changes, builds, linters, formatters or unrelated checks. LSP tools are not mounted; no supported symbol refactor was needed.

These observations establish capsule/summary consistency checks, not producer authentication or truth of a jointly forged raw witness and summary. Source scratch paths are provenance pointers and need not survive. Independent containment is lexical normalized-path containment, not a claim about historical symlink targets. The old reader's explicit-capsule interface requirement is impossible without changing the frozen instrument; its actual false-green acceptance is retained separately.

Self-assessment: accuracy 4 (bounded to recorded seven shapes, not authentication); completeness 4 (old explicit flag unsupported and documented); clarity 4 (full command evidence separated from matrix); actionability 4 (retained driver and raw bytes, scratch command paths are historical); conciseness 4 (report includes necessary interface caveat). Overall 4.0; no additional implementation change is warranted by this scoped experiment.
