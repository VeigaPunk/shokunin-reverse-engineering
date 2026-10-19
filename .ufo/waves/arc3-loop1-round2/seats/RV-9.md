# SEAT RV-9 | CHAIN c2 | ROLE reviewer — ordinary-run verdict identity (both runs at my own hand)

Wave `arc3-loop1-round2`, 2026-10-19. Repo HEAD `14b1682b…` (no seat commits). My
seat task: *verify the ordinary-run verdict is byte-identical to the pre-edit verdict
except header/version lines; run both yourself.*

**VERDICT: REFUTED AS WORDED, SEMANTICS PRESERVED.** The ordinary verdict at the
landed revision differs from the pre-edit verdict in exactly **4 lines, none of them a
header/version line** (1 removed, 3 added). Every other line — live anchors, the three
`lines=/loci=` counters, all seven class buckets and their contents, `SCOPE-ERRORS`,
`G7`, `G11`, the `VERDICT` line — is byte-identical, and the run is still
`VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0. The exemption
clause is *inert* for the ordinary run: the verdict carries no version banner at all,
so no output line can be exempted (see attack A1).

Judgement for the parent: the frozen clause "ordinary runs at HEAD stay PASS 0/0/0/0"
holds; the round-2 seat-line phrasing ("byte-identical … except header/version lines")
does not, because the new declared-class instrumentation is necessarily *printed*.
If zero output churn is a requirement, the three added lines must be conditionally
emitted (only when non-empty) and the G2 line left untouched — that is a design
decision for the parent/EX-16, not something this reviewer may write.

## Revision timeline (measured; the instrument was revised 9× inside my window)

| UTC | sha256 (first 12) | lines | ordinary run |
|---|---|---|---|
| 12:01:54 | `6f1d19ff` (pre-edit, HEAD blob) | 490 | PASS, exit 0 |
| 12:05:36 | `1431620f` | — | first landing |
| 12:05:57 | `2a89793a` | 550 | — |
| 12:06:42 | `59975ae0` | 557 | — |
| 12:07:27 | `82fb807e` | 560 | PASS (tree-level floor) |
| 12:11:01 | `c95a5cf3` | — | **FAIL exit 1** (per-block per-file floor, SKILL.md=0) |
| 12:12:31 | `df9ffdf9` | 601 | PASS (floor → per-file current-ok detections) |
| 12:15:39 | `a4c16763` | 603 | PASS, stdout sha `1db2ec31…` |
| 12:18:18 | **`d0772ce8` (final, EX-16's seat report)** | 610 | PASS, stdout sha `1db2ec31…` |

Last instrument check by me: **12:22Z, sha256 `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`,
610 lines, size 31906 B, mtime 2026-10-19 09:18:14 -0300**. The parent records the fresh
identity at landing (rule-#14 discipline); if any later revision lands, my captures below
apply to `d0772ce8` only and the audit should be re-run with
`bash .ufo/waves/arc3-loop1-round2/claims/c2/RV-9/reverify.sh` (self-contained; re-pins the
live sha, compares it to the pinned artifact, re-runs the identity audit, the creep audit
and the four decisive fixtures — tested end-to-end, output in `/var/tmp/rv9-reverify/`).
Note the bytes can be rewritten without a content change: at 12:15:39Z the same path held
`a4c16763` (31364 B), and `d0772ce8` carries mtime 09:18:14 -0300 — content identity is the
pin, mtime is not (C3's v2 custody instrument is what makes that visible).

## 1. Work performed (evidence pointers)

All artifacts under `claims/c2/RV-9/` unless stated; scratch under `/var/tmp/rv9-round2`.

- **Pre-edit baseline, captured before any EX-16 write** (12:01Z):
  `pre-edit.out` (4405 B, sha256 `d3da7509…`, 91 lines, exit 0) from
  `python3 .ufo/gates/c1-census-v10.py` on the pre-edit bytes
  `c1-census-pre-edit.py` = `6f1d19ff…` / 490 lines. Determinism: an independent re-run
  of the frozen copy reproduced `d3da7509…` byte-for-byte (`copy-run.out`).
- **Tree-identity pairing** so a verdict change is attributable to the instrument, not
  the tree: `tree-identity-T0.txt` = `tree-identity-T1.txt` (PROVINCE.md `d075a3c6…`,
  SKILL.md `483b0eba…`, SCORECARD.md `a7c72950…`, and the three live configs
  `16f496e6…` / `38d2a1d0…` / `8cbacd48…` unchanged); `git status --porcelain` shows
  the three scoped files clean at both ends.
- **Post-edit capture, sha-pinned** (`run-post.sh` hashes the instrument before and
  after the run and rejects a race): `post-edit.out` (4568 B, sha256 `1db2ec31…`,
  93 lines, exit 0) at `d0772ce8…`; `post-edit.json`; `verdict-timeline.txt`.
- **Corroboration**: EX-16's own receipt
  `claims/c2/EX-16/receipts/after/ordinary-at-head.txt` (sha256 `c93f6b6a…`, incl. its
  trailing `exit=0` line) is byte-identical to `post-edit.out` after stripping that one
  line — two independent captures, one digest.
- **Diff classifier**: `verdict-identity.py` (per-line header/version whitelist H1/H2/H3,
  plus an order-preserving substantive-residue check), self-tested on two identical runs.
- **Fixtures run by me** on `/var/tmp` copies (`fixtures.py`, outputs `fx-*.out`):
  absent-file, needle-blind, per-file collapse, inline-marker, DATED-shelter.
- **Creep audit**: round-1 tool
  `.ufo/waves/arc3-loop1-round1/claims/c3/CR-5/tools/scope-diff.py` on
  pre vs post → `rows before=20 after=20`, ADDED/REMOVED/CHANGED 0, `CREEP FLAGS: []`,
  exit 0 (my own run of the tool, not EX-16's receipt).

## 2. Proposed changes

`claims/c2/RV-9/proposed-cosmetic-fixes.patch.md` — patch TEXT only, two cosmetic
hunks anchored on `d0772ce8`: (F1) delete the duplicated 3-line docstring paragraph
at `:82-84`/`:85-87` (measured identical); (F2) fix the unit label in the G2 report
line, where the per-file numbers are current-ok *detections* (17/14/3, sum 34) while
the same line's `total loci=17` counts *loci* (6/9/2) — two units under one word.
No semantic patch proposed; none of the fail-closure logic needs a change from this seat.

## 3. Before→after measurement for my chain's claim (commands + outputs)

Instrument pinning: `$ sha256sum .ufo/gates/c1-census-v10.py` → `6f1d19ff…` (pre) /
`d0772ce8…` (post), each verified unchanged across its own run.

**C2 clause 1 — "ordinary runs at HEAD stay PASS 0/0/0/0":** holds.
```
pre : exit=0  VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)  91 lines, sha d3da7509…
post: exit=0  VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)  93 lines, sha 1db2ec31…
```

**Seat task — byte identity:** `python3 verdict-identity.py pre-edit.out post-edit.out`
```
pre lines=91 post lines=93
EXEMPT (header/version) changed lines: 0
SUBSTANTIVE changed lines: 4
  -SUBSTANTIVE   'G2 positive-assertion guard: ok'
  +SUBSTANTIVE   'UNREADABLE (could-not-evaluate): []'
  +SUBSTANTIVE   'G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)'
  +SUBSTANTIVE   'DECLARED FAIL CLASSES: []'
