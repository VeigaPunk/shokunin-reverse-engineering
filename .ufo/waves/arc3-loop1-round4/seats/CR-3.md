# CR-3 — critic seat, chain c3, wave arc3-loop1-round4

Seat: **CR-3** · chain **c3** · role **critic** · date 2026-10-19
Task (frozen): attack the sidecar guard and the mkdir guard (symlinked parent?
relative trickery? race?) — scratch only. Also: does distinct-path counting break
any v1 shape?

All work on scratch copies under `/dev/shm/cr3-r4/`. **No custody path was written**
by this seat: every custody-path vector ran against a sandbox `HOME`
(`/dev/shm/cr3-r4/atk-*/home`), never the real `~/.bashrc`, `~/.profile`,
`~/.kimi-code/config.toml`, `~/.omp/agent/mcp.json`,
`~/.config/devin/mcp_config.json`. Custody paths were only ever `stat`/`sha256`
-read.

## 1. Work performed (evidence pointers)

Identity (rule #14), all re-derived at write time — `evidence/identity-manifest.txt`:

| artifact | sha256 (16) | note |
|---|---|---|
| tool at first snapshot | `7cd19c3cfd835c78` | r3 landed revision; selftest `CLEAN cases=22` |
| tool at re-snapshot | `29bb45ae0fd795e5` | **EX-21 landed mid-run**; selftest `CLEAN cases=28` |
| `tool-N1.py` | `dd9954dc4dea192a` | neighbour-inode fix |
| `tool-N2.py` | `fdb115c3b08999c3` | + non-regular-target fix (FIFO) |
| `tool-N3.py` | `e6fce2eedc468da5` | + resolved-name neighbour derivation |
| `tool-N4.py` | `7891fcb25881d8ad` | + fd/post-open-identity atomic write |

Live revision is `29bb45ae…` at write time; README `9d9400da…`.
Every variant was re-selftested after each revision: **22/22** on `7cd19c3c…`,
**28/28** on `29bb45ae…` and on N1–N4.

Six attack batteries, all scratch, all re-runnable from `evidence/`:

- `evidence/atk.py` modes A/B/C — sidecar guard, mkdir classes, symlinked parent
  and relative trickery. Outputs `out-A-*.txt`, `out-B-*.txt`, `out-C-*.txt`.
- `evidence/atk2.py` — battery D: symlinked-parent/`..`/relative vectors aimed at
  the five custody paths. Output `out-D-*.txt`.
- `evidence/atk3.py` — battery E: attacks on the **round-4 landed** guard
  (neighbour inode arm, FIFO/ELOOP/loop classes). Output `out-E-*.txt`.
- `evidence/atk4.py` — battery F: spelling-dependence of the neighbour guard.
  Output `out-F-*.txt`.
- `evidence/sidecar-race2.sh` — the sidecar-guard race probe (swapper thread
  atomically retargets the derived sidecar path between a safe file and the
  sandbox custody file while `capture` runs). Outputs `out-race-*.txt`.
- `out-v1.txt` — the v1-shape probe (original vs distinct-path-patched tool).

Reproduction entry points (scratch only):

```
python3 evidence/atk3.py patch/tool-r4-29bb45ae.py      # E-battery on the landed revision
bash    evidence/sidecar-race2.sh patch/tool-N4.py 1200 "N4"   # race probe
```

## 2. Proposed changes

Patch texts (patch-text only — this seat never writes the real target; EX-21 owns
`.ufo/gates/custody-pair/`):

- `patch/diff-N1.patch` — neighbour set gains the **inode arm** (one line + one list).
- `patch/diff-N2.patch` — N1 + a declared class for a **non-regular `--out`**
  (FIFO/device/symlink loop) so `capture` cannot block forever.
- `patch/diff-N3.patch` — N2 + derive the neighbour from the **resolved** name so
  a directory-spelled measured path (`--paths .`) still yields its real neighbour.
- `patch/diff-N4.patch` — N3 + **atomic write**: `os.open(O_NOFOLLOW|O_NONBLOCK)`,
  post-open `os.fstat` identity check against the guarded inode set, `ftruncate`,
  write through the fd. Closes the check-vs-use window; also refuses a symlinked
  `--out` outright (fail-closed).
- Runnable variants `patch/tool-N1.py` … `patch/tool-N4.py` (each selftest CLEAN).

Recommendation: **N4** if the parent wants the residual closed in this round;
**N1** is the minimal one-line close of the highest-value residual (the neighbour
inode bypass), and N1 alone changes no existing selftest verdict.

## 3. Before → after measurement (C3 claim)

The frozen C3 claim's residuals (a)-(c) plus (d). Measured before = r3 landed
`7cd19c3c…`; after = r4 landed `29bb45ae…` (EX-21) — then attacked again.

| residual | before (`7cd19c3c`) | after (`29bb45ae`) | CR-3 verdict |
|---|---|---|---|
| (a) sidecar not scope-checked | exit 0, measured file's `.sha256` destroyed (`out-A-new` A1/A2 on r3: `CLOBBERED=True`) | **exit 2**, neighbour intact | **closed** |
| (b) `out.parent.mkdir` outside the try | traceback exit 1 on 5 parent shapes (`out-B-new` B1-B6 on r3) | **exit 2, no traceback**, all shapes | **closed** |
| (c) gate counts stanzas | 5 duplicate stanzas passed `--require-paths 5` silently (`out-v1.txt`) | `REFERENCE-COVERAGE: 1/5`, **exit 2**; USAGE line says "5 distinct paths" | **closed** |
| (d) both-sides-absent MATCH | MATCH, exit 0, no note | MATCH exit 0 **with the declared ruling note** printed | **adjudicated + documented** |
| selftest | 22 cases | **28 cases**, CLEAN | matches the claim's ≥24 |

New residuals CR-3 measured **on the landed r4 revision** (`out-E-new`, `out-F-new`,
`out-race-new`), none of which the frozen claim names:

| # | class | measurement on `29bb45ae` |
|---|---|---|
| R1 | neighbour **inode** arm missing | E1/E2/E3 exit **0**, neighbour destroyed; E10 destroys a custody neighbour `~/.bashrc.sha256` |
| R2 | neighbour derived by **string concat** | `--paths .` + `--out ../dir.sha256` → exit **0**, real neighbour destroyed (G2/G3) |
| R3 | **non-regular `--out`** | FIFO with no reader: `capture` **never returns** (E5, `HANG`) |
| R4 | **check-vs-use race** | sidecar guard defeated **56 / 1200** iterations, every hit exit 0, custody file overwritten with the sidecar line |

R4 measured against the landed revision and my own fixes:

Symlink-swap probe (`sidecar-race2.sh`; the sidecar path becomes a symlink to the
custody file):

| variant | hits / iterations |
|---|---|
| RV-8 patch text (`tool-S`) | 0 / 400 (window not observed at that length) |
| **r4 landed `29bb45ae`** | **56 / 1200 — RACY** |
| CR-3 N3 (path/inode fix, still check-then-use) | 70 / 1200 — RACY |
| **CR-3 N4 (fd + post-open identity)** | **0 / 1200** (refusals 1200/1200) |

Hardlink-swap probe (`hardlink-race.sh`; the sidecar path is atomically replaced
by a **hardlink** to the custody file — the case `O_NOFOLLOW` cannot catch, so it
isolates the post-open `fstat` layer):

| variant | hits / iterations |
|---|---|
| **r4 landed `29bb45ae`** | **97 / 600 — RACY** |
| CR-3 N3 (path/inode fix, still check-then-use) | 64 / 400 — RACY |
| **CR-3 N4 (fd + post-open identity)** | **0 / 600** |

The hardlink probe is the decisive one: it defeats both the landed revision and
the check-then-use fixes, and only N4's post-open `fstat` identity check survives.

Fix validation: N1 → E1/E2/E3/E10 exit 2, files intact. N2 → E5 exit 2, no hang.
N3 → G2/G3 exit 2, neighbour intact. N4 → all of the above and 0/1200 race hits;
selftest CLEAN 28/28 at every step. No control regressed: batteries A/B/C/D on N4
give the same verdicts as the landed revision except the intended refusals.

**v1-shape answer (the seat's second question): no.** Distinct-path counting
breaks **no** v1 shape. On 9 v1 fixtures (sums 1-path, sums 5-dup, sums 2-distinct,
sums 2-of-5, sums symlink+target, stanza 1, stanza 5-dup, pipe 1, pipe 5-dup) the
bare `verify` (no `--require-paths`) output is **byte-identical** between the r3
and r4 revisions — 0 diff lines on every fixture, same exits (`out-v1.txt` §1).
Only the opt-in gate changes, and there the change is the fix: duplicate padding
now reads exit 2 (`out-v1.txt` §2). One declared tightening: a reference carrying
symlink+target of the same file counts as **one** resolved path, so
`--require-paths 2` on that pair now exits 2 — correct under the gate's own
"distinct resolved paths" basis, but it is a behaviour change a caller could
notice, and the README's reference-coverage section should say so.

## 4. Attacks / refutations attempted (verdicts)

Battery A (sidecar) on the landed revision — 6/6 refused, no clobber. **Refuted.**
Battery B (mkdir/traceback) on the landed revision — 6/6 exit 2, no traceback.
**Refuted** (B8/FIFO survives — carried into R3).
Battery C/D (symlinked parent, relative `..`, hardlink, symlink chains, grandparent
links, `..` through a symlinked dir, deep-cwd climbs) — 15 vectors, all refused,
zero custody files touched. **Refuted**: the out-side guard holds.
Battery E (neighbour inode, non-regular targets) — E1/E2/E3/E10 bypass, E5 hang.
**Confirmed** (R1, R3).
Battery F (neighbour spelling) — F1-F5 refused (pathlib normalises `X/.`, `X/`,
`./X` to `X`), F7 **refuted as a false positive of my own battery** (the measured
path there is the directory `.`; `X.sha256` is not its neighbour — verified by
re-deriving the resolved name, `out-F-new.txt` + the F7b control, which refuses
correctly). G2/G3 **confirmed** (R2).
Race probes — R4 confirmed twice: symlink-swap **56/1200** and hardlink-swap
**97/600** on the landed revision. N4 **refuted both** (0/1200 and 0/600); N3
refuted neither (70/1200, 64/400), which is what makes N4's post-open `fstat`
layer the load-bearing one rather than the path checks.
Battery A re-run on N1/N2/N3/N4 — no regression.

Also probed and refuted: the RV-8 patch text's own new bug (moving `with_name`
before the try makes `--out .` a `ValueError` traceback at exit 1, where the
original exits 2 cleanly — `tool-S` vs `7cd19c3c`). EX-21's landed revision does
**not** have this bug (it wraps `with_name` in its own try); recorded so the
parent does not re-derive it from the RV-8 text unexamined.

## 5. Blockers

None for this seat. Two honesty notes for the parent:

1. The race probes' 0/1200 and 0/600 on N4 are **negatives at a bounded sample**,
   not proofs of atomicity. The construction removes the check-vs-use window by
   checking `fstat` on the opened fd and writing through it, but the parent should
   treat the runs as evidence, not certification. The probes race the *sidecar*
   path; the receipt path was raced in r3 by CR-4.
   Note the `refusals=1200 allowed=0` line in the symlink run: under a pure
   symlink swapper N4 never even reaches the write, because `O_NOFOLLOW` refuses
   the link — the hardlink run is what actually exercises the `fstat` layer
   (`allowed=60` there, 0 hits).
2. R1-R4 are measured on `29bb45ae…` only. If EX-21 lands another revision, R1/R2
   (and the N1-N4 patch texts) must be re-derived against the new sha256 before
   the parent applies anything — this seat's diffs are against `29bb45ae…`.
