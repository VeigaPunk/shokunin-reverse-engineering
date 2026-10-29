# Label distribution the v4 table produces today (the before-state evidence)

Measured by `sqfs-triage-v5.py --root <LANE> --rev f890bbead20ca2c549487167f56876ae47f1e1a4
--envelopes .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/` (126 envelopes).
The "v4 table" column is the table as SKILL.md carries it at the base revision; the
"v5 evaluator" column is the fixed R50-C3 precedence.  A row whose two counts differ
is a routing defect the v5 table fixes.

| label | v4 table today | v5 evaluator | difference |
| --- | --- | --- | --- |
| `clean` | 51 | 32 | -19 |
| `clean-unverified` | 0 | 19 | +19 |
| `container-depth-limited` | 3 | 3 | 0 |
| `dep-missing-be` | 2 | 2 | 0 |
| `dep-missing-le` | 8 | 8 | 0 |
| `depth-limited` | 48 | 48 | 0 |
| `in-tree-symlink-metadata` | 1 | 1 | 0 |
| `legacy-body-failure` | 7 | 7 | 0 |
| `partial-body-failure` | 2 | 2 | 0 |
| `unknown-residue` | 4 | 4 | 0 |

Totals: v4 table 126, v5 evaluator 126, envelopes 126.

**Pair mismatches at the base revision: 19 (exit 1).**

The no-reader `*_ddefault` rows among them (the round-49 F2 witness):

- `squashfs_v2_nonstandard_squashfs_v2.0_be_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`
- `squashfs_v2_nonstandard_squashfs_v2.0_le_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`
- `squashfs_v2_nonstandard_squashfs_v2.1_be_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`
- `squashfs_v2_nonstandard_squashfs_v2.1_le_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`
- `squashfs_v3_broadcom_squashfs_v3.be.1kpad_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`
- `squashfs_v3_broadcom_squashfs_v3.be.4kpad_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`
- `squashfs_v3_broadcom_squashfs_v3.be.nopad_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`
- `squashfs_v3_broadcom_squashfs_v3.le.1kpad_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`
- `squashfs_v3_broadcom_squashfs_v3.le.4kpad_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`
- `squashfs_v3_broadcom_squashfs_v3.le.nopad_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`
- `squashfs_v3_broadcom_squashfs_v3_le_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`
- `squashfs_v3_nonstandard_squashfs_v3.be.1kpad_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`
- `squashfs_v3_nonstandard_squashfs_v3.be.4kpad_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`
- `squashfs_v3_nonstandard_squashfs_v3.be.nopad_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`
- `squashfs_v3_nonstandard_squashfs_v3.le.1kpad_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`
- `squashfs_v3_nonstandard_squashfs_v3.le.4kpad_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`
- `squashfs_v3_nonstandard_squashfs_v3.le.nopad_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`
- `squashfs_v3_nonstandard_squashfs_v3_be_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`
- `squashfs_v3_nonstandard_squashfs_v3_le_ddefault`: table `clean`/`none` -> evaluator `clean-unverified`/`record-unverified`

All 19 mismatches are no-reader envelopes (v2ns / v3_broadcom / v3_nonstandard)
that the v4 `clean` row labels `clean`/`none`; every reader-backed family is unchanged,
which is what the claim requires.

## The v5 table, landed, on the same 126 envelopes

| label | v5 table | v5 evaluator |
| --- | --- | --- |
| `clean` | 32 | 32 |
| `clean-unverified` | 19 | 19 |
| `container-depth-limited` | 3 | 3 |
| `dep-missing-be` | 2 | 2 |
| `dep-missing-le` | 8 | 8 |
| `depth-limited` | 48 | 48 |
| `in-tree-symlink-metadata` | 1 | 1 |
| `legacy-body-failure` | 7 | 7 |
| `partial-body-failure` | 2 | 2 |
| `unknown-residue` | 4 | 4 |

Pair mismatches: 0.  `table_labels == evaluator_labels`: True.  Verdict: `met`.

