# R43Quarantine — round 43 wave 1, quarantine slice derivation + per-row hand-check (kaidoku)

**Verdict: CONFIRMED** — the kaidoku quarantine slice re-derived this round is **byte-identical**
to the round-42 committed slice (5 rows, sha256 `7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a`),
every line carries an S-id, and a live re-open of all five sources confirms the five standing
verdicts: **1 fabrication-class (S150, refuse), 3 present-with-anchor (S113 count-corrected,
S136, S147), 1 unverifiable-not-fabrication (S117)**. No admitted entry this round cites any of
the five, so nothing is appended from the slice.

Seat: `R43Quarantine` (leaf — no subagent dispatch). Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Base `6b9e64fe7e0de202d9383baad5792fbfe039a743` (lane `main`). Only lane writes: this report and
`artifacts/R43Quarantine/`. No lane production file, corpus, counter, plan, claims file, registry
edit, VCS mutation. Register read-only, never edited.

## 1. Inputs read

- DRAFT claims `plans/round-43-claims.md` (frontier step: quarantine slice 5 rows hand-checked).
- Register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
  (sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, 375 lines — unchanged
  from round 39's recorded hash).
- Round-42 slice artifacts `.ufo/waves/round-42/w1/artifacts/R42AssimIds/assimilation/quarantine-slice{,-r41-committed}`
  + `quarantine-slice-detail.tsv` + `sha256sums.txt`.
- Lessons `corpus/lessons/round-38.md` (Gate + `### Quarantine slice` verdicts), `round-41.md`,
  `round-42.md`; reports `w1/R38ExecQuarantine.md` §3 (prior fetch receipts), `w1/R39Quarantine.md`.
- Assimilation `w1/R42Assim.md` + `artifacts/R42Assim/drafts/entry-A-sasquatch-release-matrix.md`,
  `entry-B-avm-le-marker.md`, `sources-rows.md` (citation cross-reference).

## 2. Slice derivation and byte comparison

Command (register read-only; the seat prompt's inline backtick-quoting form was adapted to
`$2 ~ l` with `-v l=kaidoku`, the form the round-38 seat recorded and proved equivalent):

```
awk -F'|' -v l='kaidoku' '$2 ~ l && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
```

Output (5 lines, every line S-id-bearing; artifact `artifacts/R43Quarantine/quarantine-slice`):

```
 S150   `payload-absent`
 S113`   the cited source could not be fetched, so no quote was checked
 S117`   the cited source could not be fetched, so no quote was checked
 S136`   the gate block named no locator, so no quote was checked
 S147`   the gate block named no locator, so no quote was checked
```

Byte comparison:

```
$ sha256sum my-slice.txt
7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a  my-slice.txt
$ diff my-slice.txt .../R42AssimIds/assimilation/quarantine-slice   # -> empty, exit 0
```

**Byte-identical to the round-42 committed slice and to its `quarantine-slice-r41-committed`
copy (same sha256 `7383a90e…28e6a`).** The chain r38 = r39 = r40 = r41 = r42 = r43 holds. Notes
carried from prior rounds and re-verified: (a) the four never-checked ids carry a stray trailing
backtick in `$4` because the register's never-checked table has one fewer column; ids are still
unambiguous; (b) the register's per-lane totals row for kaidoku (1 payload-absent) agrees with
the slice; (c) the three never-checked ids carry no quote string in
`quote-lint-full-v5.json` (`verdict=fetch-failed` / `no-locator`), so those hand-checks run
against the registry row's own anchor/recheck columns — as in rounds 38–42, stated per row, not
a substitution of an easier test.

## 3. Per-row hand-check (live fetches, 2026-10-27T08:2xZ)

Full receipts: `artifacts/R43Quarantine/fetch-receipts.tsv`; verdict table:
`artifacts/R43Quarantine/quarantine-verdicts.tsv`; byte evidence: `s150-zenn.html`,
`s113-adb.html`, `s117-crossref.json` in the same dir.

### S150 (round5, `payload-absent`) → FABRICATION-CLASS (REFUSE)

- Fetch: `curl -sSL` → **HTTP 200, 174,088 B**, sha256 `90ffa329…0536`. Same body size as the
  round-35/36/38 captures (174,088 B); the sha differs from round-38's `42d59c48…` because
  zenn.dev embeds time-varying JSON escape sequences in the HTML — the rendered article content
  is the same (the round-38 report recorded the same size-stability observation).
- Quote check on live bytes: `シンボルがない場合のヒント` = **0**; `ヒント` = **0**;
  `シンボルがない` = **0**. The real `<h2>` set (URL-decoded) is: はじめに / 道具の準備 /
  実例：小さなプログラムを逆アセンブルする / パターン認識のコツ / aarch64-で同じバイナリを読む /
  読み進めるためのワークフロー / まとめ / シリーズを終えて — the quoted heading is in none of them.
- Row's own recheck: `grep -c llvm-objdump` → **6** (matches the row).
- **Verdict: FABRICATION-CLASS** — payload absent from a cleanly fetched live source; the
  registry row stays quarantined, marked REFUSE in the lesson. (Round-38 refuse re-confirmed.)

### S113 (round1, fetch-failed prose class cell) → PRESENT (adoptable with anchor; count correction stands)

- Fetch: **HTTP 200, 368,063 B**, sha256 `e47470df…e6f8` (same size as round-38's 368,063 B;
  sha drift from `e6d50f92…` is dynamic markup, same class as S150).
- Payload check: `grep -o 'hreflang="[^"]*"' | sort -u` → **22** values = **21 locales +
  `x-default`** — identical to round-38's count. (A case-sensitive `[a-z-]*` pattern undercounts
  at 18 because of `es-419`, `pt-BR`, `zh-Hans`, `zh-Hant`; the broad pattern is the correct one.)
