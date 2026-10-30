# Frozen-claims checklist

Revision: `ab0eafedc41402b43b41a4362084119578dfe7ce`.

Axes: constant accuracy; collision freedom; immutable evidence reproducibility.

All observations below use committed Git objects, never current worktree contents. Full command stdout, UTC timestamps, exit codes and SHA-256 digests are retained in `receipts.json`. No REA invocation, download, repository mutation or tool install occurred.

## 1. Entry stem has no collision: PASS

- Command: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-tree -r --name-only ab0eafedc41402b43b41a4362084119578dfe7ce -- corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md`
- Observed: Only corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md exists; round-52 entry absent.
- Exit code: 0
- UTC: `2026-10-30T10:46:38.322020+00:00`
- stdout SHA-256: `ec61d94dc10e040da137a132c0b1ec76faec90fd97f75dcb64f4c7394ce7f505`

## 2. Core heading is not yet present: PASS

- Command: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show ab0eafedc41402b43b41a4362084119578dfe7ce:PROVINCE.md`
- Observed: `## Round-52 additions to Core` exact heading count = 0.
- Exit code: 0
- UTC: `2026-10-30T10:46:06.179805+00:00`
- stdout SHA-256: `b0cb62abd63df687451e0f73d2e71684a20e2933b47dfd4f84e92edec79872a8`

## 3. Coverage head agrees with command A: PASS

- Command: `python3 - ab0eafedc41402b43b41a4362084119578dfe7ce < recipe from ab0eafedc41402b43b41a4362084119578dfe7ce:SCORECARD.md:94-122 (cwd /home/vgpnk/Projects/shokunin/kaidoku-shokunin)`
- Observed: mapped = 141; knowledge_files = 141; missing = []; dangling = []; coverage_score = 10.0.
- Exit code: 0
- UTC: `2026-10-30T10:46:38.319943+00:00`
- stdout SHA-256: `8bef6757914a8dd90846d60ad25c7ac0e9face5704a8dedbb446adbaee5f71b3`

## 4. Craft rule-block count agrees: PASS

- Command: `python3 - ab0eafedc41402b43b41a4362084119578dfe7ce < recipe from ab0eafedc41402b43b41a4362084119578dfe7ce:SCORECARD.md:94-122 (cwd /home/vgpnk/Projects/shokunin/kaidoku-shokunin)`
- Observed: rule_blocks = 26; citation_resolved_rules = 26; depth_score = 10.0. Count uses `re.split(r'(?m)^- \*\*', craft)[1:]`, not numbered-heading order.
- Exit code: 0
- UTC: `2026-10-30T10:46:38.319943+00:00`
- stdout SHA-256: `8bef6757914a8dd90846d60ad25c7ac0e9face5704a8dedbb446adbaee5f71b3`

## 5a. Four round-50 envelopes exist: PASS

- Command: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-tree -r --name-only ab0eafedc41402b43b41a4362084119578dfe7ce -- corpus/evidence/round-50/c1/g7581/after.json corpus/evidence/round-50/c1/g7582/after.json corpus/evidence/round-50/c1/c6490/after.json corpus/evidence/round-50/c1/c6430/after.json`
- Observed: after.json present for c6430, c6490, g7581, g7582 (4/4).
- Exit code: 0
- UTC: `2026-10-30T10:46:38.322318+00:00`
- stdout SHA-256: `1a6236e5e090320562d5183001bb2e4774670029bf0e3687449dd75f7555f08d`

## 5b. Independent oracle tables exist: PASS

- Command: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-tree -r --name-only ab0eafedc41402b43b41a4362084119578dfe7ce -- tools/round-50/oracle`
- Observed: 8 TSVs: each carrier has <id>.oracle.tsv and <id>.nonregular.tsv.
- Exit code: 0
- UTC: `2026-10-30T10:46:38.322394+00:00`
- stdout SHA-256: `de3037734442b626b92394efb3e445eb982426d2984de1f690b4e93ba56fea95`

## 6. Census instruments exist: PASS

- Command: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-tree -r --name-only ab0eafedc41402b43b41a4362084119578dfe7ce -- tools/round-51/census3.py tools/round-51/census3.json`
- Observed: tools/round-51/census3.py and tools/round-51/census3.json both present.
- Exit code: 0
- UTC: `2026-10-30T10:46:38.323079+00:00`
- stdout SHA-256: `642c848f2b70eefbf7ca1d8597b6ae12576ef9e90fb8b42d9bf6eb3c85e81a70`

## 7. Source IDs remain available for append: PASS

- Command: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show ab0eafedc41402b43b41a4362084119578dfe7ce:corpus/SOURCES.md`
- Observed: S250 and S251 rows present (lines 163–164); S252 token count = 0.
- Exit code: 0
- UTC: `2026-10-30T10:46:06.182988+00:00`
- stdout SHA-256: `99cbe8e5ece818d93d21ebd1db334b319ef9e80954333e147a43992b5dcf28f8`

## Interpretation and limits

Heading and source-ID checks inspect the complete pinned file outputs in receipts.json; path checks inspect Git tree membership. Git tree membership proves existence, not receipt validity or executable behavior. Command A is the literal pinned SCORECARD recipe, supplied on stdin with its original revision argument; its full stdin is retained in command-a.py.txt. Block 26 occurs before blocks 22–25 in this tree; counting the entire craft section still yields 26, so order is not mistaken for count.

LSP device unavailable (`read xd://lsp`: No such tool). These are Markdown/tree constants, not semantic caller/reference claims. No canonical runtime, resume path, saturation move or changed executable behavior is assessed in this scoped checklist.
