# Round-24 reproduction-input review (`.ufo/waves/round-24/repro/`)

Reviewer: `KagiR27-2.ResRepro-2` (read-only leaf). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
branch `main`, HEAD `69e82c48be5614ce96f7c1c32445fe61c4870630`. Scope asked: (a) do the manifest digests equal the
subjects in the cited r22/r23 envelopes, (b) is the fetcher safe (path escape, partial downloads). No lane file was
edited; the only write is this report. No install performed (no pacman, no new tool). Scratch used:
`/fast/scratch/kaidoku-r24/seats/KagiR27-2.ResRepro-2` (throwaway copies of `fetch-inputs.py`, local HTTP servers,
manifests). Tools: `curl` 8.23.0, `python3` 3.14.8, `sha256sum`, `tar`, `zipfile`, `git` (read-only), GitHub REST API,
F-Droid `index-v1.json`. No LSP server answers this lane (no `lsp` device is mounted: `xd://lsp` does not exist), so
caller/definition checks were done by literal text search and are reported as such, not as semantic proof.

## Verdict

**Not verified.** The six manifest digests and the six run-1 digests are byte-consistent with each other and with
five of the six cited envelope subjects; the sixth citation (sigrok-cli AppImage) points at files that never contain
that digest. The fetcher's *download* path is escape-checked, but its *member-extraction* path is not: a pre-existing
symlink at `DEST/<id>.member` makes the tool write **and then delete** a file outside `DEST`, which falsifies the
docstring's "refuses any path outside it". The receipt is also unbound to the manifest/script revision that produced
it, and `run-1.jsonl` is not valid JSONL. These are defects in the *reproduction probe*, not in either frozen claim:
R24-C1 (packet-capture family 0/4 → 4/4) and R24-C2 (claim-freeze audit) are measured by `count-c1.py` /
`freeze-gate.py` and are untouched by anything below. This review does **not** call round 24 verified.

## Findings

### F1 — Medium — the sigrok-cli entry's `used_by` citations do not contain the manifest digest

- **Observation.** `.ufo/waves/round-24/repro/inputs.json:9` pins the sigrok-cli 0.7.2 AppImage at
  `sha256 49d2f597ec3ed3d71bfeb0465474ec2aac084fa1f66cbb132d996f7c9f50b614`, `bytes 49558848`, and cites
  `used_by` = `.ufo/waves/round-23/tools/sigrok-cli.sh`,
  `.ufo/waves/round-23/evidence/c1/inventory.envelope.json`,
  `.ufo/waves/round-23/evidence/c1/decode-official-uart.envelope.json`.
- **Observation.** `grep -c 49d2f597…` over those three files = **0, 0, 0**. The two envelopes' own subjects are
  different files: `inventory.envelope.json` subject = `sigrok-cli.sh` @ `50fe4359…`; `decode-official-uart.envelope.json`
  subject = `hello_world_8n1_9600.sr` @ `01b7261…`; `sigrok-cli.sh` contains no 64-hex digest at all.
- **Observation.** The digest is actually carried by `.ufo/waves/round-23/sigrok-extraction.json:7`
  (`appimage_sha256`), `.ufo/waves/round-23/tools/setup-sigrok.py:14` (`EXPECTED = '49d2f597…'`), and
  `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md:93`.
- **Observation (independent corroboration of the digest itself).** `sha256sum
  /home/vgpnk/.local/opt/sigrok-cli-0.7.2-x86_64.AppImage` = `49d2f597…` (the carrier is still on the author host);
  my re-download of the official URL matched `49d2f597…` exactly. So the *digest* is right and independently
  supported; the *citation* is wrong.
- **Inference.** A reader following `used_by` to "the subject in the cited envelope" finds a different subject
  digest and cannot confirm the manifest entry from the cited files. The other five entries do carry the digest in
  their cited envelope/tool file (see the table under F12).
- **Recommendation.** Point `used_by` at `.ufo/waves/round-23/sigrok-extraction.json` and
  `.ufo/waves/round-23/tools/setup-sigrok.py` (and the r23 knowledge entry), or cite an envelope whose subject *is*
  the AppImage.

### F2 — Medium — the member-extraction path is not containment-checked: a symlink makes the tool write and delete a file outside `DEST`

- **Observation.** `fetch-inputs.py:47-50` escape-checks the download target
  (`target = (dest/(id+'.download')).resolve()`; reject unless `target.parent == dest`). `fetch-inputs.py:63-66`
  computes `subject = (dest/(id+'.member')).resolve()` and writes it with **no escape check**; `fetch-inputs.py:75`
  then `subject.unlink(missing_ok=True)` when `--keep` is absent.
- **Reproduction (read-only against the lane; a copy of the script was exercised).** With `DEST/m.member` pre-created
  as a symlink to an outside file `precious.txt`, a manifest entry `{"id":"m","member":"m/x.apk"}` over a local zip:
  the tool resolved the symlink and wrote the member bytes through it; the outside file
  `/fast/scratch/…/outside3/precious.txt` was **overwritten and then deleted** (`VICTIM still exists? False`;
  with `--keep` the outside file was 4000 bytes of `EVIL…` instead of its original content). The `.download` path
  *is* protected against the same trick (symlinked `x.download` → rejected with `path_escape`, exit 2).
- **Observation.** The `.resolve()` on line 63 follows the symlink, so the write target is outside `DEST` — exactly
  what the docstring (line 8: "refuses any path outside it") claims cannot happen.
- **Inference.** Likelihood in the lane is low (the destination is operator-chosen scratch), but the guarantee is
  stated in the docstring and in `SKILL.md:777` ("deletes bytes unless `--keep`"), and the failure mode is destructive
  (data loss outside the destination) rather than merely a wrong verdict.
