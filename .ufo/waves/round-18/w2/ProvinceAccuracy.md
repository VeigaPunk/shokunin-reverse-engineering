BROKEN

# ProvinceAccuracy — round 18, wave 2 (connector, author-side advisory)

The lane's own census gate fails three CURRENT PROVINCE blocks against live state. The cause is not round-18
lane work: all three client configs now pin `rea-agents@6.7.0`, and the Devin and OMP config files changed at
2026-10-20 13:35:56 -03, two minutes before `b2aad08` was committed. Separately, the r18 Swiss-map ground is
missing from Core, and `PROVINCE.md:26` carries a broken `HEAD:` self-citation that no round-18 jj check can
see. No Frontier line needs to change. Below is one line-neutral patch, verified in a sandbox.

Scope: REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, baseline `9011581d84527ba34c675f9cf912e54d2e72d470`.
`PROVINCE.md` is byte-identical between them (C1). All `path:line` anchors are at REV (`git show REV:path`)
unless marked as live host state. Read-only in the lane. Scratch work ran in a mkdtemp clone with its origin
removed. No REA, Ghidra or carrier was executed. Installs: none.

## Answers

- **Core: yes, change it.** Row `:44` and the CURRENT lines `:8-12`, `:15-17`, `:21-23` and `:25` are false
  against live state (F1, F2). Rows `:48` and `:52` lack the r18 Swiss limit (F3).
- **Frontier: no.** No bullet is falsified: census `frontier_errors: []` at REV. Adding any bullet makes the
  census fail unless its FRONTIER register is re-keyed in the same commit (F5, observed).
- **jj tooling: no Core/Frontier row.** PROVINCE has 0 gate/instrument rows (C16). But `:26` holds the only
  `HEAD:`-keyed pin in the file, and it is broken (F4).

## Findings

**F1 — Devin/OMP pins drifted to 6.7.0 (observation).**
- Live state: `mcp_config.json:7`, `mcp.json:8` and `config.toml:4126` all read `rea-agents@6.7.0` (C2).
- Devin and OMP config mtime: 2026-10-20 13:35:56 -03 (C3). The r18 carrier pass ended at 13:32:10 -03
  (`.ufo/waves/round-18/runs/run-log.txt`, tail). `b2aad08` was committed at 13:38:07 -03 (C4).
- PROVINCE still says Devin/OMP 6.5.0 at `PROVINCE.md:8-10`, `:15-17` and `:44`.
- `.ufo/gates/c1-census-v10.py` reads the live anchors `{devin: 6.7.0, omp: 6.7.0, kimi: 6.7.0}` and returns
  exit 1 FAIL (C5). Stale blocks: `PROVINCE.md` 8-13, 15-26 and 44-44, plus `SKILL.md` 18-20. Undeclared:
  `SCORECARD.md` 2380-2382 and `SKILL.md` 511-519. The output at `9011581` is identical (C5), so round 18
  added nothing to this failure.
- [INFERENCE] The config edit was made by someone outside the lane (fleet or operator). The C3 data is
  unaffected: all 15 r18 receipts record `steps.analyze.argv[2] = rea-agents@6.5.0` with exit 0 (C6).

**F2 — the 6.4.0 npx cache is gone (observation).** `/home/vgpnk/.npm/_npx/dea9475797100b20` does not exist
(C7). The 6.5.0 and 6.7.0 caches remain. This contradicts three places:
- `PROVINCE.md:12` ("both versions have separate npx cache installs");
- `:21-23` (the 6.4.0 cache identity);
- `:25` (6.4.0 "expects v37").

Once the F1 lines are fixed, the census reports these as UNRESOLVED (C12a). Before that, STALE outranks
UNRESOLVED in `classify` (`c1-census-v10.py:525-625`), so they were hidden.

**F2b — the census dropped out of verification (observation).**
- Last run: round-14 verification, `label: census`, exit 0, anchors devin/omp 6.5.0 (C8).
- Rounds 15-17: 0 `c1-census` mentions in `verification.json`.
- Round 18: 0 in `measure.py`/`verify.py` (C8).
- [INFERENCE] This is why neither the r17 undeclared records nor today's pin drift was caught.

