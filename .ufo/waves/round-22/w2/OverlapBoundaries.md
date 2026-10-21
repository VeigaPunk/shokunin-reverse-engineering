# OverlapBoundaries — round-22 W2 (KaidokuR22R.OverlapBoundaries-6)

Author-side evidence only, written 2026-10-21. This report does not admit anything, edit source, or award ownership. The lane HEAD is `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`, which is two commits past the frozen baseline `7787fea4…`: `75f04a4` froze the claims and `2ee3d9f` retained the evidence and dispositions. Revenger HEAD is `cf02419`. Revenger was read-only throughout.

Nothing was installed or updated. No REA producer was invoked. No counter, selftest, build, or test was run. No source tree was edited. The only file written is this report.

## Axes

- **coverage** (R22-C1).
- **calibration** (R22-C2).

The proposed move improves calibration and leaves coverage unchanged: it neither adds nor removes counted verbs, and no counter outcome changes.

## Evidence

### Where kaidoku and revenger overlap at L0

The overlap is declared in both provinces, but revenger has not exercised any of it.

| # | Ground | kaidoku anchor | revenger anchor | revenger exercised? |
|---|---|---|---|---|
| O1 | Reverse engineering of shipped artifacts with REA: native, managed, Electron/JS, APK, archives, firmware; evidence-ledger discipline | `PROVINCE.md:3-6`, Core table | `PROVINCE.md:3-7` "Owns" | yes for PE/EVM/JS fixtures (LOG.md) |
| O2 | Browser/Electron runtime evidence (CDP) | Core rows "Runtime observation (CDP)" `PROVINCE.md:53` and "Runtime observation verbs" `:127`; MINT Frontier `MINT.md:34-35` | `PROVINCE.md:5` | **no.** LOG.md has 0 matches for `cdp\|list-browser-targets\|inspect-web-page\|observe-web\|electron-page\|capture-browser`; only 1 corpus file matches |
| O3 | Android APKs | `MINT.md:34` "Android APK analysis" (Frontier); Core "APK surface (full)" `PROVINCE.md:56`; r22 Flutter negative `PROVINCE.md:200-205` | `PROVINCE.md:5` | **no.** LOG.md has 0 matches for `apk\|android`; the corpus mentions them only in `knowledge/2026-10-12-rea-readiness-checklist.md:17-18` and `seed.md:12` |
| O4 | REA registration and engine readiness | Core "REA MCP server" `PROVINCE.md:44`; the cross-lane registry `PROVINCE.md:64-71` | `PROVINCE.md:10-12` "server registration and engines are the lane's readiness domain" | readiness checklist only |
| O5 | REA pin | carriers pin `rea-agents@6.5.0` (`PROVINCE.md:12`) | Sources pin `rea-agents@6.4.0` (`PROVINCE.md:13`); LOG.md has `@6.4.0` ×9 and `@6.5.0` ×1 (`LOG.md:775`) | n/a |
| O6 | REA-native dynamic verbs (Frida, gdb/rizin debug, adb device mutation) | Adjacent "Non-REA dynamic analysis … Frida-style hooking (unowned)" `PROVINCE.md:103-106`; `claims.json` `not_claimed` keeps the overlap open | Refuses "live-target execution beyond the declared target and lifecycle" `PROVINCE.md:19-20`. No clause names Frida, debuggers, adb, pcap, Cutter, sigrok, or Flutter | **no.** Word-bounded search `rg -i -w 'frida\|adb\|tshark\|pcap\|cutter\|sigrok'` finds 0 matches in LOG.md and 0 corpus files. The 11 unbounded LOG hits were `deadbeef`/hex substrings. `flutter\|dart` matches nothing in LOG or corpus |

Contradictions, stated without resolving them:

