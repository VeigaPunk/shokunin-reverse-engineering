# R39C1AxisFit — axis fit, control reachability and clause completeness of the DRAFT R39-C1

**Verdict: DEFECTS FOUND.** Four of them block or weaken the freeze: (1) the draft's symlink
classification sentence, implemented with any POSIX normaliser, calls K1 **in-tree** and would
complete an honest run as an honest-stop (d.0); (2) a copy-the-round-38-receipts control with
genuine K5/K6 present reaches `carriers_matched == 6` (b); (3) K5/K6's new edge classes exist in
the wave dispatch but in no frozen artifact (c); (4) both documents still assert
"big-endian stays Frontier" and the predicate never binds their retraction (e). The claim's
*form* is axis-correct — a Frontier → Core move is the coverage unit the round-38 closure itself
used — and every defect is one clause, not a new carrier set.

Evidence for every finding is in
`.ufo/waves/round-39/w1/artifacts/R39C1AxisFit/` (this report cites file names only).

---

## 0. What I read and ran

| # | command | exit | note |
|---|---|---|---|
| 1 | `cat plans/round-39-claims.md` | 0 | the draft under attack |
| 2 | `sed -n '1,80p' corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` | 0 | ground round 38 already holds |
| 3 | `grep -n 'unpublished-entry' -A30 dist/firmware/FirmwarePublication.js` (rea-agents 6.5.0) | 0 | gap emitter: every entry whose `kind !== "file"` |
| 4 | `sed -n '1,110p' <unblob 26.6.4>/unblob/extractor.py` + `file_utils.is_safe_path` | 0 | `fix_symlink`: kept/rewritten vs removed |
| 5 | `grep -n semanticProjection -A25 dist/domain/evidence.js` | 0 | `parameters` is inside the hashed projection |
| 6 | `node tools/round-27/xpin-attribute.mjs --pkg65 <6.5.0> --pkg67 <6.5.0> K{1..4}.wrapped.json` | 0 | all four r38 receipts **still recompute** (`both`) → `xpin-r38-receipts.txt` |
| 7 | same, with K1's `parameters.output_directory` rewritten to a `/kaidoku-r39/` path | 0 | id becomes `none` → a copied receipt cannot be re-pathed → `xpin-parameters-binding.txt` |
| 8 | `sasquatch-v4be -be -ll` on K1–K4 | 0 | link/special-file inventory → `carrier-audit.txt` |
| 9 | `python3 tools/round-37/gen-squashfs.py t out-be.sqsh --endian be --comp gzip` on a 5-link probe tree, then `sasquatch-v4be -be -ll` | 0 | a symlink whose target is a **directory** is silently dropped → `probe-gen-squashfs.txt` |
| 10 | `unblob -e ub-out out-be.sqsh` on the same probe | 0 | absolute link re-rooted and kept; escaping link removed (1 `MaliciousSymlinkRemoved`) → `probe-unblob-tree.txt` |
| 11 | `REA_UNBLOB_COMMAND=~/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware --format json --full-output out-be.sqsh <fresh outdir>` (my own dev carrier) | 0 | 3 kept links → **3** `unpublished-entry` gaps → `probe-rea-envelope.json`, `probe-rea-summary.txt` |

No REA run touched any round-37 carrier and no K5/K6 or held-out C2 carrier was built. Scratch
`/fast/scratch/hyaku/kaidoku-r39/R39C1AxisFit` is deleted at the end; the cited files are copied
into the artifacts dir.

---

## (a) Is Frontier → Core of ground measured last round a coverage move, or re-scoring?

**Answer: it is a legitimate coverage *surface* move, and its coverage *content* collapses to
re-scoring unless the new carriers' content is bound in the freeze.**

- The prompt's own test (`kaidoku-round-39.md` §6 item 9) names the surface: *"A coverage claim
  names the surface it moves (frontier → core, a new tool, operation or edge class) and the
  command that would show it unmoved."* C1 names PROVINCE:156-157 + the README Frontier bullets
  and shows them unmoved with the counter. That is the right shape.
