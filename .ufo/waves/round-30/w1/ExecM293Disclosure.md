# ExecM293Disclosure — round-30 wave 1: draft of the round-29 M29-3 disclosure

Seat `KaidokuR30.ExecM293Disclosure` (executor, leaf). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
read-only; the only lane write is this report. Sandbox clone base `4ee65c6771058284aa947a266475839d196ed4d4`.
REA: none. Network: none. Installs: none. All timestamps UTC, 2026-10-23. All measurements below were run in
the sandbox clones under `/fast/scratch/hyaku/kaidoku-r30/seats/w1/ExecM293Disclosure/`.

## What is being disclosed (observation)

- `.ufo/waves/round-29/claims.json` (freeze `dbd87cfa09eb89306c4e07d3171a4556eb732024`, base
  `bacbe9cc31d09b5e58e265b0138bd75d0cdb6b47`) names `tools/round-28/c1-heldout-naming.py` inside the R29-C1
  `primary_rule` string: `"openchain_sole_unfiltered_args_consistent (round-25 rule 5; unchanged from
  tools/round-28/c1-heldout-naming.py)"` (line 41 of the file). The v2 gate's `SCRIPT` regex
  (`tools/round-29/freeze-gate.py:63`) matches it, and because the freeze blob records no sha256 for it under
  `instruments` / `loaded_by_counter` / `producers_not_counters` (`:58`, `:107-111`, `:127-128`) the round-29
  freeze is reported `FLAGGED [{"finding": "INSTRUMENT_UNPINNED", "path": "tools/round-28/c1-heldout-naming.py"}]`.
- The file is not loaded or run by the R29-C1 counter (`tools/round-29/c1-fresh-naming.py`); it is named as the
  provenance of the unchanged rule text. It is unchanged across the round:
  `git rev-list dbd87cfa..4ee65c67 -- tools/round-28/c1-heldout-naming.py` → 0 commits (02:45Z), and its sha256 is
  `29c2b571ac97098ac90b6aefc2112306b8b816722fe25abb3d84e03f22eeb27c` at `bacbe9cc`, at `dbd87cfa` and at
  `4ee65c67` (three `git show <rev>:<path> | sha256sum` runs, identical output, 02:45Z).
- The routed remedy names this disclosure: `corpus/lessons/round-29-verifier-spotcheck.md:125` item 3 —
  "Record a supersession or pin note under `instrument_supersessions`".
- **Headline result (observation).** The routed construct is append-only and *inert to the gate*: after the draft
  the round-29 verdict and finding are byte-identical (`FLAGGED`, `INSTRUMENT_UNPINNED`), `--require-clean round-29`
  still exits 1, and `--disclosures` stays exact for the round-29 row. The gate reads pins from the **freeze blob**
  (`frozen`, `:102`, `:107-111`) and consumes `instrument_supersessions` from the current file **only** for
  `INSTRUMENT_REVISED` (`:112-114`, `:132-136`). There is no post-freeze pin-note that clears this finding; the
  only construct that does is a pin present in the freeze blob (probe C below), which is a re-freeze / history
  rewrite, not an append.

## 1. The draft (exact)

Two commits in `clone/` on top of `4ee65c67` (sandbox commits, `git -c user.name=ctl -c user.email=ctl@sandbox`):

```
85ced0a8 round-30 w1 draft: M29-3 pin note appended to round-29 claims.json instrument_supersessions
c29c299a round-30 w1 draft: M29-3 pin-note sentence on the v2 ledger round-29 row
```

### 1a. `.ufo/waves/round-29/claims.json` — appended lines

Line diff `4ee65c67..c29c299a` (numstat): `3  0  .ufo/waves/round-29/claims.json` (3 insertions, 0 deletions).
Exact added text (three lines, after the existing `not_claimed` array):

