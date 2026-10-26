# R36W2ReviewerEntryAssim — wave-2 falsification: assimilated entry `unblob-sasquatch-dependency`

Seat: reviewer (leaf), round 36 wave 2, 2026-10-26. Scope: compare the lane's admitted entry
`corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md` with the staged package entry
`/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/unblob-sasquatch-dependency.md`
and round-36 lesson `## Gate` decision 1 — corrections c1 (pin by tag/commit/sha), c2 (inference
labelled, host-state re-scoped), c3 (no "fork" wording); ungrounded carry-over; renumber map
(staged S106→S110, S107→S111) by document. Judged on coverage and calibration.

Bounds: this report is the only file written. `/home/vgpnk/Projects/shokuknow` accessed read-only
(file reads of the staged package only; no campaign tool run there). Read-only git in the lane
(`show`, `log`, `diff`, `status`, `rev-parse`) plus `git ls-remote` against github.com (network
read; no lane VCS mutation). No pacman transaction, no tool installed or upgraded, no subagents,
no background jobs, no `agent://all`. Scratch `/fast/scratch/hyaku/kaidoku-r36/R36W2ReviewerEntryAssim`
removed before finishing; every cited value is embedded below.

## 0. Mid-review lane mutation (disclosure — affects what "landed" means)

The lane moved while this seat worked:

| time (2026-10-26 -03) | event | evidence |
|---|---|---|
| (assignment tip) | integration tip `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930` | assignment |
| 02:01:31 | `6f2ba761` "wave-1 results (43/43 settled) and last report; wave-2 spec/dispatch" — no corpus change | `git log --oneline 01a44dbf..HEAD` |
| 02:07:46 | wave-2 corrections applied to the **working tree**: entry, `corpus/SOURCES.md`, `corpus/lessons/round-36.md` (plus `PROVINCE.md`, `corpus/README.md`) | `stat` mtime `2026-10-26 02:07:46.327720867 -0300`; `git status --porcelain -- corpus/` → 3 × `M` |
| 02:11:08 | `38c1a8be` "wave-2 corrections (assimilated entry pip-route scope + Very-beta attribution, S107 asset set, S111 teaches, lesson quote count, dated pointers on superseded PROVINCE/README lines)" | `git log -1 --format='%H %ci %s'` |

This seat's **first read of the entry returned the pre-correction text** (consequence 2 = "Because
the producer calls its own extractor \"Very beta\"…"); later greps returned the corrected text —
the edit happened between the two reads. After `38c1a8be` the corpus tree is clean; at report time
still dirty: `.ufo/waves/round-36/w2/R36W2CriticAssimDecisions.md`, `R36W2CriticTrends.md`
(sibling seats' reports, mid-write) and untracked `after/c1-final.json`, `after/c2-final.json`,
`census-end.txt`, `w2.ready.dispatched`.

Verdicts in §1–§5 hold for **both** states (the corrections do not touch c1/c2/c3 substance or the
renumber map); §6 reviews the `38c1a8be` corrections themselves.

## 1. c1 — pin by tag/commit/sha256 instead of `HEAD` — **APPLIED**

Staged (staged entry lines 4–7): `source: S106 — …/onekey-sec/unblob/HEAD/README.md … HEAD as
fetched 2026-10-23`, `source: S107 — …/devttys0/sasquatch/master/README.md … as fetched
2026-10-23`, `recheck: 180d — curl … \| grep -c 'sasquatch' -> 3`.

Landed (entry lines 1–4): `source: S110 — …/unblob/26.6.4/README.md — tag 26.6.4 (commit
1fcc7a0a584a70a96c31f5a276c20944d199a089), 235 lines, sha256 6544d60f…3716, byte-identical to HEAD
on 2026-10-26`; `source: S111 — … sha256 f09961ee…1fef`; `recheck: 180d — curl … | sha256sum →
6544d60f…3716`.

First-hand reproduction (this seat, 2026-10-26):

```
curl -fsSL https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md | sha256sum
  → 6544d60f22f7b521f8705b3bba5d47a50e428ccbd3359542708dbd009ccf3716   (wc -l → 235)
curl -fsSL https://raw.githubusercontent.com/devttys0/sasquatch/master/README.md | sha256sum
  → f09961ee6c2bf5ddadc0c7e52bdfb68e50c877cabec20ec0370f54c311e01fef   (wc -l → 30)
curl -fsSL https://raw.githubusercontent.com/onekey-sec/unblob/HEAD/README.md | sha256sum
  → 6544d60f…3716   (byte-identical to the tag today — the entry's "byte-identical to HEAD on
                     2026-10-26" verified same-day, exit 0)
git ls-remote https://github.com/onekey-sec/unblob refs/tags/26.6.4
  → 1fcc7a0a584a70a96c31f5a276c20944d199a089	refs/tags/26.6.4
```

Registry rows carry the same pins (`corpus/SOURCES.md:116-117`). No floating ref remains in the
entry or its two rows. **No disagreement found.**

## 2. c2 — inference labelled, host-state re-scoped — **APPLIED**

- The entry's one multi-step inference carries the `[INFERENCE]` label (entry line 33,
  consequence 2).
