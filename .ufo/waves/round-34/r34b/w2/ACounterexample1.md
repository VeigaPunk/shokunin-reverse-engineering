# ACounterexample1 — independent reproduction A against the frozen green surface

Seat: `L1Kaidoku34-2.ACounterexample1` (executor leaf). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scratch (the only writable area used): `/fast/scratch/hyaku/kaidoku-r34b/w2/ACounterexample1/`.
Lane VCS: no `git`/`jj` command run. No lane file written except this report. No ELF, carrier, fixture or
production reader executed as a program; readers ran only as `python3` inside counters. No network.
Nothing installed or upgraded (host `python3` was 3.14.8 already; `pacman` untouched).

**Summary verdict (details in §3–§7):** the stop's decisive counterexample reproduces independently.
My own from-scratch content-multiset reader (written before I saw the w1 source — disclosure in §3)
reaches `matched=8/target=8` on the frozen green counter (`tools/round-34/mini-fix/mini-counter.py`,
which is the counter named by `claim-stop.json.decisive_counterexample.argv`) on all three seeds, exit 0,
and is blind both to the header fields and to every record tuple (proved by corruption probes, §4).
The stop's own source `nameset.py` also scores 8/8 on the same three seeds, and behaves exactly as the
stop describes: payload-independent, name-set-keyed, embedded table. The frozen transform is layout-only
(§5). So the stop's *evidence* is not falsified on this axis; it is corroborated, and two channels the
stop did not list are weaker than its stated one (§6, §7).

Against the *proposed fresh-content repair* (`w1/CtlMultiset-files/mini-counter-fresh.py`) the
content-multiset class and a zero-knowledge answer-file class both die at 0/8 — the repair defeats the
stop's class. But the repair leaks its seed on the counter's own command line: a reader that reads
`/proc/<ppid>/cmdline` and replays the published generator reaches 8/8 whenever `--seed` is passed
(three pinned seeds and `--seed=` form), and only fails when the seed is unguessable (two unseeded runs,
0/8). That is a conditional falsification of the repair's "the association is unpublished, so only
record-array traversal recovers it" guarantee, not of the stop.

No clause, target, class, threshold or label is changed here; no capability or score is claimed.

---

## 1. Axes named

1. **Frozen-green reachability** — can a structure-blind reader written from the fixture format alone
   hit `8/8` on `mini-counter.py`, without reading header fields or record tuples?
2. **Stop-evidence identity** — does the stop's `source_sha256`, class description and three-seed
   receipt reproduce on bytes, and is the stop's source *actually* header/record blind (black box)?
3. **Transform invariance** — is the counter's only transformation layout-only, and therefore unable to
   exclude any class keyed on a public layout-invariant of the content?
4. **Repair reachability** — does that class (and a zero-knowledge variant) survive the fresh-content
   candidate, and does the candidate introduce a new structure-blind channel?
5. **Knowledge cost** — what must a reader know beyond the opaque temp path the counter hands it?

---

## 2. Instruments and artifacts

Frozen counter (lane, read-only), sha256 `43ef669ff6ea9fe752798cc376d9dfe83819fa8a2425afea4b275d5cc47c4b52`
(`tools/round-34/mini-fix/mini-counter.py`). Expected records: `mini-fix/expected.json`
`5ebb5349fd21eb3e885c775cb0068ece04188b9a9a7fdc414c1c83a2d8828483`. Eight 512-byte fixtures under
`mini-fix/fixtures/`. All work ran on a copy: `scratch/clone/tools/round-34/…` (`cp -a`), with
`--root .` from `scratch/clone`, so the lane bytes were never the counter's input.

