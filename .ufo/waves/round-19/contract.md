# kaidoku round 19 — shared seat contract (L1-authored)

LANE = /home/vgpnk/Projects/shokunin/kaidoku-shokunin. W19 = LANE/.ufo/waves/round-19.
Baseline B = 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 (refs/heads/main at dispatch). Claims: W19/claims.json.
Previous outside check: LANE/corpus/lessons/round-18-verifier-spotcheck.md (routed defects at :191-199;
carried items at :201-206). Round-18 lesson: LANE/corpus/lessons/round-18.md (Open list :86-92).

## Writers: one integration owner (the L1), separate worktrees

- Every seat that changes or creates a lane file works in its OWN clone:
  `git clone -q --no-hardlinks LANE /tmp/kr19-<SeatName>` then
  `git -C /tmp/kr19-<SeatName> checkout -q --detach 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`
  (record `git -C <clone> rev-parse HEAD` as your observed base). Edit and test only there.
- Deliver as a patch: `cd /tmp/kr19-<SeatName> && git add -A && git diff --cached --binary 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 > LANE/.ufo/waves/round-19/<wave>/patches/<SeatName>.patch`
  (mkdir -p the patches dir). Never include `__pycache__`, `.pyc`, or files outside your assignment in the patch.
  Then paste `git -C <clone> diff --cached --stat B` in your report.
- Never write the LANE working tree except your report and your patch file. Never run git writes or any `jj`
  command in LANE. Read-only git in LANE (log/show/diff/ls-files/rev-parse/cat-file/grep/merge-base) is fine;
  use `refs/heads/main` or the full baseline hash, never bare `HEAD`, `@`, or `HEAD~N`.
- Never write the fleet repo /home/vgpnk/Projects/shokunin (except via your own LANE report path), sibling
  lanes, `.ufo/state/`, MANIFEST.json, client configs (`~/.omp/agent/*`, `~/.config/devin/*`,
  `~/.kimi-code/*`), or REA/Ghidra installs.

## Tool conventions (match round 18)

- Python tools: `#!/usr/bin/env python3`, stdlib only, run as `python3 -I -B`, `--selftest` prints
  `SELFTEST: CLEAN cases=N` (exit 0) or `SELFTEST: FAILED ... cases=N fails=M` (exit 1); fixtures under
  `tempfile.mkdtemp()` only, removed after. Revision-scoped checks read Git objects (`git show REV:path`,
  `git cat-file`) with `--no-optional-locks`, never the working tree, unless the tool's contract says live.
- Exit codes: 0 clean, 1 findings under `--strict` (or red), 2 unusable input/refusal.
- Every count a tool prints carries its rule; every refusal names its cause.

## REA / Ghidra

- REA CLI only: `npx -y rea-agents@6.5.0 <command>` (the OMP rea MCP entry is disabled by operator
  authorization; never use xd://mcp__rea_* devices). Round-19 C3 measured runs are the L1's: seats never run
  REA `analyze`/`search`/`decompile` or Ghidra `analyzeHeadless` on the C3 carriers before the L1 freezes
  predictions. Read-only REA catalog/doctor/version calls are fine for C2 seats.
- Never execute a carrier binary. Ghidra 12.1.4 at /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC (source:
  Ghidra/Features/Base/lib/Base-src.zip; Go type data: Ghidra/Features/Base/data/typeinfo/golang).
- C3 carriers: /home/vgpnk/.local/opt/go-1.25.0/bin/{go,gofmt} and
  /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/{asm,cgo,compile,cover,link,preprofile,vet}.
  Emulator prescan (L1, before dispatch): W19/evidence/prescan/kr19-sm-<name>.json — vet H1 invalid_index,
  link unparseable (no Go build info), the other seven predicted silent.

## Reports

Every `Report:` trailer path is relative to LANE — write it at LANE/<that path>. Reports: observation vs
inference labelled; every command pasted with its exit; path:line anchors; never fabricate. A dead or partial
result is reported as such.
