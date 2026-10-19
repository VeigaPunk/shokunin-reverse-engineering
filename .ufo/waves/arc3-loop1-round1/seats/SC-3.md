# Seat report — SC-3 | chain c1 | role scribe

Wave: arc3-loop1-round1 (kaidoku-shokunin) | Date: 2026-10-19 | Status: COMPLETE
(drafts landed; parent-only values marked [[FILL]])

Task per seat line: records drafts for the PARENT (not applied) — a LOG.md
entry draft + a SCORECARD.md round-section draft for arc3-loop1-round1 C1,
two files under `claims/c1/records-drafts/`. Nothing else written.

## 1. Work performed (each bullet with an evidence pointer)

- Read the frozen claims/roster/rules (`claims-frozen.md:1-104`); confirmed
  seat identity SC-3, chain c1, scribe. Read the repo `AGENTS.md` (5 lines)
  and the format authorities: LOG.md recent entries (`LOG.md:1258-1394`),
  SCORECARD round sections (`SCORECARD.md:636-702`, `:1220-1336`),
  measurement recipes (`SCORECARD.md:86-142`), owned axes (`:19-31`),
  saturation (`:626-634`), recording ruling (`:376-380`).
- Located the C1 evidence base: the superseded synthetic leg
  (`corpus/knowledge/2026-10-13-r3-evm-interface.md` — candidate 3 at
  `:47-76`, 3/3 planted selectors; run log `:117-120`) and the frontier debt
  (`PROVINCE.md:91-93`, "real solc/vyper-compiled bytecode untested").
- Measured the before-state independently: command A (recipe copied verbatim
  from `SCORECARD.md:92-124`) at HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`
  → `{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [],
  "depth_score": 10.0, "knowledge_files": 81, "mapped": 81, "missing": [],
  "rule_blocks": 13}` — matches EX-11's recorded artifact
  (`claims/c1/EX-11/command-A-before.txt`, sha256 `8787e0c4…`).
- Drafted the LOG entry: `claims/c1/records-drafts/LOG-entry-draft.md` —
  pasteable entry block (dispatch / C1 / C2 / C3 / custody / process notes /
  carried debt / retired / scope) plus SC-3 poll notes; every parent-only
  value marked `[[FILL: …]]`; the frozen honest-stop alternate paragraph
  included.
- Drafted the SCORECARD round section:
  `claims/c1/records-drafts/SCORECARD-section-draft.md` — format per
  `:636`/`:1270` (intro → wave → C1/C2/C3 bullets → Measured at → axis table
  → trends/planned/debt/retired); C1 bullet and table row filled from
  measured evidence; C2/C3 shape-only placeholders for the other chains'
  scribes.
- Polled the wave dir (~10:00–10:15Z) and folded verified values into both
  drafts across four revisions: probe legs and reconciliation
  (`claims/c1/EX-05/`, `EX-06/evidence/`, `EX-07/reconciliation.md`,
  `RV-2/probe-*.json` + `rv2-verify-ex05-kdx-*.json` + `attack/`,
  `EX-08/probe-*.json`), install receipt (`EX-02/install-receipt.txt` +
  patch), entry + map artifacts (`EX-12/knowledge-entry.patch.md`,
  `EX-13/verification.txt` + map-token variants + `_scratch/`), custody and
  containment (CU-1, EX-01, EX-15 T0/T1 + `containment.md`, EX-10, EX-14
  `MANIFEST.draft.txt`), EX-26 census, seat reports.

## 2. Proposed changes (patch text — NOT applied)

- `claims/c1/records-drafts/LOG-entry-draft.md` — proposed LOG.md entry
  (parent edits/applies at integration).
- `claims/c1/records-drafts/SCORECARD-section-draft.md` — proposed SCORECARD.md
  round section (parent edits/applies).
- No other artifact; the real targets (`LOG.md`, `SCORECARD.md`,
  `corpus/`) were never touched by this seat (read-only inspections only).
- Note: my artifacts sit at `claims/c1/records-drafts/` per the seat line
  (not `claims/c1/SC-3/`); the two files are the complete deliverable.

## 3. Before→after measurement (chain c1 claim)

BEFORE (SC-3 independent re-run; command + output):

```
$ cd kaidoku-shokunin && REV=$(git rev-parse HEAD); python3 - "$REV" <<'PY'
  ... recipe body copied unmodified from SCORECARD.md:92-124 ...
PY
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 81, "mapped": 81, "missing": [],
 "revision": "e845c2b524ad2e59871e004c51a1386e192a74ab", "rule_blocks": 13}
