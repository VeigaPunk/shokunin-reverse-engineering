# SentReceipts — security review of the round-50 attempt-2 receipt path

**Verdict: 2 FINDINGS (one Medium, one Low), both at the tip; the tip credential surface is CLEAN.**
Credential-class material: **0 live hits** in the attempt-1 evidence this attempt re-uses and in the
whole round-50 wave tree. `tools/round-50/fetch-vendor.py` containment: **6 of 7 controls PASS**;
the one partial (lane-cache refusal) is CLI-only and self-relative. The `.gitignore`/`.gitattributes`
gap is real but low-severity (it needs a lane-resident path, which the fetcher blocks on its CLI path).

Seat artifacts: `.ufo/waves/round-50/w3/SentReceipts/` — `credscan.py`, `containment-diff.sh`,
`redirect-repro.py`, `redirect-real.py`, `mkfixture-drift.py`, `credscan-attempt1.json`, `receipts/`
(18 receipts, each with cmd / exit / stdout sha256 / UTC start+end). Nothing was written outside the
seat dir; no vendor bytes remain in the lane (verified twice); no REA run; no git mutation.

---

## Findings table

| # | Sev | Finding | File:line | Repro (one command) | Result |
|---|-----|---------|-----------|---------------------|--------|
| **F1** | **Medium** | **The frozen counter's operator-facing text names the UNHARDENED fetcher.** `tools/round-50/c1-counter.py` is frozen and its `--carrier-cache` help, its docstring, and its frozen-file map all point at `tools/round-41/fetch-vendor.py` — which has **no** origin allowlist, **no** redirect policy, **no** size cap and **no** lane-cache refusal. The hardened `tools/round-50/fetch-vendor.py` (allowlist + redirect + 64 MiB cap + lane refusal) is the file the *plan* names, but the instrument an operator reads says otherwise. An L1 that runs the file the counter names fetches from any origin and can write vendor bytes into the lane. | `tools/round-50/c1-counter.py:938` (docstring), `:2522-2524` (`--carrier-cache` help), `:415` (`FROZEN_PATHS`), `:3009` (frozen-file map), `:4262` (mutation fixture) | `bash .ufo/waves/round-50/w3/SentReceipts/containment-diff.sh` (case B) | round-41 fetcher: `file://` URL **ACCEPTED**, exit 0, carrier materialised. round-50 fetcher: **REFUSED**, exit 1, nothing written. See `receipts/r09-containment-diff.stdout` (sha256 `6bde4d18e9677adfc07a30b63f5f49759e6227431937d1de86a109bc0ab3aea3`) |
| **F2** | **Low** | **No `.gitattributes` anywhere in the lane; `.gitignore` covers only `__pycache__/` and `*.pyc`.** A dropped `.image`/`.bin`/`.sqsh` anywhere in the lane tree is **not** ignored and **is** staged by `git add -A`. No LFS is active (global `filter.lfs.*` is configured, but LFS only engages via `.gitattributes`, which does not exist), so such a file lands as a raw blob. This is a last-resort net only: it does not stop a write, it only fails to stop the commit. | `.gitignore:1-2` (whole file, 2 lines) | `D=$(mktemp -d); git -C $D init -q; cp .gitignore $D/; cd $D; mkdir -p tools/round-50; printf V > tools/round-50/x.image; git add -A --dry-run` | `add 'tools/round-50/x.image'` — **not ignored**; `git check-ignore` exit 1. Also reproduced in the live lane: a `probe.bin` in the seat dir showed as `?? ` and was not ignored. See `receipts/r14-gitignore-probe.stdout` (`de9175851fba14d349ef9e34e273ec0c20743e1c7e32e84d68343687e44181b2`), `receipts/r15-lane-residency.stdout` (`e098dc642cbaf37bccfa31d9d692efb85ff1f3d8b02ec2d25f4354bc036bd5c1`) |

---

## (1) Credential-class scan of the re-used attempt-1 evidence — CLEAN

