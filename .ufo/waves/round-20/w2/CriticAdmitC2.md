PARTIAL — the measured verb-count delta, five bound exercises, and README map control hold; C2’s universal carrier/subject-hash wording does not hold for `list-objdump-architectures`.

Axes: coverage (catalog/count and map integrity), calibration (what “uncovered” means), depth (operation-specific provenance and semantic limits).

## Evidence (revision-scoped)

**Observation — verb counts and target coverage.** I extracted `.ufo/waves/round-20/tools/verb-coverage.py` from S with `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/tools/verb-coverage.py` (exit 0), then ran the extracted script from `tempfile.mkdtemp()` against Git objects:

- `python3 -I -B /tmp/r20-c2-summary-lf3hsh1q/verb-coverage.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 14f0260ad319ecc26994381b2415d5a999003375` — exit 0; 128/153 named. All five target entries were 0 and `exercised:false`.
- `python3 -I -B /tmp/r20-c2-summary-lf3hsh1q/verb-coverage.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9` — exit 0; 133/153 named. Target entry/exercised results: inspect-wasm 1/true; compare-wasm 1/true; execute-rizin 2/true; list-objdump-architectures 1/true; project-harmony 1/true. Returned bound IDs and cited evidence files exist at S.
- `python3 -I -B /tmp/r20-c2-critic-cew51frg/verb-coverage.py --selftest` — exit 0, `SELFTEST: CLEAN cases=8`.

The temporary scripts were sourced from S and removed after use. The counter’s contract is the exact CLI-name/entry test; C2 itself labels this “mention-level” and not proof of mastery (`claims.json:27-29`).

**Observation — coverage-map control.** I loaded `controls-r20.py` from S, set its repository root to LANE, and ran its `command_a` against B and S Git objects via `/tmp/r20-c2-controls-64uyrwux/controls-check.py`:

- `python3 -I -B /tmp/r20-c2-controls-64uyrwux/controls-check.py 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 14f0260ad319ecc26994381b2415d5a999003375 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9` — exit 0. B: 97/97 mapped, missing/dangling empty. S: 102/102 mapped, missing/dangling empty; 17/17 citation rules resolve. `SELFTEST: CLEAN cases=12`.

This is 100% index integrity, not 100% REA-domain coverage: command A intersects knowledge-file stems with tokens in the README coverage-map section (`controls-r20.py:48-75`; `SCORECARD.md:88-122`). S’s map row groups the new entries at `corpus/README.md:69`.

## Novelty and counterexample

**Observation.** At the exact REA CLI-verb level, all five names were absent from B’s knowledge entries under the counter’s hyphen/underscore matching rule, and each has a retained entry at S. Do not inflate that into five wholly new domain concepts. B already held adjacent knowledge: EVMole’s WASM-bundled EVM operation (`corpus/knowledge/2026-10-13-r3-evm-interface.md:5-8,133`); Android application-graph projection and the shared Apple/Android `inventory_evidence` feed law (`corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:50,70`); and `inspect_with_objdump` `file_headers`, with other operations expressly unestablished (`corpus/knowledge/2026-10-16-l7-06-inspect-with-objdump.md:1,5,10`). The earlier Rizin note says Rizin was absent from PATH (`corpus/knowledge/2026-10-13-pe-surface.md:65-70`). These are adjacent, not prior holds of the five exact target operations; the new ground is operation- or format-specific.

**Counterexample — pathless objdump.** C2 says every target entry is from a run “on real (or recipe-retained synthesized) carriers” and cites a subject SHA-256 (`claims.json:25,27`). The target `list-objdump-architectures` takes no artifact: its entry explicitly records `subject:null`, provider version null, and host-output equality with `objdump -i` (`corpus/knowledge/2026-10-20-r20-objdump-architecture-list.md:1,9`). The jq digest belongs to the separate `inspect-with-objdump disassemble` companion run (`:11,16`), not to the pathless target Evidence. Thus the 5/5 `exercised` result is true by the counter’s ID/path/operation-token rule, but does not make this target carrier-bound or supply its subject SHA (`verb-coverage.py:136-163`). This is a fixable wording/provenance mismatch, not evidence that the host-inventory command failed.

**Weakest evidence.** `project-harmony-application-graph` is weakest for broad semantic capability: two recipe-retained synthetic ZIP/HAPs produce Stage/FA hints, but the entry says classification is path-presence only; the `.abc` is invalid placeholder text and no shipped package, HSP, App Pack, signing, or runtime semantics were tested (`corpus/knowledge/2026-10-20-r20-harmony-application-graph.md:9-12,22-26`). The earlier Android/Apple feed law further limits novelty to Harmony-specific behavior. It is admissible only as that narrow synthetic path-hint result, which the entry already states. `list-objdump-architectures` is instead weakest on subject-bound provenance: null is correct by design, and its independent `objdump -i` comparison supports the narrow host-inventory claim.

## Smallest safe correction

Keep the 128→133/153, 5/5, and 102/102 results. Narrow C2’s universal wording: require a subject SHA for subject-bearing runs; for pathless host-inventory verbs, record `subject:null` and require the independent host-command/output comparison. Define “uncovered” as exact CLI-operation or format-specific ground, not novelty of generic WASM, application-graph, or objdump concepts. Do not promote the HAP result beyond synthetic path-hint behavior.
