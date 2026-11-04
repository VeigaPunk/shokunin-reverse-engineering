# Round 78 — declared claims (frozen; no amendments after the freeze commit)

Base `6205ec8c575fb070243c0c40e34a2b0daacde46a` (the round-77 lane tip after the round-77
non-author spot-check and after this round committed that wave's late `CriticClaims` evidence,
the round-77 routed item 12). Lane tree clean and pushed at the start.

Two claims on two distinct axes, causally separable: C1 reads committed attack fixtures and the
frozen round-77 instruments' verdicts on them; C2 reads `PROVINCE.md` and the live host objects
it names. Neither instrument reads the other's receipt. Both are capability acquisitions in the
AXES sense: the instrument runs, its output verifies, and its row enters the SCORECARD
capabilities table in the same round.

**Lowest-axis obligation.** The lane's three owned proxies (coverage/depth/calibration) sit at
10.0 behind different proxies; the stagnation nudge's waiver is not met (capability rows entered
in rounds 73–77, inside the 10-round window), so no waiver is claimed. **`lowest-axis:
calibration`** — R78-C1 works a tied-lowest axis. C2's axis is `freshness` (the record's
drift-prone surface values), which the lane reports on every round; it is not a second
calibration claim.

**Population — the round-77 closure's routed defects** (`corpus/lessons/round-77-verifier-spotcheck.md`
§6 and §8). Disposition:

- §8 items 8–10 (A1 accepts a failing run; A2 does not enforce the filing revision; no receipt
  authentication in C1) and §6 item 7's two mutation survivors and grammar limits → **R78-C1**.
- §6 items 1–6 and §8 item 11 (the wave accounting, the misattributed controls, the prose
  mistakes, the exit-less receipts, the forged-arms detail, the Stale-lane line) are record and
  prose repairs, carried **unclaimed**, closed in the round's record and report; the two prose
  mistakes become `## Mistakes` rows in `corpus/lessons/round-78.md` (append-only).
- §8 item 12 (settle the wave before filing) is a process duty: the inherited evidence is
  committed at the base commit above and named in the report.

## R78-C1 — calibration: the frozen instruments' attack classes are enumerated and refused

**Type.** Capability acquisition. Round 77 landed two instruments and a wave seat showed with
committed fixtures that both accept records they must refuse: a hand-authored green receipt with
no rev and no instrument pin, a re-punctuated verdict (`D24: true`, `mismatch 0`), a negated cell,
a nested field the top-level grammar cannot see, a clone-run arm met by a `FAIL` run, a filing
receipt at a foreign revision, and any JSON with an integer `exit` standing in for a gate receipt.

**Surface.** The lane's evidence instruments and the ten attack classes, one committed fixture
tree per class under `.ufo/waves/round-78/attacks/` (`gen-fixtures.py` writes them). Each fixture
names one receipt; the gate measures the frozen round-77 instrument's verdict on that tree (the
base arm), then applies the one declared rule that must refuse it (the after arm), then judges the
real record with every rule (the genuine control).

**Rules (one per class).** `receipt_auth` (a named receipt must carry a 40-hex `rev` and an
`instrument.sha256` that re-derives from the blob at that rev), `qualified_atom` (an atom id
carrying a qualifier), `near_miss_field` (a verdict token in a spelling the grammar does not
define), `negated_verdict` (a verdict group that says what is not), `value_mismatch` (a parsed
clause bound through a unique nested key whose value differs), `unbound_verdict` (a parsable
clause that binds nothing — the round-77 instrument records its `defect` status and drops it),
`clean_run` (a clone-run receipt must exit 0 with `prefile: PASS`), `filing_rev` (the filing
receipt's rev must be an ancestor of the measured rev), `gate_receipt_schema` (a `gate-*.json`
must pass the receipt contract: argv naming the gate, stdout digest, verdict line, four-key env),
`gate_receipt_rev` (its rev must be an ancestor of the measured rev).

**Predicate (one sentence, frozen).** R78-C1 is verified iff
`python3 -I -B tools/round-78/attack-gate.py --root . --rev <measured> --work <scratch> --battery
--json-out <receipt>` exits 0 with `fixtures_total 10`, `base_accepted 10`, `refused 10`,
`genuine.mismatch_count 0`, `genuine.defects []` and a defect-free `validate`, every fixture
refused by its declared rule id and every base acceptance re-derived by running the frozen
round-77 instruments on the same fixture tree, while the do-nothing control `--control base-only`
reports `refused 0` of 10 and `--control all-refuse` reports `genuine.mismatch_count >= 1`, and
the selftest carries the legitimate look-alikes beside reds for the rule boundaries (qualified
atom, near miss, negation, ambiguous and absent field, typed comparison, receipt schema and
stale revision).

