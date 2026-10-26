# R39C1SymlinkK1K4 — frozen symlink tables for C1 carriers K1–K4 (pre-freeze)

**VERDICT: DEFECTS FOUND — one freeze-blocking defect in the draft's class convention, zero
carrier/receipt contradictions.** All four round-38 after-receipts match unblob 26.6.4's actual
symlink behaviour (K1 escaping → removed, no gap; K2 in-tree → one `unpublished-entry` gap; K3/K4 →
no symlinks, no gaps). But the sentence that defines the class in `plans/round-39-claims.md`
("resolved POSIX-style against the link's own directory inside the image root, image root = /")
resolves K1's link to `/hello.txt`, i.e. **`in-tree`**, under `posixpath.normpath`,
`os.path.realpath` and `path.posix.normalize` — every stock normaliser clamps a leading `..` at `/`.
A counter written that way demands one gap on K1, K1's frozen receipt has none, and P39-C1 dies on
its first carrier. The class must be frozen as *extraction-root* semantics (the rule unblob
implements), and K1 must be frozen as `escaping`. Exact replacement wording in §5.

Seat: `R39C1SymlinkK1K4` (leaf). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
base `a2f64e1da78afcf8cc39287106604dbcc270844c`. Item scope: K1–K4 only. **No REA run on K5/K6,
no held-out carrier built.** Tools were not installed or changed (no `pacman`, no `uv`, no `npx`
install beyond the pinned `rea-agents@6.5.0` invocation on a scratch dev carrier).

## 1. Deliverables (all under `.ufo/waves/round-39/w1/artifacts/R39C1SymlinkK1K4/`)

| path | content |
|---|---|
| `symlinks-K1.tsv` | `link-to-hello\t../hello.txt\tescaping` |
| `symlinks-K2.tsv` | `var/lib/run-link\t../../a/run.sh\tin-tree` |
| `symlinks-K3.tsv`, `symlinks-K4.tsv` | empty (no symlink in the image; 0 bytes) |
| `symlinks-combined.tsv` | carrier, symlink, target, class, resolved path, round-38 gap, removed-by-unblob, coverage |
| `symlink-tables.py` | derivation tool (committed git blobs for K1/K2, `sasquatch-v4be -be -ll` for K3/K4, non-clamping classifier, frozen-expectation assertions). `python3 -I -B symlink-tables.py` → `{"assertions": "pass", "rows": {"K1": 1, "K2": 1, "K3": 0, "K4": 0}}`, exit 0. A class flip fails the run with exit 2. |
| `evidence/sasquatch-ll-K{1..4}.txt` | `sasquatch-v4be -be -ll` listings of the four committed carriers (exit 0 each) |
| `evidence/receipt-crosscheck.json` | per-carrier receipt bindings recomputed from committed bytes (below) |
| `evidence/dev-tree.txt`, `evidence/dev-carrier.sqsh`, `evidence/dev-links-envelope.json` | dev BE v4 carrier (524 B, sha256 `186903e6…442`, built from a fresh tree with `tools/round-37/gen-squashfs.py --endian be --comp gzip`) + its full REA 6.5.0 envelope: absolute in-root, dangling and in-tree links kept with a gap; escaping link removed |
| `evidence/dev2-tree.txt`, `evidence/dev2-carrier.sqsh`, `evidence/dev-outcomes.json` | second dev carrier: `/../out.txt` (absolute, ascends after `lstrip("/")`) removed; `/hello.txt` rewritten to `../hello.txt` and kept; `../hello.txt` kept |
| `evidence/convention-clamp-vs-extraction.txt` | `normpath`/`realpath`/`path.posix.normalize` all print `/hello.txt` while `readlink -f` on a real extraction dir lands outside it |

The four `symlinks-K*.tsv` are the per-carrier oracle rows in the schema the draft freezes —
`relative path, link target, in-tree|escaping` — ready to be committed as
`corpus/evidence/round-39/c1/K*/symlinks.tsv` by the L1.

