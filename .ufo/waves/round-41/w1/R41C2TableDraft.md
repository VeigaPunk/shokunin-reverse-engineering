# R41C2TableDraft — SKILL rule block 20 (table v3), its knowledge entry, and the row-by-row rationale

**DONE** — block 20, the v3 knowledge entry, the two supersession sentences and a row-by-row rationale
are drafted, and the block is proved to parse and to decide the round-40 data plus eighteen
precedence-derived combined sets before the freeze (48/48, with a red control at 0/4 and 7/18).

Seat: `R41C2TableDraft` (leaf; no subagents, no background jobs, no `agent://all`). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `49096c7e6f226af0c750c4b003be58883cb6049f`
(read-only). Nothing committed, nothing frozen; `SKILL.md`, `corpus/`, `tools/`, `plans/`,
`PROVINCE.md`, `SCORECARD.md` untouched. The L1 integrates.

## Deliverables (all under `.ufo/waves/round-41/w1/artifacts/R41C2TableDraft/`)

| file | sha256 | what |
|---|---|---|
| `block20.md` | `648134a7…` | SKILL rule block 20: bullet prose, the layout pre-check, `<!-- sqfs-triage-table v3 -->`, the action-vocabulary line, 12 rows |
| `entry.md` | `e0e4001f…6177010` | `corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md`, frontmatter and body in the v2 entry's shape |
| `rationale.md` | `8c3ded38…39fc3fdfe` | clause → row map, grammar deltas, row-by-row table, measurements, fallbacks |
| `block18-19-prose.md` | `371973af…` | the repaired block-18 sentence (L1 + F7) and the one sentence block 19 gains, with every clause it asserts measured |
| `l2-wrapper-measurement.md` | `c982bc07…de3306da8` | the `-be` PATH-wrapper run through REA — closes the carried L2 `[INFERENCE]` |
| `v3-refparse.py` | `851f7d36…ef15063` | reference reader for the v3 grammar (3 deltas), `--selftest` 20/20 |
| `checks.py` | `ece8d1db…d9abd42c54` | the three measurement groups + the exact-only control |
| `a-heldout-26.tsv`, `b-c1-4.tsv`, `c-combined.tsv`, `ctl-exact-*.tsv` | — | result tables; `c-envelope-*.json` are the synthetic inputs |
| `l2-env-baseline.json`, `l2-env-wrapper.json`, `l2-*-sasquatch-v4be.sh` | `3deb947b…`, `449fca4c…`, `5bce229e…`, `9e683c9e…` | the wrapper receipts |

## The table, in one paragraph

Twelve rows, twelve labels, twelve action tokens, one row per clause of the precedence list in
`plans/round-41-claims.md` § R41-C2 (`no-squashfs-chunk`, `dep-missing-be`, `dep-missing-le`,
`partial-body-failure`, `avm-marker-be-dropped`, `body-extractor-failure`, `depth-limited-nested`,
`mixed-symlinks`, `escaping-symlink-removed`, `in-tree-symlink-metadata`, `clean`, `clean-empty`).
Row order is clause order, and each cell carries exactly the constraints its clause names and `*` for
everything the clause leaves open — so the executable table cannot refuse an envelope the precedence
labels. The new content: contains cells (`kind+`) on the four failure rows, the depth row and the
mixed row; `depth-limited-nested` / `raise-depth` for the depth gap; `escaping-symlink-removed`'s gap
cell pinned to `none`; `none-v4` for clause 2; and one layout pre-check hoisted above the table so the
two failure rows stop contradicting their own causes.

## Repairs, defect by defect

