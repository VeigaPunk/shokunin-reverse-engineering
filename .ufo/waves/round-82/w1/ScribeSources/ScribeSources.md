# ScribeSources — round 82 candidate text

Candidate only; no admission, scoring, or production-edit authority. Axes: quote fidelity, source-overlap disclosure, scoped applicability, provenance.

## Candidate S299 row

| S299 | Python shlex documentation — https://docs.python.org/3/library/shlex.html#shlex.split (same document, anchor and quoted sentence already held by S286; reopened this round, not a newly discovered authority) | docs | A | Shell-like tokenization of printed command strings into argv; not shell execution, command authorization, or a security proof | shlex.split definition, snapshot `.ufo/waves/round-82/l1/sources/shlex.html:229`, 66 497 bytes, SHA256 `00b999f61bd2a4b8dcc4b8bd4597295c1273adcbcf4f221320d0991bfff59369`; composite quote, markup normalized with `s` inside an em tag: Split the string s using shell-like syntax. | Grounds tokenization with shlex.split before separately enforced pinned-script authorization; substantial overlap with S286, not new tokenizer knowledge | mined | 2026-11-04 | on-release | corpus/knowledge/2026-11-04-r82-conjunction-and-printed-commands.md, corpus/lessons/round-82.md |

Retains the assigned S299 identifier and existing cadence as a candidate, not an endorsement of duplicate admission. Preferred curation alternative: reuse S286 for this same proposition. That alternative conflicts with the declared C2 requirement that S299 be a new row absent at base; the frozen requirement must not be silently rewritten by this seat.

## Gate notes

- Official page opened: https://docs.python.org/3/library/shlex.html. The reader identified Python 3.15.2 documentation. Retained line 229 contains `Split the string <em>s</em> using shell-like syntax.`; quotation is composite after markup normalization, not a contiguous plain-text byte substring.
- The retained round-82 snapshot is 66 497 bytes with the SHA256 above. Live curl fetch returned `HTTP 200 bytes 66497`; `cmp` against the retained file succeeded and printed `LIVE_MATCHES_RETAINED`. This establishes observed live/snapshot identity for that fetch, not future identity.
- Existing `corpus/SOURCES.md:215` has 11 cells, id S299, status mined, opened 2026-11-04, cadence on-release, and both named consumers. The knowledge entry's first line cites S299. No sourced-arm battery or gate verdict was executed by this seat; cell observations are not whole-predicate certification.
- Read-only base lookup at `9cc8fbbc893d4f76ced1ac8cf66a6239cde91770` printed zero S299 matches and two S286 matches. These are raw substring counts, not a structural parser proof. The declared new-row requirement is therefore distinct from novelty of the authority or proposition.
- S286 (`corpus/SOURCES.md:202`) already quotes the same sentence at the same line and grounds the shell-like tokenizer plus list-argv/shell=False recommendation. The round-76 snapshot SHA256 is `4c1f8bf65662ed0a4cde315df6602cde5c103b34a1ede6ae2552c227fb745ee5`. Comparing retained copies found exactly four differing bytes: only the footer changes `Last updated on Nov 04, 2026 (09:12 UTC).` to `Last updated on Nov 04, 2026 (14:31 UTC).` This is not a substantively new source edition for the scoped proposition.
- Cadence disclosure: inspected recent rows S290–S296 and S298 carry 180d, including rejected rows S291/S294; S299 carries on-release. This is an observed difference, not evidence that on-release is invalid.
- The quoted sentence has seven whitespace-delimited words (`wc -w` = 7), while the current round-82 lesson says eight. A hyphen-splitting convention could yield eight; no such convention was established here. Candidate correction: say “7 whitespace-delimited words” or omit the count.

## Rejected usage candidate

REJECTED: treating shlex.quote, shlex.split, or the shlex page as proof that arbitrary printed commands are safe or authorized to execute. Reason: tokenization and quoting do not establish script identity, pinned allowlist membership, execution containment, or the local executor's correctness. The same page warns, composite quote at snapshot line 265: “The shlex module is only designed for Unix shells.” Warning context is lines 264–272 and recommends argument lists with shell=False. Flip: a separately scoped Unix-shell single-token quoting consumer using shlex.quote, with its shell assumptions and limitations explicitly established; never an arbitrary-execution guarantee.