## 2. The table

| carrier | symlink (in-image path) | target (image bytes) | class | resolved under the frozen rule | round-38 after-receipt outcome |
|---|---|---|---|---|---|
| K1 | `link-to-hello` | `../hello.txt` | **escaping** | leaves the root (`..` at depth 0) | `extraction_gaps: []`, `unpublished_entries: []`, `diagnostics[0].report.__typename__ = MaliciousSymlinkRemoved`, `coverage: partial`. Diagnostic in the committed receipt: `link …/extracted/firmware.bin_extract/link-to-hello`, `target …/extracted/hello.txt` — the target resolves one level **above** the extract dir |
| K2 | `var/lib/run-link` | `../../a/run.sh` | **in-tree** | `/a/run.sh` | `extraction_gaps: [{kind: unpublished-entry, input_path: $output/firmware.bin_extract/var/lib/run-link, relative_path: firmware.bin_extract/var/lib/run-link, continuation_id 602c674b…}]`, `unpublished_entries: [{kind: symlink, link_target: ../../a/run.sh, relative_path: firmware.bin_extract/var/lib/run-link}]`, `diagnostics: []`, `coverage: partial`. The link target `a/run.sh` **is** published as a regular file and the gap still exists |
| K3 | (none) | — | — | — | `extraction_gaps: []`, `unpublished_entries: []`, `diagnostics: []`, `coverage: complete` |
| K4 | (none) | — | — | — | `extraction_gaps: []`, `unpublished_entries: []`, `diagnostics: []`, `coverage: complete` |

**Kill-signal answer: none of the four receipts contradicts the stated rule** (`in-tree` → exactly
one `unpublished-entry` gap; `escaping` → removed, no gap). K1 is the escaping example and K2 the
in-tree example, both exactly as the rule predicts. The defect is in the *definition of the class*
(§5), not in the carriers or the receipts.

**Independent agreement.** Seat `R39C1AxisFit` measured the same four carriers from a separate
probe (`.ufo/waves/round-39/w1/artifacts/R39C1AxisFit/`): same two links, same classes, same
gap/removal outcomes, same zero-link K3/K4, same `gen-squashfs` drop of dir-target links, same
1-gap-per-kept-link cardinality and `firmware.bin_extract/` prefix. The one divergence is the
absolute-target corner: that seat records "absolute = in-tree, re-rooted"; `/hello.txt` is, but
`/../out.txt` is removed here — measured on `dev2` (§6.1). No frozen carrier has an absolute link,
so the divergence only matters if K5/K6 introduce one.

**Second independent check.** Seat `R39C1IndepReader` also reproduced the four classes and added
the cycle case (a symlink loop is *kept*, not removed, because `Path.resolve()` no longer raises on
loops). I confirmed it on a dev carrier — see `dev3` in §3 and §6.7 — including the extra wrinkle
that `a -> b` is rewritten to a self-loop `a -> a`.

Independent confirmation that the receipts are not stale or edited (all recomputed from committed
bytes in `evidence/receipt-crosscheck.json`):

| carrier | carrier sha256 = receipt `subject.digest.sha256` | handler | oracle regular files matched (suffix + sha256) | gaps | stored id recomputes (`tools/round-27/xpin-attribute.mjs --pkg65 rea-agents@6.5.0`) |
|---|---|---|---|---|---|
| K1 | `1cfb6c33…117e` ✓ | `squashfs_v4_be` | 5/5 | none | `ev_400465e0…c1e9` ✓ |
| K2 | `403cb0a8…9154` ✓ | `squashfs_v4_be` | 3/3 | 1 `unpublished-entry` | `ev_e9386786…8914` ✓ |
| K3 | `9c7c523c…97c0` ✓ | `squashfs_v4_be` | 4/4 | none | `ev_e31cb700…aa66` ✓ |
| K4 | `a29ddc15…56ed` ✓ | `squashfs_v4_be` | 4/4 | none | `ev_4348dcaf…ae2e` ✓ |

