# C1SentinelFetch — round 50 wave 1: custody and security review of the vendor-carrier path

Lane `main`, base `7c678ae6d97aedb969fd253b52b3d2882ef1e186` (HEAD at check time). Run 2026-10-28, UTC 23:3x.
Scope: `tools/round-41/fetch-vendor.py`, `tools/round-41/c1-run.sh`, `tools/round-49/c1-run.sh`, `tools/round-49/c1-run.py`, the round-50 draft plan (`draft/plans/round-50-claims.md`, tag 9B2A), the lane `.gitignore`, and the lane's round-45/49 receipts for F1 (`W2Sentinel.md`). Receipts: `.ufo/waves/round-50/w1/C1SentinelFetch/` (`commands.txt`, `repro-custody.py`, `repro-custody.out`, `repro-custody.err`).

## Verdict

**NOT CLEAN for the port inputs. Do not freeze the round-49 runner or the round-41 fetch path unchanged.**

Four defects must be fixed in the port before the freeze (S1, S4, S5, S6), one wrapper defect must be fixed (S7), and two landed-record credential findings need an L1 decision (S2, S3). Everything else checked is clean or low.

1. **S1 (High):** the round-49 runner copies REA's whole published tree into the evidence directory. With the round-50 carriers that is AVM rootfs file contents, which the licence forbids committing, and nothing ignores or rejects them. Reproduced.
2. **S2 (High, credential class, landed at HEAD):** `.ufo/waves/round-45/w2/R45W2S138Top/receipts/f1.hdr:15-16` still carries unredacted GitHub session cookie values. The round-49 sentinel did not see it (it scanned only the round-49 diff).
3. **S3 (Medium):** round-49 F1 is redacted at HEAD, but the unredacted blob is still reachable from six commits. History rewrite or rotation is an operator decision.
4. **S4/S5 (Medium):** the fetch path accepts any origin, follows redirects off AVM, accepts `file://`, reads without a size cap, and writes vendor bytes to any caller-named directory, including the lane. Reproduced for redirect and `file://`.
5. **S6 (Medium):** the runner's timeout kills only the direct child. A grandchild (the REA → unblob → sasquatch chain) survives and keeps writing after the run is reported and its scratch deleted. Reproduced.
6. **S7 (Medium-low):** the round-41 wrapper `c1-run.sh` deletes a caller-supplied `SCRATCH` on exit when the path only contains a `/kaidoku-r41/` segment. Reproduced (a user file was deleted).

Checked and clean: TLS verification (on, with a self-signed-origin rejection repro), tar member-name handling (in-memory, no traversal), carrier-id traversal (`[a-z0-9]{2,8}` guard), extractor handling of `..` member names (`sasquatch` LE and `unsquashfs` both refuse), fetch selftest (16/16), and no live cookie values in the round-50 tree.

**Lane `.gitignore` answer:** it contains only `__pycache__/` and `*.pyc`. A copied `.image`, `filesystem.image`, `.bin`, `.part` or `firmware.bin_extract/` file is **not** ignored and **would be staged and committed** by `git add -A` (reproduced). No nested `.gitignore` covers `corpus/evidence` or `tools/`.

## Findings table

Command notation: `L` = lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; `S` = `/fast/scratch/hyaku/kaidoku-r50/C1SentinelFetch`; `A` = `L/.ufo/waves/round-50/w1/C1SentinelFetch`. All repros ran in scratch against a clone (`git clone --shared` checked out at 7c678ae); none wrote into `L`. Single repro: `python3 -I -B A/repro-custody.py S` → exit 0, stdout sha256 `c23a1a2372054dbe83120943bcb69fbe573fd0abfb86b4b7ba254db414560928`, UTC 2026-10-28T23:39:11Z. Its script sha256 is `aab9ab3055447b5d2a9d1710f4bfd465d1a4947c2efa926ea00cbe30edf6b604`.