- The round-38 closure uses the same unit: §2 R38-C1 records *"coverage unchanged … but no
  Frontier → Core move and score 10 → 10"*. So by the closure's own metric, the move C1 makes
  **is** the coverage delta, and its absence was the reason coverage did not move last round.
- The warning clause bites on the *measurement*: *"Re-scoring a rule the lane already holds on
  new inputs … is quality work, never coverage or depth."* The lane already holds the measured
  rule in two places:
  - `SKILL.md:1241` (round-36 LE table): *"Symlinks (and special files) are retained as metadata
    only … **Not** a sasquatch failure and **not** blocked recursion"* — i.e. "symlink gaps are
    not extraction failure" is a **prior holding**, not a round-39 discovery.
  - `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` §Symlinks: both
    outcomes (in-tree kept → gap; escaping removed → no gap), stated and measured, and the entry
    ends *"Standard BE v4 stays on the PROVINCE Frontier until a claim that states the symlink
    behaviour up front verifies."* R39-C1 is that pre-announced discharge, not a new measurement.
- Therefore the promotion is honest but cheap **unless** the round's measurement adds ground the
  corpus does not hold. As dispatched that ground exists (see (c)); as *drafted* it is not bound.

Consequence for the closure: with K1–K4 alone, a strict reading of §6 item 9 scores C1 as
quality (a rule re-scored on the same four inputs) and coverage would not move. With K5/K6
bound to the new edge classes it is a real (if modest) coverage claim.

**Smallest safe correction (a):** in the claims file, state which part of the rule is a prior
holding and which is new, so the knowledge entry cannot claim as discovered what `SKILL.md` and
the r38 entry already hold:

> The in-tree-symlink retention is the lane's prior holding (round-36 LE, `SKILL.md:1241`;
> round-38 BE entry §Symlinks). What round 39 adds and measures is: a non-gzip (compression id 2)
> BE v4 carrier, a BE carrier holding two in-tree symlinks at once (per-link gap cardinality), two
> escaping symlinks at a depth greater than one, and one carrier carrying both link classes in a
> single run.

---

## (b) Can a do-nothing or copy-the-round-38-receipts control reach the target?

**Do-nothing: no. Copy: yes — the control as drafted is scored on the wrong state.**

Measured: all four round-38 `after.json` receipts still recompute to their stored `ev_…` id
under the pinned 6.5.0 rule (`xpin-r38-receipts.txt`, exit 0, verdict `both`, four of four), and
every non-documentary binding of P39-C1 already holds on them (`carrier-audit.txt`):

| carrier | handler | extraction_failed | gaps | r38 published vs oracle |
|---|---|---|---|---|
| K1 | `squashfs_v4_be` | false | `[]` (its one link is **escaping**) | 5/5 |
| K2 | `squashfs_v4_be` | false | 1 × `unpublished-entry` on `var/lib/run-link` (**in-tree**) | 3/3 |
| K3 | `squashfs_v4_be` | false | `[]` (no links) | 4/4 |
| K4 | `squashfs_v4_be` | false | `[]` (no links) | 4/4 |

So the predicate's per-carrier clauses are satisfied *verbatim* by copying
`corpus/evidence/round-38/c1/K*/after.json` into `corpus/evidence/round-39/c1/K*/after.json`.
The draft's kill rule scores the copy control with *"K5/K6 absent"* (4/6) — that state fails only
because of the missing carriers. **The strong state — copies for K1–K4 plus genuine K5/K6 — is
6/6 and `met_target` true**, and "first added in a commit that descends from the freeze"
(`git log --diff-filter=A`) cannot distinguish a copy from a run.

`parameters` is inside the hashed `semanticProjection` (`dist/domain/evidence.js:168`), and I
measured that rewriting `parameters.output_directory` on the K1 receipt drops the recompute to
`none` (`xpin-parameters-binding.txt`). That gives a non-spoofable provenance binding for free.

**Smallest safe correction (b):** add one conjunct to P39-C1 and one selftest case.

