# R45W2Src141 — S141 (`git-diff-tree`) live re-open, row audit, and the arm it claims to justify

Seat `R45W2Src141` (scribe), round 45 wave 2, lane `kaidoku`. Leaf member: no subagent
dispatch. Read-only on the lane tree; everything below was written under
`.ufo/waves/round-45/w2/R45W2Src141/`. No install was made (nothing was needed; git 2.56.0,
python 3.14.8, curl 8.23.0 were already present).

## 1. What was attacked

| # | attack | artefact under test |
|---|---|---|
| A1 | page identity: live re-fetch, bytes, sha256, HTTP | S141 row `anchor` cell, `corpus/SOURCES.md:147`; lesson `## Gate` row |
| A2 | the located quote, byte-for-byte, and its length | same |
| A3 | the recorded word count at the named measured revision | `corpus/lessons/round-45.md` (A1 `1f4b27f`) |
| A4 | both named anchors resolve and locate the quote | row `anchor` cell |
| A5 | 11 registry columns, none empty | `corpus/SOURCES.md:147` vs header line 5 |
| A6 | `used-by` names the consumers | row `used-by` cell |
| A7 | block 22's commit arm actually uses `--name-status` | `SKILL.md` block 22 + `tools/round-45/frozen-path-preflight.py:93` |
| A8 | block 22 / claims / R45-CL11 claim about `-z` | `plans/round-45-claims.md:167-168`, `corpus/lessons/round-45.md:127-131`, docstring |
| A9 | does S141 support the arm's parsing, or only its field-separator claim | the whole citation chain |
| A10 | what the plain form does to the gate's own receipts (quoted pathnames) | the frozen gate, on fixtures |
| A11 | the 11-case selftest at the frozen blob | `--selftest` |
| A12 | freeze integrity at the named measured revision and at HEAD | frozen blobs, `git log` over `FREEZE..HEAD`, `--check-dirty` |
| A13 | `git diff-tree` doc grounds a `git log` invocation | page + fixture |

## 2. Verdicts

| # | verdict | the command that shows it |
|---|---|---|
| A1 | **holds** | `curl -sS -o s141.html https://git-scm.com/docs/git-diff-tree` → HTTP 200, 256,810 bytes, `sha256 f81c1e3141b2e8e2cfc5790b8923881862f964ae5e3f85c157299b71f80c9640` (UTC 15:59Z and a third fetch at 16:03Z, both identical; `cmp` against wave-1's saved copy → exit 0) |
| A2 | **holds** (modulo HTML markup) | `probe.json`: `quote_in_normalized_text true`, `quote_words 20`; `quote_is_raw_byte_substring false` because the page wraps the four options in `<code>` and breaks the line between `been` and `given` |
| A3 | **falsified at the named revision, repaired at HEAD** | lesson Gate cell = `(23 words)` at `e715263` and at `1f4b27f` (A1); measured `printf '%s' "$Q" \| wc -w` → **20**; HEAD = `(20 words)` (fixed by `fedd11bf`, amendment A2) |
| A4 | **holds** | raw line 3644 = `id="Documentation/git-diff-tree.txt--z"`; raw 3647 = the quote; raw 5369 = `id="_raw_output_format"` |
| A5 | **holds** | `probe.json`: `ncols 11`, `all_nonempty true`, cells printed verbatim |
| A6 | **falsified (minor)** | `used-by` = `corpus/lessons/round-45.md` only; `SKILL.md` block 22 cites S141 twice and the gate docstring cites it; registry precedent admits both (`S036` → `corpus/lessons/round-18.md, SKILL.md`; `S081` → `tools/round-27/xpin-attribute.mjs, …`) |
| A7 | **holds** | `frozen-path-preflight.py:93` = `git log -m --diff-merges=first-parent --name-status --format=%x00%H <base>..<tip>`; receipt A `touched: [{"path": "frozen/a.txt", "status": "M"}]` |
| A8 | **falsified** | the arm passes **no** `-z` (line 93; parser splits `"\t"` at 99-107); claims bullet says "the commit arm parses that" where "that" = the `-z` form; receipt C shows the path the arm records is C-quoted `"\303\274"`, which only the plain form emits |
| A9 | **falsified for the plain form; holds for `-z` only** | page `-z` dd: NUL terminators + "Without this option, pathnames with \"unusual\" characters are quoted"; the tab separator is stated **only** in the raw-format field list (raw 5453/5459/5465), not for `--name-status` |
| A10 | **falsified (general), no effect on this round** | receipt C: `touched[].path = "\"frozen/\\303\\274.txt\""`, `blob_changed = ["frozen"]` (the file is **absent**), `git rev-parse F:"frozen/\303\274.txt"` → exit 128; receipt F (touched twice, ends at FREEZE bytes): `restored []` |
| A11 | **holds** | `python3 preflight.py --selftest` → exit 0, `PREFLIGHT_SELFTEST: cases=11 failures=0` |
| A12 | **holds** | gate at A1 `1f4b27f` → exit 0 `verdict clean`; at HEAD `0ee50aaf` → exit 0 `verdict clean`; `git log --name-status F..HEAD -- tools/round-45/ plans/round-45-claims.md` → empty; frozen blobs identical at F/A1/HEAD |
| A13 | **holds** (note only) | `diff-tree -r --name-status` and `log --name-status` emit the same record bytes on the same commit (`log-vs-difftree.txt`) |

Count: 7 holds, 5 falsified (one of them already repaired at HEAD, two minor/record-level),
0 not-run in this seat's scope.

## 3. The A9/A10 detail — what the page actually licenses

The page's `-z` `<dd>` (anchor `Documentation/git-diff-tree.txt--z`, raw 3644; sentence at
raw 3646-3647) reads, verbatim and complete:

