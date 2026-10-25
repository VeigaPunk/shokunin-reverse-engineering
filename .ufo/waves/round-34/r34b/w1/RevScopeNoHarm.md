# RevScopeNoHarm — R34-C2 scope and no-harm audit (r34b/w1)

Seat: `L1Kaidoku34-2.RevScopeNoHarm`. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Range audited: `f432c8e3` (inherited tip) → `c79bbe7b0959132b9873ff3431cf5eb313b58b33` (freeze).
Mode: read-only. No VCS mutation, no gate/counter/reader execution as a program of interest,
no pacman, no tool installs (`uv`/`npx`/`~/.local/bin` untouched — nothing was needed).
UTC window of this audit: 2026-10-25T07:18:14Z … 2026-10-25T07:22Z.

## Verdict

**SCOPE_CLEAN / NO_PREEXISTING_HARM** — the freeze commit is 27 additions, 0 deletions,
0 modifications, 0 renames, confined to `tools/round-34/**` (26 paths) and
`.ufo/waves/round-34/**` (1 path); `SCORECARD.md`, `LOG.md`, `SKILL.md`, `PROVINCE.md` and
`corpus/**` are byte-identical at both tips. Three defects found, none of them a scope breach:
F1 is a falsified claim-level identity assertion, F2/F3 are evidence-integrity gaps. No finding
falsifies any of the six scored gate clauses.

## 1. Per-file diff (all 27 paths, `A` = added, git mode, committed bytes)

`git -C <lane> diff --name-status f432c8e3 c79bbe7b` → exit 0, 27 lines, all `A`.
`git -C <lane> diff --shortstat f432c8e3 c79bbe7b` → `27 files changed, 1345 insertions(+)`.
Status-letter histogram: `27 A` (no `M`, `D`, `R`, `C`, `T`).

| # | path | mode | bytes |
|---|---|---|---|
| 1 | `.ufo/waves/round-34/r34b/claims.json` | 100644 | 6999 |
| 2 | `tools/round-34/c2-shortcut-gate-counter.py` | 100755 | 6911 |
| 3 | `tools/round-34/gate-config-mini.json` | 100644 | 1273 |
| 4 | `tools/round-34/gate-config-naive.json` | 100644 | 1274 |
| 5 | `tools/round-34/replay-gate.py` | 100755 | 14902 |
| 6 | `tools/round-34/mini-fix/build.py` | 100755 | 3369 |
| 7 | `tools/round-34/mini-fix/expected.json` | 100644 | 2065 |
| 8 | `tools/round-34/mini-fix/spec.json` | 100644 | 1385 |
| 9 | `tools/round-34/mini-fix/mini-counter.py` | 100755 | 6429 |
| 10 | `tools/round-34/mini-fix/naive-counter.py` | 100755 | 2835 |
| 11–18 | `tools/round-34/mini-fix/fixtures/{alpha,beta,delta,epsilon,eta,gamma,theta,zeta}.mrec` | 100644 ×8 | 512 ×8 |
| 19–26 | `tools/round-34/mini-fix/readers/{all_false,digest_keyed,fixed_slice,label_keyed,label_replay_full,record_order_replay,size_keyed,string_scan}.py` (eight shortcut readers) | 100755 ×8 | 168…2320 |
| 27 | `tools/round-34/mini-fix/readers/structural.py` (positive control) | 100755 | 943 |

Binary paths: exactly the eight `.mrec` fixtures (`git diff --numstat` rows `- -`); text
insertions 1345 (`awk '$1!="-"{s+=$1}'`). No symlink entries (`120000` count 0).
`git diff --check f432c8e3 c79bbe7b` → exit 0 (no whitespace/conflict artifacts).

## 2. Deletions and pre-existing content

Two independent proofs, both empty:

- `git diff --diff-filter=MDRTC --name-status f432c8e3 c79bbe7b` → exit 0, **no output**.
- Tree set difference over `git ls-tree -r --name-only` (LC_ALL=C `comm`):
  `REMOVED_COUNT=0`, `ADDED_COUNT=27`; tree blob count 22866 → 22893 (+27 exactly).
- `git diff --stat HEAD` on the whole lane worktree → exit 0, **no output**: no tracked file
  is modified or missing relative to the freeze.
- Prior-round instruments are blob-identical at both tips:
  `tools/round-34/elf-version-needs.py` `f69688ed…`, `tools/round-34/version-needs-counter.py`
  `ac89ecd0…`, `tools/round-34/freeze-integrity.py` `c2c4798b…`; base tree at `f432c8e3`
  holds exactly those three files under `tools/round-34`.
