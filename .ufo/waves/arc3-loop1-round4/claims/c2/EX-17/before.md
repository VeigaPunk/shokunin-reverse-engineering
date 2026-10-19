# EX-17 — before-state: stale-item census + baselines at HEAD (chain c2, arc3-loop1-round4)

Seat EX-17, chain c2, role executor. Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
HEAD `015e1bab914713568f339fd53999bc180459cc40` (unchanged through this seat's work; no git
mutations, no custody writes). Date 2026-10-19. Lane: devin (`devin/deepseek-v4-1-flash-max`)
— the declared fallback dispatch (`claims-frozen.md:11-15`), not a lane signal. Scratch
`/var/tmp/ex17` (disk-backed `TMPDIR` on every probe; `/tmp` never used). The seat writes only
its report and this artifact tree; `PROVINCE.md` was never opened for writing.

Line numbers below are valid **only at the pinned revision** — every item also carries the
sha256 of its exact byte range, and the whole file is pinned at `d075a3c6…` / 162 lines
(worktree byte-identical to `git show HEAD:PROVINCE.md`; both hashes re-derived below).

## 1. Baselines at HEAD (the claim's falsifiable before-side)

**Command A** (recipe `SCORECARD.md` §Measurement recipes, run from Git objects at `015e1ba`;
capture `evidence/command-a-head.json`, sha256 `dad373fb…`):

```json
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [],
 "revision": "015e1ba", "rule_blocks": 14}
```

