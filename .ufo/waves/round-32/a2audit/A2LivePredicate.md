# A2LivePredicate — static audit: C1 full-envelope committed equality excluding meta

Seat: `KaidokuR32A2.A2LivePredicate` (reviewer, leaf). UTC: 2026-10-23T06:59Z.
Scope: `tools/round-32/c1-arm64x-positive.py` committed-envelope clause (`committed_check`,
`first_added`, `strip_meta`, write-mode path). Lane rev at audit time `33393e594f1e278777fa49020b42c66ac4fa352e`
(work started at `f382e3b7`; integrator landed a2 controls mid-audit; no envelope files exist at
either rev: `git ls-tree -r --name-only HEAD -- corpus/evidence/round-32/c1/envelopes` → 0).
Instrument pins verified: `sha256(c1-arm64x-positive.py)=7a534be6…0f1a`, `sha256(arm64x_oracle.py)=17eea1f9…f686`
— both equal `claims.json` `instruments` entries. No carrier binaries were run; the only live REA
call was one `inspect` on the frozen probe DLL (non-carrier), identical argv to the counter.
Scratch: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2LivePredicate/` (sandbox git repo + `insp3.json` + probe scripts).
No tools installed (nothing needed beyond system git/python/npx).

## 1. Mechanism as implemented (vs. frozen predicate wording)

Predicate (claims.json:18): "committed envelope, first added after the freeze commit, equals the
live envelope in every field except meta, and the round-32 entry names that evidence_id."

- **First-added timestamp** — `first_added()` (counter:103-106) runs
  `git log <rev> --diff-filter=A --format=%ct -- <envelope path>` and takes `min()` of the
  committer timestamps. `freeze_ct` (measure:184-186) is the same query for
  `.ufo/waves/round-32/claims.json`. `committed_check` (counter:114-116) requires
  `added > freeze_ct` — a **committer-timestamp proxy for DAG ordering**, not ancestry.
- **Full-envelope equality excluding meta** — `strip_meta` (counter:65-66) drops only the
  **top-level** `meta` key; `committed_check` compares `strip_meta(committed) != strip_meta(live)`
  (counter:121-122) as Python object equality after `json.loads` (key order and whitespace are
  not compared). The committed bytes must be exact REA stdout, not a re-serialization with
  extra/missing fields.
- **Evidence id in entry** — `eid = live["data"]["evidence_id"]`; fails unless `eid` is a
  substring of the entry file at `--rev` (counter:123-125). `eid` is taken from the **live**
  envelope; equality already forces `committed.data == live.data`, so the committed id is the
  same value.
- **Before/after timing** — all state the check reads (`freeze_ct`, `entry_text`, PROVINCE,
  committed envelope) is read at `--rev` *before* the 12 live REA runs (measure:166-189), but
  `committed_check` is applied to each carrier *after* its live run (measure:199-201). Live
  output is never written anywhere in measure mode.
- **Write-mode exit 3** — under `--write-evidence` the committed clause is skipped entirely
  (`not write` guard, counter:199), envelopes are written to worktree only (counter:206-210),
  `runs.tsv` records `verdict_without_committed_clause` (accurate label — the clause is never
  evaluated in write mode), prints `WRITE-MODE ... not a receipt; no target line` and
  `return 3` (counter:211-218). The target line cannot be printed in write mode. Exercised by
  code reading; sibling seats exercise write mode end-to-end in sandboxes.

## 2. Probe evidence (exercised)

Sandbox: `git init` repo at `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2LivePredicate/repo`
(HEAD `cba2f937…`), freeze-analog committer time `T0=1792735426` (same value as the real
`9a73680a` claims.json add commit). All sandbox git used `git -C <abs>` with
`GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE` unset. `committed_check`/`first_added` were invoked by
importing the frozen counter module itself — same code path as production.

| carrier | scenario | `first_added` | `committed_check` | DAG-truth |
|---|---|---|---|---|
| k01 | add ct=T0+600 | 1792736026 | **True** (ok) | descendant of freeze — correct pass |
| k02 | add ct=T0 (same second as freeze), linear descendant | 1792735426 | **False** "not added after the freeze" | descendant — false fail |
| k03 | add commit backdated ct=T0−1800, linear descendant | 1792733626 | **False** | descendant — false fail |
| k04 | `git mv` rename (commit status `R100`), post-freeze | 1792736226 | **True** | descendant — pass |
| k05 | add commit on side branch ct=T0−600, merged post-freeze | 1792734826 | **False** | descendant — false fail |
| k06 | add on pre-freeze-rooted branch ct=T0−3000, merged post-freeze | 1792732426 | **False** | descendant — false fail |
| k07 | path added pre-freeze ct=T0−2900, content rewritten (M) post-freeze | 1792732526 | **False** | path add predates freeze |
| k08 | added pre-freeze, deleted, re-added post-freeze ct=T0+1500 | `1792736926 1792732626` → min 1792732626 | **False** | min() picks the dead add |
| k99 | absent | — | False "committed envelope absent" | correct fail |

Also exercised:
- `committed_check(root,"main","k01",live_with_different_subject.local_path/name)` →
  False "committed envelope differs from the live envelope (full comparison)".
- `committed_check(...,entry_text="no ids here")` → False "entry does not name ev_7ec576da9fb0…".
- `GIT_DIR=<lane .git>` + `git -C <sandbox> show main:envelope` → `fatal: path … exists on
  disk, but not in 'main'` → `show()` returns None → "committed envelope absent". `GIT_WORK_TREE`
  or `GIT_INDEX_FILE` alone: harmless (probe, git 2.56.0).
- Probe-envelope determinism (the frozen probe `x.dll`, sha256 `424777cb…`, non-carrier):
  `npx -y rea-agents@6.5.0 inspect /fast/scratch/hyaku/kaidoku-r32/probe/x.dll --format json
  --full-output` run from `cwd=/tmp`, exit 0, stderr 0 bytes, stdout 5240 B
  (`insp3.json` sha256 `507b2178…02c`). Against the two pre-freeze stored runs
  (`insp.json` `4eabbb60…b15`, `insp2.json` `dac0c759…697`): identical leaf sets; only
  `meta.duration` differs (6802ms / 7539ms / 7448ms); `strip_meta` equality holds across all
  three pairs; `data.evidence_id` identical (`ev_7ec576da9fb0f57cdf56bf26446cd7ef54c426093a98235d9710c487a68714e0`);
  `meta` contains exactly `{command:"inspect", duration:"<n>ms"}`.
- `evidence_id` derivation (REA 6.5.0 source,
  `dist/cli-runtime/reconstructionObligationLedgerSchemas-Bao0xMr-.js:557`):
  `ev_<sha256 of canonical JSON of semanticProjection>`; the projection's subject is
  `{digest, format, architecture}` — `local_path`/`name` excluded — and `parameters` is `{}`
  for inspect → evidence_id is path- and filename-independent and deterministic per
  (bytes, profile).
- Rename-arrival hypothesis **refuted**: `git log --diff-filter=A -- path` reports the
  destination `A` for a `git mv` rename (commit-level `R100`, pathspec-filtered `A`);
  `first_added` is correct.
- `document` naming is digest-derived (`target-<sha256[:12]>.dll` observed in
  `normalized_result.document`), filename-independent; `predictions.tsv` `document`,
  `segment_count`, `native_exports`, `ec_exports`, `opt` columns are never read by the counter —
  only `procedure_count` (measure:198). A stale `document` column cannot desync anything.

## 3. Findings

### F1 (medium) — "first added after the freeze" is a committer-timestamp proxy, not a DAG check; `min()` over all add events
`first_added` uses `%ct` and `added <= freeze_ct` fails. For the honest linear history the lane
produces this is fine, but it is a **commit-time** defect: a legitimate envelope data commit that
is a DAG descendant of `9a73680a` fails `committed_check` forever (the committed history is
immutable under reruns) when:
- the add commit lands in the **same wall-clock second** as the freeze commit (k02 — plausible
  for automation; here the gap was 375 s, no hazard realized);
- the add commit has a **non-monotone committer date** — backdating, `GIT_COMMITTER_DATE`
  inheritance, rebased/amended metadata (k03);
- the envelope is added on a **branch whose commit predates the merge** into the measured rev
  (k05, k06 — the check should be "the path did not exist at the freeze commit", not "the add
  commit's clock was later");
- the path had **any earlier add event** (deleted-then-re-added, or a stale placeholder at the
  same path rewritten post-freeze): `min()` selects the dead add and the path is permanently
  poisoned (k07, k08).

Symmetric hole in the other direction (not a rerun failure, noted for completeness): a path
committed *before* the freeze whose add commit carries a post-freeze committer date passes
`added > freeze_ct` — the timestamp test never proves ancestry. A correct implementation is
`git merge-base --is-ancestor <freeze_commit> <add_commit>` plus `git cat-file -e
<freeze>:<path>` failing — both cheap and deterministic. [INFERENCE: none of k02-k08 shapes
exist in real lane history (linear log, `git log --format=%h\ %ct` shows monotone committer
times); the defect bites only if the data commit is produced under clock games, merges, or
same-second automation.]

### F2 (low) — `GIT_DIR` (and friends) leak into the counter's own git calls; clean_env is asymmetric
`clean_env()` (counter:90-92) is applied only to the REA subprocess (counter:98). `git()`
(counter:56-57) inherits the caller environment. Probe: with `GIT_DIR` exported to a different
repository, `git -C <sandbox> show main:envelope` resolves the rev inside the foreign repo and
errors → `show()` returns None → every carrier reports "committed envelope absent" (exit 1).
`GIT_WORK_TREE`/`GIT_INDEX_FILE` alone do not perturb `show`/`log` (probe, git 2.56.0). The
run contract itself says sandbox git must run with `GIT_DIR` unset — the counter does not
guarantee it. If the measure argv is ever invoked by an orchestrator that exports `GIT_DIR`,
the rerun fails deterministically with a misleading reason.

### F3 (low) — git plumbing failures are misattributed to predicate failure
`first_added`/`show` ignore `git` returncodes (counter:104-105, 60-62). Any `log`/`show` error
(missing rev mid-history, env leak per F2, corrupt object) is reported as "committed envelope
absent"/"not added after the freeze" (exit 1) rather than the PIN-style environment failure
(exit 2) used for pinned inputs. An empty-but-parseable `log` output line would also raise an
uncaught `ValueError` in `int(x)` (counter:105). Same for `subprocess.run` `TimeoutExpired`
(counter:98, 600 s) and missing `npx` binary (`FileNotFoundError`) — crashes, not clean exits.
None of these are reachable on the frozen happy path; all make real failures harder to read on
rerun.

### F4 (observed-clean, residual risk) — full-envelope equality relies on run-to-run determinism of every non-meta field
`strip_meta` exempts only top-level `meta` (observed to be exactly `{command, duration}`).
Everything else is compared — including fields outside the oracle's predicate surface:
`data.subject.local_path`/`name` (absolute input path and basename — deterministic only because
`carriers.tsv` pins `/fast/scratch/hyaku/kaidoku-r32/carriers/kNN.dll` absolute paths; the PIN
sha check makes a relocated file fail at exit 2 before this clause anyway),
`data.normalized_result.string_count` and the whole `analysis_profile`/`limitations`/`provider`
blocks, `data.environment` (null), `data.evidence_id`. Three live probe runs show REA 6.5.0 emits
all of them deterministically for the probe DLL. Residual risk: any per-run nondeterminism REA
emits **outside** `meta` for the carrier binaries (e.g., a future `meta` nested under `data`,
host-stamped fields, timing strings inside `limitations`) breaks committed-vs-live equality on
an honest rerun and cannot be distinguished from tampering. Unexercised: real carrier envelopes
do not exist yet (envelope count at HEAD = 0) and this seat ran no carrier calls per
assignment; the probe covers only `x.dll`.

### Non-findings checked and cleared
- Document-name hazard: envelope `document`/`subject.name` are digest- or basename-derived and
  deterministic; the digest-derived `document` is what the oracle compares — file renames do
  not affect it (oracle:123; probe envelopes).
- `evidence_id` is content-derived, not random (three identical runs; REA source above).
- `predictions.tsv` `document`/`segment_count` columns are dead weight for the counter — no
  desync vector.
- Write-mode ordering: `runs.tsv` `verdict_without_committed_clause` is literally accurate;
  exit 3 can never print the target line (counter:211-218 vs 219-223).
- Rename-introduced envelopes are visible to `--diff-filter=A` (probe k04).
- `git show` text-conversion: no `.gitattributes`, `check-attr` unspecified → no eol/text
  mangling of committed JSON; even if enabled, `json.loads` equality absorbs whitespace diffs.
- `.ufo/waves/round-32/claims.json` has exactly one add commit (`9a73680a`, ct 1792735426) —
  `min()` over its log is unambiguous; claims-v3 freeze does not shift the C1 freeze clock
  (freeze rule keys the claims.json add commit itself, matching counter:184-186).
- At `--rev` preceding the data commit the check fails closed ("absent"), correct.

## 4. Bottom line

The clause is correct and honest on the lane's intended linear flow: committed envelope must
postdate (by committer clock) the claims.json add commit and equal the live run modulo `meta`,
and the entry must cite the deterministic `ev_...` id. The realistic rerun-breakers are all in
the timestamp proxy (F1) — same-second, non-monotone, merged, or re-used-path commits — plus the
`GIT_DIR` leak (F2) and reason-misattribution (F3). None can silently *pass* bad data; the
asymmetric acceptance hole (pre-freeze path + post-freeze date) is flagged for the record.

Residual risk / verification gaps: committed-vs-live equality never exercised on real carrier
envelopes (none committed; no carrier calls allowed); REA determinism beyond `meta` for carriers
is inferred from the probe, not proven; write-mode exercised only by code reading.