**F3 — Swiss ground is missing from Core; REA's own result is silent (observation).**
- `PROVINCE.md` has 0 matches for `swiss|OldMapType|GolangSymbolAnalyzer|r18` (C9). The README Go row
  (`corpus/README.md:35`) and SKILL (`SKILL.md:528`, `:548-566`) do carry r18. LOG's landed list
  (`LOG.md:2162-2167`) omits PROVINCE.
- New synthesis, not stated in the entry or SKILL: on all 15 labels, `analyze.json` contains 0
  `Go analysis failure|Invalid index|read past EOF|GolangSymbolAnalyzer` hits (C10). Meanwhile:
  - the three failing carriers (calib-aether, s1246-swiss-nethttp, real-kimi-webbridge) each show 2 hits in
    their bound `ghidra.log`;
  - their `analyze.stderr` has 0 hits and `steps.analyze.exit` is 0;
  - the failing s1246-swiss-nethttp and its non-failing noswiss sibling have identical `analyze.json` key
    paths and identical `limitations`.
- So the probe in Core row `:48` ("`rea analyze <elf>` → overview + procedure inventory") cannot tell
  aborted Go markup from completed markup.
- Counts: 9 Swiss labels with 3 failing, 6 noswiss labels with 0 failing (C11; entry
  `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:72-88`).
- Landing gate: `PROVINCE.md:31-32` admits Core ground only via a LOG entry that cites `evidence_id` and the
  subject sha256. `LOG.md:2125-2167` cites neither (C13). `LOG.md:2167` says measured values follow.

**F4 — `PROVINCE.md:26` cites `HEAD:PROVINCE.md:19-26` (observation).**
- The citation was introduced at `75af886` (2026-10-16, C14). It was meant to point at the parent,
  `a4bd355e216bff474c0cb2fc824d712c28a44cac`, whose lines 19-26 hold the `.bashrc` provider-key inventory.
- `REA_BINWALK_COMMAND` count in lines 19-25: 1 at `a4bd355`, 0 at REV (C15). At REV those lines hold three
  `_npx/` cache paths, and line 26 is the citing line itself.
- `arc2-loop1-round2/E4.md:82` ruled that it "stays valid because line-count-neutral". That was already wrong
  at `75af886`, which rewrote lines 19-25.
- Under jj, HEAD can name an off-branch commit (`SKILL.md:569-573`). `head-rev-lint` scans only `*.py`/`*.sh`
  (`.ufo/waves/round-18/tools/head-rev-lint.py:7-8`, `:179`), and `JjAuditKaidoku.md` has 0 PROVINCE
  mentions (C16). This prose pin escapes both.
- `a4bd355` is an ancestor of REV (C15, exit 0).

**F5 — Frontier (observation).** At REV the census reports `frontier_errors: []`. Appending one bullet past
`:162` in a sandbox gave exit 1: `PROVINCE.md:163 unregistered bullet … (FRONTIER-UNEVALUABLE)` (C17). The
check is at `c1-census-v10.py:449-468`; the same-commit re-key rule is at `:112-116`, with the register at
`:292-308`. Recommendation: add the silent-misread probe (entry `:96`, `:114-115`) only together with a
register re-key.

**F6 — host drift, outside r18 scope (observation).** `PROVINCE.md:62` lists as absent
"`cabextract`, `rizin`, `ltrace`, pacman-contrib". Actual state: rizin 0.8.2-2 (installed 2026-10-19 18:31
-03) and pacman-contrib 1.13.1-1 (2026-10-20 07:45 -03) are present; cabextract and ltrace are still absent
(C18).

**F7 — registry cadence (observation).** `PROVINCE.md:66-67` says the registry is "refreshed by `rea doctor`
each round". No doctor invocation is tracked under `.ufo/waves/round-14`…`round-18`; the only hits are
non-run mentions and file listings (C19).

## Proposed move (one patch: in place, 162 lines kept)

Apply as exact substring replacements on `PROVINCE.md`. Verified in sandbox commit
`f814d021a8366ca1a5b02af1bde48e3e3421cd38` on top of REV; diff sha256
`a641d14971ce49c6f91c9f1d623e4c7e7640b2487c5fdb4f91255bd0a5819762`.

