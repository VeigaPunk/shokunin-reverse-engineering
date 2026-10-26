# R39W2Sentinel — round-39 wave-2 seam check (fleet root, scratch, lane drift, secrets, escaping symlinks)

**Verdict: DEFECTS FOUND.** Three seam defects outside the two claims themselves: a wave-2
report written into the **fleet repo** instead of the lane (F1), **post-freeze uncommitted edits +
one deleted committed evidence binary** in the wave-1 material the landing rests on (F2), and a
**depth-dependent symlink hazard** that makes the K5/K6 escape links safe only under a
whole-tree copy discipline (F4, pre-existing design, not a round-39 regression). Items 4 and 5
are otherwise **CONFIRMED**: no secrets in the round-39 evidence, and no lane tool, hook or REA
run follows the K5/K6 escaping symlinks or copies anything from their targets.

Frozen material is intact: `carriers.json`, both oracles, both symlink tables and both carriers
are **byte-identical freeze→HEAD** (`8fcda41c`→`e40a25df`) and the working tree shows no drift on
those paths; the K5/K6 carrier pins on disk equal `carriers.json`. No frozen predicate, counter,
carrier, oracle or table was changed by me; I wrote only this report and
`.ufo/waves/round-39/w2/artifacts/R39W2Sentinel/`.

## Findings