> … and its `parameters.output_directory` lies under `$HYAKU_SCRATCH/kaidoku-r39/`
> (default `/fast/scratch/hyaku/kaidoku-r39/`).

Reason: the field is hashed, so it cannot be edited into a copied receipt without destroying the
id; a real round-39 run writes that root by construction (round-38 receipts carry
`/fast/scratch/hyaku/kaidoku-r38/l1-receipts/K<N>-after`). Red case: *"round-38 receipts
byte-copied for K1–K4 with genuine K5/K6 present → those four carriers unbound"*, exit 1.

**Honest limit (must be disclosed, not papered over):** this binding does **not** refuse
CTL-C1-3 (fabricated receipts with the id *re-minted* by the xpin rule). No receipt-only counter
can: the id authenticates self-consistency, not a run. The claims file should say so in one
sentence and drop "a fabricated receipt" from the kill rule (it is unscorable as written),
replacing it with "an *edited* receipt (published file or gap rewritten after the run) — id no
longer recomputes", which the counter does refuse and round-36's selftest already proves.

---

## (c) Do K5/K6 add discriminating power, or are they decoration?

**As dispatched: real discriminating power. As *frozen* (claims file + carriers.json): nothing —
the claims file states no content, so the freeze cannot bind it.**

The `w1-dispatch.json` seat text requires K5 = 2 in-tree relative symlinks + 1 escaping +
0-byte + >3-block + space + UTF-8 name, and K6 = `xz` + 1 in-tree + 2 escaping. Against the four
round-37 carriers that adds five things the corpus does not hold:

1. A **non-gzip compressor id** on BE v4 — K1–K4 all declare compression id 1 (gzip); K6
   declares id 2 (verified from the superblock: `superblock-compression.txt`). Caveat that must
   reach the claim text: `gen-squashfs --comp xz` writes id **2** while its body is a raw
   LZMA2 stream (`COMP = {'gzip': 1, 'xz': 2}`, `comp_bytes` uses `lzma.FORMAT_RAW` preset 6), so
   the carrier is a valid BE v4 image that *declares* LZMA, not a standard squashfs `-comp xz`
   image (which would declare id 4). `sasquatch-v4be` decodes it either way, but the claim must
   not say "xz".
2. **Two** in-tree links in one image → per-link gap cardinality. Measured: gap emission is per
   entry (`FirmwarePublication.js`, `unpublished.push` per `kind !== "file"`), and my probe with
   three kept links produced exactly three gaps. Every r38 carrier holds at most one link, so
   "exactly on the symlinks" was never discriminated from "at least one gap".
3. A second escaping link at depth (`../../../../…`) — K1's escaping link is at the root.
4. Both link classes in **one** run (K5) — no prior carrier holds an escaping and an in-tree link
   together, so "removal does not perturb the gap set of the retained link" is untested.
5. A UTF-8 non-ASCII name on BE (K2 holds a space, not a non-ASCII name).

But P39-C1 as drafted says only *"K5/K6 = new standard-BE v4 images built for this round before
the freeze"*. The counter reads `carriers.json` (id, path, sha256, oracle, symlinks, receipt) and
`symlinks.tsv` — a K5 that ended up with no links at all would still be frozen-compliant, and the
escalating clauses would go vacuous (see (e)).

**Smallest safe correction (c):** freeze the content requirement where the counter can read it,
not only in a dispatch prompt.

> Every carrier entry in `.ufo/waves/round-39/c1/carriers.json` carries
> `symlinks` (path to its frozen table) and `compression`; the counter asserts, over the frozen
> set: `in_tree >= 2`, `escaping >= 2`, at least one carrier with `in_tree == 2`, at least one
> carrier with superblock compression id `!= 1` (superblock bytes 20-21, BE u16), and per carrier
> `len(symlinks.tsv rows) == len(gaps)` where both are matched by relative-path suffix.

Reason: those five numbers are exactly the new ground; they cost one loop over two frozen files
and they are what makes the promotion a measurement rather than a replay.

