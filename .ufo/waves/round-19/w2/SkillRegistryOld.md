# Round 19 wave 2 — SkillRegistryOld

## Axes and scope

- **Calibration:** distinguish a fixture/selftest pass from a claim about authenticity or live operation; check row wording against observed exit semantics.
- **Freshness:** all source and variant probes below use the observed integrated main tip `279e8b19c51658bfd05b9e31a1c0894ab2e70537` (T), detached in my private clone.
- **Depth:** seven targeted selftests, the explicitly-unexercised citation probe mode, five additional pseudo-ref spellings, malformed-ELF input, and a targeted `--require-mid-maps` list-step variant.

## Findings by severity

### Low — `receipt-validate` can treat a non-REA command argument as an `analyze` subcommand

**Observation:** `SKILL.md:541` describes the list-shaped `steps` criterion as an entry whose argv carries the `analyze` subcommand. In `.ufo/waves/round-17/tools/receipt-validate.py:148-161`, `_is_analyze_step` searches *every* argv token for `rea-agents@X.Y.Z` and takes the following token as the command; it does not establish that the executable is `npx`/`rea-agents` or that the package token occupies a command position. `verify_mid_maps` uses this predicate to satisfy `--require-mid-maps` at `:607-630`.

I made a valid carrier-shaped fixture in the private clone with one list step whose argv was `['printf', 'rea-agents@6.5.0', 'analyze']`, plus a correctly hashed mid-map. The actual validator CLI returned `exit=0`, `valid=1`, and `findings=[]` under `--require-mid-maps`. Thus the argv marker is not sufficient evidence that the recorded command was the analyze subcommand. The added identity cases at `:1105-1119` reject ordinary trailing `analyze` arguments and conflicting labels, but do not test a version-token decoy in an unrelated executable's arguments.

**Boundary / inference:** this is a parser false-positive against the stated subcommand criterion, not an authenticity break. The same row explicitly says the validator does not authenticate a receipt against a forger who rewrites and rehashes it; argv and declared step labels are receipt data. Still, a non-forged list receipt with a decoy package token can incorrectly satisfy the required-map check. A tighter command-shape check (or a clearly separate, trusted step identifier) would close this variant. No source change was made.

Reproduction used a temporary harness in the clone (removed after the run):

```sh
python3 -I -B /tmp/kr19-w2-SkillRegistryOld-8em8q1m5/skillreg_variant_probe.py
# exit=0; inner receipt-validate.py --require-mid-maps returned exit=0,
# valid=true, findings=[] for argv ['printf','rea-agents@6.5.0','analyze']
```

## Row-by-row observations
Command notation: selftest paths in the table are relative to `cwd=/tmp/kr19-w2-SkillRegistryOld-8em8q1m5`; the actual invocations used the corresponding absolute paths in that clone. Explicit variant commands follow.

