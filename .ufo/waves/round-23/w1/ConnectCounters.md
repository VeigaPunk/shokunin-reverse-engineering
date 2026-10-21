# ConnectCounters — two denominators, one revision: held k/6 vs lexical m/153

Seat: `KaidokuR23.ConnectCounters` (connector, leaf, author-side). Round 23, claim
`R23-C1` (coverage). Read set: round-23 claims and wave cache, round-22 claims,
counter, verification records and knowledge entries, retained 6.5.0 CLI catalog,
round-20/21 helpers. No REA invocation, no target, no execution, no device, no
network, no production file edited. This report is advisory to L1; it is not
outside verification and it does not add a held verb.

## Findings

### F1. What the `133/153` number actually counts

Observation. The number is emitted by the frozen R22 counter as
`catalog_mentioned_count` / `catalog_total` (`.ufo/waves/round-22/tools/count-c1.py:181-183`).
Its unit is **one retained 6.5.0 CLI verb that appears at least once in any tracked
blob under `corpus/knowledge/`**, not an occurrence count:

- `.ufo/waves/round-20/tools/verb-coverage.py:34` — `KNOWLEDGE_PREFIX = "corpus/knowledge/"`.
- `.ufo/waves/round-20/tools/verb-coverage.py:99-105` — `command_pattern` matches the
  hyphenated name **or** its underscore form at ASCII token boundaries, case-insensitively.
- `.ufo/waves/round-21/tools/verb-coverage.py:125-129` — catalog loaded from the retained
  `round20/verb-coverage.json`; `per[verb] = sum(bool(pattern.search(text)) for text in texts)`,
  i.e. a **file-level boolean summed over files**, then `mentioned`/`zero` at `:151`.
  Two knowledge files naming the same verb still count as one mentioned verb.
- The R22 claim itself describes the baseline as “153 commands, 20 with zero knowledge
  mentions at baseline” (`.ufo/waves/round-22/claims.json:10`), and its own control
  observed `catalog_zero_count 20`, `catalog_mentioned_count 133`, with **all six T1
  verbs inside `catalog_zero`** (`.ufo/waves/round-22/w2/ControlPriorKnowledge.md:76`;
  retained stdout `.ufo/waves/round-22/verify/before-c1.json:13`).

Observation, runs of the frozen counter (three direct here — `7787fea`, `aa1450b`,
`a3c92eb` — plus the retained R22-final record whose `script_sha256` is the same
pinned counter; `GIT_*` cleared, replacement refs empty — `git replace -l` printed
nothing):

| rev | role | k/6 | catalog | zero | T1 verbs in zero |
|---|---|---|---|---|---|
| `7787fea4d6fd718726de92ed20759d11ce7b8b48` | R22 baseline | 0/6 | **133/153** | 20 | all six |
| `e9db7e2d5798ff3d5f1ba5ccd76bb86f2cc5c1bb` | R22 final (retained `verify/final/after-c1.json:16`, exit 1) | 1/6 (`identify-flutter-build`) | 135/153 | 18 | four (debug×2, signal×2) |
| `aa1450b82f9ede35aada63efe8a34e01c6e02f72` | R23 declared baseline | 1/6 | 135/153 | 18 | four |
| `a3c92eb6bc70984e90ae5b895412de978840b2c5` | R23 freeze / HEAD | 1/6 | 135/153 | 18 | four |

Exact argv for every direct run:

```
python3 -I -B .ufo/waves/round-22/tools/count-c1.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV>
# observed exit 1 at 7787fea, aa1450b and a3c92eb; stdout parsed fields as tabled
# counter sha256 c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879
```

Each direct run printed one JSON object to stdout and nothing to stderr; the
`GIT_*` environment was cleared and `GIT_NO_REPLACE_OBJECTS=1` was set inside the
child, and `git replace -l` was empty. The output was captured to `/tmp` only for
field extraction; the lane was not written by these runs.

