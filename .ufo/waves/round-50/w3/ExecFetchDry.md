# ExecFetchDry — R50-C1 fetch chain dry-run (round 50, attempt 2, wave 3)

**VERDICT: the fetch chain is sound and ready to run — but the C3 instrument
path in `plans/round-50-attempt2-claims.md` (R50-C3) will make BOTH the C1
counter and the C2 consistency gate unevaluable (exit 2, `frozen_path_changed`)
at the landing rev. Change the C3 instrument path, or the round closes with two
red gates.** Everything else the L1 needs is measured and below.

Fetch plan (exact argv): `.ufo/waves/round-50/w3/ExecFetchDry/fetch-plan.md`.
Receipts: `.ufo/waves/round-50/w3/ExecFetchDry/receipts/*.json` (each carries
argv, exit code, stdout/stderr sha256, UTC start/end).

---

## 1. Findings table

| # | Command (exact) | exit | stdout sha256 | UTC |
|---|---|---|---|---|
| 01 | `python3 -I -B tools/round-50/fetch-vendor.py --selftest` | **0** | `828a9add44cff9e88dc7751bd290d981ba040eff20bb25a09666d9dad34804ec` | 2026-10-29T20:36:20Z |
| 02 | `curl -sSI --max-time 60 https://download.avm.de/fritzbox/fritzbox-7581/other/fritz.os/FRITZ.Box_7581-07.18.image` | 0 | `901b8e3a8ed77f3cf82ed9381365ca42ee02b211362e85aae4370ab868a5f723` | 2026-10-29T20:36:20Z |
| 02 | `curl -sSI --max-time 60 …/FRITZ.Box_7582-07.18.image` | 0 | `83613f9a2f1040e3ca428740afacffe796afafae0e349f11b4b1e8fc50299812` | 2026-10-29T20:36:21Z |
| 02 | `curl -sSI --max-time 60 …/FRITZ.Box_6490_Cable-07.57.image` | 0 | `45ec2739365ec303bd4beb1c58ff09eb3a6a72c32cd34072bbb38c74c89f33ce` | 2026-10-29T20:36:22Z |
| 02 | `curl -sSI --max-time 60 …/FRITZ.Box_6430_Cable-07.30.image` | 0 | `73ca32b4845591503d8a9eba89ad582a015ba36a2c5f473105c1181d1cbea097` | 2026-10-29T20:36:22Z |
| 03 | `fetch-vendor.py --spec <scratch>/ok.json --cache <LANE>/.ufo/.../never-cache` | **2** | `e3b0c442…b855` (empty) | 2026-10-29T20:36:23Z |
| 04 | `fetch-vendor.py --spec <scratch>/ok.json --cache <scratch>/c --image-cache <LANE>/.ufo/.../never-ic` | **2** | `e3b0c442…b855` (empty) | 2026-10-29T20:36:23Z |
| 05 | `fetch-vendor.py --spec <scratch>/badhost.json --cache <scratch>/c` (`https://example.com/x`) | 1 | `86fb77b6606282594e1740313f6cec7e9d65fdc342f90b23fa5310654fd4fc39` | 2026-10-29T20:36:24Z |
| 06 | `fetch-vendor.py --spec <scratch>/badscheme.json --cache <scratch>/c` (`http://download.avm.de/x`) | 1 | `77e16bfb2e5cf4285757277cffd60f1278d61a93b875196514e477d31707adb4` | 2026-10-29T20:36:24Z |
| 07 | `fetch-vendor.py --cache <scratch>/c` (no spec) | 2 | `e3b0c442…b855` (empty) | 2026-10-29T20:36:24Z |
| 08 | `git -C <LANE> rev-parse 435d41fd…:tools/round-50/carriers.json f890bbea…:… 6f4aba63…:…` | 0 | `11dc38210a84c218cca5cbb5b5ec8e9f5e01f8779f09f1315c488e0a01abf27a` | 2026-10-29T20:36:24Z |
| 09 | `git -C <LANE> log -m --diff-merges=first-parent --name-status --pretty=format:COMMIT %h %s 435d41fd..HEAD -- tools/round-50/` | 0 | `e3b0c442…b855` (**empty** — no post-freeze commit touched `tools/round-50/`) | 2026-10-29T20:36:24Z |
| 10 | fixture clone: `c1.frozen_drift` + `c2.freeze_check` at a commit adding the C3 instrument | 0 | `93af2956dcba51e2c56e62e1a03950067ba60452c4f72cf03a9dcb3969f182cf` | 2026-10-29T20:36:24Z |

