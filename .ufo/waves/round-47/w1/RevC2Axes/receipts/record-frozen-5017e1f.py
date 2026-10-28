#!/usr/bin/env python3
"""Round-47 C2 counter — the lane's current self-assessment, re-derived atom by atom.

Reads the last two `## Round N` sections of `SCORECARD.md` at `--rev` and compares every
machine-checkable atom with committed repo state:

  seats   `Waves: A + B = C seats` / `Wave 1: A seats; wave 2: B seats`
          derived from `.ufo/waves/round-N/*-dispatch.json` -> counts.spawn, in file order
  window  a sentence claiming a `git log …` "is empty" over `X..Y -- paths`
          derived by running the same log at --rev; a `<tip>`/`<REV>` placeholder is
          `unverifiable` and counts as a mismatch
  path    every `.ufo/waves/…` token in the sections -> exists at --rev
  rev     every backticked 7–40 hex token -> resolves and is an ancestor of --rev

Repairs append a `## Record corrections — round 47` section. Each
`- corrects <class> <key>: <statement>` line exempts the atoms it names and is itself
re-derived; a correction that disagrees with committed state keeps the atom red.

Exit codes: 0 met; 1 not met; 2 could-not-evaluate.
"""
import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "round-46"))
import gate  # noqa: E402

SELF = "tools/round-47/record.py"
CLAIMS = "plans/round-47-claims.md"
CARD = "SCORECARD.md"
CORR_HEAD = "## Record corrections — round 47"
EXEMPT_MAX = 3
CORR_MIN = 2
CLASSES = ("seats", "window", "path", "rev", "axes")
AXIS_ROW = re.compile(r"(?m)^\|\s*(coverage|depth)\s*\|(.*)$")
FRAC = re.compile(r"\b(\d+)/(\d+)\b")
CRAFT = "## Queue-drain craft "
HARD_REF = re.compile(r"((?:corpus|plans|tools)/[A-Za-z0-9._/-]+)(?::(\d+)(?:-(\d+))?)?")
CORR_AXES = re.compile(r"(\d+)/(\d+)")

SEATS_SUM = re.compile(r"Waves?:\s*(\d+)\s*\+\s*(\d+)\s*=\s*(\d+)\s*seats")
SEATS_PAIR = re.compile(r"Wave 1:\s*(\d+)\s*seats;\s*wave 2:\s*(\d+)\s*seats")
WAVE_DIR = re.compile(r"\.ufo/waves/round-[0-9]+/[A-Za-z0-9._/-]*")
REV_TOKEN = re.compile(r"`([0-9a-f]{7,40})`")
WINDOW = re.compile(r"([0-9a-f]{7,40})\.\.([0-9a-f]{7,40})")
CORR = re.compile(r"^- corrects (seats|window|path|rev) (\S+):\s*(.+)$")
CORR_SEATS = re.compile(r"(\d+) waves?,\s*(\d+) seats total")
CORR_WINDOW = re.compile(r"empty in ([0-9a-f]{7,40})\.\.([0-9a-f]{7,40})\s+--\s+(.+)$")


def sections(card):
    """The last two `## Round N` sections, in file order, with their round numbers."""
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^## Round (\d+)", card)]
    out = []
    for pos, rnd in heads[-2:]:
        end = card.find("\n## ", pos + 1)
        out.append((rnd, card[pos:end if end >= 0 else len(card)]))
    return out


def dispatch_counts(files, rnd):
    """(spawns in wave order, error)."""
    spawns = []
    i = 1
    while True:
        path = f".ufo/waves/round-{rnd}/w{i}-dispatch.json"
        body = files(path)
        if body is None:
            break
        try:
            payload = json.loads(body)
            spawns.append(int(payload["counts"]["spawn"]))
        except (ValueError, KeyError, TypeError):
            return None, f"{path}: unreadable counts"
        i += 1
    if not spawns:
        return None, f"no dispatch file for round {rnd}"
    return spawns, None


def git(root, *args):
    r = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
    return r


def window_empty(root, rev, base, tip, paths):
    r = git(root, "log", "--name-status", "--format=", f"{base}..{tip}", "--", *paths)
    if r.returncode != 0:
        return None, "git log failed"
    return r.stdout.strip() == "", None


