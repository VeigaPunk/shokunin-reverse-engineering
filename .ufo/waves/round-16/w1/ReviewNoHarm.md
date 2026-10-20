# Round 16 w1 — ReviewNoHarm (reviewer, leaf)

seat: KaidokuR16.ReviewNoHarm
axes: calibration (primary), depth
scope: source contract for NoHarmProducer (`.ufo/waves/round-16/controls.py` is ABSENT; reviewed the spec and the round-15 producers it inherits from). Review is contract plus proposed failure, not an observed run.

## Findings (by severity)

### F1 — high — A byte-prefix proves retention of old bytes, not that a file is unchanged
- Contract: `.ufo/waves/round-16/wave1-spec.json`, NoHarmProducer prompt asks for "LOG old-prefix, old lesson and knowledge old-prefix". Round-15 lesson `corpus/lessons/round-15-verifier-spotcheck.md:141` says "retain their baseline bytes as prefixes"; `.ufo/waves/round-15/no-harm-controls.json:19-23` records these as `append_only`.
- Live evidence: `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md` read as 74 lines / 9,496 B (`wc`) earlier this session; now 91 lines / 10,457 B. The difference is the round-16 correction appended at lines 76–91. A prefix test against the pre-append state passes, yet the file changed.
- Consequence: `old-prefix` means only "first L bytes unchanged; N bytes appended." It cannot support "unchanged" wording, and it does not check whether an appended suffix supersedes earlier text.
- Fix: report `relation: byte-prefix` (old length, suffix length, suffix SHA-256) separately from `byte-identical` (full digest). Keep "unchanged" only for digest equality. Round-15 `measurement-pins.json` already uses digests for its unchanged set, which is the right model.

### F2 — high — The "old" referent is unpinned
- NoHarmProducer says "using immutable git objects" but names no revision, blob ID, byte length or digest. `claims.json:3` pins baseline `6235498b…`. `no-harm-controls.json:2-11` pins `9719dd2…` and `7ad23fe…`, not `6235498`. `.ufo/waves/round-16/w1/CorrectionDraft.md:49` says baseline `6235498` "was not checked for this file by this seat."
- Consequence: the prefix test's referent can be whichever revision or worktree state the code picks. Round-15's "74 lines" figure was a worktree reading.
- Fix: controls.py should pin, per old-prefix file, the revision, `git rev-parse <rev>:<path>` blob ID, byte length and SHA-256, and exit 2 if any pin is missing or mismatched.

### F3 — high (conditional on implementation) — Character length used as a byte bound
- `.ufo/waves/round-15/measure.py:31-34` runs git with `text=True, encoding="utf-8"`; `get()` at `:52-56` returns `str`. All three prefix targets are multibyte UTF-8 (I checked bytes and decoded code points):
  - `LOG.md`: 126,586 B vs 125,604 code points (gap 982; 1,481 bytes ≥0x80, em dash at line 1)
  - `corpus/lessons/round-14.md`: 13,787 B vs 13,725 (gap 62)
  - `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`: 9,009 B vs 8,983 (gap 26)
- Proposed failure: if controls.py compares `after_bytes[:len(before_text)] == before_bytes[:len(before_text)]`, the final `gap` bytes of each old file are never compared, so a tail rewrite passes. If it compares `after_bytes[:len(before_text)] == before_bytes`, every file fails falsely. Neither is a valid prefix proof.
- Fix: bytes only (`git cat-file blob <rev>:<path>` with `capture_output`), compare against `len(before_bytes)`. Nothing in the spec forbids text mode, and measure.py is the precedent that would be copied.

### F4 — medium — Text-mode decoding hides CR edits; line counts use `splitlines`
- measure.py:32-34 (universal newlines) maps CRLF/CR to LF before any comparison. Round-15 lesson `:143` counts lines with `len(get(rev,path).splitlines())`, which also splits on `\x0b \x0c \x1c-\x1e \x85 \u2028 \u2029`.
- Present effect: none observed. All four files have zero CR bytes, and `\n` count equals `splitlines()` count (LOG 1922, round-14 lesson 166, r14 knowledge 129, r15 knowledge 91).
- Latent: a CR-only or CRLF edit inside the old range is invisible to a text-mode prefix test; a Unicode line separator in a rule would change craft line counts.
- Fix: count on bytes, split on `b"\n"` only, record the byte count of each file.

