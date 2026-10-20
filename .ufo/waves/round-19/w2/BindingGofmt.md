# BindingGofmt — attack on the C3 binding for t1250-gofmt (round 19, wave 2)

Seat: `KaidokuR19.BindingGofmt-3` (reviewer). This seat is author-side, not an outside verifier.
Axes: calibration, freshness, depth.
LANE = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; RUN = `LANE/.ufo/waves/round-19/runs/t1250-gofmt`.

Revisions observed:
- freeze `a1140e76fffdc1be032d9d813dbb686157803bbc`;
- `refs/heads/main` was `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` when I started;
- `refs/heads/main` moved to `279e8b19c51658bfd05b9e31a1c0894ab2e70537` during the review (commit 16:21:51 -03, pushed 16:21:53) and was still there at 16:27:38 -03. All revision-scoped checks and the mutation clone use `279e8b19`.

## Verdict

**The binding holds. I found no defect in the t1250-gofmt binding chain.** Each leg of the frozen `binding_gate` (`git show a1140e7:.ufo/waves/round-19/predictions/decision-rule.json` line 3) holds independently:

1. **`receipt-validate.py --require-mid-maps` exits 0.**
   - I reproduced it with the documented procedure: producer bytes restored at the pinned path.
   - The output equals the retained `evidence/receipt-validation/t1250-gofmt.json` except for `pins_path`.
   - Under today's bytes the only findings are the expected 2 on the validator file; no other pin has drifted.
2. **Carrier sha256 equals the prediction's.** This holds only transitively; the log has no full sha256 (see INFO-1).
3. **The prediction blob is unchanged from a1140e7.** Confirmed.

t1250-gofmt contributes 1 label to the C3 count: it has a bound retained log and a `compare.json` (decision-rule line 6). Two findings are LOW and the rest are INFO; none changes the gofmt verdict.

## Findings by severity

No HIGH or MEDIUM.

**LOW-1 — the validator does not bound the mid-map count and does not see orphan maps. This is a depth gap, not a gofmt defect.**
- **Mutation M7** (below):
  - Change: delete `pin_checks[1]` from the receipt, keep `pins/mid-2.json`, and add an orphan `pins/mid-3.json`.
  - Result: the tip validator exits **0** (360 checks, 0 findings).
- **Why the validator misses it:** `verify_mid_maps` only requires at least one analyze check (`receipt-validate.py@279e8b19:607-630`). Its documented limit already trusts the receipt as the run-window record (`:49-52`).
- **Precedent:** round 18 ran an orphan/unreferenced scan by hand (`.ufo/waves/round-18/w2/MidMapsRetained.md:24,191`), but it was never added to the tool.
- **Gofmt itself is clean:** maps are 2 on disk, 2 tracked at `279e8b19`, and 2 referenced; orphans 0; cadence predicts 2 (§2).
- **Hardening:** enumerate `pins/mid-*.json`, flag unreferenced files, and require at least `1 + floor((ended − first_check)/PIN_CHECK_S)` checks.

**LOW-2 — the retained validation JSON does not name the code that produced it. This is a calibration recording gap, not material here.**
- **What is missing:** `evidence/receipt-validation/t1250-gofmt.json:10` records `"pins_path": "/tmp/pins.py"`, and `:22` records `"tool": "receipt-validate.py"`. That tool value is a constant (`receipt-validate.py@279e8b19:698-700`). Neither the validator digest nor the pins.py digest is recorded.
- **What the bytes probably were (inference):**
  - `main:corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md:46` says the corrected validator was "extracted to `/tmp`".
  - `/tmp/kr19-fixed-validator.py` has sha256 `9276b198…6d45` and mtime 16:07:55.656 -03.
  - `/tmp/pins.py` has sha256 `9e9c7250…0fe0` and mtime 16:07:55.658.
  - The 8 evidence files have mtimes 16:07:55.749–16:07:56.465.
  - Both `/tmp` copies are non-durable.
- **Why it is not material:** the frozen, d0690fd and tip validators give the same verdict (exit 0, 366 checks) on the restored state (§7).