Candidate repair (w1, read-only), copied to `scratch/frozen/mini-counter-fresh.py` (lane sha256
`5181330d07ca83a46249e6f3596a9c3258ebff2697a0ecebd45daadec153ff5c`, matching the w1 report's pin).
Stop source, copied to `scratch/frozen/nameset.py`; lane sha256
`2e8feaea92eedb8d73e80c098d39534e5e7755b81d32babf38029ee4e2a88b97` = `claim-stop.json.source_sha256`
(verified by `sha256sum`, 2026-10-25T07:29:45Z, exit 0). `pathkey.py`
`28acfe5a79b29977c89de26accc55233d54c08daededf2452893e91043d481a9` used as the negative control.

My readers (all in scratch, all `python3`, all invoked only by a counter):

| artifact | sha256 | what it parses |
|---|---|---|
| `memtable_a.py` | `52406039956a6cd64810a917953c2ad8c08067e89a3688bab220994c2202f79e` | **nothing structural**: whole file as bytes, NUL-split, printable tokens containing `.so.`, keyed table |
| `sidefile_a.py` | `2ca326964ca9974726914290f5fa9cf8c1a2a2e9f1ee2f865183d1fab17f2f67` | same scan, but table loaded at run time from the counter's public `expected.json` relative to cwd |
| `seedregen_a.py` | `47b3dc2f01c7da10818ac26c16521f0c5df9d95f31210add12e7b8912860f747` | parent `/proc/<ppid>/cmdline` seed; replay of the published fresh generator; whole-file hash only |
| `fixedlayout_a.py` | `addcc4014e278d1be4b5d35c0d510179be4d578c237e25c9e14929e2bb8b6d9f` | boundary probe **that does walk records**; no header field |
| `mut-counter.py`, `probes2.py`, `procpeek_a.py` | see `receipts.log` / `probes2.log` | scratch harnesses, no domain role |

`memtable_a.py` is generated by `build_table.py` from `expected.json`; its table is fixture knowledge,
disclosed in §3. All receipts are in `scratch/receipts.log`, `scratch/probes2.log`, `scratch/procpeek.txt`.

---

## 3. Reproduction of the stop's counterexample — and knowledge cost

### 3.1 My own class, on the frozen green counter

Reader: `memtable_a.py`. It does not parse version/count/records_off/names_off, does not dereference
`name_off`, and does not read a `(flags, value)` tuple: it splits the 512 bytes on NUL, keeps printable
tokens containing `.so.`, and looks the resulting name multiset up in an embedded table.

| argv (cwd `scratch/clone`) | UTC | exit | result |
|---|---|---|---|
| `python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . --control-reader …/memtable_a.py --seed kaidoku-r34-mini-v1` | 07:33:07Z | **0** | `matched=8 target=8 met_target=true`, rows 8/8, row exits [0] |
| same, `--seed alt-1` | 07:33:08Z | **0** | `matched=8 met_target=true`, rows 8/8 |
| same, `--seed alt-2` | 07:33:08Z | **0** | `matched=8 met_target=true`, rows 8/8 |

The first run of this reader (07:30:07Z, same file, same three seeds) reproduced the same 8/8 on all
three seeds before the consolidated receipt sweep at 07:33. The counter ignores `--seed` in its output document, so `seed=null` in the receipt is the
counter's omission, not mine.

**Class:** content-multiset memorization — sorted multiset of SONAME tokens as key, stored
name → (flags, value) table as answer. Matches the stop's `decisive_counterexample.class` exactly.
**Matched:** 8/8. **Seeds:** `kaidoku-r34-mini-v1`, `alt-1`, `alt-2` (three distinct permutations;
§5 shows the transformed byte sets differ). **Exit:** 0.

### 3.2 Knowledge the reader needed

Yes: fixture knowledge. The counter gives a reader only an opaque temp path and an environment of
`PATH`/`HOME`; it does not hand over records or a key. My memorizer supplies the answer table from the
public repository (`expected.json`, `fixtures/` are world-readable lane files, and the counter itself
reads `expected.json` from `--root`). The counter never withholds the *answers*; it only scrambles the
pool order. So the stop's statement — "the shortcut reads no header, walks no record array and reads no
`name_off`; it keys on the sorted set" — is the correct description of what I built too.

### 3.3 The stop's own source, same counter

`frozen/nameset.py`, three seeds, same argv shape: **8/8, exit 0**, rows 8/8, at 07:33:08Z–07:33:09Z.
Negative control `frozen/pathkey.py` on the same counter: `matched=0`, exit 1, every row exit 3
(07:33:12Z) — the permutation does defeat the path/digest class, as the stop records.

### 3.4 Independence disclosure (important)

I did **not** open `nameset.py`/`pathkey.py` source files. I did read, before writing my reader,
`w1/ExecRedReproduce.md` lines 1–120, which describes the class and the fixture format consequence
(stopping before its appendix), and I later read lines 124–263, whose Appendix A quotes the source of
`r_nameset.py`. Sequence on the clock: my reader and table were written and first run (frozen receipts
07:30:07Z, `receipts.log`; the build call immediately precedes them) **before** the appendix read;
the class itself is also stated in
`claim-stop.json` ("content-multiset memorization (SONAME-set key + stored name->flags/value table)").
So: artifact independent (own tokenizer, own table shape, own refusal behaviour), knowledge not blind —
I did not rediscover the class from nothing. This report does not claim a blind rediscovery.

---

## 4. Black-box proof that the stop's source is header- and record-blind

Probe counter `mut-counter.py` runs a reader on one static file; four mutations of `alpha.mrec`
(count 3, records at 16, pool at 40), receipts 2026-10-25T07:32:28Z and 07:33:28Z:

| input mutation | `nameset.py` | `memtable_a.py` | `structural.py` (control) |
|---|---|---|---|
| base alpha | exit 0, table | exit 0, table | exit 0, correct |
| flags/value zeroed (records 16..40, name_off kept) | **exit 0, byte-identical output** | exit 0, identical | exit 0, all values 0 |
| record array zeroed (16..40), header intact | **exit 0, byte-identical output** | exit 0, identical | exit 0, junk names |
| header zeroed (bytes 4..16), records intact | **exit 0, byte-identical output** | exit 0, identical | **exit 1** (refuses) |
| one pool token renamed same length (`libc.so.6`→`libq.so.6`) | exit 3 (unknown key), empty stdout | exit 3 | echoes the renamed token |

This is the operative meaning of "never reads the header / never walks the record array": no
interpreted header field and no record tuple can change the output. The stop's source and mine both
satisfy it; the structural control fails every one of these probes, so the probes discriminate.

## 5. Invariance of the frozen transform (measured)

`mini-counter.permute` imported in-process and applied to all eight fixtures under the three seeds
(2026-10-25T07:32:05Z): for all 24 combinations, `size_eq=True`, `digest_changed=True`,
`decoded_eq=True`, `nameset_eq=True`, and every changed byte lies in a `name_off` field or at/after
`names_off` (`outside_nameoff_and_pool = []`). So the transformation changes only pool order and the
`name_off` pointers, exactly as the stop's `why_this_falsifies_the_surface` says. Any transform that
must preserve `decode(x)` and is layout-only cannot exclude a class keyed on the content multiset.

## 6. Zero-knowledge variant: the frozen counter leaks its own answer key

`sidefile_a.py` has **no** embedded table. It performs the same structure-blind scan, then loads
`tools/round-34/mini-fix/expected.json` relative to the process cwd and looks up the name set. The
counter replaces the child environment but not the child cwd, and the counter's own `--root` is the cwd
where the canonical argv is issued:

| invocation | UTC | exit | result |
|---|---|---|---|
| counter from `scratch/clone` (cwd = root), seeds `kaidoku-r34-mini-v1`/`alt-1`/`alt-2` | 07:33:08Z | 0 | **8/8 each** |
| counter with `--root <clone>` but cwd `/tmp` | 07:32:29Z | 1 | `matched=0`, all rows exit 3 |

So even a reader that knows nothing about the fixtures reaches the green target, provided the counter is
invoked from its own root — which is exactly the canonical invocation in `claim-stop.json`. This is a
stronger channel than the stop's memorization class (zero prior content knowledge) and is not in the
stop's defect list; it strengthens, not weakens, the stop.

## 7. Attack on the proposed fresh-content repair

Target: `frozen/mini-counter-fresh.py` (w1 candidate), `--root .`, cwd `scratch/clone`. Row receipts
from `scratch/receipts.log`, 2026-10-25T07:30:19Z–07:33:12Z.

### 7.1 The repair defeats my class

| reader | invocation | UTC | exit | matched |
|---|---|---|---|---|
| `memtable_a.py` | unseeded (seed `916921cd…`) | 07:33:10Z | 1 | **0/8**, all rows exit 3 |
| `memtable_a.py` | `--seed kaidoku-r34-mini-v1` / `alt-1` / `alt-2` | 07:33:09Z | 1 | **0/8** each |
| `sidefile_a.py` | unseeded / `alt-1` / `kaidoku-r34-mini-v1` | 07:30:19Z–20Z | 1 | **0/8** each |
| `nameset.py` | unseeded / `alt-1` / `kaidoku-r34-mini-v1` | 07:30:20Z | 1 | **0/8** each |

`memtable_a` cannot key on content that has never been published, and `sidefile_a` finds no expected
file to side-load. The fresh surface is not reachable by either class. `nameset.py` itself is 0/8 here,
so the stop's class is repair-sensitive.

### 7.2 The repair is still reachable when its seed is on the command line

The generator is published (`generate(rng, index)` in the w1 counter), the seed is a CLI argument with a
supported `--seed`/`--seed=` form, and the reader is a child of the counter, so `/proc/<ppid>/cmdline`
is readable (verified: `procpeek.txt`, 07:33:56Z — cmdline fully readable; parent `mem` **denied**
`PermissionError`, yama=`1`; no seed in parent environ). `seedregen_a.py` replicates `generate` exactly
(same call order), identifies the current fixture by whole-file SHA-256 (opaque blob, no field parsed),
and prints the expected records from the regeneration.

| invocation | UTC | exit | matched |
|---|---|---|---|
| `--seed kaidoku-r34-mini-v1` | 07:33:10Z | **0** | **8/8** (`met_target=true`) |
| `--seed alt-1` | 07:33:11Z | **0** | **8/8** |
| `--seed alt-2` | 07:33:11Z | **0** | **8/8** |
| `--seed=alt-1` (equals form) | 07:33:11Z | **0** | **8/8** |
| unseeded, run 1 (seed `1d2ca752…`) | 07:33:10Z | 1 | **0/8**, rows exit 3 |
| unseeded, run 2 (seed `b2886ddd…`) | 07:33:10Z | 1 | **0/8** |
| same reader under the **frozen** counter (must refuse) | 07:33:12Z | 1 | 0/8, all rows exit 3 (parent gate) |

So the fresh counter's guarantee — "no memorised table can be keyed on the content, because the content
has never been published … only record-array traversal recovers the association" — is false under any
invocation that pins the seed in argv. The content *is* a deterministic function of published code plus a
seed that the counter hands to its child in its own command line. Crucially, the counter **replaces the
child environment** (`PATH`/`HOME` only), so a seed passed by environment or kept out of argv would not
leak; the leak is specifically argv, and `--seed` is the documented reproducibility path. A repair audit
that pins seeds for reproducible receipts re-opens the gap the repair was built to close — a
structure-blind class meeting the target without record traversal — even though it is a replay class,
not the memorization class.

### 7.3 Boundary: what the fresh counter still admits

`fixedlayout_a.py` reads no header field; it assumes records start at 16, finds the pool start as the
first offset whose tail is a printable/NUL token run, derives `count`, then walks records. It is *not* my
seat class (it walks the record array), and it is reported only to mark the frontier:

| invocation | UTC | matched |
|---|---|---|
| unseeded (seed `efb5f6e1…`) | 07:30:21Z | **8/8** |
| unseeded (seed `32d20370…`) | 07:33:11Z | 7/8 |
| `--seed alt-1` / `--seed kaidoku-r34-mini-v1` | 07:33:11Z–12Z | 7/8 |

Failure diagnosis (in-process, 07:32:36Z): for seed `alt-1`, fixture `gen-4` has header `names_off=32`
but the last value byte is printable (`0x74`), so the first matching token run starts at 31
(`"tlib4w3o6yo8us.so.7"`); `(31−16) % 8 ≠ 0`, the reader refuses, the counter scores 7/8. The fresh
counter therefore does force record-array traversal for a fixed-layout decoder (as intended), and its
randomly generated content sometimes misleads even that decoder. No stronger conclusion is drawn from a
7/8 boundary result.

## 8. Findings

1. **Stop evidence reproduces.** Same counter, same class, same three seeds, same `matched=8`, exit 0;
   the source pin matches; the class characterization is exact under black-box mutation; the transform
   is measured layout-only. On this axis the stop is not falsified; if anything its case is stronger.
2. **The stop's defect list is incomplete (measure, not record).** Two channels are absent from
   `record_defects_disclosed` F1–F5: (a) the frozen counter's answer-key co-location (`cwd` shared with
   `expected.json`) admits a zero-knowledge structure-blind class at 8/8 — a more severe form of the
   same gap than memorization; (b) the fresh candidate's seed-on-argv channel admits a replay class at
   8/8 under pinned seeds. (a) corroborates the stop; (b) is a defect in the proposed repair, not in the
   stop record. Neither reopens a frozen clause, and neither is a score event.