| id | severity | one line |
| --- | --- | --- |
| F1 | **medium** | `R39W2HeldReproB`'s report landed at `/home/vgpnk/Projects/shokunin/.ufo/waves/round-39/w2/R39W2HeldReproB.md` (fleet repo), no copy in the lane; its artifacts are in the lane. All 39 dispatch prompts give a lane-**relative** `Report:` path and only 1 carries the absolute lane anchor. |
| F2 | **low-medium** | Wave-1 evidence edited **after** the freeze commit and left uncommitted (2 reports, `+8/-1` in `symlink-tables.py`), and a committed 365-byte w1 carrier deleted from the working tree. `git log -1` for all four paths is still `8fcda41c` (14:12:51); the edits are 14:13:30-14:14:45. |
| F3 | low | Scratch hygiene: 850 leaked `gen.*` fixture dirs under `/fast/scratch/hyaku/kaidoku-r39/` (14:10:12→14:34:58, fastest growth ~6/min). Live wave — report only, nothing removed. |
| F4 | low (design) | K5/K6 escape-link safety is **depth-, not target-dependent**: a *bare* link placed at depth ≤3 resolves to a real host `/etc` path (measured: K6's link read 64 B of `/etc/passwd` from `/tmp`); `cp -a` of the whole tree stays inert (measured). `/etc/shadow` is 0600 root and unreadable as `vgpnk` in every configuration. |

## 1. Fleet-root seam

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
 M .scratch/goal-20261026-hyaku-run9.md
?? .ufo/reports/round-48/tameshi.md
?? .ufo/waves/round-39/
```

* Only one untracked fleet-root path names kaidoku/round-39: `.ufo/waves/round-39/`, which
  contains exactly one file — `w2/R39W2HeldReproB.md`, 10085 B, mtime `2026-10-26 14:30:15`.
  It is a finished wave-2 report ("**Verdict: CONFIRMED.** All five committed R39-C2 held-out
  envelopes (H06–H10) reproduce…", tail says "Scratch `$S` removed"). Its artifact directory
  **is** in the lane (`.ufo/waves/round-39/w2/artifacts/R39W2HeldReproB/`, 12 files, 14:28-14:29),
  so the seat split artifacts (lane-relative, correct) from the report (fleet-root).
  Rechecked at 14:36:56 and 14:38:42: still no `kaidoku-shokunin/.ufo/waves/round-39/w2/R39W2HeldReproB.md`.
* **The mechanism is measured, not inferred** — this seat reproduced it: its session cwd is
  `/home/vgpnk/Projects/shokunin`, and the first `write` of this report with the relative path
  `.ufo/waves/round-39/w2/R39W2Sentinel.md` landed at
  `/home/vgpnk/Projects/shokunin/.ufo/waves/round-39/w2/R39W2Sentinel.md` (16262 B, 14:39),
  alongside HeldReproB's file. It was moved into the lane immediately and the fleet-root copy
  removed; the fleet repo is back to exactly the three pre-existing entries above.
* Root cause is mechanical, not a stray typo: every one of the 39 wave-2 dispatch items says
  `Report: write your scoped findings to .ufo/waves/round-39/w2/<seat>.md` — a **lane-relative**
  path — and `json.dumps(w2-dispatch.json).count("Every \`Report:\` trailer path is relative
  to")` = **1** (this seat's prompt only). A seat whose cwd is the fleet root resolves the
  relative path there.
* Impact: the report is invisible to lane wave-2 aggregation/L2 review and leaves an untracked
  `.ufo/waves/round-39/` in the fleet repo (shared `git status` signal); its artifact references
  (`…/w2/artifacts/R39W2HeldReproB`) do not resolve from where the report sits. Note the report
  itself asserts "nothing written outside this report and the artifacts directory" — true only
  relative to the lane it is not in.
* Smallest remediation (owner action, outside my write scope): copy that file to
  `kaidoku-shokunin/.ufo/waves/round-39/w2/R39W2HeldReproB.md` and have `w2-gen.py` emit
  `Report: … /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-39/w2/<seat>.md`
  (absolute), for the remaining seats of this wave and for round 40.
* Out of scope, untouched: `.ufo/reports/round-48/tameshi.md` (names tameshi/round-48, not
  kaidoku/round-39); `.scratch/goal-20261026-hyaku-run9.md` is the orchestrator's goal file
  (`M`, names kaidoku r39 across its queue table). I read (grep) only that single modified path
  named by `git status` — no enumeration of `.scratch/` or `.ufo/state/`, nothing written there.

## 2. Scratch leftovers (`/fast/scratch/hyaku/kaidoku-r39/`, names/ages only)

```
top_level=870  gen_prefix=850   (14:31 snapshot: 873/850; ~6 new/minute)
oldest gen.*: 2026-10-26 14:10:12 gen.s8vhrz_z
newest gen.*: 2026-10-26 14:34:58 gen.8touyt2f
non-gen top-level: 19 seat dirs (R39W2AbsenceGate … R39W2Simplifier, incl. R39W2Sentinel), counter/, l1/
```

850 `gen.*` dirs of 93 bytes are leaked `mktemp` fixture roots from a live fixture loop that is
not cleaning up per iteration (they are not seat scratch; the wave is still running, so this is a
hygiene note, not cleanup work). I did not enter other lanes' trees and did not `find`/`du`
anywhere under `/fast/scratch` outside my own `$S`.

## 3. Lane status outside `.ufo/waves/round-39/w2/`

```
HEAD = e40a25df3987d881513de581112d2dad30605673
 M .ufo/waves/round-39/w1/R39C1IndepReader.md
 M .ufo/waves/round-39/w1/R39C1SymlinkK1K4.md
 D .ufo/waves/round-39/w1/artifacts/R39C1SymlinkK1K4/evidence/carrier.sqsh
 M .ufo/waves/round-39/w1/artifacts/R39C1SymlinkK1K4/symlink-tables.py
?? .ufo/waves/round-39/w2.ready            (L1 dispatch marker — expected)
?? .ufo/waves/round-39/w2.ready.dispatched (L1 — expected)
```

(F2 detail.) Freeze commit is `2026-10-26T14:12:51-03:00`; the three modified files carry mtimes
14:13:51, 14:14:45, 14:13:30 — **after** it — and `git log -1` for each still resolves to
`8fcda41c`. The content added is substantive, not cosmetic: an interpreter-version pin for the
symlink-cycle class ("under an interpreter whose `Path.resolve()` raises … the same link becomes
`escaping`/no-gap — so the freeze should pin that runtime"), a chain-resolving `classify()`
signature change (`classify(rel, target, links)`, `+8/-1`), and a retraction of the
"K5/K6 must be chain-free" requirement. The deleted file is the 365-byte BE v4 dev carrier
(`dev3-loop` family); blob `49f56151` is still in git (`git cat-file -s 49f56151` → 365), so it
is recoverable.

Impact: two readers get two evidence sets — a checkout of `HEAD` shows the older, weaker w1 text,
while the working tree (what wave-2 seats read) shows the corrected one; the w1 artifact dir on
disk is no longer the committed set. This is **not** frozen-predicate drift: for
`.ufo/waves/round-39/c1/carriers.json`, both `oracle.tsv`, both `symlinks.tsv` and both
`carrier.sqsh` the blob id is `SAME` freeze vs `HEAD`, and
`git status --porcelain -- .ufo/waves/round-39/c1 corpus/evidence/round-39/c1` is empty. On-disk
`sha256sum` of the K5/K6 carriers equals the `carriers.json` pins (`5999eafc…b228`, `00152518…b25b`).
Smallest remediation: commit the three corrections (or revert them) and restore `carrier.sqsh`
from blob `49f56151` before wave-2 scoring is frozen.

## 4. Secrets scan — CONFIRMED clean

Patterns (`ghp_`, `github_pat_`, `sk-ant-`, `AKIA`, `xox[abpsr]-`, `npm_`, `-----BEGIN … PRIVATE
KEY-----`, `op://`, `Authorization: Bearer …`, `(API_KEY|TOKEN|SECRET|PASSWORD)=…`) run over
`git grep <rev> -- corpus/ .ufo/waves/round-39/ SKILL.md PROVINCE.md tools/round-38/ tools/round-39/`
for `8fcda41c`, `6fdaf4f1`, `52b0eb29`: **0 hits**. Same patterns over the w1+w2 working trees
(including every artifact): **0 hits**. Credential-path scan (`.ssh/`, `id_rsa`, `id_ed25519`,
`.netrc`, `.aws/credentials`, `.gnupg`, `.config/gh`, `.docker/config`, `.npmrc`,
`.git-credentials`, `.pypirc`): **0 hits**.

The only secret-shaped lines in the round-39 tree are `w1/R39Sentinel.md:64-70`, which quote the
wave-1 seat's own grep pattern and its "ZERO" context — self-referential, no credential. Not a
secret but worth knowing: the committed C1/C2 receipts embed absolute scratch paths
(`/fast/scratch/hyaku/kaidoku-r39/l1/c1runs/K5-scratch/rea-firmware-…/extracted/…`), i.e. the
evidence points at a tree outside the lane that must still exist for a replay
(`/fast/scratch/hyaku/kaidoku-r39/l1/c1runs` was present at 14:36).

Only passwd-shaped bytes in round-39 evidence: `printf 'root:x:0:0\n'` written by
`w1/artifacts/R39C2ReconClean/build-dev-carriers.sh:49` (also inside its `carriers/b2.sqsh`).
That is an 11-byte fabricated fixture; the host `/etc/passwd` first line is 31 bytes, so it is
**not** host content. No file in the lane matches `^root:\$[0-9]` (no shadow hash lines).

## 5. Escaping symlinks in the K5/K6 `src` trees — CONFIRMED safe as landed

The three links (git mode `120000`, tracked; identical copies also under
`w1/artifacts/R39C1CarrierK5/src` and `…K6/src`, so 6 link files in all):

| path | target | host resolution | target exists |
| --- | --- | --- | --- |
| `K5/src/usr/share/demo/escape` | `../../../../etc/shadow` | `corpus/evidence/round-39/c1/K5/etc/shadow` | no |
| `K6/src/data/escape-deep` | `../../../../etc/passwd` | `corpus/evidence/round-39/etc/passwd` | no |
| `K6/src/outside` | `../outside` | `corpus/evidence/round-39/c1/K6/outside` | no |

Depth accounting: 4×`..` from `usr/share/demo` (3 components) lands **one level above** the tree
root; from `data` (2 components) it lands **two levels above** it. In-image the same arithmetic
puts the target above the image root, which is exactly why they are `escaping` (K5 1, K6 2), and
why on the host the resolved path is inside the lane and absent — `cat`/`ls -L` on them fails
`ENOENT` here.

Lane-wide audit of **all 20** tracked symlinks (`git ls-files -s` mode `120000`, `os.path.realpath`):
18 resolve inside the lane; **2 escape the lane** — `.ufo/waves/arc3-loop1-round4/claims/c3/EX-25/fixtures/scratch/alias-{1,2}.conf`
→ `/var/tmp/ex25-r4/…` (pre-round-39 residual absolute links, dangling today; flagged as adjacent
residue, no round-39 path involved). 11 of the 20 have missing targets, all dangling by design
(oracle/escape fixtures).

No lane tool or hook follows them:

* **Hooks**: `.git/hooks` holds only `*.sample`; `git config --get core.hooksPath` is empty.
* **Generators/readers**: `grep -rn -E 'copytree|followlinks=True' tools/` → none.
  `tools/round-39/gen-squashfs.py:70-81` walks with default `followlinks=False` and, for a link,
  stores `os.readlink(p)` text only — it never opens the target. `tools/round-39/c1-run.sh:166-179`
  walks the **extraction** root with explicit `followlinks=False` and calls `os.path.exists` only on
  lexically in-tree resolved paths. `sqfs-triage.py`/`c1-counter.py` read receipts/oracles, never
  the `src` trees.
* **Clone**: `git clone -q --shared` into scratch reproduces the links byte-exact as links, their
  resolution stays inside the clone and is absent (`…/clone/corpus/evidence/round-39/etc/passwd`
  → `exists: False`), clone status clean (0 lines).
* **REA/unblob**: receipts show the links are removed, never published. K5 publishes 10 files
  (none named `escape`/`link*`/`outside`), 1× `MaliciousSymlinkRemoved`, gaps only for the two
  in-tree symlinks (`unpublished-entry`); K6 publishes 8 files, 2× `MaliciousSymlinkRemoved`
  (`data/escape-deep`, `outside`), gap only for `a/b/link-in`. In the source tree the generator's
  own dev probe (`w1/artifacts/R39C1CarrierK5/dev-probe.txt`) records
  `Path traversal attempt through symlink, removing … target=etc/shadow`.
* **Nothing copied from the targets**: no `/etc/shadow` hash line anywhere in the lane (the only
  passwd-shaped bytes are the fabricated fixture in §4), and the two escapes' host paths do not
  exist. `/etc/shadow` is `mode=600 owner=root` — `head -c 20 /etc/shadow` as `vgpnk` fails
  `Permission denied`, so even a follower could not exfiltrate it.

(F4 hazard, measured.) Safety here is a function of the *copy depth*, not of the target string:

```
# A. cp -a of the whole tree — inert (copy root $S/K6src, link dir $S/K6src/data)
realpath: /fast/scratch/hyaku/etc/passwd   exists: False

# B. a BARE link lifted into a depth<=3 dir (what `cp -a <link> /tmp/` does)
cp -a K6/src/data/escape-deep /tmp/sent-probe-$$/passwd-link
passwd-link -> /etc/passwd   exists: True   READABLE: 64B sample sha256[:16]=7092cbe64ac6f123
cp -a K5/src/usr/share/demo/escape /tmp/sent-probe-$$/shadow-link
shadow-link -> /etc/shadow   exists: True   read error: PermissionError Permission denied
```

So a future tool that lifts a single link (or copies a tree to `/x`, depth 1) turns K6's link into
a real `/etc/passwd` read; K5's can never yield content. Smallest remediation, no re-freeze
needed: record next to the K5/K6 pins that these trees must only be copied whole (`cp -a` of the
tree, never a link in isolation), or re-target the escapes at paths that cannot name `/etc`
(e.g. `../../../../no/such/shadow`) — the image-level class and every receipt stay identical
either way, because unblob removes the link on lexical escape, not on target existence.

## Artifacts

`.ufo/waves/round-39/w2/artifacts/R39W2Sentinel/`

| file | content |
| --- | --- |
| `01-fleet-root-status.txt` | fleet `git status`, the stray dir tree, file stat + head, missing lane copy, `.gitignore` rules, dispatch Report-path statistics |
| `02-lane-status.txt` | lane status/diffstat outside `w2`, w1 mtimes vs freeze time, deleted-blob id, seat-vs-report snapshot |
| `03-scratch.txt` | `/fast/scratch/hyaku/kaidoku-r39` counts, gen.\* ages, non-gen entries |
| `04-secrets.txt` | every scan pattern and its (empty) hit list, credential-path scan, self-referential hits, passwd-byte provenance |
| `05-symlink-audit.txt` | all 20 tracked symlinks with host resolution, hook surface, dereferencing-primitive grep, generator/reader source excerpts |
| `06-escape-probes.txt` | depth-preserved vs bare-link probes, `/etc` permissions, shared-clone test, K5/K6 receipt published-file/gap/diagnostic tables |
| `07-frozen-index.txt` | blob identity freeze→HEAD for the frozen seven, additions-only diff, empty working-tree drift, on-disk pins |
| `08-w1-drift-diff.txt` | full uncommitted w1 diff, last-commit per path, deleted blob size |

## Tooling, limits, and bounds

* No tool installed, upgraded or moved (no pacman — host-wide pause respected — no uv, no npx
  install; `npx -y rea-agents@6.5.0` was **not** run by this seat: no REA extraction was needed
  for a seam check). Binaries used: `git` (read-only: status/show/log/diff/ls-files/rev-parse/
  cat-file/grep/clone), `python3`, `sha256sum`, `stat`, `grep`.
* VCS untouched: no add/commit/checkout/reset/stash/pull/push, no mutating `jj`. The one clone is
  `git clone -q --shared` inside my scratch.
* Writes: this report and `.ufo/waves/round-39/w2/artifacts/R39W2Sentinel/` only. Scratch
  `/fast/scratch/hyaku/kaidoku-r39/R39W2Sentinel` removed at exit; the `/tmp` probe used
  `<1 KB` and was removed in place.
* Limits: peers were still running (19 lane reports / 26 artifact dirs of 39 seats at 14:36), so
  F1's "missing lane copy" is a state observation at 14:36:56/14:38:42, not a final census; a
  later lane copy of `R39W2HeldReproB.md` would supersede it. Fleet-root `git status` is a live
  signal (the goal file is being edited by the orchestrator). The receipt scratch paths in §4
  were spot-checked for existence, not walked.
* `[INFERENCE]` markers: (a) that **HeldReproB's** report came from a fleet-root cwd is inference
  from the split artifact/report locations and the dispatch statistics — its transcript was not
  read (the mechanism itself is now measured, see §1); (b) "no lane tool follows" is established for `tools/` and for
  the hook surface, not for every interactive shell any seat may type into.
* Report: `.ufo/waves/round-39/w2/R39W2Sentinel.md`
