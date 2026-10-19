# merged records text — arc3-loop1-round4 LOG entry (seat CN-2, cross connector)

Assembled 2026-10-19 by seat CN-2 from the chains' literal drafts — literal
blocks spliced verbatim, placeholder-normalized. **Pasteable text only**; the
parent lands R1. LOG.md is not census-scanned, but the entry keeps the same
pin-free voice (one voice across both records). Identity:
receipts/identity.txt.

## Literal LOG entry (append at EOF after the round-3 entry)

<!-- BEGIN LITERAL ENTRY TEXT -->
### arc3-loop1-round4 — coverage: [[FILL: C1 short phrase]] + freshness: [[FILL: C2 short phrase]] + operability: [[FILL: C3 short phrase]] (2026-10-19)

- Dispatch: 48 seats frozen PRE-DISPATCH (roster enumerated mechanically —
  16+14+14+4, every name exactly once; the items-array assertion held at
  dispatch). Declared on the hyper lane; re-dispatched on the devin lane after
  the hyper lane returned 402 out-of-credits on all 48 seats (the schedule's
  declared fallback; recorded with cause, not a lane signal). Delivered
  [[FILL: N]]/48 per the roster reconciliation (count the items array, never
  the intent).
- C1 coverage (owned) — the **Vyper leg** of the named Unknown "Vyper and solc
  versions other than 0.8.37" (the r3 entry's own Unknowns line). The round's
  one authorized install landed: `vyper` **0.4.3** in the wave-isolated venv
  (wheel `vyper-0.4.3-py3-none-any.whl` sha256 `3b967172…`, 403,104 B, four
  independent derivations across two seats and equal to the registry's own
  published digest; interpreter Python 3.14.7; the host has no system pip
  module and no pip on PATH — the venv was made with the stdlib module).
  Five Vyper carriers were compiled on-host with that compiler and probed with
  `inspect-evm-interface`: a fee/pause vault (K=15), a second independent vault
  (K=7), an ERC-20-bearing steward token (K=22), a four-mutability planner
  carrier (K=9) and the install smoke leg (K=4). **Every runtime leg recovered
  its planted set K/K — zero missing, zero extra, `dispatch:"abi"` on all** —
  across both pins and both encodings, against Vyper's own ABI-derived selector
  sets; the raw-on-hex-text and hex-on-rawbin traps reproduce as
  parsed-and-empty (exit 0, 0 functions, decoded digest equal to the input
  file's own), and creation-code legs are uniformly parsed-and-empty. Three
  measured deltas beyond K/K, each independently corroborated by three or more
  seats: (i) Vyper 0.4.3's dispatcher is a **third shape** — a modulo-indexed
  jump table (`bucket = selector % 13`, a 13-entry uint16 table copied from the
  runtime tail, three empty-bucket sentinel entries, then a fall-through chain
  comparing with XOR-equals-zero rather than the solc carriers' EQ/GT tree);
  (ii) the reported `bytecode_offset` on this family is **not a JUMPDEST** —
  0 of 15 land on one; each is the fall-through handler body at the compare
  site's push + 11, so the r1/r3 "offsets land on JUMPDESTs" reading is
  solc-scoped and was re-derived byte-for-byte on two carriers by this seat;
  (iii) the mutability inference reads payable for 8 of the 15 vault functions
  whose compiled ABI says view/nonpayable/pure (no case reads a more
  restrictive class; no selector misassigned) — an upstream-inference delta on
  this dispatcher family, recorded as observed, not as a defect. Zero false
  positives at byte level: the runtime's non-selector four-byte constants (the
  `Error(string)` revert selector, an ASCII fragment) were not reported, and
  Vyper's `method_identifiers` carries one phantom non-function key per carrier
  (`__default__()`) whose bytes do not occur in the runtime at all. The result
  lands as `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md`
  (RESULT-class, family-scoped, no availability→holding) + the coverage-map
  token **additive-only and line-neutral** (README 190 → 190, exactly one line
  differs); command A **83/83 → 84/84**, missing [], dangling [], rules 14/14,
  prior 83 byte-identical (this seat's scratch-tree rehearsal of the pair;
  [[FILL: parent re-measure at the records commit from real Git
  objects]]).
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
  repair here avoids it. [[FILL: the landed patch-text paths, the
  scope-true wording chosen, and the patched PROVINCE sha256 — re-derived after
  the final write]].
- C3 operability — custody-pair residual closures (the r3 c2 verdict's named
  debt: (a) sidecar path not scope-checked, (b) `out.parent.mkdir` outside the
  guarded `try`, (c) coverage gate counts stanzas not distinct paths, (d) the
  both-sides-absent `MATCH` semantics to adjudicate). **Before-state
  independently reproduced at the round-3 landed identity by this scribe on a
  scratch copy of the committed instrument** (`claims/c3/SC-3/evidence/before/`,
  scratch `/var/tmp/sc3-r4`, captured-utc 2026-10-19T14:04–14:07Z; no custody
  path touched — every fixture is a scratch file): (i) `capture --paths X.sha256
  --out X` exits 0 and the derived sidecar **replaces the measured file** with
  the two-line digest text, while the mirrored spelling `--out X.sha256
  --paths X` exits 0 and writes both the neighbour and a second derived sidecar;
  (ii) `--out <regular-file>/sub/r.txt` dies with a raw `NotADirectoryError`
  traceback from the `mkdir` call outside the guarded write region, exit 1,
  outside the declared class table; (iii) a reference carrying the same path five
  times passes `--require-paths 5` — in the current receipt shape and in both
  legacy reference shapes — with **zero** coverage lines printed (the gate's line
  exists only on the failure path), the other four custody paths unexamined;
  (iv) a path absent on both sides reads `MATCH` (compared 0 fields, sha
  contract 0/0), and the same shape at five stanzas reads `MATCH 5/5 exit 0`
  **while also passing the coverage gate** — a reference that examined nothing
  reads clean (this compound case is the round's sharpest finding and is what
  makes (c) and (d) one decision, not two). Cross-corroboration: two independent
  seats reproduced the same four shapes on the same revision (a sidecar probe
  and an injection matrix in the c3 tree; a custody seat's attack battery, whose
  verdict on the padded-reference attack is "real and open at the landed
  revision"). The r3 write guard held at the base throughout (self-aim, hardlink
  alias and the canonical profile aim all refused, exit 2, victim bytes
  unchanged), and legitimate writes beside a measured `.sha256` file still
  worked. After (first-hand at the landing, 14:10Z): the revised tool —
  `29bb45ae…`, 1343 lines, README `125e7e02…` — refuses **both** sidecar
  spellings at the declared usage class with the victim bytes re-derived intact
  and no derived-sidecar-of-a-sidecar created; the directory-creation shape reads
  the declared usage class with a named message and no traceback, while a fresh
  parent is still created and captured into; all three padded reference shapes
  (current receipt, legacy sums, legacy pipe) are refused with
  `reference covers 1 of the required 5 distinct paths` plus the coverage line
  naming the five unaccounted canonical paths, while a distinct-path reference
  still passes and the one-of-five refusal is unchanged; and the absence ruling
  landed in the gate README ("only error-carrying stanzas are `UNEVALUABLE`; a
  cleanly absent stanza on both sides is `MATCH`") with every both-absent row
  now annotated `the MATCH is an agreement on absence, not a verified presence`
  — so the round's compound finding (an all-absent reference reading clean) is
  now non-silent by construction. Selftest 22 → **28**
  (`CLEAN cases=28 passed=28 failed=0`), the new names covering the duplicate
  -stanza refusal, the distinct-five pass, both sidecar spellings, the
  directory-creation usage exit and the both-absent ruling. The round's own live
  pre/post pair is captured by the revised tool — both receipts self-pin
  `29bb45ae…`, captured-utc 2026-10-19T14:10:24Z, 5/5 present exit 0 — and
  verifies `MATCH 5/5` plain and under the coverage gate (pre sha `7f5a6fd5…`
  = its sidecar, post sha `2225f866…` = its sidecar; both sidecars re-derive);
  the pair was re-verified independently by this scribe against the landed
  instrument with the same verdict. The registry row is **patch text, not yet
  applied** (`SKILL.md` still carries the round-3 row), so the same-commit
  coupling is open at draft close. [[FILL: apply
  `claims/c3/EX-21/patch/proposed-skill-registry-row.patch.md` in the SAME
  commit as the tool + README (line-neutral; base `5eec51c0…`/390 L → patched
  `8e56f3d9…`/390 L), re-derive the settled tool + README identities at the
  commit point (rule #14 — the README moved three times inside the landing
  window while the tool digest stayed fixed)]]. Baseline re-measured at the
  records-side HEAD: command A reads
  83/83 files mapped, missing [], dangling [], 14/14 craft rules, 10.0/10.0; the
  census instrument reads PASS with zero stale/ambiguous/undeclared/unresolved
  loci; the citation probe unchanged (13/13 selftest, findings 0 both modes).
- Custody: [[FILL per CU-1 / the C3 landing: pre-pair capture time + 5/5,
  post-pair capture time + 5/5, the in-window drift comparison; any
  operator-side churn recorded verbatim, not repaired; custody paths read-only
  for every seat]].
- Scope: kaidoku repo only; no pushes (standing rule); no installs beyond C1's
  authorized vyper venv into the wave tree; custody paths read-only; scratch
  under `/var/tmp` or `/dev/shm` (the host `/tmp` quota exhaustion is standing).
<!-- END LITERAL ENTRY TEXT -->
