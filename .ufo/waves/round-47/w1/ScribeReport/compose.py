#!/usr/bin/env python3
"""Compose report-draft.md (Work performed + Landed changes) from seat reports.

Honesty rules:
  * a bullet is emitted ONLY from text a seat wrote; the extractor quotes it;
  * a seat with no report.md gets a GAP line, never a result;
  * evidence pointers are the seat dir + report, and any receipt paths named in the report.
"""
import json, os, re, glob, subprocess

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
WAVE = os.path.join(ROOT, ".ufo/waves/round-47")
W1 = os.path.join(WAVE, "w1")
OUT = os.path.join(W1, "ScribeReport", "report-draft.md")

AREAS = [
    ("C1 verification (executors)", ["C1Struct", "C1Ids", "C1Tokens", "C1Digest", "C1Order",
                                      "C1Refs", "C1Battery", "C1SelfTest", "C1FreezeWindow"]),
    ("C2 verification (executors)", ["C2Atoms", "C2Mismatch", "C2Corrections", "C2Vacuity",
                                      "C2CorrGrammar", "C2SelfTest"]),
    ("C1 review (attackers)", ["RevC1Before", "RevC1Ids", "RevC1Tokens", "RevC1Digest",
                                "RevC1Order", "RevC1Refs", "RevC1Last", "RevC1Battery"]),
    ("C2 review (attackers)", ["RevC2Before", "RevC2Scope", "RevC2Exempt", "RevC2Window",
                                "RevC2Axes", "RevC2Dispatch"]),
    ("critique (falsifiers)", ["CritC1Predicate", "CritC1Sizing", "CritC1Order",
                                "CritC2Calibration", "CritC2Corrections", "CritC2Axes",
                                "CritC2Scope", "CritBattery", "CritDigest", "CritGold"]),
    ("mutation (clause deletion / artefact mutation)", ["MutExactClauses", "MutRecordClauses",
                                "MutBlock24", "MutRecordAtoms", "MutCorrections", "MutGate",
                                "MutScratch", "MutExitCodes"]),
    ("cross-seat connectors", ["ConnSeparability", "ConnRouted", "ConnSiblings", "ConnCraft"]),
    ("sentinels (scope / fixtures)", ["SentScope", "SentFixtures"]),
    ("revengers (intent / history)", ["RevIntent", "RevHistory"]),
    ("falsifiable probes", ["LabOrderProbe", "LabWindowProbe"]),
    ("simplifiers (YAGNI)", ["SimplC1", "SimplC2"]),
    ("scouts (maps)", ["ScoutCraftTail", "ScoutSources", "ScoutAxes", "ScoutRounds",
                        "ScoutDispatch", "ScoutCraftBlocks", "ScoutTools", "ScoutState"]),
    ("drafting (scribes)", ["ScribeBlock24", "ScribeCorrections", "ScribeAxesRow",
                             "ScribeLesson", "ScribeQuality", "ScribeSources", "ScribeShonen",
                             "ScribeReport"]),
]

VERDICT_HEADS = re.compile(r"^(#{1,4}\s*[0-9.]*\s*(Verdict|VERDICT|Bottom line|Summary|Seat headline|headline).*)$", re.I)
BOLD_VERDICT = re.compile(r"^\*\*(Verdict[^*]*|VERDICT[^*]*)\*\*\s*(.*)$")
BOLD_ANY = re.compile(r"^\*\*([^*]{3,80})\*\*[.:]?\s+(\S.*)$")


def strip_md(s):
    s = re.sub(r"\s+", " ", s)
    s = s.replace("`", "")
    s = re.sub(r"\*\*|__", "", s)
    return s.strip(" *-—:")


def first_sentence(s, limit=260):
    s = strip_md(s)
    if len(s) <= limit:
        return s
    cut = s[:limit]
    m = re.search(r"[.;]\s", cut)
    if m and m.start() > 80:
        return cut[:m.start()] + "…"
    return cut.rstrip() + "…"


