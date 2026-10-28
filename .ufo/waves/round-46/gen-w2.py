#!/usr/bin/env python3
"""Generate the round-46 wave-2 spec, validated dispatch and ready file (L1 artifact)."""
import collections
import json
import os
import subprocess
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
WAVE_DIR = os.path.join(ROOT, ".ufo/waves/round-46")
F4 = "0425224756791b414454df28a9abf93dcdf154ce"
A3 = "7bf33e312d75ad09d55df399814e9ae3ef7cee49"
LREG = "781e19ae674225b6be0b5de56ee8574679bac0b6"
GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

"""
AXES = ["coverage", "depth", "calibration"]
MILE = ("Round 46 wave 2: falsify the landed claims — every forgery class, every block-23 row, "
        "every registered instrument and both counters, after data")
REPORT = ".ufo/waves/round-46/w2"
W = REPORT + "/"

CTX = f"""# Target
kaidoku-shokunin round 46, wave 2 = FALSIFICATION of the landed claims, after data. Lane root (absolute): {ROOT}. L1 = KaidokuR46 (integration owner; it holds the canonical section-3 planner seat — the validator rejects `planner` as a swarm role, so bounded planning data-walks ride scout/connector/revenger seats).

# What was landed (attack THIS, not a description of it)
- **Freeze** `{F4}` — `plans/round-46-claims.md` and `tools/round-46/` ({{gate,attest,registry,census}}.py + census.json). The freeze moved three times before any score existed (`3182047` → `50862e4a` → `65678df0` → `{F4}`); the record is `corpus/lessons/round-46.md` M46-3. Whether those moves were justified is fair game.
- **R46-C1** — `SKILL.md` `## Queue-drain craft` rule block 23, marker `<!-- freeze-integrity-table v2 -->`, 13 rows, 9 line-selected citations, a sha256 pin of `tools/round-46/attest.py`. Landing `227d6982`, A1 `87578656`, A2 `6e018068`, A3 `{A3}`. Measured: `.ufo/waves/round-46/l1/scores/c1-at-F4.json`.
- **R46-C2** — the `<!-- instrument-registry v2 -->` section at the end of `SKILL.md`, 38 rows over `tools/round-46/census.json`. Landing `{LREG}`. Measured: `.ufo/waves/round-46/l1/scores/c2-at-F4.json`.
- Both counters claim a **discrimination battery**: every forgery class is built by mutating the landed bytes and must score v1-green / v2-red while the genuine artefact scores green.

# Read first
`{ROOT}/plans/round-46-claims.md` (both predicates clause by clause), then the artefact you attack. Do not re-derive the claims from this prompt.