1. **`:8-11`** — replace these four whole lines with:
   ```
   Surface summary: the `rea` MCP/CLI surfaces resolve per client: Devin, OMP and Kimi
   all use `rea-agents@6.7.0` (configs re-grepped 2026-10-20, `.ufo/waves/round-18/w2/ProvinceAccuracy.md`; 207 MCP tools + 153 CLI
   commands; Devin and OMP used the historical `rea-agents@6.5.0` pin, catalog `805433f1…`, until their configs changed 2026-10-20 13:35:56 -03;
   catalog tools_sha256 `af39310c…` — the package's compiled, recorded
   ```
2. **`:12`** — replace `both versions have separate npx cache installs` with
   `its npx cache was absent on 2026-10-20`.
3. **`:15-17`** — replace these three whole lines with:
   ```
   Drift-prone values: reverified 2026-10-18; pins re-grepped 2026-10-20 — configured REA MCP pins are Devin
   `rea-agents@6.7.0` (`/home/vgpnk/.config/devin/mcp_config.json:7`), OMP
   `rea-agents@6.7.0` (`/home/vgpnk/.omp/agent/mcp.json:8`; both files changed 2026-10-20 13:35:56 -03), and Kimi
   ```
4. **`:21-23`** — make three changes:
   - In `:21`, replace the final `; 6.4.0 at` with
     `; 6.4.0 (historical pin; 127 CLI commands, 170 MCP tools,`.
   - Replace all of `:22` with
     ``its cache `/home/vgpnk/.npm/_npx/dea9475797100b20` absent on 2026-10-20, historical;``
   - Replace all of `:23` with
     `` `tools_sha256=25802f6de8c14ba736dc61ff1cbc7c5cd738fd74426aa01338f2dd03e0911166`) ``
5. **`:25`** — replace `6.4.0 expects v37` with `6.4.0 (historical) expects v37`.
6. **`:26`** — replace `` `HEAD:PROVINCE.md:19-26` `` with
   `` `a4bd355e216bff474c0cb2fc824d712c28a44cac:PROVINCE.md:19-26` ``.
7. **`:44`** — replace
   `(Devin/OMP 6.5.0, Kimi 6.7.0; pins per the 2026-10-18 custody receipt, see surface summary)` with
   `(Devin, OMP and Kimi 6.7.0 — configs re-grepped 2026-10-20, see surface summary)`.
8. **`:48`** — replace ``recovered `process()` loop |`` with:
   ``recovered `process()` loop; Go 1.24/1.25 Swiss carriers (r18, 2026-10-20, author-side, one pass): `GolangSymbolAnalyzer` aborted after bootstrap on 3/9 Swiss labels and 0/6 `noswissmap` labels while `analyze` exited 0 and its JSON carried no trace of the abort (0/15) — read the bound `ghidra.log`; mechanism and limits in `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md` |``
9. **`:52`** — replace the final `(r2-08) |` with:
   ``(r2-08); one nethttp source aborted Go symbol markup under go1.24.6 Swiss and was silent under go1.25.0 Swiss (r18: name-table bytes decide, not the Go release), so two Go builds can differ in markup outcome from layout bytes alone (`corpus/knowledge/2026-10-20-r18-swiss-map-replay.md`) |``
10. **`:62`** — replace ``| absent: `cabextract`, `rizin`, `ltrace`, pacman-contrib |`` with:
    ``| absent at the 2026-10-13 sweep: `cabextract`, `rizin`, `ltrace`, pacman-contrib; on 2026-10-20 `rizin` 0.8.2-2 and pacman-contrib 1.13.1-1 are installed (`pacman -Q`), `cabextract` and `ltrace` still absent |``
11. **`:67`** — replace the leading `each round.` with
    `when a round re-probes REA (no doctor invocation is tracked in rounds 14–18).`

**When to land each part**

- **Now** (independent of the C3 verdict): edits 1-7, 10 and 11. These fix live state and the citation.
- **With the measured round-18 LOG entry**, and only if wave 2 leaves C3 `confirmed`: edits 8 and 9. That
  entry must cite `ev_fa79d26f6dc180710d10f7666f35a40a41aa7e1df92bb882ce10903a19045dd3` with sha256
  `5c9faf239ed2c68304666992a8d2c1dc40c36e90f8021c62fef4cc4453f201b6` (s1246-swiss-nethttp) and
  `ev_3d0da5949267d6a1c3718d258d9d6bfa30d04ac865031bfd4eb24d5c320b4096` with sha256
  `71067480bd99c2ba0f6d76df50a17e4911917cec8878320c107105066f8ad35d` (kimi-webbridge), per `PROVINCE.md:31-32`.