## 3. Rule under test — what the tools actually do

*(unblob 26.6.4 at `~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/`,
rea-agents 6.5.0 at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`)*

- `unblob/extractor.py:50` `fix_symlink`: relative target → `path.resolve()`; absolute target →
  `Path(as_posix().lstrip("/"))`; then `file_utils.py:34` `is_safe_path(outdir, target)` =
  `outdir.joinpath(target).resolve().relative_to(outdir.resolve())`.
- Not safe → `MaliciousSymlinkRemoved(link, target)` (class at `unblob/report.py:133`, severity
  WARNING), file unlinked, **no other record**. Safe → target rewritten relative to the link's
  parent (`os.path.relpath`) and the link kept.
- unblob's `squashfs_v4_be` handler is `handlers/filesystem/squashfs.py:513`, extractor binary
  `sasquatch-v4be` (`:26`); this is why the after-arm needs that binary on the child PATH.
- REA `dist/firmware/FirmwarePublication.js:66-75`: every extracted entry whose `kind` is not
  `file` becomes `unpublished_entries[]` (`kind: symlink`, `link_target` = the **post-rewrite**
  readlink); `:301-307` maps each one to one `extraction_gaps[]` row of kind `unpublished-entry`
  with `input_path = $output/<relative_path>` and the shared continuation
  `602c674b7f83f4acd6bf01c5655a5dd669f206d33ee3bc9b8bc2c0ba9f08cfca` ("retained as metadata",
  `:18`). `dist/firmware/FirmwareFiles.js:178-185` is where `symlink` / `special` / `file` are
  assigned; directories never enter the list (K1 publishes 5 files and 0 entries with an empty
  `unpublished_entries`, which proves it).
- Consequences that the freeze must live with: coverage is `partial` for **both** classes (K1 via
  unblob's WARNING, K2 via the unpublished entry); a `special` entry (device/fifo/socket) would
  also produce one `unpublished-entry` gap, so "gaps exactly on the oracle's symlinks" is only
  true because no carrier holds a special file.

Live re-verification on a dev carrier (`evidence/dev-links-envelope.json`, REA 6.5.0 + unblob
26.6.4, carrier `186903e6…442`):

| link in image | classification | extraction | REA |
|---|---|---|---|
| `abs-in -> /hello.txt` | in-tree | kept, **rewritten to `hello.txt`** | `unpublished_entries[].link_target = hello.txt` (≠ image bytes), 1 gap |
| `dangle -> missing.txt` | in-tree (dangling) | kept | `link_target = missing.txt`, 1 gap |
| `a/b/rel -> ../../hello.txt` | in-tree | kept | `link_target = ../../hello.txt`, 1 gap |
| `a/b/deep-up -> ../../../hello.txt` | escaping | removed | `MaliciousSymlinkRemoved`, **0 gaps** |
| `a/b/updir -> ../..` | — | **silently absent from the image** (see §6) | — |
| `abs-up -> /../out.txt` (dev2) | escaping (absolute, ascends after `lstrip("/")`) | removed | `MaliciousSymlinkRemoved` |
| `a -> b`, `b -> a`, `self -> self` (dev3, cycle) | in-tree | **all kept**, no WARNING; `a` rewritten to `a -> a` | 4 gaps, 0 diagnostics, `coverage: partial` (`evidence/dev3-loop-envelope.json`) |
| `x -> y`, `y -> ../outside.txt` (dev4, chain out) | `x` looks in-tree one-step | **both removed**, 2 WARNINGs | **0 gaps** for `x` and `y` (`evidence/dev4-chain-envelope.json`) |
| `p -> q`, `q -> hello.txt` (dev4, chain in) | in-tree | both kept, targets **flattened to `hello.txt`** | 2 gaps with `link_target = hello.txt` |

The last two rows are why §6.7 asks for a chain-free K5/K6: a one-step lexical class is exact for
every single-link image and only approximate once one link's target names another link.

## 4. Cross-checks against the upstream unblob fixture (K3/K4 provenance)

- `GET https://api.github.com/repos/onekey-sec/unblob/contents/tests/integration/filesystem/squashfs/squashfs_v4_be/__output__?ref=26.6.4`
  → four `*_extract` dirs, all pointing at tree `192d46c79d89e6e669a9325401ec3aa08c7d8a30`;
  recursive listing of that tree = **`100644 apple1.txt … apple4.txt` only — no symlink, no
  directory, no special file.** (That is the whole expected output of the fixture, so K3/K4's
  empty symlink tables are sourced, not assumed.)
- LFS pointers (`raw.githubusercontent.com/.../26.6.4/...__input__/<name>`, `...__output__/…/appleN.txt`):
  `squashfs_v4.4kpad.bin` oid `9c7c523c…97c0` = K3 `carrier.bin` bytes; `squashfs_v4.nopad.bin`
  oid `a29ddc15…56ed` = K4; `squashfs_v4.bin` shares K3's oid; `apple1..4.txt` oids equal the four
  `oracle.tsv` rows (and the committed `apple*.txt` files hash to those rows).
- Therefore K3 (4kpad, chunk 0..4096) and K4 (nopad, chunk 0..307) are the **same four-file
  filesystem** padded differently: across the six-carrier freeze they contribute exactly one
  distinct symlink-free image, and the rule is exercised only by K1 and K2.

## 5. Freeze-blocking defect and the minimum fix

The draft says the class is "resolved POSIX-style against the link's own directory inside the image
root, image root = /". Two natural implementations of that sentence disagree on K1:

| implementation | `link-to-hello -> ../hello.txt` | consequence for P39-C1 |
|---|---|---|
| `posixpath.normpath`, `os.path.realpath`, `path.posix.normalize` (all clamp `..` at `/`) | `/hello.txt` → **in-tree** | predicate demands 1 gap on K1, receipt has 0 → **C1 stops** |
| unblob's `is_safe_path` on the real extraction dir (what the receipt shows) | escapes → **escaping** | matches |

Evidence: `evidence/convention-clamp-vs-extraction.txt` — `readlink -f` on a real directory lands
**outside** it for the same link, while all three normalisers print `/hello.txt`. Seat
`R39C1AxisFit` reproduced the arithmetic independently (`normpath('/../hello.txt') == '/hello.txt'`,
`normpath(join('/', '../hello.txt')) == '/hello.txt'`, `normpath(join('/var/lib', '../../a/run.sh'))
== '/a/run.sh'`), so the L1 has two sources for the same defect. The same split
appears for absolute targets: `/../out.txt` is removed by unblob but would clamp to `/out.txt`
(`in-tree`, dangling) under POSIX normalisation.

**Recommended frozen wording (replaces the parenthetical only):**

> `in-tree` iff the target, joined to the link's directory (an absolute target first losing exactly
> one leading `/` and re-based at the extraction root) and cancelled component-by-component, never
> needs a `..` while the path is already at the extraction root; otherwise `escaping`. The
> extraction root is the extractor's own output directory for that filesystem — unblob's `outdir`
> in `is_safe_path` — not the host `/` and not the carrier file's directory. Cancellation never
> clamps at `/`: a `..` with nothing left to cancel marks the link `escaping`, i.e. it resolves
> outside the extraction root. This is the rule unblob 26.6.4 implements
> (`unblob/extractor.py:fix_symlink` + `unblob/file_utils.py:is_safe_path`), and it is the only
> convention under which K1's frozen receipt (removed, zero gaps) is the predicted outcome.

