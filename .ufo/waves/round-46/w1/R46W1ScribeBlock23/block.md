- **23. A measure is only evidence when its own forgeries fail.** <!-- freeze-integrity-table v2 -->

  Block 22 stated the freeze arms; this block states what makes the statement checkable. The
  frozen set is re-derived from the claims file at the measured revision, so the log scope, the
  blob arm and the dirty scope read one list and cannot drift apart. Each row is a defect the
  round-45 closure routed, the clause that let it pass, and the arm that now fails it. Exits keep
  their meanings: 1 is a clause that ran and failed, 2 is could-not-evaluate — a malformed
  heading, an unknown revision, a refused output path or a scratch root on a temporary partition
  is 2, never a crash and never a clean verdict. Interpreter pin: `tools/round-46/attest.py`
  `sha256:e6c44d2d57dbbc65ed8d14b642a6101eea264b05faf68c25606525b8fe532346`. S142 grounds the
  merge arm: `--diff-merges=first-parent` shows the diff a merge introduced on the first-parent
  side. Freeze chain, recorded so the pin cannot be read against the wrong bytes: the first
  freeze commit carried pre-final instrument bytes hashing to
  dd1e7df1682c5b63ed9f5f75a3aff26c7914e6d41885e5e2da717aa91165d0fb, and the F3 commit `65678df0`
  that carried the final instrument — the measured freeze — is the pin above.

| trigger | v1 hole | v2 arm | exit |
|---|---|---|---|
| R45-CL2 a registry row names a tool that exists at no revision | cell 0 matching was the whole test, so a ghost row registered | presence: the row's path must resolve at the measured revision or the surface is not met | 1 |
| R45-CL6 a merge's own resolution edit touches a frozen path | the round-45 log arm printed no diff for a merge, so the edit was invisible | merge: `-m --diff-merges=first-parent --name-status -z` shows it and the blob arm must agree | 2 |
| R45-CL7 a block floor and a missing-block reason survive the selftest | clause 1 was exercised only from below and clause 2 by no case | marker: counted by occurrence, with block presence by identity, each clause carrying its own red case | 1 |
| R45-CL9 a citation resolves but names nothing about the defect | the regex saw three trees and took a line-less reference; a body bullet manufactured a block, and a row registered under any heading with cell 0 searched | refs and rows: every path-like token is parsed with its selector, rows register only between the markers, and cell 0 is compared whole | 1 |
| R45-CL13 a 44-line artefact with garbage rows scores met | row count and exit cells were structural tests, the stub interpreter passed a banner check, and two markers in one block still counted once | pin and rows and battery: the sha256 pin kills the stub, a row needs a routed id and a vocabulary arm, and the nine forgeries must go red | 1 |
| R45-CL14 six fenced rows anywhere in the file register | the parser was fence-blind, comment-blind and heading-blind, matched cell 0 by search, and let the first row win | header and marker and presence: rows register only inside the marked section, outside fences and comments, under the exact house header | 1 |
| R45-CL15 a dirty-pathspec flag narrows the dirty scope instead of adding to it | the flag replaced the scope, and two arms had no unique detection | dirty and restored: the scope is a union, and each arm has a case that only that arm kills | 1 |
| R45-CL18 a path named only by a freeze-path never entered the touched set | the log scope and the freeze scope were different sets, so a tamper-then-restore read clean | pathspec: one frozen set derived at the measured revision feeds both arms, so the path lands in restored | 1 |
| R45-CL19 a tamper-then-restore folded away by a squash merge | the surviving history names nothing, and the blob arm reads equal after a restore | blob: the blob arm is the remaining defence, and the limit is stated instead of claimed away | 2 |
| R45-CL20 the scratch root silently falls back to a temporary partition | the gettempdir fallback was an accepted root, and the registry header was never validated against the house schema | output and header: a temporary-partition root is refused as could-not-evaluate and the header is compared cell for cell; the eight-column gap stays routed, not claimed | 2 |
| R45-CL22 a json-out target inside the graded surface is written before the verdict | the output path was trusted and opened first | output: the target must resolve inside the lane root and outside the graded and frozen set, or nothing is written | 2 |
| R45-CL23 a pathname holding a newline or tab is recorded C-quoted | the comparison was between quoted strings and real paths, so the restored arm was dead | commit: the history arm splits NUL-terminated name-status records, so pathnames compare unmodified | 1 |
| R45-CL24 the record drifts from the instrument it describes | nothing bound the prose to the code, and an ambiguous arm cell read as covering a case it did not | pin: the block carries the interpreter sha256, so prose and bytes cannot diverge silently | 1 |

  Refs: `corpus/lessons/round-45.md:77-79` (R45-CL2, the presence gap), `corpus/lessons/round-45.md:90-97` (R45-CL6, the merge blind spot), `corpus/lessons/round-45.md:98-101` (R45-CL7, the selftest holes), `corpus/lessons/round-45.md:107-120` (R45-CL9 A1–A6, the six landed mutants), `corpus/lessons/round-45.md:142-159` (R45-CL13, the 44-line greened artefact), `corpus/lessons/round-45.md:160-172` (R45-CL14, the six fenced rows), `corpus/lessons/round-45.md:173-183` (R45-CL15, the replaced dirty scope), `corpus/lessons/round-45.md:197-211` (R45-CL18 and R45-CL19, the pathspec boundary and the squash limit), `corpus/lessons/round-45.md:212-217` (R45-CL20, the fallback root), `corpus/lessons/round-45.md:224-234` (R45-CL22 and R45-CL23, the trusted output path and the quoted pathname), `corpus/lessons/round-45.md:235-247` (R45-CL24, record drift), `plans/round-46-claims.md:37-109` (the R46-C1 predicate, clause by clause), `plans/round-46-claims.md:110-167` (the R46-C2 predicate), `plans/round-46-claims.md:168-177` (the frozen set both counters derive), `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:36-48` (a registered class set can hold while the surface is still shortcut-reachable — the reason a measure needs its own forgeries).
