# R38W2RegistryTally — registry integrity of the round-38 landing

**Verdict: DEFECTS FOUND.** Structure, ids, dates, tallies and the S110 edit are exactly as the landing describes, and `sources-census.sh validate` exits 0. The defect is registry economy and independence accounting: the landing appends **S112, a second row for the same document S108 already holds** (same URL, same tag, same 590-line file, same sha256 `2d7b901b…9287`, positive scope a proper subset of S108's), so the registry reports 116 rows for 115 distinct documents and the round-38 BE entry binds its dependency claim to the duplicate instead of S108. Four minor cell-level defects follow from the same landing (unpinned floating-ref row S114, half-pinned S113, own-work row S115 with no artifact path, `applies`→`apples`).

Judged at `0fc6113376a156fddc3ec385386d71c3a4a9f690` against base `77091b492cc53f8743bd0701b1e7d5e66123dd84`. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Read-only throughout: `git show`, `git ls-tree`, `git diff --stat`, `git ls-remote`, `curl`, `sha256sum`, `grep`, one read-only census run. No VCS mutation, no writes outside this report, scratch removed, no tools installed.

---

## 1. What the assignment expected, measured

Two SOURCES.md snapshots were extracted and parsed independently in Python (split on `|`, strip, 11 cells) and cross-checked against `sources-census.sh`, which parses the same file with gawk under SOURCES-CONTRACT-v1 (NF=13). Both parsers agree on every number below.

| Expected | Measured | Verdict |
|---|---|---|
| row count delta | base 111 → head 116 (+5) | as expected |
| ids added | `S112, S113, S114, S115, S116`, all appended at the table tail, base order byte-preserved (`order preserved: True`) | as expected |
| per-status tally | base `mined 107 / rejected 4` → head `mined 111 / rejected 5` (delta +4 mined, +1 rejected) | arithmetic consistent |
| per-tier tally | base `A 104 / B 6 / C 1` → head `A 108 / B 7 / C 1` (A +4 = S112, S113, S115, S116; B +1 = S114) | arithmetic consistent |
| per-kind tally | base `code 30 / community 4 / dataset 13 / docs 38 / own-work 9 / paper 6 / spec 8 / tool 3` → head `code 31 / community 4 / dataset 14 / docs 40 / own-work 10 / paper 6 / spec 8 / tool 3` | consistent with the five new kinds |
| cells changed in pre-existing rows | **exactly 2**: `S110.scope`, `S110.used-by` | as expected, nothing else |
| every new row 11 columns, no literal or escaped `\|` in a cell | 116/116 rows = 11 cells; `grep '\\|'` on SOURCES.md = 0 matches; census E01 (NF≠13) silent | clean |
| `opened` = 2026-10-26 on new rows | all five `2026-10-26`; `recheck` all `180d` | as expected |
| id integrity | `S001…S116` contiguous, 116 ids, 0 duplicates, all `^S\d{3}$` | clean |
| registry section integrity | one `## Registry` table, rows on lines 7–122, `## Paths` at 125, then `## Search log`, `## Leads (unopened)`; no row-shaped line outside the table (census E12 silent) | clean |

`git diff --stat 77091b49 0fc61133 -- corpus/SOURCES.md` → `1 file changed, 6 insertions(+), 1 deletion(-)`, i.e. five appended rows plus the single replaced S110 line. No `Paths`, `Search log` or `Leads` cell moved.

### The two changed cells, byte-exact

```
S110 / scope
  BASE: …its Debian-package install route only; not evidence about any image
  HEAD: …its Debian-package install route, plus its own "78+" format-count sentence (lines 5, 22) only; not evidence about any image
S110 / used-by
  BASE: corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md
  HEAD: corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md, corpus/knowledge/2026-10-26-unblob-format-matrix.md
```

Both halves of the widened scope verify against live bytes (see §3): line 5 and line 22 of the pinned README are the only two `78` matches in that file, so "(lines 5, 22)" is exact, and the new used-by target is a real entry that cites S110 in its frontmatter.

### New-row cells

| id | kind | tier | status | opened | recheck | used-by (head) |
|---|---|---|---|---|---|---|
| S112 | code | A | mined | 2026-10-26 | 180d | `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` |
| S113 | dataset | A | mined | 2026-10-26 | 180d | `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` |
| S114 | docs | B | mined | 2026-10-26 | 180d | `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` |
| S115 | own-work | A | rejected | 2026-10-26 | 180d | `—` |
| S116 | docs | A | mined | 2026-10-26 | 180d | `corpus/knowledge/2026-10-26-unblob-format-matrix.md` |

Enums, tiers and the community-never-A rule are respected (no community row added).

---

## 2. used-by ⇄ citation check (both directions)

The lane's binding rule (`SKILL.md`, round-22 checklist) is that a counted entry's `source:` names a **mined** row that names that entry in `used-by`. Tested mechanically over `corpus/knowledge/*.md` (126 files) for all five new ids:

| id | entry declaring `source: <id>` | row used-by | binding |
|---|---|---|---|
| S112 | r38-sasquatch-be-squashfs-recursion | same entry | closed |
| S113 | r38-sasquatch-be-squashfs-recursion | same entry | closed |
| S114 | r38-sasquatch-be-squashfs-recursion | same entry | closed |
| S116 | unblob-format-matrix | same entry | closed |
| S115 | none (cited only in prose: "recorded as a rejected row (S115), not as a source") | `—` | correct for a rejected row, see D5 |

Reverse direction — does any `used-by` cell name a file that does not mention the id? **Zero rows out of 116.** No used-by claim in the registry is fabricated.

Third direction — prose mentions. 24 of 116 rows omit ≥1 knowledge file that mentions the id without declaring it a source (e.g. S003 omits `2026-10-19-arc3-r12-go-evidence-id-domain.md`, S075–S078 omit the r28/r29 EVM entries). So prose-mention accounting is not this lane's convention, and S112/S115 sit inside a 24-row-consistent class rather than violating a rule — recorded as D5 (calibration), not a defect on its own.

---

## 3. Anchors re-opened live (registry rows must stand without the wave artifact)

Network available; all fetches HTTP 200, digests computed locally.

| row | live check | row claim | agrees |
|---|---|---|---|
| S110 | `README.md` @26.6.4, 235 lines, sha256 `6544d60f22f7b521f8705b3bba5d47a50e428ccbd3359542708dbd009ccf3716`; `grep -n 78` → lines 5, 22 | 235 lines, same sha256, `"78+"` at 5 and 22 | yes |
| S112 | `squashfs.py` @26.6.4, 19842 B, 590 lines, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`; class `SquashFSExtractor` at line 24, `V4BE_EXECUTABLE = "sasquatch-v4be"` line 26, `case Endian.BIG, 4:` line 40 → `executable = self.V4BE_EXECUTABLE` line 41, `get_dependencies` lines 68-69 → `[self.EXECUTABLE, self.V4BE_EXECUTABLE]` | same tag, `SquashFSExtractor` lines 24-70, V4BE argv, `get_dependencies()` returns both names | facts yes; no digest in row (D-minor) |
| S113 | raw LFS pointer `__input__/squashfs_v4.nopad.bin` @26.6.4 → `oid sha256:a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed` / `size 307`; `git ls-remote` tag 26.6.4 → `1fcc7a0a584a70a96c31f5a276c20944d199a089` (lightweight, no `^{}`) | same oid, same size, same commit | yes |
| S113 | lane carriers hashed in place: `K3/carrier.bin` 4096 B `9c7c523c5d1d1cafc0b679af9092ce0289d9656f6a24bc3bd0009f95b69397c0`, `K4/carrier.bin` 307 B `a29ddc15…56ed` | scope: "byte provenance of R38-C1 carriers K3/K4" | yes for K4 from the registry alone; K3's oid absent from the row (D3) |
| S114 | `AVM-BE-format.txt` on `master`, 1496 B, sha256 `c1c43f6f97d7477dcdab15203d11e43b49beb12e3a43a3b52bdd71b672a9a5d5`; lines 1-2 the quoted opening sentence; lines 13-14 `mkfs_time` "contains … the same value as … `bytes_used`" | quoted sentence; `mkfs_time == bytes_used` | facts yes; no pin in row (D2) |
| S116 | `https://unblob.org/formats/` 200, 216890 B, sha256 `8f8c29aff33d5aa1ee2a69f8a66f272d45fa3dd98d271c95337c3ff15a65bbc5`; 97 `<h2 id=`; `id="squashfs-v4-be"` titled `SquashFS (v4-BE)` under "Fully supported"; meta "more than 30 different archive, compression, and file-system formats" ×3; ten `squashfs*` headings | exactly these counts and strings | yes |
| S115 | committed artifact `.ufo/waves/round-38/w1/artifacts/R38CrossToolK4/7z-refusal.txt` at `0fc61133`: K1/K2/K3/K4 each `ERROR: … Cannot open the file as archive`, `### exit_code=2`; LE control `7z-le-positive-control.txt`: `Type = SquashFS`, `File System = SquashFS 4.0`, `Big-endian = -`, listing, `exit=0`, image sha256 `b1d283fb…`; `tool-versions.txt` → `7z: 7-Zip 26.04 (x64) 2026-10-05`; installed `/usr/bin/7z` banner identical | "7-Zip 26.04 … exit 2 on K1-K4; LE v4 control opens (exit 0)" | yes, fully grounded |

No row's stated fact was refuted by live bytes. [INFERENCE] The registry's factual layer is sound; the defects below are accounting and pin-discipline defects, not fabrications.

---

## 4. Findings

### D1 (major, unique to this seat) — S112 is a second row for the document S108 already holds

S112 and S108 are the same URL at the same tag, and the same bytes:

```
S108 source: unblob SquashFS handler at tag 26.6.4 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py
S108 scope : How unblob 26.6.4 names and invokes its SquashFS extractors (sasquatch, sasquatch-v4be), the LE/BE argv and the AVM test only; not unblob's traversal engine, not REA's gap wording, not any carrier
S108 anchor: tag 26.6.4 = commit 1fcc7a0…; 590 lines, sha256 2d7b901b…9287; lines 24-26 EXECUTABLE and V4BE_EXECUTABLE, 48-50 AVM test, 58-62 argv tail, 68-69 get_dependencies
S112 source: unblob SquashFS handler at tag 26.6.4 — (same URL)
S112 scope : v4 BE extractor dependency and argv for unblob 26.6.4 only; not the binaries themselves, not other versions
S112 anchor: tag 26.6.4 = commit 1fcc7a0…; `SquashFSExtractor` lines 24-70: … `get_dependencies()` returns `sasquatch` + `sasquatch-v4be`
```

- S112's **positive** scope ("v4 BE extractor dependency and argv") is contained in S108's scope, which already names `sasquatch-v4be` and "the LE/BE argv and the AVM test" explicitly.
- Every fact S112 asserts is in S108's anchor at the same or a wider line range (lines 24-26 ⊂ 24-70; 68-69 = `get_dependencies`). S112's own anchor carries **no** file-level digest and no file length (it gives only the nested line range 24-70) — it is strictly less pinned than S108 for identical bytes.
- `git ls-remote` + local sha256 confirm the two rows resolve to one file (`2d7b901b…9287`), and the round-38 lesson's own S112 gate row records that digest as "= S108 digest".
- Consequence: rows 111 → 116 appends **five rows for four distinct documents** (S112≡S108, S113, S114, S115 own-work, S116), and the round-38 BE entry's `source:` binds the BE-v4 dependency claim to the duplicate rather than to S108, whose `used-by` therefore still names only the round-36 entry even though round 38 depends on those exact bytes. The format-matrix entry also cites `(S112)` in prose, so the duplicate is cited twice.
- Why the contract does not catch it: SOURCES-CONTRACT-v1 E04 keys on identical URL **and identical scope text**; differing wording downgrades to W04 ("duplicate url … across scopes"), which is a warning and left exit status 0. Census emitted exactly one new W04 for this (S112), so the landing is visible to the tool and was described by the L1 as "across scopes, not E04" — the wording differs, the asserted fact does not.
- Precedent check: the lane's other nine W04 groups assert materially distinct things from one artifact (S083 Ghidra target naming vs S090 Rust reader vs S092 SQLite reader on one tarball; S047 a specific archive digest vs S038 the index; S032/S033 where S033 adds a head-commit pin and patch digest that S032 lacks). S112 adds no fact and no pin, so it does not fall in that precedent.

[INFERENCE] Advisory fix (L1-owned, not applied): drop S112 and bind `2026-10-26-r38-sasquatch-be-squashfs-recursion.md` `source: S112` → `S108`, appending that entry to S108's `used-by`; or, if the BE-v4 isolation is wanted as a teaching unit, declare S112 as superseding S108 (the lane's S052/S054 pattern) and mark S108 `superseded`, so the count of live rows does not double a document.

