# R36W2ConnCrossClaim — cross-claim pattern: the lane freezes counters over a weakened relation and controls only the absent case

Seat: `R36W2ConnCrossClaim` (connector, leaf, round 36 wave 2). Synthesis seat: no counter, predicate,
carrier, oracle, surface or receipt was executed, edited or re-frozen; every disagreement below is
reported with evidence; inference is marked `[INFERENCE]`.

Tree state while reporting: lane HEAD `6f2ba761bb5bcd6482d45523379376dcb6a386f6` (wave-1 results +
wave-2 dispatch commit). Landed claim revisions as assigned: C2 repairs `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be`,
C1 + assimilation `ffc813417d3bceeeb7b028b12ce0be8a5dc33d95`, integration tip `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930`;
freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0`; base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`.
All cited paths are lane-relative under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

## 0. Bottom line

Yes — there is one underlying design error the lane keeps repeating, and both round-36 counters fell
into it in different costumes:

> **A frozen counter is validated only against inputs that are absent, junk, deleted or wrongly
> substituted (true negatives), and never against an input that is self-consistent — one that passes
> every check the counter actually implements while violating the predicate's operative clause. The
> implemented check is therefore always a weakened projection of the stated predicate, and the kill
> rule, which fires only on the frozen controls, cannot fire on the shortcut class.**

For R36-C1 the self-consistent input is a fabricated `after.json` re-hashed with REA's own digest code
(wave-1 F1). For R36-C2 it is a duplicate-unit shadow row, a second contradictory statement, or a
same-basename decoy (wave-1 classes A1–A6). The last three rejected rounds are the same shape one level
up: r33's freeze maps vacuously CLEAN, r34's size/name-set replays scoring 12/12 and 8/8 on the green
surface, r35's substring matches (`S1060`, substring-anywhere PROVINCE checks, a fabricated census
receipt).

**QUALITY 77 and 78 do not already state the general rule.** They state the two instance-level fixes
this round (enumerate every surface occurrence; receipt integrity is not provenance), each scoped to
the claim shape just burned. The general freeze-time rule exists only in embryo: QUALITY #48's
"id-keyed shortcut controls" and #67's pre-freeze structure-blind replay, each scoped to one counter
family. R36 followed the letter of #48 — frozen controls scored before data, kill rules, 27 selftest
cases — and the error recurred anyway, because no row defines the missing control as *passes the
implemented check, violates the operative clause*.

## 1. The shared shape, evidence per round

In each row: the predicate's operative clause → the relation the frozen counter actually checks → the
post-freeze shortcut class that satisfies the check while violating the clause → the instance-patch
QUALITY row written afterwards.

### Round 33 (rejected; verifier spotcheck `corpus/lessons/round-33-verifier-spotcheck.md`)

- Operative clause: the freeze-integrity gate's CLEAN means "the claim's instruments are pinned and
  unchanged".
- Implemented check: "every pin listed in the instrument map matches" — over a map that may be empty
  or malformed.
- Shortcut class: 7 empty/malformed freeze-map variants score CLEAN (`corpus/lessons/round-33.md:57`,
  verbatim: "7 empty/malformed freeze-map variants are falsely CLEAN"). Vacuous truth: the check
  quantifies over the claimant-authored map, not over the claim.
- Instance patch: QUALITY #66 (`corpus/QUALITY.md:76`) — reject absent/empty/malformed maps.
  `[INFERENCE]` r33's headline rejection was "unprovable" (held builder), but the routed instrument
  limits are the same family, and QUALITY 66 was written from r34's recurrence of it.

### Round 34 (rejected; verifier spotcheck `corpus/lessons/round-34-verifier-spotcheck.md`)

- R34-C1: predicate claimed the frozen fixtures *force structural record traversal*; the counter
  checked fixture size and fixed name slices. A size/fixed-slice replay scores 12/12 on both
  schedules, exit 0, `documents_ok true`, with no ELF structure decoding
  (`corpus/lessons/round-34.md:18`, M34-4, citing `w1/CtlLabels-files/size-pristine.receipt.json`).
