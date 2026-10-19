#!/usr/bin/env python3
"""PL-3 arc3-pointer extension builder + scratch validation.

Builds the arc3-era entry fragment (68 proposed entries + 9 exempt rows),
splices it into a SCRATCH copy of the real pointer table, re-pins the scratch
expected.json, and runs the probe at HEAD. The real artifacts under
.ufo/gates/citation-drift/ are opened READ-ONLY; nothing is written there.
Writes only under /var/tmp/pl3.
"""
import hashlib
import json
import subprocess
import pathlib
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
OUT = pathlib.Path("/var/tmp/pl3")
TABLE = pathlib.Path(REPO) / ".ufo/gates/citation-drift/pointer-table.json"
EXPECTED = pathlib.Path(REPO) / ".ufo/gates/citation-drift/expected.json"
PROBE = pathlib.Path(REPO) / ".ufo/gates/citation-drift/citation-drift-probe.py"

W1 = ".ufo/waves/arc3-loop1-round1"
W2 = ".ufo/waves/arc3-loop1-round2"
R1E = "corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md"
R3E = "corpus/knowledge/2026-10-13-r3-evm-interface.md"

A = lambda i, f, m, note: {"id": i, "kind": "anchor", "file": f, "must_match": m, "note": note}
X = lambda i, f, ln, p, t, g1, g2, m, note: {
    "id": i, "kind": "extracted", "file": f, "line": ln, "pattern": p, "target": t,
    "target_group": g1, **({"target_group_end": g2} if g2 else {}), "must_match": m, "note": note}
E = lambda i, f, ln, m, note: {"id": i, "kind": "exact", "file": f, "line": ln, "must_match": m, "note": note}

NEW = []

# ---- F1a: line-number citations from the r1 EVM entry (6 extracted) ----
NEW += [
    X("a3r1-r1e-cites-r3-errata", R1E, 17, r"2026-10-13-r3-evm-interface\.md:(\d+)-(\d+)", R3E, 1, 2,
      r"JUMPDEST dispatch-target position",
      "the r1 entry's offset-semantics pointer (r3-07 round-4 erratum) must land on the erratum paragraph that states the JUMPDEST semantics."),
    X("a3r1-r1e-cites-r3-stubmut", R1E, 18, r"2026-10-13-r3-evm-interface\.md:(\d+)-(\d+)", R3E, 1, 2,
      r'inferred_state_mutability: "pure"',
      "the delta-vs-r3-07 claim cites the stub legs' pure-mutability observation; the cited range must still hold it."),
    X("a3r1-r1e-cites-quality15", R1E, 21, r"QUALITY\.md:(\d+)-(\d+)", "corpus/QUALITY.md", 1, 2,
      r"content\+params-keyed",
      "the no-content-addressed-identity-claim line cites QUALITY #15's per-verb-family domain wording."),
    X("a3r1-r1e-cites-quality11", R1E, 24, r"QUALITY\.md:(\d+)", "corpus/QUALITY.md", 1, None,
      r"parsed-and-empty or excluded-from-inventory",
      "the creation-legs observation cites QUALITY #11 (parsed-and-empty vs exclusion) — the cited line must carry that criterion."),
    X("a3r1-r1e-cites-r3-kindhyp", R1E, 25, r"2026-10-13-r3-evm-interface\.md:(\d+)-(\d+)", R3E, 1, 2,
      r"appears to need richer bytecode",
      "the refuted-hypothesis bullet cites r3-07 candidate-2's classification note; the cited range must hold the refuted text."),
    X("a3r1-r1e-cites-r3-positional", R1E, 26, r"2026-10-13-r3-evm-interface\.md:(\d+)-(\d+)", R3E, 1, 2,
      r"encoding is a POSITIONAL arg",
      "the input-shape-traps bullet cites the r3 positional-encoding quirk; the cited range must hold it."),
]

# ---- F1b: anchors on the r1 entry's cited evidence artifacts (27) ----
def ev(rid, rel, needle, note):
    return A(rid, f"{W1}/claims/c1/{rel}", needle, note)

