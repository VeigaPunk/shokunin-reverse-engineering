# CriticSourcedClaim — kaidoku round 18, wave 1 (critic, author-side advisory)

Target: the sourced-claim duty (`/home/vgpnk/Projects/shokunin/.ufo/prompts/kaidoku-round-18.md:73-74`, and
`/home/vgpnk/Projects/shokunin/PROTOCOL.md:141-142`: "files at least one claim of the round as *sourced* — its evidence citing an `S###` row").
Planned mapping under attack: `claims.json:14` (C1 → S033), `:21` (C2 → jj docs), `:28` (C3 → Go notes / internal/abi).
Axes: calibration (does the cited row actually carry the claim?), operability (can the row be opened and anchored
stably today?), depth (does the row add knowledge the lane did not already hold?).

## Verdict

- **File C3 as the sourced claim, on a new tier-A `code` row for `internal/abi/map_swiss.go` + `map_noswiss.go` (+ `type.go`).**
  Go 1.24 release notes are a second, narrower row (they ground only the `noswissmap` carrier arm).
- **C2 is an acceptable second sourced claim only if** the jj row is anchored at v0.45.1 (not `/latest/`) and its
  `teaches` stays at "jj usually leaves Git HEAD detached" — the doc does not say HEAD differs from the branch tip.
- **Do not file C1 as the sourced claim.** S033 is legitimate curation, but as a learning source it is
  bookkeeping, and C1 citing it is circular. Keep S033 in Sources & frontier as an added row / correction.

## Counterexamples and evidence

### 1. C1 ← S033 is circular (calibration: harmed if filed)

- Observation: the C1 counting check for R17-S032-DIGEST passes for *any* 11-column row "whose teaches cell starts
  with `supersedes S032 —` and whose anchor cell contains `fetch-time`" (`contract.md:44-45`). What S033 teaches
  never enters the check. So C1 does not *rest on* S033. C1 *produces* S033, and S033 is one of its six measured
  deliverables (`claims.json:12-13`).
- Observation: the other five defects (PINMAP, VALIDATE16, PRODUCER-REV, SUMS-RUNLOG, REGISTRY) and the new QUALITY
  row draw on the lane's own outside spot-check (`corpus/lessons/round-17-verifier-spotcheck.md:137-147`), not on
  any external source.
- Observation: S033's domain content is the same as S032's: same PR, same tier B `community` scope
  (`corpus/SOURCES.md:38`). The r17 verifier already judged S032 "correctly tier B and a lead only"
  (`round-17-verifier-spotcheck.md:107`). The only new information is metadata: GitHub HTML digests are not stable
  (`round-17-verifier-spotcheck.md:147`).
- Inference: that metadata lesson belongs in `## Mistakes` / QUALITY (an anchor-stability lesson), not as the round's
  learning source. CORPUS sanctions the superseding row as the form a correction takes (`CORPUS.md:116-118`), so
  S033 is valid curation and counts toward the census and rows-added. It just cannot carry the sourced duty
  without self-reference. A strict verifier could also argue that re-opening a source already registered in r17
  is not "a row opened this round" in substance. That leaves the duty ambiguous, which is a calibration risk.
- Strongest counterexample: replace S033's `teaches` with any text after `supersedes S032 —` and keep `fetch-time`
  in the anchor. C1 still closes 6→0. A claim whose evidence does not change when its source's content changes
  is not sourced.

### 2. C3 ← internal/abi row is load-bearing and fills a real gap (calibration + depth: improved)