- R34-C1 binding record unchanged: `.ufo/waves/round-34/claim-stop.json` =
  `9e487015544013919b190a2a43e9dd596d301bf7` at **both** tips.
- No R34-C1 reader or carrier was executed by this seat (constraint honoured; nothing named
  carrier appears in the changeset at all).

## 3. Scope containment

- Commit-scope: `26` paths `^tools/round-34/`, `1` path `^\.ufo/waves/round-34/`, and
  `0` paths outside those prefixes (`git diff --name-only | grep -Ev …` → empty).
- 27 pins + `claims.json` = the exact changeset. All 26 pinned paths were re-hashed by me
  against the **committed** `c79bbe7b` blobs (`git cat-file blob` → sha256): `26/26` match,
  0 mismatches. Pins therefore bind the frozen bytes, not a staged copy.
- Worktree == HEAD for the whole lane (`git diff HEAD` empty). `git status --porcelain` in the
  lane lists **only** untracked `?? .ufo/waves/round-34/r34b/**` entries (receipts, prompts,
  payload/seat-map/spec, assimilation scratch) — every one inside the allowed prefix.
- Gitignored writes cannot hide: `.gitignore` contains only `__pycache__/` and `*.pyc`
  (`--ignored=matching` shows only `.jj/…`). A lane-wide `find . -newermt <freeze cI>`
  (excluding `.git`, `.jj`) returns 64 paths, **all** under `.ufo/waves/round-34/r34b/`;
  `corpus/**` newer files: `0`. No file outside the two allowed prefixes was created or
  rewritten after the freeze.

## 4. Docs unchanged (as of this audit)

Blob-id equality at `f432c8e3` vs `c79bbe7b`:

| doc | blob | state |
|---|---|---|
| `SCORECARD.md` | `e2c82c1d1facca2f67f25e216dd9eff1bce68d11` | SAME |
| `LOG.md` | `2b3d2b23348ffa6692070795baa398d95e25cf26` | SAME |
| `SKILL.md` | `d9dd15fcf83a1463093c5000ce04f7020d741abb` | SAME |
| `PROVINCE.md` | `d453a29ddeb6e6a48bc59ccb863d7fff24c08f6f` | SAME |

`git diff --name-status f432c8e3 c79bbe7b -- corpus/` → empty. Lane doc mtimes remain
2026-10-23 (SCORECARD 08:07:02 -03, LOG 08:06:39 -03, SKILL 08:10:59 -03, PROVINCE 04:02:18 -03),
i.e. untouched since round-33 work, consistent with "doc drafts only, L1 lands them".

## 5. Findings

### F1 — HIGH (claim-level honesty, frozen assertion false at the freeze): `predicate_identity` is false as written

`claims.json` `predicate_identity` asserts: *"The same sentence is the gate config's
`predicate` field, the C2 counter's PREDICATE constant and the receipt label."* Two distinct
sentences carry the label. Verified by exact string compare:

- **A** (length 237) — `claims.predicate` == `gate-config-mini.json predicate` ==
  `gate-config-naive.json predicate`: `"P34-shortcut-replay: a finite structural-decoding
  counter is frozen only after registered structure-blind shortcut readers are scored under the
  counter's own predicate and none meets the target, while a registered structural reader does."`
- **B** (length 351) — `c2-shortcut-gate-counter.py:23 PREDICATE` ==
  `.ufo/waves/round-34/r34b/after/c2-at-instruments.json .predicate`, beginning
  `"P34-shortcut-replay: the committed replay gate refuses the shape-only counter whose
  label-keyed memorization meets its target, …"`.

Receipts: `receipt == counter PREDICATE literal (B): True`, `config == claims (A): True`,
`A == B: False`. Command: python3 re-parse of the file + ast/regex literal concatenation,
exit 0.

Impact, stated precisely: the *operational* clauses are unaffected — the gate evaluates the
config predicate (A) and the counter emits (B) as its receipt label, and `evaluate()` never
compares the two. What is false is the frozen identity claim itself. It must be reported as a
miss on the `predicate_identity` sub-assertion, **not** silently re-worded before landing
(the kill rule forbids post-freeze predicate edits). For other seats: this intersects
`RevPredicateIdentity`; my evidence is static and independent of that seat's run.

### F2 — MEDIUM (evidence integrity): receipts are untracked and unpinned