NEW += [
    ev("a3r1-rv2-probe-hex64", "RV-2/probe-runtime-hex-6.4.0.json", r'"normalized_result"',
       "primary Rv2Token hex probe envelope (r1 entry source list + the K=5 observation)."),
    ev("a3r1-rv2-probe-raw64", "RV-2/probe-runtime-raw-6.4.0.json", r'"normalized_result"',
       "raw-encoding twin envelope (raw equiv hex observation)."),
    ev("a3r1-rv2-probe-hex67", "RV-2/probe-runtime-hex-6.7.0.json", r'"normalized_result"',
       "6.7.0 re-derivation envelope (CBOR-metadata observation)."),
    ev("a3r1-rv2-rerun-a", "RV-2/probe-rerun-a.json", r'"normalized_result"',
       "same-request rerun a (id re-derivation observation)."),
    ev("a3r1-rv2-rerun-b", "RV-2/probe-rerun-b.json", r'"normalized_result"',
       "same-request rerun b (id re-derivation observation)."),
    ev("a3r1-rv2-cwdroot", "RV-2/probe-cwd-root-6.4.0.json", r'"normalized_result"',
       "repo-root-CWD rerun envelope (path-invariance observation)."),
    ev("a3r1-rv2-creation", "RV-2/probe-creation-hex-6.4.0.json", r"ev_c80379e1",
       "creation-code parsed-and-empty envelope named by the entry."),
    ev("a3r1-rv2-smoke", "RV-2/probe-EX02-smoke-bin-6.4.0.json", r"ev_f875e21e",
       "Smoke carrier creation-bytes envelope named by the entry."),
    ev("a3r1-rv2-many", "RV-2/attack/probe-many.json", r"ev_d0d0b054",
       "11-selector attack envelope (zero-false-positives observation)."),
    ev("a3r1-rv2-manysel", "RV-2/attack/expected-many.txt", r"K=11",
       "planted set K=11 recorded pre-probe (attack carrier)."),
    ev("a3r1-rv2-sel5", "RV-2/expected-selectors.txt", r"K=5",
       "planted set K=5 recorded pre-probe (Rv2Token)."),
    ev("a3r1-rv2-abi", "RV-2/Rv2Token.abi.json", r'"type": "function"',
       "compiled ABI the mutability/argument consistency check is made against."),
    ev("a3r1-rv2-creationhex", "RV-2/Rv2Token.creation.hex", r"^60806040",
       "creation blob carrier cited by the creation-legs observation (hex text shape)."),
    ev("a3r1-rv2-solcinput", "RV-2/solc-input.json", r'"language": "Solidity"',
       "solc standard-JSON input named by the carrier paragraph."),
    ev("a3r1-ex06-runhex", "EX-06/evidence/run-hex-6.7.0.json", r"ev_56d89cb4",
       "KdxToken hex 6.7.0 envelope (6/6 observation)."),
    ev("a3r1-ex06-runraw", "EX-06/evidence/run-raw-6.7.0.json", r'"normalized_result"',
       "KdxToken raw 6.7.0 envelope (hex-shape-variants observation)."),
    ev("a3r1-ex06-plantedk", "EX-06/evidence/planted-K.json", r'"K": 6',
       "KdxToken planted set recorded pre-probe (keccak-anchored)."),
    ev("a3r1-ex06-transcript", "EX-06/evidence/transcript.txt", r"rea 6.7.0: 6.7.0",
       "compile/probe transcript named by the entry's source list."),
    ev("a3r1-ex06-compilejs", "EX-06/evidence/compile.js", r"deployedBytecode",
       "KdxToken compile recipe (deployedBytecode object) named by the carrier paragraph."),
    ev("a3r1-ex07-recon", "EX-07/reconciliation-run.txt", r"VERDICT: ALL SOURCES AGREE",
       "independent recon verdict the entry quotes."),
    ev("a3r1-ex07-m1rv2", "EX-07/m1-rv2token-runtime.json", r'"code_sha256": "c1081a56',
       "recon leg for Rv2Token runtime (decode-equality observation)."),
    ev("a3r1-ex07-m1kdx", "EX-07/m1-kdxtoken-runtime.json", r'"code_len": 1789',
       "recon leg for KdxToken runtime (offset-semantics re-confirmation)."),
    ev("a3r1-ex07-m2keccak", "EX-07/m2-kdxtoken-keccak.json", r'"found": true',
       "pure-Python keccak recon leg for KdxToken."),
    ev("a3r1-rv1-sha3", "RV-1/validation-sha3-and-vectors.txt", r"two independent SHA3-256 oracles",
       "keccak reference validation against two independent oracles."),
    ev("a3r1-ex02-receipt", "EX-02/install-receipt.txt", r"INSTALL RECEIPT",
       "solc install receipt pinning the compiler provenance."),
    ev("a3r1-ex02-smokebin", "EX-02/smoke/out/Smoke_sol_Smoke.bin", r"^60806040",
       "install smoke carrier (685 B hex text) named by the creation-legs observation."),
    A("a3r1-solcprefix-pkg", f"{W1}/tools/solc-prefix/package.json", r"0\.8\.37",
      "the cited wave-isolated solc prefix's manifest (dir citation covered by its package.json; install receipt carries the provenance)."),
]

