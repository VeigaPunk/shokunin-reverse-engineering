# Round 27 wave 1 — SiblingOverlap seat (KaidokuR27.SiblingOverlap)

Scope: read-only scan of 20 sibling lanes (every `*-shokunin` except kaidoku), `corpus/knowledge` and `corpus/SOURCES.md`, for evidence-ID identity, content addressing of tool output, package-version pinning of tool runs, and attributing an artifact to the tool version that produced it. Also tameshi `mte-report-interop.md` at f4e8f7d8, read against the C1 counter's red selftest. No installs or updates. No REA calls.

## Method (observation)

- Broad scan, 2026-10-22T14:54:57Z, exit 0: `grep -rilE '<broad pattern>'` over each lane matched 228 files. Generic words (`byte-identical`, `tool version`, `canonical`) made this mostly noise.
- Strong scan, 14:55:04Z, exit 0: `grep -rinE 'evidence[ _-]?id|ev_[0-9a-f]{16}|content[ -]address|content-keyed|rename[- ]sensitive|rea-agents|digestcanonical|semanticprojection|canonical digest'` matched 38 files in 15 lanes. Medium scan (version pin, producer origin, attribution), 14:55:12Z, exit 0.
- Sibling heads read: revenger 876630db, tameshi 06b59b93, game-dev-3d 89dd182b. Tameshi f4e8f7d8 resolves to f4e8f7d835a8e33c64a87ff93e79da32264f031c (2026-10-22T06:40:33-03:00). `git show f4e8f7d8:corpus/knowledge/mte-report-interop.md | sha256sum` gives b173e3e5…0fac (170 lines).

## Hits and dispositions

Dispositions: cite (kaidoku may name it as fleet prior art), adjacent (related or contested scope; report it, do not absorb it), reject (same words, different object).

