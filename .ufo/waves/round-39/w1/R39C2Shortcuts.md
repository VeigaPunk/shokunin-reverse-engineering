# R39-C2 pre-freeze shortcut controls — R39C2Shortcuts

**Verdict: DEFECTS FOUND** — all six controls are built, grammar-valid and scored against
the seven draft classes; **no shortcut reaches 14/14** (ceiling 10/14, CTL-C2-6), so the
draft's own kill rule does not fire and no class/feature change is needed to defeat a
shortcut. Three freeze-text holes (D1-D3) do make the *intended* 14/14 unreachable if the
predicate is frozen as worded, and two held-out-generator constraints (D4-D5) must be
frozen with it.

Scratch removed at the end; no VCS mutation; no K5/K6 carrier and no held-out carrier was
built or run; no REA run touched K5/K6.

## 1. Deliverables (all under `.ufo/waves/round-39/w1/artifacts/R39C2Shortcuts/`)

| file | what it is |
|---|---|
| `CTL-C2-1-catch-all.md` | one `*` row -> `clean` |
| `CTL-C2-2-gap-count-only.md` | two rows keyed only on gap kinds `none` / `*` |
| `CTL-C2-3-gap-kind-only.md` | four rows keyed only on G, every other cell `*` |
| `CTL-C2-4-published-only.md` | rows keyed only on `published files` `0` / `>0` |
| `CTL-C2-5-round36-le-transcribed.md` | the round-36 table (`SKILL.md:1231-1242`) transcribed into the grammar |
| `CTL-C2-6-no-be-no-sr.md` | best table using no `-be` and no `MaliciousSymlinkRemoved` knowledge |
| `FEASIBILITY-full-table.md` | full 7-class table (plus the optional `no-squashfs-chunk` row), 14/14 — proves grammar + recon signatures are satisfiable |
| `BOUND-no-be-no-sr-8class.md` | the no-BE/no-SR shape with `no-squashfs-chunk` available, 12/16 |
| `triage-eval.py` | my grammar interpreter (validation + prediction only; the frozen counter is the L1's) |
| `class-signatures.json`, `class-signatures-with-nochunk.json` | the seven/eight class fixtures, each pointing at a committed or copied envelope |
| `bounds.json`, `CTL-C2-*.prediction.json`, `FEASIBILITY-*.prediction.json`, `BOUND-*.prediction.json` | machine outputs cited below |
| `evidence/` | dev carriers and every envelope the features are read from |

Every control file has the same shape: `# title`, a `## Queue-drain craft` section, the
marker `<!-- sqfs-triage-table v1 -->`, then exactly one table with the exact nine header
cells. My interpreter parses them exactly as the L1 contract states (section = heading to
next `## `, first table after the marker, cells stripped of backticks/spaces, first
matching row wins, no match = `unclassified`, malformed cell = exit 2).

## 2. Recon feature matrix (all six features read from real envelopes)

H = squashfs chunk handlers, G = gap kinds, D = gap dependencies, BE = standalone `-be`
in a recorded sasquatch command, SR = `MaliciousSymlinkRemoved`, P = published file count.

| class | H | G | D | BE | SR | P | evidence |
|---|---|---|---|---|---|---|---|
| `clean` | {`squashfs_v4_be`} | {} | {} | `n/a` | `no` | 4 | `evidence/rea-healthy.json` (dev BE, same tree) |
| `escaping-symlink-removed` | {`squashfs_v4_be`} | {} | {} | `n/a` | **`yes`** | 5 | `evidence/r38-K1-after.json` (round-38 K1 after) |
| `in-tree-symlink-metadata` | {`squashfs_v4_be`} | {`unpublished-entry`} | {} | `n/a` | `no` | 3 | `evidence/r38-K2-after.json` (round-38 K2 after) |
| `dep-missing-be` | {`squashfs_v4_be`} | {`missing-extractor-dependency`} | {`sasquatch-v4be`} | `n/a` | `no` | 0 | `evidence/r38-K1-before.json`; dev `evidence/rea-dep-be-healthy.json` |
| `dep-missing-le` | {`squashfs_v4_le`} | {`missing-extractor-dependency`} | {`sasquatch`} | `n/a` | `no` | 0 | `evidence/rea-dep-le-healthy.json` |
| `avm-marker-be-dropped` | {`squashfs_v4_be`} | {`extractor-failure`} | {} | **`no`** | `no` | 0 | `evidence/probe-rea-k1-avm.json` (R38W2AvmProbe) and independent dev `evidence/rea-avm.json` |
| `body-extractor-failure` | {`squashfs_v4_be`} | {`extractor-failure`} | {} | **`yes`** | `no` | 0 | `evidence/rea-bodyfail.json` (dev, inode table damaged) |
| `no-squashfs-chunk` (conditional 8th) | {} | {} | {} | `n/a` | `no` | 0 | `evidence/rea-trunc.json`, `evidence/rea-badmagic.json` |

A body failure on an **LE** v4 image is the same class-signature shape with the other
endianness: H {`squashfs_v4_le`}, G {`extractor-failure`}, BE `no`, P 0 — measured
(`evidence/rea-le-bodyfail.json`); see D2.

I did not take the round-38 receipts on faith: the K1/K2 features above were recomputed
from the committed JSON, and every BE-side feature was reproduced on my own fresh trees in
scratch (commands in §6). Two details worth freezing:

- The round-38 `dep-missing` envelopes already report `dependencies = ["sasquatch-v4be"]`
  (not `sasquatch`), even though the BE handler's dependency list is
  `[sasquatch, sasquatch-v4be]`. A dev run with **both** binaries stripped from the child
  `PATH` still reports only `["sasquatch-v4be"]` for a BE chunk (and only `["sasquatch"]`
  for an LE chunk), so the exact-set cell is stable.
- unblob 26.6.4's `SquashFSExtractor.extract` (installed package,
  `handlers/filesystem/squashfs.py`) appends `-be` for BE v4 **unless**
  `header.bytes_used == header.mkfs_time` (the AVM test). This is the whole of the BE
  feature: `-be` is recorded only in a failing `ExtractCommandFailedReport`, so a successful
  BE run yields `n/a`, not `yes`. The craft text must say that.

