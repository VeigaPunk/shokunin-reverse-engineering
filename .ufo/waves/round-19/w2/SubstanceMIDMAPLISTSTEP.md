# C1 R18-MIDMAP-LISTSTEP — substance review

## Verdict and source identity

**Observation:** The baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` is red for MIDMAP; the final observed `refs/heads/main` (`279e8b19c51658bfd05b9e31a1c0894ab2e70537`) is green. The current validator correction matches the routed defect: when `--require-mid-maps` is active, list entries count only when identified as the analyze step; ambiguous/multiple analyze entries do not satisfy the requirement. I found no actual MIDMAP false-close or false-open at the final main tip. The retained integrated result is stale (details below).

**Immutable-blob observations:** `corpus/lessons/round-18-verifier-spotcheck.md:193` specifies the original defect: any list step's `pin_checks` satisfied the flag. At main, `receipt-validate.py` identifies analyze from an unconflicted `step`/`name` declaration or the command position in `argv` (`.ufo/waves/round-17/tools/receipt-validate.py:134-161`), and the list branch requires exactly one identified analyze step with checks (`:607-630`). The CLI-to-validator forwarding is present (`:634-645`, `:662-685`, `:1160-1162`). The routed correction is named at `SCORECARD.md:2483` and `corpus/lessons/round-19.md:56`. B→main diff contains additions only for these correction records (SCORECARD +32/−0; round-19 lesson +134/−0), so the actual records are append-only in this range.

## Findings by severity

### Medium — `s_midmap` can false-close if caller forwarding regresses

`routed-r18.py:s_midmap` imports REV's validator and calls `verify_mid_maps(..., require_mid_maps=True)` directly (`.ufo/waves/round-19/tools/routed-r18.py:92-117`). It does not exercise the public caller path that forwards the CLI flag. On final main that path is correct, but I changed only the `validate_receipt` call in an isolated clone to omit `require_mid_maps=require_mid_maps` (mutation commit `be4de04afd8d129608dbbd2c87d57d35d8c0c1ac`, based on main `279e8b1`). Running the unmodified routed counter on that mutant returned `open_count=0`, `substance_open=0`, exit 0. Thus a future wiring regression can disable the required check while C1 still closes. This is a demonstrated mutant-only false close, not a defect observed in main. The tool's test needs to exercise the forwarding path as well as the helper.

### Medium — current counter misses the latest analyze-identity hardening

The two `s_midmap` fixtures test only the simple non-analyze-with-checks / analyze-with-checks pair and only inspect `mid_checks_absent` (`routed-r18.py:99-117`). They do not cover command-position spoofing, conflicting `step`/`name`, or duplicate analyze identities. Those are now part of the validator behavior and are covered in its own selftest at `receipt-validate.py:1105-1119`, but the routed C1 substance check does not invoke those cases.

I tested a latest-main clone with `_is_analyze_step` mutated back to the earlier “any argv token exactly `analyze`” classifier. A non-analyze `inspect-go-binary` argv with a trailing `analyze` token was then classified as analyze, yet the routed counter still reported MIDMAP named/substance true and all 7 defects closed (mutation commit `c2e6baaaa3c854d2106d7bfa5bed3aad842342b9`, exit 0). Current main itself rejects that spoof and conflicting labels; the gap is in the counter's coverage, not current validator behavior.

### Low — green fixture's success reason overstates what was checked

The fixture `pc` at `routed-r18.py:99-100` lacks `map_path` and `map_sha256`. Directly invoking the current validator on the green fixture produced `mid_map_missing` while correctly omitting `mid_checks_absent`. `s_midmap` intentionally checks only the latter code, but returns the reason “analyze-carrying list receipt clean” (`:112-117`). The tested property is “no missing-analyze-check finding,” not a clean receipt; the current success diagnostic is therefore inaccurate.

## Commands and observed results

Baseline/main/selftest counter runs below used the immutable main-blob copy extracted with `git show refs/heads/main:.ufo/waves/round-19/tools/routed-r18.py` (exit 0; SHA-256 `54020829303e1b16592c947978d4925c72405c776a6aa221d57b2fd04aa18003`); mutation runs use that revision's counter blob in the isolated clones. The observed main ref was rechecked as `279e8b19c51658bfd05b9e31a1c0894ab2e70537`.

```text
python3 -I -B /tmp/routed-r18-latest-main.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --strict
exit 1; open_count=7, named_open=7, substance_open=7; MIDMAP named=false, substance=false; “list-shaped receipt with pin_checks only on a non-analyze step is accepted”

python3 -I -B /tmp/routed-r18-latest-main.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev refs/heads/main --strict
exit 0; resolved rev=279e8b19c51658bfd05b9e31a1c0894ab2e70537; open_count=0, named_open=0, substance_open=0; MIDMAP named=true, substance=true

python3 -I -B /tmp/routed-r18-latest-main.py --selftest
exit 0; SELFTEST: CLEAN cases=13
```

The counter selftest is not the MIDMAP evidence: its fixture repository does not carry REV's round-17 validator. Independent direct calls using the immutable B and main validator blobs showed B emits no `mid_checks_absent` for either fixture, while main emits it for red only. On current main the green call still reports `mid_map_missing`, confirming the diagnostic limitation above. Direct latest-main probes also returned false for all four identity-spoof cases and raised `mid_checks_absent` for duplicate analyze steps.

Targeted mutation counter commands (each clone was created under `/tmp` from observed main `279e8b1`; no production tree was edited):

```text
python3 -I -B /tmp/kr19-w2-midmap-latest-regression.0XKsJC/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-midmap-latest-regression.0XKsJC --rev 81896cb2bc7293bbe025117babd828f2302efc9d --strict
exit 1; open_count=1; MIDMAP substance=false (“non-analyze step is accepted”)

python3 -I -B /tmp/kr19-w2-midmap-latest-wiring.3mZoPR/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-midmap-latest-wiring.3mZoPR --rev be4de04afd8d129608dbbd2c87d57d35d8c0c1ac --strict
exit 0; open_count=0 despite required-flag forwarding removed

python3 -I -B /tmp/kr19-w2-midmap-latest-identity.xrLziM/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-midmap-latest-identity.xrLziM --rev c2e6baaaa3c854d2106d7bfa5bed3aad842342b9 --strict
exit 0; open_count=0 despite spoofed analyze-token acceptance
```

## Verification gaps and residual risk

- `.ufo/waves/round-19/evidence/routed-r18-integrated.json:46-49` in current main is bound to older `4f6c73f81ae8d31de18377d7ff57e4e10140ce48` and reports `open_count=1` (INSTALL-RECORD). It is not a false result for that recorded revision, but there is no retained integrated JSON bound to current main `279e8b1`; the fresh current-tip run above is not persisted. `SCORECARD.md:2493` still says the final measured verdict is appended after verification.
- `named()` checks only for a line prefix in both files (`routed-r18.py:304-309`); it does not itself establish historical append-only behavior. The B→main content diff does establish that these specific correction records were added without deletions.
- No `lsp` device/server was mounted (`xd://lsp` returned “No such tool”); caller/definition review used the immutable source blobs and explicit call chain. No builds, broad suite, installs, or production edits were made.
