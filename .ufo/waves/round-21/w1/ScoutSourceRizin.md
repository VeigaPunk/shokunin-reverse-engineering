# S043 `-c` anchor check

**Axes:** calibration (source-row anchor honesty) and depth (direct source branch evidence). **Scope:** read-only check of S043 and its pinned Rizin v0.8.2 `-c` source; no source-row or production edits.

## Observed facts

- `corpus/SOURCES.md:49` scopes S043 to Rizin v0.8.2 `iI`, `iS`, `ie`, `-N`, `-q`, and `-c`, but its anchor cell does not include the `-c` help or implementation anchors.
- Opened the immutable source URL on **2026-10-21**: <https://raw.githubusercontent.com/rizinorg/rizin/5a611eee2999d312317ff90d600e37dde0f58992/librz/main/rizin.c>.
- At `librz/main/rizin.c:111`, the help row says **“Execute rizin command”** (3 words; exact source text).
- At `librz/main/rizin.c:586-588`, `case 'c'` appends `opt.arg` to `cmds`. At `:353-355`, the `/* -c */` loop passes each `cmdn` to `rz_core_cmd_lines`. Together these anchor the flag's help, argument handling, and command execution in the pinned source.
- The earlier R20 reopen finding is consistent: `.ufo/waves/round-20/w2/ReopenS043S044.md:4-5` records the missing `:111` and `:586-588` anchors and correctly calls S043 partially anchored rather than factually contradicted.

## Assessment

The pinned source supports the existing narrow `-c` scope; no factual correction or scope narrowing is indicated. The issue is an omitted anchor cell entry. This source does not by itself establish REA policy, a sandbox, or safety of arbitrary command strings. Existing `-N`, `-q`, UTF-8, and info-command anchors remain as in S043.

## Advisory successor-row proposal

Do not rewrite S043. At the time inspected, `corpus/SOURCES.md:55-56` contains S049 and S050, so **S051 was the next observed free ID**; recheck ID availability when integrating. A fresh immutable successor should preserve S043's source identity, kind, tier, scope, teaching and recheck limit, while extending the anchor cell with these pinned locations:

`librz/main/rizin.c:111` (`-c` help), `:353-355` (`-c` command execution), `:586-588` (`-c` argument handling), plus all existing S043 anchors (`:128`, `:130`, `:678-697`, `:930-933`; `librz/core/cmd_descs/cmd_descs.c:12897,12956,13086`).

This is a report-only proposal; no row was created and no consumer citation or `used-by` value was changed.

## Checks and remaining limits

Read-only source-row inspection and pinned raw-source opens/searches only. No tests, REA operation, production edit, source-row write, or verification command was run. No unresolved source-content gap remains for the scoped `-c` help/handling/execution claim. If integrated, the parent should recheck the next ID, migrate source citations/`used-by` references as appropriate, and run the source-census validator plus its normal stable changed-path smoke/final suite once. The integration checks were not run here.
