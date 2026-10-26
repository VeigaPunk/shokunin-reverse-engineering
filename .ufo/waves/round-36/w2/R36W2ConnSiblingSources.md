# R36W2ConnSiblingSources — cross-lane source overlap for kaidoku S107–S111

Method (2026-10-26, wave-2 leaf seat, read-only over siblings): enumerated every sibling lane with
`corpus/SOURCES.md` under `/home/vgpnk/Projects/shokunin/*-shokunin` (20 of 20 siblings have one;
no sibling has any other `SOURCES.md` at depth ≤3 outside `corpus/`), then grepped each for (a) the
five URLs of kaidoku rows S107–S111 and (b) any `sasquatch|unblob|squashfs|squash` content, plus
partial-overlap patterns `onekey-sec`, `devttys0`, `neovim`, `appimage`. Kaidoku row cells verified
at `corpus/SOURCES.md:113-117` (tip `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930`). No tools installed;
scratch `/fast/scratch/hyaku/kaidoku-r36/R36W2ConnSiblingSources` (created per spec, empty, removed).

## 1. Exact-URL duplicate scan — zero hits

Kaidoku URLs checked (all five, exact substrings):

| kaidoku row | line | URL | sibling hits |
|---|---|---|---|
| S107 | 113 | `github.com/onekey-sec/sasquatch/releases/tag/sasquatch-v4.5.1-6` | 0 / 20 |
| S108 | 114 | `raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py` | 0 / 20 |
| S109 | 115 | `github.com/neovim/neovim/releases/tag/v0.12.6` | 0 / 20 |
| S110 | 116 | `raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md` | 0 / 20 |
| S111 | 117 | `raw.githubusercontent.com/devttys0/sasquatch/master/README.md` | 0 / 20 |

Broad pattern sweep confirms the negative: `onekey-sec` appears in **0** sibling SOURCES.md;
`devttys0` in **0**; `appimage` in **0**; `neovim` only in mado-shokunin (disposition below).
**No sibling lane registers any of the five documents kaidoku admitted this round — no duplicate
rows exist.**

## 2. Sasquatch / unblob / squashfs row scan — zero subject-matter rows

Case-insensitive `sasquatch|unblob|squashfs|squash` over all 20 sibling registries yields exactly
three files, all dispositions below; **no sibling registry row is about the onekey-sec sasquatch
tool, unblob, or SquashFS.**

- **kotodama-shokunin `corpus/SOURCES.md:383` (S354, tier B, paper)** — Schembri 2011,
  *Cryptozoology as a pseudoscience* (DOI 10.21083/surg.v5i1.1341). "Sasquatch" here is the
  mythical creature (Bigfoot), scope "the naming history of Sasquatch". Word collision only;
  unrelated subject and tier to kaidoku's tool-provenance rows.
- **kumitate-shokunin `corpus/SOURCES.md:151` (S199, tier A, docs)** — Firefox Source Docs on
  Jujutsu workspaces. Matched only as the substring "squas**hing**" ("rebasing, editing or
  squashing"). False positive; nothing to do with squashfs.
- **revenger-shokunin `corpus/SOURCES.md:101` (not a row)** — a bullet under `## Leads (unopened)`
  (header at line 96): "REA firmware guide (`docs/firmware-analysis.md`, Binwalk 3.1.x / Unblob
  26.6.x requirement) — read by the scout, **not yet a row**; open it when the firmware family is
  claimed." An intentional unopened lead, not registry content.
- **mado-shokunin `corpus/SOURCES.md:106,109` (S094, S097)** — omarchy theme payload rows; the
  string `neovim.lua` is a filename inside the theme tree. Word collision with the neovim editor;
  no relation to the v0.12.6 release page of kaidoku S109.

## 3. Closest adjacent sibling row — revenger S036, and why it is not a better source

revenger-shokunin `corpus/SOURCES.md:50` (S036, tier A, docs) registers the REA
`docs/firmware-analysis.md` at tag `rea-agents-6.5.0` — the same REA generation kaidoku's harness
runs (rea-agents 6.5.0 pkg65). But its scope cell is load-bearing: "route-scope sentences only:
what `inspect-firmware-regions` returns and bounds … ; **not provider execution on this host**,
**not extraction or completeness**". revenger's round-66 note (corpus/lessons/round-64.md:90) quotes
its "Binwalk 3.1.x / Unblob 26.6.x" prerequisite lines, and revenger's round-64 byte-evidence entry
documents an author-side Unblob probe outside the saved record. This is adjacent REA expertise, not
an overlapping source:

- Kaidoku's R36-C1 knowledge entry (`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`)
  cites **S107, S108, S109**; the assimilation entry
  (`corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`) cites **S110, S111** (verified by
  grep of the entries). Neither cites the REA guide, and P36-C1 requires the entry to cite rows
  **opened 2026-10-26** — S036 fails that predicate by construction (it is not a 2026-10-26 row).
- S036's scope explicitly excludes extraction behaviour, so it cannot substitute for S108's
  handler-code evidence (argv `-no-exit-code -f -d {outdir} {inpath}`, `get_dependencies`) or S107's
  digest evidence (the amd64 deb sha256 that M36-1's lesson line rests on). Its document is the REA
  repo docs, not unblob's handler; it says nothing about sasquatch, SquashFS recursion, or the
  neovim carrier digests.
- Tier check: kaidoku's five rows are tier A (S107–S110) and B (S111); S036 is tier A. No tier
  conflict arises because the documents and scopes do not intersect.

## 4. Would any sibling row be a better source for a kaidoku claim? — No

Per kaidoku claim need:

| Claim need | kaidoku row | Any sibling row on the same document / a better one? |
|---|---|---|
| sasquatch Debian release digest + asset (tool provenance for C1 receipts; M36-1 fix) | S107 | none — no sibling registers any onekey-sec URL |
| unblob 26.6.4 squashfs handler invocation contract (missing-dependency gap wording; recursion argv) | S108 | none — revenger S036 is REA-docs scope, extraction explicitly excluded |
| neovim v0.12.6 release digests (K3/K4 byte provenance vs GitHub-published sha256) | S109 | none — mado rows are an omarchy theme filename collision |
| unblob README "SquashFS support needs sasquatch" + Debian route (assimilation Decision 1) | S110 | none |
| devttys0 sasquatch README "Very beta." self-label (assimilation Decision 1) | S111 | none |

There is therefore no duplicate to reconcile, no conflicting scope/tier between lanes, and no
adoptable better source. The only cross-lane signal worth recording for the integration owner:
three lanes converge on the same REA 6.5.0 / unblob 26.6.4 stack (kaidoku via the npx pkg65 pin,
revenger via S036 + the unopened firmware-guide lead, game-dev-3d via its `corpus/knowledge/rea.md`
tool census noting `unblob --version` 26.6.4) yet only kaidoku has registered any of the
sasquatch/SquashFS documents — so no sibling can corroborate or undercut kaidoku's five rows, and
no id-collision surface exists for S107–S111 against sibling registries (contrast kaidoku's own
assimilation collision S106→S110/S111, which was lane-internal).

## Bottom line

Zero duplicates of kaidoku S107–S111 URLs across all 20 sibling lanes; zero sibling registry rows
on sasquatch (tool), unblob, or squashfs (three scan hits are a cryptozoology paper, a "squashing"
substring, and an explicitly-unopened revenger lead); zero conflicting scopes/tiers; and no sibling
row — revenger's REA-docs S036 included — would be a better source for any kaidoku round-36 claim.
Nothing found to falsify; coverage and calibration axes unaffected by cross-lane source overlap.
