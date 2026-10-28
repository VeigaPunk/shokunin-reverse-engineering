# R44W2ConnSibling — sibling-overlap scan and path-collision audit (read-only, fleet-wide)

- **Seat** `R44W2ConnSibling` · role `connector` · wave `r44-w2`
- **Axes** coverage · depth · calibration
- **Lane** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- **Revisions** BASE `c29360e3ba5381a5ab69e372d0d9577970f85018` · FREEZE
  `c48f8a4bfd449300c975668e59aae5b5538b6a84` · REV `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac` ·
  TIP `8bb1090af3fef64477c4337855e4347472db2701`
- **Mode** read-only. Every git call was `show`, `log`, `diff`, `rev-parse`, `ls-tree`, `ls-files`,
  `worktree list`, `cat-file`, `for-each-ref`. No mutating git/jj command ran anywhere; no fixture
  repo was created (this seat needs none).
- **Receipts** `.ufo/waves/round-44/w2/artifacts/R44W2ConnSibling/receipt.json` — 18 rows, each with
  the exact command, cwd, exit code, stdout sha256, byte count and wall time; one `<row>.txt` per
  command holds its verbatim stdout.

## 0. Executed vs. read

Executed by this seat: the 18 receipt rows below (fleet scans, per-lane commit-bound witness, the
three frozen-path-preflight arms, PROVINCE prefix check, counter-digest check, tracked-status check,
`/tmp` residue check, re-read of the committed M44-2 receipt).

