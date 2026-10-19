# LOG.md entry draft — C2 records (SC-2, arc3-loop1-round4)

Seat SC-2 · chain c2 · role scribe · 2026-10-19. **Draft for the PARENT; LOG.md
was not touched by this seat.** Append at EOF (after the `arc3-loop1-round3`
entry; HEAD at draft time `015e1bab914713568f339fd53999bc180459cc40`, file 1487
lines). `⟨…⟩`/`⟨PARENT-FILL⟩` = parent-fill slots, the producing seat named.

**Pin-free discipline (kept deliberately, same voice as the SCORECARD side).**
LOG.md is not census-scanned today (the instrument's declared scope names
`PROVINCE.md`, `SKILL.md`, `SCORECARD.md` only), but this entry is written
pin-free anyway so both records read in one voice and no future re-scoping
surprises: no `rea-agents@x.y.z` literal, no bare client-version literal, no
`~`- or `/`-absolute `*.json|toml|yaml:NNN` pointer, no client config filename.
The five custody paths are named as what they are — "three client configs + two
shell profiles". Artifact identities are sha256 fragments or file stems.

## Literal entry text (append as-is; fill `⟨FILL⟩`/`⟨PARENT-FILL⟩` slots first)

<!-- BEGIN LITERAL ENTRY TEXT -->
### arc3-loop1-round4 — coverage: the Vyper leg + freshness: PROVINCE staleness census + operability: ⟨PARENT-FILL: C3 short phrase⟩ (2026-10-19)

- Dispatch: 48 seats frozen PRE-DISPATCH (roster enumerated mechanically —
  16 + 14 + 14 + 4, every seat name exactly once; the items-array assertion
  `len(items) == 48` held at dispatch, per the counting lesson). Lane: the
  hyper lane returned 402 out-of-credits on all 48 seats (zero delivered, ~30 s);
  per the round schedule's declared fallback and the operator directive the full
  roster re-dispatched on the devin lane — **recorded with cause and per-lane
  delivery counts, not a lane signal**. Delivered ⟨PARENT-FILL: N⟩/48 per the
  roster reconciliation (count the items array, never the intent).
