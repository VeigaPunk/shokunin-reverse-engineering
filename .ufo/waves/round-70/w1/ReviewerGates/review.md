# ReviewerGates — frozen round-70 w1 review

Axes: calibration (C1), operability (C2), coverage (C3); review dimensions: clause coverage, verdict dependency, negative reachability, exit typing, provenance.

Reviewed freeze 4737a542ae3b1b910d8fe43efbd572bc578b07c6. All six extracted blob SHA256 values matched claims.json. Paths/line numbers below refer to tools/round-70 at that freeze. Read-only review: no repairs, commits, integrations, alternate agent runtime, or tool installations. LSP device unavailable (`xd://lsp`: no such tool); source inspection is literal analysis, not semantic references/diagnostics proof. Scratch was confined to the assigned root and removed after evidence preservation. This report is inside the binding directory; the conflicting shorter trailer path outside that directory was not written.

## Findings ordered by severity

1. **HIGH RG-1 — runtime arms remain assertions in the receipt checker.** packed-elf.py:439-451 tests that reported `ok` and arm booleans are true, but never derives identity, recovery, detection or controls from recorded evidence. The producer binding at 391-401 compares public revision/hash strings, not authentic execution provenance. `asserted-arms.json` is a declaration receipt fixture relabelled to the freeze revision, with every carrier's `runs`, `unpacked_counts`, and `control` removed, `section_count=99` and `upx_list_rc=1`, retaining true arm flags. The frozen checker exits 0 / met true. This directly contradicts its stated “every green field is re-derived” guarantee (365-376), and the broader M69-8 closure; it does not negate that the specific ten enumerated shapes are rejected. Evidence: negative-probes.json, checker-asserted-arms.
2. **HIGH RG-2 — C1 never requires its two distinct-directory runs to be green.** forged-receipts.py:249-256 reads work_dir from w1/w2, and 265/274-275 folds only distinct nonempty strings. Both return codes, `ok`, pristine state and mutant results are ignored. C1 explicitly requires distinct work_dir values on *two green runs*. Fault injection changing only those two real successful subprocess result codes to 1 still returns ok true, failures []. Evidence: green-run-rc-not-folded.json. QUALITY #87: the green-run clause is unread; #105 analogue: the invocations' exit results do not enter the verdict. No source files were mutated.
3. **MEDIUM RG-3 — validators accept structurally dishonest counter receipts.** All five validators reject an empty object with exit 1, but accept the supplied stronger false-green fixtures with exit 0. Their documentation promises structural honesty, not merely JSON syntax. forged-receipts.py:345-355 accepts one invented shape, clause_found false and genuine.checker_rc=1. seam-probe.py and contract-probe.py:319-336 accept one invented passing arm despite declared target 7/6. mutation-check.py:207-229 accepts one invented `killed` mutant with rc 0, no expected case and no pin/floor derivation. controls.py:237-245 accepts seven false arms while overall ok true and failures empty. Evidence: five *.forged.json files and negative-probes.json. These auxiliary modes do not by themselves replace the canonical counting commands; the exact C1 constant-with-no-rows negative is correctly rejected.
4. **MEDIUM RG-4 — readable malformed receipts escape the named exit contract.** packed-elf.py:391 assumes object root. Supplying readable JSON `[]` produces AttributeError traceback and exit 1, rather than a named not-met or typed could-not-evaluate result. Evidence: non-object.json, negative-probes.json checker-non-object. Similar unchecked row/object assumptions occur in the other validators, but only the checker root case was exercised here.

## packed-elf.py

Predicate mapping: C1 F1/F2/F10 producer checks 391-401; F3/F9 registry and source checks 402,423-434,478-479; F4/F5/F6 ratio/original/packed checks 452-477; F7 row cardinality 403-410; F8 required arms 441-451. Every collected failing clause enters `met` and exit at 480-486. C3 target/matched/control/failing 403-416; exact carrier kinds 418-421; pinned ids/sources/kinds/ceilings and declared originals 423-460; packed ceiling/derived ratio/0.75 bound 461-477. dinit table 105-109 and declared count 116 encode 1268, static-exe, pinned docker-init; row ratio derives as 10/1268 rounded to 0.0079. The 29/1111 and 3/3/5 descriptive inventories are not independently pinned by this checker; the frozen predicate only fixes the original procedure count, class and ratio constraints.

