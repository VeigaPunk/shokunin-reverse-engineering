# R46W1ProbeCost — battery cost probe (executor, leaf; one labrat)

Seat: `R46W1ProbeCost`. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Read-only on the
lane tree; every run below executes the counters from the lane worktree and writes only into my
report dir. Scratch `/fast/scratch/hyaku/kaidoku-r46/R46W1ProbeCost` removed after receipts were
copied to `R46W1ProbeCost/receipts/`. **No installs** (`time` 1.9 at `~/.local/bin/time`,
`hyperfine` 2.0.0, `strace` were already present; `/usr/bin/time` is absent — see the
"Not done / not claimed" section and the tool-deviation note in the labrat report).

Labrat note: this seat's toolset has no task/spawn tool, so no child was dispatched; I executed the
labrat protocol directly. Its deliverable is `R46W1LabratBatteryCost/report.md` (written).

Measured at `HEAD=c0112995…` (frozen paths unchanged from 332f4884 through `13a9e9e1`, verified);
instrument bytes executed = `attest.py c4056131…`, `registry.py 5e16e4af…`, `gate.py c3ba6b93…`
(the F5 bytes), identical at `332f4884`, `58eb04b6` and `HEAD`.

## Hypothesis verdict: not falsified, but the specified command measures nothing

"A full C1 + C2 run costs under 60 s and under 50 MB of scratch."

- **Literal command** (`--freeze 3182047… --rev 3182047…`): attest exit 1 in 0.10 s / 22.7 MiB /
  **0 B scratch**; registry exit 1 in 0.09 s / 18.5 MiB / **0 B**. Both print
  `"battery": {"skipped": "artefact fails a structural clause first"}` — at that commit block 23 and
  the registry section do not exist, so the hypothesis is satisfied **vacuously** and the battery is
  never entered. A closure must not quote this run as evidence of cost.
- **Full battery path** (`--freeze 332f4884 --rev 58eb04b6`): C1 **1.08 s**, 26.5 MiB peak RSS,
  **724 KiB** peak scratch (599 032 B exact; 9 forged fixtures + battery root; 5.38 MB churn); C2 **2.35 s**,
  22.1 MiB, **3.99 MB** peak scratch (3 785 292 B, 113 files, 7 forged fixtures + battery root, 26.49 MB churn);
  concurrent C1+C2 **3.2 s**, combined peak 4.37 MB; full closure bundle (2 selftests + C1 + C2 +
  2 fidelity reproductions) **8.04 s**. All runs `leftover=0`.

Margin: 60 s → 3.2 s (19×); 50 MB scratch → 3.99 MB (12.5×). Cheap enough for a closure to re-run;
five repeat runs produced byte-identical receipts (C1 `0b3d8c3f…`, C2 `f4a0c39b…`), so a closure can
diff them.

**Cost is dominated by `git` subprocess spawns, not by Python or disk**: C1 235 git calls (226
`git show`), 70 % of wall (92 % counting fixture `init/add/commit`); C2 539 calls (530 `git show`),
78 % (94 %). Per-call `git show` = 3.78 ms. Both counters re-read the same blobs — 54 unique pairs
asked 235×, 168 unique asked 539× (repeat 4.35× / 3.21×), because each fixture is scored twice
(v1+v2). A memoised `gate.show` (semantics unchanged) measured 0.933→0.372 s (C1) and
1.637→0.854 s (C2): ~1.3 s of the 3.2 s is redundant reads. Not required by either claim.

## Findings the L1 must route (frozen instrument is wrong in named places; I did not fix it)

**F1 — the dispatch's freeze cannot score the artefact.** `tools/round-46/` is touched by four
commits after `3182047` (50862e4a, 65678df0, 04252247, 332f4884). Measured:
`attest.py|registry.py --freeze 3182047… --rev 04252247` → **exit 2** `frozen_path_changed
['tools/round-46/', 'tools/round-46/attest.py', 'tools/round-46/gate.py', 'tools/round-46/registry.py']`;
same at `--rev HEAD`. Block 23 first appears at `65678df0`, after 50862e4a had already changed the
frozen paths: the pair is unscorable by construction. The lane's own receipts use 50862e4a /
65678df0 / 04252247 / 332f4884 as freezes. Any landing statement must cite 332f4884 (and rev ≥
58eb04b6), not 3182047.

