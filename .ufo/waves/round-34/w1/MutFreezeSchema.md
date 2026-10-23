# MutFreezeSchema — strict freeze-map lexical mutation probe

## Axes and result

Axes: **depth / schema discrimination**, **lexical precision**, and **containment / exact-byte restoration**.

One bounded text-input mutation matrix exercised the unchanged Round-34 freeze gate: **12 variants, 36 pristine→mutated→restored detector calls; 5 survived, 7 were rejected, 0 inconclusive**. Every pristine and restored call exited 0 with `CLEAN pins=1`. No production reader, version-needs counter, carrier parser, target executable, or REA was run.

The primary surviving mutant adds an earlier malformed value under the same JSON member name. The JSON decoder discards that occurrence before schema validation. Duplicate JSON-member detection is **absent**, not a tested capability of this successor. Its preparation report already discloses this limitation at `.ufo/waves/round-34/prep/R34FreezeSchema.md:210-213`; this probe supplies fresh end-to-end evidence, not a novelty claim.

A distinct measured lexical limit: `a/b` and `./a/b` across the two maps produce **CLEAN pins=2 for the same one-file payload**. By contrast, `a/./b` and `a//b` are rejected later as missing Git blobs, **not** as duplicate/schema errors.

These are lexical coverage findings. Duplicate-free JSON and canonical-path uniqueness are not retroactively added to the frozen contract. No claim judgment, admission, integration, production score, or repair is made.

## Frozen scope and measured source

Frozen predicate, preserved verbatim:

> P34-version-needs: twelve public ELF carriers yield exactly their independently frozen GNU version-needs records on opaque paths, including randomized same-length string-table naming wherever requirements are present, and the pinned source-backed decision table is present.

- Sandbox: `/fast/scratch/hyaku/kaidoku-r34/w1/MutFreezeSchema`.
- Source revision measured: `54a87a51a865ab931fd355e767303337b05cccf4`.
- Exercised gate: sandbox `tools/round-34/freeze-integrity.py`.
- Gate SHA-256 at that revision, before probing, and afterward: `fe955c5789123a94a575a2a2e29e2fac8702889817417b4d9892e91bc8a40138`.
- Python `3.14.8`; Git `2.56.0`; no installs or updates.
- Visible answering model: `openai-codex/gpt-6.1-sol`. No safety refusal, reroute, or quota fallback was observed.
- Driver UTC: `2026-10-23T10:56:03.147294+00:00` through `2026-10-23T10:56:05.550841+00:00`; exit **0**, stderr empty, elapsed **2.403510 s**.

Only the explicitly assigned text-fixture exception used other commits. The gate has no `--freeze` argument: it discovers the first-add claims commit. Each phase therefore used an independent parentless snapshot in one tiny nested sandbox Git repository. Stable `--rev HEAD` resolves to that phase's recorded commit, so freeze and measured revision are equal. This avoids the known inability to test changed claims by editing descendants of the original first-add commit. It does not test descendant tamper/restore history.

## Mutant and expected detector

The mutation point was the **claims JSON input**, not gate code. The fixture contains only `a/b` with these 31 inert bytes:

```text
MutFreezeSchema inert text pin
```

Let `H = bd7d6e82a1c62ea93a50305621ac3b27b9df8f09f3b4b7e960a189cae1eecad7`, its SHA-256. Pristine claims are `{"instruments":{"a/b":"H"},"frozen_inputs":{}}` plus a final newline, with H expanded.

Primary mutant: insert `"a/b":"not-a-sha256",` immediately before the valid `"a/b":"H"` member. Its complete exact bytes are retained in `MutFreezeSchema-files/evidence/duplicate_pin_bad_then_good.claims.json`.

Expected adversarial detector: reject ambiguous duplicate pin members before a malformed occurrence can be lost; a nonzero rejection kills this acceptance mutant. **No frozen duplicate-member error code exists or is asserted.** For the promised retained-value format rule, standalone malformed digests must instead exit **3**, `code=pin_digest_format`, with no `ok` row or CLEAN. For an exact cross-map duplicate, the promised detector is exit **3**, `code=pin_path_duplicate`.

Every phase used this exact bounded detector argv (the same argv for pristine, mutant and restored):