- **K1 (O4).** Both lanes claim REA registration and engine readiness. Kaidoku's routing rule (`PROVINCE.md:66-71`: map entries "never re-base a sibling lane's frozen receipt … never stand for that lane's current runtime capability") limits harm but does not assign the ground.
- **K2 (O6).** Kaidoku's Adjacent bullet separates ground by REA vs non-REA. REA 6.5.0 now ships `instrument-with-frida`, `debug-with-gdb`, and `debug-with-rizin` (`dist/frida`, `dist/gdb`, `dist/rizin`), so that split no longer separates Frida-style hooking from the REA surface. Revenger refuses only live execution *beyond the declared target*, which implicitly permits declared-target execution. Neither text assigns REA-native dynamic verbs.
- **K3.** The r22 knowledge entry (`corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md:15`) says "Debugger/Frida ownership remains contested with revenger". The C2 preamble (`PROVINCE.md:176`) says "revenger's contested runtime province". Revenger's runtime clause covers browser/Electron only, and none of the 14 T2 verbs is a browser/Electron verb. The text-grounded contact for T2 is:
  - ADB: revenger's "Android APKs" clause and its live-target refusal clause.
  - Frida: revenger's refusal clause only.
  - pcap/packet and Cutter: no revenger clause.
- **K4 (O5).** Revenger's pinned surface includes the 24 adb verbs; `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:8,75-77` was observed under 6.4.0. For the other 15 T1/T2 zero-mention verbs, whether they exist at 6.4.0 is **UNKNOWN**: the 6.4.0 npx cache is absent and `rg -l -F 'rea-agents-6.4.0.tgz' ~/.npm/_cacache/index-v5` found nothing (exit 0). [INFERENCE] The 127→153 command delta (+26) leaves room for them to be 6.5.0-new. This is unverified, so revenger's ability to reach them stays unknown.

### Static Flutter (R22-C1, `identify-flutter-build`)

- **Target.** Recomputed `sha256sum` gives `6d1bb2cfa126a1b1c87e064a35b3cbd181bef0ec784dec1efd1d64dffa8be6cb`, which equals the entry. Recorded evidence `ev_3458b996…` reports `flutter_detected:false`, `abis:[]`, `coverage:"complete"`.
- **Provider.** The parser is provider-free. `rg -o 'REA_[A-Z_]+' dist/flutter` found no env key. `rg -i 'spawn|execFile|child_process' dist/flutter` found no match. The files are `DartElf.js`, `ElfBuildId.js`, `ElfLoadMap.js`, `FlutterBuildProvider.js`, and `FlutterPayloadScan.js`. A held result therefore says nothing about host engine or provider readiness.
- **`abis:[]` is not "no native code".** `unzip -l` on the same APK (exit 0) lists 8 `lib/<abi>/*.so` members across `arm64-v8a`, `armeabi-v7a`, `x86`, and `x86_64`: `libc++_shared.so` and `libgodot_android.so`. Zero members match `libapp.so|libflutter.so` (rg exit 1, no match). So `abis` reports Flutter ABIs only, and the entry's decision row "ABI list empty → do not infer absence of all native code" is backed by an observed counterexample, not just caution.
- **No positive carrier located.** `timeout 60 find /home/vgpnk /opt /usr/share /usr/lib -xdev \( -name libapp.so -o -name libflutter.so -o -name libflutter_linux_gtk.so -o -name '*.apk' \)` listed only the two Godot templates (`android_debug.apk` and `android_release.apk`). The search exited 124 when it hit the 60 s timeout, so it is **partial**.

### Explicit absent-provider C2 probes (R22-C2)

All 14 receipts have a `meta.command` equal to their row verb, and every `error.code` and `ok` value matches its row's `observed` cell (read-only `jq`; the counter was not run). Envelope `meta` carries only `command` and `duration`; the REA version is recorded only in the `.run.json` argv (`rea-agents@6.5.0`).

Provider env keys read by each 6.5.0 family (`rg -o 'REA_[A-Z_]+' dist/<family>`):

