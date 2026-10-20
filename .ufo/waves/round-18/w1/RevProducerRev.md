# RevProducerRev — R17-PRODUCER-REV: which `carrier-run.py` produced each carrier pass

Baseline `9011581d84527ba34c675f9cf912e54d2e72d470` (lane `kaidoku-shokunin`, branch `main`).
Seat: `KaidokuR18.RevProducerRev`, author-side advisory. Read-only: this file is the only write.
Evidence class: Git objects (`show`, `rev-parse`, `cat-file`, `log`, `diff`, `grep`) and receipt bytes.
No REA, no Ghidra/`analyzeHeadless`, no carrier execution, no jj or git write, no installs.
Worktree was clean at seat start (`git status --porcelain --untracked-files=no` → empty, exit 0).
During the seat, other round-18 owners modified tracked tools
(`.ufo/waves/round-17/tools/{carrier-run,compare,log-extract}.py`,
`.ufo/gates/citation-drift/citation-drift-probe.py`, `.ufo/waves/round-17/verify.py`); those edits are
not mine and none of my conclusions reads working-tree bytes. Every anchor below is a Git object at a
named revision (`git show <rev>:<path>`), fixed by hash.

## 0. Answer

| Pass | Receipts stored at | First pre-pin / last analyze end (UTC) | **Producing revision** | `carrier-run.py` blob | Blob sha256 |
|---|---|---|---|---|---|
| A, first (8 receipts) | `da64646adcb19c1ede7537b799b8c7d283fe43da` | `13:47:05.973725` / `14:00:05.228761` | **`271167473d87ef710f07ecdd98caf0ce12091686`** | `bc964acdfb0751310ee014799627774c45469f38` | `00af3845c432590cb5cfe9b82d7adb40778a144d45cfd7a263bb66e0d4c28221` |
| B, second (8 receipts) | `d0ab2992149a38794e5ef2474ba5d4ef5ee1e905` (unchanged at `9011581`) | `14:27:41.944543` / `14:40:02.270081` | **`95e34db62f2693c455d7ee4dfef24b8f3ebc007d`** | `c536e3e4bd0b3091efd43d01448326cec5a63cc8` | `11641f0ed3b998043e29f333162406378796e5f4bd64f0742a63cb21965e7677` |

Two non-producer commits are easy to conflate with those:

- `da64646` is the **receipts commit** for pass A, not the producing revision: it does not touch
  `carrier-run.py` (E1/E2) and was committed 6 m 00.8 s after the last pass-A receipt ended (E8).
- `d0ab299` (S) is the **receipts commit** for pass B and the round's verification/measured source
  revision, not a producer: its blob `f91bbc76c73991ba5d74137ca69b115dcee7c12f` adds
  `carrier.md5_pre` and `binding.md5_ok`, which no pass-B receipt contains (E5/E6), and it was
  committed 7 m 21.7 s after the last pass-B receipt ended (E8).

The R17 lesson's pass-B attribution (`corpus/lessons/round-17-verifier-spotcheck.md:139`) is
**confirmed**; no earlier lane text names a pass-A producer.

## 1. Timeline (observation, all times UTC)

| Commit | commit `%cI` | push to `origin/main` | Event | `carrier-run.py` blob at that tree |
|---|---|---|---|---|
| `2711674` | `13:46:45` | `13:46:47` | predictions + tool frozen **pre-run** (file added here) | `bc964ac` |
| — | — | — | pass A runs 8 carriers, `13:47:05.973` → `14:00:05.229` | — |
| `da64646` | `14:06:06` | `14:06:09` | pass-A receipts committed; tool unchanged | `bc964ac` |
| `95e34db` | `14:27:35` | `14:27:37` | w2-hardened tools committed **pre-rerun** | `c536e3e` |
| — | — | — | pass B runs 8 carriers, `14:27:41.944` → `14:40:02.270` | — |
| `d0ab299` | `14:47:24` | `14:47:26` | pass-B receipts committed; md5 fields added to tool | `f91bbc7` |
| `b31975d`…`de6c721` | `14:48:35`…`14:50:03` | `14:48:37`…`14:50:05` | verification pass, records | `f91bbc7` |
| `9011581` | `15:06:56` | `15:06:58` | verifier spot-check; receipts untouched | `f91bbc7` |