- Host-state re-scope (entry lines 38–43): the staged sentence "the `sasquatch` absence on this
  host is a packaging/build decision" (staged consequence (a)) becomes "the staged text's 'sasquatch
  is absent on this host' was true at the package's 2026-10-23 snapshot and is false from
  2026-10-26" — dated, with evidence.

First-hand host-state reproduction (all commands exit 0):

```
sha256sum ~/.local/bin/sasquatch      → ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754
                                        (= S107's deb-member digest usr/bin/sasquatch)
sha256sum ~/.local/bin/sasquatch-v4be → fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6
                                        (= S107's deb-member digest)
unblob --show-external-dependencies   → "sasquatch ✓", "sasquatch-v4be ✓" (unblob 26.6.4)
~/.local/bin/sasquatch -version       → "unsquashfs version 4.5.1 (2022/03/17)"
grep -o '"dependencies":[^]]*]' corpus/evidence/round-36/c1/K1/before.json
  → "dependencies":["sasquatch"]      (same in K2/K3/K4; all four contain missing-extractor-dependency)
grep -o '"extraction_gaps"[^]]*]' corpus/evidence/round-36/c1/K1/after.json
  → "extraction_gaps":[]              (gap disappears with sasquatch on PATH)
grep -o 'unsquashfs version[^"]*' corpus/evidence/round-36/c1/K1/after-run.json
  → "unsquashfs version 4.5.1 (2022/03/17)"
```

Observation (calibration note, not a defect): the wave-1 scribe's draft c2 also wanted the
packaging-route consequence labelled inference; the landed entry treats it as direct reading of
S110 lines 49–53 (the README literally shows the `curl`/`dpkg -i` commands). The frozen lesson
wording ("inference labelled") is satisfied by the one label.

## 3. c3 — no "fork" wording — **APPLIED**

- Staged carried the claim twice: "The `.deb` is built from onekey-sec's fork (tag
  `sasquatch-v4.5.1-6`)" (staged line 29) and "Upstream `devttys0/sasquatch` and the onekey fork
  are different builds of the same idea" (staged line 32).
- The landed entry contains "fork" exactly once, in **Not claimed** (entry line 47): "…or that the
  onekey-sec package is a fork of devttys0 (neither README says so)."
- "neither README says so" verified first-hand: `grep -inc fork` on the fetched bytes → unblob
  README **1**, devttys0 README **0**; the single unblob occurrence is line 225 "3. Fork the
  repository, implement your changes, and open a pull request." — a contributing instruction, not
  package provenance.
- The replacement wording is grounded: devttys0 `build.sh` downloads squashfs-tools **v4.3**
  (S111 line 26, verified exact); the packaged binary reports **4.5.1** (K1/after-run.json +
  first-hand `-version` above). R36W2ScoutS111 item 8 adds independent git evidence for the
  non-claim (`git merge-base main dev` exit 1 — no common ancestor); this seat verified the
  README-level claim only.

## 4. Staged claims — carry-over audit

