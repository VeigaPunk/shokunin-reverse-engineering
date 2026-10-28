# R44C1Doc — R44-C1 documentation deltas (wave 1, pre-freeze)

- Seat: `R44C1Doc` (scribe). Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
- Claim: **R44-C1** (coverage: `squashfs_v1` + `squashfs_v2`, both byte orders, through REA 6.5.0
  `extract-firmware` → Core). This seat writes documentation artifacts only.
- Base revision `c29360e3ba5381a5ab69e372d0d9577970f85018`. Lane HEAD when writing: `3b0fcaa9`
  (`round-44: frozen carriers.json + unblob __output__ oracle trees`). `git diff c29360e3..HEAD`
  over `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`, `SKILL.md`, `SCORECARD.md` is
  empty, so every anchor below is identical at base and at HEAD.
- Worktree: the only paths this seat wrote are under
  `.ufo/waves/round-44/w1/R44C1Doc.md` and `.ufo/waves/round-44/w1/artifacts/R44C1Doc/**`
  (untracked). No tracked lane file was created, modified or deleted; nothing outside the lane
  except `probe-R44C1Doc-*` files under `/fast/scratch/hyaku/kaidoku-r44/`.

## Status

Deltas are **drafted and gate-checked, not landed**. They are meant to land *after* the frozen
C1 counter scores, in the L1's landing commit; this seat cannot know the measured outcome and
must not assert it. Two blocks carry an `<AFTER-DATA: …>` slot that the L1 replaces with the
frozen receipt headline. Landing those markers verbatim is a defect: after landing,
`grep -n 'AFTER-DATA' PROVINCE.md corpus/README.md` must print nothing.

Nothing was run from the after-side data procedure: no `tools/round-44/c1-run.sh`, no REA run,
no C1 counter (it does not exist yet), no `c2-counter.py --selftest` (not this claim).

## Deliverables (canonical bytes)

| artifact | bytes | sha256 |
|---|---|---|
| `artifacts/R44C1Doc/block-a-province-round-44-core-row.md` | 1372 | `ce0e8b74b75573968a33212299b1ef8eba125c8f672d9f57bee6a7d5542dad2f` |
| `artifacts/R44C1Doc/block-b-province-frontier-note.md` | 667 | `95bc7b62b92fcd19e01ce0a14d014ad63f543e6112f80ca6aba91f7beb5df44e` |
| `artifacts/R44C1Doc/block-c-readme-coverage-map-row.md` | 736 | `09dfb76f11cffecd14da6ca9ad281effd631c93a8bf672ba5f4c2aa72c56f13a` |
| `artifacts/R44C1Doc/companion-readme-rows.md` (routed, not one of the three blocks) | 1457 | `35872940f64e33934573b70d1fc2ac750e1933282fb9a08ad4c828df86a39597` |
| `artifacts/R44C1Doc/check-map-invariant.py` (the (d) gate) | — | `903155ae139e4f34a49e385df1864fdd683581a92039dad784abe3ed21ebd0b4` |

`artifacts/R44C1Doc/receipts/` holds every receipt quoted below plus `run-log.txt`.

## (a) PROVINCE row — `## Round-44 additions to Core`

```markdown
## Round-44 additions to Core

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| `squashfs_v1` and `squashfs_v2` (SquashFS v1 and v2, gzip bodies, both byte orders) | no new REA key — unblob 26.6.4 names the `squashfs_v1`/`squashfs_v2` handlers (S108 :101-102, :158-159) and runs `sasquatch -le`/`-be` from the child `PATH` per superblock endianness (S108 :24-26, :51-54, :68-69; dependency contract S110); `REA_UNBLOB_COMMAND` = unblob 26.6.4; `extract-firmware` (rea-agents 6.5.0) | `tools/round-44/c1-counter.py` at the round-44 freeze; independent oracle `/usr/bin/unsquashfs` (squashfs-tools 4.7.5) `-lls` member census + extracted member digests, cross-checked against the unblob 26.6.4 `__output__` expected trees committed under `corpus/evidence/round-44/oracle/` (S138; S139 grounds the squashfs-tools oracle identity) | four committed MIT unblob 26.6.4 fixtures, 4 KiB each, frozen in `tools/round-44/carriers.json` (V1LE `b45925fa…`, V1BE `529e1077…`, V2LE `7c62dbe3…`, V2BE `79c0f388…`; 3/3/4/4 expected regular files): <AFTER-DATA: the frozen counter receipt headline — every oracle regular file published at its exact relative path, gap kinds per the frozen gap rule, `carriers_matched 4`, exit 0 — quote the receipt, never this marker>; entry `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` (SquashFS v1/v2) |
```

