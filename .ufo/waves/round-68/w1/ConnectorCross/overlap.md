# Sibling-overlap scan — kaidoku round 68 wave 1 (seat ConnectorCross)

Read-only scan of the 20 non-kaidoku `*-shokunin` lanes for prior ownership of round 68's two
surfaces:

- **(a)** an instrument-registry / inventory-conformance census — a gate comparing a **declared
  table** against the **files a plan names**;
- **(b)** a packed-executable / UPX triage route;
- **(c)** a sha256-identity rule of the form "the unpack restores the original".

Lane `kaidoku-shokunin` at `6ffa9ce1119ec01c953494d8f5b28e419efad646` (worktree carrying L1's
uncommitted `PROVINCE.md` / `SKILL.md` / `corpus/QUALITY.md` edits — none read as evidence here).
Base `fcbe200f6739c38939e0dabf3f251de2cc6bd727`, operative freeze
`1eaf596e5f241762349fbd102c9e09ec1df18e3f` (both verified present with `git cat-file -e`).
Sibling lanes are separate repositories and were read as working trees.

Nothing outside `.ufo/waves/round-68/w1/ConnectorCross/` was written. No sibling tool was run, no
sibling file imported, no `pacman` transaction, no install. Scratch
`/fast/scratch/hyaku/kaidoku-r68/ConnectorCross` removed after its receipts were copied here.

**Fleet-root `merge/` and `considerthese/` do not exist** (`ls` → "No such file or directory").
Per-lane `considerthese/` directories do exist and were scanned (hit 13 below).

---

## 1. Hit table

`relation` is asserted against the surface kaidoku round 68 declares, not against the sibling's own
purpose. Line numbers are the sibling's working-tree lines at scan time.

### Surface (a) — declared-table vs files/instruments conformance census