| ID | Sev | Location (file:line) | Finding | Repro (command → exit) and evidence | Fix (section) |
|---|---|---|---|---|---|
| S1 | High | `tools/round-49/c1-run.py:598` `copy_tree_verbatim(rea_outdir, outdir)`; `:436` `copytree(symlinks=True)`; `:608` snapshot of `outdir`; `:346-347` scratch default | The REA-published tree is copied into `corpus/evidence/<round>/c1/<id>/`. Vendor file bytes would be committed. | `python3 -I -B A/repro-custody.py S` → `CHECK C1-COPY VIOLATION` (file and symlink copied into evidence); `CHECK C1-GITIGNORE VIOLATION` (`git add --dry-run -A` lists 2 `firmware.bin_extract/` paths, exit 0). `git check-ignore --no-index` on the probe names → exit 1 (none ignored). | §S1 |
| S2 | High (credential class; impact low, `logged_in=no`) | `.ufo/waves/round-45/w2/R45W2S138Top/receipts/f1.hdr:15` `_gh_sess` (value 352 chars), `:16` `_octo` (26 chars), `:17` `logged_in=no`. Blob `ba6b0d6ec4d791ced391a08523bfd2e66ddbb2b6`, sha256 `5b8427796c8b47b121580c776adec2a6017499e0dff93cf30fa1427deae7daf1`. Introduced by `96fafefd` / landed `ef3edf4b`. | Unredacted session cookie values are committed at HEAD. The round-49 sentinel (`W2Sentinel.md`) scanned only the round-49 diff and missed this file. | `git show 7c678ae:.ufo/waves/round-45/w2/R45W2S138Top/receipts/f1.hdr \| sed -n '15,17p' \| cut -d= -f1` → exit 0, names only (values withheld in this report). Length check by the same file, value length withheld. | §S2 (L1 decision) |
| S3 | Medium | round-49 F1 (`.ufo/waves/round-49/w1/C1CarrierPins/receipts/tree.hdr`, `…/C1S138Reopen/receipts/top.hdr`) | HEAD now holds `[redacted by L1 ...]` placeholders (`tree.hdr` blob `f89013cd543de095fe50f8670cdbbce1488d1d87`, sha256 `2d5ccfc6b8c12f5cff6710e14d5309d143183d161b7e9eba2ca9b157d2b5269b`). The unredacted blob `5f8478b4fc25c8b1c5718eeafba2591f62010a1f` (sha256 `bee3ed2a38e68e970e3d4b97851ed5f94ae1b7c86ce217aba48e02ed484b956d`; `_gh_sess` 348, `_octo` 27 chars) is still reachable. | `git log --all --oneline --find-object=5f8478b4fc25c8b1c5718eeafba2591f62010a1f` → 6 commits (`14936cb9`, `5855962d`, `3533793c`, `7017c450`, `b1fa2ae3`, `95016095`). | §S3 (operator decision) |
| S4 | Medium | `tools/round-41/fetch-vendor.py:103` `urllib.request.urlopen(url, timeout=300)`; `:95-111` `fetch`; `:105` unbounded `r.read()` | No host, scheme or size constraint. Redirects are followed to any origin; `file://` is accepted. The sha256 gate (`:188`, `:235`) keeps integrity, not containment. | `python3 -I -B A/repro-custody.py S` → `CHECK C1-REDIRECT VIOLATION` (302 to a second 127.0.0.1 origin followed; 2600 bytes returned and accepted by `fetch`), `CHECK C1-FILE-SCHEME VIOLATION` (`file://` read). | §S4 |
| S5 | Medium | `tools/round-41/fetch-vendor.py:404-405` `--cache`/`--image-cache` (verbatim), `:107-109` writes `<sha>.image` (25–36 MB vendor image), `:240-243` writes `<pin>.bin` (vendor rootfs bytes) | Nothing refuses a cache directory inside the lane. Vendor bytes would be written there and would be committed (S13). By code reading; the write path is the same one the selftest exercises in `TMPDIR`. Not run against `L`. | Code reading. Confirm with `fetch-vendor.py --spec … --cache S/x` (writes), against the lane-clone to see the lane-path case. | §S5 |
| S6 | Medium | `tools/round-49/c1-run.py:572-581` `subprocess.run(..., timeout=timeout)` | On timeout only the direct child is killed. REA's grandchildren (`npx`→`node`→`unblob`→`sasquatch`) survive, keep writing into `run_dir`, and `run_dir` is `rmtree`'d at `:757-758`. The run is recorded as `timed_out` and the scratch deleted while the grandchild runs. | `python3 -I -B A/repro-custody.py S` → `CHECK C1-TIMEOUT VIOLATION`: runner wall 2.6 s for `--timeout 2`, exit 1, `sleep 25` grandchild alive after return. Round-41 shell path (GNU `timeout`, signals the group) → rc 124, no orphan (test below). | §S6 |
| S7 | Medium-low | `tools/round-41/c1-run.sh:120-135` (scratch accepted if the path merely contains `/kaidoku-r41/`); `:140` `trap 'rm -rf -- "$scratch"' EXIT` | A caller-supplied `SCRATCH` is `rm -rf`'d on exit, existing contents included. | `env -i PATH=/usr/bin:/bin bash tools/round-41/c1-run.sh after dummy.bin out S/x/kaidoku-r41/keep` → exit 2 (npx absent; the trap still runs); `keep/precious.txt` DELETED. | §S7 |
| S8 | Low | `tools/round-49/c1-run.py:840-841` `allowed_roots` (the whole scratch base); `:514-528` `clear_outdir` → `shutil.rmtree` at `:525` on `evidence_root/<cid>` (no re-check against allowed roots); `:825`/`:840` hard-code round-49 | `--force` deletes `<base>/<cid>` when the scratch base is set broadly (`/`, `$HOME`). Porting that changes only `DEFAULT_EVIDENCE` makes `writing_committed` false (`:826-827`), which silently bypasses the `--data-run` assertion. The guard refused a round-50 path with exit 2 (`outside …/round-49/c1`), so an unchanged port fails closed. | Config-dependent; by reading. `c1-run.py --evidence-root S/clone/corpus/evidence/round-50/c1 …` → exit 2 (guard refusal, observed). | §S8 |
| S9 | Low | `tools/round-49/c1-run.py:284-289` (`os.path.isabs(val)` accepted; `os.path.join(lane, val)` with `../` accepted) | Fixture resolution has no containment. The sha of an arbitrary local file reaches the manifest on a pin mismatch (`:1005`, `:1011`). No REA run on a mismatch (`:995-1000`, good). | By reading. | §S9 |
| S10 | Low (hygiene; not exploitable) | `tools/round-41/fetch-vendor.py:173-176` (length check only); `:97`, `:108` (`want + '.image'`) | Pins and image hashes are not hex-validated. A non-hex value cannot reach a write: the write at `:240` requires `carrier_sha256 == pin` (`:235`), and `:106-109` writes only when `sha256(b) == want`. | By reading; `fetch-vendor --selftest` 16/16 (exit 0). | §S10 |
| S11 | Low (hygiene) | `tools/round-41/fetch-vendor.py:88` `f'{a.rev}:{CARRIERS}'` into `git show` | `--rev=--output=<path>` reaches git's argv. Test: exit 2, no file written (the derived output path's parent did not exist). Not a practical write primitive. | `fetch-vendor.py --root S/clone --rev=--output=S/argv-inj --cache S/c` → exit 2, no file. | §S11 |
| S12 | Low | `tools/round-41/c2-counter.py:432` and `:1930` (`tempfile.gettempdir()` fallback) | When `HYAKU_SCRATCH` is unset and `TMPDIR` is unset, the C2 counter writes under `/tmp`. The C1 counter default is clean (`c1-counter.py:358-359` → `/fast/scratch/hyaku`). `fetch-vendor.py:263` selftest writes under `/tmp` if `TMPDIR` is unset. `c1-run.py:549` (`TMPDIR=run_dir`) and `c1-run.sh:141` (`TMPDIR=scratch`) are clean. | By reading. | §S12 |
| S13 | Info (lane) | `L/.gitignore` (2 lines; sha256 `862263fa1f46c20f0d1e4dac5ffcc75abd55c08211b2c3864c5f8764b9d87793`); `.git/info/exclude` and `core.excludesfile` empty | Not ignored: `*.image`, `filesystem.image`, `*.bin`, `*.part`, `firmware.bin_extract/`. Would be staged. Precedent: 326 tracked `.bin`/`.sqsh`/`.image`/`.part`/`.squashfs` files under `corpus/`, `tools/`, `plans/` (lane-built), so a bare `*.bin` ignore would hide new fixtures. `.ufo/waves/round-50/` is wholly untracked (417 files at check time; siblings still writing). | `git -C L check-ignore --no-index x.image filesystem.image y.bin z.part` → exit 1. `git -C clone add --dry-run -A corpus/evidence/round-49/c1/repro …` → exit 0, lists the paths. | §S13 |