| staged statement | landed counterpart | re-grounding |
|---|---|---|
| unblob README makes SquashFS conditional on sasquatch (S106) | Claim ¶, quote at S110 line 49 | fetched tag bytes: line 49 exact, line 43 "Then install the required external extractor tools. On Ubuntu/Debian:" exact; the `apt install` list at line 46 contains no sasquatch |
| "publishes the install as a prebuilt Debian package … (`sasquatch-v4.5.1-6`) … `curl`/`dpkg -i`" | Claim ¶ (post-38c1a8be: "prebuilt `.deb` release asset … (not a distribution package)", pip-route scoped) | fetched lines 51–53: `curl -L -o sasquatch_1.0.deb "https://github.com/onekey-sec/sasquatch/releases/download/sasquatch-v4.5.1-6/sasquatch_1.0_$(dpkg --print-architecture).deb"`; `sudo dpkg -i` |
| sasquatch = patch set over unsquashfs for vendor-specific SquashFS; header fields; LZMA options | "What sasquatch says about itself (S111)" | devttys0 fetched bytes: line 5 (patch set), line 6 (header fields), line 8 (LZMA brute-force) — all exact |
| "Very beta" | consequence 2 + S111 line 12 | exact (`grep -n 'Very beta'` → 12) |
| prerequisites C/C++ + liblzma/liblzo/zlib dev | line 17 | exact (`grep -n 'C/C++ compiler'` → 17) |
| build.sh downloads squashfs-tools v4.3 | line 26 | exact |
| (a) host absence | re-scoped consequence 3 | host verified first-hand (§2) |
| (b) `.deb` second non-AUR path | Claim ¶ + consequence 4 | S110 lines 49–53 |
| (c) very beta ⇒ failed extraction ≠ no SquashFS | [INFERENCE] consequence 2 | labelled; attribution corrected in 38c1a8be (§6) |
| fork caveat | **dropped** (c3), replaced by measured base-version difference | §3 |
| "operator must confirm the package satisfies the pinned unblob's expected sasquatch" | superseded by observation | `unblob --show-external-dependencies` lists sasquatch ✓ (first-hand); K1 after.json `extraction_gaps:[]` |
| `ground: F1` front-matter line | dropped | lane convention: `grep -rl '^ground:' corpus/knowledge/` → 0 files |
| recheck `grep -c 'sasquatch' -> 3` | replaced by sha256 recheck | staged value still reproduces on the tag bytes (`grep -c sasquatch` → 3) |
| staged S107 source line cited `§ "sasquatch"` (heading does not exist) | landed S111 source line cites line numbers 12/17/26 | all three exact (scribe F5 fixed) |

**Result: no staged claim is carried over without re-grounding at the current tip.** In the
*original* landing (pre-38c1a8be) two statements were loose, both caught by wave-2 scouts and
corrected (§6); this seat independently confirms both defects:

- **Attribution slip** (R36W2ScoutS110 D2, R36W2ScoutS111 item 7): original consequence 2 said
  "Because the producer calls its own extractor 'Very beta'" — the entry's own "producer" usage
  (Claim ¶ "(producer contract)") is unblob; the label is devttys0's. Independent confirmation:
  `grep -inc beta` → S110 (unblob README) **0**, S111 (devttys0 README) **1** (line 12). The lane
  runs the onekey-sec package, which S111's scope explicitly excludes.
- **Route overgeneralisation** (R36W2ScoutS110 D1/D3): the sasquatch step sits under
  "### pip (recommended for most users)" (line 38); Docker "bundles all extractors" (line 64) and
  Kali is a single package install — both verified in the fetched bytes.

## 5. Renumber map by document — **CORRECT**

Independent reproduction (not a re-read of the committed evidence):

```
git -C <lane> show 790561d4e3aca732a434081aa9573ec2fa5fd7d0:corpus/SOURCES.md
  → 106 id rows (S001–S106, contiguous)
grep -cE '^\|[[:space:]]*S[0-9]+[[:space:]]*\|' /home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md
  → 132 rows (ids S106–S237)
comm -12 <(freeze ids) <(staged ids) → S106        (exactly one collision)
```

Matches the committed evidence `.ufo/waves/round-36/assimilation/{reg-ids,staged-ids,collisions}`
(106 / 132 / `S106`).

