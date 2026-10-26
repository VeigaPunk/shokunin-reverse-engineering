# Independent re-run of all six frozen round-39 C1 carriers (seat R39W2C1AxisFit)

Command per carrier (fresh outdir under $HYAKU_SCRATCH/kaidoku-r39/R39W2C1AxisFit/reaout/<K>):
`cd $S && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware --format json --full-output <carrier> <outdir>`

| carrier | handler | failed chunks | published | = committed receipt | gaps (re-run) | = receipt gaps | subject digest = carriers.json pin | oracle rows / mismatches |
|---|---|---|---|---|---|---|---|---|
| K1 | `squashfs_v4_be` | 0 | 5 | yes | none | yes | yes | 5 / 0 |
| K2 | `squashfs_v4_be` | 0 | 3 | yes | unpublished-entry:run-link | yes | yes | 3 / 0 |
| K3 | `squashfs_v4_be` | 0 | 4 | yes | none | yes | yes | 4 / 0 |
| K4 | `squashfs_v4_be` | 0 | 4 | yes | none | yes | yes | 4 / 0 |
| K5 | `squashfs_v4_be` | 0 | 10 | yes | unpublished-entry:link-blob, unpublished-entry:link-notes | yes | yes | 10 / 0 |
| K6 | `squashfs_v4_be` | 0 | 8 | yes | unpublished-entry:link-in | yes | yes | 8 / 0 |

ALL_SIX_OK = True. Exit codes: 0 for every carrier; stderr empty.

Evidence id differs from the committed receipt for every carrier because `parameters.output_directory` is inside the hashed projection and this run used `$HYAKU_SCRATCH/kaidoku-r39/R39W2C1AxisFit/reaout/<K>`; the semantic payload above is identical. That behaviour is itself the property wave-1 (b) relied on: the id binds the run path, so a byte-copied receipt cannot keep its id.
