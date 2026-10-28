#!/usr/bin/env python3
"""Round-48 C2 counter — the record re-derived from committed bytes, with a floor.

Routed defects this counter closes (`corpus/lessons/round-47.md`):

- **R47-CL1** the round-47 counters grade committed bytes but execute their own code
  from the worktree.  Here the atom oracle (`tools/round-47/record.py`) is executed
  from the bytes at `--rev`, in a scratch file, so a worktree stub cannot change a
  verdict.
- **R47-CL10 (C2 side)** the round-47 counter measures consistency, never
  completeness: a card whose last two round sections are tautologies scores
  `mismatches []`.  Here every round section in scope must yield a seat, a path and a
  revision atom (or a re-derived seats correction), name its claims, and carry a
  quoted number only when a cited receipt backs it.
- **R47-CL14** an `axes` correction line is silently inert because the round-47
  grammar parses only `seats`, `window`, `path` and `rev`.  Here `axes` corrections
  parse and must re-derive against the card's own Owned-axes rows.

Profiles:
  v3 (default) — oracle consistency + completeness floor + quoted-receipt binding +
                 axes score-cell binding + re-derived corrections (incl. `axes`).
  v2           — the round-47 semantics ported (oracle consistency only), used only to
                 score the round's own forgeries against the hole it measures.

Exit codes: 0 met; 1 not met; 2 could-not-evaluate.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "round-46"))
import gate  # noqa: E402

SELF = "tools/round-48/record2.py"
CLAIMS = "plans/round-48-claims.md"
ORACLE = "tools/round-47/record.py"
CARD = "SCORECARD.md"
# The heading is matched as a whole line: the round section quotes it in prose, and a
# substring split took that quote for the section (A5).
CORR_HEAD = re.compile(r"(?m)^## Record corrections — round 48[ \t]*$")
CORR = re.compile(r"^- corrects (seats|window|path|rev|axes|quote) (\S+):\s*(.+)$")
CLAIM_ID = re.compile(r"\bR\d\d-C\d\b")
QUOTE = re.compile(r"\b(atoms|exempted|corrections|mismatches)\s+(\d+)\b")
RECEIPT = re.compile(r"\.ufo/waves/round-[0-9]+/l1/scores/[A-Za-z0-9._-]+\.json")
AXIS_SCORE = re.compile(r"(?m)^\|\s*(coverage|depth)\s*\|(.*)$")
SCORE_CELL = re.compile(r"(\d+(?:\.\d+)?)\s*(?:→|->)\s*(\d+(?:\.\d+)?)")
FRAC = re.compile(r"\b(\d+)/(\d+)\b")


class Malformed(Exception):
    pass


# --- the oracle, executed from committed bytes ------------------------------------

_ORACLE_CACHE = {}


def oracle(root, rev):
    """The round-47 record module, exec'd from the bytes at `rev` (never the worktree)."""
    key = (os.path.abspath(root), rev)
    if key in _ORACLE_CACHE:
        return _ORACLE_CACHE[key]
    body = gate.show(root, rev, ORACLE)
    if body is None:
        raise Malformed(f"{ORACLE} absent at rev")
    ns = {"__name__": "round47_record", "__file__": ORACLE}
    exec(compile(body, ORACLE, "exec"), ns)  # noqa: S102 - committed lane bytes
    _ORACLE_CACHE[key] = ns
    return ns


def spawns_cache(mod, files):
    cache = {}

    def get(rnd):
        if rnd not in cache:
            cache[rnd] = mod["dispatch_counts"](files, rnd)
        return cache[rnd]
    return get


# --- clauses ----------------------------------------------------------------------

def section_bodies(card):
    """[(round, text)] for the last two round sections, bounded at the next `## `."""
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^## Round (\d+)", card)]
    out = []
    for pos, rnd in heads[-2:]:
        end = card.find("\n## ", pos + 1)
        out.append((rnd, card[pos:end if end >= 0 else len(card)]))
    return out


def corrections_section(card):
    m = CORR_HEAD.search(card)
    if not m:
        return []
    body = card[m.end():].split("\n## ", 1)[0]
    out = []
    for line in body.splitlines():
        m = CORR.match(line.strip())
        if not m:
            continue
        key = m.group(2)
        key = key[6:] if key.startswith("round-") else key
        out.append({"class": m.group(1), "key": key, "text": line.strip(),
                    "statement": m.group(3)})
    return out