**F2 — the bytes frozen at 3182047 cannot run a battery.** `gate.main_guard` there prints and
`return 2` (an int) while both `main()`s unpack `code, receipt = gate.main_guard(...)`; `attest.py`'s
`m_self_refs` names an undefined `REF`. Measured on the extracted frozen copies
(`R46W1ProbeCost/receipts/frozen-*-3182047.py`):
`frozen attest.py --freeze 04252247 --rev 04252247` → exit **1**, `{"reason": "unhandled NameError:
name 'REF' is not defined"}` + `TypeError: cannot unpack non-iterable int object` traceback;
`frozen registry.py --freeze 3182047 --rev 3182047` → exit **1** + AttributeError/TypeError
traceback; both exit 0 with `--no-battery`. A crash surfacing as **exit 1 with a traceback** is the
R45-CL13(f) class the claim says it closes — the frozen bytes still have it; 50862e4a/65678df0 fixed
it after the freeze.

**F3 — claims text vs instrument: selftest count.** `plans/round-46-claims.md:194` says
`registry.py --selftest` prints `cases=11`; the frozen bytes and HEAD both print
`REGISTRY_SELFTEST: cases=12 failures=0` (12 `case(` calls at 3182047 and at HEAD). `attest.py
--selftest` = 15 at the freeze (line 192 matches) and 18 at HEAD.

**F4 — the fidelity sentence needs an unstated `--no-battery`.** `--spec r45 --profile v1` at
`f59565b7`/`f762b727` (as written in the claims file) exits **2** `IsADirectoryError …
/tools/round-45/` for attest (the r45 block cites the *directory* `tools/round-45/`; the fixture
builder `open()`s every cited path as a file) and **1** `battery v1_green 0 != 7` for registry. With
`--no-battery` both reproduce the control receipts exactly (`rule_blocks 22, block_present 1,
rows 10, refs 8, unresolved []`; scope 6, 6 registered, exit 0). The control receipts
(`ctl-c1-fidelity.json`, `ctl-c2-fidelity.json`) carry no `battery` key, consistent with
`--no-battery` — but the claim text does not say so.

**F5 — the pin binds, and C1's scorable window opens late.** `--freeze 332f4884 --rev 332f4884` →
attest exit 1 `interpreter sha256 pin does not match the bytes at rev` (block 23 still pinned
`e6c44d2d…`; F5 bytes are `c4056131…`), re-pinned by A4 `58eb04b6`. Registry was already green
there. So C1 is green only for rev ≥ 58eb04b6 with freeze 332f4884.

**F6 — `-B` is load-bearing for frozen-byte identity, and pycache is invisible to the dirty arm.**
Running the counters with plain `python3` writes `tools/round-46/__pycache__/gate.cpython-314.pyc`
(14 281 B) inside the frozen directory; `.gitignore` hides it, so F5's `git status` dirty arm does
not see it (verified: a *non-ignored* stray file in the frozen dir correctly yields exit 2
`frozen_worktree_dirty`). The documented counting command uses `-I -B`, which prevents the write.

**F7 — `--json-out` cannot leave the lane** (exit 2 `--json-out outside the lane root`), and cannot
target a graded/frozen path (exit 2 `inside a graded or frozen surface: SKILL.md`). Receipts must be
written inside `.ufo/waves/…`; size 3.3 KB / 3.1 KB. Scratch guard: unset root → exit 2, `/tmp` →
exit 2 (`scratch root is a temporary partition: /tmp`).

## Calibration: "50 MB" depends on the unit

Scratch peak is **3.99 MB**; per-process RSS peak is 26.5 MiB (C1) and 22.1 MiB (C2) — concurrently
~47 MB, within 6 % of the 50 MB line if the bar meant memory. The hypothesis is true in the scratch
(`du`) reading only. Peak scratch is one fixture at a time (registry fixture = SKILL.md 299 KB + 38
census tools 2.39 MB + 1.08 MB git objects = 3.78 MB), and the total written per run is 5.38 MB
(C1) / 26.49 MB (C2) even though the peak stays under 4 MB.

Host load was 55–75 with 40+ sibling seats live: the same C1 run measured 1.55 s at load 67 vs
1.07 s quiet, and earlier F4-byte hyperfine passes gave 2.08 s / 3.85 s means. Treat ±40 % as host
noise, not instrument drift.

