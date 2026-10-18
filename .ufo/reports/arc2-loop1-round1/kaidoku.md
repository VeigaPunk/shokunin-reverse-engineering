# kaidoku arc2-loop1-round1 — freshness/operability/depth: carried-debt closure + custody pair + custody rule

Date: 2026-10-18. Wave: 64 seats (18 first-attempt on opencode-go + 46 devin
replacements per the operator directive of 2026-10-18), parent-integrated, no
seat commits; seat reports under `.ufo/waves/arc2-loop1-round1/`. Work
commits: `58116aa` (content + receipts, lane identity) and `df31bfb` (wave
artifacts, lane identity) — this report lands after them and cites them
(lands-last, `PROTOCOL.md:117-122`). Report path follows the lane's standing
wave-dir convention (`.ufo/reports/<wave>/kaidoku.md`, used since round 5;
R5-D3 deviation from the fleet `round-<N>` template recorded for the
integrator; the literal `round-1` path holds the blocked interactive-r1
report).

## Work performed

Declared claims (3, distinct axes, causally separable — separability proved
`C1.md`, counterfactual directions observed `CR6.md`):

1. **C1 — freshness** (fleet axis, unowned proxy): r3-jq-provenance
   safety-label loci `:60`,`:136` scoped by an append-only byte-identity +
   recorded-provenance, non-endorsement qualification (form of
   `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:244`; the only draft
   passing CR1's three-limb boundary test — E6's text via CR1 §3); stale
   `PROVINCE.md:107-109` pointer in `corpus/lessons/2026-10-15-round-1.md:152`
   covered by an append-only correction note (CR2 §5 text; describe-never-
   command); `SCORECARD.md:79` adjudicated NO-CHANGE-with-cause (baseline-
   revision-correct under `SCORECARD.md:16-17`; in `## Open gaps`, not the
   frozen :39-49 table — E4's correction to the earlier "frozen table"
   wording).
2. **C2 — operability** (fleet axis, unowned proxy; capability acquisition):
   config custody pre/post-pair around the live battery — three client
   configs sha256-frozen pre-dispatch (14:49:13Z) and re-verified after the
   battery closed (receipt 16:52:56Z), zero drift; closes the luna-round-8
   no-pre-pair defect (`SCORECARD.md:544-545`; `LOG.md:856-858`). Wave-wide
   agreement: 18+ capture instants across 7+ seats, all byte-identical
   (`CR8.md`).
3. **C3 — depth** (owned axis; most-falsifiable tie-break of the saturated
   10.0 three-way): `SKILL.md` queue-drain craft rule #10 — a live-probe
   round's zero-drift claim requires a same-round pre/post-pair (R4's merged
   text); bounded by the already-landed luna-round-8 record
   (`corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:15`;
   `SCORECARD.md:544-545`; `LOG.md:856-858`), deliberately not this round's
   receipts. Plus the custody SOP as its own `##` section (E12's text;
   placement avoids command A counting it as a craft rule — E12's measured
   hazard).

Work items (evidence pointers):

- **C1(a):** independent census sweeps agree on exactly two unqualified loci
  (`E1.md`, `V1.md`, `C2.md` connector, `CR5.md` — 13-token wide sweep);
  qualification note appended at EOF, prefix-identity proven against the
  frozen 8453-byte base (`697804b5…`, blob `ed838ba5`).
- **C1(b):** correction note appended after line 160, prefix-identity proven
  against the frozen 8568-byte base (`71e003e8…`, blob `0cb945bd`); both
  drafts dry-run-verified (`E10.md`, `CR2.md`); index needs no edit (`E9.md`).
