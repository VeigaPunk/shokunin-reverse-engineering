# Verdict: the C1 miss survives

The frozen score remains a valid **2/4, exit 1** miss: both `g7581` and `g7582` have 12 required char-device entries with no matching gap or removal; their only silent-admitted char device is `dev/led` (`247:0`). The C-pair each has only that one char-device, so both pass this disposition rule. I did not run REA or the C1 counter predicate.

## Findings and impacted axes

| Axis | Finding |
|---|---|
| Coverage | Re-derived oracle char-device counts are `g7581=13`, `g7582=13`, `c6490=1`, `c6430=1`; details match the expected major/minor census. Exact char-path matching finds 12 missing dispositions on each G carrier, not a counter false positive. |
| Depth | The broad `dev/`-is-zero expectation is false as written: `g7581` has gap paths `firmware.bin_extract/dev/kdsld_misc` and `.../dev/new_led` (oracle kind `symlink`), plus one `MaliciousSymlinkRemoved` for `dev/log` (also an oracle symlink). None is a char-device path, so none disposes `dev/pts/*`, `dev/tiatm`, or `dev/ttyp*`. The claim is valid only when scoped to the char-device oracle paths. |
| Calibration | The rerun assertion is false for the pair: `g7582.projection_ok=true`, but `g7581.projection_ok=false`; its rerun failed with `ENOENT` on `.../usr/www.myfritz/avme/cgi-bin/luacgi`, so its projection was not compared. Do not claim paired rerun stability. |

### Hand-simulated rule outcome (`g7581`)

The frozen rule sets `required.char-device=true` and admits silent char-device detail `247:0` only. `disposition_check` indexes nonregular entries by exact relative path, resolves gap/removal dispositions, then admits an otherwise-undisposed required entry only if its detail is on that silent list (`c1-counter.py:1458-1564`). Thus `dev/led` is the single silent-admitted row. The other 12 rows have neither exact-path gaps nor exact-path removals, and their details are not `247:0`; the check must fail. The `dev/log` removal cannot match those rows and is a symlink, while the frozen `removed.kinds` contains only `symlink`.

### Projection qualification

The selected profile is `plus-extractor`; the projection explicitly includes normalized `extraction_gaps` (`c1-counter.py:1830-1872, 1890-1900`) and `projection_diff` compares every profile key (`1903-1918`). `g7582` has `projection_ok=true` and `projection_diff=[]`, so its gap set was compared. `g7581` has `projection_ok=false`, `projection_diff=null`; the score receipt records REA `execution_failure`, exit 1, retryable false, caused by `ENOENT: ... readlink '.../usr/www.myfritz/avme/cgi-bin/luacgi'`. This is not a projection mismatch, but it is also not a passed projection check.

**Smallest safe correction:** retain the 2/4 miss and frozen rule; qualify broad `dev/` searches as char-device-path checks, disclose the unrelated symlink paths above, and amend the rerun statement to “g7582 passed; g7581 rerun failed, projection unverified.”

## Evidence table

The exact command string or full argv (including the structured `python3 -c` code) is preserved verbatim in `CritC1MissReal/checks.json` under each label. Matching stdout files are adjacent; hashes below are SHA-256 of the captured stdout bytes. Census and receipt-extraction commands were run at `2026-10-29T21:29:27Z`; later rows carry their own UTC time.

