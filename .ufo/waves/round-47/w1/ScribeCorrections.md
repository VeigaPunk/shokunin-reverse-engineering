# ScribeCorrections — round 47, wave 1

Seat: `ScribeCorrections` (leaf, no subagent dispatch). Lane `kaidoku-shokunin`.
Base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`, original freeze
`5017e1f7299c3a812e87e7950148f54313dd279e`.

**The lane moved while this seat ran.** At my first command HEAD was `3186f69b`; by my third it was
`2e4ae434` with the landing (`e856beb5`) and three freeze amendments (`9018c53b` A1, `62e33f7d` A2,
`2e4ae434` A3) already committed. Every measurement below is re-based on `2e4ae434`; the `3186f69b`
run is kept because it is the control that shows the pre-landing state. I adapted; I did not treat
the prompt's `5017e1f7` freeze as current.

---

## 1. Behaviour — what I produced

`corrections.md` is a grammar-exact draft of the `## Record corrections — round 47` section, written
to be pasted into `SCORECARD.md` by the L1. It carries:

- two parseable `- corrects` lines (`seats round-45`, `window round-46`), each with the superseded
  original quoted, the corrected statement, and a path/command evidence pointer;
- one clearly-labelled prose note for the two `## Owned axes` heads, which are repaired **in place**
  rather than exempted, because `axes` is not a parseable correction class (§3, F1).

Verified by substituting the draft over the landed section in the card at HEAD and running the live
parser plus its battery:

```
DRAFTED CARD: exit 0
  sections ['round-45','round-46']  atoms 50  verified 48  exempted ['seats/45','window/46']
  mismatches []  corrections 2  corrections_bad []
  battery: correction_forgeries 3  forgeries_green 0
    correction-wrong-seat-total   -> 1
    correction-window-not-empty   -> 1
    correction-ghost-atom         -> 1
```

Per-line re-derivation at `2e4ae434`:

| line | counter's own derivation |
|---|---|
| `seats/45` | `claimed [2,76]`, `derived [2,76]`, `dispatch [40,36]` |
| `window/46` | `window 332f4884..58eb04b6`, `empty true` |

The draft deliberately **omits** the two `- corrects axes …` bullets the landed section carries; §3
F1 is the measurement that makes them inert. If the L1 prefers the landed text, nothing breaks — but
those two bullets can never fail and must not be cited as re-derived evidence.

## 2. Gates

| gate | state |
|---|---|
| Lane tree read-only | held. Wrote only `.ufo/waves/round-47/w1/ScribeCorrections/` (draft, 5 receipts, `probes/`). No edit to `SKILL.md`, `plans/`, `tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`. |
| No mutating git/jj | held. Only `rev-parse`, `log`, `show`, `diff`, `status`, `ls-tree`, `rev-list`, `merge-base`, `cat-file`-class reads. No `add/commit/checkout/reset/switch/pull/push`, no `jj`. |
| Fixture repos | none created. Every mutation was an in-memory card string; no commit was made anywhere, so the fixture-identity gate was never engaged. |
| Frozen bytes | never written. Copied nothing into `tools/round-47/`; the drift in §3 F3 is pre-existing, from the L1's amendments. |
| Scratch | `S=/fast/scratch/hyaku/kaidoku-r47/ScribeCorrections`, `TMPDIR`/`HYAKU_SCRATCH` exported; removed after copying `probes/` into the report dir. Nothing under `/tmp` is cited. |
| Installs | none. No `pacman`, `uv`, `npx`, or `~/.local/bin` write. |
| Exit codes | reported as returned; the two `2`s (§3 F3, F5) are stated as could-not-evaluate and counted toward nothing. |

## 3. Findings

### F1 — the landed section's two `axes` bullets are inert; clause 3's axes arm is vacuous (depth)

`CORR` at `tools/round-47/record.py:50` is `^- corrects (seats|window|path|rev) …` — `axes` is not
admitted, so an `axes` bullet is dropped before re-derivation. The landed section
(`SCORECARD.md:3663`) carries `- corrects axes coverage: 138/138` and `- corrects axes depth: 24/24`
that are therefore never checked. Measured at HEAD with the landed card:

```
as-landed:                     exit 0  corrections 2  corrections_bad []
axes bullets set to 999/999:   exit 0  corrections 2  corrections_bad []
axes bullet with fake key:     exit 0  corrections_bad []
```

`plans/round-47-claims.md:168` still requires "an `axes` correction must state `<resolved>/<total>`".
No reachable input can violate that requirement. The two axes atoms are in fact green (derived
`{'coverage': (138,138), 'depth': (24,24)}` at HEAD), so the record is not false — the clause that
claims to bind it is.

### F2 — the landed window correction silently re-bases a false sentence (calibration)