## Minimal fix text for the port

Each block is the change to the frozen-to-be port; line numbers are the round-49 source.

### §S1 — evidence receives only receipts, never REA's tree (`c1-run.py`, `run_carrier`)

```
-    if rea_outdir != outdir:
-        if os.path.isdir(rea_outdir):
-            try:
-                copy_tree_verbatim(rea_outdir, outdir)
-                copy_note = ('copied verbatim from the REA output root %s'
-                             % rea_outdir)
-            except (OSError, shutil.Error) as e:
-                raise Unevaluable('verbatim copy of the REA tree failed: %s' % e)
-        else:
-            copy_note = 'REA produced no output root at %s' % rea_outdir
+    # REA's published tree stays in scratch: vendor file contents never enter the lane.
+    copy_note = 'not copied: REA output remains in %s' % rea_outdir
 ...
-    tree_entries = snapshot_tree(outdir, skip=set(RECEIPT_FILES))
+    tree_entries = snapshot_tree(rea_outdir)            # metadata only: kind, size, sha256
 ...
+    stray = [n for n in os.listdir(outdir) if n not in RECEIPT_FILES]
+    if stray:
+        raise Unevaluable('evidence dir holds non-receipt entries: %s' % stray)
```
Delete `copy_tree_verbatim` (`:432-436`) and the `shutil.copytree` import use. Set `copied_verbatim: null` and `rewritten: false` in `provenance.json`. Refuse `--rea-outdir-mode evidence` for the data run (REA writing into the evidence dir has the same effect). If the counter needs bytes, it reruns REA from the pin in scratch; it must never read committed trees.

