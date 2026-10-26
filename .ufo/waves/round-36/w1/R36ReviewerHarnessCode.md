# R36ReviewerHarnessCode — code review of the R36-C1/C2 harness and counters (w1)

Seat: reviewer, kaidoku-shokunin round 36 wave 1. Scope: `tools/round-36/c1-run.sh`,
`tools/round-36/c1-counter.py`, `tools/round-36/c2-counter.py` — hardcoded /tmp (addendum §7
item 4 class), unbounded writes, shell quoting, error paths that silently pass, git calls
without `-C`, selftest fixture identity confined to scratch repos, and frozen-rule diffs vs
`plans/round-36-claims.md`. Advisory only; nothing was edited.

## 0. Method, identity, environment

- **Reviewed bytes are the frozen bytes.** `git cat-file -p 790561d:<f> | sha256sum` vs
  worktree sha256 → `SAME` for all six inputs checked (`c1-run.sh` 16907dca…, `c1-counter.py`
  5533e17d…, `c2-counter.py` f079aff1…, `tools/round-27/xpin-attribute.mjs` 8ea63837…,
  `plans/round-36-claims.md` 2c9cbde7…, `corpus/evidence/round-36/c1/carriers.json` 2ebcf15a…).
  Lane `git status --porcelain` shows only untracked wave files + the r36 knowledge entry.
- **No LSP server is available** (`xd://lsp` → "No such tool"); all checks are full-text review
  plus live behavioral probes, per the fallback rule. Recorded as a verification gap.
- Live probes (all under scratch `/fast/scratch/hyaku/kaidoku-r36/R36ReviewerHarnessCode`,
  `TMPDIR` pointed there; scratch removed at the end of this seat):
  1. `python3 -I -B tools/round-36/c1-counter.py --selftest --pkg65 <rea-agents 6.5.0 root>` →
     `{"cases": 14, "green_ok": 1, "red_ok": 13, "failures": []}`, rc=0.
  2. `python3 -I -B tools/round-36/c2-counter.py --selftest` →
     `{"cases": 13, "green_ok": 1, "red_ok": 12, "failures": []}`, rc=0.
  3. Exit-code probes: c1 bad args → 2; c1 unknown rev → 2 (Unevaluable); c2 bad args → 2;
     `c1-run.sh` with no args → 2 (usage).
  4. Harness oracle mode on a synthetic 8 KiB fixture (fake ELF header, `e_shoff=3584`,
     `e_shentsize=64`, `e_shnum=8`, real mksquashfs image appended at 4096) → rc=0, receipt
     `squashfs_offset 4096`, `oracle.tsv` correct, unsquashfs 4.7.5 recorded. Corrupted magic at
     the offset → `no hsqs magic at offset 4096`, rc=3 (loud).
  5. Harness `before`/`after` on the non-carrier `tools/round-36/selftest/dev-le-xz.sqsh`:
     both rc=0; before receipt records `sasquatch: ""`, envelope gap
     `missing-extractor-dependency [sasquatch]`, 0 files; after receipt records
     `~/.local/bin/sasquatch`, sha `ad02d27a…`, version 4.5.1, 2 files, no gaps. `/tmp` listing
     diffed before vs after both runs → **no new /tmp entries**. No `c1-run.*` scratch left
     after any run (trap works, six runs exercised).
- Tooling directive: nothing installed or updated for this seat (none needed). No pacman use.
- Lane VCS untouched (read-only `cat-file`/`status`/`show` only); the only file written is this
  report.

## 1. Findings (severity-ranked)

No High or Medium findings. Every deviation found either fails loud (nonzero exit + stderr, no
receipt JSON), or can only push a counter toward an honest stop (false negative), or is prose.
The claim-critical direction — a counter falsely reaching `met_target` — had no defect in any
reviewed path: every C1 binding is a positive conjunction over verified fields, and every C2
check plus its three guards matches the claims sentence.

### LOW

**L1 — Exit-code contract violated on malformed input (crash → undocumented exit 1).**
Docstrings promise exactly 0/1/2 (`c1-counter.py:20`, `c2-counter.py:20`) and 0/2/3
(`c1-run.sh:18`), but these paths exit 1 with a Python traceback:

- `c1-run.sh:38` — `struct.unpack_from('<Q', b, 0x28)` raises `struct.error` for a file with an
  ELF magic but < 48 bytes. **Live repro**: 13-byte `\x7fELF\x02\x01garbage` carrier →
  `struct.error: unpack_from requires a buffer of at least 48 bytes … actual buffer size is 13`,
  harness rc=1 (contract says 2 or 3). Same class: `c1-run.sh:45` (dd I/O failure) and
  `c1-run.sh:21` (mkdir/realpath failure) exit 1.