| Registry row (T anchor) | Executed evidence | Calibration / residual |
|---|---|---|
| `receipt-validate` (`SKILL.md:541`) | `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --selftest` — **exit 0**, `SELFTEST: CLEAN cases=26`. The selftest includes list-step off-analyze red, analyze-on green, ordinary argument decoys, conflicting identities, and duplicate analyze identities (`receipt-validate.py:1045-1119`). The targeted decoy above is the uncovered parser case. | The row's no-authenticity limit is material; a green validation establishes current-byte consistency, not who produced the receipt or whether its argv was executed. |
| `citation-drift` (`SKILL.md:448`) | `citation-drift-probe.py --selftest` — **exit 0**, `CITATION_DRIFT_SELFTEST: CLEAN cases=33 passed=33 failed=0`. The retained round-17 argv is `verification.json:1524-1547` (`citation-strict`, expected exit 0). I also ran the same pinned-revision invocation with and without `--strict`: probe mode reported 5 findings but **exit 0**; strict mode reported the same five and **exit 1**. This confirms the row's newly explicit non-strict behavior. | The row correctly calls the non-strict argv unexercised in retained receipts; my clone run exercises that variant but is not retained project evidence. The five extra CLI calls for `CHERRY_PICK_HEAD`, `REVERT_HEAD`, `REBASE_HEAD`, `BISECT_HEAD`, and `AUTO_MERGE` each returned **exit 2**, finding `rev_moving_state`. Together with the built-in alias cases (`citation-drift-probe.py:539-559`), the denylist variants exercised here refuse before revision resolution. |
| `custody-pair` (`SKILL.md:449`) | `python3 -I -B .ufo/gates/custody-pair/custody-pair.py selftest` — **exit 0**, `CUSTODY_PAIR_SELFTEST: CLEAN cases=31 passed=31 failed=0`. The new subdirectory red case is `custody-pair.py:1420-1449`; the retained capture argv starts at `.ufo/waves/round-17/verification.json:1552`. | The tested `--repo <repo>/sub/deep` form records the top-level repo and separately retains the argument (`:382-420,1425-1449`). The reported 31 cases and current SKILL row agree. This is fixture evidence, not a claim that every worktree/symlink spelling was run. |
| `pins` (`SKILL.md:542`) | `python3 -I -B .ufo/waves/round-17/tools/pins.py --selftest` — **exit 0**, `SELFTEST: CLEAN cases=7`; the CLI mutated-file case returns compare exit 1 and names the changed path (`pins.py:233-245`). | The row accurately says no persisted baseline and only two snapshot instants; it also discloses `snapshot --out` uses `os.replace` without a no-clobber check (`pins.py:114-129`). Neither is a continuity or tamper-authenticity claim. |
| `go-buildinfo-probe` (`SKILL.md:545`) | `python3 -I -B .ufo/waves/round-17/tools/buildinfo-probe.py --selftest` — **exit 0**, `SELFTEST: CLEAN cases=11`. A separate short ELF-magic malformed fixture produced `{"error":"malformed: not ELF"}` and **exit 2**, as the row states (`buildinfo-probe.py:611-637`). | The selftest covers inline section, writable-segment fallback, pointer format, no magic, and several parser bounds (`:518-595`); malformed input is not among its 11 cases, so the separate command exercised that error path. The SKILL row correctly discloses there is no external baseline: the source file is where the constants live, not a digest pin. |
| `routed-defects` (`SKILL.md:586`) | `python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --selftest` — **exit 0**, `SELFTEST: CLEAN cases=19`. It checks default-open exit 0 versus `--strict` exit 1 (`routed-defects.py:1103-1117`) and wrong validator digest/revision red cases (`:1160-1193`). | The registry row accurately distinguishes reporting mode from strict gate mode. C1 integration is not globally clean: `evidence/routed-r18-integrated.json:34-49` has `R18-REGISTRY-PINNED` named/substance true, but `R18-INSTALL-RECORD` substance false and `open_count=1`. Do not read the registry subcheck as a whole-claim pass. |
| `jj-red-before` (`SKILL.md:589`) | `python3 -I -B .ufo/waves/round-18/tools/jj-red-before.py --selftest` — **exit 0**, `SELFTEST: CLEAN cases=9`. Its safety cases cover GIT/JJ sentinels and absolute, `..`, and symlink pointer-table escapes (`jj-red-before.py:70-78,1121-1183`). `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5` was available. | The row's fixed-version `--out` execution is not a substitute for the nine-fixture selftest; no live main-lane run was performed. The guard and selftest are confined to the private/temporary fixture lane. |

The citation probe-mode and strict commands were, respectively (both run against T in the clone):

```sh
python3 -I -B .ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-SkillRegistryOld-8em8q1m5 --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --table /tmp/kr19-w2-SkillRegistryOld-8em8q1m5/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-SkillRegistryOld-8em8q1m5/.ufo/gates/citation-drift/expected.json
# exit=0; reported findings=5

python3 -I -B .ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-SkillRegistryOld-8em8q1m5 --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --table /tmp/kr19-w2-SkillRegistryOld-8em8q1m5/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-SkillRegistryOld-8em8q1m5/.ufo/gates/citation-drift/expected.json --strict
# exit=1; reported the same five findings
```

