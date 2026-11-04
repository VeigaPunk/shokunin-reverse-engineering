# ReviewerGates — round-68 w1 clause-to-line review of the two frozen instruments

Seat: ReviewerGates (leaf reviewer). Base `fcbe200f6739c38939e0dabf3f251de2cc6bd727`; operative freeze
`1eaf596e5f241762349fbd102c9e09ec1df18e3f`. Review target: the frozen instruments vs the frozen
predicates (R68-C1, R68-C2), the container pins, and atom order. No counter executed beyond
`--selftest`; nothing edited; no tool installed or upgraded; no pacman transaction; no LSP device is
mounted in this session, so all semantic checks are text-level on sha-verified freeze bytes
(equivalent here: working bytes hash-equal the freeze blobs, so line numbers cited are freeze line
numbers). Every conclusion below is labeled observation / inference / unknown.

## 1. Pin integrity (observation)

| file | working sha256 | claims.json `instruments` | freeze `git show 1eaf596:<p>` sha256 | verdict |
|---|---|---|---|---|
| tools/round-68/registry-conformance.py | a300d831…8315 | a300d831…8315 | a300d831…8315 | identical |
| tools/round-68/packed-elf.py | 48ef4c68…276e | 48ef4c68…276e | 48ef4c68…276e | identical |
| tools/round-68/controls.py | 0657ee08…8fb4 | 0657ee08…8fb4 | 0657ee08…8fb4 | identical |

Both commits resolve; freeze blobs exist (mode 100755). A0 order verified (observation):
`git merge-base --is-ancestor 6020eb60 1eaf596e` exit 0; first-add commits — all three instruments,
all three `l1/pre/*.json` receipts at `6020eb60`; `.ufo/waves/round-68/claims.json` first-added by
`1eaf596e` itself, matching the container's own freeze-identification rule.

Selftests (the only executions performed, observation):
- `registry-conformance.py --selftest` → `{"cases": 11, "failed": [], "ok": true}`, rc 0.
- `packed-elf.py --selftest` → `{"cases": 13, "failed": [], "ok": true}`, rc 0.
Both match the declared 11/13 case inventories (registry-conformance.py:63-75; packed-elf.py:65-79),
each closed by the registered case-inventory assertion (registry-conformance.py:267;
packed-elf.py:336) — QUALITY #109 satisfied.

## 2. R68-C1 — clause → implementing line (registry-conformance.py, 296 ln)

| predicate clause | line(s) | notes |
|---|---|---|
| "frozen registry-conformance census" | 183-192 (`run_score` stamps receipt `instrument.sha256` from `__file__`) | verdict layer compares receipt sha to the container pin a300d831…; the committed base receipt bears exactly that sha (observation) |
| "run at the measured revision" | 186 (`result["rev"] = rev`); all reads at `--rev` via `git show/ls-tree` 163-180 | — |
| "reports mismatches 0" | 136 (`mismatches` = sum of four named sets); 151 (`ok` = mismatches==0 AND scope>0); 197 (exit 0 iff ok) | the extra `scope>0` guard is stricter than the predicate — safe direction |
| "scope_size 71" | 125 (`scope = regime ∩ existing`); reported 140-141 | arithmetic below |
| "registry_rows 77" | 82-98 (rows = backticked cell-0 lines between the v2 markers 54-55; marker-count guard 83-84); reported 142 | header/separator rows cannot match ROW_RE:58 (needs backticks) — live SKILL.md:1782 header is unbackticked (observation) |
| base "mismatches 2 … names exactly <r67 pair>" | 130 (`unregistered` sorted list); "exactly" discharged as list equality in the control arm controls.py:93-104 | base receipt c1-at-base.json: mismatches 2, unregistered == [avm-le-counter.py, mutation-battery.py] (observation) |
| regime: own round | 108-118 (`own = tools/round-N/`; foreign round `continue` at 114-115 BEFORE `named.add`) | A4 "a foreign round's tool is not scope" holds; also never named_but_absent |
| regime: N ≥ 41 | 53 (`REGIME_START = 41`); 117 | — |
| regime: exists-at-rev | 125 | — |
| rounds < 41 never counted | 117 (legacy bucket); 135 (`legacy_unregistered`); excluded from the mismatch sum at 136 | base receipt legacy list = 26 entries (2+3+1+3+7+10) matching A1 (observation) |
| named_but_absent reported, excluded | 126; excluded from scope by 125 | base receipt = 12 entries (6+6), matches A1 (observation) |
| four mismatch sets | 130-133 (unregistered, duplicate_rows, row_absent, thin) | — |
| thin verdict grammar | 59-61 (VERDICT_RE) applied 133-134 | grammar = "digit at cell start or after `;`/`|`/space, then `=`/`:`/space+word" — implements A4's thin definition; see ADV-4 |
| `--selftest` inventory assertion | 200-272; assertion 267 | 11 cases, green (observation) |
| exit contract 0/1/2 | 197 (0/1); 282-283 (selftest); 284-286 (bad argv → 2); 288-292 (Unevaluable → 2) | matches plan lines 34-35 |

