# SCORECARD.md round-section draft — C2 records (SC-2, arc3-loop1-round4)

Seat SC-2 · chain c2 · role scribe · 2026-10-19. **Draft for the PARENT;
SCORECARD.md was not touched by this seat.** Append at EOF (after the
`arc3-loop1-round3` section; HEAD at draft time `015e1bab…`, file 1580 lines).
`⟨…⟩`/`⟨FILL⟩` = parent-fill slots, the producing seat named; the **C2 bullet,
the C2 verdict row and the C2 learning sentence are drafted complete**, with the
chain's own verifier census as the count of record and this seat's first-hand
measurements as the corroboration.

**Pin-free discipline (measured, load-bearing).** The census instrument
(`.ufo/gates/c1-census-v10.py`, sha256 `d0772ce8…`, 610 lines) declares a fixed
scope table over `PROVINCE.md`, `SKILL.md` and `SCORECARD.md`; the last declared
SCORECARD row ends well before the current EOF, so a locus past that bound reads
UNDECLARED → FAIL. A locus exists only where a `REA_GATE` line also carries a
pin, a bare client-version literal, or an absolute `path.json|toml|yaml:NNN`
pointer. The text below therefore carries **no version literal, no `@`-pin, no
`path:line` pointer, and no client config filename** — the five custody paths
are named as "three client configs + two shell profiles". §3 records the
simulation that measures this (PASS with zero added loci, plus a planted-pin
control that FAILs).

## Literal section text (append as-is; fill `⟨FILL⟩`/`⟨PARENT-FILL⟩` slots first)

<!-- BEGIN LITERAL SECTION TEXT -->
## arc3-loop1-round4 — coverage: the Vyper leg + freshness: PROVINCE staleness census + operability: ⟨PARENT-FILL: C3 phrase⟩: ⟨PARENT-FILL: verdict phrase per the cross seat's outline⟩, 2026-10-19

Round 4 of the reset window (4/10). Axis set: **coverage (owned)**,
**freshness (fleet)**, **operability (fleet)**; all three owned proxies remain
tied at 10.0 with none retired, so the owned claim was selected by the standing
most-falsifiable-next-claim tie-break. Claims are causally separable: a corpus
knowledge entry + map token, a set of PROVINCE surface repairs, and the custody
tool share no edit target. Roster frozen PRE-DISPATCH: 48 seats enumerated
mechanically (16 + 14 + 14 + 4, every name exactly once; the items-array
assertion held at dispatch). Lane: the hyper lane returned 402 out-of-credits on
all 48 seats (zero delivered); per the schedule's declared fallback and the
operator directive the roster re-dispatched on the devin lane — **recorded with
cause and per-lane delivery counts, not smoothed into a lane signal**.

- Wave: ⟨PARENT-FILL: reports path, work / wave-artifacts / records commits,
  delivery ⟨N⟩/48 per the roster reconciliation⟩.
- C1 coverage (owned) — the Vyper leg, the r3 EVM entry's last named Unknown:
  one authorized install into an isolated wave venv, then carriers compiled with
  the pinned Vyper and probed **15/15 K/K** against a set derived independently
  from the compiler's own ABI (`ev_405e2a2a…` at the older pin; five probe legs
  re-run first-hand by the C1 scribe seat, plus a 4/4 control carrier and a
  creation-form parsed-and-empty control). The dispatch mechanism is
  **modulo-indexed** — a 13-entry `uint16` jump table of JUMPDESTs with a
  `bucket = selector % 13` rule and 15 compare sites reached by a chain walk —
  and the tool's reported offsets are **not** JUMPDESTs for this compiler: each
  is the fall-through body entry eleven bytes past its compare `PUSH4`, with the
  compare-site JUMPDEST twelve bytes before it carrying that function's own
  selector (re-derived 15/15 and 4/4). Zero false positives; mutability inference
  reads 7/15 agreeing with the ABI and 8/15 `payable` (ABI view ×5, nonpayable
  ×2, pure ×1), recorded rather than smoothed. Lands as the new entry + an
  additive line-neutral map token; command A 83 → 84 with the prior 83
  byte-identical.
