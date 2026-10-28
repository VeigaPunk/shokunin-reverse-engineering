# ScribeScore — `## Round 48` SCORECARD draft (before landing)

Draft for the L1. Every measured number below is backed by a receipt named beside it
(committed controls or this seat's own receipts under
`.ufo/waves/round-48/w1/ScribeScore/receipts/`). Every unmeasurable "after" cell is
marked pending with a fill instruction — no after number exists yet, and none is
claimed. The prompt's declared freeze `dc73587a` is superseded: the claims file
(amendment A4) names `0f06251b` as the declared freeze; all A4 numbers are this seat's
own runs at `2026-10-28T18:53Z`, worktree `663f30ee`.

## `## Round 48 — verdict maps bound to meanings over the 42-instrument census; the record re-derived with a completeness floor`

Base `61b87d742032e65fca9c38267d7d6ed7e555edad`. The freeze is a disclosed series of five
commits, all before any claim verdict: `7fe11332` (plan + both counters + census), `dc73587a`
(A1: the axis-score clause read the evidence cell — vacuous green over zero rows), `ac02a79f`
(A2: the exit-0 classifier rejected a legitimate success meaning on the word `failing`),
`f3a7afc4` (A3: the census clause compared a derived object with a committed list — a clause
that could never be true, unreachable only while block 25 is absent), `0f06251b` (A4: the
exit-0 classifier accepted a negated meaning — `0=not met` scored success — and the row
parser skipped an indented row; two selftest cases added, `red-opposite-polarity`,
`red-hidden-row`). **The declared freeze is A4 `0f06251bf6a3a6964c715f67243d4df12e854258`**;
the wave dispatch named A1 `dc73587a` (the seat brief), and A2–A4 were declared while wave 1
measured — each is a defect the round found in its own instrument before any landing, all
disclosed rather than folded, per the round-46 M46-3 finding. Frozen-path integrity:
`git log --name-status --format=%H 0f06251b..HEAD -- tools/round-48 plans/round-48-claims.md`
is empty at `663f30ee` (the two commits after A4 touch only `.ufo` wave evidence).
Waves: 75 + 0 = 75 seats. Measurements `<FILL: landing short sha>`.

| claim | axis / surface | before | after | counting command | measured at |
|---|---|---|---|---|---|
| R48-C1 | depth — craft rule block 25 (marker `<!-- verdict-meaning-table v1 -->`, exactly two rows keyed `{R46-CL7: meaning, R47-CL10: floor}`, name+body `mutations_sha256`, `interpreter_sha256`, ≥5 line-selected citations incl. a `corpus/knowledge/` entry) and the `<!-- instrument-registry v2 -->` section re-bound to `tools/round-48/census2.json` (42 paths) by meaning class | at the A1 freeze exit 1: `marker_occurrences 0`, `block_present 0`, `rule_blocks 24`, battery skipped (`.ufo/waves/round-48/controls/ctl-c1-0-do-nothing.json`); at A4 exit 1, identical fields (this seat: `receipts/c1-v3-at-A4.stdout`, sha256 `9c5048d2…`, exit 1, 2026-10-28T18:53:53Z); census derivation: 42 paths at `dc73587a` vs 40 registry rows — `tools/round-48/meanings.py` + `record2.py` missing, none extra/duplicate (`w1/C1Census`, stdout sha256 `af2ff190…`); v2 profile on the absent block also exits 1 (`receipts/c1-v2-at-A4.stdout`) | `<FILL — pending landing + re-measure>` | `python3 -I -B tools/round-48/meanings.py --root . --freeze 0f06251b --rev <REV> --profile v3` | `<FILL: landing rev>` |
| R48-C2 | calibration — `tools/round-48/record2.py`: round-47 oracle executed from `--rev` bytes, completeness floor over the last two round sections, every `## Record corrections — round 48` line re-derived (incl. `axes`, `quote`), quoted numbers bound to cited receipts, Owned-axes score cells bound to fractions, 5-forgery battery | at A1 exit 1: oracle green (`met_target true`, `mismatches []`, per `.ufo/waves/round-48/l1/scores/probe-record47.json`), floor failing `round-47: no seat atom and no re-derived seats correction`, `no \`## Record corrections — round 48\` line re-derived`, `quoted numbers with no backing receipt: 1` — the round-47 `exempted` count vs its cited receipts (`.ufo/waves/round-48/controls/ctl-c2-0-do-nothing.json`; A4 identical: `receipts/c2-v3-at-A4.stdout`, sha256 `1055fb82…`, exit 1); `--profile v2` exits 0 — the hole being closed (`.ufo/waves/round-48/controls/ctl-c2-1-v2-profile.json`; A4: `receipts/c2-v2-at-A4.stdout`, exit 0) | `<FILL — pending landing + re-measure>` | `python3 -I -B tools/round-48/record2.py --root . --freeze 0f06251b --rev <REV> --profile v3` | `<FILL: landing rev>` |

Owned scores: coverage `10 → 10` (`git ls-tree -r --name-only <rev> corpus/knowledge |
grep -c '\.md$'` → 138 at `0f06251b`; this round adds no domain surface — no knowledge
entry, no coverage-map row, `git log --name-status 61b87d74..0f06251b -- corpus/knowledge
PROVINCE.md` empty); depth `10 → 10` (rule blocks `24 → 25` with
`citation_resolved_rules` `<FILL>` — the move is the meaning binding and its forgeries,
not a number above the ceiling); calibration `10 → 10` (the record's self-assessment now
re-derives `<FILL: atom count>` atoms with floor + quote + axes bindings; the numeric
axis cannot rise above 10).

