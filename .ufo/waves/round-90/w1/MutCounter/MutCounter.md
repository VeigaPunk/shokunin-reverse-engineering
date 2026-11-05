# MutCounter — R90-C1 counter-control mutation test (round 90, wave r90-w1)

Seat: `MutCounter` (mutation-tester). Lane `kaidoku-shokunin`, base `fc52cc9dc`.
Instrument under test: `tools/round-90/upx-later-block-battery.py` (the R90-C1
counter). Question: **does the battery notice a repair that cheats?**

Everything below is measured on this host; every number carries the command that
produced it and the receipt that stores the output. Nothing in the lane tree was
written: `git status --porcelain` lists exactly one untracked path for this seat,
`?? .ufo/waves/round-90/w1/MutCounter/` (HEAD `499d2183a`, command and output in
§9). Seat writes are restricted to this directory; scratch is
`/fast/scratch/hyaku/kaidoku-r90/MutCounter` (removed at the end, receipts copied
here). No tool was installed or upgraded for this seat.

---

## 1. Two revisions of the counter (read this before the table)

| object | sha256 | evidence |
|---|---|---|
| battery **as declared** (`claims.json` `instruments`) | `84664f52afa0c03b38aca23552046fcf5e8e04056a597da7b2b06ef6d5eb8206` | copied to scratch at 23:59:46, `sha256sum` in §9 |
| battery **on disk now** (mtime 00:10:15) | `5462ef134c680e4f811c59da5e8f17ff84159ed5a55bdd5e1fe5ad7226de3210` | `sha256sum tools/round-90/upx-later-block-battery.py` |
| repair as declared | `aaf3536e…` (claims.json) | — |
| repair on disk now (mtime 00:09:30) | `90dea08720a37e876e7f08eafe339a62c710baf402c1342924f9b41b44d5cd6a` | `sha256sum tools/round-90/upx-break-repair.py` |

**The 8 mutants in §4 are mutants of the declared revision `84664f52`** — that is
the revision `claims.json` pins, and it is frozen in
`/fast/scratch/…/MutCounter/pristine/upx-later-block-battery.py`. The lane file
moved to `5462ef13` while this seat was running; the delta (62 diff lines, stored
in §9) renames the `controls_ok` keys to the claim's vocabulary, adds a `rea`
arm, adds `own_sha256`, adds `rev_state`, and rewrites the isolation docstring.
Consequences are stated per finding (F5 is **fixed** upstream; F1/F3/F4/F6/F7 are
not). Any mutant the L1 wants against `5462ef13` has to be re-cut from it — the
anchors differ (e.g. `"N1"` → `"N1-refuse-plain"`, `cheat_live`/`cheat_killed` →
`cheat_repack`).

Consistency of the runs: every mutant run loaded the counter **from scratch**
(`$S/mut/<id>/upx-later-block-battery.py` or `$S/pristine/…`) while its module
dependencies came from `--root` (the lane). The receipt's `pins.modules` records
those sha256s, and all four equal the declaration's `instruments`:
`upx-magic-repair.py 96da7d8e…`, `upx-chain-repair.py 59ee51b0…`,
`upx-field-value-repair.py 41f29f21…`, `control-cheat-repack.py faafc982…`; the
packer is `upx 5.2.0` / `cf2f6e7c…` (`receipts/run-base-prov.json`). The two runs
that used the lane repair (`base-genuine`, `h-expect-ignored-mismatch`) record
`repair.sha256 = 90dea087…`, i.e. the **current** repair, not the declared one.

**Provenance gap on the declared repair.** No artifact in the checkout carries
`aaf3536e…`:

```
$ git -C <lane> cat-file -e fc52cc9dc:tools/round-90/upx-break-repair.py
fatal: path 'tools/round-90/upx-break-repair.py' exists on disk, but not in 'fc52cc9dc'   (rc 128)
$ find .ufo/waves/round-90 -name '*.py' | xargs sha256sum | grep '^aaf3536e'   # no match
```
i.e. the declared repair bytes are not recoverable from this checkout; only the
declaration and its derived score receipts mention the hash. The declared
**counter** bytes *are* preserved by this seat
(`receipts/upx-later-block-battery-declared-84664f52.py`) because they exist
nowhere else either.