# ---- F2: SCORECARD arc3-section needles (4) ----
NEW += [
    E("a3r1-sc-section-head", "SCORECARD.md", 1338, r"^## arc3-loop1-round1",
      "the section key rule #14's citation anchors by (SKILL.md:253 names the arc3-loop1-round1 section, never a bare range)."),
    E("a3r1-sc-fresh-identity", "SCORECARD.md", 1366, r"fresh identity recorded \(10,225 B, sha256",
      "the 'fresh identity recorded' line rule #14's citation names (SKILL.md:253)."),
    X("a3r2-sc-shonen-refresh", "SCORECARD.md", 1435, r"SHONEN\.md:(\d+)", "SHONEN.md", 1, None,
      r"14/14",
      "the r2 section's same-commit coupling: SHONEN.md:6 must carry the 14/14 count the record states. If a later round refreshes SHONEN:6, this entry must be re-aimed in the same commit."),
    A("a3r1-sc-dirty-path", ".ufo/waves/arc2-loop1-round10/C3.md", r"round-10 rerun-leg containment watch plan",
      "the r1 section names this pre-existing dirty path; the file must keep existing (it is tracked at HEAD — the 'dirty' wording is the r1 record)."),
]

# ---- F3: registry rows + rule #14 citations (7) ----
NEW += [
    A("a3r2-custody-tool", ".ufo/gates/custody-pair/custody-pair.py", r"CUSTODY_PATHS",
      "the r2 registry row + SCORECARD dir citation: the committed instrument must exist and keep its path-registry constant."),
    A("a3r2-custody-readme", ".ufo/gates/custody-pair/README.md", r"^# custody-pair",
      "the r2 registry row + SCORECARD dir citation: the tool's README must keep existing."),
    A("a3r2-skill-custodyrow", "SKILL.md", r"custody-pair \| tool / kaidoku",
      "the r2-added registry row itself; its LINE is deliberately unpinned (the lane appends rows to the table — same reason as the sibling row entry)."),
    A("a3r1-skill-cdrow-guard", "SKILL.md", r"pointer_table_tampered",
      "the r1-updated citation-drift registry row's declared guard finding id (row LINE unpinned; the table grows)."),
    A("a3r1-cd-probe", ".ufo/gates/citation-drift/citation-drift-probe.py", r"pointer_table_tampered",
      "the registry row's instrument citation: the script must exist and keep the frozen-run finding class."),
    A("a3r1-cd-table", ".ufo/gates/citation-drift/pointer-table.json", r'"entries"',
      "the registry row cites the table itself; the table must exist and keep its entries array (its bytes change this round — this needle is revision-agnostic by design)."),
    A("a3r1-cd-expected", ".ufo/gates/citation-drift/expected.json", r'"pointer_table"',
      "the registry row cites the expected-values file; it must keep the frozen-run digest pin."),
]