def knowledge_paths(root, rev):
    r = git(root, "ls-tree", "-r", "--name-only", rev, "--", "corpus/knowledge")
    if r.returncode != 0:
        return None
    return [p for p in r.stdout.splitlines() if p.endswith(".md")]


def coverage_pair(root, rev, files):
    readme = files("corpus/README.md")
    paths = knowledge_paths(root, rev)
    if readme is None or paths is None or "## Coverage map\n" not in readme:
        return None
    section = readme.split("## Coverage map\n", 1)[1].split("\n## ", 1)[0]
    mapped = set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+", section))
    stems = {os.path.basename(p)[:-3] for p in paths}
    return (len(stems & mapped), len(stems))


def depth_pair(files):
    """Resolved craft rule blocks over the total, exactly as command A reads them."""
    skill = files("SKILL.md")
    if skill is None or CRAFT not in skill:
        return None
    craft = skill.split(CRAFT, 1)[1].split("\n## ", 1)[0]
    rules = re.split(r"(?m)^- \*\*", craft)[1:]
    resolved = 0
    for rule in rules:
        refs = HARD_REF.findall(rule)
        valid = bool(refs)
        for name, first, last in refs:
            body = files(name)
            if body is None:
                valid = False
                break
            count = len(body.splitlines())
            start, end = int(first or 1), int(last or first or 1)
            if not (1 <= start <= end <= count):
                valid = False
                break
        resolved += valid
    return (resolved, len(rules))


def axis_pairs(files, root, rev):
    return {"coverage": coverage_pair(root, rev, files),
            "depth": depth_pair(files)}


def collect(section_text, rnd, files, root, rev):
    atoms = []

    for m in SEATS_SUM.finditer(section_text):
        atoms.append({"class": "seats", "key": rnd, "atom": m.group(0),
                      "shape": "sum", "claim": tuple(int(x) for x in m.groups())})
    for m in SEATS_PAIR.finditer(section_text):
        atoms.append({"class": "seats", "key": rnd, "atom": m.group(0),
                      "shape": "pair", "claim": (int(m.group(1)), int(m.group(2)))})

    for line in section_text.splitlines():
        if "is empty" not in line:
            continue
        m = WINDOW.search(line)
        atoms.append({"class": "window", "key": rnd, "atom": line.strip()[:160],
                      "line": line.strip(),
                      "pair": (m.group(1), m.group(2)) if m else None})

    for m in WAVE_DIR.finditer(section_text):
        token = m.group(0).rstrip(".,;:)`")
        atoms.append({"class": "path", "key": token, "atom": token, "path": token})

    for m in REV_TOKEN.finditer(section_text):
        atoms.append({"class": "rev", "key": m.group(1), "atom": f"`{m.group(1)}`",
                      "rev": m.group(1)})
    return atoms


def collect_axes(card):
    if "## Owned axes" not in card:
        return []
    body = card.split("## Owned axes", 1)[1].split("\n## ", 1)[0]
    atoms = []
    for m in AXIS_ROW.finditer(body):
        frac = FRAC.search(m.group(2))
        if not frac:
            continue
        atoms.append({"class": "axes", "key": m.group(1), "axis": m.group(1),
                      "atom": f"{m.group(1)} {frac.group(0)} at the head of its Owned-axes row",
                      "claim": (int(frac.group(1)), int(frac.group(2)))})
    return atoms