The malformed-ELF check used a six-byte `7f 45 4c 46 02 01` fixture created and removed under the clone:

```sh
python3 -I -B /tmp/kr19-w2-SkillRegistryOld-8em8q1m5/.ufo/waves/round-17/tools/buildinfo-probe.py /tmp/kr19-w2-SkillRegistryOld-8em8q1m5/buildinfo-malformed-tigm3qsa/malformed.elf
# exit=2; {"error":"malformed: not ELF", ...}
```

Additional pseudo-ref variants (same root/table/expected arguments shown in the citation commands above; each was an individual invocation):

```sh
python3 -I -B .ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-SkillRegistryOld-8em8q1m5 --table /tmp/kr19-w2-SkillRegistryOld-8em8q1m5/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-SkillRegistryOld-8em8q1m5/.ufo/gates/citation-drift/expected.json --strict --rev CHERRY_PICK_HEAD
# exit=2; finding=rev_moving_state
python3 -I -B .ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-SkillRegistryOld-8em8q1m5 --table /tmp/kr19-w2-SkillRegistryOld-8em8q1m5/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-SkillRegistryOld-8em8q1m5/.ufo/gates/citation-drift/expected.json --strict --rev REVERT_HEAD
# exit=2; finding=rev_moving_state
python3 -I -B .ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-SkillRegistryOld-8em8q1m5 --table /tmp/kr19-w2-SkillRegistryOld-8em8q1m5/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-SkillRegistryOld-8em8q1m5/.ufo/gates/citation-drift/expected.json --strict --rev REBASE_HEAD
# exit=2; finding=rev_moving_state
python3 -I -B .ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-SkillRegistryOld-8em8q1m5 --table /tmp/kr19-w2-SkillRegistryOld-8em8q1m5/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-SkillRegistryOld-8em8q1m5/.ufo/gates/citation-drift/expected.json --strict --rev BISECT_HEAD
# exit=2; finding=rev_moving_state
python3 -I -B .ufo/gates/citation-drift/citation-drift-probe.py --root /tmp/kr19-w2-SkillRegistryOld-8em8q1m5 --table /tmp/kr19-w2-SkillRegistryOld-8em8q1m5/.ufo/gates/citation-drift/pointer-table.json --expected /tmp/kr19-w2-SkillRegistryOld-8em8q1m5/.ufo/gates/citation-drift/expected.json --strict --rev AUTO_MERGE
# exit=2; finding=rev_moving_state
```

## Freshness, method, and verification gaps

- Observed lane command: `git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse --verify refs/heads/main` — **exit 0**, `279e8b19c51658bfd05b9e31a1c0894ab2e70537`.
- Private clone setup: `git clone -q --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr19-w2-SkillRegistryOld-8em8q1m5` — **exit 0**; checkout `git -C /tmp/kr19-w2-SkillRegistryOld-8em8q1m5 checkout -q --detach 279e8b19c51658bfd05b9e31a1c0894ab2e70537` — **exit 0**; clone `rev-parse --verify HEAD` — **exit 0**, same T.
- **LSP unavailable:** `read xd://lsp` returned `No such tool: xd://lsp` and listed mounted devices without an LSP route. Therefore no LSP references/definitions/diagnostics were available. Literal grep was used only to locate declarations and anchors; semantic conclusions above come from source inspection and executed CLI behavior, not grep output.
- No production source edits, builds, broad suite, formatting, installs, REA/Ghidra analysis, or carrier execution. The only lane write for this assignment is this report; the temporary fixture harness and its files were removed after the probe. All selftests and custom mutations were confined to the private clone or their documented temporary fixture roots.