> When --raw, --numstat, --name-only or --name-status has been given, do not munge pathnames
> and use NULs as output field terminators. Without this option, pathnames with "unusual"
> characters are quoted as explained for the configuration variable core.quotePath (see
> git-config[1]).

The row records the first sentence (20 words) and stops. The second sentence is the one that
governs the arm the row is cited to justify, because the arm does **not** pass `-z`.

Measured on a fixture (git 2.56.0), same commit:

```
git log --name-status --format='%x00%H' F..R        ->  M \t "frozen/\303\274.txt"
git log --name-status -z --format='%x00%H' F..R     ->  M \0 frozen/ü.txt \0   (raw UTF-8 303 274)
```

A pathname containing a literal newline behaves the same way: plain form `M\t"frozen/a\nb.txt"`
(the newline is C-escaped, so the record still fits one line); `-z` form `M\0frozen/a<LF>b.txt\0`
(raw). So:

- S141 grounds `--name-status` itself ("Show only the name(s) and status of each changed file").
- S141 grounds the NUL field-separator rule **for the `-z` form** and nothing else; the
  "a tab or a NUL when -z option is used" lines are in the raw-diff field list, not the
  `--name-status` entry.
- S141 says the plain form **quotes** unusual pathnames. That is a warning, not a safety
  guarantee, and the plain-form parser the row justifies does not unquote.
- For this round's frozen set the distinction is inert: `git ls-tree -r --name-only F` over
  `tools/round-45/` + `plans/round-45-claims.md` yields 5 entries, all ASCII
  (`LC_ALL=C grep -c '[^ -~]'` → 0), and both representations coincide.

Consequence measured on the instrument (fixtures, not the lane): with a quoted frozen name,
`touched[]` records the C-quoted string, which is not a repo path (`git rev-parse` on it exits
128), the blob arm's two `rev-parse` calls both fail and the path is skipped by the
`if not a_ok and not b_ok: continue` branch, so `blob_changed` never names the file; and the
`restored` classification is unreachable (receipt F: touched at two commits, final bytes equal
to FREEZE, `restored []` and `blob_changed []`). The verdict stays `1` because the commit arm
fires — but table rows 2 and 3 promise `restored[]` and `blob_changed[]` receipts that do not
appear for quoted names. No selftest case covers it (case list at 265-275:
`green-clean, red-touched, red-restored, red-dirty, green-dirty-without-arm,
red-dirfreeze-no-pathspec, green-dirfreeze-pathspec, red-unknown-freeze, red-nonancestor,
red-bulk-sweep, green-empty-range`; `grep quotePath` → no match).

