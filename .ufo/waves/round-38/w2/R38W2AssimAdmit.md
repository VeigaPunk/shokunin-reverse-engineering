# R38W2AssimAdmit — admission review: `corpus/knowledge/2026-10-26-unblob-format-matrix.md`

**VERDICT: CONFIRMED — admit stands. Every re-derivable claim in the admitted entry reproduces against today's live page, the pinned tag bytes, and the cloned handler source; both stated corrections are real improvements over the staged original; no falsifying finding.**

Axes (godspeed): coverage (every numeric/quote claim re-derived from primary bytes) and calibration (correction honesty, producer-coverage vs outcome separation). No tooling installed or updated (curl and git were preinstalled host tools; scratch used, then removed).

## 1. Live-page claims re-derived (https://unblob.org/formats/)

Re-fetched 2026-10-26 into scratch and copied to `.ufo/waves/round-38/w2/artifacts/R38W2AssimAdmit/formats.html`:

| Entry claim | My re-derivation | Match |
|---|---|---|
| HTTP 200, 216890 B, sha256 `8f8c29af…5bbc5` | `curl -fsSL -w 'HTTP %{http_code} %{size_download}B'` → `HTTP 200 216890B`; `sha256sum` → `8f8c29aff33d5aa1ee2a69f8a66f272d45fa3dd98d271c95337c3ff15a65bbc5` | byte-identical — zero drift since the entry's 03:44-03:00 read |
| 97 `<h2 id=` handler sections | `grep -o '<h2 id=' formats.html \| wc -l` → `97` | ✓ |
| meta description quote "parses unknown binary blobs for more than 30 different archive, compression, and file-system formats" | found verbatim in `<meta name="description">` (line 9); the 3 occurrences are meta + `og:description` + `twitter:description` (lines 9, 75, 83) | ✓ |
| 3 occurrences of "more than 30 different" | `grep -c 'more than 30 different'` → `3` | ✓ |
| Ten SquashFS sections: v1, v2, v2-non-standard, v3, v3-Broadcom, v3-DDWRT, v3-non-standard, v4-BE, v4-broadcom, v4-LE | exactly ten `squashfs-v*` h2 ids; display text extracted: `SquashFS (v1)`, `(v2)`, `(v2-non-standard)`, `(v3)`, `(v3-Broadcom)`, `(v3-DDWRT)`, `(v3-non-standard)`, `(v4-BE)`, `(v4-broadcom)`, `(v4-LE)` | ✓ incl. the BE/broadcom casing |
| Each section has a support status and a handler type; "in some cases" a vendor | structural: 97 `Handler type` occurrences; 97 status admonitions (89 `admonition success` + 8 `admonition warning`), i.e. exactly one per section; `Vendor` ×42 of 97 | ✓ |
| ZIP note "Does not support encrypted ZIP files." | exact string found once, as `<li>Does not support encrypted ZIP files.</li>` | ✓ |
| Footer present but not used as staleness evidence | `Copyright © 2021 - 2025 ONEKEY GmbH` present (1 occurrence) | ✓ honestly scoped |
| Both recheck commands | `grep -o '<h2 id=' \| wc -l` → 97 and `grep -c 'more than 30 different'` → 3, reproduced today | ✓ |

## 2. README '78+' at tag 26.6.4 (S110)

- `curl https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md` → sha256 `6544d60f22f7b521f8705b3bba5d47a50e428ccbd3359542708dbd009ccf3716` — identical to the hash pinned in lane SOURCES row S110; 235 lines, matching S110's "235 lines".
- Line 5: "…**78+ archive, compression, and file-system formats**…" ✓; line 22: "- **78+ supported formats** …" ✓; `grep -n '78+'` → only lines 5 and 22 ✓. Exactly as the entry states.

## 3. The two stated corrections — both verified as genuine

1. **`v4-Broadcom` → `SquashFS (v4-broadcom)`:** the page's display text for `id="squashfs-v4-broadcom"` is literally `SquashFS (v4-broadcom)` (lowercase b), while v4-BE is uppercase. The staged original's "SquashFS (v4-Broadcom)" misquoted the page; the correction is exact.
2. **"42 vendor-attributed entries" → count of the word `Vendor`:** `grep -o 'Vendor' formats.html | wc -l` → `42` (separately, lowercase `vendor` ×2). The staged number was a token count, not a per-handler attribution count; the admitted entry's deflation is correct and material (42 of 97, consistent with "in some cases a vendor").

