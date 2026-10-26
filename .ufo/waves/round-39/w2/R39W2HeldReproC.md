# R39W2HeldReproC — provenance attack on the committed R39-C2 held-out envelopes H11–H15

**Verdict: CONFIRMED.** All five committed envelopes H11–H15 re-derive exactly from their committed
`carrier.sqsh` in the manifest's declared arm: features identical, labels identical to `manifest.json`,
`run.json` claims identical, zero non-volatile payload differences. One low-severity consistency
observation about the interpreter's `--print-table` (below) does **not** touch any C2 label.

## Table

| id | class | label (manifest) | fresh label | payload match |
|----|-------|------------------|-------------|---------------|
| H11 | dep-missing-le | dep-missing-le | dep-missing-le | YES (0 non-volatile diffs) |
| H12 | dep-missing-le | dep-missing-le | dep-missing-le | YES (0 non-volatile diffs) |
| H13 | avm-marker-be-dropped | avm-marker-be-dropped | avm-marker-be-dropped | YES (0 non-volatile diffs) |
| H14 | avm-marker-be-dropped | avm-marker-be-dropped | avm-marker-be-dropped | YES (0 non-volatile diffs) |
| H15 | body-extractor-failure | body-extractor-failure | body-extractor-failure | YES (0 non-volatile diffs) |

Committed envelopes also label identically before any re-run (`python3 -I -B sqfs-triage.py --skill SKILL.md <committed envelope.json>` → same label, exit 0), so committed label ≠ fresh label is not the
only agreement: the committed artefact itself carries the manifest label.

## Per-id register (committed vs fresh)

Features are the frozen interpreter's own `features()` surface (`H` chunk handlers, `G` gap kinds,
`D` gap dependencies, `BE` `-be` in the child sasquatch argv, `SR` `MaliciousSymlinkRemoved`,
`P` published file count).

| id | arm | H | G | D | BE | SR | P | extraction_failed | diag `__typename__` |
|----|-----|----|----|----|----|----|----|-------------------|---------------------|
| H11 | before | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | n/a (no sasquatch command recorded) | no | 0 | true | `ExtractorDependencyNotFoundReport` |
| H12 | before | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | n/a | no | 0 | true | `ExtractorDependencyNotFoundReport` |
| H13 | after | `squashfs_v4_be` | `extractor-failure` | none | **no** (`-be` absent) | no | 0 | true | `ExtractCommandFailedReport` |
| H14 | after | `squashfs_v4_be` | `extractor-failure` | none | **no** (`-be` absent) | no | 0 | true | `ExtractCommandFailedReport` |
| H15 | after | `squashfs_v4_be` | `extractor-failure` | none | **yes** (`-be` present) | no | 0 | true | `ExtractCommandFailedReport` |

Every cell above is byte-identical between the committed `envelope.json` and my fresh run; the only
differing leaves anywhere in the five envelopes are run ids (`provider_id`, `evidence_id`), absolute
paths (input/out dir, `raw_result.execution.args[]`, `report[].path`, `subject.local_path`,
`parameters.path`/`output_directory`), and H15's base64 `stderr` — which decodes to the same three lines
with only the `firmware.bin` directory differing:

```
Reading a different endian SQUASHFS filesystem on <tmp>/firmware.bin
read_id_table: failed to read id table block
FATAL ERROR: File system corruption detected
```

`MaliciousSymlinkRemoved` is absent (`SR=no`) in all five, committed and fresh — correct for these
classes (no symlink class among H11–H15).

## Evidence (exact commands, exit codes)

Scratch `S=/fast/scratch/hyaku/kaidoku-r39/R39W2HeldReproC` (removed at end; cited artefacts copied to
`.ufo/waves/round-39/w2/artifacts/R39W2HeldReproC/`). Carrier digests recomputed with `sha256sum` and
all five equal `manifest.json`:

```
665ecf26…821c  H11/carrier.sqsh    (manifest 665ecf26…c821c)
52a9359d…b16f  H12/carrier.sqsh
774bfcf6…7bed  H13/carrier.sqsh
63824907…f06a  H14/carrier.sqsh
a11f8fcf…ec7d  H15/carrier.sqsh
```

Re-runs, `cd "$S"` first (unblob writes `unblob.log` into cwd), fresh outdir each time:

```
# before arm (H11, H12) — $HOME/.local/bin stripped from the child PATH, unblob still absolute
env PATH=/run/user/1000/fnm_multishells/5071_1793027685454/bin:/usr/local/bin:/usr/bin:/bin \
  REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output H11/carrier.sqsh out-H11
# exit 0, 7771 B JSON; identical invocation for H12 (exit 0, 7770 B)

# after arm (H13, H14, H15) — default PATH
  REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output H13/carrier.sqsh out-H13
# exit 0; H13 8888 B, H14 8457 B, H15 8426 B
```

Each fresh `{"ok",data,meta}` had `data` extracted to `H<id>/fresh-envelope.json` and labelled:

```
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-39/sqfs-triage.py \
  --skill /home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md H11/fresh-envelope.json
```

All `run.json` fields reproduce from the fresh envelopes (`handlers`, `gap_kinds`, `diagnostics`,
`files=0`): MATCH=True for H11–H15. `home_bin_on_path:false` matches the before arm for H11/H12 and
`true` the after arm for H13–H15. Committed `envelope.json` equals `rea-full.json["data"]` for all five
(no hand-edited envelope separate from the recorded full output).

### Carrier honesty (the envelopes describe real files, not just real runs)

