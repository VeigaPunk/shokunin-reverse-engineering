# ScribeCapabilityRow — receipts (offline; no REA run by this seat)

All values below were measured by this seat on 2026-10-29 (UTC) against lane tip
`addbfb4df0d33fedff51d46f2a983a5bd8ea0c10` and against scratch clones of that tip. No REA invocation was
made. Exact commands are quoted in the report's findings table and in `../scorecard.md`.

| file | sha256 | what it is |
|---|---|---|
| `triage-v4-126-envelopes.json` | `1a02cbfbd1e2dcdf387311ac64f731808a36ca0494b3f0fa250ef78b4a864611` | frozen v4 interpreter over the 126 committed round-42 recon envelopes, exit 0 — 19 no-reader `_ddefault` rows label `clean`/`none` at handler level |
| `triage-v4-table-only.txt` | `65abca784fbaafc0318df5d05eee97036081f8a1a6aff96d38b5c2cbc76c510f` | `sqfs-triage-v4.py --skill SKILL.md --table-only`, exit 0 — 15 rules, marker line 526 |
| `cmdA-at-f890bbe.json` | `7ee3abeb4c045ca0394be2b987d61d02fc56517e59d03b670e29c90761b736e0` | command A (the SCORECARD recipe) at the attempt-2 base `f890bbea` — `mapped 139`, `missing []`, `dangling []`, `rule_blocks 25`, `citation_resolved_rules 25` |
| `c1-control-c0-counter.json` | `1615b563eb1f3db50f74dde6b0a01194641ccf5ad5d3c2b46ac967c6033f8469` | the lane's own CTL-C1-0 attempt-2 control receipt, copied from `.ufo/waves/round-50/controls-attempt2/c0/` — exit 1, `carriers_matched 0`, `met_target false` |
| `c2-at-HEAD.json` | `6b2275bcebe292393e16651998e764c13656db9746a20245b47005926145ffab` | `c2-record.py` at the tip — `mismatches 0`, `atoms_total 11`, exit 0 |
| `c2-row.json` | `f462f5dd6fe2b34828e416a60d2a0eeeab3f32e8555bb68e589a767f7ab647c5` | `c2-record.py` with the entry + README coverage-map row + the proposed 140/140 coverage head → `mismatches 0`, exit 0, B1 `ok: true` |
| `c2-comb.json` | `18a3ef26c5af878d1959370279f0cc0ad052eae6742621e625c5f38e3362bf2b` | `c2-record.py` with **both** head edits (coverage 140/140 + depth 26/26) → `mismatches 0`, exit 0 |
| `c2-final.json` | `200c21eb3cc34f9e3f026780e6f553110f84a2cdbe56ca42b65e265859baa983` | `c2-record.py` re-run at the real C3 landing `addbfb4d` with both head edits → `mismatches 0`, `atoms_total 11`, exit 0 |
| `c2-bad3.json` | `5315a76af8150c194bf86107c0864df368586e3827a6b26b421259e54ab67dd5` | `c2-record.py` with the heading `## Record corrections — round 50, attempt 2` → **`mismatches 5`, exit 1** (B3, B4, B5, B10, B11 red: "2 `## Record corrections — round 50` sections, want 1") |
| `c2-safe2.json` | `54cce6f3549b6d28eb9114434ecfadcdd2bbf1ae6307d65531c3813cfbe9d152` | `c2-record.py` with the heading `## Record corrections — round-50 attempt 2` → `mismatches 0`, exit 0 |

`c2-bad3.json` and `c2-safe2.json` are the two ends of the heading measurement: the same base tree, the same
counter, the same freeze — only the correction-section heading differs.
