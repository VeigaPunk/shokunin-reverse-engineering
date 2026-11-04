#!/usr/bin/env python3
"""Round-72 wave-1 spec generator (lane kaidoku, round 72).

Writes .ufo/waves/round-72/r72-w1-spec.json for the v1 policy band 8-16.
Sixteen seats: 5 executor, 2 reviewer, 2 mutation-tester, 1 critic, 1 sentinel,
1 scout, 1 connector, 3 scribe. Attack roles (reviewer/critic/mutation-tester)
= 5 of 16 = 31%.
"""

import json
import os

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SCRATCH = "/fast/scratch/hyaku/kaidoku-r72"
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
Scratch: create ONE dir `{SCRATCH}/<your-seat-name>/` (mkdir -p), pass it explicitly,
and delete it with `trap 'rm -rf -- \"$S\"' EXIT` (or a finally:) before you yield;
receipts first copied under {LANE}/.ufo/waves/round-72/w1/<your-seat-name>/.
Never run `git`/`jj` writes, never commit, push, stash or check out anywhere; read-only
git (`log`, `show`, `diff`, `status`, `ls-files`) is fine. Never touch
/home/vgpnk/Projects/shokunin/.ufo/state/, .ufo/watchdog.log, MANIFEST.json, templates/,
scripts/, or another lane. Never message agent://all.
Tooling authorization (operator 2026-10-19): you may install or upgrade tools that help
the task; read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety
gate, record tool/version/channel/reason in your report). PACMAN IS PAUSED host-wide:
no pacman transaction of any kind; use uv tool / npx / an official binary in ~/.local/bin.
Every `Report:` trailer path a validator renders is relative to {LANE} \u2014 write it at
{LANE}/<that path>. Your final answer is a short JSON: files_changed, behavior, evidence,
risks.
"""

FROZEN = f"""
## Frozen state
base `56241b1c8baff95862730c008f1ae5132b03388e` (round-71 lane tip); declaration
`6316c1053f927a1a1cdc3e0960b70acab5f56381` (the six round-72 instruments, the plan
`plans/round-72-claims.md`, the nonce commitment, the census-start receipt); operative
freeze `34fe7aa70b627d92e2d27dbce308d9f5bebda63d` (the first commit adding
.ufo/waves/round-72/claims.json; the round-29 freeze gate audits it CLEAN, findings []),
with four pre-freeze declaration fixes (17d8b5f, 306cbb3, 25ecc71, 1563ea3) whose bytes
are the pinned state.
Claims (frozen sentences in the plan and in .ufo/waves/round-72/claims.json):
R72-C1 coverage (checker-mode children under the allowlist; A11), R72-C2 calibration
(A10 verdict from the checker's JSON; the r71 mutation survivor dies), R72-C3 operability
(the raw-witness capsule audit; a lying summary cannot pass).
Instruments (all `python3 -I -B`, all committed at the declaration):
 tools/round-72/packed-elf.py, tools/round-72/seam-probe.py,
 tools/round-72/mutation-check.py, tools/round-72/capsule-audit.py,
 tools/round-72/capsule_audit.py, tools/round-72/controls.py.
Receipts: .ufo/waves/round-72/l1/pre/ (route receipt, nonce commitment, base receipts,
controls) and .ufo/waves/round-72/l1/scores/ (landing).
REA 6.5.0 package root: /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
(package.json sha256 a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c).
Pinned packer: /usr/bin/upx (upx 5.2.0, sha256 cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969);
make your own scratch copy for --expect-upx.
"""

ITEMS = [
    ("ExecC1", "executor", """
Independently re-derive R72-C1's landing-side evidence with YOUR OWN harness; do not run
tools/round-72/seam-probe.py or trust the lane's receipts. Write your own launcher, PATH
shims and env parser.
1. Create a scratch shim dir with `git` and `readelf` sh scripts that record their exact
   `/proc/self/environ` bytes (`cat /proc/self/environ > <abs-record>`) then `exec` the
   real tool by absolute path (resolve it yourself). Put the shim dir first on PATH.
2. Export KAIDOKU_ENV_CANARY and run
   `python3 -I -B tools/round-72/packed-elf.py --root . --rev 6316c1053f927a1a1cdc3e0960b70acab5f56381 --pkg <rea root> --work <scratch> --check-receipt .ufo/waves/round-72/l1/pre/route-at-declaration.json --child-env-log <scratch>/checker.jsonl --nonce-commitment 2532bd5bd8bbf48b5576821b29f35d90b55ab136a9e7179eff989cf961b84fd5`
   with your shim PATH and canary in the caller environment.
3. Independently parse: the shim records (NUL-split KEY=VALUE) for both classes, the
   checker's JSON `checker_child_env` and `clauses`, and the checker rc.
4. Report exact key sets per class, canary presence, HOME/TMPDIR containment under the
   checker's --work, and the child census; state whether every checker-mode child ran
   under the four-key allowlist. If any record shows an extra key, a canary or an
   out-of-root HOME/TMPDIR, say so plainly.
Write receipts + `{lane}/.ufo/waves/round-72/w1/ExecC1/` and a short ExecC1.md.
"""),
    ("ExecC1Base", "executor", """
Independently measure R72-C1's BEFORE state with your own harness; do not run the lane's
probe. Reproduce the round-71 defect directly:
1. Same shim method as ExecC1 (git + readelf shims dumping /proc/self/environ, shim dir
   first on PATH), caller environment carrying KAIDOKU_ENV_CANARY and a TMPDIR outside
   the work root.
2. Run the round-71 checker:
   `python3 -I -B tools/round-71/packed-elf.py --root . --rev b827a8b5d54f2885ec9be7786389f356c59226ce --pkg <rea root> --work <scratch> --check-receipt .ufo/waves/round-71/w1/ExecC1/c1-route.json --nonce-commitment 20256a954f2613bef25019a6b8c260883cb5f852a624e3af7a5335005326822e`
   under the shim PATH.
3. Parse each shim record: key set, canary presence, HOME/TMPDIR. This is the inherited
   caller environment; report it verbatim (key list truncated to 20 keys + count).
4. Also run the round-72 checker with the same receipt and show it rejects for the
   producer-binding clause (not as evidence for C1; label it clearly).
Write receipts + `{lane}/.ufo/waves/round-72/w1/ExecC1Base/` and ExecC1Base.md.
"""),
    ("ExecC2", "executor", """
Independently re-derive R72-C2. Do not trust the lane's receipts; run the frozen battery
yourself and build your own mutant copies.
1. `python3 -I -B tools/round-72/mutation-check.py --root . --rev b827a8b5d54f2885ec9be7786389f356c59226ce --tool tools/round-71/seam-probe.py --patch-set r71 --work <scratch> --json-out <receipt>`:
   confirm survivor_count 1, survivors ["A10_binding_force_true"].
2. `python3 -I -B tools/round-72/mutation-check.py --root . --rev 6316c1053f927a1a1cdc3e0960b70acab5f56381 --tool tools/round-72/seam-probe.py --patch-set r72 --work <scratch> --json-out <receipt>`:
   confirm killed, failed names a10-binding-from-checker, pristine green.
3. Independently apply the patch yourself to a scratch copy of the round-72 probe
   (`binding_ok = clauses.get("run_binding") is True and present` -> `binding_ok = True`),
   run `--selftest`, and record the failing case list. Then restore and re-run.
4. Read the landing probe receipt .ufo/waves/round-72/l1/scores/c1-at-landing.json (when
   present) and check A10's `genuine_verdict` and the wrong-nonce/broken-binding clause
   readings. If the landing receipt is absent, say so; do not invent it.
Write receipts + `{lane}/.ufo/waves/round-72/w1/ExecC2/` and ExecC2.md.
"""),
    ("ExecC3", "executor", """
Independently re-derive R72-C3 with your own cutter and your own audit calls; do not
import tools/round-72/capsule_audit.py for your own derivation (you may compare against it).
1. Read .ufo/waves/round-71/l1/scores/c1-env-at-landing.jsonl (46 records) and
   c1-env-audit.json. Re-derive per-record key sets, canary presence, HOME/TMPDIR
   containment and the child census yourself; compare with the summary.
2. Build the seven tampered capsules yourself (digest, record count, extra key, canary
   key, HOME escape, TMPDIR escape, child-class change) under your scratch; keep the
   genuine summary as the claim.
3. Run `python3 -I -B tools/round-72/capsule-audit.py --capsule <shape> --audit
   .ufo/waves/round-71/l1/scores/c1-env-audit.json` on each; record rc, failures and
   whether the declared clause is named. Also run the genuine capsule.
4. Run the two receipt readers on a lying receipt you build from the round-71 route
   receipt (exec1 route receipt at .ufo/waves/round-71/w1/ExecC1/c1-route.json,
   `child_env_observed.log` pointed at your polluted capsule): the round-71 checker
   (rev b827a8b5..., commitment 20256a95...) must accept; the round-72 checker on the
   round-72 route receipt with its log pointed at a polluted copy of its own capsule must
   reject naming receipt_capsule. Use --capsule explicitly.
Write receipts + `{lane}/.ufo/waves/round-72/w1/ExecC3/` and ExecC3.md.
"""),
    ("ExecSweep", "executor", """
Standing duties + the instrument sweep. Record every command and its exit code in
`{lane}/.ufo/waves/round-72/w1/ExecSweep/`:
1. Sources census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin kaidoku` (exit 0 required; paste warnings count).
2. Registry census: `python3 -I -B tools/round-71/registry-census.py --root . --rev
   56241b1c8baff95862730c008f1ae5132b03388e --generate --out <scratch>/registry.json`;
   report rows/nonconformant/duplicates.
3. Run `--selftest` for all six round-72 instruments and for tools/round-71/registry-census.py;
   record cases/failures per tool.
4. no-/tmp scan of tools/round-72/*.py: list every literal "/tmp" and judge each (a
   hardcoded scratch root is a routed defect; a documented non-fallback note is not).
5. Receipt audit: `python3 -I -B tools/round-70/packed-elf.py --check-receipt
   .ufo/waves/round-72/l1/pre/route-at-declaration.json --root . --rev
   6316c1053f927a1a1cdc3e0960b70acab5f56381` — report rc and whether it accepts the
   round-72 receipt (it should reject on the producer binding; that is expected, label it).
6. `git -C {lane} status --porcelain` (read-only) at your start; report nonempty unexpected
   paths. Do not modify them.
Write ExecSweep.md with a table of command/rc/verdict.
"""),
    ("ReviewerGates", "reviewer", """
Clause-by-clause review of the six round-72 instruments against the frozen predicates in
`plans/round-72-claims.md` and `.ufo/waves/round-72/claims.json` (when present). Name every
defect with file:line.
1. Is each predicate the same sentence in the plan, in the container's `claims[]`, and in
   the instrument's own counter? Quote all three.
2. Can any arm go green on a world where the claimed work is absent? Walk A11's condition
   list, `binding_verdict`, `capsule_audit.audit` clause by clause; construct at least one
   fixture per green path that should be red.
3. Does `--check-receipt`'s capsule clause fail closed (a named capsule that is absent,
   unreadable, or whose summary carries no digest)? State the exact behaviour code.
4. Does `controls.py` really skip the claimed work in each arm (read the arm's commands)?
5. Check the freeze order: declaration commit precedes the pre receipts and the container;
   instruments are pinned by sha256 in the container; every post-freeze edit would need an
   `instrument_supersessions` entry carrying the replacement sha (the round-71 container's
   gap) — state whether the round-72 container has it.
Write ReviewerGates.md with findings RG72-1.. and their evidence commands.
"""),
    ("ReviewerRepairs", "reviewer", """
Verify the carried repairs and record shape; name defects precisely.
1. The round-71 routed defect 1 (report role count): confirm the round-72 wave's spec role
   census from your own count of .ufo/waves/round-72/r72-w1-spec.json items (name, role)
   and say what the report must state.
2. Routed defect 2 (`c2-do-nothing` citation): confirm the committed pre file's real
   values and which receipt the next round must cite.
3. Routed defect 3 (container pins vs supersession): read .ufo/waves/round-71/claims.json
   `instrument_supersessions`; confirm the missing replacement sha and state the exact
   shape the round-72 container must use.
4. Routed defect 4 (S274 column contract): read corpus/SOURCES.md S274 row; confirm where
   the rejection reason sits now and what a conformant row requires (CORPUS.md / the
   census script's schema). Do not edit.
5. SHONEN: read SHONEN.md and say which boxes a named non-author verifier can close this
   round, with the evidence pointer each needs.
Write ReviewerRepairs.md.
"""),
    ("CriticClaims", "critic", """
Falsify the three claims. Your job is to find the world where each counter is green but
the claimed property false. Use your own fixtures under your scratch; never edit the lane.
Attack at least these:
1. R72-C1: build a fake "checker" wrapper that records a clean checker_child_env JSON and
   an allowlisted shim record while its real child still inherits the caller env (e.g. a
   script that writes the log then runs a child with os.environ). Does A11 detect it? If
   not, A11 measures the wrapper, not the route — is the claim's predicate exposed to that?
2. R72-C2: can the round-72 probe's A10 go green while the checker's clauses are absent or
   self-contradictory (clauses true but `met false`)? Test the fail-closed path.
3. R72-C3: can the audit accept a capsule whose summary omits `log_sha256` (a
   not-evaluated clause) and whose records were rewritten consistently (a wholly forged
   clean capsule)? State the limit this exposes and whether the claim as frozen is
   falsified.
4. Check the plan's denominator arithmetic against the committed receipts.
Write CriticClaims.md with each attack, the exact command, the observed result, and a
verdict per claim (intact / falsified-with-repro).
"""),
    ("MutProbe", "mutation-tester", """
New mutants on the round-72 seam probe. Write them as scratch copies + patches under your
scratch, never edit the lane.
Mutate at least: (a) `A11`'s `observed_ok` (`and all(name in children ...)` dropped);
(b) A11's shim `keys_exact` clause (`and s["keys_exact"]` dropped); (c) A11's canary clause;
(d) A11's rc requirement (`res["rc"] == 0` dropped); (e) `binding_verdict`'s `present` guard
(dropped); (f) `binding_verdict`'s `clauses.get("run_binding") is True and present` ->
`is not None`.
For each: apply to a scratch copy, run `--selftest`, record rc/failed cases; restore by
re-reading the committed blob. A mutant that survives the selftest is a survivor — name it
and say which case should bind it. Also score the same six against the round-71 probe
(selftest-only) to show the before state.
Write MutProbe.md + per-mutant patches and a results.json.
"""),
    ("MutReaders", "mutation-tester", """
New mutants on the round-72 route checker and the capsule audit.
Mutate at least: (a) `git_blob_sha256`'s `env=env` -> `env=None`; (b) the readelf call's
`env=cenv` -> dropped; (c) `check_receipt`'s capsule auto-resolution removed; (d)
`capsule_audit`'s canary clause (`and want.get("canary_present") is not True` dropped);
(e) `capsule_audit`'s `under()` -> string prefix; (f) `capsule_audit`'s `records` clause
dropped; (g) `nonce_verdict`'s `binding_ok` -> `receipt.get("run_binding") is not None`.
For each, apply to a scratch copy, run the tool's `--selftest` and a behavioural fixture of
your own (e.g. an allowlisted env record, an escaped HOME), record rc/failures, and
restore exact bytes (`sha256sum` before/after). A survivor is named with the case that
should bind it. Note especially whether (a) and (b) are detectable by any current test —
if not, say so; they are behavioural and may need a new selftest case.
Write MutReaders.md + results.json + patches.
"""),
    ("SentinelScope", "sentinel", """
Adversarial security review of the round-72 instruments and this wave's evidence. Read-only.
1. Shims: the A11/ExecC1 method execs `git`/`readelf` resolved from PATH and writes into
   scratch. Can a hostile PATH or a symlinked shim exfiltrate or execute unintended bytes?
   Is the recorded environ ever used as a write destination (corpus QUALITY 120)?
2. Capsule audit: can a receipt-named capsule path (`child_env_observed.log`) point outside
   the lane (path traversal, absolute host path, symlink) and make the checker read outside?
   Test read-only paths and report the exact behaviour.
3. `--work`/mkdtemp usage: every mkdtemp must honour the caller's dir/TMPDIR; find any
   hardcoded /tmp or world-writable scratch.
4. Canary handling: the canary value is a fixed string; can it appear in committed files?
   grep the lane.
5. Cleanup: does each new instrument remove its scratch on failure paths (Sentinel SS-4
   from round 71)? Name any path that leaks.
Write SentinelScope.md with SS72-n findings, each with a repro command and severity
(blocking / advisory / fixed-in-round).
"""),
    ("ScoutSource", "scout", """
Per-surface reconnaissance + the sourced claim's row.
1. Open https://man7.org/linux/man-pages/man5/proc.5.html (one live fetch, HTTP 200): save
   the page bytes under `{lane}/.ufo/waves/round-72/w1/ScoutSource/`, record sha256, and
   locate the `/proc/pid/environ` paragraph. Quote it verbatim (<= 25 whitespace-separated
   words for the row) and give the byte offset/line of the quote in your snapshot.
2. Verify the row does not duplicate an existing URL: `grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}'
   corpus/SOURCES.md` and each row's source URL; report the next free id and any duplicate
   (0-3 leading spaces, the census parser's tolerance — prove the guard on a scratch
   fixture with an indented row).
3. Reconnaissance: does any committed lane instrument read /proc/self/environ or record
   child environments anywhere else? `grep -rn 'environ' tools/ corpus/` and report every
   hit with file:line and what it measures.
4. Report whether the quote grounds measurement at the exec boundary (initial environment,
   NUL-separated name=value) and its limit (it says nothing about later modifications).
Write ScoutSource.md + snapshot + `sources-row.md` holding the exact 11-cell registry row
in CORPUS.md schema (id, source, kind, tier, scope, anchor, teaches, status=mined, opened,
recheck, used-by), with no literal or escaped pipe inside any cell.
"""),
    ("ConnectorCross", "connector", """
Sibling-overlap scan (read-only) + cross-source pattern.
1. Read /home/vgpnk/Projects/shokunin/shonin.conf (or shokunin.conf) and each sibling
   lane's PROVINCE.md `## Frontier`/`## Core` headings (read-only) for the surfaces
   "child environment", "checker", "capsule", "receipt audit". Name any sibling that
   claims the same surface; the lane must report contested scope, not absorb it.