| defect | repair in this draft | status |
|---|---|---|
| **M1** stale embedded table copy | the block states the interpreter parses `SKILL.md` and carries no embedded copy; `--print-table` prints the parsed block | repaired in prose |
| **M2** body-failure cause vs a marker-stripped genuine AVM body | cause rewritten: `-be` present is the wrong reading for an AVM-layout body; fault is body bytes or extractor build; layout pre-check decides first | repaired |
| **M3** avm row's action vs its cause's damage branch | the damage branch leaves the row and lives in the pre-check; the pre-check overrides the cell when it fires | repaired |
| **L1** block-18 verb | "mislabels" kept for mixed links and non-firmware; "cannot label" for partial failures and empty trees; the AVM wrapper added | drafted (`block18-19-prose.md` §1) |
| **L2** wrapper delivery unmeasured | **measured this wave**: `sasquatch-v4be` earlier on PATH is the binary unblob runs under REA, and `-be` flips the marker-only carrier from `extractor-failure`/`P=0` to three files sha256-identical to its tree; a publishing decoy proves the PATH resolution | closed by run |
| **L3** dep rows omit REA as gap minter | both dep sources cite S119 `FirmwarePublication.js:161-186` / `:186-201` and `firmwareAnalysis.js:85` | repaired |
| **L4** partial row's oracle half unmeasured | cited as measured: H21 publishes 5 files, 4 match the oracle, the fifth is a 16384-byte truncation of an 19873-byte file (`w2/R40W2C2IndepEval.md` §6) | retired by evidence (not marked `[INFERENCE]` — that would be the wrong direction) |
| **L6** silent empty-target removal | clean row: `SR = no` never proves no link was dropped; the oracle-tree diagnostic is stated, with `[INFERENCE]` on the population | repaired |
| **L7** `none` double duty | disclosed in the entry's Limits; the token is kept because forcing it out invents a second word for "no action" | disclosed |
| **L5 / F6** escaping row absorbs combined sets | gap cell `*` → `none`, plus contains cells above it | repaired |
| **F4** `dependencies` never decides | the block now **screens** eight fields and says seven decide; `dependencies` is required by clause 3, redundant with `handler` on every measured class | repaired in prose + Limits, not removed |
| **F7** block-18 scope word | "routing **and for the action column**", then "itself superseded by block 20"; block 19's supersession sentence also retires its AVM bullet's "only" | drafted |
| **R40-CL4** partial recipe pinned by compressed length | out of this seat's scope (generator); the row stays compression-generic | not touched |
| timeout corner, multi-chunk masking | stated in the block prose and the entry's Limits (`ExtractorTimedOut` records `cmd`, S120 :125-138; a dep gap on one chunk masks a failure on another) | repaired (previously unstated) |

## What the freeze must ratify (my decisions, not the claims')

1. **Three grammar deltas** — v3 marker; `kind+` contains cells in `gap kinds` *and* `dependencies`;
   handler cell `none-v4`. The claims sanction the contains form for gap kinds; I extended it to
   `dependencies` because clause 3 ("D names sasquatch-v4be") is membership, and added `none-v4`
   because clause 2 says "no `squashfs_v4_*` handler", which a v1-v3-chunk image satisfies.
   **Fallback if rejected:** `dependencies` cells revert to exact singletons and row 1 to `none`; the
   entry then must disclose both narrowings (v1-v3 chunk → `unclassified`; a dep gap beside other gaps
   → falls through). `rationale.md` §1 states this.
2. **One new action token** `raise-depth` (the dispatch named it), vocabulary line now 12 tokens.
3. **Cells loosened to `*` where the clause is silent**: `be`/`sr`/`files` on the dep rows, `sr` on the
   symlink and clean rows, `be` on the partial and body rows. Each loosening is what makes the table
   equal the precedence rather than narrower than it; the specific-row-above-general order does the
   rest.
