#!/usr/bin/env python3
"""Round-73 wave-1 spec generator (lane kaidoku, round 73).

Writes .ufo/waves/round-73/r73-w1-spec.json for the v1 policy band 8-16.
Sixteen seats: 5 executor, 3 scribe, 2 reviewer, 2 mutation-tester, 1 critic,
1 sentinel, 1 scout, 1 connector. Attack roles (reviewer/critic/mutation-tester)
= 5 of 16 = 31%.
"""

import json
import os

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SCRATCH = "/fast/scratch/hyaku/kaidoku-r73"
DECL = "da6c17c1eb8dec0b780e276c7f1cb8d9b4fa4d4b"
BASE = "05bf065684e52d72ea25aad95f7acb71fcd7874c"
GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim \u2014 let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

COMMON = f"""
## Bounds (read first)
Lane repo: {LANE}. Every path you write is absolute under that lane; a write anywhere
else is a defect (never write the fleet root, a sibling lane, or /tmp). Work from
{LANE}; seat tools start at the fleet root, so relative paths are wrong.
Scratch: create ONE dir `{SCRATCH}/<your-seat-name>/` (mkdir -p), pass it explicitly
(TMPDIR=... and any --work), and delete it with `trap 'rm -rf -- "$S"' EXIT` (or a
finally:) before you yield; receipts first copied under
{LANE}/.ufo/waves/round-73/w1/<your-seat-name>/.
Never run `git`/`jj` writes, never commit, push, stash or check out anywhere; read-only
git (`log`, `show`, `diff`, `status`, `ls-files`, `rev-parse`) is fine. Never touch
/home/vgpnk/Projects/shokunin/.ufo/state/, .ufo/watchdog.log, MANIFEST.json, templates/,
scripts/, or another lane. Never message agent://all.
Security (round-72 incident, QUALITY row 128): never write a raw environment dump into
the lane. A probe that must show an environment writes the KEY NAMES and the canary
presence only; values stay out of every committed file.
Tooling authorization (operator 2026-10-19): you may install or upgrade tools that help
the task; read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety
gate, record tool/version/channel/reason in your report). PACMAN IS PAUSED host-wide:
no pacman transaction of any kind; use uv tool / npx / an official binary in ~/.local/bin.
Every `Report:` trailer path a validator renders is relative to {LANE} - write it at
{LANE}/<that path>. Your final answer is a short JSON: files_changed, behavior, evidence,
risks.
"""

FROZEN = f"""
## Frozen state
base `{BASE}` (round-72 lane tip); declaration `{DECL}` (the six round-73 instruments +
plans/round-73-claims.md + the census-start receipt; committed BEFORE any claim data).
Claims (frozen sentences in plans/round-73-claims.md and .ufo/waves/round-73/claims.json):
R73-C1 coverage  -- the probe gains a producer-independent kernel witness (A12): genuine
  kernel samples = HOME/LANG/PATH/TMPDIR, canary absent; a forged run's child dumps read
  clean while its kernel samples read dirty; the probe reports 12 of 12 arms.
R73-C2 calibration -- the record audit re-derives 7 atoms from the round-72 non-author
  spot-check's routed defects: 0 mismatches at landing, 6 at base.
R73-C3 operability -- the three reader-seam survivors (git-reader env, checker-readelf
  env, implicit capsule) are killed by named selftest cases: mutation battery patch set
  r73 survivor_count 0 at landing, 3 at base (patch set r73base on the r72 route).
Instruments (all `python3 -I -B`, committed at the declaration):
 tools/round-73/packed-elf.py, tools/round-73/seam-probe.py,
 tools/round-73/mutation-check.py, tools/round-73/record-audit.py,
 tools/round-73/controls.py, tools/round-73/capsule_audit.py.
Route receipt (produced by tools/round-73/packed-elf.py at the declaration):
 .ufo/waves/round-73/pre/route-at-declaration.json
Commitment (sha256 of the nonce; the nonce plaintext is scratch-only):
 .ufo/waves/round-73/l1/nonce-commitment.txt
REA 6.5.0 package root: /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
Pinned packer: /usr/bin/upx (upx 5.2.0, sha256
 cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969); make your own
 scratch copy for --expect-upx (it must NOT be the module default /usr/bin/upx).
"""

