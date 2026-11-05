source: S116 — https://unblob.org/formats/ — `<h2 id=` handler headings, `squashfs-v4-be` section, ZIP limitation note, meta description — HTTP 200, 216890 B, sha256 8f8c29aff33d5aa1ee2a69f8a66f272d45fa3dd98d271c95337c3ff15a65bbc5, as read 2026-10-26T03:44-03:00 (staged as package S122, renumbered by document)
source: S117 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md — lines 5 and 22, "78+" format count — sha256 6544d60f…3716, as read 2026-10-26T04:07-03:00 (staged as package S106; same document as lane S110, whose scope cell covers only the sasquatch sentence, so the count sentences get their own row)
verified-at: 2026-10-26
recheck: 180d — `curl -fsSL https://unblob.org/formats/ | grep -o '<h2 id=' | wc -l` → 97 and `| grep -c 'more than 30 different'` → 3 (ran 2026-10-26); different counts mean the site was rebuilt and the entry is re-read

# unblob's format matrix lists 97 handlers, including `SquashFS (v4-BE)` and the vendor-mangled variants; its site description still says "more than 30"

Assimilated in round 38 from the shokuknow `corpus-expansion-1` package
(`merge/kaidoku/knowledge/corpus/knowledge/unblob-format-matrix.md`, staged 2026-10-23). The lane
re-opened both sources on 2026-10-26 and renumbered the staged ids by document: staged S122 → S116
(new row), staged S106 → S117 (new scope row on the document lane S110 already holds; S110 itself
is unchanged). One correction was made
before admission: the staged "v4-Broadcom" is spelled `SquashFS (v4-broadcom)` on the page. The
staged "42 vendor-attributed entries" stands as a per-section count: 42 of the 97 sections carry
one `Vendor:` field, and one of the 42 values is the literal `unknown` (`squashfs-v3-non-standard`).
(Wave-2 seat `R38W2SrcS116` caught an earlier draft that wrongly "corrected" this count.)

**Claim (producer's coverage statement, not outcome).** The documentation site's
"Supported Formats" page carries 97 `<h2 id=` handler sections. Each section has a support status
(89 "Fully supported", 8 "Partially supported", counted per section), a handler type, and 42 of
them a `Vendor:` field (S116). Ten SquashFS sections are listed: `v1`, `v2`, `v2-non-standard`,
`v3`, `v3-Broadcom`, `v3-DDWRT`, `v3-non-standard`, `v4-BE`, `v4-broadcom`, `v4-LE`. The matrix
also records limits as well as support: ZIP is "Partially supported" with "Does not support
encrypted ZIP files."

**The count conflict.** The page's own meta description says unblob "parses unknown binary blobs
for more than 30 different archive, compression, and file-system formats" (S116, 3 occurrences in
the served HTML). The README at tag 26.6.4 says "78+ archive, compression, and file-system formats"
(S117, line 5; repeated as "78+ supported formats" at line 22). The matrix itself lists 97 sections.
Quote the site's description as the site's sentence, never as a format count.

**What it adds to the lane.** `SquashFS (v4-BE)` is a separate section on the producer's matrix.
That is the producer-side counterpart of the lane's measured BE v4 run
(`corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`). The handler source shows
that the section is served by the external `sasquatch-v4be` (S112). The vendor-mangled variants
(Broadcom, DD-WRT, non-standard) are named on the same page and are still unmeasured lane Frontier.

**Caveats.** A support matrix claims coverage, never an outcome: "Fully supported" says nothing
about whether a given image extracts. The staged entry inferred that the site is stale from its
copyright footer ("2021 - 2025 ONEKEY GmbH"). The footer is present, but it is not used here as
evidence of staleness; the count conflict above stands on its own quotes.
