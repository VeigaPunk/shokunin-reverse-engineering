# EX-38 — probe interplay: citation-drift probe at HEAD after EX-31

Seat EX-38 · chain c3 · role executor · wave arc3-loop1-round2 · 2026-10-19.
Seat task: after EX-31 (the designated C3 implementer) lands `.ufo/gates/custody-pair/`,
run the citation-drift probe at HEAD → the verdict must read `findings=0`; and the
new files' paths must not resemble pinned citations.

All commands below were run from the repo root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` unless a `cd` is shown. Scratch
lives under `/var/tmp/ex38` (never `/tmp`: EDQUOT hazard, `SCORECARD.md:990-991`).
No git mutation ran in the real repo; the only `git add/commit/checkout` calls
were inside throwaway clones under `/var/tmp/ex38/`.

## 0. Verdict

**Both halves of the seat line are delivered on the landed bytes.**

- **Probe at HEAD after EX-31 → `findings=0`.** Real repo, HEAD
  `14b1682b1128d2e41085ebc79c9addeb8786d420`, EX-31's files in the worktree:
  `CITATION_DRIFT_VERDICT: reported findings=0 exit=0` (default probe semantics)
  and `clean findings=0 exit=0` (`--strict`); selftest 13/13. Same verdict in the
  recipe-A harness form (`--root . --rev HEAD`). Evidence:
  `after-probe-mode.txt`, `after-probe-strict.txt`, `after-probe-recipeA.txt`,
  `after-probe-selftest.txt`.
- **The new paths do not resemble pinned citations.** 30 new paths (the
  custody-pair gate dir, two files, + EX-31's 28 artifacts) tested against the
  probe's 17 needle files: **0 hard findings (R1/R3)**; 1 advisory (R2, basename
  `README.md` vs pinned `corpus/README.md`) — semantics and adjudication in §4.
  Evidence: `resemblance-real.txt`, tool `path-resemblance-check.py`.
- **Why, in one line:** the probe resolves *Git objects at `--rev`* and only ever
  reads the 17 files named in its pointer table; none is under `.ufo/gates/`, so
  the new directory is invisible to it by construction. The check is made
  non-vacuous by a teeth control that fires 9 findings on a one-line insertion
  (§6). Because the read path is `--rev`-bound, the load-bearing measurement is
  the scratch-clone simulation that *commits* EX-31's final bytes (§5).

## 1. Instrument state pinned (sha256)

| file | roll-1 landing (unchanged) | at this seat's close |
|---|---|---|
| `.ufo/gates/citation-drift/pointer-table.json` | `738b3a569fb7…` | `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f` (byte-stable) |
| `.ufo/gates/citation-drift/expected.json` | `ff47bfd60b38…` | `ff47bfd60b383c22c0897e8c89081dd738f67d7f28904292c47f5d09e4173ba7` |
| `.ufo/gates/citation-drift/citation-drift-probe.py` | `e2665074a685…` | `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a` |
| `.ufo/gates/custody-pair/custody-pair.py` (new) | — | `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` (889 lines, 39157 B, mtime 09:05:19 -0300) |
| `.ufo/gates/custody-pair/README.md` (new) | — | `fa484d573b0debb0d2ed134d076cb9593e7c3ee910ad4487d99cb9f3a8239bba` (6180 B, mtime 09:07 -0300) |

The gate dir ships **exactly those two files** at close (EX-31 removed its own
`__pycache__` residue; this seat re-verified with `find … -type f` → 2 paths).

**Mid-wave revision, recorded per the C1 rule-14 discipline (identity
re-derivation).** EX-31's tool was rewritten while this seat measured it:
`9aad4c5a…` (883 L, 09:03:47) → `887 L` → **`112d01dc…` (889 L, 09:05:19)**.
This seat's first captures were superseded; every number quoted here was
re-derived against the final bytes (`new-paths.txt`, `resemblance-real.txt`
carry the post-close re-derivation timestamp `2026-10-19T12:14:16Z`;
`landed-state.txt` holds the state capture and the mid-wave pyc observation).
The simulation in §5 grades the byte-exact final blob (checked:
`git show ff78ece:…custody-pair.py | sha256sum` = `112d01dc…`, re-checked at
`9c593c1`).

## 2. Before → after

Before EX-31 (this seat's baseline, 12:0xZ):
```
CITATION_DRIFT_VERDICT: reported findings=0 exit=0        (base-probe-mode.txt)
CITATION_DRIFT_VERDICT: clean findings=0 exit=0           (base-probe-strict.txt)
CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0   (base-probe-selftest.txt)
```
After EX-31 landed: identical — `reported findings=0 exit=0`, `clean findings=0
exit=0`, selftest 13/13, table byte-identical (`738b3a56…`). The before→after is
therefore **0 → 0**, which on its own is weak evidence (see A1/A4 in §7); the
discriminating evidence is the committed-bytes simulation (§5) and the teeth
controls (§6).

## 3. Why 0 findings — three isolation channels (measured, not assumed)

1. **Target-set disjointness.** The probe's needle set — extracted mechanically
   from `pointer-table.json` (`entries` + `quoted`, citing files + non-`@`
   targets) — is **17 files** (`needle-targets.txt`), none under `.ufo/gates/`:
   `LOG.md PROVINCE.md SCORECARD.md SHONEN.md SKILL.md corpus/{QUALITY,README}.md
   corpus/knowledge/2026-10-13-mcp-registrations.md
   corpus/knowledge/2026-10-13-r4-12-godot-arm64-scale.md
   corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md
   corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md
   corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md corpus/lessons/2026-10-15-round-1.md
   evidence/round-1-2026-10-15/rea-bundle.json
   .ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt
   .ufo/waves/arc2-loop1-round8/E2.md
   .ufo/waves/arc2-loop1-round8/receipts/r8-ctl-envelope.json`.
   Nothing in EX-31's write target intersects it; the census instrument likewise
   never names `.ufo/` or `gates` (`grep -n "gates\|\.ufo/" .ufo/gates/c1-census-v10.py`
   → no output).
2. **Line-shift isolation.** Needle staleness needs an edit *inside a pinned file
   at or before a pinned line*. The new files are additions in a new directory;
   no pinned file's bytes moved (worktree `git status` shows only the pre-existing
   `M .ufo/waves/arc2-loop1-round10/C3.md` plus untracked wave trees).
3. **Read-path isolation (with its cost stated).** The probe reads targets as Git
   objects at `--rev` (`citation-drift-probe.py:100` `git_show`, `:125`
   `Tree.lines`, default `--rev HEAD` at `:477`). Seats never commit, so the
   literal "probe at HEAD" run cannot see worktree-level new files *at all* —
   trivially green by construction. That is why §5 commits the final bytes in a
   scratch clone and grades that revision; the 0-findings result survives where
   the new files *are* objects in the graded tree.

## 4. Path resemblance — "the new files' paths must not resemble pinned citations"

Tool: `path-resemblance-check.py` (this seat). Classes are exact string tests;
no fuzzy matching:

| class | test | severity |
|---|---|---|
| R1 exact-path identity | `new == needle` | **HARD** (the probe would grade the new file as the pinned artifact) |
| R3 suffix identity on a multi-segment tail | `new.endswith("/"+needle)` or vice versa, tail containing `/` | **HARD** (a path-suffix matcher or a human reader could conflate them) |
| R2 basename collision | `basename(new) == basename(needle)`, different dir | advisory (naming hygiene) |
| R4 same-directory adjacency | dirname equality | informational |

Result on the real landing (30 new paths, re-derived 12:14:16Z, after EX-31's
close removed its `__pycache__` residue):
```
RESEMBLANCE: R2 new=.ufo/gates/custody-pair/README.md needle=corpus/README.md (same basename, different directory)
RESEMBLANCE_SUMMARY: new_paths=30 needles=17 hard_findings=0 (R1/R3) advisory=1 (R2) informational=0 (R4)
exit=0
```
(`resemblance-real.txt`.) The single advisory is **adjudicated benign**: the new
file is a tool README inside C3's own write target; the pinned `corpus/README.md`
is a different artifact whose basename is generic. Nothing resolves the bare
string `README.md` as a citation.

Controls proving the tool's classes are not inert (`resemblance-positive.txt`,
`resemblance-negative.txt`):

- Positive control (constructed collisions): `.ufo/gates/custody-pair/PROVINCE.md`,
  `.../nested/SKILL.md`, `.../receipts/config-pre-pair.txt` → 4× R2, and
  `.../mirror/.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt` → **R3**
  (hard, exit 1).
- Negative control: a proposed `custody-pair/README.md` reproduces the advisory
  (documented over-fire), and `custody-pair/receipts/r2-pre.txt` is clean.

**Content dimension (same question, one level down).** Are there citation-shaped
tokens inside the new files? `grep -rnoE '[A-Za-z0-9_./~-]+\.(md|json|toml|sh|py|txt|out):[0-9]+'`
over `.ufo/gates/custody-pair` + `claims/c3/EX-31` → **0 hits**; bare
`config.toml:<N>` live-pointer tokens (the probe's declared defect class) → **0
hits**. The only needle-adjacent strings are basename mentions:
`config-pre-pair.txt` in `custody-pair/README.md:103`,
`label-defect-regression.out`, `verify-v1-stanza-vs-live.out`; and `README.md`
inside EX-31's `sha256s.txt`. Each `config-pre-pair.txt` mention refers to the
**round-1 arc3 receipt**
(`.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt`, exists
— verified), **not** the pinned arc2-round3 file of the same basename. No
full-path occurrence of any needle appears in any new file. Verdict: no
citation-shaped content in the new surface; the basename reuse is pre-existing
round-1 material, not introduced here.

## 5. Committed-bytes simulation (the load-bearing run)

Scratch clone `/var/tmp/ex38/clone2` (base `14b1682`), EX-31's final bytes and
its artifacts committed (all git mutations confined to the clone):

| rev | shape | probe `--strict` |
|---|---|---|
| `ff78ece` | + `custody-pair/{custody-pair.py,README.md,__pycache__/*.pyc}` + `claims/c3/EX-31/` + `claims/c3/EX-38/` (37 files) | `clean findings=0 exit=0` |
| `044844a` | + records-style EOF appends to `SCORECARD.md` and `LOG.md` (simulating the parent's records shape) | `clean findings=0 exit=0` |
| `ca44997` | teeth insert reverted (clone hygiene) | `clean findings=0 exit=0` |
| `33ea3c1` | **teeth**: one line inserted at the top of `SCORECARD.md` | `failed findings=9 exit=1` |
| `9c593c1` | **post-close exact shape**: gate dir re-copied as the final 2 files (the pyc staged as a deletion) + refreshed EX-31/EX-38 artifacts | `clean findings=0 exit=0` |

Transcript: `sim-transcript.txt`; default-mode runs of the same revisions agree.
The committed blob faithfulness is verified (§1). Conclusion: with EX-31's new
files as *committed objects in the graded tree*, the probe stays at 0 findings;
appends at EOF do not move pins; insertion does (teeth, §6).

## 6. Teeth — would this check have caught a real staling?

- **T1 (probe teeth, current bytes):** one inserted line at the top of
  `SCORECARD.md` (clone rev `33ea3c1`) → **9 findings**, exit 1 — entries
  `sc59-stanza-key-anchor`, `sc59-receipt-stamp`, `sc68-discharge-record`,
  `sc69-readme-177`, `sc72-readme-nitrow`, `sc270-dated-record`,
  `sc698-sc2-refuted-record`, `readme175-sc1217`, `sc622-capability-r8`
  (`teeth-scorecard-insert.txt`). The r10 lesson's own needle is among them.
- **T-R1 (the exact boundary this seat guards):** a *new file landing on a pinned
  needle path* — clone rev `1c90983`, line 1 of
  `.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt` replaced — fires
  `CITATION_DRIFT: citation_dead entry=prov18-receipt-exists … lacks
  '^2026-10-18T17:55:49Z$'`, `failed findings=1 exit=1`. So: disjoint new paths
  are invisible; an R1-class collision would be caught by the probe itself. The
  check is not vacuous, and the R1/R2/R3 separation in §4 is the right boundary.

## 7. Attacks / refutations attempted

- **A1 "run-the-probe-after-EX-31 is trivially green and proves nothing."**
  PARTIALLY TRUE — accepted and mitigated, not papered over: the `--rev`-bound
  read path (§3.3) makes the literal worktree run insensitive; §5's committed-
  bytes simulation plus §6's teeth are what carry the claim.
- **A2 "new paths could collide silently."** REFUTED at the boundary by T-R1:
  a collision at a needle path fires, and the resemblance tool reports R1/R3
  before anything lands.
- **A3 "the resemblance checker is a handmade regex ready to over-fire."**
  PARTIALLY TRUE, measured: R2 fires on the benign `README.md` basename reuse
  (`resemblance-negative.txt`) — R2 was therefore demoted to advisory and R3
  tightened to multi-segment tails during this seat (first draft counted any
  basename tail as R3; the revision is visible in the tool's docstring).
- **A4 "appends at EOF could still stale something."** REFUTED: `044844a`
  (SCORECARD + LOG EOF appends) → 0 findings. Note the asymmetry: the *census*
  (C2's instrument) is the one that is not append-tolerant; the probe is.
- **A5 "EX-31's receipts might emit citation-shaped tokens that a later records
  section pins."** MEASURED, negative: 0 `path:NNN` tokens and 0 bare
  `config.toml:<N>` tokens anywhere in the new surface (§4).
- **A6 "the new files could have moved the probe's frozen-run pin (table
  digest)."** REFUTED: `pointer-table.json` is byte-identical (`738b3a56…`) in
  the real repo and in every simulation revision.
- **A7 "the new `README.md` cites pinned files, so the interplay is not
  disjoint."** CHECKED on bytes: its three path references were each verified to
  exist; all are line-number-free (nothing can go stale), none is a needle path,
  and the shared basename `config-pre-pair.txt` resolves to a different, existing
  round-1 file (§4). No needle is staled.

## 8. Residuals and flags for the parent (not this seat's to fix)

1. **`__pycache__` class (resolved in the target, still live elsewhere)**: EX-31
   removed its own residue at close — the gate dir now ships exactly
   `custody-pair.py` + `README.md` (re-verified: `find … -type f` → 2 paths, §1).
   The class regenerates whenever a seat *imports* the module (this seat's
   `landed-state.txt` caught the pyc mid-wave: `364adafb…`, 61223 B), and
   `.ufo/gates/__pycache__/c1-census-v10.cpython-314.pyc` (another seat's import,
   mtime 09:06:58) is still untracked. The wave commit should exclude
   `__pycache__/` globally (round-1 precedent: the wave `.gitignore` carries it,
   `CN-1 §5`).
2. **New `README.md` inside `.ufo/gates/custody-pair/`** — two flags, both for
   adjudication, neither a citation defect: (a) the hard rule "NEVER edit …
   README files" — this is a *new* file inside C3's own write target, not an edit
   of an existing repo README; (b) it is the single R2 advisory (§4).
3. **Do not widen the pointer table.** Any records commit that added an entry
   citing custody-pair paths would edit the digest-pinned table; without a same-
   commit re-pin the probe returns `pointer_table_tampered` (exit 2, by design).
   Keep `738b3a56…` and let the parent's records re-run reproduce §5.
4. **EX-31's close is consistent with this artifact** (seat report landed
   ~12:10Z; tool sha `112d01dc…` stable across 6 polls 12:11–12:13Z; artifact
   tree grew to 28 files, all covered by the re-derived 30-path resemblance run).
   If anything in the gate dir changes after this close, re-derive §1/§5 (C1
   rule-14 discipline); the one-command re-run is below.
5. **Re-run at integration**: the parent's real records commit must reproduce
   `findings=0` on the real text (this seat's sims use this seat's snapshot).

## 9. Reproduction (exact commands)

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
# 1. probe at HEAD, three forms
python3 .ufo/gates/citation-drift/citation-drift-probe.py                # reported findings=0 exit=0
python3 .ufo/gates/citation-drift/citation-drift-probe.py --strict       # clean findings=0 exit=0
python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest     # cases=13 passed=13 failed=0
python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD   # recipe-A form
# 2. needle set + resemblance
find .ufo/gates/custody-pair .ufo/waves/arc3-loop1-round2/claims/c3/EX-31 -type f | sed 's|^\./||' > /var/tmp/new-paths.txt
python3 .ufo/waves/arc3-loop1-round2/claims/c3/EX-38/path-resemblance-check.py \
  --table .ufo/gates/citation-drift/pointer-table.json --paths-file /var/tmp/new-paths.txt
# 3. committed-bytes simulation (scratch clone; the sim's revisions are disposable)
git clone -q --no-hardlinks . /var/tmp/ex38/clone2 && cd /var/tmp/ex38/clone2
mkdir -p .ufo/gates/custody-pair && cp -a <repo>/.ufo/gates/custody-pair/. .ufo/gates/custody-pair/
git add -A .ufo/gates/custody-pair && git -c user.email=e@x -c user.name=e commit -qm sim
python3 .ufo/gates/citation-drift/citation-drift-probe.py --rev HEAD --strict   # clean findings=0
```

Scratch `/var/tmp/ex38` (two clones, ~90 MB each) removed at seat close; all
quoted outputs are committed under `claims/c3/EX-38/`.