3. **Repair status.** Defeats content-multiset memorization and answer-file side-loading (0/8); fails its
   own published-content guarantee whenever `--seed` is in argv (8/8). Its safety condition must be
   stated as "seed unguessable and never on the command line", otherwise the green target is reachable
   without record traversal.
4. **Assignment questions answered.** Class: content-multiset memorization (SONAME multiset key + stored
   table). Matched: 8/8 on the frozen green counter, seeds `kaidoku-r34-mini-v1`/`alt-1`/`alt-2`, exit 0.
   Knowledge beyond the opaque path: yes for the memorizer (public `expected.json`/fixtures); no for the
   `sidefile` variant, which reads the counter's own public answer file from the inherited cwd.

## 9. Limits, risks, blockers

- Counter and candidate were run on copies in `/fast/scratch`; no lane bytes were modified. The lane
  `tools/round-34/*`, `claims.json`, `claim-stop.json` and all corpus/doc files were read-only.
- Single host, `python3 3.14.8`; reproducibility of `seedregen_a` depends on the same interpreter's
  `random` stream (true here, both processes are `/usr/bin/python3`).
- `/proc` visibility is host configuration (yama `1`); only the parent *cmdline* was readable. I did not
  attempt to defeat `mem` denial. The unseeded fresh path was not broken by any class I tried.
- `mini-counter-fresh.py` is a wave-1 candidate in `.ufo`, not a frozen instrument; my attack is against
  that candidate's code as copied, sha256 `5181330d…`.
- Not done by this seat: verification of F1–F5 (sibling seats), any gate/`replay-gate.py` rerun, any
  clause/CLEAN/REFUSED recomputation, any repair edit, any SCORECARD/LOG/claims touch. No 100-seed sweep
  of the fresh counter; no mutation testing of a fresh-counter selftest (it has none).

## Verdict

`STOP_EVIDENCE_REPRODUCED`: independent content-multiset reader `matched=8/target=8, exit 0` on the
frozen green counter for seeds `kaidoku-r34-mini-v1`, `alt-1`, `alt-2`; stop source `nameset.py` also
8/8; both proved header- and record-blind by header/record corruption probes; transform measured
layout-only (24/24 fixture-seed combinations). `REPAIR_PARTIAL`: same class 0/8 on the fresh candidate
(3 seeds + unseeded), but seed-on-argv replay 8/8 on three pinned seeds and `--seed=alt-1`, 0/8
unseeded; zero-knowledge side-file class 8/8 on the frozen counter from its canonical cwd, 0/8 when cwd
is elsewhere. No clause reopened, no capability or score awarded.