def receipts_at(files, section_text):
    out = []
    for path in sorted(set(RECEIPT.findall(section_text))):
        body = files(path)
        if body is None:
            continue
        try:
            out.append((path, json.loads(body)))
        except ValueError:
            out.append((path, None))
    return out


def quote_value(receipt, key):
    if not isinstance(receipt, dict) or key not in receipt:
        return None
    val = receipt[key]
    if isinstance(val, list):
        return len(val)
    if isinstance(val, bool):
        return None
    if isinstance(val, int):
        return val
    return None


def axis_scores(files):
    card = files(CARD)
    if card is None or "## Owned axes" not in card:
        return {}
    body = card.split("## Owned axes", 1)[1].split("\n## ", 1)[0]
    out = {}
    for m in AXIS_SCORE.finditer(body):
        axis, rest = m.group(1), m.group(2)
        cell = rest.split("|")
        if len(cell) < 2:
            continue
        score = SCORE_CELL.search(cell[0])
        frac = FRAC.search("|".join(cell[1:]))
        if score and frac:
            out[axis] = {"score": (float(score.group(1)), float(score.group(2))),
                         "fraction": (int(frac.group(1)), int(frac.group(2)))}
    return out


def _quote_correction(c, secs, files):
    """A `quote` correction must state a receipt's true value and correct a wrong quote."""
    m = QUOTE.search(c["statement"])
    if not m:
        return False, {"reason": "a quote correction must state '<key> <n>'"}
    key, value = m.group(1), int(m.group(2))
    text = dict((rnd, body) for rnd, body in secs).get(c["key"])
    if text is None:
        return False, {"reason": f"no round-{c['key']} section in scope"}
    quoted = [int(v) for k, v in QUOTE.findall(text) if k == key]
    recs = receipts_at(files, text)
    backed = any(quote_value(r, key) == value for _, r in recs)
    detail = {"key": key, "value": value, "quoted": quoted,
              "receipts": [p for p, _ in recs], "backed": backed}
    if value in quoted:
        return False, dict(detail, reason="the section already quotes that value")
    if not backed:
        return False, dict(detail, reason="no cited receipt states that value")
    return True, detail