ITEMS = [
    ("ExecC1Verify", "executor", """
Independently re-derive R73-C1's after state with YOUR OWN harness. Do not call
tools/round-73/seam-probe.py's A12; do not trust the lane's receipts.
1. Write your own observer: a `/proc` poller that finds a process by argv and reads
   `/proc/<pid>/environ` (key census only), plus your own perl shims for git and readelf
   that dump nothing but sleep 0.4 s and exec the real tool by absolute path.
2. Genuine world: path-first shim dir + an exported KAIDOKU_ENV_CANARY, then run
   `python3 -I -B tools/round-73/packed-elf.py --root . --rev <decl> --pkg <rea root>
    --work <scratch> --check-receipt .ufo/waves/round-73/pre/route-at-declaration.json
    --nonce-commitment $(cat .ufo/waves/round-73/l1/nonce-commitment.txt)`
   and read YOUR poller's samples: exact key sets per class, canary, HOME/TMPDIR.
3. Forged world: a lying shim that writes a fabricated four-key dump, run by a producer
   that inherits the caller environment (a 3-line python fixture calling the shim with
   env=None). Your poller must see the dirty env while the dump reads clean.
4. State plainly whether the kernel record can be forged by the child, and what a
   wrapper WOULD have to do to defeat it (/proc is the kernel's record; a child cannot
   rewrite it, only a different process can be observed - say which pid you sampled).
Write receipts + `{lane}/.ufo/waves/round-73/w1/ExecC1Verify/` and ExecC1Verify.md.
"""),
    ("ExecC1Base", "executor", """
Measure R73-C1's BEFORE state. The round-72 probe has eleven arms and no kernel channel.
1. `grep -c '/proc/%d/environ' tools/round-72/seam-probe.py tools/round-73/seam-probe.py`
   and `grep -n 'def .*kernel\\|proc_' tools/round-72/seam-probe.py` - record exactly what
   the round-72 probe can and cannot see.
2. Load tools/round-72/seam-probe.py as a module (importlib) and feed its `a11_verdict`
   a world whose shim dumps are a clean four-key fabrication while the true child env was
   the caller's: does A11 pass? Show the exact call and result. (This is the class
   boundary the round-72 entry recorded; the point is that a producer-side witness cannot
   tell a dump from the truth.)
3. Run the round-72 probe end to end at the declaration rev against the round-73 route
   (it has 11 arms) and confirm it reports `target 11` and no A12.
4. Run `python3 -I -B tools/round-73/seam-probe.py --selftest` and record its case count.
Write receipts + `{lane}/.ufo/waves/round-73/w1/ExecC1Base/` and ExecC1Base.md.
"""),
    ("ExecC2", "executor", """
Re-derive R73-C2 independently. Do not trust tools/round-73/record-audit.py's verdicts.
1. Read corpus/lessons/round-72-verifier-spotcheck.md section 6 (the routed defects) and
   write down, in your own words, the mechanical fact each defect asserts.
2. For each of the 7 atoms in tools/round-73/record-audit.py, re-derive it YOURSELF from
   committed bytes at base `{base}` and at the declaration `{decl}` (git show, jq/sha256sum):
   the C2 target sha, the pin, the disclosures block, the lying receipt's rc, the
   provenance trio position, the lowest-axis label, the before receipts.
3. Run `python3 -I -B tools/round-73/record-audit.py --root . --rev {decl} --json-out ...`
   and compare its rows with yours. Report every disagreement with the exact bytes.
4. Say whether any atom can pass without the defect being fixed (a false green), and
   whether any atom fails for a reason the routed defect does not name.
Write receipts + `{lane}/.ufo/waves/round-73/w1/ExecC2/` and ExecC2.md.
"""),
    ("ExecC3", "executor", """
Re-derive R73-C3 independently.
1. From the committed patches .ufo/waves/round-72/w1/MutReaders/{a,b,c}.patch, apply each
   defect to a scratch copy of `tools/round-72/packed-elf.py` (base `{base}`) and to a
   scratch copy of `tools/round-73/packed-elf.py` (declaration `{decl}`): your own text
   surgery, not the battery's patch table.
2. Run `--selftest` on pristine and on each of the six mutants; record rc, case count and
   the failed case list.
3. Confirm each round-73 mutant fails the DECLARED case name and that the failure is
   caused by the mutated seam (not by an import error or a missing fixture).
4. Run the frozen battery both ways:
   `--patch-set r73 --tool tools/round-73/packed-elf.py --min-pristine-cases 38`
   and `--patch-set r73base --tool tools/round-72/packed-elf.py`, at `--rev <decl>`;
   report survivor_count for each and whether `--expect-target-sha256` is honoured.
Write receipts + `{lane}/.ufo/waves/round-73/w1/ExecC3/` and ExecC3.md.
"""),
    ("ExecSweep", "executor", """
Run the three claim commands end to end at the declaration `{decl}` and report each rc and
the head of each receipt (no re-interpretation, just the frozen commands):
1. `python3 -I -B tools/round-73/seam-probe.py --root . --rev {decl}
    --tool tools/round-73/packed-elf.py --battery tools/round-73/mutation-check.py
    --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work <scratch>
    --receipt .ufo/waves/round-73/pre/route-at-declaration.json
    --expect-upx <your pinned copy> --nonce-commitment $(cat .ufo/waves/round-73/l1/nonce-commitment.txt)
    --json-out <receipt>` - report arms_passed/target/failed and A12's key observation fields.
2. `python3 -I -B tools/round-73/record-audit.py --root . --rev {decl} --json-out <receipt>`
   - report mismatch_count and the mismatch list.
3. `python3 -I -B tools/round-73/mutation-check.py --root . --rev {decl}
    --tool tools/round-73/packed-elf.py --patch-set r73 --work <scratch>
    --min-pristine-cases 38 --json-out <receipt>` - report survivor_count and each mutant's
   verdict/failed case.
4. Also run the base arms: the probe against `--tool tools/round-72/packed-elf.py`
   (expect 11 of 12, A12 false) and the audit at `{base}` (expect 6 mismatches).
Write receipts + `{lane}/.ufo/waves/round-73/w1/ExecSweep/` and ExecSweep.md.
"""),
    ("MutProbe", "mutation-tester", """
Attack the round-73 PROBE's new code. Mutate `tools/round-73/seam-probe.py` in scratch
copies (never the lane file) and run `--selftest` on each:
 a `a12_verdict`: drop the `forged_detected` conjunct; drop `lie_clean`; drop the genuine
   canary test; drop the `genuine_rc` test; make `forged_detected` accept any sample.
 b `kernel_witness`/`_proc_environ`: return `{}` for an unreadable environ; return the
   first sample only; drop the `canary_present` field.
 c the arm's wiring: swap `genuine`/`forged` in the `a12_verdict` call; skip the forged
   sub-run entirely.
For each mutant report rc, failed cases, and whether the case that should bind it does.
Any survivor is a real coverage gap: name the exact case that must be added.
Write mutant patches + results.json + `{lane}/.ufo/waves/round-73/w1/MutProbe/` and MutProbe.md.
"""),
    ("MutBattery", "mutation-tester", """
Attack the round-73 BATTERY's honesty.
1. Apply each of `PATCH_SETS["r73"]` by hand to a scratch copy of the route and run
   `--selftest`; verify the declared case fails, and verify that a mutant that ALSO
   breaks an unrelated case is reported as `killed_wrong_case`, not `killed`.
2. Delete one of the three new `cases.append` blocks from a scratch copy of the route
   (leave the registry line) and run the selftest: `case-inventory` must fail. Then
   delete the registry line only: `case-inventory` must fail as well. Report both.
3. Attack `EXPECTED_SURVIVORS`: a patch set whose declared expectation is 0 but whose
   patch matches a different site, a patch set applied to the wrong route, and a target
   whose `--expect-target-sha256` is wrong - each must exit non-zero / unevaluable.
4. Report whether `--min-pristine-cases` can be satisfied by a route whose selftest is
   green only because a case was silently dropped (case-inventory should prevent it).
Write receipts + `{lane}/.ufo/waves/round-73/w1/MutBattery/` and MutBattery.md.
"""),
    ("ReviewerClaims", "reviewer", """
Review the three frozen claims in `plans/round-73-claims.md` against the canons:
1. Do-nothing reachability: for each claim, is the target reachable by a move that skips
   the claimed work? (e.g. could C1's 12 of 12 be met with a blind observer; could C3's
   survivor_count 0 be met by deleting a patch rather than adding a case; could C2's 0
   mismatches be met by deleting an atom?)
2. Counter binding: does each counting command read committed bytes, and is the value it
   prints the one the predicate names?
3. Axis naming: is each claim named by the surface it moves, not by the number it
   produces? Is any two claims the same axis? Is the lowest-axis label honest?
4. Kill rules: is any predicate's kill rule unable to fail?
Write findings with file:line pointers + `{lane}/.ufo/waves/round-73/w1/ReviewerClaims/`.
"""),
    ("ReviewerGates", "reviewer", """
Audit the three instruments for FALSE GREENS.
1. `tools/round-73/record-audit.py`: can an atom pass on a record that still carries the
   routed defect? Can the audit pass when a receipt is absent? Does D1 accept the wrong
   token because the correction block is merely present?
2. `tools/round-73/seam-probe.py` A12: can the arm pass when the genuine sub-run's
   children never ran (no samples) or when the forged sub-run's kernel samples are empty?
   Does the forged fixture really inherit the caller environment (read the code)?
3. `tools/round-73/mutation-check.py`: is `survivor_count 0` derivable from the mutant
   rows only, or can a mutant be absent from the rows and not counted?
4. `tools/round-73/controls.py`: do the six arms actually skip the claimed work, and does
   the aggregate read the strict verdict?
Run what you need; report each finding with the exact line and a proposed fix.
Write receipts + `{lane}/.ufo/waves/round-73/w1/ReviewerGates/` and ReviewerGates.md.
"""),
    ("CriticClaims", "critic", """
Falsify the round's three claims.
1. C1: construct the strongest wrapper that still defeats A12 (e.g. a shim that forks a
   child and exits before the poller samples, or a producer that spawns the real tool in a
   clean env while lying about the observed process). Say exactly what A12 cannot see and
   whether the claim's predicate is falsified by it or whether the class boundary moves.
2. C2: find an atom that is satisfied by editing prose rather than fixing the defect; say
   which and whether that makes the calibration claim vacuous.
3. C3: check whether the three cases test the SEAM or merely the patched line; propose a
   case that would pass a wrong implementation.
Report `falsified` / `not falsified` per claim with the receipt.
Write receipts + `{lane}/.ufo/waves/round-73/w1/CriticClaims/` and CriticClaims.md.
"""),
    ("SentinelScope", "sentinel", """
Security review of the round-73 surfaces.
1. A12 reads `/proc/<pid>/environ` of processes the probe itself started: enumerate what
   else it could read, whether the pid selection can be widened (a prefix match on argv),
   and whether a lane-local file can redirect it.
2. The shims are written into scratch and placed first on PATH: can a caller-supplied
   directory, a receipt field or an environment variable change where they are written or
   which real tool they exec?
3. The lying-shim fixture fabricates a dump: does it ever write a raw environment (the
   round-72 credential-capture class)? Verify by grepping the committed receipts for
   long-lived token shapes and for `=`-heavy env dumps.
4. Check the round-73 instruments for writes outside the lane and for reads of operator
   config (~/.omp, ~/.config) beyond what is documented.
Report blocking / non-blocking with file:line.
Write receipts + `{lane}/.ufo/waves/round-73/w1/SentinelScope/` and SentinelScope.md.
"""),
    ("ScoutSource", "scout", """
Source reconnaissance for the round's sourced claim.
1. Fetch https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html (and the index
   https://man7.org/linux/man-pages/dir_section_5.html). Record HTTP status, byte size,
   sha256 and ONE located quote (<=25 words) that grounds "the kernel exposes each
   process's command line" - the mechanism a kernel-side observer uses to find a child.
2. Also check whether man-pages 6.19 splits `proc(5)`: name the page that actually carries
   the `/proc/pid/cmdline` paragraph and its URL.
3. Read corpus/SOURCES.md: report the highest id and whether the candidate URL is already
   present (any S-row). Report the exact next id under CORPUS.md rule 2.
4. Check the round-73 knowledge entry draft target
   `corpus/knowledge/2026-11-04-r73-kernel-witness-record.md`: what must its `source:` row
   cite, and does any existing entry already claim the kernel-witness surface?
Write the fetch evidence + `{lane}/.ufo/waves/round-73/w1/ScoutSource/` and ScoutSource.md.
"""),
    ("ConnectorCross", "connector", """
Sibling-overlap scan for the round-73 surfaces (read-only across the fleet).
1. Search the sibling lanes at /home/vgpnk/Projects/shokunin/*-shokunin for (a) a
   `/proc/<pid>/environ` observer, (b) a record-vs-receipt audit, (c) a mutation battery
   with a named-case kill rule. Use grep over `tools/`, `corpus/`, `SKILL.md`.
2. For any hit, report whether the sibling owns the surface better, whether the round's
   claim should cite it, and whether it is adjacency (report, do not absorb).
3. Report the cross-source rule the round's instruments share with the siblings (one
   sentence) and whether the round mislabels any shared rule as new.
Write findings + `{lane}/.ufo/waves/round-73/w1/ConnectorCross/` and ConnectorCross.md.
"""),
    ("ScribeKnowledge", "scribe", """
Draft the round-73 knowledge entry at
`{lane}/.ufo/waves/round-73/w1/ScribeKnowledge/entry.md` (do NOT write corpus/).
Target path: corpus/knowledge/2026-11-04-r73-kernel-witness-record.md.
Requirements: the provenance trio (`source:`, `verified-at:`, `recheck:`) as line-start
fields in the FIRST TWELVE LINES (QUALITY row 112 binds it; the round-73 audit D5 checks
it). Body: what the kernel witness is, the exact A12 clauses, the forged control and its
result, the limits (what a wrapper can still do: a process the observer never samples, a
namespace, a producer that spawns the real tool elsewhere), and the receipts it cites
(`.ufo/waves/round-73/l1/scores/c1-at-landing.json`). Read the round-72 entry for voice.
Cite the S277 row (proc_pid_cmdline) once it is opened.
Write the draft + ScribeKnowledge.md.
"""),
    ("ScribeLesson", "scribe", """
Draft `corpus/lessons/round-73.md` at
`{lane}/.ufo/waves/round-73/w1/ScribeLesson/lesson.md` (do NOT write corpus/).
Sections: the round narrative (three claims, instruments, what landed), `## Mistakes` (at
least one, in the lane's table shape: class | evidence pointer | captured-by | fix - the
obvious candidate is round 72's A11 measuring only a producer-side witness and calling the
boundary unfalsifiable; find at least one more from this round if you can), `## Gate` (row,
URL, opened date, <=25-word located quote, snapshot sha256 for S277), and the
non-author closure placeholder. Read corpus/lessons/round-72.md for voice and shape.
Write the draft + ScribeLesson.md.
"""),
    ("ScribeRecord", "scribe", """
Draft the record fragments at `{lane}/.ufo/waves/round-73/w1/ScribeRecord/` (do NOT edit
the real files):
1. `scorecard-round.md`: a round-73 section in SCORECARD.md's own voice: base/declaration/
   freeze/landing lines, `**lowest-axis: coverage**` (the audit's D6 atom reads that
   literal), the three claim rows (axis, type, predicate pointer, before->after, verdict
   placeholder `[L1]`), the capabilities rows, the `planned (next steered round only)`
   list, and the round-72 CORRECTION blocks the audit's D1/D3 atoms need
   (`**Correction (round 73 ...` naming both the old `39a2193e...` token and the receipt's
   `602b305d...`).
2. `province-core.md`: `## Round-73 additions to Core` naming exactly what moves Frontier
   -> Core (the kernel-side witness class) and what stays Frontier.
3. `quality-rows.md`: 3-4 new QUALITY.md rows in the file's voice (bold title, normative
   sentence, evidence pointer) tied to the round's defects/lessons.
Read the last 20 QUALITY rows and the round-72 SCORECARD section first; match the voice.
Write the three fragments + ScribeRecord.md.
"""),
]


