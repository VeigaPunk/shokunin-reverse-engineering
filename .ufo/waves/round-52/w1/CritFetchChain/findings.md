# CritFetchChain — attack on the round-52 carrier re-fetch chain

Seat: CritFetchChain (critic). Round 52, wave r52-w1, attempt 1.
Scope: `tools/round-50/fetch-vendor.py`, `tools/round-50/carriers.json`, the
`plans/round-52-claims.md` data-run bullet. Read-only on the lane tree.

## Target under attack

The round-52 claims' data-run bullet (`plans/round-52-claims.md:154-160`) says:

> `tools/round-52/fetch-vendor.py` re-fetches each carrier through the pinned chain
> (vendor image URL → member extraction → member pin verification) into
> `/fast/scratch/hyaku/kaidoku-r52/carrier-cache/` (vendor bytes never committed;
> **the round-50 cache no longer exists and no cached byte is trusted without its pin**),
> then `tools/round-52/c1-run.sh after --id <id> --carrier <CACHE>/<pin>.bin --data-run`
> per carrier … If the fresh run reports `carriers_matched < 4`, the claim is missed as
> frozen — honest stop.

The chain that must produce those bytes is `tools/round-50/fetch-vendor.py`
(`url → sha256(image) → tar member → sha256(member) → carve length → sha256(carrier pin)`
→ `CACHE/<pin>.bin`), consumed by `tools/round-50/c1-counter.py` via
`--carrier-cache` (`c1-counter.py:2239-2243`, read as `<pin>.bin`).

Everything below is measured against the **round-50 fetcher, which is the file the
round-52 claims say is re-landed** (`plans/round-52-claims.md:74`:
`tools/round-52/fetch-vendor.py` "(with the network-guard selftests the routed defect
demands)"). The counter side is the round-50 counter, which the claims say the v2
counter ports (`plans/round-52-claims.md:72`).

**Verdict: the chain's hash discipline is sound (F0 below), but the chain is NOT
fail-closed in the sense the claims assert. Three defects allow the data run to be
green while the bytes are not what the receipt says they are, and one of them
defeats routed defect 4 outright.**

---

## F0 — (holds, no defect) The hash chain itself is correctly ordered

The two questions the task asks about the *order* of the pin stages are answered
correctly, and I confirmed both by execution rather than by reading:

* **Image sha256 IS verified before member extraction.** Probe P3
  (`probe-evidence-2.py`, `probe-results-2.json`): with `image_sha256 = 0*64` and a
  fetcher that returns a perfectly valid tar, the run exits 1 with
  `link=image_sha256` and **`tar_member` was called 0 times**. So an AVM
  re-publish of a changed image fails closed *before* any member is read.
* **The member sha256 IS verified before the carve**, and the carve length is
  verified against the carrier pin after it (`fetch-vendor.py:217-257`). The
  round-50 selftest's 16 cases already cover each link independently; my
  mutants D/E/F (delete the image-sha / member-sha / carrier-pin comparison)
  each turn the selftest **red** — `SELFTEST cases=16 pass=15 fail=1` (D, E) and
  `pass=14 fail=2` (F). So the *hash* links are genuinely able to fail and are
  genuinely covered.
* **The member extraction does not touch device nodes and needs no privilege.**
  `tar_member()` opens the tar with `tarfile.open(fileobj=…, mode='r:')` and calls
  `tf.extractfile(m).read()` — an in-memory read of one regular member
  (`m.isfile()` is checked first). There is no `extractall`, no `extract`, no
  `mknod`, no fifo, no socket, no disk write anywhere in the fetcher (verified by
  grep and by a synthetic tar containing a `CHRTYPE` and a `FIFOTYPE` member:
  both are `isfile() == False` and are simply skipped). So task item (3) —
  "does extracting the outer container hit device nodes/fifo rows (privilege)?"
  — is answered **no**: the outer container is a tar read in memory, and the
  SquashFS member is never *extracted* by the fetcher at all (it is carved
  bytes). The device-node question belongs to the counter's oracle arm
  (`unsquashfs -lln`), which is not this seat's scope.