| # | lane | path:line | what it does | class | relation to ours |
|---|---|---|---|---|---|
| 1 | kama | `tools/gate-registry-check.py:1-45`, population regex `:79` | Population = tracked `.ufo/waves/round-*/count-*.py` **or** flat `tools/round<N>-*.py` (one regex, `:79`); registry = the five-column tables in `SKILL.md`; grades `thin-row`, `empty-entry`, `empty-exit-map`, `missing-path:PATH`; prints `registered R unregistered U defective D` | **same class**, disk → registry | **nearest precedent.** Same shape (unregistered paths named individually, U/D tally, exit 2 for could-not-evaluate). Differs in derivation direction **and in population rule**: layout-keyed, not plan-keyed |
| 2 | kama | `SKILL.md:1266`, `:1362`, `:1417` | The gate's three generations: round 28 occurrence-only (`unregistered .ufo/waves/round-25/count-c2.py` at its base); round-32 repair adding row-meaning grades; round 43 registering sixteen counters the gate had reported unregistered **since round 35** | class history | The same defect kaidoku round 67 hit, with the same repair shape. Round 34 widened the glob because "the round-33 counters live in `tools/` and were invisible to this gate" — a layout-keyed population going blind on a layout change |
| 3 | kama | `corpus/QUALITY.md:362` (KQ54) | Standing criterion: a round adding/keeping/inheriting a round-scoped counter ends with the registry green **at the landed tip**, every population member has a five-column row, "a row already present is re-derived, not assumed, **because a registered row can still be false**" | class criterion | Ours is a one-shot round claim; kama's is a standing per-round criterion. Same mismatch taxonomy |
| 4 | kama | `tools/capability-repertoire-audit.py:1-40` | Canonical capability table vs union of all capability tables: `missing`, `unsubstantiated` (evidence cell paths must resolve at the revision) | adjacent | Same family (declared vs repo), different object: SCORECARD capabilities, not instruments |
| 5 | mori | `tools/mori-gate-registry.py:1-30` | Eight-cell rows read wherever they sit; attribution by `entry_names` (the row whose entry cell's first backticked command invokes the path); a real `--selftest` **branch** required (comment/docstring mention is not a branch); `duplicate`, `wrong_row` | **same class, stricter** | Owns an arm we do not grade: our census never checks that a row's self-test flag is a real branch |
| 6 | mori | `tools/mori-register-check.py:1-22`; `corpus/QUALITY.md:994` | Active capabilities register vs `MANIFEST.json` keys; output `registered=29 unregistered=3 no_selftest=6 duplicate=0 wrong_row=0 tables=7` | same class | Its `duplicate` / `wrong_row` vocabulary is our `duplicate_rows` / `row_absent` |
| 7 | kotoba | `verifiers/check_gate_registry.py:1-45` | Universe = every blob directly under `verifiers/`; eight-cell row equality; verdict-map pair grammar; self-test flag must be an **exact active handler** (Python `add_argument` string or shell `case` arm, via AST); pinned-values paths must exist; a `probe` may not declare `1=failed` | **same class, strictest** | Strongest row semantics in the fleet. Population is still layout-keyed (`ls-tree` over one directory) |
| 8 | kotoba | `corpus/QUALITY.md:46` (Q35) | Every `verifiers/` script has exactly one registry row; the check is "shown able to fail by its `gate with self-test none` arm and, from round 55, by an **all-`probe` table (`0 of 26`)**" | class criterion | **Owns the population-collapse arm** — the one arm I would otherwise have proposed for R68-C1 |
| 9 | tsukuroi | `tools/check-registry-coverage.py:1-20` | Operative `SKILL.md` gate/probe registry vs committed tools, git subprocesses under an allow-listed child environment | same class | Layout-keyed population; adds a sandboxed-git contract |
| 10 | tameshi | `tools/registry-check.py:1-30` | Replays every active row of `tools/registry.json` against its registered outcome (exit + stdout needles, timeout) | adjacent | Registry → **execution replay**, not files → registry. Registry is JSON, not a SKILL table |
| 11 | souji | `tools/souji-registry-agreement.py:1-24` | Declared-vs-observed over committed bytes only: K1 SOURCES-row ↔ `used-by` entry agreement, K2 stale-statement append-only agreement; `mismatches=0` exit 0 | adjacent | Same declared-vs-observed family; object is a source registry, not an instrument inventory |
| 12 | revenger | `corpus/self_assessment_check.py:1-30` | Six named mismatch classes (SM1-SM6) between the lane's self-description and the repository: index ranges, index coverage, quoted digests, verifier authorship, commit citations, `K_HELD_BACKED` | adjacent (calibration) | Multi-class declared-vs-repo census; different predicates, same calibration goal |
| 13 | chousa | `considerthese/2026-10-25.md:28-34` | Registry history: 54/54 → widened to "anything a verdict names or a gate runs" (72/72, then 94/94); "of round 47's 25 mismatches, 8 were real self-assessment gaps and **10 were the counter's own escaped-pipe parsing bug**" | class history + false-positive risk | The fleet's clearest statement that this class's false positives come from the counter's own cell parsing |

### Surface (b) — packed-executable / UPX triage

| # | lane | path:line | what it does | class | relation to ours |
|---|---|---|---|---|---|
| 14 | revenger | `corpus/knowledge/round-73-re-resource-atlas.md:324-333` | Packer / obfuscation / anti-analysis RE atlas: S348 "SoK: Deep Packer Inspection" (Type I-VI taxonomy), S343-S350. Limit recorded verbatim: "A memory dump is a time-indexed observation, not 'the unpacked binary'" | adjacent **knowledge**, no route | Nearest RE authority. It is a source ledger, not an instrument; it declares no packer-detection capability |
| 15 | revenger | `corpus/SOURCES.md:259` (S244), `:264` (S249), `:295` (S280), `:343` (S328) | Static unpackers mined (kavanoz, pkg-unpacker, qc_image_unpacker); **dynamic unpackers rejected** — S249 mal_unpack: README says "This unpacker deploys the original malware"; disposition "live-malware execution is refused in this province" | adjacent, refusal precedent | Confirms a **static-only** unpack route sits inside the fleet's existing refusal line |
| 16 | revenger | `corpus/knowledge/2026-10-12-rea-readiness-checklist.md:17`, `:40` | Host table row: `jadx/binwalk/unblob/pwntools` ABSENT → "firmware extraction, ELF-layout routes blocked until caller-supplied"; the 2026-10-19 re-verification marks that row **STALE → 3 of 4 present** | adjacent host-state, no route | Records the class as *blocked*, never as owned |
| 17 | revenger | `reports/round-73/scout-packs/ReFrameworkTargets.md:13` | GoReSym anchor quoting "malformed **unpacked** binaries, such as from UPX" | not a route | Source text, no instrument |
| 18 | game-dev-3d | `reports/round-102/adversary/F6.md:54` | A past `pacman -S … upx …` install line in a report | not a route | Only other literal `upx` occurrence outside kaidoku in the scanned set |
| 19 | kumitate | `scripts/omp-binary-probe.sh:7-9` | Runs `<binary> --version` **only when the file is ELF**, so a script masquerading as the release binary fails closed | adjacent (ELF type gate) | ELF *typing* as a fail-closed gate; not packing, no decompression, no identity round-trip |

No sibling tool, gate registry row, `corpus/QUALITY.md` criterion, or `SKILL.md` entry anywhere in
the 20 lanes names UPX, a packer, or a packed-binary arm. `grep -rn -iE '\bupx\b' */SKILL.md
*/corpus/QUALITY.md` → no hits.

### Surface (c) — sha256 identity, "the unpack restores the original"

| # | lane | path:line | identity relation it establishes | relation to ours |
|---|---|---|---|---|
| 20 | chousa | `tools/receipt-pin.py:1-12` | Receipt `SHA256=<64 hex> <path>` must equal `git cat-file blob REV:PATH` — **committed bytes**, never the worktree; and "Header consistency is NOT execution authenticity" | Pin of committed bytes. Nearest wording for "the digest must equal the pin", but the object is a receipt/record pair, not a transform's output |
| 21 | revenger | `corpus/audit_source_quotes.py:1-6` | A receipt is VERIFIED only when the row's quote appears verbatim at its recorded span in the fetched-bytes file **whose sha256 the receipt pins** | Pin of acquired external bytes |
| 22 | kama | `tools/gguf-identity.py:1-10` | Parses a fixed header/KV table, streams sha256 over the complete bounded file; "tensor payloads are never decoded" | Pin of the inspected file itself — identity of the *input*, not of a derived copy |
| 23 | kama | `corpus/QUALITY.md:440` (KQ85) | "a digest says **which bytes run**, not which file"; the running image is opened through `/proc/<pid>/exe`, not read as a path | Identity **doctrine**: the pin must name the bytes that execute. Directly supports pinning the original carrier rather than the packed stub |
| 24 | kotoba | `verifiers/check_substrate_pins.py:43-47`, `:64-67` | "the `~/.local/bin/opencode` npx wrapper executes — the wrapper itself is never the pinned file, **its sha says nothing about the ELF that runs**"; round 72 moves `omp` to `omp.real` for the same reason | Same doctrine, second lane. The packed stub's sha says nothing about the program — the unpacked copy's sha does |
| 25 | revenger | `corpus/knowledge/round-64-firmware-region-byte-evidence.md:5`, `:16`, `:179` | Scans every byte offset for a zlib stream that reaches end-of-stream cleanly, **inflates in memory and hashes the inflated bytes** against an authored oracle; coverage-map explicitly excludes "the REA `extract_firmware` route, vendor or device firmware families, **any container format**" | **Nearest (c) precedent**: derived bytes hashed against pinned values. Scoped by an explicit refusal, so it claims no route |
| 26 | chousa | `tools/capture-text.py:1-30` | Derives one defined text form from an OOXML zip or an OLE compound file (CFB FAT/mini-FAT/directory chains, FIB `wIdent`, piece table) "so a quote's offset is reproducible" | Transform-with-reproducible-output precedent. Reproducibility of offsets, not sha identity of the derived copy |
| 27 | kama | `corpus/QUALITY.md:396` (KQ69) | A filed receipt records every input's origin (URL, SHA-256, archive member path) and a replay tool "verifies every digest **before** anything is extracted or executed" | Ordering rule for *acquired* inputs. Adjacent; our route's post-extraction hash is an identity check on a local deterministic transform, not a gate on a remote input |
| 28 | audio | `corpus/knowledge/2026-10-14-sox-preemptor-map-complete.md:95` | A decoder's output is "byte-identical to r65-critic's `D1_hcomdecode+act.wav`" | Identity across a transform, but the reference is another decode, not a pin of an original |

No sibling states the rule R68-C2 uses — **the unpacked bytes' sha256 equals the original's pin, so
unpacking is an identity**. The rule is composed from owned parts (derived-byte hashing, #25;
digest-names-the-bytes-that-run, #23/#24) and is stated by no lane.

---

## 2. Verdict per surface

### (a) Instrument-registry / inventory-conformance census — **DUPLICATE CLASS, distinct instance**

Five lanes own an instrument of this class (`kama` #1, `mori` #5, `kotoba` #7, `tsukuroi` #9, plus
`chousa`'s registry history #13), and two more own adjacent declared-vs-repo censuses (`tameshi` #10,
`souji` #11, `revenger` #12). Re-implementing "a declared table compared against the repository" would
be the fifth copy of an owned class.

**The class is owned. The population rule is not.** All five derive the population from the **tree
layout** — a glob (#1 `:79`) or an `ls-tree` over one directory (#7). R68-C1 derives it from
`plans/round-N-claims.md` for the round's own N. That is not a cosmetic difference; it is the axis
that produced the round-67 defect, and it is measurable:

```
$ python3 .ufo/waves/round-68/w1/ConnectorCross/poprule.py fcbe200f… 1eaf596e…
BASE rev=fcbe200f6739c38939e0dabf3f251de2cc6bd727
  plan_keyed_scope=69
  kama_layout_rule_matches=0
  kama_layout_rule_misses=69
  round67_in_scope=['tools/round-67/avm-le-counter.py', 'tools/round-67/mutation-battery.py']
  round67_matched_by_kama=[]
FREEZE rev=1eaf596e5f241762349fbd102c9e09ec1df18e3f
  plan_keyed_scope=71
  kama_layout_rule_matches=0
  kama_layout_rule_misses=71
  round67_in_scope=['tools/round-67/avm-le-counter.py', 'tools/round-67/mutation-battery.py']
  round67_matched_by_kama=[]
```

*(observation)* Applying kama's frozen population regex (`gate-registry-check.py:79`,
`^(?:\.ufo/waves/round-[^/]+/count-[^/]+|tools/round[0-9]+-[A-Za-z0-9._-]+)\.py$`) to this lane's
plan-keyed scope matches **0 of 69** paths at base and **0 of 71** at the freeze, including **0 of the
2** round-67 instruments. Kaidoku keeps counters in the nested `tools/round-N/` layout, which the flat
`tools/round<N>-…` alternative cannot match, and has no `.ufo/waves/round-*/count-*.py` population at
all. A lane importing that instrument verbatim would score this lane's inventory as empty and print a
clean green.

*(observation)* `plan_keyed_scope` reproduces the claim's `scope_size`: 69 at base, **71 at the freeze** —
an independent re-derivation of one R68-C1 atom by a second code path (`poprule.py`, not the frozen
instrument). `registry_rows` was not re-derived here.

*(observation)* kama's own repair record (#2) is the same failure mode in the same class: round 34
widened the glob because a directory of counters was "invisible to this gate". A layout-keyed
population goes blind once per layout change and is repaired one glob at a time. Kaidoku's round-67
instruments sit in a nested directory, i.e. the layout has already drifted once.

*(observation)* kotoba #8 owns the **population-collapse** arm ("all-`probe` table (`0 of 26`)"),
mori #5 owns the "self-test must be a real branch" arm, and kama #3 owns "a registered row can still
be false". Our four mismatch classes (`unregistered`, `duplicate_rows`, `row_absent`, `thin`) cover
neither the collapse direction nor the self-test-branch arm. `thin` is stricter than kama's `thin-row`
(it requires the verdict cell to name all three exit codes) and weaker than kotoba's eight-cell
equality.

No contested ownership: no sibling names a kaidoku tool path, and no sibling registry row describes
`tools/round-68/*`.

### (b) Packed-executable / UPX triage — **UNOWNED (instrument), ADJACENT (knowledge)**

No lane in the fleet has an instrument that takes a packed binary as input. The literal token `upx`
appears outside kaidoku in exactly two text surfaces (#17, #18), neither a route. No `SKILL.md`
registry row, no `corpus/QUALITY.md` criterion, and no `tools/` script in the 20 lanes names UPX or a
packer.

The nearest possession is revenger's (#14, #15, #16): the RE lane, which owns the *source ledger* for
packers and packer taxonomy, explicitly **rejected** dynamic unpacking on charter grounds (S249,
"live-malware execution is refused in this province"), and records ELF-layout routes as "blocked until
caller-supplied". That is a knowledge claim and a refusal, not a route. Detecting packing, unpacking
with an identity check, and recovering the original's inventory is uncontested.

Two boundaries the precedent sets on a new route, both already satisfied by R68-C2's arms:
i. it must stay **static** (`upx -d` on bytes, no sample execution) — S249's rejection line;
ii. it must not be read as contradicting the atlas's S348 caution "a memory dump is a time-indexed
observation, not 'the unpacked binary'". A `upx -d` output is a deterministic, byte-exact inverse of a
known transform whose sha256 is checked against a pin of the original — not a dump. The distinction is
worth one sentence in the report, because the atlas sentence reads like a counter-argument out of
context.

### (c) sha256 identity, "the unpack restores the original" — **UNOWNED AS A RULE, ADJACENT PARTS**

Four distinct identity relations are owned (record↔commit #20, receipt↔fetched bytes #21,
file↔itself #22, derived copy↔pin #25), plus the doctrine that the pin must name the bytes that run
(#23, #24). None is the rule "a decompression's output hashes to the original's pin". The nearest is
revenger #25 (inflate members, hash the inflated bytes against an oracle), and it is scoped by an
explicit exclusion of `extract_firmware` and "any container format", so it claims no route and cannot
be read as one.

The rule itself is **composed**, and composition is where the risk sits: a reviewer who finds #25 can
say "derived bytes hashed, already owned"; a reviewer who finds #23/#24 can say "pin the bytes that
run, already owned". Both are true and neither is this rule: #25's reference is an authored oracle for
one fixture, #23/#24's is a doctrine about which file to pin. R68-C2's identity arm is the stronger
statement — the transform is provably lossless because its output equals the *original's own pin*, so
`identity_ok` is not an agreement between two measurements but an equality with the carrier.

---

## 3. Commands run (verbatim, in scan order)

```text
ls -d /home/vgpnk/Projects/shokunin/*-shokunin/
ls /home/vgpnk/Projects/shokunin/merge ; ls /home/vgpnk/Projects/shokunin/considerthese
for L in *-shokunin; do ls "$L" ; done
grep -ril --include='*' -e 'upx' -e 'packed-executable' -e 'packed_executable' … (discarded: binary false positives)
grep -rilE 'upx|packed[ -]?elf|decompress' --include='*.py' --include='*.md' --include='*.sh' --include='*.mjs' --include='*.json' .
grep -rinE '\bupx\b' --include='*.py' --include='*.md' --include='*.sh' --include='*.mjs' --include='*.json' --include='*.txt' .
grep -rilnE 'conformance' --include='*.py' --include='*.md' .
grep -rilnE '\bcensus\b' --include='*.py' --include='*.md' .
ls souji-shokunin/tools ; find souji-shokunin/census -maxdepth 2 ; cat souji-shokunin/census/round-1/seat-12.json
ls kama-shokunin/tools ; find kama-shokunin/registry -maxdepth 2
sed -n '1,40p' kama-shokunin/tools/{gate-registry-check,capability-repertoire-audit,manifest-crosscheck,census-waiver-boundary,instrument-agreement}.py
grep -n 'gate-registry-check' kama-shokunin/SKILL.md
sed -n '1,22p' mori-shokunin/tools/{mori-gate-registry,mori-register-check,mori-entry-claims-check}.py
sed -n '1,26p' tameshi-shokunin/tools/registry-check.py
sed -n '1,20p' tsukuroi-shokunin/tools/check-registry-coverage.py
sed -n '1,24p' souji-shokunin/tools/souji-registry-agreement.py
sed -n '1,30p' revenger-shokunin/corpus/self_assessment_check.py
sed -n '1,45p' kotoba-shokunin/verifiers/check_gate_registry.py
sed -n '40,48p;60,70p' kotoba-shokunin/verifiers/check_substrate_pins.py
grep -rniE 'round-?trip|byte-identical|restores the (original|pinned)|sha256 (equals|matches) the pin' --include='*.md' --include='*.py' */corpus/knowledge */tools */SKILL.md
grep -rlnE 'readelf|objdump|binwalk|unblob|e_machine|PT_LOAD|section header' --include='*.py' --include='*.sh' --include='*.mjs' */tools */scripts */corpus/*.py */verifiers
grep -rn -iE '\bupx\b' */SKILL.md */corpus/QUALITY.md
grep -rn -iE 'registry.*(unregistered|conformance)|unregistered' */corpus/QUALITY.md
grep -rn -iE 'extra(ct|ction).*(sha256|digest|identical)|sha256.*(extract|unpack)' */corpus/QUALITY.md
grep -rn -iE 'registry|upx|packed' */considerthese/*.md
sed -n '24,34p' chousa-shokunin/considerthese/2026-10-25.md
sed -n '1,45p' revenger-shokunin/corpus/knowledge/{round-64-firmware-region-byte-evidence,2026-10-12-rea-readiness-checklist}.md
sed -n '324,335p' revenger-shokunin/corpus/knowledge/round-73-re-resource-atlas.md
grep -n 'upx\|packed' revenger-shokunin/SKILL.md
command -v upx && upx --version ; command -v binwalk unblob
# kaidoku side (read-only)
git -C …/kaidoku-shokunin cat-file -e <base>^{commit} ; cat-file -e <freeze>^{commit}
python3 tools/round-68/registry-conformance.py --root … --rev <base> --json-out $S/base.json   (exit 1)
python3 $S/poprule.py <base> <freeze>
sed -n '1,60p' tools/round-68/registry-conformance.py ; sed -n '1,50p' tools/round-68/packed-elf.py
grep -n 'REGISTERED_CASES' -A 20 tools/round-68/registry-conformance.py
```

## 4. What this scan did not do

- No sibling tool was executed; every sibling statement above is a read of its text (`observation` of
  what it says, not of what it prints).
- No sibling counter's green was re-derived. Where a sibling's history is cited (#2, #13) it is the
  sibling's own recorded numbers.
- `registry_rows` (77) and the R68-C2 arms were not re-derived here; the base census re-run in §2 is
  the only measurement of my own lane, and it reproduces `mismatches 2`, `unregistered` = the two
  round-67 paths, `scope_size 69`, `registry_rows 73` at the base revision.
- No claim, predicate, atom, or route was judged, admitted, edited, or integrated.