**INFO-1 — wording of the binding gate: "the bound log's carrier sha256" (decision-rule line 3).**
- The log carries only `target-2aa4122abbd1.bin` (sha256[:12], `ghidra.log:46`) and the full MD5 (`ghidra.log:59`).
- Full-sha equality is transitive. Log (prefix + MD5) → carrier on disk (sha256 `2aa4122a…0a80`, MD5 `51928083…6fe3`) → prediction.
- The validator computes the MD5 only while the carrier still has the recorded sha (`receipt-validate.py@279e8b19:188-195,218-225`). If the carrier changed, `md5_ok` is None and binding does not fire. The pin re-hash still fails the receipt (M5).

**INFO-2 — dates on jj-exported commits.**
- `4f6c73f` has author date 15:57:44 -03 but contains the gofmt run (16:00:00–16:00:33) and the validation evidence (16:07:55). Its committer date is 16:09:17 and it was pushed 16:09:20.
- Ordering proofs must use committer date or the reflog, not `%ad`.
- The knowledge text at `main:…toolchain-replay.md:17` says the freeze was "committed and pushed … 15:57:47". The push reflog line records epoch 1792522666 = **15:57:46** (`.git/logs/refs/remotes/origin/main:38`). This 1 s nit does not change the ordering.

**INFO-3 — the log capture cut is systematic.**
- All 8 round-19 logs end at `ANALYZING changes made by post scripts`. For gofmt that is `ghidra.log:182`, 16:00:31.
- The last gofmt copy was 1.000819 s before the analyze step ended (`receipt.json:1911,1931`). This is disclosed by `log_capture_limit` (`receipt.json:24`).
- Every Go line (`ghidra.log:122-142`) and `REPORT: Analysis succeeded` (`:176`) come before the cut. The post-script re-analysis phase is unobserved in every run.

**INFO-4 — outcome artifacts sit outside the receipt's digest set but re-derive exactly.**
- `observation.json` binds the log through its own `log_sha256` (`observation.json:168`, equal to `receipt.json:1903`).
- `compare.json` records input paths only.
- Both re-derive byte-for-byte from the bound log with the a1140e7 tool bytes. `compare` run against the a1140e7 prediction blob gives the same fields (§8).

**INFO-5 — freshness.**
- **Main moved during the review.** It went d0690fd → 279e8b19, and the validator changed 9276b198 → 6afb7ef6.
- **The LANE working tree was dirty with uncommitted edits.** For example, `receipt-validate.py` was modified at 16:19:33, before 279e8b19 committed it.
- **Exactly two findings, nothing else.** At tip, and live against the LANE working tree, the result is exactly 2 findings: `sha256_mismatch` and `size_mismatch` on the pinned validator path (C0, C0-live). The other 151 pins still re-hash equal at 16:2x -03: the carrier, the prediction, the emulator, `selection.py`, 4 W17 tools and the 143 Ghidra Go data files.
- **Retained artifacts were not rewritten.** The run tree `17969e61…` and the validation blob `88a61f6e…` are identical at `4f6c73f` and `279e8b19`.

## Observations (commands, exits, anchors)

### 1. Re-hash of bound logs, maps, step outputs and carrier

```
$ cd RUN && sha256sum logs/rea-ghidra-kDM6dB/ghidra.log logs/rea-ghidra-kDM6dB/script.log pins/mid-1.json pins/mid-2.json analyze.json analyze.stderr inspect-go.json inspect-go.stderr /home/vgpnk/.local/opt/go-1.25.0/bin/gofmt   # exit=0
$ stat -c '%s %n' logs/rea-ghidra-kDM6dB/{ghidra,script}.log; md5sum /home/vgpnk/.local/opt/go-1.25.0/bin/gofmt   # exit=0
$ git show refs/heads/main:.ufo/waves/round-19/runs/t1250-gofmt/<file> | sha256sum   # per file, exit 0 (279e8b19 blobs = working tree)
```

All values are [OBSERVATION]:

| file | sha256 now (disk = main blob) | receipt record | match |
|---|---|---|---|
| ghidra.log (19119 B) | `6fbfca76…7066` | `receipt.json:1901-1903`, `:1959-1961` | yes |
| script.log (105 B) | `6248e2b0…f7e3` | `:1906-1908`, `:1964-1966` | yes |
| pins/mid-1.json | `180fbc3d…d6ac` | `:1940` | yes |
| pins/mid-2.json | `02688f0b…8b58` | `:1949` | yes |
| analyze.json | `3df8623e…ecad2` | `:1978` | yes |
| inspect-go.json | `e9113bb1…e020` | `:1997` | yes |
| analyze/inspect-go stderr | `e3b0c442…b855` (empty) | `:1976`, `:1995` | yes |
| carrier gofmt (3000838 B) | `2aa4122a…0a80`, md5 `51928083…6fe3` | `:6`, `:8`, `:9` | yes |

### 2. Mid maps: count and content

```
$ python3 -I -B - <<'EOF' … (orig_argv --pin set, pins_pre/post/mid entry equality, canonical re-dump, monotonic gaps) EOF   # exit=0
orig_argv --pin count 152 unique 152 | pins_pre 152, pins_post 152 | keys == argv pins + defaults: True
mid-1: entries 152 keys==pre True differing [] | canonical re-dump equal: True
mid-2: entries 152 keys==pre True differing [] | canonical re-dump equal: True
pre->mid1 s 0.865107086  mid1->mid2 s 30.075139518
analyze duration s 31.623427  first check offset s 0.047068  expected checks 2  recorded 2
$ git ls-tree --name-only refs/heads/main RUN/pins/   # exit=0 → mid-1.json, mid-2.json
```

[OBSERVATION]
- There are 2 maps on disk, 2 tracked at 279e8b19 and 2 referenced (`receipt.json:1934-1953`). There are no orphans.
- Each map has 152 entries, and every entry's (sha256, size, mtime_ns) equals `pins_pre`.
- Each map re-serialises byte-for-byte in the carrier-run form (`carrier-run.py:504-512`).
- `mid_run_drift_steps` is `[]` (`receipt.json:25`), and `pins_compare` shows equal with nothing changed or missing (`:348-355`).

[INFERENCE from code] The first check fires on the first poll, because `last_pin_check = 0.0` (`carrier-run.py:470`, `:484`). Later checks fire every `PIN_CHECK_S = 30.0` (`:39`). A 31.62 s analyze step therefore yields exactly 2 maps; the observed gap of 30.075 s is at least 30.

### 3. Carrier sha256 against the frozen values

```
$ git show a1140e7:.ufo/waves/round-19/predictions/carriers.tsv a1140e7:.ufo/waves/round-19/predictions/SHA256SUMS   # exit=0
$ git show a1140e7:.ufo/waves/round-19/predictions/t1250-gofmt.prediction.json   # exit=0
$ sha256sum /tmp/kr18-dl/go1.25.0.linux-amd64.tar.gz; tar -xzOf /tmp/kr18-dl/go1.25.0.linux-amd64.tar.gz go/bin/gofmt | sha256sum   # exit=0 (pipe 0 0)
2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613  /tmp/kr18-dl/go1.25.0.linux-amd64.tar.gz
2aa4122abbd1593ee7c9e184366feef7cb06e52ce790b5ef2119e8aee8640a80  -
```

[OBSERVATION] `2aa4122abbd1593ee7c9e184366feef7cb06e52ce790b5ef2119e8aee8640a80` appears identically at every point below:
- `carriers.tsv@a1140e7:2`;
- `t1250-gofmt.prediction.json@a1140e7:33-34`;
- `predictions/swiss-misread/t1250-gofmt.json@a1140e7` `.carrier.sha256`;
- prescan `85589ac:.ufo/waves/round-19/evidence/prescan/kr19-sm-gofmt.json`, which is identical to the frozen output except for a trailing newline (`diff` exit 1, a single newline difference);
- receipt `sha256_pre` and `sha256_post`, `pins_pre` (`:1839`) and `pins_post` (`:1073`);
- `inspect-go.json` `.subject.digest.sha256` and `.normalized_result.artifact.sha256` (go_version `go1.25.0`, module `cmd/gofmt`);
- `analyze.json` `.subject.digest.sha256`;
- the live file;
- the official archive member `go/bin/gofmt`. Its archive sha `2852af0c…b613` equals S038 and decision-rule line 27.

The log binding uses the prefix `target-2aa4122abbd1` and `MD5=519280831603a98c964d066cbf506fe3` (`ghidra.log:46,59`), which equals the live carrier's MD5.

