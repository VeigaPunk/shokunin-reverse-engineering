# SentScope — round-48 w1 write-scope audit

Seat: SentScope (sentinel). Scope: write-scope of both frozen counters
(`tools/round-48/meanings.py` C1, `tools/round-48/record2.py` C2) and the shared
`tools/round-46/gate.py` they sit on. Method: read-only code audit of the frozen
bytes, then measured reproduction on a fixture fleet (`$S/fleet` with nested
`fx-shokunin` and `sib-shokunin` repos mirroring the real layout). Nothing was
written to the lane tree; every lane-path answer was measured through the pure
`gate.out_path()` function. Receipts: `.ufo/waves/round-48/w1/SentScope/all.jsonl`
(each entry = tag, exact command, exit code, stdout sha256, UTC). Fixture lane
carried the real `plans/round-48-claims.md` + all four frozen tools at
`FREEZE=8bab2b7a…` and a tip commit `TIP=9d62b983…`.

## Headline answers to the three assigned questions

1. **Can `--json-out` write inside the graded bytes or outside the lane?** YES to
   both, without any race. `gate.out_path()` bounds the write by
   `realpath(--root)` — and `--root` is caller-chosen, never validated to be a
   git worktree or the lane. `--root=<fleet>` ⇒ writes inside the lane's FROZEN
   `tools/round-48/` and inside `SCORECARD.md` (measured, F1). `--root=/` ⇒
   writes any absolute path on the filesystem (measured, F2).
2. **Can a fixture repo be created outside scratch?** The counters never create
   fixture repos at all — both `run_battery` functions mutate card/skill text in
   memory only (`git status` clean before/after; W8s). The only filesystem
   creation is `gate.scratch()`/`tempfile.mkdtemp` in `--selftest`, confined to
   `HYAKU_SCRATCH`/`TMPDIR` — which *does* accept the lane itself (F8).
3. **Can a counter read or write a sibling lane or the fleet repo?** WRITE: yes —
   `--root=<sibling>` writes into the sibling (measured: `.ufo/state/corrupt.json`
   created, W4); symmetrically a sibling seat wedges THIS lane without ever
   naming it as `--root`. READ: every artifact read is `git -C <root> show
   rev:path`, bounded to `--root`'s object store; `--root=<sibling>` happily
   reads/scores that repo, and receipts carry **no `root` field**, so receipts
   are repo-indistinguishable (F10).

## Findings (severity / exploit / evidence / impact / smallest remediation)

### F1 HIGH — fleet-root `--root` puts a write inside the FROZEN `tools/round-48/` ⇒ permanent round wedge
- Exploit: `python3 tools/round-48/meanings.py --root <fleet> --freeze <F> --rev <R>
  --json-out <fleet>/kaidoku-shokunin/tools/round-48/wedge.json`. `out_path`
  computes rel `fx-shokunin/tools/round-48/wedge.json`, head `fx-shokunin` ∉ GRADED
  → allowed. The counter exits 2 (`unknown freeze revision`) — **but `gate.emit`
  runs regardless**, so the write lands on a failed verdict.
- Evidence (receipts W1b/W1c): write exits 2, file `tools/round-48/wedge.json`
  exists, `git status` shows `?? tools/round-48/wedge.json`; the next lane-root
  run returns exit 2 `frozen_worktree_dirty`, `dirty:["tools/round-48/wedge.json"]`.
  Identical for `record2.py` (W5). Recovery needs a manual `rm` (W1d).
- Impact: any seat (or any script, nothing authenticates the caller) wedges BOTH
  claims for every later run — a silent availability kill on the whole round.
  Same primitive overwrites `SCORECARD.md`, `.ufo/waves/**` committed receipts.
- Remediation: bound `out_path` to the lane root derived from the counter's own
  `__file__` (`realpath(join(__file__,"../../.."))`), not to `--root`.

### F2 HIGH — `--root=/` (or `$HOME`, `/fast`, any ancestor) ⇒ `--json-out` writes anywhere
- Exploit: `--root / --json-out /any/absolute/path`. `commonpath([full, "/"]) ==
  "/"`; rel head never in GRADED → write lands. Evaluate's exit-2 doesn't stop it.
