# R38W2C1RescoreV1 — R38-C1 author verdict re-scored with the first-freeze counter

**Verdict: CONFIRMED.** The author verdict for R38-C1 (honest stop, `carriers_matched 3`,
`met_target false`, K2 fails on one `unpublished-entry` gap) reproduces **exactly** at both judged
revisions with the first-freeze counter bytes, and
`.ufo/waves/round-38/l1/scores/c1-v1-at-3b960fe5.json` is reproduced **field-for-field** (canonical
hash equal, only `argv` differs). Three instrument defects and one landed pair-inconsistency are
recorded below; **none changes the verdict** — all of them push the score down or leave it
unchanged, never up.

Seat: advisory leaf. No VCS mutation, no writes outside this report and
`.ufo/waves/round-38/w2/artifacts/R38W2C1RescoreV1/`, no REA MCP device, no subagents, no installs.
Scratch `S=/fast/scratch/hyaku/kaidoku-r38/R38W2C1RescoreV1` (removed at exit); every cited value is
copied into the artifacts directory.

## 1. Instruments (identity checked before use)

| instrument | source | sha256 | lines | git blob |
|---|---|---|---|---|
| counter v1 (the rule) | `git show e059ca93:tools/round-38/c1-counter.py` | `a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8` | 395 | `8e33ac68` |
| counter v3 (informational) | `git show f1010f67:tools/round-38/c1-counter.py` | `d9aa8b622086d3efab4cf59f189bc8f51b2eb07f2fe73e08ab4a0774065d0347` | 427 | `115085f0` |

`a7a62b09…` matches the assignment pin exactly (`artifacts/instrument-identity.txt`).

**Instrument-identity defect (new, and it matters for anyone reading HEAD):** the counter committed
*at both judged revisions* is **v3, not the first freeze**. `git rev-parse
3b960fe5:tools/round-38/c1-counter.py` = `115085f0…` = v3 bytes, and
`git rev-parse 0fc61133:tools/round-38/c1-counter.py` = `115085f0…` too. `plans/round-38-claims.md`
was rewritten in the same commit (`git diff --stat e059ca93 3b960fe5 -- tools/round-38/c1-counter.py
plans/round-38-claims.md` → 72 and 83 changed lines). So the lane's HEAD instrument and HEAD claims
are the amended pair; the first-freeze pair is reachable only via `git show e059ca93:…`. The L1 did
run the freeze bytes explicitly and stored the v3 receipt under an explicit `NOT-THE-RULE` name,
which is the correct handling — this note is for later readers, not a finding against the L1 run.

## 2. Re-score (exact commands, exit codes)

```
python3 -I -B $S/c1-v1.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev <REV> --freeze e059ca9391642d5b71b6662cabcbdce0d9308719 \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --json-out <OUT>
```

| REV | exit | `carriers_matched` | `carriers_unchanged` | `met_target` | receipt |
|---|---|---|---|---|---|
| `3b960fe5` (C1 landing) | **1** | **3** | true | **false** | `artifacts/…/c1-v1-at-3b960fe5.json` |
| `0fc61133` (round landing) | **1** | **3** | true | **false** | `artifacts/…/c1-v1-at-0fc61133.json` |
| `77091b49` (base, do-nothing) | **1** | 0 | false | false | `artifacts/…/c1-v1-at-base.json` |

The C1 score is unchanged by the round's second landing commit: `corpus/evidence/round-38/c1/*` and
`.ufo/waves/round-38/c1/carriers.json` are byte-identical across `e059ca93 → 3b960fe5 → 0fc61133`
(`git diff --stat` empty on those paths), and the four carrier files still hash to their frozen pins
(K1 `1cfb6c33…`, K2 `403cb0a8…`, K3 `9c7c523c…`, K4 `a29ddc15…`).

Selftest of the same bytes (`python3 -I -B $S/tools/round-38/c1-counter.py --selftest --pkg65 <pkg>`)
→ `{"cases": 15, "green_ok": 1, "red_ok": 14, "failures": []}`, exit **0**. The claimed 15-case
count is exact (`artifacts/…/selftest.txt`).

## 3. Per-carrier clause matrix and the failing clause

Identical at both judged revisions (`artifacts/…/receipt-and-clauses.txt`):

| carrier | oracle files | published hits | handler | gaps | evidence id | matched |
|---|---|---|---|---|---|---|
| K1 | 5 | 5/5 | `squashfs_v4_be` | `[]` | ok | **true** |
| K2 | 3 | 3/3 | `squashfs_v4_be` | **1 gap** | ok | **false** |
| K3 | 4 | 4/4 | `squashfs_v4_be` | `[]` | ok | **true** |
| K4 | 4 | 4/4 | `squashfs_v4_be` | `[]` | ok | **true** |