- R34-C2 (r34b): the replay gate's registered class set did not include the structure-blind class the
  freeze names; a SONAME name-set replay (`nameset.py`) reads no header, no record entry and no
  `name_off`, keys on the sorted name set, and scores 8/8 on the gate's own green counter at three
  seeds (`corpus/lessons/round-34.md:49`; M34-7 at `:57` — "the green surface keys on invariants it
  did not vary"). Registering the class flips the gate to REFUSED, i.e. the refusal mechanism worked
  and the *registration set was unfaithful to the class it names*.
- Instance patches: QUALITY #67 (`corpus/QUALITY.md:77`) — pre-freeze structure-blind replay, scoped
  to "finite ELF structural-decoding counters"; #69 (`:79`) — one replay class per keyable invariant,
  scoped to fixture transformations; #70 (`:80`) — registered class-set equality; #71–74 — gate/receipt
  hygiene. M34-4's own fix cell says: "QUALITY 48/50 rejected blind constants/labels/hashes but did
  not require an adaptive structure-blind replay" — the lane's own words for the repeated error.

### Round 35 (rejected; verifier spotcheck `corpus/lessons/round-35-verifier-spotcheck.md`)

- Operative clauses: D-3 "the r34b entry cites S106"; the C1 counter's PROVINCE/README checks name
  specific table placements; the census receipt is a frozen input whose hash pins it.
- Implemented checks: `re.search(r"(?m)^source\s*:.*S106", body)` — a substring, which `S1060`
  satisfies (`corpus/lessons/round-35.md:62`); PROVINCE/README "row" checks that are
  substring-anywhere (r35 spotcheck R35-C1 re-check; lesson M35-2 at `corpus/lessons/round-35.md:10`);
  D-1 accepted "a fabricated substring receipt `rows=106 EXIT=0 W04` without exact warning count or
  validating the frozen input hash".
- Instance patch: routed as R35-D3 ("new C2 attempt must be severable and token-exact") — the
  general rule was again not abstracted; r36's C2 predicate inherited the shape and wave-1 re-found
  it as classes A2/A3.

### Round 36 wave 1 (both counters green on the real landing *and* on shortcut classes)

**R36-C1** (`w1/R36CriticC1Shortcut.md`). Predicate operative clause: "the committed REA
extract-firmware **receipt run with sasquatch on PATH** publishes every regular file of the frozen
independent unsquashfs oracle … with no sasquatch extraction gap". Implemented checks (the critic's
§4 enumeration, verified against the frozen counter): subject digest equals `carriers.json` entry;
two literals (`operation == 'extract_firmware'`, `provider.id == 'unblob'`); `normalized_result.files`
covers the oracle with `fp == rel or fp.endswith('/'+rel)` (size, mime, `path`, `analysis_depth`,
`reported_sha256` all ignored); one gap object present/absent; stored `evidence_id` recomputes under
the caller-supplied package root. Every input to those checks is claimant-authored bytes. The
self-consistent shortcut class F1 fabricates `after.json` from the frozen oracle and recomputes the
id with ~25 lines of stdlib Python that reproduce REA's own 6.5.0 digest byte-for-byte → **exit 0,
`met_target: true`, `carriers_matched: 4`** (critic §3, with id-fidelity table against genuine
receipts). The frozen control nearest to the class, CTL-C1-2, kills only the stale-id variant
(`ctl-c1-2-forged-oracle-copy.json`, `after_evidence_id_ok false`); the critic's §6 notes the frozen
selftest passes 14/14 *while* F1 passes — "None of them is a self-consistent forgery — the one
variant the frozen control family does not cover." The kill rule's three named controls are all
absent/no-sasquatch/stale-id classes.

**R36-C2** (`w1/R36CriticC2Shortcut.md`). Predicate operative clause: "the SCORECARD `## Owned axes`
rows, the SCORECARD `## Capabilities` table rows and the SHONEN.md boxes **carry zero mismatches** …
every pointer unresolved at the base repaired by a resolving pointer to **the same document**." The
word *every* is operative. Implemented checks: units keyed by first cell / box title into a dict
(later duplicate overwrites the earlier — the earlier row is then neither count-checked nor
pointer-resolved); `re.search` validates the first matching statement per unit; the base-repair test
accepts any same-basename-suffix path; the pointer guard is a count `>= base_total`. Shortcut classes
A1–A6 all reach `met_target: true` while the base's false statements (`116/116`, `receipts-B/`,
`ScoutSkillPlacement.md`) remain in the scored files; A1 is a three-line append. The critic's method
section, verbatim: "**None of the 13 cases exercises any class below**, so the selftest certifies
the counter against a shortcut set that excludes all of them." The frozen controls CTL-C2-0..3 are
do-nothing / junk counts / delete pointers / substitute a *different-basename* document — all absent
or wrong classes; A4's same-basename decoys pass the substitution control's test by construction.

