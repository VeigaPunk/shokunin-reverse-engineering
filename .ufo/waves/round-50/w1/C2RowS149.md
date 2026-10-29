# C2RowS149 — S149 correction row (reserved id S153): wave 1, pre-freeze

Seat: `C2RowS149` (scribe; leaf, no subagents). Lane `kaidoku-shokunin`, base `7c678ae6d97aedb969fd253b52b3d2882ef1e186`. Date of all observations: 2026-10-28 (UTC).

## Verdict

**Draft ready for the freeze, with two corrections to the L1 draft text.** The S149 defects the round-49 closure named are confirmed from committed bytes and a fresh fetch. The draft correction row `S153` validates (census `validate` exit 0 on a lane-shaped copy; verifier exit 0 on 20 checks). The closure's stated provenance is itself wrong in one point, so the plan atom B6 must not repeat it:

1. **Origin.** The closure and the plan atom B6 say "FreeBSD is the origin of sysexits". The FreeBSD page does not say that. Its `HISTORY` says "The sysexits file first appeared in 4BSD." The Linux page (S148's committed snapshot) says "The <sysexits.h> file appeared in 4.0BSD for use by the deliverymail utility". Both attribute the origin to BSD; neither page is the origin. The correction row must say "4BSD".
2. **Not a mirror.** S149's "second mirror of S148" is also wrong as a description: the two pages carry different prose. S148 gives the header comment `/* command line usage error */`; the FreeBSD page gives `ERRORS` prose "The command was used incorrectly". The row stays rejected for a different reason (see the draft `teaches` text).
3. **Census accepts a wrong target.** The census `supersedes` check is a bare regex (`teaches !~ /supersedes S[0-9]{3}/`, `scripts/sources-census.sh:648`). A correction row that says `supersedes S147` instead of `supersedes S149` still exits 0 (mutation receipt below). Atom B6 must check the named target, not the presence of the word.

## Draft correction row (reserved id S153)

Full row: `.ufo/waves/round-50/w1/C2RowS149/S153-row.md` (sha256 `df4a4dd60d641eb8dcf4a1aee9bfa9e6aefb27a55efb932b4d9769d88ef38879`). Teaches cell as drafted:

> supersedes S149 — REJECTED: S149's reason was wrong; this page is not a second mirror of S148, because its `HISTORY` places the first appearance of the interface in 4BSD (S148's Linux page says 4.0BSD, for deliverymail) and its `ERRORS` gloss is prose, not S148's header comment; it stays rejected, because S148's header already gives 64 the meaning "command line usage error" and this page adds no claim the registry's rows make; flip: a claim whose verdict rests on the prose gloss "used incorrectly" beyond S148's header comment, or on the 4BSD origin, which would admit this page with locator `ERRORS` or `HISTORY`

Other cells: id `S153`; source "sysexits(3) FreeBSD manual, correction of S149 — https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3" (same URL as S149); kind `docs`; tier `C` (unchanged from S149; not re-tiered here); scope "The stated reason and locator of S149 only: …"; anchor names `ERRORS` and `HISTORY` with both quotes, 7 words each, verbatim, the sha256 `1fc793a2…5dbf` and the committed snapshot path; status `rejected`; opened `2026-10-28`; recheck `on-request`; used-by `—`.

Id note: `.ufo/waves/round-50/gen-w1.py` assigns S150/S151 to C1 rows, S152 to the S147 tier row and S154 to S138; S153 is free (no `S15x` row in the committed `corpus/SOURCES.md`, last id S149).

## Findings table