- pcap: `REA_TSHARK_COMMAND`, `REA_CAPINFOS_COMMAND`, `REA_TSHARK_PRLIMIT_COMMAND`
- cutter: `REA_CUTTER_BRIDGE_DIR`
- gdb: `REA_GDB_COMMAND`
- rizin: `REA_RIZIN_COMMAND`
- signals: `REA_SIGROK_COMMAND`, `REA_SIGROK_PRLIMIT_COMMAND`
- frida: none
- flutter: none

Host `command -v` on 2026-10-21:

- absent: `tshark`, `capinfos`, `frida`, `sigrok-cli`, `cutter`
- present: `adb` → `/usr/bin/adb`, `rizin` → `/usr/bin/rizin`, `gdb` → `/usr/bin/gdb`

Also: this interactive shell has `REA_ADB_PATH=/usr/bin/adb` and `REA_TSHARK_COMMAND` unset, and `/proc/sys/kernel/pid_max` is `4194304`.

| family (rows) | `env_overrides` in run record | gate actually hit | honest label |
|---|---|---|---|
| ADB (5) | `{"REA_ADB_PATH":"/usr/bin/false"}` | client version check: "The selected adb binary did not report a usable version." This fires before any serial or device check. | **Explicit absent-provider control.** These are the only 5 rows that earn the label. The gate differs from the real-client dead-serial path (`unsupported_target`, plus a daemon autostart on :5037 that REA's `may_have_started_adb_server` misreports; r4u-06 `:81-92,153-160,194-196`). That difference is why the false-client control is required: it avoids daemon contact. |
| packet (2): `inspect-packet-fields`, `inspect-packet-capture` | `{}` | `TsharkCaptureProvider.js:73-75` raises "Supply absolute REA_TSHARK_COMMAND" before any binary lookup | **Ambient unconfigured.** The refusal would recur even if TShark were installed on PATH, so it is not evidence about the provider. |
| pcap (2): `inspect-pcap-client`, `inspect-pcap-capture` | `{}` | `PcapConfiguration.js` falls back to PATH: "spawn tshark ENOENT"; capinfos was never reached | **Ambient host absence at capture time.** Not an explicit control. |
| Frida (3) | `{}` | `dist/frida` has no REA env key, so no env-level absent-provider control can exist. PID `2147483647` exceeds `pid_max` 4194304. | **Missing-target control** for `instrument-with-frida`; the error message is generic. The two list rows are positive provider observations. |
| Cutter (2) | `{}` for `list-cutter-sessions`; **no `env_overrides` key** in `cutter-command-missing.run.json`, whose keys are `argv, exit, stderr, stdout` | `list-cutter-sessions` returned an empty discovery at the ambient bridge dir; the well-formed missing UUID got `invalid_request` | **Ambient instant observation.** The row receipt `cutter-command-missing.json` was not produced by `tools/capture-probes.py`, which emits the malformed-id `cutter-command.json` (`VALIDATION_ERROR`). Its producer and env are unrecorded: a provenance gap. |

Placement versus the frontier anchor. `PROVINCE.md:74` defines Frontier as "Claimed in MINT.md, not yet held":

- ADB `frontier-blocked` is grounded: `MINT.md:34` and PROVINCE Frontier "adb device surface" `:149-150`.
- Frida `adjacent` is grounded: `PROVINCE.md:103-106`.
- pcap/packet `frontier-blocked` (4 rows): neither MINT.md nor PROVINCE Frontier names pcap, TShark, or packet capture. A saved capture is not a "shipped artifact" in the domain statement.
- Cutter `frontier-blocked` (2 rows): not named either. The closest anchor is the Frontier "Alternate providers — IDA, Hopper, JEB" bullet (`:86-87`), which is an extension by analogy [INFERENCE].

`count-c2.py:33` accepts both `frontier-blocked` and `adjacent`, so placement wording has no effect on the counter.

### T1 debugger verbs under this wave's contract

The wave contract forbids target execution and debug attach.

- **`debug-with-rizin`.** `RizinDebugSessionManager.js:207-219` always runs `rizin -N -0 -d … <resolvedPath>`. Session start spawns the selected target as an inferior. Any non-refused record therefore implies target process creation, which this wave forbids and which revenger's live-target refusal also touches. It cannot be held under the current contract.
- **`debug-with-gdb`.** `reverseEngineeringCommands.js:128-141` takes one unrestricted console command and a required `--inferior-tty`. `GdbSessionManager.js:287,324-326` launches `--nx` with no inferior until `execute()` is called. REA's one-shot filter (`:1404-1416`) rejects only:
  - redirections, `;`, and newlines
  - `source`, `define`, `alias`, and `py`/`python`
  - `tty` and `set inferior-tty`

  It does **not** reject `run`, `start`, `starti`, `attach`, `target remote`, or `shell`/`!`. REA is therefore not the no-execution boundary; the caller's command allowlist is. Whether a non-interactive agent can supply a TTY that passes validation is **UNKNOWN**: no probe was run.
- **`inspect-signal-decoders` and `decode-signal-recording`.** The provider command `sigrok-cli` is absent on this host, so any probe would be a refusal, which the C1 falsifier excludes [INFERENCE from absence; no probe run].

## Proposed move (one bounded synthesis)

The move tightens claim language so each disposition and limit names its **actual gate and the exact province clause** it touches. It changes no counted fact, receipt, or prior file. All edits fall inside surfaces the frozen claims already touch: the C2 section of `PROVINCE.md` and the new r22 knowledge entry. Nothing goes outside the claims.

### 1. Static Flutter limits

L1 should apply these to the r22 entry as text.

1. **Scope.** The held ground is one parsed negative on SHA-256 `6d1bb2cf…` only. `android_debug.apk` is unprobed.
2. **Parser.** The parser is provider-free (no env key, no spawn). The record must not be cited for provider or engine readiness.
3. **Counterexample.** `abis:[]` coexists with 8 `lib/<abi>/*.so` members across 4 ABIs and zero `libapp.so`/`libflutter.so`. Cite this as the observed counterexample for the existing decision row.
4. **`inspect-dart-aot`.** Do not count it from the Godot carriers. Any envelope there is a refusal or negative on a non-Flutter APK, and the C1 falsifier already rejects refusals. A synthetic `libapp.so` would exercise ELF symbol location, not Dart snapshot parsing. If used, label it synthetic and limit the claim to the four-symbol lookup.
5. **No device ground.** No install, device selection, or adb verb attaches to Flutter ground.
6. **Ownership wording.** Replace "Debugger/Frida ownership remains contested with revenger" with wording that cites exact clauses: "No revenger PROVINCE clause names debuggers or Frida. Revenger refuses live-target execution beyond the declared target (`../revenger-shokunin/PROVINCE.md:19-20`); kaidoku Adjacent lists Frida-style hooking as unowned (`PROVINCE.md:103-106`). Ground stays open and unassigned." Static APK ground remains declared by both lanes (`MINT.md:34`; `../revenger-shokunin/PROVINCE.md:5`). This entry is verb coverage, not APK or Flutter domain ownership.

### 2. Explicit absent-provider C2 limits

L1 should apply these as reason or preamble text; no row values change.

1. Reserve "explicit absent-provider control" for the 5 ADB rows. State that their gate is the client version check, distinct from the r4u-06 real-client dead-serial `unsupported_target` path.
2. Packet rows: "ambient: `REA_TSHARK_COMMAND` unset; configuration gate `TsharkCaptureProvider.js:73-75` fires regardless of TShark presence."
3. Pcap rows: "ambient PATH lookup ENOENT at capture time; capinfos not reached."
4. Frida: "no REA env key exists, so an env-level absent-provider control is impossible. The PID exceeds `pid_max` 4194304, making this a missing-target control." Also record that the retained `list-frida-processes.json` is a host-wide inventory of 149 undeclared process names and PIDs, and must not be re-captured or extended.
5. Cutter: either record `cutter-command-missing`'s producer argv and `env_overrides` beside it, or mark it as hand-run with env unrecorded.
6. Placement:
   - pcap/packet (4 rows): re-place as `adjacent`. Neither MINT nor PROVINCE Frontier names this ground; counter-neutral.
   - Cutter (2 rows): keep `frontier-blocked` only with a reason citing the Alternate-providers bullet as an analogy [INFERENCE]; otherwise re-place as `adjacent`.
7. Preamble `PROVINCE.md:176`: replace "revenger's contested runtime province" with the per-family clause contact from K3.

### 3. C1 ceiling under this contract

`debug-with-rizin` is structurally unholdable in this wave. `debug-with-gdb` is holdable only with a caller-enforced no-inferior command allowlist (e.g. `show version`, or `file <elf>` followed by static `info functions`; never `run`, `start*`, `attach`, `target`, or `shell`/`!`) and a TTY that validates (UNKNOWN). Report `k` exactly as measured.

## Risks

- Re-placing rows as `adjacent` could read as a lane conceding ground. Neither choice awards ownership; L1 may keep `frontier-blocked` if it adds an explicit MINT-anchor note instead.
- Rewording the r22 knowledge entry must not touch its S051–S053 citations, evidence id, or recheck line, which C1 counting depends on. Prior knowledge files stay byte-identical; this entry post-dates the baseline.
- K4 stays unknown. Do not assert that revenger cannot reach the T1/T2 verbs.
- Any new pcap or Cutter control probe would be new evidence. It needs the wave's REA-via-npx@6.5.0 path and must not use real TShark, Cutter, or adb clients. None was run here.

## Verification for L1 after integration (not run here)

- `python3 -I -B .ufo/waves/round-22/tools/count-c2.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV>` should give `accounted_count 14/14`, `mismatched []`, `foreign_rows []`, exit 0. Placement and reason edits must leave this unchanged.
- `python3 -I -B .ufo/waves/round-22/tools/count-c1.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV>`: `t1_exercised_count` unchanged by the wording edit.
- `git diff 7787fea4d6fd718726de92ed20759d11ce7b8b48 <REV> -- corpus/knowledge ':!corpus/knowledge/2026-10-21-r22-*'` should be empty.
- `git -C /home/vgpnk/Projects/shokunin/revenger-shokunin status --short` should be unchanged. Revenger is never written.

## Commands run (all read-only)

| command | exit | key stdout |
|---|---|---|
| `git -C kaidoku rev-parse HEAD`; `git log --oneline 7787fea..HEAD` | 0 | `2ee3d9f`; 2 commits |
| `git -C revenger rev-parse HEAD`; `git log -1` | 0 | `cf02419`, 2026-10-19 |
| `jq` over `evidence/c2/*.run.json` and `*.json` (argv, `env_overrides`, ok, `error.code`, `meta`) | 0 | table above |
| `rg -c/-l -i[-w] …` over revenger LOG.md and corpus | 0 | O2/O3/O6 counts above |
| `rg -l -F 'rea-agents-6.4.0.tgz' ~/.npm/_cacache/index-v5` | 0 | no match |
| `rg -o 'REA_[A-Z_]+' dist/{flutter,pcap,frida,cutter,signals,gdb,rizin}` | 0 | key list above |
| `command -v tshark capinfos adb frida rizin gdb sigrok-cli cutter`; `cat /proc/sys/kernel/pid_max` | 0 | host list above; 4194304 |
| `timeout 60 find … libapp.so/libflutter.so/*.apk` | 124 (timeout at 60.00 s wall) | 2 Godot APKs; partial |
| `sha256sum` + `unzip -l` on `android_release.apk` | 0 / 0 | `6d1bb2cf…`; 8 `lib/` `.so` members |
| `unzip -l … \| rg -c 'libapp\.so\|libflutter\.so'` | 1 | no match (0) |

No blocker. Tool installs: none.
