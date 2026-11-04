# Checker-mode child environments and the raw-witness capsule audit

## Scope and evidence status

This entry covers the Linux packed-ELF route's checker-mode `git`/`readelf` environment class
and the seven-clause raw-witness capsule reader. The route is `tools/round-72/packed-elf.py`;
the measurement, calibration, reader, library and controls are
`tools/round-72/seam-probe.py`, `mutation-check.py`, `capsule-audit.py`, `capsule_audit.py`
and `controls.py` (declaration `plans/round-72-claims.md`; container
`.ufo/waves/round-72/claims.json`). The frozen claims separate coverage C1, calibration C2
and operability C3. This is a source-grounded decision guide; the landing receipts named
below are the evidence, not this prose.

The measured contract names REA 6.5.0 and a pinned UPX copy; it does not establish behavior
for other packers or other operating systems. Digest comparison accounts for retained bytes,
not cryptographic producer authenticity, and the shim reads `/proc/self/environ` at the exec
boundary, not later environment mutation (S275).

## Decision table v1 — seven tampered capsule shapes

Each shape keeps the genuine summary as its claim. The failure column names the required
clause, not necessarily the only failure: an edit usually invalidates the digest too. The
battery requires genuine acceptance and all seven rejections with their declared clauses
(`tools/round-72/capsule-audit.py --tamper-battery`).

| Tampered capsule shape | Clause and failure name | Re-derived comparison |
| --- | --- | --- |
| Append a newline without changing the records | `log_sha256` | Byte digest versus the claimed digest (`capsule_audit.py` audit) |
| Remove the last record | `records` | Parsed count versus summary count |
| Add `EXTRA_KEY=1` to the first environment | `keys` | Every record must have exactly HOME/LANG/PATH/TMPDIR |
| Add `KAIDOKU_ENV_CANARY=not-a-secret` | `canary` | The canary key absent from every raw environment |
| Move HOME to the run root's sibling `outside-home` | `home_under_run` | Component-aware `commonpath` containment, never a string prefix |
| Move TMPDIR to the run root's sibling `outside-tmp` | `tmpdir_under_run` | Component-aware containment for every TMPDIR |
| Replace the first argv with `/usr/bin/curl` | `children` | Basename child census versus the claimed census |

Malformed JSON and an empty capsule have additional named failures; unreadable input is
unevaluable. The checker prefixes reader failures with `receipt_capsule: ` and exposes
`clauses.receipt_capsule`. A receipt-named capsule is resolved under the lane root and must
stay there (`commonpath`), be a regular file and be at most 64 MiB; an external absolute
pointer is recorded as `skipped_external` and never read (round-72 SentinelScope SS72-2).
A lane-relative named capsule that is absent is a named failure, never a silent pass.

## Probe arms — which witness binds which property

| Probe arm | Witness and bound property | Boundary |
| --- | --- | --- |
| A10 `A10_run_binding` | `binding_verdict()` reads the checker JSON's `clauses.run_nonce` / `clauses.run_binding`, `checker_met()` requires the checker's `met` and `clauses.met` to agree, and the arm requires genuine acceptance plus wrong-nonce/broken-binding rejection from those emitted verdicts. | Not a probe-side re-computation from receipt fields; missing clauses fail closed. The frozen mutant `binding_ok = True` is killed by `a10-binding-from-checker` (`tools/round-72/mutation-check.py --patch-set r72`). |
| A11 `A11_checker_env` | Two independent witnesses: `git` and `readelf` perl shims (a shell adds `PWD`/`SHLVL`/`_`, a perl shim does not) dump `/proc/self/environ`; the probe also parses the checker's own JSONL log. `a11_verdict()` requires exact key sets, no canary, HOME/TMPDIR under the checker's own run root, a log with `git` and `readelf` records, and summary/log agreement. | Measures the instrument under test; a hostile replacement wrapper that forges both witnesses is outside this class (round-72 CriticClaims). |
| A8 `A8_child_env_observed` | The route's raw JSONL is parsed independently of its returned summary: exact keys, no canary, HOME/TMPDIR under the receipt run root, child classes include `upx`, `node`, `readelf`; the summary count/key claims must agree. | Route witness, not checker-mode witness. |

## Limits and interpretation

- Dead scratch paths in receipts are provenance pointers; use the retained capsule bytes and
  summary, not the existence of the original run directory.
- A summary without `log_sha256` makes that clause **not evaluated** (`null`), not true. The
  route records `log_sha256` so a filed receipt's digest is evaluable.
- The canary is a fixed key and string, not a random secret or a comprehensive secret-leak
  detector.
- Containment is lexical absolute-path/`commonpath` containment over the recorded paths; it
  does not resolve the historical symlink targets those paths referred to.
- A11's shims and log are target-owned witnesses: the arm measures the route's behavior, not
  an adversary's willingness to fabricate its own evidence.

## Provenance and recheck

source: S275 — `proc_pid_environ(5)`, Linux man-pages 6.19, https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html (fetched 2026-11-04, HTTP 200, 7 747 bytes, sha256 `93394d9edb801ad44e342e8e8ab057bea619d995803221edaf008226b2062c46`; snapshot `.ufo/waves/round-72/w1/ScoutSource/proc_pid_environ.5.html`)
verified-at: 2026-11-04 — landing receipts `.ufo/waves/round-72/l1/scores/c1-at-landing.json` (11/11; A10/A11 true), `c2-at-landing.json` (mutant killed by `a10-binding-from-checker`), `c3-at-landing.json` (46-record genuine capsule, 7/7 shapes rejected), `c3-genuine-filed.json` (capsule clause true) and `c3-lying-check.json` (capsule clause false)
recheck: re-run the frozen C1 probe, C2 mutation battery and C3 tamper battery/checker pairing exactly as declared in `plans/round-72-claims.md`, with lane-owned receipt outputs and `$HYAKU_SCRATCH` scratch; verify the instrument pins in `.ufo/waves/round-72/claims.json` and its `instrument_supersessions` before citing a receipt.