Same output from an exact-helper scan (round-20 helper extracted from Git, sha256
`cfbf1880c4fb2bba80e3c2e40e236165a67c03bf51cced4983b469cfe315b26f`, matching the
counter's `HELPER_SHA256` pin):

| rev | knowledge blobs | mentioned/153 | zero | T1 file-presence (identify, dart, gdb, rizin, signal-inv, signal-dec) |
|---|---|---|---|---|
| `7787fea` | 103 | 133 | 20 | 0, 0, 0, 0, 0, 0 |
| `e9db7e2` | 105 | 135 | 18 | 2, 1, 0, 0, 0, 0 |
| `aa1450b` | 105 | 135 | 18 | 2, 1, 0, 0, 0, 0 |
| `a3c92eb` | 105 | 135 | 18 | 2, 1, 0, 0, 0, 0 |

### F2. What the `k/6` held number counts

Observation. `R23-C1` freezes six verbs and a denominator of 6
(`.ufo/waves/round-23/claims.json:16-25`), with `before: 1` (`:24`) and target
“cumulative sourced original-envelope bound held count >=2/6, exact k reported”
(`:26`). The counter counts a verb only when a `corpus/knowledge/` entry names it,
cites a retained file under the evidence prefix, the envelope has `ok:true`,
`meta.command` equals the verb (debugger aliases preserved), the record binds the
cited `evidence_id` and operation, no refusal ancestry remains, and the entry's
source row is eligible (`.ufo/waves/round-22/tools/count-c1.py:33,101-183`).
Mention alone, refusal, unbound copy, or uncited file never count; the claim's
falsifiers say so explicitly (`.ufo/waves/round-23/claims.json:30-38`), and R22's
own knowledge entry records the split: the Dart refusal is “**not held or counted**”
and remains “mention-level catalog coverage here, not exercised success”
(`corpus/knowledge/2026-10-21-r22-flutter-positive-dart-refusal.md:15,23`); “a
mention without a bound record must not count”
(`corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md:26`).

At `aa1450b`/`a3c92eb` the exact per-verb state is: `identify-flutter-build`
entries 2, exercised true; `inspect-dart-aot` entries 1, exercised false (typed
`unsupported_target`); the other four entries 0. Exact incomplete count at the
R23 baseline: **5 of 6**, decomposed as 1 mentioned-but-refused (`inspect-dart-aot`)
plus 4 with no knowledge entry at all (debug pair, signal pair).

### F3. The two figures are nested scopes with different units — never interchangeable

- Scope: the six T1 verbs are a subset of the 153-command catalog. At baseline the
  catalog numbers decompose as **133 mentioned non-T1 / 147 + 0 mentioned T1 / 6**;
  the 20 zero as **14 non-T1 + 6 T1**. After R22, **135/153 = 133 non-T1 / 147 +
  2 T1 / 6**, zero **18 = 14 non-T1 + 4 T1**. The entire +2 movement in the
  catalog metric came from the six-verb claim's own two new knowledge entries; the
  non-T1 map did not move.
- Refinement: under this counter architecture, held implies mentioned (a held verb
  must have a naming `corpus/knowledge/` entry), never the converse. Same-revision
  cross-tab:

| rev | both | mentioned-only | held-only | neither | total |
|---|---|---|---|---|---|
| `7787fea` | 0 | 0 | 0 | 6 | 6 |
| `e9db7e2` / `aa1450b` / `a3c92eb` | 1 (identify) | 1 (inspect-dart-aot, refused) | 0 | 4 | 6 |

- Therefore `1/6` and `135/153` are not 17% vs 88% of one thing. They are a strict
  refinement (bound exercise) over a much wider, weaker lexical map (file-level
  prose presence) on a different denominator. The only same-scope mention ceiling
  for the claim is **2/6**, not 135/153. The mention map's legitimate use is to
  name the remaining ground: the four T1 verbs still in `catalog_zero` cannot be
  held until an entry names them, and a mention is still necessary-but-insufficient.
- Revision pairing is mandatory: `133/153` pairs with `0/6` at `7787fea`; the
  claim's `before: 1` pairs with `135/153` at `aa1450b`. Mixing `133/153` with
  `1/6` would compare different revisions.

### F4. R23-specific second-order effect: mention delta is expected and semantically empty

Observation/inference. The mention scan reads every tracked `corpus/knowledge/`
blob, including code blocks, boundary prose, copied JSON operation names, and
disclaimers. An R23 entry that names `inspect-signal-decoders` and
`decode-signal-recording` — even to say what was *not* done — moves the catalog
metric to at most 137/153 and the T1 zero set to 2, with **zero** change to `k/6`
unless bound envelopes also survive the counter. Repeating the wave's
“no debugger execution” boundary in an entry could additionally move
`debug-with-gdb`/`debug-with-rizin` out of `catalog_zero`.
[INFERENCE, conditional on a tracked `corpus/knowledge/` entry: n rises by one per
previously-zero verb named, zero falls correspondingly.] Reports under
`.ufo/waves/round-23/w1/` or `claims.json` do **not** move this metric; only
`corpus/knowledge/` does. Also, the counter reads commits via `git show`: R23
evidence currently in the worktree (`round-23/evidence/c1/`, 0 files tracked at
`a3c92eb`) is invisible until committed.

So the R23 statement “after” numbers may show n/153 rising (e.g. 135→137) while
k stays 1 or rises only for the signal verbs that actually bound. Reporting that
rise as coverage would be exactly the claim's “mere mention counts” falsifier
(`.ufo/waves/round-23/claims.json:33`).

### F5. Wrapper surface: observed implementation takes one catalog block

Observation. The R23 wrapper — authored during this wave, sha256
`7220573647a41052c539ea08f3c2b33f9b41d68bd8e0a9a6b05150e86a045b97` — loads the
exact R22 counter by sha256, resolves one commit, and calls `r22.measure` twice
with `EVIDENCE_PREFIX` set to the R22 and R23 evidence roots
(`.ufo/waves/round-23/tools/count-c1.py:41-56`). It unions only
`targets[verb].historical` from scan 0 with `new` witnesses gated in scan 1
(`:77-87`), and it emits the catalog fields from **scan 1 only** (`:90-91`), not a
sum. So the `270/153` merge defect is not present in the observed implementation.
Two residual wrapper properties matter to this ledger: the legacy five-candidate
cap (`.ufo/waves/round-22/tools/count-c1.py:168`, `witnesses[:5]`) can undercount
beyond the retained window, and the new-witness gate names the verb in hyphen
form, case-sensitively (`round-23/tools/count-c1.py:83`), while the mention scan
accepts hyphen **or** underscore, case-insensitively (round-20 helper `:99-105`).
An underscore-only entry can therefore move `catalog_mentioned_count` without
ever qualifying as a new held witness.

## Affected axes

- **Coverage (primary, no numerator change):** makes the R23-C1 frontier statement
  exact about what is held (1/6), what is mentioned-but-refused (1), what is
  untouched (4), and what an entry-only move can and cannot do. The claim target
  and denominator remain `>=2/6` / 6.
- **Calibration (primary):** fixes the unit and denominator of both published
  numbers, forbids cross-revision pairing, forbids substituting n/153 into the
  six-verb numerator, and makes an accidental sum visible.
- **Depth:** untouched; no new domain claim, no execution, no dynamic ownership,
  no source row.

## Proposed move (one, bounded)

**Adopt a five-line, same-revision coverage ledger in the R23 final completeness
statement (DraftCompleteness/L1 report), with the catalog mention figure
quarantined as descriptive map context.** Proposed text, with values filled at the
final rev:

```
held         k/6     = <k>/6     (bound original envelopes; denominator frozen at 6)
T1 mentions  m/6     = <m>/6     (corpus/knowledge lexeme presence; not a holding)
catalog      n/153   = <n>/153, zero <z>   (retained 6.5.0 catalog; descriptive only)
cross-tab    both <b> | mentioned-only <u> | held-only <h> | neither <z6>   (b+u+h+z6=6)
same-rev     <REV>; mention deltas after aa1450b are entry-side, not holdings
```

Rules for L1:

1. `k` is the only numerator for `R23-C1`; `m` and `n` are context and cannot
   substitute, be averaged, or be called coverage.
2. Emit the catalog block once per revision (max 153, `total == 153`); never sum
   the two measure calls.
3. Measure `k`, `m`, and `n` at the same resolved commit; pair the historical
   `133/153` only with `0/6` at `7787fea`.
4. Attribute every final `catalog_zero` exit to the specific new
   `corpus/knowledge/` entry and verb, and label it “mention-only”; do not add it
   to `k`.
5. Assert held ⊆ T1 mentions at that revision; `held-only` must be 0 under the
   current counter. A nonzero value means entry scope moved, not that coverage
   grew.

Why this is compatible across the round's proposals: BuildCounter supplies the
union/`k`; CoverageMap supplies which verb leaves `zero` and why; DraftCompleteness
needs the exact `1/6` incomplete line; ReviewFrozenTargets freezes both
denominators; CriticVacuity's mention-only and duplicate-witness attacks become
visually checkable in the cross-tab. No proposal is displaced.

## Risks

1. **Revision mixing** is the main failure mode: `133/153` belongs to `7787fea`
   with `0/6`; `1/6` belongs to `aa1450b` with `135/153`.
2. **Mention metric is prose-shaped:** code blocks, operation names, and boundary
   disclaimers all match; a negative statement about debug-verbs still counts as a
   mention. It has no source eligibility, no envelope, and no refusal check.
3. **File-boolean, not occurrence count:** one entry repeating a verb 20 times is
   one mentioned verb; two files are still one catalog verb.
4. **Union/sum bug:** the observed wrapper takes one catalog block
   (`round-23/tools/count-c1.py:90-91`), so `270/153` is not present in that
   revision; assert `catalog_total == 153` and a single block anyway, because the
   wrapper is a mutable wave artifact.
5. **Uncommitted evidence:** the counter sees Git objects only; R23 evidence must
   be committed before the final count, or new witnesses are invisible.
6. **Scope drift:** held ⊆ mentioned holds only while entries are read from
   `corpus/knowledge/`; changing that prefix invalidates the cross-tab.
7. **Inventory-only adjudication is not mine:** whether a pathless
   `inspect-signal-decoders` inventory envelope counts as held is L1/reviewer
   territory; the ledger will expose it as held only if the wrapper reports it in
   `t1_exercised`, and the mention map stays unaffected either way.
8. **No final values yet:** the 135/153 and 1/6 figures are baseline observations;
   R23 evidence/drafts are still moving (evidence untracked at observation).

## Verification (for L1; none of this is claimed as run at R23 final)

1. Frozen reference at the R23 baseline (observed here, exit 1):

```
python3 -I -B .ufo/waves/round-22/tools/count-c1.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev aa1450b82f9ede35aada63efe8a34e01c6e02f72
# expect: t1_exercised_count 1/6 [identify-flutter-build];
#         catalog_mentioned_count 135, catalog_total 153, catalog_zero_count 18;
#         inspect-dart-aot entries 1 exercised false; other four entries 0
```

2. R23 wrapper at the final commit: assert `catalog_total == 153`,
   `catalog_mentioned_count <= 153` and equal to a single-measure recount (never
   `270`), `t1_exercised_count >= 1` with `identify-flutter-build` preserved, and
   every new witness path starting `.ufo/waves/round-23/evidence/c1/`. For each
   new witness, confirm the entry's first line cites a mined A/B S058+ row opened
   2026-10-21 with that exact entry in used-by, and that the entry names the verb
   in hyphen form (the wrapper's `:83` gate is case-sensitive and hyphen-only).
   Account for the legacy five-candidate cap (`count-c1.py:168`): a verb with
   more than five retained bound candidates may be undercounted, which can only
   lower `k`, never inflate it.
3. Recompute the ledger at the final rev with the helper-exact scan used here
   (round-20 helper pinned by sha256
   `cfbf1880c4fb2bba80e3c2e40e236165a67c03bf51cced4983b469cfe315b26f`, `GIT_*`
   cleared, `GIT_NO_REPLACE_OBJECTS=1`); expected baseline output is the F1 table.
4. Cross-tab assertions: `b+u+h+z6 == 6`; `h == 0`; held set ⊆ T1 mention set; T1
   zero set is the complement of T1 mentions.
5. No-harm spot check (L1 scope): prior `corpus/knowledge/` blobs and prior
   SOURCES rows byte-identical between `aa1450b` and final; new knowledge files
   and appended S058+ rows are additions, not replacements of prior rows.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/ConnectCounters.md`
  — this report. Its sha256 (of the file bytes before the self-hash trailer line)
  is recorded at the end of the file; verify with `sed '$d' <file> | sha256sum`.
- No other outputs written. Scratch stdout captures existed only under `/tmp`
  (`connectcounters-r22-at-7787fea.json`, `-aa1450b.json`, `-a3c92eb.json`) and are
  not lane artifacts; key fields are reproduced above.

## Installs

None. No pacman/uv/npx/cargo/npm install or upgrade; no config edit; no service
restart. All tools were pre-existing (`python3`, `git`).

## Open risks / honest limits

- The R23 counter appeared after this seat's first measurement. It was inspected
  read-only at sha256
  `7220573647a41052c539ea08f3c2b33f9b41d68bd8e0a9a6b05150e86a045b97` and was
  **not executed by this seat** (its `measure` creates `round-23/runtime/`; the
  final run belongs to L1). F5 reflects the observed code, not a final-run
  result, and the file may change before integration.
- R23 evidence under `round-23/evidence/c1/` is untracked at `a3c92eb`
  (`git ls-tree` count 0); final counts depend on L1 committing it.
- The 1/6 baseline is a cumulative inherited witness (R22 final);
  at `7787fea` the same counter observed 0/6. Both are reported, not conflated.
- `inspect-dart-aot`'s typed refusal is retained and explicitly not counted; it
  remains mention-level only. No claim is made that the signal pair, debugger
  pair, or inventory-only evidence adds a held verb.
- At final observation the worktree had `corpus/SOURCES.md` modified (sibling
  scribe work, not this seat; this seat wrote only this report). L1 must run every
  count at a resolved commit, not the mutable worktree.
- No REA probe was selected or attempted; no target sha256 applies to this seat.
  No failures occurred; the only “incomplete” is the claim's intended 5/6
  incomplete state.
Report body sha256 (this line excluded; verify with `sed '$d' <file> | sha256sum`): c4df0fac3c5022fe24baa73b910f9126df3348762365e3afcf8f4ccd8eeb88f4
