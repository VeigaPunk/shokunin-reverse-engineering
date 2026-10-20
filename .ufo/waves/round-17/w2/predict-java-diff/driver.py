#!/usr/bin/env python3
"""driver.py -- PredictJavaDiff differential driver (Kaidoku r17 wave 2).

Compares predict.py's GoVer normalization + GoVerRange("1.15-1.25")
containment against the REAL Ghidra 12.1.4 GoVer.java/GoVerRange.java
compiled under /tmp.

Pipeline:
  1. build the corpus (>=200 strings, deterministic)
  2. write corpus.txt (escaped, one per line) next to this file
  3. feed to `java -cp <classes> Harness`, keep java_results.tsv
  4. run predict.py's _strip_go_prefix/gover_parse/gover_is_invalid/
     supported_versions_contains in-process
  5. diff; write results.json + disagreements.tsv next to this file

Python -B only; scratch under /tmp; never executes a carrier.
"""

import json
import subprocess
import sys
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

LANE = Path(__file__).resolve().parent
PREDICT = LANE.parent.parent / "tools" / "predict.py"
CLASSES = Path("/tmp/pjd/classes")

_spec = spec_from_file_location("predict", PREDICT)
predict = module_from_spec(_spec)
_spec.loader.exec_module(predict)


def build_corpus():
    corpus = []
    add = corpus.append

    # --- realistic build-info version strings ------------------------------
    for minor in range(0, 40):
        for patch in (0, 1, 2, 5, 12):
            add(f"go1.{minor}.{patch}")
    for minor in range(10, 30):
        add(f"go1.{minor}")
    for s in (
        "go1.21rc1", "go1.21.0rc2", "go1.22beta1", "go1.25rc3", "go1.26rc1",
        "go1.20beta2", "go1.19rc2", "devel go1.24-abcdef", "devel +abcdef",
        "go1.23.4 X:nodwarf5", "go1.27.2-X:nodwarf5", "go1.25.1 X:tracebacklimit",
        "go1.22.8 X:rangefunc", "go1.19.5 windows/amd64", "go1.20.14 linux/arm64",
        "go2.0.0", "go0.5.0", "go1.0.0", "go1.5.4", "go1.4.2", "go3.1.0",
    ):
        add(s)

    # --- prefix / emptiness / whitespace ----------------------------------
    for s in ("", "go", "g", "og", "goo", "go ", "go\n", "Go1.20", "GO1.20",
              "gogo1.20", "go.go1.20", " go1.20", "go 1.20", "go1.20 ", "go1.20\t",
              "\tgo1.20", "go\t1.20", "go1. 20", "go1 .20", "go1.20 x",
              "go1.20x", "gox", "go1", "go.", "go1.", "go.1.2", "go..2",
              "go1..2", "go1.2.", "go1.2..", "go1.2.3.4", "go1.2.3.4.5.6"):
        add(s)

    # --- integer edge cases ------------------------------------------------
    for s in ("go2147483647.1", "go1.2147483647", "go1.2.2147483647",
              "go2147483648.1", "go1.2147483648", "go1.2.2147483648",
              "go9999999999.1", "go19999999999.1", "go99999999999.1",
              "go42949672960.1", "go1.20.5000000000",
              # leading zeros that keep the value inside int range
              "go1." + "0" * 15, "go" + "0" * 20 + ".1.2",
              "go1." + "0" * 5000, "go" + "0" * 5000 + ".1.2",
              "go1.00000000000.2", "go1.2.00000000000000000000",
              "go1.2.00000000003", "go000000000000.1.2", "go0.0.0",
              "go00.00.00", "go1.20.02147483647", "go00000000000.00000000000",
              "go1." + "0" * 15, "go" + "0" * 20 + ".1.2",
              "go1.2.-3", "go1.2.+3", "go+1.2", "go-1.2", "go1.2-",
              "go1.2e3", "go1.2_0", "go0x1.2", "go1.2,3"):
        add(s)

    # --- line terminators / newlines (Java $ vs Python $, Java . vs .) ------
    for s in ("go1.20\n", "go1.20\n\n", "go1.20x\n", "go1.20x\ny",
              "go1.20x\n\n", "go1.20\nx", "go1.20\r\nx", "go1.20\r\n",
              "go1.20x\r\n", "go1.2\rx", "go1.2\r\r\n", "go1.2x\r",
              "go1.20 ", "go1.20x ", "go1.20 x", "go1.20 ",
              "go1.20x ", "go1.20 ", "go1.20.3\r", "go1.20\rjunk",
              "go1.20.\n", "go1.20x\r\ny",
              "go1.2x\ry", "go1.2x\r\ry", "go1.2\r", "go1.20\r", "go1.20x\r",
              "go1.2\r\n\r\n", "go1.2x\n"):
        add(s)
    # Java line terminators (. can't cross) followed by more text.
    # Terms: \r, NEL, LINE SEPARATOR, PARAGRAPH SEPARATOR.
    for s in ("go1.2x\vy", "go1.2x\fy", "go1.20.\r", "go\r1.2", "go1.\r2",
              "go1.2\x0bx", "go1.2\x0cx"):
        add(s)
    for term in ("\r", chr(0x85), chr(0x2028), chr(0x2029)):
        for s in ("go1.2x" + term + "y", "go1.2" + term + term + "y",
                  "go1.2x" + term, "go1.2" + term, "go1.2x" + term + "\ny",
                  "go1.2x" + term + ".99"):
            add(s)

    # --- unicode / control / astral ---------------------------------------
    for s in ("go١.٢٠", "go１.２０", "go१.२०", "go1.２０",
              "go1.20\x00", "go1.20🙂x", "go1.20é", "goé1.20",
              "go1.20 x", "go1.20　x", "go1.20​x"):
        add(s)

    # dedupe preserving order, keep >=200 guarantee
    seen, out = set(), []
    for s in corpus:
        if s not in seen:
            seen.add(s)
            out.append(s)
    assert len(out) >= 200, len(out)
    return out


