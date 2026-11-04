# ReviewerC2 — R88-C2 scoped findings (round 88, kaidoku)

Full per-attack record with commands: `.ufo/waves/round-88/w1/ReviewerC2/report.md`.
Pins verified (4/4 instruments + r87 module match `claims.json`). SKILL.md identical at
base/HEAD/worktree — craft section 27 blocks, promised 28th not landed.

**F1 (high)** — The frozen R88-C2 evidence sentence ("68 cells, closed 7-label
vocabulary") is false for its own pinned instrument: my run of
`tools/round-88/field-tamper-matrix.py` exits **1** with `other-refusal 5`
(`b0-method` ×4 → `bad method 0 at 0x…`; libz `l-checksum` → `IOException: bad seek`),
cell-identical to the executor's committed v1 receipt. Superseding v2 (10 labels,
63 effective, declared in `claims.json` `instrument_supersessions`) is honest and my
rerun reproduces its receipt with 0 cell differences — but `plans/round-88-claims.md`
was never reconciled, so the landed block must document 10 labels (or scope the
7-label subset) or the claim sentence is dead.

**F2 (high)** — `FIELDS` mislabels two entries: anchor `l` is the l_magic offset, so
`l-checksum`(+4,w2) tampers **l_lsize** and `l-size`(+8,w4) tampers **p_progid**
(probed on jq: l_info `f48eb603 55505821 380c 0e 16`; p_progid already zero → no-op).
Real `l_checksum` (m−4) is unmeasured (tolerated). Decision-table rows keyed on these
names will misattribute.

**F3 (high)** — Reachable fields outside the 17 print typed refusals outside even v2's
vocabulary (probed on jq): `l_magic` → `l_info corrupted` (the r87 repair's own anchor),
`ph-version` → `I am not compatible with older versions`. The matrix is a 4×17 sample,
not a closed population; "every field a tamperer can reach" (v1+v2 docstrings) is false.

**F4 (medium)** — Counter (`depth-blocks.py`) `met_target = not unresolved`: untouched
tree exits 0 at base and HEAD (`27/27`, measured via `--rev` both). Label 28/28 is
reachable with a content-free block citing a one-line file containing `.` (measured:
`28/28, unresolved [], exit 0`, bare or `:1-1`); a block that merely names/forbids a real
file resolves (mention = citation). Depth content is bound only by the frozen block text,
not by any instrument.

**F5 (medium, latent — no live corpus hit)** — Parser mis-splits can false-kill real
blocks: filename charset `[a-z0-9-]+\.md` blind to `_`/uppercase (measured `no-citation`
on a real 5-line file), nested paths invisible, a fenced do-NOT-ship example inside the
craft section becomes a phantom block (`29/28, exit 1`), and the plan's "matrix receipt
path" (JSON outside `corpus/knowledge/`) can never be a resolving citation. All 170 live
knowledge names match PATTERN and are UTF-8-clean, so today's 27 blocks are unaffected.
Zero-byte floor holds (`range:1-1 of 0` fails).

**F6 (low)** — v1 `tolerated` conflated 5 no-op writes (p_progid ×4, libz ph-filter
already 0x00) with 3 real ignores; v2 splits `noop` correctly. Same logical field
(l_lsize) is tolerated on jq/xxd/dinit but crashes bad-seek on libz — carrier-dependent
rows needed. v2 `met` tolerates up to 17 noop cells (info).

**Confirmed good**: population is exactly 4×17=68; block writable at base citing only
`corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md:8-20` (measured 28/28 exit 0
at base bytes — R88-C2 does not need R88-C1); base and junk-block controls reproduced;
good rows verified first-hand (ph-checksum→header corrupted, sentinel-sz_cpr→compressed
data violation, l-p_filesize→p_info corrupted, l-p_blocksize→corrupt b_info).

Axis verdict: R88-C2 as instrumented moves *count of citation-resolvable rule blocks*
(exit already reachable by do-nothing; label reachable by a one-line citation), not
decision-table depth; the refusal-signature content is review-bound only.