Row shape mirrors `## Round-42 additions to Core` (`PROVINCE.md:412-414`). What the row asserts
now, all from frozen bytes on disk: handler names and extractor argv (S108, re-opened by this
seat — see Provenance), the oracle identity (`tools/round-44/carriers.json` `oracle` block), and
the four carriers with their sha256 pins and expected regular-file counts. What it deliberately
does **not** assert: publication completeness, gap set, or `carriers_matched` — those are the
after-data slot.

## (b) PROVINCE Frontier note — supersedes the `SquashFS v1/v2` clause only

```markdown
Round-44 frontier note, 2026-10-28: SquashFS v1/v2 moved Frontier → Core with `2026-10-28-r44-squashfs-v1v2-core` (`squashfs_v1` and `squashfs_v2`, both byte orders, through rea-agents 6.5.0 `extract-firmware` on four committed unblob 26.6.4 fixtures, oracle `/usr/bin/unsquashfs` 4.7.5 plus the unblob `__output__` expected trees). This note supersedes the `SquashFS v1/v2` clause of the round-42 frontier note above and nothing else: `squashfs_v2_nonstandard` (`v2ns-*`; no independent reader), `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies, v4 Broadcom, LE AVM members (`hsqs`), AVM kernels and nested sub-images below depth 1 stay Frontier.
```

Scope guard: the note names the superseded clause explicitly ("of the round-42 frontier note
above and nothing else") and re-lists every survivor. `PROVINCE.md:416` (the round-42 note) is
**not edited**; the round-41 (`:408`) and round-39 (`:384`) notes, the `- **sasquatch** —`
bullet (`:156-157`) and the round-42 `Still Frontier:` tail keep their bytes. The v2ns sentence
is strengthened, not dropped: v2ns was not in the frozen carrier set (`carriers.json` note:
"v2ns stays Frontier (no independent reader)"), and the S108 bytes show
`SquashFSv2NonStandardHandler` overriding only `NAME`/`PATTERNS`/`DOC` (`:199-227`, no extractor
change), i.e. the same `sasquatch` path with no independent reader behind the claim.

## (c) `corpus/README.md` coverage-map row

```markdown
| SquashFS v1/v2 through REA (round 44) | `2026-10-28-r44-squashfs-v1v2-core` | **Core** — rea-agents 6.5.0 `extract-firmware` (unblob 26.6.4, `sasquatch` 4.5.1 on the child `PATH`) resolves the `squashfs_v1` and `squashfs_v2` handlers on four committed MIT unblob 26.6.4 fixtures, both byte orders (v1.0 le/be, v2.0 le/be; 4 KiB each, 3/3/4/4 expected regular files); oracle `/usr/bin/unsquashfs` (squashfs-tools 4.7.5) `-lls` member census + extracted member digests, cross-checked against the unblob `__output__` expected trees (S138); <AFTER-DATA: frozen-counter receipt headline — carriers_matched, gap kinds, exit code; quote the receipt, never this marker>; `squashfs_v2_nonstandard` stays Frontier (no independent reader) |
```

The stem `2026-10-28-r44-squashfs-v1v2-core` is the exact knowledge-file stem the entry must be
committed under; the row names no other `2026-10-*` token, so it cannot create a `dangling`
stem under command A.

## Placement (exact anchors, verified at base and HEAD)

| block | insert |
|---|---|
| (a) | append at end of `PROVINCE.md` (file ends `… remain Frontier.\n` at `:422`, after the round-43 frontier note `:418-422`), then one blank line |
| (b) | immediately after the (a) table, as its own paragraph (same shape as the round-42 heading+table+note at `:410-416`) |
| (c) | `corpus/README.md`: new line immediately after `:103` (`| SquashFS triage v4 score (round 43) | …`), i.e. before the blank line at `:104` and `## Knowledge` at `:105` |
| companion 1 (README Frontier bullet) | after `:272` (`- Blocked-on-operator: …`), before `## Known gaps` (`:274`) |
| companion 2 (README Knowledge row) | after `:222` (`| \`2026-10-27-sasquatch-release-matrix\` | …`), before `## Lessons` (`:224`) |

