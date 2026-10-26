# R36W2SentinelHygiene — hygiene and misroot audit (read-only)

Seat: `R36W2SentinelHygiene`, leaf, wave 2. Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Nothing in the lane, the fleet repo or
`/home/vgpnk/Projects/shokuknow` was moved, deleted or edited; the only file written is this report.
No VCS mutation, no installs, no subagents, no background jobs.

Pinned for every check below: freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0`, base
`cab59f221fe19726b5692bfa4d9a9679e96b8a73`, integration tip `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930`
(all three resolve: `git cat-file -t` → `commit`). Lane HEAD at audit time was **`6f2ba761`**, one
commit past the integration tip (see §5).

---

## Verdict

| item | result |
|---|---|
| 1. untracked fleet-root files naming kaidoku round 36 / an R36 seat | **2 files** (`.scratch/goal-20261026-hyaku-run8.md`, `.ufo/state/inline-dispatcher.log`). **0** name an R36 seat id. Neither is a misroot. |
| 2. `/tmp` entries created today mentioning kaidoku/r36 | **8 files** (6 by filename, 2 by content only). All wave-2/round coordination scratch; **no secrets**, but `frozen_expect.txt` is an unauthenticated copy of the frozen blob set (§3.2). |
| 3. committed lane files with absolute `/tmp` paths cited as evidence | **No new one this round in the pinned path set** (`corpus`, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`): 0 added `/tmp` lines. **One pre-existing live dangling pointer remains at the tip**: `corpus/lessons/round-35.md:21` (§2.1). This round's only new `/tmp`-bearing committed file is `tools/round-36/selftest/dev-after.json` (§2.2) — inert for every counter, but outside the pinned path set. |

No fabrication, no forged readiness, no live-access claim found. No frozen predicate, counter,
carrier or oracle was touched (and none was changed after the freeze — §4.3).

---

## 1. Untracked fleet-root inventory

Command: `git -C /home/vgpnk/Projects/shokunin status --porcelain -uall` → **214 untracked entries**
(152 under `.tower/`, 39 under `.ufo/`, plus one entry per lane repo). Content was grepped for
`kaidoku`, then intersected with `round-36|R36|<digits>36`.

### 1.1 Qualifying files (content names kaidoku round 36)

```
.scratch/goal-20261026-hyaku-run8.md   3613 B
  L1: <!-- ORCHESTRATOR-OWNED run state (hyaku run 8). Not a misroot: lanes and seats never move, copy-then-delete, or edit this file. -->
  L2: # hyaku run 8 — inline swarm rounds toward round 100 (2026-10-26)
  L45: - Block A: tabi (29, fresh-start), souji (30), kasegi (33), kaidoku (36, fresh-start), kengaku (37),

.ufo/state/inline-dispatcher.log       50530 B, 93 matching lines
  L1: 2026-10-26T01:05:36 run8-skip-stale-ready /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-36/falsify.ready
  L87: 2026-10-26T01:26:46 partial kaidoku 36 w1 4 43
  L88: 2026-10-26T01:26:46 cap-defer /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-36/w1.ready occupied 98
  … (partial/cap-defer pairs through `occupied 116`, then settle lines)
```

Assessment: both are fleet-level orchestration state that *names* the lane; neither is lane content
stranded at the fleet root, and the goal file self-declares orchestrator ownership. Not a misroot.

**Round-number collision (informational).** `inline-dispatcher.log:1` shows
`kengaku-shokunin/.ufo/waves/round-36/falsify.ready` — a *different lane* is also at round 36 today.
Any fleet-level glob of `*/.ufo/waves/round-36/` conflates kaidoku 36 with kengaku 36; the
dispatcher itself keys on `lane round wave` (`partial kaidoku 36 w1 4 43`) and is correct.
`cap-defer … occupied 98…116` records that the fleet concurrency cap throttled this lane's w1
dispatch; w1 still settled 43/43 (§5).

### 1.2 R36 seat ids in untracked fleet-root files: none

`grep -coE 'R36(W2)?[A-Z][A-Za-z]+'` over every untracked regular file <3 MB → no hits. The 43-name
roster appears only under `/tmp` (§3), not at the fleet root.

### 1.3 Negative / calibrated noise

- `?? kaidoku-shokunin/` in the fleet status is the lane's own git repo, untracked at the fleet root
  exactly as 20 sibling lane repos are (21 such `?? <lane>-shokunin/` entries, one each) — uniform
  layout, not a misroot.
