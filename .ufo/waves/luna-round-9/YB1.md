## CLAIM
Independent pre-landing audit of the r4-16 tail at `HEAD a280e07`: stale-locus localization, EOF append mechanics, and target-errata span precision. No tracked file was modified; this claims no landing and no re-derivation of the corrected numeral.

## METHOD
Read-only: `grep -n` / `awk` / `cat -n` line maps of `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md` and `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md`; `wc -c`, `sha256sum`, `tail -c 64 | sha256sum | base64 -w0`, `od -c`; `git diff --quiet HEAD --` and `git hash-object` vs `git rev-parse HEAD:<path>`; command A recipe (`SCORECARD.md:92-123`) with `REV=a280e07`. Independent of T2; no probes, network, or `/tmp` inventory.

## FINDINGS
- Baseline reproduced independently of T2: 64,080 bytes; SHA-256 `622e3661d3e7f824393554b7cb428a233cc607a890ef77b4dfebeb24cce1d22e`; tail-64 SHA-256 `908ced6ddae54587a408e37870522db18232b11bd1e36145cd9c8ccdd99073ee`; tail-64 base64 `Y2g7IHRoZSBhZGFlbW9uIHNpZGUtZWZmZWN0IGtpbGxlZCwgOjUwMzcgdmVyaWZpZWQKICBjbG9zZWQuCg==`; `od -c` terminal bytes `…verified\n  closed.\n`. Worktree blob == HEAD blob `8116e6fa0040a5c8cc53e56ba198b8ee2e4bed89`; `tracked-diff-exit=0`.
- Command A at `a280e07`: `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "revision": "a280e07", "rule_blocks": 9}` — 79/79 + 9/9 holds pre-landing.
- Stale locus 1 CONFIRMED: `:751-752` ("modulo caller output dir (`files[].path`) + per-run `chunks[].provider_id`"), inside the `:728` r12-01 erratum block; superseded by `r12-01:99-104`, restated `:112-120`, "7 values" attributed (`:117-118`).
- Stale locus 2, uncited by any round-9 receipt (`grep -rn "row-7 class\|CENSUS DEFECT\|105-108\|:730" .ufo/waves/luna-round-9/*.md` → grep-exit=1): `:730-733` labels table lines 195/196/197/199/200 "CENSUS DEFECTS of the row-7 class"; `r12-01:105-108` restricts the label to L195 and reclassifies the rest as queue-bookkeeping lag. A pointer covering only locus 1 leaves `:730-733` stale; P0's "both errata" phrasing covers it only if retained.
- EOF mechanics: last heading `:875` (r14-01); `:877-925` is ONE bullet item — blank-line map of `875-925` yields only `:876`. Appending after `:925` without a preceding blank line and a new heading extends the r14-01 bullet, misattributing the pointer.
- Span precision: P0 cites `:97-114`; the second erratum block runs `:110-120` (file is 120 lines), so `:115-118` (four-site list, attributed numeral) drops out. Prefer `:97-108` + `:110-120` (A2's spans) or `:97-120`.

## THREATS
Line anchors hold only at `a280e07`. "7 values" not re-derived (receipts gone, `r12-01:117-118`); other row-7-label uses (e.g. `:553`) are outside this tail scope, not adjudicated. Landing mechanics are the parent's call; this seat wrote no corpus bytes.

## VERDICT
FINDING: land the pointer under its own new heading after a blank line, cover stale locus `:730-733` (cite `r12-01:105-108`) as well as `:751-752`, and cite `:97-108`+`:110-120` — not `:97-114`.
