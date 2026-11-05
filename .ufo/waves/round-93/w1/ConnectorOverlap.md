# ConnectorOverlap — round 93 sibling-overlap scan (read-only)

Seat: ConnectorOverlap (connector), lane kaidoku, round 93, L1 KaidokuR93.
Scope: read-only greps over every sibling `*-shokunin/` (corpus/, plans/, PROVINCE.md, SCORECARD.md; `.md` only unless noted).
No lane file, sibling file, counter or manifest was written. Only this report and receipt files in this seat directory.

## Verdict

- **R93-C1 surface (fresh-pack held-out arm, nonce-marked carrier, UPX stop-boundary repair): no sibling claims the class.** The terms `fresh-pack`, `stop-boundary` and `sz_cpr` occur only in kaidoku (31 `.md` files in scope). `sz_unc`, `UPX 5`, and packed-ELF `b_info` do not occur in any sibling `.md` outside kaidoku. One sibling records upx 5.2.0 as a host tool probe: corroboration of the tool version only, no class claim.
- **R93-C2 surface (craft citation semantics, D-91-3): no sibling holds a craft-row citation rule.** One sibling lesson (tameshi) uses the same failure wording ("a criterion citation that does not say what it is cited for") as a lesson-class label. It is a label in a different lane, not a claim on the same rule.
- Shared *method* (held-out forgery or counterfeit batteries, repairs tuned on their own battery) appears in several siblings. These are separate claims on separate classes, with no shared counter, file, predicate or manifest. Recorded below as method overlap only.

No sibling claim overlaps the R93-C1 or R93-C2 claim surface. Nothing requires a coordination message.

## Commands run (all read-only; cwd `/home/vgpnk/Projects/shokunin`)

Per-sibling file counts (receipt: `hit-counts-by-sibling.txt`):