`claims.json` pins 26 instruments but only *names* `after_receipt`
(`after/c2-at-instruments.json`); no receipt digest exists in the claim or in the commit
(`grep` for a receipt hash field → none; the only matching key is the path `after_receipt`).
The gate/counter bytes are therefore immutable by hash while the documents that carry the
verdict are ordinary untracked files with no VCS trace, rewritable without detection.
Digests captured now, so the L1 can pin them at landing:

```
da78f44419ecf83935e1fe6b1cd72f611c5a0e7e03029e97580d515a0796f3e9  after/c2-at-instruments.json
378f1b5e35751839e9be9bcd7880b01eadeecfc3c5fc247c86346ba9a3d786e0  after/c2-at-instruments.txt
b512cfc25d401c31a16dd4a4dd977a19c7252fd6b4a4d26f56af2de73bc19c2b  before/c2-at-base.txt
bce6aa9febd85aa8f61c398c144ca987b05bdd2f96582ba3291738251b138097  controls/do-nothing.json
22f819c4bf421466fdb2f961837823ed7273976d5d0690423fd71d9df44c894f  controls/gate-always-clean.py.json
25485cb94137dd982e1dd5e7554651f4ae7d4fafba12e59ec67c8f5d66a19165  controls/gate-junk-clean.py.json
50516d79c0bc899734a7a2a100016be00e30cda352554ef7888f050b1cc02266  controls/gate-no-positive-check.py.json
a12f720dee315541b17d3c50888804a154fb91af3778ebc949777199d347b040  controls/gate-vacuous-no-floor.py.json
dc9cde99590debd500e76d75f56cacacc96085097fb9a0bcecadf6a716d39429  controls/do-nothing.txt
33b667a5b9e929e3a7dfffc951fd3e74f5f16a6e2312be9ff56e863b7e7d54e4  controls/gate-always-clean.py.txt
a4ac1d8ff677c438eab00caf1d6f657880b4401a80928b87fd46129483a5bc74  controls/gate-junk-clean.py.txt
f8da2041bd2c7306275b70f8da45e67f01760e85da16d4c14887261514b5e15d  controls/gate-no-positive-check.py.txt
3bdd79752b166b1e2c405a34bf033bb4ded9900c7c561ea3c1aafd96e0884280  controls/gate-vacuous-no-floor.py.txt
```

### F3 — LOW (provenance): the "before" receipt was measured at a revision other than the inherited tip

`before/c2-at-base.txt`: `GATE_COUNTER_UNEVALUABLE finding=gate_absent
measured_revision=ec3125ad3d130d92f888a4128dfaa2982f36fff7 gate_path=tools/round-34/replay-gate.py`.
`ec3125ad` is the round-33 tip (`round-33 verifier spot-check (integrator, hyaku)`,
2026-10-23T07:18:52-03:00), five commits behind `f432c8e3`; `claims.json` discloses both
(`base_revision=ec3125ad…`, `inherited_tip=f432c8e3…`), so the claim is internally consistent,
but the receipt alone does not demonstrate the base state at the tip it inherits.

I closed that gap statically: `git cat-file -e` shows `tools/round-34/replay-gate.py`,
`c2-shortcut-gate-counter.py` and `mini-fix/spec.json` ABSENT at `ec3125ad` **and** at
`f432c8e3`; the `f432c8e3` tree holds only the three prior-round instruments under
`tools/round-34`. The "no replay gate exists at base" claim therefore holds at the inherited
tip too — no scope harm, the receipt is simply not the artefact that proves it.

### F4 — LOW (instrument-set hygiene): the ninth reader is pinned but never registered

`mini-fix/readers/` holds **9** files; both gate configs register **7** shortcut classes plus
the structural positive control (`mini-fix/readers/structural.py`), i.e. 8 readers wired.
`readers/label_keyed.py` (class `label-keyed`) is pinned in `claims.json`
(`f727c152…`) but appears in neither `gate-config-mini.json` nor `gate-config-naive.json`, so
the pinned instrument set is strictly larger than the scored class set.

Not a dropped class, and not a CLEAN-by-omission: its `TEMPLATE` covers only
`alpha.mrec`/`gamma.mrec`, and every row of it is a strict subset of the registered
`label_replay_full.py` (`label-memorization`) template, which equals `expected.json` byte for
byte over all eight fixtures (verified by literal parse). Since the registered, strictly
stronger class is REFUSED by the counter, an unregistered weaker variant cannot meet the
target; `mini-counter.py::permute()` shuffles the name pool, rewrites each `name_off`, and
writes the copy as `opaque-<sha256[:20]>.data`, destroying basename identity. Residual value:
if a later round claims "every pinned reader was scored", that would be false for
`label_keyed.py`.