---

## 2. Detectors

* **D (cheat detector).** Run the (mutated) counter with a *declared cheat repair*
  and the frozen `--expect`; read `met_target` from the receipt.
  `met_target true` on a cheat = the counter did not notice.
* **D2 (label detector).** Run with the genuine repair and a deliberately
  **mismatched** `--expect`; the frozen kill rule says such a label must fail.

Verdict vocabulary used in §4:

| verdict | meaning |
|---|---|
| **killed** | the mutated counter still reports `met_target false` on the cheat; the named case is the arm that still rejects it |
| **survived** | the mutated counter reports `met_target true` on the cheat; the missing case is named |
| **inert** | the mutated arm's input does not depend on the repair at all, so no cheat repair can change the verdict (proved from the code path, §5/F4) |

---

## 3. Apparatus and premises

### 3.1 Pinned inputs (verified independently of the counter)

```
$ for f in /usr/bin/upx /usr/bin/jq /usr/bin/xxd /usr/lib/libz.so.1.3.2 /usr/bin/docker-init; do
    printf '%s ' "$f"; sha256sum "$f"; done
$ /usr/bin/upx --version | head -1        # upx 5.2.0
$ sha256sum ~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json
a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
```
All six values equal the pins in `claims.json` and in the counter's `preflight`.
`bwrap` and `node v24.21.0` present.

### 3.2 The declared cheats (this seat's, `receipts/cheat-manifest.txt`)

| cheat | sha256 | what it does |
|---|---|---|
| `cheat-provenance.py` (`46ea31d1…`) | re-packs the four **pinned carrier paths** with the pinned packer and emits the pristine packed image when the input differs from it only inside one `sz_cpr` window; refuses non-UPX input (N1) and non-window diffs (N2); verbatim on an intact input (N3). No derivation. |
| `cheat-provenance-leak.py` (`b1320419…`) | same + writes a `leak` sibling of its input inside the invocation box (isolation probe). |
| `cheat-scribble.py` (`aa9f5908…`) | same + flips the emitted image's byte 8 (out-of-window scribble). |
| `cheat-copy.py` (`e758508a…`) | **source-free**: same matching, but the pristine images are its own copies in `carriers/<id>.packed`; it never touches a pinned path. |
| `cheat-copy-scribble.py` (`bfc847fb…`) | `cheat-copy` + byte-8 scribble. |

Cell completeness of the cheats, measured with a harness that rebuilds the
counter's own 14 scored cells plus its N1/N2/N3 fixtures
(`receipts/probe-cheat-cells.py`, 26 invocations each, no REA — REA is
deterministic once `upx -d` equals the carrier pin):

```
$ python3 -I -B cheat-cells.py <cheat> <out.json>
cheat-provenance     -> P1 6/6 P2 4/4 P3 4/4, N1/N2/N3 true   receipts/cheat-cells-provenance.json
cheat-copy           -> P1 6/6 P2 4/4 P3 4/4, N1/N2/N3 true   receipts/cheat-cells-copy.json
cheat-copy-scribble  -> 14/14 cells: repair_rc0+test_ok+unpack_pin true, field_only+identity false
                                                             receipts/cheat-cells-copy-scribble.json
declared control-cheat-repack.py as a *repair*: P1 4/6 (xxd refused: symlink), N2 false on jq/libz/dinit,
  N3 false on xxd                                            receipts/cheat-cells-declared-control.json
```
So the provenance cheats are **cell-complete**: only provenance/pixel arms can
reject them. (This is also why the declared `control-cheat-repack.py` is a
control and not a repair: it is size-keyed, so it also "repairs" a payload flip
and fails N2.)

