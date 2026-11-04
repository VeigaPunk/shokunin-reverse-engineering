# SentinelScope — round-68 w1: scope, secret and provenance audit

**Surface.** The round's committed bytes `fcbe200f6739c38939e0dabf3f251de2cc6bd727..1eaf596e5f241762349fbd102c9e09ec1df18e3f`
(2 commits, 15 paths, 1720 insertions), the post-freeze commit `6ffa9ce1`, and the uncommitted `w1/` tree
(snapshot 2026-11-03T22:45-03:00). Read-only over the lane; per-check commands and raw readings are in
`w1/SentinelScope/audit.md`.

**Verdict summary.** Four of six checks PASS on the committed bytes; check 5 fails on three named
provenance defects (P1–P3 below), all in `.ufo/waves/round-68/l1/pre/`. No credential material, no scope
escape, no cache/scratch artifact, no pin drift, no fleet-root write by the lane. Nothing here changes a
claim predicate — P1/P2/P3 hit frozen atoms A2/A3/A6/A9, i.e. the container's own evidence contract, not
the after-arm scoring surface.

| # | Check | Verdict |
|---|---|---|
| 1 | every path touched is in-lane and in the round's write scope | PASS |
| 2 | no credential material in any committed byte of the round | PASS |
| 3 | `claims.json` instrument pins match the blobs at the freeze | PASS |
| 4 | no `__pycache__`/`.pyc`/scratch artifact committed | PASS |
| 5 | `l1/pre/` receipts: scratch paths, revision existence, instrument binding | FINDING P1, P2, P3 |
| 6 | fleet root untouched by this lane's seats | PASS (attribution inference noted) |

---

## P1 — the C2 before-arm and all six control arms are bound to instrument builds that never existed in git

**Severity: HIGH** (provenance of the only red→green evidence on the coverage axis).

**Evidence.**
- `l1/pre/c2-dryrun-at-base.json` → `instrument.sha256 = 7ee286c03391dc464c90a3f24498258bfef09dd89300aa9a246fd35ac85ef25c`.
- `l1/pre/c2-skiprun.json` → `instrument.sha256 = ff11d8ec27cbce94b4790041ed4e0dc4dfffa241cb243ece24e08491c415a302`.
- Frozen pin (`claims.json.instruments`, `git show 1eaf596e:tools/round-68/packed-elf.py | sha256sum`) →
  `48ef4c688a14faf381abbd2cc2b29061035f38c97815e2365957843433e5276e`.
- `git rev-list --all -- tools/round-68/packed-elf.py` → 4 commits (`6020eb60` on `main`, plus `6e190259`,
  `a32968ae`, `eea03ce5` on `hyaku/*` branches); every one carries blob `48ef4c68…`. Neither receipt hash
  ever entered the object store.
- No surviving copy: `find /fast/scratch/hyaku/kaidoku-r68 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo
  -name '*.py' | xargs sha256sum | grep -E '7ee286c0|ff11d8ec'` → no match; `find / -maxdepth 6 -name
  'packed-elf*.py'` → the committed file only.
- `l1/pre/controls-at-base.json` keys are `arms/base/control_arms/green/ok/schema` — **no instrument
  digest at all**, while `tools/round-68/controls.py:38` drives `tools/round-68/packed-elf.py` by path
  (`subprocess.run`), so the six arms were computed against whatever bytes sat on disk at 22:39, i.e. ~2 min
  before the frozen bytes were committed at 22:40:22 (committer time; the pre receipts' mtimes run
  22:36–22:39).

**Exploit path.** The container's atoms A2 and A3 present `c2-dryrun-at-base.json` and the six-arm controls
as measuring "the route". They measure a *draft of the route* that was then edited before commit. A builder
who greens a permissive draft and commits a stricter instrument gets: (a) a before-arm that cannot be
replayed — re-running the frozen instrument against the base tree today is a different observation, not a
reproduction; (b) do-nothing controls that were never executed against the shipped code, so the
"every shortcut is not met" property is asserted about bytes nobody ran. Symmetrically, a verifier who
tries to falsify the claim by replaying the pre receipts will get a different result from a different
program and cannot tell whether the receipt lied or the route was improved.

**Impact.** R68-C2's "0 → 2 carriers" story survives only on the after-arm; its red-side evidence (base
dry run) and its anti-shortcut evidence (six controls) are unverifiable artifacts. The predicate itself
does not require them, so this is not a predicate kill — but A2/A3 as written in the frozen container are
not established by the committed bytes.

**Smallest remediation.** Re-run the base dry run and the six control arms against the committed
instrument: `python3 -I -B tools/round-68/packed-elf.py --root <lane> --rev fcbe200f… --pkg <rea-agents>
--work <scratch> --json-out l1/pre/c2-dryrun-at-base.json` from `6020eb60`'s bytes, and add an
`instrument: {path, rev, sha256}` stanza to `controls.py`'s receipt. Two commands, two receipts, one commit;
no predicate change.

---

## P2 — every measured revision is the movable ref `main`, and `instrument.rev` is null in all three receipts