def build():
    items = []
    for name, role, body in ITEMS:
        prompt = (GODSPEED + COMMON + FROZEN
                  + "\n## Your assignment\n"
                  + body.replace("{lane}", LANE)
                  .replace("{base}", BASE).replace("{decl}", DECL)
                  + "\n\nWrite your `Report:` inside "
                  + f"{LANE}/.ufo/waves/round-73/w1/{name}/"
                  + " (absolute). Never write outside the lane.")
        items.append({"name": name, "role": role, "prompt": prompt})
    spec = {
        "wave": "r73-w1",
        "milestone": ("r73-w1: three frozen claims verified and attacked (kernel "
                      "witness, record audit, reader-seam battery), instruments "
                      "reviewed for false greens, new mutants, security audit, "
                      "sourced row, sibling scan."),
        "reportDir": ".ufo/waves/round-73/w1",
        "context": (COMMON + FROZEN + """
## Wave
One v1 wave, 16 seats: 5 executor, 3 scribe, 2 reviewer, 2 mutation-tester, 1 critic,
1 sentinel, 1 scout, 1 connector. Attack roles (reviewer/critic/mutation-tester) 5/16 =
31%. The L1 holds the planner seat. You are one seat: do your assignment, write only
inside the lane, return a short JSON (files_changed, behavior, evidence, risks), and
delete your scratch dir before you yield.
"""),
        "items": items,
    }
    out = os.path.join(LANE, ".ufo/waves/round-73/r73-w1-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(spec, fh, indent=1)
        fh.write("\n")
    print(out, len(items), "items")
    roles = {}
    for it in items:
        roles[it["role"]] = roles.get(it["role"], 0) + 1
    print(json.dumps(roles, sort_keys=True))


if __name__ == "__main__":
    build()
