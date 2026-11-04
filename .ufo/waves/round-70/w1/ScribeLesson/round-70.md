# Round 70 — producer-bound receipt readers, a safe packer seam, and a static-executable carrier

Lane `kaidoku`, round 70, attempt 1. Base `5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d` (the round-69 non-author closure carry-in); operative declaration `8b82516182a269482f3a7dc96b50cd2ac349f3a6`; operative freeze `4737a542ae3b1b910d8fe43efbd572bc578b07c6` (the commit that first adds the claims container). Declaration plan: `plans/round-70-claims.md`; container: `.ufo/waves/round-70/claims.json`. The container also records initial declaration `2c77672509517c773e0687c86dba5266ef329e83` before the operative declaration fix.

Three declared claims on three axes, all capability acquisitions (declarations, not results):

- **R70-C1 — calibration:** bind receipt readers to their producers; ten forged shapes must pass the base reader and fail the frozen reader on their named clauses, identity shapes must fail the hardened probe, genuine receipts must pass, and the mutation battery must enforce its pin, pristine floor, distinct per-run work directories and constant-receipt rejection.
- **R70-C2 — operability:** seven safe-packer seam arms — hash before execution, thread the pinned-copy path, allowlist child environment, type broken-node and packer exec-format errors, avoid the temporary-directory HOME fallback, and isolate per-run work — must score 7/7 after and 0/7 at the base. The subprocess environment candidate below grounds A3/A6; admission remains evidence-dependent.
- **R70-C3 — coverage:** add `/usr/bin/docker-init` as kind `static-exe`, pinned sha256 `0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115`; require four bound carriers and reject the old receipt on producer binding. The plan declares original inventory 1268/29/1111, packed 3/3/5, ceiling 10/1268 = 0.0079; independent wave confirmation: <L1 fills: measured revision, receipt and static-carrier measurements>.

The intended wave is the single v1 build+attack wave `w1`: 15 seats within the 8–16 band, with reviewer ×2, critic ×1 and mutation-tester ×2 (5/15 = 33%). Execution and settlement: <L1 fills: registry/result evidence, completed seats and attack share>.

## Gate

Candidate decisions below must be supported by the scout's fetched bytes and located quotes, not by this draft's declaration. No source was fetched by the lesson scribe.

| candidate | fetch | located quote / reason | decision |
|---|---|---|---|
| S272 — `https://docs.python.org/3/library/subprocess.html#subprocess.Popen`, Python 3.15.2 documentation | Scout fetch 2026-11-04T04:17:30Z, HTTP 200, 208 648 B, sha256 `4b88b8316a05baadaa7b2dd254c320a40b5406d8158a57f2a50b55b4d872a2c7`; snapshot `.ufo/waves/round-70/w1/ScoutSource/subprocess.html`, receipt `ScoutSource/sources.md:17–32` | Popen raw lines 881–883, bytes 88623–88718: “these are used instead of the default behavior of inheriting the current process’ environment” (14 words, scout count). The adjacent composite clause at bytes 88438–88591 says “If env is not None, it must be a mapping that defines the environment variables for the new process” (19 words). These are separate clauses, not one ≤25-word quote. | **ADMIT — scout assessment**, S272, tier A, `docs`: replacement versus inheritance grounds R70-C2 A3/A6, not measured arm success. S260 on the same URL concerns argv composition, not environment replacement. <L1 fills: final source decision and registry landing>. |
| `https://docs.python.org/3/library/tempfile.html#tempfile.mkdtemp`, Python 3.15.2 documentation — screen | Scout fetch 2026-11-04T04:17:30Z, HTTP 200, 75 198 B, sha256 `edf721761f0de44769b1fb817b8105447a9a8cecb1d6df1c6347a804db442560`; snapshot `.ufo/waves/round-70/w1/ScoutSource/tempfile.html`, receipt `ScoutSource/sources.md:66–84,155–190` | Raw line 485: “mkdtemp() returns the absolute pathname of the new directory.” (9 words, composite, scout count). The scout reports zero matches (exit 1) for `unique`, `distinct`, `collision`, `collide` in fetched bytes; consumer search reports 19 `mkdtemp` sites and seven hits all concerning `work_dir` distinctness, no predicate consuming mode/ownership/absolute-path properties. | **REJECT — scout assessment**, on demand, not overlap: added creation/cleanup/absolute-path claims are not consumed by a frozen claim; A7 measures differing work directories. Flip: mode/ownership/privacy or absolute-path predicate, a claim citing no creation races, or explicit uniqueness wording in the page. <L1 fills: final reject disposition; scout proposes S273 only if rejects enter the registry>. |
| <L1 fills: additional admitted candidate, if any> | <L1 fills: fetch evidence> | <L1 fills: located quote and scope> | <L1 fills: admit decision and reason> |
| <L1 fills: additional rejected candidate, if any> | <L1 fills: fetch evidence> | <L1 fills: located quote or rejection evidence> | <L1 fills: reject decision, reason and flip condition> |

