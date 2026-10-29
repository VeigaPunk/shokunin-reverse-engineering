# Captured review receipts

UTC times. Stdout SHA-256 is over the exact payload-command stdout captured to scratch with `tee`; `set -o pipefail` preserved pipeline exit status. Source `git show` stdout was the full blob bytes.

| Exact payload command | Exit | Stdout SHA-256 | UTC | Captured stdout / note |
|---|---:|---|---|---|
| `git ls-tree -r --name-only f890bbead20ca2c549487167f56876ae47f1e1a4 -- corpus/knowledge \| grep -c '\.md$'` | 0 | `690e07064753123c967bbac0180f32da6a753a5bd8b79a47644cef58e776d9f0` | 2026-10-29T20:36:21Z | `139\n` |
| `git show f890bbead20ca2c549487167f56876ae47f1e1a4:tools/round-50/c2-record.py` | 0 | `4749bcd86c8f61bfb6994baeab3bd990b61ea0c369b87197351d0a4618e71285` | 2026-10-29T20:36:21Z | Full counter source blob |
| `git show f890bbead20ca2c549487167f56876ae47f1e1a4:SCORECARD.md` | 0 | `b7e11602738cd167ab4b56463316566539956a9f9631ce2485d09cafd2200790` | 2026-10-29T20:36:21Z | Full scorecard blob |
| `git show f890bbead20ca2c549487167f56876ae47f1e1a4:plans/round-50-attempt2-claims.md` | 0 | `9f091ac06206e5561fc71c95e56f836243efa2750eb10fb301d39a0baf145528` | 2026-10-29T20:36:21Z | Base claims blob; current working-tree plan has the entry-stem correction below |
| `git diff --name-status f890bbead20ca2c549487167f56876ae47f1e1a4 -- SCORECARD.md plans/round-50-attempt2-claims.md corpus/knowledge` | 0 | `e906eae53935123eb4e77b2d2a37839308568bb517ded50866f474b31097dff8` | 2026-10-29T20:36:53Z | `M\tplans/round-50-attempt2-claims.md\n`; no scorecard or knowledge-tree delta |
| `git diff f890bbead20ca2c549487167f56876ae47f1e1a4 -- plans/round-50-attempt2-claims.md` | 0 | `0ac105adca65b6e9aae23aad8fbc531472f18c3b68aabe5e3cd0da55ab9aa029` | 2026-10-29T20:37:35Z | Diff replaces initial `2026-10-29-r50-le-avm-hsqs-core` name with frozen-counter stem `2026-10-28-r50-avm-le-squashfs-core`; retains the `140/140` planned head |
