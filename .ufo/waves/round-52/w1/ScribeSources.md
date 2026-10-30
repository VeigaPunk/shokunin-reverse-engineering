# ScribeSources — round 52 wave 1

**Verdict: the source is opened, the quote is located, and one draftable SOURCES row (S252)
is delivered with its Gate block, fetch receipt and offline census validation.**

## Behaviour

- Fetched `https://man7.org/linux/man-pages/man2/mknod.2.html` into scratch
  (`/fast/scratch/hyaku/kaidoku-r52/w1-ScribeSources`). **HTTP 200, 16,407 bytes,
  sha256 `f867026fdb9bd5659971c912b68d6745666211495aafefee9c0645b3923ba5f7`**, exit 0,
  2026-10-30T10:45:48Z. Re-fetched 10:48:47Z: HTTP 200, same 16,407 bytes, same sha256,
  `cmp -s` byte-identical. **The page did not move.**
- Located the EPERM privilege text: the `ERRORS` section (`<h2 id="ERRORS">`, served HTML
  line 148), `EPERM` entry, served HTML lines 188-192, with the `CAP_MKNOD` token on line
  191. The quote used in the Gate block is **25 words** (limit 25) and is contiguous in
  the flattened served text.
- Delivered **one** row in the exact 11-column registry grammar (id `S252`, kind `docs`,
  tier `A`, scope "unprivileged device-node creation is CAP_MKNOD-gated on Linux",
  anchor = section title + access date, `teaches` = a one-sentence CAP_MKNOD paraphrase,
  status `mined` at first registration, `used-by` = the round-52 entry stem), plus the
  Gate block fields (URL, access date, ≤25-word located quote with its location) and the
  fetch receipt.
- Deliverable: `.ufo/waves/round-52/w1/ScribeSources/rows.md`.

## Gates (all exercised, with exit codes)

| gate | command | exit | result |
|---|---|---|---|
| fetch | `curl -sS -L --max-time 60 -A '…' URL > mknod.2.stdout.html` | 0 | HTTP 200, 16,407 B, sha256 `f867026f…3ba5f7` |
| fetch stability | same URL again, `cmp -s` | 0 | identical bytes, same sha256 |
| quote located | `python3 -I -B quote-check.py` | 0 | `QUOTE_CHECK located=1 missing=0` |
| checker able to fail | body mutated `CAP_MKNOD`->`CAP_MKNODX` | **1** | `located_in_flattened_text=False`, `missing=1` |
| checker restored | same command again | 0 | `located=1`, sha256 back to `f867026f…` |
| census BASE (no S252) | `sources-census.sh validate --file <mirror> --today 2026-10-30` | 1 | 273 pre-existing lane E11 findings |
| census WITH S252 | same, registry + this row, entry placeholder present | 1 | 273 findings, **S252: none**; WITH-minus-BASE empty; no W04 for the man7 URL |
| census NEG (entry absent) | same, row present, entry file removed | 1 | 274 findings, `E11 S252 missing used-by corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md` — the binding can fail |
| counter `sourced` binding | read `ExecCounterV2/c1-counter.py:377-378,:394,:424,:2460-2470` and simulated the binding against the row | 0 | passes iff the r52 entry cites `S252` on a `source:` line and `opened` is `2026-10-30`; negative controls (entry omits S252; wrong opened date) both fail |

No REA run, no `--data-run`, no vendor download, no package-manager or git-mutating
command. No tool was installed, so the operator tooling-authorization note has nothing to
record.

## Touched surfaces

Only inside the seat's own scope:

- `.ufo/waves/round-52/w1/ScribeSources/rows.md` — the deliverable (row + Gate block +
  receipt + census arms + search-log entry).
- `.ufo/waves/round-52/w1/ScribeSources/quote-check.py` — the mechanical quote locator.
- `.ufo/waves/round-52/w1/ScribeSources/body/mknod.2.html` — the served page bytes
  (16,407 B, sha256 `f867026f…3ba5f7`).
- `.ufo/waves/round-52/w1/ScribeSources/body/SOURCES.mirror-with-S252.md` — the scratch
  census mirror (lane registry + the one row).
- `.ufo/waves/round-52/w1/ScribeSources/receipts/{fetch-receipt.tsv,census-base.out,
  census-with-S252.out,census-with-S252-entry-absent.out}`.
- `.ufo/waves/round-52/w1/ScribeSources/status.json`.

The lane tree (`corpus/SOURCES.md`, `corpus/lessons/`, `corpus/knowledge/`, `plans/`,
`tools/`, `SKILL.md`) is **unmodified** — this seat delivers a draft, the L1 lands it.
Scratch `/fast/scratch/hyaku/kaidoku-r52/w1-ScribeSources` was removed after copying the
receipts into the seat directory.

## Findings the L1 should act on

1. **The `used-by` binding is the one live constraint on the landing commit.** S252's
   `used-by` is `corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md`, and that entry
   file **does not exist in the lane yet** (verified by `ls`, 2026-10-30T10:47Z). The
   census `NEG` arm shows that landing S252 without creating the entry in the same commit
   raises `E11 S252 missing used-by …` and breaks the round-end census receipt
   (`validate --root … kaidoku`, exit 0 required). The entry and this row must land
   together.
2. **The claims file already reserves this id, so the row needs no renumbering.**
   `plans/round-52-claims.md` (`## Frontier step`) names "the round-52 SOURCES row S252
   (man7 `mknod(2)`)"; the lane registry ends at S251 (158 rows) and the merge package
   (`/home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md`, ids S106-S237) has
   no S252, so there is no id collision. `used-by` names the entry **stem**
   (`2026-10-30-r52-avm-le-squashfs-core`), which satisfies the counter's `sourced`
   binding (`c1-counter.py:2469`) and the entry's `source:` line must cite `S252` for it
   to pass.