| # | finding | command (exact) | exit | key output / sha256 |
|---|---|---|---|---|
| F0 | fresh fetch of the FreeBSD page | `curl -sS -D headers.txt -o freebsd-sysexits.html -w '%{http_code} %{size_download}' 'https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3'` (run 2026-10-28T23:32:20Z) | 0 | HTTP 200, 59,251 B, sha256 `1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf` |
| F0b | fresh fetch equals committed snapshot | `cmp freebsd-sysexits.html corpus/evidence/round-49/c2/freebsd-sysexits.html` | 0 | IDENTICAL; both sha256 `1fc793a2…5dbf` |
| F0c | headers: no cookies | `grep -ci set-cookie headers.txt` | 0 (count 0) | stripped copy `receipts/fetch-headers.txt` |
| F1 | ERRORS quote verbatim, 7 words, under `ERRORS` | `python3 -I -B s153-verify.py --snapshot <snap> --sources corpus/SOURCES.md --id S149` (check `quote.ERRORS.*`) and the same on the S153 row | 0 for quote checks | offset 13908; section `ERRORS` at start and end; `<a id="ERRORS">` anchor |
| F2 | HISTORY quote verbatim, 7 words | same run, `quote.HISTORY.*` | 0 for quote checks | offset 16209; section `HISTORY` |
| F3 | S149's cited `DESCRIPTION` does not hold the EX_USAGE quote | same run, `quote.not-in-DESCRIPTION` | 0 | "none" — S149's anchor cell is wrong (confirmed) |
| F4 | S148 snapshot HISTORY attributes the origin to 4.0BSD | `python3 -I -B -c` tag-strip and whitespace-collapse of `corpus/evidence/round-49/c2/sysexits.html`, then find `appeared in 4.0BSD` (snapshot sha256 `d9db4b96…340`, re-read 2026-10-28) | 0 | "The <sysexits.h> file appeared in 4.0BSD for use by the deliverymail utility, later renamed to sendmail(8)" |
| F5 | S149 row as committed fails the S153 contract on the expected fields (red control) | `s153-verify.py … --id S149` | 1 | `row.teaches-supersedes-S149` FAIL, `row.anchor.ERRORS` FAIL, `row.anchor.HISTORY` FAIL; receipt `receipts/s153-verify-control-S149-committed.tsv` (sha `638861fa…`) |
| F6 | S153 draft row passes the contract | `s153-verify.py … --sources <lane-shaped clone>/corpus/SOURCES.md --id S153` | 0 | 20 checks pass; `summary ok failed=0`; receipt `receipts/s153-verify-S153.tsv` (sha `131d4b8d…`) |
| F7 | census `validate` on committed registry (baseline) | `sources-census.sh validate --root <fleet> --file corpus/SOURCES.md --today 2026-10-28` | 0 | 149 rows, 15 W04, `ok`; receipt `census-validate-committed-registry.tsv` (sha `86296f51…`) |
| F8 | census `validate` on base copy in a lane-shaped clone | `git clone --shared <lane> <S>/clone; git -C <S>/clone checkout --detach 7c678ae6…`; `sources-census.sh validate --root <S>/clone --file <S>/clone/corpus/SOURCES.md --today 2026-10-28` | 0 | 15 W04, `ok`; sha `e36d8222…` |
| F9 | census `validate` with S153 inserted after S149 (the lane-shaped clone holds the draft; the lane is untouched) | same command with the draft-inserted `SOURCES.md` (sha `e71dda9c…`) | **0** | 16 W04 (one new: S153 URL across scopes, warning only), `ok`; receipt `census-validate-S153-lane-shaped-scratch.tsv` (sha `05288218…`) |
| F10 | census placement artifact | same registry copied to an unshaped scratch dir (`--file` resolves `used-by` against `dirname(file)/..`) | 1 | 16 `E11 missing used-by` lines and no finding about S153 — an artifact of placement, not of the row; receipt `census-validate-S153-UNSHAPED-scratch-exit1.tsv` |
| F11 | census accepts a wrong supersedes target | S153 teaches changed to `supersedes S147 — REJECTED…` in the lane-shaped clone; `sources-census.sh validate …` | **0** | 0 findings beyond W04; receipt `census-mutation-wrong-supersedes-target.tsv` |
| F11b | the verifier catches the same wrong target | `s153-verify.py … --id S153` on the mutated copy | 1 | `row.teaches-supersedes-S149` FAIL; `summary fail failed=1` |
| F12 | restored draft | copy back, census `validate` and verifier | 0, 0 | sha `e71dda9c…`; receipts `census-validate-S153-restored.tsv`, `s153-verify-S153.tsv` |
| F13 | census `census` mode counts with S153 | `sources-census.sh census --root <fleet> --file <S>/…/SOURCES-with-S153.md --today 2026-10-28` | 0 | rows 149 → 150; tier.C 4 → 5; status.rejected 8 → 9; receipt `census-census-S153-committed-plus-row.tsv` |
| F14 | E04 control was not informative | row with S149's scope and no `supersedes`, status rejected | 1 (E11 placement noise) | E04 did not fire: `url_scope_nonrejected` requires a non-rejected row in the same scope; a rejected-only pair is not an E04 finding. Recorded so nobody reads the control as a pass |