def derive(atom, files, root, rev, spawns_cache):
    """(ok, detail) for one atom."""
    cls, rnd = atom["class"], atom["key"]
    if cls == "seats":
        spawns, err = spawns_cache(rnd)
        if err:
            return False, err
        if atom["shape"] == "sum":
            a, b, c = atom["claim"]
            got = (spawns[0] if len(spawns) > 0 else 0,
                   spawns[1] if len(spawns) > 1 else 0, sum(spawns))
            return (a, b, c) == got, {"claimed": [a, b, c], "derived": list(got),
                                     "dispatch": spawns}
        a, b = atom["claim"]
        got = (spawns[0] if len(spawns) > 0 else 0,
               spawns[1] if len(spawns) > 1 else 0)
        return (a, b) == got, {"claimed": [a, b], "derived": list(got),
                               "dispatch": spawns}
    if cls == "window":
        line = atom["line"]
        m = WINDOW.search(line)
        if not m:
            return False, {"reason": "unverifiable", "detail":
                           "the claimed window names no concrete A..B revisions"}
        tail = line[m.end():]
        paths = re.findall(r"--\s+([A-Za-z0-9._/ -]+)", tail)
        pathspec = paths[0].split() if paths else []
        empty, err = window_empty(root, rev, m.group(1), m.group(2), pathspec)
        if err:
            return False, {"reason": err}
        return bool(empty), {"window": f"{m.group(1)}..{m.group(2)}",
                             "pathspec": pathspec, "empty": empty}
    if cls == "path":
        exists = files(atom["path"]) is not None
        return exists, {"path": atom["path"], "exists": exists}
    if cls == "axes":
        pairs = axis_pairs(files, root, rev)
        got = pairs.get(atom["axis"])
        if got is None:
            return False, {"reason": "unobservable", "axis": atom["axis"]}
        return tuple(atom["claim"]) == got, {"axis": atom["axis"],
                                            "claimed": list(atom["claim"]),
                                            "derived": list(got)}
    if cls == "rev":
        r = git(root, "rev-parse", "--verify", "--quiet", atom["rev"] + "^{commit}")
        oid = r.stdout.strip()
        if r.returncode != 0:
            return False, {"rev": atom["rev"], "resolves": False}
        a = git(root, "merge-base", "--is-ancestor", oid, rev)
        return a.returncode == 0, {"rev": atom["rev"], "oid": oid,
                                   "ancestor": a.returncode == 0}
    return False, {"reason": f"unknown class {cls}"}


def corrections(card):
    """The correction lines, or ([], '') when the section is absent."""
    if CORR_HEAD not in card:
        return [], ""
    body = card.split(CORR_HEAD, 1)[1].split("\n## ", 1)[0]
    out = []
    for line in body.splitlines():
        m = CORR.match(line.strip())
        if m:
            key = m.group(2)
            key = key[6:] if key.startswith("round-") else key
            out.append({"class": m.group(1), "key": key, "text": line.strip(),
                        "statement": m.group(3)})
    return out, body


def corrects(entry, files, root, rev, spawns_cache):
    cls, key, stmt = entry["class"], entry["key"], entry["statement"]
    if cls == "seats":
        m = CORR_SEATS.search(stmt)
        if not m:
            return False, "a seats correction must state '<n> waves, <total> seats total'"
        spawns, err = spawns_cache(key)
        if err:
            return False, err
        claimed = (int(m.group(1)), int(m.group(2)))
        got = (len(spawns), sum(spawns))
        return claimed == got, {"claimed": list(claimed), "derived": list(got),
                                "dispatch": spawns}
    if cls == "window":
        m = CORR_WINDOW.search(stmt)
        if not m:
            return False, "a window correction must state 'empty in A..B -- paths'"
        pathspec = m.group(3).split()
        empty, err = window_empty(root, rev, m.group(1), m.group(2), pathspec)
        if err:
            return False, err
        return bool(empty), {"window": f"{m.group(1)}..{m.group(2)}", "empty": empty}
    if cls == "axes":
        m = CORR_AXES.search(stmt)
        if not m:
            return False, "an axes correction must state '<resolved>/<total>'"
        got = axis_pairs(files, root, rev).get(key)
        if got is None:
            return False, {"reason": "unobservable", "axis": key}
        claimed = (int(m.group(1)), int(m.group(2)))
        return claimed == got, {"axis": key, "claimed": list(claimed),
                                "derived": list(got)}
    if cls == "path":
        return files(key) is not None, {"path": key, "exists": files(key) is not None}
    if cls == "axes":
        pairs = axis_pairs(files, root, rev)
        got = pairs.get(atom["axis"])
        if got is None:
            return False, {"reason": "unobservable", "axis": atom["axis"]}
        return tuple(atom["claim"]) == got, {"axis": atom["axis"],
                                            "claimed": list(atom["claim"]),
                                            "derived": list(got)}
    if cls == "rev":
        r = git(root, "rev-parse", "--verify", "--quiet", key + "^{commit}")
        return r.returncode == 0, {"rev": key, "resolves": r.returncode == 0}
    return False, f"unknown class {cls}"