```
  ],
  "instrument_supersessions": [
    {"path": "tools/round-28/c1-heldout-naming.py", "commit": "dbd87cfa09eb89306c4e07d3171a4556eb732024", "sha256": "29c2b571ac97098ac90b6aefc2112306b8b816722fe25abb3d84e03f22eeb27c", "reason": "M29-3 pin note (not a revision disclosure; the named commit is the round-29 freeze that omitted the pin): the R29-C1 primary_rule names this file only as the provenance of the unchanged rule text; tools/round-29/c1-fresh-naming.py never loads or runs it; no commit in dbd87cfa..measured touches it (rev-list empty), so the sha256 above holds at bacbe9cc, at that freeze and at the measured rev. Routed remedy of corpus/lessons/round-29-verifier-spotcheck.md item 3, appended in round 30 after the round-29 filing; this entry does not clear the gate's INSTRUMENT_UNPINNED finding on round-29 (the gate reads pins from the frozen blob), which stays disclosed in corpus/claim-freezes-v2.tsv."}
  ]
```

Resulting blob sha256 `eec205d3b388b557e63a6253f95c80e94a6e121c57b3b0012d2a9123c7461ee4` (was
`76bc0d8f556019763157bbb74cd43b9983b9e7cf77ad9d92cae898365a60cf79`). The **freeze blob is untouched**:
`git show dbd87cfa:.ufo/waves/round-29/claims.json | sha256sum` → `76bc0d8f…cf79` before and after the draft.

Field notes: `path` and `sha256` as routed. `commit` names the round-29 freeze `dbd87cfa` (the pin-less freeze),
not a revision; probe F shows the gate output is identical if that field instead names `bacbe9cc` (the parent's
"sha256 at bacbe9cc" reading) — the field only feeds the `(path, commit)` disclosure set, which is unused for a
path with no revisions. `sha256` is the digest at `bacbe9cc` = at `dbd87cfa` = at `4ee65c67`.

### 1b. `corpus/claim-freezes-v2.tsv` — round-29 row

Line diff `4ee65c67..c29c299a` (numstat): `1  1  corpus/claim-freezes-v2.tsv`. The first three tab-separated
cells (`round-29`, `FLAGGED`, `INSTRUMENT_UNPINNED`) are byte-identical; only the pointer cell changes. Pointer cell
before → after (exact):

```
… (named as the source of the unchanged rule text, not run by the counter; M29-3)
… (named as the source of the unchanged rule text, not run by the counter; M29-3); a pin note for that path is appended to .ufo/waves/round-29/claims.json instrument_supersessions (sha256 29c2b571... at bacbe9cc, unchanged since the freeze; appended in round 30), and it leaves this verdict and code set unchanged, the gate reading pins from the frozen blob)
```

Resulting ledger blob sha256 `59840c7c3f12bb4007ebf1170129a959b112260600dd70c6ac734ae99df64d9a` (was `c08e84e281f56b7f…`).
The row's verdict/findings must stay `FLAGGED` / `INSTRUMENT_UNPINNED` — probe D below.

## 2. Gate runs, before and after

Command shape (run from the clone root, `--root .`):

```
python3 -I -B tools/round-29/freeze-gate.py --root . --rev <REV> [--require-clean round-29] [--disclosures corpus/claim-freezes-v2.tsv]
```

| mode | before, rev `4ee65c67…` (02:45:20Z) | after, rev `c29c299a…` (02:46:29Z) |
|---|---|---|
| no flags | exit **0** | exit **0** |
| `--disclosures corpus/claim-freezes-v2.tsv` | exit **1** | exit **1** |
| `--require-clean round-29` | exit **1** | exit **1** |
| `--require-clean round-29 --disclosures …` | exit **1** | exit **1** |

Every output is identical between the two states except the `"rev"` value — verified by JSON-dict equality after
popping `rev`, for all four modes (`True` each; 02:48:51Z). Exact after-run fields (before-run values are the same
with `"rev": "4ee65c6771058284aa947a266475839d196ed4d4"`):

```
{"audited": 20, "claim": "R29-freeze-gate", "clean": 3, "disclosures": {"exact": 19, "mismatched": [], "missing": ["round-30"], "of": 20, "path": "corpus/claim-freezes-v2.tsv", "present": true, "stray": []}, "flagged": ["round-14", "round-14/claims-review.json", "round-15", "round-15/claims-review.json", "round-16", "round-17", "round-18", "round-19", "round-20", "round-21", "round-22", "round-23", "round-25", "round-26", "round-27", "round-28", "round-29"], "required_clean": ["round-29"], "required_failed": ["round-29"], "rev": "c29c299ae9a22666b738cf6666824414f2a00fbd", "summary": {"INSTRUMENT_ABSENT": 12, "INSTRUMENT_NONE": 5, "INSTRUMENT_PIN_MISMATCH": 0, "INSTRUMENT_REVISED": 15, "INSTRUMENT_UNPINNED": 6, "INSTRUMENT_UNRESOLVED": 9}}
```

