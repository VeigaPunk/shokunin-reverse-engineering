# R45W2CensusEnd — falsification of the round-45 census figures

Seat `R45W2CensusEnd`, round 45 wave 2 (adversarial falsification), lane `kaidoku-shokunin`.
Axes attacked: **coverage** (do the numbers cover the whole registry state, not a sample),
**depth** (does each number survive a mutation that should move it), **calibration**
(does each claim say exactly what the instrument measures).

Nothing in the lane tree was written. Every measurement below is either read-only git or a
scratch copy under `/fast/scratch/hyaku/kaidoku-r45/R45W2CensusEnd` (removed after the
receipts were copied here). No installs were made (pacman is paused host-wide; none needed).

## 0. Revisions measured

| label | commit | notes |
|---|---|---|
| base | `149133d47aa7e90796f96047afe6d251a3e65b2c` | `plans/round-45-claims.md` base; round start |
| freeze | `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` | 139 rows, no S140/S141 |
| landing | `e715263cb51b713c342ab992d527fe9d61d6f8ff` | adds block 22, registry rows, S140/S141 |
| A1 (measured rev in the w2 dispatch) | `1f4b27f82353d6544dc0c8048b3cfdadd8525d12` | SOURCES.md identical to A3 |
| A3 (this seat's worktree) | `f59565b782c18b0eb691bec12f52d2f80d9f5032` | |
| live | lane working tree | `corpus/SOURCES.md` clean, sha `70be416d…` |

Trees for historical revisions were materialised with `git archive <rev> | tar -x -C <scratch>`
(read-only git), each into its own fleet-root shape `<root>/kaidoku-shokunin` plus a
one-line `shokunin.conf`.

## 1. Verdicts

| # | attacked claim (where it is written) | verdict | measured |
|---|---|---|---|
| 1 | "`corpus/SOURCES.md` rows 139 → 141" (`corpus/lessons/round-45.md:56`) | **holds** | 139 @base, 141 @landing/A1/A3/live |
| 2 | the delta is exactly the two new rows, nothing else changed (same paragraph, append-only reading of CORPUS rule 2) | **holds** | `git diff --numstat freeze A1 -- corpus/SOURCES.md` = `2 0`; id-set diff is only `+S140 +S141`; ids contiguous S001…S141; no E-code at any revision |
| 3 | round-start census: `validate … kaidoku` → `kaidoku ok`, exit 0, 14 W04 (`round-45.md:57-59`) | **holds** | base replay: exit 0, 14 W04 (sha `2b72b623…`) |
| 4 | round-end: same command, exit 0, **16 W04** (`round-45.md` at landing and A1, lines 58-60) | **falsified** | measured **14** at the landing, at A1, and at A3. The number was never 16. Repaired at A2 `fedd11bf`, which is why the A3 lesson reads 14 |
| 5 | "the two added warnings are the within-scope URL repeats class" (same sentence, landing/A1) | **falsified** | no warning was added at all; and within-scope repeats are **E04** (exit 1), not W04. Probe `mutF` (same URL, same scope cell) yields `E04 … within scope …`, exit 1 |
| 6 | "S140 and S141 add no new duplicate-URL warning" (`round-45.md:60`, A2/A3) | **holds** | 0 of 14 W04 ids are S140/S141; deleting either row leaves the validate output **byte-identical** (`diff-exit=0`, rows 140); the instrument is shown able to flag duplicates of both URLs (`mutA`, `mutC`) |
| 7 | "four of them deliberate CORPUS-rule-2 supersession rows" (`round-45.md:61-62`) | **holds** | exactly **S033, S054, S062, S069** carry a `supersedes` statement in `teaches`; the other 10 are same-URL re-registrations at new scopes with no supersede wording |
| 8 | "the lesson says … '16 W04 warnings' at round end" (this seat's prompt, `.ufo/waves/round-45/w2-spec.json`, and `w2-gen.py:101` at f59565b7) | **falsified at f59565b7** | at f59565b7 the lesson says **14** and documents the correction. The spec/dispatch still carries 16 because it was committed at `faa875bc`, before A2 `fedd11bf`; it was never updated |
| 9 | "run … `validate --root /home/vgpnk/Projects/shokunin kaidoku` at `<rev>`'s worktree" | **not run as written** | that command cannot address a revision: `--root` is the live fleet root, so it measures the live working tree. Substituted `git archive` replicas. Harmless here — live `SOURCES.md` is byte-identical to f59565b7 (`70be416d…`), and both runs agree (14 W04, exit 0) |

## 2. The numbers, exactly

`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`

| revision | rows | tier.A | tier.B | tier.C | mined | rejected |
|---|---|---|---|---|---|---|
| base `149133d4` | 139 | 131 | 7 | 1 | 134 | 5 |
| A1 `1f4b27f8` | 141 | 133 | 7 | 1 | 136 | 5 |
| A3 `f59565b7` | 141 | 133 | 7 | 1 | 136 | 5 |

`census` (the script's own metric) agrees with the grep at every revision: `kaidoku rows 141`
at A1/A3/live (sha `01eb62a2…`), `139` at base (sha `3da9ecab…`). Delta is exactly
+2 tier A, +2 mined.

`validate` is 14 W04 + one `ok` line, exit 0, at **every** revision — base, landing, A1, A3,
live. No E-code fires anywhere.

## 3. What S140/S141 add to the W04 set — nothing, and why that is not vacuous

The 14 W04 warnings are 10 duplicate-URL groups, 14 later-occurrence rows:

| normalized URL | rows (first → warning) | supersession? |
|---|---|---|
| `registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz` | S079 → S083, S090, S092, S119, S123 (5) | no |
| `github.com/…/ghidra/pull/9348` | S032 → S033 | **yes (S033)** |
| `go.dev/dl/?mode=json&include=all`,` | S038 → S047 | no |
| `developer.android.com/ndk/guides/abis` | S052 → S054 | **yes (S054)** |
| `raw.githubusercontent.com/…/sigrok-cli.1` | S058 → S062 | **yes (S062)** |
| `www.wireshark.org/docs/man-pages/tshark.html` | S065 → S069 | **yes (S069)** |
| `learn.microsoft.com/…/debug/pe-format` | S100 (rejected) → S102 | no |
| `raw.githubusercontent.com/…/squashfs.py` | S108 → S112 | no |
| `raw.githubusercontent.com/…/README.md` | S110 → S117 | no |
| `github.com/…/tests/integration/filesystem/squashfs` | S130 → S138 | no |

That is 4 + 10 = 14, and the four supersession rows are exactly S033/S054/S062/S069 — the
lesson's "four" is correct.

S140 (`git-scm.com/docs/git-status`) and S141 (`git-scm.com/docs/git-diff-tree`) are each
**occurrence 1 of 1**: no other row carries either normalized URL, and no other row's cells
mention either page (`grep -iE 'git-status|diff-tree'` matches only their own lines). They are
therefore W04-neutral by content, not by accident.

Sensitivity controls (all on a full-tree scratch copy, `--root` = scratch, exit recorded):

| control | mutation | validate exit | W04 | output vs clean |
|---|---|---|---|---|
| `mutA` | insert a 2nd `git-status` row at a new scope | 0 | 15 | `+ W04 S999 duplicate url git-scm.com/docs/git-status` |
| `mutC` | insert a 2nd `git-diff-tree` row *before* S141 | 0 | 15 | `+ W04 S141 duplicate url git-scm.com/docs/git-diff-tree` |
| `mutB` | delete the S141 row | 0 | 14 | identical (0 diff lines) |
| `mutD` | delete the S140 row | 0 | 14 | identical (0 diff lines) |
| `mutE` | 2nd `git-status` row, URL in markdown backticks | 0 | 14 | identical |
| `mutE2` | same row, URL plain | 0 | 15 | `+ W04 S996 …` |
| `mutF` | same URL **and same scope cell** as S140 | **1** | 14 | `E04 S995 duplicate url … within scope …` |

So both new rows *can* produce a warning if they duplicated anything, and the duplicate
path is exercised at the right scope granularity (E04) as well as the cross-scope one (W04).

## 4. Instrument limits found (new; none of them invalidate claims 1-7)

- **Markdown punctuation is part of the URL.** `url_of` matches `[^[:space:]|]+`, so S047 is
  compared as `go.dev/dl/?mode=json&include=all`,` (backtick + comma retained). It pairs only
  because S038 carries the same artifact. A duplicate written in backticks is invisible
  (`mutE`: 14 warnings, output byte-identical) while the plain form is caught (`mutE2`: 15).
  "No new duplicate-URL warning" is therefore an exact-string claim, not a same-document one.
- **Exact path only.** The host `git-scm.com` now holds four rows (S073 merge-base, S074 log,
  S140 status, S141 diff-tree) at four distinct paths; W04 cannot see same-host/same-manual
  overlap. S140/S141 are new *documents*, which is the correct reading here.
- **Warnings ≠ duplicate documents.** `rea-agents-6.5.0.tgz` appears 6 times and yields 5
  warnings, so a warning count must not be read as a duplicate-pair count.

## 5. Record discrepancies for the L1

1. **The dispatch prompt is stale.** `.ufo/waves/round-45/w2-spec.json` (and `w2-gen.py:101`)
   at f59565b7 still say "The lesson says … '16 W04 warnings'", while
   `corpus/lessons/round-45.md:59-60` at the same revision says 14 and cites the A2 correction.
   The spec was committed at `faa875bc`, before A2 `fedd11bf`, and was not regenerated. Every
   wave-2 seat attacking this premise received the stale number; this seat measured 14 and
   treated "16" as the claim under test.
2. **Freeze-time unregistered ids.** At the freeze, `corpus/SOURCES.md` carries **0** rows for
   S140/S141 (`grep -c` = 0) while `plans/round-45-claims.md` names them 5 times. The claim's
   own predicates never read `SOURCES.md`, so nothing breaks, but the lesson's "rows opened
   this round" is only true from the landing commit onward, and a freeze-time
   "cited-source-is-registered" check would fail.
3. The A3 lesson's repair sentence ("An earlier draft of this paragraph said 16; the measured
   number is 14 at both ends") is accurate, including "at both ends" — base and A3 both 14,
   identical id sets.

## 6. Receipts

`receipts/receipts.tsv` — one line per invocation: label, UTC, exit, stdout sha256, command.
Files: `receipts/*.out` (stdout), `receipts/*.err` (stderr, all empty), `receipts/*.diff`
(mutant vs clean, `diff` exit recorded in the tsv).

Headline receipts:

| label | exit | stdout sha256 |
|---|---|---|
| `live-validate` | 0 | `9f32a8a84ef13933a0539a92a4475534aeb2ae858a407d35b176aa26662acf19` |
| `a3wt-validate` | 0 | `3298f460c5ffa64c56c6c9d7f5e8bee88128224413b41e6d6cafcd8c46e9e795` |
| `a1-validate` | 0 | `55b543ec15a1bc28e05692fc420ea6b60374080d19a8e0e6a4b39323a623ec64` |
| `base-validate` | 0 | `2b72b62331f3234fb4ee148b684afed763c797c48f48c65eadb497e8f7317f5c` |
| `a3wt-census` / `a1-census` / `live-census` | 0 | `01eb62a20aebb739a171fe8547f4f25ecb3423174b2861251bcba45c07e7964d` |
| `base-census` | 0 | `3da9ecabc4607e314df5fbb3900f9925b6776c6db2161a855a60e2c1e93c0d5c` |

The two validate shas differ only in the trailing `ok <path>` line (lane path); the W04 block
is byte-identical across live/A3/A1.

Reproduction (each in a scratch root, nothing written to the lane):

```sh
S=/fast/scratch/hyaku/kaidoku-r45/R45W2CensusEnd
mkdir -p "$S/root/kaidoku-shokunin"
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin archive <REV> | tar -x -C "$S/root/kaidoku-shokunin"
printf 'LANES="\nkaidoku|kaidoku-shokunin|x"\n' > "$S/root/shokunin.conf"
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root "$S/root" kaidoku
grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/root/kaidoku-shokunin/corpus/SOURCES.md"
```

## 7. Bottom line

Row growth **139 → 141** and **exit 0** hold at every revision; the growth is exactly
S140+S141 with no other cell touched. The round-end **"16 W04"** was wrong and is already
repaired to **14** at A2/A3 — 14 is the measured value at both ends, and both new rows are
provably W04-neutral. The only live defect this seat found is upstream of the lesson: the
wave-2 dispatch spec still ships the pre-A2 "16", so seats that trust the prompt rather than
the record are aiming at a number the record no longer claims.