Producer runtime: hash precedes first supplied-packer execution 311-328; selected path is returned and used at 499,563,567,573,587-589. Allowlist builder 154-167 is passed as env to packer calls; node/REA retains the normal environment (the declared seam is packer children). Broken node is typed at 333-339. Exec-format wrong bytes fail hash first. Per-run packed work uses mkdtemp/finally cleanup 539,622-623. HOME builder does not fall back to system temporary storage.

Selftest executed: 23/23, exit 0. Five named arm-negative mutants all killed with expected names by mutation-check. RG-1/RG-4 qualify honesty/typing; the narrow C3 scalar checker predicate is implemented, but authentic run provenance is not established by public field equality. No final landing receipt existed in l1/scores during this review, so C3 landing acquisition is not attested here.

## contract-probe.py

C1 identity corroboration: 140-161 producer binding; 164-220 registry, host source SHA/readelf format, packing argv, originals/counts/ratio and ids; A5 combines failures at 223-224; A6 combines host pin/version and producer failures at 225-248; final all-six fold at 301-309/371. Missing-node/work/impostor/bumped-binary scenarios derive from subprocess results at 285-300. No observed final comparison was merely printed. RG-3 applies to validate; normal six-arm target is fixed by construction.

Important limitation: F1/F2/F3/F9/F10 fixtures start from the round-69 receipt, so its old producer fields already fail the new producer check. F3/F9 do not independently make A6 false when only a correctly producer-labelled carrier identity is altered: A6 only incorporates producer failures, not A5's carrier failures. This is masking within the declared finite battery, not proof of universal identity-shape rejection.

Predicate survival: the declared finite C1 identity checks passed in the full declaration-revision battery; broader receipt authenticity does not follow. No --selftest mode exists. Empty-object validator negative exits 1; invented-arm validator exits 0 (RG-3).

## mutation-check.py

Target blob/pin: 126-144; pristine run and floor: 134-152; per-run work: 130/184; five unique patch sites, expected named failures and survivors: 155-178; pin/floor participate in verdict 178-179. Constant no-mutant receipt is explicitly rejected at 214-216. Exit 0/1 final fold 266; pristine non-green is designated exit 2 at 135-136; unknown blob/patch sites also typed 2. No --selftest exists; the battery runs the target selftest.

Executed pristine 23 cases / five named kills, zero wrong-case kills and zero survivors, exit 0. Full C1 battery observed wrong pin exit 1 with name, floor 24 exit 1 with name, and distinct work dirs. RG-3 affects stronger validate honesty, not the exact empty-mutant negative. Predicate survival: this instrument satisfies the explicit pin/floor/constant checks; its caller's two-green check is defective (RG-2).

## seam-probe.py

C2 mapping: A1 impostor with execution-log absence and sha refusal 180-194; A2 public producer field binding 147-166 plus pinned-copy hash/nondefault path and every pack/unpack argv 198-220; A3 committed inventory and matching selftest case count 225-237; A4 typed node result 239-256; A5 typed packer result 258-268; A6 unset HOME skip-run plus child-env home and source fallback check 270-282; A7 both rc0, distinct work dirs under work 284-301. All seven feed failed/arms_passed/ok at 303-308 and exit 375. Unlike C1, A7 correctly checks both run return codes.

A3 tests the builder via the producer selftest, not an actual child environment capture; this is exactly the narrow declared A3 criterion. A6 trusts the producer's audit output and checks one literal fallback spelling; direct source inspection confirms the current builder. A2 trusts reported argv once public producer strings match, not actual process execution. These are observation limits, not omitted finite clauses. A4 requires `node` substring rather than the exact `broken_tool: node` class described in its docstring. The actual producer emits that class.

RG-3 affects validate. No --selftest mode. Predicate survival: all seven arm expressions feed verdict; full 7/7 versus 0/7 execution was not repeated by this review. Existing base/pre receipts were not substituted for landing measurements.

