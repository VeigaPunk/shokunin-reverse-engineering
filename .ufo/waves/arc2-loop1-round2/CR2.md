# CR2 (critic) — scope attack on C2: are README summary labels in scope for safety-label qualification?

Seat CR2, wave arc2-loop1-round2, 2026-10-18. Read-only: every command below was
run by this seat this session; scratch confined to `/tmp/arc2-l2r2-CR2-scope/`
(three copied README variants, repo untouched). HEAD at every command:
`165057e36f558c95eb02bf24de4a874d559d6950`; `git status --porcelain` →
`?? .ufo/waves/arc2-loop1-round2/` only. My only write is this report. No MCP
session opened by this seat (`pgrep -af '[r]ea\.mjs|[r]ea-agents|[r]ea doctor|[r]ea mcp'`
→ rc=1 — no process of mine to close). Round-2 seat reports read this session:
C2.md, E1.md, E2.md, E9.md, E17.md, E19.md, V2.md, V5.md, V6.md, CR6.md, CR8.md.

## 1. Verdict

**SCOPE OBJECTION REFUTED on the record — `corpus/README.md:90,:160` ARE in
scope — but with two live defects the parent must fix: (a) the *appended-note*
form is the wrong form for README (measured citation drift makes it stale the
way `SCORECARD.md:68` went stale); the *in-cell* form is the correct
index-appropriate analogue of the r3 erratum; (b) the round's own after-
measurement is form-dependent and fails by construction on the recommended
form, and the "drifted pointer 1 → 0" measurable undercounts — the drift is
DOUBLE.**

Three parts:

1. **The strongest scope objection** ("README rows are index pointers, not
   knowledge claims; the genre split excludes them") is real but already
   adjudicated against, by the record itself (§3).
2. **Form finding (§4):** both loci drifted +10/+17 lines across the arc
   (measured table below). An appended note that names `:90`/`:160` re-creates
   exactly the `SCORECARD.md:68` failure class this round is repairing.
   In-cell qualification is self-anchoring. Dry-run verified (§4.3).
3. **Instrument finding (§5, the round's most useful repair):** E19's skeleton
   asserts `grep -c '\*\*Safety-label scope'` → 0→1, which only passes on the
   appended form (measured: in-cell variant → 0; appended variant → 1). And
   `SCORECARD.md:68` carries **two** drifted pointers (`:160`→`:177` and
   `:128`→`:138`), not one — repairing only `:160` leaves a drifted pointer
   inside the repaired bullet.

## 2. The scope question, stated plainly

C2's measurable: "unqualified safety-label loci in editable corpus files
2 → 0 (r3 file already clean from round 1); drifted pointer 1 → 0" (round
claim). The loci are `corpus/README.md:90` (Knowledge-table row, topic cell:
`` `~/.local/bin/jq` = byte-identical upstream jq-1.8.2 release — benign ``)
and `:160` (Lessons-table row, gist cell: `… shadow-binary verdict benign`).
Both verified byte-exact at HEAD this session:

```
$ git grep -nE 'benign|malicious' -- corpus/README.md
corpus/README.md:90:| `2026-10-13-r2-jq-shadow-verdict` | `~/.local/bin/jq` = byte-identical upstream jq-1.8.2 release — benign | rea analyze + upstream sha256 match | 2026-10-13 |
corpus/README.md:160:| `2026-10-13-round-2` | 2 | r1 survives audit (1 erratum); catalog≠provider≠held; doctor aux-blind; 32MiB crash cap; MCP-session-scoped ev_ids; shadow-binary verdict benign |
$ awk -F'|' 'NR==90||NR==160 {print NR": cells="NF-2}' corpus/README.md
90: cells=4
160: cells=3
```

File identity: `corpus/README.md` 187 lines, sha256
`f6fb46d6be47c75723c98406a9fad480b43c5e7ae51379cd68b9fc95c99a3b35` (equals
round-1 C2's recorded hash — README unchanged since 2026-10-16).

## 3. The strongest scope objection (steelman), then the counter

### 3.1 Objection O1 — "an index is not a knowledge file"

- README calls itself an index (`corpus/README.md:1`:
  `# kaidoku-shokunin corpus — index`) and states row-derivativeness at `:9`:
  "A row is written when its file exists, never before." Its rows are
  *summaries of files that exist*; the knowledge files are the claims.
- The r3/r2 qualification precedent was applied to **knowledge files**
  (`corpus/knowledge/2026-10-13-r3-jq-provenance.md:141`,
  `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:244`). Neither note
  names any README row (`sed -n '244p' … | grep -c 'README'` → `0`, this
  session) — the precedent's own scope was file-local.
- The coverage-map instrument that *does* read README (command A) reads only
  the `## Coverage map` slice (`SCORECARD.md:101`); both loci sit outside it —
  my slice check on `git show HEAD:corpus/README.md` returns
  `benign-in-cov: False | verdict-benign-in-cov: False`; the slice's last
  nonblank line is the l8-01 map row. V6 independently measured the same
  (`.ufo/waves/arc2-loop1-round2/V6.md:39`: ":90 and :160 are past map slice
  end (:69)").
- Conclusion of O1: the repo's only automated content reader never treats
  `:90`/`:160` as claims; qualifying them could be index-hygiene scope creep.

### 3.2 Counter — CR5's partition already answered the genre question, and the record classifies them as debt, not exclusion

- **The partition precedent.** Round 1's critic listed, under the heading
  **"Editable — census targets"**:
  "`corpus/README.md` — editable index, **repair precedent exists** (7125dd4,
  3395b6d, 18dc397); carries the two unowned labels at `:90`,`:160`"
  (`.ufo/waves/arc2-loop1-round1/CR5.md:300-305`). The genre distinction O1
  relies on was on the table and was *not* used to exclude; CR5's frozen-scope
  list (§:309-320) excludes only `LOG.md` entries, `SCORECARD.md:79`, prior
  `.ufo/` artifacts and `evidence/` — not README.
- **The record's own scope sentence.** The round-1 landing recorded: "Census
  scope … scoped to safety-sense artifact-verdict loci in **editable corpus
  files** … The fleet token census also matches `corpus/README.md:90,:160`
  (unqualified safety-sense labels on the same jq verdict — **deferred with
  cause**)" (`LOG.md:993-998`; also `SCORECARD.md:680`). The sentence's only
  exclusion is `LOG.md` ("frozen historical entry — not editable"). README is
  an editable corpus file; "deferred" is sequencing, not a scope carve-out.
- **The carried-debt ledger lists them as obligations.**
  `LOG.md:1008-1010` and `SCORECARD.md:696-700`: "Carried debt (named, not
  landed): `corpus/README.md:90,:160` label qualification (deferred with
  cause)". A debt entry is the queue, not the exclusion list — C2 is that
  item's discharge round.
- **Empirical necessity for `:160`.** Its apparent referent, the round-2
  lessons file, carries **no safety token at all**:
  `grep -nEi 'benign|malicious|trustworthy|safe|trust|compromis|legit|harmless|endorse|safety' corpus/lessons/2026-10-13-round-2.md` → rc=1 over
  all 75 lines (file sha256 `2296667f06213c244a60ef81fbd82f85456ba81e405d8e61ff2e46a01dcbf12f`).
  So "fix the source instead" is impossible for `:160` — the index cell is the
  sole current carrier of that label. For `:90` the source is qualified at
  `:244`, but `:244` does not name README (§3.1), so the index reader sees no
  path to the qualification either.
- **A machine instrument already treats README row text as content.**
  `.ufo/waves/luna-round-5/receipts/census-pre.sh:26-27` reads the README
  frontier section and the r13 row and returns `README PASS/DEBT` from their
  *text* (`.ufo/waves/luna-round-5/receipts/census-pre.out:4` → `README DEBT`).
  O1's premise ("no instrument treats README rows as content") is contradicted
  by a landed census.
- **The refusal makes the labels wrong wherever they sit.** `PROVINCE.md:114-116`
  refuses safety/trust verdicts outright; `PROVINCE.md:100-102` refuses even the
  label vocabulary ("does not … label samples malicious/benign"). A present-tense
  "benign" in an editable file — index or not — is the bleed class C2 exists to
  close. The index is the entry point; the qualification must be visible there.

**O1 verdict: refuted. The genre split is real (form consequences in §4) but
does not remove the loci from scope; the record adjudicated them in-scope and
deferred, and CR5's partition stands as the precedent the round claim cites.**

## 4. Form finding — in-cell, not appended (measured)

### 4.1 Both loci drift with every mid-file row insertion

Measured this session (`git show <c>:corpus/README.md | grep -n …`):

| revision | knowledge-row (`:90` at HEAD) | lessons-row (`:160` at HEAD) | README lines |
|---|---|---|---|
| `6645585` (baseline) | 80 | 143 | 167 |
| `c265db9` | 80 | 143 | 168 |
| `6a71cd5` (luna-4) | 83 | 146 | 173 |
| `7125dd4` (luna-5) | 83 | 146 | 173 |
| `3395b6d` (luna-7) | 89 | 158 | 185 |
| `18dc397` (luna-8) | 90 | 160 | 187 |
| `165057e` (HEAD) | 90 | 160 | 187 |

An appended EOF note that cites `:90`/`:160` (the round claim's "form of the r3
erratum") is therefore a *dated* pointer: it was accurate only from `18dc397`
on, and the next luna-round-7-style row insertion (12 rows landed mid-file)
stales it — the precise mechanism that produced `SCORECARD.md:68`'s drift
(`:157`→`:160` "correction" was itself written against a bullet that had
already moved to `:163`; `cfc84c2` vs `6a71cd5` — re-verified this session).
The in-cell form has no line citation to drift: the qualifier travels inside
the cell it qualifies.

### 4.2 Citation-shape inconsistency among the drafters (parent must pick one)

- `E9.md:140,144` (round-2): `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:244`
  — repo-root-prefixed.
- `S1.md:269-283`: `knowledge/2026-10-13-r2-jq-shadow-verdict.md:244` — missing
  the `corpus/` prefix.
- `C2.md:230-231` (round-2): bare `2026-10-13-r2-jq-shadow-verdict.md:244` +
  `PROVINCE.md:114-116`.
- `E17.md:147` conflates forms: "qualified in place, r3-erratum form,
  index-appropriate" — "in place" is the in-cell form; "r3-erratum form" is
  the appended form. They are different landings.

Recommendation: E9's prefixed form (resolvable from repo root; matches the
citation convention command A resolves). Whichever is chosen, one form must be
landed, not a blend.

### 4.3 Dry-run (scratch `/tmp/arc2-l2r2-CR2-scope/`, repo untouched)

Variants built from a byte-copy of the worktree README (base sha256
`f6fb46d6…` = worktree, `cmp`-verified):

| variant | form | lines | cells :90/:160 | tokens (`benign|malicious`) | marker count |
|---|---|---|---|---|---|
| base | — | 187 | 4 / 3 | 2 | 0 |
| A | E9 in-cell (prefixed cite) | 187 | 4 / 3 | 2 | 0 |
| B | appended `**Safety-label scope …**` note | 189 | 4 / 3 | 3 (note's own line) | 1 |
| C | C2.md §6(a) exact strings | 187 | 4 / 3 | 2 | 0 |
| D | = A (recommended; also the exact text in §6 below) | 187 | 4 / 3 | 2 | 0 |

`B` prefix-identity: `head -c 43022 variantB.md | cmp - base.md` →
PREFIX-IDENTICAL. No trailing whitespace on edited rows (`grep -oE '[ \t]+$'`
→ rc=1); pipe counts preserved (9 `|` chars across the two rows). E9's
re-census caveat confirmed: token count stays **2** after either form — the
measurable is a text property, not a token-count change (`E9.md:147`).

## 5. Instrument findings (the parent must not ship the E19 assert as-is)

### 5.1 The skeleton's marker assert is form-dependent

`E19.md:276-284` (bullet at :276-284; marker assert at `:280-281`) drafts the
round's C2 after-measurement as: "both named by the appended
`**Safety-label scope` note … Marker assert:
`grep -c '\*\*Safety-label scope' corpus/README.md` → 0 before, 1 after."
Measured against my dry-runs: in-cell variants A/C/D → marker count **0**;
appended variant B → **1**. If the parent lands the in-cell form that
E9/E17/S1/C2 recommend, the round's own after-measurement returns 0 and the
C2 acceptance fails by construction — the same defect class as CR5's round-1
instrument findings (`.ufo/waves/arc2-loop1-round1/CR5.md:171-204`). The assert
must be form-matched (§6).

### 5.2 "Drifted pointer 1 → 0" undercounts — the drift is DOUBLE

`SCORECARD.md:68-71` (read verbatim this session) names two README targets,
both drifted at HEAD:

- `:160` → the frontier bullet actually at `corpus/README.md:177` (CR5's
  finding; re-verified: `grep -n 'Runtime-obs' corpus/README.md` → `177:`).
- `:128` → the r13-distillation row actually at `corpus/README.md:138`
  (`grep -n 'round-13-distillation' corpus/README.md` → `138:`; at baseline
  `6645585` it *was* `:128`, so that pointer was baseline-correct).
- Both described content debts were discharged at `7125dd4` (hunks
  `@@ -128,7 +128,7 @@` and `@@ -160,7 +160,7 @@`; re-verified from the commit
  diff). E9.md:3 found the second drift; C2.md:26-29 (round-2) confirms it.
  E17.md:147 already drafts the verdict cell as "drifted pointers 2 → 0" —
  the round claim's "1 → 0" contradicts its own drafting seats. Repairing only
  `:160` leaves `:128` drifted inside the repaired bullet.

## 6. Text for the parent to land VERBATIM (fenced)

**(a) The two README rows — in-cell form (variant D; dry-run verified: 187
lines, cells 4/3, no trailing whitespace, tokens stay 2).** Replace the exact
current rows (byte-exact `old_string` material in §2) with:

```text
| `2026-10-13-r2-jq-shadow-verdict` | `~/.local/bin/jq` = byte-identical upstream jq-1.8.2 release — benign (historical wording, not a present safety/trust verdict; scope note `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:244`) | rea analyze + upstream sha256 match | 2026-10-13 |

| `2026-10-13-round-2` | 2 | r1 survives audit (1 erratum); catalog≠provider≠held; doctor aux-blind; 32MiB crash cap; MCP-session-scoped ev_ids; shadow-binary verdict benign (historical wording, not a present safety/trust verdict; scope note `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:244`) |
```

**(b) Form-matched after-measurement — replaces the marker assert at
`E19.md:280-281`** (the marker assert only passes on the appended form):

```text
C2 after-measurement (in-cell form): sed -n '90p;160p' corpus/README.md | grep -c 'historical wording'   # 0 before → 2 after
Token counts are a text property and do NOT change: git grep -ciE 'benign|malicious' -- corpus/README.md  # 2 → 2 (both historical rows retained; do not phrase as "benign count 2→0")
```

**(c) `SCORECARD.md:68-71` repair — two drifted pointers, both debts
discharged (facts re-verified by this seat; text follows C2.md §6(b) with the
`:138` pointer included).** Candidate:

```text
- **Other stale summaries:** discharged by luna-round-5 (`7125dd4`): the frontier
  bullet now reads "held, not frontier" (`corpus/README.md:177`) and the r13 row
  now reads "4 nits: 2 fixes applied at integration…" (`corpus/README.md:138`).
  Both named content debts are closed; this bullet is kept as a record, not a live
  gap. (Prior pointers `:157`→`:160` and `:128` were line-drifted by README growth
  and the `7125dd4` repairs.)
```

If the parent instead lands the appended-note form (C2.md §6(a) alternative),
then (a) is replaced by that note and (b)'s assert becomes the marker assert —
but the note then carries `:90`/`:160` citations with the §4.1 drift exposure,
and should be dated like the r3 erratum. **Recommendation stands: in-cell (a) +
(b), not appended.**

## 7. Conclusions, labeled

**Observations** (ran/read this session): both loci byte-exact at HEAD and
their cell structure (4/3 cells; §2); README sha256 `f6fb46d6…` and 187 lines;
the seven-revision drift table (§4.1); `SCORECARD.md:68`'s two drifted pointers
and both discharges at `7125dd4` (§5.2); CR5's partition text placing README in
"Editable — census targets" with the two labels named (CR5.md:300-305, :352-357);
the round-1 scope sentence and carried-debt entries (LOG.md:993-998, :1008-1010;
SCORECARD.md:680, :696-700); `:244` does not name README (grep → 0); the
round-2 lessons file's zero safety tokens (75 lines, rc=1); the landed census
instrument reading README row text (luna-round-5 `census-pre.sh:26-27`);
E19's marker assert and its form dependence (§5.1, measured against dry-runs);
the five-variant dry-run table with prefix identity and pipe/whitespace checks
(§4.3); `pgrep` → no REA process of this seat's.

**Inferences:** (1) the scope objection fails on the record — the loci were
adjudicated in-scope by CR5's partition, recorded as deferred debt, and the
"fix the source" alternative is impossible for `:160` (no token in the referent)
and unlinked for `:90` (`:244` names no README row). (2) The in-cell form is
the correct index-appropriate analogue of the r3 erratum because the erratum's
mechanism (an appended note naming loci by line) is the one mechanism README
provably breaks (§4.1). (3) If the parent lands in-cell text but keeps E19's
marker assert, the round records a false C2 failure; the assert must be
form-matched (§6b). (4) The "1 → 0" measurable must read "2 → 0" or the
repaired bullet still contains a drifted pointer (§5.2).

**Unknowns:** (a) which form the parent lands — the in-cell and appended
options are both evidenced; I recommend in-cell; (b) whether the parent also
repairs the `:128` pointer or adjudicates it separately; (c) whether the
`PROVINCE.md:114-116` refusal citation belongs inside the row (E9's variant
carries it; C2.md §6(a) line-160 string omits it) — wording adjudication, not a
measurement; (d) whether `SCORECARD.md:68`'s bullet is inside the frozen
2026-10-15 section for edit purposes — round-1 adjudicated only `:79` as
frozen (`LOG.md:884`; `SCORECARD.md:672-676`); `:68` sits in `## Open gaps`
(:51-84), which the same record distinguishes from the frozen table (:39-49).

## 8. Reproduction commands (all read-only; scratch under `/tmp/arc2-l2r2-CR2-scope/`)

```bash
git rev-parse HEAD; git status --porcelain
git grep -nE 'benign|malicious' -- corpus/README.md
awk -F'|' 'NR==90||NR==160 {print NR": cells="NF-2}' corpus/README.md
for c in 6645585873c4e66372b15687c47000abf8d91978 c265db9 6a71cd5 7125dd4 3395b6d 18dc397 165057e; do printf '%s: ' $c; printf 'know=%s ' "$(git show $c:corpus/README.md | grep -n 'r2-jq-shadow-verdict' | tail -1 | cut -d: -f1)"; printf 'lessons=%s\n' "$(git show $c:corpus/README.md | grep -n '| .2026-10-13-round-2. |' | cut -d: -f1)"; done
sed -n '68,71p' SCORECARD.md; sed -n '177p;138p' corpus/README.md
sed -n '300,305p;352,357p' .ufo/waves/arc2-loop1-round1/CR5.md
sed -n '993,998p;1008,1010p' LOG.md; sed -n '680p;696,700p' SCORECARD.md
sed -n '244p' corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md | grep -c 'README'
grep -nEi 'benign|malicious|trustworthy|safe|trust|compromis|legit|harmless|endorse|safety' corpus/lessons/2026-10-13-round-2.md; echo rc=$?
sed -n '26,27p' .ufo/waves/luna-round-5/receipts/census-pre.sh
sed -n '278,284p' .ufo/waves/arc2-loop1-round2/E19.md
# dry-run (scratch only):
mkdir -p /tmp/arc2-l2r2-CR2-scope && cp corpus/README.md /tmp/arc2-l2r2-CR2-scope/base.md
#   variants A-D built per §4.3; checks: wc -l, awk cell count, grep -c tokens, marker count, cmp prefix
```