## (d) — the map invariant, measured

**Finding first: there is no `awk` command on this path.** `corpus/README.md`,
`PROVINCE.md` and `SKILL.md` contain zero `awk` occurrences; the two `awk` matches in
`SCORECARD.md` (`:3125`, `:3126`) are prose inside round-25/26 audit findings about counting
*capability-table* rows, not commands. The coverage-map invariant is enforced by
**command A** (`SCORECARD.md:85-121`), pure Python over git objects. This seat ported that map
leg verbatim (`check-map-invariant.py`): knowledge stems = `git ls-tree -r <REV> -- corpus/knowledge`
`.md` stems; mapped stems = `re.findall(r'2026-10-\d{2}-[a-z0-9-]+', <## Coverage map section>)`.

**Second finding: the invariant is stem-set equality, not row count.** Command A never compares
row counts. Measured at base: `knowledge_files 137`, `map_stems 137`, `map_rows 89`,
`missing []`, `dangling []`, `mapped 137` — i.e. 89 rows name 137 stems (many rows bundle two or
three entries). A literal "map row count == knowledge file count" check would fail today at
137/89. The load-bearing predicate is `missing == [] and dangling == [] and
mapped == knowledge_files`.

Measured after the (c) landing (simulated: row inserted at the end of the map section, stem added
to the knowledge set): `knowledge_files 138`, `map_stems 138`, `map_rows 90`, `mapped 138`,
`missing []`, `dangling []`, `ok true` → the invariant stays true and `coverage_score` stays 10.0.

Three red controls show the gate can fail (each exit 1):

1. `--corrupt-stem` (row says `…squashfs-v1-v2-core`): `missing
   ["2026-10-28-r44-squashfs-v1v2-core"]`, `dangling ["2026-10-28-r44-squashfs-v1-v2-core"]`.
2. `--placement after-knowledge` (row landed outside `## Coverage map`): `missing
   ["2026-10-28-r44-squashfs-v1v2-core"]`, `mapped 137`.
3. knowledge file added, no row: `missing ["2026-10-28-r44-squashfs-v1v2-core"]`, `mapped 137`.

Exit-code contract of the gate: `0` invariant holds, `1` broken, `2` could-not-evaluate (usage
error or unreadable git object) — a `2` never counts as a pass.

## Gate receipts (this seat; exit, stdout sha256, wall)

