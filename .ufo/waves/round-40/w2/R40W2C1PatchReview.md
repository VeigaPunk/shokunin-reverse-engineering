# R40W2C1PatchReview — DEFECTS FOUND (none flip the C1 landing; all fail-closed or latent)

Attacked: the L1's pre-freeze patch to `tools/round-40/c1-counter.py` (diff of the wave-1 artifact
`.ufo/waves/round-40/w1/artifacts/R40C1Counter/c1-counter.py` against
`git show 7fce308631a8b457d6b7c5a4b39a923c4e9a49de:tools/round-40/c1-counter.py` — external carriers
via `--carrier-cache`, `carriers_spec` external keys, `FROZEN_PATHS` additions), plus the L1-authored
`tools/round-40/fetch-vendor.py` and `tools/round-40/c1-extra.py` for correctness and selftest
adequacy. The three seat questions — pin checked on external bytes? missing cache silent pass? stale
selftest case? — all come back clean; the defects found are an unclassified crash path, a selftest
coverage hole for the patched machinery, and minor fetch-vendor robustness/contract gaps.

## Patch provenance and shape

- The counter was first committed **at the freeze**: `git log fa6a8a3f..7fce3086 -- tools/round-40/c1-counter.py`
  → only `7fce3086`; `git log -S carrier_cache …` → only `7fce3086`. The w1 artifact is the pre-patch
  draft; the patch (91 diff lines, 5 hunks: `FROZEN_PATHS`, `carriers_spec`, `measure`, argparse,
  main call) went straight into the freeze commit. Artifact: `artifacts/R40W2C1PatchReview/patch.diff`.
- Working-tree counter is byte-identical to the frozen version (sha256 `8d288e4cf203d745…` both) — the
  frozen path is untouched through tip `4d62ee5a`.
- Patch content: (1) `FROZEN_PATHS` += `c1-extra.py`, `c1-run.sh`, `fetch-vendor.py`, `sqfs-list.py`,
  `gen-squashfs.py`, `mk-l-carriers.py` — exactly the claims file's C1 frozen-path list (7 tools +
  claims file + `carriers.json` + `gap-rule.json` + spec-named carrier/oracle/nonregular paths);
  (2) `carriers_spec`: external carriers drop the `path` requirement, require
  `external{url,image_sha256,member,length}`, 64-hex `image_sha256`, reject `path`+`external` together;
  (3) `measure()`: cache branch `fp = <carrier_cache>/<pin>.bin`; (4) `--carrier-cache` flag.

## Q1 — Is the pin still checked on externally loaded bytes? **YES (confirmed)**

- Code: `carrier_pin_ok = sha256(raw) == pin` is computed after both branches
  (`frozen-c1-counter.py:1036-1038`), so cache-loaded bytes go through the same pin check, the same
  `layout_probe(raw)`, the same rerun (`runner(raw, k, params)` gated on `carrier_pin_ok`), and the
  receipt's `subject_pin_ok` must equal the same pin.
- Empirical: a cache file holding 4096 random bytes at V1's pin filename → `carrier_present: true`,
  `carrier_pin_ok: false`, `layout_ok: false`, projection skipped → exit 1
  (`artifacts/…/exp-junk.json`).
- Real data: `fetch-vendor.py --root <lane> --rev 7fce3086 --cache …` reproduced the whole chain over
  HTTPS for both vendor carriers — image sha256 `f518ce6b…ede6d` / `3948449d…9450`, full-member sha256
  `334e56df…f3d4` / `cacc6461…4b19`, carve 5442392 / 26013550 bytes, carrier pins `ac4098bd…8e95` /
  `5ccc7614…089b`, exit 0 (`artifacts/…/fetch.json`; vendor bytes kept in scratch, deleted after,
  cited by sha256 only).

## Q2 — Can a missing cache silently pass? **NO (confirmed fail-closed)**

- Code: missing `<pin>.bin` → `raw = None` → `carrier_present: false`, `carrier_pin_ok: false`,
  `projection_skipped` → `carriers_matched < 4` → exit 1. Omitting `--carrier-cache` entirely takes the
  same `else: raw = None` path (`elif … and carrier_cache and pin:` is False).
