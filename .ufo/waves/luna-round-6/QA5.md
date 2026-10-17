# QA5 — git-object discipline (lane B)

## CLAIM
No seat substituted the worktree for git objects on repo source facts: all 35 repo-tracked pointers across lane A resolve at HEAD f0e8cde within line bounds, with zero worktree drift. Caveat: 12 of 141 pointers cite mutable untracked artifacts and no longer resolve.

## METHOD
Froze lane-A frame = 52 reports, mtime 18:16:42–18:29:27 (frame listing digest `fd65eda5…`; EX7.md falls outside this window — its current 18:53 content is a leg-7 replay, any earlier version unobservable). Regex-extracted 141 `path:line` tokens from 29 pointer-bearing reports; resolved each: tracked → `git cat-file -e HEAD:<p>` + line bound via `git show HEAD:<p>`; wave artifacts / out-of-repo (parent workspace, sibling repos, /tmp, system) → filesystem + line bound. Deterministic 6-report sample (sorted pointer-bearing list, indices round(k·28/5), k=0…5): CA1, CE2, K1, RE1, RV4, XG1 = 21 pointers. Auxiliary snapshot: 43 lane-B reports, 257 pointers (roster still growing). Read-only; no probes/MCP.

## FINDINGS
- Sample: all 5 HEAD-tracked pointers resolve at HEAD (K1→`PROVINCE.md:45-49` = Electron/ASAR row; CE2→`SCORECARD.md:92-123` spans the bash fence to `PY`); 15/16 non-HEAD resolve (RE1's leg-8 cite is the one stale).
- Sweep: 35/35 HEAD-tracked pointers resolve; zero HEAD overruns; every cited tracked file byte-equal to HEAD (`git status` clean — no untracked repo file is cited anywhere in the 52-report frame).
- 10 stale: CA2/EX9/PS3/RE1/RV7 cite `receipts/leg-8.md` (now 25L) and `leg-9.md` (now 13L) up to line 47; both receipts were rewritten 18:28:03/04, after those reports (18:22–18:27). CC9 (lane B) independently flags EX9's pointer. 2 unresolvable: RV2's `/tmp/luna-round-6-rv2/{leg-3,leg-4}.md` deleted scratch.
- Lane-B flags all resolve once lane-B's own `receipts-B/leg-N.md` (62–95L), sibling-repo corpus files (kama/tsukuroi/revenger), and the npx-cache contract file are used as roots.

## THREATS
On a clean worktree, `Read`/grep and `git show` are byte-indistinguishable, so method use is only falsifiable; positive git-object evidence appears in 4 reports (CA5 `git show HEAD:corpus/README.md`; CE2 "reads immutable Git objects"; SE4; XA), the rest silent. Receipts are untracked by construction, so their cites resolve only against mutable worktree state (overwrites proven by mtimes). Lane-B scan is a mid-flight snapshot, not a closing state. Line-range semantics are report-defined.

## VERDICT
FINDING: repo-source discipline held (35/35 HEAD-tracked pointers resolve, zero drift), but 12/141 lane-A pointers are stale — leg-8/leg-9 receipt rewrites at 18:28 postdate five reports' cites, and RV2's /tmp receipts are gone.
