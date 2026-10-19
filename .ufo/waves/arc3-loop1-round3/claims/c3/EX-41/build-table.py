#!/usr/bin/env python3
"""Build the EX-41 candidate pointer table (arc3-era extension) on scratch.

Round-trip check first: json.load + json.dumps(indent=2, ensure_ascii=False)+"\n"
must reproduce the committed bytes exactly, so the landed diff is additive.
Then append the census's conforming entries + the NO-ENTRY adjudication rows.
"""
import hashlib
import json
import sys

REAL = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json"
OUT = "/var/tmp/ex41/pointer-table.ext.json"

orig_bytes = open(REAL, "rb").read()
doc = json.loads(orig_bytes.decode("utf-8"))
roundtrip = (json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
print("roundtrip byte-identical: %s (orig %d bytes, redump %d bytes)"
      % (roundtrip == orig_bytes, len(orig_bytes), len(roundtrip)))
if roundtrip != orig_bytes:
    sys.exit("format convention does not reproduce the committed bytes")

DOC_ADD = (
    " Extended arc3-loop1-round3 (EX-41) with the arc3-era citations introduced"
    " by arc3 rounds 1-2 on the lane's durable surfaces: the r1 EVM entry's own"
    " cited lines, the rule-#14 provenance pins and the round-2 registry rows in"
    " SKILL.md, the r1 README map token, the arc3 SCORECARD section keys and"
    " their SHONEN.md pointer, the census E22 disposition's SCORECARD citations,"
    " and the custody receipt conventions (including the three in-tree v1-shape"
    " example receipts the README names). NO-ENTRY adjudications for the same"
    " census are recorded in `exempt`."
)

NEW_ENTRIES = [
    {
        "id": "arc3r1-entry-r3-offsets",
        "kind": "extracted",
        "file": "corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md",
        "line": 17,
        "pattern": "2026-10-13-r3-evm-interface\\.md:(\\d+)-(\\d+)",
        "target": "corpus/knowledge/2026-10-13-r3-evm-interface.md",
        "target_group": 1,
        "target_group_end": 2,
        "must_match": "JUMPDEST",
        "note": "the r1 entry cites the r3-07 entry's round-4 erratum for the offset semantics it re-confirms on real bytecode. Reddens on: the named lines no longer holding the JUMPDEST dispatch-target correction."
    },
    {
        "id": "arc3r1-entry-r3-stub-mutability",
        "kind": "extracted",
        "file": "corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md",
        "line": 18,
        "pattern": "2026-10-13-r3-evm-interface\\.md:(\\d+)-(\\d+)",
        "target": "corpus/knowledge/2026-10-13-r3-evm-interface.md",
        "target_group": 1,
        "target_group_end": 2,
        "must_match": "inferred_state_mutability: \"pure\"",
        "note": "the delta the r1 entry is built on (synthetic stubs read `pure`; real bytecode does not). Reddens on: the named range losing the stub-mutability observation it contrasts against."
    },
    {
        "id": "arc3r1-entry-quality-ids",
        "kind": "extracted",
        "file": "corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md",
        "line": 21,
        "pattern": "QUALITY\\.md:(\\d+)-(\\d+)",
        "target": "corpus/QUALITY.md",
        "target_group": 1,
        "target_group_end": 2,
        "must_match": "content-addressed",
        "note": "the entry's refusal to claim a content-addressed `ev_` id cites the quality rows that forbid the claim. Reddens on: the criteria rows moving away from the identity-domain wording they cite."
    },
    {
        "id": "arc3r1-entry-quality-11",
        "kind": "extracted",
        "file": "corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md",
        "line": 24,
        "pattern": "QUALITY\\.md:(\\d+)",
        "target": "corpus/QUALITY.md",
        "target_group": 1,
        "must_match": "parsed-and-empty",
        "note": "the creation-code legs are declared parsed-and-empty under criterion 11, not excluded. Reddens on: the named line no longer carrying the parsed-and-empty criterion the entry invokes."
    },
    {
        "id": "arc3r1-entry-r3-hypothesis",
        "kind": "extracted",
        "file": "corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md",
        "line": 25,
        "pattern": "2026-10-13-r3-evm-interface\\.md:(\\d+)-(\\d+)",
        "target": "corpus/knowledge/2026-10-13-r3-evm-interface.md",
        "target_group": 1,
        "target_group_end": 2,
        "must_match": "need richer bytecode",
        "note": "the r3-07 candidate-2 hypothesis the r1 entry measures dead. Reddens on: the named range losing the hypothesis text the refutation quotes."
    },
    {
        "id": "arc3r1-entry-r3-cli-quirk",
        "kind": "extracted",
        "file": "corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md",
        "line": 26,
        "pattern": "2026-10-13-r3-evm-interface\\.md:(\\d+)-(\\d+)",
        "target": "corpus/knowledge/2026-10-13-r3-evm-interface.md",
        "target_group": 1,
        "target_group_end": 2,
        "must_match": "POSITIONAL arg",
        "note": "the positional-encoding quirk the r1 entry re-uses is cited, not restated. Reddens on: the named range no longer documenting the positional form."
    },
    {
        "id": "skill-rule14-entry-recheck",
        "kind": "extracted",
        "file": "SKILL.md",
        "line": 252,
        "pattern": "2026-10-19-arc3-r1-evm-real-solc\\.md:(\\d+)",
        "target": "corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md",
        "target_group": 1,
        "must_match": "TMPDIR=/var/tmp/cr2-recheck",
        "note": "rule #14's worked example names the landed entry's recheck line as the re-established check; the pinned line must still carry the disk-backed-TMPDIR invocation (the host requirement the round-1 critic fixed). Reddens on: the named line ceasing to hold the recheck form rule #14 points at."
    },
    {
        "id": "skill-rule14-cr2-identity",
        "kind": "extracted",
        "file": "SKILL.md",
        "line": 246,
        "pattern": "arc3-loop1-round1/seats/CR-2\\.md:(\\d+)-(\\d+)",
        "target": ".ufo/waves/arc3-loop1-round1/seats/CR-2.md",
        "target_group": 1,
        "target_group_end": 2,
        "must_match": "F2 \\(recommended\\)",
        "note": "rule #14's measured incident: the CR-2 finding that the patch's self-identity was stale. Reddens on: the committed seat report's named range losing the finding the rule cites as its authority."
    },
    {
        "id": "skill-rule14-verdict-identities",
        "kind": "extracted",
        "file": "SKILL.md",
        "line": 248,
        "pattern": "arc3-loop1-round1/claims/c1/verdict\\.md:(\\d+)-(\\d+)",
        "target": ".ufo/waves/arc3-loop1-round1/claims/c1/verdict.md",
        "target_group": 1,
        "target_group_end": 2,
        "must_match": "Three different applied identities",
        "note": "rule #14's second authority: the chain verdict's D9 measuring three applied identities in ~20 minutes. Reddens on: the named range losing the measurement that motivates the rule."
    },
    {
        "id": "skill-rule14-log-fresh-identity",
        "kind": "extracted",
        "file": "SKILL.md",
        "line": 254,
        "pattern": "LOG\\.md:(\\d+)-(\\d+)",
        "target": "LOG.md",
        "target_group": 1,
        "target_group_end": 2,
        "must_match": "dd986f56",
        "note": "rule #14 points at the integrator's fresh-identity record in the round-1 LOG entry; LOG.md is append-only, so the named lines are stable and the landing digest must stay there. Reddens on: the named lines losing the recorded landing identity."
    },
    {
        "id": "readme38-arc3r1-token",
        "kind": "anchor",
        "file": "corpus/README.md",
        "must_match": "2026-10-19-arc3-r1-evm-real-solc",
        "note": "the map row's token for the r1 EVM entry, graded where it is written. The LINE is deliberately not pinned: the coverage map grows by rows and its numbering moves (the r10 `readme175` lesson), so this entry registers the token's survival, not its line -- a row insertion is not drift here."
    },
    {
        "id": "sc-arc3r1-section-key",
        "kind": "exact",
        "file": "SCORECARD.md",
        "line": 1338,
        "must_match": "^## arc3-loop1-round1 — coverage \\+ operability \\+ freshness: three claims admitted, 2026-10-19",
        "note": "the section key SKILL.md rule #14 anchors by (rule #11's conforming form). SCORECARD is append-only, so :1338 is stable; this is the arc3-r1 record's own heading."
    },
    {
        "id": "sc-arc3r2-section-key",
        "kind": "exact",
        "file": "SCORECARD.md",
        "line": 1419,
        "must_match": "^## arc3-loop1-round2 — depth \\+ freshness \\+ operability: three claims admitted, 2026-10-19",
        "note": "the arc3-r2 record's heading, pinned as the section key a reader follows from the round's records. Append-only file, stable line."
    },
    {
        "id": "sc-arc3r2-cites-shonen",
        "kind": "extracted",
        "file": "SCORECARD.md",
        "line": 1435,
        "pattern": "SHONEN\\.md:(\\d+)",
        "target": "SHONEN.md",
        "target_group": 1,
        "must_match": "SKILL\\.md:81-\\d+` \\(craft section",
        "note": "the round-2 record cites the SHONEN promotion assertion it refreshed; the needle pins the FORM (a craft-section range) rather than a count/range value, so the next same-commit refresh does not redden it. Reddens on: the named SHONEN line ceasing to be the promotion assertion naming the craft section."
    },
    {
        "id": "skill-registry-citation-drift-row",
        "kind": "anchor",
        "file": "SKILL.md",
        "must_match": "frozen-run preflight",
        "note": "the citation-drift registry row (arc3 r1/r2 era) must keep stating its preflight semantics. Line deliberately unpinned -- the lane appends to this file and to this table (the rule-#11 reasoning of `skill-registry-row`). Reddens on: the row's semantics phrasing disappearing."
    },
    {
        "id": "skill-registry-custody-pair-row",
        "kind": "anchor",
        "file": "SKILL.md",
        "must_match": "precedence CONTENT-DRIFT > ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH",
        "note": "the round-2 custody-pair registry row's declared worst-finding precedence. Line unpinned for the same reason as its sibling row."
    },
    {
        "id": "custody-readme-v2-fieldset",
        "kind": "anchor",
        "file": ".ufo/gates/custody-pair/README.md",
        "must_match": "MTIME_UTC_RENDER",
        "note": "the receipt-convention surface the round-2 registry row points at: the v2 field set (epoch + explicit UTC/LOCAL renders). Reddens on: the README losing the labeled-render convention that closes the v1 label defect."
    },
    {
        "id": "custody-readme-rewrite-identity",
        "kind": "anchor",
        "file": ".ufo/gates/custody-pair/README.md",
        "must_match": "Rewrite identity is `INODE` \\+ `CTIME`",
        "note": "the same-content-rewrite convention (sha256 equality is not identity). Reddens on: the README losing the rewrite-identity contract the v2 instrument is built on."
    },
    {
        "id": "custody-readme-precedence",
        "kind": "anchor",
        "file": ".ufo/gates/custody-pair/README.md",
        "must_match": "Severity precedence for the verdict of a `verify` run",
        "note": "the declared severity precedence of the verify map. Reddens on: the README losing the precedence statement the registry row's map rests on."
    },
    {
        "id": "custody-readme-scratch-never-tmp",
        "kind": "anchor",
        "file": ".ufo/gates/custody-pair/README.md",
        "must_match": "never `/tmp`",
        "note": "the standing host rule (disk-backed scratch; `/tmp` is quota-exhausted on this host) recorded as a receipt convention. Reddens on: the README losing the never-/tmp rule the round's recipes depend on."
    },
    {
        "id": "custody-readme-v1-stanza-example",
        "kind": "anchor",
        "file": ".ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt",
        "must_match": "custody receipt \\(CU-1\\)",
        "note": "first in-tree v1 shape the README's compatibility table names (`stanza-v1`); graded file-level (no line pin) because it is a frozen wave receipt. Reddens on: the named example receipt absent or rewritten out of its recorded shape."
    },
    {
        "id": "custody-readme-v1-sums-example",
        "kind": "anchor",
        "file": ".ufo/waves/arc3-loop1-round1/claims/c3/EX-26/custody-sha256.txt",
        "must_match": "custody 5-path sha256 capture",
        "note": "the `sums-v1` example the README names; sha256-only shape. Reddens on: the example receipt absent or rewritten away from its sums form."
    },
    {
        "id": "custody-readme-v1-pipe-example",
        "kind": "anchor",
        "file": ".ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair-metadata.txt",
        "must_match": "format: path \\| inode \\| ctime\\(UTC\\)",
        "note": "the `pipe-v1` example the README names; inode/ctime attribution shape. Reddens on: the example receipt absent or rewritten away from its pipe form."
    },
    {
        "id": "census-cites-sc-e22-debt",
        "kind": "extracted",
        "file": ".ufo/gates/c1-census-v10.py",
        "line": 7,
        "pattern": "SCORECARD\\.md:(\\d+)-(\\d+)",
        "target": "SCORECARD.md",
        "target_group": 1,
        "target_group_end": 2,
        "must_match": "scope-table drift",
        "note": "the census instrument's E22 disposition (arc3 r1) cites the carried-debt row it discharges. Reddens on: the named range no longer holding the debt text the disposition names."
    },
    {
        "id": "census-cites-sc-laundering-refusal",
        "kind": "extracted",
        "file": ".ufo/gates/c1-census-v10.py",
        "line": 33,
        "pattern": "SCORECARD\\.md:(\\d+)",
        "target": "SCORECARD.md",
        "target_group": 1,
        "must_match": "laundering path refused",
        "note": "the disposition cites the round-4 record for the laundering path it also refuses. Reddens on: the named line ceasing to carry that record."
    },
    {
        "id": "census-cites-sc-round4-range",
        "kind": "extracted",
        "file": ".ufo/gates/c1-census-v10.py",
        "line": 27,
        "pattern": "SCORECARD\\.md:(\\d+)-(\\d+)",
        "target": "SCORECARD.md",
        "target_group": 1,
        "target_group_end": 2,
        "must_match": "^## arc2-loop1-round4",
        "note": "the disposition's declared scope range must still begin at the round-4 records section (the span is a scope declaration, so the needle grades its start, not a claim inside it). Reddens on: the declared range no longer starting at the round-4 section header."
    },
]

NEW_EXEMPT = [
    {
        "token": "round-report line pins (`arc3-loop1-round1/kaidoku.md` stating `SKILL.md:371`; `corpus/README.md:38`)",
        "cause": "append-only round records: they state where a row sat at that round's revision. Measured at HEAD (arc3 r3): `SKILL.md:371` now holds `## Refuses` (round 2 inserted the rule-#14 block above the registry table, moving the citation-drift row to :389) while `corpus/README.md:38` still holds the EVM map row. The LOG.md-history class (the `SCORECARD.md:291` precedent): a live or stamped entry would report or re-record history, and the round's own claim is findings=0. The records' live surfaces are graded where they are written (the SKILL.md registry rows and the README token above)."
    },
    {
        "token": "wave-internal citations (`.ufo/waves/arc3-loop1-round{1,2}/**` claim artifacts citing one another)",
        "cause": "evidence-internal provenance inside a wave, not the lane citations the probe's contract names (its header). The r10 extension precedent scoped the table to durable surfaces; wave targets are graded where a durable surface cites them (existing `readme22-r8envelope`; this round's `skill-rule14-cr2-identity`, `skill-rule14-verdict-identities`)."
    },
    {
        "token": "the five operator paths as written in `.ufo/gates/custody-pair/README.md`",
        "cause": "operator-mutable files outside the repo, unresolvable as Git objects; rule #11 forbids pinning them at all. The instrument pins the five identities at run time (`CUSTODY_PATHS`, printed by `paths`), and this probe never reads a custody path."
    },
    {
        "token": "current-state count tokens in the arc3 surfaces (`82/82`, `13/13`, `15/15`, `31 entries`, `10.0/10.0`)",
        "cause": "measurement tokens, not pointers: a pin would have to be refreshed by the owning round in its own commit (the r10 CR2 constraint) and buys zero drift detection; the counts are graded by their instruments' re-runs (command A, the two selftests)."
    },
    {
        "token": "`LOG.md` / report prose naming in-repo paths without a stated number (the arc3 entries' evidence rosters)",
        "cause": "no stated number means no drift class for this probe to grade; file existence is graded where a durable surface cites the path with a needle. LOG.md is append-only history by rule (existing `LOG.md:1018` exemption)."
    },
]

t = doc
t["_doc"] = t["_doc"] + DOC_ADD
t["entries"] = t["entries"] + NEW_ENTRIES
t["exempt"] = t["exempt"] + NEW_EXEMPT

out_bytes = (json.dumps(t, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
open(OUT, "wb").write(out_bytes)
print("candidate: %s" % OUT)
print("bytes %d -> %d" % (len(orig_bytes), len(out_bytes)))
print("entries %d -> %d ; quoted %d ; exempt %d -> %d"
      % (len(json.loads(orig_bytes)["entries"]), len(t["entries"]),
         len(t["quoted"]), len(json.loads(orig_bytes)["exempt"]), len(t["exempt"])))
print("candidate sha256: %s" % hashlib.sha256(out_bytes).hexdigest())