### D2 (minor) — S114 is the only new row pinned to a floating branch with no digest

`source` is `…/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt`; the anchor cell contains no sha256 and no byte/line count (`re.search('[0-9a-f]{64}')` → False). This is the exact defect the lane fixed two rounds ago and recorded **in this same registry**: S111 carries "branch master, 30 lines, sha256 `f09961ee…1fef`" and the round-36 gate decision was "pins by document instead of a floating `HEAD`". With a 180d recheck and no digest, drift on `master` is undetectable from the row; the digest `c1c43f6f…a5d5` (1496 B, identical to the committed `.ufo/waves/round-37/probes/avm.txt`) exists only in the lesson.

### D3 (minor) — S113's scope covers K3 and K4, its anchor pins only K4's LFS object

The anchor gives one pointer, `squashfs_v4.nopad.bin` (`a29ddc15…56ed`, size 307) = K4. K3's object (`squashfs_v4.bin`, oid `9c7c523c5d1d1cafc0b679af9092ce0289d9656f6a24bc3bd0009f95b69397c0`, 4096 B) is absent from the row and appears only in `.ufo/waves/round-38/w1/R38ScoutUnblobFixtures.md`. I verified both lane carriers equal those oids, so the claim is true — but a registry-only reader can close one of the two halves the scope promises. (Sibling `R38W2SrcS113.md` owns the per-row check; this is the cross-check of the row's scope against its own anchor.)

