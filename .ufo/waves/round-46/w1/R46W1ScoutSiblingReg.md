# R46W1ScoutSiblingReg — sibling registry overlap

Read-only scan. No install. No counter executed. UTC 2026-10-28T16:56:53Z (`date -u`, exit 0; stdout sha256 not retained).

Axes: coverage (which lanes own a registry section), depth (one verbatim foreign row; whether any sibling counter scores forgeries), calibration (7-column kaidoku header vs the PROTOCOL.md field list).

## Verdict

Other lanes already own instrument/gate registries. Several already score forgeries. No sibling SKILL.md owns a freeze-integrity counter; kaidoku does. Kaidoku's 7-column header conflicts with the fleet schema: PROTOCOL.md fixes eight row fields. The field kaidoku dropped is entry command.

## Lanes with a registry section

Scan: `/home/vgpnk/Projects/shokunin/*-shokunin/SKILL.md` (21 lane dirs). Heading pattern `^#{1,4} .*[Rr]egistry`. Kama and tsukuroi lists capped at 20 matches per file; both already have a registry section inside that cap.

- audio-shokunin: no SKILL.md.
- game-dev-2d-shokunin: no SKILL.md.
- game-dev-3d-shokunin: no registry section. SKILL.md:13 uses "registry" only for corpus/SOURCES.md.
- chousa-shokunin: gate table, heading is not "registry". `## Gates` SKILL.md:76; 8-column header :78. Rows :113-115 say `(r46 registration)` inside that table.
- kagi-shokunin: yes. `## Gate registry — round-22 changed contracts` :694.
- kaidoku-shokunin: yes (this lane). `### Round-32 instrument registry` :1377. Current block `### Round-44/45 instrument registry` :1659.
- kake-shokunin: yes. `### Owned freshness gate registry` :208.
- kama-shokunin: yes. `## Local gate/probe registry` :296. `## Round-20 instrument registry` :673. Later instrument-registry headings through at least round 51.
- kasegi-shokunin: yes. `## Gates & probes registry` :977. `## Submitted-state registry` :715 is a do-not-refile set, not this table.
- kengaku-shokunin: yes. `## Gate/probe registry (PROTOCOL §Gate standard)` :560.
- kotoba-shokunin: yes. `## Gate registry` :448.
- kotodama-shokunin: gate table under `## Gates and probes` :619, header :648. `### Registry correction chains` :468 is the source-id registry, not the gate table.
- kumitate-shokunin: yes. `## Gate registry` :587.
- lore-shokunin: yes. `## Gate registry` :48 (definition lists; cites ../PROTOCOL.md:360-406).
- mado-shokunin: yes. `## Gate registry` :684.
- mori-shokunin: yes. `## Round21 retained-loss observation and policy-test registry` :541. Rows at :162 were not under a heading this scan titled.
- revenger-shokunin: yes. `## Gate registry (registry home; PROTOCOL.md §Gate standard)` :281.
- souji-shokunin: yes. `## Gate registry` :189.
- tabi-shokunin: yes. `### Freshness gate registry` :1555. Conformance restatement `## Round 24 — gate registry conformance` :2455.
- tameshi-shokunin: yes. `### Gate/probe registry` :1527.
- tsukuroi-shokunin: yes. `### Gate registry` :1705. Operative form `## Gate and probe registry — roundN superseding current rows`, observed through round 32.

Tools named like counter.py / attest outside kaidoku (not registries by themselves): kama tools/round58-c1-counter.py through round62-c2-counter.py and tools/gate-registry-check.py; souji census/round-29 through round-35 counters and tools/souji-registry-agreement.py; kumitate scripts/receipt-attest.mjs; tameshi tools/registry-check.py; tsukuroi tools/check-registry-coverage.py; mori tools/mori-gate-registry.py; chousa counters under corpus/evidence/roundNN/. audio has corpus/live/r77-boundary/p7p8_bigwav_counter.py and no SKILL.md.

## One verbatim row (another lane)

/home/vgpnk/Projects/shokunin/souji-shokunin/SKILL.md:201 (header :199, eight cells):

| souji-verify | probe | `bash tools/souji-verify.sh <path>...` | 0 clean, SAFE/NOT-SAFE data; 1 failed selftest or could-not-evaluate setup (legacy debt); 2 could-not-evaluate usage | `TMPDIR=/var/tmp bash tools/souji-verify.sh --selftest` | none; no pinned complete id set | read-only targets; isolated selftest under TMPDIR | souji |

That row is the fleet shape: name, kind, entry command, verdict map, self-test, pinned-value path, write scope, owner.

## Discrimination battery — siblings do score forgeries

Not run this seat. Source predicates say yes.

Closest analogue to kaidoku R46 (weaker check accepts, stronger check refuses, genuine accepted): tabi round 33.

