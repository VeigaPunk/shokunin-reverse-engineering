# R43CritAssim — adversarial review: adopting `sasquatch-prebuilt-package-inventory` in round 43

**Verdict: CONFIRMED — ADOPT** (re-grounded draft A only); the flip does not fire on 2026-10-27
bytes; four smallest-safe corrections for the integrator, none blocks adoption.

Seat `R43CritAssim`, critic. Leaf: no subagents, no background jobs, no `agent://all`. Base
`6b9e64fe7e0de202d9383baad5792fbfe039a743`. Writes: this report and
`.ufo/waves/round-43/w1/artifacts/R43CritAssim/` only. No REA, no unblob, no sasquatch run; no
pacman transaction; **no tool installed or upgraded** (host tools used read-only: `curl`,
`python3`, `git show`/`grep`). Scratch `/fast/scratch/hyaku/kaidoku-r43/w1-R43CritAssim` removed
after copying evidence into artifacts.

Assigned questions: (a) duplicate-ground risk against the held r36/r38 admissions and the r42
refusal of `sasquatch-unblob-compatibility`; (b) durability of the GitHub-releases-API citation;
(c) PROVINCE scope; (d) reproduction of the entry's `recheck:` on today's bytes; (e) whether the
round-42 verdict's flip fires today.

## (a) Duplicate-ground risk — what the matrix teaches that held rows do not

Held material read line by line at the base:

| held artifact | what it already says | overlap with draft A | net new ground in draft A |
|---|---|---|---|
| `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md` (r36) | pip-route external dependency (S110 quote); "a packaged route exists beside a source build" (its `:43` point 4 — the staged headline's "AUR was never the only route" half); devttys0 self-description; host-state correction; Frontier "AUR-only" phrase correction | **route existence only** — the deliberate overlap; the r42 review already re-titled the draft to the matrix claim so the route fact is not restated as news | release count (8); per-release asset-count vector `[6,6,6,6,6,6,6,2]`; matrix start tag `v1.0.1`; `v1.0` amd64-only (2 assets); digest asymmetry (sha256 `digest` on 6/6 newest, 0/6 all older → older rows size-pinned only); "no release body states a package/upstream version pair" (corrects the staged text's second false sentence); the page-has-no-assets citation correction |
| `corpus/knowledge/2026-10-26-unblob-format-matrix.md` (r38) | unblob's own format coverage: 97 handlers, 10 SquashFS sections, "more than 30" vs "78+" count conflict | **none** — it is the producer's format matrix, not sasquatch packaging | all of draft A |
| r42 REJECT `sasquatch-unblob-compatibility` | runtime compatibility of the installed binary with unblob; refused as superseded by held receipts | **none** — draft A's "Not claimed" explicitly disclaims any compatibility/behaviour statement ("Nothing here says any of these packages works with the installed unblob") | n/a — the refusal stands untouched; ≥1 reject stays on record for the round's assimilation clause |
| `corpus/SOURCES.md` S107 (held row) | the single newest release v4.5.1-6: 6 assets, sizes, amd64 deb digest, installed member digests | newest-release row of the matrix table (sizes 187244/170080/164428) and the `ad02d27a…` installed-binary binding | the other 7 releases; count vector; start tag; digest asymmetry; body/version-pair findings |