2. Read /home/vgpnk/Projects/shokunin/PROTOCOL.md's claim/closure rules that touch
   "counter", "predicate", "seal" and check the three round-72 predicates against them;
   report any rule the predicates do not satisfy.
3. Cross-source pattern in this lane: compare the round-71 A8 (route children observed),
   A10 (binding from receipt fields) and the round-72 A10/A11 (from the checker); state
   the general rule the round establishes and whether any earlier instrument violates it.
4. Look for an unclaimed adjacency produced by the new capsule reader (e.g. a shell or
   Python artifact that also writes a JSONL witness); report it as a pointer, never absorb.
Write ConnectorCross.md.
"""),
    ("ScribeKnowledge", "scribe", """
Draft the round's knowledge entry at
`{lane}/.ufo/waves/round-72/w1/ScribeKnowledge/2026-11-04-r72-checker-env-capsule.md`
(the L1 lands it at corpus/knowledge/). Content:
- Title + scope: the checker-mode child environment class and the raw-witness capsule
  audit; the route and instruments it covers; what it does NOT claim (other packers,
  other OSes, cryptographic authenticity).
- Decision table v1: which clause catches which tampered capsule shape (7 rows), with the
  failure name each produces; a second table: which probe arm binds which property
  (A10 clause source, A11 shims/log, A8 route log).