- Observation: r17's aether INFERENCE states "aether's maps use the Swiss layout (0x70 bytes)" against
  `internal/abi.OldMapType` (0x58) (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:145-148`). The
  entry's `source:` line cites S003, S023, S024, S025, S026, S029, S031 and S032, and no `internal/abi` source
  (`:1`; grep count 0 below). At baseline nothing in `corpus/` or `SKILL.md` cites `map_swiss`/`SwissMapType` except
  S032, which is tier B (`git grep` below). The 0x70 figure therefore has no tier-A source today.
- Observation: `go-1.25.0/src/internal/abi/map_swiss.go:32-43` (`SwissMapType`: Type, Key, Elem, Group, Hasher,
  GroupSize, SlotSize, ElemOff uintptr, Flags uint32) and `map_noswiss.go:25-36` (`OldMapType`: …, KeySize uint8,
  ValueSize uint8, BucketSize uint16, Flags uint32). Both files are **byte-identical in go1.24.6 and go1.25.0**
  (same sha256, below), so one row covers both arms of the pair.
- Inference (my arithmetic from `type.go:20-42`, amd64): `abi.Type` = 48 B. Swiss = 48+4·8+3·8+4 = 108 → 112 = 0x70.
  Old = 48+4·8+1+1+2+4 = 88 = 0x58. This matches r17 `:146-148`. The emulator's `true_size` vs `ghidra_size`
  (`contract.md:115-116`) is exactly this difference, so the row moves C3's predictions.
- Observation: noswissmap still builds in 1.25.0: `runtime/map_noswiss.go:5` and `internal/abi/map_select_noswiss.go:5`
  carry `//go:build !goexperiment.swissmap`, and the `SwissMap: true` default is set at `internal/buildcfg/exp.go:85`
  (1.25.0) and `:81` (1.24.6). The source tree, not the 1.25 notes, grounds the 1.25 noswiss arm.
- Observation: the Go 1.24 notes ground the opt-out. Under `<h2 id="runtime">` (page lines 560-574; there is no
  dedicated id) the quote reads: "The new builtin `map` implementation and new runtime-internal mutex may be
  disabled by setting `GOEXPERIMENT=noswissmap` and `GOEXPERIMENT=nospinbitmutex` at build time respectively."
  (21 words). The page sha256 `d35c2d52…` was stable across two fetches. The notes say nothing about descriptor
  layout, so they cannot carry the misread mechanism.
- **Defect to fix (operability/calibration):** the spec's evidence basis for C3 is `swiss-misread.py` `basis:
  [Base-src.zip member:line ...]` (`contract.md:117`), which is S003 (opened round 16). As specified, C3's landed
  evidence would cite **no row opened this round**, and C3 would not be formally sourced. The duty needs the
  landed evidence or knowledge entry to cite the new `S###` (`kaidoku-round-18.md:73-74`;
  `CORPUS.md:163-166`, the `source:` provenance trio).

### 3. C2 ← jj docs grounds the premise only partly (calibration: neutral if scoped; harmed if overstated)

- Observation, jj v0.45.1 `docs/git-compatibility.md` (raw, sha256 `0fb71f99…`): ":114-115" reads "`jj` commands will
  usually put the Git repo in a "detached HEAD" state, since in `jj` there is not concept of a "currently tracked
  branch"". `:208` (a comment inside the manual colocation procedure) reads "Convince jj to update .git/HEAD to point
  to the working-copy commit's parent".
- Observation (lane): HEAD is detached but **equal** to `refs/heads/main` and `refs/remotes/origin/main` (9011581,
  below). A detached HEAD alone does not make `git rev-parse HEAD` record the wrong commit. The C2 red state needs an
  unbookmarked commit (`contract.md:89-91`), and only the own-work sandbox receipt shows that, not the doc.
- Inference: the doc grounds "why pin to `refs/heads/main` and not HEAD". The defect itself is grounded by
  `jj-red-before.py`. A `teaches` cell or knowledge sentence saying "jj docs state HEAD ≠ branch tip" would be false
  provenance.
- Operability: `/latest/` is a moving anchor, the same defect class as R17-S032-DIGEST. The versioned pages
  `https://jj-vcs.github.io/jj/v0.45.1/git-compatibility/` and `raw.githubusercontent.com/jj-vcs/jj/v0.45.1/docs/git-compatibility.md`
  both return 200. Also, the C2 deliverables in `contract.md:49-98` (tools, receipt) have no field that cites an
  `S###`. C2 is formally sourced only if the SKILL note or a knowledge entry cites the row.
- Province: `PROVINCE.md` has no git/jj ground (grep is empty). The row is operational, not domain. That is allowed
  (the contract has no domain restriction), but it adds nothing to the expansion count (`CORPUS.md:123-125`).

### 4. S033 operability hazard (observation)

- `api.github.com/repos/NationalSecurityAgency/ghidra/pulls/9348` returned **HTTP 403, rate limit exceeded** for
  this host. Any seat that depends on the API for head sha/state (ScoutPr9348Reopen, DraftS033Row) may come back
  empty. A rate-free fallback works: `git ls-remote` → `refs/pull/9348/head a214355498e84aa86280be0c31c955aaf94f2d12`,
  `refs/pull/9348/merge b25164e7…`. Inference: the merge ref is still present, which is consistent with OPEN, but it
  does not prove "unmerged".

