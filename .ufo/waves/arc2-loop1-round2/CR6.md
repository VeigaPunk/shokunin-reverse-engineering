# CR6 — critic: separability attack on C1 × C3 (one move wearing two hats?)

Seat CR6, wave arc2-loop1-round2, 2026-10-18. Read-only over the repo and home;
the only repo write is this report. All commands below were run by this seat
this session in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; scratch
confined to `/tmp/arc2-l2r2-CR6/`. HEAD at every command:
`165057e36f558c95eb02bf24de4a874d559d6950`; `git status --porcelain` →
`?? .ufo/waves/arc2-loop1-round2/` only. No MCP session was opened by this
seat; `pgrep -af 'rea\.mjs|rea-agents|rea doctor'` at 17:09:29Z → rc=1 (no
process remains — every session closed).

## 0. Verdict

**ONE-MOVE CHARGE REFUTED as stated, conditional on the landed text.** The
strongest conflation case — one artifact (the 6.7.0 cache), one round-given
receipt (the 5-path pre-pair), one motivating refutation (SC2 round 1) — is
real but not the protocol's test. Both directions of `AXES.md:31-33`'s
separability test ("each verifiable without the others having landed",
distinct axes) were exercised with live commands this session: **C1's entire
acceptance chain (pin grep + package.json + static catalog counts/digest)
passes with zero C3 battery artifacts committed** — I reproduced all of it
myself — and **C3's drift clause passes with zero C1 edits landed** (`git diff
HEAD` on the four doc files is empty while the pre-pair self-checks 5× OK).
Failure modes do not propagate: C1 fails on a surviving stale sentence or an
availability→holding slip; C3 fails on drift or a session-close defect. The
charge survives only as two landing-text conditions (§3): the landed
PROVINCE text must back its 6.7.0 values from the package's **recorded
identity / static census**, not from the battery or doctor output, and must
cite the pre-pair receipt as the **round's** pre-pair, never as "C3's
zero-drift result".

## 1. The strongest one-move case (steelman, as constructed)

1. **One artifact.** C1's core finding (Kimi pin `rea-agents@6.7.0` at
   `config.toml:2940`) and C3's probe target (doctor + `binary_session` on the
   6.7.0 cache) are the same object. C1's landed numbers (207 MCP / 153 CLI /
   6 prompts, `tools_sha256 af39310c…`) are byte-identical to C3's leg-1
   doctor identity and leg-2 census outputs. One package, one number set, two
   ledger rows.
2. **One receipt.** Both claims are bracketed by the same file —
   `.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt`
   (`2026-10-18T16:57:35Z`, 6-line/5-path, self-hash `4097ec77…`). Nineteen
   round-2 seat reports cited it at 17:08Z (29 by 17:13Z as seats landed;
   `grep -l` run both times), including C1 seats (E1, E2, E7) and battery
   seats (E13, E14). E7's landed PROVINCE draft cites it **inside
   PROVINCE.md itself** (`E7.md:246-247`). The 5-path extension is C3's
   claimed scope; C1's text would cite C3's artifact family.
3. **One window.** Every receipt on both sides is stamped 16:57–17:07Z
   (pre-pair 16:57:35Z; leg 1 `16:59:31Z` `E13.md:106`; leg 2 `started_at
   16:59:36.101Z` `E14.md:43`; C1 census E1 16:59:18Z/16:59:40Z; my own runs
   17:01:04Z/17:01:42Z/17:07:45Z). One probe window.
4. **One provenance.** Both exist because of SC2's round-1 refutation: C1
   reconciles the docs to the pin SC2 found; C3 probes the counts/digest SC2
   left "unprobed" (`SC2.md:68` round 1). Round 1's carried debt lists both
   in one breath (`SCORECARD.md:697-700`).
5. **One state change.** Nothing on the host changed for either claim; both
   are measurement+bookkeeping of a pre-existing 6.7.0 state. Executing the
   battery and landing the reconciliation could be narrated as one act
   recorded twice.

## 2. Evidence refuting it — both counterfactuals, observed

### 2.1 C1's acceptance passes with C3 unlanded (ran this session)

The round-2 receipts dir contains **only** `config-pre-pair.txt` (no leg
artifacts committed) — verified `ls .ufo/waves/arc2-loop1-round2/receipts/`
multiple times to 17:08Z. Against that state, C1's full evidence chain
reproduces from static instruments with no battery, no doctor, no MCP session:

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-18T17:01:42Z
$ grep -n 'rea-agents' ~/.kimi-code/config.toml
2940:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
$ sed -n '1478p' ~/.kimi-code/config.toml
model = "kimi-k3"
$ jq -r '.name + " " + .version' ~/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/package.json
rea-agents 6.7.0
```

Static catalog census (my scratch `/tmp/arc2-l2r2-CR6/cr6-count-probe.mjs`,
pure `node` imports from the cache, no server):

