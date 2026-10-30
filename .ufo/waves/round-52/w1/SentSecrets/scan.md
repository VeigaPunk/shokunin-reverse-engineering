# SentSecrets — inheritance-surface credential scan (round 52, wave 1)

Seat `SentSecrets`. Read-only. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`;
scratch `/fast/scratch/hyaku/kaidoku-r52/w1-SentSecrets` (removed after receipts were copied here).
Tooling: **none installed** — the lane's own calibrated scanner
`.ufo/waves/round-50/w3/SentReceipts/credscan.py` was reused read-only, plus stdlib
`hashlib`/`json`/`re`/`subprocess` and the fleet's own `scripts/sources-census.sh`
(read-only `validate --file` mode). No pacman/`uv`/`npx` transaction; the pacman guard was
never engaged.

## 0. Verdict

**PASS on the credential question. Zero credential material in the inheritance surface.**

* Round-51 wave tree (`.ufo/waves/round-51/w1/` + `.ufo/waves/round-51/l1/drafts/`, 310 files):
  `live_hits 0`, `placeholder_hits 0`, `synthetic_fixture_hits 0`.
* Merge package `/home/vgpnk/Projects/shokuknow/merge/kaidoku/` (80 files, incl. the 11
  squashfs/AVM-adjacent staged entries): `live_hits 0`. **`op://` refs: 0. `Set-Cookie`: 0.
  `PRIVATE KEY`: 0. URL userinfo (`://user:pass@`): 0. base64/hex blobs ≥300/200 chars: 0.**
* The four vendor URLs in `tools/round-50/carriers.json`: **no credentials embedded** — all four
  are `https://download.avm.de/…`, no userinfo, no query string, no fragment, no port.