(The line above is the `--require-clean` run; the plain `--disclosures` run is the same without
`"required_clean"`/`"required_failed"`. The `--disclosures` exit 1 is the pre-existing **missing `round-30` row**,
not a round-29 mismatch: `"mismatched": []`. See §6.)

Round-29 freeze entry, identical before and after (observation):

```
{"claims_file": ".ufo/waves/round-29/claims.json", "findings": [{"finding": "INSTRUMENT_UNPINNED", "path": "tools/round-28/c1-heldout-naming.py"}], "freeze": "dbd87cfa09eb89306c4e07d3171a4556eb732024", "instruments": ["tools/round-28/c1-heldout-naming.py", "tools/round-29/c1-fresh-naming.py", "tools/round-29/c2-filtered-unseen.py", "tools/round-29/collect-c1.py", "tools/round-29/collect-c2.py", "tools/round-29/make-carriers.py"], "verdict": "FLAGGED"}
```

The claims-only intermediate state (`85ced0a8`, ledger still old) was measured too: `--disclosures` exit 1,
`{"exact": 19, "mismatched": [], "missing": ["round-30"], …}` — i.e. **no ledger change was required** for the
row to agree with the gate; the ledger sentence in §1b is editorial (it records the disclosure where the row is
read), and `--disclosures` is unaffected by it (the gate compares verdict + code set only, `freeze-gate.py:177-188`).

The round-24 (v1) gate at `c29c299a` with `--disclosures corpus/claim-freezes.tsv` exits 1 with
`{"exact": 16, "mismatched": [], "missing": ["round-30"], "of": 17, …}` and reports round-29 findings
`INSTRUMENT_UNPINNED` × 4 paths (`make-carriers.py`, `collect-c1.py`, `collect-c2.py`, `c1-heldout-naming.py`) —
its row's code set is unchanged, so the appended entry is inert there too (02:47:01Z).

## 3. Why the finding stays — mechanism and probes (all observation)

`tools/round-29/freeze-gate.py`:

- `:101-103` — `freeze` = first-add commit of the claims file; `frozen` = blob at that commit; `current` = blob at `--rev`.
- `:107-111` — `pins` are built **from `frozen`** over `PIN_KEYS` (`:58`).
- `:112-114` — `disclosed` is built from `current.instrument_supersessions`, keyed `(path, commit)`; it is
  consumed only at `:132-136` (`undisclosed = [r for r in revs if (path, r) not in disclosed]`).
- `:127-128` — `INSTRUMENT_UNPINNED` fires on `path not in pins` with **no disclosure hook**.
- The v1 gate (`.ufo/waves/round-24/tools/freeze-gate.py`) is the same shape: pins at `:87` from `frozen`
  (`:82`), disclosure set at `:89-91` used only for revisions.

Four probes, each in its own throwaway clone (all in the seat scratch):

| probe | what was changed | command / rev | observed |
|---|---|---|---|
| **B** | pin appended to `producers_not_counters` in the **current** round-29 claims.json (after the freeze) | `clone-c`, rev `f58765ed…`, 02:47:46Z | exit 0, round-29 still `[{"finding": "INSTRUMENT_UNPINNED", "path": "tools/round-28/c1-heldout-naming.py"}]`, `FLAGGED` — a post-freeze pin does not pin |
| **C** | a copy `.ufo/waves/round-29/claims-fixed.json` whose **freeze blob** carries the pin | `clone-b`, rev `3c3e6b0b…`, `--require-clean round-29/claims-fixed.json`, 02:47:33Z | exit **0**; entry `{"claims_file": ".ufo/waves/round-29/claims-fixed.json", "findings": [], "freeze": "3c3e6b0b…", "verdict": "CLEAN"}`; the original round-29 claims.json in the same run stays `FLAGGED` — a pin in the freeze blob is the only construct that clears it |
| **D** | round-29 row flipped to `CLEAN` / `-` while the gate still flags it | `clone-c`, rev `e63ff7d1…`, `--disclosures`, 02:47:57Z | exit **1**, `{"exact": 18, "mismatched": ["round-29"], "missing": ["round-30"], …}` — the row must keep `FLAGGED`/`INSTRUMENT_UNPINNED` |
| **E** | a later revision of the named path (comment appended) after the pin note | `clone-d`, rev `31122d70…`, 02:48:36Z | round-29 findings become `[UNPINNED, {"finding": "INSTRUMENT_REVISED", "path": "tools/round-28/c1-heldout-naming.py", "commits": ["31122d70…"], "disclosed": 0}]` — the entry cannot launder a future revision |
| **F** | pin-note `commit` field set to `bacbe9cc…` instead of `dbd87cfa…` | `clone-e`, rev `4be91d8b…`, 02:49:32Z | exit 0; output identical to the draft state ignoring `rev` — the field value cannot matter here (no revisions) |

