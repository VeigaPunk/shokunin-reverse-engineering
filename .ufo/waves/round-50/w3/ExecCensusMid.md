# ExecCensusMid — round 50 attempt 2, wave 3 (build): SOURCES census receipts

**Verdict: PASS with one prompt-drift flag.** The maintained census and all seven frozen
manual census commands ran clean against `kaidoku-shokunin/corpus/SOURCES.md`. The
`validate` re-run is **byte-identical** to the L1's attempt-2 start receipt
(sha256 `ac7a98508b801e2612f50d71569b091f835bc4bdd8e55dd210f5c9a133e2865c`) — zero drift.
**Flag:** the seat brief predicted *15* W04 lines; the actual and the attempt-2 receipt both
carry **18**. The *15* figure is the attempt-1 **start** count, stale against attempt 2.
The attempt-2 receipt is the authority and it agrees exactly with the re-run.

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only; no writes outside this seat dir).
Base revision `f890bbead20ca2c549487167f56876ae47f1e1a4`; lane HEAD `6f4aba635fc47b5823ed42afe9c8b5dc3e28127f`;
C1 freeze `435d41fd4ad9211d1579fc447936fb33d2b74467` is an ancestor of HEAD (verified, read-only).
Artifacts: `.ufo/waves/round-50/w3/ExecCensusMid/` — `manual-census.txt`, `drift.txt`,
`validate-attempt2.out`, `census-attempt2.out`, `run-census.sh`, `run-drift.sh`, per-command `.out` files.

Scratch used: `/fast/scratch/hyaku/kaidoku-r50/w3-ExecCensusMid` (removed after copying receipts).
Disk guard: `scripts/hyaku/disk-guard.sh status` → exit 0 (ran before the pass; `/fast/scratch/hyaku` 39% used, 495.7G free).
No REA invocation, no `--data-run`, no corpus write, no git mutation, no network download, no tool install.

## Row count (the "before" number the report needs)

**152 rows.** Both the frozen column-zero count and the brief's spacing-tolerant count agree.

| command | exit | stdout | sha256 (stdout) | utc |
|---|---|---|---|---|
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` (cwd = lane root) | 0 | `152` | `a6ade98870a92fc7e8bfd6eee3662e7823131fe83fdcdab6b73af38144accd49` | 2026-10-29T20:33:37Z |
| `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md` | 0 | `152` | `a6ade98870a92fc7e8bfd6eee3662e7823131fe83fdcdab6b73af38144accd49` | 2026-10-29T20:33:37Z |

Both give 152 ⇒ no row is indented 1–3 spaces, so the frozen (column-zero) examples and the
maintained 0–3-space parser see the same registry. The maintained CLI agrees independently:
`rows 152`, `tier.A 139 / tier.B 8 / tier.C 5`, `status.mined 143 / status.rejected 9`,
`tier.invalid 0`, `status.queued 0`, `status.invalid 0`, `missing 0` (exit 0).

## Findings table — frozen manual census (CORPUS.md §Census, verbatim, cwd = lane root)

| # | check | command (verbatim from CORPUS.md) | exit | stdout | sha256 (stdout) | utc |
|---|---|---|---|---|---|---|
| 1 | rows | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 0 | `152` | `a6ade98870a92fc7e8bfd6eee3662e7823131fe83fdcdab6b73af38144accd49` | 2026-10-29T20:33:37Z |
| 2 | malformed rows (must be 0) | `awk -F'\|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md` | 0 | `0` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | 2026-10-29T20:33:37Z |
| 3 | tier histogram | `awk -F'\|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md` | 0 | `A=139 B=8 C=5` | `eb79a825a8a1f17b03b4a1293b86d1dd1e9b9370e7b683d8f465374d93535d9d` | 2026-10-29T20:33:37Z |
| 4 | status histogram | `awk -F'\|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md` | 0 | `mined=143 rejected=9` | `c9d7f75487c3692fbe1b16058b3948e79e642ff9d85e366273af55d98a6bc565` | 2026-10-29T20:33:37Z |
| 5 | duplicate ids (must be empty) | `awk -F'\|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md \| sort \| uniq -d` | 0 | *(empty)* | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-29T20:33:37Z |
| 6 | enum violations + tier inflation (must be empty) | `awk -F'\|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued\|mined\|rejected)$/) print "status", i, s; if (k !~ /^(spec\|docs\|paper\|code\|tool\|dataset\|talk\|book\|community\|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md` | 0 | *(empty)* | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-29T20:33:37Z |
| 7 | mined used-by paths missing on disk (must be empty) | `awk -F'\|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+\|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md \| while read -r p; do [ -e "$p" ] \|\| echo "missing: $p"; done` | 0 | *(empty)* | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-29T20:33:37Z |