Learning trends: expansion **unchanged** (no admitted knowledge entry, no coverage-map
row, no PROVINCE move; the corpus/PROVINCE window over `61b87d74..0f06251b` is empty);
quality **improved on the instruments** (two new counters each score their own battery —
4 forgeries for the meaning counter, 5 for the record counter — and the meaning counter's
selftest scores 18 cases 0 failures at A4 (`receipts/c1-selftest-A4.stdout`, exit 0; the
record selftest exercises parsers only, `receipts/c2-selftest.stdout`, exit 0); the bound
is measure quality, not domain ground); discernment **improved** (four of the round's own
defects were found before the operator, all by measuring the instrument before landing:
A1 a vacuous clause scoring zero rows green, A2 a false-red on legitimate prose, A3 a
clause that could never be true, A4 a false-green on a negated meaning plus a skipped
indented row — the bound is that all four are instrument-level, and the round's own
record enters this landing already wrong twice: round 47 has no seat atom and quotes an
`exempted` cell its own receipt does not back).

**Routed to round 49.** `R46-CL1`, `R46-CL5`, `R46-CL8` stay open (the merge-squash tamper
arm, the registry `purpose` cell, the claims-file `--selftest` grammar). New from this
round: (a) the freeze definition itself was ambiguous this round — "first commit
containing the claims file + `tools/round-48/`" is not the same answer as "commit
carrying the amendment paragraph", and a four-commit amendment series left the dispatch
naming A1 while A4 was operative (`w1/CritClaims.md`); (b) the battery clause is
unobservable until a landing exists — both counters skip the battery when any structural
clause fails, so the kill rule cannot be red-beforeed pre-landing (`w1/C2Battery.md`);
(c) the record's seat grammar accepts only `Waves: A + B = C` or `Wave 1: A; wave 2: B`
atoms, so a one-wave round can only satisfy the floor through a `seats` correction, not
prose (`record.py` `SEATS_SUM`/`SEATS_PAIR`, this seat's re-derivation); (d) the meaning
classifier is a substring vocabulary, not an exact binding — A4 closed the negation
false-green but the accepted language is still a token match (`w1/C1Gold.md`);
(e) `.ufo/waves/round-48/` was untracked at the freeze tip — `path` atoms, the seats
correction's dispatch file and `receipts_at` all require wave evidence committed before
the measured revision (this seat; `git ls-tree 0f06251b .ufo/waves/round-48/` empty).
**planned (round 49):** calibration or depth from the routed list — pin down (a) with a
joint-pathspec freeze derivation; second choice coverage via the open R44-CL2-style
promotion. **retired:** none. Coverage, depth and calibration stay tied at 10; the last
capability entered in round 43.

---

## Appendix — verified landing inputs (scratch checks at `0f06251b`, 2026-10-28)

The following are re-derivations this seat ran against the real code paths
(`record2._quote_correction`, oracle `corrects()`); they are not a counter pass.

**`## Record corrections — round 48` (both lines verified to re-derive):**

- `corrects seats round-47: 1 wave, 75 seats total` — oracle `corrects()` →
  `(True, derived [1,75], dispatch [75])`; `.ufo/waves/round-47/w1-dispatch.json`
  `counts.spawn` = 75 at `0f06251b`.
- `corrects quote round-47: exempted 1` — `_quote_correction()` → True; the round-47
  section quotes a count of two, cited receipts `…/c1-at-A7.json`, `…/c2-at-A7.json`,
  and the round-47 c2 receipt's `exempted` list has length one.

**Grammar hazards verified for the `## Round 48` section text (each checked against the
oracle's own regexes):**

- Seat atom: only `Waves: 75 + 0 = 75 seats.` derives (SEATS_SUM); `Wave 1: 75 seats`
  matches neither SEATS_SUM nor SEATS_PAIR. If a wave-2 dispatch is added the atom must
  become `75 + <w2> = <total>` — re-derive `counts.spawn` at the measured revision.
- QUOTE keys are `atoms|exempted|corrections|mismatches N`: any such `key + digit`
  string inside the section must equal a top-level cell of a receipt the section cites
  (`quote_value` reads top-level only — nested `oracle.atoms` does not count) or a
  `quote` correction keyed to that round. Numbers describing an unbacked value (e.g.
  the round-47 exempted quote) must be written without the digit, as above.
- Claim ids: `R48-C1`, `R48-C2` exactly, and **no `R47-C\d`/`R46-C\d` literal** in the
  section (claim ids are unique across the last two sections; `R4\d-CL\d` routed ids
  are a different class and safe).
- Revs must be backticked 7–40-hex, each `rev-parse`-able and an ancestor of the
  measured rev (`61b87d74`, `7fe11332`, `dc73587a`, `ac02a79f`, `f3a7afc4`,
  `0f06251b`, `663f30ee` all verify at report time); sha256 digests are 64-hex and
  never match.
- `path` atoms: every `.ufo/waves/round-N/…` token must exist at the measured
  revision — this draft cites `controls/`, `w1/C1Census`, `w1/C1Gold.md`,
  `w1/C2Battery.md`, `w1/CritClaims.md`, `receipts/` and `l1/scores/` paths that are
  untracked today and must be committed before the measured revision.

**Fill list for the L1:** landing rev; both counters' after receipts
(`.ufo/waves/round-48/l1/scores/c1-at-<REV>.json`, `c2-at-<REV>.json` by round-47
convention); `atoms`/`mismatches`/`corrections`/`exempted` after-values; block-25
`refs`/`unresolved_citations`; `citation_resolved_rules 25`; commit the wave evidence
tree (incl. `w1-dispatch.json`, controls, seat receipts, `l1/scores/`) before the
measured revision; the claims file names `ctl-c1-1-v2-profile.json` as a committed
control that does not exist on disk (a port of the v2 semantics on a genuine block is
not possible until landing; produce it or correct the controls list).