```text
/usr/bin/timeout --signal=TERM --kill-after=1s 12s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r34/w1/MutFreezeSchema/tools/round-34/freeze-integrity.py --root /fast/scratch/hyaku/kaidoku-r34/w1/MutFreezeSchema/.ufo/waves/round-34/w1/MutFreezeSchema-files/text-fixture --round 99 --rev HEAD
```

Exact launch argv:

```text
/usr/bin/timeout --signal=TERM --kill-after=2s 150s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r34/w1/MutFreezeSchema/.ufo/waves/round-34/w1/MutFreezeSchema-files/probe-freeze-schema.py
```

## Actual outputs and verdicts

All mutant stderr streams were empty; no detector timed out. “Killed” below means nonzero end-to-end rejection, **not necessarily duplicate detection**. All 12 baseline/restoration pairs were clean, so no rejection is attributed to a failing baseline.

| Input mutation / control | Exit | Actual finding | Verdict |
|---|---:|---|---|
| Duplicate pin: malformed first, valid last | 0 | `CLEAN pins=1` | Survived |
| Duplicate pin: valid first, malformed last | 3 | `pin_digest_format` | Killed by retained digest, not duplicate detection |
| Duplicate top-level `instruments`: absent-file pin first, valid map last | 0 | `CLEAN pins=1`; absent pin discarded | Survived |
| Duplicate top-level `frozen_inputs`: exact conflicting pin first, empty map last | 0 | `CLEAN pins=1`; earlier conflict discarded | Survived |
| Duplicate pin after JSON escape decoding: `a/b` malformed, `a/\u0062` valid | 0 | `CLEAN pins=1` | Survived |
| Exact `a/b` key in both maps | 3 | `pin_path_duplicate`, `where=a/b` | Killed by actual cross-map duplicate detector |
| Cross-map `a/b` versus `a/./b` | 1 | `FAIL a/./b sha=absent`; `FAIL pins=2 changed=1` | Killed at blob lookup, not schema |
| Cross-map `a/b` versus `./a/b` | 0 | Both rows `ok`, same payload SHA; `CLEAN pins=2` | Survived |
| Cross-map `a/b` versus `a//b` | 1 | `FAIL a//b sha=absent`; `FAIL pins=2 changed=1` | Killed at blob lookup, not schema |
| Standalone `not-a-sha256` digest | 3 | `pin_digest_format` | Killed |
| Standalone 64-character uppercase digest | 3 | `pin_digest_format` | Killed |
| Standalone correct digest plus escaped final newline | 3 | `pin_digest_format` | Killed |

Pristine and every restored stdout:

```text
ok	a/b	sha=bd7d6e82a1c6	commits_after_freeze=0
freeze-integrity: CLEAN pins=1 freeze=ac05168af6a8 rev=HEAD
```

Primary surviving mutant stdout, exit 0:

```text
ok	a/b	sha=bd7d6e82a1c6	commits_after_freeze=0
freeze-integrity: CLEAN pins=1 freeze=014055506258 rev=HEAD
```

Leading-dot alias stdout, exit 0:

```text
ok	./a/b	sha=bd7d6e82a1c6	commits_after_freeze=0
ok	a/b	sha=bd7d6e82a1c6	commits_after_freeze=0
freeze-integrity: CLEAN pins=2 freeze=40e538fc7879 rev=HEAD
```

Standalone malformed digest stdout, exit 3:

```text
freeze-integrity: ERROR schema code=pin_digest_format claims=.ufo/waves/round-99/claims.json where=instruments:a/b
```

Full stdout/stderr/exit, UTC, exact argv, input hashes, and full measured/freeze revisions for **every** phase are retained in `MutFreezeSchema-files/evidence/receipt.json`.

## Known lexical limits — do not overstate the repair