[INFERENCE from control flow] The runner compared the live sha with the tsv column before the run (`run-carriers.sh@a1140e7:286-290`). A mismatch writes exit 2 and skips the label, so `carrier-run.exit` = `0` shows this preflight passed.

### 4. Prediction blob unchanged

```
$ for r in a1140e7 refs/heads/main; do git show $r:.ufo/waves/round-19/predictions/t1250-gofmt.prediction.json | sha256sum; done; sha256sum <working tree file>   # exit=0
```

[OBSERVATION] The digest is `f946efe2…69de` in all of these places:
- the a1140e7 blob, the 279e8b19 blob and the working tree;
- `SHA256SUMS@a1140e7:8`;
- `pins_pre` (`receipt.json:1879`), `pins_post` (`:1113`), mid-1 and mid-2.

`compare.py` read the working-tree path (`run-carriers.sh@a1140e7:277,329`). Its bytes are pinned before, during and after the run.

### 5. Producer identity

```
$ sha256sum <7 tools>; git show a1140e7:<tool> | sha256sum; git show refs/heads/main:<tool> | sha256sum   # exit=0
```

[OBSERVATION]
- `producer.json:5` records `branch_tip` = a1140e7 at 19:00:00Z (`:3`). Main still pointed at a1140e7 until 16:09:17 (reflog).
- 7/7 `tool_sha256` values equal the a1140e7 blobs. Six are unchanged at tip.
- `receipt-validate.py` changed: `70672eb3…d145` (a1140e7, `producer.json:11`) → `9276b198…6d45` (4f6c73f, d0690fd) → `6afb7ef6…c762` (279e8b19).

### 6. Freeze-before-run ordering

```
$ git log --format='%H author=%ad commit=%cd' --date=iso-strict 8a8da7e..refs/heads/main   # exit=0
$ grep -n a1140e7… .git/logs/refs/heads/main .git/logs/refs/remotes/origin/main   # exit=0
$ git log -1 --format='committer-epoch=%ct author-epoch=%at' a1140e7   # 1792522664 / 1792521438
```

[OBSERVATION] Timeline (all -03):
- a1140e7 committed at 15:57:44 (author date 15:37:18);
- exported to `main` at 15:57:44 (`.git/logs/refs/heads/main:151`);
- pushed at 15:57:46 (`…/origin/main:38`);
- first run started at 15:57:51 (`runs/run-log.txt:2`);
- the gofmt run took 16:00:00–16:00:33 (`run-log.txt:4-5`), with analyze starting at 19:00:01.368Z (`receipt.json:1974`).

So the freeze was pushed 134 s before gofmt began. No gofmt artifact is in a1140e7: its 22-file stat lists only predictions, the generator and the runner.

### 7. Retained validation reproduction and mutation matrix

Setup:
- The clone is `/tmp/kr19-w2-BindingGofmt-8MDSpP/clone` (`git clone -q --no-hardlinks LANE`), checked out detached at `279e8b19c516…`; `rev-parse HEAD` printed 279e8b19.
- Validators came from blobs: `v_tip` (`6afb7ef6`), `v_d069` (`9276b198`), `v_frozen` (`70672eb3`), each next to pins.py `9e9c7250`.
- Each case runs `unshare -rm --propagation private sh -c "mount --bind CLONE LANE && exec python3 -I -B V --require-mid-maps LANE/…/receipt.json"`. The receipt bytes and absolute paths therefore stay unchanged, and LANE is never written. A namespace probe confirmed the bind is invisible outside.
- The harness is `/tmp/kr19-w2-BindingGofmt-8MDSpP/harness.py`, with raw outputs in `out/`.
- After the run the clone was restored (`git status` empty), then deleted together with the mutated carrier copy.

```
$ python3 -I -B harness.py   # harness-exit=0, wall 1.82 s
```