Predicate arithmetic (inference from committed state, confirmed achievable): base scope 69 + the two
round-68 counters named by the round-68 plan (plans/round-68-claims.md:34,67 — the only
`tools/round-68/` paths the plan names; controls.py is NOT named, see ADV-6) = 71; rows 73 + 4
(r67 pair at SKILL.md:1858-1859, r68 pair at :1860-1861, present at HEAD mid-wave) = 77; mismatches 0
requires the four new rows to be non-thin (their cells use `0=…; 1=…; 2=…` grammar, passes 59-61) and
present as blobs (they are the frozen files). The frozen numbers 0/71/77 are exactly the ones the
declared repair surface produces. The L1's measured-revision run decides; unobserved by me (unknown).

## 3. R68-C2 — clause → implementing line (packed-elf.py, 368 ln)

| predicate clause | line(s) | notes |
|---|---|---|
| "carriers_matched 2 of target 2" | fold 123-127; verdict assembled 292-293 with `target = len(CARRIERS)` | — |
| "control_ok true" | per-carrier 275-277 (`upx -l` rc≠0 AND `upx -d` rc≠0 on the ORIGINAL copy); folded over both carriers 292-293 | "neither listed nor decompressible" implemented on the non-packed original, both carriers required |
| detected | 248-249 (`upx -l` rc 0 AND `readelf -SW` section count 0; section_count 94-99) | matches A7 |
| before_ok uses the carrier floor, NOT the packed count itself | 252-254: `floor = min_orig_procedures // 2` (253), `before_ok = packed procedure_count < floor` (254); floors 50 (jq, 100//2) and 25 (xxd, 50//2) | confirmed: the arm compares against the carrier's declared floor, never a self-referential packed value; also guards counts_from()=None |
| identity_ok vs the PIN, not an in-run value | 256-258: `sha256_file(unpacked) == c["sha256"]` where the pin is the CARRIERS constant 56-63; drift pre-checked → Unevaluable 233-235 | confirmed: compares against the frozen pin, not anything derived during the run |
| recovery_ok vs ORIGINAL counts | 259-261: `rec_counts == orig_counts` where orig_counts is REA's inventory of the pinned original copy (236-240) | confirmed: unpacked is compared to the original, on all three counts (procedure/segment/string; counts_from 101-111 requires all three ints) |
| refusal_ok on the carrier that pins an address | 262-273, gated by `c.get("address")` 264 — jq only (0x103fa0 / FUN_00103fa0 at 59); refusal_ok = packed rc≠0 AND unpacked rc 0 AND pinned symbol in code AND len(code)>200 (268-269) | stricter than A7 by the >200-byte floor — safe direction |
| "packed bytes at exactly 3 procedures" | REPORTED, not enforced: before_procedures captured 252, payload list 294, per-carrier packed_counts 280-294 | no `== 3` assertion exists; exit 0 is possible for any stub count < floor (e.g. 2, 4, 7). The predicate discharges this at the receipt-vs-target comparison (claims.json target `before_procedures [3, 3]`). Verdict layer must compare the receipt; exit 0 alone is not C2 verification. See ADV-5 |
| pins (A6) | carriers enforced 233-235; REA package.json sha + version enforced 182-190; npx lock recorded-not-pinned 191-205; CLI `node <pkg>/scripts/rea.mjs` 136-137 (never npx -y) | upx RECORDED but never enforced — ADV-2 |
| skip-run never claims | 207-214 (`verdict_claimed: false`, `met_target: null`, rc 1) | matches selftest case skip-run-no-claim 331-334 |
| exit contract 0/1/2 | 302 (0 iff met_target AND failing empty; failing names every false arm 296-297); 353-357 (bad argv → 2); 358-364 (Unevaluable → 2) | matches plan lines 67-68 |

Kill-rule coverage check (observation): carrier pin drift → exit 2 (233-235); REA drift → exit 2
(186-190); detection on original → control_ok false → exit 1 (275-277, 292-293); unpack not
restoring pin → identity_ok false → exit 1 (256-258); inventory ≠ original → recovery_ok false →
exit 1 (259-261); packed inventory ≥ floor → before_ok false → exit 1 (252-254); refusal not
separating packed/unpacked → refusal_ok false → exit 1 (268-269); undisclosed post-freeze edit →
receipt instrument.sha256/rev (167-175) exposes it to the verdict layer. "Detection fires on the
unpacked bytes" is not directly run, but identity_ok (256-258) makes unpacked ≡ original bytes and
the control proves the original is not listable — derivable, sound (inference).

## 4. Findings by severity

**Blocking: none.** Every clause of both frozen predicates maps to an implementing line; both
selftests are green; all three pins are byte-identical to the freeze; A0's declaration order holds.

**ADV-1 (top advisory; conditional-blocking for the verdict layer) — C2 before-arm provenance.
observation.** `.ufo/waves/round-68/l1/pre/c2-dryrun-at-base.json` records
`instrument.sha256 = 7ee286c03391dc464c90a3f24498258bfef09dd89300aa9a246fd35ac85ef25c` — NOT the
frozen `48ef4c68…276e` — with `rev: "main"` (not the base sha) and `instrument.rev: null`. The
committed C2 before-state evidence was therefore produced by a pre-freeze draft of packed-elf.py.
The C1 pre receipt, by contrast, bears the frozen a300d831… (its c1-base arm is also re-derived live
with the frozen module at controls.py:55-59). The edit pre-dates the freeze commit, so no kill-rule
clause fires and `instrument_supersessions` is technically not violated — but nothing in the
container (A0/A2) discloses the draft→frozen divergence. Conditional edge: if the verdict layer ever
cites c2-dryrun-at-base.json as C2's verifying receipt, the claim would be verified on non-frozen
bytes; the frozen counter must produce the measured-revision receipt itself. Recommend one disclosed
erratum line in the round report (or a fresh base dry-run with the frozen bytes).

**ADV-2 — A6's "packer pinned by sha256 and version" is recorded, not enforced. observation.**
packed-elf.py:53 (`UPX_SHA256 = None  # set at run time; recorded in every receipt`) and :175-181
(upx sha/version computed into the receipt env, never compared to any constant). A host upx change
between the base dry-run and the measured run is invisible to the exit class. Carriers (233-235) and
REA (182-190) are enforced; the packer is not. The iff sentence has no packer clause, so this does
not block the predicate — but A6's wording overstates the code.

**ADV-3 — exit-2 contract broken on a broken environment (fails closed, mislabeled). observation.**
Docstring packed-elf.py:27-28 promises exit 2 for "missing upx/node" and "a refused --work root".
- `rea()` 136-137 invokes bare `"node"` with no `shutil.which` guard → missing node raises
  FileNotFoundError, uncaught → traceback, exit 1 ("not met") instead of 2; :204-205 records
  `which("node")` but never asserts it. The live SKILL.md row (:1861) repeats the "absent upx or
  node" exit-2 claim.
- :179 `run([UPX, "--version"])…splitlines()[0]` → IndexError if upx exists but prints no stdout.
- :359 defaults `--work` to "/proc/self/fd"; `mkdtemp` at :221 inside procfs raises uncaught OSError
  → exit 1 instead of the promised exit-2 "refused --work root" (only reachable when --work is
  omitted; the frozen counting command always passes it).
No false-green path exists in any of these — severity advisory (diagnostics, not verdicts).

**ADV-4 — thin-grammar edge cases, both safe-direction. observation.** registry-conformance.py:59-61
rejects comma-tight lists ("`0=met,1=not met,2=…`") as thin (comma is not in the separator class) →
a false mismatch, never a false green; live new rows use "; " separators and pass (SKILL.md:1860-1861).
The thin check grades only the first row's verdict cell for a duplicated path (:133-134, `r[0]`);
duplicates already mismatch at :131, so no clause is weakened.

**ADV-5 — "exactly 3 procedures" is a receipt-level check, not an instrument arm. observation.**
See the C2 map row above; by design faithful to the predicate's wording ("reports … at exactly 3"),
but the verdict layer must compare `before_procedures` to `[3, 3]` — exit 0 alone under-determines
the clause.

**ADV-6 — scope self-exclusions, declared but worth naming. observation.** controls.py is a
round-68 tool its own plan never names (plans/round-68-claims.md names only the two counters at
:34,67), so the census regime cannot see it — consistent with the declared regime (own-round
plan-named tools) and A5's four-row repair surface; the lane's control driver is itself an
unregistered instrument by construction. Also `instrument.rev` in both receipts comes from
`git log -1 -- <TOOL>` at HEAD (registry-conformance.py:186-192; packed-elf.py:167-175): for a
non-tip `--rev` it names the newest bearing commit, not necessarily an ancestor of `--rev` — honest
null in the pre receipts; an A9 interpretation note for the verdict layer.

**ADV-7 — controls.py docstring inaccuracy. observation.** controls.py:5-6 says the driver "never
runs REA, upx or git", but `arms()` at :58 calls `read_revision(LANE, BASE)`, which shells read-only
git (registry-conformance.py:163-180). Harmless (read-only), but the header misdescribes behavior.

## 5. Residual risk and verification gaps

- The counters were not executed beyond `--selftest` (bound). The measured-revision after-state
  (mismatches 0 / scope 71 / rows 77; carriers_matched 2/2, [3,3], every arm true) is unknown to me —
  the L1's runs decide. (unknown)
- Because controls never run REA/upx and the C2 pre receipt came from draft bytes (ADV-1), the C2
  before-state is not currently re-derivable from committed frozen bytes alone; only a fresh
  frozen-instrument run at `--rev fcbe200…` would close that gap. (inference)
- The SKILL.md repair is in flight mid-wave; I confirmed only that the four new rows exist at HEAD
  with passing thin grammar. The registry at the measured revision is the L1's measurement surface.
  (unknown)
- No LSP device mounted this session; clause checks are text-level on sha-verified freeze bytes.
  (observation)

## 6. Verdict

No blocking defect. Both frozen instruments implement every clause of their frozen predicates at
mapped lines, fail closed on every degraded path, and carry green selftests (11 + 13 cases, rc 0).
Seven advisories, one of which (ADV-1) must be respected by the verdict layer: C2's verification
receipt must come from the frozen 48ef4c68… bytes, and the dry-run draft divergence deserves a
disclosed erratum.

Tooling record: nothing installed or upgraded (official-channel rule N/A); no pacman transaction
run; writes limited to this report's two paths; scratch `/fast/scratch/hyaku/kaidoku-r68/ReviewerGates/`
created and removed before yield.
