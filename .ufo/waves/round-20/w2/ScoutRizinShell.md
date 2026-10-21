FALSIFIED — In the tested REA call, Rizin accepted `!true` and executed `/usr/bin/true` directly; it did not spawn a shell for the escape. The outer npx package launcher did invoke a shell, which is a separate layer.

**Observed — 2026-10-21T07:27:23Z**

- Exact call: `npx -y rea-agents@6.5.0 execute-rizin-command /usr/bin/jq '!true'` (argv invocation, cwd `/tmp/kr20ScoutRizinShell-f8cqyx6r`); CLI exit **0**, stdout 1,735 bytes (the Evidence envelope), stderr 0 bytes.
- Evidence ID: `ev_0c36171c8a1393d960cac58016e3baaf918c849170c0c84c4d833320071a555a`; subject SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`.
- Exact `raw_result`: `stdout=""`, `stderr=""`, `exit_code=0`, `signal=null`, `output_truncated=false`, `completion_status=complete`, `artifact_sha256_after=e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`, `artifact_changed=false`. The envelope records `command_arguments`: `rizin -N -q -c '!true' /usr/bin/jq`.
- I repeated the call under strace, including a marker-env run; each returned CLI exit 0 and the same Evidence ID/raw result.

**Process evidence**

- Traced exact REA call: `strace -f -v -qq -s 600 -e trace=execve,clone,clone3 -o <mkdtemp>/trace.log npx -y rea-agents@6.5.0 execute-rizin-command /usr/bin/jq '!true'`; strace exit **0**. Trace: `/tmp/kr20reamark-r28jmopj/trace.log`.
- Rizin (`/usr/bin/rizin`, argv `-N -q -c !true /usr/bin/jq`) cloned a child; that child searched PATH and successfully `execve`d `/usr/bin/true` with argv `['true']`. `KR20_MARK=kr20scoutshell` propagated from the traced invocation into that child, confirming it belongs to the Rizin process rather than an unrelated host process. Its only additional environment entries were Rizin's 14 `RZ_*` exports (`RZ_ARCH`, `RZ_BIN_DEMANGLE`, `RZ_BIN_LANG`, `RZ_BIN_PDBSERVER`, `RZ_BITS`, `RZ_BSIZE`, `RZ_COLOR`, `RZ_CONFIG`, `RZ_DEBUG`, `RZ_ENDIAN`, `RZ_FILE`, `RZ_IOVA`, `RZ_OFFSET`, `RZ_SIZE`). No shell exec occurred on that escape path.
- The trace does show `/usr/bin/sh -c "'rea' execute-rizin-command /usr/bin/jq !true"` for npx/npm's package-bin launcher. Do not conflate that wrapper shell with Rizin's `!true` handling.
- Direct control, same Rizin argv: `strace -f -qq -s 300 -e trace=execve -o <mkdtemp>/trace.log /usr/bin/rizin -N -q -c '!true' /usr/bin/jq`; exit **0**, stdout/stderr empty; its child likewise execve'd `/usr/bin/true` without a shell (`/tmp/kr20rizintrace-hy5r43uq/trace.log`). Local version output: `rizin 0.8.2 @ linux-x86-64`.

**Assessment / boundary**

- Observed: this `!true` escape is accepted and executes an external program, but no shell process is spawned for it. That falsifies the literal `system(3)`/shell characterization for this tested command shape. The broader safety warning that Rizin commands can execute programs remains warranted.
- The target entry at source revision S (`corpus/knowledge/2026-10-20-r20-rizin-command-observation.md:41`) attributes `!<command>` to a shell via `system(3)` and relies on S044. The retained wave-1 table records `!echo REA_RIZIN_SHELL_OK` exit 0 but only a completion status (`.ufo/waves/round-20/w1/ScoutRizinSchema.md:125`); that row alone does not establish a shell process. Wave-1's notes describe shell execution (`:210-211`).
- **Unresolved:** only `!true` was used, as instructed. This does not establish how Rizin treats shell metacharacters in other `!` commands; do not generalize the no-shell observation beyond the tested form. Suggested wording: “`!true` is not refused and executes the named program directly on Rizin 0.8.2; shell execution/syntax for other forms was not tested.”

Report: .ufo/waves/round-20/w2/ScoutRizinShell.md
