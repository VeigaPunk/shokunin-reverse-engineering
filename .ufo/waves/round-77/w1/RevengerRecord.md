# RevengerRecord — the round-76 correction history, reconstructed from committed bytes

Seat: `RevengerRecord` (r77-w1). Scope: round-76 routed defects **1** (the landing receipt cited as
green in three files) and **2** (loose tip-receipt revision prose), under the lane's traceability
rules. Read-only: this seat wrote no lane file; every proposed text below is for the L1 to land.

Revisions read: base `188562d43e3cc58b217ad7aa763fb296c5b8a0b7`; first correction commit
`fd0b95bd28c3af8ab56fdaf75beaff74f96ba604`; round-section commit
`41543a54…`; tip at last read `509c105140e90f7299b024796914e2639c206cb9` (the L1 was still
landing commits while this seat read; every claim below names the rev it was measured at).
The round-76 receipts are fixed blobs and do not move.

## 1. True values, from the receipts (literal `jq` output)

```
$ for f in c1-at-tip c1-at-landing c2-at-tip c2-at-landing; do jq -c '{rev,exit,ok,mismatch_count,arms_ok,arms_total,atoms:(.atoms|length),d24:([.atoms[]|select(.id=="D24_capability_rows")|.ok][0]),validate}' .ufo/waves/round-76/l1/scores/$f.json; done
{"rev":"1ab1e16480526ec2ad87def4c750a9dee85b9464","exit":0,"ok":true,"mismatch_count":0,"arms_ok":null,"arms_total":null,"atoms":9,"d24":true,"validate":{"atoms":9,"defects":[]}}
{"rev":"821d9eb64cb41be4dca640305feae0b5773ffb35","exit":1,"ok":false,"mismatch_count":1,"arms_ok":null,"arms_total":null,"atoms":9,"d24":false,"validate":{"atoms":9,"defects":[]}}
{"rev":"1ab1e16480526ec2ad87def4c750a9dee85b9464","exit":0,"ok":true,"mismatch_count":null,"arms_ok":3,"arms_total":3,"atoms":null,"d24":null,"validate":null}
{"rev":"821d9eb64cb41be4dca640305feae0b5773ffb35","exit":0,"ok":true,"mismatch_count":null,"arms_ok":3,"arms_total":3,"atoms":null,"d24":null,"validate":null}
```

`c2-at-*.json` carry no `atoms` array, hence the `null`s (the `for` loop's unified filter is the
only reason the columns exist).

```
$ jq -c '.atoms[]|select(.id=="D24_capability_rows")|.evidence.defects' .ufo/waves/round-76/l1/scores/c1-at-landing.json
["row 'capability-row binding': evidence path absent at the measured revision: ['.ufo/waves/round-76/l1/scores/c1-at-landing.json']","row 'executable printed counting command': evidence path absent at the measured revision: ['.ufo/waves/round-76/l1/scores/c2-at-landing.json']"]
```

```
$ jq -c '{rev,clean,audited,disclosures:(.disclosures|{exact,of,missing,stray})}' .ufo/waves/round-76/l1/scores/gate-at-tip.txt
{"rev":"862c48a8b8cbea1ad020261354bdc86f9bceba78","clean":27,"audited":51,"disclosures":{"exact":51,"of":51,"missing":[],"stray":[]}}
```

`gate-at-tip.txt` has **no `exit` and no `ok` key** (`keys` = `audited, claim, clean, disclosures,
flagged, freezes, required_clean, required_failed, rev, summary`) — routed defect 3, quoted here only
because the report's closing sentence counts it among the claims.

**First commit of the landing receipts' evidence paths.**

```
$ git log --diff-filter=A --format='%H %h %s' -- .ufo/waves/round-76/l1/scores/c1-at-landing.json
a89089306f920e5c64e5626c1c417ebcf9b87753 a8908930 round-76: instrument revision before the landing score …
$ git log --format='%H %h parents=%p' -1 a8908930
a89089306f920e5c64e5626c1c417ebcf9b87753 a8908930 parents=821d9eb6
$ git cat-file -e 821d9eb6:.ufo/waves/round-76/l1/scores/c1-at-landing.json   # fails
$ git cat-file -e a8908930:.ufo/waves/round-76/l1/scores/c1-at-landing.json   # succeeds
```