**Conclusion on (a).** The duplicate-ground risk is real only if the staged original were admitted
— its headline ("each carrying a Debian package per architecture") and its "release body shows
4.5.1 against 1.0" sentence are the two falsified sentences behind the r36 refusal
(`corpus/lessons/round-36.md:42`) and remain false as universals. The round-42 ADMIT is explicitly
**"ADMIT, re-grounded → `drafts/entry-A-sasquatch-release-matrix.md`"**, and every load-bearing
sentence of the re-grounded draft was re-verified against the 2026-10-26 fetch receipts and again
against today's fetch (§d/§e). The surviving claim — the release matrix, its start tag, the digest
asymmetry, and the no-version-pair finding — is held nowhere else in the lane. **Not duplicate.**
The adoption must land the re-grounded text; the staged text stays refused-as-staged with the
reversal pointer (QUALITY #35/#36 traceability both ways).

## (b) Is the GitHub-releases-API citation durable?

**Yes, in this corpus's semantics — and no per-release asset URL pinning is required.** Evidence:

1. **Precedent.** Held row S094 already cites
   `https://api.github.com/repos/lerocha/chinook-database/releases/tags/v1.4.5` as `kind: dataset`,
   `tier: A`, anchoring observed API fields (`assets[]` sizes, `digest: null`) with a teaches cell —
   the identical citation shape to the proposed S130. CORPUS.md's schema (`source` = canonical
   URL; `anchor` = revision + located content; rule 1 = URL + access date + ≤25-word quote) is met
   by the round-42 proposal (fetched-at, HTTP 200, byte count, sha256, the digest-presence counts).
2. **The endpoint is the machine-readable feed that actually serves the facts.** S131's negative
   citation (re-verified today: `grep -c 'sasquatch_1.0_amd64.deb'` → 0 on the rendered page, exit
   1) shows the page does not carry the asset list — the API is the only durable locater of the
   matrix facts.
3. **The body sha256 is point-in-time, and must be treated that way.** Today's fetch differs from
   the round-42 receipt (87700 B → 107313 B) in exactly seven JSON values, all
   `assets[].download_count` counters; every structural field is byte-identical (full field-level
   diff in `artifacts/R43CritAssim/refetch-analysis.md` §4). So the pinned sha256 is provenance of
   what was read, never a freshness check; the durable recheck is the structural one
   (`8 [6,6,6,6,6,6,6,2]`), which is what the draft's `recheck:` runs. A future seat must not
   "repair" the row the day its sha256 stops byte-matching.
4. **The digest-bearing assets are already pinned by digest.** The only release whose assets carry
   sha256 digests (v4.5.1-6, 6/6) has those digests recorded (amd64 `efbc92bd…`, matching held
   S107); the seven older releases expose no digest, so the draft quotes exact sizes only where it
   pins them (v4.5.1-6, v1.0.1, v1.0) and writes "present" for the middle four — correctly
   calibrated to what the source can support.

Residual limit (disclosed, not a defect): the recheck compares counts, not per-asset sizes; a
same-count size change would not flip the recheck but would age the entry's pinned sizes, caught
on the 180d recheck re-read or the flip refetch. The draft's own flip condition ("changed assets")
covers it semantically.

## (c) PROVINCE scope check (`git show 6b9e64fe:PROVINCE.md`)

In scope, unchanged from the r42 mapping: `:156-157` the `sasquatch` Frontier bullet (the
operator-facing packaging half — its "(AUR-only)" phrase still stands in the bullet text, with the
r36 route correction living in the `:374` note); `:122` the round-36 official-deb install record;
`:372` the sasquatch recursion Core row. The Adjacent refusals are not engaged: the entry makes no
malware-triage, non-REA dynamic-analysis, engine-install or quality/safety verdict claim — it is a
packaging-inventory ground for an existing Frontier bullet.

## (d) The entry's `recheck:` on today's bytes — reproduces

Both, verbatim, 2026-10-27 (receipt `artifacts/R43CritAssim/refetch-analysis.md` §1–2):

- draft A recheck: `curl -fsSL https://api.github.com/repos/onekey-sec/sasquatch/releases | python3 -c '…print(len(d),[len(r["assets"]) for r in d])'` → **`8 [6, 6, 6, 6, 6, 6, 6, 2]`**, exit 0. Reproduces.
- staged entry's own recheck: `curl -fsSL 'https://api.github.com/repos/onekey-sec/sasquatch/releases' | grep -c 'sasquatch-v4.5.1-6'` → **`12`**, exit 0. Reproduces (this is the r36 refusal's surviving check; its two falsified sentences stay falsified).