- `.ufo/watchdog.log`, `.ufo/state/*.report-baseline`, `scripts/hyaku/hyaku.env`,
  `scripts/hyaku/lane-addendum.md` are *modified tracked* fleet files (` M`), outside this seat's
  untracked criterion; not inspected further (lane-external, operator territory).
- `.tower/comms/*` matched an over-broad `36` token but **none** matches `R36[A-Z]|round-36`
  (`grep -rlE 'R36[A-Z]|round-36' .tower/` → no output). Census prose there contains `kaidoku 6` and
  `game-dev-2d 36` — unrelated numbers, not this round.
- Out-of-criterion, pre-existing observation: `.ufo/waves/round-30/wave1/ScribeLesson.md` (1521 B,
  mtime 2026-10-25 15:58) is shaped exactly like a lane seat report ("Axes: depth:verifiability (C1)
  and coverage (C2)… final lesson is `corpus/lessons/round-30.md`") but sits at the fleet root, which
  has no `corpus/` (`ls -d corpus` → No such file or directory). **[INFERENCE]** it is a kaidoku
  round-30 report misrooted outside its lane. It names neither kaidoku nor round 36, so it does not
  meet this seat's criterion; recorded only so a later hygiene pass can route it.

---

## 2. Absolute `/tmp` paths in committed lane files

### 2.1 The pinned command, verbatim

```
$ git -C …/kaidoku-shokunin grep -n '/tmp/' 01a44dbf… -- corpus PROVINCE.md SKILL.md SCORECARD.md
… 746 lines / 91 files …                       exit 0
```

Per surface at the tip:

| surface | `/tmp/` hits | what they are |
|---|---|---|
| `SCORECARD.md` | **0** (`git grep -c` → exit 1) | — |
| `PROVINCE.md` | 1 (`:48`) | "sessions `mkdtemp /tmp/rea-ghidra-*`, `-readOnly -deleteProject`, self-cleaning" — describes REA's ephemeral session namespace, not evidence |
| `SKILL.md` | 2 (`:39`, `:537`) | shared `/tmp/rea-ghidra-*` namespace; `RUNS_DIR=/tmp/<dir>` "makes a non-destructive recheck" — instructions, not evidence |
| `corpus/` | 89 files (top: `corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md`:43, `…r10-01-queue-ops.md`:41, `…r9-01-queue-a-ops.md`:35) | historical round 2–14 knowledge entries whose `source:`/`verify:` lines name /tmp scratch; plus one binary false positive (`corpus/evidence/round-34/elf/e11.bin`) |

**Added by this round: zero.** `git diff cab59f22 01a44dbf -U0 | grep -cE '^\+.*/tmp/'` → **9**, and
none is under `corpus/` or the three root files: 8 across 5 w1 reports
(`R36ExecAppImageExtract` 2, `R36ExecHarnessRun` 3, `R36ExecEvidenceIds` 1, `R36ScribeEntry` 1,
`R36SentinelInstall` 1) and 1 in `tools/round-36/selftest/dev-after.json`, a single JSON line that
carries 8 distinct `/tmp` paths. `git diff cab59f22 01a44dbf -- PROVINCE.md SKILL.md
SCORECARD.md | grep -cE '^[+-].*/tmp/'` → **0**.

Exactly one `/tmp`-citing corpus file was also modified by this round —
`corpus/lessons/round-35.md` — and its `/tmp` line is untouched context:
`git diff -U0 cab59f22 01a44dbf -- corpus/lessons/round-35.md | grep -E '^[+-].*adb.html' | wc -l` → `0`.

### 2.2 Finding H1 — one live dangling `/tmp` **evidence** pointer remains at the tip (severity: low, real)

```
01a44dbf:corpus/lessons/round-35.md:21
  - **S113 reachable-now, not fabrication.** URL `https://developer.android.com/tools/adb?hl=en`,
    accessed 2026-10-25; HTTP 200, 368,063 bytes; … evidence in
    `.ufo/waves/round-35/assimilation/quarantine-verdicts.md` and live `/tmp/adb.html` capture.

$ ls -l /tmp/adb.html
ls: cannot access '/tmp/adb.html': No such file or directory
```

Exploit path (adversarial, not executed): the round's own S113 claim is graded on a byte count
(368,063) taken from a capture that no longer exists. A later verifier (round-37 closure, or this
wave's assimilation audit) that runs the documented check gets ENOENT and must either (a) declare
the claim unsupported — exactly the "fabrication" reading the row exists to refute — or (b) re-fetch
a live page whose bytes have had a day to change, then record a "contradiction" against a claim that
was true when measured. Either way a correct 2026-10-25 observation is converted into a defect by a
pointer, not by the measurement. This is the round-24 lesson's own M24-3 class ("held witnesses cite
inputs under `/tmp` … the closure could not find them on its clone",
`corpus/lessons/round-24.md:58`) and it is **not** listed in round-36's mistake table
(`corpus/lessons/round-36.md` M36-1..M36-7).

Smallest remediation (not applied — no remediation scope): delete the eight-word `/tmp/adb.html`
clause, or replace it with the retained capture path + sha256 if one was kept; the row's durable
pointer (`quarantine-verdicts.md`) is already present, so the claim does not lose support.

### 2.3 Finding H2 — this round's only new `/tmp`-bearing committed file is the C1 selftest fixture (severity: informational)

`tools/round-36/selftest/dev-after.json` (added at the freeze commit) contains 8 distinct absolute
paths, all under one dead REA session:

```
/tmp/rea-firmware-6TQbeD/firmware.bin            /tmp/rea-firmware-6TQbeD/report.json
/tmp/rea-firmware-6TQbeD/unblob.log              /tmp/rea-firmware-6TQbeD/extracted/firmware.bin_extract/{a.txt,sub/b.bin}
```

Calibrated as **inert**, verified rather than assumed:
- they occur only inside `raw_result`; the published list is relative —
  `normalized_result.files[*].relative_path` = `firmware.bin_extract/a.txt`,
  `firmware.bin_extract/sub/b.bin`;
- the counter reads only the published list (`c1-counter.py` `published()` = `normalized_result.files`
  `relative_path`/`sha256`; `matched()` compares those by equal sha + `fp == rel or
  fp.endswith('/'+rel)`) — so no `/tmp` string is ever compared, hashed or fetched;
- `dev-before.json` has **0** `/tmp` hits, so the paired control is clean;
- the fixture is disclosed as a non-carrier dev probe in the frozen claim
  (`plans/round-36-claims.md`: "Development inputs are a non-carrier probe image
  (`tools/round-36/selftest/dev-*`), never a carrier") and is distinguishable from real evidence by
  subject: fixture `subject.name=le-xz.sqsh`, digest `acc64a3d…94b93`, 2 files, id `ev_6edec5a4…`;
  corpus K1 `k1-le-xz.sqsh`, digest `9380293…a589`, 3 files, id `ev_b5bd2e7f…` (different subject,
  different id, different bytes: `d9193aea…` vs `a50bb972…`).

Residual risk (why it is reported at all): the file carries a plausible `ev_` id and a plausible
`/tmp/rea-firmware-XXXX` session path with **no in-file synthetic marker**, so a hygiene or
provenance pass that greps `/tmp/` under `tools/` can mistake it for a measured receipt and either
cite `ev_6edec5a4…` as a lane record or try to re-derive it under xpin (which would mint a different
id and read as tampering). Smallest remediation: one `"fixture": "selftest dev probe; not a recorded
measurement"` key, or a line in `tools/round-36/selftest/README.md` — though note the pinned path set
of item 3 (`corpus PROVINCE.md SKILL.md SCORECARD.md`) does not cover `tools/`, which is where every
new `/tmp` string this round actually lives.

### 2.4 Finding H3 — the wave-1 report publishes a `/tmp` recheck that its durably-committed copy does not (severity: low)

```
.ufo/waves/round-36/w1/R36ScribeEntry.md:53
  recheck: 180d — tools/round-36/c1-run.sh after corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh /tmp/r36-recheck
            && jq -c '.normalized_result|{files:(.files|length),gaps:(.extraction_gaps|length)}' /tmp/r36-recheck/after.json

corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md:5   (same recheck, durable copy)
  recheck: 180d — S=/fast/scratch/hyaku/recheck-r36 && tools/round-36/c1-run.sh after
            corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh "$S" && jq -c '…' "$S/after.json" → `{"files":3,"gaps":0}`
```

Two differing copies of one reproduction command. Not a bounds violation — seat bounds allow `/tmp`
files <50 MB — and not a dangling pointer, because the command regenerates its own output dir from
the committed fixture. The defect is (a) drift between the report and the row of record and (b)
instructing a `/tmp` write on a host where the fleet's own guard is repainting `/tmp` as pressured:

```
.ufo/state/disk-guard.log   (untracked, 1073314 B)
  2026-10-26T02:31:01Z pressure /tmp ? idle=? use=89% soft=70%
  2026-10-26T02:31:05Z pressure /tmp ? idle=? use=89% soft=70% target=60% emergency=0 all=0
```

Impact: a recheck run under the guard can be reclaimed mid-run (the round-3/round-8 EDQUOT family),
producing a recheck failure that looks like a predicate failure. Smallest remediation: make the w1
report cite the same `$S=/fast/scratch/hyaku/recheck-r36` line the entry uses.

### 2.5 Calibrated-safe: `/fast/scratch` pointers in committed evidence are not dangling evidence

Committed C1 envelopes name removed scratch on every path-bearing field, e.g.
`corpus/evidence/round-36/c1/K1/after.json`:

```
subject.local_path              /fast/scratch/hyaku/kaidoku-r36/L1/carriers/k1-le-xz.sqsh
parameters.path                 (same)
parameters.output_directory     /fast/scratch/hyaku/kaidoku-r36/c1-run.dcmJTg/out
raw_result.report[].task.path   /fast/scratch/hyaku/kaidoku-r36/c1-run.dcmJTg/rea-firmware-ris5IG/extracted/…
```

and its `*-run.json` receipt records `"carrier": "/fast/scratch/hyaku/kaidoku-r36/L1/carriers/k1-le-xz.sqsh"`.
Reproduction is nevertheless path-independent, measured:

```
sha256sum corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh → 93802938486d952abe0f06a83b55ca882e2272805ea11dcc3c35b9b9c9b8a589
K1 after.json subject.digest.sha256 / carrier_sha256        → 93802938486d952a…
carriers.json  K1 path = corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh, same sha
carriers.json  K2 path = corpus/evidence/round-36/c1/fixtures/k2-le-gzip.sqsh, sha ce5bf60e765e9942…
carriers.json  K3 K4    path = null, digests b644d034…/8efcec73… = published neovim v0.12.6 release digests
normalized_result.files = firmware.bin_extract/{README.txt,etc/config.ini,payload.bin}   (relative)
```

So the committed fixture + digest, not the scratch path, is the reconstructable anchor; K3/K4 are
re-acquirable from the upstream release. 22 of 43 w1 seat outputs mention `/fast/scratch`, every one
as a "scratch created and removed" declaration (e.g. `R36ExecReproK2`: "`/fast/scratch/hyaku/kaidoku-r36/R36ExecReproK2`
created and removed (verified absent)"). **[INFERENCE]** if a future counter ever reads
`parameters.output_directory` or `raw_result` instead of `normalized_result.files`, every committed
receipt becomes unevaluable; today's `matched()`/`published()` do not.

---

## 3. `/tmp` entries created today that mention kaidoku/r36

Sweep: every top-level `/tmp` entry with mtime 2026-10-26, content-grepped for
`kaidoku|R36|round-36` (regular files <3 MB). No directory under `/tmp` names kaidoku or r36; the
`systemd-private-*`, `scoped_dir*`, `zcode-bash-*`, `omp-*`, `node-compile-cache` entries are
unrelated runtime dirs.

| path | size | how it matches | content |
|---|---|---|---|
| `/tmp/r36seat_specnames.txt` | 857 | filename | 43 R36 wave-1 seat ids, one per line |
| `/tmp/r36seat_disp.txt` | 857 | filename | byte-identical roster copy (mtime 02:05, later) |
| `/tmp/r36r36w2map.txt` | 86 | filename | integers 0–31 (wave-2 item map) |
| `/tmp/r36r36w2rep.txt` | 448 | filename | 32 wave-2 report basenames (`AAxisVerdict`…`AWhatRemains`) |
| `/tmp/r36w2-reg.txt` | 530 | filename | registry ids `S001`…`S106` |
| `/tmp/r36w2-staged.txt` | 0 | filename | empty |
| `/tmp/frozen_expect.txt` | 957 | content (12 R36 paths) | `path blobsha` pairs for the 12 frozen files |
| `/tmp/u2.tsv`, `/tmp/z2.tsv` | 365 each | content only | oracle rows whose *paths* contain `usr/lib/kaidoku/…` (K2 fixture members); **not** lane or seat references |

### 3.1 No secret material

Nothing here is a credential, token or key: seat ids, registry ids, report names, and git blob
hashes. All files are mode 0644 in a sticky-bit `/tmp`.

### 3.2 `frozen_expect.txt` is accurate but unauthenticated (severity: informational)

```
$ while read p h; do a=$(git rev-parse 790561d4:$p); [ "$a" = "$h" ] || echo MISMATCH $p; done < /tmp/frozen_expect.txt
match=12 mismatch=0
```

It is a correct snapshot of the freeze **right now**, and the freeze holds through HEAD:
`git diff --stat 790561d4 01a44dbf -- <the 12 paths>` and `… 790561d4 6f2ba761 …` both empty. The
risk is provenance, not accuracy: a world-readable, unauthenticated copy of the frozen blob set in a
world-writable directory. A later seat that verifies freeze integrity against
`/tmp/frozen_expect.txt` instead of `git rev-parse 790561d4:<path>` is checking its own input — any
process on the host can rewrite that file into a self-consistent forged set, and the check would
pass. Smallest remediation for any seat that needs it: re-derive from the commit as above (that is
what this audit did); treat the `/tmp` copy as a cache, never as the oracle.

### 3.3 Round accounting cross-check (cheap, on-topic)

`/tmp/r36seat_specnames.txt` (43 names) vs `.ufo/waves/round-36/w1/*.md`: `comm -23` (spec minus
committed) → empty; `comm -13` (committed minus spec) → `swarm-registry.json` only. 43/43 w1 reports
exist and none is missing; `/tmp/r36seat_disp.txt` is a duplicate of the spec list, not a second
dispatching set.

---

## 4. Additional measurements taken while auditing

### 4.1 Wave-2 dispatch hygiene

`.ufo/waves/round-36/w2-spec.json` and `w2-dispatch.json` are tracked (commit `6f2ba761`) and hold
exactly one `/tmp` substring each — inside this seat's own task text ("`ls /tmp` entries created
today…"), i.e. an instruction, not an evidence pointer. `w2-spec.json` context length 3664 chars,
`/fast/scratch.*find|find.*du` matches **1** — the lesson's M36-6 red/green claim ("wave-2 context
carries the sentence") is true of the spec as committed. The wave-2 dispatch adds no `/tmp` write
instruction.

### 4.2 Misroot-adjacent check: the stated "integration tip" is not HEAD

`git log --oneline` → `6f2ba761` (wave-1 results, `R36ReviewerQualityBar.md`, wave-2 spec/dispatch)
on top of `01a44dbf`. Every `/tmp` measurement in §2 is pinned at `01a44dbf` exactly as the seat
specifies; `git diff 01a44dbf 6f2ba761` adds no `/tmp` evidence line (the only added `/tmp` strings
are the three quoted task texts, plus the `+.*/fast/scratch` count of 30 in spec/dispatch text). The
round is therefore **not** closed at the stated tip — a later reader who assumes `01a44dbf` is the
last word will undercount wave-1 results by one seat and miss the wave-2 spec entirely.

### 4.3 Frozen-set integrity through HEAD

Unchanged, `git diff --stat` empty at both `01a44dbf` and `6f2ba761` for all 12 frozen paths
(`plans/round-36-claims.md`, both counters, `carriers.json`, 4 `oracle.tsv`, 4 `before.json`).
Custody of those blobs is another seat's surface; recorded here only because §3.2 needed it.

---

## 5. Coverage, limits, and what I did not do

- Read: `plans/round-36-claims.md`, `corpus/lessons/round-36.md`, the freeze/base/tip objects,
  `.ufo/waves/round-36/**` file list and the w1 reports' `/tmp` lines, the C1 counter's
  `published()`/`matched()`/`selftest()`, the C1 selftest fixtures, `LOG.md`/`PROVINCE.md`/`SKILL.md`
  `/tmp` rows, and the fleet-root untracked inventory.
- Not re-run: any counter, harness, oracle, selftest, REA verb, or carrier extraction. No build,
  lint, test or formatter was run (leaf bounds). Every sea-level claim above is a read or a
  `git`/`grep`/`sha256sum`/`python3 -c` inspection of committed bytes; the one live filesystem check
  is `ls /tmp/adb.html` (ENOENT).
- The seat's pinned path set (`corpus PROVINCE.md SKILL.md SCORECARD.md`) excludes `.ufo/` and
  `tools/`; all of this round's genuinely new `/tmp` strings live in those two trees. Had I answered
  the pinned command literally, item 3 would read "only historical hits, nothing new" and would miss
  H2 and H3. Both are reported above so the next wave's grep pin can cover `tools/` and `.ufo/waves/`.
- Scratch: `/fast/scratch/hyaku/kaidoku-r36/R36W2SentinelHygiene` (two intermediate file lists) —
  removed before this report was yielded; nothing cited above lives there.
- Tooling: none installed, none upgraded (no `pacman` transaction, no `uv`/`npx`/`pip` install).