**Not executed** (other seats' arms; not re-run here): `tools/round-44/c1-counter.py`,
`tools/round-44/c2-counter.py`. Where I state C1/C2 values they come from the committed receipts
`.ufo/waves/round-44/l1/{c1,c2}-score-at-55bcce69.json` and are marked *read, not re-run*:

| receipt | fields read | values |
|---|---|---|
| `c1-score-at-55bcce69.json` | `exit_code`, `carriers_matched`, `met_target`, `frozen_path_changed` | `1`, `4`, `false`, `[]` (*read*) |
| `c2-score-at-55bcce69.json` | `entries_evaluated`, `mismatches`, `met_target`, `frozen_path_changed` | `80`, `[]`, `true`, `[]` (*read*) |

## 1. Q1 — does any sibling lane already claim `squashfs_v1`/`squashfs_v2` Core?

**No. Kaidoku's Frontier statement is not contradicted by any sibling lane at its committed head.**

| row | command (full text in `receipt.json`) | exit | observed |
|---|---|---|---|
| R18 | per-lane `git -C <lane> rev-parse HEAD`, `HEAD:PROVINCE.md`, and `grep -c 'squashfs_v1\|squashfs_v2'` over 21 lanes | 0 | 20 sibling `PROVINCE.md` blobs contain **0** tokens each (blob shas bound per lane, e.g. `revenger 2d3542c1…`, `kotoba 71a4106b…`); kaidoku's blob `7f3f6563cff9130e2e0cd6050630244fb0d5a0b8` contains **2** |
| R01 | per-lane `grep -c` over `*/PROVINCE.md` | 0 | only `kaidoku-shokunin` non-zero (2); all others 0 |
| R03 | `grep -rin 'squashfs' */SCORECARD.md */PROVINCE.md */SHONEN.md \| grep -v '^kaidoku'` | 1 (no match) | empty — no sibling decision doc mentions squashfs at all |
| R04 | `grep -rn 'squashfs' */corpus \| grep -v '^kaidoku-shokunin'` | 0 | one hit: `revenger-shokunin/corpus/live/runs/round-63/LEDGER.md:51`, which lists `squashfs` among the signature families its 2048-byte synthetic image **cannot** test ("No evidence about any other signature family") — a refusal, not a Core claim |
| R02 | fleet-wide `grep -rn 'squashfs_v1\|squashfs_v2'` outside kaidoku and `templates/` | 0 | 2 hits, neither a claim: kaidoku's own fleet report `.ufo/reports/round-44/kaidoku.md:6,124,126,162`, and a `/tmp` listing captured inside a tsukuroi artifact (§3a below) |

R18 is the load-bearing row: it binds the negative to *commits* (per-lane HEAD + `PROVINCE.md` blob
sha), not to mutable worktrees, so the witness can be re-derived by anyone. Scope caveat: it is
head-relative at 2026-10-28; a sibling that lands a squashfs Core row later invalidates it, which is
why §6 proposes committing it with its scan timestamp.

## 2. Q2 — does a sibling own a `tools/round-45/` path this lane created a file in?

**No collision. `tools/round-45/` is kaidoku-only.**

| row | command | exit | observed |
|---|---|---|---|
| R05 | `for d in */tools/round-45; do [ -d "$d" ] && ls -1 "$d"; done` plus a `*/tools` census | 0 | exactly one `round-45` dir in the fleet (kaidoku), one file: `frozen-path-preflight.py`. Nine lanes keep a `tools/` dir (chousa, kaidoku, kama, kotodama, mado, mori, souji, tameshi, tsukuroi); none has `round-45/**` |
| R06 | `find . -name 'frozen-path-preflight.py' -not -path './kaidoku-shokunin/*'` + fleet grep for `tools/round-45` | 0 | no sibling copy of the filename; the only fleet referents are kaidoku's own fleet-level report `.ufo/reports/round-44/kaidoku.md:48,80,142,153` |
| — | `git ls-tree -r --name-only HEAD -- tools/round-45/` | 0 | `tools/round-45/frozen-path-preflight.py` (committed at TIP) |

Note: tsukuroi's r48 connector report (`.../round-48/w2/ConnWave.md:7`) still asserts "only
kaidoku-shokunin has a `tools/` dir" — stale *for tsukuroi's own census*, not a claim on kaidoku's
paths. Nothing to resolve before commit.

## 3. Q3 — does a sibling report cite kaidoku round-44 artifacts?

**Yes, four citations. All verified intact; none needs an edit in this lane.**

| cite | what it says | verified |
|---|---|---|
| a) `tsukuroi-shokunin/.ufo/waves/round-48/w2/ConnWave.md:9,31-34` | cites `kaidoku-shokunin/tools/round-44/c2-counter.py` **by line** (`:279-280`, `:595-634`, `:538-591`, doc line 87) as "the freeze-integrity walk … one idea worth copying" | R14: counter sha256 `085192ea6c3f3f4d67c58ce459ef06e1febd0b668dc367ccfbdd12661736c277` is **identical at FREEZE and at REV**; each cited line resolves as described — `:279` `def is_ancestor`, `:538` `def verify_expected_edit`, `:595` `def freeze_integrity`, `:87` "the freeze blob must be a prefix of the REV blob". The citation is protected by the `tools/round-44/` directory freeze |
| b) same file `:752` and `TExecCounterB/tmp-listing-pre-run.txt:1419-1420`, `TExecLiveKill/ps.snapshot.txt:50` | a `/tmp` listing and process snapshot that observed this lane: `/tmp/kaidoku-r44`, `squashfs_v2.1_{be,le}.bin`, and `c1-counter.py --selftest --work /fast/scratch/hyaku/kaidoku-r44/probe-R44C1Counter/selftest-work` | R16 — all five paths still exist (§4 D2) |
| c) `kengaku-shokunin/.ufo/waves/round-49/w1/R49SentHygiene.md:112,312,345` | records `/fast/scratch/hyaku/kaidoku-r44/…` npm/REA runs and attributes them to this lane | attribution only, no artifact claim; the scratch namespace is the dispatch contract's own |
| d) `souji-shokunin/.ufo/waves/round-36/w1/SwarmExecutor22.md:194,342` | records a **second live worktree registration** `/fast/scratch/hyaku/kaidoku-r44/R44W2Census/base-wt` as `DRIFT REGS-CHANGED kaidoku-shokunin record=1 live=2` (`live_regs=24`) | `git -C <lane> worktree list` now shows **one** worktree (TIP, detached); `.git/worktrees/` is absent and the scratch dir is gone. The sibling's contract declares `live_regs` observed-not-target, so its counter is unharmed |
| e) `mado-shokunin/.ufo/waves/round-44/w2/RerunCensus/census-fleet.txt:11` | records kaidoku's W04 duplicate-URL warning for `S112` (unblob `squashfs.py`) | matches the lane's own census end-state; a sources fact, not a claim cite |