def evaluate_text(card, files, root, rev, battery=None):
    secs = sections(card)
    receipt = {"counter": "round-47-c2", "rev": rev,
               "sections": [f"round-{rnd}" for rnd, _ in secs]}
    if len(secs) != 2:
        return 2, dict(receipt, reason="fewer than two `## Round N` sections")
    failing = []
    cache = {}

    def spawns_cache(rnd):
        rnd = str(rnd)
        if rnd not in cache:
            cache[rnd] = dispatch_counts(files, rnd)
        return cache[rnd]

    atoms = []
    for rnd, text in secs:
        atoms.extend(collect(text, rnd, files, root, rev))
    atoms.extend(collect_axes(card))
    corr, corr_body = corrections(card)
    exempt_keys = {(c["class"], str(c["key"])) for c in corr}
    known_keys = {(a["class"], str(a["key"])) for a in atoms}
    known_pairs = {(a["class"], a.get("pair")) for a in atoms if a.get("pair")}

    def exempt(atom, entry):
        if atom["class"] != entry["class"]:
            return False
        if atom["class"] == "window":
            if atom.get("pair") is None:
                return True  # a placeholder claim is replaced by a concrete window
            cm = CORR_WINDOW.search(entry["statement"])
            return bool(cm) and (cm.group(1), cm.group(2)) == atom["pair"]
        return str(atom["key"]) == str(entry["key"])


    mismatches, verified, exempted = [], [], []
    for atom in atoms:
        ok, detail = derive(atom, files, root, rev, spawns_cache)
        if ok:
            verified.append({k: atom[k] for k in ("class", "key", "atom")})
            continue
        if any(exempt(atom, entry) for entry in corr):
            exempted.append({k: atom[k] for k in ("class", "key", "atom")})
            continue
        mismatches.append({"class": atom["class"], "key": atom["key"],
                           "atom": atom["atom"], "derived": detail})

    corrections_bad = []
    for entry in corr:
        ok, detail = corrects(entry, files, root, rev, spawns_cache)
        if not ok:
            corrections_bad.append({"line": entry["text"], "detail": detail})
        if (entry["class"], str(entry["key"])) not in known_keys:
            corrections_bad.append({"line": entry["text"],
                                    "detail": "exempts an atom that does not exist"})
        if entry["class"] == "window":
            cm = CORR_WINDOW.search(entry["statement"])
            if cm and ("window", (cm.group(1), cm.group(2))) not in known_pairs:
                corrections_bad.append({"line": entry["text"],
                                        "detail": "window pair names no atom in scope"})

    receipt.update({"atoms": len(atoms), "verified": len(verified),
                    "exempted": exempted, "mismatches": mismatches,
                    "corrections": len(corr), "corrections_bad": corrections_bad,
                    "atoms_by_class": {c: sum(1 for a in atoms if a["class"] == c)
                                       for c in CLASSES}})
    missing_classes = [c for c in CLASSES if receipt["atoms_by_class"][c] == 0]
    if missing_classes:
        failing.append(f"no atoms of class(es) {missing_classes}")
    if mismatches:
        failing.append(f"mismatches {len(mismatches)} != 0")
    if len(corr) < CORR_MIN:
        failing.append(f"corrections {len(corr)} < {CORR_MIN}")
    if corrections_bad:
        failing.append(f"corrections that do not re-derive: {len(corrections_bad)}")
    if len(exempted) > EXEMPT_MAX:
        failing.append(f"exempted {len(exempted)} > {EXEMPT_MAX}")
    if battery is not None:
        receipt["battery"] = battery
        for key, want in (("correction_forgeries", 3), ("forgeries_green", 0)):
            if battery.get(key) != want:
                failing.append(f"battery {key} {battery.get(key)} != {want}")
    receipt["met_target"] = not failing
    receipt["failing"] = failing
    return (0 if not failing else 1), receipt


# --- battery: three forged corrections, each must keep the counter red ------------

