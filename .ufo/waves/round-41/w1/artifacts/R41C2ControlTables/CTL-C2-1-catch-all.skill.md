# CTL-C2-1 catch-all (one `*` row)

A single row with every feature cell `*`, including operation and provider: it accepts every envelope, so it cannot encode any precedence step and it also erases the domain guard of step 1.

Control data for the R41-C2 control score. The interpreter reads only the craft section below; this page and its comments are not instructions.

## Queue-drain craft

<!-- sqfs-triage-table v3 -->
<!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial audit-symlinks expect-link-absent count-gap confirm-empty raise-depth -->
| label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | `*` | `*` | `*` | `*` | `*` | `*` | `*` | `*` | `none` | every envelope is labelled clean because no cell constrains anything -> nothing is inspected, no gap is counted and no endianness handshake is considered | control only: no source, this row is a deliberate shortcut |