Fixture used for 10: `git clone --shared <LANE> $S/clone` +
`git checkout --detach f890bbea…`; `git rev-parse --show-toplevel` verified to
equal the clone; `user.name`/`user.email` set **in that clone only** (the lane's
identity is untouched); two commits, one per candidate path. No lane file was
written, no lane commit was made.

---

## 2. The blocker: the C3 instrument path breaks both frozen gates

`plans/round-50-attempt2-claims.md` R50-C3 puts the instrument at
**`tools/round-50/sqfs-triage-v5.py`**, in a commit that lands *after* the C1/C2
freeze `435d41fd`. Two frozen instruments treat that as drift:

* `tools/round-50/c1-counter.py` — `FROZEN_PREFIXES = ('tools/round-50/',)`
  (c1-counter.py:425) and `frozen_drift` (c1-counter.py:1661-1720): an **added**
  path under a frozen prefix is drift (`if code == 'A': if any(path.startswith(pfx) …)`).
  `measure()` then raises `FrozenPathChanged` → `main()` prints
  `reason: frozen_path_changed` and returns **2** (c1-counter.py:2570-2579).
* `tools/round-50/c2-record.py` — `FROZEN = ('tools/round-50', 'plans/round-50-claims.md')`
  (c2-record.py:123) and `freeze_check` (c2-record.py:1055-1069) compares the
  **whole `tools/round-50` tree** at FREEZE and REV → `frozen_path_changed`.
  The attempt-2 landing order item 4 requires
  `c2-record.py --rev <final> --freeze 435d41fd…` to exit 0 at the final rev.

Measured (receipt 10, in-process calls into the two frozen modules):

| fixture commit adds | `c1.frozen_drift` | `c2.freeze_check` |
|---|---|---|
| `tools/round-50/sqfs-triage-v5.py` (the planned path) | `['tools/round-50/sqfs-triage-v5.py']` | `('frozen path touched in FREEZE..REV: … A tools/round-50/sqfs-triage-v5.py', 'frozen_path_changed')` |
| `tools/round-50-c3/sqfs-triage-v5.py` (outside the prefix) | `[]` | `(None, None)` — green |

Both baselines are green: `frozen_drift` at `f890bbea` = `[]`, `freeze_check` at
`f890bbea` = `(None, None)`, and receipt 09 shows **no** post-freeze commit has
touched `tools/round-50/` yet — the lane is clean *today*; only the planned C3
freeze breaks it.

**Why the ordering cannot rescue it.** The C1 `--rev` must descend from the
freeze *and* contain the `after.json` receipts, which are committed after the
data run, which is after the C3 freeze (attempt-2 landing order 1→2→3). So every
rev the C1 counter can legally score is after the C3 freeze commit → drift →
exit 2. The C2 gate is scored at `<final>` for the same reason.

**Options for the L1 (all measured, not guessed):**

1. **Land the instrument outside `tools/round-50/`** — e.g.
   `tools/round-50-c3/sqfs-triage-v5.py`. Measured green for both gates.
   Consequence for B9: `census_paths` (c2-record.py:845-849) scopes the registry
   census to `tools/round-49/**` at BASE + `tools/round-50/**` at REV, so an
   instrument outside `tools/round-50/` is **not** census-scoped; B9 does not
   require a row for it and does not penalise an extra one (`registry_region`,
   c2-record.py:828-842, only checks census paths). Add the registry row anyway
   — the C3 claim asks for one and it is harmless.