* Round-52 wave tree (peers' drafts, 280 files at scan time): `live_hits 0`.

**One carried item, restated with fresh measurement (not a new regression, nothing re-appended):**
the open L0 "unredacted session cookies in pushed history" (`plans/round-52-claims.md:259-260`)
is still live in three blobs reachable from `origin/main`. The tip tree is clean; the blobs are
not. Details in §4.

**One defect found in the sibling's merge-adoption draft (not a credential defect) — found, reported,
fixed by the owning seat, and independently re-verified here as closed.** See §5 and §5-1. Two
landing rules for the L1: insert the new rows **after the last registry row** (an EOF append raises
8 × `E12`), and keep the `recheck` cell a **bare cadence** (prose raises 8 × `E09`).

---

## 1. (1) Round-51 inheritance surface — credential material a port could copy into `tools/round-52/`

### 1a. Class-pattern scan (12 credential classes, values never reproduced)

Scanner: `python3 .ufo/waves/round-50/w3/SentReceipts/credscan.py` (patterns `set_cookie`,
`cookie_hdr`, `authorization`, `x_api_key`, `github_token`, `github_pat`, `bearer`, `op_ref`,
`aws_key`, `sk_key`, `private_key`, `jwt`; live vs placeholder classed separately).

| # | Command (cwd = lane) | Exit | stdout sha256 | Result |
|---|---|---|---|---|
| 1 | `python3 .ufo/waves/round-50/w3/SentReceipts/credscan.py .ufo/waves/round-51/w1/ .ufo/waves/round-51/l1/drafts/` | 0 | `bb1b58c3d90629165b3339b2d211ff41892dd0398982f148c8e3f0db8d37c221` | `live_hits 0`, `placeholder_hits 0`, `synthetic_fixture_hits 0`; 310 files / 5 776 021 B |

Exact argv, exit code, stdout/stderr sha256, byte counts and UTC stamps for every command in
this receipt are in `receipts/receipts.json`.

### 1b. `file:line` of every credential-WORD hit in that surface

Full table (447 hits, `file:line` + the matched word) is in
`receipts/r51-credential-words-by-line.tsv`. **No line carries a credential value** — every hit
is a lexical/prose occurrence. Classified by hand, grouped by file (hit count · words · line range):

| `file:line` range | words | what it is |
|---|---|---|
| `.ufo/waves/round-51/w1/SentCreds/scan.md:1-246` (102 hits) | `cookie, set-cookie, token, session, secret, password, authoriz, credential, api_key, bearer, op://, private key, akia, ghp_, github_pat` | The round-51 sentinel's own report: it names the 12 classes it searched for and the *lengths* of live values it found, and it states it never reproduces a value. Prose + class names. |
| `.ufo/waves/round-51/w1/SentCreds.md:1-66` (23) | same set | Same seat's summary report. Same discipline. |
| `.ufo/waves/round-51/w1/SentCreds/whole-tree-credscan.json:6-147` (24) | `bearer, cookie, secret` | The round-51 whole-tree sweep output: class names + `value_len` integers. No value bytes. |
| `.ufo/waves/round-51/w1/SentCreds/final-receipts.json:67` (10) | same set | One `argv` string quoting the grep pattern list (the scanner's own regex). Instruction, not data. |
| `.ufo/waves/round-51/w1/ExecTriV6/sqfs-triage-v6.py:98-936` (34) | `token` | The triage **action-vocabulary tokenizer** (`token_re`, `action_re`, `command_tokens`, `OPERATION_TOKEN = 'extract_firmware'`). "token" = an action word. |
| `.ufo/waves/round-51/w1/CritTriV6/v5-source-snapshot.py:97-935` (34) | `token` | The v5 source snapshot of the same tokenizer. Lexical. |
| `.ufo/waves/round-51/w1/ExecCounterV2/c1-counter.py:35-4412` (12) | `token` | The counter's **frontier-note token** (`token='LE AVM'`) and `def sid_tokens(text)` — a lexeme helper for S-ids. Lexical. |
| `.ufo/waves/round-51/l1/drafts/c1-counter.py:71-4864` (12) | `token` | Same, L1 draft copy. Lexical. |
| `.ufo/waves/round-51/w1/RevCounterPort/checklist.md:75-1628` (9) | `token` | The port checklist's token-rule text. Prose. |
| `.ufo/waves/round-51/w1/ScribeSources/mirror-SOURCES.md:7-229` (20) | `authoriz, password, secret, session, token` | The staged SOURCES mirror. The `password`/`secret` hits are inside **source titles** (e.g. a Trail of Bits write-up naming 1Password) and `session` appears in "session routing" / "public session call". |
| `.ufo/waves/round-51/w1/ScribeReadme/receipts/README.patched.md:23-287` (20) | same | The patched README coverage map. Same nature: product names ("1Password", "Obsidian"), "mcp-session" knowledge stems, "secret-file-detection" rule text. |
| `.ufo/waves/round-51/w1/ScribeProvince/frontier-note-edits.md:21-189` (12) | `session, token` | Frontier-note prose + token rule. |
| `.ufo/waves/round-51/w1/CritTriV6/receipts/e7_skill_markers_at_base.out:25-1784` (36) | `authoriz, secret, session, token` | A dump of the lane's own SKILL.md marker lines. `authoriz`/`secret` occur inside quoted SKILL rule text ("authorization", "no credential material"); `token` inside rule text. |
| `.ufo/waves/round-51/w1/ScribeSources.md:82` (7) | `api_key, authoriz, secret, set-cookie, token` | The seat's own scan-summary line ("secret scan of the whole seat dir for `set-cookie` / `authorization` / `api_key` / `token=`"). Prose about the scan. |
| `.ufo/waves/round-51/w1/ScribeSources/rows.md:134`, `rows_template.md:134`, `fetch-sources.sh:24` | `set-cookie, cookie, authoriz` | The row text and the fetch driver's own header scrub: "No `Set-Cookie`/`Cookie`/`Authorization` header was saved" and `grep -iE '^(content-type|content-length|last-modified|etag):'` — i.e. **the scrub itself**, which keeps four allow-listed headers and drops cookies. |
| `.ufo/waves/round-51/w1/ScoutMksquashfs/receipts/fetch-receipt.json:19-23`, `ScoutMksquashfs.md:4-20`, `quotes.md:9`, `sources-row-fields.md:18` | `set-cookie, token` | "No `Set-Cookie` header was captured or stored"; "`-nopad`, one **token**, no hyphen". Prose + lexical. |
| `.ufo/waves/round-51/w1/ScribeScorecard/section.md:177`, `ScribeScorecard.md` | `cookie, session` | "the carried L0 **cookie** note". Prose about the open issue. |
| `.ufo/waves/round-51/w1/ScribeLesson/receipts/spotcheck_routed_defects_6.txt:14` | `cookie, session` | The carried-L0 line. Prose. |
| `.ufo/waves/round-51/w1/CritCensus/findings.md:38-184`, `CritCensus.md:39-40`, `CritClaims/findings.md:43`, `CritRuleDerive/findings.md:239`, `CritTriV6/findings.md:63`, `ScribeEntryC1.md:66`, `ScribeEntryC1/entry.md:18-116`, `ScribeProvince.md:10-92`, `ScribeProvince/receipts.md:95`, `ScribeProvince/round-50-block-fate.md:17`, `ExecCensusDrift.md:46-50` | `session` | "REA session", "adb session", "study-group session", "session routing" — ordinary English usage in prose. |
| `.ufo/waves/round-51/w1/RevSweep/findings.md:17-34`, `RevSweep.md:13`, `RevDocsDrafts.md:16`, `ConnSiblings.md:12`, `ConnSiblings/scan.md:36-55`, `RevFetchGuards/findings.md:17`, `RevTriPort/checklist.md:19-60`, `ScribeReadme.md:26-50`, `ScribeReadme/frontier-note.md:21-158`, `ScribeReadme/coverage-map-row.md:36`, `ScribeReadme/receipts/patch_readme.py:8-192`, `ScribeReadme/receipts/readme-patch-check.log:11-20`, `RevDocsDrafts/findings.md:23`, `CritTriV6/receipts/e5_marker_chain.out:18-30`, `CritCensus/receipts/meanings-*.json:6` (×6) | `authoriz, credential, secret, token` | Prose about the credential rules, the token rule, and the coverage-map token. No values. |

**`op://` refs in the round-51 surface: the only hits are inside `SentCreds/scan.md:59-70,198-212`
and `SentCreds.md:41-46` — the round-51 sentinel's own report *naming* the `op://` class and
restating the carried-L0 blob paths. There is no `op://` **reference** (no vault path) anywhere in
the round-51 tree.** Verified independently:
`grep -rn 'op://' .ufo/waves/round-51/w1 .ufo/waves/round-51/l1/drafts` → exit 0, 1 139 bytes
out; every line is one of the above report lines (sha256 `c1b984ab0e14229c`).

### 1c. The port candidates specifically

The eight files that will land in `tools/round-52/` were checked separately
(`receipts/port-candidate-credential-words.tsv`, 58 hits, **0 flagged as REVIEW** — every hit is
lexical/prose):

| candidate | hits | what they are |
|---|---|---|
| `.ufo/waves/round-51/w1/ExecCounterV2/c1-counter.py` (sha256 prefix `c0b4c98c6d3aaaef`) | 12 | `token` = frontier-note token / `sid_tokens` lexeme helper |
| `.ufo/waves/round-51/l1/drafts/c1-counter.py` (`1787291d13f1e9c2`) | 12 | same, L1 draft |
| `.ufo/waves/round-51/w1/ExecTriV6/sqfs-triage-v6.py` (`b79ff2165874ae53`) | 34 | `token` = action-vocabulary tokenizer |
| `.ufo/waves/round-51/w1/ExecControls/c1-controls.py` (`ee12a7221fab9212`) | 0 | — |
| `.ufo/waves/round-51/w1/ExecFetchSelftest/fetch-vendor.py` (`451768778284ae16`) | 0 | — |
| `.ufo/waves/round-51/w1/ExecCensusDrift/census3.py` (`2dff5cd6c81ad2a4`) | 0 | — |
| `.ufo/waves/round-51/w1/ExecRuleDerive/gap-rule-v2.json` (`e5e9fb3f67f65bb8`) | 0 | — |
| `.ufo/waves/round-51/l1/drafts/c1-run.sh` (`e6bcf8aaa97f1509`) | 0 | — |

The **r52** port draft `.ufo/waves/round-52/w1/ExecFetchVendor/fetch-vendor.py` was diffed against
`tools/round-50/fetch-vendor.py`: the header-handling lines are identical modulo line numbers
(`ALLOWED_HOST = 'download.avm.de'` at `:62`, the https+host predicate at `:113-114`, the redirect
hook at `:101-105`). The new `--plan`/`--prior` code paths read `external.url` from a local JSON
spec and print it; **no `getheaders()`, no `Set-Cookie` read, no header dump into any receipt.**
No `.hdr`/`*cookie*`/`*header*` file exists anywhere in the round-52 wave tree.

### 1d. Vendor bytes

The twelve AVM pins from `tools/round-50/carriers.json` appear in the round-51 tree only as
**digest strings** (`entry.md`, `MutControlsV2/probe/fixture-carriers-4.json`, `grammar.md`) — never
as image bytes. A base64/hex probe over the whole round-51 tree + `l1/drafts` for runs ≥300
(base64) / ≥200 (hex) chars returned **0** blobs.

---

## 2. (2) Merge package — credential material or `op://` refs in the staged entries

Package: `/home/vgpnk/Projects/shokuknow/merge/kaidoku/` (read-only). 80 files, 536 KB, **all
text** (`file` reports no binary; `SOURCES.append.md` 132 rows + `MERGE-REPORT.{md,json}` +
`knowledge/corpus/knowledge/` 77 entries).

| # | Command | Exit | stdout sha256 | Result |
|---|---|---|---|---|
| 1 | `python3 .ufo/waves/round-50/w3/SentReceipts/credscan.py /home/vgpnk/Projects/shokuknow/merge/kaidoku` | 0 | `c48e6929dac4f90a…` | `live_hits 0`, `placeholder_hits 0`, `synthetic_fixture_hits 0`; 80 files / 236 609 B |
| 2 | same, restricted to the **11 squashfs/AVM-adjacent staged entries** (`avm-firmware-image-unblob`, `avm-image-build-blocker`, `avm-image-extraction`, `avm-le-image-genuine-marker`, `avm-le-variant-reachability`, `sasquatch-unblob-avm-branch`, `sasquatch-unblob-compatibility`, `sasquatch-unblob-compatibility-precondition`, `sasquatch-prebuilt-package-inventory`, `unblob-format-matrix`, `unblob-sasquatch-dependency`) | 0 | `2279432f272746a4…` | `live_hits 0` (11 files / 40 345 B) |
| 3 | `grep -rn 'op://' <pkg>` | 1 | `e3b0c44298fc1c14` (empty) | **0 hits** |
| 4 | `grep -rn 'Set-Cookie' <pkg>` | 1 | `e3b0c44298fc1c14` | **0 hits** |
| 5 | `grep -rn 'PRIVATE KEY' <pkg>` | 1 | `e3b0c44298fc1c14` | **0 hits** |
| 6 | `grep -rnoE '://[^/\s]*:[^/@\s]*@' <pkg>` | 1 | `e3b0c44298fc1c14` | **0 credentialed URLs** |

**CORPUS rule 6 verdict: PASS.** `/home/vgpnk/Projects/shokunin/CORPUS.md:129` — *"No credential
material, session or private URLs, or `op://` references — ever."* The staged entries contain
none of the three.

### 2a. Every credential-word hit in the package (22 total), classified

| `file:line` | word | what it is |
|---|---|---|
| `knowledge/corpus/knowledge/adb-locale-pinned-reference.md:32` | `token` | "~97 k-**token** page" — a page-size unit. |
| `knowledge/corpus/knowledge/dumpsys-window-focus-line-printer.md:12,38` | `token` | "the `Window{…}` **token** it prints" — a printed string shape. |
| `knowledge/corpus/knowledge/adb-second-image-api34.md:51` | `token` | "the line is printed … and the **token** is". A lexical token. |
| `knowledge/corpus/knowledge/adb-device-conditions-and-states.md:19-20` | `token`, `private key` | The **adb AUTH handshake described by upstream AOSP** ("the host sends a random token, the recipient signs it with its private key and replies with an `AUTH` packet whose type is `SIGNATURE(2)`"). Protocol *mechanism*, no key bytes, no key material. CORPUS.md:50 asks exactly this: "Cite the file path, the mode, and the mechanism." |
| `knowledge/corpus/knowledge/japanese-rea-practitioner-account.md:9-33` | `session` (×5) | A Japanese study-group **session** write-up. Ordinary usage. |
| `knowledge/corpus/knowledge/rea-catalogue-version-join.md:43` | `session` | "re-enable MCP registration on every **session** spawn". |
| `knowledge/corpus/knowledge/rea-evidence-graph-ratio-two-real-applications.md:19,39`, `rea-evidence-graph-scaling.md:40`, `rea-evidence-graph-third-application.md:16` | `password` (×4) | The word appears inside **"1Password"** — the analysed application's name in a byte-count table. Not a credential. |
| `SOURCES.append.md:48,82,103,111,112,125` | `authoriz, password, secret, session, token` | Source **titles and anchor cells** of rows S147/S181/S202/S210/S211/S224 (e.g. "AOSP's adb host-to-device protocol … the upstream **authorization** condition a device must satisfy"). Citations, not secrets. |

### 2b. URL surface of the package

Distinct hosts across all 29 distinct URLs in the package: `android.googlesource.com`,
`api.github.com`, `api.semanticscholar.org`, `arxiv.org`, `atsum.in`, `bbs.kanxue.com`,
`cloud.tencent.com`, `cynex.nict.go.jp`, `developer.aliyun.com`, `developer.android.com`,
`developer.android.google.cn`, `dev.mi.com`, `doi.org`, `download.avm.de`, `gihyo.jp`,
`github.com`, `man7.org`, `qiita.com`, `raw.githubusercontent.com`, `repository.hkust.edu.hk`,
`unblob.org`, `web.archive.org`, `www.cnblogs.com`, `www.heqiangfly.com`, `www.kanxue.com`,
`www.kkaneko.jp`, `zenn.dev`, `zenodo.org`. **No `file://`, no `localhost`/`127.0.0.1`, no
`userinfo@`, no query-string credential parameter** (`?token=`/`?key=`/`?sig=`/`?auth=` → 0 hits).

### 2c. Two hygiene notes on the package (not credential breaches)

1. **Absolute host paths.** Six staged rows/entries cite the operator's absolute home paths
   (`SOURCES.append.md:53` → `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/cliCommandNames.js`;
   `SOURCES.append.md:128` → `/home/vgpnk/Android/Sdk`; `knowledge/.../rea-adb-operation-vocabulary.md:4,6`,
   `rea-evidence-graph-ratio.md:34`, `rea-evidence-graph-ratio-real-application.md:16`,
   `sasquatch-unblob-compatibility.md:15`, `adb-second-image-api34.md:17`,
   `adb-device-conditions-and-states.md:41`). These are **paths, not secrets** — and the lane's own
   committed `corpus/SOURCES.md` already carries 22 `/home/vgpnk/...` paths, so this is the
   established house style, not a new exposure. Flagged for the L1's awareness only.
2. **Staged rows cite paths that do not exist in this lane.** 86 rows cite `lanes/kaidoku/roundN/work/…`
   (the *other* lane's workspace layout). The lane has no `lanes/` directory; those four probed
   paths are all **missing** here. If such a row is adopted verbatim, its `anchor` cell names a file
   a reader in this lane cannot open. Not a credential issue; a citation-hygiene issue for whoever
   adopts.

---

## 3. (3) The four vendor URLs in `carriers.json` — no embedded credentials

`tools/round-50/carriers.json` (the source the r52 fetcher draft reads) — parsed with `urlsplit`:

| id | scheme | host | userinfo | port | query | fragment |
|---|---|---|---|---|---|---|
| `g7581` | `https` | `download.avm.de` | none | none | empty | empty |
| `g7582` | `https` | `download.avm.de` | none | none | empty | empty |
| `c6490` | `https` | `download.avm.de` | none | none | empty | empty |
| `c6430` | `https` | `download.avm.de` | none | none | empty | empty |

Full paths: `/fritzbox/fritzbox-7581/other/fritz.os/FRITZ.Box_7581-07.18.image`,
`/fritzbox/fritzbox-7582/other/fritz.os/FRITZ.Box_7582-07.18.image`,
`/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/FRITZ.Box_6490_Cable-07.57.image`,
`/fritzbox/fritzbox-6430-cable/deutschland/fritz.os/FRITZ.Box_6430_Cable-07.30.image`.

**No credentials.** No `user:pass@`, no `?token=`/`?sig=`, no bearer, no cookie, no fragment-borne
token. The `notes.http_etag` / `notes.http_last_modified` fields are response *metadata* (an ETag
and a date), not `Set-Cookie`. The host set across every `carriers.json` in the lane
(`tools/round-44`, `tools/round-49`, `tools/round-50`, `.ufo/waves/round-{38,39,40,41,42,49}/…`) is
`{download.avm.de, archive.openwrt.org, download1.dd-wrt.org}` with **0 credentialed URLs** in any
of them.

`corpus/evidence/round-50/c1/` (the committed round-50 receipts): `credscan` → `live_hits 0`; a
direct grep for `set-cookie|^cookie:|authorization|bearer |op://|ghp_|AKIA` → **0 hits**.

---

## 4. Carried L0 (restated, freshly measured — NOT a round-52 regression)

`plans/round-52-claims.md:259-260` carries the open L0: *"unredacted session cookies in pushed
history — `kaidoku | round-50` stands; not re-appended; no credential use this round."*

Re-measured against `origin/main` at the round-52 base (`1842addcef3458515859b928b92d9bbd0a46c5d5`):

* **Tip tree: clean.** Every `set-cookie:` line in the working tree is a redaction placeholder
  (`[redacted by L1 round 50: cookie value]` / `[redacted by L1: session cookie value]` /
  `<REDACTED>`). Zero live values.
* **History: not clean.** Three blobs carrying **live** `_gh_sess` / `_octo` values remain reachable
  from the pushed ref (`git rev-list origin/main --objects` matches all three):

  | blob | path | live value lengths |
  |---|---|---|
  | `ba6b0d6ec4d791ced391a08523bfd2e66ddbb2b6` | `.ufo/waves/round-45/w2/R45W2S138Top/receipts/f1.hdr` | `_gh_sess` 352, `_octo` 26, `logged_in` 2 |
  | `5f8478b4fc25c8b1c5718eeafba2591f62010a1f` | `.ufo/waves/round-49/w1/C1CarrierPins/receipts/tree.hdr` | `_gh_sess` 348, `_octo` 27, `logged_in` 2 |
  | `815e2951e830e2ffea5c0995444c19a47225879b` | `.ufo/waves/round-49/w1/C1S138Reopen/receipts/top.hdr` | `_gh_sess` 364, `_octo` 27, `logged_in` 2 |

  `logged_in` value length 2 ⇒ `no` ⇒ anonymous GitHub session cookies. Impact low; remediation
  (history rewrite + force-push, or operator-authorised rotation) is outside a wave seat's remit.
  **This wave re-appends nothing and adds nothing to it.** The redacted successors sit at the tip.

**Smallest remediation if the operator ever wants it closed:** rotate/expire the anonymous GitHub
sessions (no code change needed — the values are anonymous and already expired-in-effect), then a
one-off `git filter-repo --invert-paths --path <those three .hdr files>` on a rewritten branch +
force-push. Both steps are operator-authorised and out of scope here.

---

## 5. Defect found in the merge-adoption draft — FIXED by the owning seat, independently re-verified

Seat `ScribeMergeAdopt` drafted 8 new registry rows (`S253`–`S260`) in
`.ufo/waves/round-52/w1/ScribeMergeAdopt/sources-rows.md`. The round's own claims require the
scratch mirror to pass `scripts/sources-census.sh validate --file` exit 0 **before** the first
append (`plans/round-52-claims.md`, Frontier step → Assimilation).

Measured on a scratch mirror (lane `corpus/SOURCES.md` + the 8 draft rows inserted in the
`## Registry` section, with the sibling's `entry.md` staged as
`corpus/knowledge/2026-10-30-r52-avm-le-format.md`):

| command | exit | finding |
|---|---|---|
| `sources-census.sh validate --file <lane corpus/SOURCES.md> --today 2026-10-30` | **0** | baseline clean: `ok` + 19 `W04` (the known duplicate-URL debt) |
| `sources-census.sh validate --file <mirror + S253..S260> --today 2026-10-30` | **1** | **8 × `E09`** on S253–S260 |

`E09` = *"invalid recheck (ISO date, `NNd`, or symbolic cadence)"*. The draft puts a **prose**
recheck in the cell — `180d — recheck run 2026-10-30, exit 0, count 1 (command in the entry's
recheck line and \`## Gate\`)` — and the validator's rule is
`recheck !~ /^[0-9]+d$/ && !symbolic(recheck)` → `E09`. Reproduced with a minimal fixture
(`receipts/fixture-escaped-pipe.md` shows the same fixture family): a row whose recheck cell is
exactly `180d` passes (`ok`, exit 0); the same row with `180d — extra text` fails `E09`.

**Smallest remediation:** put the bare cadence in the cell (`180d`) and keep the run detail in the
knowledge entry's own `recheck:` header / `## Gate` block — which is what the sibling's `plan.md`
already says the convention is, and what the lane's 158 committed rows already do (they carry bare
`90d` / `on-release` / ISO dates). One cell edit per row; no other change.

**Also checked, and it is fine:** the draft rows have exactly 12 pipes each (11 cells) — the
sibling fixed the one row that briefly carried an unescaped `|` in its anchor cell (S255) before
this scan closed. The `used-by` target `corpus/knowledge/2026-10-30-r52-avm-le-format.md` is a
**draft** (`entry.md` under the seat dir) and will be E11 until the entry lands in
`corpus/knowledge/`; in the mirror with the entry staged it resolves, and the only remaining
`E11`s are the lane's own four pre-existing dangling used-by paths (`SKILL.md` ×2,
`corpus/QUALITY.md`, `tools/round-27/xpin-attribute.mjs`).

### 5-1. The owning seat fixed it; independently re-verified here

`ScribeMergeAdopt` applied the remediation (the `recheck` cell of S253–S260 now holds the bare
cadence `180d`; the ISO run date, the exact command and the observed count moved to the adopted
entry's `recheck:` header and its `## Gate` block). It also surfaced a **second placement rule**
this scan had measured independently: appending the rows at EOF raises **8 × `E12`** ("row outside
Registry section") — they must go **after the last registry row** (line 164), not at EOF.

Re-verified here on a fresh scratch mirror, independently of the sibling's own run:

| mirror variant | exit | result |
|---|---|---|
| lane `corpus/SOURCES.md` alone (baseline) | **0** | `ok` + 19 `W04` (known debt) |
| + the 8 **fixed** rows after the last registry row, entry staged at `corpus/knowledge/2026-10-30-r52-avm-le-format.md`, cited lane-root files present | **0** | `ok` + 19 `W04` — **0 error codes** (`receipts/census-sibling-rows-S253-S260-FIXED.tsv`, stdout sha256 `d8d9e092508d9ce2…`) |
| + the same 8 rows appended at **EOF** | **1** | **8 × `E12`** on S253–S260 (`receipts/census-sibling-rows-EOF-append-E12.tsv`, stdout sha256 `045737e8a9a583a0…`) |

The fixed rows' shape, read directly from
`.ufo/waves/round-52/w1/ScribeMergeAdopt/sources-rows.md` (sha256 prefix `beb6c67d703ab0da`):
all 8 rows carry exactly 12 pipes (11 cells), `recheck` = `180d` for every row, `used-by` =
`corpus/knowledge/2026-10-30-r52-avm-le-format.md` for every row.

**Credential re-scan of the sibling's whole seat after the fix** (10 files): `live_hits 0`,
`placeholder_hits 0`; no `op://`, `Set-Cookie`, `PRIVATE KEY`, `ghp_`, `AKIA`, `Bearer` or
`Authorization:` hit (`receipts/credscan-sibling-seat-after-fix.json`, stdout sha256
`27864bc90e183171…`).

**Status: F1 is CLOSED.** The two landing rules the L1 must keep are now recorded in the sibling's
`plan.md` §5–§6: (a) insert the rows **after the last registry row**, (b) keep the `recheck` cell a
**bare cadence**.

### 5-2. Final re-verification against the seat's delivered state

The sibling's final `sources-rows.md` (sha256 prefix `beb6c67d703ab0da`, 11 347 B) was re-read and
re-gated here after the seat closed:

* 8 rows, **every one with exactly 12 pipes** (11 cells), `recheck` = `180d`, `status` = `mined`,
  `opened` = `2026-10-30`, `used-by` = `corpus/knowledge/2026-10-30-r52-avm-le-format.md`.
* Gate re-run on a fresh mirror (lane registry + the 8 rows after the last registry row + the
  entry staged + the lane-root files the rows cite): **exit 0**, `ok` + 19 `W04`, **0 error codes**.
* The two **own-work** rows' pinned campaign artefacts were digest-verified against the bytes on
  disk: `lead2-avm-le-genuine.tsv` (940 B) — claimed `523637c885bb50c6…`, actual
  `523637c885bb50c6…` ✓; `lead2-stale-build.tsv` (964 B) — claimed `4c962bacd24af813…`, actual
  `4c962bacd24af813…` ✓. Both cited files **exist** on disk at
  `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work/`.
  (Contrast §2c: the *merge package's* rows cite the **relative** `lanes/kaidoku/roundN/work/…`
  form, which does **not** resolve in this lane. The adopted rows use the absolute, existing path —
  the better convention, and the L1 should keep it.)

### 5a. Same defect class in the *package's* 132 staged rows (for whoever appends them)

If the L1 appends rows from the merge package's `SOURCES.append.md`, the package's own rows carry
the same schema defects, in a stronger form. Measured on a scratch mirror (lane registry + the
132 package rows renumbered S252–S383, staged knowledge copied in):

| defect | count | cause |
|---|---|---|
| `E01` (malformed row, fields ≠ 13) | **44** | A literal `\|` inside the recheck cell. The validator's `gawk -F'|'` **does not honour backslash escapes** (proved by fixture `receipts/fixture-escaped-pipe.md`: a cell containing `anch\|or` yields `E01 fields=12`). 41 rows have it in the recheck cell; 3 rows (`S127`, `S141`, `S158`) also in the anchor cell. |
| `E09` (invalid recheck) | **88** | Every one of the 132 rows has a prose recheck cell (`180d — <command> -> N (ran …)`). Only the 44 `E01` rows short-circuit before the recheck check, so 88 surface as `E09`. |
| `E11` (missing used-by) | **132** | All 132 rows' `used-by` name `corpus/knowledge/<file>.md` files that exist only in the package's own `knowledge/` tree, not in the lane — until the knowledge entries are copied in. |
| `W04` (duplicate URL across scopes) | 19 → 25 | The lane's 19 known warnings plus **6 new** ones from the package rows. |
| `E03` (duplicate id) | **0** | Renumbering by document avoids collisions — the package's own ids (`S106`–`S237`) overlap the lane's (`S001`–`S251`), so a blind append would collide; the renumber map is `receipts/merge-renumber-map.tsv` (S106→S252 … S237→S383). |

**Smallest remediation (measured, in scratch):** normalise each adopted row — (a) recheck cell to a
bare cadence (`180d`), (b) remove the literal `|` characters from cells (they cannot be escaped
through `gawk -F'|'`), (c) copy the referenced knowledge entries into `corpus/knowledge/` — and the
mirror validates with **0 `E`-codes on the merged range** (only `W04`/`W01` warnings remain).
Receipts: `receipts/census-mirror4-merge-normalized.tsv` (recheck normalised → 0 E01/E09/E11 on
the merged range) and `receipts/census-mirror5-merge-pipes-stripped.tsv` (pipes stripped as well →
`E01 0`, `E09 0`, `E11 4`, all four being the lane's own pre-existing dangling used-by paths).

**Scope note:** this defect class lives in the *package's* 132 staged rows, and only bites if the
L1 appends those rows **as staged**. The round-52 adoption actually lands **8 re-grounded rows**
(S253–S260, written by `ScribeMergeAdopt` from pinned upstream Freetz-NG documents, not copied from
the package's rows), and those are clean — see §5-1. So F2 is a **latent risk for any future bulk
append**, not a blocker for the round-52 freeze. The L1 should still hold the two normalisation
rules on file for any later bulk append.

---

## 6. Other surfaces checked (context)
* **Round-52 wave tree** (peers' drafts, 280 files at scan time): `credscan` → `live_hits 0`.
  0 `op://` refs outside the wave-spec prompt text; 0 `Set-Cookie` lines; no `.hdr`/header-capture
  files; no base64/hex blob ≥300/200 chars.
* **`plans/round-52-claims.md`**: `credscan` → `live_hits 0`. Its only credential mention is the
  carried-L0 line 259-260.
* **Lane strays** `kaidoku-r26/`, `kaidoku-r51/` (tracked, 2 files): `credscan` → `live_hits 0`.
  Both are misrooted wave artefacts (a round-26 seat report and a round-51 sibling's
  `amended-law-battery.py` sitting at the lane top level instead of under `.ufo/waves/`).
  Credential-clean, but a **lane-hygiene** observation the L1 may want to relocate or drop.
* **`corpus/evidence/round-50/c1/`**: no credential material; no vendor bytes (JSON receipts only).
* **This seat's own output** (this report, `status.json`, all 14 receipt files — 16 files):
  `credscan` → `live_hits 0`, `placeholder_hits 0`. The first build of
  `receipts/r51-credential-words-by-line.tsv` put the matched word in the *last* column, so the
  scanner's `bearer\s+<12+ chars>` rule matched the newline plus the next line's file path
  (5 false `live` hits); the table was regenerated with the word in the middle column and the
  re-scan is clean. No credential value is reproduced anywhere in this seat's output — the
  round-51 hit table lists *file, word, line* only, and the L0 restatement in §4 gives blob ids and
  value **lengths**, never the values.

## 7. Limits of this scan (stated, not hidden)

* **No REA run, no `--data-run`, no vendor download** was performed by this seat. Nothing was
  fetched; the URLs were parsed from the local JSON only.
* The credential scan is **pattern-based** (12 classes). A secret matching none of the 12, or
  split across lines/encodings, would not be found. The word-level sweep (§1b, 447 hits) plus
  the base64/hex blob probe are the mitigation, and every hit was classified by hand.
* The vendor-byte check is **pin- and marker-based**; a re-encoded vendor payload would not be
  caught by it. (Not applicable to this seat's three questions, which are about credential
  material and URL shape.)
* The tree changed under the scan (siblings kept writing): counts are as of the UTC stamps in
  `receipts/receipts.json`. The round-51 and merge-package surfaces were re-scanned at
  2026-10-30T10:50:39Z, after the last sibling write observed at that moment.
* `gawk -F'|'` behaviour (backslash escapes not honoured) was established by direct fixture, not
  assumed.

## 8. Files in this seat directory

| file | what |
|---|---|
| `scan.md` | this report |
| `receipts/receipts.json` | exact argv, cwd, UTC start/end, exit code, stdout/stderr sha256 + byte counts for all 35 commands |
| `receipts/credscan-r51-w1-l1drafts.json` | raw scanner output, round-51 surface |
| `receipts/credscan-merge-pkg.json` | raw scanner output, merge package |
| `receipts/credscan-self-output.json` | raw scanner output over this seat's own 16 files — `live_hits 0` |
| `receipts/r51-credential-words-by-line.tsv` | all 447 credential-word hits in the round-51 surface, `file:line` + word |
| `receipts/port-candidate-credential-words.tsv` | the same for the 8 port candidates (58 hits, 0 flagged) |
| `receipts/census-lane-baseline.tsv` | `sources-census.sh validate` on the lane registry — exit 0, `ok` + 19 W04 |
| `receipts/census-mirror-lane-plus-merge.tsv` | lane + the 132 package rows appended raw — 132 E12, 44 E01, 88 E09, 136 E11 |
| `receipts/census-mirror4-merge-normalized.tsv` | same after normalising the recheck cell — 0 E01/E09/E11 on the merged range |
| `receipts/census-mirror5-merge-pipes-stripped.tsv` | same after also removing literal `|` from cells — `E01 0`, `E09 0`, `E11 4` (lane's own) |
| `receipts/census-sibling-rows-S253-S260.tsv` | the sibling's 8 draft rows → **8 E09** (before the fix) |
| `receipts/census-sibling-rows-raw.tsv` | same, before the entry was staged (8 E09 + 8 E11) |
| `receipts/census-sibling-rows-S253-S260-FIXED.tsv` | the same 8 rows **after the fix**, re-verified here → exit **0**, `ok` + 19 `W04`, 0 error codes |
| `receipts/census-sibling-rows-EOF-append-E12.tsv` | the same rows appended at EOF → 8 × `E12` (the second placement rule) |
| `receipts/census-sibling-rows-FINAL-delivered-state.tsv` | final re-gate against the seat's delivered `sources-rows.md` — exit **0**, 0 error codes |
| `receipts/credscan-sibling-seat-after-fix.json` | credential re-scan of the sibling's 10 files after the fix — `live_hits 0` |
| `receipts/fixture-escaped-pipe.md` | minimal fixture proving `gawk -F'|'` does not honour `\|` |
| `receipts/merge-renumber-map.tsv` | S106→S252 … S237→S383 document renumbering |