### D4 (minor) — S115 `source` names no artifact path, against 9/9 own-work precedent

`7-Zip 26.04 BE v4 refusal — own-work (committed tool output)` contains no path. All nine base own-work rows name their receipts in the `source` cell (S039, S053, S055, S057, S060, S061, S063, S067, S072 — each carries one or more `.ufo/waves/…` paths). The committed artifact exists and I read it (`.ufo/waves/round-38/w1/artifacts/R38CrossToolK4/7z-refusal.txt`), so this is a locatability defect on the one row class whose whole value is "the output is committed": nothing in the registry points at it.

### D5 (calibration, no census rule) — used-by under-records prose citations

S112 is cited in `2026-10-26-unblob-format-matrix.md:32` and S115 in `2026-10-26-r38-sasquatch-be-squashfs-recursion.md:22`, but neither appears in those rows' `used-by`. Base rate: 24/116 rows already omit knowledge-file mentioners, so this is convention-consistent for mined rows; for **rejected** rows the lane's older rows do record their citers (S022 → `lessons/round-13.md`, S028 → `lessons/round-17.md`, S100, S105 → their knowledge entries), so S115's `—` is the weaker choice of two lane-precedented behaviours. No fix needed for the census; recorded so the next round does not read `—` as "uncited".

### D6 (cosmetic) — two cell-text defects