def run_battery(card, files, root, rev):
    out = {"correction_forgeries": 0, "forgeries_green": 0, "fixtures": []}
    ok_card = CORR_HEAD in card

    def forged(name, mutate):
        if not ok_card:
            out["fixtures"].append({"name": name, "error": "no corrections section"})
            out["correction_forgeries"] += 1
            out["forgeries_green"] += 0
            return
        text = mutate(card)
        if text == card:
            out["fixtures"].append({"name": name, "error": "mutation was a no-op"})
            out["correction_forgeries"] += 1
            out["forgeries_green"] += 1
            return
        code, rec = evaluate_text(text, files, root, rev, battery=None)
        out["correction_forgeries"] += 1
        out["forgeries_green"] += 1 if code == 0 else 0
        out["fixtures"].append({"name": name, "exit": code,
                                "failing": rec.get("failing", rec.get("reason"))})

    def wrong_total(text):
        m = re.search(r"- corrects seats round-[0-9]+: .*?(\d+) seats total", text)
        if not m:
            return text
        n = int(m.group(1)) + 1
        return text[:m.start()] + m.group(0).replace(m.group(1), str(n), 1) + \
            text[m.end():]

    def non_empty(text):
        m = re.search(r"empty in ([0-9a-f]{7,40})\.\.([0-9a-f]{7,40})", text)
        if not m:
            return text
        # the base..tip window of the round itself is never empty
        return text.replace(m.group(0), f"empty in {m.group(1)}..{rev}", 1)

    def ghost_atom(text):
        return text + "\n- corrects path does/not/exist/at/any/revision.md: never\n"

    forged("correction-wrong-seat-total", wrong_total)
    forged("correction-window-not-empty", non_empty)
    forged("correction-ghost-atom", ghost_atom)
    return out


# --- CLI --------------------------------------------------------------------------

def evaluate(root, rev, with_battery=True):
    tip = gate.resolve(root, rev)
    if tip is None:
        return 2, {"counter": "round-47-c2", "reason": "unknown revision"}
    card = gate.show(root, tip, CARD)
    if card is None:
        return 2, {"counter": "round-47-c2", "reason": "SCORECARD.md absent at rev"}
    files = lambda p: gate.show(root, tip, p)  # noqa: E731
    code, receipt = evaluate_text(card, files, root, tip, battery=None)
    if with_battery and code in (0, 1):
        battery = run_battery(card, files, root, tip)
        code, receipt = evaluate_text(card, files, root, tip, battery=battery)
    receipt["rev"] = tip
    return code, receipt


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--no-battery", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    out, err = gate.out_path(args.root, args.json_out)
    if err:
        print(json.dumps({"reason": err}))
        return 2
    code, receipt = gate.main_guard(lambda: evaluate(args.root, args.rev,
                                                     not args.no_battery))
    gate.emit(receipt, out)
    return code


# --- selftest ---------------------------------------------------------------------

def _card(seats="Waves: 1 + 1 = 2 seats", window=None, corrections=3, total=2,
          path=".ufo/waves/round-9/w1-dispatch.json", rev="0000000", wbase="0000000"):
    window = window or f"`git log {wbase}..{wbase} -- tools/x/` is empty"
    text = ("# card\n\n## Owned axes\n\n"
            "| Axis | Baseline → current score, 0–10 | Observable | Evidence | Round |\n"
            "|---|---|---|---|---|\n"
            "| coverage | 9.72 → 10.0 | 1/1 knowledge files mapped | x | r1 |\n\n"
            "## Round 8\n\nAn earlier round with no atoms.\n\n"
            "## Round 9\n\nBase `%s`. %s. %s. See `%s`.\n\n"
            % (rev, seats, window, path))
    if corrections is not None:
        text += CORR_HEAD + "\n\n"
        if corrections >= 1:
            text += f"- corrects seats round-9: 2 waves, {total} seats total\n"
        if corrections >= 2:
            text += ("- corrects window round-9: empty in %s..%s -- tools/x/\n"
                     % (wbase, wbase))
        if corrections >= 3:
            text += f"- corrects path {path}: landed\n"
    return text