Push instants are the `update by push` entries of `.git/logs/refs/remotes/origin/main` (read-only);
the commit objects themselves record no push time.

Lineage is linear (each commit's sole parent is the previous one; `git merge-base --is-ancestor
2711674 9011581` exit 0), so no merge can hide a fourth tool blob.

## 2. Evidence chain

### E1 — only three commits ever touch the tool; `da64646` is not one

```
$ git log --format='%H %cI %s' --all -- .ufo/waves/round-17/tools/carrier-run.py
EXIT: 0
d0ab299... 2026-10-20T11:47:24-03:00 round-17: w2 integration — … (source revision)
95e34db... 2026-10-20T11:27:35-03:00 round-17: w2-hardened tools and frozen replicate expectations (pre-rerun)
2711674... 2026-10-20T10:46:45-03:00 round-17: frozen carrier predictions, wave-1 evidence and integrated tools (pre-run)
```

`git log --diff-filter=A -- .ufo/waves/round-17/tools/carrier-run.py` → `2711674`, exit 0: the file
first appears at the pre-run commit. There is no earlier committed version to fall back to.

### E2 — blob identity per revision

```
$ git rev-parse <rev>:.ufo/waves/round-17/tools/carrier-run.py
2711674 EXIT:0 bc964acdfb0751310ee014799627774c45469f38
da64646 EXIT:0 bc964acdfb0751310ee014799627774c45469f38   # unchanged
95e34db EXIT:0 c536e3e4bd0b3091efd43d01448326cec5a63cc8
d0ab299 EXIT:0 f91bbc76c73991ba5d74137ca69b115dcee7c12f
9011581 EXIT:0 f91bbc76c73991ba5d74137ca69b115dcee7c12f   # unchanged
```

### E3 — receipt key alphabet ⇔ blob emission surface

All 8 pass-A receipts at `da64646` carry exactly 16 top-level keys:
`bound_sessions, carrier, label, log_capture_limit, orig_argv, pins_compare, pins_post, pins_pre,
python, rea_ghidra_env, retained_logs, session_dir_baseline, session_parent,
session_parent_leftovers, steps, unbound_sessions`.
All 8 pass-B receipts at `9011581` carry the same 16 **plus exactly two**:
`child_env_keys` and `mid_run_drift_steps` (18 keys).

Literal `receipt[...]` assignment extraction (regex over each blob):

| Blob | `child_env_keys` | `mid_run_drift_steps` | `pin_checks` | `md5_pre` | `md5_ok` |
|---|---|---|---|---|---|
| `bc964ac` (2711674/da64646) | absent | absent | absent | absent | absent |
| `c536e3e` (95e34db) | `:311` | `:396` | `:462` | absent | absent |
| `f91bbc7` (d0ab299/9011581) | `:323` | `:414` | `:481` | `:344` | `:149` |

The only keys absent from the file in a successful run are `error` (error paths only) and
`receipt_path` (set **after** the JSON is written, `carrier-run.py:369-372` at bc964ac), so the
observed 16/18 split is exactly the expected success shape per blob.

### E4 — what changed between pass A's blob and pass B's blob

```
$ git diff 2711674 95e34db -- .ufo/waves/round-17/tools/carrier-run.py
EXIT: 0   (45 insertions, 5 deletions)
```

The added observable fields and their exact anchors at `95e34db`:

- `receipt["child_env_keys"] = child_env_keys` — `:311` (unconditional).
- `receipt["mid_run_drift_steps"] = mid_drift` — `:396` (unconditional, before the receipt write).
- `rec.setdefault("pin_checks", []).append({...})` — `:462`, inside `_run_polled`, with
  `last_pin_check = 0.0` — `:444`.

`bc964ac` has none of these. Therefore **no pass-A receipt can have come from a run of either
later committed blob**, and the only committed blob in the pass-A window is `bc964ac`.

### E5 — what changed between pass B's blob and S's blob

```
$ git diff 95e34db d0ab299 -- .ufo/waves/round-17/tools/carrier-run.py
EXIT: 0   (31 insertions, 12 deletions)
```

Three code-level facts make the pass-B producer decidable:

1. `carrier.md5_pre` is written at `:344` inside the **same branch** as `carrier.sha256_pre` (`:339`):
   `if pins_pre["entries"].get(carrier, {}).get("sha256"):` → set `sha256_pre` → compute MD5 → set
   `md5_pre`. All 8 pass-B receipts have `carrier.sha256_pre` and the carrier present in
   `pins_pre.entries` (146 entries), so under `f91bbc7` the branch fires and `md5_pre` is
   unavoidable. None has it.
2. `bind_session` gains `carrier_md5=None` and `out["md5_ok"]` (`:126`, `:149`), and the call site
   passes `receipt["carrier"].get("md5_pre")` (`:395`). Every retained-log `binding` would then be
   `{logfile_ok, target_ok, md5_ok}`. All 8 pass-B receipts carry exactly
   `{logfile_ok, target_ok}`.
3. The remaining diff (`stop` on timeout, timeout exit 2) is conditional on a timeout; no pass-B
   run timed out (all `carrier-run.exit` = 0), so it cannot mask a `f91bbc7` run.

Therefore pass B was produced by `c536e3e` (95e34db), not by S's blob. This is the same
discriminator the R17 lesson used, now checked on all 8 receipts and on the emission condition.

### E6 — receipt bytes, all 16 checked (not sampled)

```
git show <rev>:.ufo/waves/round-17/runs/<label>/receipt.json   # 8 labels × 2 revs, exit 0 each

da64646  (16 keys)  carrier.md5_pre=False  binding.md5_ok=False  pin_checks=False  child_env_keys=False  mid_run_drift_steps=False   8/8
9011581  (18 keys)  carrier.md5_pre=False  binding.md5_ok=False  pin_checks=True   child_env_keys=True   mid_run_drift_steps=True    8/8
```

Representative anchors, `pro-aether`:

- `da64646` receipt: `receipt.json:8` `"sha256_pre": "06c91f55…"`; `:1800-1802`
  `"binding": {"logfile_ok": true, "target_ok": true}`; no `pin_checks`, no `child_env_keys`,
  no `mid_run_drift_steps`.
- `9011581` receipt: `:10-19` `child_env_keys` (9 entries incl. `NODE_DISABLE_COMPILE_CACHE`);
  `:23` `"mid_run_drift_steps": []`; `:1812-1815` `binding` with two keys only; `:1851` `pin_checks`.

Second-pass `pin_checks` first instant vs `analyze.started_at_utc` is **+0.048…+0.064 s** in all 8
runs (one per label), i.e. the check fires on the first poll because `last_pin_check = 0.0`
(`c536e3e:444`). That makes `pin_checks` absence in pass A a *structural* exclusion, not a
duration-dependent one.

### E7 — where the receipts live, and when they were overwritten

```
receipt blob at da64646  ==  receipt blob at 95e34db   8/8 same     (pass A untouched before rerun)
receipt blob at da64646  !=  receipt blob at d0ab299   8/8 overwritten
receipt blob at d0ab299  ==  receipt blob at 9011581   8/8 same     (verifier committed no receipt bytes)
```

`run-log.txt`: `da64646` and `95e34db` share blob `b7939a5f8628…`; `d0ab299` and `9011581` share
`e33131dcf0dd…`. Pass-A log: 14 lines, 7 labels, no header and no final exit line. Pass-B log:
18 lines, 8 labels, header + `run-carriers exit=0`. The pass-B header text is not emitted by
`run-carriers.sh` at `95e34db` (`grep -n 'argv\|started'` hits only a comment at `:4`), so it is
author/wrapper text — corroborative ordering only, not a producer proof.

### E8 — timing against commit and push instants

Push instants are the `update by push` entries of `.git/logs/refs/remotes/origin/main` (read-only
file; the commits themselves record no push time).

| Boundary | Delta |
|---|---|
| `2711674` commit `13:46:45` → push `13:46:47` | +2 s |
| `2711674` push `13:46:47` → first pass-A pin `13:47:05.973725` | **+18.97 s** |
| last pass-A end `14:00:05.228761` → `da64646` commit `14:06:06` (push `14:06:09`) | **+360.77 s** |
| `95e34db` commit `14:27:35` → push `14:27:37` | +2 s |
| `95e34db` push `14:27:37` → first pass-B pin `14:27:41.944543` | **+4.94 s** |
| last pass-B end `14:40:02.270081` → `d0ab299` commit `14:47:24` (push `14:47:26`) | **+441.73 s** |

Each run window sits strictly between its producer's push and its receipts' commit: pass A runs
18.97 s after `2711674` is pushed and ends 6 m 00.8 s before `da64646`; pass B runs 4.94 s after
`95e34db` is pushed and ends 7 m 21.7 s before `d0ab299`.

### E9 — executed-path and direct-hash checks

- `orig_argv` in both passes (all 16): `['python3','-I','-B','tools/carrier-run.py', …]`, with
  `steps.analyze.cwd = /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17`.
  `-I` isolates the interpreter (no user site, no env-based path injection), so the executed file is
  exactly `<W17>/tools/carrier-run.py`.
- No receipt, stdout, stderr or run-log records a digest of the tool itself:
  `git grep -n -E 'bc964ac|c536e3e|f91bbc7|carrier-run\.py' 9011581 -- .ufo/waves/round-17/runs`
  returns only the literal argv path (exit 0), never a hash; and `git grep -c -F` for the first 16
  hex of each candidate blob's **sha256** (`00af3845c432…`, `11641f0ed3b9…`, `953373e52ab9…`)
  matches 0 files for all three. The classification therefore rests on the emission surface, not on
  a self-recorded tool hash.
- `/usr/bin/aether` is a regular file (`readlink -f` = same path), so the `realpath` change added at
  `c536e3e:278` is not observable in `carrier.path` and is not used as evidence.

## 3. Why the absence arguments are decisive

For pass A, three independent fields would have been written by either later blob:

1. `child_env_keys` is assigned unconditionally at `c536e3e:311` / `f91bbc7:323`.
2. `mid_run_drift_steps` is assigned unconditionally at `c536e3e:396` / `f91bbc7:414`.
3. `pin_checks` is appended on the **first** poll (`last_pin_check = 0.0`, `c536e3e:444`) at
   `c536e3e:462` / `f91bbc7:481`; observed first-check latency in pass B is ≤ 64 ms.

All 8 pass-A receipts lack all three. Hence pass A ≠ `c536e3e`, `f91bbc7`.

For pass B, two independent md5 fields would have been written by `f91bbc7` and neither was:
`carrier.md5_pre` (same branch that produced the present `carrier.sha256_pre`) and
`binding.md5_ok` (call site `:395`). Hence pass B ≠ `f91bbc7`; with pass B also showing
`child_env_keys`/`mid_run_drift_steps`/`pin_checks`, pass B = `c536e3e`.

## 4. Divergences from current lane text

1. `corpus/lessons/round-17-verifier-spotcheck.md:139` — **confirmed as written** for pass B
   (`95e34db`), including the run window `14:27:41–14:40:02Z` (measured `14:27:41.944`–
   `14:40:02.270`) and "S (14:47:24Z)" = `d0ab299`.
2. `.ufo/waves/round-17/predictions/replicate-expectations.json:83` —
   `"first_pass_revision": "da64646adcb19c1ede7537b799b8c7d283fe43da"`. True as a **storage**
   location, wrong if read as the producing revision. `[INFERENCE]` Replace with `2711674…` or
   carry both, labelled `first_pass_receipts_at` / `first_pass_producer`.
3. `SCORECARD.md:2353-2355` — "Measured source revision … `d0ab299…`" is the verification
   revision. It is the producer of neither pass. No line currently names `2711674` as pass A's
   producer (the knowledge entry at `:47-48` names `2711674` only for the frozen predictions).
4. `SCORECARD.md:2374` capability row — "16 across two passes, 8 retained at HEAD, 8 at
   `da64646`" is correct as storage and does not claim a producer.

Correction text that satisfies C1's R17-PRODUCER-REV check (one line, `R17-PRODUCER-REV`, two
distinct 40-hex hashes; suitable for both `SCORECARD.md` and the r17 knowledge entry):

```
R17-PRODUCER-REV: the pass-1 receipts stored at da64646adcb19c1ede7537b799b8c7d283fe43da were produced by carrier-run.py at 271167473d87ef710f07ecdd98caf0ce12091686 (blob bc964ac, the same blob da64646 carries); the pass-2 receipts stored at 9011581 were produced by 95e34db62f2693c455d7ee4dfef24b8f3ebc007d (blob c536e3e); d0ab2992149a38794e5ef2474ba5d4ef5ee1e905 is the verification revision and added carrier.md5_pre/binding.md5_ok only after both passes.
```

## 5. Residual uncertainty

1. **Working-tree bytes (the main limit).** Git proves committed blobs, not the exact file present
   during a run. A jj-colocated working-copy edit that was reverted before the next commit leaves no
   Git trace. The bounded claim is: in every emission-relevant respect (field alphabet, conditional
   branches, `binding` shape, first-poll pin check), all 8 receipts per pass match the named blob and
   exclude the other two. Non-emitted code (comments, dead branches, error paths) is unobservable.
   The working tree changed *after* this seat began (round-18 C3 added `map_sha256`/`pins/mid-*.json`
   on top of `f91bbc7`); that diff is a later round's fix and does not alter any `git show` result
   cited here.
2. **Byte equality vs surface equality.** For pass A, `da64646` carries the identical blob
   `bc964ac`, so "the `carrier-run.py` at `da64646`" is byte-identical to the producer; only the
   *revision attribution* differs (commit ordering). For pass B, the receipts commit `d0ab299`
   carries a *different* blob, so citing it as producer is a genuine byte-level error, not a label
   choice.
3. **Commit timestamps are jj-rewritable.** `9011581` is the only rewritten commit in the chain
   (`author 2026-10-20T11:51:47-03:00`, `committer 12:06:56-03:00`, +15 m 09 s). Its committer date
   therefore reflects a later rewrite. `95e34db`'s author = committer date, which is consistent with
   no rewrite, but ordering is used only as corroboration; the field-alphabet proof is
   time-independent.
4. **Identity form.** Hashes are the current Git ids in this jj-colocated lane; if jj rewrote any
   commit, earlier ids would differ. `9011581…` is the branch tip and all five cited commits are
   ancestors of it (`git merge-base --is-ancestor` exit 0).
5. **No self-recorded tool hash.** The receipts do not pin `carrier-run.py` (only carrier, r16
   `selection.py`, prediction, 143 Go data files = 146 paths). A future `receipt-validate` check
   could add `producer_sha256` to the receipt; absent that, this attribution is an inference from
   emitted bytes, not a recorded digest.
6. **Not exercised.** No command in this item ran `carrier-run.py`, REA, Ghidra, or any carrier; no
   `jj` or git write was performed in the lane; no tool was installed or upgraded.

## 6. Reproduce

From `LANE`:

```
git log --format='%H %cI %s' --all -- .ufo/waves/round-17/tools/carrier-run.py
git rev-parse 2711674:.ufo/waves/round-17/tools/carrier-run.py \
              da64646:.ufo/waves/round-17/tools/carrier-run.py \
              95e34db:.ufo/waves/round-17/tools/carrier-run.py \
              d0ab299:.ufo/waves/round-17/tools/carrier-run.py \
              9011581:.ufo/waves/round-17/tools/carrier-run.py
git diff 2711674 95e34db -- .ufo/waves/round-17/tools/carrier-run.py
git diff 95e34db d0ab299 -- .ufo/waves/round-17/tools/carrier-run.py
git show <rev>:.ufo/waves/round-17/runs/<label>/receipt.json   # 8 labels × 2 revs
```

All exit 0. The decisive checks are the 16/18 key split (`child_env_keys`, `mid_run_drift_steps`,
`pin_checks`) and the two missing md5 fields, not the timestamps.
