# DRAFT — LOG.md round-17 append entry (author-side, not integrated)

Status: draft for L1 (KaidokuR17) integration. Not appended to LOG.md. Every
`<SLOT …>` is filled by L1 from retained receipts; an unfilled slot means the
check has not run, and no slot may be filled with an unobserved value.

Placement: append after the last line of LOG.md (line 2031,
`and pushed. No following round is started.`), with one blank line between
sections. Style follows the round-16 pair (LOG.md:1924 declared entry,
LOG.md:1978 measured-records entry): declared scope first, immutable measured
records appended only after commit.

Line-format constraint: `temporal-sweep.py` tests each physical line. The
`R16-PROVENANCE` token and every site path in the correction bullet must sit on
one physical line, so that bullet is deliberately not hard-wrapped. Its
wording avoids the sweep's trigger phrases, so the bullet does not itself
become an unqualified site.

---

## 2026-10-20 — round-17 — R16-PROVENANCE and R16-INVOCATION discharge; retained Go carrier diagnostics (declared)

Declared separable claims: **C1 calibration**, discharge both routed round-16
outside defects and ground QUALITY #19; **C2 depth**, retain the Ghidra
analyzer log from REA 6.5.0 analyze sessions on L1-selected real Go carriers,
extract its Go diagnostics, and compare them field by field with predictions
derived from installed source. Baseline:
`b563c799d97774aae4351276fe43cb897311e349`; tracked tree clean at declaration,
with `.ufo/waves/round-17/` untracked.

- R16-PROVENANCE correction (round 17, append-only; no round-16 bytes rewritten): the round-16 temporal-stability sentence at LOG.md:2012 and the matching sentences at corpus/lessons/round-16.md:154 and .ufo/waves/round-16/verification.json:419 are qualified. The 20-entry producer/fixture hash map at .ufo/waves/round-16/verification.json:397-418 matches committed source-revision blobs (author re-derivation at drafting, `git show 27b8fc13156230981312c44380cddab1f2bd318d:<path>`, 20/20 equal). Temporal stability is not evidenced: no before/after maps, per-command hashes, or before/after timestamps were retained, and that boolean is not a measurement.

- C1(a) tool: `.ufo/waves/round-17/tools/pins.py` records `snapshot` maps with UTC timestamps and monotonic time, and `compare` returns exit 1 on any sha256 or size difference. Its selftest red case mutates a temp file between snapshots and expects exit 1 naming that path: `<SLOT selftest line, sha256 of pins.py>`. It proves same bytes at two instants only, not unchanged throughout; `--help` says so.

- C1(b) R16-INVOCATION: the SKILL.md citation-drift row (SKILL.md:448) advertised `python3 … --root .` without `-I`. Its runnable form is re-exercised with isolated absolute argv and the receipt is retained at `<SLOT receipt path>` (sha256 `<SLOT>`). `invocation-audit.py` counts `unlabelled_variant` rows `<SLOT before>` → `<SLOT after>`; any row still a variant is labelled `unexercised`.

- C1(c) QUALITY #19 (corpus/QUALITY.md): presence 0 → 1 (rows 1–18 present before). Grounded in corpus/lessons/round-16-verifier-spotcheck.md:183-184: temporal-stability assertions need retained pre/post records with timestamps; a same-revision hash map proves only byte match.

- C2 carriers, pinned by path and SHA-256 before any run: `/usr/bin/shfmt` (sha256 `58f765638eed5309573967726d9f9f54c8ba16cbcc65a6a5dfe0e5285aeab459`, pacman owner shfmt 3.14.1-1; pilot README records go1.27.0-X:nodwarf5 — not re-inspected here); `/home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.25.12/node_modules/@esbuild/linux-x64/bin/esbuild` (sha256 `bab29b2ca7a9e89b67cf720b77b2d743f9f31f5cf0d5bd74ee8c8de30ced7014`, go1.23.12). Pilot runs under `.ufo/waves/round-17/pilot/` are not final and are not cited as measured; the pilot recorded no pre/post pins.

- C2 runs: `.ufo/waves/round-17/runs/<label>/receipt.json` (receipt sha256 `<SLOT>`), analyze exit `<SLOT>`, REA evidence id `<SLOT ev_…>`, retained `ghidra.log` sha256 `<SLOT>`, polls `<SLOT>`, last copy `<SLOT utc>`. Retained log is polling-captured; lines after the final poll before REA deletes its runtime root can be missing, and the receipt says so.

- C2 prediction comparison: predictions from GoRttiMapper range `1.15-1.25` and r16 `selection.py`, compared by `compare.py`: `<SLOT n fields, n match, n mismatch>`. Mismatches are reported in `<SLOT path>`, not hidden.

- C2 knowledge and capability: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` (sha256 `<SLOT>`) and the capability row for retained REA Ghidra-session log, admitted only if `receipt-validate.py` exits 0 on the run receipts (`<SLOT exit>`).

- Tools created (stdlib Python 3, `--selftest` each): pins.py, retain.py, carrier-run.py, log-extract.py, predict.py, compare.py, invocation-audit.py, temporal-sweep.py, buildinfo-probe.py, receipt-validate.py, carrier-census.py, measure.py, controls.py. Tool installs/updates: `<SLOT — L1 records any install with tool, version, channel, reason; none by this draft>`.

Limits: no target execution (REA analyze is static; carriers are never run); no Go 1.27 symbol recovery promised; no new selector law (r16 `selection.py` reused as-is); no SHONEN `[x]`, promotion, or outside verification by author seats. Author-side drafting produced no executed round-17 check; no unrun check is called passed here.

## 2026-10-20 — round-17 measured records

Source revision: `<SLOT measured-source-sha>` (baseline `b563c799d97774aae4351276fe43cb897311e349`). Commands, exits, stdout/stderr hashes and producer hashes: `.ufo/waves/round-17/verification.json`.

- Selftests: `<SLOT per tool: SELFTEST: CLEAN cases=N, exit>`.
- temporal-sweep (`--rev <SLOT>`): sites `<SLOT>`, corrected `<SLOT>`, unqualified `<SLOT>`. Before this round the regex matched 2 sites (corpus/lessons/round-16.md:154, .ufo/waves/round-16/verification.json:419); LOG.md:2012 is a third temporal-stability sentence the regex does not match. Sweep counts are presence measurements, not semantic proof.
- invocation-audit (`--rev <SLOT>`): registry rows `<SLOT>`, exercised_match `<SLOT>`, labelled_unexercised `<SLOT>`, unlabelled_variant `<SLOT before> → <SLOT after>`.
- pins.py red case: `<SLOT exit 1, path named>`; pins.py green case `<SLOT exit 0>`.
- Carrier runs: `<SLOT per carrier: argv, exit, evidence id, receipt sha256, log sha256, polls>`. Any REA nonzero exit is recorded here, not hidden.
- Prediction comparison: `<SLOT n matched / n mismatched, field by field>`.
- Controls (`controls.py <BEFORE> <AFTER>`): `<SLOT old LOG prefix, lesson/knowledge prefixes, frozen blobs byte-identical, QUALITY rows 1–18 unchanged, sha256 of QUALITY row 19 line>`.
- Source census: `<SLOT start/end exit; rows before→after; used-by appends>`.
- Scorecard and axes: `<SLOT axis verdicts with numeric before→after, from measured values only>`.
- No unrun check is called passed. Retained receipts are the only evidence for the statements above.