2. **Amend the attempt-2 claims** (not frozen — `plans/round-50-attempt2-claims.md`
   is *not* in `FROZEN_PATHS`, only `plans/round-50-claims.md` is) to name the
   outside path, so the written claim matches the landable one. This is the
   cheapest honest fix and keeps C3's own claim text truthful.
3. **Not viable:** editing `c1-counter.py` / `c2-record.py` to relax the rule.
   The C1 counter byte-checks itself against the freeze
   (`own_sha` vs `show(root, freeze, COUNTER_PATH)`, c1-counter.py:2155-2163) and
   raises `CounterNotFrozen` → exit 2; and the edit itself is drift.

Historical precedent for the same collision: round 43 **did** add
`tools/round-43/c2-score-r43.py` after its C1 freeze — but round 43's counter had
no prefix-family rule (`FROZEN_PATHS` only). Round 49 introduced the prefix
rule and therefore landed its C2 instrument **inside** the freeze commit
(round 42 did the same: `tools/round-42/sqfs-triage-v4.py` was added by the
freeze commit `d1681696` itself). Round 50 inherited the hardened rule from
round 49 but plans a *post-freeze* instrument — the one combination nobody has
tried.

---

## 3. The fetch chain — what it does, what it enforces

Chain per carrier (fetch-vendor.py:181-272), fail-closed, nothing written for a
broken carrier:

```
url  ->  sha256(image) == external.image_sha256
     ->  tar member external.member  (whole member, no carving)
     ->  sha256(member) == external.member_sha256     (mandatory since round 41)
     ->  carve to external.length
     ->  sha256(carve) == the carrier pin
     ->  <CACHE>/<pin>.bin   (written via <pin>.bin.part + os.replace)
```

Containment rules (all measured, receipts 03-07):

| rule | implementation | measured behaviour |
|---|---|---|
| origin allowlist | `fetch()` requires `scheme == 'https'` **and** `hostname == 'download.avm.de'` (fetch-vendor.py:117-119); `_AvmOnlyRedirect` refuses any redirect that leaves that host or drops to http (fetch-vendor.py:106-113) | `https://example.com/x` → exit 1 `link=url` (no network reached); `http://download.avm.de/x` → exit 1 `link=url`; redirect to `https://evil.example/x`, `http://download.avm.de/x`, `https://sub.download.avm.de/x` → all **refused** (offline unit test of the handler) |
| size cap | `MAX_IMAGE = 64 MiB`; `r.read(MAX_IMAGE+1)`, over-size → `link=url` | all four images ≤ 39.7 MB → under the cap |
| cache-not-in-lane | `main()` refuses `--cache` / `--image-cache` whose realpath is inside the lane root (fetch-vendor.py:437-444) | both → **exit 2**, `refusing: … is inside the lane (vendor bytes are never committed)`; **no file created in the lane** (checked) |
| pin checks | image sha256, member sha256 (mandatory), carrier pin, `length` bounds (`0 < length <= len(member)`) | 9 of the 16 selftest cases are negative pin checks |
| no temp file in the fetch path | the image is held in memory; only `<pin>.bin.part` is written, inside the cache | — |
| spec resolution | `git -C <root> show <rev>:tools/round-50/carriers.json`; unknown rev → `SystemExit(2)` | measured |

**Fetch exit codes:** 0 = all four materialised and verified; 1 = a chain link
failed; 2 = usage / unreadable spec / lane-resident cache.

---

## 4. What `--selftest` covers (run: exit 0, 16/16)

`python3 -I -B tools/round-50/fetch-vendor.py --selftest` — offline, no network,
no sasquatch, no unblob; the member images are built by the reader's own writer
inside the process.