def score(card, files, root, rev, profile, battery=None):
    hard = profile == "v3"
    receipt = {"counter": "round-48-c2", "profile": profile, "rev": rev}
    failing = []
    try:
        mod = oracle(root, rev)
        secs = section_bodies(card)
        if len(secs) != 2:
            raise Malformed(f"the card carries {len(secs)} round sections, not 2")
        code, oreceipt = mod["evaluate_text"](card, files, root, rev)
    except Malformed as exc:
        return 2, {"reason": str(exc), "counter": "round-48-c2", "profile": profile}
    except Exception as exc:  # noqa: BLE001
        return 2, {"reason": f"oracle: {type(exc).__name__}: {exc}",
                   "counter": "round-48-c2", "profile": profile}
    receipt["oracle"] = {k: oreceipt.get(k) for k in
                         ("atoms", "atoms_by_class", "mismatches", "corrections",
                          "exempted", "met_target")}
    receipt["sections"] = [f"round-{rnd}" for rnd, _ in secs]
    if code != 0:
        failing.append("the round-47 atom oracle does not accept the card "
                       f"(mismatches {len(oreceipt.get('mismatches', []))})")
    if not hard:
        receipt["met_target"] = not failing
        receipt["failing"] = failing
        return (0 if not failing else 1), receipt

    # clause: completeness floor (closes R47-CL10 C2 side) -------------------------
    spawns = spawns_cache(mod, files)
    corrs = corrections_section(card)
    corr_by_round = {}
    for c in corrs:
        corr_by_round.setdefault(c["key"], set()).add(c["class"])
    floor = []
    for rnd, text in secs:
        atoms = mod["collect"](text, rnd, files, root, rev)
        by = {}
        for a in atoms:
            by[a["class"]] = by.get(a["class"], 0) + 1
        ids = sorted(set(CLAIM_ID.findall(text)))
        seats_ok = by.get("seats", 0) >= 1 or "seats" in corr_by_round.get(rnd, set())
        row = {"round": f"round-{rnd}", "atoms_by_class": by, "claims": ids,
               "seats_via_correction": "seats" in corr_by_round.get(rnd, set())}
        floor.append(row)
        if not seats_ok:
            failing.append(f"round-{rnd}: no seat atom and no re-derived seats correction")
        for cls in ("path", "rev"):
            if by.get(cls, 0) < 1:
                failing.append(f"round-{rnd}: no {cls} atom")
        if not ids:
            failing.append(f"round-{rnd}: names no claim id")
    receipt["floor"] = floor
    seen = {}
    for row in floor:
        for cid in row["claims"]:
            seen[cid] = seen.get(cid, 0) + 1
    dup = sorted(k for k, v in seen.items() if v > 1)
    receipt["claim_ids"] = seen
    if dup:
        failing.append(f"claim ids claimed by both sections: {dup}")
    axes_atoms = mod["collect_axes"](card)
    receipt["axes_atoms"] = len(axes_atoms)
    if len(axes_atoms) < 2:
        failing.append(f"axes atoms {len(axes_atoms)} < 2")

    # clause: every correction line re-derives, `axes` and `quote` included
    # (closes R47-CL14: the round-47 grammar made an axes correction silently inert)
    bad_corr = []
    quote_fixes = {}
    for c in corrs:
        if c["class"] == "axes":
            m = re.search(r"(\d+)/(\d+)", c["statement"])
            pairs = mod["axis_pairs"](files, root, rev)
            got = pairs.get(c["key"])
            ok = bool(m) and got is not None and \
                (int(m.group(1)), int(m.group(2))) == tuple(got)
            detail = {"axis": c["key"], "derived": list(got) if got else None}
        elif c["class"] == "quote":
            ok, detail = _quote_correction(c, secs, files)
            if ok:
                quote_fixes.setdefault(c["key"], {})[detail["key"]] = detail["value"]
        else:
            ok, detail = mod["corrects"](c, files, root, rev, spawns)
        if not ok:
            bad_corr.append({"line": c["text"][:120], "detail": detail})
    receipt["corrections"] = len(corrs)
    receipt["corrections_bad"] = bad_corr
    if not corrs:
        failing.append("no `## Record corrections — round 48` line re-derived")
    if bad_corr:
        failing.append(f"corrections that do not re-derive: {len(bad_corr)}")

    # clause: a quoted number is bound to the receipt it cites, or to a re-derived
    # `quote` correction (R47-CL13: a number the record quotes from its own receipt)
    quote_bad, quote_checked = [], 0
    for rnd, text in secs:
        quotes = QUOTE.findall(text)
        if not quotes:
            continue
        recs = receipts_at(files, text)
        if not recs:
            quote_bad.append({"round": f"round-{rnd}",
                              "reason": "quotes a number and cites no receipt that "
                                        "exists at rev", "quotes": quotes})
            continue
        fixed = quote_fixes.get(rnd, {})
        for key, val in quotes:
            if any(quote_value(r, key) == int(val) for _, r in recs):
                quote_checked += 1
            elif key in fixed and int(val) != fixed[key] and \
                    any(quote_value(r, key) == fixed[key] for _, r in recs):
                quote_checked += 1
                receipt.setdefault("quotes_corrected", []).append(
                    {"round": f"round-{rnd}", "quote": f"{key} {val}",
                     "corrected": fixed[key]})
            else:
                quote_bad.append({"round": f"round-{rnd}", "quote": f"{key} {val}",
                                  "receipts": [p for p, _ in recs]})
    receipt["quotes_checked"] = quote_checked
    receipt["quotes_bad"] = quote_bad
    if quote_bad:
        failing.append(f"quoted numbers with no backing receipt: {len(quote_bad)}")

    # clause: the Owned-axes score cell follows its own fraction (R47-CL2) --------
    scores = axis_scores(files)
    cell_bad = []
    for axis, val in scores.items():
        n, d = val["fraction"]
        want = round(10 * n / d, 2) if d else None
        if want is None or abs(val["score"][1] - want) > 1e-9:
            cell_bad.append({"axis": axis, "score": val["score"], "fraction": [n, d],
                             "derived": want})
    receipt["axis_score_cells"] = {k: v for k, v in scores.items()}
    receipt["axis_score_bad"] = cell_bad
    if cell_bad:
        failing.append(f"axes score cells disagree with their fraction: {len(cell_bad)}")

    if battery is not None:
        receipt["battery"] = battery
        for key, want in (("forgeries_total", 5), ("v2_green", 5), ("v3_green", 0),
                          ("genuine_green", 1), ("crash", 0)):
            if battery.get(key) != want:
                failing.append(f"battery {key} {battery.get(key)} != {want}")
    receipt["met_target"] = not failing
    receipt["failing"] = failing
    return (0 if not failing else 1), receipt