**Census gate** `.ufo/gates/c1-census-v10.py` (sha256 `d0772ce8…`; capture
`evidence/census-head.txt`, sha256 `6a87844b…`): exit 0 —
`VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, scope-errors `[]`,
unreadable `[]`, G2 floor `PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3`. Note the gate grades
version/pin/pointer loci only; it is **blind** to the Frontier prose this chain repairs
(VZ-2 arm A1, re-derived below in §5).

**Citation-drift probe** `.ufo/gates/citation-drift/citation-drift-probe.py` (sha256
`e2665074…`; capture `evidence/probe-head.txt`, sha256 `5c9142c2…`): exit 0 —
`CITATION_DRIFT_VERDICT: reported findings=0 exit=0`; pointer-table sha256 `1b3ab955…`
equals its own pin.

**Pinned identities at HEAD** (all re-derived first-hand this run):

| object | sha256 |
|---|---|
| `PROVINCE.md` (worktree and `git show HEAD:PROVINCE.md` — identical) | `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad` |
| `SKILL.md` | `5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f` |
| `SCORECARD.md` | `21042196b51dae57182c2d25b014f8928a4360139bbecd72127dac1031c18ef7` |
| `corpus/README.md` | `a451ad1664cda0cb87f3a76e974de818a1e401387bad6251b98cd6b0df8ede3a` |
| census instrument | `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` |
| pointer table / expected | `1b3ab955…` / `9df0452c…` |
| `corpus/knowledge/` file count | **83** (no vyper entry; `ls corpus/knowledge/ | grep -i vyper` → no match) |

## 2. The stale-item census

Every Frontier bullet (both sections), the surface summary, the drift-prone block, and the
Core host-fallback row were checked against admitted corpus state (`corpus/knowledge/*.md`,
`corpus/README.md`) and against live host re-derivations. **16 items; 7 carry at least one
falsified clause** (the primary stale set below); 2 adjudicated NO-CHANGE with cause (S5
below; F2 under the alternative reading); the remainder current.

### 2.1 Stale items — exact current text (verbatim) + sha256

Verbatim bytes of each item (extracted from `PROVINCE.md` at HEAD, LF-joined, trailing
newline included; full capture `evidence/stale-items-verbatim.txt`, sha256 `f5723eb2…`):

**F1b — `PROVINCE.md:82-83` — sha256 `54d0a7c6043bb2aab88b8a56f601026be349321c23a90058cd8b42d110315182`**

```
- **PE subtypes** — x86-64 AND ARM64 both held (r3-08: cli-arm64.exe, 136
  procedures via Ghidra). Reserve: 91MB Godot ARM64 template, ARM64X hybrids.
```

Falsified clause: `Reserve: 91MB Godot ARM64 template`. The 91.6 MB Godot ARM64 export
template is the r7 held run's subject (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md`:
91,662,336 B, sha256 `7a2ccd68…`, 75,218 procedures, exit 0) with the r8 no-disable natural
control (OOM at 9G in 4m42.945 s) recorded as an append-only erratum in the same entry;
`corpus/README.md` frontier list reads `>90MB PE scale — CLOSED, not frontier`. It is no
longer an un-run reserve. The `ARM64X hybrids` half stays correct (no corpus entry runs one).

**F2 — `PROVINCE.md:84-86` — sha256 `871bce3288c8c31800ecbf2b321eb3bd10ce0316e755405d660ee7ad09578d6e`**

```
- **Recorded crashes >32 MiB** — mechanism held (Core); all 3 organic cores
  exceed the cap (waybar 434MB). Needs a cap-raising knob or partial-core
  intake — neither exists. Retention decays oldest-first.
```

Falsified clauses, first-hand this run:
- `all 3 organic cores exceed the cap` — an organic core sits **under** the 32 MiB cap and
  inspects: `coredumpctl list` PID 1857 (`/chrome_crashpad_handler`, SIGBUS, Grok Bot
  Electron 42.1.0 AppImage crash, 2026-10-19 00:35:13) reads COREFILE `present`, 48.5K;
  `coredumpctl dump 1857` → **17,608,704 B** (raw ELF), and
  `npx -y rea-agents@6.4.0 inspect-recorded-crash <raw>` → **exit 0**,
  `ev_8051329d2e8172cbd460153bbf92d1c4c3bc77a6005c55888bdabdc1ea2017b8`,
  `format: elf-core`, `x86_64-little-endian`, 53 segments / 3 threads (capture
  `evidence/crashpad-probe.json`, sha256 `841441e1…`).
- `(waybar 434MB)` — no waybar core file exists any more: `coredumpctl list` shows two
  waybar entries, both COREFILE `missing`; localsearch has 0 entries. Retention decayed the
  exemplar — which the bullet's own last clause (`Retention decays oldest-first`) predicts,
  so that clause is *confirmed*, not stale.
- The headline class still holds and was re-confirmed on an organic oversize core: git PID
  1214442 (2026-10-19 09:05:41), dump → 36,360,192 B → `out_of_range` /
  "Selected artifact exceeds 33554432 bytes", exit 1 (capture
  `evidence/git-oversize-probe.json`, sha256 `3c4c3d24…`).

Adjudication note: this row is the wave's one *contested* item. VZ-2's census adjudicated it
(`adjudicated`, "the class claim holds; the named exemplar decayed"); EX-13 repaired it
(`claims/c2/EX-13/province-frontier-recorded-crashes-organic.patch.md`). Both dispositions
are defensible under the frozen claim ("repaired same-line **or** adjudicated NO-CHANGE with
cause"); the falsified bytes are recorded here either way.

**F3 — `PROVINCE.md:87-88` — sha256 `b5007d085a8d99a23f26bcb9331b5fc49e362423df4323c408e1733f5c294312`**

```
- **Alternate providers** — IDA (`REA_IDA_MCP_CONFIG` unset), Hopper (absent),
  JEB (unprobed). Engine installs are operator-owned.
```

Falsified clause: `JEB (unprobed)`. The JEB provider was probed and its gate recorded as a
typed refusal since r2: `corpus/knowledge/2026-10-13-r2-provider-capability-matrix.md` run
log (`inspect-jeb-client` → `capability_unavailable` / `unsupported_provider`, live probe
`fetch failed`), `corpus/knowledge/2026-10-13-r2-frontier-prereqs.md` (JEB provider:
"Fully absent… operator-owned"), and `corpus/knowledge/2026-10-14-r12-02-queue-b-ledger.md`
(L201 re-verify: key UNSET, no install, :8425 closed). Re-derived first-hand this run:
`REA_JEB_MCP_URL` unset, `ss -ltn | grep 8425` empty, and
`npx -y rea-agents@6.7.0 inspect-jeb-client --format json` → exit 1,
`{"code":"capability_unavailable","category":"unsupported_provider", … "details":{"provider_id":"jeb","operation":"inspect_jeb_client","reason":"fetch failed"}}`
(capture `evidence/jeb-probe-6.7.0.json`, sha256 `fbb74657…`). The IDA and Hopper halves
re-checked current (`REA_IDA_MCP_CONFIG` unset; `/opt/hopper/bin/Hopper` absent).

**F5b — `PROVINCE.md:91-93` — sha256 `643ab1c40ef9ff5b4d16466d3de80082effffa0e0022dd9b924165e2b92c03ed`**

```
- **EVM bytecode (extended)** — selectors held on synthetic dispatcher
  (Core, r3-07); real solc/vyper-compiled bytecode untested; selectors stay
  bare hashes (no signature DB → no name resolution).
```

Falsified clause: `real solc/vyper-compiled bytecode untested` — the **solc** half is
falsified by two admitted entries: `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`
(real solc 0.8.37 runtime carriers, K/K: 5/5, 6/6, 11/11) and
`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md` (optimizer-enabled +
non-ERC-20 shapes: 13/13, 11/11, 8/8, 5/5); `corpus/README.md` EVM row reads "held … and
from real solc-0.8.37-compiled runtime carriers (arc3-r1)". The **vyper** half is still
true **against admitted corpus state** at HEAD: `corpus/knowledge/` is 83 files with no
vyper entry. (C1's vyper leg has succeeded in the wave tree — vyper 0.4.3, 15/15 — but the
entry is patch text, not admitted; recorded in EX-14 §5.3 and VZ-2 A6.) The trailing
`selectors stay bare hashes` clause is current.

**R2 — `PROVINCE.md:139-144` — sha256 `1fd6b1a3498c3b0d114864c3322f7abf75a44435ddfedcb8986e0a1a965060b3`**

```
- **>90 MB PE scale wall** — 91.6 MB Godot ARM64 PE hits REA's ~900s internal
  session deadline (`provider_timeout`, GhidraClient.js:607), still progressing
  at kill (r4-12) [r5-audit C1: r4-12 cite added]. Not OOM (RSS ~2.36GB vs
  -Xmx2G headroom exists). Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` to
  ~3.6Ms + `GHIDRA_HEADLESS_MAXMEM=6-8G` on an idle host, or bisect with a
  2-5MB PE.
```

Stale as written: the wall fell (r7 mitigated hold, r8 natural control) and the bullet's
`Next:` remediation list is spent. Evidence: `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md`
(user service `arc2-r7-pe`, exit 0, wall 1424.663 s vs the raised 7200 s deadline unused,
75,218 procedures, `ev_a4aa9b0d…`, analyzer-disable preset; r8 control OOM-killed at 9G) and
`corpus/README.md` frontier list (`>90MB PE scale — CLOSED, not frontier …`). The one
genuinely open residual — rerun id-stability — is named in the r7 entry's erratum, not in
this bullet's remediation.

**X1 — `PROVINCE.md:157-160` — sha256 `2b683cd35ab0ae3f41cfe3954bc6b4a42004013f0fe08926e180904ca6ce70aa`**

```
- **Cross-version residuals** — `compare-application-versions` still
  probe-refused since r2; multi-version pacman pairs beyond expac unexercised
  [r5-audit C1: merged from the pruned Frontier bullet — its
  `compare_javascript_export_shapes` item is now held (Core, r4-09)].
```

Falsified clause: `` `compare-application-versions` still probe-refused since r2 ``. The verb
is exercised and admitted: `corpus/knowledge/2026-10-14-r12-02-queue-b-ledger.md` (row L203
"WAS TRULY-OPEN, NOW EXERCISED"; run-log rows 4 and 9 — JS `ev_7a8d0ec4…` and managed
`ev_b5fc998f…`, both byte-identical re-runs) and
`corpus/knowledge/2026-10-14-r14-01-queue-b-residual.md` Candidate 1 ("L203 is now wholly
discharged: all three named input classes … exercised with live successes"). The second
clause (`multi-version pacman pairs beyond expac unexercised`) stands — the admitted pacman
work covers expac, bwrap and op; no entry claims pairs beyond those.

**C1 — `PROVINCE.md:62` (Core row) — sha256 `8b51268f490be75b767fdcd7658e65b80802c488001429178d7f4db63d8fe92b`**

```
| Host fallback readers | `file`, `readelf`, `objdump`, `llvm-readobj`, `nm`, `strings`, `unzip`, `tar`, `gdb`, `eu-stack`, `coredumpctl`, `pacman`, `zstd`, `gpg`, `python3`, node/npx | `command -v <tool>` | absent: `7z`, `cabextract`, `xxd`, radare2/rizin, strace/ltrace, upx, pacman-contrib |
```

Falsified: five of the claimed-absent tools are **present**. First-hand sweep this run
(capture `evidence/tool-sweep.txt`, sha256 `8f9e7b1c…`):
`7z /usr/bin/7z`, `xxd /usr/bin/xxd`, `radare2 /usr/bin/radare2`, `r2 /usr/bin/r2`,
`strace /usr/bin/strace`, `upx /usr/bin/upx`; `pacman -Qo` attributes them to
`7zip 26.03-1`, `tinyxxd 1.3.16-1`, `radare2 6.2.0-1`, `strace 7.0-1`, `upx 5.2.0-1`.
Genuinely absent: `cabextract`, `rizin`, `ltrace`, `paccheck`/`pactree`/`pacfiles`
(pacman-contrib). Admitted corpus already contradicts the row under a same-day reading:
`corpus/knowledge/2026-10-13-r4u-03-unblob-extract.md` records `7z` present.
Adjudication note: this row sits inside DATED scope `("PROVINCE.md", 45, 62)`; a parent may
alternatively adjudicate NO-CHANGE (dated record) with this cause — EX-13's patch text
carries the same two-disposition note.

### 2.2 Adjudicated NO-CHANGE (with cause)

**S5 — `PROVINCE.md:18` Kimi pointer `~/.kimi-code/config.toml:3298`** (inside the
drift-prone block, sha256 `3de1bd43…` for :15-26). The cited line now holds
`max_context_size = 1048576`; the live pin sits at `:3546` (`[mcp_servers.rea]` stanza at
`:3544`, `args = [ "-y", "rea-agents@6.7.0", "mcp" ]`). The pointer is **receipt-stamped by
design** ("at the 17:55:49Z receipt"; the same sentence already labels `:2940` and `:3227`
historical) and the pinned value `6.7.0` matches the live anchor. Disposition: NO-CHANGE —
a config.toml line number is unpinnable (operator-owned churn, six+ states recorded since
arc2), and the sentence's own historical markers already cover it. The census gate never
evaluates this pointer (`ptr_check` is only reached for clauses carrying no pin/bare
version — VZ-2 A3, re-derived: the `:18` clause carries the pin, so the pointer is
unreached; direct call returns `stale`). Named instrument blind spot, not a PROVINCE defect.

**F2** — see §2.1: if the parent prefers the class-claim reading, F2 is adjudicated
NO-CHANGE (exemplar decay) rather than repaired.

### 2.3 Checked and current (no change)

| item | lines | evidence pointer |
|---|---|---|
| B2 first clause (x86-64 AND ARM64 held, 136 procs) | :82-83 | `corpus/knowledge/2026-10-13-r3-pe-arm64.md` |
| B4 IDA/Hopper halves | :87-88 | env unset; `/opt/hopper/bin/Hopper` absent (this run) |
| B5 macOS-only surfaces | :89-90 | `corpus/knowledge/2026-10-13-r2-provider-capability-matrix.md` (8 available / 10 `unsupported_host`) |
| B6 first + last clauses (synthetic dispatcher held; bare hashes) | :91-93 | r3-07 entry; no corpus signature-DB claim |
| B7 RISC-V (10,766 functions @900 s cap) | :135-138 | `corpus/knowledge/2026-10-13-r5-01-riscv-bypass.md` |
| B9 `.jsc` mapping frontier | :145-146 | `corpus/knowledge/2026-10-13-r4-07-jsc-bytecode.md` (Ignition disasm held; jscd refuses V8 14.8) |
| B10 sasquatch | :147-148 | `corpus/knowledge/2026-10-13-r4u-03-unblob-extract.md`; `command -v sasquatch` → absent |
| B11 adb surface (22/24 need device; bugreport bound) | :149-150 | `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md` (bound `BUGREPORT_TIMEOUT_MS = 600_000` ≈ the bullet's ~10min) |
| B12 asar scale | :151-156 | `corpus/knowledge/2026-10-13-r4-06-1password-asar.md` (40.7 MB + 188 MB core), `…-r4-05-signal-asar.md` (1,866 entries), `…-r4-14-libsignal.md` (neon) |
| X2 second clause (pacman pairs beyond expac) | :157-160 | no corpus entry claims one |
| B14 operator-gated footer | :161-162 | IDA/Hopper/JEB all absent (this run) |
| S1-S4, S6-S7 (surface summary + drift-prone pins/digests/skill/Ghidra) | :8-13, :15-26 | live re-reads: devin:7, omp:8 = `rea-agents@6.5.0`; kimi `:3546` = `6.7.0`; caches 6.7.0/6.5.0/6.4.0 at `a1722018f28f9df2`/`ad9a3fdbcad992c6`/`dea9475797100b20`; **live `doctor` re-derivations this run**: 6.7.0 → 153/207/6, `tools_sha256 af39310c…`; 6.5.0 → 153/207/6, `805433f1…`; 6.4.0 → 127/170/6, `25802f6d…` — all three match the PROVINCE drift-prone block (captures `evidence/doctor-6.{7,5,4}.0.json`); installed skill `c8639823…`, v42; `application.version=12.1.4` at `Ghidra/application.properties:17`; `java -version` → 21.0.12.1 |

## 3. First-hand re-derivations performed by this seat

1. Command A at `015e1ba` from Git objects (§1).
2. Census gate + citation-drift probe at HEAD (§1).
3. Worktree/HEAD blob byte-identity of `PROVINCE.md` (§1).
4. Live pins: `sed` of devin `mcp_config.json:7`, omp `mcp.json:8`, kimi `config.toml:3298`
   and `:3544-3546`; `grep -n rea-agents@ ~/.kimi-code/config.toml` → `:3546`.
5. Cache versions: `package.json` version fields for the three `_npx` hashes.
6. Skill: `sha256sum ~/.agents/skills/reverse-engineer-anything/SKILL.md` → `c8639823…`,
   22,513 B; front-matter `version: "42"`.
7. Tool sweep + `pacman -Qo` (§2.1 C1); `command -v sasquatch` → absent.
8. JEB live probe at 6.7.0 (§2.1 F3); env keys `REA_IDA_MCP_CONFIG`, `HOPPER_LAUNCHER_PATH`,
   `REA_JEB_MCP_URL` unset; `ss -ltn` :8425 closed.
9. Crash surface: `coredumpctl list` (1,538 rows; 89 COREFILE `present`), waybar rows
   `missing`, localsearch 0, crashpad 7 entries (1 `present`); dump+probe of PID 1857
   (§2.1 F2); dump+probe of the oversize git core (same item).
10. Corpus count 83 and no vyper entry; `corpus/README.md` EVM row + frontier CLOSED line
    read at HEAD.
11. Live `doctor` catalog re-derivations at all three pins (6.7.0 / 6.5.0 / 6.4.0) — the
    drift-prone block's three `tools_sha256` digests all reproduce (captures
    `evidence/doctor-6.{7,5,4}.0.json`).

## 4. Cross-seat reconciliation (as of write time)

- VZ-2's census (`claims/c2/VZ-2/evidence/census-before.txt`, 26 rows): `stale=6` —
  `F1b, F3, F5b, X1, C1, R2`; `adjudicated=2` (F2, S5); `current=18`. My §2 reproduces all
  six as stale and both adjudications; my census additionally records F2's falsified
  inventory clauses as measured (VZ-2 adjudicated the same bytes — no contradiction, a
  unit choice, both recorded).
- EX-13's seven patch texts (`claims/c2/EX-13/*.patch.md`) cover exactly the seven items in
  §2.1 — including the F2 repair and the C1 Core-row repair with its two-disposition note.
  My verbatim texts are the byte-level input those patches' search blocks must match; the
  sha256s in §2.1 are the pinned search-side identities.
- EX-14's measurements (line-neutrality, needle-freedom, UNDECLARED 72-118, DATED marker at
  :119) are consistent with the item boundaries recorded here; nothing in this artifact
  conflicts with `claims/c2/verdict.md` (which named F3 and C1 as the two then-unpatched
  rows — EX-13 has since authored both).

## 5. Blind-spot confirmations relevant to this before-state

- The census gate reads the same PASS before and after any Frontier prose repair
  (Frontier 72-118 and post-unlock 132-162 are UNDECLARED; the items carry no needle) —
  VZ-2 arm A1, consistent with the gate output in §1.
- `ptr_check` never evaluates `config.toml:3298` because the `:18` clause carries a pin
  (S5, §2.2).
- The stale set is measured against **admitted corpus state**; C1's vyper leg exists only
  in the wave tree (F5b note, §2.1).

## 6. Evidence files (this seat's write scope)

All under `.ufo/waves/arc3-loop1-round4/claims/c2/EX-17/evidence/`; `MANIFEST.sha256`
lists every file and its sha256 (`sha256sum -c` clean):

| file | sha256 |
|---|---|
| `command-a-head.json` | `dad373fb…` |
| `census-head.txt` | `6a87844b…` |
| `probe-head.txt` | `5c9142c2…` |
| `stale-items-verbatim.txt` (7 items, verbatim + per-item sha256) | `f5723eb2…` |
| `jeb-probe-6.7.0.json` | `fbb74657…` |
| `crashpad-probe.json` | `841441e1…` |
| `git-oversize-probe.json` | `3c4c3d24…` |
| `tool-sweep.txt` | `8f9e7b1c…` |
| `doctor-6.7.0.json` (live catalog re-derivation) | `af39310c…` digest inside; file hash in MANIFEST |
| `doctor-6.5.0.json` | idem (`805433f1…`) |
| `doctor-6.4.0.json` | idem (`25802f6d…`) |

This file's own identity is re-derived after the final write and recorded out-of-band in the
seat report (a self-hash inside the file would invalidate itself on write).