Secondary (not a predicate change): K1–K6 are all images the lane wrote itself with
`tools/round-37/gen-squashfs.py` (K5 with a byte-patched copy of it, see change #5), so the
self-built share rises from 2/4 to 4/6. No third-party BE v4 writer exists (`mksquashfs` is
LE-only), so this is unavoidable; the mitigation already in
the wave is the independent reader (K3/K4's unblob fixtures plus `sasquatch-v4be`). Disclose it
in the entry rather than let the closure find it.

---

## (d) Is "no other gap" too strict or too loose, given the round-36 LE entry and K3/K4?

**On this carrier set it is neither — but it is silently conditional on a carrier property that
is not frozen, and it is too loose about *published* files.**

What the carrier inventory actually holds (`carrier-audit.txt`, `sasquatch-v4be -be -ll`):

| carrier | dirs | regular files | symlinks | special files |
|---|---|---|---|---|
| K1 | 5 | 5 (incl. 0-byte `empty`) | 1 — `link-to-hello -> ../hello.txt` (escaping) | none |
| K2 | 5 | 3 (incl. a name with a space) | 1 — `var/lib/run-link -> ../../a/run.sh` (in-tree) | none |
| K3 | 1 | 4 | 0 | none |
| K4 | 1 | 4 | 0 | none |

No device node, FIFO, socket or hardlink exists in K1–K4, and `tools/round-37/gen-squashfs.py`
can only emit `TYPE_DIR`, `TYPE_FILE`, `TYPE_SYMLINK` inodes, so K5/K6 cannot introduce a
special-file `unpublished-entry` gap. "No other gap" is therefore *correct* here: REA's emitter
creates a gap for every non-regular entry, and there are none besides the symlinks.

Three defects around the clause:

1. **It is conditional on a rule that is not frozen.** Round 36's LE entry (`SKILL.md:1241`)
   lumps *"Symlinks (and special files)"* together; if a K5/K6 builder ever adds a FIFO the
   predicate would reject a correct run. State, in `carriers.json`'s `frozen_note`: *the frozen
   generator writes only directories, regular files and symlinks; no frozen carrier holds a
   device node, FIFO, socket, hardlink or cyclic symlink.* (Absolute targets: no frozen carrier
   holds one — but state the rule below rather than leave a later round to guess.)
2. **A symlink whose target is a directory is invisible to the builder and fatal to the oracle.**
   Measured: `gen-squashfs.py` walks with `followlinks=False`, so a directory symlink lands in
   `dnames`, is never yielded, and the `islink` branch never sees it — my probe tree's
   `dir-link -> dir` is **absent** from the built image and from the `sasquatch-v4be -ll`
   listing (`probe-gen-squashfs.txt`). A source-derived oracle alone would then predict one
   in-tree link (one gap) that the image cannot produce, and an honest REA run would be scored a
   miss. Freeze the constraint above **and** ship both halves of the pair K6 built: tables
   derived from `src/` (the independent statement of intent) **plus** a build-time assert that
   the built image equals them (file sha256/size, link count, link targets, no extra
   non-regular entry). An image-only derivation cannot observe a silently dropped entry — the
   image would simply agree with itself.
3. **Too loose about extra published files.** The predicate requires every oracle file to be
   published and forbids a path at an escaping symlink's name, but says nothing about any other
   path. Add: *publishes no relative path outside the set {oracle regular files} ∪ {the single
   `<firmware.bin>_extract/` prefix}*. It costs nothing — it already holds on all four r38
   receipts (5/5, 3/3, 4/4, 4/4 files, no extras) — and it closes a "materialise the escaping
   target under a different name" state.

Provenance note for the knowledge entry: because retention is a prior holding (round-36 LE), the
round-39 entry must cite `SKILL.md:1241` and the r38 entry for that half, and the rows opened
this round only for the *mechanism* (`unblob/extractor.py::fix_symlink`,
`FirmwarePublication.js` gap emission). Claiming both halves as new would inflate expansion
credit — exactly the provenance defect the closure spot-checks.

Rule text the measured behaviour supports (my probe, 5 links, one REA run; the `abs-up` row is
`R39C1SymlinkK1K4`'s dev carrier — code path consistent, not re-measured by this seat):

| link | outcome | gap |
|---|---|---|
| relative, resolves inside root, target **exists** | kept | 1 |
| relative, resolves inside root, target **missing** (dangling) | kept | 1 |
| relative, resolves **outside** root | removed (`MaliciousSymlinkRemoved`) | 0 |
| **absolute, re-base stays under the root** (`/etc/passwd`) | kept, **rewritten** to `etc/passwd` | 1 |
| **absolute, re-base still ascends** (`/../out.txt`) | removed (`MaliciousSymlinkRemoved`) | 0 |
| target is a **directory** | n/a — the frozen generator cannot emit it | — |

`fix_symlink` strips exactly one leading `/` and then applies the same non-clamping walk, so
"absolute ⇒ in-tree" is **false**; the correct sentence is "one leading `/` is dropped, the
remainder is re-based at the image root, and the normal in-tree/escaping test then applies".

### d.0 — freeze-blocking: the draft's resolution sentence flips K1

The draft says `symlinks.tsv` classifies "resolved POSIX-style against the link's own directory
inside the image root". Implemented with any POSIX normaliser, that **clamps** a leading `..` at
`/`:

```
posixpath.normpath('/../hello.txt') == '/hello.txt'
posixpath.normpath(posixpath.join('/', '../hello.txt')) == '/hello.txt'   # K1 -> in-tree
posixpath.normpath(posixpath.join('/var/lib', '../../a/run.sh')) == '/a/run.sh'  # K2 -> in-tree (right)
```

K1's `link-to-hello -> ../hello.txt` sits at the image root, so a clamping classifier calls it
**in-tree**, the predicate then demands one `unpublished-entry` gap on it, and K1's genuine
receipt has none (it is removed as escaping — `MaliciousSymlinkRemoved`, `carrier-audit.txt`).
The frozen rule would manufacture an honest-stop on a correct run.

Fix: define the walk, not POSIX: split the target on `/`, start at the link's own directory
inside the image root, pop one directory per `..` and **record an escape the moment the walk
would ascend above the root** (never clamp). `R39C1SymlinkK1K4` implements exactly this in
`symlink-tables.py:classify()` and asserts K1 = escaping, K2 = in-tree.

---

## (e) Universal clauses the counter does not enumerate

1. **Vacuous symlink clauses.** *"carries extraction gaps … exactly on the frozen oracle's
   in-tree symlinks"* and *"publishes no path for the oracle's escaping symlinks"* are both
   satisfied by an empty symlink table. Nothing forces any carrier to hold an escaping link, and
   a builder whose escaping link targets a directory gets it silently dropped (see d.2). Fix:
   the non-emptiness assertion in (c).
2. **"a round-39 frontier note supersedes the big-endian part of the Frontier bullet" is not
   enumerable as written**; the counter seat reduces it to *"a line containing `Round-39 frontier
   note` naming the entry stem"*. But `PROVINCE.md:157` still reads `big-endian/AVM stays here`
   and `:376` still reads `Big-endian SquashFS stays Frontier.` A dated note does not retract
   either sentence — round 38 added exactly such a note and left both in place. Fix: bind
   `grep -c 'big-endian/AVM stays here' == 0` and `grep -c 'Big-endian SquashFS stays Frontier' == 0`
   at the measured revision, plus the existing note+stem check.
3. **`corpus/README.md` `## Frontier` is not bound at all.** The draft's only README binding is a
   coverage-map row naming the entry stem, which is the *knowledge map*, not the frontier list.
   Lines 238-239 still assert `Still frontier: big-endian/AVM (\`sasquatch-v4be\`)` and `Still
   frontier: standard BE v4 promotion, AVM-BE, vendor-mangled images.` The counter can report
   `met` while the lane's own map contradicts itself. Fix: bind both literals absent inside the
   `## Frontier` section (superseded by a dated note naming the stem), and keep the coverage-map
   row binding.
4. **"no failed chunk" is undefined.** Define it as `chunks[].extraction_failed == true` (all four
   r38 chunks are `false`). Wide reading would also catch K1, whose `diagnostics[]` carries a
   `MaliciousSymlinkRemoved` **WARNING** — a legitimate escaping-link removal, not a failure.
   Say so, or the K1 leg is refused by an over-broad reading.
5. **"no frozen C1 path changed after the freeze"** is only enumerable through the frozen list:
   name it (`plans/round-39-claims.md`, `tools/round-39/c1-counter.py`, `tools/round-39/c1-run.sh`,
   `.ufo/waves/round-39/c1/carriers.json`, every carrier/oracle/symlinks file it lists) and keep
   the counter's `exit 2 frozen_path_changed` — that is the R38-CL4 answer (drift blocks the
   score).
6. **Extra published files** — see (d.3).
7. **Exit-code discipline.** The "command that shows it unmoved" says *"exits non-zero"*. It must
   be **exit 1** (a missing receipt is a failed binding), never exit 2 (unevaluable): otherwise
   the do-nothing control is not a scored control. The round-38 counter already implements this
   (`after_present false → matched false`); state it in the claims file so the freeze pins it.

---

## Exact wording changes proposed (each with its reason)

| # | draft text | proposed text | reason |
|---|---|---|---|
| 1 | "the committed round-39 REA `extract-firmware` after-receipt … first added in a commit that descends from the freeze" | + "**and whose `parameters.output_directory` lies under `$HYAKU_SCRATCH/kaidoku-r39/`**" | (b): the strong copy control reaches 6/6 without it; the field is hashed, so it cannot be forged by editing (`xpin-parameters-binding.txt`) |
| 2 | "carries extraction gaps of kind `unpublished-entry` exactly on the frozen oracle's in-tree symlinks and no other gap" | "the multiset of `extraction_gaps` equals exactly one `unpublished-entry` per frozen `in-tree` row of `symlinks.tsv`, matched by relative-path **suffix**, and no gap of any other kind; over the frozen set `in_tree >= 2`, `escaping >= 2`, at least one carrier with `in_tree == 2`, at least one carrier with superblock compression id `!= 1`" | (c)(e): makes the cardinality and the new edge classes binding, not prose; measured per-link emission. Bind `!= 1`, **not** `== 2 (xz)`: `gen-squashfs --comp xz` writes id 2 (LZMA-declared, LZMA2 body) and a real `mksquashfs -comp xz` image would write id 4 |
| 3 | "publishes every regular file of the frozen independent oracle (same relative-path suffix, same sha256)" | + "**and publishes no other relative path** (after stripping the single `<name>_extract/` root)" | (d.3): closes extra-file states at zero cost — already true on K1–K4 |
| 4 | (symlink rule) "a symlink whose target resolves inside the extraction root is kept as metadata …, a symlink that escapes is removed …" and the oracle clause "resolved POSIX-style against the link's own directory inside the image root" | + "**classify by a non-clamping lexical walk from the link's own directory inside the image root: one `/` step per component, one directory popped per `..`, and an escape recorded the moment the walk would ascend above the root (never clamped — a POSIX normaliser turns K1's `../hello.txt` into in-tree and would demand a gap K1 does not have). Resolution is path resolution, not existence: a dangling in-root link is kept and gapped. An absolute target has exactly one leading `/` stripped and is then re-based at the image root — kept+rewritten if the remainder stays under the root, removed if it still ascends. The frozen generator cannot emit a directory-target, device, FIFO, hardlink or cyclic entry, so no frozen carrier carries one**" | (d.0)(d.1): measured; the draft's wording is a freeze-blocking misclassification, not a nuance |
| 5 | "K5/K6 = new standard-BE v4 images built for this round before the freeze" | "K5 = BE v4 **gzip**, **two** in-tree relative symlinks + **one** escaping; K6 = BE v4 **compression id 2**, **one** in-tree + **two** escaping; every link targets a regular file; tables derived from `src/` **and** asserted equal to the built image at build time; `kind` names the writer's sha256 (K5 was built with a byte-patched `gen-squashfs.py` — the in-tree tool corrupts non-ASCII directory entries, so a stock rebuild of K5 is not byte-identical)" | (c): the dispatch already says this; the freeze must, or the requirement evaporates. Writer pin: `R39C1CarrierK5` measured the in-tree generator's non-ASCII `name_size` bug |
| 6 | "a round-39 frontier note supersedes the big-endian part of the Frontier bullet" | "`PROVINCE.md` contains no `big-endian/AVM stays here` and no `Big-endian SquashFS stays Frontier`, contains a dated `Round-39 frontier note` naming the entry stem, **and** `corpus/README.md` `## Frontier` contains no `Still frontier: big-endian/AVM` and no `Still frontier: standard BE v4 promotion`" | (e.2)(e.3): the surface actually moved is the sentence, not the note; today both documents still assert BE is Frontier |
| 7 | kill rule: "a fabricated receipt" | "an **edited** receipt (a published file or gap rewritten after the run) — id no longer recomputes. A wholesale fabrication with a re-minted id is refused by no receipt-only counter; the defence is the closure's independent re-run, and this claim does not claim otherwise" | (b): as written the control is unscorable, and CTL-C1-3 proves the class is reachable |
| 8 | kill rule: "round-38 receipts copied into the round-39 paths for K1–K4 with K5/K6 absent" | same, **plus** "and, scored with K5/K6 present and genuine, the four copied carriers are unbound by the `parameters.output_directory` binding" | (b): the control must be scored on the state a cheater would actually build |
| 9 | "Command that shows it unmoved: the C1 counter at the base exits non-zero" | "…exits **1** (a missing receipt is a failed binding; exit 2 is only for unevaluable inputs)" | (e.7): keeps the do-nothing control scorable |

---

## Impacted axes

| axis | impact | why |
|---|---|---|
| **coverage** (claimed) | at risk, repairable before the freeze | as drafted the promotion rests on replays of ground the corpus already holds (a) and its new edges are unpinned (c); with changes 1–3, 5, 6 the move is measured surface change, not bookkeeping |
| **depth** (not claimed) | no harm; two facts belong in the C1 entry | per-link gap cardinality and the dangling/absolute link outcomes are cheap depth the entry should carry rather than lose |
| **calibration** | no impact | no SCORECARD/SHONEN statement is touched; the r38 score rows stay byte-identical |
| **operability** | no impact | no tool is edited by this seat; `c1-counter.py` gains two checks (changes 1, 2) and stays self-tested |
| **quality** | improves | changes 6 and 9 remove two self-contradicting/unevaluable statements from the frozen predicate |

Cross-claim note sent to `R39C2AxisFit` (corroborated by them and by my probe envelope):
`MaliciousSymlinkRemoved` is the only signal separating `escaping-symlink-removed` from `clean`
(both have `extraction_gaps == []`), and its `link`/`target` fields are **absolute temp-dir paths
resolved at run time** (measured; round-38 K1 carries a `/tmp/rea-firmware-XXXX` path). Three
consequences for C2: any rule keyed on that text or on its path shape is non-deterministic across
runs and will fail a held-out seed it was not tuned on (key on `report.__typename__` presence
only); one typename covers **both** a symlink loop (`extractor.py:59`) and a traversal removal
(`:82`), so a class named "escaping" is only sound if the generator excludes loop carriers; and a
single envelope can carry **both** an `unpublished-entry` gap and the diagnostic (my probe has
three gaps plus one removal), so the class list is a product, not a partition, and a first-match
triage table would label by row order.

## Checked and cleared (no defect)

- **No special files in K3/K4**: verified by listing both images — 4 regular files each, zero
  links, zero device/FIFO/socket/hardlink. The round-36 LE entry's *"and special files"* wording
  is over-broad for this set but harms nothing.
- **`unpublished-entry` for in-tree symlinks is not a regression**: it is exactly what round 36
  measured for LE (`.DirIcon`, `nvim.png`), and round-38's *stricter* "no gaps at all" was the
  anomaly. Relaxing it to the symlink set restores the lane's own rule.
- **K1's zero-byte file** is published and hashes to `e3b0c442…` — the oracle row is sound.
- **Subject digests** of all four r38 receipts equal the frozen `carriers.json` pins
  (`carrier-audit.txt`).
- **Cold-start evidence set is not thin**: six frozen carriers, a separate `symlinks.tsv` per
  carrier, before/after arms for K1–K4 from round 38, and K5/K6 never touched by REA before the
  freeze. The anti-tuning property of that last point is preserved only if nobody runs REA on
  K5/K6 pre-freeze — the wave text already forbids it (dev checks by `sasquatch-v4be -be` only).

## Artifact index (`.ufo/waves/round-39/w1/artifacts/R39C1AxisFit/`)

| file | what it establishes |
|---|---|
| `carrier-audit.txt` | K1–K4 image inventory (dirs/files/links, no specials) and every r38 after-receipt fact (handler, `extraction_failed`, gaps, files, diagnostics, `parameters.output_directory`, subject sha256) |
| `xpin-r38-receipts.txt` | the four r38 receipts still recompute to their stored ids under the pinned rule (`both`, exit 0) — the copy attack is live |
| `xpin-parameters-binding.txt` | rewriting `parameters.output_directory` breaks the id (`none`) — the proposed binding cannot be forged by editing |
| `probe-carrier.sqsh` (sha256 `f17a20fe…57ca`, 522 B), `probe-unblob.log` | the dev carrier itself and unblob's verbose log, so the probe is reproducible byte-for-byte |
| `probe-gen-squashfs.txt` | a directory-target symlink is silently dropped by the frozen generator; an absolute target is preserved verbatim |
| `probe-unblob-tree.txt` | unblob keeps the absolute link re-rooted and the dangling link; removes the escaping one (1 `MaliciousSymlinkRemoved`) |
| `probe-rea-envelope.json`, `probe-rea-summary.txt` | REA on that dev carrier: 3 kept links → 3 `unpublished-entry` gaps, 2 files published, coverage `partial`; **one envelope carries both a gap and a `MaliciousSymlinkRemoved` diagnostic** |
| `superblock-compression.txt` | compression ids: K1–K4 = 1 (gzip), K6 = 2; `gen-squashfs` `COMP = {'gzip':1,'xz':2}`; and the POSIX-clamping arithmetic that flips K1 to in-tree |

## Peer corroboration received during this seat (and what changed)

| from | claim | effect on this report |
|---|---|---|
| `R39C1SymlinkK1K4` | an **absolute** target is not always in-tree: `/hello.txt` is kept+rewritten but `/../out.txt` is removed, because unblob strips one `/` then walks without clamping | change #4 rewritten and the rule table's absolute row split in two (peer-measured on `dev2-carrier`; my code reading of `fix_symlink` is consistent) |
| `R39C1SymlinkK1K4` | a POSIX normaliser clamps `..` at `/`, so the draft's sentence flips K1 to in-tree | promoted to **d.0** (freeze-blocking), with my own arithmetic as evidence (`superblock-compression.txt`) |
| `R39C1CarrierK6` | `gen-squashfs --comp xz` writes compression id **2**, not 4 | (c) item 1 and change #2/#5 reworded; the claim must not say "xz" |
| `R39C1CarrierK5` | in-tree `gen-squashfs.py` corrupts non-ASCII directory entries (`name_size` from character count); K5 needed a patched writer | change #5 now requires the writer's sha256 in the frozen `kind` |
| `R39C2AxisFit` | (C2-scope) `MaliciousSymlinkRemoved` covers both symlink loops and traversal, and an envelope can carry a gap **and** the diagnostic | cross-claim note below extended; my probe envelope is direct evidence for their "class list is not a partition" finding |