Every table cell of draft A re-verified against the 2026-10-27 fetch: v1.0 = 2 assets/185708 B
amd64-only; v1.0.1 = 6 assets 185724/168184/162288; v4.5.1-6 = 6 assets 187244/170080/164428 with
6/6 digests; middle four = 6 assets each, 0 digests; published_at timestamps byte-equal to the
draft table.

## (e) The flip, run today — does not fire

Round-42 verdict's flip: "refetch shows a ninth release / changed assets / a body stating a
version pair." Refetch 2026-10-27 (HTTP 200, copy `artifacts/R43CritAssim/rel-2026-10-27.json`):
**no ninth release** (8, same tags); **no changed asset set** (names, counts, sizes byte-equal to
the round-42 receipt); **no version-pair body** (only three non-empty bodies: v4.5.1-6 645 B change
lines + changelog URL; v4.5.1-5 560 B; v4.5.1-1 38 B "Rebased on top of squashfs-tools 4.5.1" —
upstream version alone, no `1.0` package pair; regex pair scan over all bodies: no hits).
**Flip status: NOT FIRED.** The admission conditions from the r42 review stand satisfied on
today's bytes.

## Smallest safe corrections (integrator/L1)

1. **Land the re-grounded draft-A text only.** The staged `sasquatch-prebuilt-package-inventory`
   headline and body keep their r36 refusal; the admitting entry and its SOURCES rows name the r36
   refusal by path/line with the fired flip (QUALITY #35/#36 both ways).
2. **Fresh row ids — the round-42 proposal's ids are taken.** At this base the registry already
   runs S001–S134 (S130 = unblob fixtures, S131/S132 = OpenWrt Kamikaze, S133/S134 = DD-WRT), and
   the round's claim file takes S135 for the unblob 26.6.4 LICENSE. The two assimilation rows must
   take the next free ids (S136 API, S137 page) after a fresh scratch collision guard at
   `6b9e64fe` (round-42's `id-collision.txt` guard, re-run — the r42 check was against base
   `c4a38ea2`'s 129-row registry).
3. **Row anchor wording: point-in-time pin.** The API row's anchor should keep the fetched-at
   instant prominent and mark the body sha256 as a record of the bytes read (download_count is
   volatile — §b item 3), so no later seat treats a sha256 mismatch as row rot.
4. **Cite held S107 where draft A touches the installed binary.** The "Not claimed" paragraph's
   `ad02d27a…` binding is S107's ground; the landed entry should cite S107 there instead of
   re-deriving it free-floating (also removes the appearance of duplicating S107's newest-release
   row, since the citation then reads as a cross-reference, not a re-measurement).

None of these touches the claim's truth; all four are integration hygiene. If any of 1–2 is not
done, the correct verdict degrades to **DEFER** (condition: re-grounded text with fresh-id rows
committed).

## Artifacts

`artifacts/R43CritAssim/`: `refetch-analysis.md` (this seat's commands/outputs), `rel-2026-10-27.json`
(API body, 107313 B, sha256 `cb42cd61…`), `rel-2026-10-27.headers`, `releases-page-2026-10-27.html`
(349250 B). All fetches are citation-only; nothing extracted, nothing run.

## Limits and markers

- [INFERENCE] none in the verdict; every claim above is backed by a 2026-10-27 command output in
  the artifacts. The sole judgment call is ranking the four corrections as hygiene vs. blockers.
- I did not re-adjudicate the other staged package entries; the r42 standing decisions apply.
- The round's assimilation clause also requires ≥1 reject on record: the r42
  `sasquatch-unblob-compatibility` REJECT (superseded content, movable `unblob/main` cite,
  self-contradicting TSV) remains on record and is unaffected by this adoption.
- `considerthese/`: no such directory in the lane root at the base — the report line for the
  frontier step is "absent" (verified: `git ls-tree 6b9e64fe -- considerthese` → empty; no
  untracked directory at the lane root).
