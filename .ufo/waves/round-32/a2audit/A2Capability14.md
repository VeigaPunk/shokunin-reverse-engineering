# A2Capability14 — R32-C2 v3 round-14 quote-regression audit (independent re-open)

- Seat: `KaidokuR32A2.A2Capability14` (leaf, no delegation)
- UTC timestamp: 2026-10-23T06:54Z (runs at ~06:50-06:52Z)
- Lane: kaidoku-shokunin (read-only); scratch: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2Capability14`
- Pins opened: fleet `cef00867ab3279ac2c2d10421e3e62c0e5d693f3` (MANIFEST.json); lane base `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525` (SCORECARD.md + anchors)
- Sandbox: fresh clones created 2026-10-23 ~06:48Z — fleet clone HEAD `575bcedac44943fae1cd43f9030aea7662ddb6be`, kaidoku clone HEAD `f382e3b7978e6091a19ca93277c15a75c0016b43` (= C2 v3 freeze commit); `git -C` absolute, GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset throughout. No lane/fleet writes, no git writes outside clones.
- Freeze integrity checks (sha256):
  - claims-v3.json @ `f382e3b7` = worktree = `a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d`
  - claims.json @ `9a73680a` = worktree = `8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435`
- Extracted artifacts (from pins; sha256 / size):
  - `manifest_cef00867.json` `2e089615936dae60d1b4ab3883dbbc8ed7608018b9c7f4694209207d84b3207f`
  - `SCORECARD_base.md` `bba9f55de85001d6259ed728bdec82a20dd49830ccb9e01634909bb14c9c38e3` (3267 lines)
  - `expected.json` `ef3714bbb77df1f03db0de325f6c49ea1a8bbf66a1fdeecdd2e8bb3d5474cadf` (64 lines)
  - `verification.json` `dd1c57912a98039af99985063dc7e08697b836bbd41ef8e50b18062f2a5a5a9c` (163 lines)
  - `quote-fidelity.py` `0d939e231d73e02fab8898cd0f79f65ea2f6811e9300884c7e694992e19866d8`
  - round-14 subtree extracted via `git archive 283aad7f .ufo/waves/round-14 | tar -x` → 849,136 bytes (≤1 MiB bound)

## 1. Fleet MANIFEST at cef00867 — round-14 closure record (outside, non-author)

Round-14 kaidoku closures in MANIFEST: two entries — train `2026-10-16` (luna-round-10, no `capabilities_added`) and closure `2026-10-20` (type closure, `admitted: true`). The closure entry is the one carrying `capabilities_added`:

> "local raw-quote/heading regression audit (bounded retained-defect controls; committed CLI and frozen evidence)" — MANIFEST.json @ cef00867, round-14 closure entry `capabilities_added[0]` (extracted file line 7195).

Closure metadata: `closed_at: 2026-10-20T05:44:40Z`, `commit: kaidoku-shokunin@9719dd232687f5ee78a4ed323b37f8810e833d10`, `verification.reviewer: "hyaku-closure (@m_strong session, non-author)"`, spotcheck pointer `corpus/lessons/round-14-verifier-spotcheck.md@9719dd232...`. This is the outside-recorded closure item (fleet ledger, non-author closure) that the C2 statement targets. The statement's frozen key `14 /quote.{0,40}regression audit/` matches the item's wording (`quote/heading regression audit`), and no other key pattern appears in the item.

## 2. Base SCORECARD at 283aad7f — section vs deeper record

- `## Capabilities` section (:615-626) at base holds exactly 5 rows: luna-round-6, luna-round-8, arc2-loop1-round2, arc2-loop1-round7, round 27. No round-14 row → at base the section credits 1 of 4 outside-recorded capabilities (round 27), consistent with the C2 surface.
- Round-14 capability row exists deeper, in the append-only `### Capability addition` table of the Round-14 section at :2208:

> "| local raw-quote/heading regression audit | Rejects the retained S017 splice and S018 wrong section, accepts corrected controls, and refuses malformed/tampered inputs; frozen runs pin every manifest/source input | `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --selftest` → 28/28; same script `--frozen .ufo/waves/round-14/fixtures/expected.json` → seven expected verdicts matched; source commit above, `.ufo/waves/round-14/verification.json` | round-14 |" — SCORECARD.md:2208 at 283aad7f (re-opened from base blob).

- Earlier observation at :3116 (re-opened): the section is the 4-row summary (at that point; 5 at base tip) while the card holds deeper capability rows at :2135/:2207/:2374 (rounds 13/14/17) — "so a reader of `## Capabilities` alone undercounts by 3". This matches the C2 surface text and confirms the calibration gap was observed, not repaired, at base.
- Row first cell matches only key 14 (no `source registry`, `Ghidra-session log capture`, or `cross-pin evidence-ID attribution` substrings); last cell `round-14` names exactly the MANIFEST round.

## 3. Anchors re-opened at base — evidence demonstrating capability

Frozen anchors for statement 14 (claims-v3 `anchors_at_freeze["14"]`) all resolve at base (extracted from 283aad7f, hashes above):

