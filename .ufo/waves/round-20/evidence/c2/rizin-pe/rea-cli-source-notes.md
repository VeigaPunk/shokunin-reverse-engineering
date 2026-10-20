# Installed REA CLI source notes

Package: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, `package.json` names `rea-agents` version `6.5.0` (lines 1-5). These are installed-source observations, not a claim that npm package source is an independent behavioral run.

- `dist/cli/reverseEngineeringCommands.js:114-125` defines `execute-rizin-command`, with `path` and `command` string arguments, then calls `service.executeRizinCommand`.
- `dist/domain/reverseEngineering.js:22-31` requires a nonempty path and nonempty single command-line string; its command refinement rejects CR, LF, and NUL, but does not reject semicolons.
- `dist/application/reverse/ReverseEngineeringService.js:150-168` resolves and digests the path before spawning the provider; non-access-denied, non-timeout digest failures become `AnalysisInputError`.
- `dist/application/reverse/ReverseEngineeringService.js:617-622` makes the digest gate require a regular file (`EINVAL` otherwise). Provider launch follows the digest gate at `:186-195`.
- `dist/contracts/reverseEngineeringToolContracts.js:42` warns that caller-selected Rizin commands/plugins can execute foreign code, mutate files, access the network, and read outside the selected artifact; those external inputs are not bound to Evidence.

Official upstream documentation (Rizin Handbook, fetched 2026-10-20): `https://book.rizin.re/src/first_steps/commandline_rizin.html` §§8.0.2 and 8.0.5 state that `!<command>` runs through `system(3)` and `;` separates commands; `https://book.rizin.re/src/basic_commands/sections.html` documents `iS` as listing sections. These docs do not claim that REA refuses shell escapes.


This source matches the two observed path errors' generic `invalid_input` projection and explains why no Evidence was emitted for them. The tool output does not itself identify the failing filesystem operation, so the typed mechanism is source-backed interpretation, not an extra runtime field.