Fleet round-44 lane reports (R08): **no sibling report mentions kaidoku at all** — only
`.ufo/reports/round-44/kaidoku.md` does.

## 4. Findings

Every finding below names the path:line, the command and its exit code, and the observed value.

### D1 — the record cites an **uncommitted** receipt (L1 must act)

`corpus/lessons/round-44.md:49` (committed blob `106484695678ffff7846f13516e5f0ba43ae3caa`) ends
the census line with "round-end receipt `.ufo/waves/round-44/l1/sources-census-end.txt`".

```
$ git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-files --error-unmatch \
    .ufo/waves/round-44/l1/sources-census-end.txt
exit 1        → UNTRACKED (R15)
$ wc -c .ufo/waves/round-44/l1/sources-census-end.txt
1518          (14 W04 lines, present in the worktree only)
```

Impact: a fresh clone of TIP cannot reproduce the round's sources-census end-state from the record.
Same class, also untracked and uncited: `l1/sources-census-start-replay.txt` (1494 B),
`l1/selftest-c1-counter.txt` (1803 B), `l1/selftest-c2-counter.txt`. Action: `git add` the cited
file in the wave-2 landing (L1 is the only seat allowed to commit), or drop the citation.

### D2 — kaidoku-named residue left in `/tmp`, already captured by two sibling lanes (L1 must decide)

```
$ ls -ld /tmp/kaidoku-r44 ; stat -c '%n %s %y' /tmp/squashfs_v2.1_be.bin /tmp/squashfs_v2.1_le.bin
drwxr-xr-x 2 vgpnk vgpnk     6 Oct 28 11:23 /tmp/kaidoku-r44
/tmp/squashfs_v2.1_be.bin 4096 2026-10-28 08:14:41.552234776 -0300
/tmp/squashfs_v2.1_le.bin 4096 2026-10-28 08:14:41.151485546 -0300
/tmp/sqfs-v2-{dqt3nv2y,pt4r0uhp,qjtd1gw2,y6dl5_fb}
exit 0 (R16)
```

Observed by siblings: `tsukuroi .../round-48/w2/TExecCounterB/tmp-listing-pre-run.txt:752,1419,1420`
and `.../TExecLiveKill/ps.snapshot.txt:50`. Authorship is **[INFERENCE]** — the names match the v2.1
unblob fixtures the frozen claims describe as fetched in wave-1 exploration, and the mtime is inside
round 44 — but no receipt binds a seat to them. The two 4 KiB files sit inside the prompt's "/tmp
files under 50 MB" allowance; the four `sqfs-v2-*` directories and the undeclared placement are not
covered by the scratch contract (`/fast/scratch/hyaku/kaidoku-r44/<seat-name>/`). They carry no claim
evidence (claims item 1 excludes v2.1) and change no score. Action: L1 removes them before landing
and adds one disclosure line (a wave-2 seat may not write outside its own paths).

### D3 — the lane worktree is on a **detached HEAD**; a landing commit here does not advance `main` (L1 must act)

```
$ git -C <lane> rev-parse --abbrev-ref HEAD   → HEAD
$ cat .git/HEAD                               → 8bb1090af3fef64477c4337855e4347472db2701
$ git -C <lane> rev-parse HEAD  ==  git -C <lane> rev-parse main  ==  8bb1090a…
$ git for-each-ref refs/heads                 → main 8bb1090a
```

Values agree today, but `git commit` in detached HEAD moves only `HEAD`; `main` would stay at
`8bb1090a` and the wave-2 landing would be invisible to `git log main`. Action: L1 asserts the branch
(or re-points it) and verifies `git log --oneline -1 main` names the landing commit. This is a
pre-commit precondition, not a record defect.

### D4 — `M44-2` says "added/edited"; all eight paths are **modified** (record precision, low)

`corpus/lessons/round-44.md:16` (committed blob `10648469…`): "`c86ea508` **added/edited** 8 files
under `tools/round-44/control-fixtures/`".