## 4. Is the change append-only?

- **claims.json: yes, line-level pure insertion** — `git diff --numstat 4ee65c67..c29c299a` gives `3  0`; no
  existing line is removed or edited, and no byte before the insertion point changes. It is not an EOF append
  (JSON has no place for one): the new key is inserted before the closing `}` and the pre-existing `  ]` line is
  reused as the new array's closing bracket. Round 24's precedent was `+4 -1` (round-26 `CapinfosFacts.md:38`);
  this draft is strictly additive.
- **ledger: no** — the round-29 row is replaced in place (`1  1`); its first three cells are byte-identical, only
  the pointer cell gains one sentence. A TSV row keyed by round cannot take a prose note append-only (a new row
  would be `stray`). The ledger edit is optional (§2).
- The freeze blob (`dbd87cfa:…claims.json`, `76bc0d8f…`) is untouched by construction: `dbd87cfa` is an ancestor
  commit and nothing in the draft rewrites history.

## 5. What this means for M29-3 (inference, from the measurements above)

- The draft is the routed disclosure and nothing more: it records the name, its identity (`29c2b571…`) and the
  reason in the claims file and the v2 ledger, while leaving the gate verdict, the code set and
  `--require-clean round-29` exactly as they were. It must not be presented as turning round-29 green.
- Clearing the flag is only possible by putting the pin into the freeze blob (probe C) — i.e. rewriting `dbd87cfa`
  or re-freezing under a new claims path. Both change the freeze identity / history; neither is append-only, and
  the round-25 claims file states the project's stance against using `instrument_supersessions` to "launder" a
  post-freeze unpinned debt (`.ufo/waves/round-25/claims.json:169`). This seat did not do either.
- The exit-code remedy for the class is the round-30 `prefreeze-gate.py` (sibling seat `ExecPrefreezeGate`), which
  is not this item.

## 6. Observations beyond this item (not integrated, reported as measured)

- At the lane tip both gates' `--disclosures` runs exit 1 for one reason: **`missing: ["round-30"]`** — the
  round-30 freeze `4ee65c67` has no row yet in `corpus/claim-freezes.tsv` (v1: `exact 16 of 17`) or
  `corpus/claim-freezes-v2.tsv` (v2: `exact 19 of 20`). `round-30` itself audits CLEAN
  (`{"claims_file": ".ufo/waves/round-30/claims.json", "findings": [], "freeze": "4ee65c6771058284aa947a266475839d196ed4d4", "instruments": ["tools/round-30/c1-rust-positive.py", "tools/round-30/c2-rust-refusals.py"], "verdict": "CLEAN"}`).
  `tools/round-29/prefile-check.sh` runs both gates with `--disclosures` and would fail at filing until round-30
  rows land (observation; not this seat's item).
- The v1 ledger row for round-29 (`corpus/claim-freezes.tsv:17`) needs no change to stay exact; if the L1 wants
  the same note there, the mirror sentence would be appended to its pointer cell after "… not run by the counter
  and not pinned; M29-3)". Not applied here (the item named the v2 ledger).

## 7. Artifacts (sha256, all under `/fast/scratch/hyaku/kaidoku-r30/seats/w1/ExecM293Disclosure/`)