| case | change | validator | exit | checks | findings |
|---|---|---|---|---|---|
| C0-live | none; real LANE working tree (validator 6afb7ef6) | tip | 1 | 366 | `sha256_mismatch` + `size_mismatch` @ `pins_post.entries.…/receipt-validate.py` only |
| C0 | clone at tip as-is | tip | 1 | 366 | same two findings only |
| G1 | a1140e7 validator bytes restored at the pinned path (procedure in `…toolchain-replay.md:46`) | d069 / tip / frozen | 0 / 0 / 0 | 366 each | none; **d069 output equals the retained JSON except `pins_path`** |
| M1 | delete `pins/mid-2.json` | tip | 1 | 363 | `mid_map_missing`, `missing_file` |
| M2 | one hex char of the carrier digest flipped inside mid-1 | tip | 1 | 366 | `mid_map_sha256_mismatch`, `mid_map_compare_mismatch` ×2, `sha256_mismatch` |
| M3 | one hex char of the loader MD5 flipped in ghidra.log | tip | 1 | 366 | `binding_mismatch`, `sha256_mismatch` ×2 |
| M4 | t1250-cgo's log swapped in, receipt sha/bytes forged to match | tip | 1 | 366 | `binding_mismatch` only (content binding is load-bearing) |
| M5 | carrier last byte flipped (copy bind-mounted over the carrier path in-namespace, 0644, never executed) | tip | 1 | 366 | `sha256_mismatch` @ pins_post carrier, `sha256_mismatch` @ `$.carrier` |
| M6 | prediction file +1 newline | tip | 1 | 366 | `sha256_mismatch`, `size_mismatch` @ prediction pin |
| M7 | receipt `pin_checks[1]` dropped; mid-2 left as an orphan, plus orphan mid-3 | tip | **0** | 360 | **none** (LOW-1) |
| M8 | all analyze `pin_checks` dropped | tip | 1 | 354 | `mid_checks_absent` |
| M9 | mid-2 shows carrier drift; `map_sha256` forged to match; recorded `equal:true` | tip | 1 | 366 | `mid_map_compare_mismatch` (equal, changed) |
| M10 | `bound_sessions` renamed to a dir no retained log holds | tip | 1 | 366 | `binding_mismatch` |

[OBSERVATION] The retained "valid" verdict implies the pinned validator path held the producer bytes when validation ran: any other bytes yield the C0 pair of findings.

### 8. Re-deriving the outcome artifacts

```
$ python3 -I -B v_frozen/log-extract.py --log RUN/logs/rea-ghidra-kDM6dB/ghidra.log > out/observation.rederived.json   # exit=0
$ cmp out/observation.rederived.json RUN/observation.json   # exit=0
$ python3 -I -B v_frozen/compare.py --prediction LANE/.ufo/waves/round-19/predictions/t1250-gofmt.prediction.json --observation RUN/observation.json > out/compare.rederived.json   # exit=0
$ cmp out/compare.rederived.json RUN/compare.json   # exit=0
$ python3 -I -B v_frozen/compare.py --prediction pred-a1140e7.json --observation out/observation.rederived.json   # exit=0; equals retained except path fields: True, all_match True
```

The tool bytes are a1140e7 blobs: log-extract `eb8f2c78…`, compare `582a77f3…`.

Other session and step facts:
- The receipt records exactly one bound session (`receipt.json:2-4`), no unbound sessions (`:2000`), an empty session baseline and no leftovers (`:1916-1918`).
- `carrier-run.stdout` equals `receipt.json` plus `receipt_path`.
- `carrier-run.exit`, `observation.exit` and `compare.exit` are all `0`.
- The 8 runs use 8 distinct private session parents.

## Residual risk and verification gaps

- **Modify-and-restore cannot be excluded.** Per `receipt-validate.py:49-52`, validation does not rule out bytes being changed and restored between the run and validation. The same applies to a full rewrite-and-rehash of the chain (knowledge `:46`). Push reflog times are the only external ordering anchor.
- **The retained validation's code identity is inferred** (LOW-2). It does not change the verdict.
- **The post-script phase is not observed** in any log (INFO-3).
- **About 50 ms between `pins_post` (19:00:33.038Z) and compare's read** is not covered by pins. The file still hashes to the frozen blob [INFERENCE: no drift].
- **Not done (out of scope):** I ran no REA, no Ghidra and no carrier execution. Outcome correctness (silent versus failure) belongs to the OutcomeGofmt seat. I ran no validator `--selftest` and no broad suite.

Installs or updates: none. No LANE writes except this report. No git writes or jj commands in LANE.