| # | check | command (abbreviated; full text in receipts) | exit | stdout sha256 | wall |
|---|---|---|---|---|---|
| R1 | command A verbatim port at base (ad-hoc) | `python3 - c29360e3… <<'PY'` (recipe A body, unmodified) | 0 | `66a78f754537aa209babee60da641e38959e1f7f04bd6fd88ee5397b69338529` | not captured — the timing shim called `bc`, absent on this host; receipt body kept at `receipts/commandA-base-port.json` |
| R2 | map invariant at base | `python3 -I -B …/check-map-invariant.py --root <lane> --rev c29360e3…` | 0 | `286fef32b3c6d16985e6572413e55074d5d0d168774389e21762b633075f9b0f` | 39 ms |
| R3 | map invariant, (c) landed (simulated) | `… --simulate-row …/block-c-readme-coverage-map-row.md --simulate-new-stem 2026-10-28-r44-squashfs-v1v2-core` | 0 | `bb14f0a90c5c04936b58ccda16e9584d7262b8a73159e9ed1c932ff79f3cc9b0` | 39 ms |
| R4 | control: wrong stem | `… --corrupt-stem` (as R3) | 1 | `e5d3bfaf0f2d62a4834610e907d13f2304a39e9b1b681c1bcc14c48660e91f92` | 35 ms |
| R5 | control: row outside map section | `… --placement after-knowledge` (as R3) | 1 | `07b54d45cfc9f841ded46b69537ab12c76e288c4e1becb8dcf3861ca82c41912` | 36 ms |
| R6 | control: knowledge file, no row | `… --simulate-new-stem 2026-10-28-r44-squashfs-v1v2-core` (no row) | 1 | `1a0908311c163ebd9402c05a9998145a8ea149b536447373fec1867bf64c6b80` | 37 ms |
| R7 | S108 re-open (citation check) | `curl -sS -o probe-R44C1Doc-squashfs.py https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py` | 0 | http 200, 19842 B, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` | 26 ms |

R1–R7 stdout bodies and the R1 body are under `artifacts/R44C1Doc/receipts/`; R1's port file is
`receipts/commandA-base-port.json`.

## Findings

1. **No `awk` map command exists** (task text said "the README map-block `awk` command"). Zero
   `awk` in `corpus/README.md`/`PROVINCE.md`/`SKILL.md`; the map gate is command A's Python
   (`SCORECARD.md:85-121`). Handled by porting that leg exactly (R2–R6).
2. **The invariant is a stem set, not a row count.** 89 rows / 137 stems at base. Block (c) keeps
   `missing []`, `dangling []`, `mapped == knowledge_files` true at 138/138; it would *not* keep a
   literal row count equal to the file count — that predicate is already false and is not what
   command A computes.
3. **S138/S139 are not yet in `corpus/SOURCES.md`.** Only S136/S137 exist (`:142-143`). Blocks
   (a)/(c) cite S138 (and (a) S139). The landing commit must include both SOURCES rows, or the
   citation dangles. Whose seat owns S138/S139: not this one — recorded here as a landing
   dependency, not as a claim.
4. **The committed oracle tree is a superset of the frozen carriers.**
   `corpus/evidence/round-44/oracle/` holds `squashfs_v2.0_{le,be}` **and** `squashfs_v2.1_{le,be}`
   `__output__` trees, but `tools/round-44/carriers.json` freezes only four carriers (v1.0 le/be,
   v2.0 le/be). Blocks (c)/(a) therefore spell the versions out ("v1.0 le/be, v2.0 le/be") and
   never say "all v2". A row that said "every `__output__` tree" would over-claim v2.1.
5. **`corpus/README.md`'s own `## Frontier` section still says `v1/v2` is frontier**
   (`:268`: "Still frontier: v1/v2, `squashfs_v3_broadcom`/`_nonstandard`, gzip v3."). That line
   is outside the three named blocks, so this seat did not touch it; left as is, README Frontier
   contradicts the new Core row. Companion 1 in `companion-readme-rows.md` is the one-line fix
   (append-only, same shape as the round-36..43 lines) — an L1 decision, not landed here.
6. **`## Knowledge` would otherwise lack the new entry.** Command A does not read that table, so
   it is not part of the invariant; companion 2 supplies the row for consistency.
7. **The `<AFTER-DATA>` slots are real gates, not decorations.** Two exist (block (a), block (c)).
   A landing that leaves either marker in place fails the prose honestly but ships a placeholder;
   the post-landing guard is `grep -n 'AFTER-DATA' PROVINCE.md corpus/README.md` → no output.
8. **Block (b) must not be read as widening the Frontier list.** It re-lists every survivor the
   round-42 note named (`squashfs_v2_nonstandard`, `squashfs_v3_broadcom`,
   `squashfs_v3_nonstandard`, gzip v3, v4 Broadcom, LE AVM (`hsqs`), AVM kernels, nested
   sub-images below depth 1) and adds none. v2ns is named with its reason (no independent reader),
   which is stricter than the round-42 note's bare mention.

