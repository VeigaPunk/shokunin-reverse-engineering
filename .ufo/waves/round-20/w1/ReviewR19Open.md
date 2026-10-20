# ReviewR19Open — round-19 Open/residual-limits/Mistakes vs the routed D1-D6

Reviewer: KaidokuR20.ReviewR19Open-2 (read-only leaf). Scope: `corpus/lessons/round-19.md` Open
(:95-101), residual limits (:180-191), Mistakes (:82-91), mapped against the round-19 outside
check's routed defects (`corpus/lessons/round-19-verifier-spotcheck.md:178-190`, D1-D6) and the
round-20 interfaces (`​.ufo/waves/round-20/contract.md:36-70`). No installs performed.

Method ([O]; all read-only, no gate/counter executed — closure discipline):
- `git --no-optional-locks rev-parse refs/heads/main` → `d1d981d2cc041dda4656c5b01d2c8445d8d17124`, exit 0.
- `git --no-optional-locks diff --stat 14f0260ad319ecc26994381b2415d5a999003375 -- corpus/lessons/round-19.md corpus/lessons/round-19-verifier-spotcheck.md` → empty, exit 0.
- same diff for `.ufo/waves/round-18/tools/jj-red-before.py .ufo/waves/round-19/tools/routed-r18.py .ufo/waves/round-19/w1/R12Disclosure.md .ufo/waves/round-19/w1/LiveConfigPins.md corpus/SOURCES.md corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` → empty, exit 0.
[I] All cited bytes are baseline-identical, so round-19 line anchors are valid at B=14f0260.

## Coverage map (observation unless labelled)

| Round-19 item | Anchor | Routed to | Verdict |
|---|---|---|---|
| Census undeclared blocks (SCORECARD 2380-2382, SKILL 511-519) | round-19.md:98 | D4 (contract.md:53-54; spotcheck:186-187) | covered; scope re-key with true class, checks not widened |
| head-rev-lint nested compare-only reads | round-19.md:99 | D6a (contract.md:56-57) | covered; r19 inherited patch was rejected (`round-19.md:33`, selftest FAILED 3) and is correctly re-scoped, not carried |
| Citation snapshot-slug read escape | round-19.md:180-181 | D6c (contract.md:62-64) | covered |
| Validator decoy `analyze` token | round-19.md:181-183 | D6d (contract.md:65-67) | covered |
| wave-outcomes `causes` key collision | round-19.md:183 | D6e (contract.md:68-69) | covered |
| jj sandbox selftest coverage limits | round-19.md:184 | D6f (contract.md:70) | covered; the r19 gap is concrete: selftest had 9 cases, none over the env-inheritance path of the in-process `revpin` call (`w2/SkillRegistryOld.md:38`, `w2/ReviewJjRedBefore.md:46-48`, fix shape `w2/ToolJjSandbox.md:9`) |
| Trusted-revision import trust / mkdtemp not a sandbox | round-19.md:177-179 | D6b (contract.md:58-61) | **partial**: D6b sandboxes only extracted REV blobs; the same bullet's "trusted lane Python/JavaScript is still executed by checker/catalog tools" (live working-tree execution) stays outside its interface |
| Unmasked-variadic full-walk bug | round-19.md:188 | **not in D-set**; C3 (claims.json claims[2]) | addressed by C3's masked v2 + first_failure forecast, not by D1-D6 |
| Prior vet prediction exposure | round-19.md:187 | not in D-set; C3 process only | covered only by C3's freeze-before-analyze rule (claims falsified_if "a run starts before the freeze push"); no mechanism fix exists or is routed |
| Physically unattainable multi-index exact forecast | round-19.md:188 | none | open by reformulation: v2 changes the forecast target (first failure) rather than fixing the old one; the full-list forecast stays falsified (round-19.md:118-119) |
| Compile's separate RTTI NPE | round-19.md:189 | none | open; recorded separately, no routed owner |
| D1 selftest residue / D2 future timestamp / D3 carrier execution / D5 census at tip | spotcheck:180-188 | D1, D2, D3, D5 (contract.md:38-52,55) | covered, each interface carries a refusal/tamper case |

## Not covered by D1-D6 and still open

1. **Round-12 custody/precondition residuals** (round-19.md:97) — no D item. [O] The recheck
   precondition is now false on this host: `/usr/bin/docker` upgraded 1:29.7.2→1:29.9.1 at
   09:16:36 -03, sha256 `566a4e83…` vs recorded `70f68a77…`, and both retained copies are absent
   (`w1/R12Disclosure.md:33-36,99-100`; entry recheck line still pins the old hash,
   `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md:7`). The entry's recheck
   instruction is unactionable until fresh copies are made; disclosure-only. [I] Also open: the
   C1 custody addendum's "no pre-pair, post-only captures, current configs outside the last
   receipt" limitation (round-19.md:97; S039 scope, `corpus/SOURCES.md:45`) — inherent to the
   evidence class, no fix routed.