def extract_verdict(text):
    """Return (quote, kind) where kind is one of verdict/heading/none."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = BOLD_VERDICT.match(line.strip())
        if m:
            parts = [m.group(2).strip()]
            for l in lines[i + 1:i + 4]:
                t = l.strip()
                if not t or t.startswith(("#", "|", "```")):
                    break
                parts.append(t)
                if re.search(r"[.]\s*$", t):
                    break
            rest = " ".join(x for x in parts if x)
            return first_sentence(rest), "verdict"
        m = VERDICT_HEADS.match(line.strip())
        if m:
            body = []
            for l in lines[i + 1:]:
                if l.strip().startswith("#"):
                    break
                t = l.strip()
                if t.startswith("|") or t.startswith("```"):
                    continue
                if t:
                    body.append(t)
                elif body:
                    break
            if body:
                return first_sentence(" ".join(body)), "heading"
    # a bold opener anywhere that states a result (first two such lines)
    for i, line in enumerate(lines):
        m = BOLD_ANY.match(line.strip())
        if line.strip().startswith("|"):
            continue
        if m and re.search(r"verdict|finding|conclu|result|attack|fires|holds|fails|green|red",
                           m.group(1), re.I):
            cand = m.group(2).strip()
            if cand and len(cand) >= 40 and not cand.startswith(("(", "see", "§")):
                return first_sentence(cand), "bold"
    # fall back to a section heading + its first sentence, preferring a result-bearing one
    order = [i for i, l in enumerate(lines)
             if re.match(r"^##\s+\d", l.strip())
             and re.search(r"verdict|finding|result|attack|net|conclusion|headline|bottom",
                           l.strip(), re.I)]
    order += [i for i, l in enumerate(lines) if re.match(r"^##\s+\d", l.strip()) and i not in order]
    for i in order:
        if True:
            head = re.sub(r"^#+\s*", "", lines[i].strip())
            body = []
            for l in lines[i + 1:]:
                if l.strip().startswith("#"):
                    break
                t = l.strip()
                if t.startswith("|") or t.startswith("```"):
                    continue
                if t:
                    body.append(t)
                elif body:
                    break
            if body:
                return f"§{head} — {first_sentence(chr(32).join(body))}", "section"
    return None, "none"


def named_receipts(text):
    hits = set()
    for m in re.finditer(r"(receipts?/[A-Za-z0-9_.\-/]+|\.ufo/waves/round-47/w1/[A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)*)", text):
        p = m.group(1).rstrip(".,;:)`")
        last = p.rsplit("/", 1)[-1]
        if p.startswith(".ufo/") and "." in last and not last.endswith(".md"):
            hits.add(p)
    return sorted(hits)[:4]


def git(*args):
    r = subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True)
    return r.stdout.strip()


def main():
    spec = {i["name"]: i for i in json.load(open(os.path.join(WAVE, "w1-spec.json")))["items"]}
    head = git("rev-parse", "HEAD")
    head_sub = git("log", "-1", "--format=%s", head)
    base = git("rev-parse", "13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5")

    rows = {}
    for name in spec:
        d = os.path.join(W1, name)
        rp = os.path.join(d, "report.md")
        if os.path.exists(rp):
            text = open(rp, encoding="utf-8", errors="replace").read()
            q, kind = extract_verdict(text)
            rows[name] = {"report": True, "quote": q, "kind": kind,
                          "bytes": len(text), "receipts": named_receipts(text)}
        else:
            arts = sorted(os.listdir(d)) if os.path.isdir(d) else []
            rows[name] = {"report": False, "artifacts": arts}

    n_rep = sum(1 for r in rows.values() if r["report"])
    gaps = [n for n, r in rows.items() if not r["report"]]

    L = []
    L.append("# round 47 — report draft: Work performed + Landed changes\n")
    L.append("Draft for the L1 (`KaidokuR47`). Generated from the seat directories of")
    L.append("`.ufo/waves/round-47/w1/` at lane tip `%s` (`%s`)." % (head[:8], head_sub))
    L.append("")
    L.append("**Coverage at this draft: %d of %d work items have a `report.md`**; %d are gaps (listed"
             % (n_rep, len(spec), len(gaps)))
    L.append("after the bullets). Every bullet below quotes or paraphrases only what the named seat")
    L.append("wrote; a gap is never upgraded to a result. `w1-results.json`")
    L.append("was %s at generation time." % ("**present**" if glob.glob(os.path.join(WAVE, "*results*.json")) else "**absent**"))
    L.append("")
    L.append("## Work performed\n")

    for area, names in AREAS:
        L.append(f"### {area}\n")
        for name in names:
            r = rows.get(name)
            if r is None:
                L.append(f"- **{name}** — not in the wave's spec roster. GAP.")
                continue
            role = spec[name]["role"]
            if not r["report"]:
                arts = r.get("artifacts") or []
                note = ("%d artifact(s) present: `%s`" % (len(arts), "`, `".join(arts[:6]))) if arts else "no artifacts"
                L.append(f"- **{name}** ({role}) — **GAP: no `report.md`** at draft time; {note}. "
                         f"Evidence: `{os.path.relpath(os.path.join(W1, name), ROOT)}/`.")
                continue
            q = r["quote"]
            if q:
                L.append(f"- **{name}** ({role}) — {q}")
            else:
                L.append(f"- **{name}** ({role}) — report present ({r['bytes']} B); no verdict field "
                         f"in a recognisable form, so no result is asserted here.")
            ev = [f"`{os.path.relpath(os.path.join(W1, name, 'report.md'), ROOT)}`"]
            for p in r["receipts"]:
                ev.append(f"`{p}`")
            L.append(f"  Evidence: {', '.join(ev)}.\n")

    if gaps:
        L.append("### Gaps (no report at draft time)\n")
        L.append("These seats have directories (and in most cases artifacts) but no `report.md`. "
                 "A seat can return through the swarm without writing one, so a gap here is "
                 "**not** a claim that the seat did nothing — it is the absence of a file this "
                 "draft may quote. Nothing they produced is stated as a result above:\n")
        L.append(", ".join(f"`{g}`" for g in gaps) + "\n")

    # ---------------- Landed changes ----------------
    L.append("## Landed changes\n")
    L.append("Derived from git, not from a seat: `git log --format='<hash> <subject>' "
             + base[:8] + ".." + head[:8] + "`.")
    L.append("")
    for c in git("log", "--format=%H|%h|%ad|%s", "--date=iso", f"{base}..{head}").splitlines():
        full, short, when, subj = c.split("|", 3)
        stat = git("show", "--stat=100", "--format=", full)
        files = [l.split(" | ")[0].strip() for l in stat.splitlines() if " | " in l]
        L.append(f"- `{short}` ({when}) — {subj}")
        if files:
            L.append(f"  Files: {', '.join('`%s`' % f for f in files)}.")
        L.append("")
    # ---------------- notes for the L1 ----------------
    tracked = git("ls-tree", "-r", "--name-only", "HEAD", ".ufo/waves/round-47/").splitlines()
    untracked = [l for l in git("status", "--porcelain", "--", ".ufo/waves/round-47/").splitlines()
                 if l.startswith("??")]
    L.append("### Draft notes for the L1 (not part of the report)\n")
    L.append(f"- Wave tree at generation: **{len(tracked)} paths tracked** at `{head[:8]}`, "
             f"**{len(untracked)} untracked**. A bullet whose evidence is still untracked does not "
             f"resolve at a rev, which is exactly what `record.py`'s `path` atom class checks; "
             f"commit the remainder before citing these bullets at a rev.")
    L.append("- C1's counter is green only at `--freeze == --rev` (task freeze `5017e1f7` and every "
             "declared amendment A1–A6 exit 2 `frozen_path_changed`). Cite the freeze as the literal "
             "measured rev and disclose the degenerate pairing — see `ScribeReport.md` F1.")
    L.append("- `record.py` has no freeze guard and its `CORR` regex cannot parse `axes` corrections "
             "(F3/F4): `corrections: 2` is two of the four lines the card carries.")
    L.append("- Every bullet above is a quote from the named seat's own `report.md`; a bullet is "
             "absent, not softened, where the seat had not written one at generation time.")
    L.append(f"- **Count reconciliation:** this draft counts **{n_rep} `report.md` files** "
             f"({len(gaps)} gaps). The L1's landing commit for the wave tree reports a different "
             f"measure (seats that returned). The two are not comparable; use this draft's gap "
             f"list as 'no quotable file', not as 'no work'.\n")
    open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"wrote {OUT}: {n_rep}/{len(spec)} reported, {len(gaps)} gaps")


if __name__ == "__main__":
    main()
