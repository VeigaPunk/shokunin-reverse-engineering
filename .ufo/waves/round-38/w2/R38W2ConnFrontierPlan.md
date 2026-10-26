# R38W2ConnFrontierPlan — coherence of the frontier after round 38; strongest round-39 claim shape

Seat: connector (godspeed), advisory. No lane mutation, no VCS write, no REA/extractor run, no
tool installs, no subagents. All reads at HEAD `e265533e` (round-38 attempt-2 wave-2 spec/dispatch) or
at the first freeze `e059ca9391642d5b71b6662cabcbdce0d9308719` for the frozen predicate.

**Verdict: CONFIRMED** — the four named surfaces agree on what stays frontier (standard BE v4
promotion, AVM-BE, vendor-mangled) and on the symlink constraint; the AVM marker statements match
S112/S114 exactly. One low-severity staleness defect is reported outside the four compared surfaces
(PROVINCE.md:372 “unmeasured” aside), plus a framing nit: PROVINCE.md:157 and the historical README
bullet lump “big-endian/AVM” where the round-39 planned field and the current README bullet separate
standard-BE promotion from AVM-BE — substance identical, vocabulary not.

## 1. What was compared (exact reads)

| # | Surface | Location | Source of read |
|---|---|---|---|
| 1 | SCORECARD `planned (round 39)` | `SCORECARD.md:3410` (Round 38 section tail) | `read` :3399-3416 |
| 2 | corpus `## Frontier`, sasquatch-v4be bullet | `corpus/README.md:239` (plus historical :238) | `grep` + `read` |
| 3 | PROVINCE frontier note | `PROVINCE.md:156-157` (bullet sasquatch, round-38 bracket) and `PROVINCE.md:374` (round-36 frontier note) | `grep` + `read` |
| 4 | Entry Status paragraph | `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` (Status, last ¶) | `read` full file |

Also read: `plans/round-38-claims.md` at `e059ca93` (frozen P38-C1/P38-C2), `SCORECARD.md:3399-3416`
(round-38 section), `corpus/README.md:91` (coverage-map round-38 row), `corpus/README.md:199`
(knowledge-index row), `corpus/SOURCES.md:118-123` (S112-S116 rows), `corpus/lessons/round-38.md`
(Mistakes M38-1..4, Gate), `.ufo/waves/round-38/w1/R38CriticClaimsC1.md` (§3, lines 72-128),
`R38ConnSeparability.md` / `R38ConnSiblingOverlap.md` (w1 connector siblings — no overlap with this
comparison), `.ufo/waves/round-38/w2/R38W2ConnLaneHistory.md` / `R38W2ConnSiblingGates.md` (w2
connector siblings — no overlap).

## 2. Do the four surfaces agree on what stays frontier?

Yes. All four name the same three frontier items and the same promotion barrier.

| Surface | Standard BE v4 | AVM-BE | Vendor-mangled | Symlink constraint |
|---|---|---|---|---|
| SCORECARD.md:3410 (planned r39) | promotion is the primary claim; “states the symlink behaviour before data” | second choice: “AVM-BE branch (`bytes_used == mkfs_time`, S112/S114) on a lane-built carrier” | not mentioned in planned field; implicit (no claim) | “in-tree symlinks are `unpublished-entry`, escaping symlinks are removed” |
| corpus/README.md:239 (Frontier) | “standard big-endian v4 measured … **not promoted**”; “Still frontier: standard BE v4 promotion” | “Still frontier: AVM-BE” | “Still frontier: … vendor-mangled images” | “R38-C1 stopped on K2's in-tree symlink gap under its first-freeze counter” |
| PROVINCE.md:157 (frontier note) | “standard BE v4 measured through `sasquatch-v4be` … not promoted — R38-C1 honest stop” | “big-endian/AVM stays here” (lumped) | via :374: “Big-endian/AVM and vendor-mangled images stay Frontier” | “K2's in-tree symlink leaves an `unpublished-entry` gap” |
| Entry Status | “This is not a Core promotion … Standard BE v4 stays on the PROVINCE Frontier until a claim that states the symlink behaviour up front verifies” | “AVM-BE and vendor-mangled images were not measured” | same | full split: K1 escape → removed (`MaliciousSymlinkRemoved`), K2 in-tree → `unpublished-entry` |