Full commands + stdout + exit + sha256 + UTC for all seven: `.ufo/waves/round-50/w3/ExecCensusMid/manual-census.txt`.

**Non-vacuity of check 7.** An empty result is only meaningful if the loop had candidates.
Counted: **245** mined `used-by` paths were actually resolved against the lane root (same awk, counting
instead of printing; sha256 `a82c695d045ef91073e2f52598bb4e53520b179d8b581ad43e687bd8dd868e22`,
2026-10-29T20:34:21Z). All 245 exist. The check is not vacuous.

**Histogram internal consistency.** `A=139 B=8 C=5` sums to 152; `mined=143 rejected=9` sums to 152;
both match the 152 row count. `status.queued = 0` — no row is left `queued`.

## Maintained CLI: `sources-census.sh validate`

Command (fleet root, no writes): `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`

- exit code: **0**
- stdout: 19 lines — 18 × `kaidoku W04 …` + final `kaidoku<TAB>ok<TAB>/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`
- stdout sha256: `ac7a98508b801e2612f50d71569b091f835bc4bdd8e55dd210f5c9a133e2865c`
- saved: `.ufo/waves/round-50/w3/ExecCensusMid/validate-attempt2.out`
- E-code count: **0** (no E01–E12 findings). W04 count: **18**.

### Drift vs the L1 attempt-2 start receipt — NONE

| command | exit | result |
|---|---|---|
| `diff .ufo/waves/round-50/l1/sources-census-start-attempt2.txt .ufo/waves/round-50/w3/ExecCensusMid/validate-attempt2.out` | 0 | *(no output)* |
| `cmp` of the same two files | 0 | byte-identical |
| `sha256sum` of both files | 0 | both `ac7a98508b801e2612f50d71569b091f835bc4bdd8e55dd210f5c9a133e2865c` |

Re-run determinism: a second `validate` run produced the same sha256
`ac7a98508b801e2612f50d71569b091f835bc4bdd8e55dd210f5c9a133e2865c`. The output is stable.

### The 15-vs-18 W04 flag (read this before scoring)

| receipt | W04 lines | note |
|---|---|---|
| `l1/sources-census-start.txt` (attempt 1 **start**) | **15** | ← the number quoted in the seat brief |
| `l1/sources-census-end.txt` (attempt 1 **end**) | 18 | S246/S247/S248 W04s added by the C2 landing |
| `l1/sources-census-start-attempt2.txt` (attempt 2 start) | 18 | attempt-2 authority |
| my re-run (attempt 2) | 18 | identical bytes to the row above |

`diff sources-census-start.txt sources-census-start-attempt2.txt` (exit 1) shows exactly the
three added lines and the dropped trailing `exit 0` marker line:

```
15a16,18
> kaidoku	W04	S246 duplicate url plato.stanford.edu/entries/popper across scopes
> kaidoku	W04	S247 duplicate url man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 across scopes
> kaidoku	W04	S248 duplicate url github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs across scopes
17d19
< exit 0
```

**Reading:** the brief's "expect 15 W04 lines" is stale — it is the attempt-1 *start* number. S246–S248
were landed by the R50-C2 landing commit (`11ccdb72 round-50: R50-C2 landing (record corrections,
SOURCES S246-S248, registry rows, …)`), which is why attempt 1 ended at 18 and attempt 2 starts at 18.
**Drift against the attempt-2 baseline is zero.** The three W04s are same-URL-across-scopes warnings
(S246 popper, S247 sysexits, S248 unblob squashfs tree) — W-codes never change lane status, and the
CLI's own header states warnings do not affect clean lanes. The exit code is 0 and the final line is
`kaidoku ok …` as required.

## Registry immutability (no census-side change this wave)