Lane `.gitignore` (L1 decision, not frozen; see §S13).

### §S2 — landed credential at HEAD (L1 decision)

Replace the two values in `.ufo/waves/round-45/w2/R45W2S138Top/receipts/f1.hdr:15-16` with `[redacted by L1: session cookie value]`, as done for the round-49 receipts, in a new commit. Do not edit the old commit. Record in the lesson that the round-45 receipt was outside the round-49 scan. Scan the whole HEAD tree for future rounds, not only the round diff, e.g. `git grep -nP '_gh_sess=[^\]\s;]{6,}' 7c678ae` (use the `-P` form, which excludes the `[redacted` placeholder by construction).

### §S3 — history (operator decision)

Unredacted blob `5f8478b4` is reachable from six commits. Options: rewrite history (removes it everywhere, requires a force-push the operator must authorise), or accept and rotate/expire the sessions (`logged_in=no` at capture, low impact). This seat did no mutating git. Correct `C1S139Reopen.md:36` (claims set-cookie headers were dropped) for the round-49 receipts it covers.

### §S4 — fetch containment (`fetch-vendor.py`)

```
+import urllib.parse
+ALLOWED_HOST = 'download.avm.de'
+MAX_IMAGE = 64 << 20
+class _AvmOnlyRedirect(urllib.request.HTTPRedirectHandler):
+    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
+        u = urllib.parse.urlsplit(newurl)
+        if u.scheme != 'https' or u.hostname != ALLOWED_HOST:
+            raise urllib.error.HTTPError(newurl, code, 'redirect off %s refused' % ALLOWED_HOST, hdrs, fp)
+        return super().redirect_request(req, fp, code, msg, hdrs, newurl)
+_OPENER = urllib.request.build_opener(_AvmOnlyRedirect)
 def fetch(url, image_cache, want):
+    u = urllib.parse.urlsplit(url)
+    if u.scheme != 'https' or u.hostname != ALLOWED_HOST:
+        raise ValueError('url outside %s' % ALLOWED_HOST)
     ...
-    with urllib.request.urlopen(url, timeout=300) as r:
+    with _OPENER.open(url, timeout=300) as r:
         status = getattr(r, 'status', None)
-        b = r.read()
+        b = r.read(MAX_IMAGE + 1)
+    if len(b) > MAX_IMAGE:
+        raise ValueError('image over %d bytes' % MAX_IMAGE)
```
The selftest's `fake()` fetcher bypasses `fetch`, so add two selftest cases: a redirect off-host refused, and a `file://` URL refused. Keep `ssl` untouched (default verification is correct).

