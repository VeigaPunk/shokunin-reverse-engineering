# R39C2AxisFit — attack on DRAFT R39-C2 before the freeze

**Verdict: DEFECTS FOUND.** R39-C2 stays an axis-fit *depth* claim only after three repairs: (F1) the
new craft block must carry a resolvable `corpus/knowledge/<entry>.md:N-M` citation or the depth axis
**regresses** 10.0 → 9.44; (F2/F3) the 7-class "first-match" list is **not a partition** — two draft
classes are indistinguishable in the typed envelope and one carrier legitimately carries two class
signals; (F4/F5) `body-extractor-failure` as drafted is unreachable while the real body-damage
outcome is *silent content corruption with `ok:true`*, and the AVM/body pair needs the retained
command's `-be` token, not the stderr text. Novelty is also narrower than stated: 6 of the 7 classes
already have a base-revision statement in the lane (F8). All evidence below is from development
carriers I built in scratch from my own fresh trees; no K5/K6, no held-out carrier, no lane write.

## Method (exact)

Scratch `S=/fast/scratch/hyaku/kaidoku-r39/R39C2AxisFit`. Fresh tree of my own (5 regular files,
1 empty file, 1 empty dir; a second tree adds one in-tree and one escaping symlink), then
`python3 tools/round-37/gen-squashfs.py treeA be-clean.sqsh --endian be --comp gzip` (and `--endian avm`),
plus byte-level variants derived from `be-clean.sqsh`. Rebuild recipe: `artifacts/R39C2AxisFit/dev-carriers.sh`,
pins `dev-carriers.sha256`. Twelve REA runs, each a fresh output dir, all exit 0:

```
cd "$S" && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 \
  extract-firmware --format json --full-output be-<n>.sqsh out-<n>        # n = clean avm sym trunc bodyflip magic zeroed inodeptr rootino bytesused
PATH="$S/bin-nov4be:/usr/bin:/bin" ... be-clean.sqsh out-depbe            # only `sasquatch` on PATH  -> env-depbe.json
PATH="$S/bin-v4be:/usr/bin:/bin"   ... be-clean.sqsh out-deple            # only `sasquatch-v4be`      -> env-deple.json
```

Typed projection of all twelve: `artifacts/R39C2AxisFit/projection.tsv`. Depth-recipe control:
`artifacts/R39C2AxisFit/depth-recipe-control.py|.txt` (base rev `a2f64e1d`).

| dev carrier | files | chunks/failed | gaps | diags | `-be` | unpub | coverage | class the draft would assign |
|---|---|---|---|---|---|---|---|---|
| clean | 5 | 1/0 | — | — | — | — | complete | clean |
| deple (v4be only) | 5 | 1/0 | — | — | — | — | complete | clean *(no dep class)* |
| zeroed (data region) | 5 | 1/0 | — | — | — | — | complete | **clean — but 4/5 published sha256 differ** |
| bodyflip (inode table) | 5 | 1/0 | — | — | — | — | complete | clean (bytes untouched) |
| sym (in-tree + escaping link) | 5 | 1/0 | unpublished-entry | MaliciousSymlinkRemoved | — | symlink | partial | **both symlink classes at once** |
| avm (`bytes_used == mkfs_time`) | 0 | 1/1 | extractor-failure | ExtractCommandFailedReport | **no-be** | — | partial | avm-marker-be-dropped |
| inodeptr (`inode_table_start=0xffffffff`) | 0 | 1/1 | extractor-failure | ExtractCommandFailedReport | has-be | — | partial | body-extractor-failure |
| rootino (`root_inode` bogus) | 0 | 1/1 | extractor-failure | ExtractCommandFailedReport | has-be | — | partial | body-extractor-failure (2nd stderr) |
| depbe (v4be hidden) | 0 | 1/1 | missing-extractor-dependency [`sasquatch-v4be`] | ExtractorDependencyNotFoundReport | — | — | partial | dep-missing-be |
| trunc (734 B file, `bytes_used` 934) | 0 | **0** | — | — | — | — | complete | no-squashfs-chunk |
| magic (`sqsh`→`sqsx`) | 0 | **0** | — | — | — | — | complete | no-squashfs-chunk |
| bytesused (`bytes_used=0x7fffffff`) | 0 | **0** | — | — | — | — | complete | no-squashfs-chunk |

## Findings

### F1 (blocking, axis) — the depth recipe regresses unless the new craft block cites `corpus/knowledge`

