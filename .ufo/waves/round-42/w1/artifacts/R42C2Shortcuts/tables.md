# Shortcut tables (R42C2Shortcuts artifacts)

All tables are v4-grammar (13 columns incl `failing handler`); they were produced by the minimal-table search over the A1 universe (2022 tuples: round-41 held-out, the committed round-42 dev-arm envelopes, predicted legacy/container/residue classes and the widened combo factor space). Scores are mismatch counts over that universe using the independent A1 transcription as ground truth.

## A. Canonical minimal table (15 rows, 28 constrained cells)

canonical

<!-- sqfs-triage-actions: audit-symlinks confirm-empty count-gap cross-read-legacy expect-link-absent inspect-input install-extractor-be install-extractor-le isolate-residue none preserve-failure raise-depth salvage-partial wrap-extractor-be -->

| label | operation | provider | handler | failing handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `partial-body-failure` | `*` | `*` | `*` | `squashfs_*` | `*` | `*` | `*` | `*` | `>0` | `salvage-partial` | `shortcut row 1 -> salvage-partial` | `R42C2Shortcuts analysis` |
| `in-tree-symlink-metadata` | `*` | `*` | `*` | `*` | `unpublished-entry` | `*` | `*` | `no` | `*` | `count-gap` | `shortcut row 2 -> count-gap` | `R42C2Shortcuts analysis` |
| `clean` | `*` | `*` | `*` | `*` | `none` | `*` | `*` | `no` | `>0` | `none` | `shortcut row 3 -> none` | `R42C2Shortcuts analysis` |
| `dep-missing-be` | `*` | `*` | `squashfs_*` | `*` | `*` | `sasquatch-v4be+` | `*` | `*` | `*` | `install-extractor-be` | `shortcut row 4 -> install-extractor-be` | `R42C2Shortcuts analysis` |
| `avm-marker-be-dropped` | `*` | `*` | `*` | `squashfs_v4_be` | `*` | `*` | `no` | `*` | `*` | `wrap-extractor-be` | `shortcut row 5 -> wrap-extractor-be` | `R42C2Shortcuts analysis` |
| `no-squashfs-chunk` | `*` | `unblob` | `none` | `*` | `none` | `*` | `*` | `*` | `*` | `inspect-input` | `shortcut row 6 -> inspect-input` | `R42C2Shortcuts analysis` |
| `mixed-symlinks` | `*` | `*` | `*` | `*` | `unpublished-entry` | `*` | `*` | `*` | `*` | `audit-symlinks` | `shortcut row 7 -> audit-symlinks` | `R42C2Shortcuts analysis` |
| `escaping-symlink-removed` | `*` | `*` | `*` | `*` | `none` | `*` | `*` | `*` | `>0` | `expect-link-absent` | `shortcut row 8 -> expect-link-absent` | `R42C2Shortcuts analysis` |
| `dep-missing-le` | `*` | `*` | `squashfs_*` | `*` | `*` | `sasquatch` | `*` | `*` | `*` | `install-extractor-le` | `shortcut row 9 -> install-extractor-le` | `R42C2Shortcuts analysis` |
| `container-depth-limited` | `*` | `*` | `none` | `*` | `depth-limited+` | `*` | `*` | `*` | `*` | `raise-depth` | `shortcut row 10 -> raise-depth` | `R42C2Shortcuts analysis` |
| `body-extractor-failure` | `*` | `*` | `*` | `squashfs_v4_*` | `*` | `*` | `*` | `*` | `*` | `preserve-failure` | `shortcut row 11 -> preserve-failure` | `R42C2Shortcuts analysis` |
| `clean-empty` | `*` | `*` | `squashfs_*` | `*` | `none` | `*` | `*` | `*` | `*` | `confirm-empty` | `shortcut row 12 -> confirm-empty` | `R42C2Shortcuts analysis` |
| `unknown-residue` | `*` | `*` | `*` | `*` | `unknown-chunk-handler+` | `*` | `*` | `*` | `>0` | `isolate-residue` | `shortcut row 13 -> isolate-residue` | `R42C2Shortcuts analysis` |
| `depth-limited` | `*` | `*` | `*` | `*` | `*` | `*` | `*` | `*` | `>0` | `raise-depth` | `shortcut row 14 -> raise-depth` | `R42C2Shortcuts analysis` |
| `legacy-body-failure` | `*` | `*` | `*` | `*` | `extractor-failure+` | `*` | `*` | `*` | `*` | `cross-read-legacy` | `shortcut row 15 -> cross-read-legacy` | `R42C2Shortcuts analysis` |

