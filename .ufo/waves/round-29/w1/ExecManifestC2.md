# R29-C2 fetch manifest audit

## Verdict

**Holds.** At commit `18be864a528873b2b70d8c94e31f880290249e90`, `responses_complete` is **178/178** under the counter’s response-completeness requirements. No exceptions were found.

## Findings

**[Observation]** The target has 178 unique selectors and 178 manifest entries. The database tree has exactly 179 files: one manifest plus the 178 expected selector bodies; no missing or extra files or manifest entries.

**[Observation]** All 178 entries have the exact OpenChain `filter=false` URL for their selector, status `200`, a syntactically valid UTC timestamp later than the counter commit, and a lowercase SHA-256 matching the saved body. All 178 bodies were committed no earlier than the counter commit, parse as JSON, have `ok: true`, and contain their `0x<selector>` key under `result.function`.

**[Conclusion]** The manifest and body evidence satisfy the requested criteria, so `responses_complete 178/178` holds for this committed snapshot.

**[Limitation]** No live network request was made; status `200` is the value recorded in the committed manifest, not an independently re-fetched response.

## Retained evidence

Producing command (read-only audit of Git objects at the requested commit):

```sh
python3 /fast/scratch/hyaku/kaidoku-r29/seats/w1/c2-manifest-audit/audit_manifest.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 18be864a528873b2b70d8c94e31f880290249e90; rc=$?; printf 'exit_code=%s\n' "$rc"; exit "$rc"
```

Exact output, UTC `2026-10-22T20:22:51Z`, exit code `0`:

```text
revision=18be864a528873b2b70d8c94e31f880290249e90 resolved=18be864a528873b2b70d8c94e31f880290249e90
selectors=178 unique_selectors=178 manifest_entries=178 db_files=179 expected_db_files=179
manifest_sha256=098d02bbef8a5f722b37b8dc021deaa2846646beef0f2b589bb14abe7dad6c02
url_exact=178 status_200=178 utc_valid=178 utc_after_counter_commit=178 sha256_match=178
body_json=178 body_ok_true=178 selector_key=178 body_committed_after_counter=178
responses_complete=178/178
exceptions=none
audit_utc=2026-10-22T20:22:51Z
exit_code=0
```

Scratch audit script: `/fast/scratch/hyaku/kaidoku-r29/seats/w1/c2-manifest-audit/audit_manifest.py` — SHA-256 `4db2cd7bc13934b2a47b958eed6ce494f6b3c565d46dd2836a9eeafaffc688bc`.

Installations: none. Risks/blockers beyond the live-network limitation: none identified.