## 3. Per-control predictions (2 per class, N = 14)

Labels are the control's output per class; **bold** = correct. Score counts envelopes.

| control | clean | escaping | in-tree | dep-be | dep-le | avm | body | score | ceiling why |
|---|---|---|---|---|---|---|---|---|---|
| CTL-C2-1 catch-all | **clean** | clean | clean | clean | clean | clean | clean | **2/14** | one label only |
| CTL-C2-2 gap-count-only | **clean** | clean | dep-be | **dep-be** | dep-be | dep-be | dep-be | **4/14** | two blocks, best label per block |
| CTL-C2-3 gap-kind-only | **clean** | clean | **in-tree** | dep-le | **dep-le** | **avm** | avm | **8/14** | four G blocks, 2 per block |
| CTL-C2-4 published-only | **clean** | clean | clean | **dep-be** | dep-be | dep-be | dep-be | **4/14** | two blocks (0 / >0) |
| CTL-C2-5 round-36 transcribed | **clean** | clean | **in-tree** | unclassified | **dep-le** | unclassified | unclassified | **6/14** | no row for BE dep, AVM or body failure |
| CTL-C2-6 no BE, no SR | **clean** | clean | **in-tree** | **dep-be** | **dep-le** | **avm** | avm | **10/14** | the two hidden pairs |

Free picks (a shortcut author would choose by prior belief, score unchanged because the
group sizes are equal): CTL-C2-2/CTL-C2-3's ambiguous group labels, CTL-C2-4's zero-file
label. Ties are stated in each control file.

## 4. Kill result and the ceiling proof

**No shortcut reaches 14/14.** Maximum is CTL-C2-6 at 10/14, four envelopes short. The
draft therefore survives its own enumerated kill rule (do-nothing, catch-all,
gap-count-only, gap-kind-only, round-36 transcription), and the R39-C2 kill rule has no
trigger from this wave. No class or feature change is required to *defeat a shortcut*.

Why 10 is a hard ceiling for any no-BE/no-SR table (and why each feature is load-bearing):

- `triage-eval.py --bounds` on the seven fixtures prints, and `bounds.json` records:
  - `avm-marker-be-dropped vs body-extractor-failure: differ only in ['BE']`
  - `clean vs escaping-symlink-removed: differ only in ['SR']`
  - `clean vs in-tree-symlink-metadata: differ only in ['G']`
  - no pair is feature-identical, so the seven classes are jointly separable.
- Under `{H, G, D, P-bucket}` the seven fixtures collapse into blocks
  `{clean, escaping}` (4 envelopes), `{in-tree}` (2), `{dep-be}` (2), `{dep-le}` (2),
  `{avm, body}` (4). A table that ignores BE and SR cannot give different labels inside a
  block, so its maximum is 2+2+2+2+2 = **10**, attained by CTL-C2-6.
- Dropping only SR, or only BE, caps at 12/14. Both features are needed to reach the
  target; neither alone suffices.
- With the conditional 8th class `no-squashfs-chunk` (H empty) the ceilings become
  2/16, 4/16, 8/16, 4/16, 6/16, 10/16, and 12/16 for the no-BE/no-SR shape once it uses
  `handler: none` (`BOUND-no-be-no-sr-8class.md`). Still no kill; the extra class is
  separable without either hidden feature.
