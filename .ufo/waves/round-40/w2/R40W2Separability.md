# R40W2Separability — do R40-C1 and R40-C2 read each other?

**Verdict: CONFIRMED** — separability holds on committed bytes in both directions: C2 scores 26/26 with
every R40-C1 data file and tool deleted, C1 scores its same 3/4 with every R40-C2 data file and tool
deleted and `SKILL.md` reverted to the base, and the v2 AVM-marker row's *decision* cannot depend on C1
because C2's own AVM fixture is a standard-BE body with the marker, not the AVM layout. Two fixable
**documentation defects** sit in the frozen `## Separability` paragraph (`plans/round-40-claims.md:132-136`),
and one calibration limit is confirmed by mutation: the AVM row's `cause` is prose, and inverting it to
assert the opposite of C1's finding still scores 26/26.

**Attacked:** (a) whether either counter reads the other's data or tools (read sets measured with
`strace` + a `git` argv shim, plus the counters' own materialisation records); (b) whether each claim
still scores when the other claim's files are removed in a sandbox commit — both directions, plus a
poisoned-tool variant; (c) whether the v2 `avm-marker-be-dropped` row depends on C1's result, tested by
deleting C1, by relabelling the row, and by inverting its cause; (d) the shared denominator — one
post-freeze edit of `plans/round-40-claims.md` in both counters' `FROZEN` tuples. Leaf seat: no
subagents, no background jobs, no lane writes beyond this file and
`.ufo/waves/round-40/w2/artifacts/R40W2Separability/`. Evidence: 11 scored runs, three sandbox clones
under `/fast/scratch/hyaku/kaidoku-r40/R40W2Separability/` (removed at the end), artifacts listed at the
foot of this file.

## Controls

Every run used freeze `7fce308631a8b457d6b7c5a4b39a923c4e9a49de`; the carrier cache was copied from a
sibling seat's scratch and every file's sha256 equals its filename (`ac4098bd…8e95` = V1 carrier,
`5ccc7614…089b` = V2 carrier — the `carriers.json` pins). Baseline arms reproduced the L1's receipts
exactly before any deletion:

| run | tree | C1 | C2 |
|---|---|---|---|
| baseline | sandbox `sb` @ `42c10a58`, unmodified | 3/4, exit 1, only `L2: nonregular_unpublished_ok` false; `c1-extra` met, exit 0 | — |
| baseline | sandbox `sa` @ `42c10a58`, unmodified | — | 26/26, exit 0, `bindings_false: []` |
| baseline | lane tip `0b15c8b2` (after the demotion) | 3/4, exit 1, same clause, `province_core_row`/`province_core_section` false | 26/26, exit 0 |

`c1-base.json`'s L2 record carries `nonregular_published: ["firmware.bin_extract/usr/bin/busy"]` — the
suffix false positive the L1's honest stop rests on. `walk.json` holds all eleven runs in one table.

## Q1. Does either counter read the other's data or tools?

Measured, not inferred: `strace -f -e trace=openat -y` around each counter, a `git` shim on `PATH` that
logs every argv, and the counters' own declarations (`artifacts/…/read-set.txt`, `c1-gitargv.txt`).

**Direction C2 → C1: tool bytes yes, data no.** `c2-counter.py` materialises the whole of `tools/round-40`
and `tools/round-39` at the freeze (`c2-counter.py:80,493-494`) into its scratch tree; the record
`writer.materialised_files` lists 26 files, **7 of them C1's tools** (`c1-counter.py`, `c1-extra.py`,
`c1-run.sh`, `fetch-vendor.py`, `gen-squashfs.py`, `mk-l-carriers.py`, `sqfs-list.py`). It executes only
`tools/round-39/gen-squashfs.py` (as the carrier writer, `c2-counter.py:522`), the frozen generator and
the frozen interpreter. It reads **no** C1 data path and **no** shared doc: no `PROVINCE.md`, no
`corpus/README.md`, no `corpus/SOURCES.md`, no `corpus/knowledge/…`, no `corpus/evidence/round-40/c1/…`.