- S113 scope: "unblob's own expected `__output__` **apples** too" — intended "applies".
- S112 anchor quotes `case Endian.BIG, 4: executable = self.V4BE_EXECUTABLE` inside quotation marks, but the file has these as two lines (40 and 41); S108's anchor uses line ranges instead. Same class as the paraphrase-in-quotes finding of siblings `R38W2SrcS112.md` / `R38W2SrcS114.md`.

---

## 5. Census (verbatim)

Command (from `/home/vgpnk/Projects/shokunin`):

```
bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
```

Output:

```
kaidoku	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
kaidoku	W04	S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
kaidoku	W04	S054 duplicate url developer.android.com/ndk/guides/abis across scopes
kaidoku	W04	S062 duplicate url raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1 across scopes
kaidoku	W04	S069 duplicate url www.wireshark.org/docs/man-pages/tshark.html across scopes
kaidoku	W04	S083 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S090 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S092 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S102 duplicate url learn.microsoft.com/en-us/windows/win32/debug/pe-format across scopes
kaidoku	W04	S112 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py across scopes
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
```

**Exit code: 0.** Nine W04 warnings pre-exist (round-36 lesson records nine at that time); the tenth, S112, is this landing's and is finding D1. No E-code, so no malformed row, duplicate id, enum violation, bad date, missing used-by path, or stray row outside `## Registry`.