def selftest():
    root, err = gate.scratch("kaidoku-r47-record-selftest-")
    if err:
        print(json.dumps({"reason": err}))
        return 2
    import tempfile
    import shutil
    cases = []
    d = tempfile.mkdtemp(dir=root, prefix="repo-")
    try:
        subprocess.run(["git", "-C", d, "init", "-q"], check=True)
        for k, v in (("user.email", "st@r47"), ("user.name", "r47 selftest")):
            subprocess.run(["git", "-C", d, "config", k, v], check=True)
        os.makedirs(os.path.join(d, ".ufo/waves/round-9"), exist_ok=True)
        for i, spawn in ((1, 1), (2, 1)):
            with open(os.path.join(d, f".ufo/waves/round-9/w{i}-dispatch.json"), "w") as fh:
                json.dump({"counts": {"spawn": spawn, "resume": 0, "total": spawn}}, fh)
        for name, body in (("tools/x/keep.md", "x\n"),
                           ("corpus/knowledge/2026-10-01-x.md", "x\n"),
                           ("corpus/README.md",
                            "# readme\n\n## Coverage map\n\n- 2026-10-01-x — x\n\n"
                            "## Gaps\n\ntail\n")):
            full = os.path.join(d, name)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, "w").write(body)
        subprocess.run(["git", "-C", d, "add", "-A"], check=True)
        subprocess.run(["git", "-C", d, "commit", "-q", "-m", "base"], check=True)
        base = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], capture_output=True,
                              text=True).stdout.strip()
        open(os.path.join(d, "tools/x/keep.md"), "a").write("y\n")
        subprocess.run(["git", "-C", d, "add", "-A"], check=True)
        subprocess.run(["git", "-C", d, "commit", "-q", "-m", "tip"], check=True)
        tip = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], capture_output=True,
                             text=True).stdout.strip()
        files = {"SCORECARD.md": _card(rev=tip[:8]),
                 "corpus/README.md": "# readme\n\n## Coverage map\n\n- 2026-10-01-x — x\n\n## Gaps\n\ntail\n",
                 ".ufo/waves/round-9/w1-dispatch.json":
                     json.dumps({"counts": {"spawn": 1}}),
                 ".ufo/waves/round-9/w2-dispatch.json":
                     json.dumps({"counts": {"spawn": 1}})}

        def run(name, expect, card, with_battery=False):
            got, rec = evaluate_text(card, lambda p: files.get(p), d, tip,
                                     battery=None)
            cases.append({"case": name, "expect": expect, "got": got, "ok": got == expect,
                          "failing": rec.get("failing"), "mismatches": rec.get("mismatches")})
            return got, rec

        kw = dict(rev=tip[:8], wbase=base[:8])
        run("red-seats-false-no-correction", 1, _card(
            seats="Waves: 1 + 1 = 3 seats", corrections=0, **kw))
        run("green-seats-false-superseded", 0, _card(
            seats="Waves: 1 + 1 = 3 seats", **kw))
        run("red-unverifiable-window-uncorrected", 1, _card(
            window="`git log 0425224..<tip> -- x` is empty", corrections=1, **kw))
        run("red-ghost-exemption", 1, _card(**kw) +
            "\n- corrects path does/not/exist.md: x\n")
        run("red-correction-total-false", 1, _card(total=9, **kw))
        run("red-one-correction", 1, _card(corrections=1, **kw))
        run("green", 0, _card(**kw))

        # the empty window on our own base..tip is a real, reproducible non-empty window
        real = _card(window=f"`git log {base[:8]}..{tip[:8]} -- tools/x/` is empty",
                     rev=tip[:8], wbase=base[:8])
        got, rec = evaluate_text(real, lambda p: files.get(p), d, tip, battery=None)
        cases.append({"case": "red-non-empty-window", "expect": 1, "got": got,
                      "ok": got == 1, "mismatches": rec.get("mismatches")})

        bat = run_battery(_card(rev=tip[:8], wbase=base[:8]),
                          lambda p: files.get(p), d, tip)
        ok = bat["correction_forgeries"] == 3 and bat["forgeries_green"] == 0
        cases.append({"case": "battery-discriminates", "expect": True, "got": ok,
                      "ok": ok, "battery": bat})
    finally:
        shutil.rmtree(d, ignore_errors=True)
    failures = [c for c in cases if not c["ok"]]
    print("RECORD_SELFTEST: cases=%d failures=%d" % (len(cases), len(failures)))
    print(json.dumps({"cases": cases, "failures": len(failures)}, indent=1))
    shutil.rmtree(root, ignore_errors=True)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