## 4. Gates (every row: command, exit, stdout sha256, UTC)

| gate | command | exit | stdout sha256 | UTC |
|---|---|---|---|---|
| live open #1 | `curl -sS -D headers.txt -o s141.html -w 'http=%{http_code} size=%{size_download}' https://git-scm.com/docs/git-diff-tree` | 0 (HTTP 200) | file `f81c1e31…` | 15:59:25Z (server `date:`) |
| live open #3 | same, `-o s141b.html` | 0 (HTTP 200) | `f81c1e31…` (`cmp` identical to #1) | 16:03Z |
| quote/row verifier | `python3 probe_sources.py s141.html > probe.json` | 0 (`ok true`) | `8ab214a1a16ca4c1fc4a4a7519499d3934daf40a321b6b8c1b2bb276f3f860b5` | 16:05:11Z |
| raw-byte-substring probe | `grep -c 'When --raw, --numstat' s141.html` | 1 (no match) — the quote is not a raw HTML byte substring | `18d2ac2c83f45af683c3c1d4018de4cef26eb1b1933885e3690e0e067b4b94a4` | 16:06:01Z |
| selftest at frozen blob | `python3 preflight.py --selftest` | 0 | `9f03df6538de49b733ecc71415bbb192a30aa428b82953f4ea064342389ec06c` | 16:01Z |
| fixture battery A–F | `sh fixture_battery.sh $S $S/preflight.py` | 0 | `afb093db6dba4ea8c64e5a742ce3d30d6462a8c10a4ceb7e0757ffc694759fb8` | 16:04:24Z (last case) |
| real-repo checks | `sh real_checks.sh` (run from the lane root) | 0 | `611e1380c4f8c9fedfa85a54a4b84792f488f5b9a270bc2b0d75fe894a5568aa` | 16:04:38Z |
| diff-tree vs log bytes | `git -C "$D" diff-tree -r --name-status --no-commit-id "$R" \| od -c` vs `git -C "$D" log --name-status --format=%x00%H "$F..$R" \| od -c` | 0 | `82c223804bd586c9d2394c027670d562798db59605da43460108a8855ffca329` | 16:04:54Z |

A `2` appears nowhere in this seat's work; every value was evaluable.

## 5. Findings (exact input → differing value → fix)

