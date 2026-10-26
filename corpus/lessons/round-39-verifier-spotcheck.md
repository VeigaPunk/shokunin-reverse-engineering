author: hyaku closure (non-author integrator, @m_opus)

# kaidoku round 39 — verifier spot-check (non-author closure)

Scope: lane-round kaidoku r39, attempt 1. Pre-round lane HEAD `a2f64e1da78afcf8cc39287106604dbcc270844c` → after `8b9634ed8253653e7eb994aad9860a624e3b0366` (branch `main`).
Report: `.ufo/reports/round-39/kaidoku.md` (fleet repo). Prompt: `.ufo/prompts/kaidoku-round-39.md`.
Lane gates and counters were **not executed** (PROTOCOL §Gate standard, Closure consequence). Every re-measurement below is a plain read of committed bytes (`git show <rev>:<path>`, `jq`, `sha256`, Python stdlib over blobs) or a live re-open of a public source.

Driver digest (copied from mutable `.ufo/watchdog.log`):

```
2026-10-26T13:00:45-03:00 launch kaidoku round=39 pgid=159311 driver=hyaku-inline attempt=1
2026-10-26T14:57:54-03:00 complete kaidoku round=39; hyaku-inline attempt=1
```

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report landed by the lane identity | `git log --format='%an %H' -- .ufo/reports/round-39/kaidoku.md` | `kaidoku-shokunin e3b4783cbc5e5e67a83d700797607bf2b3d8bdc5` (commit 14:57:24; adds only the report, +164) | pass |
| lands last | `git -C <lane> log -1 --format=%cd 8b9634ed` vs report commit | lane tip 14:55:51 < report commit 14:57:24 < `complete` 14:57:54 | pass |
| `SHONEN` heading | read report `## SHONEN` vs `SHONEN.md` | 4 lines, 4 boxes (`SHONEN.md:5,7,9,11`), all `[~]` with pointers | pass |
| cited hashes exist and are ancestors | `git cat-file -t <h>` + `git merge-base --is-ancestor <h> main` for the base, `8fcda41c`, `72359309`, `3c07eed7`, `6fdaf4f1`, `52b0eb29`, `e40a25df`, `2b0b6a29`, `8b9634ed` | all 9 `commit`, all ancestors of `main` | pass |
| pushed, no leftovers | `scripts/hyaku/jj-lane.sh state <lane>`; `git -C <lane> status --porcelain` | `local=remote=8b9634ed… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty | pass |
| prompt carries the template contract | line-by-line regex match of `templates/round-prompt.md` (placeholders as wildcards) against the prompt's first 140 lines | 140/140 template lines matched (line 1 differs only by the legacy `<{{LANE}}-repo>` substitution); hyaku addendum §6 and §7 appended after | pass |
| frozen paths untouched after the freeze | `git log 8fcda41c..8b9634ed -- tools/round-39 plans/round-39-claims.md .ufo/waves/round-39/c1/carriers.json corpus/evidence/round-39/c1/K{5,6}/{carrier.sqsh,oracle.tsv,symlinks.tsv}` | empty; blobs of `c1-counter.py` `182308e4`, `c2-counter.py` `bc20933b`, `sqfs-triage.py` `b5c5379a`, `heldout-gen.py` `08869713`, claims `f6707233` equal at freeze, `6fdaf4f1` and tip; SKILL triage block (marker → next heading) byte-identical at freeze and tip | pass |
| gate registry rows | grep `SKILL.md` | `c1-counter.py`, `c2-counter.py`, `sqfs-triage.py`, `absence-sweep.py` rows at `SKILL.md:1346,1351,1353,1354` with verdict maps and selftest spellings | pass |

Conformance defects (status-neutral, see §5): the report has no explicit "cross-domain evidence encountered" line (PROTOCOL §Round-robin minimum content; it names only the same-domain AVM merge theme and an unchanged Adjacent); the cited score JSONs carry no exit-code field, so the report's "exit 0" for C1/C2 rests on the wave-2 rescore reports, not on the cited `l1/scores/*.json`; the report's "3084 bytes" for the triage block is a boundary choice (my slice marker → `\n#` is 3088 B), and identity holds either way; both wave ledgers carry `status: null` for every seat (disclosed).

## 2. Claims

### R39-C1 — coverage, standard BE SquashFS v4 Frontier → Core (author: met) — re-measured

Before: `PROVINCE.md` at `a2f64e1d` and at `8fcda41c` has 0 `## Round-39 additions to Core` sections. After, at `6fdaf4f1`, it has one, with a row naming `squashfs_v4_be` (`PROVINCE.md:378-382` at the tip, frontier note `:384`, pointers at `:157`, `:376`).

Receipts, re-derived with my own script (Python over `git show 8b9634ed:<path>`). For each carrier in `carriers.json` I checked:

- the carrier sha256 equals its pin;
- each oracle row `(relpath, sha256)` is published at a path with the same suffix and the same sha256;
- the gap kinds;
- the in-tree and escaping links from `symlinks.tsv`;
- whether any escaping path is published;
- the chunk handler and whether `MaliciousSymlinkRemoved` appears in `diagnostics`.

| carrier | pin | oracle matched | files | gaps | in-tree / escaping | escaping published | handler | MSR |
|---|---|---|---|---|---|---|---|---|
| K1 | ok | 5/5 | 5 | none | 0 / 1 | none | `squashfs_v4_be` | yes |
| K2 | ok | 3/3 | 3 | 1 `unpublished-entry` | 1 / 0 | — | `squashfs_v4_be` | no |
| K3 | ok | 4/4 | 4 | none | 0 / 0 | — | `squashfs_v4_be` | no |
| K4 | ok | 4/4 | 4 | none | 0 / 0 | — | `squashfs_v4_be` | no |
| K5 | ok | 10/10 | 10 | 2 `unpublished-entry` | 2 / 1 | none | `squashfs_v4_be` | yes |
| K6 | ok | 8/8 | 8 | 1 `unpublished-entry` | 1 / 2 | none | `squashfs_v4_be` | yes |

Results:

- All six carriers meet the frozen symlink rule: exactly one gap per in-tree link, and no escaping path is published.
- Symlink totals: in-tree 4, escaping 4, at most 2 per carrier. These equal the counter's `symlink_coverage_detail`.
- K6's chunk record shows `"extraction_failed": false`.
- Superblock bytes: every carrier starts with `sqsh` (big-endian) and has major version 4 at offset 28. The compression id at offset 20 is `1` (gzip) for K1–K5 and `4` (xz) for K6. This equals `xz_leg_detail`.
- The committed counter evidence agrees: `l1/scores/c1-at-6fdaf4f1.json` and `c1-at-2b0b6a29.json` have `carriers_matched 6`, `target 6`, `met_target true` and `frozen_path_changed []`.
- The do-nothing control `controls/ctl-c1-0-do-nothing.json` has `carriers_matched 0` and `met_target false`.
- Self-test evidence `w1/artifacts/R39C1Counter/selftest-output.json`: 33 cases (1 green, 32 red), no failures.

**Verdict: verified (0 → 6/6), and I re-measured it.** The counter cannot refuse a re-minted fabricated receipt (`w2/R39W2C1Fabricate.md`). The freeze discloses this limit. My re-derivation reads the committed receipts' own contents, so it shares that limit. Six lane-dispatched re-runs (`w2/R39W2ReproK{1..6}.md`) are the only independent provenance evidence.

### R39-C2 — depth, executable SquashFS outcome-triage table in SKILL (author: met) — re-measured

Before: `SKILL.md` at `a2f64e1d` has no `<!-- sqfs-triage-table v1 -->` block, so it labels 0 of 20.

After: I wrote my own evaluator. It parses the 8 rows of the SKILL table at `8b9634ed` (wildcards `*`/`n/a`, globs `squashfs_v4_*`, `>0`; first match wins; no match gives `unclassified`). It extracts the six fields itself from each committed `corpus/evidence/round-39/c2/heldout/H*/envelope.json`:

- handler;
- the set of gap kinds;
- the union of `dependencies`;
- a standalone `-be` in a recorded sasquatch `command`;
- `MaliciousSymlinkRemoved`;
- the file count.

Result: **20/20** of my labels equal `manifest.json`'s expected labels. The manifest seed equals the freeze `8fcda41c…`, and every held-out carrier's sha256 equals its manifest pin. The held-out data first lands in `3c07eed7`, which descends from the freeze, and no later commit touches it.

Committed counter evidence: `l1/scores/c2-at-6fdaf4f1.json` and `c2-at-2b0b6a29.json` record `matched 20`, `n 20`, `met_target_consistent true` and `interpreter_exit 0`. At the freeze, `c2-at-freeze.json` records `no_manifest_at_rev`. Self-test tallies:

- `sqfs-triage.py`: 35/35 (`w2/artifacts/R39W2C2Rescore/sqfs-triage-selftest.txt`);
- `c2-counter.py`: 27/27 (`w1/artifacts/R39C2Counter/evidence/selftest.txt`);
- `absence-sweep.py`: 18/18 (`l1/absence/selftest.txt`).

**Verdict: verified as frozen (0 → 20/20), and I re-measured it.** My evaluator reads only the SKILL table bytes and the envelopes, so the table works without oral context.

Wave 2 bounds how much this score shows (`w2/R39W2C2AxisFit.md`, `w2/R39W2C2TableReview.md`):

- the axis proxy was already saturated;
- an 8-row table with 7 non-`*` cells also reaches 20/20;
- the `cause -> action` column is not scored;
- the 20 envelopes contain 9 distinct predicate decisions;
- rows 5 and 8 exclude two measured outcomes;
- mixed-symlink images (K5 and K6) get the `escaping-symlink-removed` label, whose action contradicts their own `unpublished-entry` gaps;
- the interpreter labels non-firmware envelopes (`no-squashfs-chunk`) because it has no `operation`/`provider` guard.

All of these are marked in the triage knowledge entry (`corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md:47-48,55-74`) and in the SCORECARD round-39 record. None falsifies the frozen claim, and none harms an existing axis value. I route them as next-version defects (§5).

### Harm check (owned axes coverage, depth, calibration)

`git diff a2f64e1d 8b9634ed -- SCORECARD.md` shows these changes: coverage row 126/126 → 128/128, depth row 17/17 → 18/18, calibration row unchanged, two capability rows added, and the `## Round 39` section appended. Nothing is rewritten except the living coverage/depth rows. I recounted each axis myself:

| axis | base | tip | what I counted |
|---|---|---|---|
| coverage | 126/126 | 128/128 | `corpus/knowledge/*.md` files whose slug appears in `corpus/README.md` |
| depth | 17 | 18 | top-level `- **` rule blocks in `## Queue-drain craft` (`SKILL.md:81-318` at base, `:81-347` at tip; last non-blank line 343, matching the SCORECARD/SHONEN pointer `SKILL.md:81-343`) |
| SOURCES rows | 117 | 122 | the census command |

Other checks:

- PROVINCE `## Adjacent` `PROVINCE.md:97-125` has the same md5 at base and tip (`df8f0553…`).
- SOURCES.md is append-only plus one `used-by` change (S112), which the lesson logs.
- The `round-38` false-absence corrections hold: both cited shokuknow tsvs exist (`ls`).

No axis is harmed. Verdicts:

| axis | verdict |
|---|---|
| coverage | improved |
| depth | improved (claim verified as frozen; the saturated proxy and unscored columns are noted above) |
| calibration | unchanged |
| operability | unchanged |
| freshness | unchanged |
| adjacency | unchanged |

## 3. Discernment spot-check (`corpus/lessons/round-39.md` `## Gate`)

| item | gate decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S122 unblob `file_utils.py` `is_safe_path` | admit (A, mined) | `curl https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/file_utils.py` → HTTP 200, 27989 B, sha256 `87d4dc9a…0745` | agree | size and sha equal the row; the ≤25-word quote `basedir.joinpath(path).resolve().relative_to(basedir.resolve())` is at the cited `is_safe_path` lines 34-39 (`def` at 34, `return True` at 39) |
| S118 unblob `extractor.py` symlink sanitiser | admit (A, mined) | same tag, `extractor.py` → HTTP 200, 4129 B, sha256 `1bb49811…cd23a` | agree | sha equals the row; the docstring quote "either removed it it attempts to traverse outside of the extraction directory or rewritten to be fully portable" is at lines 53-55 (docstring 51-57); the 73-77 / 79-87 / 88-91 anchors match. The row's scope omits the second report site (recursive link, lines 58-65); the lane discloses this (`w2/R39W2SrcReopen.md`) |
| S121 sasquatch `unsquashfs.c` at `sasquatch-v4.5.1-6` | admit (A, mined) | `unsquashfs.c` → sha256 `ece42b66…4cb40`, 4619 lines; `debian/rules` lines 16-18 hold `CFLAGS=-DFIX_BE dh_auto_build` | agree (loose anchor) | file identity equals the row; the quoted line lives in `debian/rules`, whose URL and sha the row does not record (disclosed, `w2/R39W2SrcReopen.md`) |
| `avm-image-build-blocker` (shokuknow `merge/kaidoku`) | reject | `/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/avm-image-build-blocker.md` | agree | its claim "a real AVM image is one release away" is superseded by the producer's own later entry `avm-image-extraction.md` ("A real AVM-BE image extracts", round 11, `MERGE-REPORT.md:79`): the premise is stale |
| `avm-le-variant-reachability` | reject | same dir, `avm-le-variant-reachability.md` vs `avm-le-image-genuine-marker.md` | agree | the producer's round-13 entry overturns it explicitly: "the round-12 measurement that said it was not came from a stale binary" |

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` exits 0 with 12× `W04` (duplicate URL across scopes). The new warning is S119, a reuse of the rea-agents 6.5.0 tarball URL. This equals the report's `census-end.txt`.

Spot-check result: the gate's admits and rejects agree with the outside sample. There is no disagreement to learn from. Loose anchors (S118 scope, S121 second file) are disclosed rather than hidden.

## 4. Trend verdicts

| trend | verdict | evidence |
|---|---|---|
| expansion | **improved** | Two admitted entries on ground the coverage map did not hold: `2026-10-26-r39-be-squashfs-v4-core` cites S122, and `2026-10-26-r39-sqfs-outcome-triage` cites S112 and S118–S121, all `mined`. Both are mapped (128/128). Standard BE v4 moved from Frontier to Core on 6 re-derived carriers, including xz and UTF-8 names. Two capability rows entered with running demonstrations. |
| quality | **improved** | The round-38 false-absence withdrawals are verified: both files exist. QUALITY 82 carries a gate with an 18-case selftest. Three round-38 gates gained selftests. Every wave-2 limit on the new table is marked in its entry, so no admitted entry was found false and left unmarked. |
| discernment | **improved** | The outside sample agrees with the gate on 3 admits and 2 rejects (§3). The disputed AVM admits were deferred rather than forced. The C1 fabrication limit was disclosed before data. |

## 5. Routed defects (lane fixes next round; status-neutral)

- **R39-CL1:** `tools/round-39/sqfs-triage.py` has no domain guard. It labels non-`extract-firmware`/non-`unblob` envelopes (`w2/R39W2C2AxisFit.md` C2). The registry row "labels REA envelopes" (`SKILL.md:1351`) is over-broad as written. Add the `operation`/`provider.id` precondition that the prose table already states.
- **R39-CL2:** SKILL rule block 18 (`SKILL.md:316-343`) does not itself carry the mixed-symlink caveat; only the entry does. Images with both link kinds (K5 and K6, 2 of 6 Core carriers) get an action that tells the reader to ignore their in-tree gaps. Add a row or held-out class, or a caveat line, in table v2.
- **R39-CL3:** Rows 5 and 8 exclude measured outcomes: `full-be1-xz` damaged with P>0, and `full-be-dirempty-gzip` clean with P=0 (`w2/R39W2C2TableReview.md` D1, D2). The C2 counter scores labels only. Score the matched rule index or the cause column, and make the held-out replicates differ so that 20 means 20 decisions.
- **R39-CL4:** Kill controls `CTL-C2-5`/`CTL-C2-6` could not be evaluated at the freeze. Their `.formatfix` inputs first landed in `72359309`, after `8fcda41c`. This is the QUALITY 80 pattern. Validate control-table format in the freeze.
- **R39-CL5:** The C1 counter cannot refuse a re-minted fabricated receipt (`w2/R39W2C1Fabricate.md`). The lane already plans this for round 40.
- **R39-CL6:** The report lacks an explicit cross-domain-evidence line. Its cited `l1/scores/*.json` carry no exit code. Both wave ledgers have `status: null` per seat. Record exit codes in score receipts and fill seat status.
- **Still open, carried from the lane's own list:** the `heldout-gen.py` `corruption_bad_minor` docstring erratum (frozen bytes); surviving interpreter and counter mutants (`w2/R39W2TriageMutants.md`, `w2/R39W2C2Mutants.md`); loose quote anchors for S118 and S121; R36-CL5.

## 6. SHONEN note for the operator

All four boxes are `[~]`. A non-author can check each of them from committed bytes:

- **Box 1:** 18/18 cited rule blocks.
- **Box 2:** I re-derived the six REA `extract-firmware` receipts against their oracles.
- **Box 3:** a non-author evaluator reading only the SKILL table reproduced 20/20.
- **Box 4:** the Adjacent block is byte-identical to base.

The operator owns promotion. This closure writes no `[x]`.