### 3.3 Premise A — is `identity` implied by `field_only ∧ test_ok`?

For every carrier and for block 0 (P2/P3 class) and block 1 (P1 class), the field
was overwritten with every value in `0..sz_unc`, 64 values above `sz_unc`, and
2000 random 32-bit values, and `upx -t -q` was run on each file:

```
$ python3 -I -B sweep-unique2.py         # receipts/probe-sweep-unique.py
$ cat receipts/sweep-unique2.txt         # per-pair digest + the two summary lines
jq    b0 2969 values, other: []  xxd   b0 2969, other: []
jq    b1 7473 values, other: []  xxd   b1 4921, other: []
libz  b0 2745 values, other: []  libz  b1 65222, other: []
dinit b0 2801 values, other: []  dinit b1 2657, other: []
STORED_UNIQUE_ALL True
TOTAL_VALUES_TESTED 91757
```
**91,757 values, 8 (carrier, block) pairs, 0 values other than the stored
`sz_cpr` pass `upx -t`,** and the stored value's file unpacks to the carrier pin
in every pair. Therefore, for any same-length output that differs from the
tampered image only inside the tampered window (`field_only`) and passes
`upx -t` (`test_ok`), the output **is** the intact packed image (`identity`).
Two consequences: `identity ⇒ field_only` and `field_only ∧ test_ok ⇒ identity`,
so the two arms are algebraically the same arm on this cell shape.

My first sweep attempt shared 12 probe filenames across 12 threads and is
discarded; this is the re-run with one unique file per probe.

### 3.4 Premise B — a repair may scribble outside the window

Bytes 8–15 of a packed ELF are `EI_PAD`. Flipping each of the eight, on each of
the four carriers, then `upx -t` and `upx -d`:

```
$ python3 - <<'EOF' … receipts/sweep-eipad.json   (32 probes)
EOF
byte8_free_pin_all True
per_carrier_ok {'jq': [8..15], 'xxd': [8..15], 'libz': [8..15], 'dinit': [8..15]}
```
All 32 keep `upx -t` rc 0 **and** the unpacked bytes at the carrier pin. A repair
that writes `EI_PAD` therefore satisfies `test_ok`, `unpack_pin` and
`rea_recover` while its output is neither the tampered image nor the intact
image: only `field_only`/`identity` see it.

### 3.5 Mutants (single anchor each, `receipts/mutant-manifest.json` + `receipts/mutant-*.diff`)

Cut from `84664f52` by exact text replacement, each anchor asserted to occur
exactly once; every diff is one hunk. All ten copies pass the counter's own
`--selftest`:

```
$ for D in root/*/; do python3 -I -B $D/tools/round-90/upx-later-block-battery.py --selftest; done
SELFTEST cases=8 failures=0      (×10)      receipts/mutant-selftests.txt
```

| id | anchor changed | sha256 |
|---|---|---|
| a | `isolation` record hard-coded `"ok": True` | `b974de875038ea7e…` |
| b | `"carrier_blind": …` → `True` in `arms_ok` | `3cbdfc9c34349fcb…` |
| c | `"no_work": controls[…] == 0` → `True` | `46d976bd4bddc749…` |
| d | `"cheat_killed": … is False` → `True` | `f3980f6e55df3e41…` |
| e | `identity` excluded from the `recovered` conjunction (still computed and recorded) | `f63b54c194b7ecdb…` |
| f | `field_only` excluded from the conjunction | `7040d44f950d7192…` |
| g | `rea_recover = (counts is None or counts == orig)` | `3f1ba18f98ddff01…` |
| h | `met = met and label == args.expect` → `met = met` | `b5be4a7101accce2…` |
| y (supplementary double) | e+f together | `c51143c6fff64394…` |
| z (supplementary double) | b+d together | `d2b60b87175aceba…` |