**F1 — block 22's warrant sentence is unsupported for the parser it names. MEDIUM.**
`SKILL.md` block 22: "the commit arm reads plain tab-separated `git log --name-status`
records, and S141 states the separator rule that makes that parsing safe". Input: the page's
`-z` dd. Differing value: the rule is conditional on `-z`, and the same paragraph says the
plain form **quotes** pathnames. The sentence refutes itself two clauses later ("the `-z` form
is the machine-safe variant this arm does not use yet"). Fix: "S141 states the NUL-terminator
rule for the `-z` form and states that without `-z` unusual pathnames are quoted; the plain
form the arm parses is therefore safe only for pathnames git does not quote".

**F2 — the frozen claims bullet asserts a `-z` usage the instrument lacks. MEDIUM.**
`plans/round-45-claims.md:167-168`: "`--name-status` with `-z` uses NUL field terminators and
does not munge pathnames; the commit arm parses that." Input: line 93. Differing value: no
`-z`; the arm parses the plain form; receipt C proves it by emitting a quoted path. The file is
frozen, so the repair is a routed supersession, not an edit: the route must say the claim
sentence is provenance, not a predicate — clause 5 of the C1 predicate only requires the block
to cite `S140` and the interpreter path, so no score changes.

**F3 — R45-CL11's premise misdescribes the frozen docstring. MEDIUM.**
`corpus/lessons/round-45.md:127-128`: "The preflight docstring says the commit arm reads
NUL-terminated `--name-status` output". Input: the docstring at all four revisions of the blob
(`b42398273da0449c01f6f26cc630853d58ea55ec` at F, A1, e715263 and HEAD). Differing value: the
docstring's arm line says `(git log --name-status)`; its source note says "with --name-status,
`-z` terminates fields with NUL instead of munging pathnames" — a statement about git, not
about the arm. Fix: "the docstring's source note cites the `-z` rule beside a parser that does
not pass `-z`; the code is plain-form".

**F4 — the receipt columns are unattainable for quoted pathnames. LOW–MEDIUM (no effect this
round).** Input: `frozen/ü.txt` touched (receipt C), and touched-then-restored (receipt F).
Differing value: `touched[].path` is the C-quoted string; `blob_changed` omits the file;
`restored` is always empty. Fix: pass `-z` and split the record on `\x00` (three fields for a
rename), or invoke with `-c core.quotePath=false` and C-unquote; add two selftest cases
(`red-quoted-touched`, `red-quoted-restored`) so the arm is tested, not just argued.

**F5 — `used-by` under-reports. LOW.** Input: `corpus/SOURCES.md:147` last cell. Differing
value: `corpus/lessons/round-45.md` only, while `SKILL.md` (block 22 prose + table cell),
`plans/round-45-claims.md:167` and `tools/round-45/frozen-path-preflight.py:32` all cite S141.
Fix: `corpus/lessons/round-45.md, SKILL.md` (precedent S036); add the tool path if the lane
wants code consumers (precedent S081). S140 shares the same single-cell shape — another seat's
call whether to change the pair together.

**F6 — the published preflight receipt does not measure the named measured revision. LOW.**
`.ufo/waves/round-45/l1/preflight-round45-frozen-both.json` pins `rev faa875bc` (the wave-2
spec commit) and `freeze f762b72`, `verdict clean`. The brief names `1f4b27f` (A1) as the
measured revision. This seat's independent run at A1 and at HEAD both exit 0 clean and the
frozen blobs are identical at F/A1/HEAD, so the verdict transfers — but the record's published
receipt would still be clean if A1 had broken a frozen path after `faa875bc`. Fix: republish
at the measured revision (and at HEAD) or state the blob-equality argument in the receipt.

**F7 — the word-count value in this seat's brief is stale. LOW.** The brief says "the 23-word
quote". Measured 20. The record itself said 23 at landing and at A1 and says 20 at HEAD. Fix:
update the brief; no lane change is needed (A2 `fedd11bf` already corrected the cell).

**F8 — "byte-for-byte" is only true against rendered text. INFO.** The sentence spans 304 raw
bytes containing 4 `<code>` elements and one newline; it is absent as a raw byte substring.
That is normal HTML quoting, and wave-1's `prove.py` already normalizes; the report should say
"rendered text", not "bytes". Also note the recorded quote stops before the sentence that
predicts the quoting behaviour, and carries no elision marker — 20 words is accurate for what
is quoted, but a reader who stops at the row does not learn the plain-form caveat.

**F9 — the second anchor does not locate the quote. INFO.** The `anchor` cell names "`-z` and
the raw output format section", but the recorded quote lives only in the `-z` `<dd>`; following
`_raw_output_format` finds the field list instead (raw 5418-5465). That field list is exactly
the evidence wave-1's F1 said the row lacked (the C/R two-path field), so the cell is
defensible only if read as "supporting anchors", not "quote locators".

## 6. Conflicts with the record, verbatim

1. `corpus/lessons/round-45.md` at `1f4b27f`: `terminators." (23 words)` — measured **20**;
   at HEAD the cell reads `(20 words)`, i.e. the conflict is between the named measured
   revision and the tip, not between the page and the record.
2. `plans/round-45-claims.md:167-168`: "…does not munge pathnames; the commit arm parses
   that." — the frozen arm at line 93 passes no `-z`.
3. `corpus/lessons/round-45.md:127-128`: "The preflight docstring says the commit arm reads
   NUL-terminated `--name-status` output" — the docstring says no such thing.
4. `SKILL.md` block 22: "S141 states the separator rule that makes that parsing safe" — the
   page states the NUL rule for `-z` and states quoting for the plain form.

## 7. Touched surfaces

Written (inside `.ufo/waves/round-45/w2/R45W2Src141/` only): `report.md` (this file),
`s141.html`, `headers.txt`, `probe_sources.py`, `probe.json`, `probe.err` (empty),
`probe.utc`, `fixture_battery.sh`, `battery.txt`, `real_checks.sh`, `real-checks.txt`,
`selftest.txt`, `log-vs-difftree.txt`, `sha256sums.txt`; plus the instructed trailer
`.ufo/waves/round-45/w2/R45W2Src141.md` (identical copy).

Read-only: `SKILL.md`, `corpus/SOURCES.md`, `corpus/lessons/round-45.md`,
`plans/round-45-claims.md`, `tools/round-45/frozen-path-preflight.py`,
`.ufo/waves/round-45/w1/R45W1SrcGitDiffTree/*`, `.ufo/waves/round-45/l1/preflight-*.json`,
and `git log/show/rev-parse/ls-tree/status`.

Not touched: `SKILL.md`, `plans/`, `tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`, `.ufo/state/`,
`.ufo/watchdog.log`, `.scratch/`, any sibling lane, the fleet repo. No `git add/commit/stash/
checkout/reset/push`, no `jj`, no package install, no write under `/tmp`. Scratch
`/fast/scratch/hyaku/kaidoku-r45/R45W2Src141` was removed after the receipts were copied out
(all six fixture repos included).

## 8. Out of scope / not run

- **S140** (`git-status`): not re-fetched or re-quoted here; another seat owns it. Its row has
  the same single-path `used-by` shape as S141 (F5 is a pair question).
- **Scoring**: the c1/c2 counters were not run; predicate values belong to the counter seats.
- **R45-CL6** (merge-blindness of the two counters) and **R45-CL15** (`--dirty-pathspec`
  replaces scope): not re-attacked; both are other arms.
- **The lane's frozen blob history** was only read as a cross-check (A12); no restored-touch
  hunt beyond `git log --name-status` over the two frozen paths, which is the commit arm's own
  view.

## 9. Evidence index

| file | sha256 | exit | UTC |
|---|---|---|---|
| `s141.html` (this seat's body, identical to wave-1's) | `f81c1e3141b2e8e2cfc5790b8923881862f964ae5e3f85c157299b71f80c9640` | curl 0, HTTP 200 | 15:59:25Z |
| `headers.txt` | `d5589da6916ea0a87f389b2657f12034230defc5c4020e4ee825c5503b3faa98` | — | — |
| `probe_sources.py` | `f8424acff3e30c8b46b096598549e2ed3b42539609b66e9af562315844f384bc` | — | — |
| `probe.json` | `8ab214a1a16ca4c1fc4a4a7519499d3934daf40a321b6b8c1b2bb276f3f860b5` | 0 | 16:05:11Z |
| `probe.err` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) | — | — |
| `fixture_battery.sh` | `c726a7d829ae5d1871fa75be008fb10c8aa1e36a38d6a9f67136d8ceab9f8d76` | — | — |
| `battery.txt` | `afb093db6dba4ea8c64e5a742ce3d30d6462a8c10a4ceb7e0757ffc694759fb8` | 0 | 16:04:24Z |
| `real_checks.sh` | `b105561c66956b5c6060fc9c1f03c149c74ed9023a4d59a4aa3c4ec0fa81b535` | — | — |
| `real-checks.txt` | `611e1380c4f8c9fedfa85a54a4b84792f488f5b9a270bc2b0d75fe894a5568aa` | 0 | 16:04:38Z |
| `selftest.txt` | `9f03df6538de49b733ecc71415bbb192a30aa428b82953f4ea064342389ec06c` | 0 | 16:01Z |
| `log-vs-difftree.txt` | `82c223804bd586c9d2394c027670d562798db59605da43460108a8855ffca329` | 0 | 16:04:54Z |
| `raw-byte-probe.txt` | `18d2ac2c83f45af683c3c1d4018de4cef26eb1b1933885e3690e0e067b4b94a4` | 1 (no match at `grep -c`; `do not munge pathnames` → 1) | 16:06:01Z |
| `sha256sums.txt` | hashes of the eleven files above | — | — |