**Severity: MEDIUM** (reproducibility; A9 unimplemented).

**Evidence.** `grep -o '"rev": *[^,}]*' .ufo/waves/round-68/l1/pre/*.json` → `"rev": "main"` ×3 and
`"instrument.rev": null` ×3. `git reflog show main` → `main@{3}=fcbe200f` (the value at run time, 22:36)
but `main@{0}=6ffa9ce1` now; `git rev-parse main` → `6ffa9ce1…`. The frozen base sha appears in the pre
receipts exactly once, in `controls-at-base.json.base`, never as the census/route revision. A9 states
"receipts name both the measured revision (`rev`) and the revision that bears the instrument
(`instrument.rev`)" — the committed receipts do neither in a pinned form.

**Exploit path.** `--rev main` is evaluated against a ref whose meaning has already changed twice inside
this round (`1eaf596e`, `6ffa9ce1`). A receipt that says `main` cannot distinguish a base measurement from
a post-landing one: replay it today and the census reads a tree containing round-68's own two instruments.
Provenance is then reconstructed from `git reflog` — host-local, unreferenced, expirable — rather than from
the artifact.

**Impact.** The before-arm is not self-reproducible; a future auditor cannot tell whether
`c1-at-base.json`'s `scope_size 69` was measured at `fcbe200f` or at any later `main`. (Observation that
mitigates but does not fix it: the receipt's content is true of the base tree — both `unregistered` paths
exist at `fcbe200f`, all 12 `named_but_absent` are absent there, and the four counts match atom A1 exactly.)

**Smallest remediation.** Re-run both base arms with `--rev fcbe200f6739c38939e0dabf3f251de2cc6bd727` and
have the counters record `instrument.rev = git rev-parse --verify <rev>^{commit}` beside `instrument.sha256`;
that alone closes A9 for the two pre receipts and for every after-arm this round lands.

---

## P3 — `lock_recorded_not_pinned: true` with `lock_sha256: null`: the receipt asserts a recording it does not carry

**Severity: MEDIUM** (false-record shape; A6 unestablished).

**Evidence.** Both C2 receipts (`c2-dryrun-at-base.json`, `c2-skiprun.json`) carry
`"lock_recorded_not_pinned": true` and `"lock_sha256": null`. Frozen atom A6 requires the npx cache-level
lock "RECORDED (`lock_sha256`, `lock_recorded_not_pinned`) and never pinned (QUALITY #110)". The value is
obtainable on this host: the round-67 container already did the same exercise —
`.ufo/waves/round-67/claims.json:59` records that a fresh npx cache resolves the same `rea-agents 6.5.0`
artifact (`package.json sha256 a5003023…`, unchanged — I re-verified it live:
`sha256sum /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json` → `a5003023…`,
version `6.5.0`) with lock `815c18f1…`.

**Exploit path.** A boolean that says "recorded" plus a null is worse than an honest gap: an automated
reader (or a scribe quoting the receipt) concludes the cache lock is bound to the evidence. It is not. That
is exactly the surface that produced the round-67 M67-3 defect (an `npx -y` invocation rewriting the cache
lock behind a pinned receipt) — this round invokes `node <pkg>/scripts/rea.mjs` correctly, but its receipt
cannot prove which cache state it saw.

**Impact.** The C2 receipt overstates its own provenance; A6 is not established by the committed bytes, and
the instrument's `rea` stanza (`version`, `package_json_sha256`, `root`) is the only package binding.

