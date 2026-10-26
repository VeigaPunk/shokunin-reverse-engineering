# R41C1Extra — `c1-extra.py` ported to round 41

**Verdict: DONE** — the round-40 supplementary C1 gate is ported to the round-41 entry identity with
a fourth frontier-note requirement (the round-40 `measured, not promoted` record must be named as
superseded); its selftest is 17 cases, 17 pass (round 40: 7), 10 of 10 single-logic mutants are killed
each by a *distinct* case, the gate is satisfiable end-to-end on a dev sandbox landing in a throwaway
clone (exit 0, all three bindings true) and, on the real lane at the base, exits 2 with
`absent at freeze: .ufo/waves/round-41/c1/carriers.json, tools/round-41/sqfs-list.py`.

Seat: executor (leaf), round 41 wave 1 (pre-freeze), lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `49096c7e6f226af0c750c4b003be58883cb6049f`.
Wrote only `.ufo/waves/round-41/w1/R41C1Extra.md` and
`.ufo/waves/round-41/w1/artifacts/R41C1Extra/`. No lane file outside my artifacts dir, no VCS
mutation in the lane or fleet (read-only `git show`/`rev-parse` only; every fixture commit is
`git -C <clone> -c user.name=fx …` inside `/fast/scratch/hyaku/kaidoku-r41/R41C1Extra/`, with the
clone's `--show-toplevel` asserted first). No REA, unblob, sasquatch or sasquatch-v4be run at all —
this gate is a reader-plus-document gate and touches no reserved carrier. No tool installed or
upgraded. Scratch `S=/fast/scratch/hyaku/kaidoku-r41/R41C1Extra` removed before yield; every artifact
below is inside the seat artifacts dir.

## 1. Deliverables

| artifact | sha256 | what it is |
|---|---|---|
| `artifacts/R41C1Extra/c1-extra.py` | `531724e1c7215ed602a06648525cc375b4c9d86370f8e37ea59657a087ceacae` | the port (262→389 lines, stdlib only) |
| `artifacts/R41C1Extra/c1-extra-r40-to-r41.diff` | `db035d783277aad8f4791de887d33161f258a2bcf4f481deffe75aa131a269a7` | `diff -u a/tools/round-40/c1-extra.py b/tools/round-41/c1-extra.py`, 9 hunks, 257 +/- lines |
| `artifacts/R41C1Extra/c1-extra-selftest.txt` | `b2ed17d23c048c399b40e07a3f730811f32e1df506bfd0f452be1d4b2b4b3399` | `SELFTEST cases=17 pass=17 fail=0`, exit 0 |
| `artifacts/R41C1Extra/red-cases-detail.json` | `48db449b71d8034a03a22dd6ef02a0cf394e43e7f8069642ba27089a4f7cc46f` | per-red-case binding detail (which sub-check fires) |
| `artifacts/R41C1Extra/probe-red-cases.py` | `722cffc137afc1df329ed5cc79a375c8392ffca53caca4728b1a1d80eeef2594` | the driver that produced the above |
| `artifacts/R41C1Extra/mutants.txt` | `ef59c47dd5111bde179a651ee13ca175d54a657dad58c42bd915d1963bdf0b6b` | 10 mutant runs on the port, each with its killing case, plus the same three clauses mutated in the round-40 file |
| `artifacts/R41C1Extra/base-probe.json` | `936cab88afcac5f3790ccf0d6bf05e32de71a2d59926020f0b158f70382117ab` | the gate on the real lane at the base, exit 2 |
| `artifacts/R41C1Extra/base-bindings.json` | `c27b66a8243ef1f150bee8f0c11a7e0dcc4df46efb2c6c1462bc30c4f0d34c9d` | the three bindings probed directly at the base (same reader/entry constants) |
| `artifacts/R41C1Extra/sandbox-demo.sh` | `0dbec431f666dff116cb04e2cb322e0d48fee8aa5b9229ddcafa382e37653ab3` | dev satisfiability driver (throwaway clone) |
| `artifacts/R41C1Extra/sandbox-demo.out` | `d4def9329e5f7750d3eb30eb455f7a34c2254e2b78bcc16da4fb38b115587c54` | its stdout (base/freeze/rev + gate JSON) |
| `artifacts/R41C1Extra/gate-demo.json` | `dd43bfcbfe4cea42a593a9af6010ff23158e5bad290033d63627b5b4cc26b936` | gate result on the dev landing: `met true`, exit 0 |
| `artifacts/R41C1Extra/SHA256SUMS` | — | all of the above |

Diff hunk map (review order): `@@ -1,25` docstring/usage; `-31,11` constants; `-52,8` scratch +
`--work`; `-65,7` absent-at-freeze message; `-106,36` `sourced_new` detail + `note_verdict` /
`frontier_content`; `-145,13` `measure`/`tool_dir`; `-180,26` selftest signature + fixture; `-208,21`
selftest cases; `-237,17` argparse/selftest dispatch.

## 2. What the port changes, and the one check it adds

Constants (the round-41 identity; `--base` stays a CLI argument):

```
CARRIERS = '.ufo/waves/round-41/c1/carriers.json'
READER   = 'tools/round-41/sqfs-list.py'
ENTRY    = 'corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md'
STEM     = '2026-10-26-r41-avm-be-squashfs-core'
HEADING  = '## Round-41 additions to Core'
NOTE     = 'Round-41 frontier note'
R40_RECORD = re.compile(r'measured[,\s-]+not[,\s-]+promoted')
```

The three round-40 bindings are kept with their semantics:

- `oracle_rederived` — carriers spec read **at the freeze**, reader bytes read **at the freeze**,
  carrier bytes at the rev (lane-built `path`) or from `--carrier-cache` (vendor), sha256 checked
  against the carrier pin before the reader runs, reader invoked `--layout avm`, and `oracle.tsv` /
  `nonregular.tsv` compared as **row sets** at the rev. Any absent piece is `Unevaluable` (exit 2),
  never a pass; a missing reader now names the path in the message.
- `sourced_new` — cited ids come only from `source:`-prefixed lines of the entry, and an id counts
  only when its `corpus/SOURCES.md` row is **absent at `--base`**, present at `--rev`, and its used-by
  cell names the entry or the stem. Detail now also names the cited ids that already exist at the base.
- `frontier_content` — PROVINCE.md at the rev must hold a line starting `Round-41 frontier note`.

The added check (the round-41 requirement) is inside `frontier_content`: the qualifying line must
satisfy **all four** of `names_heading` (literal `## Round-41 additions to Core`), `names_stem`,
`supersedes` (the substring `supersede`), and `names_r40_record` (the round-40 record phrase
`measured, not promoted`, matched after stripping markdown `*` and accepting comma, space or hyphen
separators). The detail object is now `{line, names_heading, names_stem, supersedes,
names_r40_record, ok}` instead of the round-40 bare line, so a future failure says which clause died.
Rationale: the draft's clause is "a `Round-41 frontier note` … says what it supersedes". At the base,
PROVINCE.md already holds a `Round-40 frontier note` carrying the record phrase (`PROVINCE.md:394`,
`base-bindings.json` → `names_r40_record: true`) and, a few lines above, the round-39 note's
"are superseded" wording; a gate that only asks "a note-shaped line names the heading and says
supersede" is therefore satisfiable by a note that supersedes the wrong surface — the round-40 D4
failure mode (`presence is not supersession`) one level down. Requiring the record phrase inside the
`Round-41` note line makes the superseded object explicit, and the base round-40 note itself scores
`{supersedes: false, ok: false}` while still naming the record: neither half alone is enough.

Two mechanical additions, both non-semantic: `--work DIR` and `--tools DIR`. `--work` roots the
scratch (`$HYAKU_SCRATCH/kaidoku-r41` otherwise, `tempfile` default last — no `/tmp` hardcoded).
`--tools` is **selftest-only**: it names the directory holding `gen-squashfs.py` and `sqfs-list.py`
(resolution order `--tools`, the script's own directory, `<root>/tools/round-41`,
`<root>/tools/round-40`), so the port can be selftested before `tools/round-41/` exists. It cannot
weaken a measurement: the measurement reader is read from the freeze commit, not from disk.

Exit codes are unchanged: 0 all three true, 1 any false (JSON `met: false`), 2 unevaluable.

## 3. Selftest: 17 cases, 17 pass

```
$ S=/fast/scratch/hyaku/kaidoku-r41/R41C1Extra; export TMPDIR=$S
$ python3 -I -B <artifacts>/c1-extra.py --selftest \
    --tools <lane>/tools/round-40 --work "$S/work"
PASS	green
PASS	base-has-nothing
PASS	trimmed-oracle
PASS	edited-oracle-same-count
PASS	extra-nonregular-row
PASS	marker-only-body-refused
PASS	external-carrier-pin-mismatch
PASS	external-carrier-missing-cache
PASS	old-sid-with-used-by
PASS	base-sid-s126-with-used-by
PASS	new-sid-no-used-by
PASS	presence-only-frontier-note
PASS	round-40-note-names-r41-heading
PASS	note-miscases-heading
PASS	r41-note-omits-r40-record
PASS	green-after-restore
PASS	bad-rev-unevaluable
SELFTEST cases=17 pass=17 fail=0        (exit 0; wall 1.2 s)
```

Round-40's seven cases are kept (`green`, `base-has-nothing`, `trimmed-oracle`,
`old-sid-with-used-by`, `new-sid-no-used-by`, `presence-only-frontier-note`,
`bad-rev-unevaluable`), with the fixture base changed to mirror the real base (its `corpus/SOURCES.md`
holds `S126` as the highest row, so the "old id" case is now the base's own top id territory rather
than the trivial `S001`). Ten cases are new:

| case | intent |
|---|---|
| `base-sid-s126-with-used-by` | **required red case**: entry cites `S126` (highest id at the base), the rev row even lists the entry in its used-by cell — still not new |
| `round-40-note-names-r41-heading` | **required red case**: a `Round-40 frontier note` that names the round-41 heading, stem, supersede verb and the record is not a round-41 note |
| `r41-note-omits-r40-record` | the added check: heading + stem + supersede, but the round-40 record is never named |
| `note-miscases-heading` | a miscased heading (`## round-41 additions to core`) is not the heading |
| `edited-oracle-same-count` | oracle row count kept, one sha256 digit changed — kills a count-only compare |
| `extra-nonregular-row` | a fabricated symlink row in `nonregular.tsv` — kills a files-only compare |
| `marker-only-body-refused` | carrier built `--endian avm` (marker-only, BE block lengths) with oracles read under `--layout auto`: the gate must refuse it (`reader exit 2`), so the `--layout avm` choice is load-bearing |
| `external-carrier-pin-mismatch` | cache holds a *different, well-formed* image under the pinned name with that image's own oracle — the pin check refuses it |
| `external-carrier-missing-cache` | external carrier with an empty cache — fails closed, not silently |
| `green-after-restore` | the green state is reachable again after the red mutations (no order-dependent state leakage) |

