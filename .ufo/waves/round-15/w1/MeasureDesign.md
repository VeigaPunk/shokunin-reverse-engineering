# MeasureDesign — round-15 immutable measurement script

author: KaidokuR15.MeasureDesign (executor)
scope: `.ufo/waves/round-15/measure.py` only; advisory report. No corpus,
gate, SKILL, registry, LOG, MANIFEST or SCORECARD edit; no commits; no
verification run.

## Delivered file

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/measure.py`
— stdlib only (`json`, `re`, `subprocess`, `sys`, `collections.Counter`,
`pathlib.Path`). Invocation:

```sh
python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/measure.py <revision>
```

It resolves `<revision>` with `git rev-parse --verify '<rev>^{commit}'` and
reads every byte through `git -C <repo> show <sha>:<path>` and
`git -C <repo> ls-tree -r --name-only <sha>`. The worktree and index are never
read for content; no network, writes, provider or target execution.

Delivered bytes: SHA-256
`226e2f104fbc87139476238a8ab7d17b7749557aa3caaf7f171105d2d3900775`,
3764 bytes.

Exit codes: `0` census completed, `2` usage error, unresolvable commit, or a
missing structural anchor (no `## Coverage map` section, no source rows).
It emits no verdict and no score.

## Observables (presence proxies, not semantic proof)

| JSON key | Definition | Coordinate |
|---|---|---|
| `C1_round15_knowledge_entry` | path present as a blob at `<rev>` | `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md` |
| `C1_snapshot_inventory_tool` | path present as a blob at `<rev>` | `.ufo/waves/round-15/snapshot-inventory.py` |
| `C2_quality_row17_manual_only_wording` | a numbered table row `\| 17 \|` exists **and** that row matches `must not be submitted` case-insensitively | `corpus/QUALITY.md` |
| `C2_round14_lesson_correction_marker` | exact substring present | `corpus/lessons/round-14.md`, heading `## Round-15 correction — virtual-dispatch advisory` (U+2014 em dash) |
| `knowledge_files` / `mapped` | `.md` stems under `corpus/knowledge/` vs stems named in the `## Coverage map` section | `corpus/README.md` |
| `missing` / `dangling` | `knowledge − mapped` / `mapped − knowledge`, sorted | same |
| `sources_rows` | rows matching `^\|\s*S\d{3,}\s*\|` | `corpus/SOURCES.md` |
| `tiers` / `statuses` | histograms of the trimmed tier (cell 4) and status (cell 8) values actually observed | same |

The four C1/C2 fields are deliberately strict: the C2 wording must occur
inside a row numbered 17 (the same phrase elsewhere in `QUALITY.md` does not
count), and the marker is matched byte-for-byte after UTF-8 decode, so a
hyphen, colon or different spacing reads 0 rather than a near-match. This
keeps the measurement a stated observable, not a fuzzy classifier.

Map boundary reproduces the round-14 convention: split on `## Coverage map\n`,
stop at the next `\n## `, then collect `2026-10-\d{2}-[a-z0-9-]+` stems.

## Grounded baseline readings

Observed with read-only inventory commands on
`9719dd232687f5ee78a4ed323b37f8810e833d10` (no measurement script executed):

```text
marker_lines=0  phrase_lines=0  row17=0  c1_entry=0  c1_tool=0
knowledge_md=92  source_rows=22  coverage_anchor=1
```

Expected output at that baseline: all four C1/C2 fields `0`; `knowledge_files`
92, `mapped` 92, `missing`/`dangling` empty; `sources_rows` 22;
`tiers` `{"A":20,"B":1,"C":1}`; `statuses` `{"mined":21,"rejected":1}`.

After L1 integration and commit, the expected delta is exactly the four
presence fields `0 → 1`, `knowledge_files/mapped 92 → 93` once the new entry is
mapped in `README.md`, `sources_rows` unchanged at 22 (no new source rows are
authorized), and tier/status histograms unchanged. If `missing` contains
`2026-10-20-r15-go-snapshot-inventory`, the entry is committed but the README
coverage map was not updated.

## Current worktree observation (not a measurement)

At authoring time `git status --porcelain` showed the routed-defect drafts as
uncommitted modifications (`corpus/QUALITY.md`, `corpus/lessons/round-14.md`,
`corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`) plus untracked
`.ufo/waves/round-15/`; sibling seats were still landing edits. Read-only
inspection of the worktree shows the drafted row `| 17 | … must not be
submitted as machine-gradeable … |` and the lesson heading
`## Round-15 correction — virtual-dispatch advisory` (line 144). These are
uncommitted drafting states, not readings the script can see; L1 must measure
a commit that contains them.

## Limits

- Presence is not semantic proof: row-17 presence does not prove the criterion
  is coherent or correctly scoped, marker presence does not prove the
  correction states the mechanism correctly, and file presence does not prove
  the knowledge entry is sourced. Those remain reviewer/L1 judgments.
- The map count is bookkeeping under one heading/regex boundary; a renamed
  heading produces exit 2 rather than a wrong number, and stems mentioned in
  prose inside the map section are counted exactly as round 14 did.
- Tier/status histograms count raw trimmed cells; blank or duplicated cells are
  reported as observed, with no registry-vocabulary validation.
- Committed blobs only: uncommitted edits and untracked paths are invisible.
  In particular `.ufo/waves/round-15/snapshot-inventory.py` must be committed
  in the measured revision or `C1_snapshot_inventory_tool` reads 0.
- No gate, selftest, provider, target or network operation is performed; the
  script does not establish that `quote-fidelity` behaves as documented, and
  its readings are not a SHONEN/admission verdict.

## Proposed L1 checks (L1 executes; this seat did not)

```sh
python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/measure.py 9719dd232687f5ee78a4ed323b37f8810e833d10
python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/measure.py <delivered-after-sha>
```

Independent coordinate cross-checks at the after commit:

```sh
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show <after>:corpus/lessons/round-14.md | grep -c 'Round-15 correction — virtual-dispatch advisory'
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show <after>:corpus/QUALITY.md | grep -Ei '^\|[[:space:]]*17[[:space:]]*\|.*must not be submitted'
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-tree -r --name-only <after> -- corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md .ufo/waves/round-15/snapshot-inventory.py
python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/measure.py; echo "exit=$?"
```

Expected: the first grep prints `1`, the second prints the matching row, and
the `ls-tree` prints both paths (one line per present path). The last command
prints the usage message and `exit=2`. Compare that the before/after JSON
differs only in the four presence fields (and `mapped` if the README map was
updated), then name the result as a presence census, not capability proof.

## Risks

- Measuring baseline `HEAD` while the corrections remain uncommitted keeps all
  four fields 0; wave files under untracked `.ufo/waves/round-15/` are not in
  `ls-tree` until committed.
- A renamed marker, a hyphen for the em dash, or C2 wording placed outside a
  numbered row 17 yields 0 by design; the report should not be read as a tool
  defect.
- No installs were performed or needed; no verification was executed.