- **Recommendation.** Apply the same `parent == dest` containment test to `subject` after `.resolve()`, and refuse to
  write through a symlink (`os.path.islink` / `O_NOFOLLOW`).

### F3 — Medium — the receipt is not bound to the manifest/script revision, and the negative-control manifest is not retained

- **Observation.** `.ufo/waves/round-24/repro/receipt.json` records `argv`, `cwd`, `started_utc`, `exit`, `result` and
  a `negative_control` block — but **no sha256 of `inputs.json` or `fetch-inputs.py`, and no `curl` version**. The
  negative control's `argv` points at `/fast/scratch/kaidoku-r24/neg-manifest.json`, a path outside the repository;
  `git ls-files | grep neg-manifest` = empty, so the mutated manifest survives only in scratch.
- **Observation.** The sibling lane convention *does* bind the tool: `.ufo/waves/round-24/evidence/c1/l1-pcap-client.run.json`
  carries a `tool_sha256` key; `.ufo/waves/round-24/measure/selftest-69e82c48.jsonl` records
  `instrument_sha256` for `count-c1.py` and `freeze-gate.py`.
- **Inference.** Editing `inputs.json` or `fetch-inputs.py` after the run would leave `receipt.json` looking valid;
  the round-24 freeze row `corpus/claim-freezes.tsv:12` (`round-24 CLEAN`) and `claims.json` `instruments` map cover
  only `count-c1.py` and `freeze-gate.py`, so nothing in the frozen gate would notice. The receipt is the evidence
  artifact that `corpus/lessons/round-24.md:58` (M24-3) leans on, so it is the right place to pin.
- **Recommendation.** Add `inputs_sha256`, `fetch_inputs_sha256`, `curl_version` to `receipt.json`; commit the
  negative-control manifest next to `neg-control.jsonl` (or inline its full content in the receipt).

### F4 — Low/Medium — `run-1.jsonl` is not valid JSONL

- **Observation.** `.ufo/waves/round-24/repro/run-1.jsonl` has 8 lines; lines 1-7 are JSON objects, line 8 is the bare
  text `exit=0` (`cat -A` shows `exit=0$`; `json.loads` raises `Expecting value: line 1 column 1`). A strict JSONL
  reader fails on it.
- **Observation.** `git grep -c "^exit=" -- '*.jsonl'` matches **only** this file in the whole repository; the sibling
  `neg-control.jsonl` (2 lines) and `.ufo/waves/round-24/measure/selftest-69e82c48.jsonl` are pure JSONL.
- **Observation.** The defect is in the retained artifact, not a copy: `sha256sum` of the scratch copy
  `/fast/scratch/kaidoku-r24/repro-run.jsonl` equals the committed `run-1.jsonl` (`f0410feac319bf4d…`), and
  `receipt.json:2` points readers at that file.
- **Recommendation.** Drop the trailing `exit=0` line (the exit status is already in `receipt.json` and in the final
  `{"selected": 6, "exit": 0}` summary object).

### F5 — Low/Medium — a failed fetch leaves the partial file in `DEST` (asymmetric cleanup)

- **Observation.** `fetch-inputs.py:54-58` handles a non-zero `curl` exit by printing a record and `continue`ing —
  the cleanup at lines 72-75 is never reached, so `DEST/<id>.download` survives.
- **Reproduction.** A local server that answers with `Content-Length: 1000000` then closes after 1000 bytes makes curl
  exit 18; the tool exits 2 and leaves `dest/t1.download` (1000 bytes) on disk **without** `--keep`. The mismatch path
  (exit 1) does delete its file; the success path does too. Only the fetch-error path leaks.
- **Observation.** A truncated download *with* `Content-Length` is therefore caught twice (curl exit 18 → exit 2). A
  truncated download *without* `Content-Length` is caught once: curl exits 0, the tool hashes the short body and the
  size+sha comparison (line 69) reports `match:false` → exit 1. I confirmed both branches: with `Content-Length`
  → `curl_exit 18`; without → `curl_exit 0`, `bytes 100` vs expected `5000`, `match:false`, exit 1. **No truncated
  download can be reported as a match.**
- **Recommendation.** Unlink the partial file in the error branch too, so `DEST` never holds a file that could be
  mistaken for a complete input.

### F6 — Low/Medium — unhandled exceptions exit 1 (colliding with "1 = digest mismatch") and leave the bytes on disk

- **Observation.** `fetch-inputs.py:64` (`z.open(item['member'])`) and line 69 (`item['bytes']`) are unguarded. A
  missing zip member raises `KeyError`, a corrupt archive raises `zipfile.BadZipFile`, a manifest entry without
  `bytes` raises `KeyError` — each prints a Python traceback and exits **1**, with no JSON summary line.