## forged-receipts.py

C1 all-ten definitions and declared clause substrings 110-154; base acceptance 184-186; new exit1 plus named clause 188-196,218-221; five identity shapes probe A5/A6 false and exit1 plus base exit0 198-214; genuine checker/probe 223-237; wrong pin/floor naming+exit1 239-248,268-273; distinct dirs 249-256,265,274-275; constant exit1 257-261,276-278; final failures fold 279-286/412. RG-2 is an explicit missing predicate clause. Identity filter uses nonempty all() rather than exact two-arm cardinality, and genuine probe counts permit equal missing values, but the frozen probe always emits the two arms and numeric target; these are harness robustness risks, not demonstrated current-runtime failures.

Executed full battery at declaration revision 8b825161 with the genuine declaration receipt, using the six frozen-identical blobs: exit 0, all shapes/base/probe/genuine/pin/floor/constant checks green. This is not a final landing receipt. Selftest executed 7/7; in-memory fault injection making the wrong-world base reader accept causes exit1 naming wrong-world-control-fails-base-arm. The selftest's case inventory at 327-329 compares two identically constructed local lists rather than a frozen inventory (decorative observation). RG-3 affects validate.

Predicate survival: **not fully enforced**, because two green work-dir runs can be replaced by failed runs without changing the verdict (RG-2).

## controls.py

Seven controls map directly: base wrong-rev acceptance 118-133; constant-validator rejection 135-146; base exec-format traceback 148-161; base impostor log existence 163-177; new impostor sha refusal and absent log 179-196; base target3/no-static 198-208; new producer-sha rejection 210-221. Each failed condition appends a named failure, final ok derives from failures 223-226/285. No printed comparison omitted from verdict. Base impostor control intentionally checks execution presence, not success of the refusal. Controls do not independently enforce C3 old target !=4 diagnostic, but the canonical checker does at packed-elf.py:404-405.

Executed at freeze: all seven green, exit 0. No --selftest exists. Empty-object --validate exits 1; contradictory seven-false-arm fixture exits 0 (RG-3). Control outcomes survive; validator honesty does not.

## Container and gate

claims.json has top-level instruments map for all six full tools/round-70 paths; predicates in claims name full paths; loaded_by_counter adds the three round-69 pins. The exact requested freeze-gate command executed, exit 0. Its round-70 entry has verdict CLEAN, findings [], freeze 4737a542; all nine instrument paths audited. Other historical containers remain flagged (the gate's process exit 0 does not mean the whole historical registry is clean). Raw output: freeze-gate.txt. M69-1 container-shape fix survives this audit.

## Residual risk and verification gaps

No admission/integration recommendation beyond this review. Final landing receipt was absent; no fresh four-carrier REA measurement or complete new/base seam execution was performed. All six source hashes match the freeze, and no post-freeze edits were introduced. Finite battery success is not a signature or durable proof that runtime observations occurred. Runtime continuity/same-identity rerouting and resume_continuity_v1 are not implemented by these six standalone instruments and are outside the canonical three predicates; no saturation score was recalculated or claimed.

Verification evidence: executed-checks.json, controls.json, forged-declaration.json, negative-probes.json, green-run-rc-not-folded.json, forged-selftest-negative.json, supplied forged JSON fixtures and freeze-gate.txt. No tools installed/updated.

Self-evaluation (1–5): accuracy 4 (source/fault evidence distinguished from landing evidence); completeness 4 (all clauses mapped, missing final landing measurement explicitly excluded); clarity 4 (six instrument sections plus severity order); actionability 4 (named lines and saved reproductions, no out-of-scope fixes); conciseness 4 (long clause map required by assignment). Overall 4.0. Highest-impact next evidence is canonical landing receipts, then adversarial runtime-authenticity checks; reviewer findings do not admit the claims. Would the user agree: likely, with the landing gap retained explicitly.

VERDICT: not-met — RG-2 leaves C1 two-green-run clause unenforced; RG-1 receipt runtime arms remain asserted; round-70 freeze container audits CLEAN.
