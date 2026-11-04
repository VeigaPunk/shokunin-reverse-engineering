# ScoutLoci — R84-C2 honesty reconnaissance (read-only)

Lane `kaidoku-shokunin`, round 84, wave `r84-w1`, seat `ScoutLoci`.
Declaration revision `e0de2088a7bddc16305357f90ac7e889fa0a0d11`; first container `a5663ddedd157bb9113928f5fe80509d6f3fc7a1`; BASE `043b89a25241710a68b45526c3287fb3c8d907c3`.

Scope: reconnaissance for the honesty of **R84-C2** (`tools/round-84/mutation-closure.py`).
No production edit, no git mutation in the lane tree, no sibling-lane write. All measurements were
run read-only against the lane plus a private clone under my scratch dir.

> **Mid-seat integration notice (material to this report).** While this seat was working, the L1
> landed commit `b15d8083baf4f6de420fb452bcec13a87f4bb22a` ("integrate the seven printed-command
> and two source-bind declared cases, tighten the precheck control, the mutation table identity
> and the nested-depth arms"). That commit (a) rewrote the three round-84 counters, (b) rewrote
> `.ufo/waves/round-84/claims.json`, (c) **edited two of my three C2 target tools**
> (`tools/round-82/printed-command.py`, `tools/round-83/source-bind.py`) to add the nine declared
> cases, and (d) appended `instrument_supersessions` entries — including one in the **round-82**
> container for `printed-command.py` and one in the round-84 container for `source-bind.py`.
> Everything below that cites a **frozen** byte is measured at the declaration revision
> `e0de2088`; a **§8 "post-integration re-verification"** section re-measures the same findings
> at HEAD so the L1 has both. Section 8 also carries the two items the integration did **not**
> resolve.

Tools used (no install required; all present on the host):
`git` (read-only), `python3` 3.14.8, `mksquashfs` / `unsquashfs` 4.7.5 (2026/03/01), `npx`-free
(REA not exercised — out of my item). **No tool was installed or upgraded**, so no
operator-2026-10-19 install record is owed.

---

## 1. Anchor census — every edit anchor occurs exactly once

Method: `git show <rev>:<target>` at the declaration revision, then a literal count of the
`find` string over the decoded text and over the raw bytes (both, because the sources contain
multi-byte UTF-8: `—`, `…`). Character offsets and byte offsets coincide for every anchor, i.e.
all anchors sit in pure-ASCII regions of their files.

| # | mutant | target | edit | char/byte offset | occurrences | declared `anchor_occurrences` |
|---|--------|--------|------|------------------|-------------|-------------------------------|
| 1 | floor | `tools/round-82/conjunction-gate.py` | `len(cases) < PRISTINE_FLOOR` | 4788 | 1 | (none declared — 2-edit row) |
| 2 | floor | `tools/round-82/conjunction-gate.py` | `summary[0] < PRISTINE_FLOOR` | 4928 | 1 | (none declared — 2-edit row) |
| 3 | failure | `tools/round-82/conjunction-gate.py` | `elif summary[1] != 0:` | 4706 | 1 | 1 ✓ |
| 4 | binder | `tools/round-82/conjunction-gate.py` | `if receipt.get("binder_sha256") != BINDER_SHA256:` | 4275 | 1 | 1 ✓ |
| 5 | membership | `tools/round-82/printed-command.py` | `if script not in pins:` | 4980 | 1 | 1 ✓ |
| 6 | pin-call | `tools/round-82/printed-command.py` | `        pin_matches(root, rev, script, pins[script])` | 7095 | 1 | 1 ✓ |
| 7 | static-refusal | `tools/round-82/printed-command.py` | `    if result["static_defects"]:` | 6884 | 1 | 1 ✓ |
| 8 | source-mined | `tools/round-82/printed-command.py` | `cells[8] == "mined"` | 10659 | 1 | 1 ✓ |
| 9 | source-date | `tools/round-82/printed-command.py` | `cells[9] == "2026-11-04"` | 10701 | 1 | 1 ✓ |
| 10 | source-base | `tools/round-82/printed-command.py` | `base_absent = sources_row(base_text, SOURCED_ROW) is None` | 10778 | 1 | 1 ✓ |
| 11 | source-plan | `tools/round-82/printed-command.py` | `plan_names = SOURCED_ROW in re.findall(r"\bS[0-9]+\b", read_text(root, rev, PLAN))` | 10840 | 1 | 1 ✓ |
| 12 | source-entry | `tools/round-82/printed-command.py` | `entry_ok = entry_cites(entry_text, SOURCED_ROW)` | 10989 | 1 | 1 ✓ |
| 13 | sb-header-position | `tools/round-83/source-bind.py` | `if len(fields) != 1 or fields[0][0] >= 12:` | 1454 | 1 | 1 ✓ |
| 14 | sb-duplicate-last | `tools/round-83/source-bind.py` | `if line.startswith("source:")]` | 1419 | 1 | 1 ✓ |

**Result: 14 edits across 13 rows, every anchor occurs exactly once. 0 defects.**
Receipts: `receipts/anchors.json`, `receipts/anchors.txt`, `receipts/anchors.py`.

Anchors are byte-identical at BASE and at the declaration revision — the three target blobs did
not change between `043b89a` and `e0de2088` (digests below), so the census holds at both ends of
the claim's span.

---

## 2. Target blob digests and the BASE selftest case inventory

Blob sha256 at the declaration revision `e0de2088` **and** at BASE `043b89a` (identical in both
revisions for all three targets):

| target | sha256 | bytes |
|--------|--------|-------|
| `tools/round-82/conjunction-gate.py` | `f009009993160ca40dd55d771f8c05ce1e32799c22450f5430cae2c6e0bf163a` | 20464 |
| `tools/round-82/printed-command.py` | `88b1dff2385547e1bdb2ecf802d667c38eabe929747075c27ae88f0c5c061487` | 28440 |
| `tools/round-83/source-bind.py` | `800a759e20096859a145cfbe3f95e199502f7aa38b8ca796575d00af5963db3c` | 7031 |

These are exactly the digests the round-82 container pins
(`.ufo/waves/round-82/claims.json` `instruments`) and the round-83 canonical identity
(`.ufo/waves/round-83/l1/canonical-identity.json` `target_sha256`).

### Selftest case inventory at BASE (from each target's own `--selftest`)

`conjunction-gate.py` — 21 cases, all green (`SELFTEST cases=21 failures=0`), JSON-shape
(`case_names` + `failures`):

    binder-deficiency-frozen-accepts, binder-refused, detector-absent-refused,
    detector-nonunique-refused, detector-passing-refused, failures-deficiency-frozen-accepts,
    failures-refused, first-declared-defect-binder, floor-deficiency-frozen-accepts,
    floor-refused, frozen-rule-agrees-genuine, frozen-rule-not-killed-refused,
    genuine-synthetic-passes, mutants-refused, original-names-refused, pristine-exit-refused,
    summary-bool-refused, summary-floor-independent, survivors-refused, validate-consistent-clean,
    validate-refused-mismatch

`printed-command.py` — 15 cases, all green, JSON-shape:

    bare-name-refused, ellipsis-refused, entry-cites-no-source-line, entry-cites-true,
    entry-cites-wrong-row, fixture-repo-top, metachar-refused, pin-match-accepts,
    pin-mismatch-refused, placeholder-refused, prefix-refused, row-parse-absent,
    row-parse-mined, row-parse-queued-unmet, unpinned-path-refused

`source-bind.py` — 6 cases, all green, plain `selftest <case>: ok` shape (no JSON summary):

    duplicate, duplicate-after-window, malformed, positive, unavailable, withdrawn

### Declared case present / absent

| mutant | declared case | target | present at BASE? |
|---|---|---|---|
| floor | `floor-refused` | conjunction-gate | **present** |
| failure | `failures-refused` | conjunction-gate | **present** |
| binder | `binder-refused` | conjunction-gate | **present** |
| membership | `bare-name-refused` | printed-command | **present** |
| pin-call | `runtime-pin-mismatch-refused` | printed-command | **absent** |
| static-refusal | `static-defect-no-execution` | printed-command | **absent** |
| source-mined | `sourced-row-rejected-status` | printed-command | **absent** |
| source-date | `sourced-row-wrong-date` | printed-command | **absent** |
| source-base | `sourced-row-at-base` | printed-command | **absent** |
| source-plan | `sourced-plan-missing` | printed-command | **absent** |
| source-entry | `sourced-entry-uncited` | printed-command | **absent** |
| sb-header-position | `late-single-header` | source-bind | **absent** |
| sb-duplicate-last | `duplicate-target-second` | source-bind | **absent** |

**4 present / 9 absent.** The four present cases are exactly the four the plan calls the
"recorded round-82 seven plus the round-83 two" survivor set's complement — i.e. the frozen
table's four already-bound declared cases are `floor-refused`, `failures-refused`,
`binder-refused`, `bare-name-refused`.

### Independent reproduction of the "before" state

I ran the frozen counter myself at BASE, read-only, into my own scratch:

```
python3 -I -B tools/round-84/mutation-closure.py --root <lane> --rev 043b89a2524... \
  --mutants .ufo/waves/round-84/mutants.json --work <scratch> --json-out <scratch>
→ {"killed": 4, "mutants": 13, "ok": false, "pristine_failed": [],
   "survivors": ["pin-call","static-refusal","source-mined","source-date","source-base",
                  "source-plan","source-entry","sb-header-position","sb-duplicate-last"],
   "inconclusive": []}   EXIT=1
```

This matches the lane's own `pre/c2-base.json` byte-for-byte on the fields that matter
(`killed 4`, same nine survivor ids, `inconclusive []`, `pristine_failed []`, exit 1) — receipt
`receipts/c2-base.json`. **The plan's "before" arm is honest.**

The nine survivors each carry `reason: "declared-case-absent-from-selftest"` and
`declared_case_present: false`. None is a survivor because the mutation was verdict-neutral: the
counter never got to run a verdict, because the declared case was not in the pristine inventory.

---

## 3. Verdict-relevance of each mutated expression

"Present in the text" is not the same as "changes the verdict the declared case would assert".
For each mutant I built a behaviour-level probe that makes the declared case's assertion
observable, ran it against pristine bytes and against the mutated bytes, and asked whether the
verdict flips. Probe: `receipts/probe.py`; results: `receipts/verdict_relevance.json`.

### The four present cases (already bound at BASE)

| mutant | declared case | verdict-relevant? | evidence |
|---|---|---|---|
| floor | `floor-refused` | **YES** | `conjunction()`'s floor guard is doubled. Applying **either** edit alone leaves the selftest green (`[]` failures); applying **both** turns `floor-refused` red. The 2-edit pairing in the table is therefore *necessary*, not decorative: a single-edit version of this row would be a **survivor**, not a kill. Confirmed against the lane's own BASE run: `floor` is already among the 4 killed. |
| failure | `failures-refused` | **YES** | `elif summary[1] != 0:` is the sole producer of the `pristine_failures_nonzero` defect; the case asserts `defects[0] == "pristine_failures_nonzero"`. Disabling it removes that defect. Killed at BASE. |
| binder | `binder-refused` | **YES** | `binder_digest_mismatch` is produced only by that comparison; the case asserts `defects[0] == "binder_digest_mismatch"`. Killed at BASE (also trips `first-declared-defect-binder`, a second case in the same tool — collateral, not a mis-binding). |
| membership | `bare-name-refused` | **YES** | `if script not in pins:` is the only source of `SCRIPT_NOT_PINNED` for a bare name. Killed at BASE (also trips `unpinned-path-refused` — collateral). |

Note on the last two: at BASE these two mutants fail *more than one* case in the target's own
selftest. The counter's rule (`declared_case in result["failures"]`) tolerates that, and the
declared case is present in both, so the binding is sound — but a kill is not evidence of
*exclusive* binding. Reviewers should not read `killed` as "only the declared case fired".

### The nine absent cases (the work)

| mutant | declared case | verdict-relevant? | evidence |
|---|---|---|---|
| pin-call | `runtime-pin-mismatch-refused` | **YES** | With the `pin_matches(root, rev, script, pins[script])` call replaced by `pass`, a fixture repo whose *working-tree* script bytes differ from the pin but whose committed blob matches yields: pristine → `REFUSED: SCRIPT_PIN_MISMATCH: tools/t.py executed path differs from the pin`, `executed=false`; mutant → `executed=true`. The refusal disappears; the declared case's assertion flips. |
| static-refusal | `static-defect-no-execution` | **YES**, with a stated caveat | Pristine `run_block` on a metachar command returns `static_defects=["SHELL_METACHAR: ;"]`, `defects=["SHELL_METACHAR: ;"]`, `executed=false`. Mutant: `if False and result["static_defects"]:` no longer short-circuits, the block *executes* (`executed=true`). **Caveat:** in my first probe the mutant's own defect list was `RECEIPT_UNREADABLE` (the child could not write its receipt) rather than a clean pass — the mutant is still distinguishable from pristine (executed flips false→true), but a candidate selftest case must assert on `executed`/`static_defects`, **not** on the defect string, or it will be brittle. |
| source-mined | `sourced-row-rejected-status` | **YES** | In a fixture repo whose `corpus/SOURCES.md` row has status `rejected`: pristine `sourced_arm` defects `["SOURCED_ROW_UNMET", "SOURCED_ROW_AT_BASE"]`, mutant drops `SOURCED_ROW_UNMET`. **Also flips against the real lane tree** (the live S299 row's status is `rejected`, so the real `sourced_arm` at HEAD is `defects:["SOURCED_ROW_UNMET"]` pristine vs `[]` mutant). The only one of the five `source-*` mutants that flips without a fixture. |
| source-date | `sourced-row-wrong-date` | **YES** (fixture required) | Fixture repo with a wrong date (`2026-11-05`): pristine `["SOURCED_ROW_UNMET","SOURCED_ROW_AT_BASE"]`, mutant `["SOURCED_ROW_AT_BASE"]`. Against the **real** tree the mutant does **not** flip (live S299 date is `2026-11-04`, so the date conjunct is already satisfied) — a candidate case must therefore drive a fixture, not the live tree. |
| source-base | `sourced-row-at-base` | **YES** (fixture required) | Fixture repo whose BASE commit *contains* the row: pristine `["SOURCED_ROW_AT_BASE"]`, mutant `[]`. Does **not** flip against the real tree (live S299 is absent at the tool's own BASE constant `9cc8fbbc…`, so `base_absent` is already `True`). Fixture required. |
| source-plan | `sourced-plan-missing` | **YES** (fixture required) | Fixture repo whose plan omits `S299`: pristine `["SOURCED_ROW_NOT_IN_PLAN"]`, mutant `[]`. Does **not** flip against the real tree (the live round-82 plan does name S299). Fixture required. |
| source-entry | `sourced-entry-uncited` | **YES** (fixture required) | Fixture repo whose entry lacks the `source:` line: pristine `["SOURCED_ENTRY_UNCITED"]`, mutant `[]`. Does **not** flip against the real tree (the live entry does cite S299). Fixture required. |
| sb-header-position | `late-single-header` | **YES** | Fixture entry with a single `source:` header on line 13 (index 12, i.e. at/after the 12-line window): pristine `entry_cites` → `False` (the `fields[0][0] >= 12` guard rejects it); mutant (`if len(fields) != 1:`) → `True`. The header-position guard is the sole discriminator. |
| sb-duplicate-last | `duplicate-target-second` | **YES** | Fixture entry with two `source:` fields where the **second** is the target (`source: S286 — first` / `source: S299 — second`): pristine `entry_cites` → `False` (duplicate ⇒ not exactly one field); mutant (the `[-1:]` slice keeps only the last match) → `True`. The "target second" shape is exactly the discriminating shape — the mutant picks the *last* `source:` field, so a case with the target *first* would **not** flip. |

**Summary: 13/13 mutants are verdict-relevant to their declared case.** No mutant is a
textually-present-but-verdict-neutral edit. The four that kill at BASE are bound to a case that
exists; the nine that need new cases are all reachable by a case that can be written.

### Two implementation cautions for whoever writes the nine cases

1. **`source-*` needs a fixture repo, not the live tree.** Four of the five `source-*` mutants
   (`source-date`, `source-base`, `source-plan`, `source-entry`) are verdict-neutral against the
   real lane tree, because the live `corpus/SOURCES.md` S299 row already has status `rejected`
   and the live plan/entry already name and cite S299. A case written against the live tree
   would leave those four mutants as survivors. The lane's own `sourced_arm` reads
   `SOURCES`/`PLAN`/`ENTRY`/`BASE` from module constants; a candidate case must redirect those
   (as my probe does by patching the module globals) or the target's own `--selftest` cannot
   reach the discriminating state.
2. **Do not quote an anchor string in new selftest text.** The counter requires the anchor to
   occur *exactly once* in the target blob (`tools/round-84/mutation-closure.py:141-146`:
   `counts = [text.count(edit["find"]) …]; if any(count != 1 …)` → `inconclusive`,
   reason `anchor-not-exactly-once`). I demonstrated that adding a comment containing
   `if line.startswith("source:")]` to `source-bind.py` raises that anchor's count to 2 and
   would turn `sb-duplicate-last` **inconclusive** rather than killed. Any new selftest case that
   quotes an anchor verbatim is a trap.

---

## 4. mksquashfs reproducibility, verified independently

Command used (identical to `tools/round-84/nested-sqfs.py:64-66`):

```
mksquashfs <src> <img>.sqfs -noappend -comp gzip -b 4096 -quiet -repro-time 1760000000
```

**Tiny source, two builds:**

```
$ printf 'hello reproducible\n' > src/a.txt; printf 'second file\n' > src/b.txt
$ mksquashfs src repro/img1.sqfs -noappend -comp gzip -b 4096 -quiet -repro-time 1760000000
$ mksquashfs src repro/img2.sqfs -noappend -comp gzip -b 4096 -quiet -repro-time 1760000000
$ sha256sum repro/img1.sqfs repro/img2.sqfs
fbbf635a97f34ba46c14e8f427a804fa32ef7b663a6c52070c0f48973c06518d  repro/img1.sqfs
fbbf635a97f34ba46c14e8f427a804fa32ef7b663a6c52070c0f48973c06518d  repro/img2.sqfs
$ cmp repro/img1.sqfs repro/img2.sqfs   → identical bytes
```

**Digests: `fbbf635a97f34ba46c14e8f427a804fa32ef7b663a6c52070c0f48973c06518d` (build 1) ==
`fbbf635a97f34ba46c14e8f427a804fa32ef7b663a6c52070c0f48973c06518d` (build 2). Reproducible.**

**The full three-level chain, twice, with the counter's own recipe** (leaf/mid/outer as in
`nested-sqfs.py:build_chain`):

```
level a: run1=e82c59956789a47b7524dda30d9ac4f6139a4cf279b0e5403039df88549d06c2
         run2=e82c59956789a47b7524dda30d9ac4f6139a4cf279b0e5403039df88549d06c2  equal=True
level b: run1=7d2dd0e73d1bbeffe02aef346ea45b5c3604255a598b9cb7b1daaa6ef6fc3d1a
         run2=7d2dd0e73d1bbeffe02aef346ea45b5c3604255a598b9cb7b1daaa6ef6fc3d1a  equal=True
level c: run1=f68b42fa16a9b1ed0fd57165f0a949e89271c09a59db680b3e39a155fbea4aa8
         run2=f68b42fa16a9b1ed0fd57165f0a949e89271c09a59db680b3e39a155fbea4aa8  equal=True
```

These three digests are **identical to the lane's own `pre/c3-pilot.json` pins**
(`a e82c5995…`, `b 7d2dd0e7…`, `c f68b42fa…`) — my independent rebuild reproduces the frozen
C3 fixture identity exactly, with a 2.5 s wall-clock gap between the two builds and no
timestamp normalisation of the source tree. Nested-carrier identity also reproduces:
`b_is_oracle_member true`, `c_is_oracle_member true`, oracle member counts `{a:2, b:3, c:3}`
= the 8 published members.

**Control (without the flag):** two builds 1.2 s apart, no `-repro-time` →
`ca9cdf23763933f3e6b97c913c90da3b165184a2528a128478ae0bdee4020165` vs
`ad60701e87e68d96a7277aea7ca8018d03664570cd6ec09b2b513c4855323098` — **differ**, so the flag is
doing the work.

### One honest limit on `-repro-time` worth recording (does not affect C3's fixture as built)

`-repro-time` is *not* a blanket timestamp normaliser for the **file** timestamps in the image.
Measured with `unsquashfs -d` + `stat` on the extracted member:

| source file mtime | stored mtime in image |
|---|---|
| 1000000000 (2001) | **1000000000** — preserved verbatim |
| 1759999999 | 1759999999 — preserved verbatim |
| 1760000000 | 1760000000 |
| 1760000001 (after epoch) | 1760000000 — clamped |
| 1900000000 (2030) | 1760000000 — clamped |

So the stored file time is `min(src_mtime, 1760000000)`, and only the *superblock* creation time
(`mkfs_time`, read back as 1760000000) is fixed by the flag. `-all-time 1760000000` and
`-inode-time 1760000000` both store 1760000000 unconditionally and are strictly stronger.
This does **not** affect the C3 chain as built: every fixture file is written by the tool itself
at run time (`Path(...).write_text(...)`), i.e. mtime = now (2026) > the 1760000000 epoch, so
every member clamps to the epoch and the image is byte-identical across runs — which is exactly
what I measured. It would matter only if a fixture member were ever materialised with an
mtime *older* than the epoch (e.g. copied with `cp -p` from a tree with old timestamps), where the
image would then carry that old mtime and stop being reproducible. The counter's own recipe
does not do that, and `shutil.copyfile` (used for the nested carriers) does not preserve mtime.

---

## 5. Does `mutation-closure.py` mark a mutant with a missing declared case as a survivor?

**Yes — as a survivor, and the code says so explicitly.** The cited lines:

* `tools/round-84/mutation-closure.py:161-164` — the pristine inventory is read and
  `case_present = mutant["declared_case"] in pristine_inventory` is recorded on the entry.
* `tools/round-84/mutation-closure.py:165-173` — the decisive branch:

  ```
  165  if not targets[path]["green"]:
  166      entry["status"] = "inconclusive"
  167      entry["reason"] = "pristine-not-green"
  168      inconclusive.append(entry)
  169  elif not case_present:
  170      # QUALITY 138: an absent declared case is a survivor, never a pass.
  171      entry["status"] = "survived"
  172      entry["reason"] = "declared-case-absent-from-selftest"
  173      survivors.append(entry)
  ```

* The counter's own fixture asserts this behaviour: `mutation-closure.py:310-313`
  (`check("absent-case-survives", by_id["declared-case-absent"]["status"] == "survived" and
  … ["reason"] == "declared-case-absent-from-selftest")`), and the fixture table row
  `{"id": "declared-case-absent", … "declared_case": "omega"}` (`:274-275`) exercises it.
  The counter's `--selftest` is green: `SELFTEST cases=10 failures=0`.

**Important nuance for the L1 and the reviewer: the module docstring and the code disagree.**

* Docstring, `mutation-closure.py:13-14`:
  `inconclusive  the anchor does not occur exactly once, **or the declared case is absent from the pristine case inventory**, or the pristine tool is not green`
* Docstring, `mutation-closure.py:8`: `an absent declared case is inconclusive, never a pass`.
* Code, `mutation-closure.py:169-173`: an absent declared case is **`survived`**, not
  `inconclusive`; and the in-code comment at `:170` says "an absent declared case is a
  **survivor**".

The **code and the selftest agree with each other** (`survived`), and the SKILL registry row
(`SKILL.md:1928`) also says "an absent case is a survivor (QUALITY 138)". The **docstring is the
outlier** at `:8` and `:13-14`. The lane's own BASE receipt confirms the code's behaviour: the
nine absent-case mutants land in `survivors`, and `inconclusive` is empty.

This matters for the C2 predicate as written: `survivors []` and `inconclusive []` are *both*
required for `ok true`, so the plan's predicate is satisfied by either reading — but the
**docstring is a live honesty defect in a frozen, digest-pinned instrument**
(`tools/round-84/mutation-closure.py` is pinned at `fd8aee39bdfaa1aa51d1de9a175a77be9770dd6f3e68571ca798b8f6bdbad084`
in `.ufo/waves/round-84/claims.json`, and it is on the lane's frozen-bytes list, so it cannot be
edited in place). The correct remedy is a disclosed correction in the round-84 lesson/knowledge
and a registry-row note, not a silent edit. **Recommendation: L1 should route this as a
disclosed docstring-vs-code correction (round-83's precedent — an appended named correction in
the lesson, not a rewritten report).** The behaviour the C2 predicate measures is unaffected and
is the *stricter* of the two readings, so no claim needs restating.

---

## 6. Additional honesty observations bearing on C2's kill rule

The C2 kill rule includes *"a target digest differing from the frozen release pin without a
disclosed `instrument_supersessions` entry"*. Two facts the L1 must sequence:

1. **Editing `tools/round-82/printed-command.py` (or `conjunction-gate.py`) flips the round-82
   container from CLEAN to FLAGGED** under the maintained audit. Demonstrated in a private clone:
   appending one comment line to `printed-command.py` and committing it makes
   `tools/round-29/freeze-gate.py` report
   `.ufo/waves/round-82/claims.json FLAGGED [{'finding': 'INSTRUMENT_REVISED', 'path':
   'tools/round-82/printed-command.py', 'commits': ['bcb0bf3b…'], 'disclosed': 1}]`
   (round-83 stays FLAGGED/INSTRUMENT_NONE as designed, round-84 stays CLEAN).
   Adding an `instrument_supersessions` entry for that commit to the round-82 container restores
   round-82 to **CLEAN** (verified: clean count 31 → 32). So the disclosure path exists and is
   cheap; it must simply be executed before the round-82 container is re-audited.
   Receipt: `receipts/freeze-gate-head.json`, `receipts/freeze-gate-base.json`.
2. **`tools/round-83/source-bind.py` is not pinned by any claims container.** It appears in
   round-83's `canonical-identity.json` (`target_sha256 800a759e…`) and in the SKILL registry,
   but round-83's `claims.json` `instruments` map pins only `tools/round-83/attribution-audit.py`.
   Consequently (a) editing `source-bind.py` produces **no** `INSTRUMENT_REVISED` finding at all
   (the freeze gate only tracks paths named in claim strings), and (b) the round-83 canonical
   identity digest `800a759e…` becomes stale the moment the file changes. I confirmed the
   round-83 audit instrument still passes against an edited `source-bind.py`
   (`attribution-audit.py` → `ok true`, `mismatch_count 0`, `cases_total 8`; receipt
   `receipts/attr-audit-edited.json`) because it compares *behaviour* on frozen cases, not the
   subject's digest. **But the digest recorded in round-83's receipts no longer describes the
   tree**, and the C2 kill rule's "target digest differing from the frozen release pin" clause
   will fire on it. The L1 needs an explicit disclosure for `source-bind.py`'s digest, in a place
   the freeze gate actually reads — i.e. a new `instrument_supersessions` entry in the
   **round-83** container (or, if round-83's container must stay untouched, an explicit
   round-84 disclosure naming it).
   Note also: the plan's C2 text says the nine absent cases are "the recorded round-82 seven plus
   the round-83 two", i.e. seven cases in `printed-command.py` and two in `source-bind.py`. The
   seven round-82 cases land in a file whose container *does* pin it; the two round-83 cases land
   in a file whose container *does not*. The two halves of the same claim therefore need
   **different** disclosure routes. That asymmetry is invisible from the plan text alone.

---

## 7. Registry row drift (in scope for the round's standing duties, not C2's counter)

`SKILL.md` rows for the three new round-84 tools understate their own selftest sizes:

| tool | SKILL.md claims | actual `--selftest` |
|---|---|---|
| `tools/round-84/freeze-precheck.py` (`:1927`) | "selftest 10 cases" | `SELFTEST cases=11 failures=0` |
| `tools/round-84/mutation-closure.py` (`:1928`) | "selftest 7 cases" | `SELFTEST cases=10 failures=0` |
| `tools/round-84/nested-sqfs.py` (`:1929`) | "selftest 7 cases" | `SELFTEST cases=9 failures=0` |

All three counters are green. The registry rows are the lane's own metadata for the round's
standing duty ("registry rows for the three new tools under SKILL registry grammar v2"); the
numbers are wrong and are cheap to correct. Flagging for the registry-duty owner, not for C2.

---

## Findings summary

| # | finding | severity for C2 |
|---|---|---|
| F1 | All 14 edit anchors occur exactly once in the declaration-revision target blobs; offsets recorded | none — confirms the anchor clause |
| F2 | 4 of 13 declared cases exist at BASE; the 9 absent map 1:1 onto the 9 named survivors | none — confirms the plan's inventory |
| F3 | Independent BASE run reproduces `killed 4`, nine named survivors, `inconclusive []`, exit 1, matching `pre/c2-base.json` | none — the "before" arm is honest |
| F4 | All 13 mutants are verdict-relevant to their declared case (behavioural probes, not textual) | none — no neutral mutants |
| F5 | The `floor` row's 2-edit pair is *necessary*: either edit alone leaves the selftest green | none, but a single-edit rewrite of that row would silently become a survivor |
| F6 | `-repro-time` does not normalise file mtimes below the epoch (`min(src, epoch)`); C3's fixture is unaffected because the tool writes its members at run time | none for C2; recorded for C3's fixture-identity wording |
| F7 | **Docstring/code divergence in the frozen counter**: `mutation-closure.py:8` and `:13-14` say an absent declared case is *inconclusive*; the code (`:169-173` frozen / `:200-204` post-integration) and the counter's own selftest (`:310-313` / `:311-313`) and the SKILL row say *survivor* | **needs a disclosed correction** — still live after the integration; the code's behaviour is the stricter one and satisfies the predicate, but the pinned instrument's self-description is wrong |
| F8 | Editing `printed-command.py` flips round-82 CLEAN→FLAGGED (`INSTRUMENT_REVISED`); a disclosed `instrument_supersessions` entry restores CLEAN | **discharged** — the integration added the round-82 supersession; round-82 is CLEAN at HEAD (§7b.2) |
| F9 | `source-bind.py` is pinned by no claims container; editing it trips the C2 "target digest differing from the frozen release pin" clause with no existing disclosure route | **discharged for C2** — the integration added a round-84-container supersession (§7b.2); but the **round-83 canonical-identity receipt is now stale** and the freeze gate is blind to it (§7b.3) |
| F10 | Two of the five `source-*` mutants are verdict-neutral against the live lane tree (only `source-mined` flips there) | **heeded** — the integrated cases are fixture-driven and all four kill (§7b.1) |
| F11 | A new selftest case quoting an anchor string verbatim raises that anchor's count to 2 → `inconclusive` (`mutation-closure.py:141-146`) | **heeded** — anchor census re-run at HEAD is 14/14 exactly once (§7b.1) |
| F12 | SKILL.md rows understate the three round-84 counters' selftest sizes (10/7/7 vs 11/10/9) | registry duty, not C2 — **still live**, and re-measure after the integration (§7b.3) |

## 7b. Post-integration re-verification (at HEAD `b15d8083`)

The integration commit landed mid-seat, so every finding above is re-measured here against the
integrated tree. Receipts: `receipts/c2-at-head.json`, `receipts/freeze-gate-at-head.json`,
`receipts/c1-precheck-at-head.json`, `receipts/anchors-at-head.json`.

### 7b.1 The "after" arm of C2 is now green, and every kill is bound to its declared case

```
$ python3 -I -B tools/round-84/mutation-closure.py --root . --rev HEAD \
    --mutants .ufo/waves/round-84/mutants.json --claims .ufo/waves/round-84/claims.json \
    --work <scratch> --json-out <scratch>
{"killed": 13, "mutants": 13, "ok": true, "survivors": [], "inconclusive": [],
 "pristine_failed": [], "table_identity": {"expected": "dbb6d4c9…", "matches": true, …}}
EXIT=0
```

Per-mutant, every one of the thirteen:

| mutant | status | declared case | case present | anchor occurrences | failing cases |
|---|---|---|---|---|---|
| floor | killed | `floor-refused` | true | [1, 1] | `floor-refused` |
| failure | killed | `failures-refused` | true | 1 | `failures-refused` |
| binder | killed | `binder-refused` | true | 1 | `binder-refused`, `first-declared-defect-binder` |
| membership | killed | `bare-name-refused` | true | 1 | `bare-name-refused`, `unpinned-path-refused` |
| pin-call | killed | `runtime-pin-mismatch-refused` | true | 1 | `runtime-pin-mismatch-refused` |
| static-refusal | killed | `static-defect-no-execution` | true | 1 | `static-defect-no-execution` |
| source-mined | killed | `sourced-row-rejected-status` | true | 1 | `sourced-row-rejected-status` |
| source-date | killed | `sourced-row-wrong-date` | true | 1 | `sourced-row-wrong-date` |
| source-base | killed | `sourced-row-at-base` | true | 1 | `sourced-row-at-base` |
| source-plan | killed | `sourced-plan-missing` | true | 1 | `sourced-plan-missing` |
| source-entry | killed | `sourced-entry-uncited` | true | 1 | `sourced-entry-uncited` |
| sb-header-position | killed | `late-single-header` | true | 1 | `late-single-header` |
| sb-duplicate-last | killed | `duplicate-target-second` | true | 1 | `duplicate-target-second` |

Each kill names its declared case, `declared_case_present` is true throughout, and the anchor
census **re-run against the integrated targets** is still 14/14 anchors occurring exactly once —
i.e. the new selftest text did **not** trip my F11 trap. The nine new cases fire **only** their
own declared case (no collateral case), which is a *stronger* binding than the four pre-existing
cases manage (see F4's note on `binder`/`membership`).

The nine new cases are also *exactly* the discriminating shapes I identified in §3: the two
`source-bind` cases are the late-header and target-second fixtures; the four fixture-dependent
`source-*` cases (F10) were written against a fixture, not the live tree, and they kill.

### 7b.2 My F9 concern is resolved — but by a route that is not visible to the freeze gate

The integration added a round-84-container `instrument_supersessions` entry for
`tools/round-83/source-bind.py` (commit `b15d8083`, reason: "two declared boundary fixtures …").
That satisfies the C2 kill rule's clause *"a target digest differing from the frozen release pin
without a disclosed `instrument_supersessions` entry"*.

Confirmed state at HEAD:
* `tools/round-82/printed-command.py`: round-82 container gained a matching supersession entry ⇒
  `tools/round-29/freeze-gate.py` reports `.ufo/waves/round-82/claims.json` **CLEAN** (findings
  `[]`), audited 59 / clean 32. My F8 sequencing obligation is discharged.
* `tools/round-83/source-bind.py`: round-83 container still has **no** `instruments` entry and
  names no script path, so the freeze gate raises nothing for it (round-83 remains FLAGGED /
  `INSTRUMENT_NONE`, as the plan intends). The disclosure lives in the round-84 container, which
  is where the C2 kill rule looks. That is coherent, but it is worth recording that **the freeze
  gate would not have caught a stale `source-bind.py` digest on its own** — the disclosure is
  doing the work that the gate cannot.
* Round-84 container: **CLEAN** under both the maintained audit and the C1 precheck
  (`mismatches []`, `refused_expected 1`, `accepted_expected 1`, `control_fired true`,
  `met true`, exit 0).

### 7b.3 Two items the integration did **not** resolve

* **F7 (docstring-vs-code divergence) is still live.** The rewritten counter carries the same
  divergence: docstring `:8` and `:13-14` say an absent declared case is *inconclusive*; the code
  (now `:200-204`) and its own selftest (now `:311-313`) and the SKILL row say *survivor*. The
  rewritten file is *also* digest-pinned in the round-84 container, so this is still a
  disclosed-correction obligation, not an in-place edit. The predicate is unaffected — `ok true`
  needs both `survivors []` and `inconclusive []`, and the code's reading is the stricter one.
* **The round-83 canonical identity is now stale.** `.ufo/waves/round-83/l1/canonical-identity.json`
  records `target_sha256 800a759e…` for `tools/round-83/source-bind.py`; the integrated file is
  `3986706e…`. The round-83 container is not re-pinned (it pins only `attribution-audit.py`), so
  the freeze gate is silent — but the round-83 L1 receipt now describes bytes that no longer
  exist in the tree. My §6.2 finding stands, with the added detail that the round-84 supersession
  discloses the change for C2's purposes while the round-83 receipt remains unrestated. Whether
  round-83's L1 receipt may be re-issued or must be left as history is an L1 call; it should be
  made explicitly rather than left silent.
* **F12 (SKILL.md selftest counts) is still live and now more wrong.** The counters were rewritten
  by the integration, so the registry rows must be re-measured: at HEAD the actual counts are
  `freeze-precheck 11`, `mutation-closure 10`, `nested-sqfs 9`, while `SKILL.md:1927-1929` still
  says 10 / 7 / 7. All three counters are green.

### 7b.4 What the integration changed in the counter (reviewed, no objection)

The diff of `tools/round-84/mutation-closure.py` between the declaration revision and `b15d8083`
adds three things, all of which I checked:

* `unsafe_component(mutant["id"])` refuses a table-supplied id containing a path separator, a
  parent reference or an absolute spelling, **before** any write, marking such a mutant
  `inconclusive` / `unsafe-mutant-id` (helper at `:241`, use at `:173`). This closes a real
  path-containment hole in the frozen counter (the id is joined into `--work`), and it does not
  touch the 13 frozen ids — all thirteen are leaf names, so the table is unaffected
  (confirmed: 13 killed at HEAD).
* `table_identity()` compares the frozen table's bytes to the container's `fixtures.sha256` and
  fails the run on a mismatch (`:102-129`, `table_ok` folded into `ok` at `:221`). This closes
  the "a row dropped or replaced after the freeze still yields a green counter" hole. At HEAD
  `table_identity.matches` is true — the table is byte-unchanged
  (`dbb6d4c93df656d4c8341dee8a42e9256ba77e1d2e56ecda5b07d1db77b8982b`).
* A `--claims` argument so the counter can find the container to compare against.

The kill binding itself is unchanged, and my §3 verdict-relevance analysis is unaffected —
re-verified by the 13/13 kills above.

---

## Remaining unknowns / what I did not establish

* I did not run the C3 counter end-to-end (REA/`npx rea-agents@6.5.0` is out of my item and
  would need network); I verified only the **fixture-identity** half of C3 (image digests and
  nested-carrier identity), reproducing the lane's own `pre/c3-pilot.json` pins exactly.
* I did not decide *how* the nine new selftest cases should be written (that is the executor
  seats' candidate work); I established only that each is reachable, which fixture each needs,
  and the two traps (F10, F11).
* I did not verify the C1 precheck predicate against the round-83 container beyond a green run
  (`receipts/c1-precheck-head.json`: `mismatches []`, `refused_expected 1`, exit 0) — C1 is not
  my claim.
* Whether the L1 prefers to put the `source-bind.py` digest disclosure in the round-83 container
  (making a historical container change) or elsewhere is an L1 decision; I recorded the
  asymmetry and the fact that no current route exists, not a recommendation of which container.

## Files written by this seat

* `.ufo/waves/round-84/w1/ScoutLoci.md` — this report.
* `.ufo/waves/round-84/w1/ScoutLoci/receipts/` — `anchors.json`, `anchors.txt`, `anchors.py`,
  `verdict_relevance.json`, `c2-base.json`, `c2-at-head.json`, `probe.py`,
  `freeze-gate-head.json`, `freeze-gate-base.json`, `freeze-gate-at-head.json`,
  `attr-audit-edited.json`, `c1-precheck-head.json`, `c1-precheck-at-head.json`.

Scratch dir `/fast/scratch/hyaku/kaidoku-r84/ScoutLoci/` was removed after copying the receipts
above; `/fast/scratch/hyaku/kaidoku-r84/ScoutLoci2/` (the post-integration re-verification
scratch) was removed on the same pass. No file outside `.ufo/waves/round-84/w1/ScoutLoci/` and
those scratch paths was written; no git or jj mutation was made in the lane tree. The private
clone used for the F8/F9 disclosure experiment was created under my scratch dir and deleted with
it; it was never a lane path.
