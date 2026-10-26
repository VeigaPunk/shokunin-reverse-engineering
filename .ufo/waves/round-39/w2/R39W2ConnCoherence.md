# R39W2ConnCoherence — cross-claim coherence: C1 symlink rule × C2 triage table × frontier statements

Verdict: **CONFIRMED** — the C1 symlink rule, the C2 triage table's symlink rows, the C2 triage
entry's Symlinks paragraph, the round-38 BE entry and the round-36 LE entry/table all state the
same rule; the frontier statements agree across PROVINCE.md, corpus/README.md `## Frontier`, both
round-39 entries and the SCORECARD planned row. No live contradiction found. Three low-severity
stale-history wrinkles (W1–W3) and one proposed round-40 move (the strongest frontier claim a
do-nothing control cannot reach) are listed below.

Scope: coherence only. I did not re-run the C1/C2 counters (other seats own that), did not touch
frozen bytes, and wrote only this report plus `artifacts/R39W2ConnCoherence/evidence.txt`.
Measured revision for landed surfaces: `6fdaf4f1`; freeze `8fcda41c`; HEAD `e40a25df`.
No tools installed or upgraded (read-only git + grep only; nothing needed).

## Commands (all read-only; cwd = lane root)

- `git show 8fcda41c:plans/round-39-claims.md` — frozen claims (C1/C2 predicates, symlink rule S118/S119).
- `git show 6fdaf4f1:corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md` — C1 entry.
- `git show 6fdaf4f1:corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md` — C2 entry.
- `git show 6fdaf4f1:SKILL.md` — rule block 18 + `<!-- sqfs-triage-table v1 -->` + round-36 LE table/registry.
- `git show 6fdaf4f1:corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`,
  `.../2026-10-26-r36-sasquatch-squashfs-recursion.md` — prior-round entries.
- `git show 6fdaf4f1:PROVINCE.md` (:156-157, :374, :376, :378-384), `6fdaf4f1:corpus/README.md`
  (:89-94, :236-245), `HEAD:SCORECARD.md` (:627 capabilities, :3410 planned row).
- `git show 6fdaf4f1:corpus/SOURCES.md` :128 (S122 row), `6fdaf4f1:tools/round-37/gen-squashfs.py`,
  `6fdaf4f1:tools/round-39/gen-squashfs.py` (avm-mode source lines).
- Table byte-diff: extracted the `sqfs-triage-table v1` block at freeze and at `6fdaf4f1` →
  `TABLE-BYTES-IDENTICAL` (artifact `evidence.txt`).
- Craft-block ordinal: the SquashFS triage block is **#18 of 18** `- **`-blocks between
  `## Queue-drain craft` and the table — matches "rule block 18" in the claims' surface sentence.

## 1. Symlink rule — one rule across six surfaces

The rule (three clauses): (a) escaping link → removed, `MaliciousSymlinkRemoved` report, **no gap**;
(b) in-tree link → kept as metadata, exactly **one `unpublished-entry` gap** per link, nothing
published for it; (c) absolute target → **re-rooted under the extraction root and kept** (not
removed). Plus the mechanism note: containment = target joined to the link's directory inside the
per-chunk extraction root, resolved, must stay under that root (`is_safe_path`, no `..` clamping).

| surface | (a) escaping | (b) in-tree | (c) absolute re-rooted | carrier counts |
|---|---|---|---|---|
| `plans/round-39-claims.md` @ freeze | removed + report + no gap | kept + 1 `unpublished-entry` | re-rooted and kept | K1 1 esc; K2 1 in-tree; K3/K4 none; K5 2+1; K6 1+2 |
| C1 entry `r39-be-squashfs-v4-core.md` @ 6fdaf4f1 | identical, + K1 `../hello.txt` no-clamp example | identical | identical | table rows 0/1, 1/0, 0/0, 0/0, 2/1, 1/2 — same as claims |
| C2 table rows `escaping-symlink-removed` / `in-tree-symlink-metadata` @ freeze | "removed it and reported MaliciousSymlinkRemoved, and REA records no gap for it" | "kept as metadata and recorded as one unpublished-entry gap per link" | (falls under in-tree after re-rooting; table silent, entry states it) | handler `squashfs_v4_*` — both endians, as claims require |
| C2 entry Symlinks paragraph @ 6fdaf4f1 | "removes one that escapes it, reporting `MaliciousSymlinkRemoved` … a removed link leaves no gap" | "records each kept symlink as one `unpublished-entry` gap … `unpublished_entries[].kind` `symlink`" | "absolute targets are re-rooted under the extraction directory and kept, not removed (S118 :73-77)" | both-kinds image → row order escaping first |
| round-38 BE entry | K1 escape → "unblob removes it and logs `MaliciousSymlinkRemoved`, so no gap" | K2 in-tree → "kept as metadata and records one `unpublished-entry` gap" | not stated (its carriers are relative-only) | K1 1 esc, K2 1 in-tree — same carriers as C1 |
| round-36 LE entry + SKILL LE table | not exercised (no escaping links in r36 carriers) | "retained as metadata", one `unpublished-entry` each (K2, K3, K4) | not stated | consistent |