**Direction C1 → C2: path names only, content-blind.** `c1-counter.py` and `c1-extra.py` contain zero
references to `SKILL.md`, `sqfs-triage-v2`, `heldout-gen-v2`, `c2-counter` or `round-40/c2`. Its 34 git
invocations never name a C2 path. The one cross-read is structural: its frozen-path check issues
`git log --pretty=format: --name-only --no-renames FREEZE..REV` **without a pathspec**
(`c1-counter.py:730`), which enumerates the whole range's changed names — 131 of them are
`corpus/evidence/round-40/c2/…` at `freeze..tip`; the trace shows 27 of C2's directory-tree objects
opened for it. No C2 file *contents* are read and no binding depends on them (proved by the `sb` run).

**Writers are distinct artifacts.** C1's L carriers come from `tools/round-40/gen-squashfs.py`
(`sha256 309c502d…`), C2's held-out carriers from `tools/round-39/gen-squashfs.py`
(`sha256 f535e60e…`). The shared-name collision is a path collision only.

**Frozen-path sets intersect in exactly one path**: `plans/round-40-claims.md` (C2 `FROZEN`,
`c2-counter.py:74-75`; C1 `FROZEN_PATHS`, `c1-counter.py:208-218`). Tested: one appended comment line in
that file, committed, makes **both** counters exit 2 — `c2-S1.json` (`unevaluable:
frozen_path_changed`) and `c1-S1.json` (naming `plans/round-40-claims.md`). That is a designed shared
denominator, symmetric in both counters, and worth stating explicitly because it means the pair is not
independently scoreable if the claim file is ever touched after a freeze.

## Q2. Could each have passed with the other's files absent?

**C2 without C1 — yes.** Sandbox `sa` at `42c10a58` + one commit deleting all of it: `.ufo/waves/round-40/c1/`
(carriers.json, gap-rule.json), `corpus/evidence/round-40/c1/` (all four carriers, oracles, non-regular
tables, receipts, run logs), the knowledge entry `2026-10-26-r40-avm-be-squashfs-core.md`, and the seven
C1 tools — 34 files, 15,853 deletions (`sandbox-commits.txt`). Result: **26/26, exit 0,
`bindings_false: []`** (`c2-A1.json`). Nothing in the C2 score degraded; the counter never looked.

**C2 with C1's tools present but poisoned — still 26/26.** Sandbox `sc`: `raise SystemExit` appended to
`tools/round-40/gen-squashfs.py` and `tools/round-40/sqfs-list.py` at `REV`, committed. `26/26, exit 0,
bindings_false: []` (`c2-C-poisoned-c1-tools.json`) — C2 executes none of C1's code, so its materialised
copies are inert bytes.

**C1 without C2 — unchanged.** Sandbox `sb` + one commit deleting `corpus/evidence/round-40/c2/` (all 26
carrier/envelope/run directories), `corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md`, the three C2
tools, and **`SKILL.md` replaced by its base blob** (`git show fa6a8a3f:SKILL.md`) — 136 files, 27,529
deletions. Result: **3/4, exit 1, the identical clause map** (`L2: ['nonregular_unpublished_ok']`,
`frozen_path_changed: []`), and `c1-extra` met, exit 0 (`c1-B.json`, `c1x-B.json`). Byte-for-byte the
same verdict as the baseline arm in the same clone — the deletion changed nothing.

**C2 is invariant to C1's landing state.** At tip `0b15c8b2`, where `4d62ee5a` has already removed
`## Round-40 additions to Core` from `PROVINCE.md` and demoted the entry to "measured, not promoted",
C2 still scores 26/26 exit 0 (`c2-tip.json`) while C1's own bindings flip (`province_core_row`,
`province_core_section` false, `c1-tip.json`). The two verdicts move independently.

## Q3. Does the v2 `avm-marker-be-dropped` cause depend on C1's result?

**No, not in any scored way — and structurally it cannot.** Three independent measurements:

1. **The fixture is not C1's layout.** `sqfs-list.py --layout auto --inspect` on the committed held-out
   AVM carriers: H17 `avm_marker: true, header_endian: "big", layout: "be", mkfs_time == bytes_used`;
   H18 the same (xz). C1's genuine carrier L1: `avm_marker: true, header_endian: "little", layout:
   "avm"`. C2's AVM class is exactly the marker-on-standard-BE body the row's cause says reaches it;
   the held-out set contains no genuine AVM-layout carrier, so no envelope can test C1's layout
   (`artifacts/…/layout-probe.json`).
2. **The row is load-bearing and unique.** Renaming only its label in the frozen table (sandbox `sc`,
   `H17`/`H18` relabelled) gives **24/26** with misses exactly `H17, H18` (`c2-M1.json`) — no other row
   silently covers those envelopes, so the row is not duplicated authority and its presence is what
   carries the 2 envelopes.
3. **The cause is unscored.** Inverting the row's cause to assert the opposite of C1's finding
   ("a genuine AVM-layout body always fails without -be …") still scores **26/26**
   (`c2-M2.json`); the only binding that fires is `v2_table_identical`, because any post-freeze edit to
   the table block is rejected by byte identity. So the table's prose truth is checked only by review at
   freeze time — which the C2 entry already discloses ("The `cause` column is prose and is not scored").

The residual coupling is documentary, not mechanical: `SKILL.md:368`'s cause and
`corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md:37-45` both state "a genuine AVM-layout body … extracts
without `-be`", whose only round-40 measurement is R40-C1 — measured, **not promoted**. The knowledge
entry names the C1 entry, which states its own status, so no false promotion is asserted; and C2's
26/26 does not become a claim about AVM coverage.

## Defects found (fixable; documentation and freeze-scope, no dependency)

**D1 — the `## Separability` paragraph's C2 read set is incomplete** (`plans/round-40-claims.md:134-135`).
It says "C2 reads SKILL.md, its interpreter, generator and held-out evidence". Measured, C2 also reads
(a) `plans/round-40-claims.md`'s history (it is in C2's `FROZEN` tuple), (b) the frozen
`tools/round-39/gen-squashfs.py` writer, and (c) every tracked file under `tools/round-40` and
`tools/round-39` at the freeze — 26 files, 7 of them C1's tools, materialised as opaque bytes.
Severity: documentation. No score dependency (Q2 proves it).
*Smallest safe correction:* extend the clause to "…and, at the freeze, the `tools/round-40` +
`tools/round-39` trees it materialises to run the generator (opaque bytes; no C1 data, no C1 code
executed)". `plans/round-40-claims.md` is frozen for both claims, so this is a round-41 errata, not an
in-place edit.