3. **Read S252 as documentation of the kernel gate only — not as host evidence.** The
   sibling seat `LB4Mknod` probed the host and reported all three probes (mkfifo,
   char-device `os.mknod(0:0)`, AF_UNIX bind) returning 0 in the initial context, i.e.
   the char-device call did **not** raise EPERM there, and the `runuser nobody` trial
   was refused by the environment so the unprivileged case was never measured. That seat
   states its result is not evidence for S252's branch; the row's `scope` cell carries the
   same limit ("nor a measurement of this lane's host capabilities"). The row's value is
   that it documents the gate **and** excludes FIFO/UNIX-socket creation from it — the
   exact distinction the round-52 law rests on, with S250 as the producer-side
   counterpart. It licenses **no** FIFO/socket inference, and the row says so.
4. **Per the `ConnSources` boundary, the row's `scope` cell was tightened to exclude
   four inferences CAP_MKNOD ground alone cannot carry: FIFO omission, symlink
   behaviour, the absence of REA gap records, and any extractor's own `mknod` use.** The
   extractor implementation and the envelope projection each need separate evidence;
   S252 is only the kernel-side permission requirement. The final scope cell reads
   (excerpt): "…so this row is not a claim about FIFO or socket creation, nor about
   symlink handling, nor about the absence of REA gap records, nor about any extractor's
   own mknod use…". Re-validated after the tightening: census arms are 273/273/274
   (BASE/WITH/NEG), WITH-minus-BASE empty, no W04 for the man7 URL, E11 on S252 in NEG.
5. **Routing correction (from `ScribeEntryC1`): the r52 entry is a NEW file, not their
   r50 draft.** They clarified their seat is the *landed* r50 entry
   (`corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`, already committed), which
   must **not** gain an S252 `source:` line — the r50 frozen counter needs exactly
   S243/S244/S245/S249. I verified their constant claims read-only against
   `ExecCounterV2/c1-counter.py`: `ENTRY`/`STEM` at :377-378 are the r52 stem
   (`2026-10-30-r52-avm-le-squashfs-core`), `OPENED_DATES = ('2026-10-30',)` at :394,
   `SID_RE` at :424 matches `S###` only on lines starting with `source:`, and the
   `sourced` binding at :2460-2470 is as described. **My row satisfies the opened-date
   and used-by conditions; the r52 entry author (not ScribeEntryC1) must supply the
   `source:` line naming S252.** Two further landing constants that differ from round
   50's: `CORE_HEADING = '## Round-52 additions to Core'` (:379) and
   `FRONTIER_MARK = 'Round-52 frontier note'` (:380) — copying r50's landing text
   verbatim would miss both.

## Coordination (peer messages sent, no content moved between seats)

- `ConnSources` (sources connector): told the id is free, the URL is new to the registry
  (no W04), and the E11 coupling with the entry file. Their reply set the scope
  boundary — CAP_MKNOD ground alone cannot establish FIFO omission, symlink behaviour or
  the absence of REA gap records — and the row's `scope` cell was tightened to say so.
- `ScribeEntryC1`: my first message assumed their seat authored the r52 entry; they
  corrected me — their seat is the **landed r50** entry, which must not gain an S252
  `source:` line. I verified their constant claims read-only against
  `ExecCounterV2/c1-counter.py` (:377-378, :394, :424, :2460-2470) and they hold. The
  `source:` line for S252 is owed by the r52 entry's author, which is not this seat and
  (per their correction) not ScribeEntryC1 either.

## Out of scope (deliberately not done)

- **Note for the L1 (not mine):** the lane's `git status` shows one tracked modification,
  `.ufo/waves/round-50/w3/ScribeEntryC1.md` (+30 lines, an "Addendum — the landing
  outcome"). It was written by the round-50 `ScribeEntryC1` seat itself (mtime
  2026-10-30T10:53:57Z), not by this seat — this seat wrote only under
  `.ufo/waves/round-52/w1/ScribeSources/` and
  `.ufo/waves/round-52/w1/ScribeSources.md`. It is recorded here for the audit trail
  only; I did not touch it.

- No vendor firmware downloaded or fetched; no carrier re-fetch; no extraction; no REA
  invocation of any kind (the L1 alone runs the data run).
- No lesson `## Mistakes` or `## Gate` file written under `corpus/lessons/` — the L1
  integrates the Gate fields from `rows.md` into `corpus/lessons/round-52.md`.
- No `PROVINCE.md` / `SCORECARD.md` / `LOG.md` / `SKILL.md` edit; no `plans/` edit; no
  corpus coverage-map row; no `## Paths` section edit.
- No commit, push, stage, stash, or any mutating git/jj command in the lane or fleet
  repo; no writes to `.ufo/state/`, `.ufo/watchdog.log`, the fleet repo, or
  `/home/vgpnk/Projects/shokunin/.scratch/`.
- Nothing written under `/tmp`.

## Artifact paths

- `.ufo/waves/round-52/w1/ScribeSources.md` — this report.
- `.ufo/waves/round-52/w1/ScribeSources/rows.md` — the row, the Gate block, the fetch
  receipt and the census arms.
- `.ufo/waves/round-52/w1/ScribeSources/status.json` — the wave-accounting status file.
- `.ufo/waves/round-52/w1/ScribeSources/quote-check.py` — the locator (exit 0 on the
  served bytes, exit 1 on the mutant).
- `.ufo/waves/round-52/w1/ScribeSources/body/mknod.2.html` — served bytes.
- `.ufo/waves/round-52/w1/ScribeSources/body/SOURCES.mirror-with-S252.md` — census mirror.
- `.ufo/waves/round-52/w1/ScribeSources/receipts/` — fetch receipt + three census arms.
