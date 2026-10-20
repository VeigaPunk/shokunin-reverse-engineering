# Round 19 — PROVINCE / SKILL / README consistency

**Scope:** requested baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`; read-only comparison of `PROVINCE.md`, `SKILL.md`, root `README.md`, and `corpus/README.md`. Axes: calibration, freshness, depth.

## Findings

**Observation — no unqualified, substantive contradiction among the named documentation on Ghidra, JDK, or provider scope.** The statements agree when their explicit capture dates and historical labels are honored. Root `README.md:6` only says native ELF/PE “via Ghidra”; it names no REA version, Ghidra version, JDK, or provider inventory, so it cannot conflict on those specifics.

**Observation — package-version/history pair:** `PROVINCE.md:8-12,15-25,44-47` and `SKILL.md:10-20` agree on Devin/OMP 6.5.0 and Kimi 6.7.0 for the stated 2026-10-18 inventory; both identify 6.4.0 as historical. The SKILL’s `6.4.0`, 170 MCP tools, and 127 CLI commands at `SKILL.md:11-13` are explicitly dated 2026-10-13 and labeled historical, consistent with `PROVINCE.md:12,21-25,45` (6.4.0 historical; 127 commands) and the dated corpus entries at `corpus/README.md:16-17,74-78`. This is not a version contradiction.

**Observation — round-claim freshness conflict (not a contradiction between the docs):** the current-version statements in `PROVINCE.md:8-10,15-18,44-45` and `SKILL.md:18-20` still put Devin/OMP at 6.5.0. Round-19 `claims.json:19-20` declares that the client config pins are now 6.7.0 for Devin and OMP and predicts two stated-vs-live mismatches at this baseline. Thus PROVINCE and SKILL are mutually consistent but stale against the round’s declared C2 target. The claim is not an independent live-config observation from this assignment; no client config or REA probe was read.

**Observation — apparent CLI/skill-version mismatch is time-scoped:** `corpus/README.md:16-17` shows 127 CLI commands and an REA skill contract v37, while `PROVINCE.md:19-25,45` distinguishes current 6.5/6.7 (153 commands) and installed shared skill v42 from historical 6.4.0 (127 commands; 6.4 expects v37). The corpus rows point to 2026-10-13 evidence (`corpus/README.md:15-18,74-81`); they do not establish the current REA package/skill identity. Because the row’s “held” label is easy to read as present-tense, this is a freshness/temporal-label ambiguity, not evidence of mutually exclusive facts. The installed shared v42 skill and the historical v37 REA skill contract are distinct, explicitly qualified identities (`PROVINCE.md:24-25`).

**Observation — Ghidra/JDK/provider pairs agree:** `PROVINCE.md:3-4,12,25,46-48` identifies Ghidra 12.1.4 and Java 21.0.12.1 / JDK 21, with native ELF and PE paths through Ghidra. `SKILL.md:3,12-14,48` names Ghidra 12.1.4/JDK 21 and the Ghidra PE loader; `README.md:6` is the compatible general description; `corpus/README.md:4-5,18,21` gives Ghidra 12.1.4, JDK 21.0.12.1, and PE via Ghidra. “JDK 21” is a major-version description consistent with the more specific 21.0.12.1 runtime.

**Observation — provider-availability pair agrees:** `PROVINCE.md:28-30,46,64-70,87-88` distinguishes provider candidates/availability from held capability, names Ghidra as configured/available, and leaves IDA unset, Hopper absent, and JEB unprobed. `SKILL.md:24-26,65-73` makes the same distinction and treats IDA/Hopper/JEB as absent/frontier. `corpus/README.md:15,42,45` describes the dated inventory as Ghidra-only and records the older provider/capability matrix; it does not claim IDA/Hopper/JEB were available. No provider contradiction found.

## One bounded move

**Proposed move (freshness + calibration, preserving depth):** make the per-client REA pin/cached-catalog state in PROVINCE the single current-state statement; once C2 has captured and verified its receipt, update that statement and replace SKILL’s duplicated current pin values with a reference to it. Preserve 6.4.0/127/v37 material as explicitly dated historical evidence, and label the 2026-10-13 corpus coverage rows as a historical snapshot rather than current inventory. Do not change Ghidra/JDK claims as part of this pin-only move. This removes duplicated mutable claims while retaining the detailed historical evidence and provider lessons.

**Risks:** `claims.json` is a declared claim, not proof of live config. Do not simply replace 6.5.0 with 6.7.0: refresh the custody evidence and associated package/catalog identities and doctor status together. A careless cleanup could erase valid 6.4.0 historical evidence or conflate the bundled REA skill contract with the installed shared skill.

## Verification and command results

**Observation:** `git diff --quiet` against the requested baseline returned 0 for all four documentation paths, so the read working-tree text used for line citations matches those baseline blobs. No REA/Ghidra analysis, live-config probe, build, or test was run.

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0
exit: 0
stdout: 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --quiet 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 -- PROVINCE.md SKILL.md README.md corpus/README.md; rc=$?; printf 'git diff --quiet exit=%s\n' "$rc"; exit "$rc"
exit: 0
stdout: git diff --quiet exit=0
```

Repository reads/searches used the read and grep tools; no additional shell commands or tool installs were used.