- Row scope says "served in **17** locales" — **not reproducible from live bytes**; the correct
  statement is 21 locales + x-default.
- Row's own recheck: `grep -c 'tools/adb?hl=ja'` → **1** (matches).
- **Verdict: PRESENT** — quote located live, row adoptable in a later round with the anchor and
  the count re-stated as 21 + x-default. Lane-registry note: the lane `corpus/SOURCES.md` already
  has an unrelated **lane** row S113 (unblob 26.6.4 BE v4 fixtures); the quarantined S113 is a
  staged campaign id on a different subject — namespace collision only, no identity.

### S117 (round1, fetch-failed prose class cell) → UNVERIFIABLE (not fabrication)

- Fetch: `https://doi.org/10.1109/SP46214.2022.9833799` → **302** →
  `https://ieeexplore.ieee.org/document/9833799/` → **HTTP 202, 0-byte body** — byte-for-byte
  the round-38 result.
- Identity check: Crossref API `https://api.crossref.org/works/10.1109/SP46214.2022.9833799` →
  **HTTP 200**, title "SoK: Demystifying Binary Lifters Through the Lens of Downstream
  Applications", *2022 IEEE Symposium on Security and Privacy (SP)*, published 2022-05. The
  citation is real; the publisher serves nothing fetchable.
- **Verdict: UNVERIFIABLE** — unreachable is not fabrication. The row's abstract-level
  quantities ("four … LLVM IR lifters; 252,063 executables") remain unchecked, as in round 38.

### S136 (round4, no-locator) → PRESENT (adopt-with-anchor)

- Locator supplied by the round-38 gate block: lane file
  `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md` — **12,897 B**, sha256
  `26eeaf6f…a26bf` (both identical to round-38).
- Quote check: `2 of 24 verbs are` → **1 occurrence, line 8** ("Answer: the adb surface is
  **bound and partially live** — 2 of 24 verbs are device-free and now return real evidence …").
- **Verdict: PRESENT** — row adoptable with this anchor. Note for the L1: the round-42
  assimilation draft `sources-rows.md` proposes a **lane** row numbered S136 (unblob `cli.py`,
  S130–S136 block) — a different subject; if landed, the lane registry and the staged register
  will both carry an S136. Namespace-only collision, recorded here so the quarantine row is not
  mistaken for the lane row.

### S147 (round5, no-locator) → PRESENT (adopt-with-anchor; two standing caveats)

- Locator supplied by the round-38 gate block: host file
  `~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md` — **3,386 B**, sha256
  `ab36b310…58fe` (**identical to the round-35 committed record** `.ufo/waves/round-35/w1/R35ReconQuarantine.md:174-178`).
- Quote check: line **41** `- REA release: `rea-agents@6.7.0`, skill v42, 207 tools.` —
  `grep -c '207 tools'` → 1.
- Caveats (unchanged from round 38): (a) the row names headings that do not exist — the real
  anchors are line 41 under `## State as of this writing` (L39) and `## Expected `doctor`
  output on this host` (L46); (b) drift: the quoted `rea-agents@6.7.0` disagrees with the
  lane's pinned `rea-agents@6.5.0`. The document is an anchor for "what the host contract said
  on 2026-10-23", not a true statement of the package this round measures.
- **Verdict: PRESENT** with both caveats carried.

## 4. Cross-reference with round-43 claims

- The round's one admitted assimilation entry `sasquatch-prebuilt-package-inventory`
  (`w1/R42Assim.md` ADMIT → `artifacts/R42Assim/drafts/entry-A-sasquatch-release-matrix.md`)
  cites staged S130/S131 only; entry B and `sources-rows.md` cite S130–S136. **None of the five
  quarantine ids is cited by any admitted or staged entry**, so the hand-check set (slice ∩
  cited ∩ no verdict) is empty and **nothing is appended from the slice** — same disposition as
  rounds 38–42.
- `considerthese/`: **absent** — `ls -d …/considerthese` → "No such file or directory"
  (re-verified this round; the round-42 lesson's report line stands).

## 5. Tally and dispositions

| row | verdict | action |
|---|---|---|
| S150 | FABRICATION-CLASS | registry row stays; REFUSE carried in lessons |
| S113 | PRESENT | adoptable later, anchor + count = 21 locales + x-default |
| S117 | UNVERIFIABLE | not fabrication; publisher 202/0 B, identity confirmed via Crossref |
| S136 | PRESENT | adoptable later, anchor = knowledge file line 8 |
| S147 | PRESENT | adoptable later, anchor = HOST-CONTRACT.md line 41, two caveats |

Tally: 1 fabrication-class refuse, 3 present-with-anchor, 1 unverifiable. No fabrication row
flipped to present; no present row flipped to fabrication. **The round-42 lesson's "quarantine
slice 5 rows, byte-identical to round 41" is confirmed for round 43.**

## 6. Limits

- S150/S113 sha256 drift vs round-38 is dynamic-page markup, not content change: body sizes are
  identical (174,088 B / 368,063 B) and every checked content counter matches round-38 exactly.
- S117's abstract-level quantities were not checked (publisher unreachable); the verdict is
  identity-only, as in round 38.
- Nothing was adopted into any corpus file by this seat; adoption is the L1's call.
- No REA/unblob/sasquatch run, no tool installed (no install needed), no VCS mutation, no
  shokuknow write. Scratch `/fast/scratch/hyaku/kaidoku-r43/w1-R43Quarantine` removed on exit.

Artifacts: `artifacts/R43Quarantine/` — `quarantine-slice` (+ `.sha256`), `quarantine-verdicts.tsv`,
`fetch-receipts.tsv`, `s150-zenn.html` (174,088 B), `s113-adb.html` (368,063 B), `s117-crossref.json`.