### §S5 — refuse lane-resident cache and image-cache (`fetch-vendor.py`, `main`)

```
+def _inside(root, path):
+    r = os.path.realpath(root) + os.sep
+    return os.path.realpath(path).startswith(r)
 ...
+    if a.cache and a.root and _inside(a.root, a.cache):
+        print('refusing: --cache is inside the lane', file=sys.stderr); return 2
+    if a.image_cache and a.root and _inside(a.root, a.image_cache):
+        print('refusing: --image-cache is inside the lane', file=sys.stderr); return 2
```
Also require `--root` (the lane) for any data run, and default both caches to `/fast/scratch/hyaku/kaidoku-r50/…`.

### §S6 — timeout reaps the process group (`c1-run.py`, `run_carrier`)

```
+import signal
 ...
-        proc = subprocess.run(plan['argv'], cwd=run_dir, env=env,
-                              capture_output=True, timeout=timeout)
-        rc = proc.returncode
-        stdout = proc.stdout
-        stderr = proc.stderr
-    except subprocess.TimeoutExpired as e:
-        rc = 124
-        stdout = e.stdout or b''
-        stderr = e.stderr or b''
-        timed_out = True
+        proc = subprocess.Popen(plan['argv'], cwd=run_dir, env=env, stdout=subprocess.PIPE,
+                                stderr=subprocess.PIPE, start_new_session=True)
+        try:
+            stdout, stderr = proc.communicate(timeout=timeout)
+            rc = proc.returncode
+        except subprocess.TimeoutExpired:
+            os.killpg(proc.pid, signal.SIGKILL)
+            stdout, stderr = proc.communicate()
+            rc, timed_out = 124, True
```
Match the round-41 shell (GNU `timeout` signals the process group: verified, rc 124 and no orphan).

### §S7 — the wrapper never deletes what it did not create (`c1-run.sh`)

```
   scratch=$(realpath -m -- "$scratch_arg")
-  case "$scratch/" in
-    */kaidoku-r41/*) ;;
+  [[ ! -e $scratch ]] || err "SCRATCH $scratch must not exist: it is removed on exit"
+  case "$scratch" in
+    "$(realpath -m -- "$scratch_root")"/*) ;;
     *)
 ...
-  mkdir -p "$scratch" || err ...
+  mkdir -- "$scratch" || err "cannot create SCRATCH: $scratch"
```
Port `scratch_root` to `${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kaidoku-r50` and enforce the `output_directory` prefix `/fast/scratch/hyaku/kaidoku-r50/` in the same place.

