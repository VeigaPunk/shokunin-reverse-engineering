# R43ScribeAssim — the admitted entry, drafted: sasquatch release matrix

**Verdict: DONE** — the entry `corpus/knowledge/2026-10-27-sasquatch-release-matrix.md` is drafted in my
artifacts dir, grounded on bytes fetched this round and cross-confirmed by the wave's re-grounding seat
(ADMIT, flip unfired), with **one** L1 placeholder left (per-asset pins for the seven older releases).
Nothing was written in the lane; no extractor, no REA, no VCS mutation, no tool installed.

Seat: scribe (leaf). Scope: the one admitted assimilation entry, `sasquatch-prebuilt-package-inventory`
(ADMIT per round 42's `R42Assim` review, re-grounded here). Round-43 base `6b9e64fe`.

## 1. Axes (what moved, what did not)

- **Coverage** — one entry on ground no held file occupies: the eight-release matrix, its start tag
  (`sasquatch-v1.0.1`), the amd64-only `sasquatch-v1.0`, the `digest`-field pattern (6 of 6 on the
  newest release, 0 on every other), the arm64/armhf package digests, and the page-vs-API citation
  correction. Held entries cover the *route* (`2026-10-26-unblob-sasquatch-dependency.md`) and the
  newest tag's asset set (S107), not the matrix.
- **Depth** — both round-36 falsifications were re-derived today rather than inherited: the asset
  counts `[6,6,6,6,6,6,6,2]` and the body scan (five empty bodies; 645/560/38 B for the three others;
  zero standalone `1.0` tokens) are this round's observations. The round-42 draft's version-pair
  sentence would have **overstated** if landed unedited: `sasquatch-v4.5.1-1`'s 38-byte body does state
  an upstream version ("Rebased on top of squashfs-tools 4.5.1"). The draft now says "no body states a
  *pair*" and quotes that body, so the surviving claim is exact where round 42's was rounded.
- **Calibration** — the `recheck:` is pinned as a **projection**, not a digest, and the reason is
  observed rather than argued: two captures 10.5 h apart agree on tags, `published_at` and all 44
  `(name,size)` pairs, and after `download_count` is removed the two payloads are **byte-identical**
  in canonical form (`diff` → 0 lines); the only differences are 7 download counters. (Round 42's
  receipt is a compact serialization, 87700 B; mine is the pretty HTTP body, 107313 B — an earlier
  version of this report read that length gap as drift, which was wrong: `jq -c .` makes both 87701 B.
  Corrected per R43-AG1, receipt `receipts/serialization-check.txt`.) The rendered page is the
  genuinely volatile object: two same-day fetches are both 349255 B with different digests.
  Inference is labelled where it is inference (the shared base of the six older `v4.5.1-*` tags).

## 2. Evidence (every command run this round, in scratch)

Scratch `S=/fast/scratch/hyaku/kaidoku-r43/w1-R43ScribeAssim`, `export TMPDIR="$S"`, `cd "$S"` before
every fetch. All times UTC, 2026-10-27. Receipts under `.ufo/waves/round-43/w1/artifacts/R43ScribeAssim/receipts/`.

| # | command (as written) | output | exit |
|---|---|---|---|
| 1 | `curl -fsSL -o rel-r43.json -w 'HTTP %{http_code} bytes %{size_download}\n' https://api.github.com/repos/onekey-sec/sasquatch/releases` then `sha256sum rel-r43.json` | `HTTP 200 bytes 107313`; `cb42cd61728f994dc18e4937d2d173b543c6a976bea25fa922e50f7213a105d0` at 2026-10-27T08:18:38Z | 0 |
| 2 | `curl -fsSL https://api.github.com/repos/onekey-sec/sasquatch/releases \| jq -c '[length, (map(.assets\|length)), (map([.assets[]\|select(.digest)]\|length))]'` | `[8,[6,6,6,6,6,6,6,2],[6,0,0,0,0,0,0,0]]` at 2026-10-27T08:20:15Z — this is the entry's `recheck:` line, run as written | 0 |
| 3 | `jq -r '.[] \| .tag_name as $t \| .assets[] \| $t + " " + .name + " " + (.size\|tostring) + " " + (.digest // "null")' rel-r43.json` | 44 asset lines; per-release tag/published/body-length also dumped (`receipts/capture-projection.txt`) | 0 |
| 4 | body scan: `4.5.1` present **and** standalone `1.0` present, per release | `has_pair=False` for all 8; body lengths `645, 560, 0, 0, 0, 38, 0, 0` (`receipts/version-pair-scan.txt`, bodies verbatim) | 0 |
| 5 | `curl -fsSL -o sasq-releases-r43.html -w 'HTTP %{http_code} bytes %{size_download}\n' https://github.com/onekey-sec/sasquatch/releases` (at 08:20:30Z and again at 09:05:48Z) | 349255 B sha256 `89e7377d…27a67`; second fetch same 349255 B, sha256 `56632d0f…b1cea` (`receipts/page-probe.txt`, `receipts/page-fetch2.txt`; both bytes retained) | 0 |
| 6 | `grep -oE 'sasquatch-v4\.5\.1-[1-6]\|sasquatch-v1\.0\.1\|sasquatch-v1\.0' sasq-releases-r43.html \| sort -u \| wc -l` | `8`; `grep -c` of each of the four asset filenames → `0` (`receipts/page-probe.txt`) | 0 |
| 7 | diff of the two captures (round-42 receipt vs today), canonical form | `tags_identical: True`; `tag+published_at+asset(name,size)_set_identical: True`; `jq -S -c` lengths equal (87701 B both); with `download_count` deleted, `diff` → 0 lines; 7 counters moved (`receipts/capture-diff-r42-r43.txt`, `receipts/serialization-check.txt`) | 0 |
| 8 | id-collision guard, read-only git on `6b9e64fe` | lane 134 rows `S001..S134`; staged 132; `comm -12` → 29 collisions `S106..S134`; `grep -c '^\| S[0-9]'` = `grep -c '^ *\| S[0-9]'` = 134 (`receipts/id-collision.txt`) | 0 |
| 9 | citation resolution in the lane (read-only) | `corpus/evidence/round-36/c1/K1/after-run.json` exists and contains `unsquashfs version 4.5.1 (2022/03/17)`; S107 carries `efbc92bd…ade95`; `PROVINCE.md:156-157` carries the quoted Frontier bullet; `R42Assim.md` has `## 1` | 0 |

Network reads only. No `REA`, no `unblob`, no `sasquatch`, no `unsquashfs`, no `7z` invocation, no
package downloaded, no archive opened. Nothing was run against a published firmware image.

## 3. The draft, and what the L1 must replace

File: `artifacts/R43ScribeAssim/drafts/2026-10-27-sasquatch-release-matrix.md` (10915 B, sha256
`30bf9688…10041`). Front-matter order per **R42-V5**: `source:` ×2 → `verified-at:` → `recheck:` →
`ground:` (`grep -n` → 1:source, 2:source, 3:verified-at, 4:recheck, 5:ground), then the H1.

**One placeholder remains**, deliberately left to the L1's freeze step:

1. `<<L1:per-asset sha256>>` — per-asset pins for the **seven older** releases. The endpoint publishes
   `digest` only for `sasquatch-v4.5.1-6`; pinning the other 42 assets costs a package download, which
   this seat did not do. The newest release's six digests **are** filled from today's capture
   (`efbc92bd…`, `28e57a4f…`, `29c72159…`, `73d44ca5…`, `7891831a…`, `9d82e6d4…`).
2. `<<L1:assim evidence>>` — **RESOLVED before filing.** `.ufo/waves/round-43/w1/artifacts/R43AssimGround/`
   did not exist at 08:22Z; when re-checked at 09:06Z it was there (artifacts mtime 09:00Z), together
   with the seat's report `R43AssimGround.md` and `rows/normalized-rows.md`. Its verdict is
   **CONFIRMED — ADMIT**, independent on every cell: same matrix and sizes, same 7 `download_count`
   deltas, same body finding, same 29 collisions, the same S136/S137 ids chosen from the same base,
   and a scratch mirror census exit 0 with the entry at the target path. **The placeholder is gone
   from the draft**; the entry now carries a `Re-grounded in-wave (2026-10-27)` paragraph citing that
   report §1–§2 (ninth-release limb closed by `?page=2` → 0 items and the 19-tag list, of which 8 are
   release tags). All three items it flags against this seat (AG1 serialization, AG2 unretained page
   digest, AG3 indented fixture) were already corrected here from the L1's IRC; its §3 fixture and my
   `receipts/id-guard-fixture.txt` agree.

Rows: `artifacts/R43ScribeAssim/drafts/sources-rows.md` proposes **S136** (releases API, `dataset`) and
**S137** (rendered page, `docs`, cited for a negative). Ids are provisional — S135 is spent on the
round's LICENSE row, and staged S130 collides with the landed S130 (unblob fixtures) while citing the
page for its assets, so no staged row is appended verbatim. The file records the alternative (drop
S137 and keep the correction sentence with the receipt) so the L1 is not blocked on a row-count call.

## 4. Checks the L1 should run on landing

- `grep -n '^source:\|^verified-at:\|^recheck:\|^ground:' <landed entry>` → 1,2,3,4,5 order.
- The entry's `recheck:` line verbatim → expect `[8,[6,6,6,6,6,6,6,2],[6,0,0,0,0,0,0,0]]`; a
  different third element (a non-zero somewhere past index 0) fires the flip clause and the entry is
  re-read, not silently kept.
- `scripts/sources-census.sh validate …` after the two rows land (not run by this seat: it writes
  nothing I own, and my scope is the draft).
- Confirm S136/S137 do not collide with what any other seat lands this wave.

## 5. Routed findings (verbatim where they are conflicts)

- **F1 — path conflict between the plan and the round ticket, for C2 (not my lane, reported because I
  read it while grounding).** `plans/round-43-claims.md`, `## Frozen paths`: "the copies under
  `corpus/evidence/round-42/local-sources/` (added after the freeze — landing paths, not pre-landing
  bytes)". The round-43 assignment states the landing as "17 in-lane copies under
  `corpus/evidence/round-43/local-sources/`". Two different directories for the same landing; the
  canonical judge should settle it before the freeze, not after.
- **F2 — a lane file appeared empty while this wave ran.**
  `corpus/knowledge/2026-10-27-r43-sqfs-triage-v4-scored.md` is 0 bytes, mtime 2026-10-27 05:19. Seats
  may not write in `corpus/`; if an L1-side placeholder, it needs filling before the freeze, and if a
  seat created it, that is a bounds breach to record. I did not touch it.
- **F3 — the round-42 draft's version-pair sentence needed tightening, not copying.** Superseded text:
  "no release body states a package/upstream version pair" was true as written; the surrounding
  framing read as "no body names a version", which `sasquatch-v4.5.1-1` falsifies. The draft now names
  that body.
- **F4 — S107 overlap, disclosed in the entry.** S107 holds the newest tag's six assets, publish date
  and the amd64 digest; what this entry adds is the matrix, the start tag, the arch gap, the
  digest-presence pattern, the arm64/armhf digests and the body finding. Not a duplicate, but an L1
  reading only S107 could think it is.
- **F5 — recheck semantics, recorded as a limit rather than a gate.** The pinned filter cannot see a
  body edit. It is a floor; the entry says so and names what re-reads.
- **F6 — capture stability, a read-only cross-check (corroboration, not evidence).** The sibling seat
  `R43AssimGround` fetched the same two objects in the same minute. Comparing hashes read-only against
  its scratch files: its `rel.json` is **byte-identical to mine** (`cb42cd61…`), while its
  `sasq-releases.html` is **349255 B with a different digest** (`150c7584…` against my `89e7377d…`).
  So the API response is stable within a minute and drifts only across accumulation (the 10.5 h
  `download_count` move), whereas the rendered page varies per request even at equal byte length.
  Scratch is not a citable path, so this appears here and **not** in the entry; the entry's limit
  sentence rests on my own two retained fetches (both 349255 B, digests `89e7377d…` and `56632d0f…`)
  plus round 42's retained 349266 B fetch, and stands without it.

- **F7 — the staged package is malformed, not just colliding.** `R43AssimGround` ran the 132 staged
  rows verbatim through the fleet validator in a scratch mirror: **266 E-lines** (44 × E01 fields=12
  from an escaped pipe inside a cell, 88 × E09 recheck-not-a-cadence, 2 × E03 duplicate id, 132 × E11
  absent used-by). So "renumber and append" was never an option; only re-grounded rows land.
- **F8 — landing order is load-bearing.** `used-by` is resolved on disk for every `mined` row and the
  entry does not exist yet, so the two rows and the entry must land in **one commit**, entry first;
  a rename of the entry moves both `used-by` cells or E11 reds. `R43AssimGround` §5 shows the check is
  live (CTL-A: removing the target file → exit 1).
- **F9 — two copies of the rows exist; the validated one wins.** `R43AssimGround/rows/normalized-rows.md`
  is census-green (NF=13, mirror validate exit 0, 13 pre-existing W04) and anchors its own fetches;
  `sources-rows.md` now says so and keeps my table as the cross-check. The two disagree on nothing
  substantive — same ids, same kinds, same `used-by`, same `180d`.

## 6. Out of scope (not touched)

C1 (SquashFS v4 table, counter, held-out set, generator), C2 (local-source gate and copies), the S135
row, the quarantine slice hand-check, `considerthese/` (absent — the report line belongs to whichever
seat owns it, not to this one), the freeze, the integration commit, `SCORECARD.md`, `PROVINCE.md`,
`SKILL.md`, `LOG.md`.

## 7. Artifacts

Manifest: `artifacts/R43ScribeAssim/sha256-manifest.txt`.

```
30bf9688092f2a35fe45a1d484626fa20c9ae471b6e4e10d7fecd37893510041  drafts/2026-10-27-sasquatch-release-matrix.md
0f2ede7f5c33d2999637fbda06e2abe0cfadba2a88bf983123bf88984bec951b  drafts/sources-rows.md
d55c477fd6ff854795517307b85d9abb1accff8c471ba4eb6220de1d4db8e20e  receipts/capture-diff-r42-r43.txt
7d955209b808b8aaff57f1fd503d82f5db4c9f026ee6ab0964a3a82aaebef423  receipts/capture-projection.txt
d0d805267c79c2a6042654be770e213520abf09ae2b0b5eb3d9a61d6f37e8fa0  receipts/id-collision.txt
2108278966bf12fddf3ef3b5e82f021766263fa3b25b17ef942f747363f1ffbb  receipts/id-guard-fixture.txt
47fc7d7bac3cf784fb25bb9fa2af657b849ba7da22034f65bb62b8110b4fc12f  receipts/page-fetch2.txt
dbf12ce7885de9eb510307d8e1933eeec8262841daa62904d49eb33abcc83f31  receipts/page-probe.txt
956c229a03c8ffab724cd73ab46d24b4ad0462597354d4ceb1396f17f3909745  receipts/recheck-jq.txt
cb42cd61728f994dc18e4937d2d173b543c6a976bea25fa922e50f7213a105d0  receipts/rel-r43.json
56632d0f19d7e7e81776e9a48e04f7ce4b89d32f9c79670617e5f2c888cb1cea  receipts/sasq-releases-r43-f2.html
89e7377d92132bfa1bf1a004bf38a6f105dfe85ea99a753cccde49af29227a67  receipts/sasq-releases-r43.html
1d5b32922c56145de220d36c2224fef124fa52bba4142acfaba367c8155db81a  receipts/serialization-check.txt
1d1dffbc7ff07cf36b07372499483c3d75eec71225f05f017d30bc1fc3335e51  receipts/version-pair-scan.txt
```

`receipts/rel-r43.json` (107313 B) and the two retained page fetches (349255 B each, digests `89e7377d…`
and `56632d0f…`) are the captured
responses — all under 5 MB, none is a firmware image nor anything carved from one. Rebuild: the
commands in §2 rows 1 and 5; `sha256sum -c sha256-manifest.txt` → all 14 `OK`.

## 8. Limits of this report

- No per-asset pin was obtained for the 42 older assets (would need downloads); marked, not guessed.
- The `R43AssimGround` evidence did not exist while this seat ran; the entry carries the placeholder
  and this report does not pretend otherwise.
- One API fetch, two page fetches; the API response is mutable by design (F5/§1), so today's digest is
  evidence of *today's* bytes only, which is why nothing in the entry is pinned by response digest.
- Scalar claims about other seats' work (F1, F2) are read-only observations of files on disk at
  08:19–08:22Z; they are not verdicts.

## 9. Corrections applied after the L1's IRC (R43-AG1, AG2, AG3)

All three were **real defects in this seat's output**, applied to the draft and the receipts before
re-filing; the front-matter order and the pinned projection are unchanged.

- **AG1 — the size comparison was wrong, and I confirmed it rather than accepting it.** Round 42's
  `receipts/rel.json` is a `jq -c` **compact** serialization (87700 B, 0 newlines); my receipt is the
  pretty HTTP body (107313 B, 1944 lines). `jq -c .` on each yields **87701 B for both**, `jq -S -c .`
  yields 87701 for both, and deleting `download_count` makes the two payloads **diff-identical (0
  lines)**. The seven counters that did move: `v4.5.1-6` dbgsym_amd64 160→161, `v4.5.1-6` amd64
  23694→23773, `v4.5.1-6` arm64 2404→2411, `v4.5.1-5` amd64 34473→34483, `v4.5.1-5` arm64 2334→2337,
  `v4.5.1-4` amd64 51254→51262, `v4.5.1-4` arm64 2748→2749. The entry's limits paragraph now says
  "serialization, not drift" and gives the counter list; receipt
  `receipts/serialization-check.txt`.
- **AG2 — resolved by retaining bytes, not by citing an unretained digest.** My earlier 349250 B /
  `d68fabf7…` fetch was overwritten in scratch and is **not** retained, so that citation is gone from
  both drafts. Replaced with retained evidence: fetch 1 `receipts/sasq-releases-r43.html` (349255 B,
  `89e7377d…`), fetch 2 `receipts/sasq-releases-r43-f2.html` (349255 B, `56632d0f…`) — **same length,
  different bytes**, which is the cleanest form of the point — plus round 42's retained 349266 B /
  `71ebf160…` fetch, cited by its lane path. Receipt `receipts/page-fetch2.txt`.
- **AG3 — the indented fixture is now exercised, and the caveat is discharged explicitly.**
  `receipts/id-guard-fixture.txt`: on `| S001 |`, `  | S002 |`, `   | S777 |`, `| S003 |` the
  column-zero pattern returns `S001 S003` (misses both indented rows) while `^ *\| S[0-9]+ ` returns
  `S001 S002 S003 S777`; counts 2 vs 4. The note in `sources-rows.md` now says the equal-count test —
  not the pattern — is what licenses the narrow form, and cites that receipt.

- **Placeholder `<<L1:assim evidence>>` closed, not deferred.** `R43AssimGround` published at 09:00Z
  (report + `rows/normalized-rows.md` + receipts); its independent re-derivation matches this seat's
  on every cell, and its extra probes (`?page=2` → 0 items; 19 tags of which 8 are release tags;
  `~/.local/bin/sasquatch` re-hashed unchanged on 2026-10-27) are now cited in the entry's
  `Re-grounded in-wave (2026-10-27)` paragraph. Its own §7 flags AG1/AG2/AG3; all three were already
  corrected here, and its §3 indented-fixture result agrees with `receipts/id-guard-fixture.txt`
  (narrow pattern 2/4, 0–3-space 4/4).

What did **not** change, because it was verified and holds: the 8-release matrix and every size, the
`[6,6,6,6,6,6,6,2]` counts, the `digest`-presence pattern `[6,0,0,0,0,0,0,0]`, the body finding (five
empty; 645/560/38 B; zero standalone `1.0` tokens; `v4.5.1-1` names only the upstream base), the page's
8 tags and 0 asset filenames, the 29 id collisions, and the `recheck:` line's output.