Counts: 15 W04 at base, 16 with S153 (warning only; S149 already duplicates the URL across scopes).

## Repaired / not repaired

- Did **not** change any lane file. `git status --porcelain` in the lane shows only the untracked `.ufo/waves/round-50/` tree (the L1's and siblings' seats); no tracked file modified by this seat.
- `corpus/SOURCES.md` S149 row untouched (append-only; the correction is the S153 row, to land at the freeze if the L1 accepts it).
- Tier of S149 (C) is **not re-judged**; the closure's tier point concerns S147 (SEP), not S149. Open for the L1: whether the FreeBSD `sysexits(3)` page is tier A/B by CORPUS text. Not decided here.

## Recommended changes to the draft plan (before the freeze)

1. **Plan B6 text**: replace "FreeBSD is the origin of sysexits" with "the FreeBSD page's `HISTORY` says the interface first appeared in 4BSD; S148's Linux page says 4.0BSD for deliverymail". The lesson's round-49 closure sentence is the source of the error; it is recorded here, not patched in the closure.
2. **Atom B6 predicate**: check, against the committed snapshot bytes, (a) the S149-correction row's `teaches` starts `supersedes S149 —` (the named target, not any `S\d{3}`), (b) every quoted string occurs verbatim in the tag-stripped, whitespace-collapsed body and is ≤25 words, (c) the section enclosing each quote equals the heading the anchor names (`ERRORS`/`HISTORY`), (d) no quote lies in `DESCRIPTION`, (e) the snapshot sha256 and size. The verifier `s153-verify.py` implements (a)–(e) and is the draft for the port.
3. **Battery for B6** (what the counter should kill): wrong target (S147 — F11 shows the census alone does not), anchor naming `DESCRIPTION` (F3), quote not verbatim, snapshot swapped, `supersedes` deleted (F5). Each should turn exactly its own atom red.

## Tools and installs

No tool installed, upgraded or removed. Used: `curl`, `git` (read-only `clone --shared` into scratch and `checkout --detach` in the scratch clone only), `python3 -I -B`, `bash` with `scripts/sources-census.sh` (read-only; stdout only). `pacman` not used. Scratch `/fast/scratch/hyaku/kaidoku-r50/C2RowS149` removed after copying receipts; `disk-guard` not consulted (no heavy pass).

## Artifacts

- Draft row: `.ufo/waves/round-50/w1/C2RowS149/S153-row.md`
- Verifier (stdlib, exit 0/1/2): `.ufo/waves/round-50/w1/C2RowS149/tools/round-50/s153-verify.py` (sha256 `eb316237c7a1e2731d9416d42f3dcdf678e84175484558ef4bd91607b0dc2fda`)
- Receipts with `SHA256SUMS.txt` (17 files, self-excluded; `sha256sum -c` exit 0): `.ufo/waves/round-50/w1/C2RowS149/receipts/` — includes fetch headers (cookies stripped; none present), `fetch.tsv`, the normalised body and an excerpt around `ERRORS`/`HISTORY` (public manual text, two short excerpts), census outputs, verifier outputs, `SOURCES-with-S153.md` (sha `e71dda9c…`).

## Limits

- F1–F3 and F6 are a re-open of one page (the S149 page) plus the S148 snapshot. No other archive was searched; no claim about other mirrors is made.
- The verifier checks the quote's position and section; it does not judge whether the teaches prose is correct. The provenance sentence (4BSD vs 4.0BSD) is checked against the two pages' text only.
- The census `validate` run is a shape check; it does not check the quotes, the target or the heading (F11). The quote checks are the verifier's.
- The W04 warning count rose from 15 to 16 with S153; warnings do not change exit status.