- `FEASIBILITY-full-table.md` scores **14/14**, i.e. the grammar as stated can express the
  intended table over the recon signatures. The 10/14 is a control limit, not a grammar
  limit. That table qualifies the AVM row with `handler = squashfs_v4_be` and carries both
  a BE-body and an LE-body row, so it stays correct if D2's endianness is left open.

## 5. Defects in the draft (freeze-blocking unless the text changes)

**D1 — `names sasquatch` must include `sasquatch-v4be`; otherwise the draft is
unachievable.** The grammar says BE is computed for reports "whose `command` ... names
sasquatch". Read as an exact argv token, both AVM and body-failure commands name only
`sasquatch-v4be` and do not name `sasquatch`, so BE is `n/a` for both; the two classes
become feature-identical and **no table can reach 14/14**. Measured (exact-token variant
over `evidence/rea-avm.json` and `evidence/rea-bodyfail.json`): `exact-token BE = n/a` for
both. Smallest safe correction: freeze the sentence as "names sasquatch = some argv token
whose basename starts with `sasquatch`" (what my interpreter does), or state BE's source
explicitly as the report whose `__typename__` is `ExtractCommandFailedReport`.

**D2 — `body-extractor-failure` has no endianness, so its signature depends on the
generator's choice — measured both ways.** BE body damage runs `sasquatch-v4be -be ...`
-> H {`squashfs_v4_be`}, BE `yes`; LE body damage runs `sasquatch -le ...` -> H
{`squashfs_v4_le`}, BE `no` (`evidence/rea-le-bodyfail.json`, same inode-table damage on
the LE tree). The class as named admits both, but a single row cannot catch both, and a
row keyed only on `G = extractor-failure, BE = no` would mislabel an LE body failure as
`avm-marker-be-dropped`. Smallest safe correction: freeze the class as "a v4 **BE** image
whose body is damaged with an intact superblock and no AVM marker" (then the BE row is
enough), or keep both endiannesses and require the table to handler-qualify the AVM row
and carry both body rows — exactly what `FEASIBILITY-full-table.md` now does.

**D3 — `no-squashfs-chunk` is real, cheap and confusable with body damage.** A
truncated image (`bytes_used` past EOF) and a bad magic both yield H empty, G empty, P 0
(`evidence/rea-trunc.json`, `evidence/rea-badmagic.json`) — not `extractor-failure`. If
`heldout-gen.py` makes body failures by truncating, the envelope silently leaves the
`body-extractor-failure` class and no seven-class row matches it (`unclassified`).
Smallest safe correction: adopt the 8th class (it costs exactly one `handler: none` row,
see `FEASIBILITY-full-table.md`) **and** freeze that body damage keeps the superblock and
file length coherent.

**D4 — exact-set gap cells need single-fault held-out carriers.** All G/D cells match the
set exactly, so a carrier with two faults (e.g. missing BE dependency *and* an in-tree
symlink -> G = {missing-extractor-dependency, unpublished-entry}) matches no row and is
`unclassified`; `matched < N` by construction. Smallest safe correction: freeze "each
held-out carrier carries exactly one fault / one gap kind" in `heldout-gen.py`'s contract,
or require the table to carry product rows.

**D5 — `clean` and `escaping-symlink-removed` rows rely on `published files >0`.** An
escaping-symlink carrier that publishes only the symlink has P 0 and would fall through to
`unclassified` (or to a later `handler: none` row if one exists). Either freeze "every
clean / escaping carrier publishes at least one regular file" or keep `>0` only if the
generator guarantees it; do not replace it with `*` before a `handler: none` row, which
would absorb `no-squashfs-chunk`.

Not a defect, but freeze it in the craft text: `n/a` for `-be` means "no sasquatch command
was recorded" (normal success), not "little-endian".

## 6. Evidence — exact commands and observed results