- Evidence W2: `$S/outside-lane.json` created, exit 2 `unknown freeze revision`.
- Impact: full unbounded write primitive riding the frozen instrument. Also means
  `--root=<sibling-lane>` (F4) and `--root=<fleet>` (F1) are the same bug.
- Remediation: require `git -C root rev-parse --show-toplevel == realpath(root)`
  AND that toplevel to be the counter's own lane (see F1).

### F3 HIGH — `.git`, `.jj`, `.ufo` are writable heads: repo corruption + evidence + state tampering
- Exploit: `--root <lane> --json-out <lane>/.git/refs/heads/main`. `.git` ∉ GRADED.
- Evidence W3: after the write, `git rev-parse main` → exit 128
  `ignoring broken ref`, `rev-parse HEAD` → fatal. The lane repo is corrupted
  in one flag. `gate.out_path` verdict table on the REAL lane (W7r, pure
  function, no write performed): WRITE allowed for `.ufo/state/corrupt.json`,
  `.ufo/watchdog.log`, `.git/HEAD`, `.jj/repo/store/x`,
  `.ufo/waves/round-48/controls/ctl-c2-0-do-nothing.json` (a committed control
  receipt), `MANIFEST.json`, `.gitignore`, `.scratch/x`, `.tower/x`…;
  REFUSED correctly for `SKILL.md`, `tools/round-48/x`, `plans/x`, `corpus/x`,
  `evidence/x`, `LOG.md`.
- Impact: `.ufo/state` + `.ufo/watchdog.log` are contract-forbidden for seats
  yet instrument-permitted; `.ufo/waves/**` holds 37,047 tracked files outside
  GRADED incl. `.ufo/gates/*.py` (other instruments' code) and every committed
  score receipt — all overwriteable, and `dirty()` won't flag them (outside the
  frozen pathspecs), so the overwrite is invisible to the counters.
- Remediation: refuse any `--json-out` whose resolved path has a `.`-prefixed
  component (covers `.git/.jj/.ufo/.scratch/.tower`) outside an allowlist
  (`.ufo/waves/round-<N>/w<M>/` at most); add `evidence`'s siblings explicitly.

### F4 MEDIUM — sibling-lane writes (cross-lane)
- Evidence W4: `--root $SX --json-out $SX/.ufo/state/corrupt.json` → exit 2, file
  created. Conversely this lane's files are writable from a sibling `--root`
  only via an ancestor root (F1) — but that ancestor is trivially `$HOME`.
- Remediation: as F1 — the write boundary must be the counter's own lane.

### F5 MEDIUM — TOCTOU between `out_path` realpath and `emit` open
- `out_path` resolves symlinks at argv-parse; `emit` opens the *string* after a
  full `evaluate` (freeze_state runs ~10 git subprocesses). Measured W9: validate
  `d.ok/x.json`, then `os.rmdir(d); os.symlink(escape, d)` → `gate.emit` lands at
  `$S/escape/x.json` — outside the lane, through the checked path.
- Impact: escapes even a fixed boundary if any path component is seat-mutable.
- Remediation: re-realpath the parent in `emit` immediately before `open`, and
  `os.open(..., O_NOFOLLOW|O_CREAT|O_WRONLY)`.

### F6 MEDIUM — `census2.py --out` has no guard at all (frozen C1 census generator)
- Evidence W12: `--root $FX --rev HEAD --out $S/census-escaped.json` exits 0 and
  writes outside the lane; `--out $FX/SKILL.md` overwrites SKILL.md with census
  JSON (verified by `head`, then fixture-restored). `--rev WORKTREE` also reads
  worktree files directly.
- Impact: the frozen artifact-generation tool is an unrestricted write primitive
  over the graded surface — and it's part of the C1 claim surface.
- Remediation: route `--out` through the same boundary check; or drop `--out`.

