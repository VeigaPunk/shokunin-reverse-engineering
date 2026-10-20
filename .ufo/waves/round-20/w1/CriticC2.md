# CriticC2 — falsify C2 (verb coverage counting)

Scope: `.ufo/waves/round-20/claims.json` C2 (:20-31) and its counter contract
(`contract.md:71-75`). Read-only seat; no subagents. All `path:line` anchors are
against the lane working tree at `refs/heads/main` = `d1d981d` (claims commit);
baseline B = `14f0260`.

## Verdict

**C2's `exercised` observable can be satisfied for all five verbs with zero real
coverage.** The three attack vectors named in my charter all hold, plus three
more the spec did not list. Claim is salvageable; the counter as specified is
not the falsifier the claim believes it is.

## Counterexample A — exercised without any run (the big one)

Contract `contract.md:74-75` defines, per target:
`exercised` = *some naming entry also carries an `ev_<64 hex>` id AND a path
under `.ufo/waves/round-20/evidence/c2/` that exists at REV*.

Nothing binds the triple (verb, ev id, file) together:

1. The ev id is not required to appear **inside** the cited file.
2. The ev id is not required to have been minted by the verb — a
   `record_unknown` id, a `doctor` id, or a fabricated 64-hex string all match
   `ev_<64 hex>`.
3. The file is only required to *exist at REV* — an empty file or an unrelated
   receipt qualifies.
4. One entry naming all five verbs + one ev id + one path marks **all five**
   exercised; the spec has no per-verb distinctness requirement.

Concrete forgery (would pass the spec verbatim): a knowledge entry containing
`inspect-wasm-artifact`, `compare-wasm-interfaces`, `execute-rizin-command`,
`list-objdump-architectures`, `project-harmony-application-graph`, the literal
`ev_` + 64 zeros, and `.ufo/waves/round-20/evidence/c2/x.json` where `x.json`
is `{}`. INFERENCE — depends on the tool implementing the contract literally;
the contract as written mandates exactly this check.

## Counterexample B — refusal-only runs mint countable evidence

[OBSERVATION] Refusal/empty results produce deterministic ev ids:
`corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:40` ("evidence_id is
deterministic: identical ev_d4d8cc77…"), :156-159 (`inspect-adb-client` refusals
and `list-adb-devices` empty-list each mint ev ids). The claim's own
`falsified_if` (claims.json:30) says "retained run evidence" — and a retained
refusal envelope *is* retained run evidence under the spec. An entry citing the
ev id of an `unsupported_target` refusal + the retained file passes
`exercised`. The observable cannot distinguish *held* from *refused*.

## Counterexample C — synthetic HAP that proves nothing

claims.json:25 legitimizes "recipe-retained synthesized" carriers, and
`gen-wave1.py:221-225` (HarmonyLeg) prescribes a minimal synthesized Stage-HAP +
FA variant — the only possible carrier, since no HarmonyOS package exists on
this host. If the synthesized zip projects to an empty or degenerate component
graph, `exercised` still passes: the observable is ev+path, not projection
depth. The counter cannot distinguish "module.json routed, abilities inventoried"
from "zip accepted, nothing recognized". INFERENCE on outcome; OBSERVATION that
the check has no depth field.

## Additional gaps the charter did not name

- **Mention = name-density, not coverage.** The 128/153 baseline counts hyphen
  *or underscore* form (contract.md:73). Underscore form is the MCP tool name;
  `corpus/knowledge/2026-10-13-rea-self-documentation.md:47` already pastes a
  five-name underscore list (`analyze_javascript_application`, …). A pasted
  catalog inflates `mentioned` without a single CLI invocation. [OBSERVATION]
- **"admitted" is unchecked.** claims.json:25 says "admitted knowledge entries";
  the spec observable is "knowledge entries at REV naming it" (contract.md:73,
  gen-wave1.py:386 `corpus/knowledge`). No admission/QUALITY gate. Draft text
  counts. [OBSERVATION: no admission test appears in the C2 interface block.]
- **No freshness / round binding.** The ev id is not required to be minted in
  round 20; the file path is round-20-scoped but the id could cite any prior
  round's run. Minor, since the path must still be new.
- **`falsified_if` is self-weakening.** claims.json:30 "fewer than three target
  verbs gain an entry with retained run evidence" is measured by the same
  forgeable observable — the falsifier cannot fire even when the coverage is
  hollow.

## Per-verb disposition