`symlink-tables.py:classify()` is that rule, in 15 lines, with K1/K2 assertions; the counter can
import or copy it. Freeze K1 as `escaping`, K2 as `in-tree`, K3/K4 as no rows.

## 6. Secondary hazards for the freeze (none of them fatal, all cheap to avoid)

1. **Absolute targets are re-rooted, not escaped — except when they ascend.** `/hello.txt` is kept
   but recorded as `link_target: hello.txt`; `/../out.txt` is **removed** (unblob lstrips one `/`,
   then `..` escapes — measured, `evidence/dev-outcomes.json` `dev2-carrier`). So "absolute =
   in-tree" holds only for targets that do not literally begin with `..` after the strip; a
   `symlinks.tsv` convention that maps every absolute target to `in-tree` is wrong for `/../x`. The
   draft does not compare `link_target` to the oracle row, which is correct — do **not** add that
   binding if K5/K6 carry absolute targets; if K5/K6 need `link_target` equality, restrict them to
   relative targets.
2. **`tools/round-37/gen-squashfs.py` silently drops symlinks whose target is an existing
   directory.** `os.walk` classifies them as `dirnames` and the generator only packs `fnames`
   (`gen-squashfs.py:59-66`); `a/b/updir -> ../..` never reached the image (8 inodes instead of 9).
   A dir-target link for K5/K6 cannot be built without fixing the generator, and the loss is
   silent — verify inode count and `sasquatch-v4be -ll` after building.