- Empirical (sandbox clone at `42c10a58`, empty cache dir): exit 1; V1/V2
  `carrier_present=false`/`carrier_pin_ok=false`/`layout{reason: absent}`; L1 still matched (its real
  REA rerun ran and matched, `projection_ok: true`), L2 fails `nonregular_unpublished_ok` exactly as at
  scoring → `carriers_matched: 1`, `met_target: false` (`artifacts/…/exp-empty.json`).

### D1 (moderate) — an unreadable (not missing) cache file crashes the counter into an unclassified exit 1

- A cache file that exists but cannot be opened (chmod 000) hits the unguarded
  `open(fp, 'rb').read()` in the cache branch → uncaught `PermissionError` → bare traceback, **exit 1
  and no `--json-out` written** (`artifacts/…/exp-noperm-traceback.txt`; `exp-noperm.stdout` is 0
  bytes). Under the receipt discipline (R39-CL6 records the scorer's exit code) an exit 1 without a
  receipt is ambiguous with the honest-stop exit 1. It can never produce a false pass, but the failure
  is unclassified; `RerunEnvError`→exit 2 is the pattern the counter already uses for environment
  failures. The same unguarded `open(fp, …)` sits in `c1-extra.oracle_rederived`.
- Fix direction: wrap the cache read → `Unevaluable` (exit 2), or a clean carrier clause failure with a
  note; same for `c1-extra`.

## Q3 — Is any selftest case now stale? **NO — but the patch added zero cases (D2, adequacy)**

- The 91-line patch leaves the selftest bytes untouched (no hunk at or below the selftest region);
  rerun today: `{"selftest": "c1-counter", "cases": 70, "green_ok": 5, "red_ok": 65, "failures": []}`,
  exit 0. No case exercises removed behavior; none is stale.
- But no case exercises the **new** machinery either: `external`/`carrier_cache` appear only in
  `carriers_spec`, `measure`, `main` — every selftest spec fixture uses in-tree `path`. Untested by
  `--selftest`: the external spec validation (probe-verified below), the cache load, missing-cache
  fail-closed (my `exp-empty.json`), wrong-cache-bytes (my `exp-junk.json`), and the six new
  `FROZEN_PATHS` drift targets (no drift case writes them). The real scoring run at `42c10a58` did
  exercise the cache branch (V1/V2 `carrier_pin_ok: true` in `c1-at-42c10a58.json`), so the machinery
  is verified in use — but the claims file's "65 red self-test cases" contains no external-carrier red
  case, and a future regression in the cache branch (e.g. dropping the pin check) would not be caught
  by `--selftest`.

### D3 (minor) — `member_sha256` is pinned in the frozen spec but enforced by no tool

- `carriers.json` `external` carries `member_sha256` (V1 `334e56df…`, V2 `cacc6461…`).
  `carriers_spec` requires only `url/image_sha256/member/length` — direct probe on the frozen spec:
  `member_sha256 dropped → probs=[]`, `member_sha256 wrong value → probs=[]`
  (`artifacts/…/probe-spec.out`). `fetch-vendor` computes the full-member sha256 into `member_detail`
  but never compares it to `ext['member_sha256']`.
- Impact: none today — the chain is closed without it (`image_sha256` pins the whole image; `length` +
  carrier pin pin the carve; both member sha256s match on real data). It is redundant documentation
  that reads as enforced. Either enforce it in `fetch-vendor` (one comparison) or drop the key.

## fetch-vendor.py — correctness confirmed on real data; D4/D5 robustness gaps

- Chain enforcement is sound: image sha256 verified (cache hits re-verified by sha256; stale cache
  files fall through to the network — probe-verified), member presence + `isfile`, `0 < length ≤
  len(member)` with type check, carrier sha256 == pin, atomic write (`.part` + `os.replace`), writes
  only under `--cache`. Selftest 8/8 pass (rerun today).
- **D4 (minor): three uncaught-crash inputs** — a sha-consistent non-tar image → uncaught
  `tarfile.ReadError`; `external` missing `member` or `length` → uncaught `KeyError`
  (`artifacts/…/probe-fetch2.out`). All exit 1 (fail-closed) but as bare tracebacks with no JSON
  record, while the docstring promises "Exit: 1 a chain link failed" with a classified `link` and a
  JSON record. Unreachable with the frozen well-formed spec + pinned image sha256; robustness only.
  Also `--spec` pointing at a missing/invalid file → traceback exit 1, not the documented 2.
- Selftest adequacy: no case reaches `carve` with a non-tar image (the fake image always fails
  `image_sha256` first — my first probe reproduced exactly that masking, `probe-fetch.out`), no
  image-cache case (positive hit verified by me: `how='cache'`, 28334080 bytes, sha ok), no
  `--root/--rev` spec-load case.
- **D5 (minor): case-handling inconsistency** — `carriers_spec` accepts an uppercase `image_sha256`
  (`SHA_RE.match(isha.lower())`), but `fetch-vendor` compares `rec['image_sha256'] != ext['image_sha256']`
  without lowering, so an uppercase value would pass spec validation and then break the fetch as an
  `image_sha256` link failure. The carrier `sha256` is lowered in both tools. Frozen spec is lowercase —
  latent only.
- Note: `run()` exits 1 when the spec has no external carriers (codified by the `no-external` case) —
  intended, slightly surprising.

## c1-extra.py — correctness confirmed; same D1 wart, small selftest gaps

- `oracle_rederived`: reader bytes **at the freeze** (`show(root, freeze, READER)`) ✓; carrier bytes
  from the cache with pin check (missing/mismatched → `'carrier bytes absent or pin mismatch'` →
  binding false → exit 1) ✓; row-set comparison against the frozen oracle+nonregular at rev ✓. Real
  data: all four carriers `'ok'` in `c1-extra-at-42c10a58.json` — V1/V2 exercised the cache branch.
- `sourced_new`: cited S-ids from `source:` lines; requires absent-at-base ∧ present-at-rev ∧ used-by
  naming the entry/stem (S124–S126 at `42c10a58`) ✓. `frontier_content`: line-start
  `Round-40 frontier note` + heading + stem + `supersede` — stricter than the main counter's substring
  `frontier_note` binding; both true at `42c10a58` ✓.
- Selftest 7/7 pass (rerun today). Gaps: no external/cache case (cache=None everywhere), no
  reader-drift case (a post-freeze reader edit is caught by the main counter's `frozen_drift`, not
  here), no explicit `entry absent` red case (covered only via `base-has-nothing`).

## Cross-checks that came back clean

- `FROZEN_PATHS` additions match the claims file's C1 frozen-path list exactly.
- Independent drift check: `git log --name-only 7fce3086..42c10a58` and `…..4d62ee5a` → **no frozen C1
  path touched** (only after/run receipts, C2 heldout data, docs, controls).
- `c1-run.sh` has no `--carrier-cache` wiring — correct: it receives carrier bytes as an argument; only
  the two counting commands take the cache.
- `layout_probe`'s plausibility/identity disambiguation resolved all four real carriers (V1 `6405` and
  L1 `a483` via plausibility, V2/L2 `1d83` via identity) — consistent with the selftest's ambiguous-length
  cases.