The round-46 sentence (`SCORECARD.md:3635`) says
`` `git log --name-status 0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every
measurement above ``. Two defects, only one of which the landed correction discloses:

- `<tip>` is a placeholder — disclosed.
- its **literal base `0425224` does not give an empty window** — not disclosed. The correction
  states `332f4884..58eb04b6` and calls it "the concrete window it meant":

```
$ git log --name-status --format='%h %s' 0425224..58eb04b6 -- tools/round-46 plans/round-46-claims.md
332f4884 round-46 F5: close the two HIGH instrument defects wave 1 found …
M	tools/round-46/attest.py
M	tools/round-46/gate.py
```

`332f4884..58eb04b6` over the same paths is empty (`test -z "$(git log …)"` → true), so the
correction re-derives — but it converts a false claim into a true one by changing the base, and a
reader of the landed prose would conclude `0425224..58eb04b6` is empty. My draft keeps the pair and
states the base defect explicitly.

### F3 — the frozen paths changed after the freeze; C2 cannot detect it at all (depth)

Blob drift, `sha256` of each frozen path at each revision:

| rev | `tools/round-47/record.py` | `plans/round-47-claims.md` | disclosed in the claims file |
|---|---|---|---|
| `5017e1f7` (freeze) | `af666ce2…` | `c8615eb8…` | — |
| `9018c53b` (A1) | `787f909a…` | `64c49ded…` | yes |
| `62e33f7d` (A2) | `fb6d5735…` | `2b5d1bef…` | yes |
| `2e4ae434` (A3) | `8c0abb8b…` | `2b5d1bef…` (unchanged) | **no** |

- `plans/round-47-claims.md` still says "Nothing in this file or in `tools/round-47/` changes after
  the freeze: a change makes both counters exit 2 `frozen_path_changed`", and A1 still calls the
  series "a series of two". There are three, and A3 touched a frozen path with no claims-file
  paragraph at all (`git show --stat 2e4ae434` → `tools/round-47/record.py` only).
- **C2 has no freeze arm.** `record.py --help` exposes `--root --rev --no-battery --selftest
  --json-out`; there is no `--freeze`, and `grep -n 'frozen_path_changed\|frozen\|FREEZE'
  tools/round-47/record.py` returns nothing. The claims sentence is false for C2 by construction.
- C1 does enforce it, which is why the round's C1 is green only because `--freeze` was re-pointed to
  the amendment commit. At the original freeze it is red:

```
$ python3 -I -B tools/round-47/exact.py --root . --freeze 5017e1f7 --rev 2e4ae434 --json-out …
exit 2   reason=frozen_path_changed
frozen_path_changed = ['plans/round-47-claims.md', 'tools/round-47/', 'tools/round-47/record.py']
```

### F4 — `corrections >= 2` is satisfiable by a contentless correction (depth)

`corrects()` re-derives a `rev` correction as `rev-parse --verify` alone and a `path` correction as
existence alone; the exemption is only required for a *failing* atom, and no clause requires a
correction to change any verdict. Measured on my draft plus one padding bullet:

```
- corrects rev 0425224: resolves; asserts nothing new
→ exit 0, corrections 3, exempted ['seats/45','window/46'], corrections_bad []
```

(`- corrects path corpus/README.md: exists` also re-derives true but trips the ghost-atom check,
because no `path` atom has that key.) So the floor of two can be met with a bullet that asserts
nothing and exempts nothing. This is the same defect class as R46-CL7, one level up.

### F5 — verified-fixed: the window forgery was a no-op before A2 (depth)

On the pre-A2 instrument, the `correction-window-not-empty` fixture replaced the tip with the
evaluated `rev`, which reproduced the real correction's own tip → "mutation was a no-op" →
`forgeries_green 1`:

```
V2 in-place window = 332f4884..3186f69b (tip == rev): exit 1
  failing ['battery forgeries_green 1 != 0']  correction-window-not-empty -> None mutation was a no-op
```

A2's `non_empty` now uses `root..rev`, and at HEAD the fixture is red as intended. Recorded because
the defect is exactly the kind clause 6 exists to catch, and it survived the first freeze.

### F6 — verified-fixed: appending `## Round 47` invalidates a round-45 correction (depth)

`sections()` takes the last two `## Round N` headings. Landing the round's own section slides the
window to `46,47`, at which point `- corrects seats round-45: …` becomes "exempts an atom that does
not exist":

```
V7 (V3 + '## Round 47' section): exit 1
  sections ['round-46','round-47']  corrections_bad ['exempts an atom that does not exist']
```

A3's historical-exemption guard addresses it. The residual hazard is structural, not a defect: once
`## Round 47` exists, the round-45 seats atom is **out of scope** and the counter can no longer see
the very record defect R46-V1 named. The correction stays as evidence; the check does not.

### F7 — the `24/24` depth head must land in the same commit as block 24 (calibration)

The head is the first fraction in the row, so it is read at `--rev` like everything else. At a
revision whose craft section still has 23 blocks, `24/24` is a mismatch:

```
V6 (draft with depth head 24/24, SKILL.md at 3186f69b = 23 blocks): exit 1, mismatches [('axes','depth')]
```

The landing `e856beb5` does carry both, and HEAD derives `(24,24)`.

## 4. Reconciliation with what has landed

The landed section at `SCORECARD.md:3663` and my draft agree on both parseable lines (identical
`seats` statement, identical `window` pair). They differ in two places, both intentional:

1. landed carries two inert `- corrects axes …` bullets; my draft records the axes repair as prose
   and states why a bullet cannot carry it (F1);
2. my draft states that the round-46 sentence's literal base `0425224` is non-empty and names
   `332f4884` (F5 at `tools/round-46/{attest.py,gate.py}`) as the cause (F2).

Nothing else in the landed section is disputed; I re-derived every atom it depends on and found no
false value.

## 5. Out of scope / not run

- **Not my seat, not scored:** the content of craft block 24 and the four-forgery exactness battery.
  I ran `exact.py` read-only only to produce the freeze receipt (F3); I did not audit its clauses.
- **No landing, no edit.** `SCORECARD.md`, `SKILL.md`, `plans/` and `tools/` are untouched; the L1
  lands the draft and re-measures.
- **Not drafted:** the `## Round 47` section itself. F6 measures the hazard its arrival creates but
  the section's own atoms are the L1's to write and verify.
- **Not run:** no `pytest`/build/lint — this seat produces a document, not code.
- **Not verified:** whether the `## Owned axes` rows read correctly as prose after the head rewrite;
  that is a reading question, and the heads are the L1's to land.

## 6. Artifact paths

Report dir `.ufo/waves/round-47/w1/ScribeCorrections/`:

| path | sha256 | bytes | UTC |
|---|---|---|---|
| `corrections.md` (the draft) | `d596304f45ca9781e5ee56c3a58e88f2360a1bca9c3c190ec65ae18e35af49e2` | 2898 | 2026-10-28T17:54:34Z |
| `c2-at-3186f69b.json` (control, pre-landing) | `467598484c5778506be8f9ad7d1a50ba2bb935f018b152c18aed22e8732e7d44` | 1769 | 2026-10-28T17:49:21Z |
| `c2-at-e856beb5.json` (landing) | `facc68dc4c21a89db21619112e11ef377c67432d7317c4d0e16402e58b7846e0` | 1111 | 2026-10-28T17:53:10Z |
| `c2-at-2e4ae434.json` (HEAD) | `553be365645d8fe69adfac6a1888c67dacd72f12e608ebe71784ea9467d88fc0` | 1111 | 2026-10-28T17:53:11Z |
| `c1-at-2e4ae434.json` (C1 at amended freeze) | `11d2269f681976f469c0fd61a12b352ca240b7c01d877927e91848d2d5951152` | 2403 | 2026-10-28T17:53:48Z |
| `c1-orig-freeze-at-HEAD.json` (F3, exit 2) | `3381e86a327cdd04e967a720dcf7477d1ec848047eca6a42a0cfc73c1d29e265` | 744 | 2026-10-28T17:55:46Z |
| `probes/probe.out` (V0–V6) | `43760c4f33aab1e46cb023efbd15f6e8f7836cee0e5a1dac1336e01ce3625c37` | 3145 | 2026-10-28T17:55:53Z |
| `probes/probe2.out` (V1-fixed, V3, V7–V9) | `d791711b07304bbf86d4bf9c800a9f2eb85e1c7c4f7dcea1acfb1b5f84ab1167` | 1142 | 2026-10-28T17:55:53Z |
| `probes/verify_draft.out` (draft acceptance) | `e76b65d7e0b358e631717b18ee27009bf203b4131bb1164bf02ed38d5b4aba16` | 1027 | 2026-10-28T17:55:53Z |
| `probes/probe.py`, `probes/probe2.py`, `probes/verify_draft.py` | sources for the three receipts above | — | — |

Commands, exit codes, receipts:

| # | command (cwd = lane root) | exit | receipt |
|---|---|---|---|
| 1 | `python3 -I -B tools/round-47/record.py --root . --rev 3186f69b --json-out .ufo/waves/round-47/w1/ScribeCorrections/c2-at-3186f69b.json` | 1 | `mismatches 4`, `corrections 0 < 2` |
| 2 | `… --rev e856beb5 --json-out …/c2-at-e856beb5.json` | 0 | `failing []`, battery `3/0` |
| 3 | `… --rev 2e4ae434 --json-out …/c2-at-2e4ae434.json` | 0 | `failing []`, battery `3/0` |
| 4 | `python3 -I -B tools/round-47/exact.py --root . --freeze 2e4ae434 --rev 2e4ae434 --json-out …/c1-at-2e4ae434.json` | 0 | `met_target true`, `rows 4`, `refs 8`, battery `4/4/0/1` |
| 5 | `python3 -I -B tools/round-47/exact.py --root . --freeze 5017e1f7 --rev 2e4ae434 --json-out …/c1-orig-freeze-at-HEAD.json` | 2 | `reason frozen_path_changed`, three paths |
| 6 | `python3 -I -B probe.py` (scratch) | 0 | `probes/probe.out` |
| 7 | `python3 -I -B probe2.py` (scratch) | 0 | `probes/probe2.out` |
| 8 | `python3 -I -B verify_draft.py` (scratch) | 0 | `probes/verify_draft.out` |

Runs 1–5 emitted their JSON on stdout and to `--json-out`; the table's sha256 is the `--json-out`
artifact. Runs 6–8 were `tee`d, so those files are the exact stdout.