All six surfaces state the same three clauses. The C2 table/entry phrase the test coarser
("resolved outside/inside the extraction root") without the join-detail or no-clamping note — same
rule, coarser wording, no contradiction. The claims' per-carrier counts (K1 1 escaping; K2 1
in-tree; K5 2 in-tree + 1 escaping; K6 1 in-tree + 2 escaping) match the C1 entry's table and the
PROVINCE round-39 row ("K5 … 2 in-tree + 1 escaping link"). The round-36 surfaces predate the BE
work and claim only the in-tree half — exactly what their carriers exercise.

Binding spot-checks that coherence relies on: triage-table bytes identical freeze → measured;
craft block is #18; C1 entry cites S122 (`is_safe_path`, opened 2026-10-26T17:09:05Z) and S122's
used-by column lists `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md` — the C1 predicate's
PROVINCE→entry→SOURCES chain closes. Table line citations into the C2 entry (`:11-28`, `:29-40`,
`:50-54`, `:11-19`) land on the right paragraphs (off-by-one onto a blank line at `:19`; trivial).

## 2. Frontier statements — one frontier across all surfaces

Live frontier after round 39, per every surface: **AVM-BE bodies and vendor-mangled images remain;
standard BE v4 and LE v4 are Core.**

| surface | statement |
|---|---|
| PROVINCE.md:384 (round-39 frontier note; HEAD adds the R36-CL2 LE-entry name) | big-endian part of the Round-4 bullet + round-38 note "superseded for standard big-endian SquashFS v4"; "AVM-BE bodies and vendor-mangled images stay Frontier" |
| PROVINCE.md:378-382 (`## Round-39 additions to Core`) | row names `squashfs_v4_be`, cites the C1 entry |
| corpus/README.md:245 | "standard big-endian v4 is **Core** … superseding the round-38 line above for standard BE. Still frontier: AVM-BE bodies, vendor-mangled images." |
| corpus/README.md:93 (coverage-map row) | "**Core** … AVM-BE and vendor-mangled stay Frontier" |
| C1 entry Limits (:44) | "Not held: AVM-BE bodies, vendor-mangled SquashFS, …" |
| C2 entry Status (:58) | "Not covered: AVM-BE bodies (LE block lengths, XZ), vendor-mangled images, …" |
| SCORECARD.md:3410 (round-38 planned row, the only round-39 planned row) | "coverage — standard BE v4 promotion. The predicate states the symlink behaviour before data …" — exactly what round 39 landed |

All agree. SCORECARD has no round-39 closure section and no planned-(round-40) row at HEAD
(expected — L1 writes the closure after wave 2), so the only SCORECARD planned row to check is the
round-38 one, and it matches the landing.

## 3. Wrinkles (stale history inside dated-note chains; no live contradiction)