- Limits: dead scratch paths in receipts are provenance pointers not evidence; the shim
  measures the exec boundary only; a summary without a digest makes the digest clause
  not-evaluated; the canary is a fixed string.
- Provenance trio as line-start lines: `source:` (the SOURCES id ScoutSource assigns,
  cite as S276 unless ScoutSource reports a different id), `verified-at:`, `recheck:`.
- Every claim cites a file:line or a receipt path in the lane.
Write the entry + ScribeKnowledge.md. Do not edit corpus/ yourself; the L1 integrates.
"""),
    ("ScribeLesson", "scribe", """
Draft `{lane}/.ufo/waves/round-72/w1/ScribeLesson/round-72.md` (the L1 lands it at
corpus/lessons/round-72.md). Sections:
- Header: author (L1 KaidokuR72), round, base, declaration, freeze (read
  .ufo/waves/round-72/claims.json when present; if absent say so), report path.
- `## Mistakes`: at least one mistake from this round or an earlier one with class,
  evidence pointer, captured-by (the criterion or rule that should have caught it, or
  `none`), fix. Use the round-71 routed gap you can verify from the repo: every route
  child was recorded but no checker-mode child was, while the docstring said "every
  child"; and the mutation survivor i was reported but not bound to a selftest case.
  Show each as a row; the fix must be a thing that can fail (point at the r72 case).