```
draft-claims.diff        1156f12e7b4202c49d05494e18d212c4c407d00aeea75cc5a7d29d994d69e0c4   git diff 4ee65c67..85ced0a8 -- .ufo/waves/round-29/claims.json
draft-ledger.diff        e4f88fef40339bd398e57f5f9e2d8d1278126e6d0cb2ce1c66b3303532a655e3   git diff 85ced0a8..c29c299a -- corpus/claim-freezes-v2.tsv
draft-combined.diff      278ff70966449fd6f492812b15a4cf20259ceebef082de6a3cb798f3b4f060a1   git diff 4ee65c67..c29c299a (both files)
before-nodisc.json       2c565c88b83167a211902a3ee4bedba918407f7a1ad741bf8375853563d80eb4   gate at 4ee65c67, no flags
before-disc.json         844525ac0cf7c32dc676d72059c288ca94cd67b7c8090b0cb884da5d4db2a90f   gate at 4ee65c67, --disclosures
before-reqclean.json     f1668b57bfe1266271ff5ee2b0b34f52603af556783045169233785267640ee2   gate at 4ee65c67, --require-clean round-29
before-reqclean-disc.json fb9d5872c3c0fdee284ee948f7b707d169b4ad6c535be9dbc59fe953ce1887fa  gate at 4ee65c67, both
s1-disc.json             bf356d6051dec576a89a20d6fa0bf044650fa187c9bf77022ba32e70ccb497ae   gate at 85ced0a8 (claims only), --disclosures
s1-reqclean-disc.json    30157551f4aa514e993c08039332bf6b1560341e2c423231fcf293f9f0a4a7b7   gate at 85ced0a8, both
s2-nodisc.json           8194e69275bbd0824c9f9d33378aa249c398aea921c4ed981e98a1ccf8c7b8bc   gate at c29c299a, no flags
s2-disc.json             d5aa9d9cee1b833795e892a54199ff7b35ce428318b0e92408d5808a01749e94   gate at c29c299a, --disclosures
s2-reqclean.json         83efde5424e19e3f29ab867e43819084dbed12468e227d8f64ec430a1a7a9e9d   gate at c29c299a, --require-clean round-29
s2-reqclean-disc.json    0902f877ae645f55a93b737e4c4a2bf38050828040841ed4f93e124391ca037c   gate at c29c299a, both
s2-v1-disc.json          11ec5b928542907ae7d8011eb814b5857621121edee9c9bbab8283449ec5699b   round-24 gate at c29c299a, --disclosures corpus/claim-freezes.tsv
probe-b.json             012d6503a787ddc6e8bf7df8782b462b17c6237e9b5aaff0a6b9727d263d385e
probe-c.json             34d10bee5fdb616fb238d8b26cabf8f3396344ad446c922d5d073e40bd9613ca
probe-d.json             d5d8be33643b0d4cc6c7596928a18987702cc70e7c479a1ae7355f4340b427fb
probe-e.json             5a39bd3a1b3a8dcd07ed61c4bee385914dc4f721259ce75071bad9715647c494
probe-f.json             e2c9090664a435ee8b7ad13d05a0b31c092c011300762513876db21491e9fb31
probe-c.py               6952bb9cfe1b993fb861db7fe4c1168c1a4e272099ddfe480b8204bb29138f7e
```

Clones kept for inspection: `clone/` (draft, HEAD `c29c299a`), `clone-b/` (probe C, `3c3e6b0b`),
`clone-c/` (probes B+D, `e63ff7d1`), `clone-d/` (probe E, `31122d70`), `clone-e/` (probe F, `4be91d8b`).
Draft blobs: claims.json `eec205d3…` (§1a), ledger `59840c7c…` (§1b).

## 8. Limits

- Everything above is observed on this host's clones of the lane tip `4ee65c67`; no lane file was modified by
  this seat beyond this report, and the lane was read with read-only git only.
- `[INFERENCE]` labels: §3's line-number mechanism reading is code reading (line numbers observed via `grep -n`);
  §5 is inference from the measurements. Everything else is observation.
- Not run: REA, any network fetch, any counter other than the two freeze gates, `--selftest` (the v2 gate has
  none). No installs.
- The probes are single-commit synthetic states in throwaway clones; they do not claim anything about lane
  history beyond the revs cited.