## Provenance notes

- **S108 re-open (R7).** `squashfs.py` at tag 26.6.4, 19842 B, sha256 `2d7b901b…`. Observed:
  `SquashFSExtractor.EXECUTABLE = "sasquatch"` (`:25`), `V4BE_EXECUTABLE = "sasquatch-v4be"`
  (`:26`), endianness → `"-be"` for `Endian.BIG, _` (`:51-52`) and `"-le"` for `Endian.LITTLE, _`
  (`:53-54`), `get_dependencies()` returns both executables (`:68-69`), `SquashFSv1Handler`
  `NAME = "squashfs_v1"` (`:101-102`), `SquashFSv2Handler` `NAME = "squashfs_v2"` (`:158-159`),
  `SquashFSv2NonStandardHandler` `NAME = "squashfs_v2_nonstandard"` (`:199-200`). The v1/v2
  subclasses do not override `EXTRACTOR`; the inherited `SquashFSExtractor(3, …)` only branches on
  `(Endian.BIG, 4)` for the AVM `-be` drop (`:40-50`), so for v1/v2 both byte orders the observed
  argv is `sasquatch -le`/`-be` plus `-no-exit-code -f -d {outdir} {inpath}`. This is why block
  (a) can state the port line rather than infer it.
- **Carrier pins reproduced from disk** (all 4096 B, matching `carriers.json`):
  V1LE `b45925fa779eae0293635ce0e6dc8760308f25227dd88645d677ba3ffce23e71`,
  V1BE `529e10775cc152e6c5df0c6c63316811004cc73ce99f03989c86ffd396d631e6`,
  V2LE `7c62dbe388b972119f5d17a12836a016737d58276184f4caa2a90dafd924f124`,
  V2BE `79c0f3886291f4abcc656acd49932446cf16afaa67e6ffb0c5258e3c2e2dfcc0`.
  Expected regular files: 3/3/4/4; v1 `__output__` members are `apple.txt`,
  `banana.txt`, `cherry.txt`, v2 `.0` members `apple1..4.txt`.
- **Oracle tree provenance**: `corpus/evidence/round-44/oracle/manifest.json` (seat
  `R44SrcOracle`) records the listings API 200s and the LFS-pointer custody note; the trees are
  committed at HEAD `3b0fcaa9`.
- No number in the drafted prose is a measurement this seat did not make; everything measured
  here is in the receipts table and the (d) section.
- Not observed / not claimed: whether the frozen C1 counter's documentation bindings match this
  exact wording (the counter does not exist at base — `tools/round-44/` holds only
  `carriers.json`); whether S138/S139 land (finding 3); whether the entry itself ships the same
  sentences (a different seat owns the entry).

## Out of scope (untouched)

- `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md`,
  `LOG.md`: no edits, no appends; landing is the L1's.
- `tools/round-44/`: not modified; no counter authored or installed.
- `corpus/knowledge/**`: the entry `2026-10-28-r44-squashfs-v1v2-core.md` is another seat's.
- No `tools/round-44/c1-run.sh`, no REA run, no `unsquashfs` run, no squashfs tooling invoked.
- No `git` mutation of any kind (no add/commit/checkout); no fleet-root file written.

## Limits

- The (d) gate is a port of command A's map leg, not command A itself: it does not compute
  `coverage_score`/`depth_score`/`citation_resolved_rules`. Its baseline numbers were
  cross-checked against a verbatim command-A run (R1: 137/137, missing `[]`, dangling `[]`,
  coverage 10.0, 21/21 rules) and agree on every map field.
- It reads git objects only, so a worktree-only edit is invisible to it by design — the same
  property command A has.
- Wall times are single-shot on a warm cache (35–39 ms); they say nothing about a cold clone.
- The simulation adds the row at the end of the map section; landing it anywhere else in that
  section is equivalent for the regex, but a row landing in `## Knowledge` is not (R5).