Cases (name → link on failure):
`nested-green` (0), `nested-writes-carved-bytes` (0), `plain-green` (0),
`bad-url`→`url`, `image-sha`→`image_sha256`, `member-sha-mismatch`→`member_sha256`,
`member-sha-omitted`→`member_sha256`, `member-absent`→`member`,
`nested-sha-mismatch`→`nested_sha256`, `nested-path-absent`→`nested`,
`nested-path-is-symlink`→`nested`, `nested-on-nonsquashfs-member`→`nested`,
`pin-mismatch-whole-member`→`carrier_sha256`, `length-overrun`→`length`,
`nested-pin-mismatch`→`carrier_sha256`, `spec-missing-image-sha`→`spec`.
Final line: `SELFTEST cases=16 pass=16 fail=0`.

**Coverage gap (calibration, worth one line in the C1 claim):** the selftest
injects a `fetcher=fake`, so it never exercises `fetch()` itself — the origin
allowlist, the `MAX_IMAGE` cap, the `--image-cache` reuse path and the lane-cache
refusal are **not** covered by the selftest. Receipts 03-06 above are the
measured substitute; the L1 may want to state that in the C1 claim's
self-test sentence (the claim currently says "fetch-vendor 8" for round 40 and
"fetch-vendor 8" for round 41 — the round-50 count is **16**).

---

## 5. Download volume (HTTP HEAD only — no image bytes downloaded)

| id | Content-Length | MiB | ETag (HEAD) | frozen `notes.http_etag` | match |
|---|---|---|---|---|---|
| g7581 | 32 010 240 | 30.54 | `"66c33b99-1e87000"` | `"66c33b99-1e87000"` | yes |
| g7582 | 32 256 000 | 30.77 | `"66c33c51-1ec3000"` | `"66c33c51-1ec3000"` | yes |
| c6490 | 39 741 440 | 37.91 | `"64f60ee7-25e6800"` | `"64f60ee7-25e6800"` | yes |
| c6430 | 35 911 680 | 34.25 | `"64f6f08b-223f800"` | `"64f6f08b-223f800"` | yes |

Total **139 919 360 B (133.4 MiB)**; cache after carving **109 036 828 B (104.0 MiB)**;
peak disk with `--image-cache` ≈ 237.4 MiB. All four HEAD `Last-Modified` values
also match the frozen `notes`. Disk guard at the time of the pass:
`/fast/scratch/hyaku` 39 % used, 495.3 G free — ample.

---

## 6. The counter's `--carrier-cache` resolution (confirmed by reading the code)

* `pin = (c.get('sha256') or '').lower() or None` — **c1-counter.py:2231**. The
  pin is the carrier entry's own **`sha256` field**, lowercased.
* `fp = os.path.join(carrier_cache, pin + '.bin')` — **c1-counter.py:2242**;
  `raw = open(fp,'rb').read() if os.path.isfile(fp) else None`.
* The fetcher writes `out = os.path.join(cache, pin + '.bin')` with
  `pin = (entry.get('sha256') or '').lower()` — **fetch-vendor.py:205, 266-270**.

⇒ `<pin>` **is** the carrier `sha256` field; the file name is
`<sha256>.bin`, lowercased, and the two programs agree by construction — no
mapping table, no renaming step. The four names are in the fetch-plan table.

Only the `external` branch uses the cache (`cpath` — the committed-lane path —
takes precedence); the frozen spec gives all four carriers an `external` block and
no `path`, so the cache path is the one that runs. Without `--carrier-cache` the
counter scores `carrier_present` false → exit 1 (the counter's own selftest
asserts this: `add('four external carriers, no --carrier-cache', …, want_fail='carrier_present')`).

---

## 6b. The cache is already materialised and it verifies green

At 2026-10-29 17:31 another actor (not this seat — the seat never wrote there)
ran the fetch into the plan's own paths. Re-hashed read-only (receipt
`11-materialised-cache-verified.json`, exit 0, stdout sha256
`da52815f6d1f34696fcc83e8ea26cd949b2ee96bc8fe32ecb526bd82a882abab`):

