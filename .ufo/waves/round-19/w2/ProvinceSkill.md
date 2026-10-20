# ProvinceSkill — scoped reproduction

**Axes exercised:** freshness (live skill/cache state), calibration (hashes and line anchors), depth (separating the skill-file digest from the REA catalog digest and the full directory contents).

## Severity-ordered findings

**No actionable finding in the requested active-skill, `.bashrc`-anchor, or named-cache checks.** The current `PROVINCE.md` statements at `:12`, `:19-26` match the observations below. I reviewed the baseline-to-main `PROVINCE.md` diff: it replaced the stale installed `c863…` digest with `fbcd…`, changed the 6.4.0 cache wording to explicitly historical/absent, and updated the `.bashrc` anchors.

## Observations

- **Installed skill SHA and 6.7.0 equality — reproduced.** `PROVINCE.md:24` names installed SHA `fbcd39d6…`. The installed `~/.agents/skills/reverse-engineer-anything/SKILL.md` and the 6.7.0 bundle's `skills/reverse-engineer-anything/SKILL.md` both hash to `fbcd39d6abe803cf7aa49c1880815bc8e22ba2af87a23681944f687bb7629eb1`; `cmp` also reports byte equality. Both files have `metadata.version: "42"` and `tool_count: 207` at lines 5-6. The named `.recovery` sibling hashes to `c86398238b2a382dd34f4df230f83a5a1c3377a4f0c4df39ea43053ea0b49da0`, confirming the old digest now identifies the recovery copy, not the active `SKILL.md`.
- **Scope of equality — observed.** Each of the six canonical reference files (`android-applications.md`, `connection-and-recovery.md`, `evidence-workflows.md`, `javascript-applications.md`, `native-and-artifacts.md`, `runtime-observation.md`) also compares byte-equal to the 6.7.0 bundle. The installed directory additionally contains `.rea.backup*` recovery files that are absent from the bundle inventory. Thus the reproduced equality is for the active `SKILL.md` and canonical references, excluding recovery backups; it is not a claim that the two directory trees have identical entry sets.
- **Counts and identity are distinct — observed.** The retained `.ufo/waves/round-19/evidence/rea-catalog.json` first record (`/0`) is version 6.7.0 with 153 `cli_commands`, 207 `mcp_tools`, and `tools_sha256=af39310c9591bb981893ec0d2188b1bcf6e9cc8ba3ac513d5bbefc8ddcb85639`. Independently, the cached package's `CLI_COMMAND_NAMES` has 153 unique entries; its single CLI alias is separate. This catalog digest is not the installed `SKILL.md` SHA.
- **`.bashrc` anchors — reproduced textually.** `PROVINCE.md:25` cites `.bashrc:28-29`, which are the `GHIDRA_INSTALL_DIR` and `JAVA_HOME` exports. They precede the non-interactive return at `.bashrc:33-34`. `PROVINCE.md:26` cites `.bashrc:63-69`, the seven `REA_*` provider exports; these follow that guard. The exact current line placement therefore matches the document, including its distinction between the above-guard and below-guard exports.
- **6.4.0 cache absence — reproduced at the named npx location.** `PROVINCE.md:12,21-23` identifies `dea9475797100b20` as historical and absent. `/home/vgpnk/.npm/_npx/dea9475797100b20` does not exist (`ls` exit 2; negative existence test exit 0). A package-manifest glob under `~/.npm/_npx/*/node_modules/rea-agents/package.json` returns only the 6.7.0 `a1722018f28f9df2` and 6.5.0 `ad9a3fdbcad992c6` locations.

## Commands and exit codes

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main
  exit 0: 279e8b19c51658bfd05b9e31a1c0894ab2e70537

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin --no-optional-locks diff --no-ext-diff --unified=3 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 refs/heads/main -- PROVINCE.md
  exit 0: relevant changes are in PROVINCE.md:8-26 and the REA/JDK table rows; baseline-to-main diff reviewed.
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin --no-optional-locks diff --no-ext-diff --unified=3 -- PROVINCE.md
  exit 0: no uncommitted PROVINCE.md diff.

sha256sum /home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/skills/reverse-engineer-anything/SKILL.md /home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md.rea.backup.c86398238b2a382dd34f4df230f83a5a1c3377a4f0c4df39ea43053ea0b49da0.recovery
  exit 0: installed and 6.7.0 bundled files both fbcd39d6…; recovery file c8639823…
cmp -s /home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/skills/reverse-engineer-anything/SKILL.md
  exit 0 (wrapper printed byte_equal=yes, cmp_exit=0).
node -p "require('/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/package.json').version"
  exit 0: 6.7.0
node --input-type=module -e 'import {CLI_COMMAND_NAMES, CLI_COMMANDS, CLI_COMMAND_ALIASES, MCP_TOOLS_WITHOUT_DEDICATED_CLI} from "file:///home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/cliCommandNames.js"; console.log(JSON.stringify({commandNames:CLI_COMMAND_NAMES.length, commandKeys:Object.keys(CLI_COMMANDS).length, uniqueNames:new Set(CLI_COMMAND_NAMES).size, aliases:CLI_COMMAND_ALIASES.length, mcpToolsWithoutDedicatedCli:MCP_TOOLS_WITHOUT_DEDICATED_CLI.length}))'
  exit 0: {"commandNames":153,"commandKeys":153,"uniqueNames":153,"aliases":1,"mcpToolsWithoutDedicatedCli":65}
ls -ld /home/vgpnk/.npm/_npx/dea9475797100b20
  exit 2: No such file or directory.
test ! -e /home/vgpnk/.npm/_npx/dea9475797100b20
  exit 0: cache_path_absent=yes.

i=/home/vgpnk/.agents/skills/reverse-engineer-anything/references; b=/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/skills/reverse-engineer-anything/references; for f in android-applications.md connection-and-recovery.md evidence-workflows.md javascript-applications.md native-and-artifacts.md runtime-observation.md; do cmp -s "$i/$f" "$b/$f" || { rc=$?; printf 'different %s cmp_exit=%s\n' "$f" "$rc"; exit "$rc"; }; printf 'equal %s\n' "$f"; done
  exit 0: all six canonical reference files equal.
```

The exact `.bashrc` anchors above were read directly from `/home/vgpnk/.bashrc:26-34,62-69`; the retained JSON counts were read from `.ufo/waves/round-19/evidence/rea-catalog.json` using `/0` fields `version`, `cli_commands`, `mcp_tools`, and `tools_sha256`.

## Residual risk and verification gaps

- **Inference/limitation:** the cache check establishes absence from the named `_npx` path and the enumerated REA package manifests under `_npx`; it does not establish that no 6.4.0 copy exists elsewhere on disk. I did not invoke `npx -y rea-agents@6.4.0 --version`: that could fetch and recreate the absent cache. Historical 6.4.0 counts/catalog identity were not rederived.
- **Limitation:** `.bashrc` verification establishes text and guard placement only. I did not source it or recheck whether each provider-export path currently resolves/executable; this report does not independently certify those separate `PROVINCE.md:26` assertions.
- No install, cache mutation, production edit, build, test suite, REA/Ghidra run, or carrier execution was performed. The only write is this report.