```
$ python3 -I -B tools/round-45/frozen-path-preflight.py --root <lane> \
    --freeze c48f8a4b… --rev 8bb1090a… --pathspec tools/round-44/        exit 1
  verdict=frozen_path_changed  touched=8  blob_changed=8  statuses=['M']
$ git show --stat c86ea508 -- tools/round-44/
  8 files changed, 342 insertions(+), 303 deletions(-)   (all `M`)
exit 0 (R10, R17)
```

No path was added: every one of the eight existed at FREEZE and its blob changed. In a round whose
freeze rule distinguishes `A` from `M`, "added/edited" overstates the status. Correction belongs in
an appended correction line, not a rewrite.

### D5 — PROVINCE narrows the contradiction to claim-vs-counter; the frozen claim is internally unsatisfiable (record precision, low)

`PROVINCE.md:428` (at REV): "the claim required the committed evidence path, while the counter
accepts only the `/kaidoku-r44/` scratch provenance." True of the counter, but the frozen claim text
requires **both** a `corpus/evidence/round-44/c1/` path (wave-1 amendment item 3) **and** the
`/kaidoku-r44/` segment (the predicate). `corpus/lessons/round-44.md:57` (R44-CL2) states this
correctly: "internally unsatisfiable on one field". A reader of PROVINCE alone could conclude the
counter is the deviant and "fix" it — which would still fail the predicate's own scratch clause.
Action: optional one-line append clarifying that both clauses are in the frozen claim.

### D6 — the fleet adjacency registry pins kaidoku at round 35 (observation; kotoba-owned, no action here)

`kotoba-shokunin/PROVINCE.md:62`: `| kaidoku | none | 3b1ab3c9d248b7afbf7fc5e5507d76cd87e26c3c | …`.
That hash is the kaidoku commit `3b1ab3c9` ("round-35 verifier spot-check"); kaidoku's `PROVINCE.md`
blob at that commit is `d453a29d…`, and at REV it is `7f3f6563…` (R09, R18). So the fleet's only
cross-lane adjacency verdict for this lane rests on a nine-round-old read. It says `none` and names
only revenger, so R44-C1's stop changes nothing. If a future round promotes SquashFS v1/v2, that row
must be re-filed by kotoba; this round must not rely on it.

### D7 — "the record" under review has two states (observation; L1 commits the edit)

```
$ git -C <lane> status --porcelain corpus/lessons/round-44.md   → " M corpus/lessons/round-44.md"
$ git rev-parse HEAD:corpus/lessons/round-44.md                → 106484695678ffff7846f13516e5f0ba43ae3caa
$ sha256sum corpus/lessons/round-44.md                          → e1b0c73a8c5ee6b427ba5dc04c467608c6c2774ad6b6827104124610dc89f1b3
$ git diff --stat -- corpus/lessons/round-44.md                 → 1 file changed, 11 insertions(+), 3 deletions(-)
```

The worktree lesson carries an uncommitted expansion (the wave-1 `R44ConnRouted` ledger paragraph and
a rewritten `R44-CL4`). Wave-2 verdicts that quote the lesson must say which blob they mean. This
seat quotes the committed blob for D1/D4/D5 and the worktree only where flagged.

## 5. Positive verifications (M44-2 fix, reproduced independently)

| arm | command | exit | observed |
|---|---|---|---|
| P1 red | preflight `--freeze c48f8a4b --rev 8bb1090a --pathspec tools/round-44/` | **1** | `frozen_path_changed`, `touched 8`, `blob_changed 8`; the 8-path list is identical to the committed `.ufo/waves/round-44/l1/preflight-c86ea508.json`, whose own `rev` is `c86ea508` (R10, R17) |
| P2 green | preflight `--freeze c48f8a4b --rev 55bcce69 --pathspec tools/round-44/` | **0** | `clean`, `touched []`, `blob_changed []` (R11) |
| P3 no spec | preflight `--freeze c48f8a4b --rev 8bb1090a` (no `--pathspec`) | 1 | 557 touched paths, `blob_changed 0` — the gate has no default frozen spec and cannot derive one from the claim; "wiring it" means freezing the pathspec list alongside the tool (R12) |
| P4 wiring | `ls .git/hooks \| grep -v sample`; `git config --get core.hooksPath`; `git worktree list` | 1 / 1 / 0 | no non-sample hook, `core.hooksPath` unset, one worktree at TIP (detached), `.git/worktrees/` absent (R19) — not wired at commit time, exactly what R44-CL1 claims ("wire it into the round's commit sequence before the next freeze"). The record does not overclaim the fix |
| P5 ancestry | preflight at `--rev` before the freeze | (not run by this seat; sibling arm) | — |

