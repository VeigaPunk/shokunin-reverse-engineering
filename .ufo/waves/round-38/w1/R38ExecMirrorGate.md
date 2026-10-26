# R38ExecMirrorGate — scratch transform + census gate for the assimilation append block

Seat: executor (leaf). Axes: coverage, calibration. Milestone: round 38 build drafts and first
falsifiers. Lane `kaidoku-shokunin`; L1 `KaidokuR38`. Advisory only — nothing in the lane was
edited; the L1 owns integration.

## 1. Verdict

The scribe's admitted-entry rows normalize to the 11-column fleet schema with **no transformation
required** (the normalized block is byte-identical to the received block) and the scratch-mirror
census gate passes:

```
sources-census.sh validate --file $S/validate/corpus/SOURCES.md   →  exit 0
```

Appended: **5 rows, S112–S116** (4 `mined`, 1 `rejected`). Mirror registry **111 → 116 rows**.
One new warning (W04 for S112, an expected cross-scope URL reuse), zero errors. The gate is not
vacuous: appending the same block a second time, dropping the entry file, or reusing a mined
URL+scope each drives exit 1 with E03/E04/E11 respectively (§6).

## 2. Inputs

| item | value |
|---|---|
| received block | `.ufo/waves/round-38/w1/artifacts/R38ScribeSOURCES/append-block.md` |
| received block sha256 | `984bcc965396fea50fc15414e4b69af5b2fa2123225a4cb2bfc4fd5d22d35f7e` (5 rows, 5926 B) |
| normalized block sha256 | `984bcc965396fea50fc15414e4b69af5b2fa2123225a4cb2bfc4fd5d22d35f7e` (identical) |
| lane registry (read-only) | `corpus/SOURCES.md` sha256 `5a4c1c8c3ed0a5fd01e03bc57e93b00a563b35f8e5dc791e966e4f4251b92ef6`, 111 data rows |
| admitted entry path | `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` (exactly the claims-doc path) |
| mirror registry after append | sha256 `6fbd760ec7c0f0a27d8be24443a092ab46ce8dd14d8c8c06c4eef4ee7895dcdd` |

The block was rewritten by the scribe between my first read and its "final" message (S112 title
and S116 source cell changed; first sha256 `b51fcf04…`, final `984bcc96…`). **Every result below
is on the final bytes.** The two runs agreed on the gate verdict; only the S112/S116 cell text
differed.

## 3. Normalized block (what the L1 appends)

Produced by `normalize-append.py` (artifact, §8) from the received block, `--opened 2026-10-26`,
`--used-by corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`:

```
| S112 | unblob 26.6.4 `squashfs_v4_be` magic-pattern dispatch — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py | code | A | The `squashfs_v4_be` versus `squashfs_v4_le` PATTERNS, the `SquashFSv4BEHandler` EXTRACTOR binding and the `Endian.BIG, 4` branch that runs `sasquatch-v4be`; a sibling scope over the same file as S108, … | … | … | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md |
```

Full bytes: `artifacts/R38ExecMirrorGate/append-block.normalized.md` (and
`append-block.as-received.md`, same sha256). Receipt: `normalize.receipt.json`
(`rows_in=5, rows_out=5, findings=[], ok=true`).

Per-row result:

| id | kind | tier | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|
| S112 | code | A | mined | 2026-10-26 | on-release | entry path |
| S113 | dataset | A | mined | 2026-10-26 | on-release | entry path |
| S114 | docs | B | mined | 2026-10-26 | 365d | entry path |
| S115 | tool | A | rejected | 2026-10-26 | on-release | entry path |
| S116 | own-work | A | mined | 2026-10-26 | on-release | entry path |