### §S8 — `--force` and the guard (`c1-run.py`)

Make `allowed_roots = [realpath(committed evidence root), realpath(scratch_root)]` with `scratch_root = base/kaidoku-r50`. Before `shutil.rmtree`, assert `os.path.commonpath([realpath(outdir), realpath(evidence_root)]) == realpath(evidence_root)`. Refuse a scratch base of `/` or `$HOME`. Change `DEFAULT_EVIDENCE` (`:112`), `:825` and `:840` in the same commit.

### §S9 — fixture containment (`c1-run.py`, `resolve_fixture`)

```
-            return os.path.realpath(cand), 'entry field %r' % key
+            real = os.path.realpath(cand)
+            if not (real.startswith(os.path.realpath(os.path.join(lane, 'tools/round-50')) + os.sep)
+                    or real.startswith(os.path.realpath(carrier_cache) + os.sep)):
+                raise Unevaluable('carrier %r fixture outside the frozen carrier dirs' % cid)
+            return real, 'entry field %r' % key
```

### §S10 — validate hex at load (`fetch-vendor.py`, `materialise`)

```
-    pin = (entry.get('sha256') or '').lower()
+    pin = (entry.get('sha256') or '').lower()
+    if not re.fullmatch(r'[0-9a-f]{64}', pin): raise SystemExit(2)
```
Apply the same check to `ext['image_sha256']` before `fetch` (`:182`).

### §S11 — validate rev (`fetch-vendor.py`, `load_spec`)

```
+    if not re.fullmatch(r'[0-9a-f]{7,40}', a.rev or ''):
+        raise SystemExit(2)
```

### §S12 — no `/tmp` fallback (`c2-counter.py:432`, `:1930`)

```
-    base = os.environ.get('HYAKU_SCRATCH') or tempfile.gettempdir()
+    base = os.environ.get('HYAKU_SCRATCH') or '/fast/scratch/hyaku'
```
For the port, the C1 counter default is already correct; the selftest mkdtemp in `fetch-vendor.py:263` should take `dir=` explicitly.

### §S13 — lane `.gitignore` and the freeze gate (L1 decision; `.gitignore` is not in the frozen list)

```
# round-50 vendor-firmware custody: carrier bytes and REA trees never enter the lane
*.image
*.part
filesystem.image
tools/round-50/carriers/
corpus/evidence/round-50/c1/**/firmware.bin_extract/
```
Do not add a bare `*.bin` (326 committed fixtures would stop being visible as new, and new fixtures would be hidden). `.gitignore` does not stop `git add -f`, so the freeze must also gate on the index: the freeze runbook should stage by explicit pathspec and run `git diff --cached --name-only | grep -E '\.(image|part|bin)$|filesystem\.image|firmware\.bin_extract/'` (must be empty) and `git diff --cached --numstat` with no entry above 1 MiB. Never `git add -A` while `.ufo/waves/round-50/` is untracked.

## Checked and clean (evidence)