Independent tally cross-check (`bash scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kaidoku`, exit 0):

```
kaidoku	rows	116
kaidoku	tier.A	108
kaidoku	tier.B	7
kaidoku	tier.C	1
kaidoku	status.mined	111
kaidoku	status.rejected	5
kaidoku	missing	0
```

This matches the independent Python parse exactly (116 / 108 / 7 / 1 / 111 / 5).

---

## 6. Calibration notes for the L1

- The landing's two observable commitments (ids S112–S116 appended; only S110's scope and used-by edited) hold exactly, and every new anchor's facts verify against live bytes. The registry's problem is not truth but **count discipline**: one appended row is a duplicate of an existing document, so "116 sources" is 115 documents, and the duplicate is load-bearing for the round-38 entry's `source:` binding.
- The duplicate passed both the census and the L1's own review because the contract's duplicate test is textual (`URL`+`scope`), while scope containment (S112 ⊆ S108) is invisible to it. [INFERENCE] A one-line addition to the census — flag a W-code when a new row's URL matches a row whose `scope` text is a superset by keyword overlap, or simply require the row to state the delta from the same-URL predecessor — would have caught this at the mirror gate that already ran (`R38ExecMirrorGate.md`, attempt-1 exit 0).
- Pin discipline regressed once against the lane's own round-36 fix: S114 is a floating-branch row with no digest while S111 (same section of the same table) shows the pattern. The registry's own `used-by`/anchor cells are the only drift detector for a 180d recheck, so an unpinned row is unpoliced until then.
- No frozen predicate, counter, carrier or oracle was touched; nothing here bears on C1 or C2 verdicts, whose counters were left alone.

## 7. Bounds compliance

- Wrote only this file. No writes to `corpus/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `tools/`, the fleet repo, sibling lanes or `/home/vgpnk/Projects/shokuknow`.
- No `git add/commit/checkout/reset/stash/pull/push`; read-only `git show`, `git ls-tree`, `git diff --stat`, `git ls-remote` only. No fixture repo created.
- Scratch `/fast/scratch/hyaku/kaidoku-r38/R38W2RegistryTally` (fetched `sq.py`, `README.unblob`, `formats.html`, `avm.txt`, `lfs.json`, snapshots of SOURCES.md) removed at end; every cited value is reproduced above.
- No REA invocation, no tools installed or updated, no pacman transaction, `~/.local/bin/sasquatch*` untouched.
- Leaf seat: no subagents, no background jobs, no broadcast. Sibling reports `R38W2SrcS112/S113/S114/S115` cover the per-row anchor re-opens; D1 (cross-row duplicate), the tallies, the used-by bidirectionality, the S110-edit verification and the census run are this seat's and did not depend on them.