```
TOOL_CONTRACTS length: 207
{"tools_sha256":"af39310c9591bb981893ec0d2188b1bcf6e9cc8ba3ac513d5bbefc8ddcb85639",
 "prompts_sha256":"7152916ab48bd2a9677a5ad9cdbde0a51dc53c113934952ad096e93f5f18aa7e",
 "combined_sha256":"96d8f6e6ea1b1ba13557216624a3461c738729d53c79b4b0100d1f3a3a32441c"}
```

and `CLI_COMMANDS keys=153` / `CLI_COMMAND_NAMES array len=153` (my
`cr6-cli2.mjs`). So every value C1 needs — pin line, resolved package
version, counts, digest — is obtainable by config grep + package.json census
+ static import, exactly the receipt classes C1's claim names. No battery
artifact is load-bearing for C1.

Corroboration (read, not run): E1's census (two captures 16:59:18Z/16:59:40Z,
`E1.md:7`), E2's inventory + structural npx-cache resolution (`E2.md:7`),
E7's static cross-checks (`E7.md:143`), SC1's static counts (`SC1.md:46-51`).

### 2.2 C3's acceptance passes with C1 unlanded (ran this session)

`git diff HEAD --stat -- SKILL.md PROVINCE.md SCORECARD.md MINT.md` → empty
(no C1 edit landed). Against that state:

```
$ tail -n +2 .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
rc=0
```