`M44-2`'s evidence pointer `git log --oneline c48f8a4..main -- tools/round-44/` reproduces:
`c86ea508` is the only commit.

## 6. Proposed move (one, bounded)

**Bind the round's Frontier statement to a committed, commit-anchored fleet-wide negative witness.**

The round's own instruments (C1/C2) can only see this repository, so "Still Frontier: SquashFS v1/v2"
is, at present, an assertion no counter in the lane can contradict or confirm — it is checked only
against kaidoku's own PROVINCE. The one place it *can* be contradicted is another lane's corpus,
which no seat in this wave is measuring. R18 already is that witness: 21 lanes, per-lane HEAD +
`PROVINCE.md` blob sha, token counts 0 for all 20 siblings and 2 for kaidoku.

Concrete form (L1 does it, in the same append-only pass as the landing):

1. commit `artifacts/R44W2ConnSibling/R18-provable-negative-witness.txt` with `receipt.json` (already
   written here), and
2. append one line under the Round-44 frontier note (or to the routed-defect ledger):
   `Frontier witness: no sibling lane's committed PROVINCE.md carries squashfs_v1/squashfs_v2 at
   2026-10-28T<hh:mm>Z (w2/artifacts/R44W2ConnSibling/R18, 21 lanes, per-lane HEAD+blob shas; only
   kaidoku 2 tokens).`

- **Axes improved:** depth (the Frontier claim becomes falsifiable by a committed receipt instead of
  a self-referential lane statement) and calibration (a reader can re-run R18's loop verbatim).
  Coverage is untouched — the claim stays stopped; nothing is promoted.
- **Harm:** none — no claim byte, no counter, no rubric, no frozen path changes. It is a citation
  appended in a file the round already appends to.
- **Risk:** head-relative, so it is a witness at a timestamp, not forever. Stating the timestamp and
  the per-lane blob shas (which R18 already prints) is what keeps it honest.
- **Optional rider, same artifact:** R14 binds tsukuroi's line-number citation of `c2-counter.py` to
  its digest; one clause can name `085192ea…` so a later edit cannot silently orphan a sibling's
  committed evidence pointer.

## 7. Risks and limits

- The negative witness is head-relative and was taken while other lanes were running; a sibling can
  commit a squashfs Core row after it. The timestamp plus per-lane blob shas bound, but do not
  future-proof, the statement.
- Scan coverage: `templates/` excluded from R02 (verified separately: no squashfs token anywhere in
  `templates/`), and non-lane trees `ok/`, `research/`, `scripts/` are covered by R02's recursive root
  scan but are not lanes with a `PROVINCE.md`.
- D2's authorship is inference, not a bound receipt; the residue is real regardless.
- This seat did not execute either counter, so it confirms neither `carriers_matched 4` nor
  `entries_evaluated 80` first-hand; it confirms that the committed receipts say so and that the
  preflight's red/green pair reproduces.
- No file was written outside this lane's `.ufo/waves/round-44/w2/` and this seat's scratch; the
  scratch directory was removed before yielding.

## 8. Artifacts

`.ufo/waves/round-44/w2/artifacts/R44W2ConnSibling/` — `receipt.json` plus
`R01-province-scan.txt`, `R02-fleet-token-scan.txt`, `R03-sibling-prose.txt`,
`R04-sibling-corpus.txt`, `R05-round45-dirs.txt`, `R06-preflight-owners.txt`,
`R07-sibling-r44-cites.txt`, `R08-fleet-r44-reports.txt`, `R09-adjacency-registry.txt`,
`R10-preflight-red-tip.txt`, `R11-preflight-green-rev.txt`, `R12-preflight-nospec.txt`,
`R13-province-prefix.txt`, `R14-counter-digest.txt`, `R15-cited-receipt-tracked.txt`,
`R16-tmp-residue.txt`, `R17-committed-preflight-match.txt`, `R18-provable-negative-witness.txt`,
`R19-hooks-wiring.txt`.