## Smallest safe corrections (L1 integrates; I edited nothing else)

1. `claims.json` C1 `sourced`: drop it, or change it to "frontier curation row S033 (correction of S032); not the round's
   sourced claim". Report S033 under Sources & frontier as an added row / S032 correction.
2. C3: open and register a tier-A `code` row: `internal/abi` `map_swiss.go:32-43`, `map_noswiss.go:25-36`,
   `type.go:20-42` at tag go1.25.0, with file sha256 `0e2fedbe…` / `03db5a82…` and a note that they are identical
   at go1.24.6. Cite that `S###` in (a) the C3 knowledge entry's `source:` line and (b) `swiss-misread.py`'s `basis`
   next to the Base-src members. Optionally add the Go 1.24 notes row (docs, A, anchor `h2#runtime` lines 568-574,
   sha `d35c2d52…`) for the noswiss arm only.
3. C2 (if also filed): anchor at v0.45.1 with quote `:114-115`; `teaches` = "detached HEAD is the normal colocated state,
   so HEAD is not a branch pin". Cite the row in the SKILL "Revision pins under jj" note.
4. S033: get the head sha via `git ls-remote`, not the API.
5. Risk note: C3 lands only after the eight sequential L1 Ghidra runs. If C3 fails to land, the sourced duty falls
   to C2 (with corrections 3/4), never to C1.

## Commands (all run 2026-10-20; exit = last pipeline stage where piped)

```
cd LANE && git rev-parse HEAD refs/heads/main refs/remotes/origin/main            # exit 0 → 9011581d… ×3
cd LANE && git rev-parse --symbolic-full-name HEAD                                 # exit 0 → "HEAD" (detached)
jj --version                                                                       # exit 0 → jj 0.45.1-7c41cdeb…
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku   # exit 0 → kaidoku ok
cd LANE && grep -n -i "go1.24\|go 1.24\|swiss\|internal/abi\|jj\|jujutsu\|GoRttiMapper\|Base-src\|rev-parse" corpus/SOURCES.md   # exit 0 → S003,S004,S029,S032 + paths/log; no go1.24/abi/jj row
cd LANE && sed -n 1p corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md | grep -c -i 'internal/abi\|map_swiss'   # → 0
cd LANE && git grep -n -i 'map_swiss\|SwissMapType' 9011581 -- corpus/ SKILL.md     # → only corpus/SOURCES.md:38 (S032)
sha256sum go-1.2{5.0,4.6}/src/internal/abi/map_{swiss,noswiss}.go                  # exit 0 → swiss 0e2fedbe… both; noswiss 03db5a82… both
grep -n "go:build" go-1.25.0/src/internal/abi/map_select_noswiss.go go-1.25.0/src/runtime/map_noswiss.go   # exit 0 → :5 !goexperiment.swissmap
grep -n -i swissmap go-1.2{5.0,4.6}/src/internal/buildcfg/exp.go                   # exit 0 → 1.25.0:85, 1.24.6:81 SwissMap: true
for i in 1 2; do curl -sL https://go.dev/doc/go1.24 | sha256sum; done               # d35c2d52… twice (stable)
curl -sL https://go.dev/doc/go1.24 | sed -n '560,576p'                              # exit 0 → h2 id="runtime" + noswissmap sentence
curl -sL -o /dev/null -w '%{http_code}' jj-vcs.github.io/jj/{latest,v0.45.0,v0.45.1}/git-compatibility/ + raw v0.45.1 md   # 200 ×4
curl -sL raw.githubusercontent.com/jj-vcs/jj/v0.45.1/docs/git-compatibility.md | sha256sum   # 0fb71f99… (one fetch; stability unverified)
curl -sL https://api.github.com/repos/NationalSecurityAgency/ghidra/pulls/9348      # HTTP 403 "API rate limit exceeded"
git ls-remote https://github.com/NationalSecurityAgency/ghidra 'refs/pull/9348/*'   # exit 0 → head a2143554…, merge b25164e7…
```

Installs: none. Writes: this file only.
