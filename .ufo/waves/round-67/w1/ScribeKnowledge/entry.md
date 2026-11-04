# LE AVM-marker SquashFS v4 (`hsqs`) through REA `extract-firmware`: `squashfs_v4_le` on four chain-pinned vendor members under a class-level gap rule (round 67, R67-C1)

status: R67-C1, the round-67 re-freeze of the round-50 measurement — met at the commit that first
adds this entry iff `tools/round-67/avm-le-counter.py --score` reports `carriers_matched 4` of
`target 4`, `met_target true` and exit 0 at that revision (SCORECARD `## Round 67`); the pre-freeze
before-arm is `.ufo/waves/round-67/l1/pre/control-dryrun.json` (`gaps_ok_round50 2`,
`gaps_ok_round67 4`, both red fixtures true, exit 0). A false carrier clause, a drifted engine, rule
or carrier table, or a post-freeze instrument edit replaces this line and the PROVINCE row with the
honest stop; the miss is reported, never narrowed.

source: S<scout-row> — squashfs-tools-ng SquashFS format documentation, `doc/format.adoc` at commit `e3dcf1770fd77a0babcca422dcbe7b2cc7b8ab90` — https://raw.githubusercontent.com/AgentD/squashfs-tools-ng/e3dcf1770fd77a0babcca422dcbe7b2cc7b8ab90/doc/format.adoc — `=== Device Special Files` (heading, fetched-bytes line 730), line 732: "Basic device special files only store a hard-link counter and a device number." (13 words, one occurrence at byte offset 28 445, single line, no markup inside the span); the layout is stated identical for character and block devices, the extended form adds an xattr index, and the Linux major/minor extraction is lines 742-746; character-device type codes 5 (basic) and 12 (extended) at `=== Common Inode Header` lines 549 and 556 — re-read 2026-11-03 (41 981 B, sha256 `08c38b69a9fda3d1a7ce9784132a75cb8c8d65f290e2747af74ab58ae50c82eb`, HTTP 200; the ScoutSource seat's proposal numbers this row S268, renumbered at append)
source: S250 — https://raw.githubusercontent.com/plougher/squashfs-tools/4.7.5/squashfs-tools/unsquashfs.c — `:1287` `if(root_process)` guards the char/block `mknod` at `:1296-1297`; the non-root branch reports "could not create … device …, because you're not superuser!" and goes to `failed` (`:1313-1318`); the FIFO `mknod` (`:1328`) and socket `mknod` (`:1349`) sit outside that gate — re-read 2026-11-03 (116 844 B, sha256 `6222d940c45537d597e2b36d1d46abbc90f0863e7106bab8fa7bdd97fd939341`, equal to the registry cell)
source: S245 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — `:455` `NAME = "squashfs_v4_le"`, `:463` the LE pattern `68 73 71 73 [24] 04 00`, `:53-54` `case Endian.LITTLE, _:` then `commands_args.append("-le")`; the only `is_avm` test (`:48`) sits inside `case Endian.BIG, 4:` — re-read 2026-11-03 (19 842 B, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`, equal to the installed copy)
source: S244 — https://download.avm.de/fritzbox/ — the publisher's listings for the four carrier model `fritz.os/` directories; as recorded in S244 and re-read in the round-50 entry (2026-10-28/29), not re-fetched at this landing
source: S249 — https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/info_en.txt — line 850 licence sentence ("The licensee may create only one copy of the software, which may be used exclusively for backup use.", 18 words); as recorded in S249 and re-read in the round-50 entry, not re-fetched at this landing
verified-at: 2026-11-03 (the landing commit that first adds this entry; the four `corpus/evidence/round-67/c1/<id>/{after.json,run.json}` receipts are present at this draft's cutoff and their own first-add commit is the L1's to name)
recheck: on-refetch — `curl -fsSL https://raw.githubusercontent.com/AgentD/squashfs-tools-ng/e3dcf1770fd77a0babcca422dcbe7b2cc7b8ab90/doc/format.adoc -o format.adoc && sha256sum format.adoc` (expect `08c38b69…`) and `grep -n 'Basic device special files' format.adoc` (line 732). The scoring recheck is `python3 -I -B tools/round-67/avm-le-counter.py --control --root <LANE> --rev <REV> --work <SCRATCH> --out <OUT>` → exit 0 with `gaps_ok_round50 2` and `gaps_ok_round67 4`, then `python3 -I -B tools/round-67/avm-le-counter.py --score --root <LANE> --rev <REV> --freeze 3663e6b21dccf4c4957f459301156664d8b151d6 --pkg65 <rea-agents 6.5.0 package root> --carrier-cache <CACHE> --work <SCRATCH> --out <OUT>` → exit 0 with `carriers_matched 4`; the counter re-runs REA 6.5.0 on the fetched bytes and re-derives the oracle with `unsquashfs` 4.7.5 at scoring time.

## What moved, and only what moved

[observation] At the base `a7a4ce6902204d5c6cc6c4e3e78b4bffe8312b92`, `PROVINCE.md` and
`corpus/README.md` listed "LE AVM members (`hsqs`)" as Frontier in the round-40, round-41, round-42,
round-44, round-49 and round-50 notes (`grep -n 'LE AVM' PROVINCE.md corpus/README.md`).

[observation] The extraction half was measured in round 50 on these four chain-pinned vendor
carriers: rea-agents 6.5.0 `extract-firmware --max-depth 1` published every oracle regular file at
its exact path under the chunk extract root — 4 556, 4 564, 4 709 and 3 955 published regular files,
equal to the frozen oracle counts. Receipts: `corpus/evidence/round-50/c1/<id>/after.json`.
[inference] The division was made on the gap-accounting half, not on publication.

[observation] The round-50 rule (`tools/round-50/gap-rule.json`) made every `char-device` oracle row
a **required** per-row disposition. Each FRITZ!Box carrier holds 13 char-device rows
(`136:0`-`136:7` at `dev/pts/`, `230:0` at `dev/tiatm`, `247:0` at `dev/led`, `3:0`-`3:2` at
`dev/ttyp*`); the round-50 rule silently admitted only `247:0` through
`removed.silent.char-device`, so 12 rows per FRITZ!Box carrier had no disposition of any kind. Each
Cable carrier holds one char-device row (`247:0`, `dev/led`), which `removed.silent` admitted.
Source: `tools/round-50/oracle/<id>.nonregular.tsv`, the `normalized_result.extraction_gaps` of the
round-50 receipts, and the before-arm `.ufo/waves/round-67/l1/pre/control-dryrun.json` (`gaps_ok`
false on `g7581` and `g7582`, true on `c6490` and `c6430`). [inference] That admission is why the
Cable carriers passed while the FRITZ!Box carriers failed.

[observation] Round 67 moves exactly one surface: **`squashfs_v4_le` on LE AVM-marker (`hsqs`)
members, Frontier → Core**, on the same four chain-pinned carriers, under the round-67 gap rule. The
counter is the round-50 engine (`tools/round-50/c1-counter.py`, sha256
`9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813`) loaded by path under
`ENGINE_PIN` and patched at the named bindings; it does not re-implement the scoring engine.

[observation] One engine clause is dropped, and disclosed: `carrier_fresh_ok` — a re-measurement of
the same four pinned carriers cannot be fresh by construction. The drop is recorded in the receipt
as `patches.dropped_clauses`. Every other clause (carrier pin, carve, layout, oracle re-derivation,
publication equality, gaps, path shape, run provenance, parameters, evidence id, projection) is the
engine's own code, unchanged.

[inference] The class rule is an **accounting** change, not a new extraction capability: the
publication of every oracle regular file was already observed in round 50. What was missing is a
disposition rule for inode kinds that a regular-file extractor cannot materialise.

[observation] The round-50 filing stays a miss under its own rule; this entry does not rewrite that
filing or its verdict. R67-C1 is a separate freeze with its own predicate and receipt.

[observation] The four round-67 data receipts are present at this draft's cutoff
`corpus/evidence/round-67/c1/<id>/{after.json,run.json}` (first written 21:54-21:56 lane-local on
2026-11-03): the subject digests equal the carrier pins, the output directories sit under
`/fast/scratch/hyaku/kaidoku-r67/`, and the counts reproduce round 50 exactly (4 556 / 4 564 / 4 709
/ 3 955 published regular files; 637 / 637 / 613 / 568 gaps; 3 / 3 / 1 / 1 removals). Their
`run.json` records name rea-agents 6.5.0, unblob 26.6.4 and sasquatch 4.5.1.

[observation] The staged `--score` at the cutoff is exit 2, not a verdict:
`l1/scores/c1-data-stage.json` records `unevaluable` "rea package does not match the freeze:
package-lock.json sha256 815c18f14daefceeee603065a291e008330ae1af763639e31bab52a58373f803 != frozen
d42d56f0f4f8baf3ecc24f2bd24f9f09e3c99b83592ef85201f74df255e0c6ca", with no `carriers_matched` key.

[unknown] No `--score` receipt with `carriers_matched` exists at this cutoff, so no carrier verdict
is claimed here; the L1 lands the score (reconciling the package-lock pin) or files the honest stop.

## The class rule and its exact scope

[observation] `tools/round-67/gap-rule-v2.json` (sha256
`e66ba022ee3607c9fe74f141902c012b2418ad6d800589b6d2fb888084a4169e`) keeps the round-50 rule's
`allowed` and `structural` blocks and sets `required.char-device` to `false`, with this
`class_disposition` text for the class:

> char-device: not-publishable-by-design: an extractor that writes regular files cannot create a
> device node, so no per-row gap record can exist for this class; the class is accounted for by the
> re-derived oracle table (every char-device row re-derived from the carrier bytes by unsquashfs)
> and by the nonregular_unpublished check (no published regular file may equal a char-device path).
> A gap that names a char device is still allowed and counted.

[observation] The disposition table is: `symlink` — allowed `["unpublished-entry"]`, required
`true`; `char-device` — allowed `["unpublished-entry"]`, required `false`; `block-device` — allowed
`[]`, required `false`; `fifo` — allowed `["unpublished-entry"]`, required `false`; `socket` —
allowed `["unpublished-entry"]`, required `false`; `dir` — allowed `[]`, required `false`.
`structural` is unchanged: `depth-limited 1`, `unknown-chunk-handler 0`.

[observation] The rule's `removed` block is **not** byte-identical to the round-50 one: the
round-50 `removed.silent {char-device: ["247:0"]}` carve-out is absent. The removal is subsumed —
`disposition_check` consults `silent` only for entries whose kind is *required*, and
`required.char-device` is now false — so it cannot make the rule stricter for any char-device row.
The round-50 rule's `claim` key is also dropped and `round`/`supersedes` are added;
`gap_rule_model` appends no problem for an absent `claim` (before-arm `rule_problems.round67 []`).
[inference] The wave text that calls `allowed`/`removed`/`structural` unchanged is therefore
accurate in effect but not byte-exact for `removed`.

[observation] The before-arm control is the do-nothing and red control over the four committed
round-50 envelopes, the same engine, and no claim repair
(`.ufo/waves/round-67/l1/pre/control-dryrun.json`, exit 0):
`gaps_ok_round50 2` of 4 (the two FRITZ!Box carriers fail), `gaps_ok_round67 4` of 4; removing the
`bin/adsl` symlink's `unpublished-entry` gap still fails under the round-67 rule
(`round67_rule_still_fails true`, note "required entry with no disposition (no gap, no
MaliciousSymlinkRemoved) on ['bin/adsl']"); a junk rule that also sets `required.symlink` false
passes that fixture (`junk_rule_would_pass true` — the waiver must stay scoped); and a char-device
path published as a regular file is named by the publication check
(`publication_check_names_it true`, hit `firmware.bin_extract/dev/led`).

[inference] The waiver is exactly one class. Symlinks remain per-row required, so extractor silence
on a symlink is still a failure; the char-device class alone loses the per-row requirement, and it
is still covered twice: every char-device row is re-derived from the carrier bytes into the oracle
table, and `nonregular_published` refuses a published regular file whose path equals a char-device
row. Silence cannot be filled with a fake file.

[inference] This is the QUALITY #94 repair for round 50: a disposition rule must be derived per
carrier class, or exercise every frozen carrier's class before the freeze. The round-50 rule was
generalised from the Cable class (one char device, admitted silently); the round-67 before-arm
exercises both carrier classes (FRITZ!Box with 13 char devices; Cable with 1) and the two red
fixtures before the data.

[unknown] The rule's behaviour on FIFOs and sockets is **unexercised**: `required.fifo` and
`required.socket` are false and `allowed` keeps `unpublished-entry`, but no FIFO or socket row
exists on any of the four carriers — the four nonregular tables hold only `symlink`, `dir` and
`char-device`. S250's gate is char/block-specific; the FIFO and socket branches are outside it, so
the device-privilege law must not be extended to those kinds (QUALITY #96).

## Why a device node is not an unpublished file

[observation] The SquashFS format description states the device-special-file inode layout:
"Basic device special files only store a hard-link counter and a device number" (the new row, line 732);
the layout is identical for character and block devices, the extended form adds an xattr index, and
on Linux the device number encodes major/minor (lines 742-746). [inference] A char-device row is
therefore an inode of a distinct type with no file payload and no path to publish — not a regular
file whose content an extractor failed to write.

[observation] In squashfs-tools 4.7.5, char/block node creation goes through `mknod` under
`if(root_process)`; a non-root run reports "could not create … device …, because you're not
superuser!" and takes the `failed` branch (S250 `:1287`, `:1296-1297`, `:1313-1318`). FIFO
(`:1328`) and socket (`:1349`) creation are not behind that gate. [inference] The privilege gate
corroborates why a regular-file extractor emits no record for a device row, but it is a statement
about one reader's node creation, not about REA's gap schema; the accounting rule rests on the inode
layout (the new row), and the gate is supporting mechanism.

[inference] A rule that demands one disposition per char-device row is unsatisfiable on any carrier:
the extractor cannot create the node, so it can neither publish it, nor report an
`unpublished-entry` gap for it, nor remove it as a malicious symlink. Removing the per-row
requirement is the only disposition that matches the class; keeping the class in the oracle table
and under the publication check is what keeps the rule from becoming a blanket waiver.

[unknown] Why the FRITZ!Box builds ship 13 char devices and the Cable builds 1 is not established
here; the device set is an observation of the oracle tables, not a vendor statement. [unknown]
Whether a root-privileged extractor, or a different extractor that creates device nodes, would
publish them is not measured; the rule's wording is scoped to "an extractor that writes regular
files".

## The four carriers and the observed gap counts

[observation] Carrier identity is the chain pin of `tools/round-50/carriers.json` (image URL → image
sha256 → tar member sha256 → carve to `bytes_used` → carrier sha256); vendor bytes are fetched,
never committed (S249). The counts below are re-counted on 2026-11-03 from the committed round-50
receipts (`normalized_result.files`, `normalized_result.extraction_gaps`, `normalized_result.diagnostics`)
and the frozen nonregular tables; the `gaps_ok` columns are from the before-arm control receipt.

| id | product | carrier B | carrier sha256 | oracle regular | symlink | dir | char-device | gaps (`unpublished-entry` + `depth-limited`) | removals | `gaps_ok` r50 | `gaps_ok` r67 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `g7581` | FRITZ!Box 7581, FRITZ!OS 07.18 | 28 368 210 | `968d997d5401a483a9250ab0e4e34bd632a40bee000af3419a2b8d0e29fa6845` | 4 556 | 639 | 349 | 13 | 636 + 1 | 3 | false | true |
| `g7582` | FRITZ!Box 7582, FRITZ!OS 07.18 | 28 607 082 | `a119b64428e7128e376317472c504605f17f81a2b802439e32194431d94a5bd0` | 4 564 | 639 | 349 | 13 | 636 + 1 | 3 | false | true |
| `c6490` | FRITZ!Box 6490 Cable, FRITZ!OS 07.57 | 28 200 029 | `880370e7f7e15d70b165a96ae3e6efef0cb8dc3e9a6b27b0b925c7fa62caf2d7` | 4 709 | 613 | 300 | 1 | 612 + 1 | 1 | true | true |
| `c6430` | FRITZ!Box 6430 Cable, FRITZ!OS 07.30 | 23 861 507 | `da1c804940f49fcfb3727efbd4f79a4788f86c5819ddda23b5a8221fb898b46f` | 3 955 | 568 | 255 | 1 | 567 + 1 | 1 | true | true |

[observation] Arithmetic of the disposition families, carrier by carrier: on `g7581` the 639
symlink rows carry 636 `unpublished-entry` gaps plus 3 `MaliciousSymlinkRemoved` removals, and the
349 directory rows and 13 char-device rows carry nothing; the same shape holds on `g7582`; on
`c6490` 613 symlinks = 612 gaps + 1 removal, with 300 dirs and 1 char device silent; on `c6430`
568 = 567 + 1. No char-device row is published, gapped or removed in any envelope. [inference] The
pre-round-67 rule's failure was therefore the 12 FRITZ!Box char-device rows per carrier that no
disposition could satisfy, not a missing publication.

## What the rule does not prove

1. [observation] No new carrier: the same four chain-pinned vendor members; four carriers, one
   vendor, xz only, depth 1. The 28-row LE-member census remains a re-count of parsed round-50
   listing metadata, not a superblock re-read of the other models.
2. [observation] No LE AVM kernel image, no nested sub-image below depth 1 (the depth-1 carve
   publishes a nested image as a regular file and does not open it), and no vendor-mangled body
   beyond these four are in scope.
3. [observation] The marker is invisible to unblob and re-stampable: `is_avm` is tested only inside
   the BE v4 branch (S245 `:48`), so every little-endian v4 member takes `sasquatch -le` whether or
   not `mkfs_time == bytes_used`; round 50's patch experiment produced the same REA projection for
   a standard LE body and its re-stamped twin. [inference] The claim is "REA publishes every oracle
   file of these four pinned vendor members", not "REA or unblob recognises AVM".
4. [observation] Vendor bytes are fetched, never committed (S249); the counter-time rerun is
   unrunnable without a `--carrier-cache`, and an image AVM withdraws makes the chain unfetchable.
   The committed receipts and oracle tables are the durable evidence.
5. [observation] The counter drops `carrier_fresh_ok` (disclosed above); the freshness clause of the
   round-50 engine is not satisfied by this re-measurement and is not part of the round-67
   predicate.
6. [observation] The class rule does not establish FIFO or socket behaviour (no such rows on these
   carriers), and the char/block privilege gate of S250 is not a FIFO/socket law (QUALITY #96).
7. [inference] The rule is an accounting rule for a regular-file extractor's projection; it is not a
   statement that device nodes are unrecoverable from the carrier bytes (the oracle tables record
   them) and not a statement about a root-privileged extractor.
8. [observation] The documentation bindings are presence checks, not semantic checks: a
   `PROVINCE.md` Core row naming `squashfs_v4_le` and the AVM marker, a `Round-67 frontier note`
   line, the entry itself, the `corpus/README.md` coverage-map row and the SOURCES row's `used-by`
   cell.

## What was NOT examined (QUALITY #7)

[observation] Not examined at this landing: the `--score` after-arm (the counter's own REA rerun,
oracle re-derivation and verdict; the staged score is the exit-2 package-lock refusal named above);
any LE member of the other 12 census models; any LE AVM body
with compression other than xz; any xattr-bearing LE body (the extended device inode's xattr index
is read from the format text, not observed on a carrier); AVM kernel images; nested sub-images below
depth 1; the big-endian ARM `sqsh` member inside the cable images (the round-41 BE layout); the
`sqsh` v3 rows and the zero-length rows of the census; the AVM 8-byte trailer's content; the git
history of the Freetz `AVM_LE` build branch; the licence text beyond the quoted line; and whether a
root-privileged or device-capable extractor would materialise the char-device rows.

## Instruments named by this entry

[observation] `tools/round-67/avm-le-counter.py` (sha256
`f78ed365ab1d014fb2e80bdee611796dfb4667c9e2ab8f16f2893fdb7c5e0320`), the pinned engine
`tools/round-50/c1-counter.py` (sha256
`9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813`), the round-67 rule
`tools/round-67/gap-rule-v2.json` (sha256
`e66ba022ee3607c9fe74f141902c012b2418ad6d800589b6d2fb888084a4169e`), the round-50 rule (sha256
`43f7c8d712f7e460a13f88b2efffced461bc9081f92bf1fe7eef0c3a900fa0ef`), `tools/round-50/carriers.json`,
`tools/round-50/oracle/**`, `tools/round-50/fetch-vendor.py`, `tools/round-67/c1-run.sh` (the data
harness), and the second reader `tools/round-41/sqfs-list.py`. The before-arm receipts are
`.ufo/waves/round-67/l1/pre/{control-dryrun.json,control-dryrun-c2.json,score-dryrun-at-base.json,selftest-r50.txt,selftest-c2.json}`.