| verb | verdict | reason |
|---|---|---|
| `inspect-wasm-artifact` | KEEP (with fix) | real carriers exist (leg spec gen-wave1.py:181-188 names ≥3 shipped WASM files); WABT pin + refusal leg (wasm-refusals) make this the strongest ground |
| `compare-wasm-interfaces` | KEEP conditionally | must be left≠right distinct digests (leg spec gen-wave1.py:190-195 requires a genuine version pair); a same-bytes-only compare is a determinism check, not interface-diff coverage — reject counting if only the control pair lands |
| `execute-rizin-command` | KEEP conditionally | legs (gen-wave1.py:199-219) do real `iI`/`iS` cross-checked vs readelf plus refusal taxonomy; a `?V`-only run would be a capability ping — reject that if it lands |
| `list-objdump-architectures` | REJECT as coverage evidence | no subject artifact exists — claim statement (claims.json:25) requires "subject SHA-256" which this verb cannot produce; it inventories the host's objdump (`objdump -i` mirror). Fine as a *named* row inside an `objdump` entry; must not earn `exercised` under the claim's own terms |
| `project-harmony-application-graph` | WEAKEST — reject `exercised` credit unless the recipe is retained byte-exact AND the projection reports the Stage-vs-FA hint on a non-degenerate graph | even then it proves parser/projection acceptance of a recipe-built zip, not a real HarmonyOS app; claims.json `limits` should record it as synthetic-only coverage |

## What counts as uncovered ground (smallest safe definition)

A verb is **uncovered** unless a retained evidence file exists at REV whose
bytes (a) contain the `ev_<64 hex>` id the naming entry cites, (b) contain the
verb's own command token, (c) record a non-refusal terminal outcome (absence of
`"status":"error"`/`unsupported_target`/`invalid_request`/`unreadable_output`
as the result), and (d) for artifact-grounded verbs name a subject sha256 that
resolves to a tracked carrier or a retained recipe sha256. Refusal envelopes
earn `named`, never `exercised` — otherwise "covered" degenerates to "we know
it refuses". `list-objdump-architectures` cannot satisfy (d) by construction —
either drop it from `targets` or define a subject-less class requiring a
retained cross-check artifact (`objdump -i` diff). INFERENCE: this definition;
it is a proposal, not a spec quote.

## Smallest safe correction (to contract.md:74-75)

1. `exercised` requires the cited ev id to occur **inside the cited file's
   bytes**, the verb token to occur in that file, and file size > 0.
2. Exclude files whose parsed outcome is a refusal (status error field).
3. Require the evidence path to be tracked-new at REV vs baseline B (no
   recycled round-19 artifacts) and per-verb distinct.
4. Require, for the four artifact-grounded verbs, a subject sha256 in the file
   matching a carrier sha256 or retained recipe.
5. Reword `falsified_if` to use the strengthened observable; add a limit line
   that synthetic-carrier coverage is tagged as such.

Impacted axes: **coverage** (metric gameable → before/after untrustworthy),
**calibration** (falsifier wired to a non-binding observable), **depth**
(single-command rizin / empty-graph HAP would claim depth they don't have).

## Commands run (all in the lane, read-only)

- `ls .ufo/waves/round-20/{,tools/,w1/}` — exit 0 (tools/ empty at review time;
  the counter does not yet exist, so this review attacks the spec).
- `git log --oneline -5 refs/heads/main && git rev-parse refs/heads/main` —
  exit 0 → `d1d981d`.
- `grep -rn "inspect.wasm.artifact\|compare.wasm.interfaces\|execute.rizin.command\|list.objdump.architectures\|project.harmony.application.graph" corpus/ .ufo/gates/` — exit 0, **zero matches** (all five verbs are uncovered ground today).
- `grep -rln "ev_[0-9a-f]\{64\}" corpus/knowledge/ | head -10` — exit 0, 10 files;
  `grep -rn "ev_..." corpus/ | wc -l` → 157.
- `node -e "…cliCommandNames.js…"` — exit 0; all five targets ∈
  `CLI_COMMAND_NAMES` (153 entries); alias map and `MCP_TOOLS_WITHOUT_DEDICATED_CLI` printed.
- `grep -rn "coverage" corpus/README.md | head -20` + `head -60` — exit 0;
  coverage-map rows cite entries by name.
- `grep -rln "inspect_wasm_artifact\|execute_rizin_command\|…" corpus/` — exit 0;
  underscore-form hits only in non-knowledge wave dirs; `rea-self-documentation.md:47`
  pastes five underscore MCP names (mention-inflation precedent).
- `sed -n '169,270p' .ufo/waves/round-20/gen-wave1.py` — exit 0; leg specs quoted above.
- `grep -rn "128\|131\|153" wave1-spec.json gen-wave1.py` — exit 0; oracle spec at
  gen-wave1.py:385-388 (`corpus/knowledge` scope, hyphen or underscore, token boundary).
- `cat corpus/knowledge/2026-10-13-r3-verb-coverage.md | head -60` — exit 0;
  note: older entries cite **truncated** ev ids (`ev_ce745d78…`, r3-verb-coverage.md:28),
  which would fail `ev_<64 hex>` — [OBSERVATION] prior-round entries are mostly
  grandfathered-out of `exercised` shape, so the new requirement applies only to
  new text (fine for targets, but means zero legacy verbs could accidentally gain
  exercised status).

## Installs

None.
