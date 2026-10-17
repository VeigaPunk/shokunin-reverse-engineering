## CLAIM
Leg-4 records support successful typed `inspect_rust_binary` results, but on two distinct artifacts. Use the lane-B result for SC2’s assigned carrier; do not merge the carrier-specific findings.

## METHOD
Read-only comparison of `receipts/leg-4.md:7-22,27-43`, `receipts-B/leg-4.md:14-18,46-47,66-71`, `SC2.md:8-15`, and `corpus/QUALITY.md:11-18`. No binaries or REA tools were run.

## FINDINGS
- **Observation:** Lane A called REA 6.5.0 on Signal’s `.node`, SHA-256 `1b44ed531f404f5358ee0618a423560463819534a38db5176bb1064b9d14d1f7` (`receipts/leg-4.md:7-22`). Its typed result is `ev_0618e7a50e32ff9556490beeff7e0debc5d6aecf3deedb92b0d4953c747c99d3`; `.dep-v0` metadata is null and the rustc commit is explicitly inferred (`:27-28`).
- **Observation:** Lane B returned typed RESULT `ev_9ea97685bf6313d1e1816a43ba644a25d68459d9ec37f06dfc1b39934eb1bff2` for `/usr/bin/rg`, SHA-256 `d006acfe51619144af4709e85945fe3b5a6f05038d356c4d8f752a33b4ecae42` (`receipts-B/leg-4.md:14-18,46-47,67-70`). This matches SC2’s carrier hash (`SC2.md:8-12`). Output reports no `.dep-v0` section and null rustc commit (`receipts-B/leg-4.md:69-70`).
- **Unknown:** A’s assigned-target identity remains unverified (`receipts/leg-4.md:15,43`); neither null metadata nor absent `.dep-v0` proves the binary has no dependencies (`receipts-B/leg-4.md:69-70`). Preserve path+hash and observation/inference/unknown labels per QUALITY criteria 4–7.

## THREATS
Lane A used a documented Signal fallback because SC2 mapping was unavailable at dispatch; lane B is the later SC2-matching rerun (`receipts/leg-4.md:15,43`; `receipts-B/leg-4.md:5,17-18`). The two results are not same-artifact corroboration.

## VERDICT
FINDING: Both calls returned RESULT, but only lane B verifies the SC2 carrier; keep the two artifact identities and claims separate.
