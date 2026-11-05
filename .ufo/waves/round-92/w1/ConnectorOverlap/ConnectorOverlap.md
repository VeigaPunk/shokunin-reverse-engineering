# ConnectorOverlap — round 92 sibling-overlap sweep (read-only)

Seat: ConnectorOverlap (connector). Lane: kaidoku-shokunin. Declaration commit `11f8606178dfd9e72001b31daf412c5463106a63` (base `73a882712907606eba074377b536c6dd82517e25`). Claims read before starting: `plans/round-92-claims.md`, `.ufo/waves/round-92/claims.json`. No sibling repo or lane file was edited; the only writes are this report at the two paths listed at the end. Tools installed: none. pacman was not run. No host state changed. Scratch (`/fast/scratch/hyaku/kaidoku-r92/ConnectorOverlap`) held no artifacts (all evidence inline below) and was removed before yield.

## Item

Find any other shokunin lane that claims the UPX stop-boundary / `sz_cpr` / `upx -t` repair class, or any tool named `stop-boundary*`, `search-repair` or `R92`; name the packed-ELF/UPX adjacency across sibling SKILL.md/PROVINCE.md; deliver a hit table, a contested-scope verdict, and the one sibling most relevant.

## Commands and exit codes (all read-only, cwd `/home/vgpnk/Projects/shokunin`)

1. Seat command: `grep -rIl --exclude-dir=.git -e 'stop-boundary' -e 'sz_cpr' -e 'upx -t' /home/vgpnk/Projects/shokunin --include='*.py' --include='*.md' --include='*.json' | grep -v kaidoku-shokunin | head -200` → exit 0, 7 files (section "Hit table"). Output was read, not written through any writer.
2. Name scan: same tree, `-e 'search-repair' -e 'R92'` → exit 0, 134 files, all classified below (section "Name collisions").
3. `search-repair` isolated: `grep -rIn --exclude-dir=.git -e 'search-repair' … | grep -v kaidoku-shokunin` → exit 0, **zero matches outside kaidoku**.
4. Adjacency: `grep -il UPX /home/vgpnk/Projects/shokunin/*/SKILL.md /home/vgpnk/Projects/shokunin/*/PROVINCE.md | grep -v kaidoku-shokunin` → exit 1 (no matches). Sanity run without the filter (exit 0): only `kaidoku-shokunin/SKILL.md` and `kaidoku-shokunin/PROVINCE.md` contain `UPX`. `grep -il packed` on the same set → exit 0, two files, both unrelated (see below).
5. Filename sweep: `find /home/vgpnk/Projects/shokunin \( -path '*/.git' -o -path '*/.jj' -o -path '*/.scratch' \) -prune -o \( -name '*stop-boundary*' -o -name '*search-repair*' -o -name 'R92*' \) -print | grep -v kaidoku-shokunin` → exit 1, no output: **no sibling file carries any of the three names**. Glob across the fleet confirms such names exist only inside kaidoku (`tools/round-92/stop-boundary-repair-battery.py`, `tools/round-92/stop-boundary-battery-v2.py`, `tools/round-91/*`, `corpus/knowledge/2026-11-05-r91-stop-boundary-refusal.md`).
6. MANIFEST attribution: python3 read-only walk of `/home/vgpnk/Projects/shokunin/MANIFEST.json` filtering `UPX|sz_cpr|stop-boundary` → every matching capability row has `lane = kaidoku` (rounds 68 packed-ELF route, 87 `UPX magic-tamper repair`, 88 notes, 90 `UPX packed-ELF interior later-block b_info.sz_cpr repair`, 91 `last-block stop-boundary refusal`). No other lane appears.

## Hit table (seat command, class terms `stop-boundary` / `sz_cpr` / `upx -t`)

