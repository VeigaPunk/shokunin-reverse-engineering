# R41SrcRea artifacts

Source anchors for the round-41 SquashFS outcome-triage table v3 (R41-C2), plus the envelope probes that
confirm the gap shapes. No vendor bytes: all fixtures are lane-built, and every vendor-side claim is a
sha256 plus a rebuild command.

| file | what it is |
|---|---|
| `anchors.md` | the anchors table: four targets, file:line + ≤25-word quote, the S-row that owns each document, and the disposition (extend / new row). §5 is the decision table for the L1; §6 is the identity check run today. |
| `row-drafts.md` | ready-to-paste `SOURCES.md` rows: **S129** (`processing.py`, required — no row covers it), optional **S130** (sasquatch writer/exit, same document as S121), and the exact anchor/scope text to append to S118, S119, S120, S121, S123. |
| `env-depth1.json` | REA 6.5.0 `extract-firmware --max-depth 1` on `fixtures/outer.sqfs`: one `depth-limited` gap with every identity field null, one published file under the same path, `coverage: "partial"`, `diagnostics: []`. |
| `env-depth3.json` | control at the default ceiling 3 on the same bytes: two files, no gap, `coverage: "complete"`. |
| `env-nodep-le.json` | same image, sasquatch unreachable: `missing-extractor-dependency`, `dependencies: ["sasquatch"]`. |
| `env-nodep-avmbe.json` | `fixtures/avm-pad.sqfs` (genuine AVM layout), sasquatch unreachable: handler `squashfs_v4_be`, `dependencies: ["sasquatch-v4be"]` only. |
| `env-fatal.json` | `fixtures/lebig-corrupt2.sqfs`: fatal sasquatch corruption → `extractor-failure` gap, `diagnostics[0].report` = `ExtractCommandFailedReport` (`exit_code: 1`, severity `WARNING`, argv visible with `-no-exit-code`). |
| `probe.sh` | the five REA invocations, verbatim, plus the reduction used to build the `env-*.json` files. |
| `fixtures/build.sh` | rebuilds all three fixtures from nothing; prints their sha256. |
| `fixtures/sha256sums.txt` | digests of the copies here. |

Run `probe.sh` from a scratch directory (unblob writes `unblob.log` into its cwd) and give every REA run a
fresh, absent output directory.