Related tally note: this seat's brief says "eight readers"; the frozen tree has nine and pins
all nine, while the freeze commit message's "seven shortcut classes" is exactly right for the
configs. Wording of the brief, not of the claim.

### F5 — INFO (containment posture verified, no execution)

- Fixtures: 512 bytes each, magic `4d 52 45 43` (`MREC`), version 1, header `count` equals
  `spec.json` entries and `expected.json` rows for all eight (`ALL_FIXTURES_CONSISTENT True`);
  8 distinct sha256 (no duplicates); mode 0644; no shebang, no ELF, no `\x7fELF` anywhere in
  the changeset (largest blob 14902 B — a Python source, not a carrier).
- 14 of 27 new paths are 100755, matching the lane's existing convention for tool scripts
  (`tools/**`: 61 × 100755 vs 25 × 100644; pre-existing `version-needs-counter.py` is 100755,
  data/config files 100644). Executable bit is house style, not an escalation.
- Readers are `#!/usr/bin/env python3`, stdlib-only imports; `mini-counter.py` invokes them as
  `[sys.executable, "-I", "-B", reader, target]` with `env={"PATH": "/usr/bin:/bin", …}` —
  python-invoked, never executed as a binary. I ran none of them.

### F6 — INFO (outside lane, no content harm)

Fleet-root repo `/home/vgpnk/Projects/shokunin` shows `MANIFEST.json` mtime
2026-10-25T04:18:37-03:00 (after the freeze) but **zero diff against its own HEAD**
(`git diff --stat -- MANIFEST.json` empty, not listed in `git status`), i.e. rewritten with
identical content. Its working tree also carries orchestrator-level churn
(`.ufo/state/*.report-baseline` incl. `kaidoku`, `.ufo/watchdog.log`, `scripts/hyaku/*`) that
is infrastructure, outside this lane, and not attributable to any lane seat from lane evidence.
No lane write reached the fleet root, a sibling lane, `shokuknow`, `~/.omp`, `~/.config` or
`~/.kimi-code` (my only writes: this report + `/fast/scratch/hyaku/kaidoku-r34b/w1/RevScopeNoHarm/`).

### F7 — INFO (dependency, scope-consistent)

`claims.json` lists `sources_opened_this_round: ["S106"]`, but the freeze commit contains no
S106 artefact (`grep -rn S106` over the changeset matches only `claims.json:60`; `corpus/**`
diff empty). The freeze is instruments-only, which is the correct pre-freeze scope; the
consequence is that S106's binding must be supplied by the wave-1 source seat's report, not by
the frozen tree.

## 6. Residual risk and verification gaps

1. **Receipts are static evidence here.** I verified the gate/counter/reader bytes and the
   receipt *contents* (field-level, incl. the six `clauses` and the three control verdicts),
   but did not execute `replay-gate.py`, `c2-shortcut-gate-counter.py`, `mini-counter.py` or
   any reader. Reproduction of the receipt by execution is `ExecRecountC2` /
   `ExecGreenIndependence` / `ExecRedReproduce`; an unfalsified receipt is not an executed one.
2. **F1 is static.** It depends only on file bytes and needs no runtime; still, it is a
   document-level falsifier and should be cross-checked by `RevPredicateIdentity` before the L1
   acts on it.
3. **Attribution limits.** Cross-lane and fleet-root writes (F6) cannot be attributed to seats
   from lane evidence; only the absence of *lane* writes outside the two prefixes is proven.
4. **jj colocation.** I deliberately ran no `jj` command (a jj read can snapshot the working
   copy, i.e. mutate); all VCS evidence is `git` read-only against commits.

## 7. Tooling record

No tool installed, upgraded or removed (no pacman, no `uv tool`, no `npx`, no `~/.local/bin`
change). Tools used: `git` (read-only subcommands), `python3` (`/usr/bin/python3`, static
parsing), coreutils `find/stat/sha256sum/od/comm/awk/cut` — all pre-existing.

VERDICT: SCOPE_CLEAN_NO_PREEXISTING_HARM — 27 additions / 0 deletions / 0 modifications confined
to `tools/round-34/**` + `.ufo/waves/round-34/**`; docs and corpus untouched; 26/26 pins bind the
committed blobs; **F1 (predicate_identity false: sentence A ≠ sentence B) is a frozen claim-level
miss that must be reported, not edited**; F2 (unpinned receipts) and F3 (before-receipt revision)
are evidence gaps I closed or quantified; F4 is inert-instrument hygiene, not a dropped class.