Scope named in the seat spec: `.ufo/waves/round-50/w1/C1Src*` receipt dirs and `.ufo/waves/round-50/l1/`.
Scanner `credscan.py` is **calibrated**: it reports a value as `live` only if the value part is ≥6
chars, has no whitespace/`;`, and is **not** a redaction placeholder (`[redacted …]`, `<REDACTED>`).
Placeholders and synthetic scanner self-test fixtures are counted in separate buckets so the two
classes never blur. 11 credential classes: `set_cookie`, `cookie_hdr`, `authorization`, `x_api_key`,
`github_token`, `github_pat`, `bearer`, `op_ref`, `aws_key`, `sk_key`, `private_key`, `jwt`.

| Scope | files | bytes | **live** | placeholders | synthetic |
|---|---|---|---|---|---|
| `w1/C1SrcAvmIndex` + `w1/C1SrcFreetz` + `w1/C1SrcUnblob` + `l1/` | 81 | 338 036 | **0** | 0 | 0 |
| whole `.ufo/waves/round-50/` tree | 1358 | 27 053 670 | **0** | 0 | 0 |
| `.ufo/waves/round-50/w3/` (this wave, in-flight) | 269 | 5 161 479 | **0** | 0 | 0 |

Commands and sha256s: `receipts/r01-credscan-attempt1` (`3742f051ede075ac5a63bfda569c0219b8f846e61eb16a96c448a198eca9b43d`),
`r02-credscan-round50-tree` (`b5e326f2082be0a3f54b753368042cf2495875eee24e302a96380959fc0c91ce`),
`r03-credscan-w3-tree` (`9ac6bed9418443f0825542237540b0486abc41d29d21bef61ce743a9372be3c2`).
Exit 0 = no live hit.

Corroborating checks:
- Every one of the 16 `*.hdr` receipt files in `w1/C1Src*` was grepped for
  `^(set-cookie|cookie|authorization|proxy-authorization|x-api-key):` → **0 lines each** (16/16).
  The AVM/Freetz headers carry only `server/date/content-type/content-length/last-modified/etag/accept-ranges`.
- `SHA256SUMS` in `w1/C1SrcAvmIndex/receipts/` verifies clean: `sha256sum -c` → exit 0, 22 files OK, 0 mismatches.
- HEAD tree, live-value form: `git grep -nPI '(?i)(set-cookie:\s*_gh_sess=)(?!\[redacted)(?!<REDACTED)[^;\s]{8,}' HEAD -- .`
  → **exit 1, no output** (`receipts/r04-headtree-live-cookies.stdout`, empty). Same for `_octo`.
- Entropy sweep for *unlabelled* long opaque tokens over the re-used scopes: 258 hits, **all** inspected
  and all are paths, env-var names or sha256/git-sha pins (e.g. `REA_UNBLOB_COMMA`, `/fast/scratch/hy…`).
  No unlabelled secret.

### The round-45 precedent: redaction at the tip is intact; **history is still unpurged** (L0, unchanged)

The tip is redacted (`git show HEAD:…/f1.hdr` line 15 → `_gh_sess=[redacted by L1 round 50: cookie value]`).
The **unredacted blobs are still in the object database and still reachable**:

| blob | file | reachable from | live value still extracts |
|---|---|---|---|
| `ba6b0d6e…` | `.ufo/waves/round-45/w2/R45W2S138Top/receipts/f1.hdr` | `ef3edf4b` (**ancestor of HEAD**) | **353 chars** (`r05`, sha `788a375d5055941786dd7e62bb7be0e986ad858a9b1cc84033fcf295634a9cf4`) |
| `5f8478b4…` | `.ufo/waves/round-49/w1/C1CarrierPins/receipts/tree.hdr` | `14936cb9`, `5855962d` (**both ancestors of HEAD**) | **349 chars** (`r06`, sha `e11e6079110680dbfcebe02b69f00171df4e71bdd97ff8b23599db0038721eff`) |
| `815e2951…` | `.ufo/waves/round-49/w1/C1S138Reopen/receipts/top.hdr` | same range | 365 chars |

