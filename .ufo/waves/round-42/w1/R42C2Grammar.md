# R42C2Grammar — v4 grammar and precedence review before the freeze (A1)

Verdict: **DONE** — the A1 15-step precedence encodes exactly as a first-match
table under the L1 grammar decision (13th `failing handler` column over HF,
`handler` cell over F, deps contains form), verified exhaustively: **0
divergence classes over a 4,478,976-tuple sweep** between the reference
precedence implementation and the two-column table emulator. The one-column
variant it replaces diverges in **19 classes** (enumerated below, frozen-tool
confirmed on 7 vector witnesses). 68 feature-tuple vectors covering every step
boundary incl. legacy handlers, container and residue are delivered as
`artifacts/R42C2Grammar/vectors-v4draft.json` (sha256
`b99cd74af78071cc90d9bfc69e2cbd0f27d029600c70a33bec7438a08875f62b`), usable by
the interpreter and evaluator seats' selftests via `build-envelope.py`.

Built against amendment A1 from the first artifact (the L1 amendment arrived
before anything was written; no pre-A1 delta section is needed).

## 1. Scope and method

Item: can the A1 label precedence (`plans/round-42-claims.md` `## R42-C2`,
steps 1–15) be encoded as a first-match table with a handler glob; which steps
need order; where do mixed chunk sets (a v3 and a v4 chunk in one envelope; a
failing v3 chunk beside a clean v4 chunk) diverge between the precedence and a
handler-glob table. Feature-level review only: no REA/unblob run, no carrier,
no lane write outside this report and `artifacts/R42C2Grammar/`. No tool was
installed or upgraded (stdlib Python only; the tooling-authorization ledger is
therefore empty).

Method: (a) hand-derived the (label, action, step) for 68 vectors from the A1
text; (b) wrote an independent reference implementation of the 15 steps
(`ref-eval-v4draft.py classify()`); (c) emulated the table grammar (two-column
A1 and one-column pre-decision variants) and swept the whole bounded feature
space (H ⊆ {squashfs_v3, squashfs_v4_be, squashfs_v4_le, squashfs_v4_broadcom,
trx_v1, cpio}; HF ⊆ H; G ⊆ {missing-extractor-dependency, extractor-failure,
depth-limited, unpublished-entry, encrypted-chunk, unknown-chunk-handler};
D ⊆ {sasquatch-v4be, sasquatch, unsquashfs}; BE ∈ {yes,no,n/a}; SR ∈ {no,yes};
P ∈ {0,7}); (d) confirmed the one-column emulator against the FROZEN round-41
interpreter `tools/round-41/sqfs-triage-v3.py` on 11 built envelopes; (e) scored
the draft's control-table variants on the vectors.

## 2. Findings

**F1 — the one-column encoding is wrong; the 13th column closes it (verified
exhaustively).** Steps 6/7 test the FAILING chunk's handlers (`squashfs_v4_be`
∈ HF; HF ∩ L ≠ ∅), but a round-41-style table's single `handler` cell fnmatches
the run-wide SquashFS set F. On any envelope with a clean sibling chunk of a
different family the glob table fires the wrong failure row, and no row order
fixes both directions: {legacy failing, v4_be clean} needs legacy-before-avm
while {v4_be failing, legacy clean} needs avm-before-legacy. The complete
one-column census (4,478,976 tuples) has **19 divergence classes**; the largest:
ref `dep-missing-be` → table `partial-body-failure` (207,360 tuples, D-superset
fall-through), ref `body-extractor-failure` → table `legacy-body-failure`
(155,840), ref `dep-missing-be` → table `unknown-residue` (207,360). Vector
witnesses V18, V29, V36, V40, V41, V43, V44; the FROZEN round-41 interpreter
reproduces the one-column emulator's (wrong) pair on all seven
(`frozen-interp-check.tsv`, emulator_fidelity=True on 11/11). The two-column
A1 table (failing-handler glob over HF, `*` matches anything incl. empty HF)
has **0 divergence classes over the same sweep** — with the row order = step
order it is equivalent to the precedence, not merely on the vectors.

**F2 — step 4's "D holds" requires the deps contains form; the v3 grammar
refuses it.** The frozen v3 grammar rejects a contains cell in `dependencies`
(`sqfs-triage-v3.py` selftest `c_deps_cell_has_no_contains_form`), so the v4
interpreter must lift that refusal and parse `sasquatch-v4be+` / `sasquatch+`
as membership, be-arm tested first. Without it, exact-set dep cells send every
D-superset envelope past both dep rows (the round-41 K6/K7 divergence, F1 of
`w2/R41W2C2Table.md`). CTL-C2-4 (exact sets only) kills 14/68 vectors
(`controls-check.json`) — the contains form is load-bearing, as in round 41.