Fetches and quote counts above are attributed to `ScoutSource/sources.md`, not re-executed by the lesson scribe. The source URL is mutable: the scout reports different subprocess snapshot bytes from S260; preserve this snapshot hash and locator. <L1 fills: exact recorded word-count command if required for landing>; do not silently join the two env clauses into a 33-word quote.

**Spot-check result.** `[L1 — filled by the non-author closure.]`

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M70-1 | before-arm-world | `plans/round-70-claims.md:62–67,155–158`; `.ufo/waves/round-70/claims.json` frozen atom A2: forged shapes cut from the round-70 four-carrier receipt would fail the base reader for the wrong reason (`target 4 != 3`), producing a false before-arm | The wrong-world control the forged-receipt battery's `--selftest` carries; executed selftest evidence: <L1 fills: wave receipt, command, exit and named control outcome> | Cut the forged shapes from the base-world receipt that the base reader accepts; the selftest's wrong-world control proves that the guard can fail. Execution confirmation: <L1 fills: base-world acceptance and wrong-world rejection evidence>. |
| <L1 fills: wave finding id> | <L1 fills: class> | <L1 fills: exact artifact and observation> | <L1 fills: existing criterion or none> | <L1 fills: disposition; frozen instruments remain unchanged> |

## Outcome

- **R70-C1 — <L1 fills: verified/not verified>.** <L1 fills: measured revision; exact commands/exits; ten per-shape base acceptances and named after-rejections; identity-probe A5/A6 results; genuine-reader results; battery pin/floor/per-run/constant-receipt results and artifacts>.
- **R70-C2 — <L1 fills: verified/not verified>.** <L1 fills: exact base/after commands and revisions; seven named arm observations, producer-bound pinned-copy argv, child-env registry case count and green selftest at that count; 0/7 versus 7/7 receipts or exact failures>.
- **R70-C3 — <L1 fills: verified/not verified>.** <L1 fills: exact checker command/exit, measured revision, target/matched/control/failing fields, all carrier ratios and static-executable measurements, old-receipt producer-binding failure and artifacts>.
- **Controls and attacks.** <L1 fills: seven shortcut-control outcomes, critic/reviewer/mutation findings, independent evidence and exact unresolved defects; do not treat post-freeze corroboration as a counter repair>.
- **Routed round-69 defects.** <L1 fills: evidence-backed dispositions for M69-8, M69-9/S-1, M69-10, M69-11 and M69-1; include freeze-gate evidence for the top-level instruments map and predicates in claims>.
- **No-harm / admission.** <L1 fills: axis/trend judgments, scope audit, frozen-byte checks, limitations and final admission decision; the round-69 closure rejected C2/C3 under the frozen shortcut-control rule and found quality harmed, so genuine green receipts alone cannot establish repair>.

## Census

- Start: <L1 fills: exact census command, exit, counts, warnings and committed census-start artifact>.
- End: <L1 fills: exact census command, exit, counts, admitted/rejected source ids, malformed count, warnings and committed census-end artifact>.

VERDICT: met — lesson draft prepared; wave measurements, source decisions and round admission remain explicitly unasserted pending L1 evidence.
