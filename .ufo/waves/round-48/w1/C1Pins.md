# C1Pins — Round 48 C1 freeze and digest evidence

## Frozen C1 counter at declared freeze

Command (from lane root):

```sh
HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r48/C1Pins python3 -I -B tools/round-48/meanings.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --json-out .ufo/waves/round-48/w1/C1Pins/receipt.json
```

Exit 1; stdout SHA-256 `594e618c67908dfb390e2ad654b616a321e923af4bdbaff92a13dbc940eb330a`; UTC `2026-10-28T18:47:07Z`. Exact receipt is `receipt.json`. It reports `block_present: 0`, 24 craft blocks, marker occurrences 0, `frozen_path_changed: []`, and failing clauses `marker_occurrences 0 != 1`, `marker_block_count 0 != 1`; battery skipped because structural clause failed. This measures the frozen pre-landing state, not a landing result.

## Mutation digest check

The committed implementation `_mut_digest()` hashes each listed function name, its source from `inspect.getsource(fn)`, and delimiters in mutation-list order. An isolated scratch calculation over the four implementation function source bodies returned:

- body-bearing digest: `80010be3ccb4b52ede303be8a21ed62766e2f052b58422e59c180d8b061d8e3b`
- names-only digest: `dbf00169c1f0427a5871fc9cbd98eec88d7e174e5f0ad62343d392138ea758a5`
- one-body-edited digest: `f2d80306cd8e6eccd1d0fed0940637339035432a5d8240eb5ea19c86ef591870`

Thus the names-only value differs from the body-bearing value, and a scratch edit to `_m_gold_meaning` changes the calculated digest. The mutated copy is at `/fast/scratch/hyaku/kaidoku-r48/C1Pins/meanings-body-mutated.py` (scratch removed after evidence capture as required). This was an isolated digest experiment; it did not construct/run a SKILL block forged with the names-only digest, so no red result for such a block is claimed.

## Scope and verification

No lane implementation files were changed. Only this report and `receipt.json` were written in this seat's report directory. No tests/build/lint/formatters run. Disk guard status command was attempted; it timed out after 30s while printing disk usage. No tools installed.