Run shape (one command per run, `receipts/matrix-launcher.sh`):
`python3 -I -B <mutant> --root <lane> --rev fc52cc9dc --pkg <rea-agents> --work <run dir> --expect "P1 6 of 6; P2 4 of 4; P3 4 of 4" --repair-cmd <cheat> --json-out <run dir>/receipt.json`.
16 runs in four concurrent waves of 5/5/3/3, 463.4 s / 564.0 s / 585.0 s / 548.4 s
per wave. Each run makes 18 REA 6.5.0 invocations (4 carrier originals + 14 scored
cells; the blind re-scores run with `rea_on=False`); a single dinit analysis is
48.8 s and five of the eighteen are dinit.

---

## 4. Results — killed 7 of 8, survived 1 of 8

D = cheat detector (§2). "Rejected by" is the first non-recovered entry in the
receipt; `carrier_blind/jq/-7` means the blinded re-score of the first P1 cell
(`rc 3`, no output — the repair could not read the carrier inside the sandbox).

| # | mutant | cheat | `met_target` | `exit` | rejected by | verdict |
|---|---|---|---|---|---|---|
| — | *pristine* `84664f52` | provenance | **false** | 1 | `carrier_blind/jq/-7` (0/6 blind cells) | reference: the cheat is caught |
| a | isolation accepts any listing | provenance-leak | **false** | 1 | `carrier_blind/jq/-7` | **killed** (by another arm) |
| b | carrier_blind not required | provenance | **TRUE** | 0 | — (0/6 blind cells, yet `met`) | **SURVIVED** |
| c | no_work not required | provenance | **false** | 1 | `carrier_blind/jq/-7` | **killed** + inert (§5/F4) |
| d | cheat_killed not required | provenance | **false** | 1 | `carrier_blind/jq/-7` | **killed** + inert (§5/F4) |
| e | identity arm dropped | copy-scribble | **false** | 1 | `P1/jq/-7`, `field_only` false | **killed** (equivalent to f, §5/F3) |
| f | field_only arm dropped | copy-scribble | **false** | 1 | `P1/jq/-7`, `identity` false | **killed** (equivalent to e, §5/F3) |
| g | rea null counts as True | provenance | **false** | 1 | `carrier_blind/jq/-7` | **killed** + inert (§5/F5) |
| h | `--expect` ignored | provenance | **false** | 1 | `carrier_blind/jq/-7` | **killed** on D; **live on D2** (§5/F6) |
| y | e+f (double) | copy-scribble | **TRUE** | 0 | — | survives: the pair is the real guard |
| z | b+d (double) | provenance | **TRUE** | 0 | — | survives: the two provenance controls are redundant |

Receipts: `receipts/run-<id>.json`, `receipts/run-<id>.exit.txt`,
`receipts/matrix-summary.json` / `.txt` (`receipts/probe-summarize.py` regenerates
both from the receipts).

Supporting pairs measured for the two arms that are individually redundant:

```
base-leak  (pristine + leak cheat):  isolation false, box listings ('in','leak'), ('in','leak','out')
a-run      (mutant a + leak cheat):  isolation TRUE , same listings          -> mutation is visible, D still rejects
base-prov  (pristine + provenance):  cells 6/6 4/4 4/4, only carrier_blind false
b-run      (mutant b + provenance):  cells 6/6 4/4 4/4, carrier_blind recorded 0/6 recovered, met TRUE
base-copy  (pristine + copy cheat):  met TRUE, blind_ok true, blind cells 6/6 recovered
base-copy-scribble (pristine):       cells 0/6 0/4 0/4 -> rejected by field_only+identity
y-run      (e+f + scribble):         cells 6/6 4/4 4/4, met TRUE, blind 6/6
```

---

## 5. Findings

