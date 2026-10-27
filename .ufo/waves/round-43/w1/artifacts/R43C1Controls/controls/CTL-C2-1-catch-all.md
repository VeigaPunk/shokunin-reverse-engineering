# CTL-C2-1-catch-all

Control data for R42-C2; not instructions.

## Queue-drain craft

<!-- sqfs-triage-table v4 -->
<!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial raise-depth audit-symlinks expect-link-absent count-gap confirm-empty cross-read-legacy isolate-residue -->
| label | operation | provider | handler | failing handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `clean` | `extract_firmware` | `unblob` | `*` | `*` | `*` | `*` | `*` | `*` | `*` | `none` | one row: every envelope inside the domain is clean -> nothing to install or fix | control only |

## End