4. **`cause` cells must contain `->`** (the v2 parser's rule) — every one does; this is the round-40
   `R40C2Shortcuts.md` D1 trap.

## Evidence (exact commands, exit codes)

Scratch `S=/fast/scratch/hyaku/kaidoku-r41/R41C2TableDraft`, `TMPDIR=$S`, cwd `$S`; `A` = the
artifacts dir.

```
$ python3 -I -B $A/v3-refparse.py --selftest
cases=20 pass=20 fail=0                                            exit 0
$ { printf '## Queue-drain craft\n\n'; cat $A/block20.md; printf '\n\n## Next section\n'; } > fixture-SKILL.md
$ python3 -I -B $A/v3-refparse.py --skill fixture-SKILL.md --table-only
marker line 45, header line 47, rules 12                            exit 0
$ python3 -I -B $A/checks.py
A held-out 26 : 26/26
B C1 carriers : 4/4 -> V1..L2 depth-limited-nested/raise-depth (row 7)
C combined    : 18/18
TOTAL 48/48
CONTROL exact-only (v2 set grammar): A 26/26  B 0/4  C 7/18        exit 0
```

- **A** compares against `corpus/evidence/round-40/c2/heldout/manifest.json:label_actions` — round-40
  data, not this draft. All v2 classes are empty or singleton gap sets, so 26/26 says the grammar
  extension did not regress them; it is a reproduction, and the entry says so.
- **B** is the first time the four round-40 C1 carriers get a label: `{depth-limited,
  unpublished-entry}` → row 7 for all four, where v2 returned `unclassified`.
- **C** derives each expected pair by hand from the clause number written beside it, so it measures
  table-vs-precedence agreement (a composition self-check), not label truth. That distinction is in the
  entry's Scoring paragraph.
- **Control**: the same block with every `kind+` rewritten to the exact `kind` (v2's set grammar in v3
  shape). It keeps A, loses all of B and 11 of 18 in C — the contains form is load-bearing.

REA runs (dev only, on a carrier this seat built from its own tree — no vendor image, no reserved
carrier, no lane carrier): `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0
extract-firmware --format json --full-output`, exit 0 each time, three runs plus a repeat of the
baseline; details, hashes and the unexplained side-write observation in `l2-wrapper-measurement.md`.

## Open items for the L1

1. **Re-anchor the entry citations.** `block20.md` cites the entry as `:11-24`, `:36-56`, `:57-72`;
   those ranges are the drafted entry's. Any edit that shifts them before the freeze must move the
   citations with them — this is the same drift class as M1.
2. **S-row `used-by` cells.** The entry cites S112, S118, S119, S120 and S122 as sources (S114/S121/S124
   only appear inside block rows and the v2 entry). The registry is append-only and the L1 owns it.
3. **The `recheck:` line** names `tools/round-41/sqfs-triage-v3.py`, which does not exist yet; until it
   does, the line points at `v3-refparse.py` as the fallback reader. If the L1 wants a different
   fallback, that is a one-line edit.
4. **Whether the v3 counter's held-out set includes the v1-v3-chunk envelope** decides whether
   `none-v4` is load-bearing at scoring time or only fidelity insurance. Nothing in the claims requires
   such a class; I did not add one.
5. **Two claims' sentences are now understated by measurement** (informational): the claims say the C2
   surface "repairs R40-CL5"; this draft also closes L2 with a run and retires L4 by citing a
   measurement — the freeze's `## Changes from the draft` may want to say so.

## Limits of this seat

- No round-41 interpreter, counter, held-out generator or scorer was authored: the claim's score at the
  freeze is untouched by this seat, and nothing here substitutes for it.
- No C1 carrier was built, read or run; C1's reserved images and the L3/L4 carriers were not touched.
  The four C1 `after.json` receipts were read as envelopes only.
- The v2 labels' truth is not re-argued (round 40 scored them); only non-regression is measured.
- I did not open the round-40 independent evaluator script; the claims' precedence text is the source
  for the expected labels, and `R40W2C2IndepEval.md` was read as a report only.
- The layout pre-check is prose about carrier bytes; this seat ran no sasquatch layout walk. Its
  correctness rests on the round-40 C1 entry and on S124 for the block-length endianness.
- The unexplained observation in `l2-wrapper-measurement.md` (a wrapper's writes outside the extraction
  directory do not appear) is recorded, not explained, and no claim rests on it.

## Tooling record

Nothing installed, upgraded, removed or moved. Used as installed: `rea-agents 6.5.0` (npx, package root
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`), `unblob 26.6.4`, `sasquatch-v4be`
4.5.1, system `python3`, `git` (read-only `show`/`ls-files`). No pacman transaction, no `xd://mcp__rea_*`
device, no write into `~/.local/bin` or any PATH directory. `/fast` and `/tmp` are separate xfs mounts;
nothing was left in `/tmp`.

Scratch `/fast/scratch/hyaku/kaidoku-r41/R41C2TableDraft` removed at the end; every cited receipt is
copied into the artifacts dir, and no vendor bytes exist anywhere in it.

Report: .ufo/waves/round-41/w1/R41C2TableDraft.md