* **The four vendor images are live and byte-identical to the frozen pins as of
  2026-10-30T11:02:12Z.** All four `image_sha256` in
  `tools/round-50/carriers.json` match a fresh HTTPS GET (HTTP 200, and the
  `Last-Modified`/`ETag` values match the `notes` block of each carrier
  exactly). So the round-52 data run is *feasible*; the drift risk is real but
  currently dormant.

**Therefore: the chain's problem is not the hashes. It is that nothing binds the
bytes in the cache directory to the fetch event, and the network guards are
untested.**

---

## F1 — HIGH — Routed defect 4 is not satisfied: deleting the network guards leaves the selftest GREEN

The routed defect (r51 closure item 4, carried into
`plans/round-52-claims.md:248-251`) requires:

> the repaired copy at `tools/round-52/fetch-vendor.py` gains offline selftests
> proving each guard (https-scheme, pinned-host) fails closed: **guard deleted →
> selftest red**, guards present → green, shown able to fail on fixture inputs.

The round-50 selftest — the file the round-52 copy is ported from — **does not
exercise either guard at all.** The `fake` fetcher used by every selftest case
(`fetch-vendor.py:326-331`) replaces `fetch()` wholesale, so `fetch()`'s
`u.scheme != 'https' or u.hostname != ALLOWED_HOST` check never runs; and no
selftest case calls `_AvmOnlyRedirect.redirect_request`. The `'bad-url'` case
(`fetch-vendor.py:371`) sets `url='bad://'` and relies on the *fake* fetcher
raising `OSError`, so it tests the fake, not the guard.

Measured (probe `probe-evidence.py`, `probe-results.json`):

| mutant | what was deleted | selftest result | required |
|---|---|---|---|
| MUT-A | the https-scheme + pinned-host check in `fetch()` | `SELFTEST cases=16 pass=16 fail=0`, **rc=0** | **red** |
| MUT-B | the redirect guard in `_AvmOnlyRedirect.redirect_request` | `SELFTEST cases=16 pass=16 fail=0`, **rc=0** | **red** |
| MUT-C | both | `SELFTEST cases=16 pass=16 fail=0`, **rc=0** | **red** |

**Impact.** A round-52 `fetch-vendor.py` that ports the round-50 selftest
*verbatim* would claim to satisfy routed defect 4 while proving nothing: the
mutants that delete the very guards the defect names are all green. This is a
**false-provenance** defect — the receipt would attest "network guards
fail closed" on the strength of a test that never calls them.

**Smallest safe correction.** Add to the round-52 selftest (offline, no
network) two cases that call the *real* guard code paths with a fixture URL and
assert refusal, e.g.:

* a case that invokes `fetch('http://download.avm.de/x', None, want)` and
  expects `ValueError` (scheme guard), and
  a case that invokes `fetch('https://evil.example/x', None, want)` and expects
  `ValueError` (host guard), and
* a case that calls `_AvmOnlyRedirect().redirect_request(req, fp, 302, …,
  'https://evil.example/x')` and expects `urllib.error.HTTPError`.

Each must go red when the corresponding guard line is deleted. Do **not** route
them through the `fake` fetcher — that is precisely the blind spot.

---

## F2 — HIGH — The chain is not fail-closed on a *partial* fetch: a stale `<pin>.bin` survives a failed re-fetch and the counter reads it as a fresh carrier

This is the strongest counterexample available, and it defeats the claims'
sentence "**no cached byte is trusted without its pin**" in the direction that
matters.

Measured (probe P4, `probe-evidence.py` / `probe-results.json`):

```
first (successful) fetch          -> rc=0, wrote <pin>.bin
second fetch, SAME cache dir,
  upstream member changed          -> rc=1, link=member_sha256
stale_<pin>.bin_present            = True
stale_sha_matches_pin             = True
counter would read: carrier_present=True  carrier_pin_ok=True
```