3. **Diagnostics leak the run directory.** Every `MaliciousSymlinkRemoved` embeds absolute
   `link`/`target` paths of the run's scratch dir (round-38: `/fast/scratch/hyaku/kaidoku-r38/…`;
   dev: `/tmp/rea-firmware-FnVRiI/…`). Harmless for the `ev_…` recompute (it hashes stored bytes,
   verified above), but no predicate may require path-stable or byte-reproducible envelopes for
   carriers with escaping symlinks.
4. **Gap path prefix.** REA's gap `relative_path` is `firmware.bin_extract/<in-image path>`; the
   oracle row is `<in-image path>`. Match by suffix, exactly as `c1-counter.py:matched()` does for
   regular files.
5. **Coverage is not a usable signal** for these two classes: `partial` for K1 (WARNING) and for K2
   (unpublished entry), so a counter that gates on `coverage == complete` would fail every carrier
   that exercises the rule. P39-C1 does not — keep it that way.
6. **Class-exposure gap in the six.** With K3/K4 symlink-free, K1/K2 carry one escaping and one
   in-tree link between them; K5/K6 are the only chance to test a nested in-tree link, a dangling
   in-tree link, or a second escaping shape. The rule as frozen is otherwise measured by n=1 per
   class.
7. **Chains and cycles (measured on dev3/dev4, see §3 and `evidence/dev-outcomes.json`).** unblob
   resolves the whole host chain, so a link whose target is another link of the same image is
   governed by the chain, not by its own one-step lexical class:
   `x -> y` with `y -> ../outside.txt` → **both** removed, two diagnostics, **no gap for either**
   although the lexical walk calls `x` in-tree; `p -> q` with `q -> hello.txt` → both kept with
   their `link_target` **flattened** to `hello.txt`; a cycle (`a -> b`, `b -> a`, `self -> self`) is
   **kept**, because `Path.resolve()` under unblob's own interpreter (python 3.13.16) returns the
   unresolved path instead of raising, so `is_recursive_link()` never fires — and `a -> b` is
   rewritten to a self-loop `a -> a`. Corroborated independently by seat `R39C1IndepReader`.
   Consequence: `symlinks.tsv` classes are one-step assertions and are only honest for
   chain-free images. K1–K4 are chain-free (0 chains reported by `symlink-tables.py
   chain_report()`); a frozen K5/K6 must be chain-free and cycle-free, or the table must resolve
   chains and the predicate must state the flattened `link_target` behaviour.

## 7. Sources (rows for `SOURCES.md`, opened 2026-10-26)