- `c1-counter.py:149` — `json.loads(frozen)` on a malformed `carriers.json` at the freeze commit
  → traceback, rc=1, i.e. the documented meaning of "target not met", while no receipt JSON is
  written. Adjacent: `KeyError` on a carriers.json without `carriers`/`id`/`sha256`
  (`:150,152,158`).
- `c2-counter.py:147` — `json.loads(t)` on a malformed
  `evidence/round-1-2026-10-15/result.json` → same class.
- `c1-counter.py:104-105` — `f[1]/f[2]` with no column-count check on xpin stdout → `IndexError`
  if the tool's line shape ever changes (the line-count check at `:101-102` does not cover
  columns).

Direction is safe (never a false green; the crash path writes no `--json-out`, so a receipt
absence exposes it), but the claims' kill rule reads the counter's exit as the scoring signal,
and an unevaluable run would be recorded as exit 1 "honest miss" if the operator only keeps the
code. Frozen bytes — reported, not repaired.

**L2 — c2 pointer filter is narrower than the frozen claims sentence.**
`c2-counter.py:99-100`: `if '/' not in path and not path.endswith('.md'): continue` silently
exempts bare extensionless single-component backticked tokens (`README`, `result.json`) from the
resolution check. P36-C2 says "every backticked repo pointer in them resolves". A surface
pointer like `` `result.json` `` naming nothing would not be counted as a mismatch — the only
place the frozen counter is *looser* than the frozen claims. Latent today: the surfaces'
pointers are slash-bearing or `.md` (the base mismatch `receipts-B/` *is* counted, `:106-107`
rstrip+exists), and the `pointers_not_fewer` guard counts the same filtered set, so the guard is
self-consistent. Report-only.

**L3 — unbounded runtime on the counter's xpin subprocess.**
`c1-counter.py:95-96` runs `node xpin-attribute.mjs …` with `capture_output` and no timeout,
while the harness caps REA at 900 s (`c1-run.sh:81`). A wedged node hangs the counter forever
(no receipt, no exit). Combine with the missing column validation at `:103-105` (L1).

### INFO

**I1 — hardcoded /tmp: PASS (the §7-item-4 check).** No `/tmp` literal in any of the three
files. Harness scratch = `${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r36/c1-run.XXXXXX`
(`c1-run.sh:22-27`, `TMPDIR` exported at `:27`); counters place every tempfile under
`scratch_root()` / `HYAKU_SCRATCH` default `/fast/scratch/hyaku` (`c1-counter.py:52-55,151,330`;
`c2-counter.py:306` with its `sroot` at ~`:300`); `tempfile.mkdtemp` is always called with an
explicit `dir=`. Live: `/tmp` listing diff across two REA runs → no new entries; all extraction
output landed under scratch/OUTDIR; harness scratch removed on every exit.

**I2 — unbounded writes: PASS in practice.** REA wall-clock capped at 900 s (`c1-run.sh:81`);
receipt stderr head capped (`grep -v 'npm warn' | cut -c1-400 | sed -n 1,20p`, `:86`); oracle
TSV proportional to the frozen carrier; unsquashfs tree (`:47`) and REA out (`:81`) live only
under scratch; counters write only their scratch workdir (rmtree'd, `c1-counter.py:195-196`) and
`--json-out`. No disk quota exists, acceptable for frozen carriers. Minor: `timeout` TERMs only
the npx child, so unblob workers may briefly outlive it inside the then-removed scratch.

**I3 — shell quoting: PASS.** All expansions quoted; the unquoted `-f $carrier` / `-n $outdir`
at `c1-run.sh:20` are safe inside `[[ ]]` (no splitting/glob); trap is single-quoted so
`$scratch` expands at trap time (`:26`); heredocs use quoted delimiters and `python3 -I`
(`:32,48`); the substitution at `:86` is argument-position, so `grep -v`'s rc=1 on empty input
cannot abort under `set -euo pipefail`. Empty-PATH edge measured fail-safe: bash `command -v`
on an *empty* PATH searches the cwd (live probe found `./sasquatch`, rc=0), so a fully emptied
before-filter result fails **loud** at `:72` (exit 2) instead of silently running with a
reachable sasquatch; the filter also drops empty PATH elements (`if d …`, `:71`).

**I4 — git without -C: PASS.** The harness contains zero git calls. Every counter git
invocation carries `-C root` (`c1-counter.py:41,48`; `c2-counter.py:35,40,119,167`), selftests
use `git -C <fixture>` exclusively (`c1-counter.py:332-343,351-352`; `c2-counter.py:308-321`),
and the counters touch the lane repo only as a read-only object store (`show`/`cat-file`/
`ls-tree`).

**I5 — selftest fixture identity: PASS.** Both selftests build fixtures only under
`$HYAKU_SCRATCH/kaidoku-r36` (`tempfile.mkdtemp(dir=…)` at `c1-counter.py:330`,
`c2-counter.py:306`), verify `git -C d rev-parse --show-toplevel` realpath-equals the fixture
**before the first commit** (`c1-counter.py:333-335`; `c2-counter.py:309-311`), pin the
committer identity (`:336-337` / `:303-304`), and rmtree in `finally` (`:366` / `:334`). Both
selftests pass live (14 cases 1+13; 13 cases 1+12), matching the claims' stated counts. One
selftest-only nuance: c1's selftest reads the **worktree** xpin (`c1-counter.py:272`) while
`measure` uses the freeze blob (`:83`) — byte-identical today (§0), but a worktree drift would
make the selftest validate a different tool than live runs use.

**I6 — frozen rule vs `plans/round-36-claims.md` diffs.**

- The C1 counter adds conjuncts beyond the P36-C1 sentence — subject digest ==
  carriers.json sha256, `operation == extract_firmware` + provider `unblob`
  (`c1-counter.py:171-172` region), stored-id `ev_` prefix (`:179-180`), `entry_present`,
  `coverage_map_row`, `carriers_unchanged` — all stricter, safe-direction, and each corresponds
  to a red case enumerated in the claims.
- Claims prose says "13 red:" but enumerates **12** items: "oracle or carriers changed after
  freeze" is two separate code cases (`c1-counter.py` cases list, `oracle changed` and
  `carriers changed`). Totals (14 cases, 1+13) are correct and reproduce live; the enumeration
  compresses two.