`materialise()` writes the cache entry **only on success** (`fetch-vendor.py:258-263`),
but it never *removes* a pre-existing entry when the chain breaks. So after a
failed re-fetch the cache directory still holds the previous run's
`<pin>.bin`, byte-correct against the pin.

The counter then reads exactly that file (`c1-counter.py:2239-2243`,
`fp = os.path.join(carrier_cache, pin + '.bin')`) and checks only
`carrier_present` (the file exists) and `carrier_pin_ok` (its sha256 equals the
pin). Both are true for the stale file. And the counter binds **nothing** to the
fetch event: there is no fetch-receipt read, no mtime check, no run id
(verified: `grep -n "fetch-attempt\|mtime\|st_mtime\|getmtime"` over
`c1-counter.py` returns nothing).

**Why this is fatal for round 52 specifically.** The claims waive
`carrier_fresh_ok` for exactly these four pins (`plans/round-52-claims.md:79-84`:
"the four pins are listed in the round-52 carrier table's `prior_pins` … the v2
counter honours an explicit, frozen `re_scored_pins` allow-list"). So in round 52
the **only** remaining freshness signal is that the bytes came from *this* run's
fetch — and that signal does not exist. `carrier_fresh_ok` is now `True` by
waiver for all four carriers, `carrier_pin_ok` is true for a stale file, and the
fetch receipt is not consulted. A round-52 data run that never contacted
download.avm.de at all scores identically to one that did.

**Additional confirmation that the "the round-50 cache no longer exists" premise
is only half-true.** The round-50 *carrier-cache* directory
(`/fast/scratch/hyaku/kaidoku-r50/carrier-cache`) is indeed gone, but
`/fast/scratch/hyaku/kaidoku-r50/controls-work/cache-c{1,2,3,4}/<pin>.bin`
**still exist as four symlinks each**, pointing at that removed directory. They
are currently **dangling** (verified: `DANGLING` for all four pins in all four
control dirs) — so they cannot serve bytes today. But they are a live
repopulation hazard: the round-52 cache directory the claims name,
`/fast/scratch/hyaku/kaidoku-r52/carrier-cache/`, does not exist yet, and the
sweep that removed the round-50 cache evidently did not remove the symlink
farm. A sweep that re-creates the target (or any tool that follows them)
restores stale carrier bytes under the exact `<pin>.bin` names the counter reads.

**Smallest safe correction.** Three sub-fixes, all inside
`tools/round-52/fetch-vendor.py` plus one counter clause:

1. **Fail closed on a broken link by removing the stale entry.** In
   `materialise()`, on any `ok=False` return path, `os.remove()` the
   `<cache>/<pin>.bin` entry if it exists (ignoring `FileNotFoundError`). A
   broken chain must leave *no* file the counter can read.
2. **Make the fetch receipt the counter's input.** Emit a per-run fetch receipt
   (the round-50 precedent is committed at
   `.ufo/waves/round-50/l1/fetch-attempt2.json` — 30 tracked files under
   `.ufo/waves/round-50/l1/`, so the precedent is real) and have the v2 counter
   read it: require, for every carrier, a receipt entry with
   `ok == true`, the same `pin`, and a `fetch` value of the form `http <status>`
   — **not** `cache`. A cache-served image is not a re-fetch and must not
   satisfy a "re-fetch" claim.
3. **Bind the receipt to the bytes.** The receipt should carry the UTC time of
   the fetch and the HTTP `Last-Modified`/`ETag` observed (the round-50
   `carriers.json` `notes` already record the expected
   `http_last_modified`/`http_etag` per carrier — see `g7581`:
   `"http_last_modified": "Mon, 19 Aug 2024 12:33:29 GMT"`, `"http_etag":
   "\"66c33b99-1e87000\""` — so the comparison is available). The receipt
   should also assert the observed `Last-Modified`/`ETag` equals the frozen
   `notes` value, so a re-publish is visible as a *named* drift rather than as
   an anonymous sha mismatch.

---

## F3 — HIGH — `--image-cache` makes the whole chain green with **zero network contact**, and the receipt says `cache`

Measured (probe P5, `probe-results.json`): with `--image-cache` primed and the
HTTP opener replaced by a booby-trap that raises on any network access,

```
rc=0  ok=True  fetch='cache'
```

— the entire pinned chain is satisfied **without contacting download.avm.de at
all**, because `fetch()` returns early from the image cache when
`sha256(cached) == want` (`fetch-vendor.py:114-120`). The image cache is keyed by
`want + '.image'`, i.e. by the *expected* image sha256, so it is self-verifying
against the pin — which is exactly why it is dangerous: a cached image is
indistinguishable from a fetched one by content, and the only signal is the
`fetch` field of the receipt, which reads `"cache"` instead of `"http 200"`.

Combined with F2 (nothing reads the receipt) this is the same failure mode from
the other side: **the chain can be satisfied end-to-end without the vendor
being contacted, and no clause in the counter or the claims can tell.**

**Smallest safe correction.** The round-52 fetcher should record the fetch mode
per carrier (`http <status>` / `cache` / `reuse`) and the counter's
carrier-freshness clause should require `http <status>` for the data run — or,
simpler and stronger, the round-52 fetcher should **not offer `--image-cache` on
the data-run path** (or should refuse it unless an explicit
`--allow-stale-image-cache` is passed), so the only way to obtain a carrier is
to contact the vendor. The round-52 cache directory is new
(`/fast/scratch/hyaku/kaidoku-r52/carrier-cache/` does not exist), so this
costs nothing.

---

## F4 — MEDIUM — The URL guard checks the hostname but not the port, and the redirect guard inherits the same hole

Measured (probe P6, `probe-guard-predicate.py`): replicating the guard predicate
verbatim (`u.scheme != 'https' or u.hostname != ALLOWED_HOST`) offline gives

```
PASSES https://download.avm.de/x
refused http://download.avm.de/x
refused https://evil.example/x
PASSES https://download.avm.de:8443/x          <-- non-default port
PASSES https://user:pw@download.avm.de/x       <-- userinfo present
refused https://download.avm.de@evil.example/x
refused file:///etc/passwd
PASSES redirect-> https://download.avm.de:8443/y <-- same hole in the redirect guard
```

`urllib.parse.urlsplit(...).hostname` strips the port, so
`download.avm.de:8443` compares equal to `download.avm.de` and passes. The
redirect guard has the identical predicate, so a redirect to
`https://download.avm.de:8443/y` is also accepted.

Severity is MEDIUM rather than HIGH because the content pin still holds: a
byte-substituted response from any endpoint fails `image_sha256`. But the guard
is not the pinned-origin check the round-50 claims describe
(`plans/round-50-claims.md:48`: "`tools/round-50/fetch-vendor.py` allows
`https://download.avm.de` only"), and with F1 (the guards are untested) and F5
(the redirect handler is the only redirect control — the opener's handler list
contains `_AvmOnlyRedirect` and **no** default `HTTPRedirectHandler`, verified:
`handlers: [... '_AvmOnlyRedirect', 'HTTPErrorProcessor']`,
`redirect-handler count: 0`) this is the *only* origin control in the chain.

**Smallest safe correction.** Compare the **netloc** (host **and** port), not
the hostname, and reject any URL carrying userinfo. Concretely, replace the
predicate with one that requires `u.scheme == 'https'`, `u.hostname ==
ALLOWED_HOST`, `u.port in (None, 443)`, and `u.username is None and
u.password is None` — and use the *same* predicate function for the initial URL
and for the redirect target, so the two cannot drift apart again. F1's selftest
cases must exercise this exact function.

---

## F5 — MEDIUM — One unreadable carrier aborts the whole four-carrier run with no receipt and no per-carrier diagnosis

Measured (probe P7/P11, `probe-results-2.json`): `tar_member()` opens the tar
with `tarfile.open(fileobj=…, mode='r:')` and **does not catch `tarfile.ReadError`**.
A body that is the pinned image but is not a readable tar raises
`tarfile.ReadError: truncated header` straight out of `run()`:

```
P7  UNCAUGHT ReadError: truncated header
P11 cache_dir_after=['e7e0b56e…728.bin']   A_written=True
```

Two consequences:

* **No receipt.** The exception escapes before `main()` writes `--json-out`
  (the CLI path exits with a traceback and `json_out_written=False` when the
  error is raised; when it is raised from `run()` the `--json-out` file is
  never produced at all).
* **A partial cache directory.** In P11, carrier A was materialised and written
  *before* carrier B aborted the run, so the cache dir holds A's
  `<pin>.bin` and nothing explains why B is missing. The counter would read A
  as present (F2's mechanism).

The claims' data-run bullet says "re-fetches **each** carrier through the
pinned chain" and "If the fresh run reports `carriers_matched < 4`, the claim is
missed as frozen". With an uncaught exception there is no per-carrier `link=`
diagnosis and no receipt to read `carriers_matched` from — the L1 gets a
traceback, not a receipt, and cannot distinguish "AVM republished one carrier"
from "my tool crashed".

**Smallest safe correction.** Wrap the `tarfile.open(...)` in `tar_member()`
(and the `tf.extractfile(m).read()`) in `try/except tarfile.TarError`, and
return the existing `(None, 'member %r unreadable: …')` shape so the failure
becomes a normal `link=` value on that one carrier. Then the run continues to
the other three carriers and the receipt records exactly which one broke.
This also makes the "each carrier" wording true.

---

## F6 — LOW — The `.part` write follows a pre-planted symlink (arbitrary-file overwrite)

Measured (probe P8, `probe-results.json`): with `<cache>/<pin>.bin.part`
pre-planted as a symlink to an unrelated victim file, the fetch succeeds
(`rc=0, ok=True`) and the **victim file's contents are replaced by the carrier
bytes**:

```
victim_content_after = 'CARRIERBYTES-1234'
```

`open(out + '.part', 'wb')` (`fetch-vendor.py:260`) follows the symlink, so the
bytes land in the target; `os.replace()` then replaces the symlink itself. The
victim is destroyed and the attack leaves no trace at the cache path.

Severity is LOW in the round-52 context: the cache directory is under
`/fast/scratch/hyaku/kaidoku-r52/`, created fresh by the L1's own run, and the
threat is a local hostile process on the same host rather than the vendor. But
the round-52 claims *explicitly* harden the cache path against the lane
(`fetch-vendor.py:433-438` refuses a cache inside the lane) — the intent is
clearly "the cache path is trusted", and this hole sits exactly there. The
same primitive is a write-primitive into the lane if the lane check is ever
bypassed.

**Smallest safe correction.** Open the part file with
`os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)`
(or refuse to write when the path exists and is not a regular file), and
`os.replace()` from it. One line, no behavioural change on the happy path.

---

## F7 — LOW — A carrier without an `external` key is silently dropped and the run still exits 0

Measured (probe P9, `probe-results.json`): `run()` filters
`if isinstance(c, dict) and 'external' in c` (`fetch-vendor.py:269`), so a
carrier entry that lacks the `external` block is skipped **without any record**:

```
carriers_in_spec=2  recs_emitted=1  rc=0
```

`run()` returns `(recs, 0 if recs and all(r['ok'] for r in recs) else 1)` — with
one surviving carrier that succeeded, `rc` is 0 and the receipt looks like a
clean run. The fetcher never checks that it materialised the table's `target`
count.

For round 52 this matters because the claims say the v2 counter joins
`tools/round-50/carriers.json` to `PRIOR_CARRIER_TABLES` and adds a **round-52
carrier table** whose `prior_pins`/`re_scored_pins` are honoured
(`plans/round-52-claims.md:79-84`) — a new table is being authored, and a
carrier that loses its `external` block during that edit is exactly the failure
this probe models. The counter's own `carriers_spec_ok` would catch a missing
`external` (it requires `url`/`image_sha256`/`member`/`member_sha256`/`length`),
but only for carriers that *are* in the table — and the fetcher runs first, so
the fetcher's own rc=0 would have told the L1 "the fetch worked".

**Smallest safe correction.** After the list comprehension, assert that the
number of materialised records equals the number of spec carriers that have an
`external` block (and that the set of ids matches), and return rc=1 with an
explicit `link='spec'` record naming the dropped carrier otherwise.

---

## F8 — MEDIUM — The claims' round-52 carrier table is referenced but never named as a file, and the counter hard-codes the round-50 path

The claims say the four pins are "listed in **the round-52 carrier table**'s
`prior_pins`" (`plans/round-52-claims.md:80`) and that
"`tools/round-50/carriers.json` joins the v2 counter's `PRIOR_CARRIER_TABLES`"
(line 79). But:

* the claims' **Registry** clause (line 175) says "every new `.py`/`.sh`/`.json`
  instrument under `tools/round-52/` gets exactly one `instrument-registry v2`
  row; **no other code files land there**", and the C2 clause (line 234) repeats
  "no other code files land under `tools/round-52/` beyond the claims' named
  files" — and **no round-52 carrier table is named anywhere in the claims**;
* the fetcher hard-codes `CARRIERS = 'tools/round-50/carriers.json'`
  (`fetch-vendor.py:58`) and `SQFS_LIST` pointing at `tools/round-41/sqfs-list.py`
  (`fetch-vendor.py:59-60`), and the counter hard-codes
  `CARRIERS = 'tools/round-50/carriers.json'` (`c1-counter.py:374`) and
  `PRIOR_CARRIER_TABLES = ('.ufo/waves/round-41/c1/carriers.json',
  'tools/round-49/carriers.json')` (`c1-counter.py:386-387`);
* the counter's spec validator hard-rejects `claim != 'R50-C1'`
  (`c1-counter.py:875-876`, and the gap-rule model likewise at line 793) while
  the claims' rule-grammar clause (line 152-153) says the v2 `gap_rule_model`
  accepts `{R50-C1, R52-C1}` and the frozen round-52 rule carries
  `"claim": "R52-C1"`.

So the round-52 carrier table is a **required, referenced, but unnamed** file.
Two authorities currently claim the round-50 table: the counter reads it as
*the spec*, and (per the claims) it must simultaneously join
`PRIOR_CARRIER_TABLES` — i.e. be read as a *prior-pin source* at the same
freeze. That is only consistent if a **new** round-52 table exists and the
round-50 table is demoted to a prior source. Without the file being named, the
porting seat will guess a path, and the fetch chain will read whichever table
the constant points at — possibly the wrong one, with the wrong `external`
blocks.

**Smallest safe correction.** Name the file explicitly in the claims'
Registry clause (e.g. `tools/round-52/carriers.json`), give it its own registry
row, and have the round-52 fetcher and v2 counter both read it via their
`CARRIERS` constant while adding `tools/round-50/carriers.json` to
`PRIOR_CARRIER_TABLES` in the v2 counter. The round-52 table must carry the
`external` block for all four carriers (url, image_sha256, member,
member_sha256, length) — otherwise the fetch chain has nothing to fetch — and
the `prior_pins` / `re_scored_pins` lists the claims describe.

---

## Summary table

| id | severity | finding | axis | smallest safe correction |
|---|---|---|---|---|
| F0 | — | hash chain correctly ordered; image-sha verified before member extraction; no device-node/privilege exposure in the fetcher; all four vendor images live and pin-matching as of 2026-10-30T11:02:12Z | — | none (keep) |
| F1 | HIGH | routed defect 4 unmet: guard-deletion mutants A/B/C all leave the selftest GREEN | honesty | add offline selftest cases that call the real `fetch()` guard and `_AvmOnlyRedirect.redirect_request` (not the `fake` fetcher) |
| F2 | HIGH | a stale `<pin>.bin` survives a failed re-fetch; the counter reads it as present+pin_ok; nothing binds bytes to the fetch event; `carrier_fresh_ok` is waived for all four pins | honesty | remove the stale entry on any broken link; make the counter read a committed per-run fetch receipt and require `fetch == 'http <status>'` |
| F3 | HIGH | `--image-cache` satisfies the whole chain with zero network contact (`fetch='cache'`) | honesty | record the fetch mode per carrier and require `http <status>` on the data-run path (or drop `--image-cache` for it) |
| F4 | MEDIUM | guard checks hostname only: `download.avm.de:8443` and userinfo URLs pass, in both the initial-URL and redirect guards | honesty | compare netloc (host+port), reject userinfo, use one shared predicate for both guards |
| F5 | MEDIUM | one unreadable carrier raises an uncaught `tarfile.ReadError`: no receipt, no per-carrier link, partial cache left behind | depth | catch `tarfile.TarError` in `tar_member()` and return the existing `link=` shape |
| F6 | LOW | the `<pin>.bin.part` write follows a pre-planted symlink (victim file overwritten) | honesty | `os.open(..., O_CREAT|O_EXCL|O_NOFOLLOW)` for the part file |
| F7 | LOW | a carrier without an `external` key is silently dropped and the run still exits 0 | depth | assert the materialised count/ids match the spec; fail closed otherwise |
| F8 | MEDIUM | the round-52 carrier table is referenced by the claims but never named as a file; the fetcher and counter both hard-code the round-50 path | honesty | name the file in the claims' Registry clause, give it a registry row, point both instruments at it, add the round-50 table to `PRIOR_CARRIER_TABLES` |

**Impacted axes.** F1–F4, F6, F8 hit **honesty** (a green receipt must mean the
guard ran and the bytes came from the vendor this round). F5 and F7 hit
**depth** (the chain must diagnose *which* carrier broke, not abort or drop
silently). None of these touch the device-accounting law itself (F0 confirms
the law's premise is unaffected by the fetch chain: the fetcher never extracts
a filesystem, so it never creates a device node and needs no privilege).

**Do not narrow the claim.** F2/F3 mean that, as designed, a round-52 data run
can report `carriers_matched == 4` without contacting the vendor even once. That
is a defect in the *chain*, not in the round-50 miss diagnosis, and it is
repairable inside `tools/round-52/fetch-vendor.py` plus one counter clause. It
is not a tradeoff the canonical judge should accept: the claims' own sentence
("no cached byte is trusted without its pin") is a promise the current code
does not keep, and the `re_scored_pins` waiver removes the one clause that was
doing the anti-replay work.

## Reproduction

All probes are offline (no network) except the four live vendor GETs recorded
under F0. Scripts and raw results are in this seat directory:

* `probe-evidence.py` — P1 (base selftest), MUT-A/B/C (F1), P4 (F2), P5 (F3),
  P6 (F4), P7 (F5), P8 (F6), P9 (F7), P10 (receipt fields)
* `probe-evidence-2.py` — P3 corrected (F0 image-sha ordering), P7/P11
  corrected (F5)
* `probe-guard-predicate.py` — the offline guard-predicate table (F4)
* `probe-results.json`, `probe-results-2.json` — machine-readable receipts
  (probe name, exact command, exit code, stdout sha256, byte count, UTC time)

Scratch used: `/fast/scratch/hyaku/kaidoku-r52/w1-CritFetchChain` (removed
after copying the receipts into this directory).

The live-vendor liveness check (F0) used the four URLs already pinned in
`tools/round-50/carriers.json` (ALLOWED_HOST `download.avm.de`); the downloaded
bytes were hashed and **not** copied into the lane tree and not retained.