**The plan file itself forecloses the fix.** `plans/round-36-claims.md:6` freezes "a do-nothing
control is scored with each frozen counter before any claimed data exists" — the absent class. The
selftest case lists are the frozen record of the omission: `tools/round-36/c1-counter.py:310-328`
(green, do-nothing, after:=before, forged-oracle-copy *stale id*, before:=after, oracle/carriers
changed, label/placement mistakes) and `tools/round-36/c2-counter.py:284-298` (green, do-nothing,
junk count, count deleted, pointer deleted, substituted-by-other-document, box removed, off-by-one
ranges, new unresolved pointer, wrong counts). 27 cases, 27 true negatives, zero adversarial
positives. `[INFERENCE]` this is not a counter bug the lane can patch in place; the claims file says
the counter, predicate, carriers and oracle are never changed after the freeze — so the omission was
unrepairable the moment the freeze commit landed, and wave-1 found it anyway.

## 2. The one underlying design error

Stated once, covering all five rounds:

> **The lane freezes a counter whose implemented relation is systematically weaker than the
> predicate's stated relation — hash-of-claimant-authored-bytes instead of an observed run (r36-C1,
> r33 maps); first-match-per-key instead of every occurrence (r36-C2, r35 substring); a keyed
> projection instead of the whole surface (r36-C2); an invariant the replay preserves instead of the
> traversal claimed (r34) — and validates it only against inputs that are missing or wrong. Because
> every frozen control is a true negative, a green counter certifies consistency of the claimant's
> bytes with themselves, never correspondence of the claim to the world; and because the predicate
> is frozen with the counter, the discovery of any self-consistent shortcut class forces an honest
> stop or a non-counter verdict each time.**

The mechanism that makes it repeat: each round converts the discovered class into a QUALITY row
scoped to the *instance's* claim shape, never into the general freeze-time rule. The evidence chain
of instance-patches: r33 routed-3 → #66 (maps); r34 M34-4 → #67 (ELF counters only); r34b M34-7/8 →
#69/#70 (replay gates only); r35 M35-2 → routed to r36; r36 M36-3/M36-4 (`corpus/lessons/round-36.md:17-18`)
→ #77 (self-assessment surfaces only) / #78 (receipts only). The lane's own M36-3 row names the gap:
"QUALITY #68 asks for predicate identity but no row asked the counter to enumerate every occurrence
of a statement shape". `[INFERENCE]` next round's claim will be a new shape (a coverage counter over
some other producer's receipts, or a calibration counter over some other surface), and nothing now on
the books stops it from repeating the error a sixth time.

## 3. The smallest freeze-time rule (one sentence)

> **At freeze time, for every frozen counter, the control family must include at least one
> self-consistent shortcut control — built from the frozen reference bytes alone — that passes every
> check the counter implements while violating the predicate's operative clause, and if any such
> control meets the target the claim stops before any data and the counter is redesigned, never
> repaired by amending the predicate after scoring.**

Equivalently, in the lane's vocabulary: a frozen control must be built by enumerating the invariants
the counter does **not** test (for C1: provenance of the bytes — so the class is a re-hashed
fabrication; for C2: occurrence multiplicity and document identity — so the classes are shadow rows
and same-basename decoys) and asking whether an artifact preserving exactly those invariants greens.
The existing kill-rule machinery already does the right thing once the class exists — r34b proved the
refusal mechanism flips to REFUSED when the class is registered (`corpus/lessons/round-34.md:49`);
what is missing is the obligation to *find* the class before data.

This rule is deliberately a freeze-time rule, not a counter-design rule: it does not dictate
enumerators, findall, provenance re-runs, or executable counters — those are means, and QUALITY
77/78 already carry them. It dictates the *test* every freeze must pass, whatever shape the claim
takes next.

## 4. Does QUALITY 77/78 already state it? — No

- **#77** (`corpus/QUALITY.md:85`) states the C2-side consequences for counters over
  self-assessment surfaces only: `findall` not first `search`; duplicate rows/boxes as separate
  units; populations bounded below the base; repaired pointers checked against the intended document.
  Its final sentence — "A green counter that a shadow row, a second contradictory statement or a
  decoy document can reach certifies nothing" — is the *conclusion* of the general rule applied to
  one surface family, not the freeze-time obligation to construct such a control before data.
  Nothing in #77 would have caught F1 (receipts are not self-assessment surfaces).