| Check / exact command | Result | Exit | stdout SHA-256 | UTC |
|---|---|---:|---|---|
| `awk -F'\t' '$2=="char-device"' tools/round-50/oracle/g7581.nonregular.tsv \| wc -l` | 13 | 0 | `1a252402972f6057fa53cc172b52b9ffca698e18311facd0f3b06ecaaef79e17` | 21:29:27Z |
| `awk -F'\t' '$2=="char-device"' tools/round-50/oracle/g7582.nonregular.tsv \| wc -l` | 13 | 0 | `1a252402972f6057fa53cc172b52b9ffca698e18311facd0f3b06ecaaef79e17` | 21:29:27Z |
| `awk -F'\t' '$2=="char-device"' tools/round-50/oracle/c6490.nonregular.tsv \| wc -l` | 1 | 0 | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` | 21:29:27Z |
| `awk -F'\t' '$2=="char-device"' tools/round-50/oracle/c6430.nonregular.tsv \| wc -l` | 1 | 0 | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` | 21:29:27Z |
| `awk -F'\t' '$2=="char-device"' tools/round-50/oracle/g7581.nonregular.tsv` | 13 rows, details attached | 0 | `333594a473b9e08d6a9166f8fe1e640ee8b2a951b9e463476497bc04991e3eb2` | 21:29:27Z |
| `awk -F'\t' '$2=="char-device"' tools/round-50/oracle/g7582.nonregular.tsv` | 13 rows, details attached | 0 | `333594a473b9e08d6a9166f8fe1e640ee8b2a951b9e463476497bc04991e3eb2` | 21:29:27Z |
| `awk -F'\t' '$2=="char-device"' tools/round-50/oracle/c6490.nonregular.tsv` | `dev/led char-device 247:0` | 0 | `eaff69ddcdcd2a1f1614c0a893fda13c761a402e0aee158dd6f7fcb0a7c63073` | 21:29:27Z |
| `awk -F'\t' '$2=="char-device"' tools/round-50/oracle/c6430.nonregular.tsv` | `dev/led char-device 247:0` | 0 | `eaff69ddcdcd2a1f1614c0a893fda13c761a402e0aee158dd6f7fcb0a7c63073` | 21:29:27Z |
| `checks.json` label `g7581-receipt-json` (exact argv attached) | 637 gaps; 12 missing char dispositions; 2 `dev/` symlink gaps; 1 removed `dev/log` symlink | 0 | `67efef4be050f7a2f1f748fb42f585bae7eb271dc62ef918c12882d0a2f52033` | 21:29:27Z |
| `checks.json` label `g7582-receipt-json` (exact argv attached) | 637 gaps; 12 missing char dispositions; 2 `dev/` symlink gaps; 1 removed `dev/log` symlink | 0 | `05bbac05704af60f03d934c5d26cdd2712934ec1b2eb99858adc8af495b93447` | 21:29:27Z |
| `checks.json` label `c6490-receipt-json` (exact argv attached) | 613 gaps; one silent-admitted char device | 0 | `3a4413d274539bda93e52389a1e81b8d97635f19547033752335e9e851459592` | 21:29:27Z |
| `checks.json` label `c6430-receipt-json` (exact argv attached) | 568 gaps; one silent-admitted char device | 0 | `a1e4d6bc3834a95292b7dd361a17ca82530b0ea38a3e06e47c20e03add96ef6b` | 21:29:27Z |
| `checks.json` label `counter-projection-state` (exact argv attached) | `g7581=false` (REA execution failure); `g7582=true`, diff `[]` | 0 | `aca0b154e4472f45d6ce00fd7d3edcb17d813eb67a14993fb13c3d7c21e2cb55` | 21:31:49Z |
| `checks.json` label `frozen-gap-rule-state` (exact argv attached) | Required char device; silent list exactly `247:0`; removed kinds `symlink` | 0 | `bf9eb60f207100ac058c8d16b52313042f95d927fe7f3c692325e8002c03b65b` | 21:31:50Z |
| `checks.json` label `g7581-dev-path-audit` (exact argv attached) | Gap paths `dev/kdsld_misc`, `dev/new_led`; removed path `dev/log` | 0 | `57cb33cce7be403e498905d18891b911234670288982358f2fb08ef61622d33e` | 21:33:09Z |

The complete 637-entry `g7581` gap-path list, including the one null/structural path, is `CritC1MissReal/g7581-gap-paths.tsv`. Per-carrier exact char-device rows and path-level dispositions are in `census-summary.json` and `disposition-summary.json`. The mounted `grep` search for `dev/` on the full g7581 JSON found `dev/log`; a separate search on the extracted gap-path list found the two symlink gaps above. No install/update, REA run, C1 predicate rerun, or lane source edit was performed.