- C2 freshness (fleet) — **PROVINCE Frontier + surface-summary staleness census
  and same-line repairs**, graded by two deliberately independent instruments:
  the chain's per-claim staleness census (claim × evidence × verdict over the
  document, checked against admitted corpus state) and the pre-existing
  version/pin gate (loci only). **Before: stale 6 of 26 rows, 2 adjudicated, 18
  current**; the gate reads baseline **PASS `stale=0 ambiguous=0 undeclared=0
  unresolved=0`** exit 0 at HEAD `015e1bab…` (instrument `d0772ce8…`, 610 lines;
  PROVINCE.md 162 lines, sha256 `d075a3c6…`). **After: 0.** The six stale rows
  and what falsifies each:

  | # | row | claim as written | measured state | class |
  |---|---|---|---|---|
  | i | Frontier, PE subtypes | "Reserve: 91MB Godot ARM64 template" | the reserve was consumed — the target was attempted, then the scale wall fell mitigated (9 segments / 75,218 procedures) with the disable recipe proven NECESSARY by the sealed no-disable control; the coverage map already reads the point as closed, not frontier | stale |
  | ii | Frontier, alternate providers | "JEB (unprobed)" | probed in a later round — the client verb returns its declared `capability_unavailable` refusal with the verbatim start-a-client message (default port not listening); the no-engine claim holds, the word "unprobed" does not; IDA and Hopper halves current | stale |
  | iii | Frontier, EVM extended | "real solc/vyper-compiled bytecode untested" | both halves falsified — real solc-0.8.37 carriers recovered K/K in two admitted rounds, and this round's Vyper leg reads 15/15 (the repair's wording is coupled to C1's entry landing — parent note 2) | stale |
  | iv | Round-4 frontier, cross-version residuals | "`compare-application-versions` still probe-refused since r2" | falsified — the success path ran live over three input classes (two success legs byte-identical on re-run, plus the runtime-reconciliation × static-layer pair and its cross-app variant); only the refusal datum was ever held | falsified |
  | v | Core, host fallback readers | "absent: `7z`, `xxd`, radare2/r2, strace, upx …" | all five present and package-owned (7zip, radare2, strace, upx, plus the xxd provider; one install epoch 2026-10-13 13:52 -03) while cabextract, rizin, ltrace, pacman-contrib are genuinely absent | false absence claim |
  | vi | Round-4 frontier, >90 MB PE wall | "Next: raise the startup timeout … + maxmem 6-8G" | advice overtaken by the validated analyzer-disable recipe; the scale point is closed in the coverage map; its named unknown resolves and rerun id-stability is STABLE | stale |

  **Adjudicated NO-CHANGE with cause (2 rows):** the Frontier recorded-crashes
  bullet — its class claim holds (the surviving population re-measured first-hand
  at 656 MB, 172.8 MB and 36.4 MB decompressed, all over the cap; the no-knob
  clause holds against the verb's own schema, which exposes only a path and a
  debugger-context input) while its named exemplar expired under the
  retention-decay rule the bullet itself declares, so only the exemplar needs a
  same-line refresh; and one surface-summary pointer whose cited config line no
  longer carries the pin (the live pin sits at a later line) — explicitly
  receipt-stamped and round-scoped, hence historical by construction, needing a
  re-anchor only if the summary should point at the current line.
  **Unit note (the count's honest boundary):** the row (v) sits in a DATED scope
  range and is a Core table row rather than a Frontier bullet or a
  surface-summary claim, so a narrow reading of the claim's unit counts 5, not 6.
  This section quotes the **broad** reading because it is the safer repair set;
  both readings agree on the other five rows.
  Every repair is **same-line** (PROVINCE 162 → 162) and lands as **patch text
  applied by the parent** — seats never write PROVINCE. Two constraints, each
  measured on scratch trees, hold for the whole set: **line-neutrality** (a patch
  that shifts the DATED row's marker line reads a marker SCOPE-ERROR → FAIL) and
  **needle-freedom in the undeclared Frontier region** (a version literal in a
  Frontier line reads UNDECLARED → FAIL; every repair here is prose-only). A
  reviewer seat independently re-applied each scoped-file patch on a separately
  built scratch tree and measured the gate's **entire verdict surface
  byte-identical** to the baseline across all of them (the same capture bytes,
  per-file floors and counts) — stronger than "no new gated locus". **Instrument
  honesty, carried not smoothed:** the gate certifies locus hygiene and anchor
  agreement, **not claim truth** — a reviewer measured that the EVM bullet emits
  **zero** loci in both states, so the gate neither validates nor refutes that
  repair; the census table above, not the PASS, is this claim's certificate. The
  same reviewer sustained a **content** defect in a demo patch's added wording
  (it asserted a Core promotion the corpus's own scope lines disclaim — both EVM
  entries state "RESULT-class, no Core promotion" verbatim), which is why the
  landing candidate uses the scope-true form; and it measured that a
  stale-version repair written as a bare version literal inside the Frontier
  region reads PASS — a blind shape every repair here avoids. ⟨PARENT-FILL:
  landed patch-text paths, the scope-true wording chosen, and the patched
  PROVINCE sha256 — re-derived after the final write⟩.
- C3 operability (fleet) — custody-pair residual closures, four named debts to
  declared classes: the sidecar path is scope-checked in both spellings (refused
  at the usage exit class, victim files re-deriving their pre-images, no second
  derived sidecar); the parent-directory creation moves inside the guarded
  region (raw traceback → declared usage class, fresh parent still created on the
  success path); the coverage gate counts **distinct paths, not stanzas** (three
  padded reference shapes that previously read clean now refuse; the genuine
  five-distinct reference still passes); and the both-sides-absent `MATCH` is
  **adjudicated with ruling text in the README** — every such row states the
  match is an agreement on absence, not a verified presence, so the compound
  case is a declared ruling rather than a silent pass. Tool `29bb45ae…` (1343
  lines) + README `9d9400da…` (272 lines) landed together; selftest **22 → 28**
  CLEAN; receipts self-pin the landed tool; the live pair reads `MATCH 5/5
  exit 0`; command A unchanged. The README churned four times inside the landing
  window (`f30df42e…` → `91fd386b…` → `125e7e02…` → `9d9400da…`) — recorded, and
  the parent must re-derive the settled README at the records commit. This seat
  re-derived the landed identities and re-ran the selftest first-hand on a
  scratch copy: `CLEAN cases=28 passed=28 failed=0 exit=0`.
- Measured at the records commit: command A ⟨FILL: quote the run — at HEAD this
  seat measured 83/83, missing `[]`, dangling `[]`, 14/14 rules, 10.0/10.0⟩;
  the gate ⟨FILL: verdict + the instrument's sha at read time⟩; the chain's
  staleness census ⟨FILL: re-quote — at draft time it read 26 rows / 6 stale /
  2 adjudicated / 18 current⟩; the custody tool's selftest ⟨FILL: re-quote at
  landing⟩. The landed artifacts' fresh identities are recorded at landing, per
  the standing identity discipline (rule #14): ⟨FILL: entry file lines/sha256,
  README sha256, patched PROVINCE sha256 — re-derived after the final write,
  never inline⟩.
- Custody: the five custody paths (three client configs + two shell profiles)
  stayed READ-ONLY for every seat — hash/stat capture only, every demo on a
  scratch copy, with a syscall-level proof recorded (each path opened exactly
  once, read-only; zero write/rename/chmod/utime syscalls against them).
  ⟨FILL: pre-pair time + 5/5, post-pair time + 5/5, in-window drift statement
  from the wave's landed receipts⟩. Scratch on `/var/tmp` + `/dev/shm` (host
  quota hazard standing).

| Axis | Before → after | Verdict |
|---|---|---|
| coverage — C1 | knowledge 83 → 84; the Vyper leg recovers 15/15 K/K with the modulo-indexed dispatch mechanism and the non-JUMPDEST offset rule measured at byte level; mutability 7/15 agreeing, 8/15 `payable`, recorded | ⟨FILL: parent confirm⟩ |
| freshness — C2 | PROVINCE staleness census 6 → 0 (one row falsified outright — a verb written off as probe-refused since round 2 had been exercised live over three input classes; one reserve consumed and its wall fallen mitigated; one false absence claim naming five installed tools as missing; the EVM bullet's last Unknown closed by this round's Vyper leg); repairs same-line (162 → 162); gate PASS at every patched tree, verdict surface byte-identical; certificate scope stated (locus hygiene, not claim truth) | improved |
| operability — C3 | four named custody residuals → declared classes (sidecar scope refused in both spellings; parent-dir creation inside the guard; coverage counted by distinct path — three padded shapes that previously read clean now refuse; both-sides-absent `MATCH` adjudicated by landed README ruling, non-silent by construction); selftest 22 → 28; live pair MATCH 5/5 | improved |
| depth | 10.0 → 10.0 ⟨FILL: command A at the records commit⟩ | unchanged |
| calibration | 10 → 10 | unchanged |

Learning trends: coverage — the Vyper leg closed the last Unknown of the EVM
family by measurement rather than by analogy: the mechanism turned out to be
structurally different from the solc family (a modulo-indexed jump table rather
than a linear compare chain), and the tool's offset convention inverted with it
(the reported offsets are fall-through body entries, not the JUMPDESTs the solc
family produced), so the r3 entry's "offsets land on JUMPDESTs" reading is now
explicitly solc-scoped — a cross-compiler generalization the round could not
have known before running it. Freshness — the round's two censuses were built
independently and disagreed in exactly one place (whether a Core table row is in
the claim's unit), which is reported as a count boundary (6 broad / 5 narrow)
rather than silently reconciled; the gate's certificate boundary was measured
rather than assumed (it emits zero loci for the bullet under repair, so the
census table, not the PASS, carries the claim); one repair candidate was
**refuted on content** — it asserted a Core promotion the corpus's own scope
lines disclaim — and one gate-blind repair shape (a bare version literal in the
undeclared Frontier region) was measured and avoided. Operability — the four
custody residuals closed as declared classes with the sharpest one adjudicated
rather than patched away: the both-sides-absent case stays a `MATCH` by
declared ruling, but every such row now says so in its own output, turning a
silent agreement-on-absence into a stated one — the round chose to make the
semantics visible rather than to change them, and recorded the choice as a
ruling instead of a code change. Planned: round 5 per schedule (the lane substitution rides the
devin lane while the token-plan quota is exhausted; recorded per the operator
directive). Carried debt (named): the gate's same-line inline-marker excusal and
its per-needle partial-blindness residual; PROVINCE's undeclared Frontier region
(a repair needing a version needle there requires a same-commit scope re-key of
the census instrument, which is the C1 chain's file — coordination point); the
surface-summary pointer that no longer points at the live pin line (adjudicated
historical; re-anchor optional); the landing-window README churn (four identities
inside the window, the last after the first citation — re-derive the settled
bytes at the records commit); ⟨FILL: C1 Unknowns + C3 residues from their
records⟩; the pre-existing dirty `.ufo/waves/arc2-loop1-round10/C3.md`; host
`/tmp` quota (standing). Retired: ⟨FILL: none / named⟩.
<!-- END LITERAL SECTION TEXT -->

## Notes for the parent (not part of the draft)

1. **Count of record and its boundary.** The chain's verifier census is the
   count quoted in the section (26 rows / 6 stale / 2 adjudicated / 18 current).
   This seat's own first reading of the narrow unit (Frontier bullets +
   surface-summary claims) found 5, differing only on the Core
   host-fallback-readers row. The section states the boundary explicitly instead
   of picking a number silently; if the parent prefers the narrow reading, the
   table loses row (v) and every other value stands.
2. **Cross-chain coupling (sequencing).** C1's Vyper leg has **landed its
   measurement** (15/15 K/K; five probe legs re-run first-hand) but its corpus
   entry is still **patch text** (staged stem `2026-10-19-arc3-r4-evm-vyper-leg`).
   Row (iii)'s repair therefore asserts a Vyper holding the corpus cannot yet
   back: **land the repair and C1's entry in the same commit**, or fall back to
   the solc-only wording. The round's apply-and-measure seat and its reviewer
   flagged this independently, and the landing candidate patch carries the same
   warning in its own text.
3. **The gate cannot see the row it certifies.** Measured by the reviewer: the
   EVM bullet produces zero loci under the gate in both baseline and patched
   states (its text never matches the gate's needle family). Quote the census
   table as the certificate; do not present the PASS as validating the repair.
4. **Fill the `⟨FILL⟩` slots from landed artifacts, not from the frozen claim.**
   If the landing landed differently, say so — an unrun check has not passed.
5. **Re-run §3's simulation after filling**, and again at the records commit:
   the pin-free property is measured, not asserted, and the control fails on a
   single planted line.
6. **Keep the section pin-free after filling** — quote receipt sha256s and
   epochs, never a client config path or a version literal. The gate's declared
   bound ends well before the current EOF; text appended past it must be
   locus-free in the gate's unit or the bound must be re-keyed in the same
   commit.

## §3. Pin-free census simulation (SC-2) — MEASURED

Method (round-2/round-3 scribe precedent): copy the three scoped files at HEAD
into a scratch root under `/var/tmp`, append the literal section text
(re-extracted between the BEGIN/END markers), run the gate with `--root` on that
tree, then append one planted pin literal to a second copy as the positive
control and run again. The real tree is read-only throughout.

| Tree | SCORECARD lines | loci (SCORECARD) | Verdict | exit | output sha256 |
|---|---|---|---|---|---|
| sim-base (HEAD files) | 1580 | 9 | PASS 0/0/0/0 | 0 | `7cb9b513412f47b0…` |
| sim-records (+165-line section) | 1744 | 9 | PASS 0/0/0/0 | 0 | `990598ba5bb3bfe4…` |
| sim-control (+1 planted pin) | 1745 | 10 | FAIL undeclared=1 | 1 | `4b8e7970c2113fd0…` |

- PROVINCE.md (162 lines / 6 loci) and SKILL.md (390 lines / 2 loci) were
  unchanged in all three trees at the measured revision; the G2 positive floor
  (17 / 14 / 3) was unchanged between base and records.
- The measured revision of the drafted section added **zero loci** (9 → 9) — the
  pin-free property is measured, not asserted.
- The control shows the detector is live on the same appended region: one
  planted pin literal flips the run to UNDECLARED → FAIL exit 1.
- Instrument identity bracketing the runs: `.ufo/gates/c1-census-v10.py` sha256
  `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` (610
  lines), identical before and after. HEAD `015e1bab…`. Raw outputs, the
  command A receipt and the earlier revision's captures:
  `claims/c2/SC-2/evidence/` (`SHA256SUMS` re-derived at write time).
- Caveat for the parent: re-run at the records commit and quote the then-current
  instrument sha. **Any `⟨FILL⟩` text added later must be re-measured** — the
  control above fails on a single planted line.