- **TLS verification on.** `fetch-vendor.py` has no `ssl` reference and uses the default context. A self-signed https origin → `URLError [SSL: CERTIFICATE_VERIFY_FAILED]` (C1-TLS clean). No `CERT_NONE`, `_create_unverified`, `check_hostname`, `verify=False` or `--insecure` in `tools/round-41`, `tools/round-48` or `tools/round-49` (grep). The L1 probe `.ufo/waves/round-50/l1/scan.py` uses the default `urlopen` as well.
- **Tar member names.** `fetch-vendor.py:114-122` is a `tarfile` in-memory dict lookup (`names.get(member)`), with no write from a member name. `sqfs-list.py:778-787` writes only the operator's TSV path. Nested `extract_file` (`sqfs-list.py:719`) returns bytes.
- **Crafted `..` names through extractors.** I built a LE SquashFS with a `../escape-r50.txt` member and an `a/../../escape-r50.txt` member with the lane's own writer. `sasquatch` 4.5.1 (LE) and `unsquashfs` 4.7.5 both report `invalid characters in name` and rc 1, and nothing was written outside the root. This probes the extractors only; no vendor image was used.
- **Carrier ids.** `c1-run.py:240` `[a-z0-9]{2,8}` blocks traversal in `outdir` (`os.path.join(evidence_root, cid)`).
- **Headers in receipts.** No round-41/round-49 code path or L1 probe writes HTTP headers (`fetch-vendor` returns bytes; `scan.py` reads bodies). A python scan of `.ufo/waves/round-50` for cookie literals longer than 4 characters found none (values not printed). Legacy exposures are S2 and S3.
- **`--force` containment, symlink at outdir.** `c1-run.py:524-527` removes a symlink as a link (`os.remove`), not its target. The breadth issue is S8.
- **Scratch and TMPDIR for REA.** `c1-run.py:547-550` sets `TMPDIR=run_dir`, pops `PYTHONPATH`, pins `FIXED_PATH`; `c1-run.sh:141` sets `TMPDIR=scratch`. `c1-run.sh` oracle arm writes only under `$scratch` and `$outdir`.
- **fetch selftest:** `fetch-vendor.py --selftest` → `SELFTEST cases=16 pass=16 fail=0`, exit 0 (`TMPDIR` set to scratch).
- **Round-49 wrapper** `tools/round-49/c1-run.sh`: `exec python3 -I -B`, `FIXED_PATH` pinned, `--data-run`/`KAIDOKU_C1_DATA_RUN` guard present (`c1-run.py:828-837`).
- **Symlink/timeout in the round-41 shell path:** `timeout 2 sh -c 'sleep 25 & sleep 60'` → rc 124, no orphan (GNU timeout signals the group).

## Not run

- No download from `download.avm.de`; no REA or unblob run on any vendor carrier; no counter; no round-50 control; no `--data-run`. No vendor bytes exist in `S` beyond my stand-in payloads, and none were written to `L`.
- Lane-path `--cache` write (S5) was not executed (contract); it is a code-reading finding.
- Tool installs or upgrades: none. Nothing installed, no `pacman`, no `~/.local/bin` change.
- No mutating git in `L` or the fleet repo. Read-only: `show`, `cat-file`, `log --find-object`, `ls-tree`, `ls-files`, `check-ignore`, `status`, `rev-parse`. Clones were under `S` only (`git clone --shared`, detached at base), each `rev-parse --show-toplevel` checked before use.

## Calibration notes for L1

- The round-49 sentinel's F1 is partly remediated at HEAD (S3), and its scan missed `f1.hdr` (S2) because the scan covered only the round-49 diff. For round 50, scan the whole HEAD tree for cookie literals as well as the round diff.
- The S1 defect is a port-introduced regression: round-41 never copied REA's tree (`c1-run.sh` extracts to scratch and writes only `after.json`), and the round-49 copy was introduced for round-49's lane-built carriers. The round-50 plan's "carriers never committed" is true for the carrier file but not its contents unless S1 is fixed.
- Repro script (`A/repro-custody.py`) is self-contained and re-runnable against a fresh clone: `git clone --shared L S/clone && git -C S/clone checkout --detach 7c678ae6d97aedb969fd253b52b3d2882ef1e186`, then `python3 -I -B A/repro-custody.py S`.

## Artifacts

- `.ufo/waves/round-50/w1/C1SentinelFetch/commands.txt` — every command, exit code and sha256 used.
- `.ufo/waves/round-50/w1/C1SentinelFetch/repro-custody.py` — the repro script (sha256 `aab9ab30…b604`).
- `.ufo/waves/round-50/w1/C1SentinelFetch/repro-custody.out` — its output (sha256 `c23a1a23…0928`); `repro-custody.err` empty.
