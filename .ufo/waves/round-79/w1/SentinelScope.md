# SentinelScope — round 79, wave 1: security and scope review of the two instruments and the wave bounds

Frozen inputs reviewed: base `29d2ca30b83a6a0d85b0aa979de0138fde1660e6`, freeze
`ed68cd0a6cc790cca342380a2d80d1927a668c8c`; at measurement time (`10:08–10:09`) the instrument
digests matched the frozen pins (`gate-mutation.py` `682f1e78…`, `pointer-bind.py` `91d23dad…`).
`pointer-bind.py` then changed in the worktree at `10:11:49` (F11). Every claim below was
re-measured in seat scratch; my four receipts reproduce the committed
`pre/c1-at-base.json`, `pre/c2-at-base.json`, `l1/scores/c1-at-landing.json` and
`l1/scores/c2-at-landing.json` byte-for-byte except the timestamp field.

Machine-readable receipt: `SentinelScope/sentinel-receipt.json`. Evidence: `SentinelScope/`
(`gm-base.json`, `gm-freeze.json`, `pb-base.json`, `pb-base-pathonly.json`, `pb-freeze.json`,
`c2-predicate-as-frozen.txt`, `receipt-field-inventory.json`, `wave-bounds-audit.json`,
`scratch-observation.json`, `working-tree-drift.txt`).

## Findings

