# Round 69 — the packed route's gate can fail, its contract is typed, and a shared object joins the carriers

Lane `kaidoku`, round 69, attempt 1. Base `d7d9a62cc70935304e600ed0dee864fc4f1751f7`; operative freeze
`f15998102f1ce3569e61faa2ac6f286bc414538e` (the commit that first adds
`.ufo/waves/round-69/claims.json`). Three claims on three axes, all capability acquisitions:
R69-C1 calibration (the five mutation survivors killed by the instrument's own selftest), R69-C2
operability (typed exit-2 contract and an enforced packer pin), R69-C3 coverage (a packed shared
object as a carrier class). Declaration `plans/round-69-claims.md`; container
`.ufo/waves/round-69/claims.json`.

## Gate

Every row below was opened this round by the L1 or by a seat whose fetch is committed under
`.ufo/waves/round-69/w1/ScoutSource/`; the quote is located in the fetched bytes and counts words
with `printf '%s' '<quote>' | wc -w`.

| candidate | fetch | located quote / reason | decision |
|---|---|---|---|
| `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/help.cpp` + `…/src/main.cpp` (UPX 5.2.0 packer source at tag `v5.2.0`) | HTTP 200: `src/help.cpp` 27 279 B, sha256 `0b893ca8299c061a8e1961ddbc1fa85cd8d77f3f043cba9a478a697e5d363c79`; `src/main.cpp` 41 889 B, sha256 `a02c7cba2939708e2af4c25119fe20a5a7594b7225b189848196280b03dea82c`; fetched 2026-11-03 | `help.cpp:465`: `fprintf(f, "upx %s\n", UPX_VERSION_GIT_DESCRIBE);` (4 words); `main.cpp:1174`: `if (strcmp(argv[i], "--version") == 0)` (5 words) | **ADMIT** — S270, tier A (source at the pinned tag), kind `code`, scope = the packer's identity banner and its `--version` flag; grounds R69-C2's A3/A4/A6 arms |
| `https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx.1` (the same tag's generated manual page) | HTTP 200, 40 077 B, sha256 `09552b3cf4e9073c288060b8f50ed1c1dde3dca89dcaf1230367b6c3e15d4e25`, fetched 2026-11-03 | line 164 renders `--version: print the version of UPX` (6 words) | **not a row** — the same flag at the same tag; a row would duplicate S270's scope and add no claim, so it is recorded as a secondary locator inside S270's anchor cell |
| `https://upx.github.io/` (project front page) | HTTP 200, 5 059 B, sha256 `f07678bd16df1e713cac0c04bd2eb0b3d2accfb98c589f6f63911d6f32ad1fa7`, fetched 2026-11-03 | `grep -o '5\.2\.0'` = 0 occurrences and no `--version`/banner text: the page names list/test/unpack but carries no revision identity | **REJECT** — an unversioned page cannot ground an identity claim; flip: a versioned page or a section stating the banner/`--version` contract |
| `https://manpages.debian.org/unstable/upx-ucl/upx.1.en.html` | HTTP 200, 61 251 B, sha256 `40e69ca34c2ceac37273eaf1c8dff82a00b9e46bade9e9dcdd0ed273427afbb8`, fetched 2026-11-03 | the page's own version chips read `4.2.4-1.1` / `4.2.4-2` against the pinned `5.2.0` | **REJECT** — right document, wrong revision; it would attribute 4.2-era text to the 5.2.0 binary the pin enforces; flip: a mirror rendering 5.2.0 |
| `https://github.com/upx/upx/releases/tag/v5.2.0` (release page) | HTTP 200, 162 744 B, sha256 `53033ceb745eb2ab…`, fetched 2026-11-03 | title `Release UPX 5.2.0 · upx/upx · GitHub`; `grep -o 'version of UPX\|--version'` = 0: it announces the release but states no identity probe | **REJECT as sole support** — tier C lead at most; the version is the page's subject, not a documented contract |

**S269 label correction (R68-V5).** The round-68 spot-check found S269's anchor label "(11 words)"
wrong: `printf '%s' 'Packed programs will be byte-identical to the original after uncompression' |
wc -w` = **10**. S269 is not superseded: the quote is 10 words and ≤25 either way, its location,
bytes and sha256 re-derive, and a superseding row would duplicate the same URL and scope while
carrying no new claim — the label is a miscount, not a claim drift (QUALITY #93 exists to stop claim
drift). The correction is recorded here and in the round report; a new row's word count is now
computed before the row is written.

**Spot-check result.** `[L1 — filled by the non-author closure.]`

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M69-1 | landing | the round-29 gate run against `.ufo/waves/round-69/claims.json` at the freeze reports `FLAGGED` / `INSTRUMENT_NONE`: the container lists instruments as a JSON array and keeps the predicate sentences under `frozen_atoms`, so the gate reads no claim string that names an instrument | **QUALITY #68** (a claim file's pins live in the top-level `instruments` object the lane's freeze gate accepts, with the predicate byte-identical in the claim; a map in the wrong shape is a defect) — the rule already held and this round's container did not follow it | run `tools/round-29/freeze-gate.py --rev <freeze>` against the container BEFORE committing it, and encode `instruments` as a `{path: sha256}` object with each predicate in a `claims` entry; the frozen container is disclosed, not repaired post-freeze |
| M69-2 | reference-drift | `corpus/knowledge/2026-11-03-r68-packed-elf-route.md:3` carried `**Source:**` prose and no line-start `verified-at:`/`recheck:` (R68-V1); `grep -nE '^(source|verified-at|recheck):'` was empty | **CORPUS** "a new knowledge entry opens with its provenance trio" had no write-time check | the round-69 entry opens with the trio; a `## Correction` block is appended to the round-68 entry (never an in-place rewrite); QUALITY #112 makes the trio checkable in the same command as the entry |
| M69-3 | number-drift | S269's anchor says the quote is 11 words; `wc -w` = 10 (R68-V5) | **QUALITY #21** (a count carries its command) — the count was written, the command was not run at write time | recorded reason above (no superseding row) + the count is computed before a row is written |
| M69-4 | stale-premise | `tools/round-29/prefile-check.sh:31-35` says the legacy ledger "stops at round-52" (last row is round-35) and the gate "reported 20 exact of 36 on every round from 53 on"; the failure branch's `${got:-absent}` is unreachable because `sha256sum` of empty stdin yields `e3b0c442…` (R68-V4) | **QUALITY #21** — a retention statement without the command that prints it | the script's prose and branch are corrected, and a LOG correction is appended; the filed LOG line is not rewritten |
| M69-5 | landing | `corpus/README.md:118` placed the round-68 knowledge-index row above the table header/delimiter (R68-V2), so GFM reads it as prose | **none** — no check parses the index as a table | the row is moved below the delimiter and the round-69 row added; the check is the table shape (`sed -n` header/delimiter/row order) |
| M69-6 | scope | the frozen route's `before_ok` bound was written as a floor (`packed < orig/2`) for two executables; on a shared object the packed stub keeps an export table (98 procedures), so the same rule would score a real stub as false | **QUALITY #107** (a rule generalised from one carrier family names the family and the class it cannot see) was the rule that caught it at design time | the ceiling is declared per carrier class and the counter rejects any ceiling ratio above 0.75; `libz`'s 120/184 = 0.6522 is the declared bound |
| M69-7 | landing | the r68 closure record (`LOG.md` carry-in) was committed after the claims freeze `f1599810` instead of before it; `git merge-base --is-ancestor <carry-in> <freeze>` is red for this round | **QUALITY #34** (the outside closure decision is recorded in LOG and SCORECARD before the next round's claims are measured) | disclosed in the carry-in entry and the report; the next round commits the carry-in before the declaration, and the SCORECARD records the closure decision in the same commit |
| M69-8 | vacuous | `w1/CriticClaims.md` §R69-C2/R69-C3: a fabricated receipt passes the C2 probe 6/6 (even with one carrier or `/bin/ls` as the source) and the C3 checker `met true` (invented counts, a relabelled executable as `shared-object`, a ratio that does not equal ceiling/orig, two rows while `carriers_matched` says 3); the round's own control `c3-synthetic-met` passed the checker with no run at all (`l1/pre/controls-at-base.json`) | **none as applied** — the control set framed the synthetic pass as a capability arm ("the checker can pass"), not as a shortcut that reaches the target; the fleet rule "a target a do-nothing control can reach is not an improvement" is the criterion that should have caught it | the corroboration gate `tools/round-69/provenance-check.py` binds the receipt to the instrument pin and the measured revision and re-derives carriers/ratios (five forged shapes rejected at the landing); the frozen counters stay as frozen, and the next freeze binds receipt provenance directly (routed) |
| M69-9 | scope | `w1/SentinelScope.md` S-1: `tools/round-69/packed-elf.py:253-259` executes the caller-supplied `--upx` (for `--version`) **before** hashing it and comparing the sha256 pin, with the full environment inherited and no sandbox | **none** — no criterion said identity comes before execution; QUALITY #113 is added this round for it | routed: compute and compare `sha256_file(upx)` before the `--version` invocation, and pass a minimal environment to the packer calls; no lane run passes `--upx`, so the exposure was confined to the probe's own fixtures |
| M69-10 | scope | `w1/ExecC2/rederive.md` U1/U2/U11: an exec-format-less `--upx`, an unreadable (0111) packer and a `node` symlink with a missing interpreter each escape as a traceback with exit 1 rather than a typed exit 2; the six named arms do not cover them | **QUALITY #87** (a claim clause the instrument never reads) read as a contract-shape rule, plus the plan's own wording ("missing" tools) — the leaks are outside the declared six arms | routed: preflight probes each tool with a short invocation and types the failure; the lesson and the entry claim the six arms only, never a universal contract |
| M69-11 | landing | `w1/SentinelScope.md` S-2/S-3/S-4: `--upx` is validated but the carrier loop still calls the module-global `/usr/bin/upx`; `contract-probe.py:85` carries a `/tmp` HOME fallback; `mutation-check.py`/`contract-probe.py` delete a fixed-name subdirectory of `--work`, so concurrent runs clobber each other | **none** — no check covers validated-vs-used paths, /tmp literals or concurrent scratch reuse | routed to the next freeze; no committed tool writes `/tmp` in this round's runs and no two runs shared a `--work` here |


## Outcome

- **R69-C1 — verified.** `python3 -I -B tools/round-69/mutation-check.py --root . --rev
  5ee94c56ce7490938ee38c2e5c10930a1fd1330a --tool tools/round-69/packed-elf.py --patch-set r69
  --work <scratch>` exits 0 with `survivors []`, the five `killed` mutants each naming its declared
  arm-false case, `killed_wrong_case []`, `pristine.cases 20`, `pristine.ok true`,
  `target_sha256 4ac0d83b…` (`.ufo/waves/round-69/l1/scores/c1-at-landing.json`). The same battery
  with patch set r68 against `tools/round-68/packed-elf.py` at the base exits 0 with exactly the five
  survivors and `pristine.cases 13` (`.ufo/waves/round-69/l1/scores/c1-before-recheck.json`).
  Independent re-derivation: `w1/ExecC1/rederive.md` (both a constant-`True` and the literal patch
  family; every kill names exactly its case; the r68 mutant shas equal the round-68 wave's).
- **R69-C2 — verified, with a routed counter-strength defect.** The contract probe at the landing
  reports `arms_passed 6` of `target 6`, `failed []`, against the landing receipt
  (`.ufo/waves/round-69/l1/scores/c2-at-landing.json`); the base arm reports 0 of 6 naming all six
  (`.ufo/waves/round-69/l1/pre/c2-at-base.json`). The probe does not bind the receipt to its producer
  (M69-8): a fabricated receipt passes it, so the six-arm result is evidence only together with the
  provenance gate below and the independent re-derivation (`w1/ExecC2/rederive.md`).
- **R69-C3 — verified, with a routed counter gap.** `packed-elf.py --check-receipt` on the
  three-carrier receipt reports `met true`, `failing []` (`.ufo/waves/round-69/l1/scores/
  c3-check-at-landing.json`); the receipt reports `target 3`, `carriers_matched 3`, `control_ok true`,
  ratios 0.0599 / 0.1010 / 0.6522, `before_procedures [3, 3, 98]` (`.ufo/waves/round-69/l1/scores/
  c3-at-landing.json`). The checker alone accepts a fabricated receipt (M69-8); the provenance gate
  binds the receipt to the frozen instrument (`instrument.sha256 4ac0d83b…`, `rev 5ee94c56…`) and
  re-derives the three carriers (`provenance-at-landing.json`, `met true`), and `w1/ExecC3/verify.md`
  reproduced every count, format, pin and packed sha256 independently.
- **Controls.** The seven do-nothing/shortcut controls re-run at the base: all seven arms show what
  they must (`controls-at-base-recheck.json`); the C3 synthetic receipt does reach the checker (the
  routed gap), which is why the provenance gate exists.
- **No-harm.** No owned axis score is lowered: coverage gains a carrier class, depth gains the
  contract table and the arm seam, calibration gains a gate that can fail. Two counter defects
  (M69-8) and one new security seam defect (M69-9, `--upx` executed before hashing; no lane run
  passes `--upx`) are reported, routed to the next freeze, and the container/instruments were not
  edited post-freeze.

## Census

- Start: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` exit 0,
  176 rows, 19 standing W04, malformed 0 (`.ufo/waves/round-69/l1/census-start.txt`).
- End: exit 0, **177 rows** after S270, malformed 0, mined 168 / rejected 9, tiers A 163 / B 9 / C 5,
  the same 19 W04 (`.ufo/waves/round-69/l1/census-end.txt`).

## Final decision — supersedes the intermediate Outcome

C1 verified; C2/C3 **not verified under the frozen shortcut-control rule**.
The critic's fabricated receipts meet both frozen targets; post-freeze corroboration
cannot repair those counters. Round admission: **honest stop, not admitted**.
Quality: **harmed** by the introduced execute-before-hash seam; no safety property
is inferred from the packer pin. The instruments remain frozen for reproducibility.

R68-V5 final disposition supersedes the reason-only paragraph above: **S271**
is admitted as the append-only correction required by QUALITY #93. Source opened
2026-11-03: https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx-doc.txt,
HTTP 200, 37208 bytes, sha256 4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42.
Located quote at lines 441-442 under NOTES FOR LINUX/ELF386 (heading 433):
"Packed programs will be byte-identical to the original after uncompression"
(10 words, `printf '%s' '<quote>' | wc -w`). Final registry: 178 rows.
No existing status/recheck/used-by cell was changed; S270 and S271 are new mined rows.
The admit/reject decisions remain author assessments pending outside closure.

## Erratum — round 70: the spot-check placeholder is filled by the closure record

The `## Gate` line above — `[L1 — filled by the non-author closure.]` — is filled by the
round-69 non-author closure itself, which wrote its own record file rather than editing this
lane-authored lesson: `corpus/lessons/round-69-verifier-spotcheck.md` (author
`hyaku closure (non-author integrator, @m_zfl)`, lane tip `605ce424b41f0ae6f3ddbf9dd629173990419396`,
fleet report commit `9fa113c9`). It re-opened S270/S271 and both sampled rejects byte-exact
(all four agree), re-measured C1 from committed receipts (improved), graded C2/C3 unprovable
under the frozen shortcut-control rule, and routed M69-1/8/9/10/11 to this round. Verdict:
**rejected-honest-stop**, round not admitted. This erratum is appended, never a rewrite of
the filed bytes.