| file | bytes | sha256 == frozen pin? |
|---|---|---|
| `carrier-cache/968d997d…6845.bin` | 28 368 210 | yes (= `g7581` carrier pin) |
| `carrier-cache/a119b644…5bd0.bin` | 28 607 082 | yes (= `g7582` carrier pin) |
| `carrier-cache/880370e7…f2d7.bin` | 28 200 029 | yes (= `c6490` carrier pin) |
| `carrier-cache/da1c8049…b46f.bin` | 23 861 507 | yes (= `c6430` carrier pin) |
| `images/42f1dea0…b779.image` | 32 010 240 | yes (= `g7581` `image_sha256`) |
| `images/468f8f4a…6659.image` | 32 256 000 | yes (= `g7582` `image_sha256`) |
| `images/f518ce6b…ede6d.image` | 39 741 440 | yes (= `c6490` `image_sha256`) |
| `images/52e3687d…d815.image` | 35 911 680 | yes (= `c6430` `image_sha256`) |

Every file name is exactly the `<sha256>.bin` / `<image_sha256>.image` form this
plan predicted, every byte count matches the HEAD `Content-Length` and the
frozen `length`, and every hash equals the frozen pin ⇒ the **whole chain
(url → image sha256 → member sha256 → carve length → carrier sha256) is green
for all four carriers**, and the vendor origin still serves the pinned bytes.
The L1 does **not** need to re-fetch; `--carrier-cache
/fast/scratch/hyaku/kaidoku-r50/carrier-cache` can be passed as-is.

---

## 7. Risks / notes for the L1

1. **The blocker above is the only thing that stops the round.** Fix the C3
   instrument path (options 1+2 in §2) *before* the C3 freeze commit.
2. `fetch-vendor.py` verifies **hashes only**. The superblock contract
   (`hsqs` / v4.0 / xz / `mkfs_time == bytes_used`) is checked by the counter's
   `layout_probe` on the fetched bytes and by `c1-run.sh oracle` — a green fetch
   is not a green layout.
3. The carve must be exact: `carve_ok` wants
   `external.length == bytes_used == len(file)`. The frozen table's `length`
   equals the member's `bytes_used` for all four (pad dropped: 694 / 3 486 /
   939 / 1 797 B), so the fetcher's carve is correct by construction — verify
   with `ls -l` after the fetch.
4. `--image-cache` is worth passing: it turns a retry from 133 MiB of downloads
   into zero.
5. `c1-run.sh after` requires `--data-run`; its scratch base must contain a
   `/kaidoku-r50/` segment and start with `/fast/scratch/hyaku/kaidoku-r50/`
   (`C1_ALLOW_FOREIGN_SCRATCH=1` downgrades this — do not use it for the data run).
6. The four round-50 pins are **not** in `tools/round-42/prior-pins.json`
   (the only prior-pins table present at the freeze), so `carrier_fresh_ok`
   holds; `tools/round-50/prior-pins.json` and `tools/round-49/prior-pins.json`
   are absent at the freeze and are skipped.
7. Nothing was installed or upgraded for this seat (no pacman, no `uv tool`, no
   `npx`); only `python3` (stdlib), `curl` and `git` were used, all pre-installed.

## 8. Artifacts

* `.ufo/waves/round-50/w3/ExecFetchDry/fetch-plan.md` — the exact commands.
* `.ufo/waves/round-50/w3/ExecFetchDry/receipts/01…11-*.json` — 14 receipts
  (argv, exit code, stdout/stderr sha256, UTC start/end).
* `.ufo/waves/round-50/w3/ExecFetchDry/receipts/run_receipts.py`,
  `receipts/fixture_drift.py` — the generators (re-runnable).
* Scratch `/fast/scratch/hyaku/kaidoku-r50/w3-ExecFetchDry` removed after the
  receipts were copied here (the fixture clone went with it).