2. **jj adjacency / S036 triple registration, no L0 line** (round-19.md:100) — no D item. [O]
   kaidoku retains S036 for its pin tools only (`corpus/SOURCES.md:42,53`); the fact is routed to
   kumitate (`JjConnectorProvinces.md:181,189` per round-19.md:100). [I] Cross-lane duplication
   (tameshi S061, tabi S049) remains unresolved at fleet level; correctly reported as not
   lane-owned, but it is not "closed" either.
3. **Operator-config `enabled:false` drop** (round-19.md:101) — no D item, operator-owned. [O]
   Flag last recorded in the 13:35:56 recovery copy; the same write bumped the pin and dropped
   the flag (`w1/LiveConfigPins.md:54-63,73-77`); writer remains unidentified
   (spotcheck:124-127). [O] An explicit open decision is parked in the seat report: whether
   PROVINCE may state the disable state (it cannot, as a live fact, since 13:35:56) —
   `LiveConfigPins.md:100-103`. No round-20 item answers it.
4. **W1 reportless seats (42/90)** (round-19.md:91, Mistakes 6) — no D item, no fix. [O] Only
   disclosure exists (`w1-terminal.json` retained; "do not infer death or absence solely from
   report presence", round-19.md:91). [I] No process change was routed to reduce recurrence
   (provider 429s / parent-session aborts), so this stays an open operational risk.
5. **Known model weaknesses** (round-19.md:187-191) — see map: only the variadic bug has a routed
   worker (C3); vet exposure is process-guarded only; multi-index forecast and compile RTTI NPE
   remain open with no owner.

## Fixes not shown able to fail (or falsifiable only in a narrowed sense)

- **Mistake 5 / carrier execution** (round-19.md:90): r19 itself says "No demonstrated enforcement
  fix". D3 (contract.md:46-52) supplies prevention-by-exec-bit + mode/ctime/content detection with
  `exec_refused`/`mode_restored` selftests — falsifiable by construction — but its own declared
  limits leave loader-mapped execution (`ld-linux … <file>`) and root unprevented, and execve does
  not change ctime/mode, so an ld-linux run after arm would leave no `check` finding. [I] The
  routed breach class is therefore narrowed, not closed; residual stays open by declaration.
- **D2 blind spot** (contract.md:41-45): only timestamps *with an explicit zone* are checked. [I] A
  future-dated naive local timestamp escapes the tool; the r19 defect happened to carry `-03`.
- **Mistake 3 / strict baseline** (round-19.md:88): able to fail for result drift — the substance
  check replays the pinned tool blob at 9011581 and requires byte-identical exit/stdout/stderr
  (`routed-r18.py:222-236`, comment at :222-223 "verifies its result, not the historical
  process's time/authenticity"). [I] Historical authenticity of the original run rests on the
  outside closure's independent re-measure (spotcheck C1 table), not on any lane tool.
- **Mistake 6** (round-19.md:91): no fix exists; nothing to fail.
- Mistakes 1/2/4 fixes each carry demonstrated red-before (wave-outcomes exit 1 with 4 uncaused →
  green; routed-r18-B.json red at 8a8da7e; province-pins 2→0 and census stale 4→0 red at
  8a8da7e) — round-19.md:86-89, spotcheck-verified. Not defects.

## In-flight observations (not verdicts; judged by L1/VerifyR20)

- [O] `evidence/census-start/meta.txt` (17:44:13-03): c1-census exit=1 at tip d1d981d — D4/D5
  red-before captured before the fix; sources-census exit=0.
- [O] `evidence/d1-residue-before.txt` (17:42:59): the two untracked nested-repo dirs still
  present in the working tree — D1 red-before captured.
- [O] `w1/patches/` currently holds only CausesKeyCollision-2.patch and RizinLeg-2.patch; all
  other D-fix deliveries were not yet on disk at review time. No completeness claim made.

## Residual risk and verification gaps

- Every D-fix interface carries a refusal/selftest case (contract.md:38-70) and claims C1's
  falsified_if rejects token-only closures (claims.json claims[0]) — the set is able-to-fail by
  design; delivery and selftest-clean status are outside this review.
- D6b's sandbox is unshare-based (bwrap absent, contract.md:60-61): [I] kernel-support dependent;
  live checker execution of trusted lane code (round-19.md:178) remains unsandboxed after D6b.
- I did not execute any lane gate, counter, or REA/Ghidra/Go tool; number-level verification of
  D-fix outcomes belongs to VerifyR20/L1 and the outside closure.