`git log --all --find-object=ba6b0d6e…` → 6 commits (`r07`, sha `7eef17c41a509662a3c088fa6037d8f1b9c5dc5a7a12dc1c565cf84be5a67d54`).
A plain `git clone` of the lane carries these: I cloned `--shared` at the base and `git show
ef3edf4b:…/f1.hdr` still returned the 353-char value. **This is the known L0 item (M50-5, "history
not purged"), not a new defect** — no seat may rewrite history here. Impact stays low
(`logged_in=no` at capture → anonymous session cookies), but the record should not claim the values
are gone. `corpus/lessons/round-50.md:15` already states this correctly.

## (2) `tools/round-50/fetch-vendor.py` containment — 6/7 PASS, 1 PARTIAL

Base bytes: sha256 `c53221ea9e4ba586552a65cfa3be056a0ab8c792920a8361aca1e13addc3d8a8`, identical at
`f890bbea` (base), at HEAD and in the worktree (`r08`, sha `1f227d10789098bea5baa631b0dba884533d264a22ee4d0ed07f4787c3d7f089`).
The file is inside the frozen prefix `tools/round-50/`, so it is byte-stable.

| Control | Verdict | Evidence |
|---|---|---|
| origin allowlist exactly `https://download.avm.de` | **PASS** | `fetch()` gate (`tools/round-50/fetch-vendor.py:111-113`) rejects `file://`, `http://`, other hosts, suffix hosts (`download.avm.de.evil.example`), trailing-dot host, and userinfo tricks (`https://download.avm.de@evil.example/x` → `hostname=evil.example` → BLOCKED). All 4 `carriers.json` URLs are `https://download.avm.de/...` (`r18`). |
| no `file://` | **PASS** | `ValueError` raised before any open; `FileHandler` exists in the opener but is unreachable via `fetch()`. Differential: round-50 **refused** (`link=url`, exit 1), round-41 **accepted** (`r09` case A vs B). |
| cache refuses a lane-resident path | **PARTIAL** | CLI `main()` refuses (`fetch-vendor.py:433-438`): lane root, lane root itself, `lane/.`, and a symlink→lane all → exit 2 "refusing: --cache is inside the lane". **But** (a) the refusal lives only in `main()`; `run()`/`materialise()` have no lane check, and (b) the lane root is derived from the *script's own location* (`__file__`'s grandparent-parent), so a copy of the tool placed outside the lane computes a different root and refuses nothing. Proven: `fv.run(spec, <lane path>, None, fetcher=stub)` wrote a `.bin` **into the lane tree** (exit 0) — in-lane tool and out-of-lane copy alike. |
| TLS verification on | **PASS** | No `CERT_NONE` / `create_unverified_context` in source; default `HTTPSHandler`; default context `verify_mode=2` (CERT_REQUIRED), `check_hostname=True`. Empirical: a self-signed TLS server on loopback → `SSL: CERTIFICATE_VERIFY_FAILED`. |
| redirect handling | **PASS** | `_AvmOnlyRedirect` (`:99-107`) replaces the default handler (verified: the default `HTTPRedirectHandler` is absent from the opener). 301/302/303/307/308 to another host, to `http://`, and to a suffix host are all **refused**; same-host is allowed (`r11`, sha `6eaf2f4023c464806f5190bccfd43b1d62603f423d70d48fc3dc13d79c0192d5`). |
| no header persistence | **PASS** | `fetch()` reads only `r.status` and `r.read(...)`; it never touches `r.headers`; no `Set-Cookie`/`Authorization` is captured, stored or written anywhere in the module. The 18 attempt-1 `.hdr` receipts confirm the pattern at the receipt level too. |
| size cap | **PASS** | `MAX_IMAGE = 64 << 20`; `r.read(MAX_IMAGE + 1)` then `if len(b) > MAX_IMAGE: raise` (`:124-126`). |

Two residual gaps inside the PASS verdicts, both recorded as **informational** (not findings):
- The allowlist is **host-only, not origin**: `https://download.avm.de:8443/x` passes both the fetch
  gate and the redirect handler (same host, non-default port). TLS still verifies, so impact is
  limited to "a different service on the vendor host's port 8443", which AVM does not expose.
  Smallest fix: also compare `u.port` against 443/None.
- `os.path.realpath` on the lane root means a *sibling* directory that merely shares the lane's
  name prefix is not falsely refused; confirmed no false positive.