- On-disk magic: H11/H12 `68737173` (`hsqs`, LE-read version 4.0); H13/H14/H15 `73717368` (`sqsh`,
  BE-read version 4.0). Endianness in `tree.json` (`le` / `avm` / `be`) is consistent with the handler
  unblob chose.
- `sasquatch-v4be -be -d H13/ss H13/carrier.sqsh` → exit 0, **7 files**, path set and sha256 equal to
  `H13/tree.json` oracle. H14 → exit 0, **4 files**, digests equal. So the `avm-marker-be-dropped`
  carriers are valid images whose only defect is the dropped `-be`; the class name is honest.
- H15 with `-be` **also fails** (`read_id_table` / corruption, exit 1, 0 files): its body is genuinely
  corrupt, so `body-extractor-failure` is not a mislabelled marker drop. This is the discriminator that
  separates rule 4 from rule 5.
- Cross-arm control: H11 in the **after** arm publishes **6 files** and the same interpreter calls it
  `clean`, with all six sha256 equal to `H11/tree.json` oracle. So `dep-missing-le` is caused by the arm,
  not by the carrier — the frozen table really discriminates on `BE`/`SR`/`P`, and the before-arm label
  is not an artefact of a broken image.

### Frozen-input provenance

- `heldout-gen.py` sha256 at freeze `8fcda41`, at `6fdaf4f1` and at HEAD is
  `8b3eddf8225cfb1092726f2cabd78040f5ad765c5b4248c690a2d5bfad3cf5fc` = `manifest.generator.sha256`.
- `sqfs-triage.py` is untouched since the freeze commit:
  `ef4a8a8b7428cf7221dd3aa16bc587507d308b1eacf01074def276e744beacf2` at both `8fcda41` and HEAD.
- `SKILL.md` triage block: sha256 of `SKILL.md` at `6fdaf4f1` equals at `8fcda41`
  (`29372524…890d`), and the parsed table at HEAD differs from the freeze table in **no** predicate and
  **no** prose cell (all 8 rules identical after the later `52b0eb29`/`e40a25df` skill edits). Marker
  `<!-- sqfs-triage-table v1 -->` at line 333, table at 334, 8 rules.

## Observation (not a falsification of C2): `--print-table` prints a different table than `SKILL.md`

`tools/round-39/sqfs-triage.py` documents `--print-table` as "print the frozen table block" and its
selftest only asserts `stdout == TABLE_BLOCK`; it never asserts `TABLE_BLOCK` equals the SKILL.md table
that `parse_skill()` actually classifies with. They diverge, and the divergence is behavioural:

| rule | predicate difference (TABLE_BLOCK vs SKILL.md) | consequence |
|------|-----------------------------------------------|-------------|
| 2 dep-missing-be | `files` `0` vs `*` | narrower fixture version |
| 3 dep-missing-le | `files` `0` vs `*` | narrower fixture version |
| 6/7/8 escaping-symlink-removed, in-tree-symlink-metadata, clean | handler `squashfs_v4_be` vs `squashfs_v4_*` | rules 6–8 stop matching LE carriers |

Demonstrated on the committed held-out set: with a skill file built from `TABLE_BLOCK`, H03/H04 label
`unclassified`; with `SKILL.md` they label `clean`. H11/H13 label the same under both. So an auditor
reading the printed table gets a rule set that would miss every LE clean carrier.

Impact on the C2 claim: none. `tools/round-39/c2-counter.py` line 28 pins `SKILL = "SKILL.md"`; the
20/20 score at `6fdaf4f1` is produced by the SKILL.md table, which is the frozen authority. The defect is
confined to the auditor-facing `--print-table` surface (`TABLE_BLOCK` looks like a stale wave-1 fixture
promoted to "the frozen block").

## Limits

- Seat scope was H11–H15 only; H01–H10 and H16–H20 were not re-run here.
- `TMPDIR` was not exported into the REA child, so four of five runs placed the REA scratch dir under
  `/tmp` (`/tmp/rea-firmware-*`, each well under 50 MB, removed by REA on exit — `ls -d /tmp/rea-firmware-*`
  empty afterwards). The paths only affect the volatile fields listed above.
- REA ran from the npx cache (`rea-agents 6.5.0`, root
  `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`); no network reinstall observed.
- Environment: `unblob 26.6.4` (`~/.local/bin/unblob`, `REA_UNBLOB_COMMAND` absolute in both arms),
  `sasquatch` / `sasquatch-v4be` reporting `unsquashfs version 4.5.1 (2022/03/17)`, Python 3.14.8.
- No tools installed or upgraded this seat (existing binaries and the cached npx package sufficed), so
  nothing to record under the tooling directive.
- No VCS mutation; only `git show`, `git log`, `git status --porcelain`, `git cat-file` were used.
- All five fresh envelopes come from the same unchanged interpreter and SKILL.md at HEAD; the frozen
  `sqfs-triage.py` digest confirms this is the freeze instrument.

## Artefacts

`.ufo/waves/round-39/w2/artifacts/R39W2HeldReproC/`

- `comparison.json` — per-id class/manifest label/committed label/fresh label/features/run.json match.
- `H11-fresh-envelope.json` … `H15-fresh-envelope.json` — the five re-derived data objects.
- `leaf-diff.txt` — every differing leaf, classified; non-volatile count 0 for all five.
- `oracle-check.txt` — carrier honesty: endianness magic, sasquatch `-be` oracle reproductions, H15
  corruption, H11 after-arm `clean` control.
- `printtable-divergence.txt` — the `--print-table` observation with the behavioural demonstration.