**K2's only failing clause is `after_gaps_empty`.** Every other clause is true: `oracle_frozen`,
`after_present`, `after_subject_ok` (digest `403cb0a8…` = frozen pin), `after_operation_ok`
(`extract_firmware` / `unblob` 26.6.4), `after_handler_ok`, `after_evidence_id_ok`, and
`after_oracle_hits == oracle_files` (3 == 3 — all three oracle regular files *are* published).

The single gap, verbatim from the committed receipt:

```
kind=unpublished-entry  relative_path=firmware.bin_extract/var/lib/run-link
handler=null  dependencies=[]  continuation_id=602c674b7f83f4ac…
```

That is exactly the author's "K2 one `unpublished-entry` gap". `corpus/lessons/round-38.md:9` records
the same sentence and cites the same receipt I reproduce.

## 4. Bindings — `met_target` is false for two independent reasons

| term | base `77091b49` | `3b960fe5` | `0fc61133` |
|---|---|---|---|
| `province_core_section` (`## Round-38 additions to Core`) | false | **false** | **false** |
| `province_core_row` (row naming `squashfs_v4_be`, citing the entry) | false | **false** | **false** |
| `frontier_note` | **true** | true | true |
| `entry_present` | false | true | true |
| `sourced` (`S112,S113,S114` opened 2026-10-26, used-by = entry) | false | true | true |
| `coverage_map_row` | false | true | true |