1. `load_pins` uses plain `json.loads(text)` at gate line 87, with no duplicate-member hook. Validation sees only the final decoded object. The four duplicate-member survivors directly measure this, including a JSON-escaped equivalent member name. Reversing bad/good order triggers digest validation but does not add duplicate detection.
2. The cross-map `if key in pins` check at lines 111-112 compares retained strings exactly. It correctly rejects the exact same key across maps; it does not establish canonical repository-path identity.
3. `_check_pin_path` at lines 77-81 checks nonempty text, leading `/`, embedded NUL, and literal slash-delimited `..` segments. It does not normalize `.` or repeated separators. The latter filters are source observations, not additional dynamically exercised cases in this matrix.
4. Full CLI outcomes depend on subsequent Git lookup: internal-dot and repeated-separator spellings pass schema then fail `git show`; leading `./` resolves successfully on this measured Git/toolchain. Consequently, “all aliases are rejected” and “aliases are schema-detected” are both unsupported.
5. `_DIGEST_RE.fullmatch` at lines 58 and 109 enforces exactly 64 lowercase hexadecimal characters **on retained values**. Malformed text, uppercase, and newline suffix were actually rejected. The duplicate bad-first/good-last survivor is discarded-occurrence blindness, not permissive matching of the surviving digest.
6. The preparation report's statement that historical claims lacked duplicate keys was **not rerun or independently established** here. No historical-wide, Unicode-normalization, case-folding, symlink, history-bypass, or production-counter uniqueness claim follows from this small matrix.

## Restoration and containment evidence

For every case, the same detector ran on pristine, mutated, and restored bytes. Restoration runs were in `finally`; after the matrix the claims bytes and fixture HEAD were restored again. Gate source was never edited.

| Item | Before / pristine | Mutated | After / restored |
|---|---|---|---|
| Primary claims SHA-256 | `a562135bf923f3de4b2868658ecd9a20cf00453133e0815d01be7d423d0e32ed` | `8a317345606fe7f96552977c1d39352c8c6e6bf2c150eca469603d8526d49494` | `a562135bf923f3de4b2868658ecd9a20cf00453133e0815d01be7d423d0e32ed` |
| Primary fixture revision | `ac05168af6a856614766b566a8eaa481e50ecfb7` | `0140555062589b41e74591bb9ccd3050862ea6df` | `ac05168af6a856614766b566a8eaa481e50ecfb7` |
| Payload SHA-256 | `bd7d6e82a1c62ea93a50305621ac3b27b9df8f09f3b4b7e960a189cae1eecad7` | unchanged | `bd7d6e82a1c62ea93a50305621ac3b27b9df8f09f3b4b7e960a189cae1eecad7` |
| Gate SHA-256 | `fe955c5789123a94a575a2a2e29e2fac8702889817417b4d9892e91bc8a40138` | unchanged | `fe955c5789123a94a575a2a2e29e2fac8702889817417b4d9892e91bc8a40138` |

All 12 per-case claims-restoration equality checks were true. Final restored fixture tree: `86667bf9a5f5d8edf242ae93d4b17c744780622f`.

Bounds: 150 s outer wall limit; 12 s per child command plus 1 s kill grace; child address space 256 MiB, CPU 10 s, file size 1 MiB, no core dumps, 128 file descriptors, process-count limit at most 4096. The driver bounds its own address space at 512 MiB, CPU at 90 s, and file size at 4 MiB. Only one child process tree ran at a time; each was collected and process-group cleanup attempted. All recorded groups were absent after collection, including the outer launch. No background jobs, delegates, sibling mutations, lane/fleet Git/jj writes, operator-config changes, or held-item access occurred. Git writes were confined to the named sandbox's new nested text-fixture repository, with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` removed. The sandbox's original source revision was not changed. Lane writes are only this report and its named archival directory.

## Retained evidence

`MutFreezeSchema-files/` contains the exact driver, launch receipt and stdout/stderr, gate source bytes, pristine and all twelve mutant claims files, payload bytes, detailed command/phase receipt, and a Git bundle retaining every tiny fixture snapshot. The Git bundle is archival evidence, not a target executable or ELF fixture. The restored scratch fixture remains under the named sandbox.

- Driver SHA-256: `e69e4a41c7fdb5ea67abdcec6d17c20f964733704c9036565d011128472b6dfb`.
- Detailed receipt SHA-256: `1f3f37f828ce7c42b9d6008cc3337147c4b2a9bd59abcdab8422dbf7e53b7ea8`.
- Fixture bundle SHA-256: `eb200a0be03f3dc60a600d5872bae7bd2c0dcd6c0e2042715cba6928156b8cd4`.
- `archive-manifest.json`: 21 copied evidence files, 358,996 bytes total; all source/archive SHA-256 pairs equal. The manifest itself is additional archival metadata.

No repair was attempted and no further detector run is requested by this seat.

Report: `.ufo/waves/round-34/w1/MutFreezeSchema.md`