# ---- F3b: rule #14's line-number citations (4 extracted) ----
NEW += [
    X("a3r2-skill-rule14-cr2", "SKILL.md", 246, r"arc3-loop1-round1/seats/CR-2\.md:(\d+)-(\d+)",
      f"{W1}/seats/CR-2.md", 1, 2, r"8,316 B / `f95c5a05",
      "rule #14's stale-identity instance: the cited seat-report range must still hold the 8,316 B / f95c5a05 triple."),
    X("a3r2-skill-rule14-verdict", "SKILL.md", 248, r"arc3-loop1-round1/claims/c1/verdict\.md:(\d+)-(\d+)",
      f"{W1}/claims/c1/verdict.md", 1, 2, r"D9 — the entry patch was revised mid-wave",
      "rule #14's second instance: the cited verdict range must hold the D9 debt block."),
    X("a3r2-skill-rule14-entry7", "SKILL.md", 252, r"2026-10-19-arc3-r1-evm-real-solc\.md:(\d+)", R1E, 1, None,
      r"TMPDIR=/var/tmp/cr2-recheck",
      "rule #14 cites the landed entry's line 7 as the recheck record; the cited line must still be the disk-backed-TMPDIR recheck line."),
    X("a3r2-skill-rule14-log", "SKILL.md", 254, r"LOG\.md:(\d+)-(\d+)", "LOG.md", 1, 2, r"dd986f56",
      "rule #14 cites the LOG entry recording the landing identity; LOG is append-only, so the cited range must keep the record verbatim."),
]

# ---- F4: custody receipt conventions: v1 shape examples + EX-31 evidence (12) ----
NEW += [
    A("a3r1-receipt-stanza-v1", f"{W1}/claims/cross/receipts/config-pre-pair.txt", r"^PATH: ",
      "custody README's stanza-v1 example (path-prefixed stanza shape)."),
    A("a3r1-receipt-sums-v1", f"{W1}/claims/c3/EX-26/custody-sha256.txt", r"^[0-9a-f]{64}  /home/vgpnk/\.config/devin",
      "custody README's sums-v1 example (sha256sum shape)."),
    A("a3r1-receipt-pipe-v1", f"{W1}/claims/cross/receipts/config-pre-pair-metadata.txt", r"^/home/vgpnk/\.config/devin/mcp_config\.json \| [0-9]+ \|",
      "custody README's pipe-v1 example (pipe-separated metadata shape)."),
    A("a3r2-ex31-pre", f"{W2}/claims/c3/EX-31/capture-pre.txt", r"^# receipt-version: 2",
      "the r2 round-evidence pre-pair receipt the README names."),
    A("a3r2-ex31-post", f"{W2}/claims/c3/EX-31/capture-post.txt", r"^# receipt-version: 2",
      "the r2 round-evidence post-pair receipt the README names."),
    A("a3r2-ex31-pre-side", f"{W2}/claims/c3/EX-31/capture-pre.txt.sha256", r"^[0-9a-f]{64}",
      "the pre receipt's self-identity sidecar the README's '+ sidecars' names."),
    A("a3r2-ex31-post-side", f"{W2}/claims/c3/EX-31/capture-post.txt.sha256", r"^[0-9a-f]{64}",
      "the post receipt's self-identity sidecar."),
    A("a3r2-ex31-verify-pair", f"{W2}/claims/c3/EX-31/verify-pre-vs-post.out", r"CUSTODY_PAIR_VERIFY: MATCH paths=5/5",
      "the matching verify run the README names (MATCH 5/5 exit 0)."),
    A("a3r2-ex31-attacks-sh", f"{W2}/claims/c3/EX-31/attacks.sh", r"^#!",
      "the six-attack harness script the README names."),
    A("a3r2-ex31-attacks-out", f"{W2}/claims/c3/EX-31/attacks.out", r"same-content rewrite IN PLACE",
      "the harness transcript the README names (in-place rewrite class present)."),
    A("a3r2-ex31-selftest", f"{W2}/claims/c3/EX-31/selftest.out", r"CUSTODY_PAIR_SELFTEST: CLEAN cases=15 passed=15",
      "the selftest transcript the README names (15/15 at the r2 revision)."),
    A("a3r2-ex31-labeldefect", f"{W2}/claims/c3/EX-31/label-defect-regression.out", r"v2 bare MTIME_UTC",
      "the v1-compat run the README names (the v1 label defect reproduced-as-declared)."),
]