**Counting command.** `refused` is the counter; `base_accepted` is the base arm.

<!-- counting-command: C1 -->
```sh
python3 -I -B tools/round-78/attack-gate.py --root . --rev $REV --work $WORK --battery --json-out $OUT
```
<!-- /counting-command -->

**Kill rule.** A fixture the base instruments already refuse (the class is not live) counted as
refused; a fixture refused by a rule other than its declared one; the genuine record refused
(over-tightening); a rule that reads a hard-coded fixture name instead of the fixture's bytes; a
receipt admitted without re-deriving its own instrument pin; a `validate` defect; a fixture
missing from the set or counted twice → not verified, reported, never narrowed.

**Do-nothing controls (scored before the freeze).**
- `ctl-base-only`: the same battery with the rule application skipped — `refused 0` of 10: the
  target is unreachable by re-running the frozen instruments.
- `ctl-all-refuse`: every fixture refused unconditionally and the genuine record with a forced
  defect — over-tightening is not a pass.
- `ctl-no-fixtures`: an empty fixture set — `base_accepted 0`, below the `fixtures_total 10` floor.

## R78-C2 — freshness: the record's surface values are re-derived from live bytes

**Type.** Capability acquisition (a surface recheck) with a measured drift correction. `PROVINCE.md`
records the three REA pins, the Ghidra provider and the JDK as prose dated 2026-10-20; nothing
re-derives them, so a token grep finds a recorded version whether the host runs it or not.

**Surface.** Eight values: the Devin, OMP and Kimi `rea` pins; the OMP rea disable's presence; the
Ghidra `application.version`; the `GHIDRA_INSTALL_DIR` path; the JDK version; the `JAVA_HOME`
path. Each is parsed from the record by a declared pattern and read from the live object the
record names (`mcp_config.json`, `mcp.json`, `config.toml`, `application.properties`, the
`.bashrc` exports, `java -version`); a pointer that is not the declared live source is a defect.

**Predicate (one sentence, frozen).** R78-C2 is verified iff
`python3 -I -B tools/round-78/surface-recheck.py --battery --root . --rev <measured> --json-out
<receipt>` exits 0 with `checks_total 8`, `matched 8`, `mismatches 0`, `unparsed 0` and a
defect-free `validate`, every value re-derived from the live object the record names and compared
typed to the record's parsed value, while at base `6205ec8c` the same command exits 1 with
`mismatches 2` naming `jdk-version` (record `21.0.12.1`, live `21.0.13`) and `omp-rea-disable`
(the record says the live file no longer records the disable; the live file carries
`disabledServers: ["rea"]`), and the control `--control token-grep` accepts a forged record whose
`ghidra_version` token `8.5` appears in the live `application.properties` but not as
`application.version`.

**Counting command.** `mismatches` is the counter.

<!-- counting-command: C2 -->
```sh
python3 -I -B tools/round-78/surface-recheck.py --battery --root . --rev $REV --json-out $OUT
```
<!-- /counting-command -->

**Kill rule.** A recorded value that does not parse counted as matched; a live value read from a
file the record does not name; a path compared as a string when one side is `$HOME`-relative; a
mismatch suppressed by normalising it away; a control that cannot fail; a receipt without its
`checked_at` date → not verified, reported, never narrowed.

**Do-nothing controls (scored before the freeze).**
- `ctl-token-grep`: the recorded token searched in the live text instead of the live object — it
  accepts a forged `ghidra_version 8.5` (the live `application.properties` carries
  `application.gradle.min=8.5`) and cannot see the OMP disable at all.

## Frontier step (§2b)

- Sources: three new rows opened this round (S292 `stdtypes.html`, S293 `tomllib.html`, both
  mined; S294 `re.html`, rejected). C1 cites S292 (a boolean is an integer subtype — the guard
  `isinstance(x, int) and not isinstance(x, bool)`), C2 cites S293 (a read-only TOML parser).
- Mistake: mined into `corpus/lessons/round-78.md` `## Mistakes` (the round-77 prose-only
  mistakes, the `defect`-status-not-collected hole, and the fixture-for-the-wrong-reason case).
- Census: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` at round
  start (before this file's commit) and at round end; both pasted in the report.

## Wave

One v1 wave (`r78-w1`), 8–16 seats under `ufo-wave-policy.json`, ≥25 % attack roles, at most two
connectors; the L1 holds the planner seat. Seats return findings and evidence files; the L1 lands
every lane edit.