- Selftests: c1-counter 70/70, fetch-vendor 8/8, c1-extra 7/7 — all pass at the current tree.

## Limits

- I did not re-run the full four-carrier scoring with a correct cache (the L1's receipt at `42c10a58`
  plus the refreeze seat cover it); my counter runs used sandbox clones at `42c10a58` with
  empty/junk/unreadable caches.
- Vendor bytes/images/cache lived only in scratch and were deleted; cited by sha256 only.
- The uncaught-exception probes used synthetic inputs; with the frozen well-formed spec they are
  unreachable except the unreadable-cache case (environmental).
- No tools were installed or upgraded (python3/git/npx-cached rea-agents@6.5.0/unblob/sasquatch-v4be as
  provided; pacman untouched per the host guard).

## Evidence index (`.ufo/waves/round-40/w2/artifacts/R40W2C1PatchReview/`)

`patch.diff` (frozen vs w1 draft), `exp-empty.json` (missing-cache run), `exp-junk.json`
(wrong-bytes run), `exp-noperm-traceback.txt` (D1 crash), `probe-spec.py/.out` (carriers_spec
external probes incl. D3), `probe-fetch.py/.out`, `probe-fetch2.py/.out` (D4 crashes, image-cache
behavior), `fetch.json` (real vendor chain record).
