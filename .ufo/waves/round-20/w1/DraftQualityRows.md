# DraftQualityRows — QUALITY #23 and #24 (round 20, w1, advisory author-side seat)

Written 2026-10-20T17:48:03-03:00 (clock at write). Baseline `14f0260ad319ecc26994381b2415d5a999003375` (refs/heads/main at dispatch, committed 2026-10-20T17:24:21-03:00). Read-only seat: lane files untouched; no patch; no tools installed or updated (Tooling record: none).

## Axes
- calibration: the rows must not claim a check that has not been run.
- coverage: each row names what it does NOT cover (zoneless timestamps; bypass classes).
- depth: each row grounded in a lesson line and a committed or working-tree fact.

## Observations

1. Baseline QUALITY has rows 1–22 only; `#23` and `#24` are free. Format is `| # | criterion | why (lesson) | supersedes |`, and the file says a criterion is replaced by a new row naming what it supersedes (`corpus/QUALITY.md:4-5`, verified via `git show 14f0260:corpus/QUALITY.md`). No existing row covers timestamps or guard records; row 22 is the last (`corpus/QUALITY.md:32`), so `supersedes` = `—` for both.
2. The timestamp defect: `claims.json:36` amendment with `"at": "2026-10-20T16:20:00-03:00 …"` shipped in `4f6c73f` (`git show 4f6c73f:.ufo/waves/round-19/claims.json | grep -n '"at"'` → line 36). `git show -s --format='%cI' 4f6c73f` → `2026-10-20T16:09:17-03:00`. The withdrawal sits at `claims.json:45` (`git blame -L45,45 b26a6c4`, introduced in `b26a6c4`). Lesson ruling: `corpus/lessons/round-19-verifier-spotcheck.md:100-103` and D2 at `:182-183`.
3. Calibration trap for the tool: `git blame` default date column shows the **author** time, not the committer time. `git blame -L36,36 b26a6c4 -- .ufo/waves/round-19/claims.json` prints `4f6c73f (… 2026-10-20 15:57:44 -0300 36)`, which is `4f6c73f`'s author time; its committer time is 16:09:17 (`git show -s --format='%cI' 4f6c73f`). The W20 contract specifies committer time (`.ufo/waves/round-20/contract.md:43-45`, D2). Row #23 must say `%cI`; a checker that reads blame's default column would compare against 15:57:44 and still flag 16:20, but would mis-state the margin.
4. Breach evidence for #24: `corpus/lessons/round-19-verifier-spotcheck.md:96-99` (carrier-version execution, `w1/InstallRecordDraft.md:26`, ruling "does not taint C3"). Verified text at `git show 4f6c73f:.ufo/waves/round-19/w1/InstallRecordDraft.md` line 26: `` `~/.local/opt/go-{1.24.6,1.25.0}/bin/go version` `` → `go version go1.24.6 linux/amd64`. Round-19's own Mistakes row 5 (`corpus/lessons/round-19.md:90`): "wave contract, not technically enforced … **No demonstrated enforcement fix** … SHA-256 checks do not detect prior execution."
5. D3 interface and declared limit: `.ufo/waves/round-20/contract.md:46-52` — `arm` records sha256/size/mode/ctime_ns and clears exec bits (`arm.json`); `check` exits 1 with `mode_restored`, `ctime_changed`, `content_changed`; `disarm` restores modes; declared limit "loader-mapped execution (`ld-linux … <file>`) and root are not prevented." Lesson gap statement: `corpus/lessons/round-19-verifier-spotcheck.md:184-185`.
6. Partial state already on disk: `.ufo/waves/round-20/evidence/carrier-guard/manual-arm.json` (untracked in the lane; `git status --porcelain` lists `.ufo/waves/round-20/w1/` and siblings, and the file's `action` field reads "manual-arm (L1, before the carrier-guard tool exists)"; `mode_after` `0o644` on Go carriers; no `check` or `disarm` record in that directory — `ls -R .ufo/waves/round-20/evidence/carrier-guard` shows only `manual-arm.json`). This is an arm without check/disarm, which the #24 draft must reject as evidence of non-execution. [INFERENCE] that a bare arm does not prove non-execution follows from the contract's own check semantics (`contract.md:46-52`).
7. Tool status: `W20/tools/evidence-timestamps.py` and `W20/tools/carrier-guard.py` do not exist at baseline (`git ls-tree -r --name-only 14f0260 -- .ufo/waves/round-20` lists no tools; `glob **/evidence-timestamps*` under the lane returned nothing). Both are sibling deliverables per `contract.md:41-52`. The rows can be admitted only after those tools exist and their selftests pass in a system tempdir.
8. Round-19 precedent for not retro-voiding: the breach is ruled "does not taint C3" (`round-19-verifier-spotcheck.md:96-99`), and the timestamp is "status-neutral" because `git diff a1140e7 A -- predictions/decision-rule.json` is empty (`:100-103`). The #24 draft should therefore apply forward only; it must not reopen round-19 verdicts. [INFERENCE] that a forward-only admission rule is the correct reading of the lesson's ruling.

## Draft

| # | criterion | why (lesson) | supersedes |
|---|---|---|---|
| 23 | Evidence timestamps are at or before the shipping commit. Every timestamp with an explicit zone on a line of a tracked file (`YYYY-MM-DDTHH:MM[:SS][.f](Z\|±HH:MM)`, or `YYYY-MM-DD HH:MM[:SS] ±HH[MM]`) is compared with the committer time (`%cI`, not blame's author column) of the commit that introduced that line; a later instant is a `future_dated <path>:<line>` finding. Admitted only with `python3 -I -B .ufo/waves/round-20/tools/evidence-timestamps.py --root <lane> --rev <shipping-rev> --path <dir> --strict` exiting 0 at that rev. Zoneless timestamps are not checked and must be stated as unchecked. | `corpus/lessons/round-19-verifier-spotcheck.md:100-103` (`claims.json:36` 16:20 amendment shipped in `4f6c73f`, committed 16:09:17; withdrawn at `:45`); D2 at `:182-183`; tool interface `.ufo/waves/round-20/contract.md:41-45` | — |
| 24 | A no-execution contract (for example "no carrier execution") is admitted only with a guard record: `arm` (per-artifact sha256, size, mode and ctime_ns recorded, exec bits cleared), `check` (modes still exec-free, ctime and content unchanged since arm; any of `mode_restored`, `ctime_changed`, `content_changed` exits 1), and `disarm` (recorded modes restored), with the check output retained. The record declares its bypass limits; at minimum loader-mapped execution (`ld-linux … <file>`) and root are not prevented. A contract without a guard record is stated as "instructed, not enforced". An arm without a check is not evidence of non-execution. Admission is forward-only; it does not reopen earlier verdicts. | `corpus/lessons/round-19-verifier-spotcheck.md:96-99` (`go version` execution at `w1/InstallRecordDraft.md:26`; "does not taint C3"); `:184-185` (D3: no enforcement that prevents or detects carrier execution); `corpus/lessons/round-19.md:90` (Mistakes row 5: "No demonstrated enforcement fix"; "SHA-256 checks do not detect prior execution"); guard interface and declared limit `.ufo/waves/round-20/contract.md:46-52` | — |

## Checks not run (declared)
- `evidence-timestamps.py` and `carrier-guard.py` do not exist at baseline; no selftest or `--strict` run was performed by this seat. The rows' admission depends on those runs by the L1.
- Ghidra/REA/Go toolchain binaries: not touched. Nothing executed. Byte-reading only (`git show`, `grep`, `sed`, `blame`, `stat`-free).

## Commands and exits (this seat)
- `git --no-optional-locks show 14f0260…:corpus/QUALITY.md | grep -n '^| 2[0-9] '` → exit 0, rows 20–22.
- `git --no-optional-locks show 4f6c73f:.ufo/waves/round-19/claims.json | grep -n '"at"'` → exit 0, line 36.
- `git --no-optional-locks show -s --format='%h author=%aI committer=%cI' 4f6c73f` → `author=2026-10-20T15:57:44-03:00 committer=2026-10-20T16:09:17-03:00`.
- `git --no-optional-locks blame -L36,36 --porcelain b26a6c4 -- .ufo/waves/round-19/claims.json` → exit 0; `author-time 1792522664`, `committer-time 1792523357`.
- `git --no-optional-locks show 4f6c73f:.ufo/waves/round-19/w1/InstallRecordDraft.md | sed -n 24,27p` → exit 0; line 26 names `bin/go version`.
- `ls -R .ufo/waves/round-20/evidence/carrier-guard` → `manual-arm.json` only.
- `git ls-tree -r --name-only 14f0260 -- .ufo/waves/round-20` → no tools, no gates.
- `date -Iseconds` → `2026-10-20T17:48:03-03:00`.

## Findings for L1 (no lane edit made)
- F1 (calibration): specify `%cI` committer time in #23; blame's default column is author time.
- F2 (coverage): #23 excludes zoneless timestamps; #24 names loader-mapped execution and root as bypass classes.
- F3 (depth): #24 requires the check record, not only arm; manual-arm.json is the partial example.
- F4: no `supersedes` for either row; both are new admissions, not replacements of #1–#22.