Shape gate: `wc -l` → 6; hash-line count → 5; timestamp count → 1
(6/5/1, E15's extended form). C3's drift clause reads only the five **home**
paths (none is a repo file) and its SOP amendment targets `SKILL.md:217-256`
— disjoint from C1's `SKILL.md:18-20`. C1's edits cannot move any custody
path; C3's legs cannot move any repo doc. The pre-pair predates both legs
(16:57:35Z < 16:59:31Z < 16:59:36Z), so "pre-dispatch" holds for the two
completed legs; all sessions closed (`pgrep` rc=1 at 17:09:29Z; E14 closure
block `E14.md:56-61`).

### 2.3 The shared receipt is round-given, not C3-produced

The seat line itself states the 5-path form "enters at THIS round's pre-pair,
captured 2026-10-18T16:57:35Z, parent receipt
`.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt`" — i.e. it was
captured by the parent **before any seat dispatched**, as the round's custody
freeze under SKILL.md rule #10/SOP. C3's claim brackets its battery with it
and amends the SOP to match; C3 does not produce it. A C1 citation of that
file cites a pre-existing round artifact, not a C3 deliverable. Even in the
counterfactual where C3 is dropped entirely, the receipt exists.

### 2.4 Shared values are convergent, not dependent

C1's 207/153/6 + `af39310c…` come from the package's static files (I
reproduced them with no server). The battery's identical values are an
independent second instrument on the same package — corroboration, not
causation. Same numbers ≠ same move; the protocol's test is verification
independence, which holds in both directions (§2.1, §2.2). Distinct axes as
declared: C1 = calibration (owned), C3 = operability (fleet, capability
acquisition).

### 2.5 Independent failure surfaces

C1 can fail — a stale Kimi-pin statement survives the edit, or the landed
text slips an availability→holding inference — while C3's battery closes
cleanly and its row enters. C3 can fail — drift detected → VOID per
`SKILL.md:246-252`, or a session-close defect — while C1's reconciliation
still verifies; a detected drift does not falsify C1's pin statement, only
the environment. The battery legs never read the docs: `grep -c 'PROVINCE'`
on round-1 leg artifacts (`leg-1-doctor.txt`, `leg-2-binary-session.json`,
`leg-2-tools-list.json`) → `0`, `0`, `0`; round-2 legs (E13 doctor reads
configs; E14 census reads the cache) likewise.

## 3. Residual conditions — where the charge survives

1. **Value sourcing.** If the landed PROVINCE text backs the 6.7.0 counts /
   digest from "the live probe" / doctor / battery rather than from the
   package's recorded identity and static census, C1's backing moves inside
   C3's artifact set. E7's draft avoids this ("the package's compiled,
   recorded identity, read 2026-10-18", `E7.md:249-251`) — keep it.
2. **Receipt citation form.** If the landed text cites the pre-pair receipt
   as "C3's zero-drift result" rather than as the round's pre-pair, the
   citation becomes C3-conclusion-dependent. Cite the file (timestamp +
   sha256), not the drift verdict.
3. **Same-file, one-commit overlap.** Both claims edit SKILL.md (`:18-20` vs
   `:217-256`) and SCORECARD.md (round section vs capability row) in one
   integration commit. Commit granularity is not separability (round-1 CR6's
   finding transfers), but commit named paths only — the wave dir is
   untracked and stray files are invisible to the census instruments (V5/R6
   hygiene).
4. **C1's counting instrument** (R6 item 1: no counting command frozen; 6 vs
   11 loci by instrument) must be defined in the landed text so the
   after-value is re-derivable. Not a C1×C3 coupling — flagged so the parent
   does not attribute R6's finding to this seat's adjudication.

## 4. Text for the parent — VERBATIM

```text
CR6 separability adjudication (C1 × C3) — one-move charge REFUTED as stated; conditional on landed text.
Both directions of AXES.md:31-33's test exercised 2026-10-18 at HEAD 165057e:
- C1 without C3: full chain reproduces statically with no battery artifact committed — grep config.toml:2940 → rea-agents@6.7.0, :1478 → model = "kimi-k3", package.json → 6.7.0, static TOOL_CONTRACTS=207 / CLI_COMMANDS=153 / recordedCatalogDigests tools_sha256 af39310c9591bb981893ec0d2188b1bcf6e9cc8ba3ac513d5bbefc8ddcb85639 (my runs 17:01–17:08Z; corroborated E1/E2/E7/SC1).
- C3 without C1: git diff HEAD on SKILL.md/PROVINCE.md/SCORECARD.md/MINT.md empty; pre-pair 5-path sha256sum -c → 5× OK rc=0, shape 6/5/1; SOP target SKILL.md:217-256 disjoint from C1's :18-20; no custody path is a repo file.
Shared objects are real but not the test: same 6.7.0 cache, same round-given pre-pair (16:57:35Z, captured before dispatch), same window, same motivating SC2 refutation. Failure modes do not propagate (leg artifacts contain 0 PROVINCE refs).
Landing conditions (the charge survives only here):
1) The landed PROVINCE text must source 6.7.0 counts/digest from the package's recorded identity / static census — NOT from doctor/battery output ("live-probed").
2) Any citation of receipts/config-pre-pair.txt must name it as the round's pre-pair (timestamp + sha256), not as C3's zero-drift conclusion.
3) One commit lands both; commit named paths only (wave dir untracked).
4) C1's stale-count instrument must be frozen in the landed text (R6 item 1: 6 vs 11 loci by instrument; not a C1×C3 issue).
All sessions closed at check time (pgrep rc=1, 17:09:29Z).
```

## 5. Conclusions, labeled

- **Observation** — (a) my own runs: pin grep → `:2940` = 6.7.0,
  `:1478` = `model = "kimi-k3"`, package.json → 6.7.0; static
  TOOL_CONTRACTS=207, CLI keys/names=153, recorded digests `af39310c…`
  (`/tmp/arc2-l2r2-CR6/cr6-count-probe.mjs`, `cr6-cli2.mjs`); (b) round-2
  pre-pair: 6/5/1 shape, 5× OK rc=0, self-hash `4097ec77…`; (c) receipts dir
  holds only `config-pre-pair.txt` through 17:08Z; (d) `git diff HEAD` empty
  on the four doc files; `git status --porcelain` → untracked wave dir only;
  (e) leg artifacts 0 PROVINCE refs; (f) `pgrep` rc=1 at 17:09:29Z;
  (g) 19 round-2 seat files cite the pre-pair (`grep -l`); (h) stale loci
  read this session: `PROVINCE.md:10,:18,:44,:45` (Kimi 6.4.0 /
  `config.toml:1478` / 127-commands rows), `SKILL.md:18-20` ("Current …
  Kimi 6.4.0"), `SKILL.md:12` already historical-marked, `MINT.md:10` stale
  (out of C1's declared file set); `SCORECARD.md:58-59,:291` inside dated
  round sections; `SCORECARD.md:698` / `LOG.md:1006` already carry the
  refutation.
- **Observation (read)** — E13/E14 leg reports (timestamps `E13.md:106`,
  `E14.md:43`; closure `E14.md:56-61`), E1/E2/E7/SC1 C1 receipts, E21 SOP
  amendment draft (`SKILL.md:217-256` target, prefix `1-216` byte-identical),
  R6 item 1, R7 capability precondition.
- **Inference** — the one-move charge fails because acceptance instruments,
  failure modes, and axes are disjoint; the shared cache/receipt/window are
  the wave's concurrency, not a single move. The charge survives only as the
  §3 landing-text conditions, enforceable by the §4 guards.
- **Unknown** — whether the parent lands E7's exact draft (guards apply
  conditionally); whether battery leg captures (currently `/tmp`-held,
  `E13.md:15`, `E14.md:11-25`) land as committed receipts this round; whether
  C1's final counting command is frozen (R6's open item); the final post-pair
  outcome (not this seat's scope).
- **Scope compliance** — no repo file edited except this report; no git
  mutations; no config edits; no installs; no network; no MCP session
  opened; scratch confined to `/tmp/arc2-l2r2-CR6/`.