# Contract (binding on every seat)
- **You are read-only on the lane tree.** Write ONLY inside `{ROOT}/.ufo/waves/round-46/w2/<YourSeatName>/` (create it). Never edit `SKILL.md`, `plans/`, `tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`, or the fleet repo. Never commit, push, stage, stash, or run any mutating git/jj command. Read-only git is fine: `log`, `show`, `diff`, `diff-tree`, `ls-tree`, `cat-file`, `rev-parse`, `status --porcelain`.
- **Frozen means read-only.** Copy `tools/round-46/` to scratch and mutate the copy; never the originals.
- **Fixture repos**: `D=$(mktemp -d -p "$S") && git -C "$D" init -q`, every later call names `-C "$D"`, verify the toplevel before the first commit.
- **Scratch**: `S=/fast/scratch/hyaku/kaidoku-r46/<YourSeatName>`; `export TMPDIR="$S" HYAKU_SCRATCH="$S"`. Remove `$S` before you yield, AFTER copying receipts into your report dir. Never write under `/tmp`.
- **Honest capture beats a pass.** Every receipt carries the exact command, exit code, stdout sha256, UTC time. A check you did not run is not passed.
- **Exit codes are semantic**: 0 met, 1 violation, 2 could-not-evaluate.
- **`Report:` trailer**: every `Report:` path is relative to `{ROOT}` — write it at `{ROOT}/<that path>`.
- **Tooling**: read `/home/vgpnk/.omp/agent/RULES.md` first. All pacman transactions are PAUSED host-wide; use `uv tool`/`npx`/an official binary in `~/.local/bin`. Record any install.
- Never message `agent://all`; never touch a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`, or `.scratch/`.

# The point of this wave
A finding that the landing is fake, the counter is blind, or the record is wrong is the wave's product. Report it with the exact command and the differing value. Do not "fix" a frozen file. Rank what you find: HIGH if it lets a forged artefact pass or the claim score without the work; MEDIUM if the claim text and the code disagree; LOW for wording.
"""


def T(name, agent, task):
    task = task.replace("<ROOT>", ROOT).replace("<F4>", F4).replace("<A3>", A3).replace("<W>", W)
    return {"name": name, "agent": agent, "task": GODSPEED + task}


def c1_forgery(fname, what):
    return T("R46W2C1" + fname, "critic",
             "Attack ONE forgery class of the R46-C1 battery: `%s`. The battery builds it by "
             "mutating rule block 23 of `SKILL.md` at `<A3>`; read `tools/round-46/attest.py` "
             "`m_*` and `run_battery` to see exactly what the mutation changes. Then prove or "
             "refute, with your own fixture repo, that: (a) the mutated artefact really is the "
             "defect class it claims (open both texts and diff them; a no-op mutation is a HIGH "
             "defect and the code counts a no-op as `v2_green += 1`); (b) it scores exit 0 under "
             "`--profile v1`; (c) it scores non-zero under `--profile v2` for the REASON the row "
             "claims, not for an incidental one (name the `failing` string and show it matches "
             "the table row's `v2 arm` cell); (d) the genuine artefact is not harmed by the same "
             "check. Record every command and its exit code. Write `<W>R46W2C1%s/report.md`."
             % (what, fname))


def c2_forgery(fname, what):
    return T("R46W2C2" + fname, "critic",
             "Attack ONE forgery class of the R46-C2 battery: `%s`. The battery mutates the "
             "`<!-- instrument-registry v2 -->` section of `SKILL.md` at `<LREG>`; read "
             "`tools/round-46/registry.py` `m_*` and `run_battery`. Prove or refute with your "
             "own fixture repo that: (a) the mutation really produces that defect and is not a "
             "no-op; (b) it scores exit 0 under `--profile v1`; (c) it scores non-zero under "
             "`--profile v2` for the named reason; (d) the genuine section is unaffected. Also "
             "state whether a forger who knew the check could satisfy it while still writing a "
             "false row. Write `<W>R46W2C2%s/report.md`." % (what, fname))


def block_rows(fname, ids, lines):
    return T("R46W2Block" + fname, "reviewer",
             "Review block 23's rows %s. Read `SKILL.md` `## Queue-drain craft ` block 23 at "
             "`<A3>` and, for each routed id in your set, the defect it claims: the round-45 "
             "lesson `corpus/lessons/round-45.md:%s` and `tools/round-46/gate.py` / `attest.py` / "
             "`registry.py`. For each row answer: (1) is the 'v1 hole' cell a true statement "
             "about the round-45 code (quote the round-45 source line or say 'unsupported'); (2) "
             "does the named 'v2 arm' actually exist in the round-46 code (function name and "
             "line); (3) is the exit cell the exit that arm really produces; (4) does the claim "
             "overstate — does the arm close the whole defect class or only part of it? Give a "
             "verdict per row. Write `<W>R46W2Block%s/report.md`."
             % (ids, lines, fname))


def reg_group(fname, paths):
    rows = "\n".join("- `%s`" % p for p in paths)
    return T("R46W2Reg" + fname, "reviewer",
             "Re-derive the registry rows for these instruments from source and compare with "
             "what `SKILL.md`'s `<!-- instrument-registry v2 -->` section actually says:\n\n%s\n\n"
             "For each: read the tool at `<F4>` (`git -C <ROOT> show <F4>:<path>`), extract its "
             "real exit paths, and compare to the row's `verdict map (exit codes)` cell. Report "
             "`match`, `mismatch` (with the true exit map) or `unsupported` (the row describes a "
             "behaviour the code does not have). Then state whether the purpose cell names the "
             "tool's actual job. The frozen counter checks only presence and the map's shape, so "
             "a false description passes it — that is what you are looking for. Write "
             "`<W>R46W2Reg%s/report.md`." % (rows, fname))


