# PlanClaimSizing — round 50 wave 1 (pre-freeze), review of the draft plan

Seat: `PlanClaimSizing` (leaf, wave 1 of 2). Plan reviewed: `.ufo/waves/round-50/draft/plans/round-50-claims.md`,
mtime 2026-10-28 20:30:56 -0300, sha256 `83960e43754c698965a3c8d669b8e5e03a99f877ff48044b1482cf00a1c04668`
(read unchanged at 23:32Z; mtime predates the read). Base `7c678ae6d97aedb969fd253b52b3d2882ef1e186` (HEAD verified
read-only). Contract: `kaidoku-round-50.md` item 9 "Claim sizing" (fleet prompt; wording quoted by
`.ufo/waves/round-36/w1/R36CriticPredicateIdentity.md:14-18`). Artifacts: `.ufo/waves/round-50/w1/PlanClaimSizing/`.

## Verdict

**Not freezable as drafted.** Six blocking defects, all reproduced with commands below:

1. **Model count and "dozens" are wrong.** The index holds 70 model directories, not 78. The L1 scan output
   (now present, 70 rows) gives 14 `hsqs`/v4.0/xz/AVM rows, not "dozens", and 26 rows are scan errors (HTTP 416).
2. **Carrier pin for c6430 is wrong.** Its rootfs member is `./var/remote/var/tmp/x86/filesystem.image`, not
   `./var/tmp/filesystem.image`. The carrier table's sizes are member sizes, labelled as image sizes.
3. **The after-value is not re-derivable over committed bytes** (counter needs vendor fetch, `--pkg65`, a counter-time REA rerun).
4. **Causal separability is false.** C2 atoms B1, B9 and B11 read files that C1's landing writes.
5. **Calibration atoms are mis-specified.** B3's count omits C1Battery; B11 counts an absent record, not a mismatch;
   B9 names the wrong registry section and gives no enumerator; B1's base value is wrong; B7 names no tier text or snapshot path.
6. **The P50-C1 predicate is not the round-41 clause list it claims to port.** A clause has no textual counterpart,
   and its delta is cited to a non-frozen seat file.

Everything else in the plan that I could check is consistent: the 7530 superblock, the S149 row, the S147 snapshot,
the handler name, and the round-49 freeze pattern. Replacement wording for each offending sentence is in section 3.

## 1. Findings table

Exit codes: 0 = met / identical, 1 = not met, 2 = could not evaluate. Hashes are sha256 of the bytes as read.