```

AFTER (parent-only for the records commit; the wave has a rehearsed
after-state and a full sealed probe evidence base):

- Probe clause, all legs sealed and SC-3 re-parsed: `Rv2Token` 5/5 (hex
  `ev_45849c8b…` reproduced ×3 byte-identical, raw `ev_3aacd424…`, hex@6.7.0
  `ev_19d7d3cb…`), `KdxToken` 6/6 across ten legs and both pins (EX-05 ×4
  with the determinism twin re-issuing `ev_4dd5ea20…` and the renamed twin
  `ev_b2937090…`; EX-06 ×4 own compiles + ×2 on EX-05's bytes; RV-2 replays
  re-issuing EX-05's ids), `Rv2Many` attack carrier 11/11
  (`ev_d0d0b054…`). EX-07's `reconciliation.md`: 6/6 zero missing/zero
  extra, offsets equal to its independent dispatch parse; two seats'
  independent compiles byte-identical. Input-shape traps fail closed; the
  one EDQUOT `execution_failure` is host-state (EX-15 root-caused the
  saturated /tmp quota) and was retried clean; EX-08's edge matrix
  corroborates (incl. a noTMPDIR EDQUOT reproduction). Creation blobs
  parse-and-empty — no selector claim.
- Install clause: npm `solc` 0.8.37, tarball sha256 `0e1a1ab6…`, 6,476,046 B,
  `solcjs --version` exit 0 (EX-02 receipt; patch target
  `receipts/solc-install.txt`).
- Map/entry clause: EX-12's entry patch
  (`claims/c1/EX-12/knowledge-entry.patch.md`, target
  `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`, 31 lines) applies
  cleanly; EX-13's `verification.txt` rehearses three line-neutral map
  variants with V1-V7 checks — V6 command A (entry landed, patched commit):
  `{"knowledge_files": 82, "mapped": 82, "missing": [], "dangling": [],
  "citation_resolved_rules": 13}`; V7 entry-absent control: 81/81 +
  `dangling: [token]`.
- Remaining parent-only after-values (the real records-commit re-measure;
  prior-81 diff; post-pair) are marked `[[FILL]]` in both drafts with the
  exact check commands.

## 4. Attacks/refutations attempted, with verdicts

- **Framing correction (the big one):** my first draft revisions centered
  `Rv2Token` as the canonical contract (it was the first probe evidence to
  land). EX-07's reconciliation and EX-05/EX-06's artifacts landed mid-poll
  and corrected the picture: the round's main target is `KdxToken` (K = 6,
  ten legs); `Rv2Token` (K = 5) is an independently authored replication
  carrier; `Rv2Many` (K = 11) is the attack carrier. Both drafts were
  re-written (v3/v4) around that structure. VERDICT: caught and corrected
  from late-landing evidence.
- **Variant-token consistency check (my own catch):** EX-13's h1/h2 map
  variants use token `2026-10-19-arc3-r1-evm-solc`, while EX-12's entry stem
  (and EX-13's h3) is `2026-10-19-arc3-r1-evm-real-solc`. Landing an
  h1/h2 token with EX-12's entry would create a permanent dangling/missing
  mismatch. VERDICT: flagged in both drafts — the parent must pair one
  token variant with the entry stem consistently, and must not double-land
  the map hunk (EX-12's hunk B is byte-identical to EX-13's rehearsal).
- Independent command-A re-run vs EX-11's artifact: MATCH (81/81, 13/13,
  missing [], dangling []) — before-values double-measured.
- Re-parsed every probe envelope I could (not trusting seat prose): all
  canonical legs K/K with identical offsets; the rerun twin re-issues the
  same ev id; the renamed twin is path-insensitive; cross-seat replays
  re-issue EX-05's ids. VERDICT: the probe clause is supported by sealed
  artifacts.
- EDQUOT episode: read the failure envelope (`execution_failure`, "Unknown
  system error -122" write); EX-15's containment artifact root-caused it
  (saturated per-UID 12.1G tmpfs quota on /tmp); EX-08's noTMPDIR leg
  reproduced it. VERDICT: host-state, not a bytecode refusal; honest-stop
  branch NOT triggered; recorded as a process note.
- Creation-code legs (`KdxToken.creation`, `Rv2Token.creation`, EX-02 smoke
  bin): `functions: []`. Could be misread as a miss. VERDICT: expected
  (EVMole targets runtime dispatch); no selector claim; carried debt
  (creation-code `kind` classification).
- Encoding/input traps: `kdx.hex-on-bin` / `rv2.hex-on-bin` → typed
  `invalid_request`; `trap-raw-of-hex` / text / ELF-magic / empty legs →
  honest 0-function or typed refusal; missing file → `invalid_request`.
  VERDICT: fail-closed behavior confirmed; no silent findings.
- Token-without-file integration: reproduced the dangling state via EX-13's
  scratch repo (`git --git-dir=repo.git`, read-only) and cross-checked
  EX-13's V7. VERDICT: constraint confirmed; drafts warn against landing
  the token alone.
- Draft citation audit: caught my own guessed line (`corpus/README.md:57`)
  and corrected to `:38` (grep-measured); verified `PROVINCE.md:91-93` and
  `2026-10-13-r3-evm-interface.md:47-76` by direct reads. VERDICT: corrected.
- Cross-wave custody diff (EX-15): the Kimi `config.toml` rewrite predates
  the wave (mtime 2026-10-19 02:20:43Z < wave start ~09:49Z). VERDICT:
  "no config.toml drift" is scoped to the wave window in the drafts — not
  overclaimed.
- Recipe-A invocation quirk (EX-11's claim) independently verified:
  `REV=HEAD python3 - "$REV"` passes `''` (shell expands first);
  `REV=HEAD; python3 - "$REV"` passes `'HEAD'`. VERDICT: confirmed.
- EX-15's stray-write leak (a repo path outside authorized seat paths,
  removed and recreated): noted in the drafts' poll notes; not a C1 claim
  input. VERDICT: recorded for the parent; outside my write scope.

## 5. Blockers / gaps (partial evidence recorded, not blocking)

- Remaining parent-only values: the real records-commit re-measure of
  command A (82/82 expected; rehearsed values in hand), the prior-81
  byte-identity diff, and the wave-level post-pair custody receipt (not yet
  landed at poll close; EX-02's install post-pair shows no drift). Both
  drafts carry `[[FILL]]` markers plus the exact verification commands.
- The entry + map token are patch artifacts owned by EX-12/EX-13; the
  parent must land them together and consistently (see the variant note).
- C2/C3 paragraphs and table rows are shape-only placeholders awaiting those
  chains' records (SC-4/SC-5, SC-6/SC-7 — SC-7's log-entry draft already
  exists); the C3 bullet already carries EX-26's census-at-HEAD values as a
  factual anchor.
- Wave was still in flight at poll close (32 seat reports landed, incl. this
  one) — the drafts name their poll window (~10:00–10:15Z) and remain valid
  as the C1 record.