`PROVINCE.md` at both judged revisions contains **no** `## Round-38 additions to Core` heading and no
Core row naming the handler — only the extended frontier bullet (`PROVINCE.md:157`) and the untouched
round-36 row (`:372`). So `met_target` would be false even if K2 matched: **2 of the 6 `bind_ok`
terms are false**, and the honest stop is overdetermined. Not adding a Core row is the *correct*
behaviour for an honest stop (the predicate's promotion surface is what a met target buys), so this
is an observation on completeness of the recorded reason, not a defect in the verdict.

## 5. Receipt reproduction — field-for-field

`.ufo/waves/round-38/l1/scores/c1-v1-at-3b960fe5.json` vs my run, JSON canonicalised with `argv`
removed: both hash to
`35d83b869abde25e018957a9b8960f7b2937ce82fac760740c58e45d77806513`; the set of non-`argv` differing
fields is empty. `carriers`, `bindings`, `carriers_matched`, `carriers_unchanged`, `met_target`,
`revision`, `freeze`, `predicate`, `target` all equal. **Reproduced.**

## 6. Independent re-derivation of the claim data (the receipts are genuine)

Rather than trusting the committed receipts, I re-ran the after arm on all four frozen carriers:

```
REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware <CARRIER> <NEW_OUTDIR> --full-output --format json
```

All four exits **0**; `normalized_result` compared to the committed `after.json` at `3b960fe5`
(`artifacts/…/rerun-comparison.txt`):

| carrier | files (rel+sha) equal | gaps equal | coverage | published bytes |
|---|---|---|---|---|
| K1 | true | true (`[]`) | partial | 9656 |
| K2 | true | true (`unpublished-entry` `var/lib/run-link`) | partial | 10283 |
| K3 | true | true (`[]`) | complete | 28 |
| K4 | true | true (`[]`) | complete | 28 |

So K2's gap is a **property of the frozen carrier + frozen tool**, not a bad receipt: the in-tree
symlink `var/lib/run-link` is never published as an entry and is always reported as
`unpublished-entry`. The author's diagnosis is grounded.

## 7. Informational: attempt-1 v3 counter at `0fc61133`

Cooked with `--freeze f1010f677a53ecf0e671952ce1bf4f44d51e151b`, exit **1**:
`carriers_matched 4`, `carriers_unchanged true`, `met_target false`. All four carriers match because
v3 replaced v1's `after_gaps_empty` with `after_no_missing_extractor_gap`, which an
`unpublished-entry` gap does not trip. `met_target` is still false for the same two binding reasons as
§4. So the amendment flips the carrier count 3 → 4 on *identical receipts* while leaving the round
verdict unchanged (`artifacts/…/c1-v3-at-0fc61133.json`).

## 8. Defects found (none verdict-flipping; ordered by severity)

**D1 — HEAD's claims↔counter pair is internally inconsistent; HEAD's claims sentence is false.**
`plans/round-38-claims.md` at `3b960fe5`/`0fc61133` still says the after-receipt "carries no
extraction gap", but the counter committed beside it accepts a receipt carrying one (§7). A reader
of HEAD gets `carriers_matched 4` from the instrument and "≤3" from the predicate sentence. The same
rewritten claims block asserts "*No claim was scored under v1*"; that is contradicted by
`.ufo/waves/round-38/w1/R38ExecAfterK1.md` (frozen sha `a7a62b09…`) and by
`corpus/lessons/round-38.md` M38-1, both committed in the same round.

**D2 — `frontier_note` is a rubber stamp, not a binding.** The check is
`any('big-endian' in l and 'superseded' in l)` over all of `PROVINCE.md`. The base line
`PROVINCE.md:157` already satisfies it (round-36 text: "superseded for LE SquashFS v4 … big-endian/AVM
stays here"), and my **base** run proves it: `frontier_note = true`, `met_target = false` at
`77091b49`. The predicate clause it implements — "the round-38 frontier note **supersedes** the
big-endian Frontier bullet" — is neither implemented nor true: the landed text says the opposite
("big-endian/AVM stays here … not promoted"). One of six `bind_ok` terms therefore discriminates
nothing. (Agrees with wave-1 `R38ReviewerPredicateIdentity` §2a and `R38CriticClaimsC1` §4.)

**D3 — `after_evidence_id_ok` is self-consistency only, not provenance.** Probe on the committed
K2 receipt through `tools/round-27/xpin-attribute.mjs` at the freeze pin (`artifacts/…/xpin-probe.txt`):

| mutation | 6.5.0 id changes? |
|---|---|
| `parameters.output_directory` → other dir | **yes** (`ev_309dc774…`) |
| `raw_result` emptied | **yes** (`ev_c907fa44…`) |
| `subject.local_path` → other path | no |
| stored `evidence_id` → `ev_deadbeef` | id recomputed correctly (forgery caught) |

Consequence measured, not inferred: my faithful fresh K2 run produced an **identical**
`normalized_result` and a **different** id (`ev_0bc9d25a…` vs `ev_e9386786…`). The clause checks that
a committed envelope agrees with itself; it cannot attest that the envelope came from the claimed
run. This is the mechanical reason the wave-1 fabrication kill (fake receipts + REA-minted ids
reaching `met_target`) works.

**D4 — the first-freeze predicate's "no external extractor dependency" premise is refuted by the
lane's own evidence, and v1 never tests it.** Predicate parenthetical: "run with stock unblob 26.6.4;
no external extractor dependency". I re-ran K1 with `~/.local/bin` off `PATH` (verified:
`sasquatch`, `sasquatch-v4be`, `unblob` all unreachable; `npx`/`node` still resolve, exit 0):
`published_bytes 0`, `files 0`, `handler squashfs_v4_be`, gap
`missing-extractor-dependency` / `dependencies ["sasquatch-v4be"]` — the same field values as the
committed `K1/before.json` (`artifacts/…/before-arm-k1.txt`). Since the after receipts publish all
oracle files, they necessarily ran **with** that binary reachable. `corpus/SOURCES.md` S112,
committed in the same round, says the same thing in the lane's own words:
"`get_dependencies()` returns `sasquatch` + `sasquatch-v4be`". v1 binds no clause about this, so
`carriers_matched 3` is computed while ignoring one term of the predicate the round says it is scoring
— under the strict reading the count is **0/4**, not 3/4. Direction of error: overcount. The
honest-stop verdict is unaffected.

**D5 — the target was structurally unreachable from the freeze.** `carriers_matched == 4` requires
"no extraction gap" on K2, whose carrier contains a live in-tree symlink that unblob 26.6.4 reports
as `unpublished-entry` on every run (§6, reproduced). No legitimate after-run on the frozen bytes
could ever satisfy the predicate, so C1's kill condition was determined by claim construction, not by
what a seat could discover. The honest stop is the right *response*; the claim design is the defect.

## 9. What I did not do / limits

- Did not re-run the before arm on K2/K3/K4 (K1 only); the three others are covered by the committed
  `before.json` bytes plus wave-1 `R38ExecBeforeArmRecheck`.
- Did not re-derive K1/K2/K3/K4 with `sasquatch-v4be -be` (the cross-tool arm); not needed for the
  counter's verdict.
- `[INFERENCE]` The 6.5.0 id's dependence on `parameters.output_directory` and `raw_result` explains
  my fresh-run id mismatch; the projection is imported from rea-agents 6.5.0's own
  `semanticProjection`, so I report the measured behaviour, not its internal field list.
- No tool installed or upgraded (nothing needed; `rea-agents@6.5.0` came from the existing npx cache,
  `unblob` 26.6.4 and `sasquatch-v4be` 4.5.1 were used in place and never touched).
- Scratch removed; artifacts kept:
  `c1-v1-at-{3b960fe5,0fc61133,base}.json`, `c1-v3-at-0fc61133.json`, `instrument-identity.txt`,
  `selftest.txt`, `receipt-and-clauses.txt`, `rerun-comparison.txt`, `rerun-K{1,2}-envelope.json`,
  `rerun-K1-before-envelope.json`, `before-arm-k1.txt`, `xpin-probe.txt`.

Report: .ufo/waves/round-38/w2/R38W2C1RescoreV1.md