**Differential vs the file the counter names** (`receipts/r09-containment-diff.stdout`,
`sha 6bde4d18e9677adfc07a30b63f5f49759e6227431937d1de86a109bc0ab3aea3`):

| case | round-50 fetcher | round-41 fetcher (named by the frozen counter) |
|---|---|---|
| A `file://` URL | exit 1, `link=url`, nothing written | **exit 0, carrier materialised** |
| B cross-origin 302 (loopback → loopback) | **REFUSED** (`ValueError`, allowlist) | **ACCEPTED** — 10 240 bytes returned and accepted (`how=http 200`) |
| C cache inside the lane | exit 2, refused | **exit 0, `.bin` written into the lane tree** |
| D same-host redirect | allowed (correct) | allowed |

`receipts/r10-redirect-repro.stdout` (sha `8e759e0d5c7d528c793026ca9d8b4120bfc0563c4209dd87275c104df703252c`)
is the standalone cross-origin redirect exploit: two loopback origins, no internet.

**Why F1 is Medium and not Low.** The unhardened round-41 fetcher is still in the tree, still
referenced by a frozen instrument's user-facing help, and the round-41 carrier spec
(`.ufo/waves/round-41/c1/carriers.json`, both URLs `https://download.avm.de`) is still present.
An operator who follows the counter's own `--help` gets a fetcher that will follow a redirect to a
second origin and will write vendor bytes into a lane-resident cache. The plan and the attempt-2
claims already point at the hardened tool (`plans/round-50-attempt2-claims.md:42`), so the exposure
is operator-error-shaped, not remote. **Smallest remediation:** none inside the frozen counter
(editing it trips `frozen_path_changed`); instead record it in the round-50 lesson + the L1's
runbook so the data run explicitly invokes `tools/round-50/fetch-vendor.py` and never
`tools/round-41/fetch-vendor.py`.

## (3) `.gitignore` / `.gitattributes` — F2 above; scope confirmed

- `.gitignore` is 2 lines: `__pycache__/`, `*.pyc`. No `.gitattributes` exists anywhere in the
  working tree (`find . -name '.gitattributes' -not -path './.git/*'` → empty; `git ls-tree -r HEAD`
  → 0 matches). Global `filter.lfs.*` is configured at `~/.config/git/config` but LFS only engages
  through `.gitattributes`, so it is inert here.
- Nothing in the lane currently drops a `.image`/`.bin` into the tree: 247 untracked files, largest
  is a 68 KB HTML receipt; no untracked file matches `\.(image|bin|rom|img|fw|squashfs|sqsh|gz|tar)$`.
- Committed `.bin` files exist only under `corpus/evidence/round-34/elf/` and the arc3 evidence trees
  — lane-built artefacts, not vendor bytes. The one AVM-derived artefact in the tree is
  `tools/round-50/control-fixtures/c4/overlay/…carrier.sqsh.gz`: 70 482 bytes, sha256
  `20b706241f8f9aa9048117cb741e477fe3c5263aae2392b31ec3fb49f6c09e92`, which matches **none** of the
  four vendor carrier pins — it is a mutated control fixture, not vendor bytes.
- `corpus/evidence/round-50/c1/g7581/after.json` (2.1 MB, landed by the L1's data run during this
  wave) contains **no** base64/binary content field: 4 556 file entries, keys are
  `path/relative_path/sha256/size/mime_type/…` only, no `content`/`bytes`/`blob` key. So the receipt
  carries hashes and paths, not vendor file contents. Verified against a committed round-42 envelope
  for the same shape.

---

## Pre-freeze attacks run against the *attempt's* own C3 land-path (calibration for the L1)

Not part of the seat's three numbered items, but it is a receipt-path fact the L1 needs before
committing the C3 freeze, so it is recorded here with a repro rather than in prose.

- The C1 counter's frozen-prefix set is `FROZEN_PREFIXES = ('tools/round-50/',)` **and**
  `FROZEN_PATHS` contains `tools/round-41/fetch-vendor.py` and `tools/round-41/sqfs-list.py`.
  Fixture-clone measurement (`receipts/r16-c3-path-drift.stdout`, sha
  `493b3536a4e2a366c717bbb2d45174abf8ccccbb7a9f495b1e32bc5eea178ae7`):

  | instrument land path | `frozen_drift` | C1 exit would be |
  |---|---|---|
  | `tools/round-50/sqfs-triage-v5.py` | `['tools/round-50/sqfs-triage-v5.py']` | **2** (`frozen_path_changed`, never met) |
  | `tools/round-50-c3/sqfs-triage-v5.py` | `[]` | **0** |

