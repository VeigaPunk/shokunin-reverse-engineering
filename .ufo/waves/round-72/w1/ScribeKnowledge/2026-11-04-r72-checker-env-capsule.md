# Checker-mode child environments and the raw-witness capsule audit

## Scope and evidence status

This entry covers the Linux packed-ELF route's checker-mode `git`/`readelf` environment class and the seven-clause raw-witness capsule reader. The route instrument is `tools/round-72/packed-elf.py`; the measurement, calibration, reader, library and controls are respectively `tools/round-72/seam-probe.py`, `mutation-check.py`, `capsule-audit.py`, `capsule_audit.py`, and `controls.py` (declaration inventory: `plans/round-72-claims.md:163-171`). The frozen claims separate coverage C1, calibration C2 and operability C3 (`plans/round-72-claims.md:23-55,61-91,97-128`). This is a source-grounded decision guide, not a fresh execution or a declaration that landing passed.

The measured contract names REA 6.5.0 and a pinned UPX copy; it does not establish behavior for other packers or other operating systems (`plans/round-72-claims.md:38-48`; Linux shim implementation: `tools/round-72/seam-probe.py:230-265`). Digest comparison accounts for retained bytes, not cryptographic producer authenticity (`.ufo/waves/round-71/l1/scores/c1-env-audit.json:12-16`).

## Decision table v1 — seven tampered capsule shapes

Each shape retains the genuine summary as its claim. The failure column names the required clause, not necessarily the only failure: edits may also invalidate the digest, key set or census. The battery requires genuine acceptance and all seven rejections with their declared clauses (`tools/round-72/capsule-audit.py:74-106`).

| Tampered capsule shape | Clause and failure name | Re-derived comparison / source |
| --- | --- | --- |
| Append a newline without changing the records | `log_sha256` | Actual byte digest versus claimed digest; `tools/round-72/capsule_audit.py:124-134,170`. |
| Remove the last record | `records` | Parsed count versus summary count; `tools/round-72/capsule_audit.py:134,172`. |
| Add `EXTRA_KEY=1` to the first environment | `keys` | Every record must have exactly HOME/LANG/PATH/TMPDIR; `tools/round-72/capsule_audit.py:31,74-76,135,173-175`. |
| Add `KAIDOKU_ENV_CANARY=not-a-secret` | `canary` | Canary key absent from all raw environments; `tools/round-72/capsule_audit.py:32,77,136-137,176-178`. |
| Move HOME to the run root's sibling `outside-home` | `home_under_run` | Component-aware containment, not a textual prefix; `tools/round-72/capsule_audit.py:35-41,78-79,138,179-182`. |
| Move TMPDIR to the run root's sibling `outside-tmp` | `tmpdir_under_run` | Component-aware containment for every TMPDIR; `tools/round-72/capsule_audit.py:35-41,80-81,139,183-186`. |
| Replace the first argv with `/usr/bin/curl` | `children` | Basename child census versus claimed census; `tools/round-72/capsule_audit.py:63-69,140,187-189`. |

Malformed JSON and an empty capsule have additional named failures outside these seven shapes; unreadable input is unevaluable (`tools/round-72/capsule_audit.py:44-60,116-123,142-153`). Checker integration prefixes reader failures with `receipt_capsule: ` and exposes `clauses.receipt_capsule` (`tools/round-72/packed-elf.py:832-852`). The retained base receipt records round-71 acceptance of a lying summary while the audit rejected its polluted capsule with `records`, `keys`, `canary`, and `children`; that is retained historical evidence, not a run performed for this draft (`.ufo/waves/round-72/l1/pre/c3-at-base.json:2-24`).

## Probe arms — which witness binds which property

| Probe arm | Witness and bound property | Boundary / citation |
| --- | --- | --- |
| A10 `A10_run_binding` | `binding_verdict()` reads checker JSON `clauses.run_nonce` and `clauses.run_binding`; missing clauses fail closed. Genuine, wrong-nonce and broken-binding checks bind acceptance/rejection to those emitted verdicts. | Not a probe-side recomputation from receipt fields; `tools/round-72/seam-probe.py:171-186,602-655`. Calibration mutant and required kill case: `plans/round-72-claims.md:75-91`. |
| A11 `A11_checker_env` | PATH-first `git`/`readelf` shims dump `/proc/self/environ`; shim dictionaries require exactly four allowlisted keys, no canary, and HOME/TMPDIR under work. Checker JSON `checker_child_env` must report at least two clean records including both child classes and a run root under work. | Two witness surfaces, but this arm does not itself parse `checker.jsonl`: it consumes the checker summary. Shim containment is under work, while the checker summary claims containment under run; `tools/round-72/seam-probe.py:230-297`. |
| A8 `A8_child_env_observed` | The route's raw JSONL is parsed independently of its returned summary: exact keys, no canary, HOME/TMPDIR under receipt run root; summary count/key claims must agree, and child classes include `upx`, `node`, `readelf`. | Route witness, not checker-mode witness; `tools/round-72/seam-probe.py:462-511`. |

## Limits and interpretation

- Dead scratch paths in receipts are provenance pointers, not surviving evidence. Use the retained capsule bytes and their retained summary, not existence of the original run directory (`.ufo/waves/round-71/l1/scores/c1-env-audit.json:11-17`; `.ufo/waves/round-72/l1/pre/c3-at-base.json:14,22`).
- The shim measures the exec-boundary environment via `/proc/self/environ`, not later environment mutation, all descendants, or all future subprocess behavior. It writes one named file per shim and then execs the real tool (`tools/round-72/seam-probe.py:230-255`; S275, source-seat assignment; source snapshot receipt pending at `.ufo/waves/round-72/w1/ScoutSource/proc_pid_environ.5.html`).
- A summary without `log_sha256` makes that clause **not evaluated** (`null`), not true. Other clauses still determine acceptance (`tools/round-72/capsule_audit.py:129-150`).
- The canary is a fixed key/string, not a random secret or comprehensive secret-leak detector: A11 uses key `KAIDOKU_ENV_CANARY` with value `probe-canary-r72`; the tamper shape uses `not-a-secret` (`tools/round-72/seam-probe.py:244,264-265`; `tools/round-72/capsule_audit.py:176-178`).
- Containment here is lexical absolute-path/commonpath containment; the helper does not resolve symlinks (`tools/round-72/capsule_audit.py:35-41`).

## Provenance and recheck

source: S275 (ScoutSource confirmed this id rather than the assignment's provisional S276); proc_pid_environ(5), https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html. ScoutSource reports snapshot sha256 `93394d9edb801ad44e342e8e8ab057bea619d995803221edaf008226b2062c46`, intended receipt `.ufo/waves/round-72/w1/ScoutSource/proc_pid_environ.5.html`; receipt was not yet present during this seat's inspection. Implementation anchors: `tools/round-72/seam-probe.py:230-255`, `tools/round-72/capsule_audit.py:116-153`.
verified-at: 2026-11-04 — source/receipt inspection only; no new instrument execution. Retained base evidence: `.ufo/waves/round-72/l1/pre/c3-at-base.json`; retained 46-record summary: `.ufo/waves/round-71/l1/scores/c1-env-audit.json`.
recheck: Run the frozen C1 probe, C2 mutation battery, and C3 tamper battery/checker pairing exactly as declared in `plans/round-72-claims.md:38-55,75-91,111-128`, with explicit lane-owned receipt outputs and approved scratch; retain raw bytes before deleting scratch. Check measured instrument pins and source-row confirmation before treating this draft as a landing verdict.