## 4. sasquatch-v4be / S112 cross-reference

Shallow clone of tag `26.6.4` → commit `1fcc7a0a584a70a96c31f5a276c20944d199a089`, the same commit S110 and S112 both pin. `python/unblob/handlers/filesystem/squashfs.py` (590 lines): `SquashFSExtractor` defines `EXECUTABLE = "sasquatch"`, `V4BE_EXECUTABLE = "sasquatch-v4be"` (lines 25-26), selects it via `case Endian.BIG, 4:`, and `get_dependencies()` returns both executables — exactly S112's anchor. Ten handler `NAME`s in the module (`squashfs_v1…squashfs_v4_broadcom`) match the page's ten sections one-to-one. The entry's "the section is served by the external `sasquatch-v4be` (S112)" is structurally true at the pinned tag, and the sibling measured entry `2026-10-26-r38-sasquatch-be-squashfs-recursion.md` exists and cites S112 as the entry claims.

## 5. Renumbering by document (staged S122 → S116, staged S106 → S110)

- Staged package `/home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md` carries row S106 (README at `…/HEAD/README.md`, fetched 2026-10-23) and row S122 (the formats page, fetched 2026-10-23) — the ids the entry says it renumbered.
- Lane `corpus/SOURCES.md`: S116 is the formats-page row ("staged as package S122, renumbered by document", opened 2026-10-26, sha/byte/count anchors identical to my fetch), used-by exactly the admitted entry; S110 is the README row at tag 26.6.4 ("staged as package S106, renumbered by document").
- Identity of the S106→S110 document verified beyond the label: today's `HEAD/README.md` is **byte-identical** to the tag-26.6.4 README (same sha256 `6544d60f…`), so the staged quotes at HEAD and the lane's tag-pinned row are the same document bytes — the "renumbered by document" claim is exact, not just nominal.

## 6. PROVINCE scope — in-province, not generic/sibling material

The lane's PROVINCE makes unblob extraction first-class Core: "Firmware regions + extract" (`REA_UNBLOB_COMMAND=~/.local/bin/unblob` (26.6.4), Round-4 additions), the `sasquatch` Frontier bullet, and a 2026-10-26 frontier note that already cites the sibling unblob entries. The format matrix is producer documentation of exactly that held extraction surface, and the entry grounds it on "the firmware extraction and region-inspection axis … F1 sasquatch frontier item" (staged) / the measured BE v4 run (admitted). Nothing in the entry reaches outside the domain (no verdicts, no sibling-lane routing). Generic- or sibling-domain objection: rejected.

## 7. QUALITY bar

- The claim is explicitly framed as "producer's coverage statement, not outcome", with the caveat section retaining "a support matrix claims coverage, never an outcome" — the staged entry's one unsourced inference (site staleness from the copyright footer) was dropped; the footer is recorded as present but not used as evidence. That is a calibration gain, and I verified the footer's presence so the residual statement is true.
- Every number in the admitted entry that could be checked was checked and reproduced; the two corrections are quote-backed and now independently reproduced (§3).
- Recheck line is executable as written and reproduced today (97 / 3).

## 8. Observations (non-defects, no action required)

- `grep -o 'Fully supported'` counts 90 while only 89 success admonitions exist: one prose occurrence outside sections. The entry never claims a status count, so nothing is wrong; noted only so a future reader doesn't "fix" 90+8=98 against 97.
- The entry's S110 source-line parenthetical "(staged as package S106; same document as lane S110)" is redundant with its own narrative but factually consistent.
- Handler `NAME`s use `squashfs_v2_nonstandard` where the page id is `squashfs-v2-non-standard`; the entry claims page sections, not handler NAME strings, so this is not a mismatch.

## 9. Residual risk and verification gaps

- The page fetch is live-site evidence: today it is byte-identical to the entry's pinned fetch (same sha256), but future rebuilds can change it — that is what the 180d recheck line is for, and its commands reproduce.
- The historical 2026-10-23 staged fetch (S122's original read) cannot be re-observed; its key surviving assertions (97 sections, "more than 30" ×3) all still hold today, so the staged→admitted continuity carries no contradiction.
- I verified the admission content, not the SCORECARD/LOG bookkeeping rows (other seats' scope).

**Conclusion: the admission is accurate, correctly scoped, and strictly better-calibrated than its staged original. Admit.**