# ---- F4b: the five operator paths' in-repo content anchors (5) ----
for rid, needle, nm in (
    ("a3r2-cp-path-devin", r"~/\.config/devin/mcp_config\.json", "devin MCP config"),
    ("a3r2-cp-path-omp", r"~/\.omp/agent/mcp\.json", "omp MCP config"),
    ("a3r2-cp-path-kimi", r"~/\.kimi-code/config\.toml", "Kimi client config"),
    ("a3r2-cp-path-bashrc", r"~/\.bashrc", "bashrc"),
    ("a3r2-cp-path-profile", r"~/\.profile", "profile"),
):
    NEW.append(A(rid, ".ufo/gates/custody-pair/custody-pair.py", needle,
                 f"operator-mutable path {nm} as the custody README names it: pinned only in its in-repo content-anchor form (the instrument's CUSTODY_PATHS list), never as a live file or line (rule #11)."))

# ---- F5: map-row + SHONEN r2 refresh (3) ----
NEW += [
    A("a3r1-maprow-r1entry", R1E, r"on real solc bytecode",
      "the r1 map row (corpus/README.md:38) names the new EVM knowledge entry; its file must keep existing with its subject line."),
    A("a3r1-maprow-r3entry", R3E, r"^# 07 — EVM interface inspection \(round 3\)",
      "the same map row names the r3-07 antecedent entry."),
    X("a3r2-shonen-rule14-inrange", "SHONEN.md", 6, r"SKILL\.md:(\d+)-(\d+)", "SKILL.md", 1, 2,
      r"An artifact that records its own byte-identity",
      "the r2 refresh moved the count to 14/14; the asserted craft range must still contain the newest rule (#14) — the r10 shonen-skill-range form extended to the r2 round."),
]

# ---- exempt (9 adjudicated NO-ENTRY rows) ----
EXEMPT = [
    {"token": "bare operator paths `~/.config/devin/mcp_config.json` … `~/.profile` (custody-pair/README.md:7-11, custody-pair.py:112-116)",
     "cause": "rule #11 by construction: operator-mutable files admit no line pin and no content pin from in-repo. Adjudicated NO-ENTRY; the pinnable proxy is the instrument's CUSTODY_PATHS content anchors (a3r2-cp-path-*)."},
    {"token": "`../waves/arc3-loop1-round2/claims/c3/EX-31/` (custody-pair/README.md:129)",
     "cause": "non-conforming relative form: resolves to .ufo/gates/waves/ (absent at HEAD, measured) and `git show HEAD:../waves/...` is refused (exit 128, measured). Adjudicated NO-ENTRY as written; the evidence files are covered by the a3r2-ex31-* anchors at their repo-relative paths; README path-form fix carried as patch text."},
    {"token": "receipt examples `arc3-loop1-round1/claims/…` (custody-pair/README.md:103-105)",
     "cause": "path shorthand relative to the implied `.ufo/waves/` base; resolves uniquely by suffix to the three repo-relative receipts the a3r1-receipt-* anchors cover. Adjudicated NO-ENTRY as a form; README prefix fix carried as patch text."},
    {"token": "digest / identity tokens in the arc3 sections (`0e1a1ab6…`, `dd986f56…`, `c134afcb…`, `d0772ce8…`, `112d01dc…`, `fa484d57…`)",
     "cause": "identity claims, not path citations: the discipline is rule #14 re-derivation (the r2 section's `c134afcb…` legitimately stales when a later round revises SKILL.md). Pinning a truncated digest would manufacture findings on legitimate revisions."},
    {"token": "commit short-hashes (`28aa7a9`, `679af5d…`, `e845c2b5…`)",
     "cause": "revision references, resolvable via `git rev-parse`; the probe's target model is rev:path file citations only."},
    {"token": "selector / prologue byte constants (`5f3560e01c`, `60003560e01c`, `095ea7b3` …)",
     "cause": "data values in the cited artifacts, not citations to repo objects."},
    {"token": "scratch-policy paths (`/tmp`, `/dev/shm`, `/var/tmp`, `$CUSTODY_PAIR_SCRATCH`)",
     "cause": "host scratch policy stated by the README/registry row, not in-repo objects (the `/tmp` EDQUOT fact is a host property)."},
    {"token": "version pins (`rea-agents@6.4.0`, `rea-agents@6.7.0`, `evmole@0.9.3`, `solc 0.8.37+commit.f401782d`)",
     "cause": "the census's PIN locus class (c1-census-v10.py:239-240), graded by that instrument, not by this probe; the probe grades citations to repo files."},
    {"token": "shorthand sibling filenames inside the r1 entry's `source:`/`Sources:` lists (e.g. `probe-rerun-a.json`)",
     "cause": "directory-continuation shorthand: S1's 20 distinct shorthand tokens resolve by suffix (34 occurrences); the single context-resolved case is `solc-input.json` → `RV-2/solc-input.json` (the carrier paragraph names Rv2Token) — measured in the census. Every resolvent carries its own full-path anchor in this fragment."},
    {"token": "dotted field-path tokens (`normalized_result.functions`, `bytecode.sha256 c1081a56…`, `bytecode.kind`, `subject.digest.sha256`, `evm.deployedBytecode.object`)",
     "cause": "field-access paths inside the cited evidence, not repo objects: the envelope anchors cover the files; the field names are the observation's own vocabulary."},
    {"token": "directory citations: `.ufo/waves/arc3-loop1-round1/claims/c1/{RV-2,EX-06,EX-07,RV-1,EX-02}` (r1 entry line 1) and `.ufo/waves/arc3-loop1-round1/tools/solc-prefix/` (line 11, trailing slash)",
     "cause": "directory citations name no file the probe can grade; each named directory's load-bearing members carry their own anchors in this fragment (all five staging dirs resolve; the solc prefix is covered by its package.json anchor)."},
]