- **The plan is already right and the wave-3 seat prompts are not.** `plans/round-50-attempt2-claims.md:63,75,99`
  names `tools/round-50-c3/sqfs-triage-v5.py` and says why (`:66-70`). But the wave-3 dispatch spec
  still names the **frozen-prefix** path `tools/round-50/sqfs-triage-v5.py` for three seats —
  `ExecTriageV5`, `ExecRegistryRow`, `ConnCrossClaim` (3 of 35 wave-3 seats; measured from
  `.ufo/waves/round-50/w3-spec.json`). A seat that follows its prompt lands the instrument where C1
  must reject it.
- The B9 registry census reads `git ls-tree -r REV -- tools/round-50`, and git's pathspec does **not**
  match `tools/round-50-c3/` (verified: `match-count=0`, and the fixture's
  `in_b9_census_tools_round-50: false`). So the outside path needs **no** B9 row for the census
  greenness, while the claims' "no other `.py`/`.sh` lands under `tools/round-50/`" stays satisfied.
  The claims also ask for exactly one registry row for the new file; B9 only iterates the *census*
  paths and does not flag rows for non-census paths, so one row for `tools/round-50-c3/…` is harmless
  and one for `tools/round-50/…` is not.
- Repro: `python3 -I -B .ufo/waves/round-50/w3/SentReceipts/mkfixture-drift.py` (fixture clone,
  `git init` + `rev-parse --show-toplevel` asserted, throwaway identity in that clone only).

---

## Checks run, and checks NOT run

**Run (offline, no REA, no network to the internet):**
`fetch-vendor.py --selftest` → 16/16 PASS, exit 0 (`r12`, sha `828a9add44cff9e88dc7751bd290d981ba040eff20bb25a09666d9dad34804ec`).
`c1-counter.py --selftest` → 169 cases, green_ok 17 / red_ok 152, exit 0 (`r13`, sha
`355750701b21cf82ad5bd06d7cd58756556e08b20bc90b3e654a19989fd39523`).
Containment differential, redirect exploit (loopback only), redirect-policy probe, TLS probe
(self-signed loopback), credential scans ×3, HEAD-tree live-cookie grep, blob reachability,
gitignore probe, lane-residency probe, C3 land-path drift fixture.

**NOT run (and therefore not claimed):**
- No REA invocation of any kind (contract: the L1 alone runs REA, after this wave).
- No download from `download.avm.de`; no carrier materialised from a real vendor image.
  The two loopback HTTP(S) servers in the redirect/TLS probes are 127.0.0.1 only.
- No `--data-run`; no write into `corpus/evidence/`; no fixture inside the lane tree.
- **No live credential value was reproduced in any receipt.** Where a length was material it is
  reported as a character count; no value is quoted. Every value-bearing probe used synthetic
  local bytes.
- I did **not** re-measure the C1 data run or the C1/C2 controls; those are the L1's, post-wave.
- The round-45/round-49 history purge was **not** attempted (no mutating git; operator decision).

## Bounds honoured

Lane read-only except my seat dir + this report; no commit/push/stage/stash; no write to the lane's
`tools/`, `plans/`, `corpus/`, `SKILL.md`, `PROVINCE.md`, `LOG.md`, `SCORECARD.md`, `SHONEN.md`; no
fleet-repo write; no sibling lane touched; no `agent://all` broadcast; scratch
`/fast/scratch/hyaku/kaidoku-r50/w3-SentReceipts` used and removed at yield after the receipts were
copied in; nothing written under `/tmp` (all probe fixtures were `mktemp -d -p "$S"`).
**Tooling: nothing installed, upgraded or moved** — python3 (stdlib) + git (read-only verbs) +
openssl (certificate generation for the TLS probe, in scratch only) only; `pacman` untouched.