Checks that ran and passed on all five rows (codes in §6): 11 cells / 12 raw `|` per row; no
literal or escaped `|` inside any cell (raw `\|` count 0 on every line); canonical
`| cell | cell |` spacing; ids S112+ absent from the registry (max S111) and unique in the block;
`kind` in the fleet enum; `tier` in A/B/C; no community-at-A; no tier-C-mined; `teaches` ≥ 8
chars; `opened` exactly 2026-10-26; `recheck` a valid cadence (`on-release`, `365d`); used-by
exactly the one admitted entry; no URL+scope repeat against a mined registry row.

## 4. Mirror layout

Mirror root `$S/validate` with `S=/fast/scratch/hyaku/kaidoku-r38/R38ExecMirrorGate`. The root is
deliberately the **lane root**, not the corpus dir: `sources-census.sh --file` resolves the
validation directory as `dirname(file)/..`, so a corpus-only mirror mis-resolves every used-by
path that leaves `corpus/` (measured: baseline corpus-only mirror exited 1 with
`E11 S036 missing used-by SKILL.md` and `E11 S081 missing used-by tools/round-27/xpin-attribute.mjs`).

```
$S/validate/
├── SKILL.md                                     copy of lane SKILL.md (used-by target of S036)
├── tools/round-27/xpin-attribute.mjs            copy (used-by target of S081)
└── corpus/                                      copy of lane corpus/ (2040 files, 3 symlinks preserved)
    ├── SOURCES.md                               lane bytes + 5 appended rows (Registry table, before ## Paths)
    ├── knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md   admitted entry (see §7 limit)
    ├── knowledge/ (124 lane entries)
    ├── lessons/ (incl. round-37-verifier-spotcheck.md)
    └── evidence/round-37/c1/K1..K4/…            carriers + oracles, unchanged
```

- Appended rows land at mirror lines **118–122**, i.e. inside `## Registry` (line 3) and before
  `## Paths` (line 125); `diff lane/corpus/SOURCES.md mirror/corpus/SOURCES.md` is exactly **5
  added lines, 0 removed, 0 changed**.
- Symlinks are copied as links (`copytree(symlinks=True)`); the dangling
  `evidence/round-37/c1/K1/src/link-to-hello` survives, matching the lane.
- Only two non-corpus files are needed for used-by resolution, both enumerated from the registry
  rather than guessed: every other used-by path is already under `corpus/`.
- Rebuild is one command (`merge-mirror.py`, §8) and wipes/rebuilds the mirror, so the layout is
  reproducible rather than hand-assembled.

## 5. Gate — full output and exit code

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$S/validate/corpus/SOURCES.md"
file	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
file	W04	S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
file	W04	S054 duplicate url developer.android.com/ndk/guides/abis across scopes
file	W04	S062 duplicate url raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1 across scopes
file	W04	S069 duplicate url www.wireshark.org/docs/man-pages/tshark.html across scopes
file	W04	S083 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
file	W04	S090 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
file	W04	S092 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
file	W04	S102 duplicate url learn.microsoft.com/en-us/windows/win32/debug/pe-format across scopes
file	W04	S112 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py across scopes
file	ok	/fast/scratch/hyaku/kaidoku-r38/R38ExecMirrorGate/validate/corpus/SOURCES.md
EXIT=0
```

Saved verbatim: `artifacts/R38ExecMirrorGate/gate-validate.out`. Nine W04s are the lane's
pre-existing warnings, identical to `.ufo/waves/round-38/census-start.txt`; the tenth (S112) is
new and expected — S112 and S108 read the same `squashfs.py` at tag 26.6.4 with different scope
cells, which the contract treats as a warning, not an error. W-codes do not change exit status
(`sources-census.sh:16-18`), and the validator's own selftest passes (`selftest` → exit 0).

Row counts after append (`census` mode, `gate-census.out`):

```
file	rows	116	 file	tier.A	108	 file	tier.B	7	 file	tier.C	1
file	status.mined	111	 file	status.rejected	5
FLEET	rows	116	 FLEET	invalid	0 (tier+status)	 FLEET	missing	0
```

111 → 116 rows; mined 107 → 111; rejected 4 → 5.

## 6. Falsifiers (the gate is not vacuous)

**(a) Normalizer battery — 16 cases, all killed.** `selftest-normalize.py` (artifact) builds each
mutant and asserts the finding code and exit status:

```
killed	G0-green	clean	rc=0
killed	G1-rejected-row	clean	rc=0
killed	R1-literal-pipe	N01	rc=1
killed	R2-escaped-pipe	N01	rc=1
killed	R3-id-collision	N03	rc=1
killed	R4-dup-url-scope	N14	rc=1
killed	R5-status-queued	N06	rc=1
killed	R6-wrong-opened	N07	rc=1
killed	R7-bad-recheck	N08	rc=1
killed	R8-usedby-not-admitted	N13	rc=1
killed	R9-usedby-extra	N13	rc=1
killed	R10-bad-kind	N04	rc=1
killed	R11-tierC-mined	N09	rc=1
killed	R12-empty-block	clean	rc=1
killed	R13-bad-tier	N05	rc=1
killed	R14-thin-teaches	N11	rc=1
selftest ok
```

R4 derives its URL+scope from the first mined registry row at run time, so the E04 check cannot
silently pass on a stale hard-coded scope (an earlier hand-written variant did exactly that and
survived — recorded here because it is the kind of check that looks green and is not).

**(b) Double append, on the real bytes.** Appending `normalized.final.md` a second time inside
`## Registry`:

```
file	E03	S112 duplicate id
file	E04	S112 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py within scope …
file	E03	S113 duplicate id
file	E04	S113 duplicate url github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs/squashfs_v4_be within scope …
file	E03	S114 duplicate id
file	E04	S114 duplicate url github.com/Freetz-NG/freetz-ng/blob/master/docs/wiki/60_Development/squashfs4-be.en.md within scope …
file	E03	S115 duplicate id
file	E03	S116 duplicate id
EXIT=1
```

E03 on all five ids, E04 on the three rows whose URL+scope repeats. "Refuse/supersede, never
append past" holds: the same row **with** `supersedes S102` in `teaches` and S102's exact
URL+scope passes (`ok`, exit 0) — supersession is the only way through a same-scope duplicate.

**(c) Entry file absent, on the real bytes.** Removing the placed entry:

```
file	E11	S112 missing used-by corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md
file	E11	S113 missing used-by corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md
file	E11	S114 missing used-by corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md
file	E11	S116 missing used-by corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md
EXIT=1
```

Four E11s, not five: **S115 is `rejected`, and E11 applies to mined rows only** — a rejected row
is not required to resolve a used-by pointer.

**(d) Baseline mirror.** Corpus-only mirror: exit 1 (E11 ×2, §4). Full lane-root mirror with no
appended rows: exit 0, 111 rows, 9 W04 — the append is the only delta.

**(e) Column mapping round-trip.** Feeding existing registry row S108 through the normalizer
reproduces the registry line **byte-identically** (`cmp` → identical); the only findings are the
self-collisions N03/N07/N14, which are correct for a row already present. This is the check that
the 11 columns are read in fleet order, not merely that 11 exist.

## 7. Observations, risks, limits

1. **Entry file is a placeholder at gate time.** `R38ScribeEntry` had not published
   `entry.md` when the gate ran, so the mirror carries
   `<!-- placeholder: R38ScribeEntry/entry.md not yet published -->` at the admitted entry path.
   The gate's E11 is existence-only (it never opens the file), so the exit-0 verdict is
   unaffected — but the L1 must place the real entry at
   `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` for C1's predicate
   ("which cites a `SOURCES.md` row … whose used-by lists that entry"). Re-running the gate after
   placement is one command (§8).