DOC_ADD = (" Extended arc3-loop1-round3 with the arc3-era citations: the r1 EVM entry's line-number "
           "citations and evidence anchors, the arc3 SCORECARD section needles (section-key form; no bare "
           "range into the growing section), the r2 registry rows + rule-#14 citations, and the custody "
           "receipt conventions (v1 shape examples, EX-31 evidence, CUSTODY_PATHS content anchors).")


def clean(d):
    return {k: v for k, v in d.items() if v is not None}


def main():
    DROP = {  # functional duplicates of the EX-41 landed cut (arc3-loop1-round3, 13:12Z)
        "a3r1-r1e-cites-r3-errata", "a3r1-r1e-cites-r3-stubmut", "a3r1-r1e-cites-quality15",
        "a3r1-r1e-cites-quality11", "a3r1-r1e-cites-r3-kindhyp", "a3r1-r1e-cites-r3-positional",
        "a3r1-sc-section-head", "a3r2-custody-readme",
        "a3r2-skill-custodyrow", "a3r1-skill-cdrow-guard",
        "a3r2-skill-rule14-cr2", "a3r2-skill-rule14-verdict",
        "a3r2-skill-rule14-entry7", "a3r2-skill-rule14-log",
        "a3r1-receipt-stanza-v1", "a3r1-receipt-sums-v1", "a3r1-receipt-pipe-v1",
    }
    global NEW
    NEW = [e for e in NEW if e["id"] not in DROP]
    table_bytes = TABLE.read_bytes()
    expected_bytes = EXPECTED.read_bytes()
    real_table_sha = hashlib.sha256(table_bytes).hexdigest()
    real_expected_sha = hashlib.sha256(expected_bytes).hexdigest()
    print(f"BASE table sha256={real_table_sha}")
    print(f"BASE expected sha256={real_expected_sha}")
    table = json.loads(table_bytes)
    expected = json.loads(expected_bytes)
    print(f"BASE entries={len(table['entries'])} quoted={len(table['quoted'])} exempt={len(table['exempt'])}")
    assert table["entries"][0]["id"] == "sc59-stanza-key-anchor"

    ids = [e["id"] for e in table["entries"]] + [e["id"] for e in table["quoted"]]
    new_ids = [e["id"] for e in NEW]
    assert len(set(new_ids)) == len(new_ids), "duplicate ids in fragment"
    assert not (set(new_ids) & set(ids)), "fragment id collides with existing"

    scratch = {
        "_doc": table["_doc"] + DOC_ADD,
        "entries": table["entries"] + [clean(e) for e in NEW],
        "quoted": table["quoted"],
        "exempt": table["exempt"] + EXEMPT,
    }
    frag = {"entries": [clean(e) for e in NEW], "exempt": EXEMPT, "_doc_addendum": DOC_ADD}
    (OUT / "entries-arc3.json").write_text(json.dumps(frag, indent=2) + "\n")
    tbytes = (json.dumps(scratch, indent=2) + "\n").encode()
    (OUT / "pointer-table-arc3.json").write_bytes(tbytes)
    new_sha = hashlib.sha256(tbytes).hexdigest()
    scratch_expected = dict(expected)
    scratch_expected["pointer_table"] = dict(expected["pointer_table"])
    scratch_expected["pointer_table"]["sha256"] = new_sha
    scratch_expected["pointer_table"]["note"] = (
        expected["pointer_table"]["note"].replace(
            "frozen-run guard (R6 debt, arc3-loop1-round1)",
            "frozen-run guard (R6 debt, arc3-loop1-round1; re-pinned arc3-loop1-round3 for the arc3-era extension)"))
    (OUT / "expected-arc3.json").write_text(json.dumps(scratch_expected, indent=2) + "\n")
    print(f"NEW entries={len(NEW)} new_exempt={len(EXEMPT)} new_table_sha256={new_sha} N={len(scratch['entries'])}")

    def run(*args):
        p = subprocess.run([sys.executable, str(PROBE), *args], capture_output=True, text=True, cwd=REPO)
        return p.returncode, (p.stdout + p.stderr).strip()

    print("\n--- probe: scratch table + scratch expected (default mode) ---")
    rc, out = run("--root", ".", "--rev", "HEAD", "--table", str(OUT / "pointer-table-arc3.json"),
                  "--expected", str(OUT / "expected-arc3.json"))
    print(out)
    print(f"rc={rc}")
    print("\n--- probe: scratch table + scratch expected (--strict) ---")
    rc2, out2 = run("--root", ".", "--rev", "HEAD", "--table", str(OUT / "pointer-table-arc3.json"),
                    "--expected", str(OUT / "expected-arc3.json"), "--strict")
    print(out2)
    print(f"rc={rc2}")
    print("\n--- F3 coupling demo: scratch table + REAL expected (stale pin) ---")
    rc3, out3 = run("--root", ".", "--rev", "HEAD", "--table", str(OUT / "pointer-table-arc3.json"),
                    "--expected", str(EXPECTED))
    print(out3)
    print(f"rc={rc3}")
    print("\n--- selftest with scratch expected ---")
    rc4, out4 = run("--selftest", "--expected", str(OUT / "expected-arc3.json"))
    print(out4.splitlines()[-1] if out4 else "")
    print(f"rc={rc4}")
    print("\n--- real artifacts unchanged check ---")
    print("table", hashlib.sha256(TABLE.read_bytes()).hexdigest(), "==", real_table_sha)
    print("expected", hashlib.sha256(EXPECTED.read_bytes()).hexdigest(), "==", real_expected_sha)
    (OUT / "validation.out").write_text(json.dumps({
        "base_table_sha": real_table_sha, "base_expected_sha": real_expected_sha,
        "new_table_sha": new_sha, "N": len(scratch["entries"]),
        "new_entries": len(NEW), "new_exempt": len(EXEMPT),
        "probe_default": out, "probe_default_rc": rc,
        "probe_strict": out2, "probe_strict_rc": rc2,
        "stale_pin_demo": out3, "stale_pin_demo_rc": rc3,
        "selftest_tail": out4.splitlines()[-1] if out4 else "", "selftest_rc": rc4,
    }, indent=1) + "\n")


if __name__ == "__main__":
    main()