# ReviewExactDiff — round 16, w1

Lane: reviewer (leaf, no dispatch). Axes: depth, calibration.
Scope: exact-diff selection and suppression of higher patches, against Ghidra source/data (source model only).

## Evidence state

- **No candidate artifact exists.** `.ufo/waves/round-16/selection.py` and `selection-fixtures.json` are absent at review time (`ls`, checked). This review is therefore a contract-versus-source review with proposed failure cases, as the lane permits. Nothing here is a pass on an implementation.
- `selfcheck.py` exists in the wave directory; it is outside this lane and was not reviewed.
- Source: `Base-src.zip` member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` (extracted, read). Also `golang/GoVer.java`, `rtti/JsonPatch.java` for the diff format.
- Data: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang` (inspected read-only with `ls`, `grep`, `jq`, and short Python scans of diff text; no selector, test, or build was run).
- Tools installed/updated: none.

## Source contract (verified)

| Behaviour | Anchor |
|---|---|
| Base is `goVer.withPatch(0)`; missing base returns null before any diff lookup, so no diff is considered | GoApiSnapshot.java:122-126 |
| Diff lookup is `getPatchVerDiffFile(goVer)`; with patch 0 the loop never runs, so no diff | :148-156 |
| Loop decrements only (`prevPatch`), so diffs above the request are never consulted | :153-156; GoVer.java:134-136 |
| Diff path is `typeinfo/golang/patchverdiffs/go{M.m.p}.json.diff`; no same-minor fallback | :168-171 |
| Base-only returns the unpatched base file; diff returns a derived provider with the patch applied | :128-145 |
| Snapshot is labelled with the **requested** version, not the selected base or diff | :111, :239 (`new GoApiSnapshot(ver, …)` where `ver` is the requested `goVer`) |
| Arch search list contains `""` for non-unix OS; `read` skips empty and missing names; result order is list order | :108-109, :228-237 |
| `unix` only for IS_GOOS_UNIX (aix, android, darwin, dragonfly, freebsd, hurd, illumos, ios, linux, netbsd, openbsd, solaris) | :180-181 |
| Version parsing: `Integer.parseInt` on each part; overflow yields INVALID; leading zeros accepted; trailing text after a space stripped | GoVer.java:62-80 |

## Data facts (verified)

- Bases present: go1.15.0 through go1.25.0 (11 files). No base for other minors.
- Patch diffs: 123 files. Contiguous, no gaps, for minors 1.15 (1–15), 1.16 (1–15), 1.17 (1–13), 1.18 (1–10), 1.19 (1–13), 1.20 (1–14), 1.21 (1–13), 1.22 (1–12), 1.23 (1–12), 1.24 (1–6). **No diffs for 1.25.** Consequence: a lower-fallback fixture needs a synthetic gap, or a request beyond the maximum (e.g. 1.24.9 → 6, 1.21.99 → 13).
- Diff top-level path heads (first array element of each `@` line) are a subset of base top-level keys for every minor 1.15–1.24 (checked with `comm` under `LC_ALL=C`). Diffs never add or remove top-level arch buckets in shipped data.
- Diffs are cumulative from base, not per-patch deltas. Evidence: every 1.15.1 block (header plus body) is present verbatim in 1.15.2 and 1.15.15 (16/16); 1.21.1→1.21.2 is 497/497; 1.21.12→1.21.13 is 1316/1316. Some later blocks changed (1.21.5 blocks present verbatim in 1.21.13: 704/832; 1.15.14→1.15.15: 831/836), consistent with later revisions of positions/types rather than a per-patch model. This supports the single-diff-against-base model at Java anchor :136-140. **[INFERENCE: cumulative model for all minors; checked by block identity sample, not exhaustively.]**
- go1.21.0 base contains `linux-amd64`, `linux`, `unix`, `amd64`, `all`, `windows-amd64`, `windows`. Expected base buckets for linux/amd64: all five present; for windows/amd64: `windows-amd64`, `windows`, `amd64`, `all` present.

## Findings (by severity)

**F1 — medium, correctness: overflow and loop cost are unaddressed.**
Java parses patch with `Integer.parseInt` (GoVer.java:70-77); an overflowing or invalid version becomes INVALID, whose base `go0.0.0.json` is absent, so the result is EMPTY (GoApiSnapshot:122-126, :115). A Python `for p in range(request, 0, -1)` with a request such as `1.21.2147483648` (or `1.21.999999999`) performs about 2×10⁹ or more `stat` calls before returning. The contract says "nearest present diff <= request" but does not bound request or specify the search method.
*Proposed failure:* `--request 1.21.999999999` hangs; or `1.21.2147483648` is reported as a valid request.
*Fix:* reject patch > 2³¹−1 (exit 2, or missing_base consistent with Java; state which), and find the nearest diff by listing `patchverdiffs/go{M.m}.*.json.diff` rather than counting down.