- Document identities: staged S106 = onekey-sec/unblob README (HEAD as fetched 2026-10-23,
  `SOURCES.append.md:7`) → lane **S110** = the same document pinned at tag 26.6.4
  (`corpus/SOURCES.md:116`); staged S107 = devttys0/sasquatch README, master (`SOURCES.append.md:8`)
  → lane **S111** = the same document (`corpus/SOURCES.md:117`). Lane S106 is a *different*
  document (GNU binutils readelf, `corpus/SOURCES.md:112`) — the renumber was required, and it was
  done by document, not by arithmetic.
- Three records agree: the entry's assimilation note (entry line 8: "staged S106 → S110, staged
  S107 → S111"), the rows' own annotations ("staged as package S106/S107, renumbered by document"),
  and the lesson `## Gate` renumber map.
- No duplicate row for either URL: the unblob README URL appears only in S110, the devttys0 URL
  only in S111; the registry's 9 W04 warnings are pre-existing rows (S033, S047, S054, S062, S069,
  S083, S090, S092, S102) — none touches S110/S111 (no census E04).
- "No other staged row is appended": `git diff 790561d4..HEAD -- corpus/SOURCES.md` = exactly
  5 insertions (S107 sasquatch release, S108 squashfs.py, S109 neovim — wave-1 scout rows opened
  first-hand; S110/S111 the mapped rows), **0 deletions** — which also confirms the lesson's "no
  existing row's `status`, `recheck` or `used-by` cell changed this round".
- used-by cells (post-38c1a8be, awk tail-cell extraction): S107 → `…r36-sasquatch-squashfs-recursion.md`,
  S110 and S111 → `…unblob-sasquatch-dependency.md`; status `mined`, opened `2026-10-26` for all.
- Cross-entry consistency (scribe F1 honoured): the C1 entry cites S107/S108/S109 and never cites
  or mints a row for the unblob README (`grep -n 'S110\|unblob README'` on the C1 entry → no source
  citation hit).
- Note: the wave-1 scribe's draft map (staged S106→S107, S107→S108, written at `d2e46ef5` when the
  registry still ended at S106) was superseded because wave-1 took S107–S109; the landed lesson
  records the final map. Consistent, not a defect.

## 6. The mid-review correction commit `38c1a8be` — reviewed

Verified against the fetched source bytes and the GitHub API (exit 0):

- Title/claim re-scoped to the pip route; Docker route "bundles all extractors" at **line 64**
  exact; "prebuilt `.deb` release asset … (not a distribution package)" matches fetched lines 51–53.
- Consequence 2 rewritten with devttys0 attribution; S111 **line 8** quote
  "will attempt to automatically resolve such customizations via a brute-force method" exact
  (`grep -n brute` → 8); line 12 exact.
- S107 anchor now records **six API assets** — verified against
  `https://api.github.com/repos/onekey-sec/sasquatch/releases/tags/sasquatch-v4.5.1-6`:
  `sasquatch-dbgsym_1.0_{amd64,arm64,armhf}.deb` = 323896 / 327784 / 319048 bytes;
  `sasquatch_1.0_{amd64,arm64,armhf}.deb` = 187244 / 170080 / 164428 bytes — all six match.
- S111 `teaches` reworded to the devttys0 attribution; lesson S109 quote count "3 words" →
  "2 words" ("Download nvim-linux-x86_64.appimage" is 2 whitespace tokens) — correct.
- PROVINCE Frontier bullet and README Firmware row gained dated supersession pointers
  (`[2026-10-26: superseded for LE SquashFS v4 …]` / `[2026-10-13 state; superseded 2026-10-26 …]`).
- The entry's parenthetical citations resolve: `R36W2ScoutS110.md` contains D1 (line 42), D2
  (line 47), D3 (line 52); `R36W2ScoutS111.md` item 7 at line 38 — all present and matching the
  corrections applied.

**Defect found in the correction (new, now committed):**

- **F-W2-1 (LOW, locator) — Kali route off by one.** Entry Claim: "its Kali route is a single
  `apt install unblob` (lines 77-79)". The command is at **line 80** of the pinned bytes:
  `grep -n 'apt install unblob'` → 80; line 77 = "### Kali Linux", 78 blank, 79 = "```console".
  The quoted command is not inside the cited range, while the sibling locator in the same sentence
  (Docker, line 64) is exact. Fix: cite line 80 (or 77–80). Report-only seat; not repaired.
