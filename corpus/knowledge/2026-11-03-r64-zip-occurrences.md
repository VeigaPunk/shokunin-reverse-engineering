source: S264 — Python zipfile documentation; exact reader and independent raw ZIP recipe in tools/round-64/
verified-at: 2026-11-03
recheck: on Python/parser change or wider ZIP profile

# ZIP member identity is an occurrence, not a pathname

## Scope and prior knowledge

[OBSERVATION] The older APK entry already documents central-directory
occurrences distinct from content nodes and ordinal-bearing edges:
`corpus/knowledge/2026-10-13-r3-apk-inventory.md:34-48`. This is not the
first discovery of occurrence inventories. Round64 supplies a standalone
cloud-host reader for duplicate-name payloads, explicit local-header offsets,
and a bounded static refusal recipe. It makes no new REA capability claim.

[OBSERVATION] Python here is 3.12.14; the installed zipfile module hash and
path are in `.ufo/waves/round-64/prep/host-tools.txt`. Official S264 docs
were served as 3.12.16, not the installed patch version. The docs support
API design; actual run receipts establish this installed implementation.
No client configuration, Ghidra, or REA provider was queried.

## Ordered identity and byte evidence

[OBSERVATION] The reader calls `infolist()` then `open(info)`, retaining
central-directory ordinal, decoded filename, local-header offset, payload
size/CRC and SHA256 for every member. It never uses `read(filename)` or a
filename-keyed dictionary as the occurrence collection. Duplicate groups
retain all ordinals even when the member payload hashes are identical.

[INFERENCE] A defensible citation identity is archive SHA256 plus central
ordinal and local-header offset, with payload SHA256. Filename alone is
ambiguous. Equal payload hashes do not erase distinct occurrences. Sorting
by header offset changes central-directory order when the directory is
permuted; offset and ordinal are different evidence fields.

[OBSERVATION] Independent fixtures are written with raw struct records,
not the reader's zipfile writer. The central-reordered case leaves physical
local-header order intact while permuting directory entries. The complete
scored record is `.ufo/waves/round-64/data/comparison.json`; its per-case
stdout contains ordered semantic fields and its oracle pins every archive
at `.ufo/waves/round-64/data/fixtures/expected.json`. Rechecking command:
`python3 -I -B tools/round-64/admit.py --root ABSOLUTE_LANE --rev DATA_REV --freeze 300e87a713b3f6f91aed80a29e08ca91228f7f76`.
The final measured DATA_REV is recorded in the round lesson/report, not
inferred from a moving worktree.

## Static triage table

| Situation | Action and conclusion |
|---|---|
| Same decoded name, different payload digest | Preserve both occurrences. Infer name ambiguity, not which one an installer selects. |
| Same name and same digest | Preserve multiplicity and ordinals. Equal bytes are not one archive occurrence. |
| Central-directory order differs from header offsets | Keep directory ordinal and explicit offset; never silently sort by offset. |
| Absolute, dot-dot or backslash name | Treat as metadata only. This reader writes no member paths and does not extract. |
| Truncation, CRC error or local/header-name mismatch | Exit1 malformed; no complete inventory emitted. Do not label missing output as parsed-empty. |
| Unsupported compression, encryption, non-ASCII/NUL-truncated name | Exit2 unevaluable profile refusal, not universal format corruption. |
| Over resource profile | Exit2 before payload read where declared metadata suffices; oversized archive refused before parser. |
| Empty supported archive | Exit0 with explicit empty arrays. Distinguish parsed-empty from refused. |

The local profile is regular non-symlink input <=8MiB, <=128 records,
STORE/DEFLATE, ASCII names without NUL truncation, <=1MiB/member and <=4MiB
uncompressed total, no encrypted members. Equality is permitted. The test
fixture at8MiB+1 is an expressly approved inert negative, not a cap increase.
Reader output is JSON on stdout only; errors omit occurrence arrays.

## Limits and checklist

[UNKNOWN] This evidence does not establish application/installer duplicate
selection, runtime behavior, signature authenticity, licensing, maliciousness,
APK signing-block handling, universal ZIP validity, or Unicode-name support.
Only the supported profile and declared cases are tested. There is no archive
extraction, native loading, or carrier execution. Non-execution is instructed,
not an enforced inode guard or a sandbox proof. Resource caps bound trusted
Python processes, not arbitrary attacker code.

Checklist: (1) bind archive path/hash and reader/source version; (2) retain
complete per-occurrence arrays, not just duplicate counts; (3) distinguish
central ordinal from physical offset; (4) preserve refusals with exit/finding;
(5) separate observation/inference/unknown; (6) re-run the frozen comparator
on the pinned fixtures and compare all fields, then obtain non-author review.
Fresh postfreeze salt changes names/payloads/sizes/digests for positive cases;
fixed malformed and budget cases are repeated boundary observations, not
nineteen previously unseen artifact classes.