| ID | Sev | Claim / sentence (plan line) | Evidence and command (exit, sha256) | Finding |
|---|---|---|---|---|
| F1 | blocker | "78 FRITZ!Box model directories" (L37) | `curl -sS --max-time 60 -D hdr.txt -o index.html https://download.avm.de/fritzbox/` exit 0; index.html sha `75e886e2…fc40764`; `re.findall(r'href="(fritzbox-[^"/]+)/"')` → 70 unique, no duplicates (74 hrefs total). `wc -l l1/scan-output.txt` → 70. | 78 is not reproduced by the index, the scan regex, or the scan output. Correct value 70. |
| F2 | blocker | "dozens publish … `hsqs`, v4.0, xz, `mkfs_time == bytes_used`" (L37-38) | `python3 -I -B …/tools/round-50/scan-stats.py .ufo/waves/round-50/l1/scan-output.txt` exit 0 → `scan-stats.txt` sha `fbdcd163…4732`. scan-output.txt sha `dd9e427d…d1c3` (5,607 B). | Classification of the 70 rows: **14** `hsqs`-AVM (6430, 6490, 6590, 6850-4g/5g/5g-v2/lte, 7520, 7520-B, 7530, 7583, 7583-vdsl, 7590, 7590-ax); 15 `sqsh`-AVM (BE); 2 `std`; **9 mis-parsed** (magic `./va`, size 0, labelled `std`: 4020, 4040, 6810-lte, 6842-lte, 7312, 7360-sl/v1/v2, 7390); **26 errors** (HTTP 416: Range past end of file; the cause is not diagnosed); 4 no image. "Dozens" is not supported for the LE marker: the count is 14. |
| F3 | blocker | carrier table, `a7590`/`c6430` rows and "tar member `./var/tmp/filesystem.image` sha256" (L46-53) | `python3 -I -B …/tools/round-50/avm-probe3.py fritzbox-7530 fritzbox-6430-cable fritzbox-7590` exit 0 → `probe3.json` sha `41594df1…23e2a3`. Range reads (`Range: bytes=`), no body download. | c6430's rootfs member is `./var/remote/var/tmp/x86/filesystem.image` at offset 5,470,720, size 23,863,304, `hsqs` 4.0 comp 4, `bytes_used == mkfs_time == 23861507`. The pin "`./var/tmp/filesystem.image`" would not match this carrier. 7530 and 7590 use `./var/tmp/filesystem.image` (7530 at offset 724,992; 7590 at 24,576). c6490 member path not probed (3-model limit). |
| F4 | major | carrier table sizes "34 MB", "35.8 MB", "28 MB", "23.9 MB" under "image" (L48-53) | HEAD `Content-Length` (same probe): image bytes a7530 41,850,880; a7590 42,393,600; c6490 39,741,440; c6430 35,911,680. Scan rows (`scan-output.txt` lines 17, 18, 55, 63) and the probe give member sizes 23,863,304 (c6430), 28,200,968 (c6490), 34,005,000 (7530), 35,835,912 (7590). | The table's sizes are **member** sizes. Under the "image" heading they are wrong for all four carriers. |
| F5 | major | "7530-08.25 (34,005,000 B, `mkfs_time == bytes_used == 34003969`, sha256 of the image `b17fe5cd…`)" (L40-41) | probe: 7530 member `./var/tmp/filesystem.image` size 34,005,000, `mkfs_time` 34,003,969 = `bytes_used` 34,003,969 (exact), `hsqs` 4.0 comp 4, offset 724,992. Image HEAD 41,850,880 B. `sha256 of the image` **not run** (full download is outside this seat's Range-only scope). | The superblock numbers are reproduced exactly. The sha256 is attached to "the image", but the 34,005,000 B figure is the member, not the image. Which byte string `b17fe5…` hashes is unknown from the plan. |
| F6 | blocker (§9 after-value) | "one concrete after-value re-derivable by one command over committed bytes" (§9) vs "Counting command … `--pkg65` … `--carrier-cache` … counter-time REA rerun" (L86-88, L62-75, limit 2 at L105-106) | Plan text only; `tools/round-50/` absent at base (checked `ls`). The C1 after-value conjoins a counter-time REA rerun of vendor bytes that are never committed. | Not re-derivable over committed bytes. A closure without the four vendor images (≈36-42 MB each) cannot reproduce `carriers_matched 4`. |
| F7 | major (§9 causal separability) | "The only shared path is `corpus/SOURCES.md` (C1 reads its own cited rows; C2 reads the correction rows for S138/S147/S149)." (L26-27) | Plan text: B1 "knowledge-file count at REV and the C1 entry mapped" (L115-116); B9 "round-50 instruments at REV" (L127-128); B11 "LOG" (L133-134). `git ls-tree -r --name-only 7c678ae… corpus/knowledge \| grep -c '\.md$'` → **139** (exit 0). | Shared writes/reads: `corpus/knowledge/` and `corpus/README.md` `## Coverage map` (C1 adds the entry; B1 counts it), `SKILL.md` registry (B9 counts round-50 rows at REV; C1's instrument row is one of them), `SCORECARD.md` / `LOG.md` (B11; the landing appends there). C2's values at REV therefore move with C1's landing. |
| F8 | major | "B1 owned-axes coverage fraction vs knowledge-file count at REV … (`138/138` at the base vs 139)" (L115-116) | `git ls-tree` as F7 → **139 at the base** (7c678ae). `SCORECARD.md:23` head row reads `138/138 knowledge files mapped at the round-47 landing`. | The base count is 139, not 138. The "138" is the round-47-landing text. The atom's stale value is "SCORECARD 138 vs knowledge 139 at base; 140 at REV if C1 lands". |
| F9 | major | "B3 … (`.ufo/waves/round-48/r48-w1-results.json`: 75 results, `C1Meaning` blocked, `ScribeReportNumbers` aborted; 72 report artifacts)" (L118-120) | `python3` over `r48-w1-results.json` (75 results, status is in `output` text, not a key) plus the w1 tree. Rule A (non-empty `w1/<seat>.md`, `w1/<seat>/<seat>.md` or `w1/<seat>/report.md`) → **72**, missing `C1Battery`, `C1Meaning`, `ScribeReportNumbers` (`b3-count.txt` sha `73f99290…01b1`, exit 0). | 72 reproduces only under rule A, and the plan names two of its three missing seats. `C1Battery` names `w1/C1Battery.md` (absent). `C1Meaning` has `receipt.json` only and status `blocked`. The atom must name rule A and all three seats. |
| F10 | major (§9 counts real mismatches) | "B11 the round-49 lesson's declared freeze, the round-49 SCORECARD section, `FREEZE` and LOG agree (round-49 analogue of A1)" (L133-134) | `git show decc5697…:corpus/lessons/round-49.md` → absent (`git cat-file -e` exit 1); `git show decc5697…:LOG.md \| grep -c decc5697` → 0; same for SCORECARD → 0. At base: lesson L4, SCORECARD:3754, LOG:3453 and `.ufo/waves/round-49/l1/FREEZE` (41 B, `decc5697…`) all agree. | At the freeze the record does not exist, so B11 is red by absence. At base it is green. The closure routed no round-49 freeze defect. B11 counts an absence, not a mismatch. **Drop B11**, or define a value that is red at base for a stated reason. |
| F11 | major | "B9 registry census: every `tools/round-49/**` `.py`/`.sh` path … is the cell-0 path of a `## Local round-evidence gate registry` row" (L127-128) | `git ls-tree -r --name-only 7c678ae… tools/round-49 \| grep -E '\.(py\|sh)$'` → 6 paths (c1-controls, c1-counter, c1-oracle, c1-run.py, c1-run.sh, c2-mismatch) (exit 0). `grep -n 'tools/round-49' SKILL.md` → no output (exit 1). `## Local round-evidence gate registry` is SKILL.md:772-787 and holds 4 pre-round-14 rows. Round-46/47/48 rows sit at SKILL.md:1638, 1720 and 1753-1761. | The named section does not hold round rows, so the census would return 0 rows for any reading. The plan gives no enumerator. The closure's claim that rounds 46-48 are unregistered is contradicted by those rows. |
| F12 | major | "B7 S147 tier correction row (`supersedes S147 —`, tier B per CORPUS tier text, the quote located in the committed snapshot)" (L126) | `grep -n -i tier corpus/QUALITY.md corpus/README.md` → QUALITY.md:110 defers tiers to `corpus/SOURCES.md`; SOURCES.md has no tier-definition table in its header (`sed -n 1,4p`). S147 row (SOURCES.md:153) reads tier `A`. Snapshot `corpus/evidence/round-49/c2/popper.html`: sha `2c2d48c6…ec207`, 118,135 B, matches the row's sha prefix. | "CORPUS tier text" names no file. The snapshot path is missing from the atom. The atom needs the tier-definition file and line. |
| F13 | minor | "B2 `## Owned axes` calibration row cites the round-48 `rejected-harmed` verdict and the round-49 `c2-final` measure" (L117-118) | `SCORECARD.md:25` calibration row: `grep -o -E 'rejected-harmed\|c2-final'` → no output (exit 1). It cites the round-47 landing only. | Red at base. Good as an atom, but it needs its grep command so the value is re-derivable. |
| F14 | major (§9 surface) | "R50-C2 works calibration (round-48/49 record atoms + registry census)" (L20-21); "B6–B9" (L122-127) | Atoms B6–B9 read `corpus/SOURCES.md` and `SKILL.md`. `grep -c SHONEN` on the plan → 0 (no SHONEN atom). §9 requires mismatches between self-assessment (SCORECARD/SHONEN) and observed state. | Name the surfaces: SCORECARD `## Owned axes` head rows, round sections and LOG, plus SOURCES correction rows and SKILL registry. Either add SHONEN atoms or say SHONEN is out of scope. |
| F15 | major (§9 predicate identity; port) | "its clause list is this predicate; the port's deltas are `.ufo/waves/round-50/w1/C1CounterPort/PORT-DELTA.md`" (L60-61) | Round-41 docstring (`tools/round-41/c1-counter.py:2-30`) has "publishes no non-regular entry at its exact path" and the extract-root rule (strip once, `squashfs_v4*` derivation child path, `oracle_root`). P50-C1 has neither textually; it has "accounts for every non-regular oracle entry by the frozen gap/removal rule". | (a) The predicate cites a non-frozen seat file for its deltas. (b) At least one round-41 clause has no textual counterpart. Put the deltas in the frozen plan. |
| F16 | minor (predicate text) | "Predicate P50-C1 …" paragraph opens with "(`tools/round-50/c1-counter.py`; the round-41 counter ported …)" (L60-61) | `tools/round-50/check-predicate-identity.py` (draft, this seat): `--label P50-C1 --counter …` on the round-41 counter → exit 1 (not identical); on a docstring equal to the plan body → exit 0; label absent → exit 2 (`predicate-identity-controls.txt` sha `89e5f884…037`). | The predicate starts at "At the measured revision". The parenthetical is attribution, not predicate. The instrument strips it by starting at that phrase. The counter does not exist yet, so identity is **not run** against a real counter. |
| F17 | minor | "every binding true" (L84); "REA publishes every oracle file of genuine LE AVM members" (L103); "every owned axis at the 10.0 saturation line" (L17) | Plan text. | L84: enumerate the bindings. L103: "genuine LE AVM members" has no enumerator; use "the four frozen carriers". L17: enumerated by the three named axes, acceptable. |
| F18 | minor (FREEZE format) | plan says "the single FREEZE commit pins the final bytes" (L12-13, "One freeze, committed before any data run") without a file format | `.ufo/waves/round-49/l1/FREEZE` is 41 bytes: `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d` plus LF. `git merge-base --is-ancestor decc5697… 7c678ae…` → exit 0. | Specify the round-50 FREEZE as the same one-line format at `.ufo/waves/round-50/l1/FREEZE`, written before any data run. |
| F19 | minor (scan defects, L1 awareness) | the L1 scan (`l1/scan.py`, sha `764fe01e…cff`) | 26 rows HTTP 416; 9 rows read magic `./va` size 0 (not a superblock) and labelled `std`; the `endswith('filesystem.image')` match accepted c6430's x86 path. | Do not cite the scan's `std` or per-model results. Fix the tar walk (PAX/GNU headers) and classify unparsed rows as unparsed. Not re-run (3-model limit). |
| F20 | verified | 7530 superblock (L40-41) | probe F5. | Exact match, including `mkfs_time == bytes_used == 34003969`. |
| F21 | verified | B6 S149 row: "locator `ERRORS`, status `rejected` kept, quote located in `corpus/evidence/round-49/c2/freebsd-sysexits.html`" (L122-125) | `sha256sum corpus/evidence/round-49/c2/freebsd-sysexits.html` → `1fc793a2…45dbf`, 59,251 B; equals the S149 row sha (SOURCES.md:155). `grep -c ERRORS` → 2; `grep -o 'The command was used incorrectly'` → 1. Row status REJECTED. | Atom is executable as written. |
| F22 | verified | handler name `squashfs_v4_le` (L62-72) | `unblob --version` → 26.6.4 (`~/.local/share/uv/tools/unblob`). `…/unblob/handlers/filesystem/squashfs.py:455` `NAME = "squashfs_v4_le"`; `:514` `squashfs_v4_be`; `:549` `squashfs_v4_broadcom` (shares LE magic). Committed round-36 receipts contain `squashfs_v4_le` (33,410 hits by `grep -rhoE`). | The name is real. The counter's handler test must be exact equality, or a `squashfs_v4_broadcom` match will pass silently. |
| F23 | verified | B5 "round-48 final receipts `33f65a91`/`8847042a` named" (plan B5) | `grep -c 33f65a91 LOG.md` → 3; `grep -c 8847042a LOG.md` → 0. | Half-red at base; atom is a valid check. State the FREEZE value. |

Counts used in F2 come from `scan-stats.txt`. The three re-probed models match `scan-output.txt` line for line
(6430 line 17, 7530 line 55, 7590 line 63: member size and AVM flag). That is the only overlap check possible under
the 3-model limit.

## 2. What the plan claims that I could not check

- The 78 count is not reproduced; the "dozens" count is reproduced only as 14. No full scan was run (3-model limit).
- The sha256 `b17fe5cd…` for "the image" was not verified (no full download). The image is 41,850,880 B.
- c6490 superblock and member path: not probed (only HEAD and the scan's member size 28,200,968).
- `tools/round-50/c1-counter.py`, `c2-record.py`, `carriers.json`, `control-fixtures/**` do not exist yet. Checks that need them are **not run**.
- No counter run, no `--data-run`, no unblob run on any carrier, no REA run (out of scope for wave 1).
- "CORPUS tier text" (F12) was not located. The tier definitions were not found in the three files searched.

## 3. Replacement wording (quote → replacement)

- **L37 `The L1 probed 78 model directories by HTTP Range reads`** → "The L1 probe (`l1/scan.py`, output `l1/scan-output.txt`
  sha256 `dd9e427d…d1c3`, 70 rows) covers the 70 `fritzbox-*/` directories of `https://download.avm.de/fritzbox/`
  (index sha256 `75e886e2…4076`)."
- **L37-38 `dozens publish a ./var/tmp/filesystem.image member that is hsqs, v4.0, xz (comp 4) with mkfs_time == bytes_used`**
  → "14 of 70 model directories publish a `filesystem.image` member whose superblock is `hsqs`, v4.0, xz (comp 4) with
  `mkfs_time == bytes_used` (list: `scan-stats.txt`); 26 rows are scan errors, 9 are mis-parsed, 4 have no image."
- **L40-41 `e.g. 7530-08.25 (34,005,000 B, mkfs_time == bytes_used == 34003969, sha256 of the image b17fe5cd…)`** →
  "e.g. 7530-08.25: member `./var/tmp/filesystem.image` at image offset 724,992, 34,005,000 B, `mkfs_time == bytes_used ==
  34003969` (probe receipt `probe3.json`); image 41,850,880 B, image sha256 `b17fe5cd…` (to be recomputed from the pinned chain at freeze)."
- **L46 `tar member ./var/tmp/filesystem.image sha256`** → "tar member = the entry whose basename is `filesystem.image`,
  path recorded in the pin (`./var/tmp/filesystem.image` for a7530, a7590; `./var/remote/var/tmp/x86/filesystem.image` for c6430; c6490 to be probed)."
- **L48 table header `image (download.avm.de/fritzbox/…)`, sizes "34 MB", "35.8 MB", "28 MB", "23.9 MB"** → columns
  `image bytes` (a7530 41,850,880; a7590 42,393,600; c6490 39,741,440; c6430 35,911,680) and `member bytes` (34,005,000; 35,835,912; 28,200,968; 23,863,304).
- **L26-27 `The only shared path is corpus/SOURCES.md`** → "Shared paths, each named: `corpus/SOURCES.md` (both);
  `corpus/README.md` and `corpus/knowledge/` (C1 writes its entry and map row; B1 counts them at REV, so B1 moves with C1 landing: 139 at the base, 140 at REV if C1 lands); `SKILL.md`
  registry (B9 counts round-50 rows at REV); `SCORECARD.md`/`LOG.md` (B11, if kept). C2 is evaluated at REV after C1's landing; its
  freeze-state values are reported separately."
- **L84 `every binding true`** → "every binding listed in the clause list above is true (enumerated: `bindings_false []`)."
- **L86-88 counting command (after-value)** → split into two commands: "After-value, offline: `python3 -I -B tools/round-50/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --json-out <OUT>` over committed receipts and the pinned oracle, `carriers_matched 4`. Counter-time REA rerun: a separate clause, reported as `rerun_matched N`, labelled network-dependent and not part of the offline after-value."
- **L103 `REA publishes every oracle file of genuine LE AVM members`** → "REA publishes every oracle file of the four frozen LE AVM carriers (`tools/round-50/carriers.json`)."
- **L60-61 `its clause list is this predicate; the port's deltas are …PORT-DELTA.md`** → "Predicate P50-C1 (the round-41 P41-C1 clauses ported, deltas listed in full here): [delta 1] `publishes no non-regular entry at its exact path` is restored as `…` or deleted with reason `…`; [delta 2] the extract-root rule (strip once; root = child of the `squashfs_v4*` derivation edge; `oracle_root` when ambiguous) is stated here." The counter docstring must equal this sentence (checked by `check-predicate-identity.py --label P50-C1`).
- **L114 `Atoms (draft list; the counter's docstring is the predicate)`** and **L136 `The wave-1 C2AtomSpec seat finalises the atoms`** → "Atoms B1–B10 are listed here with their exact cell values at the base and the command that computes each; the counter's docstring must equal this list."
- **L115-116 `B1 … (138/138 at the base vs 139)`** → "B1: SCORECARD `## Owned axes` coverage row `138/138` (round-47 landing text, SCORECARD.md:23) vs `git ls-tree -r --name-only <REV> corpus/knowledge | grep -c '\.md$'`: 139 at 7c678ae, 140 at REV if C1 lands."
- **L118-120 `B3 … 75 results, C1Meaning blocked, ScribeReportNumbers aborted; 72 report artifacts`** → "B3: 75 results (`r48-w1-results.json`); rule A (non-empty `w1/<seat>.md`, `w1/<seat>/<seat>.md` or `w1/<seat>/report.md`) → 72; missing exactly `C1Battery` (report named `w1/C1Battery.md`, absent), `C1Meaning` (status `blocked`, `receipt.json` only) and `ScribeReportNumbers` (aborted)."
- **L117-118 B2** → "B2: `grep -c 'rejected-harmed' <SCORECARD ## Owned axes calibration row>` ≥ 1 and `grep -c 'c2-final'` ≥ 1; at base both 0."
- **L126 `B7 … tier B per CORPUS tier text, the quote located in the committed snapshot`** → "B7: S147 row tier `A` → `B` by the tier definition at `<file:line, to be located>`; quote located in `corpus/evidence/round-49/c2/popper.html` (sha256 `2c2d48c6…ec207`)."
- **L127-128 `B9 registry census: every tools/round-49/** .py/.sh path … is the cell-0 path of a ## Local round-evidence gate registry row`** → "B9: every path listed by `git ls-tree -r --name-only <BASE> tools/round-49 | grep -E '\.(py|sh)$'` (6 paths) is the cell-0 path of a row in the SKILL.md registry tables (`<section rule to be pinned: the section whose heading contains 'registry' and the `### Round-N measurement registry` subsections>); round-50 instruments at REV likewise."
- **L133-134 `B11 … (round-49 analogue of A1)`** → drop B11. The closure routed no round-49 freeze defect, and at the freeze the record does not exist (F10).
- **L20-21 `R50-C2 works calibration (round-48/49 record atoms + registry census)`** → "R50-C2 works calibration: the lane's record (SCORECARD `## Owned axes` head rows and round sections, LOG round sections, the round-48/49 lessons, SOURCES correction rows, SKILL registry rows) against committed bytes; SHONEN is named as in scope or out of scope."

## 4. Verified as stated (no change needed)

- 7530 superblock and member size (F20).
- S149 row, locator, quote, snapshot sha (F21).
- `squashfs_v4_le` exists in unblob 26.6.4 source (F22); exact-equality test needed.
- Round-49 FREEZE format (F18) and ancestry (`git merge-base --is-ancestor` exit 0).
- Target logic: C1 target `carriers_matched == 4` and C2 target `mismatches 0` are not reachable by a do-nothing tree
  (base C1 = 0 carriers; C2 red at freeze per F8/F9/F11). The kill rules in the plan match this.

## 5. Tools, receipts, and what was not run

Receipts in `.ufo/waves/round-50/w1/PlanClaimSizing/` (all created by this seat; no lane file touched):
- `probe3.json` (sha `41594df1…23e2a3`, exit 0): HEAD of 4 carriers, index count, Range reads for 3 models; no cookies stored.
- `index.html` (sha `75e886e2…4076`), `index-headers.txt` (5 header lines, no Set-Cookie; `grep -ic set-cookie` → 0).
- `scan-stats.txt` (sha `fbdcd163…4732`, exit 0), `b3-count.txt` (sha `73f99290…01b1`, exit 0).
- `predicate-identity-controls.txt` (sha `89e5f884…037`): exits 1, 1, 0, 2 as listed in F16.
- `tools/round-50/avm-probe3.py` (sha `e23e47ff…dd58`), `tools/round-50/check-predicate-identity.py` (sha `404ad18f…c99`),
  `tools/round-50/scan-stats.py` (sha `6b86e339…aca`), `tools/round-50/pos-control-counter.py` (sha `b834ce6a…c76`).
  These are drafts for the L1 to review or rewrite. Not frozen, not in the lane tree.

Host tools used: `curl`, Python 3 standard library, host `unblob` 26.6.4 (already installed via `uv tool`; read-only use).
**No tools installed or updated.** The pacman pause was not touched.

Not run (declared): full 70/78 scan; image sha256 of any carrier; c6490 superblock; any counter, `--data-run`,
unblob or REA run on carriers; the `c2-record.py` battery. The scratch directory `/fast/scratch/hyaku/kaidoku-r50/PlanClaimSizing/`
was removed after the receipts were copied.

Git: read-only only (`ls-tree`, `show`, `cat-file -e`, `merge-base`, `rev-parse`, `status --porcelain` on the untracked round-50 tree). No mutating command ran.