def main():
    census = json.load(open(os.path.join(ROOT, "tools/round-46/census.json")))["paths"]
    tasks = []
    for fn, what in (("Noop", "a mutation that does not change the block"),
                     ("Garbage", "`garbage-rows`"), ("Thin", "`thin-rows`"),
                     ("Lineless", "`lineless-refs`"), ("Header", "`header-substring`"),
                     ("Markers", "`two-markers`"), ("StubPin", "`stub-pin`"),
                     ("SelfRefs", "`self-refs`"), ("RoutedId", "`missing-routed-id`"),
                     ("ArmVocab", "`no-vocab-arm`")):
        tasks.append(c1_forgery(fn, what))
    for fn, what in (("Fenced", "`fenced`"), ("OffSection", "`off-section`"),
                     ("Substring", "`substring-cell`"), ("ProseExit", "`prose-exit`"),
                     ("Comment", "`html-comment`"), ("Shadow", "`first-wins-shadow`"),
                     ("Header", "`no-header`")):
        tasks.append(c2_forgery(fn, what))

    tasks += [
        block_rows("A", "R45-CL2, R45-CL6, R45-CL7, R45-CL9", "90-101, 142-176"),
        block_rows("B", "R45-CL13, R45-CL14, R45-CL15", "142-196"),
        block_rows("C", "R45-CL18, R45-CL19, R45-CL20", "197-223"),
        block_rows("D", "R45-CL22, R45-CL23, R45-CL24", "224-247"),
        T("R46W2Pin", "reviewer",
          "Attack the interpreter pin. Read block 23's `sha256:` token and `attest.py`'s "
          "`SPECS['r46']['pin']` handling. Answer with probes: (a) does the pin bind the bytes at "
          "`--rev` or a string the artefact controls (edit a COPY of attest.py and see what the "
          "copied counter does — never the original); (b) can a block carry the right pin for a "
          "DIFFERENT file (e.g. gate.py's hash) and still pass; (c) what happens when the pinned "
          "path is a directory or absent; (d) is the pin ever compared against the worktree "
          "rather than the revision (it must not be). Write `<W>R46W2Pin/report.md`."),
        T("R46W2CountersRerun", "executor",
          "Re-run both counters exactly as the report will cite them, from a scratch copy of the "
          "instruments extracted at `<F4>`: `attest.py --root <ROOT> --freeze <F4> --rev <F4>` "
          "and `registry.py --root <ROOT> --freeze <F4> --rev <F4>`. Record exit codes, every "
          "receipt field, stdout sha256 and wall time; compare with "
          "`.ufo/waves/round-46/l1/scores/{c1,c2}-at-F4.json` and report any divergence. Then "
          "re-run the four control receipts (`controls/*.json`) from their committed bytes and "
          "say whether each reproduces. Write `<W>R46W2CountersRerun/report.md`."),
        T("R46W2FreezeMoves", "reviewer",
          "The freeze moved three times (`3182047` → `50862e4a` → `65678df0` → `<F4>`). Diff each "
          "step (`git -C <ROOT> diff <a> <b> -- tools/round-46 plans/round-46-claims.md`) and "
          "classify every hunk: a defect repair, a semantic change to the predicate, or a "
          "weakening of a check. Then answer the question the closure will ask: could any of the "
          "three moves have been made IN RESPONSE to data (a score or a seat finding), or do all "
          "three predate the first verdict? Use commit timestamps and the wave-1 seat report "
          "mtimes. Write `<W>R46W2FreezeMoves/report.md`."),
        T("R46W2Sweep", "reviewer",
          "Verify the freeze range claims nothing it does not. From `<F4>` to the lane tip, run "
          "`git -C <ROOT> log --name-status <F4>..<TIP> -- tools/round-46 plans/round-46-claims.md` "
          "and confirm it is empty; then confirm `attest.py`'s sha256 at `<F4>` equals block 23's "
          "pin; then run `tools/round-46/gate.py`'s `freeze_state` over the range and record the "
          "exit. Finally check the round's own commits for a frozen path that slipped in under a "
          "different name. Write `<W>R46W2Sweep/report.md`."),
        T("R46W2CommandA", "executor",
          "Re-run command A (the SCORECARD measurement recipe) at `<A3>` and at `<F4>` and record "
          "the JSON both times. State `rule_blocks`, `citation_resolved_rules`, `depth_score`, "
          "`knowledge_files`, `mapped`, `missing`, `dangling`, `coverage_score`. Then confirm the "
          "claim 'block 23 cites a knowledge entry' by `grep -c repository` on the block only, "
          "and say whether the depth score would fall without that citation (test on a scratch "
          "copy of SKILL.md). Write `<W>R46W2CommandA/report.md`."),
        T("R46W2Fidelity", "reviewer",
          "Re-run both fidelity receipts and judge the v1 port honestly. `attest.py --spec r45 "
          "--profile v1 --no-battery --freeze f762b727 --rev f59565b7` and the same for "
          "`registry.py`; compare each field with round 45's recorded values. Then answer: is the "
          "v1 profile the round-45 clause set, or a weakened imitation? Name every place the port "
          "differs from `tools/round-45/{c1,c2}-counter.py` (read both sources) and say whether "
          "the difference makes the battery easier to pass. Write `<W>R46W2Fidelity/report.md`."),
        T("R46W2Census", "reviewer",
          "Audit the census rule and its result. Read `tools/round-46/census.py`; then (a) "
          "re-derive the 38 paths with an independent grep; (b) list every `tools/round-4[1-6]` "
          "`.py`/`.sh` path that EXISTS at `<F4>` but is not named by any claim file and is "
          "therefore out of scope — is the rule defensible or does it let a claim-carrying "
          "instrument escape; (c) check `named_but_absent` is empty; (d) does the census include "
          "instruments whose claim round never froze them? Write `<W>R46W2Census/report.md`."),
        T("R46W2Sent", "sentinel",
          "Second-pass adversarial review of the landed artefacts, not the tools: can `SKILL.md` "
          "+ `census.json` be made to pass with a hostile repository state? Try: a symlink inside "
          "`tools/round-46/` pointing outside; a census path that is a directory; a row whose "
          "verdict cell uses a Unicode digit or a full-width `=`; a marker inside a fenced block "
          "in another section; 200 rows to slow the parser; a block 23 whose refs point at a file "
          "that is huge. Report each with the exact bytes and whether the counter mis-scores. "
          "Write `<W>R46W2Sent/report.md`."),
        T("R46W2Simpl", "simplifier",
          "YAGNI review of the LANDED artefacts: does block 23 need all 13 rows, and does the "
          "registry need all 38? For each row, ask what a reader loses if it is deleted and "
          "whether any counter clause fails (test on a scratch copy). Report the rows no clause "
          "needs and no reader gains from, and the rows that are load-bearing. Also name any "
          "prose in block 23 that repeats what the table says. Write `<W>R46W2Simpl/report.md`."),
        T("R46W2Conn", "connector",
          "Cross-round consistency: compare this round's instruments with round 45's and with "
          "sibling lanes. (1) Does any sibling lane's counter solve the discrimination problem "
          "differently — read-only grep for `battery`, `forgeries`, `mutation` in "
          "`/home/vgpnk/Projects/shokunin/*-shokunin/tools/`; report one transferable idea. (2) "
          "Which of round 45's routed items does this round actually close, by a table over "
          "R45-CL1..CL24 read from `corpus/lessons/round-45.md`. (3) Name one pattern the fleet "
          "should adopt from this round and one this round should have adopted from the fleet. "
          "Write `<W>R46W2Conn/report.md`."),
        T("R46W2Record", "reviewer",
          "Audit the round's record against committed bytes. Read `.ufo/waves/round-46/` (all "
          "committed seat reports), the receipt files under `l1/scores/` and `controls/`, and "
          "`corpus/lessons/round-46.md`. Report: (a) every numeric claim in the lesson that a "
          "receipt does not support; (b) every seat finding that the lesson ignores; (c) whether "
          "the `Assimilation: none` line is defensible; (d) the exact value of "
          "`grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` and whether S142's row "
          "parses as 11 columns. Write `<W>R46W2Record/report.md`."),
    ]
    groups = [census[i::8] for i in range(8)]
    for i, g in enumerate(groups):
        tasks.append(reg_group("ABCDEFGH"[i], g))

    os.makedirs(WAVE_DIR, exist_ok=True)
    items = [{"name": t["name"], "role": t["agent"], "prompt": t["task"], "axes": AXES}
             for t in tasks]
    spec = {"wave": "r46-w2", "milestone": MILE, "reportDir": REPORT,
            "context": CTX, "items": items}
    spec_path = os.path.join(WAVE_DIR, "w2-spec.json")
    with open(spec_path, "w") as f:
        json.dump(spec, f, indent=1)
    env = dict(os.environ, UFO_FLEET_ALLOW_EXTERNAL_TOOLS="1",
               UFO_CONFIG_PATH="/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json",
               UFO_PROJECT_ROOT=ROOT)
    proc = subprocess.run(["node", os.path.expanduser("~/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs"),
                           "plan", "--spec", spec_path],
                          capture_output=True, text=True, env=env, cwd=ROOT)
    if proc.returncode != 0 or not proc.stdout.strip().startswith("{"):
        raise SystemExit("validator failed: rc=%s %s %s"
                         % (proc.returncode, proc.stdout[:600], proc.stderr[:600]))
    plan = json.loads(proc.stdout)
    wave_tasks = plan["tasks"]
    members = {t["name"]: {"kind": "spawn", "agentId": None, "role": t["agent"],
                           "item": None, "axes": AXES, "milestone": MILE} for t in wave_tasks}
    dispatch = {
        "schema": "ufo-swarm-wave-dispatch-v1", "wave": "r46-w2",
        "policy": plan["policy"], "counts": plan["counts"],
        "registry": {"schema": "ufo-swarm-registry-v1",
                     "path": ".ufo/waves/round-46/w2/swarm-registry.json",
                     "reportDir": REPORT, "members": members},
        "compaction": plan.get("compaction", {"applied": False, "mechanism": None,
                                              "reason": None, "savedBytes": 0,
                                              "payloadBytesBefore": 0,
                                              "payloadBytesAfter": 0}),
        "taskCall": {"context": plan["context"], "tasks": wave_tasks},
        "resumeSends": [],
        "note": ("Issue exactly one batched task call with taskCall ({context, tasks}); "
                 "never split a wave into multiple task calls (one-swarm-per-wave)."),
    }
    with open(os.path.join(WAVE_DIR, "w2-dispatch.json"), "w") as f:
        json.dump(dispatch, f, indent=1)
    os.makedirs(os.path.join(WAVE_DIR, "w2"), exist_ok=True)
    with open(os.path.join(WAVE_DIR, "w2/swarm-registry.json"), "w") as f:
        json.dump({"schema": "ufo-swarm-registry-v1", "wave": "r46-w2",
                   "reportDir": REPORT, "members": members}, f, indent=1)
    print("wrote", len(wave_tasks), "seats;",
          dict(collections.Counter(t["agent"] for t in wave_tasks)))
    print("counts", plan["counts"])
    if "--no-ready" in sys.argv:
        print("ready file NOT written")
        return
    with open(os.path.join(WAVE_DIR, "w2.ready"), "w") as f:
        json.dump({"lane": "kaidoku", "round": 46, "wave": "r46-w2",
                   "dispatch": os.path.join(WAVE_DIR, "w2-dispatch.json"),
                   "l1": "KaidokuR46"}, f)
    print("ready written")


if __name__ == "__main__":
    main()
