| 82 | A negative existence claim names the root of the sweep that backs it **and** roots that sweep at the base its cited relative path is actually relative to (package root, campaign root): a sweep of a sibling tree, or of any directory that is not the base or an ancestor of it, cannot support "nowhere on this host". The claim's scope is the swept root, never the host, unless the sweep is the host root; the `find` is re-run under that root and its empty output is what the claim asserts. Before data, the gate carries a red case for a fleet-rooted sweep of a path relative to the shokuknow root, a red case where the properly rooted `find` returns the file, and a green case that is a true negative under the same root. | `corpus/lessons/round-38-verifier-spotcheck.md` §3 (R38-CL1) and §5; round-38 lesson `:80-82`, `:95-97` and `w2/R38W2AssimRejects.md` D3 put two existing campaign tsvs "nowhere on this host" on a `find` rooted at the fleet repo, while both sit at `lanes/kaidoku/round{7,9}/work/` under the shokuknow root (1204 B `d8fa9eae…af6d`, 1177 B `709cddc7…ea43`). Gate: `.ufo/waves/round-39/w1/artifacts/R39CL1Correction/neg-existence-check.py`; as-filed claims → exit 1 `host-claim-subtree-root+misrooted`, correctly rooted but present → exit 1 `negative-refuted`, true negative → exit 0 (`receipts/gate-as-filed.json`). | sharpens 56, 57, 65 |

### Why 82 and not an existing row

- 56 and 57 require every **spelling** of a surface to be searched and the searched revision and
  scope to be stated. Both are satisfied by the round-38 sweep: one spelling, scope stated
  ("this host"). The claim was still false, because the root was not the base — the axis those
  rows do not cover.
- 65 requires a per-file diff for a "file unchanged" claim; it says nothing about a file's
  **absence**.
- The gate is mechanical on the two facts a claim already has to carry (the `find` argv and the
  cited path's base), so it costs one line per refusal and cannot be satisfied by prose.
