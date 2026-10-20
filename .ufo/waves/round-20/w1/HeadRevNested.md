# HeadRevNested — D6a

## Result

**Observation:** Implemented bounded intra-file helper-chain resolution and a separate `nested` result class in `.ufo/waves/round-18/tools/head-rev-lint.py:54-69,566-575,758-885,957-1053`. Nested records include the helper target/chain and are not merged into `sites`, `live_count`, or strict evaluation; seat exclusions retain their own `nested` list. An immediately preceding comment annotates nested calls, covering the compare-only marker at `.ufo/waves/round-17/verify.py:82-83`. The selftest adds `nested_compare_only_records` and `nested_compare_only_separate` at `.ufo/waves/round-18/tools/head-rev-lint.py:1259-1276`.

**Observed baseline run:** `live_count=0`, `nested_count=2`, `nested_live_count=1`. Exact new records:

```json
[
  {
    "class": "nested",
    "code": "head = _git_or_none(\"rev-parse\", \"--verify\", \"HEAD^{commit}\")",
    "context": "annotated",
    "kind": "rev-parse-HEAD",
    "line": 83,
    "path": ".ufo/waves/round-17/verify.py",
    "reason": "head-rev-lint: compare-only",
    "target": "_git_or_none",
    "via": ["_git_or_none", "git"]
  },
  {
    "class": "nested",
    "code": "head = _resolve(lane, \"HEAD^{commit}\")",
    "context": "live",
    "kind": "rev-parse-HEAD",
    "line": 113,
    "path": ".ufo/waves/round-18/tools/revpin.py",
    "target": "_resolve",
    "via": ["_resolve", "_git"]
  }
]
```

**Inference:** `.ufo/waves/round-18/tools/revpin.py:113` is the comparison read: its result is compared with `source` at `.ufo/waves/round-18/tools/revpin.py:119` and gates the `head_not_branch_tip` refusal at `.ufo/waves/round-18/tools/revpin.py:123-124`. It has no adjacent compare-only annotation, so its record retains `context: live`; it remains separate from primary `live_count` as intended. The scanner explicitly does not prove compare-only use (`.ufo/waves/round-18/tools/head-rev-lint.py:148-152`).

## Verification and retained patch

- Clone base observed: `14f0260ad319ecc26994381b2415d5a999003375`.
- Selftest (run once): `SELFTEST: CLEAN cases=5` — exit 0.
- Baseline lint — exit 0; output above is from `--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 14f0260ad319ecc26994381b2415d5a999003375`.
- `git -C /tmp/kr20-HeadRevNested-2 diff --cached --stat 14f0260`:
  ```
   .ufo/waves/round-18/tools/head-rev-lint.py | 452 ++++++++++++++++++++++++++++
   1 file changed, 437 insertions(+), 15 deletions(-)
  ```
- Patch: `.ufo/waves/round-20/w1/patches/HeadRevNested-2.patch`.
- Risk: resolution is intra-file/name-based and bounded to 6 helper links and 8 templates; dynamic argument construction may be missed (`.ufo/waves/round-18/tools/head-rev-lint.py:148-152`). No tools installed. LSP was unavailable in this session: the executable probe below found no server paths.

## Commands and exits

```text
for c in pylsp pyright-langserver basedpyright-langserver jedi-language-server; do command -v "$c" || true; done — 0 (no output)
if test -e /tmp/kr20-HeadRevNested-2; then printf 'clone_exists=yes\n'; else printf 'clone_exists=no\n'; fi; git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse --verify 14f0260ad319ecc26994381b2415d5a999003375^{commit} — 0 (clone_exists=no; baseline hash printed)
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-HeadRevNested-2 — 0
git -C /tmp/kr20-HeadRevNested-2 checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375 — 0
git -C /tmp/kr20-HeadRevNested-2 rev-parse HEAD — 0
python3 -I -B /tmp/kr20-HeadRevNested-2/.ufo/waves/round-18/tools/head-rev-lint.py --selftest — 0; last line: SELFTEST: CLEAN cases=5
python3 -I -B /tmp/kr20-HeadRevNested-2/.ufo/waves/round-18/tools/head-rev-lint.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 14f0260ad319ecc26994381b2415d5a999003375 — 0
git -C /tmp/kr20-HeadRevNested-2 add -A — 0
mkdir -p /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches — 0
git -C /tmp/kr20-HeadRevNested-2 diff --cached --stat 14f0260 — 0
git -C /tmp/kr20-HeadRevNested-2 diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 — 0
```
