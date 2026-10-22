# XpinOnR27Envelopes: check of the round-27 C1 attribution receipt

Seat KaidokuR27.XpinOnR27Envelopes, wave 2, leaf (no delegation). Read-only on the lane. This file is the only lane write.

- Item: re-run and check `corpus/evidence/round-27/c2/r27-c1-attribution.tsv` (42 `6.5.0`, 6 `both`).
- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. HEAD and `main` are `4084d8975b684a8837b1c858eea0008ce9ab49e0`. No tracked file changed. Frozen claims at `a4f674b343d8564e21f7eb8984630a95089c82d6`.
- Window (UTC): 2026-10-22 15:36:49 to 15:42:35. Scratch: `/fast/scratch/hyaku/kaidoku-r27/seats/w2/XpinOnR27Envelopes/`.
- Blockers: none. No message sent.

## Verdict

Holds on every asked check. The re-run reproduces the committed receipt byte for byte, from the working tree and from a clean clone at HEAD. The six `both` rows each carry a non-null `relationship_coverage` object, and their operation is `analyze_function`. No row is `6.7.0` or `none`.

Wording caveat: the lane lesson (`corpus/lessons/round-27.md:89`) calls these `function` envelopes. `function` is the file-name suffix. The operation field says `analyze_function`.

## Checks

Command and exit code are for the run named. Times are UTC. "Holds" is the verdict.

| # | Check and command | Output excerpt | Exit | UTC | Verdict |
|---|---|---|---|---|---|
| C1 | Lane HEAD and clean state: `git -C LANE rev-parse HEAD`; `git -C LANE --no-optional-locks status --porcelain` | `4084d8975b684a8837b1c858eea0008ce9ab49e0`; status lists only four `??` main-agent wave entries, no tracked change | 0, 0 | 15:40:28, 15:42:35 | Holds |
| C2 | Committed 48 envelopes equal the working files: `git ls-tree -r --name-only HEAD -- corpus/evidence/round-27/c1/envelopes`; `git cat-file blob HEAD:<path>` against file bytes | `HEAD envelopes 48; working envelopes 48; same set True`; bytes differing `[]` | 0 | 15:40:28 | Holds |
| C3 | Pinned packages: `/usr/bin/jq -r '.name+" "+.version' <root>/package.json`; sha256 of `dist/domain/canonicalDigest.js` and `evidence.js` | `rea-agents 6.5.0` at `ad9a3fdb...`; `rea-agents 6.7.0` at `a1722018...`; digest code `f46d6bd4...` in both; `evidence.js` `f992d93e...` (6.5.0), `a3fb9f02...` (6.7.0) | 0 | 15:42:35 | Holds |
| C4 | Installed roots equal published tarballs: `python3 -I -B pin-tree-check.py` (plain HTTPS fetch from the lock URL, sha512 against lock integrity, file-by-file compare) | 6.5.0: sha512 matches True; 1650 files; differing `[]`. 6.7.0: True; 1775 files; differing `[]` | 0 | 15:41:19 | Holds |
| C5 | Registry integrity: `npm view rea-agents@6.5.0 dist.integrity` and `@6.7.0` | `sha512-C6BG7Lyr...` and `sha512-yhIx2ioJ...`; both equal the npx lock values | 0, 0 | 15:40:29 | Holds |
| C6 | Receipt shape: parse committed TSV | 48 rows, 5 columns each, 13244 bytes, ends in LF; paths equal the 48 envelopes; counts `{'6.5.0': 42, 'both': 6}` | n/a | 15:40:28 | Holds |
| C7 | Re-run, working tree: `node tools/round-27/xpin-attribute.mjs --pkg65 <6.5.0 root> --pkg67 <6.7.0 root> <48 paths in receipt order>`, cwd lane root, node v24.21.0 | Stdout sha256 `751bbce4...`, 13244 bytes, stderr 0 bytes; first line `corpus/evidence/round-27/c1/envelopes/jq-analyze-base.json` then tab-separated ids, last column `6.5.0`. Earlier ad hoc run at 15:38:07 (node v26.12.0 from mise) gave the same hash | 0 | 15:40:28 | Holds |
| C8 | Re-run, sandbox clone: `git clone -q LANE <scratch>/clone`, then the same node command inside the clone | Clone HEAD equals lane HEAD; stdout sha256 `751bbce4...`. Earlier run at 15:38:08 identical | 0 | 15:40:28 | Holds |
| C9 | Diff against the committed receipt (unified diff of the bytes) | `(no differences)` for both runs; both diff files sha256 `ceaae34c...` | n/a | 15:40:28 | Holds |
| C10 | Six `both` rows carry non-null coverage: read `.data.relationship_coverage` with `/usr/bin/jq` and the recheck script | jq-function base, renamed, repeat (jq and tinyxxd, six files): `relationship_coverage=non-null`, keys `['diagnostics', 'status']`, status `complete`, one diagnostic. All six objects have sha256 `57425e3b...`, so they are identical | 0 | 15:40:28 | Holds |
| C11 | Which verbs the `both` rows carry (operation field and object text) | `operation='analyze_function'` on all six. The object names no verb. Its only text is the diagnostic quoted below | 0 | 15:40:28 | Holds, with naming caveat |
| C12 | No row is `6.7.0` or `none` (column count and consistency) | `{'6.5.0': 42, 'both': 6}`; `rows attributed 6.7.0 or none: []`; last column consistent with columns 2 to 4 on all 48 rows | 0 | 15:40:28 | Holds |
| C13 | Controls: same root in both slots; roots swapped | Same root: `{'both': 48}`. Swapped: `{'6.7.0': 42, 'both': 6}`. The six `both` rows stay `both` under the swap | 0, 0 | 15:40:28 | Holds |
| C14 | Mechanism for the 42/6 split: `sed -n '175,177p'` on 6.5.0 `evidence.js`; `sed -n '178p'` on 6.7.0 `evidence.js` | 6.5.0: `...(evidence.relationship_coverage === null ? {} : { relationship_coverage: evidence.relationship_coverage }),`. 6.7.0: `relationship_coverage: evidence.relationship_coverage,` | 0 | 15:42:35 | Holds (explains the receipt) |

