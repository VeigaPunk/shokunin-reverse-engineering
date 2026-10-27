# R43CritC2 — attack on draft P43-C2 (coverage: 18 host-local SOURCES rows → in-lane copies)

**Verdict: DEFECTS FOUND** — the claim is a genuine coverage move (right axis), and the prepared
round-42 pack demonstrably greens the gate in a fresh clone. But the draft predicate has one
**gate-bypass hole** (symlink copies — measured green), one **fidelity hole** (every failing row
is URL-cell-unpinned, so a shadow copy greens — measured green), one **self-contradicting clause**
("byte-identical … except nothing" vs the S135 append), one **stale denominator** (129 vs measured
134/135), a **rev-binding hole** (the gate reads map and copies from the worktree — measured green
at a rev that contains neither), a **wrong disclosed limit** (`source_sha256` drift hard-fails, not
advisory), a **freeze-rule self-block** (the landing paths are listed as frozen paths), and a
**kill rule that would mis-fire** on the illegitimate greens. Ten concrete predicate changes (P-1…P-10)
are at §7. Nothing proposed touches the frozen gate bytes.

Axes named: **coverage** = the SOURCES registry's citation authority — the set of rows a fresh lane
checkout can resolve to bytes the lane holds; **depth** = not this claim's object (the gate is a
resolver, not a ranking/triage surface); **calibration** = fidelity of self-assessment vs observed
state — relevant only as a *harm* axis here (a green claim whose copies are wrong bytes would be a
false self-report, so the fidelity clauses matter even though fidelity is not the scored surface).