The depth axis is measured by command A over `SKILL.md` §Queue-drain craft (`SCORECARD.md:24`):
rule blocks are the `^- \*\*` bullets and each must carry a resolvable `corpus/knowledge/*.md[:N[-M]]`.
At `a2f64e1d`: **17 rules, 17 resolved, depth 10.0**. I scored the draft's own move against that recipe:

```
base craft                            {'rule_blocks': 17, 'resolved': 17, 'depth_score': 10.0}
base + 18th block, external cites only {'rule_blocks': 18, 'resolved': 17, 'depth_score': 9.44, 'unresolved': [18]}
base + 18th block, + knowledge cite    {'rule_blocks': 18, 'resolved': 18, 'depth_score': 10.0}
```

The draft's table is "each row source-cited", and every source it names is external (unblob handler,
REA `FirmwarePublication.js`, SOURCES rows). A block that cites only those adds +1 to the denominator
and +0 to the numerator: **the depth axis falls to 9.44, i.e. this depth claim would lower the axis it
claims to work**. Fix (one clause): the block must cite `corpus/knowledge/2026-10-26-…md:N-M`
(round 39's own knowledge entry) *in addition to* its external per-row sources, and the target must be
`rule_blocks == 18 and resolved == 18` at the measured revision.

### F2 (blocking, partition) — the class list is not a partition; one carrier holds two class signals

`sym` (one in-tree link, one escaping link) yields **both** an `unpublished-entry` gap and a
`MaliciousSymlinkRemoved` diagnostic in a single envelope (`projection.tsv` row `sym`). The draft
declares `escaping-symlink-removed` and `in-tree-symlink-metadata` as separate classes and scores with
a *first-match* table, so the label of such a carrier is decided by row order, not by the envelope.
A generator label for it is then a convention, and the predicate "the class label its frozen generator
assigned" certifies the convention. Also confirmed by R39C1AxisFit (message of 2026-10-26): an
in-root **dangling** link is kept and yields a gap, and an **absolute** link is re-rooted
(`/etc/passwd` → `etc/passwd`) and also yields a gap — so "in-tree" is a misnomer for two of the
three non-escaping causes. Fix: make the symlink surface its own 4-combination product
`(gap present?) × (MaliciousSymlinkRemoved present?)` — `none`, `retained`, `removed`, `both` — name
the causes (in-tree / dangling / absolute-re-rooted vs escaping / recursive loop), and forbid a
first-match order over co-occurring signals.

### F3 (blocking, separability) — `no-squashfs-chunk` is the same envelope as truncation and over-claimed size

`trunc`, `magic` and `bytesused` are **identical in every typed field** — `ok:true`,
`files 0`, `chunks 0`, `gaps []`, `diagnostics []`, `published_bytes 0`, `coverage "complete"` — and
differ only in `selection.length` (734 vs 934) and the carrier digest, which is not a class signal.
Two of them therefore cannot both be classes under an envelope-only read. Note the trap that makes
this worth a row: `ok:true` + `coverage:"complete"` + zero files is *not* a clean run of an empty
filesystem; it is "no handler matched". Only `data.raw_result.report[].reports[].magic`
(`"data"` vs `"Squashfs filesystem, big endian, version 4.0, … 934 bytes"` vs `… 2147483647 bytes`)
separates the three, and that is a locale-dependent libmagic string. Fix: one class
`no-handler-matched` with three named causes and an explicit **"not decidable from the envelope
alone"** row (or admit `FileMagicReport` as a declared fallback signal with its format dependence
stated; never both as separate classes).

### F4 (blocking, reachability) — `body-extractor-failure` as drafted is unreachable; the real risk is silent corruption

Zeroing the whole data region (`bytes 96..200`) still publishes **5 files, `coverage:"complete"`,
`ok:true`, no gap**, with **4 of 5 published sha256 differing from the clean extraction**
(`bin/run 29900186…→60daa3a5…`, `hello.txt 2b636191…→01d448af…`; same sizes). A 0xFF flip inside the
inode table changed nothing at all (all hashes equal). `sasquatch-v4be` fails only on **superblock
pointer damage the handler never validates**: `inode_table_start=0xffffffff` →
`read_filesystem_tables: inode table start too large in super block`; bogus `root_inode` →
`Read on filesystem failed because EOF / read_block: failed to read block @0xe00a`. Fix: define the
class as "superblock pointer damage for fields the BE handler does not validate
(`squashfs.py:516-525` matches magic + `s_major/s_minor` only; `:77-98` reads `bytes_used` only)" and
add a limit row: `extraction_failed:false` + files published establishes **publication, not integrity**
— the envelope cannot see the corruption F4 demonstrates.