Agreement is exact on substance: (a) standard BE v4 was measured but not promoted, so it stays
frontier; (b) AVM-BE was not measured and stays frontier; (c) vendor-mangled images were not measured
and stay frontier; (d) the symlink dichotomy (in-tree → `unpublished-entry`; escaping → removed) is
the barrier the promotion claim must state prospectively.

**Framing nit (not a contradiction):** `PROVINCE.md:157` and the historical README bullet
(`corpus/README.md:238`, kept as history) write “big-endian/AVM stays here”; the current README bullet
(:239) and the SCORECARD planned field (:3410) separate “standard BE v4 promotion” from “AVM-BE”.
Since standard BE v4 ⊂ big-endian, both readings are true; but a round-39 predicate that quotes the
frontier bullet verbatim should use the separated vocabulary to stay machine-checkable against the
planned field.

**Staleness defect (outside the four compared surfaces):** `PROVINCE.md:372` — the round-36 Core
table row's aside still says “`sasquatch-v4be` is its big-endian sibling, unmeasured”. Round 38
measured it: the after-arm ran the `squashfs_v4_be` handler with 4.5.1 reachable (K1 5/5, K2 3/3,
K3 4/4, K4 4/4) and the independent cross-tool check ran `sasquatch-v4be -be` directly, reproducing
16/16 oracle regular files (entry “What was measured”; README coverage-map row :91). The row is a
historical round-36 table and the frontier note at :374 supersedes it, so this is low-severity; but a
reader landing on :372 alone reads “unmeasured”, which now disagrees with current state. The C2
counter is lexical (pointer resolution + counts) and cannot catch this semantic staleness.

## 3. AVM marker statements vs S112/S114 — verified, consistent

Statement under attack: “It drops `-be` when `header.bytes_used == header.mkfs_time`, which is the
AVM-BE marker (S114)” (entry `:27`; SCORECARD.md:3410 states the same condition `bytes_used ==
mkfs_time`).

Checked against the installed unblob 26.6.4 `SquashFSExtractor`
(`~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py`,
lines 1-90; this is the S112 artifact — same tag 26.6.4, same URL as SOURCES row S112/S108):

- line 29 `V4BE_EXECUTABLE = "sasquatch-v4be"` — matches S112 row (“case Endian.BIG, 4: executable =
  self.V4BE_EXECUTABLE”).
- `match endian, self.version: case Endian.BIG, 4:` → parses header with `StructParser(SquashFSv4LEHandler.C_DEFINITIONS)` at `Endian.BIG`; then `is_avm = header.bytes_used == header.mkfs_time; if not is_avm: commands_args.append("-be")` — exactly the entry's “drops `-be` when bytes_used == mkfs_time”.
- The code comment above `is_avm` cites the Freetz URL `https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/AVM-BE-format.txt` — the S114 artifact; SOURCES row S114: “`mkfs_time` field holds the same value as `bytes_used`”.
- `get_dependencies()` returns `[self.EXECUTABLE, self.V4BE_EXECUTABLE]` = `sasquatch` + `sasquatch-v4be` — matches the entry's structural-dependency paragraph and S112 row.

Conclusion: the AVM marker claims in the round-39 planned field and the entry are byte-exact against
S112 (installed 26.6.4 code) and S114 (Freetz note). One nuance for the round-39 claim: the header is
parsed big-endian with the LE handler's field definitions, so `bytes_used`/`mkfs_time` are both read
big-endian; no surface disputes this, and it does not change the marker condition.

## 4. Strongest round-39 claim shape a do-nothing control cannot reach

A do-nothing control (run the frozen counter at the base; no claim data, no receipts) cannot produce:

1. **The fabricated-receipt control scored red at the freeze** — the planned field's first item.
   Its precedent is `.ufo/waves/round-38/w1/R38CriticClaimsC1.md` §3 (“The loud kill (v1)”), which
   shows a receipt minted from public base data (oracle.tsv rows + carriers.json pins, evidence id
   minted by the 6.5.0 XPIN rule) reaching `met_target true`/exit 0 on the frozen v1 counter. A
   round-39 counter that can kill that control must bind real extraction facts — e.g. cross-check
   `raw_result` against `normalized_result` (the §3 fabrication keeps the round-36 `raw_result` path),
   bind the extractor identity/version, require the receipt to postdate the freeze, and tie the
   subject digest to the freeze-pinned carriers rather than claimant-authored data. A do-nothing run
   cannot mint the fabricated pair, so it cannot demonstrate — and a counter that only reads envelope
   fields cannot produce — the red kill that makes the promotion meaningful.
2. **The symlink-stating predicate verified at the measured revision** — requires real after-receipts
   on four carriers exhibiting both symlink outcomes plus the freeze-stage control; do-nothing has no
   measured revision.
3. **`freeze-drift.py` clean (exit 0) from freeze to measured revision** — a do-nothing control
   never establishes a measured revision that is a descendant of the freeze with zero amendments to
   the kill-rule set. This is the gate that would have caught M38-1/M38-2 before they happened.
4. **The AVM-BE branch (second choice)** — a lane-built carrier with `bytes_used == mkfs_time` pinned
   cannot exist at the base; the `is_avm` branch has never been exercised (entry: “AVM-BE … not
   measured”). The claim would freeze the carrier's header fields, assert from S112 that `-be` is
   dropped iff `is_avm`, and measure both arms (AVM vs non-AVM twin) with argv captured.

The single strongest shape is (1): the frozen successor counter turns the §3 fabrication from green to
red while scoring the real receipts to target — because the v1 counter demonstrably could not, and a
do-nothing control cannot even construct the test.

## 5. Risks

- The round-39 planned field must name the counter bindings beyond envelope fields; a fabricated
  control rebuilt to the v1 shape (oracle list + handler string + minted id) would otherwise score
  green again and kill the wrong claim (repeat of the §3 outcome).
- The fabricated control must be scored at the freeze commit, and `freeze-drift.py` run over the same
  kill-rule set; a control added after data or after counter edits repeats M38-1/M38-2.
- The planned field's language “symlink behaviour before data” needs the exact dichotomy wording
  (in-tree → `unpublished-entry`; escaping → removed) in the frozen predicate, not just in this card,
  so the counter can bind it.

## 6. Verification / evidence commands

- `git rev-parse HEAD` → `e265533ea3a7cd4d9a75a24ef737c2ff0e98e95f`; `git log --oneline -8` (round-38
  attempt-2 chain visible: `0fc61133`, `3b960fe5`, `077e212b`, `f1010f67`, `79f69347`).
- `git show e059ca9391642d5b71b6662cabcbdce0d9308719:plans/round-38-claims.md` → frozen predicate
  P38-C1 (incl. “carries no extraction gap” and “no external extractor dependency”, both superseded by
  the honest stop), P38-C2, kill rules.
- Reads: `SCORECARD.md:3399-3416`, `corpus/README.md:91,:199,:231-244`, `PROVINCE.md:144-173,:366-376`,
  `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` (full), `corpus/SOURCES.md:118-123`,
  `corpus/lessons/round-38.md` (full), `R38CriticClaimsC1.md:1-8,72-128`.
- Code proof: `sed -n '1,90p' ~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py` (lines 28-52: `V4BE_EXECUTABLE`, `is_avm` branch, `get_dependencies`).
- grep sweep: `bytes_used|mkfs_time|is_avm` across `corpus/`, `PROVINCE.md`, `SCORECARD.md` — no
  surface contradicts the `bytes_used == mkfs_time` marker.