- **Observation.** Exit 1 is documented as "digest mismatch" (`fetch-inputs.py:10-11`; `SKILL.md:777` "0 all match, 1
  mismatch, 2 fetch error"), and exit 2 as the fetch/usage error. A usage error therefore reports itself as a
  mismatch. The archive is also not cleaned up in that path, so a 1.28 GB `.tpz` can be left in `DEST`.
- **Recommendation.** Catch `KeyError`/`BadZipFile`/`OSError` per input, emit `{"id":…,"error":…}` and exit 2.

### F7 — Low — the godot entry's pinned size/digest describe the archive *member*, not the fetched archive

- **Observation.** `inputs.json:10` pins `bytes 104803333` and the member digest with `"member":
  "templates/android_release.apk"`, while the URL serves a 1,281,349,702-byte `.tpz`. `run-1.jsonl` line 5 is
  internally consistent: `archive_bytes 1281349702`, `archive_sha256 f298490b…`, `bytes 104803333`, `sha256 6d1bb2…`,
  `match true`.
- **Observation.** The archive digest `f298490b8d44d934be425a5a65a51bf15f422428b229a06a6e11d9ffea248011` equals the
  `sha256:` digest GitHub publishes for that release asset (`api.github.com/repos/godotengine/godot/releases/tags/4.7.2-stable`,
  asset `Godot_v4.7.2-stable_export_templates.tpz`, `size 1281349702`) — but that value appears **only** in the run
  log; `inputs.json` pins no archive-level digest or size, so a re-run cannot detect a substituted archive.
- **Inference.** `receipt.json:7` ("6/6 inputs re-downloaded … with size and sha256 equal to the retained witness
  subjects") is true of the member but glosses that the artifact actually transferred for that input is 1.28 GB.
- **Recommendation.** Add an optional `archive_bytes`/`archive_sha256` to the manifest and check it, and state the
  member-vs-archive distinction in the receipt text.

### F8 — Low — no transfer-time bounds on `curl` (unbounded download / no timeout)

- **Observation.** `fetch-inputs.py:51-52` invokes `curl -fsSL --retry 2 -o TARGET URL` — no `--max-time`,
  no `--connect-timeout`, no `--max-filesize`, and the manifest's `bytes` is not enforced during transfer (it is only
  compared afterwards at line 69). A hostile or misconfigured origin can stream unbounded data into `DEST` (the
  workspace root disk is 98 % full; only the run's `--dest` was on `/fast`) or hang the run indefinitely.
- **Recommendation.** Pass `--max-time`/`--connect-timeout` and `--max-filesize <manifest bytes>` (for non-member
  entries) to curl.

### F9 — Low — exit-code precedence and non-self-describing mismatch records

- **Observation.** `fetch-inputs.py:57` sets `code = 2` unconditionally on a fetch error, while line 70-71 sets
  `code = 1` only `if code == 0`. A run containing both a mismatch and a fetch error exits 2 in either order, so
  "1 = wrong digest" (the M24-3 contract at `corpus/lessons/round-24.md:58`) is not reliable for mixed runs; the
  per-item record still shows `match:false`, so the information survives, but not in the exit status.
- **Observation.** The record has `sha256` (observed) and `match` but **no `expected_sha256`**, so a mismatch record
  alone does not say what was expected — in `neg-control.jsonl` the `sha256` field shows the *real* digest
  `a7b1f5c8…` with `match:false`, and only the receipt's prose explains that the manifest expected 64 zeros.
- **Recommendation.** Record `expected_sha256`/`expected_bytes` in each record, and define the mixed-case precedence
  explicitly (e.g. "2 if any fetch error, else 1 if any mismatch").

### F10 — Low — `--only` treats a duplicate manifest id as an unknown id

- **Observation.** `fetch-inputs.py:41-44` compares `len(selected)` with `len(set(a.only))`. With a manifest holding two
  entries with id `dup`, `--only dup` selects 2 items while `set(a.only)` has 1 element → prints
  `{"error": "unknown id in --only"}` and exits 2, even though `dup` is a known id (reproduced locally). Today's
  manifest has unique ids, so this is latent.

### F11 — Low — the sigrok re-extraction note points at the wrong directory and is blocked on this host

- **Observation.** `inputs.json:9` note: "round-23 wrapper runs the gitignored extraction
  `.ufo/waves/round-23/runtime/squashfs-root`; re-extract with `<AppImage> --appimage-extract` **in that
  directory**". The round-23 recipe extracts *into* `runtime` (producing `runtime/squashfs-root`):
  `.ufo/waves/round-23/tools/setup-sigrok.py:25-31` uses `runtime = parents[1]/'runtime'` and `cwd=runtime`; the
  wrapper `.ufo/waves/round-23/tools/sigrok-cli.sh` expects `<base>/runtime/squashfs-root/usr/bin/sigrok-cli`.
  Extracting "in that directory" would yield `runtime/squashfs-root/squashfs-root` and not satisfy the wrapper.
- **Observation.** `setup-sigrok.py:26-28` refuses when `runtime/squashfs-root` already exists
  (`{"finding":"runtime_already_exists"}`, exit 2) — and on this host it *does* exist (gitignored:
  `.ufo/waves/round-23/.gitignore:1: /runtime/`), with `runtime/squashfs-root/usr/bin/sigrok-cli` present. So the
  documented step cannot be executed as written until the existing directory is removed.
- **Recommendation.** Quote the actual recipe (`.ufo/waves/round-23/tools/setup-sigrok.py`, run from the lane) and
  note the `runtime_already_exists` precondition.

### F12 — Info — what *does* check out (so the round-24 disposition is not disturbed)

- **Observation (manifest digest ↔ cited subject).** Subject digests read out of the cited envelopes, compared with
  `inputs.json`:

  | manifest id | manifest sha256 | cited file | subject digest / bytes | equal |
  |---|---|---|---|---|
  | saber-1360103 | `de4813f9…b720` | `.ufo/waves/round-22/evidence/c1/identify-flutter-build-saber.envelope.json` | `de4813f9…b720`, 42 305 081 | yes |
  | saber-1330203 | `a7b1f5c8…a618` | `.ufo/waves/round-23/evidence/c1/inspect-dart-legacy-saber.envelope.json` | `a7b1f5c8…a618`, 41 263 437 | yes |
  | saber-1340303 | `ac68a976…b8b8d` | `.ufo/waves/round-23/evidence/c1/connect-dart-symbols/inspect-dart-aot-saber-1340303.envelope.json` | `ac68a976…b8b8d`, 42 571 868 | yes |
  | godot-4.7.2-android-release | `6d1bb2cf…e6cb` (member) | `.ufo/waves/round-22/evidence/c1/identify-godot.envelope.json` | `6d1bb2cf…e6cb`, 104 803 333 | yes |
  | wireshark-4.6.9-source | `d062d416…c0f` | `.ufo/waves/round-24/tool-pins.json` (`/wireshark/source_sha256`) | `d062d416…c0f`, 56 477 044 | yes |
  | sigrok-cli-0.7.2-appimage | `49d2f597…b614` | the three cited `used_by` files | *absent* (subjects are `sigrok-cli.sh` `50fe4359…` and `hello_world_8n1_9600.sr` `01b7261…`) | **no** (F1) |

  The three `used_by` knowledge files also carry the digests (`2026-10-21-r22-flutter-positive-dart-refusal.md` ×2,
  `2026-10-21-r23-dart-legacy-layout-boundary.md` ×1, `2026-10-21-r22-flutter-static-boundary.md` ×1).
- **Observation (independent re-acquisition, no item > 100 MB re-downloaded).** Re-running the tool over the five
  non-godot entries gave `match:true` for all five with **identical** sha256 and byte counts to `run-1.jsonl`
  (diff of the five records: only the ordering/line offset differs). The godot member was verified **without**
  downloading the 1.28 GB archive: an HTTP `Range` read of the `.tpz` central directory lists exactly
  `templates/android_release.apk` (method 8, csize 103 949 600, usize 104 803 333) and inflating just that member
  yields sha256 `6d1bb2cfa126a1b1c87e064a35b3cbd181bef0ec784dec1efd1d64dffa8be6cb` = manifest = r22 envelope subject;
  the local copy `~/.local/share/godot/export_templates/4.7.2.stable/android_release.apk` hashes the same.
- **Observation (upstream corroboration).** F-Droid `index-v1.json` lists `com.adilhanney.saber` 1360103 with
  `hash de4813f9…b720`, `size 42305081` (= the manifest), and 1330203/1340303 with the same hashes/sizes as the
  manifest (also in `.ufo/waves/round-23/evidence/c1/connect-dart-symbols/fetch.json`).
- **Observation (the `in_git` list is true).** All four `in_git` paths exist and are git-tracked (3 files + the three
  tracked captures). The three committed captures are **byte-identical** to the upstream
  `wireshark-4.6.9.tar.xz` members `test/captures/{dns_port.pcap,http.pcap,tls12-dsb.pcapng}`
  (`78c3c00e…`, `69e489a2…`, `d6034147…` on both sides), corroborating `tool-pins.json` `capture_inputs.carrier`.
- **Observation (the receipt's "bytes deleted" claim is true).** `/fast/scratch/kaidoku-r24/repro` and
  `/fast/scratch/kaidoku-r24/repro-neg` are both empty directories after the runs.
- **Observation (timeline coherent).** `receipt.json` `started_utc 2026-10-21T16:57:05Z` sits between the mtimes of
  `inputs.json` (16:57:02Z) and `run-1.jsonl` (16:58:36Z); `fetch-inputs.py` mtime 16:56:38Z precedes the run.
- **Observation (no claim depends on any of this).** `grep -c fetch-inputs` in
  `.ufo/waves/round-24/tools/count-c1.py` and `freeze-gate.py` = 0 and 0; `claims.json` `instruments` pins only
  `count-c1.py` and `freeze-gate.py`; `corpus/lessons/round-24.md:58` (M24-3) states the requirement the receipt
  satisfies ("`match:true` for each, and a wrong digest exits 1"), and `neg-control.jsonl` shows `match:false` with
  exit 1. The repro artefacts are remediation for the routed defect "MANIFEST rounds[424]", not a claim instrument.

## Residual risk and verification gaps

- The 1.28 GB godot archive was **not** downloaded in full; the member digest was proven by ranged extraction and
  the archive digest by GitHub's published asset digest, not by a full re-hash of the transferred bytes.
- The sigrok AppImage's *publisher* authenticity is out of scope: the local copy at `~/.local/opt` and the two
  corpus records agree on the digest, but the manifest records no signature check for it (contrast
  `tool-pins.json` `signature_check` for wireshark).
- All fetcher behaviour findings come from a copy of `fetch-inputs.py` under `/fast/scratch`, not from the lane file
  (the lane file was never executed in place); the copy was byte-compared to the committed script before use.
- No LSP server is mounted for this lane, so "caller"/"definition" relationships were established by literal text
  search only; they are not semantic proofs.
- Exit-code semantics were checked against a local HTTP server only; no upstream server was asked to fail.

## Recommended L1 action

1. **Do not change the R24-C1 / R24-C2 verdicts on the basis of this review** — neither gate reads `repro/`, and no
   claim names the fetcher. Round 24 remains *not verified* by this seat.
2. Fix `fetch-inputs.py` before it is re-published as the reproduction recipe: (a) containment-check the `.member`
   output path and refuse symlinked targets (F2); (b) unlink partial downloads on the fetch-error path (F5);
   (c) catch `KeyError`/`BadZipFile`/`OSError` per input and exit 2 with a JSON record (F6); (d) add
   `--max-time`/`--max-filesize` (F8); (e) record `expected_sha256`/`expected_bytes` and pin the mixed-case exit
   precedence (F9); (f) fix the `--only` duplicate-id test (F10).
3. Repair the evidence: correct the sigrok `used_by` citations to the digest-bearing files (F1); add
   `inputs_sha256`/`fetch_inputs_sha256`/`curl_version` to `receipt.json` and retain the negative-control manifest
   in-repo (F3); make `run-1.jsonl` valid JSONL by dropping the trailing `exit=0` line (F4); state the member-vs-
   archive distinction and pin the archive digest for the godot entry (F7); correct the sigrok re-extraction note to
   the actual `setup-sigrok.py` recipe and its `runtime_already_exists` precondition (F11).
4. If a re-run is performed after the fixes, keep the current positive results in view: all six digests and byte
   counts reproduce (five re-run here, godot verified by ranged member extraction), the upstream F-Droid index and
   GitHub release metadata agree with the manifest, and the `in_git` list and the three committed captures are
   genuine.

---

# Supplement — recheck of the hardened fetcher (post-fix)

Reviewer: `KagiR27-2.ResRepro-2`. Triggered by `KagiR27-2` (2026-10-21, "Fetcher/inputs.json fixed in place").
Scope: re-run my F2 / F5 / F6 reproductions against the **current** `.ufo/waves/round-24/repro/fetch-inputs.py`
(sha256 `0d49d7c7a8fd6a5cf3effa53dbf4bad8e834a2bb1b4092e7466389ba3fcfca0e`, 119 lines, working tree `M`) and the
current `inputs.json` (sha256 `5356bab0…`, `M`). New scratch: `/fast/scratch/hyaku/kaidoku-r24/ResRepro2` (no `/tmp`).
No lane file was edited by this seat; the only write is this supplement. No install performed. The lane HEAD is still
`69e82c48be5614ce96f7c1c32445fe61c4870630`; the fixes are **uncommitted working-tree changes** (`git status`:
`M fetch-inputs.py`, `M inputs.json`, `?? neg-manifest.json`).

## Verdict of the recheck

**Original findings F1–F11: closed in the working tree, with two residual defects (R1, R2) and two evidence gaps
(R3, R4) that remain.** The hardened script no longer overwrites or deletes anything outside `DEST`, cleans up partial
downloads, reports usage/extraction errors as JSON with exit 2, bounds the transfer, pins the archive digest, and
records expected digests. The round is still **not verified** by this seat: the fixed script is not committed, the
replacement run (`run-2`) exists only in scratch, and the receipt still describes the *old* script and the old
`run-1.jsonl`.

## Re-test results (each command exit and observation)

| original finding | reproduction | new exit | new observation |
|---|---|---|---|
| F2 member symlink | `dest/m.member` → symlink to outside `precious.txt`, zip member `m/x.apk` | **2** | `{"error": "ValueError: symlink_refused: m.member"}`; **outside file intact** (`b'ORIGINAL\n'`), dest residue `['m.member']` (the symlink itself, untouched). The old overwrite+delete is gone. |
| F2 download symlink | `dest/x.download` → symlink to outside dir | **2** | `{"error": "ValueError: symlink_refused: x.download"}`; nothing written outside. |
| F2 escape via id | id `sub/x`, `sub/../x`, `/etc/passwd` | 2 / 1 / 2 | `path_escape: sub/x.download`, `path_escape: /etc/passwd.download`; `sub/../x` normalises inside `DEST` and proceeds (writes `dest/x.download`, then cleans up) — still contained. |
| F2 symlinked intermediate dir | `dest/sub` → symlink to outside dir, id `sub/x` | **2** | `path_escape: sub/x.download`; outside dir stays empty. |
| F5 partial download | server sends `Content-Length: 1000000` then closes after 1000 B | **2** | `curl_exit 18`; **dest residue `[]`** — the partial file is now removed. (Old: 1000-byte `t1.download` left behind.) |
| F5 truncation without `Content-Length` | server sends 100 B, no length header | **1** | `curl_exit 0`, `bytes 100` vs `expected_bytes 5000`, `match:false`; residue `[]`. No truncation can match. |
| F6 missing zip member | member `nope.apk` not in archive | **2** | `{"error": "KeyError: \"There is no item named 'nope.apk' in the archive\""}`, JSON record, no traceback. |
| F6 corrupt archive | `not a zip` bytes | **2** | `{"error": "BadZipFile: File is not a zip file"}`, JSON record, no traceback. |
| F9 mismatch | wrong expected digest | **1** | record now carries `expected_sha256`/`expected_bytes` next to the observed `sha256`/`bytes`; `match:false`; exit 1. |
| F9 mixed mismatch + fetch error | one unreachable URL + one wrong digest | **2** | fetch error dominates (documented in the new docstring lines 13-14: "2 if any input could not be fetched/extracted … otherwise 1 if any digest/size mismatched"). Both per-item records are printed, so the mismatch is still visible. |
| F10 duplicate manifest id | two entries with id `dup` | **2** | `{"error": "duplicate manifest id", "exit": 2}` — now rejected up front instead of mis-reported as an unknown id. |
| F10 unknown `--only` | `--only nope` on a clean manifest | **2** | `{"error": "unknown id in --only: nope", "exit": 2}` — correct message. |
| F10 repeated `--only` | `--only a --only a` | **1** | accepted; the input is processed once. |
| F8 transfer bound | 20 MB response (chunked, and with `Content-Length`) vs limit | **2** | `curl: (63) Exceeded the maximum allowed file size`; residue `[]`. The bound holds for chunked responses too. |
| F7 archive pinning | `archive_sha256` correct / zeroed | 0 / **1** | `archive_match: true` → `match:true`, exit 0; zeroed → `archive_match: false`, `match:false`, exit 1. The archive digest is now enforced. |
| — full re-run | the five non-godot inputs with the new script | **0** | 5/5 `match: true`, byte counts and digests identical to `run-1.jsonl`; dest empty afterwards. |

## Residual findings

### R1 — Low/Medium — a *pre-existing regular file* at `DEST/<id>.member` is still destroyed

- **Observation.** `fetch-inputs.py:67-69` resolves the member path, then opens it with `open(subject, 'xb')`. The
  `xb` mode makes the tool **fail** on an existing file (`FileExistsError`) instead of overwriting it — good — but the
  `finally` block (lines 80-84) then unlinks the path it just refused to write.
- **Reproduction.** A regular file `dest/m.member` containing `PRECIOUS PRE-EXISTING DATA`, manifest entry
  `{"id":"m", "member":"m/x.apk"}`: run without `--keep` → exit 2 with
  `{"error": "FileExistsError: [Errno 17] File exists: '…/m.member'"}` and **the pre-existing file is gone**
  (`VICTIM STILL EXISTS? False`, dest residue `[]`). With `--keep` the file survives (exit 2, residue
  `['m.member','m.download']`).
- **Inference.** The tool did not write attacker bytes over the victim, but it did delete a file it never created.
  The `written` list is appended before the write is attempted (line 68), so the cleanup loop treats a refused target
  as its own. The same shape applies to `DEST/<id>.download` (a pre-existing regular file there is likewise unlinked
  after a run — verified: the stale `x.download` disappeared).
- **Recommendation.** Only unlink paths this invocation actually created (track creation success separately from
  "path chosen"), or unlink only when the file's inode/mtime is the one this run wrote.

### R2 — Low — a manifest entry missing `sha256`/`bytes` still crashes with a traceback and exit 1

- **Observation.** `fetch-inputs.py:47-48` reads `item['sha256']` and `item['bytes']` **before** the `try:` on
  line 50, so a malformed entry raises an uncaught `KeyError`.
- **Reproduction.** `{"id":"n","url":"file://…/small.bin","sha256":"0"*64}` (no `bytes`) → exit **1** with an empty
  stdout and `KeyError: 'bytes'` on stderr; likewise a missing `sha256` → `KeyError: 'sha256'`, exit 1.
- **Inference.** The new docstring says "Exit: 2 if any input could not be fetched/extracted or on usage error";
  a usage error here exits 1, which the same docstring reserves for a digest mismatch. The `except` clause on
  line 77 covers `KeyError` for *extraction* keys but not for the manifest keys read on line 47-48.
- **Recommendation.** Move the `record = {...}` construction inside the `try`, or validate the manifest's required
  keys in `main()` alongside the duplicate-id check (lines 96-101).

### R3 — Medium (evidence) — the replacement run is not in the lane, and the receipt still describes the old script

- **Observation.** The new run exists only in scratch: `/fast/scratch/hyaku/kaidoku-r24/run-2.jsonl` (6 records,
  all `match:true`, final `{"selected": 6, "matched": 6, "exit": 0}`), `run-2.exit` = `0`, `run2.start` =
  `2026-10-21T17:36:18Z`, plus `neg-2.jsonl` (one `match:false` record, `{"selected": 1, "matched": 0, "exit": 1}`)
  and `neg-2.exit` = `1`. **No `run-2.jsonl` / `neg-2.jsonl` exists anywhere in the repo**
  (`find .ufo corpus -name 'run-2.jsonl' -o -name 'neg-2.jsonl'` → empty).
- **Observation.** `receipt.json` is unchanged (sha256 `fe61234d…`, mtime 13:58:52, i.e. the pre-fix run): its `run`
  field still points at `run-1.jsonl`, its `argv` still names the old invocation, its `negative_control.argv` still
  points at the **scratch** path `/fast/scratch/kaidoku-r24/neg-manifest.json` (now also retained in-repo as
  `.ufo/waves/round-24/repro/neg-manifest.json`, sha256 `1d61ac75…`, but *untracked* — `git status` shows `??`), and
  it still carries **no `inputs_sha256` / `fetch_inputs_sha256` / `curl_version`** (the only `sha256` strings in it
  are prose in `result` and `manifest_change`).
- **Observation.** `run-1.jsonl` is unchanged (sha256 `f0410fea…`) and still carries the bare `exit=0` trailer
  (line 8). `corpus/lessons/round-24.md:145-146` states "Run1 retains its historical non-JSON `exit=0` trailer; run2
  is valid JSONL. Manifest/script digests and the negative manifest are retained with run2." — but at the time of
  this recheck, run2 and the digests are **not in the lane**, so that sentence is currently a claim about scratch
  state, not about retained evidence.
- **Inference.** The lesson text and the working tree disagree about what is retained. A reader of the committed
  lane sees only the old script, the old run and the old receipt; the hardened behaviour and its 6/6 evidence exist
  only outside the repository.
- **Recommendation.** Commit `fetch-inputs.py`, `inputs.json`, `neg-manifest.json`, `run-2.jsonl`, `neg-2.jsonl` and a
  `receipt-2.json` (with `inputs_sha256`, `fetch_inputs_sha256`, `curl_version`, and the new exit-code contract), and
  make `corpus/lessons/round-24.md:145-146` point at the committed paths.

### R4 — Low (evidence) — `SKILL.md:777` still describes the old contract

- **Observation.** The registry row reads: "`0 all match, 1 mismatch, 2 fetch error` … official URLs, sha256, sizes;
  deletes bytes unless `--keep`". The hardened script now also (a) supports optional `member` / `archive_sha256` /
  `archive_bytes`, (b) refuses symlinked or escaping targets, (c) reports `expected_sha256`/`expected_bytes` per
  record, (d) prefers exit 2 for usage/extraction errors even when a digest also mismatched, and (e) refuses a
  duplicate manifest id. The row is a one-line summary, so this is a staleness nit rather than a wrong instruction.
- **Recommendation.** Extend the row to mention the member/archive fields and the containment refusal, matching the
  new docstring.

## Verification gaps of this recheck

- The fixes are **uncommitted**; a checkout of HEAD `69e82c48` still contains the vulnerable script. I re-tested the
  working-tree bytes, which is what the reviewer asked for, but the durable state is not yet fixed.
- The godot entry (1.28 GB) was **not** re-downloaded by me; its `archive_sha256`/`archive_bytes` pinning is
  verified by the reviewer's own `run-2.jsonl` record (`archive_match: true`) and by my earlier ranged extraction
  (member sha256 `6d1bb2cf…` = manifest = r22 envelope subject) plus GitHub's published asset digest
  `f298490b…` = `archive_bytes 1281349702`.
- No LSP server is mounted for this lane; all "caller/definition" statements rest on literal text search.
- R1's blast radius depends on the destination directory's contents; a shared or reused `--dest` is where a
  pre-existing file is most likely to be clobbered.

## Recommended L1 action (recheck)

1. Fix **R1** (only unlink files this invocation created) and **R2** (validate manifest keys before use, exit 2).
2. Retain the run in the lane (R3): commit `run-2.jsonl`, `neg-2.jsonl`, `neg-manifest.json` and a
   `receipt-2.json` that pins `inputs_sha256`, `fetch_inputs_sha256` and `curl_version`; update
   `corpus/lessons/round-24.md:145-146` to name the committed paths.
3. Refresh the `SKILL.md:777` row (R4).
4. Nothing here changes the R24-C1 / R24-C2 dispositions: neither gate reads `repro/`, and no claim names the
   fetcher. Round 24 remains **not verified** by this seat.

---

# Supplement 2 — recheck of the R1/R2 fix (post-fix, script sha256 `3c98e4db…`)

Reviewer: `KagiR27-2.ResRepro-2`. Triggered by `KagiR27-2` ("R1/R2 fixed: contained() refuses existing paths,
.download reserved xb before adding to written, .member added only after successful xb, required fields validated
main"). Scope, as instructed: **only** the regular-file preservation tests (R1-A `.member`, R1-B `.download`) and the
missing-`sha256`/missing-`bytes` tests (R2), plus a regression sweep of the previously closed findings so the fix did
not reopen them. Script under test: `.ufo/waves/round-24/repro/fetch-inputs.py`, sha256
`3c98e4db4d0f27f51d55ae2ab149153a163bf578a330fe106c8c361aa5f424d8` (131 lines, working tree `M`; my scratch copy is
byte-identical to the lane file). Scratch: `/fast/scratch/hyaku/kaidoku-r24/ResRepro2`. No lane file edited by this
seat; no install; no download >100 MB.

## Verdict of the recheck

**R1 and R2 are closed.** Both reproductions now behave as intended, and no previously closed finding regressed.
Two **new, low-severity** observations appear (N1, N2 below), both of which are *stricter-than-before* behaviour rather
than a safety hole. The evidence gaps R3/R4 from supplement 1 are **unchanged**: the fixes are still uncommitted,
`run-2`/`neg-2` are still only in scratch, and `receipt.json` still describes the pre-fix script. Round 24 remains
**not verified** by this seat.

## R1 / R2 re-test results

| test | setup | exit | observation |
|---|---|---|---|
| **R1-A** pre-existing regular `.member` | `dest/m.member` = `PRECIOUS PRE-EXISTING DATA`; manifest `{id:"m", member:"m/x.apk"}` | **2** | `{"error": "ValueError: existing_path_refused: m.member"}`; **VICTIM EXISTS? True**, content still `b'PRECIOUS PRE-EXISTING DATA'`; dest `['m.member']` (the victim's own file, untouched). The old delete-the-victim behaviour is gone. |
| **R1-B** pre-existing regular `.download` | `dest/x.download` = `PRECIOUS DOWNLOAD FILE` | **2** | `{"error": "ValueError: existing_path_refused: x.download"}`; **VICTIM EXISTS? True**, content intact; dest `['x.download']`. Refused *before* the download (no network fetch). |
| **R2** missing `sha256` | `{id, url, bytes}` | **2** | `{"error": "invalid input manifest fields", "exit": 2}` on stdout, **no traceback**, no stderr. |
| **R2** missing `bytes` | `{id, url, sha256}` | **2** | same JSON error, exit 2, no traceback. |

## Extra manifest-validation cases (same code path, all now clean)

| manifest defect | exit | stdout |
|---|---|---|
| `sha256` of length 3 | 2 | `{"error": "invalid input manifest fields", "exit": 2}` |
| `sha256` = 64 non-hex chars | 2 | same |
| `bytes` as the string `"5"` | 2 | same |
| `bytes` as the boolean `true` | 2 | same (`type(...) is not int` correctly rejects `bool`) |
| empty `id` | 2 | same |
| missing `url` | 2 | same |

All six produce a single JSON error line and exit 2 — no Python traceback, and no `KeyError` can escape from
`fetch_one` any more (the manifest fields are validated in `main()` at `fetch-inputs.py:103-110` before selection).

## Regression sweep (previously closed findings re-confirmed on sha256 `3c98e4db…`)

| finding | reproduction | exit | observation |
|---|---|---|---|
| F2 symlink `.download` | `dest/h.download` → symlink to an outside file | 2 | `symlink_refused: h.download`; outside file intact; dest `['h.download']` |
| F2 symlink `.member` | `dest/m.member` → symlink to an outside file | 2 | `symlink_refused: m.member`; outside file intact |
| F5 partial download | `Content-Length: 1000000`, close after 1000 B | 2 | `curl_exit 18`; dest residue `[]` |
| F6 missing zip member | member absent from the archive | 2 | JSON `{"error": "KeyError: …"}`; dest residue `[]` |
| F9 digest mismatch | wrong expected digest | 1 | `match:false`; dest residue `[]` |
| — happy path, fresh dest | one small local file, correct digest | **0** | `match:true`; dest empty afterwards |
| — happy path, rerun into the same clean dest | — | **0** | `match:true`; dest empty (idempotent) |
| — five real inputs | saber-1360103 / 1330203 / 1340303 / sigrok AppImage / wireshark source | **0** | 5/5 `match:true`, byte counts 42 305 081 / 41 263 437 / 42 571 868 / 49 558 848 / 56 477 044; dest empty |
| — record equivalence vs the reviewer's `run-2.jsonl` | per-input record dicts | — | the five records I just produced are **byte-for-byte identical dicts** to the corresponding `run-2.jsonl` records (same keys, same values), and the summary shape matches (`{"selected": N, "matched": N, "exit": 0}`) |

The last row is the direct answer to the reviewer's stated concern: the record format produced by the *current*
script is identical to the one in the retained `run-2.jsonl`, so `run-2` remains a valid execution record of the
`0d49d7c7` script even though the script has since changed to `3c98e4db…` — provided the receipt says so explicitly.

## New observations (no safety hole; both are stricter behaviour worth documenting)

### N1 — Low — a `--keep` run makes the destination non-reusable, and the refusal is silent about the cause

- **Observation.** Because `contained()` now refuses any pre-existing path (`:43-44`) and the `.download` file is
  reserved with `open(target,'xb')` before the transfer (`:53-56`), a `--keep` run leaves `DEST/<id>.download` behind
  and the **next** run into the same `DEST` fails with `existing_path_refused: h.download` (exit 2).
  Reproduced: `--keep` run → dest `['h.download']`; immediate rerun → exit 2, `existing_path_refused`, dest unchanged.
- **Inference.** This is the intended "do not clobber" posture and it protects the previous run's bytes, which is the
  right trade for a forensic probe. But the error names the file, not the remedy, and a user who reuses one scratch
  directory will see a hard failure on the second run. It is documented nowhere in the docstring, which still says only
  "deletes the bytes (also partial ones) unless `--keep`".
- **Recommendation.** One line in the docstring / `SKILL.md:777`: "each run needs a fresh `--dest` (or a `--keep` dest
  must be emptied first), because existing `*.download`/`*.member` paths are refused rather than overwritten".

### N2 — Low — `contained()` refuses on `raw.exists()`, so a *dangling* symlink and a broken symlink are handled
differently from a live one, and the refusal happens before any network access

- **Observation.** `contained()` checks `raw.is_symlink()` first (`:38-39`), then `raw.exists()` (`:43-44`). A dangling
  symlink is caught by the first test (`symlink_refused`); a live symlink likewise. A **regular** file is caught by the
  second test (`existing_path_refused`). In every case the refusal happens *before* `curl` is invoked — verified for
  R1-B: the record shows no `curl_exit` key at all, i.e. no network request was made.
- **Inference.** This is correct and desirable (no wasted transfer, no clobbering). Recording it here only so the
  behaviour is not mistaken for a bug later: the two distinct error strings (`symlink_refused` vs
  `existing_path_refused`) are informative, and a caller can tell a hostile destination from a busy one.

## Residual risk and verification gaps (unchanged from supplement 1, R3/R4)

- **R3 (Medium, evidence) — still open.** `run-2.jsonl` (sha256 `cfddbc31…`) and `neg-2.jsonl`
  (sha256 `7b5e1247…`) exist only in `/fast/scratch/hyaku/kaidoku-r24/`; `find .ufo/waves/round-24 -name 'run-2*' -o
  -name 'neg-2*' -o -name 'receipt-2*'` finds nothing in the repo. `receipt.json` is unchanged (sha256 `fe61234d…`,
  mtime 13:58:52) and still points at `run-1.jsonl` and at the scratch neg-manifest path, and still has no
  `inputs_sha256` / `fetch_inputs_sha256` / `curl_version`. `neg-manifest.json` is in the repo but untracked
  (`git status`: `??`). The working tree is at `fetch-inputs.py` = `3c98e4db…`, which is **not** the script that
  produced `run-2` (`0d49d7c7…`).
- **R4 (Low, evidence) — still open.** `SKILL.md:777` still carries the pre-hardening one-line contract.
- The godot entry (1.28 GB) was not re-downloaded by me; its archive pinning rests on the reviewer's own
  `run-2.jsonl` (`archive_match: true`) and on my earlier ranged member extraction (member sha256 `6d1bb2cf…` = manifest
  = r22 envelope subject) plus GitHub's published asset digest `f298490b…` / `1281349702`.
- No LSP server is mounted for this lane; "caller/definition" statements rest on literal text search.

## Recommended L1 action (recheck)

1. **R1/R2 need no further work** — both are closed and the previously closed findings did not regress.
2. Close **R3** as planned: commit `fetch-inputs.py` (`3c98e4db…`), `inputs.json`, `neg-manifest.json`,
   `run-2.jsonl`, `neg-2.jsonl`, and a `receipt-2.json` that states which script produced `run-2`
   (`fetch_inputs_sha256: 0d49d7c7…`), plus the digests of the manifest and the `curl` version. The reviewer's plan to
   add a **separate final-script control receipt** is the right shape: `run-2` stays bound to `0d49d7c7…` and the
   control receipt binds the *current* script (`3c98e4db…`). My re-run above supplies exactly the second half — the
   five per-input records produced by `3c98e4db…` are identical to the `run-2.jsonl` records, exit 0 — so that
   control receipt can honestly say "the final script reproduces the same five records".
3. Add the N1 note (fresh `--dest` per run) to the docstring and `SKILL.md:777`, and refresh that row per R4.
4. R24-C1 / R24-C2 dispositions are unaffected (neither gate reads `repro/`); round 24 remains **not verified** by
   this seat.