**Axes**
- Calibration: the CURRENT lines become true, the `:26` citation resolves to its claim, and the Swiss limit is
  scoped as author-side, one pass.
- Operability: operators learn that the abort is visible only in the log; the citation no longer depends on HEAD.
- Depth: the r18 limit sits in the row whose probe is `rea analyze`.

**No-harm check (sandbox, C12)**
- 162 lines kept. All edits are in place, so `SHONEN.md:12` (`PROVINCE.md:88-116`) and the line cites in
  SCORECARD, SKILL and the corpus still resolve. The `prov18-*` needles on `:18` are untouched.
- Census for PROVINCE: stale 3→0, unresolved 0, ambiguous 0, undeclared 0, `frontier_errors: []`. Current-ok
  detections in PROVINCE: 10→12.
- citation-drift `--strict`: clean, 0 findings, exit 0 (same as at REV).

**Effects outside PROVINCE**

The census stays exit 1 after this patch for three reasons outside PROVINCE:
- `SKILL.md:18-20` ("Devin/OMP `rea-agents@6.5.0`") is stale and needs the same fix in the same landing.
- `SCORECARD.md:2380-2382` and `SKILL.md:511-519` are r17 records that sit past the census SCOPE bounds. They
  already fail at baseline and need a records-commit re-key (`c1-census-v10.py:41-45`).
- Recommendation: add the census to the round-18 verification pass, pointed at an archived tree as
  `SCORECARD.md:2079-2083` requires (never a bare run from a worktree).

**Risks**
- The cited re-grep receipt is this report, which records the command, output and exit (C2, C3). Swap in a
  retained receipt path if the lane prefers one.
- If the configs revert to 6.5.0, edits 1, 3 and 7 go stale again. The census is the detector.
- Edit 9 generalizes from one source pair; it says "can", consistent with entry `:97` ("Do not generalize").
- The "3/9" count includes the calibration carrier aether.

## Commands (cwd = lane unless noted; R = REV)