`red-cases-detail.json` shows each new red case failing for the intended reason, not incidentally:

```
base_sid_s126            sourced_new false   {cited:[S126], at_base:[S126], new_with_used_by:[]}
round_40_note_only       frontier false      {error: "no line starting 'Round-41 frontier note'"}
note-omits-r40-record    frontier false      {names_heading:true, names_stem:true, supersedes:true,
                                              names_r40_record:false}
presence_only            frontier false      {names_heading:true, names_stem:true,
                                              names_r40_record:true, supersedes:false}
green                    frontier true       {all four true}
measure_green            met true            {oracle_rederived:{L3:ok}, sourced_new:{S127}, frontier true}
```

## 4. Calibration: 10 single-logic mutants, 10 killed, each by a distinct case

`mutants.txt`, one mutant per run, applied to a scratch copy only:

| mutant (single clause) | selftest | killed by |
|---|---|---|
| M1 drop `names_r40_record` from the required set | 16/17 | `r41-note-omits-r40-record` |
| M2 `NOTE = ''` (round-41 prefix disabled) | 16/17 | `round-40-note-names-r41-heading` |
| M3 `sourced_new` base-absence unchecked (`s in at_rev`) | 16/17 | `old-sid-with-used-by` |
| M4 oracle files compare by row **count** only | 16/17 | `edited-oracle-same-count` |
| M5 heading compare case-blind | 16/17 | `note-miscases-heading` |
| M6 reader `--layout auto` instead of `avm` | 16/17 | `marker-only-body-refused` |
| M7 carrier pin unchecked (`raw is None` only) | 16/17 | `external-carrier-pin-mismatch` |
| M8 `met = o or s or f` | 16/17 | `base-has-nothing` |
| M9 nonregular compare disabled (`ok_n = True`) | 16/17 | `extra-nonregular-row` |
| M10 used-by cell unchecked | 16/17 | `new-sid-no-used-by` |

Finding for the freeze: three load-bearing clauses are **not exercised by the round-40 selftest**.
Measured on the round-40 file itself (`tools/round-40/c1-extra.py` at `49096c7e`, its own 7-case
selftest, with `gen-squashfs.py`/`sqfs-list.py` copied beside it in scratch): the row-count-only oracle
compare (M4), the reader forced to `--layout auto` (M6) and the unchecked carrier pin (M7) each return
`cases=7 pass=7 fail=0` — none is caught. On this port, before the cases in §3 were added, M4 was still
green at `cases=11 pass=11` and M6/M7 at `cases=14 pass=14`. The added `edited-oracle-same-count`,
`marker-only-body-refused` and `external-carrier-pin-mismatch` cases are what kill them. So round-40's
"cases=7 pass=7" was not evidence for three clauses its code reads — the row-set compare beyond count,
the `--layout avm` choice, and the pin check on externally loaded bytes — and a mutation suite run
against this gate should expect exactly those three mutants to die here.