**F1 — the counter's `met` is satisfiable by a non-repair that carries its own
copies of the packed images. (pristine counter, `met_target true`, exit 0.)**
`carrier_blind` binds decoy bytes onto the four **pinned paths** and a tmpfs onto
its own run root; `cheat-copy.py` reads `carriers/<id>.packed` inside this seat
directory and is untouched by either. The receipt shows `blind_ok true` (the
probe proves the four paths *are* blinded) and **6 of 6 blind cells recovered**,
i.e. the arm is honest about what it measures and what it measures is "did the
repair read one of four paths", not "did the repair derive the value". Evidence:
`receipts/run-base-copy.json`. This is the single most important result of the
seat: it means the claim's word "provenance" over-states the control. The same
cheat also passes the *declared* `cheat_repack` control, because that control
probes `control-cheat-repack.py`'s bytes, not the candidate's.
Status on `5462ef13`: the blinding construction is unchanged
(`blind_paths = realpath(CARRIERS[].source)`, `--tmpfs run_root`), so
`cheat-copy.py` is still outside it — [INFERENCE]; it closes with the base-copy
run repeated against the new file (`--repair-cmd <seat>/cheat-copy.py`, same flags,
--expect unchanged), which this seat did not run because the L1 called the wave.

**F2 — (b) is the only single mutation that flips `met` on the cheat, and it is
not an isolated defect.** b's receipt records 0/6 blind cells recovered and still
returns `met_target true`; but F1 shows the pristine counter accepts a cheat that
the blind arm cannot see at all. So "carrier_blind required in `met`" buys less
than it appears: it rejects the *declared* cheat and any repair that reads the
pinned paths, and nothing else.

**F3 — `field_only` and `identity` are the same arm on this class; (e) and (f)
are equivalent mutants.** From §3.3: `identity ⇒ field_only`, and
`field_only ∧ test_ok ⇒ identity` (91,757-value sweep, exhaustive over the
in-range values of both relevant blocks of all four carriers). No repair can
distinguish (e) from (f): both runs return `P1 0 of 6` on the scribble cheat, and
both return the pristine verdict on every other cheat. Dropping **both** (y) lets
a repair that emits the correct image *plus* one `EI_PAD` byte through with
`P1 6 of 6; P2 4 of 4; P3 4 of 4` and `met_target true`. The measured guard for
that is exactly one of the two arms, not two.

**F4 — `no_work`, `cheat_live` and `cheat_killed` cannot depend on the candidate
repair, so mutating them is inert for any cheat.** Code path: the scored repair
is `args.repair_cmd` (line 291), while `no_work` is `score_case(os.path.join(root,
R89_REPAIR), …)` (line 379) and both cheat probes are `score_case(cheat, …)`
(lines 437/440) with `cheat = os.path.join(root, CHEAT)`. They are instrument
-regression guards, not anti-cheat guards. `c` and `d` therefore report `false`
for a reason that has nothing to do with the mutation; their kill is real but
trivial. This matters for the claim's phrasing "every control true": five of the
eight arms constrain the candidate (N1/N2/N3/isolation/carrier_blind), three do
not. `5462ef13` keeps the same three inputs (merging `cheat_live`+`cheat_killed`
into `cheat_repack`), so this stands.

**F5 — the declared revision treats a *null* REA result as recovered (g); the
current revision fixes it.** In `84664f52`, `recovered` accepts
`arms["rea_recover"] in (True, None)`, and `rea_recover` is `None` exactly when
`unpack_pin` is false or REA never ran — the first already fails the cell, so the
allowance is reachable only through a REA failure with a valid unpack (a pinned,
working REA: not reachable with any repair). Mutant g (`counts is None or …`)
therefore cannot be killed by a repair either; its distinguishing input is an
environment failure, not a cheat. `5462ef13` adds
`rea_ok = rea_on and all(… is True …)` and a `rea` arm, so null no longer passes
when `rea_on`. **Fixed upstream; no action needed except noting that the declared
revision's receipt could not have shown it.**

**F6 — `--expect` is the only arm a *cheat* cannot reach, and it is the only arm
whose loss changes `met` without any cell moving.** Mutant h on D: `met false`
(controls still reject the provenance cheat). Mutant h on D2, genuine repair with
a declared **mismatched** label:

```
$ … --expect "P1 0 of 6; P2 0 of 4; P3 0 of 4" --repair-cmd tools/round-90/upx-break-repair.py
{"label": "P1 6 of 6; P2 4 of 4; P3 4 of 4", "met_target": true, "exit": 0}
receipts/run-h-expect-ignored-mismatch.json
```
The pristine counter with the same repair and the *correct* label also returns
`met_target true`, exit 0 (`receipts/run-base-genuine.json`, all controls true,
`no_work` 0). So h is a real, observable mutation, and D cannot see it because no
cheat can reach the label — the label arm needs a negative fixture (D2), which
the counter's `--selftest` does not contain (§F7).

**F7 — the counter's `--selftest` gives zero mutation coverage of the control
composition.** All ten mutant copies report `SELFTEST cases=8 failures=0`
(`receipts/mutant-selftests.txt`): the selftest covers `layout`, `window_only`,
the declared-orig table and the P1 cell count, and touches none of `arms_ok`,
`met`, `score_case`'s conjunction or the `--expect` clause. A superseding
revision inheriting this selftest inherits no protection against any of a–h.

---

## 6. Missing cases (what would kill what)

| missing case | kills | why it is not there today |
|---|---|---|
| **M1 — a novelty cell.** Score one cell on a carrier the repair cannot have tabulated: pack a *fifth* binary (or re-pack a pinned one after a benign, size-changing edit to its read-only data) and tamper its interior block. | the surviving cheat `cheat-copy.py`, hence F1/F2 | the six P1 cells are the same three pinned carriers the class names, so a table keyed by length (or by bytes) covers them exactly. One extra cell whose length no table can contain forces derivation. |
| **M2 — a whitelist sandbox instead of a blacklist.** Run the repair with only the box, the interpreter, and `tools/round-8{7,8,9}`/`round-90` bound, everything else hidden (`bwrap --unshare-all --tmpfs / --dev-bind /usr /usr …` per needed path), instead of binding decoys over four paths. | F1 at the root: any repair carrying data or reading a copy dies; only derivation survives | `carrier_blind` binds decoys over `realpath` of the four sources and leaves the rest of the host readable. |
| **M3 — a second provenance cheat in the counter.** Probe not only `control-cheat-repack.py` but a cheat that carries its own packed images (bytes `e758508a…`), asserted *killed*. | F1 and F2 together: they make the arm set honest about "provenance" vs "path blindness" | both cheat probes are bound to one file, `tools/round-90/control-cheat-repack.py`. |
| **M4 — `rea_recover is True` assertion when `rea_on`.** | g on the declared revision, and any future null-tolerant variant | declared `recovered` accepts `None`; fixed in `5462ef13` by the `rea` arm — keep it. |
| **M5 — a negative `--expect` case in `--selftest`**, plus a *receipt-shape* case: mutate the label, mutate `arms_ok`, assert `exit 1`. | h on D2, and a–f, g at the selftest level (F7) | the selftest never builds a receipt. |
| **M6 — an instrument-regression fixture for `no_work`/`cheat_*`.** | nothing cheat-shaped: it makes the *purpose* of those arms legible (F4) | they are candidate-independent by construction; only an instrument edit can move them. |

---

## 7. Limits and non-claims

* I did not evaluate R90-C1's truth. `receipts/run-base-genuine.json` (genuine
  repair, current bytes `90dea087…`) returns `P1 6 of 6; P2 4 of 4; P3 4 of 4`,
  every control true, exit 0 — but that is the executor/reviewer's predicate, cited
  here only as the D2 true-positive reference.
* The declared class, its limits (`libz` out of class, the last-block
  under-determination, cost of the scan) and the repair's derivation were not
  touched, ranked or judged.
* The cheat's own table (`carriers/*.packed`) is built with the pinned packer from
  `copy2` copies of the four sources; `receipts/cheat-manifest.txt` pins it. The
  cell harness confirms the table reproduces the counter's own packed fixtures
  byte-for-byte (`identity` true on all 14 cells, `receipts/cheat-cells-copy.json`).