- C1 coverage (owned) — the Vyper leg, the last Unknown of the r3 EVM entry.
  One authorized install into an isolated wave venv (interpreter resolved from
  the host's on-disk runtimes rather than the system interpreter; the venv's
  wheel set and the compiler wheel's sha256 recorded in the chain's tree).
  Five carriers compiled with the pinned Vyper (one ERC-20-bearing) and probed
  **15/15, 7/7 and 22/22 K/K** against sets derived independently from the
  compiler's own ABI (`ev_405e2a2a…` hex at the older pin for the 15-set; the
  C1 scribe re-ran five probe legs first-hand, plus a creation-form
  parsed-and-empty control). Byte-level findings: the dispatcher is
  **modulo-indexed** — a 13-entry `uint16` jump table whose every entry is a
  JUMPDEST, a `bucket = selector % 13` rule, compare sites reached by a chain
  walk; and the tool's reported offsets are **not** JUMPDESTs for this compiler —
  each is the fall-through body entry eleven bytes past its compare `PUSH4`, with
  the compare-site JUMPDEST twelve bytes before it carrying that function's own
  selector (re-derived 15/15 and 4/4). Zero false positives (the only
  non-selector `PUSH4` immediates in the runtime are a revert constant ×6 and a
  four-byte ASCII word; the `__default__` method key is absent from the runtime
  bytes). Three measured deltas against the solc family are recorded with their
  scope: the dispatch layout, the offset convention (so the r3 entry's "offsets
  land on JUMPDESTs" reading is now explicitly solc-scoped), and the state-
  mutability inference (7/15 agreeing with the ABI, 8/15 read `payable` against
  ABI view ×5 / nonpayable ×2 / pure ×1 — no case more restrictive, no selector
  misassigned). Lands as the new corpus entry + an additive line-neutral map
  token; command A 83/83 → 84/84 with the prior 83 byte-identical (the C1
  scribe's scratch-tree rehearsal of the entry-plus-token pair reads 84/84,
  missing `[]`, dangling `[]`, rules 14/14).
- C2 freshness (fleet) — **PROVINCE Frontier + surface-summary staleness census
  and same-line repairs.** Two instruments, deliberately independent: the chain's
  own staleness census (a per-claim `(claim, evidence, verdict)` table over the
  document, run against admitted corpus state) and the pre-existing version/pin
  census gate, which grades loci only. **Before: the chain's census reads
  total 26 rows — stale 6, adjudicated 2, current 18**; the gate reads baseline
  **PASS `stale=0 ambiguous=0 undeclared=0 unresolved=0`** exit 0 at HEAD
  `015e1bab…` (instrument `d0772ce8…`, 610 lines; PROVINCE.md 162 lines, sha256
  `d075a3c6…`). The six stale rows, each with the admitted state that falsifies
  it:
  (i) PE-subtypes bullet — "Reserve: 91MB Godot ARM64 template": the reserve was
  **consumed**, not reserved — the target was attempted, then the scale wall fell
  **mitigated** (9 segments / 75,218 procedures) with the analyzer-disable recipe
  proven NECESSARY by the sealed no-disable control that OOM-killed at the larger
  cap; the coverage map already reads that scale point as closed, not frontier;
  (ii) alternate-providers bullet — "JEB (unprobed)": JEB **was** probed in a
  later round and returns its declared `capability_unavailable` refusal with the
  verbatim start-a-client-or-set-the-endpoint message (the default port not
  listening); the operative claim (no engine) holds, the word "unprobed" does
  not; the IDA and Hopper halves re-measured current;
  (iii) EVM-extended bullet — "real solc/vyper-compiled bytecode untested": both
  halves now falsified — real solc-0.8.37 carriers recovered K/K in two admitted
  rounds, and this round's Vyper leg recovers 15/15 (the coupling in parent
  note 2 applies: the repair's final wording must cite the landed entry, not the
  patch text);
  (iv) cross-version-residuals bullet — "`compare-application-versions` still
  probe-refused since r2": falsified — the verb's success path was exercised live
  over three input classes (two success legs recorded byte-identical on re-run,
  plus the runtime-reconciliation × static-layer pair and its cross-app variant);
  only the refusal datum was ever held;
  (v) the Core host-fallback-readers row — a **false absence claim**: five tools
  listed as absent are present and package-owned (7zip, radare2, strace and upx,
  plus the xxd provider; one install epoch, 2026-10-13 13:52 -03) while
  cabextract, rizin, ltrace and pacman-contrib are genuinely absent. This row is
  in a DATED scope range (a record of a past verification) but the claim's own
  unit wording was read broadly by the chain's census, which counts it; the
  parent should note the narrower reading (a Core table row is neither a Frontier
  bullet nor a surface-summary claim) — the count is 6 under the broad reading
  and 5 under the narrow one, and this entry quotes the **broad** reading
  because it is the safer of the two;
  (vi) the post-unlock ">90 MB PE scale wall" bullet — its "Next: raise the
  startup timeout … + maxmem 6-8G" advice was overtaken by the validated
  analyzer-disable recipe, and the scale point is closed in the coverage map;
  **Adjudicated NO-CHANGE with cause (2 rows):** the recorded-crashes bullet —
  its class claim still holds (the surviving population re-measured first-hand
  at 656 MB, 172.8 MB and 36.4 MB decompressed, all over the cap; the no-knob
  clause re-measured against the verb's own schema, which exposes only a path and
  a debugger-context input) while its named exemplar expired under the
  retention-decay rule the bullet itself declares; and one surface-summary
  pointer whose cited config line no longer carries the pin (the live pin sits at
  a later line) — the citation is explicitly receipt-stamped and round-scoped, so
  it is historical by construction and the pointer needs a re-anchor only if the
  parent wants the summary to point at the current line.
  **After: stale 6 → 0**, every repair **same-line** (PROVINCE 162 → 162 lines),
  landing as **patch texts applied by the parent** (seats never write PROVINCE —
  the scoped-file rule). Two constraints hold for every repair in the set, each
  measured on scratch trees: **line-neutrality** (a patch that shifts the DATED
  row's marker line reads a marker SCOPE-ERROR → FAIL) and **needle-freedom in
  the undeclared Frontier region** (a version literal written into a Frontier
  line reads UNDECLARED → FAIL; every repair here is prose-only). A reviewer
  seat independently reproduced each scoped-file patch on a separately built
  scratch tree and measured the census's **entire verdict surface byte-identical**
  to the baseline across all of them (same 7,197-byte capture, same per-file
  floors, same counts) — stronger than "no new gated locus". **Instrument
  honesty, carried not smoothed:** the gate certifies locus hygiene and anchor
  agreement, **not claim truth** — a reviewer measured that the EVM bullet
  produces **zero** loci under the gate in both baseline and patched states, so
  the gate neither validates nor refutes that repair; the census table above, not
  the PASS, is this claim's certificate. A reviewer also sustained one
  **content** defect against a demo patch's added wording (it asserted a Core
  promotion the corpus's own scope lines disclaim — both EVM entries are
  RESULT-class with "no Core promotion" stated verbatim), which is why the
  round's landing candidate is the scope-true form; and it found that a
  stale-version repair written as a bare version literal inside the Frontier
  region would read PASS, i.e. the gate is blind to that one shape, so every
  repair here avoids it. ⟨PARENT-FILL: the landed patch-text paths, the
  scope-true wording chosen, and the patched PROVINCE sha256 — re-derived after
  the final write⟩.
