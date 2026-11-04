#!/usr/bin/env python3
"""Adversarial probe of the frozen round-84 prefreeze gate (blob at a5663dde)."""
import hashlib
import importlib.util
import json
import subprocess

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "a5663ddedd157bb9113928f5fe80509d6f3fc7a1"
SRC = "/fast/scratch/hyaku/kaidoku-r84/ReviewerC1/freeze-precheck-frozen.py"

body = subprocess.run(["git", "-C", ROOT, "show", f"{REV}:tools/round-84/freeze-precheck.py"],
                      capture_output=True, check=True).stdout
open(SRC, "wb").write(body)
print("frozen_module_sha256", hashlib.sha256(body).hexdigest())

spec = importlib.util.spec_from_file_location("fp", SRC)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def blob(path):
    done = subprocess.run(["git", "-C", ROOT, "show", f"{REV}:{path}"], capture_output=True)
    return done.stdout if done.returncode == 0 else None


def text(path):
    return blob(path).decode("utf-8")


r83 = text(".ufo/waves/round-83/claims.json")
r84 = text(".ufo/waves/round-84/claims.json")

FP = "tools/round-84/freeze-precheck.py"
MC = "tools/round-84/mutation-closure.py"
NS = "tools/round-84/nested-sqfs.py"
DIG = {p: hashlib.sha256(blob(p)).hexdigest() for p in (FP, MC, NS)}
CBA = "tools/round-83/attribution-audit.py"
DIG[CBA] = hashlib.sha256(blob(CBA)).hexdigest()
print("attribution-audit digest at rev", DIG[CBA])


def score(obj_or_text):
    t = obj_or_text if isinstance(obj_or_text, str) else json.dumps(obj_or_text)
    return m.check_container(t, "fixture", blob)


def show(name, result):
    print(f"{name:46s} {result['verdict']:8s} {result['findings']}")


print("\n== baseline")
show("round-83 container", score(r83))
show("round-84 container", score(r84))

print("\n== soundness: path outside the predicate satisfies the gate")
r83_obj = json.loads(r83)
r83_kill = json.loads(r83)
r83_kill["claims"][0]["kill_rule"] += f" Counter {CBA} stays frozen."
show("round-83 + path appended to kill_rule", score(r83_kill))
r83_id = json.loads(r83)
r83_id["claims"][0]["id"] = CBA
show("round-83 with path only in claim id", score(r83_id))
r83_axis = json.loads(r83)
r83_axis["claims"][0]["axis"] = "calibration (" + CBA + ")"
show("round-83 with path only in claim axis", score(r83_axis))
neg = json.loads(r83)
neg["claims"][0]["predicate"] = f"This claim does not run {FP}; it states the condition only."
neg["instruments"] = {FP: DIG[FP]}
show("negated mention of another pinned script", score(neg))

print("\n== benign false refusals of otherwise valid containers")
valid = {"instruments": {FP: DIG[FP]}, "claims": [
    {"id": "X", "predicate": f"Counter {FP} scores it."}]}
show("valid baseline fixture", score(valid))
perclaim = {"claims": [{"id": "X", "predicate": f"Counter {FP} scores it.",
                        "counter": {FP: DIG[FP]}}]}
show("pin carried inside the claim object", score(perclaim))
abs_ = {"instruments": {FP: DIG[FP]}, "claims": [
    {"id": "X", "predicate": f"Counter /home/vgpnk/Projects/shokunin/kaidoku-shokunin/{FP} scores it."}]}
show("counter named by absolute path", score(abs_))
dot = {"instruments": {FP: DIG[FP]}, "claims": [
    {"id": "X", "predicate": f"Counter ./{FP} scores it."}]}
show("counter named as ./tools/...", score(dot))
nonscript = {"instruments": {FP: DIG[FP]}, "claims": [
    {"id": "X", "predicate": "Counter tools/round-84/claims.json scores it."}]}
show("counter is a JSON receipt, not a script", score(nonscript))
outside = {"instruments": {"bin/counter.py": "0" * 64}, "claims": [
    {"id": "X", "predicate": "Counter bin/counter.py scores it."}]}
show("counter outside tools|corpus|.ufo", score(outside))
two = {"instruments": {FP: DIG[FP]}, "claims": [
    {"id": "X", "predicate": f"Counter {FP}; target {MC} stays frozen."}]}
show("counter + unpinned producer path", score(two))
show("empty claims", score({"instruments": {FP: DIG[FP]}, "claims": []}))
show("unparsable", score("{not json"))
show("near-miss extension y.python", score({"instruments": {FP: DIG[FP]}, "claims": [
    {"id": "X", "predicate": "Counter tools/round-84/freeze-precheck.python scores it."}]}))
show("near-miss extension y.pyc", score({"instruments": {FP: DIG[FP]}, "claims": [
    {"id": "X", "predicate": "Counter tools/round-84/freeze-precheck.pyc scores it."}]}))

print("\n== cheap control")
for name, t in (("round-83", r83), ("round-84", r84),
                ("instruments only, zero claims", json.dumps({"instruments": {"x": "y"}})),
                ("claims only", json.dumps({"claims": [{"id": "X", "predicate": "x"}]})),
                ("empty instruments", json.dumps({"instruments": {}, "claims": [{"id": "X"}]}))):
    print(f"{name:34s} {m.cheap_rule(t)}")

print("\n== revision fragility (same container, later rev)")
later = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"], capture_output=True,
                       text=True).stdout.strip()


def blob_at(rev):
    def f(path):
        d = subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{path}"], capture_output=True)
        return d.stdout if d.returncode == 0 else None
    return f


print("HEAD", later)
print("round-84 at HEAD", m.check_container(r84, later, blob_at(later)))