- INFO: consequence 2 cites "(lines 6-8)" for the LZMA quote that is at line 8 (line 6 is the
  header-fields sentence; the range contains both vendor-modification sentences). Loose but not
  false; S111's anchor pins line 8 exactly.

## 7. Other observations (severity-ordered)

- **LOW — cadence label mismatch.** Entry `recheck: 180d` (line 4) runs the S110 sha256 command,
  while registry S110's recheck cell is `on-release` (S111's is `180d`). The prose ("a different
  digest means the tag moved") describes on-release semantics coherently; the two records just
  label the cadence differently. Cosmetic.
- **LOW — installer attribution is self-recorded.** "installed by the round-36 L1" (entry
  consequence 3, line 40): the C1 entry's Install provenance section (landed by the L1) describes
  the unpack (`ar x` + `tar -xJf data.tar.xz`) and install without naming an actor;
  `R36SentinelInstall.md` confirms byte-identity to the deb payload but not the actor; wave-1
  repro seats state they installed nothing (`R36ExecReproK1.md:7,178`). [INFERENCE] the attribution
  is right (the C1 entry is the L1's own record and everyone else disclaims installs), but no
  third-party record names the actor.
- **LOW — S111 tier unresolved.** `R36W2ScoutS111.md` §3 argues tier B is wrong by the fleet rule
  text (`/home/vgpnk/Projects/shokunin/CORPUS.md:93-97`: tier A includes "maintainer statement"
  for the row's scope; the devttys0 README is the maintainer's own statement about his own
  project). The row still holds `B` after `38c1a8be` (verified). Unresolved disagreement; flip =
  an integration decision recording why B, or change to A.
- **INFO — package-side bookkeeping.** `merge/kaidoku/MERGE-REPORT.json` says `existing_rows: 105`,
  `accepted: 132`, `renumbered: []` — the package's own snapshot predates lane S106 and performs no
  renumbering; the lane census (106) and the gate recount agree. No lane defect.

## 8. Residual risk / verification gaps

- The GitHub API `git/ref` call was rate-limited (403) for the wave-1 scribe; `git ls-remote` was
  the substitute and this seat reproduced it. This seat's API releases call succeeded (asset sizes
  verified), so the API path is exercised for the asset set but remains unexercised for the tag-ref
  lookup this round.
- This seat did not re-run the C1/C2 counters or re-derive claim verdicts (other wave-2 seats'
  scope); only the receipt facts the entry cites were checked (before/after gap records, version
  string, digests).
- No language server applies (markdown corpus comparison; no code in scope) — text- and git-level
  checks only.
- The two still-dirty sibling reports (`R36W2CriticAssimDecisions.md`, `R36W2CriticTrends.md`) were
  mid-write during this review and were not assessed (out of seat scope).

## 9. Answers to the assigned questions

1. **Were c1, c2, c3 applied?** Yes — all three, verified first-hand at both the assignment tip
   (entry as landed in `ffc81341`) and after the mid-review correction commit `38c1a8be` (§1–§3).
2. **Is any staged claim carried over without re-grounding?** No, at the current tip (§4 audit).
   The original landing carried two loose statements (Very-beta attribution; packaging-route
   scope); wave-2 scouts caught both, the L1 corrected both in `38c1a8be`, and this seat
   independently confirms both defects and the corrections' grounding.
3. **Is the renumber map (staged S106→S110, S107→S111) by document correct?** Yes — independently
   reproduced end-to-end: sole collision S106 at the freeze, document identities match, rows
   self-annotate, no duplicate URLs, used-by correct, no other staged row appended (§5).
4. **New findings:** F-W2-1 (Kali locator off by one, committed in `38c1a8be`); S111 tier B vs the
   fleet rule text (unresolved); entry-vs-registry recheck cadence label mismatch; installer
   attribution self-recorded. No frozen predicate, counter, carrier or oracle was touched; no lane
   repair attempted.