- **#78** (`corpus/QUALITY.md:86`) states the C1-side consequence for receipt-integrity checks only:
  a stored evidence id recomputing under the pinned rule is not provenance; provenance comes from an
  independent non-author re-run comparing the semantic payload. It would not have caught A1–A6
  (nothing in #78 enumerates surface occurrences).
- **#67** (`corpus/QUALITY.md:77`) contains the general rule's stopping half — "if it meets a frozen
  target, stop without amending, re-scaling or relabelling the claim" — but is scoped to "a finite
  ELF structural-decoding counter" and its required class is a structure-blind *reader* replay,
  which is exactly inapplicable to a data-only receipt counter (C1-F1 is not a reader) and to a
  surface counter (C2-A1 is not a replay).
- **#48** (`corpus/QUALITY.md:58`) lists "do-nothing, junk-row, all-false, no-reader and **id-keyed
  shortcut** controls" and says "a control that meets the target forces a re-design before data" —
  the embryo of the rule. Two gaps explain r35 and r36 recurring despite it: the enumerated classes
  are a fixed menu keyed to id-keyed counters (no fabrication/shadow/decoy classes for data-only or
  surface counters), and #50 then narrowed what the axis-fit gate proves to field existence. R36's
  freeze satisfied #48's letter — frozen controls, pre-data scoring, kill rules — with 27 selftest
  cases all in the absent/junk/wrong family.
- **#69** (`corpus/QUALITY.md:79`) comes closest to the general form for transformations ("proves
  only the invariants it actually breaks … no key built from the surviving invariants can reproduce
  the expectation") but is scoped to replay fixtures and does not cover fabricated receipts or
  shadowed surfaces.

So: 77 and 78 each state one leg of the round-36 instance; 67 states the stopping rule for one
counter family; 48 names a shortcut control without defining it as "passes the implemented check,
violates the operative clause". The general rule — Section 3 — is not on the books.

## 5. What this means for the landed round-36 verdicts (coverage / calibration)

- **The green receipts at `ffc81341`/`01a44dbf` do not by themselves establish P36-C1 or P36-C2.**
  Each counter certifies its weakened relation, and each was shown green-able by a self-consistent
  shortcut class after the freeze. This is not a do-over claim: the lesson already concedes both
  points — M36-3 ("Not shown able to fail on the frozen counter … the round's C2 verdict is
  re-derived by a stricter non-counter check in wave 2 instead of being cited alone") and M36-4
  ("provenance of the real receipts rests on four independent seat reproductions
  `w1/R36ExecReproK{1,2,3,4}.md`").
- **Coverage (C1):** the capability move Frontier → Core is supported by the reproductions and the
  four independent re-runs, not by the counter receipt. Calibration (C2): supported by the wave-2
  stricter re-derivation, not by `c2-counter.py`'s `met_target`. A verifier should treat the
  counters' greens as necessary-not-sufficient, exactly as the lane now says.
- **The falsification target of wave 2 is therefore narrower than "the landing is wrong":** it is
  "the landing is right *for reasons the frozen instruments cannot certify*". This seat found no
  evidence against the reproductions themselves; it found that the lane's own criteria (77/78) admit
  the instruments are insufficient, and that without Section 3 the next round will re-author the same
  insufficiency in a new shape.

## 6. Risks and second-order effects of adopting the rule

- **Cost.** One self-consistent control per counter per round. Cheap next to a rejected round:
  wave-1 produced F1 in a day; A1 is three lines. The r34b precedent shows the discovered class can
  simply be *registered* (flipping the gate to REFUSED) without redesigning the counter — so the
  rule's floor effect is "register the class or stop", which r34b already absorbed once.
- **Good-faith false alarms.** A1 is reachable in good faith (a scribe restating a count by
  appending a row) — the C2 critic says so. The rule converts such an append into a stop, which is
  the intended pressure toward editing rows in place rather than shadowing them; the SCORECARD
  round-36 section already models the in-place repair at `d2e46ef5`.
- **Scope creep risk in the other direction.** If the rule is written instance-style again ("for
  receipt counters…, for surface counters…"), the sixth repetition is guaranteed. It must be one
  sentence, claim-shape-agnostic, or it repeats the #66/#67/#69/#77/#78 scoping mistake this report
  documents.
- **No harm to the frozen artifacts.** The rule binds future freezes; it asks for no edit to the
  round-36 counter, predicate, carriers, oracle, or receipts (all frozen; this seat changed none).

## 7. Verification performed here (all read-only; nothing executed against the lane counters)

| check | command | observed |
|---|---|---|
| wave-2 tree state | `git log --oneline -5`; `git status --porcelain` | tip `6f2ba761` (wave-1 results + w2 dispatch); untracked only `.ufo/waves/round-36/w2*` |
| C1 selftest case family | `grep -n "cases = \[" tools/round-36/c1-counter.py` + read `c1-counter.py:310-328` | 14 cases, all negative/absent classes; no self-consistent forgery case |
| C2 selftest case family | read `tools/round-36/c2-counter.py:284-298` | 13 cases, all negative/absent classes; substitution case uses a different-basename document |
| QUALITY row texts | read `corpus/QUALITY.md:75-86:raw` | rows 67–74, 77, 78 as quoted; no row 75; #48 at line 58 as quoted |
| r33 instance | `grep -n 'falsely CLEAN' corpus/lessons/round-33.md` | `:57` "7 empty/malformed freeze-map variants are falsely CLEAN" |
| r34 instances | `grep -n 'M34-4\|M34-7' corpus/lessons/round-34.md` | `:18` size-pristine 12/12 both schedules; `:57` nameset 8/8, "green surface keys on invariants it did not vary" |
| r35 instance | `grep -n 'substring\|S1060' corpus/lessons/round-35.md` | `:10` fabricated census receipt without hash validation; `:62` `S106` substring matches `S1060` |
| r36 lesson rows | `grep -n 'M36-3\|M36-4' corpus/lessons/round-36.md` | `:17-18` as quoted, including "no row asked the counter to enumerate every occurrence" |
| plan freeze sentence | `grep -n 'do-nothing control is scored' plans/round-36-claims.md` | `:6` |
| shortcut-class evidence | read `w1/R36CriticC1Shortcut.md` §Verdict/§3/§4/§6; `w1/R36CriticC2Shortcut.md` method + classes | F1 exit 0 `met_target` with stdlib recompute; "None of the 13 cases exercises any class below"; A1 three-line append |
| verifier spotchecks | read the three `corpus/lessons/round-3{3,4,5}-verifier-spotcheck.md` files | r33 vacuous-CLEAN maps; r34 nameset 8/8 bound to the gate's own counter by config and digest; r35 D-1/D-3 as quoted |

Not re-executed (PROTOCOL §Gate standard for a connector seat; evidence read from the committed
reports and receipts): every fixture run, counter run, and the wave-1 reproductions. No lane counter,
harness, or REA command was run.

## 8. Disclosure, tooling, cleanliness

- Installs/updates: none. No pacman, no `uv tool`, no `npm`, no `~/.local/bin` change; nothing
  removed. (`~/.local/bin/sasquatch*` untouched.)
- Network: none.
- VCS: read-only (`git log`, `git status`, `grep`, `read`). No add/commit/checkout/reset/stash;
  no jj. No fixture repos were needed — the pattern evidence is entirely in committed wave-1 and
  verifier-spotcheck reports plus the frozen counters' selftest case lists.
- Scratch `/fast/scratch/hyaku/kaidoku-r36/R36W2ConnCrossClaim` was created per the seat bounds and
  removed before this report was written; it held no files. `TMPDIR` pointed there during the
  session. Nothing under `/fast/scratch` was inventoried.
- Only this report file was written in the lane: `.ufo/waves/round-36/w2/R36W2ConnCrossClaim.md`.

## 9. Limits

- `[INFERENCE]` where marked: the r33 fit into the family (its rejection was formally "unprovable");
  the mechanism in Section 2 (instance-scoped patches guarantee repetition); the severity ordering
  of A1–A6 (the C2 critic's judgement, adopted).
- This seat does not judge, admit, or integrate: it proposes Section 3 as the single compatible
  synthesis across the round's two shortcut critics and the three rejected rounds' spotchecks. If
  the L1 adopts it, the natural home is a QUALITY row 79 superseding none, citing this report and
  `R36CriticC1Shortcut.md`/`R36CriticC2Shortcut.md` — the decision is the integration owner's.