Tools (nothing installed or updated this wave): unblob **26.6.4** at
`~/.local/bin/unblob`; sasquatch-v4be **4.5.1 (unsquashfs 4.5.1)**; rea-agents **6.5.0**
via the cached npx package at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`.
No pacman transaction, no host service touched.

Scratch root `S=/fast/scratch/hyaku/kaidoku-r39/R39C2Shortcuts`; every command below ran
with cwd `$S` (so `unblob.log` never lands in the lane).

1. Dev tree: `tree/{bin/run,docs/readme.md,docs/deep/nested/file.dat,hello.txt,empty}`.
   `python3 <lane>/tools/round-37/gen-squashfs.py tree be-healthy.sqsh --endian be --comp gzip`
   -> `wrote be-healthy.sqsh 671 bytes, inodes 10` (exit 0).
2. Body failure (in-place, superblock untouched):
   `inode_table = u64 BE @64 = 134; b[134:150] = b'\xff'*16` -> `be-bodyfail.sqsh`
   (sha256 `e95caee9…691c98`), `bytes_used` 671 unchanged.
3. AVM marker: `python3 <lane>/.ufo/waves/round-38/w2/artifacts/R38W2AvmProbe/make-avm-copy.py be-healthy.sqsh be-avm.sqsh`
   -> `mkfs_time=671 bytes_used=671 equal=True` (exit 0).
4. REA, fresh outdirs, absolute `REA_UNBLOB_COMMAND`:
   `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware --format json --full-output be-bodyfail.sqsh out-bodyfail`
   -> exit 0, 8408-byte envelope (`ev_6260b1fe60de61890…`), duration 1698 ms;
   `… be-avm.sqsh out-avm` -> exit 0, `ev_ae25a6081e4047145…`;
   `… be-healthy.sqsh out-healthy` -> exit 0, `ev_1cbc5dd273077c348…`.
   Feature extraction on these three: body = H {`squashfs_v4_be`}, G {`extractor-failure`},
   **BE `yes`**, P 0; avm = same but **BE `no`**; healthy = G {}, BE `n/a`, P 4.
   Commands quoted by REA: body `sasquatch-v4be -be -no-exit-code -f -d …`; avm
   `sasquatch-v4be -no-exit-code -f -d …`.
5. Dependency probes with `$HOME/.local/bin` stripped from the child PATH and
   `REA_UNBLOB_COMMAND` absolute: LE image -> H {`squashfs_v4_le`},
   G {(`missing-extractor-dependency`, [`sasquatch`])}, P 0; BE image -> H
   {`squashfs_v4_be`}, G {(`missing-extractor-dependency`, [`sasquatch-v4be`])}, P 0 (both
   exit 0).
5b. LE body damage: the same inode-table corruption applied to `le-healthy.sqsh`
   (`inode_table = u64 LE @64 = 134`), then the same REA command -> exit 0, 8175-byte
   envelope `ev_0e90f099a412f8de4c4de1096bee41eb4621b38bd08229b22e2f6ad2841e1146`, H
   {`squashfs_v4_le`}, G {`extractor-failure`}, BE `no`, P 0; recorded command
   `sasquatch -le -no-exit-code -f -d …`.
6. No-chunk probes: `head -c 400 be-healthy.sqsh` and magic `XXXX` -> both H {}, G {},
   P 0, exit 0 (`ev_c10fd0a4c9c6767f6…`, `ev_f4baaa73572ebbb84…`).
7. Control scoring (all exit 0):
   `python3 triage-eval.py CTL-C2-N-*.md` -> 2, 4, 8, 4, 6, 10 out of 14;
   `FEASIBILITY-full-table.md` -> 14/14; `BOUND-no-be-no-sr-8class.md`
   `--class-signatures class-signatures-with-nochunk.json` -> 12/16;
   `--bounds --json-out bounds.json` -> the three one-feature pairs above.
8. Malformed-cell behaviour of my interpreter: `-be` cell `maybe` -> `UNEVALUABLE: bad -be
   cell 'maybe'`, exit 2; trailing-`+` set cell -> `UNEVALUABLE: bad set cell
   'unpublished-entry+'`, exit 2 (never a silent non-match).

Dev carrier sha256: `be-healthy` `44750c45…5e0261`, `be-bodyfail` `e95caee9…691c98`,
`be-avm` `ebbb3720…b26976`, `be-trunc` `fe0ef0e2…cb946a`, `be-badmagic` `711922f6…59a316`,
`le-healthy` `09d9f933…b4204`, `le-bodyfail` `392a56fd…6427b5`. The body-failure and AVM envelopes carry those subject
digests, so the four features are bound to the copied carriers in `evidence/`.

## 7. Limits and inferences

- The held-out generator does not exist yet; the seven class signatures are recon-derived
  from one or two envelopes each and from my fresh-tree reproductions. They match the
  draft's class names, and `FEASIBILITY-full-table.md` proves the grammar can hit 14/14 on
  them, but that is not a claim about `heldout-gen.py`'s output.
- Body damage was reproduced one way only (inode-table corruption with a valid superblock).
  [INFERENCE] other damage that leaves `bytes_used` and the padding valid will also yield
  `extractor-failure` with `-be`; damage that leaves the superblock or length incoherent
  falls into `no-squashfs-chunk` (measured for truncation and bad magic).
- P counts are per envelope, not per class; the grammar only reads 0 vs >0.
- My interpreter is a validation aid, not the frozen `tools/round-39/sqfs-triage.py`; its
  grammar reading is stated in §1 so the L1 can diff it against the real counter.
- The 8th class is characterised from two synthetic corruptions only; a held-out
  `no-squashfs-chunk` carrier generated some other way could add a gap kind and would need
  its own row.
