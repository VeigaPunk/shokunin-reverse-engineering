# Round 25 C2 security review

Scope: `resolve-selectors.py` fetch, saved C2 responses, and the REA EVM inspection step. Review was read-only; I did not run fetch, REA, or any network request.

## Findings

### Medium — Untrusted pagination URL can make fetch contact arbitrary hosts

**Exploit path [inference]:** A compromised or malicious 4byte response can return an arbitrary `next` URL. `cmd_fetch` passes it to `_get` without checking its scheme or host; `_get` calls `urllib.request.urlopen` without an origin or redirect guard. This can make the analyst's machine issue an outbound request to an internal HTTP(S) service. Its response is written into the chosen evidence directory before the next JSON parse. No attack was attempted.

**Evidence:** `read /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-25/a2/resolve-selectors.py:125-159` (successful read; no process exit code; source-review UTC stamp 2026-10-22T10:48:48Z). Excerpt:

```python
with urllib.request.urlopen(req, timeout=30) as r:
    return r.status, r.read()
...
url = json.loads(body).get("next")
...
status, body = _get(url)
```

The same code constructs the initial URLs only for 4byte.directory and openchain, and records the requested `url` in the manifest. It does not record the final URL after redirects. The saved responses show no live pagination exploit: the offline audit found `fourbyte_nonnull_next=0`; whether any saved request followed a redirect is unknown because final URLs were not recorded.

**Impact:** Conditional SSRF from the host running fetch; the current code sends no explicit credentials or request body, but an internal unauthenticated endpoint could be contacted and its response saved locally.

**Smallest remediation:** Require `next` to be HTTPS on the exact 4byte.directory origin, and enforce the same allowlist for every redirect (or disable redirects). Record the effective URL in the manifest.

### Informational — REA envelopes retain local filesystem paths

**Observation:** All six adjacent REA envelopes contain an absolute `subject.local_path`, including the local account and project path. These paths are not included in the selector lookup URLs. If the evidence is published outside the lane, redact the paths; no credential was found by the checks below.

**Evidence:** Offline audit output at 2026-10-22T10:47:53Z: `local_absolute_paths_in_envelopes=6`, `sensitive_field_key_hits={}`; exit code 0. The first envelope also shows `operation":"inspect_evm_interface"` and a local runtime hex path (`read .../corpus/evidence/round-25/a2/c2/carrierv/envelope.json`; successful read, no process exit code).

## Other requested checks

- **Outbound data [observation]:** `fetch` uses GET-style `Request` objects with `User-Agent: kaidoku-shokunin/round-25 (research)` and `Accept: application/json`. The initial lookup URLs carry only the selector (`hex_signature=0x{sel}` or `function=0x{sel}`) and, for openchain, `filter=false`; the 4byte pagination URL is the unvalidated `next` value described above. No bytecode, ABI, local path, authorization header, cookie, or request body is set by this code. The public lookup services also see the caller's network metadata and request timing.
- **Target contact / deployment [observation]:** The REA 6.5.0 EVM contract describes inspection of explicit local bytecode “without target execution or chain/RPC access” and says “No signature lookup, wallet action or transaction broadcast.” Its provider reads the local carrier and runs a bounded local EVMole/WASM worker. The resolver exposes only `selftest`, `fetch`, and offline `analyze`. Thus this workflow contacts signature databases, not a deployed contract; no deployment or transaction step was found.
- **138 saved lookup responses [observation]:** Offline audit command: `python3 -I -B /fast/scratch/hyaku/kaidoku-r25-a3/seats/Sentinel/audit_c2.py` (UTC 2026-10-22T10:47:53Z; exit code 0). Exact output excerpts:

```text
responses=138 envelopes=6 manifests=6 manifest_entries=138
json_errors=0 decoded_shapes={('response', 'dict'): 138, ('envelope', 'dict'): 6} statuses={'200': 138} hosts={'www.4byte.directory': 69, 'api.openchain.xyz': 69} hash_mismatches=0
fourbyte_nonnull_next=0 next_host_counts={}
html_injection_secret_pii_pattern_hit_counts={}
sensitive_field_key_hits={}
audit_result=clean_for_scanned_patterns
exit_code=0
```

  The audit checked JSON decoding, manifest hashes/statuses, HTML tags and encoded tags, common prompt-injection phrases, email/SSN shapes, common credential patterns, and sensitive field names. No saved response showed unexpected HTML or the scanned injected text; the resolver parses data as JSON and emits JSON, with no `eval` or HTML rendering in this path. The patterns are not a semantic proof that no personal information exists. A broad phone-number regex was discarded after false positives on numeric ABI signatures; no phone-data conclusion is made.
- **Artifact:** `/fast/scratch/hyaku/kaidoku-r25-a3/seats/Sentinel/audit_c2.py` — SHA-256 `313d0ec2ea1dd874480e96c278dc99d1e79b73136326f62b6b426fc909d41a50`. No tools were installed or updated.