- tabi-shokunin/SKILL.md:2774-2780 — gate v1 forgeriesAccepted 8; v2 must refuse all eight and still admit the honest receipt (admitted 16, failing 0).
- Counter tabi-shokunin/.ufo/waves/round-33/counters/c2-bidi-forgery-battery.mjs:4-11 and :25-47. Question: does scripts/check-bidi-runtime.mjs refuse F1-F8 and accept H0-H2. Exit 0 met, 1 not met, 2 could not evaluate. Lines 44-45: H0, H1 and H2 accepted; every F variant not accepted.

Also, not the same "mutate the landed registry section" battery:

- kasegi corpus/instruments/r42-closure.sh:1534-1536 — forgery_verdicts: six structural forgeries, each must be rejected. r35-defect-closure.sh:91, r40-closure.sh:22, r41-closure.sh:37 reject generated forgeries inside --selftest.
- kumitate scripts/inline-dispatch-evidence.mjs:54-55 and :511-512 — cheapest five-row forgery must fail (forged-cheap-transcripts expects exit 1). scripts/report-receipt-diff.mjs:375 scores named forgeries f1-f11. scripts/receipt-attest.mjs:9-10 and :23-24 treats a nonce-colliding non-.txt ledger entry as a forgery that must be caught.
- chousa SKILL.md:118 JUNK_KILLED=3/3; :107 MUTANT_DETECTED=1/1; :113 calls the round-35-41 controls a discriminating control. Control-vs-candidate, not a forged registry section.
- kama SKILL.md:1262 records forged-cell and forged-raw fixtures and the hole: a coordinated forgery of cell, raw body and hash passes.
- mori SKILL.md:263 and :357-359 disclaims a universal-forgery proof.

Kaidoku's own battery is tools/round-46/attest.py and registry.py (plans/round-46-claims.md:73-76 and :138-142: forgeries by mutating the landed bytes; v1 green, v2 red, genuine green). Not executed here.

## Freeze-integrity counter

Owned here, not by a sibling registry.

- kaidoku SKILL.md:1501 registers tools/round-34/freeze-integrity.py ("Schema-validating freeze integrity"). tools/round-45/frozen-path-preflight.py is the row at SKILL.md:1675. Round 46's arm is tools/round-46/attest.py (plans/round-46-claims.md:20 and :80).
- Sibling SKILL.md search for freeze-integrity or frozen_path_changed: no matches.
- The only sibling hit in the tool-path search was prose attributing the tool to this lane: souji-shokunin/census/round-26/waves/w1/ConnSiblings.md:35 ("Kaidoku built … freeze-integrity.py").

## 7-column shape vs PROTOCOL.md — conflict, yes

Fleet schema line, /home/vgpnk/Projects/shokunin/PROTOCOL.md:401-403, under ## Gate standard / Registry (:398):

Row fields: name, `gate|probe`, entry command, verdict map (code to class), self-test command and spelling, pinned-value path, write scope, owner.

Eight fields. Tabi quotes the same list and calls eight columns canonical (tabi-shokunin/SKILL.md:2457-2462).

Kaidoku's frozen claim calls a seven-cell header "the house schema" (plans/round-46-claims.md:131-132):

tool | gate or probe - purpose | verdict map (exit codes) | self-test command | pinned-value path | write scope | owner

The landed round-44/45 header is also seven cells, and column 2 does not match the claim text (kaidoku-shokunin/SKILL.md:1670):

| tool | gate or probe | verdict map (exit codes) | self-test command | pinned-value path | write scope | owner |

That 7-column shape starts at round 36 (SKILL.md:1573). Round 34 still had the eight PROTOCOL fields, including a separate entry command (SKILL.md:1497):

| name | kind | entry command | verdict map | self-test command/spelling | pinned-value path | write scope | owner |

What conflicts: the separate entry-command field is gone, folded into "gate or probe" / "gate or probe - purpose". Spellings also differ (tool vs name, gate or probe vs gate|probe, self-test command vs self-test command and spelling). The claim's phrase "house schema" is not a quote of PROTOCOL.md. Landing the 7-column header can satisfy plans/round-46-claims.md clause 2 and still miss PROTOCOL.md section Gate standard. Not fixed; this seat is read-only.

## Not run

attest.py, registry.py, tabi c2-bidi-forgery-battery.mjs, kasegi r42-closure.sh, kumitate forgery selftests. No git mutation. No scratch tree (nothing to delete).

## Unknowns

- Kama headings after round 51 and tsukuroi headings after round 32 were past the 20-match cap. Both lanes already have a registry section; later titles were not listed.
- "Scores forgeries" is the source predicate, not a live exit code from this seat.
- Mori's gate rows at :162 were not given a heading by the heading search. Whether a heading exists above :162 was not re-read.