* Every probe file is unique per task; the discarded first sweep attempt (shared
  filenames) is mentioned in §3.3 and its receipts were deleted, so no number here
  rests on it.
* Wall-clock: run counts and REA timings are measured under a loaded host; they are
  shape evidence, not a cost claim.

---

## 8. Receipt index (absolute paths)

Seat: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/MutCounter/`

```
MutCounter.md                      this report
cheat-provenance.py                cheat (source-bound), sha 46ea31d1…
cheat-provenance-leak.py           isolation probe,     sha b1320419…
cheat-scribble.py                  EI_PAD scribble,     sha aa9f5908…
cheat-copy.py                      source-free cheat,   sha e758508a…
cheat-copy-scribble.py             source-free+scribble, sha bfc847fb…
carriers/{jq,xxd,libz,dinit}.packed  the cheat's own table (shas in receipts/cheat-manifest.txt)
receipts/cheat-manifest.txt        sha256 of every cheat file and table entry
receipts/mutant-manifest.json      mutant id -> path, sha256, diff size
receipts/mutant-*.diff             the ten single/double-anchor diffs (one hunk each)
receipts/mutant-selftests.txt      8/8 cases, 0 failures, for all ten copies
receipts/matrix-launcher.sh        the exact command shape of all 16 runs
receipts/probe-cheat-cells.py      cell harness (14 cells + N1/N2/N3 per cheat)
receipts/cheat-cells-provenance.json   cells 6/6 4/4 4/4, N1/N2/N3 true
receipts/cheat-cells-copy.json         cells 6/6 4/4 4/4, N1/N2/N3 true
receipts/cheat-cells-copy-scribble.json  14/14 pass test_ok+unpack_pin, field_only+identity false
receipts/cheat-cells-declared-control.json  control-cheat-repack as a repair: P1 4/6, N2/N3 false
receipts/probe-sweep-unique.py + sweep-unique2.json/.txt   91,757-value uniqueness sweep
receipts/sweep-eipad.json          32 probes: bytes 8–15 free+pin on all four carriers
receipts/probe-summarize.py, matrix-summary.json, matrix-summary.txt   the §4 table, regenerable
receipts/run-<id>.json, run-<id>.exit.txt     the 16 counter receipts (pristine, a–h, y, z,
                                              base-leak, base-genuine, h-mismatch)
```

Commands (all from `/fast/scratch/hyaku/kaidoku-r90/MutCounter`, which is removed;
the scripts are copied into `receipts/`):

```
python3 -I -B sweep-unique2.py                       # §3.3
python3 -I -B cheat-cells.py <cheat> <out.json>      # §3.2
python3 summarize.py                                 # §4 table
diff -u pristine/upx-later-block-battery.py <lane>/tools/round-90/upx-later-block-battery.py   # §1 (62 lines)
```

---

## 9. Provenance of this document

```
$ cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git rev-parse --short HEAD
499d2183a
$ git status --porcelain | grep '^?? .ufo/waves/round-90/w1/MutCounter/'
?? .ufo/waves/round-90/w1/MutCounter/
$ sha256sum /fast/scratch/…/pristine/upx-later-block-battery.py
84664f52afa0c03b38aca23552046fcf5e8e04056a597da7b2b06ef6d5eb8206   # == claims.json instruments
$ sha256sum tools/round-90/upx-later-block-battery.py tools/round-90/upx-break-repair.py
5462ef134c680e4f811c59da5e8f17ff84159ed5a55bdd5e1fe5ad7226de3210  tools/round-90/upx-later-block-battery.py
90dea08720a37e876e7f08eafe339a62c710baf402c1342924f9b41b44d5cd6a  tools/round-90/upx-break-repair.py
```

No lane file was created, edited or deleted by this seat; no git/jj mutation was
run anywhere; the fleet repo, `.ufo/state`, `.ufo/watchdog.log` and the round-89
paths were read-only or untouched. No tool was installed or upgraded.