### F5 (blocking, discriminator) — the AVM/body pair needs the `-be` token; the stderr text is a trap

Both `avm` and `inodeptr`/`rootino` carry `kind: extractor-failure`, `handler: squashfs_v4_be`,
`published_bytes 0`. They differ in `diagnostics[].report.command`: the AVM branch's command has **no
`-be`** (unblob withholds it when `bytes_used == mkfs_time`, `squashfs.py:47-50`), the pointer-damage
runs' commands **have `-be`**. But the AVM stderr says "suggests a SquashFS image of a different
endianess" while the `inodeptr` stderr — with `-be` passed — says **"Reading a different endian
SQUASHFS filesystem"**: any substring rule on `different endian` mislabels the pair. Two further
mechanics the table must state: `report.stderr` is **base64** in the envelope, and the gaps are sorted
by `[input_path, kind, provider_id, relative_path]` (`FirmwarePublication.js:47-52`), so "first gap"
is a sort order, not a severity or precedence order. Fix: row key = `gap.kind == extractor-failure`
**AND** the `-be` token presence in the retained command (decode stderr only to *name* the cause,
never to decide the class).

### F6 (blocking, reproducibility) — the dependency classes are environment-scoped, and one instance is a no-op

`depbe` (only `sasquatch` on PATH) and `clean` share the **same subject digest** `3a3a082d5afc` — the
gap is a property of the PATH the unblob child sees, not of the carrier. `deple` (only
`sasquatch-v4be` on PATH) is a **clean extraction with no gap at all**: the dependency gap names only
the binary the selected handler invokes (`get_dependencies()` returns both, `squashfs.py:68-69`, but
only the chosen executable is checked). A held-out manifest that freezes carriers only cannot
reproduce these two classes; and a table keyed on "a dependency is missing" without the handler is
wrong. Fix: the manifest freezes `(carrier, PATH environment)` per envelope, and the class set names
the two instances *and* the negative instance `deple` as its own row (it is the counterexample that a
naive dependency row fails).

### F7 (seed) — the freeze-hash seed blocks pre-freeze peeking but is a selection channel unless the generator is total

Who can see it: anyone after the freeze — the generator is in-repo and deterministic, so every held-out
carrier is publicly reproducible post-freeze (intended). The residual hole is upstream: the freeze
commit hash is a function of the table bytes, and a commit hash is *iterable* — the author can
rehearse freeze commits in a scratch repo (deterministic `heldout-gen.py`, no REA needed) and keep the
attempt whose derived set is easiest, since the labels are assigned by generation and the author
already knows every class's feature projection from the lane's own receipts. "Could a later commit
re-freeze?" — only if nothing names the first-add commit: QUALITY 33/79/80 already say the freeze is
the commit that first adds `claims.json` and a later amendment is *reported, never adopted*, but the
draft never invokes them. Fix: (i) name the first-add freeze and run
`tools/round-38/freeze-drift.py --freeze <first freeze> --rev <measured>` over claims, `SKILL.md`,
`tools/round-39/sqfs-triage.py` and `tools/round-39/heldout-gen.py` with the receipt; (ii) disclose
the number of commits that touched the freeze path before the measured revision; (iii) make the seed
choice worthless by requiring the generator to be **total and self-checking** — for each class it
emits instances where that class's declared features are present and every other class's declared
features are absent, and it refuses (non-zero exit) rather than emit an ambiguous instance. Every
seed then yields an equivalent, non-degenerate set, and grinding buys nothing. (iv) State the pre-seen
count (QUALITY 44): the class *shapes* of 6 of 7 classes are already in the lane (F8), so the held-out
test measures transcription fidelity for those rows.

### F8 (novelty) — 6 of 7 classes already have a base-revision statement; the delta is 1–2 rows

`git grep -c -I -E '<spelling>' a2f64e1d -- PROVINCE.md SKILL.md corpus/README.md corpus/knowledge`:

| signal | hits at base | where |
|---|---|---|
| `squashfs_v4_be` | 1 + 3 | `corpus/README.md`, `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` |
| `MaliciousSymlinkRemoved` | 1 | same r38 entry (the escaping-link outcome is already stated) |
| `sasquatch-v4be` | 3/2/4/2/6/1/9/1 | PROVINCE, SKILL, README, r36+r38+r4u-03 entries, format matrix, dependency entry |
| `missing-extractor-dependency` | 1/1/3/1/1 | PROVINCE, SKILL, r36 entry, r38 entry, dependency entry |
| `unpublished-entry` | 3/1/4/6/3 | PROVINCE, SKILL, README, r36 entry, r38 entry |
| `ExtractCommandFailedReport` | **0** | — |
| `extractor-failure` (as a gap kind) | **0** | — |

The r38 entry already says the `-be` flag is dropped on `bytes_used == mkfs_time` (S114), names
`MaliciousSymlinkRemoved` for the escaping link, `unpublished-entry` for the retained link, and
`missing-extractor-dependency` [`sasquatch-v4be`] for the before arm. SKILL `1231-1243` holds four
more. So the classes `clean`, `in-tree-symlink-metadata`, `dep-missing-le` are **round-36 rows**;
`escaping-symlink-removed` and `dep-missing-be` and the AVM flag-drop are **r38 knowledge prose**;
only the `ExtractCommandFailedReport` / `extractor-failure` taxonomy (F4, F5) is unstated ground — and
my evidence splits it into two signatures plus one trap. New ground ≈ 1–2 rows of 7, not 7.

### F9 (read scope + leak controls) — "reading only the table" never says which envelope fields

The predicate says the interpreter reads "only the SKILL.md craft-section triage table". It never
declares the envelope field set, and the lane's two receipt shapes differ: round-38 receipts are REA
`data` objects, the AVM probe is a full CLI envelope (`{ok,data,meta}`). Without a declared read set
F3's answer flips (normalized-only: three cases collapse; with `raw_result`: they separate), and a
manifest holding class labels sits beside the envelopes. Fix: declare the read set as
`data.normalized_result.{chunks,files,unpublished_entries,diagnostics,extraction_gaps,coverage}` +
`data.subject.digest.sha256`, forbid the manifest, and ship two controls before data:
(i) **leak control** — hand the interpreter the manifest path; it must exit non-zero and print no
labels; (ii) **provenance control** — a table whose class labels are renamed must yield the renamed
labels, proving the labels come from the SKILL bytes and not from constants in the tool
(QUALITY 75's real risk: "a claim that leaves the surface unmoved is not a depth claim, whatever
instrument it lands").

## Answers to the assigned questions

**(a) Depth claim under QUALITY 75 / AXES depth?** Yes in *shape* — the table lives in the craft
section and an interpreter reads it, which is exactly "decision tables with real thresholds, named
error signatures, cited sources". But it fails row 75's *verification* clause as drafted: the claim
never checks the surface against the axis's own counting recipe, and F1 shows the move as written
**lowers** the depth score. Add the command-A clause (F1) and the two controls (F9) and it passes.

**(b) Seed = freeze commit hash.** It does prevent the table author from *seeing* the held-out
instances (the hash cannot exist before the freeze commit). It does **not** prevent seed *selection*:
the hash is a function of the table bytes and is iterable in a scratch repo, and the derived set's
labels come from the generator, so an author can pick the attempt whose draw is easiest without ever
running REA. A later commit cannot "re-freeze" once QUALITY 33/79 are invoked — the draft must invoke
them, plus the generator-totality requirement that makes the drawing irrelevant (F7).

**(c) Is a 7-class first-match table over envelope fields deep, or "reading the kind field"?** As
drafted, 5 of the 7 classes are decided by a **single enum/typename/string** (`clean`: everything
empty; `escaping-symlink-removed`: one `__typename__`; `in-tree-symlink-metadata`: one gap `kind`;
`dep-missing-be` and `dep-missing-le`: one `dependencies[0]`), two of those five restate C1's rule,
and the optional 8th (`no-squashfs-chunk`) is **zero-feature** — indistinguishable from its siblings
(F3). Exactly **one**
pair needs two features at once: `avm-marker-be-dropped` vs `body-extractor-failure` =
`gap.kind == extractor-failure` **×** `-be` token in the retained command — and that pair also carries
the named-error-signature content (the AVM equality cause, the "different endian" trap, the two
pointer-damage stderr signatures). That pair, plus the two limits rows (silent corruption, no-handler
matched) and the handler-scoped dependency counterexample, is where the depth actually is. The
decision thresholds to state are: `len(chunks) == 0` vs `> 0`; `chunks[].extraction_failed`;
`gaps[].kind`; `diagnostics[].report.__typename__`; `-be` token in `diagnostics[].report.command`;
`gaps[].dependencies[0]`; and the superblock equality `bytes_used == mkfs_time` as the *cause* behind
the `-be` token.

**(d) Separability from C1.** The *read sets* are separable; the **premises are not**. Two of C2's
classes (`in-tree-symlink-metadata`, `escaping-symlink-removed`) restate C1's symlink rule verbatim
(C1: in-tree → one `unpublished-entry` gap; escaping → removed, no gap), and C2's BE handler names are
C1's Core surface. If that rule is wrong, both claims fail together, and C2's depth credit partly
rides on C1's coverage work. C2 must either drop those two rows for symlink-independent traps (silent
corruption, no-handler-matched, `-be` withheld, `deple`) or state the shared premise explicitly as
C1's, scored independently.

