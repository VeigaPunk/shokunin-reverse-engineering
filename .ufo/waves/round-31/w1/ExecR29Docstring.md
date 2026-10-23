# ExecR29Docstring — round-30 routed defect 8 (carried from round 29)

Seat: `KaidokuR31.ExecR29Docstring` (leaf). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
base `c369242fee9f559f895e3f7956b1242076c7b1be`. Work window 2026-10-23T04:11Z–04:16Z.
No lane file was written; the lane copy of the counter still hashes `6ad79d10…` at 2026-10-23T04:14:18Z.

Defect as routed: `corpus/lessons/round-30-verifier-spotcheck.md:151` item 8, carried from
`corpus/lessons/round-29-verifier-spotcheck.md:129` item 7 ("docstring (`:14`, `:27`) still names
round-28 paths"). This is an executor item, not a control seat: there is no frozen counter target
line to meet and none was run.

## 1. What changed

Patched file (scratch, ready for the L1 to copy in):
`/fast/scratch/hyaku/kaidoku-r31/seats/w1/ExecR29Docstring/c1-fresh-naming.py`
SHA-256 `eb685d236fdbfeba4ccb74922c447be14b5130879fc5ecd901c813adf9fae93b`
Old lane file (unmodified): `tools/round-29/c1-fresh-naming.py`
SHA-256 `6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda`
Apply with: `cp /fast/scratch/hyaku/kaidoku-r31/seats/w1/ExecR29Docstring/c1-fresh-naming.py <LANE>/tools/round-29/c1-fresh-naming.py`

Two docstring tokens changed, `round-28` → `round-29`, both on evidence paths the code builds
from `EVDIR = "corpus/evidence/round-29/c1"` (`c1-fresh-naming.py:56`):

| docstring line | before | after | code the line describes |
|---|---|---|---|
| 14 | `corpus/evidence/round-28/c1/carriers.tsv` | `corpus/evidence/round-29/c1/carriers.tsv` | `pinned(root, rev, EVDIR + "/carriers.tsv")` `:357`; pin `:69` |
| 27 | `corpus/evidence/round-28/c1/tally.json` | `corpus/evidence/round-29/c1/tally.json` | `show(root, rev, EVDIR + "/tally.json")` `:377`; entry check `:332` |

Every other path and round number in the docstring was checked against the code and left alone:

- "Round 29 R29-C1" `:2` — `COUNTER_PATH = "tools/round-29/c1-fresh-naming.py"` `:54`, `CLAIM = {"row": "S088"}` `:62`, `TARGET = {"runs": 16, "rows": 152}` `:72`; matches `.ufo/waves/round-29/claims.json` claim R29-C1.
- "round-25 … naming rule" `:2`, `:11` — `RESOLVER = "tools/round-25/a2/resolve-selectors.py"` `:55`; `rule_outputs` docstring `:142` names `tools/round-25/a3/tally-resolution.py`; `PRIMARY = "openchain_sole_unfiltered_args_consistent"` `:73`.
- `tools/round-28/c1-heldout-naming.py` `:4` — **provenance only, kept**. That file exists (30901 bytes, `ls -l` 2026-10-22), the code never references it (`grep -rn fresh-naming tools .ufo/waves/round-24/tools` returns only the round-29 file itself), and the sibling round-29 instrument keeps the same "Copied from tools/round-28/… with round-29 paths" convention (`tools/round-29/c2-filtered-unseen.py:4`). Rewriting it to round-29 would falsify history.
- "round-28 spot-check routed defect 6" `:5` — true: `corpus/lessons/round-28-verifier-spotcheck.md:91` item 6 is exactly the claim-row guard this counter adds.
- "routed defect 4 of the round-27 spot-check" `:10-11` — true: `corpus/lessons/round-27-verifier-spotcheck.md:155` item 4 is the pin-every-loaded-file remedy.
- `corpus/lessons/round-29.md` `:33` — `LESSON = "corpus/lessons/round-29.md"` `:59`.
- "package version 6.5.0" `:15` — `PKG_VERSION = "6.5.0"` `:63`; "opened 2026-10-22" — `OPENED` `:60`; "16/16, 152/152" `:35` — `TARGET` `:72` and `full = …` `:403`.

After the edit the only `round-28` strings left in the file are the two provenance sentences on
lines 4–5; the phrase "with round-29 paths" on line 4 is now true.

## 2. Proof the edit is docstring-only

Script: `ast-docstring-only.py` (sha256 `d7257a482b27d123aa2b567f74e358b67c1a095015c691110c8b534c5f54ef37`);
it parses both files, asserts `body[0]` is a module docstring, removes it, and compares
`ast.dump(tree)` (default, attributes excluded).

Command (2026-10-23T04:11:22Z):
```
$ cd /fast/scratch/hyaku/kaidoku-r31/seats/w1/ExecR29Docstring && python3 -I -B ast-docstring-only.py; echo "ast_exit=$?"
ast_equal_without_docstring=True
ast_dump_sha256_old=fb9ac80622b2dd470ac1034b711b59877a4add64d49358578cb9d7ea479c7c51
ast_dump_sha256_new=fb9ac80622b2dd470ac1034b711b59877a4add64d49358578cb9d7ea479c7c51
docstring_changed=True
docstring_sha256_old=5c6ed42bd583ca2709f18c833e7d0f9de80e3a4fd0742ec6904a238f5b4a26dc
docstring_sha256_new=22ebf01d57e8baedf50163643a5d5b9458f73cee28fe660f86be694750899c9f
docstring_lines_old=39 new=39
ast_exit=0
```
Observation: AST excluding the module docstring is byte-identical; exit 0. The docstring changed and
keeps its 39 embedded newlines.

Strengthening run (2026-10-23T04:15:57Z, `out/ast-with-attributes.txt`), same removal with
`ast.dump(..., include_attributes=True)`:
```
ast_equal_with_attributes=True
dump_sha256_old=3c7001c0c2ad5fd365410551689a5c22043130cfa77b9ad0beddcabe4ec13933
dump_sha256_new=3c7001c0c2ad5fd365410551689a5c22043130cfa77b9ad0beddcabe4ec13933
rc=0
```
Equal even with line/column attributes, because the docstring spans the same lines and every later
node keeps its position.

## 3. Diff

Command (2026-10-23T04:11:19Z): `diff -u <LANE>/tools/round-29/c1-fresh-naming.py c1-fresh-naming.py` — exit 1 (differences, as expected):
```diff
--- /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-29/c1-fresh-naming.py	2026-10-22 16:57:26.843041511 -0300
+++ c1-fresh-naming.py	2026-10-23 01:11:12.882019794 -0300
@@ -11,7 +11,7 @@
 spot-check): the round-25 resolver it imports, and the frozen carrier and selector lists.
 
 Counts, at --rev:
-  runs_ok        carriers in corpus/evidence/round-28/c1/carriers.tsv with exactly one valid
+  runs_ok        carriers in corpus/evidence/round-29/c1/carriers.tsv with exactly one valid
                  call record in runs.tsv: exit 0, frozen argv, package version 6.5.0 and the
                  frozen package.json sha256, utc_start strictly after the counter's own commit,
                  envelope file first committed no earlier than the counter, envelope sha256 equal
@@ -24,7 +24,7 @@
                  counter. Byte-identical response bodies for different selectors are legitimate
                  (an empty result is the same bytes for every unknown selector) and are never
                  refused: responses are keyed by their manifest entry, not by their bytes.
-  tally_equal    1 when corpus/evidence/round-28/c1/tally.json equals the tally this counter
+  tally_equal    1 when corpus/evidence/round-29/c1/tally.json equals the tally this counter
                  recomputes from the committed envelopes and responses.
   entry_ok       1 when the knowledge entry exists, opens with source:/verified-at:/recheck:,
                  names tally.json, states the primary rule's triple exactly as
```

Byte-scope check (2026-10-23T04:14:47Z, `out/byte-scope.txt`):
```
old_bytes 31703 new_bytes 31703 delta 0
crlf_old 0 crlf_new 0
ends_newline_old True ends_newline_new True
split_lines_old 636 split_lines_new 636
differing_lines [14, 27]
```
Observation: same byte length, no CRLF, trailing newline preserved, exactly lines 14 and 27 differ.

## 4. Drafted supersession entry (NOT applied)

`.ufo/waves/round-29/claims.json` currently has one entry under `instrument_supersessions`
(the M29-3 note, `:69-70`). Draft to append as the second element (shape mirrors the existing
entry's `path`/`commit`/`sha256`/`reason`, plus the two fields this correction needs):

```json
{
  "path": "tools/round-29/c1-fresh-naming.py",
  "commit": "<ROUND-31-LANDING-COMMIT-SHA>",
  "sha256_old": "6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda",
  "sha256": "eb685d236fdbfeba4ccb74922c447be14b5130879fc5ecd901c813adf9fae93b",
  "round": "round-31",
  "reason": "docstring-only correction (round-30 routed defect 8); ast.dump without docstring identical"
}
```

- `sha256_old` is the frozen pin (`instruments` map, `claims.json:14`); `sha256` is the corrected file, matching the existing entry's convention that `sha256` names the file at `commit`.
- `commit` is **mandatory and cannot be pre-filled**: both freeze gates match the disclosure on the exact `(path, commit)` pair of a commit that touched the file in `freeze..measured` (`tools/round-29/freeze-gate.py:132-134`; same code in `.ufo/waves/round-24/tools/freeze-gate.py`). It must be the commit that lands the corrected counter — if the counter fix and the claims append land in one commit, that commit; if they are separate commits, the counter's commit, never the claims commit.
- Do **not** edit the `instruments` pin for this path: the gates compare it against the blob at the freeze commit `dbd87cfa`, where the file is still `6ad79d10…`; rewriting it produces `INSTRUMENT_PIN_MISMATCH` (verified in source: `freeze-gate.py:104,107-114,124,129,132-133` and `tools/round-30/prefreeze-gate.py:187,193`).
- The existing entry's long prose is not a precedent for length: this reason is the exact string the assignment froze.

Prepared file: `supersession-entry.draft.json`, sha256
`fa0ab4c7d115af09a97040b9257da1af00c4c90dff5c5c223a6bd0c9e231bd4a`; it parses
(`json_parses=True keys=['commit','path','reason','round','sha256','sha256_old']`).

## 5. Sandbox proof of the supersession mechanics (round-29 claims)

Sandbox clone: `/fast/scratch/hyaku/kaidoku-r31/seats/w1/ExecR29Docstring/clone`, cloned read-only
from the lane with `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset. To avoid a 1.2 GB checkout I
cloned `--no-checkout`, pointed `refs/heads/ctl` at `35ba7c52…`, `git read-tree` that commit
(full index, 21510 entries), and `checkout-index` only the three files used. The tree stayed
complete: `ls-tree -r --name-only HEAD | wc -l` = 21510 at the base and after both commits.
Sandbox commits: `faf84da99821f27c32de1ebc47328d3080256fc9` (docstring fix, file bytes identical to
the deliverable) and `fbd7ce3d2ddcd281c2c3618205ffffdf35262fb6` (claims append).

Command (2026-10-23T04:13:14Z), gate at the fix commit with **no** supersession entry:
```
$ python3 -I -B clone/tools/round-29/freeze-gate.py --root clone --rev HEAD   # exit 0
rev faf84da99821f27c32de1ebc47328d3080256fc9 audited 21 clean 4
round29 verdict: FLAGGED
finding {'finding': 'INSTRUMENT_UNPINNED', 'path': 'tools/round-28/c1-heldout-naming.py'}
finding {'commits': ['faf84da99821f27c32de1ebc47328d3080256fc9'], 'disclosed': 0, 'finding': 'INSTRUMENT_REVISED', 'path': 'tools/round-29/c1-fresh-naming.py'}
```
Command (2026-10-23T04:13:30Z), same gate after appending the entry with `commit` = the fix commit:
```
$ python3 -I -B clone/tools/round-29/freeze-gate.py --root clone --rev HEAD   # exit 0
rev fbd7ce3d2ddcd281c2c3618205ffffdf35262fb6 audited 21 clean 4
round29 verdict: FLAGGED
finding {'finding': 'INSTRUMENT_UNPINNED', 'path': 'tools/round-28/c1-heldout-naming.py'}
```
Observation: the entry removes `INSTRUMENT_REVISED` for the counter; round-29 keeps only the
pre-existing `INSTRUMENT_UNPINNED` on `tools/round-28/c1-heldout-naming.py`. That code set equals
both ledgers' rows: `corpus/claim-freezes-v2.tsv:20` and `corpus/claim-freezes.tsv:17` are
`round-29  FLAGGED  INSTRUMENT_UNPINNED …` at `35ba7c52…` (`git show 35ba7c:corpus/claim-freezes-v2.tsv
| grep '^round-29'`). So `tools/round-29/prefile-check.sh`'s `--disclosures` comparison stays exact
and no ledger row needs a round-31 rewrite for this change — provided `commit` is filled correctly.
Observation: after the fix commit, `git log --diff-filter=A --format=%H -- tools/round-29/c1-fresh-naming.py`
still returns `dbd87cfa09eb89306c4e07d3171a4556eb732024`.

## 6. Who reads the docstring or the file hash at run time

Grep evidence (`out/greps.txt`, captured 2026-10-23T04:14:40Z):
```
$ grep -rn '6ad79d10…' tools .ufo/waves/round-24/tools          -> rc=1 (no tool holds the hash)
$ grep -rln '6ad79d10…' . --exclude-dir=.git                    -> .ufo/waves/round-29/claims.json, .ufo/waves/round-29/w1/{MutC1Counter,ScoutSkillRegistry,ScribeRegistry,CriticHeldOutC1}.md, SKILL.md
$ grep -n 'fresh-naming' tools/round-30/prefreeze-gate.py       -> rc=1
$ grep -rn 'fresh-naming' tools .ufo/waves/round-24/tools       -> only tools/round-29/c1-fresh-naming.py:38,39,40,54
$ grep -rn 'open(.*tools/|hashlib.sha256.*open' tools/round-29 tools/round-30 -> rc=1
$ grep -n 'COUNTER_PATH|__file__|__doc__' tools/round-29/*.py
  c1:54 COUNTER_PATH = "tools/round-29/c1-fresh-naming.py"
  c1:360 counter_time = first_commit_time(root, rev, COUNTER_PATH) if rev is not None else 0
  c1:441 _w(repo, COUNTER_PATH, counter_src)      # selftest fixture only
  c1:521 here = os.path.abspath(__file__)         # selftest reads its own bytes to stage the fixture
  c2:52/152/257/291 same pattern
```
Readings (observation): the only run-time use of the counter path is
`first_commit_time` → `git log --diff-filter=A` (`c1-fresh-naming.py:103-108,360`), which finds the
add commit; a later modification commit does not change it. Nothing reads `__doc__`, nothing hashes
the counter file, `tools/round-30/prefreeze-gate.py` does not mention it, and no round-29 counter
mentions it except its own `Usage:` lines and `COUNTER_PATH`. `prefreeze-gate.py` verifies pins at
the freeze commit (`:187,193`) and honours supersessions only for its `TOOL_UNPINNED` check
(`:210-212`, path + reason); the counter is already digest-pinned there, so that gate is unaffected.

Conclusion for re-measuring round 29 (inference from the observations above, not a counter run):
the counting command stays
`python3 -I -B tools/round-29/c1-fresh-naming.py --root <LANE> --rev <REV>`, and at any given `--rev`
its output is identical to the pre-edit counter's, because the executable AST is identical,
`counter_time` is the unchanged add commit, and no code path reads the docstring. The supersession
changes only round-29's freeze-gate disclosure: it converts a post-freeze `INSTRUMENT_REVISED`
finding back to the ledgered `INSTRUMENT_UNPINNED` state.

## 7. Risks, limits, out-of-scope observations

- **Blocker-shaped dependency, resolved by the L1:** the draft's `commit` placeholder must be replaced with the real round-31 commit that lands the corrected file, or the round-29 freeze audit will flag `INSTRUMENT_REVISED` and `prefile-check.sh` will disagree with both ledgers. The value cannot be computed before the commit exists.
- [INFERENCE] Counter outputs are unchanged; this seat did not execute the counter (wave rule: the parent owns post-integration checks).
- The sandbox commit SHAs are clone-local and are not the lane's future commit; only the mechanism is demonstrated.
- Old hash `6ad79d10…` survives in prose at `corpus/lessons/round-29-verifier-spotcheck.md:46` and in round-29 wave reports. Those are filed historical records, not gate inputs; leave them.
- Out of scope, observed while reading: the docstring's "Every file the counter loads is pinned below by sha256" is imprecise — only the resolver and the carrier/selector lists are in `PINS` (`:68-70`); `runs.tsv`, `db/manifest.json`, envelopes, `tally.json`, SOURCES, the lesson and the entry are loaded unpinned. Pre-existing round-27/28 wording, not a round-number/path defect; not changed.
- No tools installed; no REA run; no network access; no pacman; lane git state untouched (all lane git commands were read-only `log`/`show`/`ls-tree`/`rev-parse`/`diff`).

## 8. Scratch artifacts (sha256)

| path under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/ExecR29Docstring/` | sha256 |
|---|---|
| `c1-fresh-naming.py` (patched deliverable) | `eb685d236fdbfeba4ccb74922c447be14b5130879fc5ecd901c813adf9fae93b` |
| `ast-docstring-only.py` | `d7257a482b27d123aa2b567f74e358b67c1a095015c691110c8b534c5f54ef37` |
| `supersession-entry.draft.json` | `fa0ab4c7d115af09a97040b9257da1af00c4c90dff5c5c223a6bd0c9e231bd4a` |
| `out/ast-proof.txt` | `3b9074502d20dab7a60b6b68be282ba3887a8c14bef24b7f638dc19e20f219df` |
| `out/ast-with-attributes.txt` | `fab56a322275f2ce879c71396e25e7296775e6039169469b78cc336efbb1f1a3` |
| `out/diff.txt` | `b25dbceb60713b5b554449b8324ed17f33887c3c3dd88a21d8107d9952cdeca4` |
| `out/byte-scope.txt` | `9dcfb1ed84326577bcf14dbffbb5b00705857ad83a9877bed3ce3c87f66527f8` |
| `out/greps.txt` | `30f5e069b0ba762d92179fc1952c860ce0417b97003a9518ff6b2e3540199229` |
| `out/freeze-gate-before-entry.json` | `099eb7b2a6c1e1590d3bfc3aa4b6172774fa9de22eb0f9860b67b3c5ee523fa3` |
| `out/freeze-gate-after-entry.json` | `4342963ac9189393f517a98db514ebb2030ff9d18ecdea30f0e0585301c61d0b` |
| `clone/tools/round-29/c1-fresh-naming.py` | `eb685d236fdbfeba4ccb74922c447be14b5130879fc5ecd901c813adf9fae93b` |
| `clone/.ufo/waves/round-29/claims.json` | `adcf534f24d41921cbd1a037f078420bdac8ee73a4947ad0ea03b2622dd2239b` |

Sandbox clone URL/path and commits: `git clone --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin`;
base `35ba7c522dba55f9be27eb161d4254eacaa24330`, fix `faf84da99821f27c32de1ebc47328d3080256fc9`,
claims append `fbd7ce3d2ddcd281c2c3618205ffffdf35262fb6` (directory not hashed; 21510 tree entries at
each commit, matching the base).