Consumer search performed with `functions.grep`, path `tools/round-82`, pattern `shlex\\.quote`: `No matches found`. Search pattern `shlex\\.(split|join)` found `printed-command.py:122`, `argv = shlex.split(joined)`. These are source observations, not execution evidence.

## Exact command receipts

Paths below are absolute in executed commands. Lane = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

1. `sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-82/l1/sources/shlex.html && wc -c < /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-82/l1/sources/shlex.html` — exit 0; SHA256 `00b999f61bd2a4b8dcc4b8bd4597295c1273adcbcf4f221320d0991bfff59369`; 66497.
2. `curl -fsS --max-time 60 https://docs.python.org/3/library/shlex.html -o /tmp/shlex-live-r82.html && sha256sum /tmp/shlex-live-r82.html && wc -c < /tmp/shlex-live-r82.html && rm -f /tmp/shlex-live-r82.html` — same digest and size; temporary file removed.
3. `A=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-76/l1/sources/shlex.html; B=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-82/l1/sources/shlex.html; sha256sum "$A"; cmp -l "$A" "$B" | wc -l; diff -u "$A" "$B" | head -c 3000` — old digest above; 4 differing bytes; diff only the footer timestamp above. Pipeline status is not the underlying diff exit status.
4. `S=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md; awk -F'|' 'NR==215{print "row215_cells=" NF-2}' "$S"; awk -F'|' 'NR>=200 && NR<=215 && $2 ~ /S29[0-9]/ {print $2 " status=" $9 " opened=" $10 " recheck=" $11}' "$S"; printf 'Split the string s using shell-like syntax.' | wc -w; curl -fsS -w 'HTTP %{http_code} bytes %{size_download}\\n' --max-time 60 https://docs.python.org/3/library/shlex.html -o /tmp/shlex-live-r82b.html && cmp /tmp/shlex-live-r82b.html /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-82/l1/sources/shlex.html && echo LIVE_MATCHES_RETAINED; sha256sum /tmp/shlex-live-r82b.html; rm -f /tmp/shlex-live-r82b.html` — cells 11; quote words 7; HTTP 200, 66497 bytes, live match, same digest. Temporary file removed.
5. `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse --show-toplevel; git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 9cc8fbbc893d4f76ced1ac8cf66a6239cde91770:corpus/SOURCES.md | grep -c 'S299'; git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 9cc8fbbc893d4f76ced1ac8cf66a6239cde91770:corpus/SOURCES.md | grep -c 'S286'` — lane toplevel printed; counts 0 and 2. Read-only git operations only.

## Touched surfaces, limits, and conflicts

Only retained deliverable: `.ufo/waves/round-82/w1/ScribeSources/ScribeSources.md`. No production edits, commits, pushes, judge invocation, subagent dispatch, installations or upgrades. No build/lint/test/census sweep. No runtime battery executed. Existing production row and lesson were already present when inspected; this seat did not create them.

Operational deviations disclosed: two temporary download files were written under `/tmp` rather than the authorized private scratch directory and were removed by their commands. No private scratch directory was created or inventoried. Initial broad searches included `.jj` metadata, and shell commands used awk/grep/head rather than the preferred specialized tools for those portions. These are not evidence of product correctness or gate passes. Tool versions were not recorded; no installs/updates occurred, and pacman was untouched. RULES.md was read in the first tool batch, not strictly before the concurrent read-only source calls.

Report-path conflict, verbatim: “Write report at /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-82/w1/ScribeSources/ScribeSources.md.” versus “Report: write your scoped findings to .ufo/waves/round-82/w1/ScribeSources.md”. Chosen path is the former, within the expressly authorized seat directory; no duplicate was written outside it.

Out of scope: source admission/reuse decision, production correction, declaration changes, C2 scoring, full gate/census execution, and promotion. L1 integrates candidate text.

## Self-evaluation

Accuracy 4/5: byte and locator observations are grounded, but the base lookup is substring-count evidence only. Completeness 4/5: requested candidate, overlap, and rejection are supplied; full gate execution intentionally excluded. Clarity 4/5: candidate and observations separated; command receipts are lengthy. Actionability 4/5: reuse-versus-new-row conflict is explicit but requires L1 disposition. Conciseness 3/5: exact-command provenance expands the report. Overall 3.8/5. Improvements: preserve the overlap warning during integration; correct or remove the lesson word count; avoid redundant live fetches and keep all temporary writes inside authorized scratch. Would the user agree: likely on the evidence, with operational deviations explicitly disclosed.