**(e) What does the round-36 table already hold, and what fraction is new?** Held by
`SKILL.md:1231-1243`: dep-missing (LE, `dependencies ["sasquatch"]`), clean/all-published, opaque
container publication, `unpublished-entry` symlink metadata, AppImage chunk geometry, extra nested
carves, wrong verb/provider, forged envelope. Held by the r38 entry/prose: the `-be` drop on the AVM
equality, the escaping-link removal, the BE dependency name. New: only the `extractor-failure`
taxonomy. Fraction of the draft's 7 classes that is new ground: **≈1–2 of 7 (15–30%)**; 3 of 7 are
round-36 transcriptions (the draft's own kill rule names that as a stop, and it would not bite at 43%).

## Smallest safe corrections (drop-in wording)

1. *Surface moved* — append: "the block sits inside `## Queue-drain craft` (`SKILL.md:81-314` at the
   base: heading line 81, last non-blank line 314 per `SCORECARD.md:24`), starts `- **`, and carries a `corpus/knowledge/<round-39 entry>.md:N-M` citation in addition
   to its per-row external sources; at the base the recipe reports `rule_blocks 17, resolved 17`."
2. *Target* — replace with: "`matched == N`, every binding true, **and** the depth recipe reads
   `rule_blocks == 18 and resolved == 18` at the measured revision; the class set is the 4-value
   symlink product (none/retained/removed/both) × the 3 chunk outcomes (no-chunk, dependency-missing,
   extractor-failure) with `-be`-withheld and `-be`-passed split inside `extractor-failure`; every
   co-occurring-signal carrier takes the combination class, never a first-match label."
3. *Read set* — replace "reading only the SKILL.md craft-section triage table" with the explicit field
   list in F9, forbid the manifest, and add the leak and rename controls.
4. *Held-out* — add "the manifest binds `(carrier sha256, PATH environment)` per envelope; the
   generator is total (refuses ambiguous instances); no held-out REA run before the freeze; the
   pre-seen class-shape count is committed with the freeze."
5. *Kill rule* — add: "a `clean` row satisfied by a zeroed-content extraction (F4) is a stop; a
   first-match order that decides a both-signals carrier (F2) is a stop; a table whose only
   `corpus/knowledge` citation is absent (F1) is a depth regression, not a depth move."
6. *Freeze-integrity* — add "`freeze-drift.py --freeze <first freeze> --rev <measured>` over
   `plans/round-39-claims.md`, `SKILL.md`, `tools/round-39/sqfs-triage.py`,
   `tools/round-39/heldout-gen.py` prints zero commits (QUALITY 79/80; row 33 for first-add)."

## Limits of this review

Development carriers only; no held-out set was built or run, no K5/K6 was touched, and no lane file
was written outside this report and `artifacts/R39C2AxisFit/`. Twelve REA runs, all `ok:true`,
exit 0; the dependency probes changed only the child `PATH` (recorded above), with an absolute
`REA_UNBLOB_COMMAND`. My carriers are 934–1041 B single-block gzip images: behaviour on multi-block,
xz, fragment-bearing or AppImage-shaped BE images is **not** measured here [INFERENCE] unless a wave-2
seat builds them. `raw_result.report[].reports[].magic` strings are host libmagic output and were read
for classification only, never asserted as spec. No tool install or update was made
(`sasquatch`/`sasquatch-v4be` 4.5.1, `unblob` 26.6.4, `rea-agents@6.5.0` used as installed).
Artifacts: `artifacts/R39C2AxisFit/{projection.tsv, project.py, dev-carriers.sh, dev-carriers.sha256,
depth-recipe-control.py, depth-recipe-control.txt, env-*.json}`.