| lane | path (absolute) | line | what it claims |
|---|---|---|---|
| — (fleet mirror of kaidoku, self) | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-87/kaidoku.md` | 7 | kaidoku's own R87-C1: anti-UPX magic-overwrite repair; `upx -t/-l/-d` answered `NotPackedException` → repair restores `UPX!` magic. |
| — (fleet mirror of kaidoku, self) | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-88/kaidoku.md` | 11, 59, 84, 145, 171 | kaidoku's own R88-C1: zeroed first `b_info.sz_cpr` repaired from chain geometry; `sz_unc` vs `sz_cpr` separation. |
| — (fleet mirror of kaidoku, self) | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-89/kaidoku.md` | 14, 25 | kaidoku's own R89-C1: in-range wrong first-block `sz_cpr` class. |
| — (fleet mirror of kaidoku, self) | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-90/kaidoku.md` | 12, 160, 192 | kaidoku's own R90-C1: interior later-block `sz_cpr` repair; last-block class still Frontier at that round. |
| — (fleet mirror of kaidoku, self) | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-91/kaidoku.md` | 7, 13-19, 42-45, 99 | kaidoku's own R91-C1: last-block stop-boundary measured **refusal** (rc 2); the same report's SHONEN row cites `w1/ConnectorOverlap.md` finding no sibling claim. |
| revenger | `/home/vgpnk/Projects/shokunin/revenger-shokunin/reports/round-73/tool-probes.md` | 82-83 | **Not a claim on the class.** Tool-inventory probe rows: `upx --version` → `upx 5.2.0` (rc 0, 2026-10-29); `upx -t /usr/bin/true` → rc 2 `NotPackedException` "expected for an unpacked binary". No `sz_cpr`, no stop-boundary, no repair, no battery. |
| — (fleet manifest, self rows only) | `/home/vgpnk/Projects/shokunin/MANIFEST.json` | 48150, 48586, 50067 | capability strings for kaidoku rounds (see command 6): round-90 interior `sz_cpr` repair, round-91 stop-boundary refusal; round-88 recheck note quoting `upx -t` / `sz_cpr` values. Attribution walk: all `lane = kaidoku`. |

The seat command's `grep -v kaidoku-shokunin` filter cannot exclude items 1-5 because the fleet-level `.ufo/reports/round-*/kaidoku.md` paths do not contain the lane directory name. They are the lane's own round reports mirrored at fleet level — **self-hits, not sibling overlap**. Stated as a filter artifact, not smoothed away.

## Adjacency: packed-ELF / UPX work in sibling lanes

- `SKILL.md`/`PROVINCE.md` UPX check: **zero sibling lanes mention UPX** (command 4; only kaidoku's own two files match).
- `packed` (lowercase) hits, both unrelated to packed-ELF:
  - `souji-shokunin/SKILL.md:115` — "a keep ref is removed by jj's ref-set rewrite, and a **packed** one skips the age gate": git/jj packed-*refs* storage. Not binary packing.
  - `tsukuroi-shokunin/SKILL.md:2596` et al. — git "**packed objects**" fingerprints and pacman `.MTREE` "re-packed" wording in its write-leak and package counters. Not binary packing.
- Round-91's wider sibling sweep (`kaidoku-shokunin/.ufo/waves/round-91/w1/ConnectorOverlap.md`, read for continuity) had already classified the low-grade `upx ` prose noise (tsukuroi 12, mado 4, kotodama 2, kumitate 2, tabi 2, kengaku 1, game-dev-3d 1, revenger 2 files, none class-bearing) and the tameshi `record-cells` shared primitive. This round's fresh scan found **no new sibling material since that verdict**: no sibling SKILL/PROVINCE gained UPX ground, and the only class-vocabulary hits remain the ones above.

## Name collisions (`R92`, `search-repair`, `stop-boundary*`)

- `search-repair`: **zero** matches outside kaidoku (command 3).
- `stop-boundary*` as filename: zero outside kaidoku (command 5).
- `R92` matches are other lanes' **own round numbers and one rule number** — name collision only, no content relation to kaidoku R92-C1/C2:
  - `audio-shokunin/corpus/live/r92-*`, `reports/round-92/r92-{scout,boundary,reviewer}.md` — audio's own round 92 (simplifier/scout seats; audio-content).
  - `game-dev-2d-shokunin/reports/round-92/r92-*.md`, `corpus/live/r92-*/…` — game-dev-2d's own round 92 (run_battery fixtures, verdicts.json; 2D-content).
  - `lore-shokunin/.ufo/waves/round-91/patches/Q1-r92-proposal.md:11` — "Q1-R92-C1 — Make the r90 repaired provenance rules regression-visible in the delivered corpus": lore's own round-92 proposal about provenance rules, not UPX.
  - `kake-shokunin/.ufo/waves/round-92/freeze.md:8` — "Author: kake L1 (`KakeR92`). Round shape: one v1 wave of 14 seats": kake's own round 92.
  - `kasegi-shokunin/corpus/QUALITY.md:502` — quality-rule row `| R92 |` requiring receipts to carry driver digest + measured revision; cited by `corpus/lessons/round-66.md`. kasegi's rule numbering, not kaidoku's round label.
  - Fleet mirrors `.ufo/reports/round-92/{lore,kake}.md`, `.ufo/reports/round-{38,66}/*.md` — sibling round reports at fleet level.
- Main-agent caution: do not read the name-scan's R92 files as competitors; they are numbering collisions.

## Verdict on contested scope

**None.** No sibling lane claims the UPX 5.2.0 packed-ELF last-block stop-boundary / `sz_cpr` / `upx -t` repair class; no sibling file or tool is named `stop-boundary*`, `search-repair` or `R92` (R92 strings are other lanes' own round/rule numbers). The class exists only in kaidoku (tools/round-91 + frozen tools/round-92 + corpus/knowledge/2026-11-05-r91 + fleet mirrors of kaidoku's own reports). This confirms, freshly at the round-92 declaration commit, the round-91 connector's "no sibling lane claims the class" verdict; no drift since.

**Adjacency (named):** `revenger-shokunin` is the only sibling with any UPX trace: its round-73 RE-toolbench report (2026-10-29) documents host `upx 5.2.0` (`upx --version` rc 0) and a `upx -t` probe — tool availability only, zero claim on the tamper/repair class. souji and tsukuroi touch the word "packed" only for git packed refs/objects and pacman archives.

**Sibling most relevant:** `revenger-shokunin` — its round-73 probe row is an independent, sibling-authored host record of the exact packer (5.2.0) whose verdict decides R92-C1's repair window and R92-C2's typed refusal.

## Affected axes

- **coverage**: unharmed and clarified — R92-C1's repair ground has no sibling duplicate; no dedupe or descope is warranted.
- **calibration**: unaffected — no sibling counter or refusal-label work competes with the frozen `stop-boundary-battery-v2.py`; the R92 collisions carry no measurement claims.
- **freshness**: small positive available (move below) — one independent host-side witness for the pinned packer exists and is current (host `upx 5.2.0`, observed 2026-10-29, unchanged by any later sibling record found).
- **depth**: unaffected — no sibling SKILL/PROVINCE holds packed-ELF craft or decision tables on this class.

## One bounded move (connector proposal; does not touch frozen predicates, counters, labels or kill rules)

Cite `revenger-shokunin/reports/round-73/tool-probes.md:82-83` as a **host-environment corroboration row** (independent second lane observing `upx 5.2.0` live on this host, probed 2026-10-29) in the round-92 wave's knowledge draft / Gate notes for R92-C1 and R92-C2 — the claims whose repair/refusal verdicts are delegated to `upx -t` under the packer pin. Read-only citation only; nothing is written into revenger; no frozen artifact changes; kill rules untouched (citations live in wave prose, not in `claims.json`, counters or labels). Second-order effects checked: runtime/contract/substrate surfaces unaffected; verification surface gains an independent non-kaidoku provenance witness for the packer-version dependency. Risks: (a) a cross-lane citation could be misread as domain bleed — mitigate by wording it strictly as host tool-inventory evidence, not as a lane claim (revenger documents the binary's presence, nothing about the class); (b) the probe predates the round — mitigated by pairing it with the lane's own sha256 packer pin, which remains the binding identity.

## Contradictions / tensions (stated, not smoothed)

1. Filter artifact: the seat command reports five fleet-mirror `kaidoku.md` files as hits though they are self-records (see Hit table note).
2. The round-91 report's SHONEN row cites the sibling sweep as `w1/ConnectorOverlap.md` (flat), while this round's seat spec also names a seat directory; this report is written to both named paths to satisfy each instruction without touching any non-seat lane file.
3. revenger's round-73 installed tools via pacman before the current host-wide pacman pause; historical record, no present-tense conflict with the pause rule.

## Verification (main agent re-check, ~1 min)

```
grep -rIl --exclude-dir=.git -e 'stop-boundary' -e 'sz_cpr' -e 'upx -t' /home/vgpnk/Projects/shokunin --include='*.py' --include='*.md' --include='*.json' 2>/dev/null | grep -v kaidoku-shokunin
grep -rIn --exclude-dir=.git -e 'search-repair' /home/vgpnk/Projects/shokunin --include='*.py' --include='*.md' --include='*.json' 2>/dev/null | grep -v kaidoku-shokunin   # expect empty
grep -il UPX /home/vgpnk/Projects/shokunin/*/SKILL.md /home/vgpnk/Projects/shokunin/*/PROVINCE.md 2>/dev/null   # expect kaidoku only
sed -n '82,83p' /home/vgpnk/Projects/shokunin/revenger-shokunin/reports/round-73/tool-probes.md
```

## Files written

- `.ufo/waves/round-92/w1/ConnectorOverlap/ConnectorOverlap.md` (this file, seat dir)
- `.ufo/waves/round-92/w1/ConnectorOverlap.md` (same content, at the Report trailer path named by the seat spec)

No other lane or fleet file was created, edited or deleted. Scratch removed.