| Lane | path:line | Short quote | Disposition |
|---|---|---|---|
| revenger | corpus/knowledge/digest-scope-versus-provenance.md:33-38 | "Evidence ID shows internal consistency only where it is recomputed against named bytes … does not establish producer origin" | cite for C2: sets the boundary between attribution by rule fit and producer origin |
| revenger | corpus/SOURCES.md:29 (S015) | "Evidence IDs were rejected as proof of producer origin; they show internal consistency only." | cite for C2, through the C13 entry above |
| revenger | corpus/knowledge/tool-validation-by-function-and-version.md:23 | "A validation result binds the named function in the named version, not the product." | cite for the C1 and C2 limits (one pin, named verbs) |
| revenger | corpus/knowledge/evm-saved-interface-candidates.md:168 | "Full Evidence IDs (recorded, not recomputed)" | adjacent: rea-agents 6.4.0 ids that revenger records but never recomputes; kaidoku recomputes. Not C1 evidence |
| revenger | corpus/knowledge/commonjs-destructured-require-edges.md:204 | "digests bind the hashed bytes only; Evidence IDs are recorded identifiers" | adjacent (same stance as above) |
| revenger | corpus/knowledge/utf16-unpaired-surrogates-in-resource-names.md:116; pe-resource-directory-layout.md:155 | "Evidence ID … cited only for the saved bytes; no producer-origin or rerun claim" | adjacent; reject as identity evidence (6.4.0, PE verb, not recomputed) |
| revenger | corpus/knowledge/2026-10-12-rea-readiness-checklist.md:37-38; seed.md:60 | "`npm view rea-agents version` → 6.7.0 … package `rea-agents@6.5.0`" | adjacent for C2: 6.4.0, 6.5.0 and 6.7.0 are all in use on this host |
| tameshi | corpus/knowledge/verification-patterns-fleet.md:102 (also :35, :73-74) | "U4 — ev-id nuance: r9-02 header (renamed byte-copy, same id) vs QUALITY.md:24 path-sensitivity … unresolved" | adjacent (contested): an open contradiction that the C1 renamed run tests for 16 pairs. Second-hand retelling of kaidoku's own records (QUALITY.md:24 is kaidoku's row 14), so cite kaidoku's primary records, not this |
| tameshi | corpus/knowledge/incremental-pin-disposition.md:109-110 | "a missing repo/rev/blob or a pin mismatch is a SETUP refusal, never a pass" | cite as precedent for pinning the recompute oracle (finding F1) |
| tameshi | corpus/knowledge/guard-kill-closure.md:105 | "`tools/bash-witness-study.py` is pinned at `49e9e5e2…` in `.ufo/evidence/round-13/expected.json:11`" | cite as precedent for hash-pinning a helper that a gate reads |
| kotoba | corpus/knowledge/substrate-pin-guard-round23.md:3-8 | "the `measured_against` pins … had **zero readers** … corrupting the omp sha … left every gate green" | cite: same failure class as finding F2 (a pin that nothing reads back) |
| game-dev-3d | corpus/knowledge/rea.md:6, 11-14, 53 | "`npx -y rea-agents@6.4.0` … That lane [revenger] owns REA-as-an-end" | adjacent (contested scope): names revenger, not kaidoku, as the REA owner. Kaidoku PROVINCE.md:240/303 already lists kaidoku/revenger arbitration as open |
| kumitate | corpus/knowledge/kimi-config-plane.md:257; kimi-mcp-plane.md:62 | "`args = [ "-y", "rea-agents@6.4.0", "mcp" ]`" | reject: a config inventory of an MCP launcher pin, not run attribution |
| tabi | corpus/knowledge/browser-surface-census.md:129 | "args `["-y", "rea-agents@6.4.0", "mcp"]`" | reject (same as the kumitate row) |
| kumitate | corpus/knowledge/live-surface-probe.md:121-142 | "Two digests, one pin … defined over the CANONICAL digest" | reject: a manifest pin, not tool-output identity (a loose analog to C2's canonical-digest choice) |
| kumitate | corpus/knowledge/pinned-evidence.md:5 | "pinned evidence — the revision a verdict scored" | reject: source-revision pin for gate verdicts |
| kumitate | corpus/knowledge/distill-and-l3.md:8; native-judge-pipeline.md:94 | "sorted/deduped evidence ids" / "content-addressed distiller artifact digest" | reject: kumitate's own proposal ids |
| kasegi | corpus/knowledge/triage-thresholds.md:377; mission-ledger.md:108 | "`board_ref.evidence_id` pattern `^[0-9a-f]{64}$`" | reject: board-snapshot ids |
| kotodama | corpus/knowledge/synthesis/glossary-registry-format.md:44 | "`evidence_ids`" | reject: glossary evidence links |
| mori | corpus/knowledge/verdict-machine-r6.md:51 | "R2 — content-keyed forgery." | reject: "content-keyed" means fixture-memorizing forgery there |
| mori | corpus/SOURCES.md:67 (S061) | "content-addressable object storage as explanation of git hashing" | reject: git objects |
| kama | corpus/SOURCES.md:80, 300 (S068); served-identity-crosswalk.md:45 | "NAR serialization of content-addressed store objects" | reject: Nix and Ollama stores |
| mado | corpus/SOURCES.md:109 (S097); theme-route-r18.md:167 | "per-fetch GitHub tree-page HTML digests that rotate between fetches" | reject: web-page fixity |
| kengaku, audio, tsukuroi, mado (xdg) | kimi-model-routing-round18.md:26; sox-autodetect…ordering.md:114; root-dac-correction-r13.md:200; xdg-portal-routing-r12.md:13 | "json-canonical digest" / "content-keyed" / "Evidence identity" / "evidence ID `E-PT-PORTAL-HOST`" | reject: same words, unrelated objects |

No sibling lane computes, recomputes or compares REA evidence IDs across paths or across package versions (observation, from the strong scan: every REA id hit is recorded or cited only).

## Tameshi mte-report-interop.md at f4e8f7d8, read against the C1 red selftest

The source lines are data. Each finding below names its producing command.

- :21 "`score` is a sanity check that holds by construction", and :138-140, which pin the vendored libraries ("a new release or an offset pin requires re-verification"). The question this raises for C1: is the counter's id oracle pinned?
  - Observation: `c1-rename-identity.py:110-113` loads `tools/round-26/recompute-ids.py` with `git show <REV>:<path>` and no hash check. `claims.json` `instruments` pins only the two counters.
  - Today the file is unchanged: sha256 89afa375…208b at the worktree, at cd32264f and at a4f674b3 (`sha256sum` / `git show … | sha256sum`, 14:56:43Z, exit 0).
- F1 (attack on the red selftest case `forged-id-consistent`): **fails**.
  - Producing command: `TMPDIR=$PWD/tmp python3 -I -B oracle-pin-probe.py`, 2026-10-22T14:57:23Z, exit 0.
  - The probe imports the pinned counter unmodified (sha e0a07995…bb7) and builds the counter's own `_build_green` fixture in seat scratch. It applies the selftest's `forged_id` mutation plus a 2-line `recompute-ids.py` that returns the stored id, committed at the same REV.
  - Output: `forged-id+stub exit=0 rows_complete=16/16 entry_ok=1 rev=HEAD`.
  - Counterexample: a REV that edits both the envelope ids and the recompute file passes the C1 counter.
- :169 `balanced-flip-same-counts` (counts agree but ids are swapped): **holds** for C1. Same run: `balanced-flip exit=1 rows_complete=14/16`, with `INCOMPLETE jq analyze: table verdict rename-sensitive, derived content-keyed`. The verdict is re-derived per row (counter :300-312).
- :154-155 (a bogus status is silently dropped): **holds** by code reading (inference, not run). Any table verdict outside the derived one fails at :311-312.
- :51-52 (ambiguous input is a SETUP refusal, not a judgement): the counter has this path (exit 2 on header drift: `header-drift exit=2 input error: runs.tsv header differs from frozen header`). None of the 21 selftest cases expects exit 2 (observation, counter :528-551), so the selftest never exercises the refusal path.
- F2 (inference, a kotoba substrate-pin analog): the 6.5.0 package pin has no byte-level reader. The counter compares `runs.tsv` `pkg_version`/`pkg_json_sha256` (typed by the seat) with constants. The envelopes carry no rea-agents version: `corpus/evidence/round-26/c1/envelopes/analyze-base.json` meta keys are `['command', 'duration']`, and the only version strings are "1" and "12.1.4" (14:58:05Z, exit 0).

## Overlap verdicts

| Claim | Verdict | Basis |
|---|---|---|
| R27-C1 (evidence-ID identity across rename, 8 verbs, 2 carriers, 6.5.0) | adjacent | No sibling measures or recomputes this. Tameshi U4 names the same open question but retells kaidoku's records. Game-dev-3d's REA-ownership line is contested scope, already open in kaidoku PROVINCE |
| R27-C2 (attributing an envelope to the 6.5.0 or 6.7.0 rule) | adjacent | Revenger C13 and S015 state the boundary (ids do not prove producer origin), which the C2 limits already respect. No sibling attributes artifacts to a tool version |

## Proposed move (one, bounded)

Close F1 and F2 without re-defining any frozen rule. This improves C1 evidence strength and gives C2 real use; it changes no claim text.

1. The L1 or reviewer receipt records `git diff --exit-code cd32264f <REV> -- tools/round-26/recompute-ids.py` (exit 0) beside the C1 count. That makes the oracle pin explicit, as tameshi's SETUP-on-pin-mismatch does.
2. Synthesis: run C2's `xpin-attribute.mjs` over the 48 C1 envelopes as a supplemental receipt. Each must attribute `6.5.0` or `both`. This gives the self-reported package pin a reader derived from the bytes, and checks the recompute oracle against the package's own `digestCanonicalValue`.

Risks:
- `both` cannot tell the two versions apart. If the 6.5.0 and 6.7.0 rules agree on these envelopes, the pin reader is weak.
- The receipt must stay outside the counted claim, or it re-defines the frozen rules.
- Unknown: whether `c2-xpin-check.py` loads any helper from REV in the same unpinned way. Not inspected.

Verification: the main agent runs the diff in step 1, and `xpin-attribute` over the C1 envelopes once they exist.

## Artifacts (seat scratch)

- `/fast/scratch/hyaku/kaidoku-r27/seats/SiblingOverlap/oracle-pin-probe.py` sha256 c08387af310ce3336b0c3601481bcdf6fca60dcb03fa509c6581f5ccde7b5227
- `/fast/scratch/hyaku/kaidoku-r27/seats/SiblingOverlap/probe-output.txt` sha256 db42762cf4ad3b56244a79807b4d3b9abc2abff1b34c066f938457a80ccd1d8f

The probe removes its own fixture clones. Nothing in the lane was edited except this report.