## 5. Evidence on real data, and satisfiability

**(a) The real lane at the base — unmoved, exit 2.** `base-probe.json`:

```
$ python3 -I -B <artifacts>/c1-extra.py --root <lane> \
    --rev 49096c7e --freeze 49096c7e --base 49096c7e --work "$S/work" --json-out base-probe.json
{"unevaluable": "absent at freeze: .ufo/waves/round-41/c1/carriers.json,
                 tools/round-41/sqfs-list.py", "exit_code": 2}
```

Direct binding probes at the base (`base-bindings.json`, same constants as the CLI):
`frontier_content` → `{error: "no line starting 'Round-41 frontier note'"}`;
`sourced_new` → `{error: 'entry absent'}`; and the base's own round-40 note, scored by the same
`note_verdict`, is `{names_heading:false, names_stem:false, supersedes:false, names_r40_record:true,
ok:false}` — it names the record but neither the round-41 heading, the stem, nor a supersede relation,
so it cannot be mistaken for the round-41 note even if the prefix check were removed.
Base SOURCES maximum id, for the `S126` case: `git show 49096c7e:corpus/SOURCES.md | grep -oE 'S[0-9]{3,}' |
sort -u | tail -1` → `S126`.

**(b) Satisfiability on a dev sandbox landing — exit 0.** `/fast/scratch/.../fx.Ybqw/lane` (a
`git clone --shared` of the lane at the base, `--show-toplevel` asserted), fixture commits
`base=49096c7e`, `freeze=d3886971`, `rev=6d076ff4`; `tools/round-41/sqfs-list.py` = the round-40
reader, one dev carrier `L1dev` = the round-40 lane-built L1 (a development input; its bytes and the
committed round-40 oracle are read straight from the repo), plus a sandbox entry citing a new `S127`
row and a `Round-41 frontier note` in PROVINCE:

```
{"bindings": {"frontier_content": true, "oracle_rederived": true, "sourced_new": true},
 "detail": {"oracle_rederived": {"L1dev": "ok"}, "sourced_new": {"new_with_used_by": ["S127"]}, …},
 "met": true, "exit_code": 0}
```

So the gate's three bindings are jointly satisfiable on the real repository's file shapes (SOURCES
row grammar, PROVINCE note line, entry naming, `tools/round-41/` reader path) — this is a
satisfiability demo, **not** a score: the carrier is a round-40 development input, none of V3/V4/L3/L4
was built, and nothing in the lane was written.

## 6. Risks and open decisions for the L1 (freeze)

1. **Reader path is fixed to `tools/round-41/sqfs-list.py`.** If the round-41 reader is frozen at a
   different path, the gate is `Unevaluable` (exit 2) — loud, not silently green — but the claim's
   "supplementary gate met" clause then cannot be scored. Whoever freezes the reader should either use
   this path or change this constant in the same commit (and re-run the selftest; `--tools` is
   selftest-only, so the change is one line plus one selftest run).
2. **`sourced_new` reads only `source:`-prefixed lines** (inherited from round 40). A round-41 entry
   that cites ids in a different line shape fails the binding (fails closed). The r40 entry used
   `source: S124 — …` per line; keep that shape.
3. **`frontier_content` requires four things on one line**: the literal heading, the stem, a
   `supersede` stem and the record phrase. The phrase match strips markdown `*` and accepts
   `measured, not promoted` / `measured-not-promoted`; a note that paraphrases without any of those
   three separators fails. Deliberate: the record's label is the round-40 PROVINCE wording
   (`PROVINCE.md:386`, `:394`).
4. **No pre-freeze score is possible**: at the base the gate exits 2 because neither the carriers spec
   nor the reader exists. The claim's "supplementary gate met" can only be measured after the freeze;
   the pre-freeze obligation satisfied here is the tool and its selftest.
5. **Scratch**: a caller that omits both `--work` and `HYAKU_SCRATCH` gets `tempfile`'s default. Pass
   `--work "$S"` from a `/kaidoku-r41/` scratch segment so the `output_directory`-style provenance
   rule the round-40 harness enforces is never an issue for re-runs.
6. **Not in scope, not done**: no change to `tools/round-40/c1-extra.py`, no counter/carriers/oracle
   work, no REA or unblob run, no claim text. `[INFERENCE]` The round-41 reader (a separate seat) is
   assumed to keep the round-40 CLI (`--layout {auto,le,be,avm} --files --nonregular`), since the
   gate invokes exactly that; the sandbox demo proves the round-40 CLI satisfies the gate on a genuine
   AVM-layout body.