`corpus/SOURCES.md` sha256 = `2204e6a6475177616caa92446c68ec35c3e6cdcd8f5194e945b7b201d8f189c4`
in **all three** places: worktree, `git show HEAD:corpus/SOURCES.md`, and
`git show f890bbead20ca2c549487167f56876ae47f1e1a4:corpus/SOURCES.md` (base revision).
So the "before" number 152 is measured against the exact bytes the attempt-2 claims commit froze.
Worktree `git status --porcelain` in the lane shows only untracked wave/`.ufo` artifacts — no tracked
file is modified.

## Cross-checks (read-only)

| check | command | exit | result |
|---|---|---|---|
| census mode (fleet aggregate) | `bash scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kaidoku` | 0 | rows 152, A 139/B 8/C 5, mined 143/rejected 9, invalid 0, missing 0; stdout sha256 `ab10c0445a741b01ef306ae2011a63f4df8aa0fdbcfd0ddf44b0aead63251ef2` |
| single-file mode | `bash scripts/sources-census.sh census --file …/kaidoku-shokunin/corpus/SOURCES.md` | 0 | identical row/tier/status numbers as the lane-discovery path |
| tool selftest | `bash scripts/sources-census.sh selftest` | 0 | `selftest ok` (kills H1-no-table-cell-execution, gawk-failure-is-error-not-ok, E04-rejected-pair-exemption-exit-0, out-not-truncated-before-target-resolution) |

## Risks / blockers

- **None blocking.** The census is clean and reproducible; the L1 can score the C1/C3 controls and
  run the C1 data run against a registry whose bytes are pinned to the base revision.
- **One prompt-side correction for the L1:** do not expect 15 W04 lines in the attempt-2 end receipt;
  expect 18 (or write the attempt-2 end receipt with the same 18 W04 lines + `exit 0`, matching
  `sources-census-end.txt`'s shape minus the 15-count expectation). If the L1 wants a zero-delta
  before/after pair, the attempt-2 start receipt is the correct baseline.
- If the C1/C3 landing adds SOURCES rows, the census must be re-run — 152 is the **before** number only.
- Not run (deliberately, per the wave contract): REA controls, REA data run, `--data-run`, any
  `corpus/evidence/` write, any git mutation.

## Files written (this seat only)

- `.ufo/waves/round-50/w3/ExecCensusMid.md` (this report)
- `.ufo/waves/round-50/w3/ExecCensusMid/manual-census.txt` — 7 frozen manual census commands, full output, exit, sha256, UTC
- `.ufo/waves/round-50/w3/ExecCensusMid/drift.txt` — 14 drift/immutability commands, full output, exit, sha256, UTC
- `.ufo/waves/round-50/w3/ExecCensusMid/validate-attempt2.out` — full `sources-census.sh validate` stdout (19 lines)
- `.ufo/waves/round-50/w3/ExecCensusMid/census-attempt2.out` — full `sources-census.sh census` stdout
- `.ufo/waves/round-50/w3/ExecCensusMid/{rows,rows-spacing-tolerant,malformed-rows,tier-histogram,status-histogram,duplicate-ids,enum-violations,mined-used-by-missing}.out` — per-command stdout
- `.ufo/waves/round-50/w3/ExecCensusMid/run-census.sh`, `run-drift.sh` — the exact drivers used (re-runnable, read-only)

Nothing was written to the lane's `corpus/`, `plans/`, `tools/`, `SKILL.md`, `PROVINCE.md`, `LOG.md`,
`SCORECARD.md`, `SHONEN.md`, nor to the fleet repo. No git/jj mutation was run in the lane or fleet repo.
Lane `git status --porcelain --untracked-files=no` is empty (no tracked file modified).
The fleet repo shows one pre-existing modification, `.scratch/goal-20261029-hyaku-run12.md`
(mtime 2026-10-29 17:13:19 -0300 = 20:13Z, i.e. **before** this seat's first command at 20:33:37Z);
it is not mine — this seat never wrote under `/home/vgpnk/Projects/shokunin/.scratch/`. Noted, not touched.
No tools were installed or upgraded this wave (none needed; `gawk`, `grep`, `awk`, `sha256sum`, `bash`
were already present), so there is no tool/version/channel entry to report.