```
for p in 'fresh-pack' 'stop-boundary' 'sz_cpr' 'held-out' 'criterion citation' 'mis-stat' 'citation semantics' 'D-91-3'; do
  for d in */; do d=${d%/};
    n=$(grep -rIil -F -- "$p" --include='*.md' "$d/corpus" "$d/plans" "$d/PROVINCE.md" "$d/SCORECARD.md" 2>/dev/null | wc -l)
    [ "$n" -gt 0 ] && echo "$d $n"; done; done
```
Exit 0 (the loop's last test is the only `[ ]`; the pipeline itself succeeded).

Hit counts, files per sibling (scoped, `.md` in corpus/plans/PROVINCE/SCORECARD):

| pattern | siblings with hits (files) | total files |
|---|---|---|
| `fresh-pack` | kaidoku 9 | 9 |
| `stop-boundary` | kaidoku 14 | 14 |
| `sz_cpr` | kaidoku 29 | 29 |
| `held-out` | audio 4, chousa 20, game-dev-3d 1, kagi 1, kaidoku 55, kake 9, kasegi 2, kengaku 42, kotoba 12, kotodama 5, kumitate 4, mado 9, mori 9, revenger 4, souji 4, tabi 1, tameshi 11, tsukuroi 4 | 197 |
| `criterion citation` | kaidoku 1, tameshi 1 | 2 |
| `citation semantics` | kaidoku 1, kama 1 | 2 |
| `mis-stat` | chousa 1, kaidoku 1, kotodama 1, kumitate 2, mori 4, revenger 1, tabi 2, tameshi 1 | 13 |
| `D-91-3` | kaidoku 5 | 5 |

Combined class check (receipt: `scoped-exact-hits.txt`, last lines):

```
grep -rIl -E -- 'fresh-pack|stop-boundary|sz_cpr' --include='*.md' */corpus */plans */PROVINCE.md */SCORECARD.md | cut -d/ -f1 | sort | uniq -c
→ 31 kaidoku-shokunin        (no other sibling)
```

Sibling upx / citation / packed-ELF context (receipts: `sibling-upx-and-citation-context.txt`, `held-out-counterfeit-siblings.txt`):

```
grep -rIn -i -- 'upx' --include='*.md' <siblings except kaidoku>   # pre-filter, large; see receipt
grep -rIn -- 'criterion citation|citation semantics' ...
grep -rIn -i -- 'never refuse an intact|intact input|packer.s verdict|guard inheritance' <siblings>   # 0 hits
grep -rIl -i -- 'upx' --include='SKILL.md' --include='*.py' <siblings>   # hits only fixture/data/pacman NEWS; no tool or skill
```

**Disclosure on noise.** The first, unscoped pass returned interleaved output, including `.raw`, `.js` and `.uid` matches that the `--include='*.md'` filter should have excluded. I did not use those lines. Every claim in this report is based on the scoped reruns above, whose receipts are in this directory. The large `upx` sibling receipt contains mostly `.jj/` operation-store and vendored-JS noise. The relevant hits are listed below.

## Per-hit context

### (1) fresh-pack / held-out / nonce-marked carrier / UPX stop-boundary repair

- **kaidoku only** for `fresh-pack`, `stop-boundary`, `sz_cpr`. Own lane files, e.g. `kaidoku-shokunin/corpus/lessons/round-92.md:54-55` (M92-d pinned-image table; CHEAT-D/E), `kaidoku-shokunin/plans/round-93-claims.md:17` (R93-C1 claim). This is the lane's own surface.
- **Upx 5.2.0, host probe (corroboration only, no class claim):**
  - `revenger-shokunin/reports/round-73/tool-probes.md:82` — `upx --version` → rc 0, `upx 5.2.0`, dated 2026-10-29.
  - `revenger-shokunin/reports/round-73/tool-probes.md:83` — `upx -t /usr/bin/true` → rc 2, `NotPackedException: not packed by UPX`.
  - This records tool presence and version. It does not decompress, repair, or classify any packed ELF. The `upx 5.2.0` version match is corroboration of the pin, not a claim overlap.
- **Host install record (not a claim):** `tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/pacman.log:2083` — `installed upx (5.2.0-1)`. Recorded for completeness; unrelated to the class.
- **Sibling connector overlap files that mention kaidoku's packed-ELF territory (descriptive, no claim):**
  - `kumitate-shokunin/.ufo/waves/round-89/w1/K89Connector.md:72` — "Kaidoku performs packed-ELF reverse engineering, UPX carrier verification…". Descriptive of kaidoku, no claim on the class.
  - `kengaku-shokunin/.ufo/waves/round-90/w1/ConnectorOverlap/overlap.md:112` — a prior connector scan that names UPX / packed-ELF among its scanned terms and says its own seat (same directory name) is a different lane and item. Descriptive, no claim on the class.
  - `tabi-shokunin/.ufo/waves/round-64/w1/R64Connector/sibling-overlap-scan-r64.tsv:14-16` — lists kaidoku's own SKILL.md rows (self-reference, not sibling).
- **`held-out` in packer/refusal sense:** none found in any sibling. The 197 `held-out` files are generic (test-set or battery sense). The only sibling `held-out` lines that co-occur with carrier, refusal, label or counterfeit terms are listed as method overlap below.

### Method overlap (principle only, no shared claim)

Each sibling runs a held-out forgery or counterfeit battery for its own class. Hits:

- `revenger-shokunin/corpus/lessons/round-90-verifier-spotcheck.md:229` — "Attack `oracle_check3.py` with a fresh held-out forgery set before freezing it — its 0/40 is fitted."
- `mori-shokunin/corpus/lessons/round-89.md:37` — `repair-scored-on-its-own-fitting-battery`: a repair declared harm-free on its own battery; 78 new cases measured 12 harms.
- `mori-shokunin/corpus/lessons/round-89.md:90` and `mori-shokunin/SCORECARD.md:4576` — 30 of 78 held-out counterfeits still bind (named limit).
- `kengaku-shokunin/SCORECARD.md:2014` — held-out predictor leg V11.
- `chousa-shokunin/corpus/lessons/round-47-verifier-spotcheck.md:29` — held-out false-refusal evidence.

Relevance to R93-C1: the fresh-pack held-out arm is the same method (freeze a battery the repair's author did not write). No sibling counter, file, predicate or manifest is shared. Cite the method, not a sibling claim.

### (2) craft citation semantics / criterion mis-states / D-91-3

- **kaidoku (own lane, D-91-3 chain):**
  - `kaidoku-shokunin/corpus/lessons/round-91-verifier-spotcheck.md:169` — D-91-3 (block 31 row 3 cites QUALITY 169).
  - `kaidoku-shokunin/corpus/lessons/round-92.md:47` — D-91-3 not fixed on purpose.
  - `kaidoku-shokunin/corpus/lessons/round-92-verifier-spotcheck.md:45` and `:74` — deferred to round 93.
  - `kaidoku-shokunin/plans/round-93-claims.md:59-74` — R93-C2 claim.
- **tameshi (label overlap, not a claim):** `tameshi-shokunin/corpus/lessons/round-48.md:209` — "Class: reference-drift (a criterion citation that does not say what it is cited for) + misattributed reason." This is the same failure described in a different lane's lesson, labelled `reference-drift`. Tameshi holds no craft-block or QUALITY row on this rule (`tameshi-shokunin/corpus/QUALITY.md:1868` uses `reference-drift` as a round-60 mistake class, unrelated to craft rows). Suggest the kaidoku QUALITY row 188 text keep its own wording and not adopt the tameshi label as a cross-lane rule.
- **kama (unrelated):** `kama-shokunin/corpus/SOURCES.md:360` — "report-citation semantics" is a SOURCES-row lesson label about soname and abbreviation identity. No overlap with craft criterion statements.
- **mis-stat (generic prose, unrelated):** chousa `corpus/knowledge/audit-r11.md:138`; kotodama `corpus/lessons/round-17.md:88`; kumitate `corpus/lessons/round-60-verifier-spotcheck.md:35`, `round-81-verifier-spotcheck.md:215`; mori `corpus/lessons/round-70-verifier-spotcheck.md:184`, `round-71.md:95`, `round-78-verifier-spotcheck.md:116`, `round-79-verifier-spotcheck.md:51`; revenger `corpus/lessons/round-67-verifier-spotcheck.md:234`; tabi `corpus/knowledge/webdriver-bidi-firefox-runtime-round-35.md:252`, `corpus/lessons/round-32-verifier-spotcheck.md:87`; tameshi `corpus/lessons/round-47-verifier-spotcheck.md:43`. None concerns craft criterion citations.

## Named overlaps (file:line), for the record

1. `revenger-shokunin/reports/round-73/tool-probes.md:82-83` — upx 5.2.0 host probe. Corroboration of tool version, not a class claim.
2. `tameshi-shokunin/corpus/lessons/round-48.md:209` — same failure wording as D-91-3, different lane. Label overlap only.
3. `revenger-shokunin/corpus/lessons/round-90-verifier-spotcheck.md:229`, `mori-shokunin/corpus/lessons/round-89.md:37,90`, `mori-shokunin/SCORECARD.md:4576` — held-out battery method. Method overlap only.

No sibling claims the packed-ELF stop-boundary class, the fresh-pack oracle, or the craft citation semantics.

## Tooling and host

No tool was installed or upgraded. No host state was touched. Read-only grep and `sed` only.

## Files written

- `kaidoku-shokunin/.ufo/waves/round-93/w1/ConnectorOverlap/ConnectorOverlap.md` (this report)
- `kaidoku-shokunin/.ufo/waves/round-93/w1/ConnectorOverlap/hit-counts-by-sibling.txt`
- `kaidoku-shokunin/.ufo/waves/round-93/w1/ConnectorOverlap/scoped-exact-hits.txt`
- `kaidoku-shokunin/.ufo/waves/round-93/w1/ConnectorOverlap/sibling-upx-and-citation-context.txt`
- `kaidoku-shokunin/.ufo/waves/round-93/w1/ConnectorOverlap/held-out-counterfeit-siblings.txt`

Scratch `/fast/scratch/hyaku/kaidoku-r93/ConnectorOverlap` was created and is removed before yield.