**Smallest remediation.** Populate `lock_sha256` from the resolved `package-lock.json` under
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/.package-lock.json` (or the cache-level lock the
wrapper reads) in `packed-elf.py`'s receipt builder and re-emit the two receipts; if the lock is genuinely
unreadable, emit `lock_recorded_not_pinned: false` with a named reason instead of `true`.

---

## Observations on the passing checks (no action)

- **Scope (1).** All 15 range paths and all 4 post-freeze paths are lane-relative and round-68-scoped; the
  only non-round paths are `LOG.md` and `SCORECARD.md`, which are the lane's ledgers by rule
  (`AGENTS.md:4`) and by precedent (rounds 65–67 record commits), and both moved append-only
  (`9 0` and `24 0`, zero deletions). Modes are `100644`/`100755` only — no symlink, no gitlink. The
  `w1/` tree is untracked and nothing is staged (`git diff --cached` empty), so no seat touched the index.
- **Secrets (2).** Zero hits across 13 credential shapes, zero embedded-URL userinfo, zero env-dump
  shapes, all added blobs text (JSON/ASCII/UTF-8/Python) — no binary could be carrying material. The
  outside-lane paths present (`~/.agents/skills/godspeed/directive.md`, `~/.omp/agent/RULES.md`,
  `~/.npm/_npx/ad9a3fdbcad992c6/...`, `/run/user/1000/fnm_multishells/...`) are all already public in
  base-committed bytes (verified with `git log --all -S` and `git grep`), so no new private-path class
  entered the record.
- **Pins (3).** The three `claims.json` pins equal the freeze blobs, the working tree and `HEAD`; `main`
  touched `tools/round-68` only at `6020eb60`, which is an ancestor of the freeze; the claims blob is
  byte-identical at the freeze and in the tree (`ea65bf69…`) and was added exactly once (`1eaf596e`), so
  there is no amendment series and no undisclosed post-freeze instrument edit. Both frozen instruments pass
  their declared selftests at the declared counts (11 and 13 cases, `failed []`).
- **Caches (4).** No `__pycache__`, `.pyc` or `.pyo` in the range, in the round-68 tree, or in the
  untracked `w1/` snapshot.
- **Scratch paths (5, sub-check).** The one absolute scratch family under `l1/pre/`
  (`/fast/scratch/hyaku/kaidoku-r68/PackedDry/packed-98xah8q6/{jq,xxd}/…`) is the same class the lane
  already commits (round-67 receipts carry `/fast/scratch/hyaku/kaidoku-r67/…`), its leaf is an ephemeral
  work-dir suffix, and the tree is now empty. No foreign-lane path appears in `l1/pre/` at all.
- **Fleet root (6).** Fleet `LOG.md`/`SCORECARD.md`/`MANIFEST.json` are clean; the five dirty fleet entries
  are `after` (24 B, 20:05, a diff fragment), `.scratch/goal-20261103-hyaku-run15.md` (16:26),
  `.scratch/run13-state.json` (Oct 30), `.scratch/run15-kernel.py` (19:24) and `.scratch/run15-state.json`
  (22:41:24, hyaku run-15 orchestrator state listing lanes `revenger/tsukuroi/kama/tameshi/mado/kaidoku`).
  Four of five predate the round's first commit. The lane is a separate git repo the fleet does not track,
  so a lane commit cannot write fleet bytes. **Inference:** the 22:41 write is the fleet orchestrator that
  spawned this wave, not a kaidoku seat; no lane byte records a fleet-root write. Reported, not cleaned.

## In-flight landing surface (uncommitted, observed 22:48 — not covered by check 1)

While this audit ran, the L1's landing edits appeared in the lane worktree. They are **not** in the audited
range, so they change no verdict above; recorded because they are the bytes the round will commit next:

- `git status --porcelain` → `M PROVINCE.md` (+8), `M SKILL.md` (+4), `M corpus/QUALITY.md` (+2),
  `M corpus/README.md` (+4), `M corpus/SOURCES.md` (+1), `M corpus/claim-freezes-corrections.tsv` (+1),
  `M corpus/claim-freezes-v2.tsv` (+1), `M corpus/knowledge/2026-11-03-r67-avm-le-squashfs-core.md` (+24),
  `M tools/round-29/prefile-check.sh` (+26/−10), plus new `corpus/knowledge/2026-11-03-r68-packed-elf-route.md`
  and untracked `tools/round-68/registry-conformance.receipt.json`. This is the declared repair set
  (SKILL.md's four registry rows = atom A5's subject; the SOURCES row and the knowledge entry = the frontier
  step; the appended r67 correction = repair 1; the corrections tsv row = repair 2's QUALITY #100 companion).
- **Scope observation, not a finding.** `tools/round-29/prefile-check.sh` is a *cross-round* instrument
  edit: the diff retires `corpus/claim-freezes.tsv` as a gate input under a named erratum (`r68-1`) and
  replaces the round-24 gate call with a byte-identity assertion against a retirement pin
  (`legacy_sha=2a840d72…`). It is disclosed by container repair 4, but it edits an earlier round's tool,
  so it is outside the three `claims.json` pins and outside the "no instrument supersession at the freeze"
  atom's surface. If it lands it must be named as a repair in the round's LOG entry (repair 4 already
  declares the retirement), and a verifier should read the freeze-time "no supersession" claim as scoped to
  the three pinned instruments, not to the lane's whole tool inventory.
- **Timing hazard for the after-arm.** R68-C1's subject is `SKILL.md` itself (atom A5), and SKILL.md is
  currently modified-but-uncommitted. The census reads the registry at `--rev`, so the after-arm must be run
  at a revision that already carries the four rows; measuring the worktree or the freeze would read 73 rows
  and cannot reach `registry_rows 77`. The after-arm therefore has to follow the landing commit, and its
  receipt's `rev` must name that commit (P2's remediation applies here too).
- **Secret scan of the in-flight bytes — PASS.** `git diff` through the same 13 credential shapes → 0 hits;
  the only absolute paths are already-public classes (`/home/vgpnk`, `/fast/scratch/hyaku/kaidoku-r67/…`).

## Discipline

Observations above are from commands I ran read-only in this session; the one inference is labelled (fleet
`.scratch/run15-state.json` authorship). Unknowns carried forward: the content of the two pre-freeze
`packed-elf.py` builds (`7ee286c0…`, `ff11d8ec…`) and hence whether they differ materially from the frozen
route — unreachable on this host, and the reason P1 needs a re-run rather than a diff. No tool installed or
upgraded; no pacman transaction; no scratch dir created; no subagent; no git/jj mutation. The `w1/` snapshot
was taken while sibling seats were still writing, so it is a point-in-time view, not the settled wave tree.