All attacks ran in `--shared` clones under scratch; no lane file was touched. Receipts:
`.ufo/waves/round-43/w1/artifacts/R43CritC2/receipts/`. Gate under test: `tools/round-41/local-source-gate.py`,
sha256 `cafe232a196d…` (unchanged since round-41 freeze `d764389e`; predicate's byte-identity clause verified).

## 0. Baseline reproduced

```
git clone -q --shared <lane> $D/lane            # rev-parse --show-toplevel == $D/lane
python3 -I -B $D/lane/tools/round-41/local-source-gate.py --root $D/lane \
  --rev 6b9e64fe7e0de202d9383baad5792fbfe039a743 --json
# exit 1; rows_total 134; rows_checked 19; rows_failed = the exact 18 of the claim
# map_present: true (base map = the single S126 entry)
```

Receipt: `receipts/ctl-c2-0-gate-at-base.json`. The claim's "18 rows / exit 1 at base" is exactly right.

## (a) Axis fit — coverage, argued both ways

**For coverage (correct reading).** The measured surface is the registry's *citation authority*:
whether a fresh checkout of the lane can resolve each URL cell to bytes the lane holds. Today 18 of the
19 host-path rows resolve only on this host — outside the lane's owned surface. The landing converts 18
citations from "host-resolvable" to "lane-resolvable". That is the coverage axis's object exactly as the
round-42 non-author closure used it (registry growth, knowledge-entry counts, citation resolvability as
coverage evidence). `rows_failed` counts citations lacking an in-lane resolution path — a *resolvability
gap list*, not an error count.

**The calibration steelman.** Prompt §6.9: a calibration claim counts mismatches between a
self-assessment and observed state. The URL cell *is* a self-assessment ("the source is at
`/home/vgpnk/…`"), and `rows_failed` counts the cells whose assessment doesn't resolve. If "observed
state" is read as "the map/copy state", then the claim reduces a mismatch count row↔map → calibration.
Two facts cut this down: (i) every red row's host path **exists and matches its own pins on this host
today** — R42LocalSrc §3 re-verified all 41 row digests against the live objects; the rows are
*right*, the lane just doesn't own the bytes. What fails is not descriptive accuracy but resolvability.
(ii) The only row↔world comparator inside the gate is `source_sha256` — a host-dependent check the plan
itself treats as secondary. §6.9's test is "does the number count how wrong a self-description is vs the
world?" — no; it counts which citations lack an owned resolution. **Conclusion: coverage.** The residual
calibration ingredient is `source_sha256` (a drift watch), which is why P-6 says either drop it or scope
it explicitly; leaving it unscoped blurs exactly the line the critic is asked to draw.

**Plan text that makes the surface explicit** (drop-in for the "Surface moved" paragraph's second
sentence, and a one-liner in the Target bullet):

> Surface moved: the SOURCES registry's citation authority — the set of registry rows a fresh lane
> checkout resolves to bytes the lane holds. Before the move the authority covers 115 of 134 rows'
> citations; after, 134 of 134 (135 of 135 once S135 lands). `rows_failed` counts citations without an
> in-lane resolution — a resolvability gap list, not a self-assessment error count; row↔world fidelity
> rides in the rows' recheck cells and the round's disposition-exact copy audit (P-2), not in the gate
> exit.

## (b) Gameability — four attacks, clause by clause

The gate (`check_path`, `tools/round-41/local-source-gate.py:202-288`) binds each map entry through:
`copy-outside-lane` (abs/escape, L217-220) → `copy-is-the-external-path` (L222) → `copy-missing`
(L223) → `copy-not-a-regular-file` (`os.path.isfile`, L225-226) → `copy-digest-mismatch` (L232-234) →
`row-pin-conflict` (L242, only when the URL cell pins a digest) → `sidecar-*` →
`source-digest-mismatch` (L278, only when `source_sha256` set **and** the host path exists).

| attack | result | gate clause that must bind | binds today? |
|---|---|---|---|
| **map-only** (entries, no copies) | exit 1, 18 rows / 21 path records `copy-missing` — `receipts/t3-map-only.txt` | `copy-missing` L223 | **yes** |
| **abs-path copy** (`copy: /home/…`) | exit 1 `copy-outside-lane` — `t7-abs-copy.txt` | `copy-outside-lane` L217 | **yes** |
| **`..` escape copy** | exit 1 `copy-outside-lane` — `t8-escape.txt` | `inside()` after `normpath`, L220 | **yes** |
| **digest collision** | needs a sha256 preimage against the declared `sha256`; not practical | `copy-digest-mismatch` L234 | **yes** (computational) |
| **copy-as-symlink → host object** | **exit 0 — greens S001 on this host** (`[resolved/none]`, `t2-symlink.txt`) | `copy-not-a-regular-file` should reject a symlink — but `os.path.isfile` follows links; `inside()` checks only the link's own in-lane path | **NO — hole** |
| → same symlink, dangling | exit 1 `copy-missing` (`t2b-dangling.txt`) | — | (shows the green is host-dependent: same commit is green here, red on a fresh clone elsewhere — the claim's own "resolvable from in-lane bytes" semantics broken) |
| **in-lane shadow copy, unpinned row** (S001's `copy` pointed at S002's bytes with that file's digest) | **exit 0** (`t5-unpinned-shadow.txt`) | nothing — `row-pin-conflict` needs a URL-cell pin and none of the 18 rows has one (gate-exact census below; selftest case 21 `row-wide-digest-does-not-bind` is deliberate) | **NO — hole** for fidelity; resolvability-only gate can't see it |
| **worktree-shadow** (landing in worktree only, gate `--rev 6b9e64fe`) | **exit 0** while `git show 6b9e64fe:…/local-sources.json` has 1 entry vs 18 in the worktree (`t1-green-…json`) | nothing — the gate reads the **table at REV** (`git show`, L116) but the **map and copies from the worktree** (L303-311, L223-232). Receipt records `table: git:…` but `map:` is only a path, no digest | **NO — provenance hole**: a receipt can attribute exit 0 to a rev that contains neither the map nor the copies |
| **table edit** (URL cells' host paths re-prosed; fed via `--sources`) | exit 0 at rows_total=134, checked=1 (`t6-table-edit.txt`) | predicate's byte-identity clause (gate itself can't compare to base) | via predicate — but the clause is self-contradicted by S135 (F3) |
| **`--sources`/`--map` overrides** | gate accepts arbitrary files (argparse L683-685; `--map` may be absolute, L304) | counting command must pin them | **no — counting command doesn't forbid them** |
| directory/gitlink/hardlink copies | `copy-not-a-regular-file` catches dir/gitlink; hardlink commits as a regular file with the real bytes — legitimate | L225 | yes |

**Census (gate-exact):** for every one of the 18 failing rows, `urlcell_pins = 0` — their 41 digests
live in the anchor/teaches cells, which the gate deliberately ignores (selftest 21). Only S126 pins in
its URL cell (=1). Consequence: `row-pin-conflict` is **dead code for this claim's row set**; the map's
`sha256` is bound only to the copy's bytes, never to the host object. The *entire* fidelity binding is
the in-round audit clause — see F2/P-2.

## (c) Is `rows_total ≥ 129` the right denominator clause?

**Measured:** `rows_total` at base = **134** (base receipt; S001–S134), 135 after the S135 append —
the draft's `≥ 129` is the round-41-era count, stale by six. Exploitability check: deleting a red row
keeps exit 1 while any red remains, so no sub-total truncation greens; deleting *all* out-of-lane rows
(19) drops total to 116 < 129 → still caught. So `≥129` is not exploitable today — but it is wrong, and
the load-bearing anti-truncation clause is byte-identity of the table, not the count (T6: table edited
to prose greens at `rows_total=134` with only `rows_checked=1`). Right clause: **`rows_total == 135`
(134 if measured before the S135 commit) and `rows_checked == 19` and `rows_failed` empty.** Pinning
`rows_checked` additionally catches the case where a URL cell is edited to stop parsing as a path —
which T6 shows is invisible to `rows_total`.

## (d) Fresh-checkout semantics

**Test:** committed landing in a scratch clone (`git -c user.name=fx commit`), fresh `--shared` clone
of it, `checkout REV`, gate `--rev REV` → **exit 0** (`receipts/t4-fresh-clone-at-landing-rev.json`;
also exit 0 without `--rev`, worktree read). So yes — after a committed landing, a fresh clone passes
the gate **using only in-lane bytes under `corpus/evidence/round-41/s126/` and
`corpus/evidence/round-42/local-sources/`** — provided:

1. the gate is run with the worktree **at** REV (provenance, F5 — the map/copy reads are
   worktree-relative, not rev-relative; only the table is rev-pinned);
2. no symlink sneaks in (F1 — symlink copies are exactly the "greens here, reds elsewhere" class:
   git commits mode-120000, the link resolves only where the host object exists);
3. the host's `source_sha256` objects are absent-or-identical — `S003`, `S023`, `S082/extra.db`,
   `S126` carry `source_sha256`; a fresh clone on a host that happens to hold a *different* Ghidra at
   `~/.local/opt/ghidra_12.1.4_PUBLIC/…` goes red (`source-digest-mismatch`). So "fresh clone passes
   using only in-lane bytes" is true on a **host-free machine** and true on *this* machine, but not
   guaranteed on every machine — the residual host read is exactly those four fields. P-6 makes the
   semantics clean.

## (e) Kill-rule completeness

Current controls: CTL-C2-0 do-nothing at freeze (reproduced: exit 1/18 — base receipt) and CTL-C2-1
absent/digest-mismatched copy keeps red (T3 covers the absent half). Necessary, **not sufficient**:

- The kill rule says "a control reaching exit 0 stops C2 before the copies land". A **symlink-copy
  control reaches exit 0 today** (T2) — it would mis-fire the kill rule even though the claim's
  semantics exclude it. Same for a **shadow copy on an unpinned row** (T5). The rule must read
  *"a control reaching exit 0 **while satisfying every P43-C2 clause** stops C2"*, and two more
  controls must be scored at the freeze:
  - **CTL-C2-2** symlink copy (committed mode-120000, pointing at the host object): gate exits 0 —
    receipt *plus* the predicate's lstat clause rejecting it. Demonstrates the frozen gate alone is
    not the whole counter.
  - **CTL-C2-3** worktree-shadow (landing in worktree, not committed; gate at freeze rev): exit 0 —
    rejected by the provenance clause (receipt must record a clean checkout at REV, P-5).
  - **CTL-C2-4** (cheap, optional) unpinned shadow copy: exit 0 — rejected by the disposition-exact
    audit clause (P-2).
- CTL-C2-1's rationale says "the receipt names the map version" — **it does not**: the JSON receipt
  carries `map` (a path string), `table` (rev-pinned) and `table_sha256`, but no `map_sha256`, no
  `counter_sha256`, no cleanliness flag. P-5 names exactly what the receipt must gain.

## (f) Findings

- **F1 (hole): copy-as-symlink greens on the scoring host.** `os.path.isfile` follows links;
  `inside()` checks the link's own path. A committed symlink `…/S001/SKILL.md →
  /home/vgpnk/.agents/…` scores `[resolved/none]` — measured. It is also the portability-breaker
  (dangling on a fresh clone: `copy-missing`). *Fix: P-1 + CTL-C2-2.*
- **F2 (hole): zero URL-cell pins ⇒ copy bytes bound only to the map, never to the host object.**
  Shadow copy greens (measured, T5). The predicate's only fidelity clause — "every copy's digest
  re-verifies against the live host object it copies" — is **also worded wrong for 5 of the 17
  dispositions**: the gzip `.gz` and the four tar archives' digests are deliberately **not** the host
  object's digest; re-verification is disposition-exact (byte-copy: digest==host; `gzip -9 -n`:
  `gunzip` digest==host; member/tree-archive tars: every cited member digest==host member, container
  bound by `source_sha256` where present — i.e., the `verify-copies.py` semantics R42LocalSrc already
  proved: 67/67). *Fix: P-2.*
- **F3 (self-contradiction): "byte-identical to the base except nothing" vs the S135 append.**
  The frontier step appends S135 in-round; at the measured revision the table is base+S135, **not**
  byte-identical to base. The clause as written can never be true once the frontier step lands — and it
  is the only clause that kills T6's table-edit green. *Fix: P-3.*
- **F4 (stale): `rows_total ≥ 129`; measured 134, 135 post-S135.** Non-exploitable today, wrong on the
  freeze. *Fix: P-4.*
- **F5 (provenance hole): gate reads map+copies from the worktree regardless of `--rev`.** Measured:
  exit 0 at `6b9e64fe` with a 1-entry map at that rev. A receipt can attribute green to a rev that does
  not contain the landing; a dirty worktree can green any rev. *Fix: P-5 + CTL-C2-3.*
- **F6 (wrong disclosed limit + host-dependent exit):** "host paths that drift later re-red the row in
  the gate's advisory output without changing its exit" — **false**: `source_sha256` drift returns
  `source-digest-mismatch` which is a *hard* fail (L278; selftest `source-digest-mismatch-is-red`); it
  only becomes advisory ("skipped-absent") when the host path is **gone**. It also re-introduces a host
  read into a claim whose entire point is host-independence (F-d). *Fix: P-6.*
- **F7 (freeze-rule self-block):** the "Frozen paths" list names `corpus/evidence/local-sources.json`
  and the copies dir as C2 frozen paths while the rule forbids any FREEZE..REV commit touching a frozen
  path — the landing commit then makes the score **inadmissible** (`frozen_path_changed`). The
  parenthetical "(added after the freeze — landing paths…)" gestures at an exemption the rule never
  grants. C1 already models the carve-out (its heldout dir is first-added after the freeze and is *not*
  in C1's frozen list). *Fix: P-7 — split byte-frozen vs landing paths; better, pin the map's own sha256
  in the freeze note (the prepared pack's map digest is already fixed), which turns the exemption into
  a declared value.*
- **F8 (leftover):** Separability still names `corpus/evidence/round-43/local-sources/` after the
  landing-path amendment. *Fix: P-8.*
- **F9 (kill-rule mis-fire + thin controls):** see (e). *Fix: P-9.*
- **F10 (scope slip):** "no third-party firmware image is among them" reads over *all* mapped copies,
  but S126's entry is pre-existing round-41 evidence (a lane-built AVM image's *extraction TSV* — the
  copy itself is fine, but its dir sits next to `avm-be.squashfs`). Scope the clause to the 17 new
  mapped `copy` paths. Also minor: duplicate map keys last-win (JSON), `--sources`/`--map` overrides —
  pin them out of the counting command. *Fix: P-10.*

## (g) What already binds (keep)

`map-missing`, `no-copy-named`, `copy-missing`, `copy-not-a-regular-file` (real files), `copy-outside-lane`
(abs + `..`), `copy-is-the-external-path`, `copy-digest-mismatch`, `sidecar-*`, map-key-must-be-absolute,
ENTRY_KEYS whitelist, `EXPECTED_COLS` row-shape, and the selftest (23/23 per R42LocalSrc). The gate's
per-row/per-path records, `source_present` and `src_check` reporting are the right substrate — the
claim just needs the clauses the gate was never meant to carry.

## 7. Concrete predicate changes (numbered for the L1)

- **P-1** P43-C2: replace "exactly one in-lane regular-file copy" with "exactly one in-lane copy that
  is a regular file — not a symbolic link, and no symbolic link at any component of its path (verified
  by `lstat`/`find -type l` over `corpus/evidence/round-42/local-sources/` at the measured revision by
  the scoring wrapper; the frozen gate's `isfile` follows links and does not reject them)".
- **P-2** P43-C2 audit clause → "every copy is re-derived byte-exactly from the live host object it
  stands for, per its disposition (byte copy: copy digest == host digest; `gzip -9 -n`: decompressed
  digest == host digest; member/tree-archive tars: every cited member digest == the host member's
  digest, container bound by `source_sha256` where declared) — the `verify-copies.py` semantics — run
  by two independent seats this round against the exact committed bytes at REV".
- **P-3** Table clause → "the `corpus/SOURCES.md` table is byte-identical to the base **except the one
  appended S135 row** (an https URL; no out-of-lane path; every base row's line bytes unchanged)".
- **P-4** Target → "`rows_failed` empty, `rows_total == 135` (134 if measured before the S135 commit),
  `rows_checked == 19`".
- **P-5** Counting command → "in a clean `--shared` clone checked out at REV (`git status --porcelain`
  empty, recorded): `python3 -I -B tools/round-41/local-source-gate.py --root <CLONE> --rev <REV>
  --json`; no `--sources`/`--map` overrides. Receipt additionally records `counter_sha256 =
  sha256sum(tools/round-41/local-source-gate.py)` at REV, `map_sha256 = sha256sum(corpus/evidence/
  local-sources.json)` at REV, REV, and the cleanliness line."
- **P-6** Decide `source_sha256` for the 17 new entries — **recommended: drop it** (the gate's exit
  becomes purely in-lane; host drift watch stays in the rows' recheck cells; S126's entry may stay).
  Alternative: keep it, rewrite the disclosed limit ("a drifting host path re-reds the row **and**
  flips the exit on hosts that hold it"), and record per-row `src_check` in the receipt.
- **P-7** Frozen paths → split: byte-frozen = plan, `tools/round-41/local-source-gate.py`,
  `corpus/evidence/round-41/s126/`; landing = `corpus/evidence/local-sources.json` **pinned by digest**
  (`map_sha256` = the prepared pack's map sha256 recorded in the freeze note) and
  `corpus/evidence/round-42/local-sources/` (first-added after the freeze, exempt from the no-touch
  rule exactly like C1's heldout dir).
- **P-8** Separability: `round-43/local-sources/` → `round-42/local-sources/`.
- **P-9** Kill rule → "a control reaching exit 0 **while satisfying every P43-C2 clause** stops C2";
  add CTL-C2-2 (symlink copy), CTL-C2-3 (worktree-shadow), and optionally CTL-C2-4 (unpinned shadow
  copy) scored at the freeze.
- **P-10** "no third-party firmware image" scoped to the 17 new mapped `copy` paths; forbid
  `--sources`/`--map` overrides in the counting command; note duplicate-map-key last-wins as a
  non-binding footnote.

## 8. Evidence appendix

All runs: scratch `/fast/scratch/hyaku/kaidoku-r43/w1-R43CritC2` (removed on exit), `--shared` clones
of `kaidoku-shokunin`, gate = committed `tools/round-41/local-source-gate.py` (sha256 `cafe232a…`,
unchanged since `d764389e`). No tools installed/upgraded; pacman untouched. python3 3.14.x, git 2.56.

| test | command shape | exit | receipt |
|---|---|---|---|
| base | gate `--rev 6b9e64fe` | 1 (18 rows) | `receipts/ctl-c2-0-gate-at-base.json` |
| T1 prepared pack in worktree | `cp -a <A>/corpus/. <clone>/corpus/` + gate `--rev 6b9e64fe` | 0 | `receipts/t1-green-….json` (map at rev = 1 entry vs 18 in worktree) |
| T2 symlink→host | copy replaced by `ln -s /home/vgpnk/.agents/…` | **0** | `receipts/t2-symlink.txt` |
| T2b dangling symlink | `ln -s /nonexistent/…` | 1 `copy-missing` | `receipts/t2b-dangling.txt` |
| T3 map only | map copied, no copies | 1 (21 `copy-missing`) | `receipts/t3-map-only.txt` |
| T4 committed landing, fresh clone | clone→commit landing→fresh clone→gate `--rev <REV>` | 0 | `receipts/t4-fresh-clone-at-landing-rev.json` |
| T5 unpinned shadow | S001 `copy`→S002 bytes + that digest | **0** | `receipts/t5-unpinned-shadow.txt` |
| T6 table-edit | 18 URL cells re-prosed, via `--sources` | 0 (checked=1) | `receipts/t6-table-edit.txt` |
| T7 abs copy | `copy: /home/…` | 1 `copy-outside-lane` | `receipts/t7-abs-copy.txt` |
| T8 `..` escape | `copy: ../../../../home/…` | 1 `copy-outside-lane` | `receipts/t8-escape.txt` |

## 9. Limits of this review

I did not re-run the 41-digest row-pin audit (R42LocalSrc's numbers are cited, not re-verified — the
round's own audit seats cover it); `source_sha256` drift was established by code path + selftest case,
not by mutating a host object; and I attacked the *draft* — if the L1 lands a different map than the
prepared pack's, F2's clause wording matters more, not less. No gate bytes were modified anywhere; the
symlink run was staged only inside the scratch clone's worktree.

Report: `.ufo/waves/round-43/w1/R43CritC2.md` · receipts: `.ufo/waves/round-43/w1/artifacts/R43CritC2/receipts/`