substantive residue identical (order-preserving): False
AUDIT: DIFFERS-SUBSTANTIVELY        (audit-exit=1)
```
The 4 lines are additive declared-class instrumentation plus the extended G2 line; all
values are empty on the ordinary run (`[]`, `ok`). `--json` gains 4 additive keys
(`unreadable`, `declared_fail_classes`, `current_ok_per_file`, `g2_floor`); no key
removed or changed value.

**C2 clause 2 — declared FAIL classes (my fixtures at `d0772ce8`):**

| fixture | pre-edit | post-edit (`d0772ce8`) |
|---|---|---|
| control, three files intact | PASS exit 0 | PASS exit 0 |
| SKILL.md absent (H1) | **PASS exit 0** (silent) | **FAIL exit 1**, `UNREADABLE ['SKILL.md: FileNotFoundError']` |
| PROVINCE.md absent (H1 control) | FAIL exit 1 | FAIL exit 1, `UNREADABLE ['PROVINCE.md: …']` |
| all needles neutered (H3) | **PASS exit 0**, `loci=0`, `G2 … ok` | **FAIL exit 1**, `DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']` |
| SKILL.md → 371 needle-free filler lines (my own) | n/a | **FAIL exit 1**, `BLIND-INSTRUMENT` (`SKILL.md=0`, other files loud) |

Pre-edit latents re-measured at my own hand: `pre-absent-skill.out` (PASS exit 0) and
`pre-blind.out` (`loci=0`, `G2 … ok`, PASS exit 0).