**F3 — the `handler` cell semantics change scope: glob over F, `none` = F
empty, and the v4 interpreter's H must union gap handlers.** The frozen v3
interpreter collects H from `chunks[].handler` only, squashfs-prefixed
(`sqfs-triage-v3.py` `features()`), while the A1 feature paragraph defines
H = chunks ∪ gaps handlers and F = the `squashfs_` subset. A v4 interpreter
that keeps the v3 collection misses a handler that appears only on a gap (its
`none` cell would wrongly match F=∅). The prefix must be `squashfs_` (with
underscore) per A1. Both frozen tools read my built envelopes consistently
because every vector handler sits on a chunk; the seats' selftests should keep
that realization or fix H-union first.

**F4 — `decides` vs `reached` (wording pin for the knowledge entry).** A step
whose guard is evaluated and fails (step 4's else-continue; step 6's BE=no
guard) does not decide the pair. The vectors carry `decides` (the firing step,
mechanically checkable) and `reached` (V19/V22/V23 reached 4; V28/V29 reached
6). The draft text is first-match and unambiguous, but a transcriber reading
"step 4 … else continue" as a decision would mislabel; one sentence in
`corpus/knowledge/2026-10-26-r42-sqfs-triage-v4.md` pins it.

**F5 — HF fallback = F (A1) vs the v3 evaluator's fallback = H: equivalent for
steps 6/7, but pin the declared value.** L ⊆ F ⊆ H and `squashfs_v4_be` ∈ F ⟺
∈ H, so no tuple classifies differently under the two fallbacks. But the
DECLARED tuple differs: `declared_features` should carry the post-fallback HF
(so the counter's observed==declared equality is well-defined), or both sides
must apply the fallback identically. Related (R41-CL1 interaction): the
round-41 counter's canonical tuple has six fields; mixed-chunk combos are
undeclarable without HF as a seventh field — a combo with a legacy and a v4_be
chunk cannot say which failed, so steps 6/7 are unpinnable from its declared
tuple. The generator/counter seats must add it.

**F6 — `failing handler` `*` matches an empty HF: unreachable but harmless.**
HF = ∅ as a value arises only via the fallback HF = F with F = ∅, and F = ∅ is
decided at steps 2/3 before any failure row. Pin it in the interpreter doc so
the cell's semantics are total.

**F7 — order: 33 of the 91 step pairs overlap; 7 adjacent relations are
load-bearing.** Adjacent load-bearing (a swap changes some tuple): 2→3
(container vs no-squashfs), 4→5 (dep vs partial), 6→7 (avm vs legacy),
7→8 (legacy vs body), 8→9 (body vs residue), 9→10 (residue vs depth),
10→11 (depth vs mixed). Adjacent order-free (guards disjoint): 3→4, 5→6,
11→12, 12→13, 13→14, 14→15. Non-adjacent load-bearing pairs the adjacency list
does not imply: 4<6, 4<7, 4<8, 4<9, 4<10, 4<11, 4<15, 5<9, 5<10, 5<11, 5<15,
6<8, 6<9, 6<10, 6<11, 6<15, 7<9, 7<10, 7<11, 7<15, 8<10, 8<11, 8<15, 9<11,
11<13, 12<14 (full matrix with witnesses: `sweep-census.json` `order_pairs`).
Steps 1 and 15 share the pair (`unclassified`, `none`): the table realizes both
by pinning OP/PR on every row plus the no-match fallback — no dedicated row.

**F8 — the legacy glob must be `squashfs_v[123]*`, not `squashfs_v3*` and not
`squashfs_v*`.** unblob 26.6.4 legacy names (`handlers/filesystem/squashfs.py:102,159,200,245,319,364,410`):
`squashfs_v1`, `squashfs_v2`, `squashfs_v2_nonstandard`, `squashfs_v3`,
`squashfs_v3_ddwrt`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`;
`squashfs_v1`/`squashfs_v2` carry no `_` suffix, so `squashfs_v[123]_*`
under-matches, and `squashfs_v*` over-matches `squashfs_v4_broadcom` (a v4
handler that must land in `body-extractor-failure`, V42). A1's L definition
(v1*/v2*/v3*) is exactly `squashfs_v[123]*`. Vectors V34/V35 pin the breadth.

**F9 — controls behave as the draft intends (vector-level sanity).**
CTL-C2-0b (v3 table) kills 31/68; CTL-C2-4 14/68; CTL-C2-8 10/68 (exactly the
legacy-failure vectors); CTL-C2-9 16/68 (every legacy-only-chunk vector —
R41-CL4 resurrected, as designed); CTL-C2-10 exactly the 8 container/residue
vectors (V04–V08, V48–V50). CTL-C2-7/7b need the dev tuple inventory and are
the control seats' to score.

**F10 — the frozen v3 evaluator confirms the A1 motivation on built envelopes.**
`indep-eval-v3.py` on V04 → `no-squashfs-chunk` (step 2), V31 →
`no-squashfs-chunk` (step 2 — R41-CL4 verbatim), V36 → `body-extractor-failure`
(step 6, no legacy row), V48 → `unclassified` (step 12, no residue row). All
four are the envelopes A1's new rows exist for.

## 3. Deliverables and how the seats use them

- `vectors-v4draft.json` — 68 vectors, every step 1–15 has deciding vectors;
  fields: `id`, `decides`, optional `reached`, `tag`, `note`, `features`
  {OP, PR, H, HF, G, D, BE, SR, P}, `expected` {label, action}; `_pinned`
  records the membership/HF-fallback/glob pins. Structural invariants checked:
  HF ⊆ H, D nonempty ⇒ dep gap present, HF nonempty ⇒ extractor-failure present.
- `ref-eval-v4draft.py` — `--vectors` (validate), `--glob` (run a table file
  over the vectors), `--sweep` (order matrix + census), `--controls`,
  `--frozen-check`, `--selftest` (20 asserts). The interpreter seat can diff
  its table parse against `glob-table-v4draft.md`; the evaluator seat can diff
  its classify against `classify()`; both can run the vectors as their selftest.
- `build-envelope.py` — vector → synthetic REA envelope readable by both frozen
  round-41 tools (realization choices documented in its docstring).
- `glob-table-v4draft.md` (A1 two-column reference transcription),
  `glob-table-onecol-v4draft.md` (the diverging variant, kept as the
  enumeration witness), `glob-table-v3-transcribed.md` (CTL-C2-0b emulation).
- Generated evidence: `sweep-census.json` (order matrix + 19-class census,
  sha256 `a4f4a47263d18bf594e92cd39a1df6d4da0d2d40f0537a8d90d02690f67d276b`),
  `onecol-vector-divergences.json` (`e25f398e4309d8e361b195e583f7a6b31ddad8622dc90521f1def34b7992402a`),
  `controls-check.json` (`ed94e1320b992a951c331e7ef8726317587c9009591cfa7e4338f106bd4c6d30`),
  `frozen-interp-check.tsv` (`be70daa522b43736f85f4efa88e40413cc584ac7b09270e0b49ce17662bb73a9`).

Commands (all exit 0 unless noted; scratch `/fast/scratch/hyaku/kaidoku-r42/R42C2Grammar`, removed):
`python3 -I -B ref-eval-v4draft.py --selftest` → `selftest ok: 20 checks`;
`python3 -I -B vectors-src.py` → `68 vectors, steps covered [1..15]`;
`--vectors vectors-v4draft.json` → `68 checked, 0 failures`;
`--glob glob-table-v4draft.md …` → `68 vectors, 0 divergences`;
`--glob glob-table-onecol-v4draft.md …` → `7 divergences` (V18 V29 V36 V40 V41 V43 V44);
`--sweep` → `4478976 tuples; order pairs 33; divergence classes 19; two-column 0 classes`;
`--controls` → the F9 counts; `--frozen-check …` → 11 rows, emulator_fidelity True.

## 4. Residual risks and verification gaps

- The two-column equivalence is verified against MY emulator of the L1-stated
  cell semantics, not against the v4 interpreter (not yet written); the
  interpreter seat must implement: failing-handler glob over HF with
  `*`-matches-empty, handler glob over F with `none` = F=∅, deps contains form,
  H unioning gap handlers, row order = step order. Any deviation reopens F1/F2.
- Sweep space is bounded (6 handler names, 6 gap kinds, 3 dependency names,
  P ∈ {0,7}); unbounded names (e.g. a future `squashfs_v5_*`) are outside it —
  the grammar handles them by the same globs, but the census does not cover them.
- Whether REA mints one `extractor-failure` gap PER failed chunk (so HF can hold
  two names, V30) is [INFERENCE] from S119 `FirmwarePublication.js:288-293` and
  the v3 table cause text; no real multi-chunk REA envelope is in the corpus to
  confirm. The HF-set formulation is correct under both readings.
- `unknown-chunk-handler` and the `.unknown` residue file are taken from the A1
  text and `w1/R42CritC2Draft.md`/`w1/R42C2ReconCombo.md` as cited there; I did
  not re-verify the REA kind string against the 6.5.0 package myself.
- Feature-level only: the diagnostics-shape axis of SR/BE extraction (round-41
  K8/K9/K10) is the interpreter/evaluator seats' to close; my vectors express
  features, not envelope bytes.