## B. Minimal table with the dependencies column completely unused (15 rows)

no-deps

<!-- sqfs-triage-actions: audit-symlinks confirm-empty count-gap cross-read-legacy expect-link-absent inspect-input install-extractor-be install-extractor-le isolate-residue none preserve-failure raise-depth salvage-partial wrap-extractor-be -->

| label | operation | provider | handler | failing handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `partial-body-failure` | `*` | `*` | `*` | `squashfs_*` | `*` | `*` | `*` | `*` | `>0` | `salvage-partial` | `shortcut row 1 -> salvage-partial` | `R42C2Shortcuts analysis` |
| `in-tree-symlink-metadata` | `*` | `*` | `*` | `*` | `unpublished-entry` | `*` | `*` | `no` | `*` | `count-gap` | `shortcut row 2 -> count-gap` | `R42C2Shortcuts analysis` |
| `clean` | `*` | `*` | `*` | `*` | `none` | `*` | `*` | `no` | `>0` | `none` | `shortcut row 3 -> none` | `R42C2Shortcuts analysis` |
| `dep-missing-be` | `*` | `*` | `squashfs_v4_be` | `*` | `missing-extractor-dependency+` | `*` | `*` | `*` | `*` | `install-extractor-be` | `shortcut row 4 -> install-extractor-be` | `R42C2Shortcuts analysis` |
| `dep-missing-le` | `*` | `*` | `squashfs_*` | `*` | `missing-extractor-dependency+` | `*` | `*` | `*` | `*` | `install-extractor-le` | `shortcut row 5 -> install-extractor-le` | `R42C2Shortcuts analysis` |
| `avm-marker-be-dropped` | `*` | `*` | `*` | `squashfs_v4_be` | `*` | `*` | `no` | `*` | `*` | `wrap-extractor-be` | `shortcut row 6 -> wrap-extractor-be` | `R42C2Shortcuts analysis` |
| `no-squashfs-chunk` | `*` | `unblob` | `none` | `*` | `none` | `*` | `*` | `*` | `*` | `inspect-input` | `shortcut row 7 -> inspect-input` | `R42C2Shortcuts analysis` |
| `mixed-symlinks` | `*` | `*` | `*` | `*` | `unpublished-entry` | `*` | `*` | `*` | `*` | `audit-symlinks` | `shortcut row 8 -> audit-symlinks` | `R42C2Shortcuts analysis` |
| `escaping-symlink-removed` | `*` | `*` | `*` | `*` | `none` | `*` | `*` | `*` | `>0` | `expect-link-absent` | `shortcut row 9 -> expect-link-absent` | `R42C2Shortcuts analysis` |
| `body-extractor-failure` | `*` | `*` | `*` | `squashfs_v4_*` | `*` | `*` | `*` | `*` | `*` | `preserve-failure` | `shortcut row 10 -> preserve-failure` | `R42C2Shortcuts analysis` |
| `container-depth-limited` | `*` | `*` | `none` | `*` | `depth-limited+` | `*` | `*` | `*` | `*` | `raise-depth` | `shortcut row 11 -> raise-depth` | `R42C2Shortcuts analysis` |
| `legacy-body-failure` | `*` | `*` | `*` | `*` | `extractor-failure+` | `*` | `*` | `*` | `*` | `cross-read-legacy` | `shortcut row 12 -> cross-read-legacy` | `R42C2Shortcuts analysis` |
| `unknown-residue` | `*` | `*` | `*` | `*` | `unknown-chunk-handler+` | `*` | `*` | `*` | `*` | `isolate-residue` | `shortcut row 13 -> isolate-residue` | `R42C2Shortcuts analysis` |
| `clean-empty` | `*` | `*` | `squashfs_*` | `*` | `*` | `*` | `*` | `*` | `0` | `confirm-empty` | `shortcut row 14 -> confirm-empty` | `R42C2Shortcuts analysis` |
| `depth-limited` | `*` | `*` | `*` | `*` | `*` | `*` | `*` | `*` | `>0` | `raise-depth` | `shortcut row 15 -> raise-depth` | `R42C2Shortcuts analysis` |