- C3 operability (fleet) — custody-pair residual closures, four named debts to
  declared classes: the sidecar path is scope-checked in both spellings (each
  refused at the usage exit class with the victim files re-deriving their
  pre-images and no second derived sidecar written); the parent-directory
  creation moves inside the guarded region (the raw traceback becomes the
  declared usage class, and a fresh parent is still created on the success
  path); the coverage gate counts **distinct paths, not stanzas** (three padded
  reference shapes that previously read clean now refuse, while the genuine
  five-distinct reference still passes); and the both-sides-absent `MATCH` is
  **adjudicated with ruling text landed in the README** — every such row now
  states that the match is an agreement on absence, not a verified presence, so
  the compound case stays a declared ruling rather than a silent pass. Tool
  `29bb45ae…` (1343 lines) + README `9d9400da…` (272 lines) landed together;
  selftest **22 → 28** CLEAN, the six new cases covering the duplicate/absence
  classes, with every receipt self-pinning the landed tool's sha256; the round's
  live pair reads `MATCH 5/5 exit 0` against the landed tool (captured after the
  landing) and the round's pre-pair is unchanged; command A unchanged. The
  README moved four times inside the landing window (`f30df42e…` → `91fd386b…`
  → `125e7e02…` → `9d9400da…`, the last after the first citation) — recorded,
  and the parent must re-derive the settled README at the records commit. This
  seat re-derived the landed tool and README identities and re-ran the selftest
  first-hand on a scratch copy (basename preserved): `CLEAN cases=28 passed=28
  failed=0 exit=0`.
- Custody: the five custody paths (three client configs + two shell profiles)
  stayed READ-ONLY for every seat all round — hash/stat capture only, every demo
  on scratch copies, with a syscall-level proof recorded (each path opened
  exactly once, read-only; zero write/rename/chmod/utime syscalls against them).
  ⟨PARENT-FILL: pre-pair time + 5/5, post-pair time + 5/5, in-window drift
  statement, and the pair's own receipt sha256s — take these from the wave's
  landed receipts, never from the frozen claim⟩.
- Scope: kaidoku repo only; no pushes (standing rule); one authorized install
  (the C1 chain's compiler into the wave venv — no other install); custody paths
  read-only; scratch under `/var/tmp` or `/dev/shm` (the host `/tmp` quota
  exhaustion is standing — no recipe in this round uses `/tmp`).
<!-- END LITERAL ENTRY TEXT -->

## Notes for the parent (not part of the draft)

1. **Two independent censuses, one count.** This seat ran the version/pin gate
   and an independent content reading of the Frontier bullets and the surface
   summary; the chain's verifier seat ran its own per-claim staleness census
   over the whole document. The counts reconcile as **6 stale** under the broad
   unit (the verifier's, quoted above) and **5** under the narrow unit (Frontier
   bullets + surface summary only, this seat's first reading). The difference is
   exactly the Core host-fallback-readers row. Both readings agree on the other
   five. The drafts quote 6 because a broader repair set cannot be worse than a
   narrower one, and because the verifier's instrument is the chain's own
   grading artifact.
2. **Cross-chain coupling the parent must sequence (measured, not predicted).**
   C1's Vyper leg landed its measurement (15/15 K/K, five probe legs re-run
   first-hand by the C1 scribe) but its corpus entry is still **patch text**
   (stem `2026-10-19-arc3-r4-evm-vyper-leg`, staged by the C1 scribe). The C2
   repair of the EVM bullet therefore asserts a Vyper holding that the corpus
   cannot yet back: **the repair and C1's entry must land in the same commit**,
   or the repair must fall back to its solc-only form. The round's own
   apply-and-measure seat and its reviewer both flagged this dependency
   independently, and the landing candidate patch carries the same warning in
   its own text.
3. **Revision note (rule #14, self-correction recorded rather than hidden).**
   Revision 1 of this draft counted 7 stale items and classified the
   host-fallback-readers row as an in-unit CURRENT-scope false claim. Revision 2
   corrected the classification (the row sits in a **DATED** range and is a Core
   table row, so it is out of the *narrow* unit) and dropped the
   recorded-crashes bullet to adjudicated; revision 3 re-aligned to the chain's
   verifier census (26 rows / 6 stale / 2 adjudicated) and folded in the landed
   C1 and C3 results. The underlying host measurements never changed — only the
   classification and the count.
4. **Do not take any count from this draft without re-measuring at the records
   commit** (rule #14): the stale count, the line count, the census verdict, and
   every landed identity.
5. Delivery count and custody pair come from the wave's own reconciliation
   artifacts (roster + receipts), never from the declared 48.