1. `.ufo/waves/round-14/fixtures/expected.json` — frozen expectations for 7 manifests (exit + findings class@id per manifest) and 2 sources (s017-view8-readme-usage-deterministic.html, s018-checkpoint-introduction-decompiled.html), each with sha256 pin. Manifest pin for s017-red (`e7f19e73…`) equals the base blob hash, e.g. expected.json "manifest-s017-red.json": exit 1, findings `quote_not_contiguous@S017-Q1`.
2. `.ufo/waves/round-14/tools/quote-fidelity.py` — gate tool; docstring (lines 4-6): "Verifies that every manifest quote is a located, contiguous, <=25-word excerpt of a locally captured source. The gate is read-only: no network, no subprocess, no writes outside the self-test's TemporaryDirectory." Verdict contract: exit 0 clean / 1 failed / 2 could-not-evaluate; frozen mode hashes every pinned manifest and source before evaluation (snapshot_tampered on missing/altered input).
3. `.ufo/waves/round-14/verification.json` — committed command records with exact argv and stdout. Relevant entries:
   - `quote-selftest`: `python3 -I …/tools/quote-fidelity.py --selftest`, exit 0, stdout "QUOTE_FIDELITY_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0".
   - `quote-frozen`: `python3 -I …/tools/quote-fidelity.py --frozen …/fixtures/expected.json`, exit 0, stdout "QUOTE_FIDELITY_VERDICT: clean mode=frozen manifests=7 findings=0 exit=0" with all 7 `expected=… actual=… match` lines.
   - `s017-red`: `python3 -I …/tools/quote-fidelity.py --manifest …/fixtures/manifest-s017-red.json`, exit 1, stdout "QUOTE_FIDELITY: quote_not_contiguous ident=S017-Q1 no contiguous occurrence in source".
   - `s018-red`: same `--manifest` form, exit 1, stdout "QUOTE_FIDELITY: quote_location_mismatch ident=S018-Q1 quote lies outside the declared section".
   - `s017-fixed`/`s018-fixed`/`quote-corrected`: exit 0, "clean quotes=1/2 findings=0 exit=0".

## 4. Exercised reproduction (scratch only; no lane writes, no carriers, no REA)

Pinned tree extracted at base into scratch; ran the gate read-only:

```
argv: python3 -I -B tools/quote-fidelity.py --selftest
      (cwd = scratch r14/.ufo/waves/round-14; ulimit -v 4194304)
exit: 0
stdout tail: QUOTE_FIDELITY_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0

argv: python3 -I -B tools/quote-fidelity.py --frozen fixtures/expected.json
exit: 0
stdout tail: QUOTE_FIDELITY_VERDICT: clean mode=frozen manifests=7 findings=0 exit=0

argv: python3 -I -B tools/quote-fidelity.py --manifest fixtures/manifest-s017-red.json
exit: 1
stdout: QUOTE_FIDELITY_MANIFEST: …/fixtures/manifest-s017-red.json
        QUOTE_FIDELITY: quote_not_contiguous ident=S017-Q1 no contiguous occurrence in source
        QUOTE_FIDELITY_VERDICT: failed quotes=1 findings=1 exit=1
```

All three exits and verdict lines reproduce the committed `verification.json` records identically at the same revision. Replayed inputs hash to the pinned blobs (expected.json ef3714bb…, manifest-s017-red.json e7f19e73…, quote-fidelity.py 0d939e23…). This demonstrates the recorded capability behavior (reject splice / wrong-section, accept corrected controls, refuse malformed/tampered inputs, frozen replay pins) executes from the frozen artifacts; it does not prove the historical runs at round-14 time occurred as recorded (only that committed evidence replays identically now).

## 5. Draft summary row (faithfully copied — drafted only, no lane edit)

Per assignment, drafted only if evidence exists (it does, §3-4). Faithful copy of the base append-only row (:2208), which matches MANIFEST capabilities_added name and all v3 predicate elements (key-only match, one round `round-14`, evidence cell names anchor paths inside backticks that resolve at REV, description cell shares the anchored description verbatim):

```
| local raw-quote/heading regression audit | Rejects the retained S017 splice and S018 wrong section, accepts corrected controls, and refuses malformed/tampered inputs; frozen runs pin every manifest/source input | `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --selftest` → 28/28; same script `--frozen .ufo/waves/round-14/fixtures/expected.json` → seven expected verdicts matched; source commit above, `.ufo/waves/round-14/verification.json` | round-14 |
```

No summary repair run was executed and no lane/fleet file was edited (controls land first; L1 owns integration). The MANIFEST item's fuller name carries the parenthetical "(bounded retained-defect controls; committed CLI and frozen evidence)"; the row's first cell omits it, which still satisfies the key pattern.

## 6. Semantic vs lexical overlap limits

- Counter identity is lexical: key 14 is a case-insensitive regex over the row's first cell; a synonymously-worded cell (e.g. "quote/heading regression audit") passes without semantic equivalence, and a semantically matching cell phrased differently (no `quote…regression audit` substring) would fail.
- The description check is a 5-shared-distinct-word (len≥4, case-folded) lexical overlap with the anchored description — not semantic entailment. My drafted row copies the anchored row verbatim, so the overlap is trivially the full second cell; the counter would equally pass a row that shares 5 decorative words without carrying the meaning.
- The evidence check is anchor-path presence + resolution at REV, not that the path demonstrates the capability. The semantic step (does the pointed artifact show the behavior) is this seat's re-open: I exercised the gate and read its verdict lines. That reading is bounded by the recorded/replayed stdout; it does not establish source authenticity, full-document completeness, population accuracy, or outside admission — the row's own Limits paragraph (SCORECARD.md:2210-2212) disclaims those.
- The MANIFEST closure attestation (non-author reviewer, spotcheck) is an outside-recorded claim; its spotcheck was not independently re-executed here.

## 7. Findings

- Base state confirmed: statement 14 unmatched in `## Capabilities` (1/4 matched at base, round 27 only); capability evidence exists solely in the append-only Round-14 section and anchored files.
- Anchors resolve at base; recorded evidence demonstrates the capability and replays identically (exercised).
- Drafted summary row (§5) satisfies the v3 predicate elements if integrated by L1 after controls land.
- No blocker, no held item touched; no carrier binary executed; no REA run; no lane/fleet writes; no background processes left running.
