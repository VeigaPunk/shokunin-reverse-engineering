# MisrootSweep — round 27 wave 2

Item attacked: whether a round-27 kaidoku seat file was written at the fleet root
`/home/vgpnk/Projects/shokunin`, listing any untracked file whose content names kaidoku and
round 27 (or KaidokuR27). Read-only throughout: read-only git, plain grep, find, sha256. No jj
command run; no lane or fleet file touched; no tool installed.

Verdict on "no misrooted round-27 kaidoku seat file sits at the fleet root": **holds**. The fleet
root has zero untracked files, so the requested list is empty. Four uncommitted new entries are
intent-to-add (` A`, not `??`), and none names kaidoku with round 27. The only untracked files
containing both tokens somewhere are ignored probe copies dated three days before this round, and
no line in them carries kaidoku next to round 27.

## Checks

C1 — fleet-root status, 2026-10-22T15:38:10Z.
`git -C /home/vgpnk/Projects/shokunin status --porcelain -uall` → exit 0, 18 lines, 0 starting
`??`. Excerpt (four of the add entries; the rest are ` M`):
```
 A .scratch/goal-20261022-hyaku-12h.md
 A .ufo/state/kotoba.report-baseline
 A scripts/hyaku/__pycache__/append-closure.cpython-314.pyc
 A write
lines=18 untracked_marker_lines=0
```
Observation: no untracked file exists, so none can name kaidoku and round 27.

C2 — independent untracked enumeration, 2026-10-22T15:38:10Z.
`git -C /home/vgpnk/Projects/shokunin ls-files --others --exclude-standard | wc -l` → `0`, exit
0. Agrees with C1: the untracked set is genuinely empty.

C3 — meaning of ` A`, 2026-10-22T15:38:33Z. In the seat scratch, `git init -q .; echo hi >
f.txt; git add -N f.txt; git status --porcelain` printed ` A f.txt` and `git ls-files --stage`
printed `100644 e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 0 f.txt`, exit 0. The fleet root's ` A`
file entries show the same empty-blob index shape (`git ls-files --stage`, 15:39:25Z, all three
e69de29). Observation: intent-to-add entries — visible new files, not hidden untracked ones.

C4 — content of every uncommitted new entry, 2026-10-22T15:38:43Z.
`sha256sum write scripts/hyaku/__pycache__/append-closure.cpython-314.pyc
.scratch/goal-20261022-hyaku-12h.md` → exit 0:
```
95443b228053f4522714b3ba9cdb56cbce2e2c43b43b073b56e2c70978e0bac0  write
3700bf9a7137c40b7e13010ce982fbed99deed7574b8e0ef8357dfcfcc404579  scripts/hyaku/__pycache__/append-closure.cpython-314.pyc
944e47d4f2d5ff4429a3752158e5a75bb07747eebdc2b5cc3dc43414fa279ee9  .scratch/goal-20261022-hyaku-12h.md
```
Marker count for `kaidoku|KaidokuR27|round[- ]27`: `0 write`, `0` pyc, `2` goal file, exit 0. The
two goal lines name kaidoku r25; a count of `r27|round[- ]?27|KaidokuR27` over that file is `0`
(grep exit 1). `write` is 25 bytes whose whole content is `agent://U100N079H334f935b` (od -c),
mtime 2026-10-21T22:52:50Z, before this round's dispatch (2026-10-22T14:41:34Z,
`.ufo/waves/hyaku/PHASE3.md:535`). Observation: no uncommitted new entry names kaidoku and round 27.

C5 — two-token scan of non-lane fleet-root areas, 2026-10-22T15:38:23Z.
`grep -a -r -I -l -i kaidoku .ufo .scratch .tower .ruff_cache *.md MANIFEST.json shokunin.conf
.gitignore`, keep files also matching `round[- ]?27|KaidokuR27|r27`, classify with
`git ls-files --error-unmatch` → 64 hits, 60 tracked, 4 untracked, exit 0. Untracked hits:
```
untracked 2026-10-19T21:29:08Z 766bd33eedf82dc6 .tower/jj-probe/kotoba-shokunin/.ufo/round-23/scouts/C2.md
untracked 2026-10-19T21:29:08Z 932b74fa17502ea8 .tower/jj-probe/kotoba-shokunin/LOG.md
untracked 2026-10-19T21:29:08Z c4049aa94aa2b652 .tower/jj-probe/kotoba-shokunin/SCORECARD.md
untracked 2026-10-19T21:29:08Z d918f9d6618e0fb1 .tower/jj-probe/kotoba-shokunin/.ufo/round-24/scouts/C3.md
```
Same-line test on those four,
`grep -a -n -E 'kaidoku.*(round[- ]?27|KaidokuR27)|(round[- ]?27|KaidokuR27).*kaidoku'`, found
nothing (exit 1, 15:38:43Z). Context: `.tower/.../LOG.md:1268` is kotoba's own `Round 27
(loop 1)` dated 2026-10-19; its one kaidoku mention is a sibling dead-token count. Tracked hits are
expected orchestration files, chiefly `.ufo/prompts/kaidoku-round-27.md` (sha256
600b952f047347719400631fcdbbb84f302d119d12d22b1f68191d3eb4eaf28f) and
`.ufo/waves/hyaku/PHASE3.md` (sha256 `19edc5fd11ccf35b…`), both status-clean. Observation: no
round-27 kaidoku seat artifact among the hits.
A wider whole-tree `grep -rIl` that also crossed lane checkouts was started at 15:35Z and killed by
its 300 s deadline with no output (interrupted, 15:40Z); it proves nothing and is replaced by the
bounded scan above, whose scope is the non-lane fleet root.

C6 — ignored areas `-uall` cannot show, 2026-10-22T15:38:33Z. Ignored top-level names: lane
checkouts, `.jj`, `.ruff_cache`, `.tower`, `.ufo/waves/*-scratch`. Ignored files under `.ufo` and
`.scratch`: 36, newest mtime 2026-10-14T14:30:02Z. Observation: nothing ignored was written today.

C7 — top-level regular files, 2026-10-22T15:37Z window. 14 files by `find . -maxdepth 1 -type f`;
per-file `git status --porcelain -uall -- <file>`: 13 clean and tracked, only `write` shows
` A write`; today's mtime at that depth only on `README.md`, `LOG.md`, `MANIFEST.json`, all clean.

## Artifacts (seat scratch)

Base `/fast/scratch/hyaku/kaidoku-r27/seats/w2/MisrootSweep/`:
```
01d05cfa383b83912b04c95bf3494f6052fc720982c319f5d816749036ed0da0  status.porcelain.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  status.err.txt (empty)
8d71772bc04652ce092ac63b80ad8f46ca4bd2ef81d7ca182d972e216b0b2007  check.log
7896dc75964170540463a11be92757441cda0d2dda5dfb229c2460ecef8a1c58  hits.txt
4600c2ae18d68b0f6fd6e8886ad40d7c63be2d484aba2cf208974685ddc55759  t3.log
2f09b0f57e9f760868c9ef32374b1343a14524884978f4e555562fb538128c65  facts.log
855b722e814715f583a85a180f49aeb1f3fcab810d23ac74fa59ce2b88a637ed  intent-to-add-proof.txt
```

## Unknowns
- Authorship of the intent-to-add entries and the 25-byte `write` file is unrecorded; their
  mtimes precede this round's dispatch, so they are not round-27 seat writes, but the author is
  unknown (not inferred).
- A seat writing into another lane's checkout is invisible to fleet-root status; outside this item.