**D2 — the AVM pointer is attributed to the wrong artifact** (`plans/round-40-claims.md:135-136`: "the v2
AVM-marker row's cause points to the C1 entry by name only"). The SKILL v2 row's `cause` cell names no
entry; its `source` cell points at the C2 knowledge entry. The C1 entry is named only in
`corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md:42-44`. Severity: documentation / provenance precision.
*Smallest safe correction:* "…the C2 knowledge entry's AVM paragraph points to the C1 entry by name
only". Also an errata to the frozen file.

**D3 — C1's frozen-path check reads the other claim's path names** (`tools/round-40/c1-counter.py:730`):
the unpathspaced `git log --name-only` over `FREEZE..REV` opens 27 of C2's directory-tree objects.
Content-blind, no binding effect, but it makes the read set range-sized. *Smallest safe correction* (needs
a re-freeze): pass `FROZEN_PATHS` as the pathspec, as `c2-counter.py:134-136` already does.

**Calibration note (not a defect, disclosed):** M2 shows a false `cause` would ship undetected as long as
it was authored before the freeze; `v2_table_identical` only forbids *changing* it later. Since the C2
knowledge entry is **not** in C2's frozen set (verified: the counter reads no knowledge file), the honest
and safe follow-up is to add the "measured, not promoted (R40-C1 stopped)" qualifier to that entry's AVM
paragraph — it cannot disturb the 26/26.

## Impacted axes

- **coverage (R40-C1)** — untouched by this seat; the 3/4 and its single clause reproduce exactly, at
  `42c10a58` and at tip. C1's verdict does not depend on C2 in any way measured here.
- **depth (R40-C2)** — the 26/26 is independent of C1 and of `PROVINCE`; the AVM row is load-bearing for
  2/26 and unique. Its row decisions are unaffected by C1's landing state.
- **calibration** — the pair is score-independent but shares one frozen denominator (`plans/round-40-claims.md`),
  so one post-freeze edit voids both; and the AVM row's prose truth is review-only. D1/D2 are the record's
  own inaccuracies about its read set, which is exactly the kind of claim a critique round should fix
  before the pair is cited as "separable".

## Not attacked (other seats own it)

Forged-manifest/fabrication paths inside C2 (the manifest declares the correct round-39 writer sha; the
`None`-permissive sha bindings are C2-internal, `c2-counter.py:428,513`); the counters' own
selftest suites; C1's clause semantics. One observation worth passing on: the v2 interpreter's
`--selftest` is lane-coupled — `sqfs-triage-v2.py:137-140` resolves `LANE` absolutely and reads
`corpus/evidence/round-39/{c1,c2}` plus `LANE/SKILL.md`; run from scratch cwd it printed
`SELFTEST cases=45 pass=45 fail=0`, i.e. it read the real lane and round-39's C1 evidence, not the tree
under test. The scored path is unaffected (the counter passes explicit envelope paths).

## Reproduce

```
S=/fast/scratch/hyaku/kaidoku-r40/R40W2Separability; mkdir -p "$S"; export HYAKU_SCRATCH=/fast/scratch/hyaku TMPDIR=$S/tmp
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
git clone -q --shared "$L" "$S/sb" && git -C "$S/sb" checkout -q 42c10a58
cp <sibling cache>/*.bin "$S/cache/"          # sha256 must equal the filename
# baseline
python3 -I -B "$S/sb/tools/round-40/c1-counter.py" --root "$S/sb" --rev 42c10a58 \
  --freeze 7fce3086 --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --carrier-cache "$S/cache" --json-out "$S/c1-base.json"           # exit 1, 3/4
# C2 with C1 absent: delete .ufo/waves/round-40/c1, corpus/evidence/round-40/c1, the entry, the 7 C1 tools; commit
python3 -I -B tools/round-40/c2-counter.py --root "$S/sa" --rev HEAD --freeze 7fce3086 \
  --json-out "$S/c2-A1.json"                                        # exit 0, 26/26
```
Every sandbox commit used `-c user.name=fx -c user.email=fx@fx`; `git rev-parse --show-toplevel` was
asserted to print the sandbox before each commit. No lane file, no VCS state in the lane and no vendor
byte was written or copied. Tooling: nothing installed (python3, git, strace 7.2 were already present and
are the only tools this seat added to the run); `strace` and the `git` argv shim live in scratch only.

## Artifacts

`.ufo/waves/round-40/w2/artifacts/R40W2Separability/`: `walk.json` (all 11 runs), `c1-base.json`,
`c1-B.json`, `c1-tip.json`, `c1-S1.json`, `c1x-base.json`, `c1x-B.json`, `c2-base.json`, `c2-A1.json`,
`c2-tip.json`, `c2-C-poisoned-c1-tools.json`, `c2-M1.json`, `c2-M2.json`, `c2-S1.json`,
`layout-probe.json`, `c1-gitargv.txt`, `read-set.txt`, `sandbox-commits.txt`.

## Lane state at finish (not this seat's writing)

`git -C <lane> status --porcelain` shows `M SKILL.md` — a 19-line "### Round-40 instrument registry"
section appended after line 1384, file mtime 16:24:08, i.e. before this seat's first run and not written
here. It does not affect any number above: both counters read `SKILL.md` through `git show <rev>:SKILL.md`
(`c2-counter.py:446-448`), so working-tree dirt is invisible to them — which is also why the M1/M2 probes
had to be committed in the sandbox. Flagged because a dirty C2 surface in the working tree would mislead
anyone who inspects the tree instead of a rev.

Report: .ufo/waves/round-40/w2/R40W2Separability.md
