# Round 48 registry audit — ExecRegistryAudit

Scope: independently checked every path in the frozen `tools/round-48/census2.json` (`dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`) against the existing marker-bound instrument-registry rows in `SKILL.md` (lines 1705–1750). The registry currently has **no** `tools/round-48/` row. The census contains 45 paths; this report concerns whether each row's claimed self-test command exists/is runnable and whether claimed test counts can be produced. No selftests were run (heavy selftests explicitly excluded).

## Finding: census instruments with an explicit selftest command but no argparse `--selftest`

Static source inspection found four census entries whose registry rows state a selftest command, but source does not declare `--selftest` as an argparse option:

| tool | Registry claim | Source finding |
|---|---|---|
| `tools/round-43/c2-score-r43.py` | Registry says no selftest flag; only help/bad-argument probe. | **No mismatch**; no selftest advertised. |
| `tools/round-43/verify-copies-r43.py` | Registry says no `--selftest`; probe only. | **No mismatch**; no selftest advertised. |
| `tools/round-46/census.py` | Registry says none. | **No mismatch**; no selftest advertised. |
| `tools/round-46/gate.py` | Registry explicitly says no selftest of its own; calls out `registry.py` as shared-core test. | **No mismatch**; no selftest advertised. |

Among explicit selftest commands in the registry, the relevant source check found `--selftest` option declarations for `tools/round-41/c1-counter.py`, `c1-extra.py`, `c2-counter.py`, `fetch-vendor.py`, `gen-squashfs.py`, `heldout-gen-v3.py`, `indep-eval-v3.py`, `local-source-gate.py`, `sqfs-list.py`, `sqfs-triage-v3.py`; round-42 `c1-counter.py`, `c2-counter.py`, `fetch-carrier.py`, `heldout-gen-v4.py`, `indep-eval-v4.py`, `prefile-gate.py`, `sqfs-triage-v4.py`, `sqfs3-oracle.py`; round-43 `c1-counter.py`, `heldout-gen-v4r43.py`; round-44 `c1-counter.py`, `c2-counter.py`; round-45 `c1-counter.py`, `c2-counter.py`, `frozen-path-preflight.py`; round-46 `attest.py`, `registry.py`; round-47 `exact.py`, `record.py`. Registry claims of their selftest commands were consistent with presence of argparse option declarations on source inspection. `tools/round-48/meanings.py` and `record2.py` also declare their own options, but no row yet exists.

## Findings: claims of case counts not supported by the named tool's selftest

No claimed case count was conclusively found impossible from source inspection. Counts are descriptive receipts/expected output, not necessarily literals in the tool (many are computed by a case list); absence of a literal count is not evidence it cannot produce it. I did find concrete row descriptions that need careful classification, not to be misrepresented as runnable selftests:

- `tools/round-41/mk-l-carriers.py`: says **none**, explicitly no selftest; its `--builds 2` deterministic rebuild is not an argparse selftest. No unsupported count claim.
- `tools/round-41/c1-run.sh`, `tools/round-42/c1-run.sh`, `tools/round-42/unblob-logtee.sh`, `tools/round-44/c1-run.sh`: say **none**, no selftest mode.
- `tools/round-41/c2-controls.py`, `tools/round-42/c2-controls.py`: say **none**; their in-script control scoring is not a `--selftest` interface.
- `tools/round-41/c1-extra.py` selftest requires `--tools` and `--work`; the row supplies both. Source supports 17 cases (the selftest list is explicit).
- `tools/round-42/prefile-gate.py` selftest requires `--work`; row supplies it, and its source has a 12-case fixture set.
- `tools/round-46/attest.py` selftest requires `--root/--freeze/--rev`; row supplies them; source supports the described changing case total. `gate.py` is appropriately described as library-only and its shared test belongs to `registry.py`.

The strongest actionable gap relative to the assigned question is not a bad selftest command/count in the existing census rows: it is the absence of rows for all round-48 census paths in the marker-bound registry, which is a frozen acceptance requirement for C1. Existing rows cover paths only through round 47.

## Evidence / method

- Read the entire frozen claims file first; its clause 8 specifies exact equality to the 45-path `census2.json` set.
- Read census paths and source files without modifying lane data. Static scan reported explicit `--selftest` string plus argparse option declaration per path; inspect included each census path. No selftests, builds, lint, or tests were run.
- Disk guard status before analysis: exit 0, `/tmp` 19%, `/var/tmp` 38%, `/fast/scratch/hyaku` 32%.
- No tools installed.

## Limitations

Static source presence is not proof a selftest completes or emits a particular count. Counts are not claimed as freshly verified here; heavy selftests were not run by assignment. Exact source inspection establishes no explicit `--selftest` option for entries explicitly documented as having none; no claimed count was shown impossible. No lane files were changed.