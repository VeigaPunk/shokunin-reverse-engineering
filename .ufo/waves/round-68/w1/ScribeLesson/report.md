# ScribeLesson — sources opened (round 68, wave w1)

Seat `ScribeLesson` (scribe; leaf, no dispatch). Everything below was opened on **2026-11-03** from
this host, read-only. No lane gate, counter or instrument was executed by this seat; where a number
appears it was counted from committed or fetched bytes with the command shown.

## Lane files and git objects (path or object → what was taken from it)

| source | opened as | taken |
|---|---|---|
| `plans/round-68-claims.md` | full read | both predicates, the regime, the counting commands, the kill rules, the do-nothing arms, the six repairs, the frontier step |
| `.ufo/waves/round-68/claims.json` | full read | base, freeze pointer, the three instrument pins, `instrument_supersessions: []`, atoms A0–A9, the repairs list |
| `.ufo/waves/round-68/l1/pre/c1-at-base.json` | full read | `mismatches 2` naming the two round-67 paths, `scope_size 69`, `registry_rows 73`, `registry_paths 73`, `legacy_unregistered 26`, `named_but_absent 12`, `rev: "main"` (line 56), `instrument.rev: null` (line 6) |
| `.ufo/waves/round-68/l1/pre/c2-dryrun-at-base.json` | JSON parsed (carriers, packer, rea, closure) | `carriers_matched 2/2`, `control_ok true`, `met_target true`, `before_procedures [3, 3]`, per-carrier counts (jq 167/30/190 and packed 3/3/3; xxd 99/29/103 and packed 3/3/6), `packer` `upx 5.2.0` sha256 `cf2f6e7c…c969`, `rea` 6.5.0 / `package.json` `a5003023…`, `lock_sha256 null`, `instrument.sha256 7ee286c0…`, `instrument.rev null`, `rev: "main"` |
| `.ufo/waves/round-68/l1/pre/controls-at-base.json` | full read | six arms, `ok true`, `green` list, the two false-green C1 arms (`c1-shortcut-self` 0/72, `c1-constant-zero` 0) and the two not-met C2 arms |
| `.ufo/waves/round-68/l1/census-start.txt` | full read | `validate` exit 0, 19 W04 lines, `ok` on `corpus/SOURCES.md`; no row-count line |
| `.ufo/waves/round-68/w1/ScoutSource/gate.md`, `row.S270.md`, `SHA256SUMS`, `fetch/` | full read | the five candidates and their decisions, the S270 row text, the fetched-copy manifest |
| `corpus/lessons/round-67-verifier-spotcheck.md` | full read | the outside closure's per-check table, its four conformance defects, its routed list (defect 2 = the missing registry rows; defect 6 = receipt rev provenance) |
| `corpus/lessons/round-67.md` | full read | the lesson's section shape, M67-0…M67-8, the QUALITY rows it added |
| `corpus/knowledge/2026-11-03-r67-avm-le-squashfs-core.md` | lines 30-60, working tree | the stale sentence at line 33 and the appended `## Correction — 2026-11-03, round 68` block at line 49; the block is **working-tree only** (`grep -c 'round 68 (appended'` = 0 at `2dd5f2cd`, `fcbe200f`, `6020eb60`, `1eaf596e`, `6ffa9ce1`) |
| `corpus/SOURCES.md` | current file + `git show fcbe200f…:corpus/SOURCES.md` | 175 rows at the base (`A=161 B=9 C=5`, `mined=166 rejected=9`, malformed 0, 11-column split); `S269` absent at the base, present in the working tree (`git diff` = 1 insertion); current count 176 |
| `SKILL.md` | `git show fcbe200f…:SKILL.md` and `git diff SKILL.md` | 73 rows between the two instrument-registry v2 markers at the base; four rows added in the working tree (two round-67, two round-68), uncommitted |
| `tools/round-68/packed-elf.py` | lines 1-60, 182-260 | the arm definitions, the `rea`/lock/pin block, `pack = run([UPX, "--best", "-q", …])` at line 242, `identity_ok` at 257-258, the only commit `6020eb60` and its sha256 `48ef4c68…` |
| `tools/round-68/registry-conformance.py` | lines 14-34, 56-69, 100-151 | the regime text, `PLAN_RE`/`TOOL_RE`, `plan_scope`, `scope_size`/`registry_rows`/`mismatches` construction |
| `plans/round-51-claims.md`, `plans/round-52-claims.md` | grepped for their own `tools/round-N/` names | six named instruments each; `round-52` has no tool blob at the base |
| `PROTOCOL.md` (fleet root) | §Gate standard (375-420), §Evidence standard (343-369) | the Registry, Delivery, Two evidences and Scope clauses; the resolvable-pointer and counting-command clauses |
| `corpus/QUALITY.md` | rows 105-110 | QUALITY #107 (a rule generalised from one carrier family) as the criterion cited in M68-4; #33/#100/#110 from the round-67 lesson and spot-check |

## External sources (all opened 2026-11-03, `curl -sSL`, copies in `ScribeLesson/`)

| locator | HTTP | bytes | sha256 | used for |
|---|---|---|---|---|
| https://raw.githubusercontent.com/upx/upx/v5.3.0/doc/upx-doc.txt | 200 | 39 224 | `9b980dca…d3c35` | independent re-measure of S270's sentence (line 484, ELF386), the `--exact` note (101-106), the PE carve-out (759-764) |
| https://upx.github.io/ | 200 | 5 059 | `f07678bd…1fa7` | reject candidate (b); `byte-identical` 0, `checksum` 1; matches ScoutSource's sha, differs from its stated size (M68-5) |
| https://upx.github.io/upx-doc.html | 404 | 9 379 | `b6205073…0368` | reject candidate (c) |
| https://raw.githubusercontent.com/upx/upx/v5.3.0/README | 200 | 3 718 | `23954720…7ff0` | `byte-identical` 0; the README is byte-identical to the devel branch, used only for the operations list |
| https://raw.githubusercontent.com/upx/upx/v5.3.0/doc/upx.1 | 200 | 42 280 | `ae0da473…9897` | second serialization of the same sentences; duplicate-locator check |
| https://api.github.com/repos/upx/upx/tags | 200 | 3 539 | — | tag → commit: `v5.3.0` = `7c7bea44146c7ad6e17cb2d0bb9566805b44a91a`, `v5.2.0` = `034b6d0d81c5…` |

## Receipt and copies written by this seat

- `.ufo/waves/round-68/w1/ScribeLesson/gate-fetch.json` — the six external opens with HTTP status,
  size, sha256 and decision.
- `.ufo/waves/round-68/w1/ScribeLesson/upx-doc.txt` (39 224 B, sha `9b980dca…`),
  `upx-home.html` (5 059 B, sha `f07678bd…`) — the bytes the Gate table's quotes come from.

## Not opened

No round-51 or round-52 lane report (M68-3's cause is left `unknown` for that reason); no browser;
no `npx`; no pacman; the lane's instruments were read, never executed.