# --- battery ----------------------------------------------------------------------

SEATS_LINE = re.compile(r"(?m)^.*(?:Waves?:\s*\d+\s*\+\s*\d+\s*=\s*\d+\s*seats"
                         r"|Wave 1:\s*\d+\s*seats).*$")
WINDOW_LINE = re.compile(r"(?m)^.*\bis empty\b.*$")


def _round_sections(card):
    """[(round, start, end)] for the last two `## Round N` sections."""
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^## Round (\d+)", card)]
    out = []
    for pos, rnd in heads[-2:]:
        end = card.find("\n## ", pos + 1)
        out.append((rnd, pos, end if end >= 0 else len(card)))
    return out


def _m_gold_tautology(card, ctx):
    """Replace both round sections with tautologies, keeping only seat/window atoms.

    The round-47 oracle already refuses a card with no seats or window atom, so a
    forgery that removes them measures the old counter, not the new clause; this one
    keeps the atoms and removes the *claims*.
    """
    out = card
    for rnd, start, end in reversed(_round_sections(card)):
        body = out[start:end]
        keep = [l for l in body.splitlines()
                if SEATS_LINE.match(l) or WINDOW_LINE.match(l)]
        head = body.splitlines()[0]
        wave = f".ufo/waves/round-{rnd}/w1/"
        new = (head + "\n\n" + "\n".join(keep) +
               f"\n\nSeats were read off the dispatch files in `{wave}`. One path "
               "exists: `corpus/README.md`. `1e32827b`.\n")
        out = out[:start] + new + out[end:]
    return out, {}


def _m_seats_moved(card, ctx):
    """Move the seat total into the older section only: one atom, one section."""
    spans = _round_sections(card)
    if len(spans) != 2:
        return card, {}
    files = ctx["files"]
    rnd0 = spans[0][0]
    spawns, i = [], 1
    while True:
        body = files(f".ufo/waves/round-{rnd0}/w{i}-dispatch.json")
        if body is None:
            break
        try:
            spawns.append(int(json.loads(body)["counts"]["spawn"]))
        except (ValueError, KeyError, TypeError):
            return card, {}
        i += 1
    if not spawns:
        return card, {}
    line = (f"Waves: {spawns[0]} + {spawns[1] if len(spawns) > 1 else 0} = "
            f"{sum(spawns)} seats.")
    out = card
    for rnd, start, end in reversed(spans):
        out = out[:start] + SEATS_LINE.sub("", out[start:end]) + out[end:]
    rnd, start, end = _round_sections(out)[0]
    cut = out.find("\n", start)
    out = out[:cut + 1] + "\n" + line + "\n" + out[cut + 1:]
    return out, {}


def _m_quote_off(card, ctx):
    return QUOTE.sub(lambda m: f"{m.group(1)} {int(m.group(2)) + 1}", card, count=1), {}


def _m_axes_cell_off(card, ctx):
    m = AXIS_SCORE.search(card)
    if not m:
        return card, {}
    row = m.group(0)
    cells = row.split("|")
    if len(cells) < 3:
        return card, {}
    sm = SCORE_CELL.search(cells[2])
    if not sm:
        return card, {}
    bad = row.replace(sm.group(2), f"{float(sm.group(2)) - 1.0:.1f}", 1)
    return card.replace(row, bad, 1), {}


def _m_axes_correction_forged(card, ctx):
    line = ("\n## Record corrections — round 48\n\n"
            "- corrects axes depth: 999/999 — a forged axes correction the round-47 "
            "grammar ignores\n")
    return card.rstrip() + "\n" + line, {}


MUTATIONS = [("gold-tautology", _m_gold_tautology),
             ("seats-moved", _m_seats_moved),
             ("quote-off-by-one", _m_quote_off),
             ("axes-score-cell-off", _m_axes_cell_off),
             ("axes-correction-forged", _m_axes_correction_forged)]


def _mut_digest():
    import inspect
    h = hashlib.sha256()
    for name, fn in MUTATIONS:
        h.update(name.encode())
        h.update(b"\n")
        h.update(inspect.getsource(fn).encode())
        h.update(b"\n---\n")
    return h.hexdigest()


