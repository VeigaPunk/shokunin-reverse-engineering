# Round 64 declaration — freeze pending

Base: c7fe6898e9a8b3ff04486b4a1d672e9db37610c9.
One proposed claim, R64-C1, depth capability acquisition. Coverage, depth
and calibration are tied at 10 in the base Owned axes table, so depth is a
lowest non-retired axis. Saturated finite proxies do not imply mastery.

## Proposed task and falsification

A package archive may contain multiple central-directory entries with the
same filename. A filename-keyed inventory can discard an earlier payload.
Add an occurrence-preserving static ZIP reader plus a source-backed craft
table and checklist. Preserve ordinal, decoded filename, local-header
offset, declared size/CRC and actual per-occurrence SHA256. Duplicate groups
name all ordinals, including equal-payload occurrences; never silently
collapse them. Read each ZipInfo, not a name lookup. No extraction, package
installation, native loading or member execution.

Bounded profile: regular non-symlink archive <=8 MiB; <=128 members;
ZIP_STORED/ZIP_DEFLATED only; <=1 MiB/member and <=4 MiB total uncompressed;
no encryption; ASCII names only, with NUL-truncated names refused as
unsupported_name (exit 2). Valid profile returns 0 and the complete occurrence array;
malformed/truncated/CRC or header-name mismatch returns 1 without a complete
inventory; unsupported/budget/nonregular input returns 2 (unevaluable).
Names are metadata, never output paths. Static inventory does not prove
which duplicate an application selects, signature authenticity, safety or
runtime behavior. No universal ZIP validity assertion beyond parser/profile.

Before: targeted base grep across SKILL.md, PROVINCE.md, corpus/README.md
and corpus/knowledge for ZipInfo/infolist/duplicate ZIP variants returned
zero lines. This is a scoped token-search observation, not lane-wide novelty. Independent
review identified related existing knowledge at
corpus/knowledge/2026-10-13-r3-apk-inventory.md:34-48: APK central-directory
occurrences, deduplicated nodes and per-occurrence hash verification were
already known. New claim is strictly the current-cloud-host standalone
duplicate-name test, explicit local-header offsets, ordered digest records
and a bounded refusal recipe, not the first occurrence-inventory concept.
The proposed reader and specific craft table do not exist at the base.
After target: an independently authored fixture set and expected ordered
records is checked by an independently authored comparator with outer CLI
positive/negative controls; reader demonstrates changed-payload duplicates,
reverse order, same-payload duplicates, unique/empty and malformed/refused
inputs. All named cases must match exit and semantic payload. A missing
receipt or no-op reader cannot pass. Exact counts and pins will be frozen
only after development tests and independent input design are settled.

The sole claim is sourced to official Python zipfile docs (opened in this
round), to be registered as S264. Each quoted passage is <=25 words total
per source and structurally located. Installed Python version/source hash
must be measured separately; online documentation is not runtime evidence.

## Preparation and authority

Parent appoints independent fixture author and reviewer. Author-side tests
are never outside admission. Before execution, review scripts and retain
explicit permitted argv, versions, hashes, stdout/stderr/exit, UTC and root.
Trusted stdlib tooling only; temporary fixtures under own explicit round
scratch; process timeout and memory caps. No OS sandbox or no-execution
inode enforcement is claimed: carrier non-execution is instructed.

Literal inherited scratch restriction: NEVER run du/find over /fast/scratch
through bash builtins; use /usr/bin/du or /usr/bin/find only. No scratch
inventory is needed here. Never read credentials/client configs or install
engines. No fleet writes and no round65 authority.

Instrument + red fixtures + before receipts must be committed before the
claims container/data; first claims.json commit freezes the contract and
pins instruments. Pre-freeze dry runs are development/re-observation, not
held-out results. Fresh scored fixtures follow the freeze. Frozen-path drift,
source census, registry and no-harm checks remain admission duties, not new
claims. Report is staged outside the fleet until parent authorizes delivery.

## Declared predicate and frozen target

All frozen case names match fresh post-freeze ZIP occurrence records and refusal classes, with committed provenance and a source-linked craft rule.

Nineteen cases, every one required: archive_budget, central_reordered,
count_boundary, count_budget, crc_invalid, deflated, different_duplicates,
empty, encrypted, header_name_mismatch, member_boundary, member_budget,
metadata_names, nul_name, reverse_payloads, same_payload, total_budget,
truncated, unsupported_method. Scored fixtures are generated with a new
reviewer-selected salt only after the first freeze; development fixtures
use dev64 and are explicitly not the scored population. The static recipe
and invariants are known, so fresh vocabulary is not a claim of statistical
independence or unbiased generalization. The unchanged malformed/budget
classes are re-observations, not held-out content.

Semantic comparator: tools/round-64/compare.py, independently authored.
It compares exact case output, integer types, duplicate-key-free JSON and
pins each fixture; private controls test no-op/all-false/junk/wrong digest,
partial-error, boolean schema, duplicate JSON and a positive. Independent
shortcut controls include collapsing same-name entries, sorting by local
header offset, reading by filename, no-op, all-false and development-table
replay; full target must reject every shortcut (target is all nineteen).
Fresh vocabulary changes payloads, names, sizes and digests together.
No numeric score increase is asserted; repertoire/craft depth is the move.

Admission: tools/round-64/admit.py reads only committed Git objects. It
binds the first claims commit, frozen instrument bytes and no-touch
history, committed fixture hashes, exact receipt case set, strict semantic
payloads and first-commit/run chronology. Run time is the recorded UTC,
not authenticated execution; independent replay is essential. It checks a
single craft marker and a S264-linked knowledge entry/source registry
binding; these are structural checks, and the reviewer separately judges
technical correctness and no-harm. Its eleven outer CLI controls include
old run, old data, edited instrument, alternate freeze and edited claim.
No lexical check is presented as semantic comprehension.

## Frozen paths

- plans/round-64-claims.md
- .ufo/waves/round-64/claims.json
- tools/round-64/zip-occurrences.py
- tools/round-64/compare.py
- tools/round-64/admit.py
- tools/round-64/fixtures.py
- tools/round-64/controls.py
- .ufo/waves/round-64/prep/dev-expected.json

The first claims container also pins the relied-upon older freeze gate,
preflight and registry census. Current-host resource controls bound only
trusted Python tooling. They are not an OS sandbox. No carrier extraction
or execution occurs. Explicit parent approval covers one inert8MiB+1
negative fixture; the reader refuses it before parsing, no cap increase.
The source, absence/search, prior closure and draft mistakes are retained
under prep. Their dates are past observations, not future milestones.