The two paths `c1-at-landing.json` and `c2-at-landing.json` first appear in `a8908930`, **the child**
of the commit `c1-at-landing.json` measures (`821d9eb6`). The landing receipt is red *by
construction* — the audit ran one commit before its own evidence was committed. This is the ground
truth the correction must state; the outside document's phrase "first appear in the commit it
measures" is off by one commit and must not be copied (see §5).

Instrument digests: `c1-at-landing` `18b2d7ba2adbe4f34603d86a15fa071ccba5dc6fcea868939f219ab8eece855d`
(first cut), `c1-at-tip` `805a8ba5ff6c83a374e88db589ff95b6f70b90fee1b102123b47ada22fe70f0e`
(revised at `a8908930`); `c2-at-landing` `4766df50…`, `c2-at-tip` `c169d670…`.

## 2. The form the correction must take (QUALITY 34, 35, 36, 65, 74; PROTOCOL §Evidence standard)

`PROTOCOL.md` §Evidence standard: "A falsified claim in an append-only file gets a named correction
entry in the lane's next round — appended, never rewritten"; "Corrections sweep every mention";
"Commits are cited by hash". `QUALITY.md` row 65: "An outside disagreement gets an appended measured
correction in the next LOG/lesson, never a rewrite of the filed report." Rows 34–36 govern reversal
traceability; row 74 governs registry/index edits (row count **and** tallies, insertion anchor
re-read).

From those, the surface split for these two defects:

- **Editable in place** (living record cells that currently assert a false value, where the old→new
  is preserved in this round's appended correction block):
  - `SCORECARD.md` `## Capabilities` row `capability-row binding`, evidence cell — it is the current
    repertoire index, not a filed round section; a false verdict left standing there is the live
    defect.
  - `SCORECARD.md` round-76 R76-C1 row, before→after cell — edited in place **only** because the
    original landing result stays named in the same cell ("records 1 by construction"), so the
    revised result is reported *beside* the original (QUALITY 34), not substituted for it.
  - `PROVINCE.md` round-76 `- **Core —` C1 evidence lines — same reasoning: the superseded path is
    replaced and the landing value restated in the same bullet.
  - The round-77 "Record corrections — round 77" block itself (this round's own new text, not filed
    bytes) — its quotations must be exact and its parentage corrected.
- **Append only**: `LOG.md` (explicitly append-only; the round-76 entry at `LOG.md:4563` stays
  byte-identical, and the round-77 entry carries the correction) and `corpus/lessons/round-76.md`
  (filed lesson; its disposition row 5 is superseded by the appended LOG/lesson text, not rewritten).
  The appended block must contain: the spot-check path and section (`corpus/lessons/round-76-verifier-spotcheck.md`
  §6 items 1–2), each old string quoted exactly, each new value with its receipt `rev`, the reason
  the old value was wrong (off-by-one commit for defect 1; wrong commit named for defect 2), the
  rule applied (QUALITY 34/65), and what remains byte-identical.
- **Never rewritten**:
  - `.ufo/reports/round-76/kaidoku.md` (the filed report — QUALITY 65); its lines 115/127/135 stay as
    filed and the correction names them by line.
  - `.ufo/waves/round-76/claims.json` and `plans/round-76-claims.md` (frozen contract; the frozen
    `after` clause "landing: exit 0, mismatch_count 0…" is a declaration, not the measurement — the
    correction names the receipt that decides, it does not touch the frozen text).
  - Every `.ufo/waves/round-76/**` receipt, including `c1-at-landing.json` (red, and must stay red).
  - The round-76 LOG entry and the round-76 lesson bytes (append/supersede only).

## 3. Defect 1 — the three cells (landed at `fd0b95bd`; two precision fixes remain)

### (a) `SCORECARD.md` round-76, R76-C1, before→after cell (base `188562d4:5907`; HEAD `:5909`)

Old (base, verbatim):

```
base `pre/c1-at-base.json`: 1 mismatch, both absent rows named → `l1/scores/c1-at-landing.json`: 0 mismatches, nine atoms
```

Landed at `fd0b95bd` (verbatim, HEAD):

```
base `pre/c1-at-base.json`: 1 mismatch, both absent rows named → `l1/scores/c1-at-tip.json`: 0 mismatches, nine atoms (the landing receipt `c1-at-landing.json` records 1 by construction: its two evidence paths first appear in the commit it measures)
```

**Mode: in-place.** **Status: landed**; the trailing clause is wrong about *which* commit first adds
the paths. Proposed precision text (replace the parenthetical only):

```
(the landing receipt `c1-at-landing.json` records 1 by construction: it was scored at `821d9eb6`, the parent of `a8908930`, the commit that first adds the two evidence paths it cites)
```

### (b) `SCORECARD.md` `## Capabilities`, row `capability-row binding`, evidence cell (`:656`)

Old (base, verbatim):

```
`.ufo/waves/round-76/l1/scores/c1-at-landing.json` (D24 true, mismatch_count 0)
```

New (landed at `fd0b95bd`, verbatim):

```
`.ufo/waves/round-76/l1/scores/c1-at-tip.json` (D24 true, mismatch_count 0, nine atoms)
```

**Mode: in-place.** **Status: landed and complete** — every annotation binds against
`c1-at-tip.json` (`D24 true`, `mismatch_count 0`, `len(atoms)==9`). The row no longer shows the
landing value; that is correct for a repertoire index (the pair lives in the claim row and in
PROVINCE), and QUALITY 34 is satisfied at the round level rather than in this cell.

### (c) `PROVINCE.md` round-76 C1 evidence (base `188562d4:588-590`; unchanged line numbers at HEAD)

Old (base, verbatim, three lines):

```
  revision and a first-working-round cell naming the claiming round; six red fixtures in its selftest. Retained
  evidence: `.ufo/waves/round-76/l1/scores/c1-at-landing.json` (D24 true, mismatch_count 0) and
  `.ufo/waves/round-76/pre/c1-at-base.json` (mismatch 1, both absent rows named).
```

Landed at `fd0b95bd` (verbatim, HEAD):

```
  revision and a first-working-round cell naming the claiming round; six red fixtures in its selftest. Retained
  evidence: `.ufo/waves/round-76/l1/scores/c1-at-tip.json` (D24 true, mismatch_count 0) and
  `.ufo/waves/round-76/pre/c1-at-base.json` (mismatch_count 1, both absent rows named); the
  landing receipt `c1-at-landing.json` records 1 by construction (its two evidence paths first
  appear in the commit it measures).
```

**Mode: in-place.** **Status: landed**; same off-by-one clause. Proposed precision text (replace
the last clause):

```
; the landing receipt `c1-at-landing.json` records 1 by construction: it was scored at `821d9eb6`,
  the parent of `a8908930`, the commit that first adds the two evidence paths it cites.
```

## 4. Defect 2 — the LOG append (not landed; the record currently claims it is)

The filed report (fleet root, `.ufo/reports/round-76/kaidoku.md`, never rewritten) carries the loose
prose:

- `:115` — "After, at the measured revision `875e6488`: exit 0, `mismatch_count 0`…"
- `:127` — "After, at `da41dfba`: exit 0, `arms_ok 3` of 3…"
- `:135` — "Both claims are measured against committed bytes at `875e6488`, the lane tip at filing…"

The receipts record `rev 1ab1e164` for both `*-at-tip.json`; `875e6488` is the lane tip at filing and
`da41dfba` is the scout's source-repair commit. `git diff --stat 1ab1e164 875e6488 -- SCORECARD.md
PROVINCE.md SKILL.md corpus/` prints nothing, and the round-76 audit reads only round-75 receipts
(`tools/round-76/record-audit.py:73-82`), so the values stand — the measure is the receipt's own
`rev`, not the tip.

**There is no round-77 `LOG.md` entry at `509c1051`** (`git show HEAD:LOG.md | grep -c 'round 77'`
→ 0), while both `SCORECARD.md` (corrections block, bullet 2) and `corpus/lessons/round-77.md:46`
say "the correction is appended in `LOG.md` (round-77 entry)". That closure is unsupported today.

**Proposed LOG append** (append mode; a new round-77 entry, after the round-76 entry):

```
- **Correction to the filed round-76 report and to the round-76 closure rows (appended per QUALITY
  65; the filed bytes stay).** The report at `.ufo/reports/round-76/kaidoku.md:115` says R76-C1 was
  measured "at the measured revision `875e6488`", at `:127` that R76-C2 was measured "at
  `da41dfba`", and at `:135` that "Both claims are measured against committed bytes at `875e6488`".
  Each receipt names its own revision: `c1-at-tip.json` and `c2-at-tip.json` both record
  `rev 1ab1e16480526ec2ad87def4c750a9dee85b9464` (exit 0; `mismatch_count 0` over nine atoms with
  `D24_capability_rows true`; `arms_ok 3` of `arms_total 3` respectively). `875e6488` is the lane
  tip at filing and `da41dfba` the scout's source-repair commit; neither is a measured revision.
  The record surface the C1 atoms read is byte-identical from `1ab1e164` to `875e6488`
  (`git diff --stat 1ab1e164 875e6488 -- SCORECARD.md PROVINCE.md SKILL.md corpus/` prints
  nothing), so the values stand and the receipt's `rev` is the measure. The gate receipt is
  measured at `862c48a8` and carries no `exit` field (routed defect 3). The round-76 lesson's
  disposition row 5 (`corpus/lessons/round-76.md:80`, "closed in the round-76 report: each receipt
  is named with the revision it records") and this lane's round-76 entry (`LOG.md:4563`, "the
  receipt-revision prose is restated in the report") are superseded by this entry; the filed text
  stays.
```

**Proposed LOG bullet for defect 1 traceability** (so the LOG, not only the SCORECARD block, carries
the old→new):

```
- **Correction to the round-76 record (routed defect 1).** Three cells cited the landing receipt as
  green, each in its own wording: the R76-C1 after-cell `→ l1/scores/c1-at-landing.json: 0
  mismatches, nine atoms`; the `capability-row binding` evidence cell
  `.ufo/waves/round-76/l1/scores/c1-at-landing.json (D24 true, mismatch_count 0)`; and the PROVINCE
  round-76 evidence line `c1-at-landing.json (D24 true, mismatch_count 0)`. That receipt records
  `rev 821d9eb6`, `exit 1`, `mismatch_count 1`, `D24_capability_rows false`, and it was scored at
  the parent of `a8908930`, the commit that first adds the two paths it names. The three cells now
  cite `c1-at-tip.json` (`rev 1ab1e164`, exit 0, `mismatch_count 0`, nine atoms) and state the
  landing value as 1 by construction; the old→new is in the SCORECARD "Record corrections — round
  77" block. The receipt and the filed report stay byte-identical.
```

## 5. Sweep — hits the spot-check did not name

1. **The correction block's own quotation is inexact.** `SCORECARD.md` "Record corrections — round
   77", bullet 1, says "Three cells said `c1-at-landing.json (D24 true, mismatch_count 0)`". Only two
   cells used that wording; the R76-C1 after-cell said "`l1/scores/c1-at-landing.json`: 0 mismatches,
   nine atoms". Traceability requires each old string quoted. **Fix (in-place, this round's block):**
   replace that summary with the per-cell quotation now in the proposed LOG bullet above.
2. **The off-by-one commit clause is replicated in four places**: the outside document
   (`corpus/lessons/round-76-verifier-spotcheck.md:99`, "first appear in the commit it measures"),
   the filed report (`:120-121`, "the receipt its rows point at first appears in that commit"), the
   R76-C1 cell, the PROVINCE bullet, and the SCORECARD corrections block (bullet 1). The true
   relation is parent `821d9eb6` → child `a8908930`. The filed report and the outside document stay
   byte-identical; the two living cells and the block take the precision fix in §3.
3. **`LOG.md:4563`** (round-76 entry): "the receipt-revision prose is restated in the report" — false;
   the report's prose is the loose one this defect names. Append-only: the round-77 entry supersedes
   it (text in §4). The spot-check did not name this sentence.
4. **`corpus/lessons/round-76.md:80`** (disposition row 5): "closed in the round-76 report: each
   receipt is named with the revision it records" — false for the two tip receipts. Filed lesson:
   supersede via the appended LOG/lesson, do not rewrite. Not named by the spot-check.
5. **`corpus/knowledge/2026-11-04-r76-capability-row-binding.md:1`** lists
   `c1-at-landing.json` among the entry's receipts without a verdict. It is not a green citation, but
   it invites the same misreading. Optional in-place precision fix: point the `source:` line at
   `c1-at-tip.json` (the record value) or append "(the landing receipt records 1 by construction)".
   No other lane file carries the false verdict: the remaining hits are quotations of the defect
   (`tools/round-77/verdict-bind.py:6,523` and the two do-nothing controls; `plans/round-77-claims.md:31`;
   `corpus/knowledge/2026-11-04-r77-verdict-binding.md:9`; `corpus/lessons/round-77.md:33`;
   `SCORECARD.md:5977` inside the correction block) and must not be "corrected".
6. **Mid-landing contradiction at `fd0b95bd`.** That commit's round-77 section says "Capabilities
   rows appended … `evidence-cell verdict binding` and `prefile gate receipt`", but the committed
   table holds neither (`git show fd0b95bd:SCORECARD.md | grep -c 'evidence-cell verdict binding'`
   → 0). `41543a54` adds them; at `509c1051` the table has both and `verdict-bind.py` reports
   `capability_rows 41, in_scope_rows 11`. Not a final-record defect, but the record commit that is
   gated must be the one carrying the rows — the same claim-vs-table class round 76 was built to
   catch.
7. **`corpus/lessons/round-77.md:46` and the SCORECARD block bullet 2 assert the LOG append exists.**
   At `509c1051` it does not. The claim is premature, not false forever; it becomes true only when
   the text in §4 lands in `LOG.md`.

## 6. Evidence chain and confidence

- Defect 1's three old strings: `git show 188562d4:SCORECARD.md` lines 656 and 5907;
  `git show 188562d4:PROVINCE.md` lines 588-590. New strings: `git show fd0b95bd:…` (verified equal
  at `41543a54` and `509c1051`).
- Landing receipt red: `.ufo/waves/round-76/l1/scores/c1-at-landing.json` (`rev 821d9eb6`, `exit 1`,
  `mismatch_count 1`, `D24 ok false`, `validate` clean), and the two `D24` defect strings naming the
  absent paths.
- Path existence per rev: `git cat-file -e` at `821d9eb6` (absent) and `a8908930` (present);
  `git log --format='%p' -1 a8908930` → `821d9eb6`.
- Tip values: `c1-at-tip.json`/`c2-at-tip.json`, `rev 1ab1e164`, exit 0.
- Byte-identity claim: `git diff --stat 1ab1e164 875e6488 -- SCORECARD.md PROVINCE.md SKILL.md
  corpus/` is empty; the audit's receipt inputs are round-75 paths
  (`tools/round-76/record-audit.py:73-82`), unchanged in that range.
- LOG append absent: `git show 509c1051:LOG.md | grep -c 'round 77'` → 0.
- Confidence: high on every number and quotation; medium on the judgement that the capability row may
  cite the tip alone (QUALITY 34 read at round level) — the alternative (adding the landing value
  beside it in the row) is defensible and would also satisfy the rule.

## 7. Limits

- The L1 was landing commits while this seat read (`fd0b95bd` → `41543a54` → `440ee041` → `509c1051`);
  line numbers above are per the named rev. Any re-read must re-anchor on the rev, not the text.
- No gate was executed to re-derive the round-76 values; the tip re-derivation is R77-C1's job and
  this report does not substitute for it.
- The filed report and the outside document were read at the fleet root (read-only); they are outside
  the lane and untouched.