| # | Severity | Surface | Finding | Smallest remediation |
|---|----------|---------|---------|----------------------|
| F1 | **HIGH** (frozen) | R79-C2 predicate/CLI contract | The frozen counting command and predicate — `pointer-bind.py:43-47`, `plans/round-79-claims.md:85-86`, `.ufo/waves/round-79/claims.json:22` and `:25` — omit `--battery`, but the pinned instrument's `main` (`pointer-bind.py:319-321`, sha `91d23dad…`) exits **2** with a usage line when `--battery` is absent. The verbatim command at the freeze writes no receipt and exits 2 (`c2-predicate-as-frozen.txt`), so the sentence "exits 0" cannot be executed as written. The measurement itself is sound: with `--battery` my runs give base 5/3/2/0 (exit 1) and freeze 5/5/0/0 (exit 0). **Worktree note:** an uncommitted edit landed at 10:11:49 (sha `3f07bd2a…`) makes `--battery` the default and the frozen command now exits 0; F1 stays open for the frozen text/pin until that edit is committed with a claims supersession (see F11). | Add `--battery` to the counting command and the predicate text (record edit by the L1), or make `--battery` the default when `--rev` is given. |
| F2 | LOW | pointer-bind digest scope | `line_sha256` is computed at `pointer-bind.py:105` **before** the token test, so a mismatched check still retains a sha256 of the live line at the stale line number (`omp-pin` :8, `kimi-pin` :4126 at base). Digest only, never bytes, so the security bound is met, but it is evidence for a line the check rejects. | Set `line_sha256` only once `matched` is true (or rename it and document it); one-line move. |
| F3 | LOW | gate-mutation scratch hygiene | `battery()` creates `tempfile.mkdtemp(prefix="gate-mutation-", dir=work)` (`:252`) and never removes it; there is no `shutil`/`rmtree`/cleanup in either instrument. Two runs left 436K + 400K, 9 files each (`pristine.py` + 8 mutants), under `--work`. With `--work` omitted, `main` (`:395`) creates a second unreaped `gate-mutation-work-*` in `TMPDIR` (else `/tmp`). | `try/finally shutil.rmtree(run_root)` (or keep on failure only) and remove the default work dir. |
| F4 | LOW | write-path containment | No containment guard exists for `--work`/`--json-out` (grep finds no `commonpath`, `is_relative_to`, `realpath`). A caller can point `--work` at the fleet root, `/tmp` or a sibling lane (`gate-mutation.py:251-252,395`; `--json-out` truncates any path at `:402-404` and `pointer-bind.py:329-331`). Not exercised outside the sanctioned scratch: the wave prompts pin the paths, so the round is unaffected; the risk is caller error, especially since seat tools start at the fleet root. | Reject paths outside an explicit allow-root (lane + seat scratch), or document that containment is the caller's. |
| F5 | INFO | receipt secret exposure | No field can carry a client-config line, an env value or a credential (full table below). The only pointed-line string appearing verbatim is the Ghidra `application.version=12.1.4` token — exactly the record's declared token (the pointed line is that 26-char string). The `.bashrc` range lines (111 chars) and the pin lines in the three client configs do **not** appear; only the pin, the key names and line digests. `gate-mutation` carries no file content, no env and no stderr on a normal run. | If the conditional `stderr_tail` is kept for a future target, store its sha256 and line count instead of the raw line. |
| F6 | INFO | provenance naming | `l1/scores/c1-at-landing.json` and `c2-at-landing.json` are untracked, timestamped `10:03:14` — **before** the `10:06:25` dispatch — and record rev `ed68cd0a` (the freeze), not a later landing commit. Their content equals my independent freeze runs exactly, so the measurements are genuine; the filename overstates. `freeze-audit-at-freeze.json` is likewise untracked but records round-79 `CLEAN`, `findings: []`, with the three instrument paths. | The L1 commits the scores at landing and notes that the landing rev equals the freeze rev for these instruments, or renames them `-at-freeze`. |
| F7 | LOW | digest semantics | `line_sha256` hashes decoded text (`open(..., errors="replace")`, `readlines`, join), so it is a raw-byte digest only for UTF-8/LF files; a CRLF or non-UTF-8 file would digest a normalised line. The five live files are UTF-8/LF, so the round's receipts are exact. | Read bytes, split on `b"\n"`, digest the raw slice; or state the normalisation. |
| F8 | LOW | `--rev` parsing | Both instruments interpolate `rev` into one argv as `f"{rev}:{path}"` (`gate-mutation.py:140-143`, `pointer-bind.py:68-71`) without validating it as a commit name; a leading `--` makes git parse the operand as an option. Not reachable from the wave (callers pass 40-hex); no execution path demonstrated. | Reject `--rev` unless `^[0-9a-f]{7,40}$`. |
| F9 | INFO | wave bounds | All three required bounds hold for all 12 seats (details below): write-only-lane, scratch root named, no seat told to commit. Report trailers and the dispatched task text are lane-contained. | None. |
| F10 | INFO | working tree outside evidence dirs | Uncommitted edits exist to `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, plus untracked `corpus/knowledge/2026-11-04-r79-mutation-and-pointers.md` and `corpus/lessons/round-79.md`, mtimes `10:05:56–10:09:04`, straddling the dispatch. No seat prompt authorizes writes outside its evidence dir; the L1 is the lane writer. Attribution is not establishable from local evidence. | The L1 should own/confirm these before landing; seats stay read-only on lane files. |
| F11 | **HIGH** | post-freeze instrument drift | `tools/round-79/pointer-bind.py` changed in the lane worktree at `10:11:49`, during this review: sha `3f07bd2a…` vs frozen pin `91d23dad…`, uncommitted. The diff makes `--battery` the default when `--rev` is supplied and rewrites the usage/docstring (it removes the F1 failure). Seat prompts reserve lane edits to the L1 ("Editing a lane file … is a blocking defect of your seat"); so either the L1 is landing the F1 fix (then `claims.json`'s instrument pin and the predicate text must be superseded) or a seat edited a frozen instrument (blocking defect). The frozen command now exits 0 on the worktree (`working-tree-drift.txt`), but the frozen text still omits the flag, so the frozen predicate and the worktree disagree until the L1 lands the pair. | The L1 owns it: commit the edit and update `claims.json` instruments/predicate, or revert it and repair only the predicate text. |

**Post-freeze drift.** The two instrumentation receipts I copied (`pb-base.json`, `pb-freeze.json`,
`pb-base-pathonly.json`) were produced at `10:08–10:09` from the pinned `91d23dad…` blob; the
worktree `pointer-bind.py` changed at `10:11:49`. My `gate-mutation.py` receipts are unaffected
(that file is still the frozen `682f1e78…`). The frozen-command probe in
`SentinelScope/working-tree-drift.txt` was re-run against the worktree and exits 0, which is
evidence of the fix, not of the frozen revision.

## 1. Receipt fields — secret-exposure review

Method: `grep -n 'json.dump\|receipt\['` on both instruments (29 matches), plus a field
inventory of the four measured receipts, a `KAIDOKU_ENV_CANARY` scan, and an in-memory
scan for every pointed line's stripped bytes. No config line, token or env value was printed
or written. Full verdicts: `SentinelScope/receipt-field-inventory.json`,
`SentinelScope/sentinel-receipt.json.receipt_fields`.

**gate-mutation** — all fields are constants, counts, case names, booleans, rev/digest
metadata of the tracked target, or mutant text. `target.{path,rev,bytes,sha256}` and
`target_pin.{expected,actual}` are metadata/digests only. `pristine.failed_cases[]`,
`mutants[].{id,edit,declared_case,failed_cases,apply_note}` carry no file or env content.
One conditional field:

- `mutants[].stderr_tail[]` — set only when the mutated copy emits no `SELFTEST` summary
  (`:283-284`); the last stderr line. Can carry the run_root scratch path; **cannot** carry
  config/env content in this target, because `attack-gate.py --selftest` reads no file and no
  env (selftest `:813-929` builds in-memory fixtures; the only `open()` is the battery-only
  `write_json` at `:692`). No guard. Recommend `stderr_sha256` + line count.

**pointer-bind** — `checks[].pointer` is the record's own pointer cell; `checks[].path` is that
cell expanded; `checks[].tokens[]` are the declared tokens only (`rea-agents@<pin>`,
`application.version=<value>`, `GHIDRA_INSTALL_DIR=`, `JAVA_HOME=`); `checks[].reason` names a
token and line numbers; `checks[].line_sha256` is the digest of the pointed lines. No bytes,
no env, no credential. `record.sha256` is the digest of the tracked `PROVINCE.md`.

Scan results (`marker_scan`): `KAIDOKU_ENV_CANARY` absent from all five receipts; no
`/fast/scratch/` path in any receipt; no `stderr_tail` on a normal run. Pointed-line byte scan:
only the Ghidra version line matches, and it equals the declared token; every other pointed
line has bytes that do not appear in any receipt.

## 2. Path/scope review — where the instruments write

| writer | path | escapable | guard / code path |
|---|---|---|---|
| gate-mutation | `--work <dir>` | **yes** | none — `:251 os.makedirs(work, exist_ok=True)`, `:252 tempfile.mkdtemp(dir=work)`; `--work /home/vgpnk/Projects/shokunin` would create `gate-mutation-XXXX/` in the fleet root |
| gate-mutation | default work dir | **yes** | none — `:395 tempfile.mkdtemp(prefix="gate-mutation-work-")` → `TMPDIR`, else `/tmp` |
| gate-mutation | `--json-out <file>` | **yes** | none — `:402-404 open(path,"w")`, any caller path, truncates |
| gate-mutation | mutant copies | no (relative to work) | two-level construction `mkdtemp(dir=work)/<id>.py`; escapes only if `--work` escapes; dir mode 0700; copies are the public tracked target |
| gate-mutation | `--root`, `--rev` | no (read-only) | `git -C <root> show <rev>:<path>` (`:142`), no write; no `shell=True`; no `rev` validation (F8) |
| gate-mutation | `--validate <file>` | no (read-only) | `open(..., "r")` (`:384-385`) |
| pointer-bind | `--json-out <file>` | **yes** | none — `:329-331 open(path,"w")` |
| pointer-bind | live files from the record | no (read-only) | `read_lines(expand(path))` (`:115-121`), digests the pointed lines only (`:105`) |
| pointer-bind | `--root`, `--rev` | no (read-only) | `git -C <root> show <rev>:PROVINCE.md` (`:70`) |

Both instruments are caller-trusted: no argument is untrusted data, and the wave prompts fix
`--work`/`--json-out` to seat scratch and lane evidence. There is no code-level lane guard, so
a mistyped relative path (seat cwd is the fleet root) is the realistic failure mode.

## 3. Scratch hygiene

`gate-mutation.py --battery` creates one `tempfile.mkdtemp(prefix="gate-mutation-", dir=work)`
per run and never removes it (no `shutil`, no `rmtree`, no `try/finally`; also left behind on
an uncaught error or the 300 s child timeout). Observed: two runs → `gate-mutation-93mrdjbj`
(436K) and `gate-mutation-h3edc72s` (400K), 9 files each. Consequence: scratch litter only —
the copies are the public tracked `tools/round-78/attack-gate.py`, inside a 0700 dir, no
secret. The round is not affected while every seat passes its own scratch as `--work` (all 12
prompts do): the driver's reaper can then delete `/fast/scratch/hyaku/kaidoku-r79/<seat>/`, and
the lane landing cleanup has nothing to remove because no artifact lands in the lane. If a
seat omits `--work`, the leftover goes to `TMPDIR` (else `/tmp`), which neither the reaper nor
the landing cleanup covers.

## 4. Child environment

`gate-mutation.py:253`: `env = {k: os.environ.get(k, "") for k in ("HOME","LANG","PATH","TMPDIR")}`.
Keys are exactly those four. `KAIDOKU_ENV_CANARY` and every credential variable
(`GITHUB_TOKEN`, `AWS_*`, API keys, `SSH_AUTH_SOCK`, …) are excluded because only the allowlist
is copied. The child is `[sys.executable, "-I", "-B", <copy>, "--selftest"]` (`:178`): isolated
mode, no shell, no `PYTHON*` inheritance, script directory not on `sys.path`. Values are
inherited verbatim (paths, not secrets); an unset key becomes `""`, not absent. Residual: a
future target selftest that echoed an env or config value could surface it, but this target
reads neither.

## 5. Wave bounds (`r79-w1-spec.json`)

`SentinelScope/wave-bounds-audit.json` audits all 12 prompts and the 12 dispatched tasks:

- `all_write_only_lane`: true — one `Write only under <lane>/.ufo/waves/round-79/w1/<seat>/.` per seat.
- `all_name_scratch_root`: true — `/fast/scratch/hyaku/kaidoku-r79/<your-seat-name>/` in every prompt.
- `no_seat_told_to_commit`: true — every `commit`/`push` occurrence is a prohibition
  ("never commit, push, stash or check out") or a noun ("committed bytes/receipts").
- `all_report_at_in_lane`: true — each `Report at` target is `<lane>/.ufo/waves/round-79/w1/<seat>.md`.
- `all_dispatch_prefix_match` and `all_dispatch_extra_contained`: true — each dispatched task is
  the spec prompt plus the lane-bounds/milestone/report trailer, with no `/tmp` or
  out-of-lane absolute path.

## Independent reproduction (counters reproduce; the frozen predicate text is defective per F1)

| run | result |
|---|---|
| gate-mutation base `29d2ca30` | mutants_total 8, killed 5, survivors 3 (`m03-near-miss-re-dead`, `m05-atom-absent-bound`, `m08-validate-no-refusal-guard`), `target_pin.matched false`, exit 1 |
| gate-mutation freeze `ed68cd0a` | mutants_total 8, killed 8, survivors 0, declared_case_hits 8, pin true, pristine 29 cases / 0 failures, exit 0 |
| pointer-bind base | checks_total 5, matched 3, mismatches 2 (`omp-pin`, `kimi-pin`), unparsed 0, exit 1 |
| pointer-bind base `--control path-only` | checks_total 5, matched 5, mismatches 0, exit 0 |
| pointer-bind freeze | checks_total 5, matched 5, mismatches 0, unparsed 0, exit 0 |

The instrument digests equal the frozen pins at measurement time; the target blob at the freeze
is `4e4baf00…` as pinned. No tool was installed or upgraded (no pacman transaction; PACMAN
paused host-wide). Scratch removed after the evidence copies were made.