### F7 LOW — `--json-out` naming a directory crashes (traceback, exit 1) instead of verdict 2
- Evidence W10: `--json-out $FX/.ufo` → `IsADirectoryError` traceback, exit 1.
  `gate.main_guard` wraps `evaluate` only, not `emit`; the docstring's "unhandled
  exception is a defect, never a verdict" is violated at the emit edge.

### F8 LOW — `gate.scratch` accepts the lane (or a sibling) as TMPDIR
- `scratch()` refuses bare `/tmp`,`/var/tmp` (measured W8b) and requires a root —
  but any non-temp dir passes, including the lane: `TMPDIR=<lane>` ⇒
  `mkdtemp(<lane>/probe-*)` inside the worktree (W8r; selftest then rmtree's it,
  W8s leaves clean status). `TMPDIR=<lane>/tools/round-48` would wedge via
  residue if the process is killed before rmtree; `TMPDIR=<sibling>` is a
  transient cross-lane write.
- Remediation: refuse scratch roots inside the measured lane or any `*-shokunin/`.

### F9 LOW (latent) — `record2.oracle()` exec gives the round-47 oracle a CWD-relative import scope
- `oracle()` sets `ns["__file__"]="tools/round-47/record.py"` (relative). The
  exec'd module then runs `sys.path.insert(0, dirname(abspath(__file__)))` →
  prepends `<CWD>/tools/round-47` and `<CWD>/tools/round-4[6-7]` (W11 measured).
  Harmless today: `gate` is already in `sys.modules` when the oracle's
  `import gate` runs, and a normal CWD has no `tools/round-47/`. But any lazy
  import added later to `record.py` resolves CWD-first → shadowed-module risk.
- Remediation: `ns["__file__"] = os.path.join(realpath(root), ORACLE)`.

### F10 LOW — receipts carry no `--root`/worktree binding
- A green receipt generated against a private fixture repo is indistinguishable
  from a lane receipt; only embedded `freeze`/`frozen_derived` values tie it to
  the lane's claims (partial mitigation — a forger would replay the same commit
  ids inside a fixture). Worth a `root`/`lane` field in `emit` receipts.

## Clean surfaces verified (measured, not inferred)

- GRADED enforcement works **when `--root` is the lane**: `SCORECARD.md`,
  `SKILL.md`, `plans/`, `tools/`, `corpus/`, `evidence/` all refused (W2/W7r).
- Outside-root refusal works: fleet root refuses `$S/refused.json` (W2).
- `run_battery` (both counters) is in-memory: no fixture repo, no FS writes.
- `/tmp` scratch refused (W8b); selftest cleans its mkdtemp (W8s status empty).
- `census_rederive` execs `census2.py` as `census2_mod` → `__main__` CLI/subprocess
  never runs; no sys.path insert → no import hijack through that path.
- `record2` reads: SCORECARD.md, `.ufo` receipts, oracle bytes — all via
  `git show <rev>:<path>` (committed bytes, repo-bounded). `receipts_at` paths
  come from card text but resolve through `git show` — cannot escape the repo.
- Relative `--json-out` resolves against CWD, not `--root` (W7c) — refuses when
  CWD is outside the lane; consistent but worth noting for seat invocations.

## What a seat could exploit, ranked

1. F2: `--root /` → write anywhere. One flag, no setup.
2. F1: `--root <fleet>` → wedge both round-48 claims (`frozen_worktree_dirty`) or
   overwrite `SCORECARD.md`/committed receipts.
3. F3: corrupt the lane repo (`.git/HEAD`, `.jj/`) or `.ufo/state`.
4. F5: symlink-swap an approved `--json-out` path mid-evaluate → outside-lane write.
5. F6: `census2.py --out` → same graded-byte overwrite without needing `--root`
   tricks.
6. F8/F9/F10: residue, latent import shadowing, receipt provenance.

## Install record
None — system python3 3.14.8 + git only. pacman untouched (host pause honored).

## Contract compliance
Lane tree untouched (all writes hit `$S/fleet` fixtures or `out_path` answers in
memory; `git status` on the real lane never invoked for mutation). Fixture repos
lived under `$S` only. No commits outside fixtures. Scratch `$S` removed after
receipts copied to `.ufo/waves/round-48/w1/SentScope/`.