2. **S115 is `rejected` but carries the entry path in used-by**, not `—`. The contract allows it
   (E11 is mined-only; W02 only checks `teaches` length, and the cell reads "REJECTED as a BE-v4
   oracle: …" with its flip). Not a defect; noted because a reviewer scanning used-by columns will
   see five identical paths across four mined and one rejected row.
3. **S112 produces a new W04** (same URL as mined S108, different scope). Warning only. If a later
   round tightens W04 into an error, S112 is the row that trips it.
4. **The block changed under me once** (§2). Any receipt that quotes a block sha256 must quote
   `984bcc96…`; `b51fcf04…` is the superseded intermediate and appears only here.
5. **Not claimed:** that the row contents are true (quote fidelity, digests, the 7-Zip refusal) —
   those are the scouts'/scribes' receipts. This seat establishes only schema conformance and gate
   outcome on the received bytes.
6. No tool was installed, no VCS command was run, no lane file was written. Scratch is removed.

## 8. Reproduction

Artifacts (all under `.ufo/waves/round-38/w1/artifacts/R38ExecMirrorGate/`):
`normalize-append.py`, `selftest-normalize.py`, `merge-mirror.py`,
`append-block.as-received.md`, `append-block.normalized.md`, `normalize.receipt.json`,
`mirror-SOURCES.md`, `gate-validate.out`, `gate-census.out`, `census-start.txt`.

```sh
S=/fast/scratch/hyaku/kaidoku-r38/R38ExecMirrorGate; mkdir -p "$S"; export TMPDIR="$S"
A=$PWD/.ufo/waves/round-38/w1/artifacts/R38ExecMirrorGate
E=corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md
python3 -I -B "$A/normalize-append.py" \
  --block .ufo/waves/round-38/w1/artifacts/R38ScribeSOURCES/append-block.md \
  --sources corpus/SOURCES.md --out "$S/block.md" --used-by "$E"   # → rows_in=5 findings=0
python3 -I -B "$A/merge-mirror.py" --lane "$PWD" --mirror "$S/validate" --block "$S/block.md"
# place the real entry, then:
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$S/validate/corpus/SOURCES.md"
python3 -I -B "$A/selftest-normalize.py"                            # → 16 killed, selftest ok
rm -rf "$S"
```

## 9. Out-of-scope observation: the frozen C1 counter is modified in the worktree

Not my seat's work, not repaired by me, but it touches this wave's claim integrity and the L1
must see it:

```
$ git status --porcelain
 M tools/round-38/c1-counter.py
?? unblob.log
```

- Frozen blob at the freeze commit `e059ca93`: `8e33ac6843c07d60835118312cb844def4385935`.
- Worktree blob now: `e405d11b670ed97dcfaefe446cf3b28cc7ff4783` (43 insertions, 21 deletions).
- Full diff: `artifacts/R38ExecMirrorGate/frozen-counter-drift.diff`.

The edit rewrites the **frozen predicate text** in the counter's docstring from "run with stock
unblob 26.6.4; **no external extractor dependency**" to "run with **sasquatch-v4be available**, as
unblob 26.6.4's SquashFSExtractor requires", and adds a new binding requirement that the paired
before-receipt "publishes none of them and names sasquatch-v4be as a missing extractor
dependency". That is the round-37 before-arm premise which `plans/round-38-claims.md` records as
**not reproducing** and reports as a corrected premise. `plans/round-38-claims.md` also states
"the counter, predicate, carriers and oracle are never changed after this commit" (freeze
`e059ca93`), and the instruments map ships `c1_counter` as a frozen instrument.

Also present: an untracked `unblob.log` (3617 B, 03:24) in the **lane root**, logging an extraction
against `corpus/evidence/round-37/c1/K3/carrier.bin`; its last chunk-search lines read
`all_chunks=[]`. Both are sibling artefacts outside the assigned artifact directory. I did not
run REA/unblob and did not touch either file.

[INFERENCE] If the measured revision is scored with the modified counter, R38-C1's target changes
meaning (it would demand a before-arm gap the freeze says does not reproduce), so the L1 should
either revert to `8e33ac68…` before scoring or treat the edit as a new frozen counter requiring a
fresh freeze commit.

## Report

`.ufo/waves/round-38/w1/R38ExecMirrorGate.md`