| source | exact locator | what it establishes |
|---|---|---|
| unblob 26.6.4, symlink sanitiser | `…/site-packages/unblob/extractor.py:50` (`fix_symlink`), `:95` (`fix_extracted_directory`), `…/unblob/file_utils.py:34` (`is_safe_path`), `…/unblob/report.py:133` (`MaliciousSymlinkRemoved`) | in-tree link kept and rewritten; escaping link unlinked with a WARNING report |
| unblob 26.6.4, BE handler | `…/unblob/handlers/filesystem/squashfs.py:25-26`, `:513` (`squashfs_v4_be`, extractor `sasquatch-v4be`) | handler name and the `PATH` dependency |
| rea-agents 6.5.0, publication | `dist/firmware/FirmwarePublication.js:18`, `:66-75`, `:301-307`; `dist/firmware/FirmwareFiles.js:178-185` | non-file entries → `unpublished_entries[]` + one `unpublished-entry` gap each; the continuation id |
| unblob fixture, expected output | `tests/integration/filesystem/squashfs/squashfs_v4_be/__output__` @ tag `26.6.4`, tree `192d46c7…`, recursive listing | expected output is four regular files; no symlink in the BE v4 fixture |
| frozen receipts | `corpus/evidence/round-38/c1/K{1..4}/after.json` | observed outcomes in §2 |
| carriers | `corpus/evidence/round-37/c1/K{1,2}/src` (git mode `120000` blobs), `K{3,4}/carrier.bin` | the link bytes and the images |

## 8. Commands actually run (exit codes)

```
git -C <LANE> ls-files -s corpus/evidence/round-37/c1/K1/src corpus/evidence/round-37/c1/K2/src   # 120000 rows, 0
git -C <LANE> cat-file blob 55bf5ed0…  -> ../hello.txt
git -C <LANE> cat-file blob 034758ff…  -> ../../a/run.sh
~/.local/bin/sasquatch-v4be -be -ll <K1|K2|K3|K4>/carrier.*                                    # 0,0,0,0
~/.local/bin/unblob -e <S>/u{1..4} --report <S>/k{1..4}-report.json <K{1..4}>/carrier.*         # 0,0,0,0
   -> K1: MaliciousSymlinkRemoved(link-to-hello -> ../hello.txt), no link in the tree
   -> K2: `l … run-link -> ../../a/run.sh` kept
   -> K3/K4: four regular files, no link, no report
cd <S> && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware \
   --format json --full-output <S>/dev/carrier.sqsh <S>/dev/rea-out                     # 0 (dev carrier only)
node <LANE>/tools/round-27/xpin-attribute.mjs --pkg65 <rea-agents 6.5.0> --pkg67 … K{1..4}.wrapped.json  # 0, "both" ×4
python3 -I -B .ufo/waves/round-39/w1/artifacts/R39C1SymlinkK1K4/symlink-tables.py         # 0, assertions pass
curl api.github.com/…/git/trees/192d46c7…?recursive=1 ; curl raw…/__input__/*, __output__/…/apple*.txt
```

Scratch `S=/fast/scratch/hyaku/kaidoku-r39/R39C1SymlinkK1K4` was removed after copying every cited
artifact into this seat's artifact dir; nothing outside this seat's artifact dir and report was
written, and no VCS state was touched.

## 9. Limits

- K1–K4 only. No K5/K6 was run, built or scored; no held-out C2 carrier exists in this seat.
- The dev-carrier REA run exists to pin the *rule*, not to produce C1 evidence; it is not a receipt
  for any frozen carrier and must not be committed as one.
- `[INFERENCE]` The claim that a `special` (device/fifo/socket) entry also yields exactly one
  `unpublished-entry` gap is code-derived (`FirmwarePublication.js:66-75`), not measured: no
  carrier in K1–K4 contains one, and `gen-squashfs.py` cannot emit one.
- `[INFERENCE]` The chain and cycle behaviour in §6.7 is measured on `unblob` **CLI** extractions
  plus one REA run per dev carrier; the general statement that every chain shape follows its chain
  rests on `fix_symlink`'s single `path.resolve()` call, not on an exhaustive shape census.