| # | Command | Exit | Result |
|---|---|---|---|
| C1 | `git diff --quiet 9011581d84527ba34c675f9cf912e54d2e72d470 R -- PROVINCE.md; echo $?` | 0 | unchanged |
| C2 | `grep -n -o 'rea-agents@[0-9][0-9.]*' /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json /home/vgpnk/.kimi-code/config.toml` | 0 | `:7`, `:8`, `:4126` all `rea-agents@6.7.0` |
| C3 | `stat -c '%y %n'` on the same 3 files | 0 | devin/omp `2026-10-20 13:35:56 -0300`; kimi `2026-10-19 16:09:51 -0300` |
| C4 | `git log -3 --format='%h committer=%cI author=%aI %s' R` | 0 | b2aad08 committer 13:38:07 -03 |
| C5 | sandbox: `git clone --no-local -q LANE $T/lane && git -C $T/lane remote remove origin && git -C $T/lane checkout -q --detach R`; then `python3 -I -B lane/.ufo/gates/c1-census-v10.py --root lane --json`; repeated after `checkout --detach 9011581…` | 1 / 1 | FAIL; stale and undeclared as in F1; identical at both |
| C6 | for each `R:.ufo/waves/round-18/runs/*/receipt.json`: python prints `steps.analyze.argv[2]` and `exit` | 0 | `15 rea-agents@6.5.0 0` |
| C7 | per hash: `test -e /home/vgpnk/.npm/_npx/<h>/node_modules/rea-agents/package.json`; `ls -d /home/vgpnk/.npm/_npx/dea9475797100b20` | ls: 2 | dea94… ABSENT; ad9a3… 6.5.0; a1722… 6.7.0 |
| C8 | `git show R:.ufo/waves/round-1N/verification.json \| grep -c c1-census` for N = 4..7; `git grep -c c1-census R -- .ufo/waves/round-18/measure.py .ufo/waves/round-18/verify.py` | 0 / 1 | 1, 0, 0, 0; r14 entry `{'label': 'census', 'exit': 0}` with devin/omp 6.5.0; r18: no match |
| C9 | `git show R:PROVINCE.md \| grep -ciE 'swiss\|OldMapType\|GolangSymbolAnalyzer\|r18'` | 1 | 0 |
| C10 | per label: `grep -cE` (pattern as F3) on `analyze.json`, bound `ghidra.log` and `analyze.stderr`; python key-path and `limitations` diff, s1246-swiss-nethttp vs s1246-noswiss-nethttp | 0 | analyze 0/15; logs 2, 2, 2 on the failing 3; stderr 0; key-path sets equal; limitations equal |
| C11 | `layout.true_kind` from `R:.ufo/waves/round-18/predictions/swiss-misread/*.json` | 0 | 9 swiss, 6 old |
| C12 | sandbox: edits 1-11 with the edit tool, `git commit` in the clone; census `--root lane --json`; `citation-drift-probe.py --root lane --rev <patched> --table lane/.ufo/gates/citation-drift/pointer-table.json --expected lane/.ufo/gates/citation-drift/expected.json --strict`; `wc -l` | 1 / 0 | PROVINCE: 0 stale, 0 unresolved; drift `clean findings=0`; 162 lines |
| C12a | census after edits 1, 3, 6, 7, 8 and 9 only (before 2, 4, 5) | 1 | `PROVINCE.md` 15-26 UNRESOLVED: `no cache at _npx/dea9475797100b20`, `no cache for 6.4.0` |
| C13 | `git show R:LOG.md \| sed -n '2125,2167p' \| grep -nE 'ev_[0-9a-f]{8}\|sha256\|[0-9a-f]{64}'` | 1 | no match |
| C14 | `git log -S'HEAD:PROVINCE.md:19-26' --format='%H %ad %s' R -- PROVINCE.md`; `git rev-parse 75af886^` | 0 | `75af886a…`; parent `a4bd355e…` |
| C15 | `git show <r>:PROVINCE.md \| sed -n 19,25p \| grep -c REA_BINWALK_COMMAND` for r ∈ {a4bd355, R}; `git merge-base --is-ancestor a4bd355e216bff474c0cb2fc824d712c28a44cac R` | 0 | 1 vs 0 (R:19-25 hold 3 `_npx/` paths; R:26 is the citing line); ancestor exit 0 |
| C16 | `git show R:.ufo/waves/round-18/tools/head-rev-lint.py \| grep -n …`; `grep -c PROVINCE /home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md`; `git show R:PROVINCE.md \| grep -cE 'citation-drift\|custody-pair\|quote-fidelity\|temporal-sweep\|receipt-validate\|head-rev-lint\|revpin\|\bjj\b'` | 0 / 1 / 1 | scope `*.py`/`*.sh` (`:7-8`, `:179`); 0; 0 |
| C17 | sandbox: append one bullet past `:162`, run census, then `git checkout -- PROVINCE.md` | 1 | `FRONTIER-UNEVALUABLE` |
| C18 | `pacman -Q pacman-contrib rizin ltrace cabextract`; `pacman -Qi rizin pacman-contrib \| grep -E '^(Name\|Install Date)'` | 1 / 0 | pacman-contrib 1.13.1-1, rizin 0.8.2-2; ltrace and cabextract not found |
| C19 | `git grep -nE doctor R -- .ufo/waves/round-1N/ ':(exclude)*/runs/*' ':(exclude)*.stdout'` for N = 4..8 | 0 | 1, 0, 3, 20, 0 hits; all are non-run mentions or `controls.json` listings |

## Not examined

- Doctor alignment for the new Devin/OMP 6.7.0 registrations (no doctor run).
- Whether the running MCP servers have reloaded the new configs.
- Who edited the configs.
- The silent-misread program state.
- Anything that needs REA or Ghidra execution.

## Lane hygiene (observation, not this seat's change)

At my final check, the lane worktree held an uncommitted modification to `.ufo/gates/custody-pair/custody-pair.py`.
`git status --porcelain` shows ` M`; `git diff --stat` shows 2 insertions and 2 deletions; file mtime is
2026-10-20 14:07:24 -03. HEAD and `refs/heads/main` are both `b2aad08…`.

This seat wrote only this report. Its patch simulation ran in a removed mkdtemp clone. The modification
matters because a custody or citation gate run against the worktree, rather than against REV objects, would
use those bytes.