Diagnostic text quoted in C11: "Only resolved Ghidra call references are returned; unresolved computed or indirect calls remain unknown, while function classifications distinguish thunks and externals."

## Which verbs

- The six `both` rows: operation `analyze_function` only. Their `relationship_coverage` object has two keys, `status` and `diagnostics`. No verb is named inside it.
- The 42 `6.5.0` rows, by file verb and operation (from `rows-check.tsv`): analyze and inspect give `binary_overview` (12 rows); decompile gives `procedure_pseudo_code` (6); inspect-binary-layout gives `inspect_binary_layout` (6); instructions gives `read_function_instructions` (6); read-bytes gives `read_bytes` (6); xrefs gives `xrefs` (6). All 42 have `relationship_coverage` null with the key present.
- Observed: no record among the 48 lacks the key.

Why the split is 42/6 (observation from C14, and my inference): the 6.5.0 projection includes `relationship_coverage` only when it is not null. The 6.7.0 projection always includes it. The digest code is identical in both pins. So a null-coverage record hashes differently under the two rules, and a non-null record hashes the same under both.

## Residual risk and gaps

1. Observation: `both` means both rules return the stored id, so such a record cannot show which release made it. Inference: the `6.5.0` label shows only that the stored id follows the 6.5.0 rule and not the 6.7.0 rule. The lesson says the same at `round-27.md:88-90`.
2. Observation: the receipt has no header and records no package roots or tool hash. A re-run needs the same two roots. This run used the roots the checker hard-codes (`tools/round-27/c2-xpin-check.py:53-54`), and C4 verified them.
3. Unknown, not evaluated: no record here lacks the `relationship_coverage` key, so the keyless path is not exercised by this receipt. The lesson's claim about how the 6.7.0 rule treats keyless records (`round-27.md:84-87`) is outside this item.
4. Not run: the REA command-line tool (not in this item) and `c2-xpin-check.py` (another item's check).

## Installs and updates

None. Existing tools used: node v24.21.0 (fnm, for the 15:40 run) and v26.12.0 (mise, for the earlier ad hoc run), `/usr/bin/jq` 1.8.2 (the shell's `jq` is an alias for `jaq` 3.1.1, so I called the binary by path), python3 3.14.8, npm, git. No pacman, uv, npm -g or cargo call.

## Scratch artifacts (sha256)

Directory `/fast/scratch/hyaku/kaidoku-r27/seats/w2/XpinOnR27Envelopes/`:

- `recheck.py` 35af4fa11fcd92b29b4a58d8d7c129c14dc4d35a4b6c62281be7bec7847c0bc2
- `pin-tree-check.py` 0857d7311d847653cfb853fe98b04ac27c9052baba2aebd630ac743733a11ca0
- `receipt-HEAD.tsv` 751bbce4481dc79c4b168f3c0cbb513e12930d18adce0f287716db2496fd4599
- `rerun-working-tree.tsv` 751bbce4481dc79c4b168f3c0cbb513e12930d18adce0f287716db2496fd4599
- `rerun-clone-at-HEAD.tsv` 751bbce4481dc79c4b168f3c0cbb513e12930d18adce0f287716db2496fd4599
- `rerun-clone-head.tsv` (earlier ad hoc run) 751bbce4481dc79c4b168f3c0cbb513e12930d18adce0f287716db2496fd4599
- `rerun-working-tree.stderr` and `rerun-clone-at-HEAD.stderr` e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (both empty)
- `control-same-root.tsv` c6ff70a0950652058eeac30e82a0c335da1b610690906f8a9d2fb51e5e30d2aa
- `control-swapped-roots.tsv` b61676d778e4e233ca951bf2e795938ef0188a679d5156d9709d7b7b1c46bca6
- `diff-working-tree-vs-receipt.txt` and `diff-clone-at-HEAD-vs-receipt.txt` ceaae34ce24ed03109aa05ce8b37a8c6fb30b1c55915749758901af639305d24
- `rows-check.tsv` 22f6755f8d7666f544c1df77e21b1f393e465c0ab0ad08243ebc8259b629a778
- `transcript.json` cb7210cb1be93069492fc39dc5170a5a3345ee2f797525665d3296169ce19ae7
- `recheck-log.txt` 07f39aaa6902847681cd12e33960f8107c3ab80132e2d31afa7ec700ad2b0fd6
- `pin-tree-check.log` 9b674382151ea135d538bf034c1885db60da426742f9ea09b52ea42b36fb5f0a
- `pins/rea-agents-6.5.0.tgz` 531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699
- `pins/rea-agents-6.7.0.tgz` 20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90
- `SHA256SUMS` (16 files, written by the 15:40 run); `control-*.tsv` and `rerun-*.tsv` are the raw outputs listed above.
- Also present: `pins/6.5.0/` and `pins/6.7.0/` (extracted tarballs) and `clone/` (sandbox clone at HEAD).

Lane files read (not changed), with sha256: `tools/round-27/xpin-attribute.mjs` 8ea638379a4397dfc901334767d8015c88b16cf36c7f86e6a5beaf03a5d7f708; `tools/round-27/c2-xpin-check.py` d8de667ff82a46d5c0c9a19d4fc2f5a3c36c12fa037f9a32287046a377209bd3.