- **W1 — README `## Frontier` :243 tail.** The round-36 dated note on the `sasquatch` bullet ends
  "Still frontier: big-endian/AVM (`sasquatch-v4be`) and vendor-mangled images." The round-39 line
  (:245) supersedes only "the round-38 line above" (:244) for standard BE; it never explicitly
  retires :243's "big-endian/AVM" clause. A reader of :243 alone is told big-endian is still
  frontier. Reconcilable by reading the chain (:245's "Still frontier: AVM-BE bodies,
  vendor-mangled" covers the surviving half). Severity: low.
- **W2 — PROVINCE Round-4 bullet :157.** The bullet's inline bracket history stops at round 38
  ("… not promoted"); the round-39 supersession lives only in the separate note at :384. Matches
  the lane's note-per-round convention (and the claims required exactly "a round-39 frontier
  note"), but the live bullet's latest inline word is stale. Severity: low.
- **W3 — SCORECARD capabilities table (HEAD :627).** The round-36 row still says "Big-endian/AVM
  not demonstrated"; no BE capability row exists yet. Closure-time work, not a rule contradiction;
  flagged so the round-39 closure section doesn't forget it. Severity: informational.

## 4. The strongest round-40 frontier claim a do-nothing control cannot reach

**Claim candidate (coverage): REA `extract-firmware` publishes the members of a true AVM-BE body.**
Why this and not the alternatives:

- It is the only frontier item named first on **every** round-39 surface (§2 table).
- Its mechanism is half-open and half-measured. The marker branch (`mkfs_time == bytes_used`)
  is already a scored C2 held-out class (`avm-marker-be-dropped`, 20/20 at 6fdaf4f1) — but only on
  a **standard-BE body** carrying the marker, where sasquatch-v4be without `-be` fails with
  "different endianess". What no surface has measured is the **true AVM-BE layout** (big-endian
  metadata, **little-endian block lengths**, XZ — S114; C2 entry "Not covered: AVM-BE bodies (LE
  block lengths, XZ)"), which is the layout real AVM images use and the reason the format exists.
  Whether REA/unblob extracts that body cleanly — and with what handler, argv, gaps and symlink
  behaviour — is unknown, stated nowhere, and exactly the shape of claim this lane freezes well.
- **A do-nothing control cannot reach it.** Verified from source: the lane's writer
  (`tools/round-37/gen-squashfs.py`, and the round-39 copy) builds its `avm` mode as a standard BE
  body with `sqsh` magic and `mkfs = bytes_used` — the only `avm` deltas are `MAGIC` (:7/:20) and
  `mkfs` (:173/:185); block-length/inode layout is unchanged BE. So no existing tool mints a true
  AVM-BE carrier, no oracle, counter or frozen predicate exists, and re-scoring round-39 bytes
  yields nothing. Vendor-mangled (`qshs`/Broadcom) is further out (no pinned format source — only
  the S116-class coverage statement — and no writer route at all); the C2 not-covered envelope
  classes (`unknown-chunk-handler`, `encrypted-chunk`, `depth-limited`, LE body damage) are table
  rows, not coverage frontier. AVM-BE is the strongest reachable-but-unreached claim.
- Synthesis across landed surfaces: it is the round-38 SCORECARD planned row's named second choice
  ("the AVM-BE branch (`bytes_used == mkfs_time`, S112/S114) on a lane-built carrier"), it
  consumes the C2 table's `avm-marker-be-dropped` row as its mechanism grounding, and it walks the
  frontier every round-39 surface names. Round 39's claims said "Not claimed: AVM-BE bodies" —
  claiming it in round 40 is the direct frontier walk, improving coverage without touching depth's
  axis state.

**Proposed move (one, bounded):** R40-C1 freezes, before data: a predicate over N≥2 true-AVM-BE
carriers (xz; frozen oracle regular files via the lane reader + a sasquatch-v4be run; frozen
symlink table — none) stating the expected envelope shape up front (handler `squashfs_v4_be`,
`-be` dropped per the marker, extractor exit 0, every oracle file published, gap set exactly the
frozen symlink table's in-tree links) — plus the honest-stop branches (if the body fails without
`-be`, the claim records the failure verbatim and stays Frontier; if a new envelope shape appears,
the C2 table gains a ninth label instead of stretching row 5). Do-nothing and
fabricated-receipt controls scored pre-freeze per the round-39 kill-rule pattern; provenance by
independent wave-2 re-runs, per the disclosed receipt-only limit.

**Risks.** (1) The lane must extend `gen-squashfs.py` to write LE block lengths under the AVM
marker — writer work the round must budget; if that proves wrong, the fallback carrier is a
published AVM image (the round-38 planned row's alternative; note the round-38 lesson refused an
AVM-image assimilation once, D5, on provenance grounds — acquisition needs a fresh source mining).
(2) If the predicate's expected shape is wrong (e.g. unblob routes AVM-BE elsewhere), the claim is
an honest stop — acceptable, it sharpens the frontier note either way. (3) C2 separability: the
new carrier classes must not disturb the frozen C2 held-out set (separate evidence tree).

**Verification.** Build carrier(s) with the extended writer; run `extract-firmware` (rea-agents
6.5.0 pin, `REA_UNBLOB_COMMAND=~/.local/bin/unblob`) into fresh outdirs under `/kaidoku-r40/`;
oracle via `tools/round-39/sqfs-list.py` + direct `sasquatch-v4be`; freeze carriers/oracles/
symlink tables + predicate; pre-freeze controls; score with a round-40 counter at a named
revision; freeze-drift gate over the round-40 frozen paths.

## 5. Limits of this seat

Coherence of stated rules only: I compared the rule texts and binding chains, not the receipt
semantics (other seats re-run counters and replay fixtures). Statements about unblob/REA internals
are quoted from the cited entries and SOURCES rows, not re-derived from source. The W1–W3 wrinkles
are cosmetic-stale-history findings; none falsifies a landed claim or its counter verdicts.

Artifact: `.ufo/waves/round-39/w2/artifacts/R39W2ConnCoherence/evidence.txt` (table byte-diff,
block-ordinal check, S122 used-by tail, generator avm-mode lines).
