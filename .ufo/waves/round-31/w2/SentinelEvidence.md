# Round 31 W2 — committed evidence hygiene

**Scope:** C1/C2 committed `.json` envelopes and `.stderr` files; counter/oracle direct file effects; frozen carrier/mutant hashes. No counter or REA command was run, and no carrier or mutant was written.

## Severity-ranked findings

### Medium — C2 `--build` writes outside `--write-evidence` using revision-supplied paths

**Observation:** `build(root, rev)` parses `PRED` from the selected revision, assigns `kind, path = r["build"], r["path"]`, then creates directories and writes/copies files or symlinks at `path` (including a 268,435,457-byte sparse-file branch). The CLI invokes this independently via `--build`; it is not guarded by `--write-evidence`. There is no destination-root/ID allowlist. The existing-parent check skips rows whose parent already exists; the demonstrated consequence is therefore creation under a chosen writable path whose parent is absent, not a claim that it overwrites an existing file.

**Exploit path [INFERENCE]:** An operator runs the counter's `--build` against a checkout/revision with an untrusted `predictions.tsv` row whose build kind writes and whose path points outside the fixture tree. The builder can create the missing parent and artifact there. This was not exercised.

**Impact:** A build action can create unexpected files/directories outside the evidence directory and outside `/fast/scratch/.../mutants`; repeated rows can consume storage. The current frozen rows name the expected mutant paths, and this audit did not invoke the builder.

**Smallest remediation:** Build destinations from an allowlist of fixed IDs beneath the mutants root; do not use the prediction's `path` as a filesystem destination. Reject any row that does not map to that fixed destination before creating anything.

**Evidence:** Read-only source inspection of `tools/round-31/c2-sqlite-refusals.py:78-131,400-414` returned, among other lines: `kind, path = r["build"], r["path"]`; `os.makedirs(d)`; `open(path, "wb").write(...)`; `shutil.copyfile(base, path)`; `ap.add_argument("--build", action="store_true")`; `if a.build: sys.exit(build(a.root, a.rev))`. Source-read tool completed successfully (no spawned process / numeric exit code applies). The same source shows C1 writes at lines 187-196 and C2 measurement writes at lines 349-358 only inside `if write:`; `sqlite_oracle.py:96-97,154-159,162-219` opens inputs for reading and connects with `mode=ro&immutable=1`. **Unknown:** the counters also spawn `npx`/REA; indirect npm-cache or REA temp effects were not exercised or established by this source-only audit.

### Low — committed outputs expose fixed scratch paths and a bounded row sample

**Observation:** The envelopes contain absolute paths rooted at `/fast/scratch/hyaku/kaidoku-r31/carriers/` and `/fast/scratch/hyaku/kaidoku-r31/mutants/` in subject/parameter/artifact/location fields and refusal messages. They do not show a `/home/<user>` path. `hyaku` is a path component; the evidence does not establish that it is a login name. Five PROJ envelopes also include schema DDL containing public `https://cdn.proj.org/%` and `https://cdn.proj.org/` strings. The C1 reports otherwise disclose schema DDL and metadata, not row data. C2 `q-ok-rows.json` includes three Album rows (IDs 1–3): “For Those About To Rock We Salute You,” “Balls to the Wall,” and “Restless and Wild,” with their ArtistIds and text-byte hex. This is the explicitly selected Chinook fixture sample, not evidence of private data.

**Impact:** Readers learn the host's scratch path layout and receive the selected fixture sample. No credentials or personal host-home path were found; the row sample is from the test database.

**Smallest remediation:** If these artifacts will be shared outside the lane and host paths are not intended disclosure, normalize/redact filesystem paths at evidence serialization and compare their normalized form. If selected rows are not intended in future evidence, use a metadata-only acceptance request; the frozen R31 predicate currently requires the q-ok-rows result.

**Evidence:** Scan command `timeout 300 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/SentinelEvidence/scan_envelopes.py` (stdout saved to `envelope-scan.txt`), UTC **2026-10-23T04:37:12Z**, exit **0**. Exact excerpts: `files=70 envelopes=35 stderr=35`; `ENVELOPE envelopes/proj-371.json bytes=301670 ...`; `LARGE_ENVELOPES=[]`. Thus all 35 parsed JSON envelopes are below 1 MiB; largest is 301,670 bytes. The scan found no home/tmp path, environment-variable, or secret-pattern match; its only output-field matches are captured stdout/stderr strings that are empty. URL extraction command at **2026-10-23T04:35:11Z**, exit **0**, returned `URL file=proj-371.json urls=('https://cdn.proj.org/%', 'https://cdn.proj.org/')` (same for the other four PROJ versions). The disclosure detail command at **2026-10-23T04:33:45Z**, exit **0**, emitted the three row values above and eight `CAPTURED_OUTPUT` records, each with `stdout=""`, `stderr=""`, `truncated=false`.