def escape(s):
    out = []
    for ch in s:
        o = ord(ch)
        if ch == "\\":
            out.append("\\\\")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif 32 <= o < 127:
            out.append(ch)
        elif o <= 0xFFFF:
            out.append("\\u%04x" % o)
        else:  # astral -> UTF-16 surrogate pair
            u = o - 0x10000
            out.append("\\u%04x\\u%04x" % (0xD800 + (u >> 10), 0xDC00 + (u & 0x3FF)))
    return "".join(out)

def py_side(raw):
    stripped = predict._strip_go_prefix(raw)
    try:
        ver = predict.gover_parse(stripped, 0)
    except Exception as e:
        # gover_parse's contract is "None for INVALID"; a raise here is a
        # defect. run() still maps it to exit 2 via `except ValueError`,
        # so the CLI-level outcome equals INVALID -- record both facets.
        return {"valid": False, "exception": "%s: %s" % (type(e).__name__, e)}
    if ver is None or predict.gover_is_invalid(ver):
        return {"valid": False}
    return {
        "valid": True,
        "ver": list(ver),
        "toString": predict.gover_to_string(ver),
        "inRange": predict.supported_versions_contains(ver),
    }


def main():
    corpus = build_corpus()
    corpus_path = LANE / "corpus.txt"
    corpus_path.write_text(
        "".join(escape(s) + "\n" for s in corpus), encoding="utf-8")

    proc = subprocess.run(
        ["java", "-cp", str(CLASSES), "Harness"],
        stdin=corpus_path.open("rb"),
        capture_output=True, check=True)
    java_lines = proc.stdout.decode("utf-8").splitlines()
    (LANE / "java_results.tsv").write_text(
        "\n".join(java_lines) + "\n", encoding="utf-8")
    assert len(java_lines) == len(corpus), (len(java_lines), len(corpus))

    rows, disagreements, internal = [], [], []
    for i, (raw, jline) in enumerate(zip(corpus, java_lines)):
        f = jline.split("\t")
        assert int(f[0]) == i
        if f[1] == "INVALID":
            java = {"valid": False}
        else:
            java = {"valid": True, "ver": [int(f[2]), int(f[3]), int(f[4])],
                    "toString": f[5], "inRange": f[6] == "true"}
        py = py_side(raw)
        row = {"i": i, "input_escaped": escape(raw), "java": java, "python": py}
        rows.append(row)
        if "exception" in py:
            internal.append(row)
            if py["valid"] != java["valid"]:
                disagreements.append(row)
        elif java != py:
            disagreements.append(row)

    (LANE / "results.json").write_text(
        json.dumps({"count": len(rows), "corpus": corpus, "rows": rows,
                    "disagreements": disagreements,
                    "internal_exceptions": internal},
                   indent=2, sort_keys=True),
        encoding="utf-8")
    (LANE / "disagreements.tsv").write_text(
        "".join("%d\t%s\tJAVA=%s\tPY=%s\n" % (
            r["i"], r["input_escaped"],
            json.dumps(r["java"]), json.dumps(r["python"]))
            for r in disagreements),
        encoding="utf-8")

    print("corpus=%d outcome_disagreements=%d internal_exceptions=%d"
          % (len(rows), len(disagreements), len(internal)))
    for r in disagreements:
        print("  DIFF #%d %r  java=%s  py=%s" % (
            r["i"], corpus[r["i"]], r["java"], r["python"]))
    for r in internal:
        print("  RAISE #%d %r  java=%s  py=%s" % (
            r["i"], corpus[r["i"]], r["java"], r["python"]))


if __name__ == "__main__":
    main()