### F5 — medium — The "17/17 resolving" rule control covers only `corpus/knowledge/` anchors
- Lesson `:143` extracts `corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?` only. The craft section is `SKILL.md:81-318` (next `## ` at `:319`) and holds 17 top-level `- **` rules (lines 86, 108, 118, 137, 151, 162, 170, 175, 187, 196, 207, 219, 233, 240, 256, 279, 293). Several rules cite anchors the regex never matches: `LOG.md:856-858` and `SCORECARD.md:544-545` (`:207-210`), `corpus/QUALITY.md:21` (`:256-278`), and `.ufo/waves/...` (`:240-255`, `:279-292`, `:313-314`).
- Inference from the described check: it tests only that the range fits the file, so `:0` or `start > end` would not be rejected. The producer is not present, so this is [INFERENCE].
- Consequence: "17 resolving blocks" means each rule has at least one resolving knowledge range where it cites one. It does not mean every anchor resolves. The lesson describes the extraction correctly, but the headline reads more broadly.
- Fix: count anchors by kind (knowledge, LOG, SCORECARD, QUALITY, `.ufo/waves`), report unresolved counts per kind, and reject `:0` and `start > end`.

### F6 — medium — The craft-section boundary moves with any new `## ` heading
- The section runs from `SKILL.md:81` to the next `## ` (`:319`). A `## ` added inside the gap, or inside a code fence, truncates the section and changes its digest and rule count with no rule edited. No fences exist in SKILL.md now (checked).
- Fix: record the start heading and end heading strings and their line numbers; fail if the end heading is absent or duplicated; report the digest of the section and of the heading strings separately.

### F7 — medium — A peer correction check uses a line count as its byte baseline and says "unchanged"
- `.ufo/waves/round-16/w1/CorrectionDraft.md:49`: "the pre-append bytes (74 lines, as read in this session) must be unchanged." That is a worktree line count, not a byte prefix, and it uses the same "unchanged" wording F1 warns about. The append has since landed (see F1 evidence).
- `SKILL.md:240-242` says size, hash and line-count claims must bind the bytes they describe and be re-derived after every revision. This draft's "74 lines" is a stale self-identity by that rule.
- Fix: pin the pre-append blob at the integration base; check `after.startswith(blob)`; report the suffix length and SHA-256 that landed; drop the line count as evidence.

### F8 — low — Exit-code and bound gaps in the producer precedent
- measure.py:10-11 documents exit 0 or 2. `git()` and `get()` catch only `CalledProcessError`/`OSError`, so a non-UTF-8 blob raises `UnicodeDecodeError` and exits 1, outside the documented contract. All five files decode as UTF-8 (checked), so there is no present effect.
- `snapshot-inventory.py:101-118` (`read_regular`) reads with no size cap. At these sizes (under 127 KB) it is harmless. controls.py should still state a cap and exit 2 above it.

## Checked, no defect
- Round-15 unchanged claims (advisory, prior verifier, quote script, frozen expected) are digest-backed (`measurement-pins.json`, `no-harm-controls.json` `pins_match`). This is the correct method.
- Craft rule count: 17 top-level `- **` bullets at `SKILL.md:86-293`, matching the recorded 17. No indented or `* **` bullets found.
- The r15 knowledge correction heading is at line 76 with a blank line 75. I did not verify the first 74 lines against a git blob.

## Proposed L1 checks (not run)
1. Resolve `6235498…` and each old-prefix file's blob ID; record byte length and SHA-256.
2. For LOG.md, the round-14 lesson, the r14 knowledge entry and the r15 knowledge entry: bytes-only `startswith(old_blob)`; report suffix length and suffix SHA-256 separately; no "unchanged" wording.
3. Full-digest equality for the unchanged set (quote script, frozen baselines, prior verifier, old advisory).
4. Recount craft rules on bytes; list citation anchors by kind, not only knowledge.
5. Confirm the r15 knowledge correction is the only suffix added since the pinned blob.

## Residual risk and verification gaps
- controls.py is absent. Findings F3, F4, F6 and F8 are conditional on how it is implemented.
- I did not read git objects, so the "old" bytes are unverified. The 74-line and 9,496 B figures are worktree readings from earlier this session.
- Measurements were read-only: `wc`, `tail | od`, and Python byte and UTF-8 decoding of five source files. No checks, tests, producers or builds were run.
- Tool installs or updates: none.