### Informational — frozen SHA pins cover all listed objects, not every structural fixture entry

**Observation:** All 12 carrier hashes, 9 mutant database hashes, and 6 sibling hashes declared by `carriers.tsv` and `claims.json` match the current files/links. The mutant inventory also includes structural entries without a SHA pin: `m-db-symlink/db.sqlite` (symlink to the pinned Chinook carrier), `m-directory/db.sqlite` (directory), and `m-enotdir/file` (16-byte file); `m-missing/db.sqlite` is absent. The unpinned `m-enotdir/file` currently has SHA-256 `2fa094a71c4db3487671e0e47c06e35146c20603ae81fd2a7b37b60066d4585d`, equal to the hash of the builder's literal `not a directory\n` payload. No mismatch or unexpected inventory entry was observed. The SHA manifest alone cannot prove byte-for-byte history for the unpinned structural entries; their expected shape is instead checked by the C2 counter's state predicates.

**Impact:** No current alteration is indicated, but a blanket “every item under mutants is SHA-pinned” claim would be too strong.

**Smallest remediation:** Keep the current state checks and add an explicit frozen manifest for structural entries (file hash, symlink target, directory/absence state), or scope integrity claims to the objects actually hash-pinned.

**Evidence:** Pin/inventory command `timeout 300 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/SentinelEvidence/pin_scan.py` (stdout saved to `pin-scan.txt`), UTC **2026-10-23T04:35:41Z**, exit **0**: `carrier_pins=12 mutant_main_pins=9 mutant_sibling_pins=6`; all listed rows showed `match=1`; final `PIN_RESULT=PASS mismatches=0`. Inventory excerpt: `ENTRY mutants/m-enotdir/file file bytes=16 sha256=2fa094...`; `ENTRY mutants/m-db-symlink/db.sqlite symlink:/fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite`; `ENTRY mutants/m-directory/db.sqlite directory`. The expected-literal hash check at **2026-10-23T04:38:02Z**, exit **0**, printed the same `2fa094...` digest.

## Hygiene summary

- All 35 `.stderr` files are empty (0 bytes); scan output shows the empty SHA-256 for each. No non-benign stderr content exists to disclose.
- Eight envelopes include `captured_output`; every stdout/stderr value is empty and `truncated` is false.
- The envelope scan identified no environment-variable values, credential/token patterns, home paths, or ephemeral `/tmp`/`TMPDIR` names. It does disclose the fixed `/fast/scratch/hyaku/...` carrier/mutant paths described above.
- All frozen carrier/mutant hashes checked matched. No carrier, mutant, or lane file other than this report was modified by this audit. No tools were installed.

## Scratch artifacts

All audit scripts and raw outputs are under `/fast/scratch/hyaku/kaidoku-r31/seats/w2/SentinelEvidence/`; SHA-256 values below were produced by `sha256sum` at **2026-10-23T04:38:09Z**, exit **0**.

- `scan_envelopes.py` — `dd882d81e942945dbfc51e4130ebea8a926f902be66c6c1dd5669b78f19a8f4c`
- `envelope-scan.txt` — `484c82cdcbd8b578031666072efccd5fd9af2f55c7f062e387f46d6dffb60f20`
- `pin_scan.py` — `33b681f5ba90c27a5e12f3305f55a104faa5535959a70b24f6f0a6ef050d64c1`
- `pin-scan.txt` — `16eb0db35743758ca0d473750c298f03383f830a306ed563def94bbb1d3434b1`
- `disclosure_details.py` — `5e193ac75c60b639193b1fea4a022181056ee436c49fcc57903f34fe71abbaee`
- `disclosure-details.txt` — `5b55f4a9a4a16c890fbf627a45024beb3358a1eeaa3b32e5856da98bfb105837`
- `extract_urls.py` — `86b2d5e8c44d2b38e4c26f0585fdf620a3f264079d96ecfb746f669cb1bb2fbf`
- `extracted-urls.txt` — `87e09b2546c55b78ce2411758c71492570432b412239f79f28d037aaa358af3b`