**C2 clause 3 — "every round-1 silent-PASS injection now reproduces as a declared FAIL":**
true for the two holes the claim itself names (H1/H3, row 2 and row 4 above), **false as
worded**. Two round-1 injections still read PASS at the landed revision, each also named
as not-closed in EX-16's own header and seat report: H2 inline-marker excusal
(`PROVINCE.md:44` → `rea-agents@6.4.0  (historical)`: PASS, `fx-h2-marker.out`) and t5
DATED-shelter (`rea-agents@9.9.9` planted inside `SCORECARD.md`'s DATED range 273-326:
PASS, `fx-t5.out`, `fx-t5-d0772ce8.out`). The parent should record the scoped reading
(H1/H3 injection set) explicitly, or restate the clause.

**C2 clause 4 — scope bounds byte-stable:** holds; creep audit above, 0 flags, rows
20/20, and the ordinary-run locus counts unchanged (6/9/2).

**C2 clause 5 — H4 residual stays named + external diff audit as certificate:** the
residual is named in the instrument header and EX-16's report; the external certificate
(the `scope-diff.py` diff audit on the v11 diff) was run by me, clean.

## 4. Attacks / refutations attempted

| # | attack | result | verdict |
|---|---|---|---|
| A1 | Launder a substantive change as a "header/version line" | the ordinary verdict contains **no** version banner; my classifier exempted 0 of the 4 changed lines, and the residue check fails | strict claim **refuted**, cannot be excused by widening the exemption on this evidence |
| A2 | Per-file collapse the global floor would miss (SKILL.md blanked to needle-free filler, other files loud; total loci 15 > 0) | FAIL, `BLIND-INSTRUMENT`, exit 1 | landed floor is **strictly stronger** than CR-5's proposed global floor; no refutation |
| A3 | H3 partial blindness (PIN alone neutered) | PASS exit 0, all files' counts unchanged | residual reproduced; **named** by EX-16 (not claimed closed) |
| A4 | H2 inline-marker excusal (fabricated non-live pin + marker) | PASS exit 0 (count drops 17→16, still ≥1) | residual reproduced; **named**; refutes the broad clause-3 reading |
| A5 | t5 DATED-shelter (fabricated pin inside a DATED range) | PASS exit 0 | as A4 |
| A6 | Transient red gate: the `12:11:01` revision read FAIL exit 1 at plain HEAD (`floor=1/file` counted current-ok **blocks**; SKILL.md's block dispositions are `info`/`historical`) | observed by me for ~90 s, then fixed by EX-16 at `12:12:31` (metric → detections); EX-16's report records it as A5 | caught and closed by measurement; no lingering defect at `d0772ce8` |
| A7 | Identity laundering: a verifier claiming the final bytes while pinning interim revisions | EX-16's earlier receipts claimed `82fb807e` and their `landing-diff.md` names that intermediate sha; the receipts were refreshed at 12:16-12:18Z against `d0772ce8`, and the final report names the interim→final gap explicitly | gap closed by re-derivation; my capture independently confirms the final stdout digest equals the interim `1db2ec31…` |
| A8 | Self-certification (H4): trust the instrument's own clean run | external diff audit run by me (scope-diff 0 flags; counts unchanged) | certificate holds for this diff; residual stays named |
| A9 | Hygiene: `.ufo/gates/__pycache__/c1-census-v10.cpython-314.pyc` (mtime 09:16:31) | untracked; created by EX-16's module-import harness; my runs invoke the instrument as a script and create no cache | named for the parent; not touched (target is EX-16-only) |

## 5. Blockers

None for this seat. Three notes for the parent:

1. **Claim wording vs delivery** (clause 3) — see §3; needs an explicit scoped reading or
   a restatement, plus a decision on whether the ordinary-run output may gain the three
   declared-class lines (my reading: the frozen clause "PASS 0/0/0/0" is the operative
   one and it holds).
2. **Verifier identity-pin gap** — PL-2/EX-12/VZ-2/CR-2/CR-3 verified interim revisions
   (`82fb807e`/`df9ffdf9`); the final `d0772ce8` is verified by me and by EX-16's
   refreshed receipts. Doc-only steps were behaviour-neutral, measured (identical stdout
   digest `1db2ec31…` at `df9ffdf9`…`a4c16763`…`d0772ce8`; my `a4c16763` capture is the
   independent half of that claim).
3. **Post-final-check revision risk** — last instrument check 12:22Z = `d0772ce8…`;
   any later write invalidates the pins above and requires
   `bash .ufo/waves/arc3-loop1-round2/claims/c2/RV-9/reverify.sh` (re-pins the live sha
   and re-runs identity + creep + fixtures).