- SOURCES.md parsing (`c1-counter.py:216-222`: 11 cells, `c[8]` opened, `c[10]` used-by split
  on `,`, exact `ENTRY` element match) matches the real table (verified rows S101–S103: bare
  unbackticked used-by paths, 11 cells). Format drift (backticks in used-by, `;` separators,
  escaped pipes inside cells → `len(c) != 11` skip) can only produce false negatives (honest
  stops), never a false green.
- `heading_range` stop rules differ per surface (`c2-counter.py:185` craft stops at `## ` so
  `###` subheads stay inside the range; `:186` adjacent stops at any `#`). Internally consistent
  for the stated-vs-observed comparison and covered by selftest red cases; noted only because
  the claims phrase "heading-to-last-non-blank-line ranges" does not pin the stop rule.
- The harness `/usr/bin/unsquashfs` hardpin (`c1-run.sh:47,63`) is the claims' frozen oracle;
  `oracle-run.json` records the version string but nothing compares it against 4.7.5 — oracle
  re-freeze discipline lives outside the counter (by design; the frozen oracle bytes are the
  TSVs).

**I7 — sasquatch receipt fields.** Before/after receipts record path, sha256 and version of the
resolved sasquatch (`c1-run.sh:76-78,84-87`); `-version` failure is swallowed to an empty string
(`|| true`, `:78`) — visible in the receipt, acceptable. Control spot-check: `controls/ctl-c1-0-do-nothing.out`
shows `met_target: false`, `carriers_unchanged: false`, exit 1 — consistent with the claims'
kill-rule precondition (full re-derivation is R36ReviewerControls' seat).

## 2. Residual risk and verification gaps

- I did not run the harness against the real K1–K4 carriers (covered by the R36ExecReproK1–K3 /
  R36ExecHarnessRun seats); the oracle's ELF-end arithmetic was verified on a synthetic 8 KiB
  fixture, and the before/after PATH logic on the sanctioned dev fixture.
- xpin column semantics (`f[1]`=stored, `f[2]`=6.5-rule id) were verified against the tool's own
  docstring (`xpin-attribute.mjs:8-11`) and the passing selftest, not against rea-agents 6.5.0
  source; note `--pkg67 pkg65` (`c1-counter.py:95`) intentionally points the unused 6.7 column
  at the 6.5.0 package — the compared column is the 6.5 rule, as claimed.
- No LSP server: findings rest on full-text review + behavioral probes, not semantic indexing.
- The "addendum §7 item 4" document itself was not located in the lane (only referenced in
  `w1-dispatch.json`); the named defect class (hardcoded /tmp) was reviewed directly.
  [INFERENCE: it is a wave/SOP addendum listing scratch-discipline items.]
- /tmp non-writes are evidenced by a before/after `/tmp` listing diff across two live REA runs
  plus code reading, not strace/inotify.
- Scratch `/fast/scratch/hyaku/kaidoku-r36/R36ReviewerHarnessCode` (fixtures, probe outputs,
  receipt copies) was removed after this report; nothing cited above depends on it, and no
  cited evidence lives under /tmp or scratch.