- `## Gate`: the SOURCES row (URL, access date, <=25-word located quote, snapshot digest
  from ScoutSource when available; if the scout has not written yet, leave the exact
  placeholder `[L1 — filled by the non-author closure.]`).
- `## What the wave found`: leave a placeholder list the L1 fills from the seats.
Write the draft + ScribeLesson.md.
"""),
    ("ScribeRecord", "scribe", """
Draft the record text the L1 will land (write under
`{lane}/.ufo/waves/round-72/w1/ScribeRecord/`): three fragments, each ready to paste.
1. `scorecard-round.md`: a round-72 section in SCORECARD.md style (base/declaration/
   freeze/landing lines with the hashes you can read; the three claim rows with axis,
   type, predicate pointer, before→after, verdict placeholder `[L1]`; capability rows
   for the three acquisitions; the `planned (next steered round only)` list from the
   round-72 plan's open queue).
2. `province-core.md`: a `## Round-72 additions to Core` section + a one-paragraph
   frontier note, naming exactly what moves Frontier → Core (checker-mode child
   environments; the receipt-bound capsule audit) and what stays Frontier.
3. `quality-rows.md`: 3-4 new QUALITY.md rows in the file's own voice (bold title,
   normative sentence, Evidence pointer), each tied to a defect the round-72 instruments
   close (a capture claim names the mode; a verdict read from the producer's fields;
   a summary is not the witness; a not-evaluated clause is recorded, not green).
Read the last 20 QUALITY rows, the last two SCORECARD round sections and PROVINCE's
round-71 section first; match their voice and citation style. Write the three fragments +
ScribeRecord.md. Do not edit the real files.
"""),
]


def build():
    items = []
    for name, role, body in ITEMS:
        prompt = (GODSPEED + COMMON + FROZEN
                  + "\n## Your assignment\n" + body.replace("{lane}", LANE)
                  + "\n\nWrite your `Report:` inside " + f"{LANE}/.ufo/waves/round-72/w1/{name}/"
                  + " (absolute). Never write outside the lane.")
        items.append({"name": name, "role": role, "prompt": prompt})
    spec = {
        "wave": "r72-w1",
        "milestone": ("r72-w1 build+attack: three frozen claims verified and attacked, six "
                      "instruments reviewed clause-by-clause, new probe/reader mutants, counter "
                      "false-green probes, security audit, sourced row, sibling scan, knowledge "
                      "and lesson drafts."),
        "reportDir": ".ufo/waves/round-72/w1",
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
    out = os.path.join(LANE, ".ufo/waves/round-72/r72-w1-spec.json")
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
