# Proposed fixes to the C1 landing — PATCH TEXT (NOT APPLIED) — seat CR-2 (critic)

Wave: arc3-loop1-round1. Target (post-landing): `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`
(from `claims/c1/EX-12/knowledge-entry.patch.md` hunk A) and `corpus/README.md:38`
(from hunk B). Each fix names what it reddens on. Nothing here was applied; no
repo file was modified by this seat outside its report + `claims/c1/CR-2/`.

---

## F1 (REQUIRED — measured failure): the entry's `recheck:` line fails as written

Measured: the entry's recorded recheck command, run verbatim on this host
(2026-10-19T10:12–10:14Z), exits 1 with a typed `execution_failure`
(`reason: "Unknown system error -122 … write"`, EDQUOT in the EVMole worker):

```
$ cd /tmp && npx -y rea-agents@6.4.0 inspect-evm-interface \
    <wave>/claims/c1/RV-2/Rv2Token.runtime.hex hex --format json
exit=1  {"code":"execution_failure", … "phase":"worker", "reason":"Unknown system error -122: …, write"}
$ (same, cwd=repo root)                        exit=1  same class
$ (same, TMPDIR=/var/tmp/cr2-arc3l1r1-scratch/reatmp)  exit=0  ev_45849c8b…, 5/5 functions
```

Evidence: `claims/c1/CR-2/recheck-fail-cdtmp.json`, `recheck-fail-root.json`,
`recheck-ok-disk-tmpdir.json`. Corroborated by RV-2's seat report §5 ("Any parent
re-run of the canonical probe MUST set TMPDIR to a non-/tmp path") and EX-06's
`evidence/repro.sh:11` ("required: the system /tmp tmpfs is usrquota-exhausted").

Replace the `recheck:` line (the `…` path stays byte-identical; only the prefix changes):

```diff
-recheck: `cd /tmp && npx -y rea-agents@6.4.0 inspect-evm-interface /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.hex hex --format json` → expect 5 functions, all `dispatch:"abi"`, decoded `bytecode.sha256 c1081a56…`; the sealed id `ev_45849c8b…` was re-derived across same-request reruns — the `ev_` id domain for this verb family was not measured, so if a fresh run mints a different id, compare by `subject.digest.sha256` + function payload instead.
+recheck: `mkdir -p /var/tmp/cr2-recheck && TMPDIR=/var/tmp/cr2-recheck npx -y rea-agents@6.4.0 inspect-evm-interface /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.hex hex --format json` → expect 5 functions, all `dispatch:"abi"`, decoded `bytecode.sha256 c1081a56…`; the sealed id `ev_45849c8b…` was re-derived across same-request reruns (measured again with the disk-backed TMPDIR, 2026-10-19T10:14Z) — the `ev_` id domain for this verb family was not measured, so if a fresh run mints a different id, compare by `subject.digest.sha256` + function payload instead. On this host a `/tmp`-defaulted run fails EDQUOT (errno -122) in the EVMole worker: a disk-backed `TMPDIR` is required, not optional.
```

## F2 (recommended): the entry's recorded file identity is stale vs its own patch text

Measured: applying hunk A as written yields 8,598 bytes / 31 lines /
sha256 `d8d85949cc98cd0312655d1eeacd1c7b387f15ce4b564478dc60ceb3d7abd23f`;
the patch text's "Verification performed" step 4 claims 8,316 bytes /
`f95c5a05f0500ab9d16b3f653880d575f229baa60d1e265dd7a7248389c65d49`.
EX-12's own scratch file (`/var/tmp/ex12-apply-test/corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`)
hashes `f95c5a05…` — the patch text was revised after hashing (path-style edits
only: `attack/probe-many.json` → fully-qualified path; `corpus/knowledge/…` added
to the r3-errata cite). Diff: `claims/c1/CR-2/entry-version-diff.txt`.

Do NOT revert the patch; the landed revision is the more explicit one. At landing,
record the fresh hash of the landed bytes in the LOG/SCORECARD evidence and drop
the stale `f95c5a05…`/`8,316` claim (or re-hash EX-12's verification section).

## F3 (optional, scope-language): record that r3-07's candidate-2 hypothesis is refuted

`corpus/knowledge/2026-10-13-r3-evm-interface.md:44-45` records the suggestion
"classification appears to need richer bytecode (real solc output) to engage".
Measurement refutes it: `bytecode.kind` stayed `"unknown"` on real solc 0.8.37
output on every leg (runtime `probe-runtime-hex-6.4.0.json` / `…-6.7.0.json`;
creation `probe-creation-hex-6.4.0.json`, `probe-EX02-smoke-bin-6.4.0.json`;
KdxToken `run-hex-6.7.0.json`). The entry records `kind:"unknown"` but does not
mark the hypothesis refuted, leaving the r3-07 sentence standing unamended.
Append one sentence to the creation-code observation (append-only discipline —
the entry is a new record, so place it in the new entry, not in r3-07):

```diff
 - **Observation (creation code — parsed-and-empty, not excluded):** `Rv2Token.creation.hex` @6.4.0 `ev_c80379e1…` → 0 functions, `bytecode.kind:"unknown"`; `Smoke_sol_Smoke.bin` @6.4.0 `ev_f875e21e…` → 0 functions. Creation blobs carry no runtime dispatch table; these are parsed-and-empty results (`corpus/QUALITY.md:21`), not inventory exclusions.
+- **Observation (r3-07 hypothesis, refuted):** r3-07's candidate-2 note ("classification appears to need richer bytecode (real solc output) to engage", `2026-10-13-r3-evm-interface.md:44-45`) is refuted by measurement: on real solc 0.8.37 runtime and creation output alike, `bytecode.kind` stays `"unknown"` (same envelopes as the line above; KdxToken `run-hex-6.7.0.json`). `kind` classification remains open, not engaged.
```

## F4 (optional, scope-language): the coverage-map row's state text now understates the row

`corpus/README.md:38` after hunk B lists both entries but keeps the state text
"held — EVMole selectors recovered from synthetic dispatcher; positional encoding
quirk", which describes only the r3-07 leg. Still line-neutral (same physical
line, line count unchanged — measured 190 → 190 lines). PL-1's plan §S12 drafted
the accurate form; land this variant of the same-line edit or record the gap as
named debt:

```diff
-| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc` | held — EVMole selectors recovered from synthetic dispatcher; positional encoding quirk |
+| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); positional encoding quirk |
```

## F5 (nit, label consistency): "r3 erratum" → "the r3-07 entry's round-4 erratum"

The entry cites `(r3 erratum, 2026-10-13-r3-evm-interface.md:149-155)`; the
errata section in that file is titled "Errata (round 4)" (authored by the r4
audit-A). The line range is correct; the label can be misread as "round-3
erratum". Suggested same-line wording: `(the r3-07 entry's round-4 erratum,
`corpus/knowledge/2026-10-13-r3-evm-interface.md:149-155`)`.