## C. All-but-one-class example: legacy-body-failure row removed (14 rows); legacy envelopes fall to (unclassified, none)

no-legacy

<!-- sqfs-triage-actions: audit-symlinks confirm-empty count-gap expect-link-absent inspect-input install-extractor-be install-extractor-le isolate-residue none preserve-failure raise-depth salvage-partial wrap-extractor-be -->

| label | operation | provider | handler | failing handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `partial-body-failure` | `*` | `*` | `*` | `squashfs_*` | `*` | `*` | `*` | `*` | `>0` | `salvage-partial` | `shortcut row 1 -> salvage-partial` | `R42C2Shortcuts analysis` |
| `in-tree-symlink-metadata` | `*` | `*` | `*` | `*` | `unpublished-entry` | `*` | `*` | `no` | `*` | `count-gap` | `shortcut row 2 -> count-gap` | `R42C2Shortcuts analysis` |
| `clean` | `*` | `*` | `*` | `*` | `none` | `*` | `*` | `no` | `>0` | `none` | `shortcut row 3 -> none` | `R42C2Shortcuts analysis` |
| `dep-missing-be` | `*` | `*` | `squashfs_*` | `*` | `*` | `sasquatch-v4be+` | `*` | `*` | `*` | `install-extractor-be` | `shortcut row 4 -> install-extractor-be` | `R42C2Shortcuts analysis` |
| `avm-marker-be-dropped` | `*` | `*` | `*` | `squashfs_v4_be` | `*` | `*` | `no` | `*` | `*` | `wrap-extractor-be` | `shortcut row 5 -> wrap-extractor-be` | `R42C2Shortcuts analysis` |
| `no-squashfs-chunk` | `*` | `unblob` | `none` | `*` | `none` | `*` | `*` | `*` | `*` | `inspect-input` | `shortcut row 6 -> inspect-input` | `R42C2Shortcuts analysis` |
| `mixed-symlinks` | `*` | `*` | `*` | `*` | `unpublished-entry` | `*` | `*` | `*` | `*` | `audit-symlinks` | `shortcut row 7 -> audit-symlinks` | `R42C2Shortcuts analysis` |
| `escaping-symlink-removed` | `*` | `*` | `*` | `*` | `none` | `*` | `*` | `*` | `>0` | `expect-link-absent` | `shortcut row 8 -> expect-link-absent` | `R42C2Shortcuts analysis` |
| `dep-missing-le` | `*` | `*` | `squashfs_*` | `*` | `*` | `sasquatch` | `*` | `*` | `*` | `install-extractor-le` | `shortcut row 9 -> install-extractor-le` | `R42C2Shortcuts analysis` |
| `container-depth-limited` | `*` | `*` | `none` | `*` | `depth-limited+` | `*` | `*` | `*` | `*` | `raise-depth` | `shortcut row 10 -> raise-depth` | `R42C2Shortcuts analysis` |
| `body-extractor-failure` | `*` | `*` | `*` | `*` | `extractor-failure+` | `*` | `*` | `*` | `*` | `preserve-failure` | `shortcut row 11 -> preserve-failure` | `R42C2Shortcuts analysis` |
| `clean-empty` | `*` | `*` | `squashfs_*` | `*` | `*` | `*` | `*` | `*` | `0` | `confirm-empty` | `shortcut row 12 -> confirm-empty` | `R42C2Shortcuts analysis` |
| `unknown-residue` | `*` | `*` | `*` | `*` | `unknown-chunk-handler+` | `*` | `*` | `*` | `*` | `isolate-residue` | `shortcut row 13 -> isolate-residue` | `R42C2Shortcuts analysis` |
| `depth-limited` | `*` | `*` | `*` | `*` | `*` | `*` | `*` | `*` | `>0` | `raise-depth` | `shortcut row 14 -> raise-depth` | `R42C2Shortcuts analysis` |