- **C2:** pre-pair parent-captured before any dispatch; corroborated 3-way
  (E11, V4, V5) plus wave-wide scan (`CR8.md`); post-pair captured by the
  parent after all three legs closed; `sha256sum -c` 3× OK on both receipts;
  leg artifacts copied from seat scratch into committed receipts with a
  `sha256sum -c`-checkable `MANIFEST.txt` (E13's layout).
- **C3:** rule inserted after `SKILL.md:195`, pure additive (61/0 numstat);
  command A replay at `df31bfb` below.
- **Live battery:** leg 1 `doctor` — exit 1, `healthy:false`, 11 ok / 11
  not-ok scope_checks, identity 6.5.0 / 207 / 153 (`E24.md`; raw capture
  `receipts/leg-1-doctor.txt`); leg 2 `binary_session {}` — 207 MCP / 153
  CLI, `tools_sha256 805433f1…`, closed clean, server exit 0 (`E25.md`;
  `receipts/leg-2-*.json`); leg 3 pinned libjq `7e8bccc6…` open → decode
  `0x117070` = `f30f1efa`/ENDBR64 → export 18991 B → close `{"result":
  null}`, exit 0 (`E26.md`; `receipts/leg-3-*.json`); zero residue (`E28.md`).
- **Cross-domain evidence (domain noted):** the operator-owned configs read
  by C2 belong to the Devin/OMP/Kimi client domains — SC2's census refutes
  PROVINCE.md's Kimi pin (live `rea-agents@6.7.0` at `config.toml:2940`,
  drift bounded 2026-10-16 → 2026-10-18 08:56:45); routed as carried debt,
  not absorbed. The battery targets the REA-toolchain domain. No sibling repo
  touched.
- **Adversarial record:** CR1 (disguised-verdict attack — failed against the
  landed text), CR2 (append-only purity — holds, with E8 disqualified as
  imperative), CR3 (security-theater attack — refuted on facts: the kimi
  config was rewritten 3m16s before the pre-pair; residual value stated
  honestly), CR4 (generic-advice attack — no violation; legibility gradient
  noted), CR5 (census completeness — r3 complete; README :90/:160 deferred;
  the naive census instrument has two proven defect modes and was NOT
  landed), CR6 (separability — refuted), CR7 (no smuggled exploratory
  claims), CR8 (provenance/forgery — 18-instant agreement; residual holes
  closed by the committed post-pair).

## Landed changes

- `corpus/knowledge/2026-10-13-r3-jq-provenance.md` — append-only
  "Safety-verdict scope" note naming `:60` and `:136`; historical bytes
  prefix-identical (8453 B base). LOG: this round's entry; commit `58116aa`.
- `corpus/lessons/2026-10-15-round-1.md` — append-only pointer-refresh note
  (baseline-correct at `6645585`/`c265db9`, stale at HEAD; refusal now
  `PROVINCE.md:114-116`; drift commit `7125dd4`); prefix-identical (8568 B
  base). LOG: this round's entry; commit `58116aa`.
- `SKILL.md` — queue-drain craft rule #10 (after `:195`, zero deletions) +
  `## Config custody for live-probe rounds (SOP)` section. LOG: this round's
  entry; commit `58116aa`.
- `SHONEN.md` — box-1 and box-4 evidence-line pointer refresh (:6, :12) in
  the same commit as the SKILL landing (Z2's same-commit dependency). Commit
  `58116aa`.
- `SCORECARD.md` — this round's section + capability row (entered; conditions
  per `AXES.md:62-64` met); `SCORECARD.md:79` left byte-identical
  (NO-CHANGE-with-cause). LOG: this round's entry; commit: this report's
  commit.
- `LOG.md` — this round's append-only entry. Receipts
  `.ufo/waves/arc2-loop1-round1/receipts/` (pre/post-pair, leg artifacts,
  MANIFEST) committed TRACKED at `58116aa`; wave seat reports at `df31bfb`.
  No config edits, no pushes, no writes outside this repo.

## Before → after measurements

- **C1(a) census** — unqualified safety-label loci in
  `corpus/knowledge/2026-10-13-r3-jq-provenance.md`: **2 → 0** (`:60`, `:136`
  both named by the appended note; bytes retained). Counting command:
  case-insensitive `grep -niE 'benign|malicious|safe|trust'` sweep with the
  `**Safety-verdict scope` marker asserted present (CR5's fixed instrument;
  the naive pointer-presence form is not used — CR1). Measured at `df31bfb`:
  marker count 1; both loci named; "not an absence-of-malice" clause present.