**F2 — medium, calibration: status enum conflates an exact base with an unpatched preview.**
For request `M.m.0`, Java returns the base unchanged (:128-131 with patchDiffFile null), which is the exact snapshot for that version. The contract labels every no-diff base result `base_only`, and says base-only matching "is unpatched preview." For patch 0 that label understates the base and is inconsistent with a nonzero request without a diff (e.g. 1.25.1, where the base is go1.25.0 and not 1.25.1).
*Fix:* add an explicit basis field (e.g. `selection_basis: "base_exact" | "base_unpatched_preview" | "exact_diff" | "fallback_diff"`), or document that `base_only` with `selected_patch: null` and `requested` patch 0 means exact base.

**F3 — medium, contract wording: "must be labelled so when diff selected" is undefined.**
The contract requires `base_matching_buckets` to be "unpatched preview… labelled so when diff selected," but does not say what the label is, which statuses carry it, or which key it uses. In shipped data this is harmless (F-data above: top-level keys are invariant under the diffs for 1.15–1.24), but a generic selector cannot rely on that, and Java's applicability is computed after patching (:136-142, read at :239).
*Fix:* emit `bucket_source: "base_unpatched"` on every status where `selected_diff` is non-null, and document that buckets are computed on the base file only.

**F4 — low, calibration: `arch_search_order` representation of the empty placeholder is unspecified.**
Java's list is `[goos-goarch, goos, unix|"", goarch, all]` (:108-109). For non-unix OS the `""` is a placeholder that `read` drops (:229-231). The contract does not say whether `""` appears in the emitted `arch_search_order`.
*Fix:* emit without `""`, document it, and make the windows fixture expect `["windows-amd64","windows","amd64","all"]`.

**F5 — low, calibration: strict parsing diverges from Java; the choice is not recorded.**
Java accepts `1.21.03` (parseInt gives 3; the label becomes `1.21.3`) and `1.21.3 X:rangefunc` (GoVer.java:63-65). The contract asks for "strict stable M.m.p parsing" without saying whether leading zeros are rejected or canonicalized. If canonicalized, the emitted `requested` must echo the canonical form, or a consumer will see a mismatch.
*Fix:* state the rule and add a fixture for `1.21.03`.

**F6 — medium, correctness: missing base must short-circuit selection.**
Java returns before any diff lookup when the base is missing (:122-126). A selector that checks diffs first would emit `exact_diff` or `fallback_diff` for a missing base. Shipped data has no missing base for 1.15–1.25, so this needs a synthetic fixture (diff present, base absent). Expected output: `status: missing_base`, `base: null`, `selected_diff: null`, `selected_patch: null`.

**F7 — medium, correctness: minor isolation and unseen minors.**
Same-minor base is required (:122 `withPatch(0)`), and the diff loop stays in the same minor (:148-156). Cases to lock in fixtures: `1.23.0` must not use `go1.22.12.json.diff`; `1.25.1` must not use `go1.24.6.json.diff` (real data: base go1.25.0 exists, no 1.25 diffs → `base_only`, `selected_patch: null`); `1.26.0` and `2.0.0` are syntactically valid and must yield `missing_base` (exit 0), not exit 2, unless the contract defines them as invalid. Java returns EMPTY for them (:115).

**F8 — medium, correctness: unreadable base must not produce a status.**
Java parses the whole base through Gson (:205-226); a malformed base throws IOException from `get`. The contract says "exit2 invalid/unreadable" but does not say that a present-but-unparseable base exits 2 rather than emitting `exact_diff` from the sha256 path alone. `base_matching_buckets` requires parsing, so this is reachable.
*Fix:* exit 2 on JSON parse failure or non-object top level, before emission.

**F9 — low, calibration: labelling by Ghidra itself.**
Ghidra labels every result with the requested version, including base-only and fallback results (:111, :239). The selector must not inherit this: `selected_patch` is the only field that identifies the data version. Flag in the report that a fallback or base-only result is not the requested patch.

## Fixture expectations (source-law, for the fixtures author; not computed)

| Case | Request | Expected status | selected_patch | Anchor |
|---|---|---|---|---|
| missing base despite diff | 1.21.3, no go1.21.0.json | missing_base | null | :122-126 |
| exact diff | 1.21.3, base + diff 3 | exact_diff | 3 | :153-156 |
| lower fallback | 1.24.9 (real data) | fallback_diff | 6 | :153-156 |
| no diff (nonzero, same minor absent) | 1.25.1 (real data) | base_only | null | :148-156 |
| patch0 | 1.21.0 | base_only (see F2) | null | :128-131 |
| future diff ignored | 1.21.5 (real data; 6–13 exist) | exact_diff | 5 | :153-156 |
| minor isolation | 1.23.0 | base_only, no 1.22 diff | null | :122, :148-156 |
| unix order (linux/amd64) | 1.21.0 | order `[linux-amd64,linux,unix,amd64,all]`, all present | — | :108-109, :180-181 |
| windows omission | 1.21.0 windows/amd64 | order `[windows-amd64,windows,amd64,all]`, all present | — | :108-109 |

## Residual risk and verification gaps

- No selector exists; F1–F8 are proposed failures from source, not observed behaviour.
- The cumulative-diff model is supported by block-identity samples, not an exhaustive check of every minor; [INFERENCE] remains.
- Diff content (position and type changes) is not validated; this review is selection-only.
- The contract text itself is the only spec; there is no separate shared-fixture schema file to check against.