MUT_DIGEST = _mut_digest()


def run_battery(root, rev):
    card = gate.show(root, rev, CARD)
    if card is None:
        return {"error": "SCORECARD.md absent at rev"}
    files = lambda p: gate.show(root, rev, p)  # noqa: E731
    out = {"fixtures": [], "forgeries_total": 0, "v2_green": 0, "v3_green": 0,
           "genuine_green": 0, "crash": 0, "mutations_sha256": MUT_DIGEST}
    code, _ = score(card, files, root, rev, "v3", battery=None)
    out["genuine_green"] = 1 if code == 0 else 0
    out["genuine_exit"] = code
    out["crash"] += 1 if code == 2 else 0
    ctx = {"files": files}
    for name, fn in MUTATIONS:
        text, _ = fn(card, ctx)
        if text == card:
            out["fixtures"].append({"name": name, "error": "mutation was a no-op"})
            out["forgeries_total"] += 1
            out["v2_green"] += 1
            continue
        c2, r2 = score(text, files, root, rev, "v2", battery=None)
        c3, r3 = score(text, files, root, rev, "v3", battery=None)
        out["forgeries_total"] += 1
        out["v2_green"] += 1 if c2 == 0 else 0
        out["v3_green"] += 1 if c3 == 0 else 0
        out["crash"] += 1 if c3 == 2 else 0
        out["fixtures"].append({"name": name, "v2_exit": c2, "v3_exit": c3,
                                "v2_failing": r2.get("failing", r2.get("reason")),
                                "v3_failing": r3.get("failing", r3.get("reason"))})
    return out


# --- CLI --------------------------------------------------------------------------

def evaluate(root, freeze, rev, profile="v3", with_battery=True):
    flat, fs = gate.freeze_state(root, freeze, rev, CLAIMS)
    if flat == 2:
        return 2, dict(fs, counter="round-48-c2", profile=profile)
    card = gate.show(root, rev, CARD)
    if card is None:
        return 2, {"reason": "SCORECARD.md absent at rev", "counter": "round-48-c2"}
    files = lambda p: gate.show(root, rev, p)  # noqa: E731
    code, receipt = score(card, files, root, rev, profile, battery=None)
    if with_battery and code == 0:
        battery = run_battery(root, rev)
        if "error" in battery:
            return 2, {"reason": "battery: " + battery["error"], "counter": "round-48-c2"}
        code, receipt = score(card, files, root, rev, profile, battery=battery)
    elif with_battery:
        receipt["battery"] = {"skipped": "the card fails a structural clause first"}
    receipt.update({"freeze": fs["freeze"], "frozen_derived": fs["frozen_derived"],
                    "frozen_path_changed": fs["frozen_path_changed"],
                    "touched": len(fs["touched"]), "restored": fs["restored"]})
    return code, receipt


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root")
    ap.add_argument("--freeze")
    ap.add_argument("--rev")
    ap.add_argument("--profile", default="v3", choices=("v2", "v3"))
    ap.add_argument("--no-battery", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    missing = [k for k in ("root", "freeze", "rev") if not getattr(args, k)]
    if missing:
        ap.error("missing required arguments: " + ", ".join("--" + k for k in missing))
    out, err = gate.out_path(args.root, args.json_out)
    if err:
        print(json.dumps({"reason": err}))
        return 2
    code, receipt = gate.main_guard(
        lambda: evaluate(args.root, args.freeze, args.rev, args.profile,
                         not args.no_battery))
    gate.emit(receipt, out)
    return code


# --- selftest ---------------------------------------------------------------------

def selftest():
    root, err = gate.scratch("kaidoku-r48-c2-selftest-")
    if err:
        print(json.dumps({"reason": err}))
        return 2
    print(json.dumps({"note": "record2's clauses are exercised against the lane's own "
                              "history by the round-48 controls and wave seats; this "
                              "selftest checks the parsers only",
                      "corr_parse": bool(CORR.match(
                          "- corrects axes depth: 24/24 — forged")),
                      "quote_parse": QUOTE.findall("atoms 42, exempted 1"),
                      "receipt_parse": RECEIPT.findall(
                          "`.ufo/waves/round-47/l1/scores/c2-at-A7.json`")}, indent=1))
    shutil.rmtree(root, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