- **C1(b) pointer** — lesson `PROVINCE.md:114-116` count 0 → 1; the
  historical `:152` token remains (superseded append-only); uncovered stale
  loci 1 → 0. `SCORECARD.md:79` 1 → 1 (NO-CHANGE-with-cause).
- **C2 custody pair** — pre: `receipts/config-pre-pair.txt`
  (2026-10-18T14:49:13Z; devin `16f496e6…`, omp `38d2a1d0…`, kimi
  `3546e033…`); post: `receipts/config-post-pair.txt`
  (2026-10-18T16:52:56Z) — drift **0/3 files**. Counting command:
  `tail -n +2 receipts/config-{pre,post}-pair.txt | sha256sum -c -` → 3× OK,
  rc 0 (observed this session on both receipts).
- **C3 rule census** — command A (`SCORECARD.md:92-123`): rules **9 → 10**,
  citation_resolved_rules **9 → 10**, depth_score 10.0 both sides. Before at
  `4b806e14`: `{"citation_resolved_rules": 9, "rule_blocks": 9, "mapped": 79,
  "knowledge_files": 79, "missing": [], "dangling": [], "coverage_score":
  10.0, "depth_score": 10.0}`; after at `df31bfb`:
  `{"citation_resolved_rules": 10, "coverage_score": 10.0, "dangling": [],
  "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [],
  "revision": "df31bfb", "rule_blocks": 10}`.
- **Side-harm check** — command A at `df31bfb`: mapped 79/79, missing [],
  dangling [], coverage 10.0; calibration unchanged. Append-only proofs:
  `head -c 8453` / `head -c 8568` prefix sha256s match the pre-edit blobs
  (gates run pre-commit).

## SHONEN — all four boxes retained [~]

- [~] Decision tables/error patterns/checklists, cited sources: ten
  queue-drain rules in the section at `SKILL.md:81` (rule #10 added after
  `:195`); citations resolve — command A 10/10 at `df31bfb`; no semantic
  audit, no outside verifier (`SHONEN.md:5-6`).
- [~] End-to-end task executed and logged: this round's three-leg live
  battery (doctor / 207-153 census / libjq `0x117070` ENDBR64
  decode+export+close) — `E24.md`, `E25.md`, `E26.md`; receipts
  `.ufo/waves/arc2-loop1-round1/receipts/` + LOG entry this round; the
  2026-10-15 libjq smoke remains at
  `evidence/round-1-2026-10-15/rea-bundle.json`; no outside verifier
  (`SHONEN.md:7-8`).
- [~] Executable without oral context: counting recipes replay from the
  record (`SCORECARD.md:92-123`); this round's custody procedure is written
  into `SKILL.md` as the SOP section; documentation-level only
  (`SHONEN.md:9-10`).
- [~] No cross-domain bleed: refusal/adjacency boundary `PROVINCE.md:88-116`
  (safety refusal `:114-116`; this round's r3 erratum and lessons note
  enforce the safety-label scope); contested RE ownership (SC2's Kimi-pin
  refutation) routed as carried debt, not absorbed — no complete outside
  audit (`SHONEN.md:11-12`).

Gate `../PROTOCOL.md:63-72`: lane-dispatched seats are still the lane; `[x]`
needs a named non-author verifier — none exists; all four boxes stay `[~]`.

## Verdicts

- freshness: **improved** — 2 unscoped safety-label loci → 0; correction note
  landed; `SCORECARD.md:79` NO-CHANGE-with-cause.
- operability: **improved** — pre/post-pair custody demonstrated end-to-end;
  zero drift; closes the luna-round-8 defect; capability row entered.
- depth: **improved** — rules 9 → 10, 10/10 resolvable at `df31bfb` (finite
  proxy stays 10.0).
- coverage / calibration: **unchanged** (measured at `df31bfb`).

Round admitted: all three claims verified at the landed commits, no axis
harmed. First round of the reset stagnation window; window 1/10.