## Receipts (exact command, exit, stdout sha256, UTC)

Run 2026-10-28T17:10–17:37Z from scratch cwd, `TMPDIR=HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r46/R46W1ProbeCost/…`,
`python3 -I -B`, root the lane, `head=c0112995…`, loadavg 67.74/64.34/55.66 at the receipt batch
(17:32Z). Per-row UTC lives in `receipts/receipts.json`; rows marked `approx` there are from run
order, not a captured clock.

| command | exit | stdout sha256 (16) | wall | maxRSS |
|---|---|---|---|---|
| `attest.py --freeze 3182047… --rev 3182047…` | 1 | `dda3086b126619bb` | 0.10 s | 23 292 KB (22.7 MiB) |
| `registry.py --freeze 3182047… --rev 3182047…` | 1 | `8841358751b18788` | 0.09 s | 18 920 KB (18.5 MiB) |
| `attest.py --freeze 332f4884 --rev 58eb04b6` | 0 | `0b3d8c3f88f87b2c` | 1.07–1.55 s | 25 768 KB (25.2 MiB) |
| `registry.py --freeze 332f4884 --rev 58eb04b6` | 0 | `f4a0c39bf424b80e` | 2.17–2.96 s | 21 828 KB (21.3 MiB) |
| `attest.py … --json-out <lane>/.ufo/…/c1-F5.json` | 0 | `0b3d8c3f…` | 1.31 s | 24 812 KB (24.2 MiB) |
| `registry.py … --json-out <lane>/.ufo/…/c2-F5.json` | 0 | `f4a0c39b…` | 3.00 s | 21 828 KB (21.3 MiB) |
| `attest.py --freeze 332f4884 --rev HEAD` | 0 | — | 1.15 s | 25 304 KB (24.7 MiB) |
| `registry.py --freeze 332f4884 --rev HEAD` | 0 | — | 2.54 s | 21 504 KB (21.0 MiB) |
| `attest.py --selftest` (HEAD args) | 0 | `6aa73c612069dd72` | 2.31 s | 21 828 KB (21.3 MiB) |
| `registry.py --selftest` (HEAD args) | 0 | `0fa8c31a6419905f` | 0.92 s | 18 072 KB (17.6 MiB) |
| `attest.py … --no-battery` | 0 | `0866041b0d3f220c` | 0.16–0.25 s | 24 184 KB (23.6 MiB) |
| `registry.py … --no-battery` | 0 | `8fe65a95e015bd00` | 0.32–0.45 s | 19 996 KB (19.5 MiB) |
| `census.py --root <lane> --rev 332f4884` | 0 | — | 0.21 s | 16 420 KB (16.0 MiB) |
| `attest.py --freeze 3182047… --rev 04252247` | 2 | — | 0.11 s | 21 872 KB (21.4 MiB) |
| frozen attest (3182047 bytes) `--freeze 04252247 --rev 04252247` | 1 (traceback) | `816ca9535f2db75b` | 0.56 s | 25 324 KB (24.7 MiB) |
| frozen registry (3182047 bytes) `--freeze 3182047 --rev 3182047` | 1 (traceback) | `528c1d21d81389fa` | 0.08 s | 19 084 KB (18.6 MiB) |
| bundle: 2 selftests + C1 + C2 + 2 fidelity | 0×6 | — | **8.04 s** | — |

Peak scratch: C1 `du -sk` **724 KiB** (700 samples @4 ms + 300 @5 ms), exact walk 599 032 B / 44
files; C2 `du -sk` **3 992 KiB** (900 @4 ms + 400 @5 ms), exact walk 3 785 292 B / 113 files;
concurrent `du -sb` peak 4 369 995 B. Evidence files: `R46W1ProbeCost/receipts/receipts.json`
(command/exit/sha/UTC per row), `c1-F5.json`, `c2-F5.json`, `env.txt`, and the two frozen-byte copies.

## Not done / not claimed

`inotifywait` and `fatrace` are not installed; peak scratch is sampled (4–20 ms), not event-exact —
the in-process `os.walk` sampler and `du` agree to within one 4 KiB block. Cold-page-cache cost was
not measured (dropping caches would perturb 40+ sibling seats); a fresh `git clone` of the lane
(146 MB `.git`) measured C1 1.27 s / C2 1.97 s, i.e. no object-cache penalty beyond noise. Anything
labelled "not run" above was not run.
