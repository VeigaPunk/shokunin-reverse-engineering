#!/usr/bin/env python3
"""Seat MutBlock24 — row-by-row mutation of landed craft block 24.

Each mutation edits ONE defect class in the marked block (or, for flag order, the
fixture's gate.py), is committed to a one-commit fixture repo built from the
measured revision's own bytes, and is scored by the frozen counter's own
`score()` under `--profile v3` and `--profile v2`.

Usage: python3 mut13.py <lane-root> <rev> <scratch-root> <out.json>
Exit: 0 driver ran; the table is in the JSON. Never a verdict on the block.
"""
import hashlib
import json
import os
import re
import shutil
import sys

LANE, REV, SCRATCH, OUT = sys.argv[1:5]
DET = os.environ.get("DETECTOR") or LANE  # detector bytes, pinned from REV by the caller
sys.path.insert(0, os.path.join(DET, "tools", "round-47"))
sys.path.insert(0, os.path.join(DET, "tools", "round-46"))
import exact  # noqa: E402
import gate  # noqa: E402

MARKER, ORDER, REVERSED = exact.MARKER, exact.ORDER, exact.REVERSED


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def header_line(block):
    return [l for l in block.splitlines() if l.strip().startswith("|")][0]


def row_lines(block):
    lines = [l for l in block.splitlines() if l.strip().startswith("|")]
    return lines[2:]  # header + separator


def replace_row(block, index, cells):
    """Rewrite table row `index` (0-based over data rows) with `cells`."""
    lines = block.splitlines()
    idx = [i for i, l in enumerate(lines) if l.strip().startswith("|")]
    lines[idx[2 + index]] = "| " + " | ".join(cells) + " |"
    return "\n".join(lines)


def cells_of(block, index):
    return exact._cells(row_lines(block)[index])


def set_header(block, header_cells):
    lines = block.splitlines()
    idx = [i for i, l in enumerate(lines) if l.strip().startswith("|")]
    lines[idx[0]] = "| " + " | ".join(header_cells) + " |"
    return "\n".join(lines)


def pin(block, kind):
    pat = exact.MUT_PIN if kind == "mut" else exact.SELF_PIN
    m = pat.search(block)
    return m.group(0) if m else None


# --- the 13 core mutations (categories from the seat spec) ------------------------

def m_token_substring(b):
    rows = [cells_of(b, i) for i in range(len(row_lines(b)))]
    rows = [r[:2] + ["order-ish"] + r[3:] for r in rows]
    out = b
    for i, r in enumerate(rows):
        out = replace_row(out, i, r)
    return out, {}, "every v3-arm cell -> `order-ish` (a superstring of `order`)"


def m_token_synonym(b):
    r = cells_of(b, 0)
    return replace_row(b, 0, r[:2] + ["symbolic"] + r[3:]), {}, \
        "row 1 v3-arm cell -> `symbolic` (a superstring of `symbol`)"


def m_id_duplicate(b):
    rows = [cells_of(b, i) for i in range(len(row_lines(b)))]
    rows.insert(2, ["R46-CL2", "a duplicate trigger cell", "order", "1"])
    return exact.rewrite_rows(b, rows), {}, \
        "a fifth row claims R46-CL2 a second time"


def m_id_two_per_cell(b):
    r = cells_of(b, 0)
    return replace_row(b, 0, [r[0] + " and R46-CL3"] + r[1:]), {}, \
        "row 1 trigger cell names R46-CL2 and R46-CL3"


def m_cells_five(b):
    r = cells_of(b, 1)
    return replace_row(b, 1, r + ["extra"]), {}, "row 2 carries a fifth cell"


def m_cells_three(b):
    r = cells_of(b, 2)
    return replace_row(b, 2, [r[0], r[2], r[3]]), {}, \
        "row 3 drops its v2-hole cell (3 cells, exit moves to index 2)"


def m_exit_out_of_range(b):
    r = cells_of(b, 0)
    return replace_row(b, 0, r[:3] + ["3"]), {}, "row 1 exit cell -> `3`"


def m_exit_word(b):
    r = cells_of(b, 0)
    return replace_row(b, 0, r[:3] + ["met"]), {}, "row 1 exit cell -> `met`"


def m_title_unnumbered(b):
    return b.replace("24. ", "", 1), {}, "title loses its `24. ` number"


def m_marker_duplicated(b):
    return b.replace(MARKER, MARKER + " " + MARKER, 1), {}, \
        "the marker occurs twice inside the block"


def m_header_reordered(b):
    return set_header(b, ["exit", "v3 arm", "v2 hole", "trigger"]), {}, \
        "header cells permuted, rows left positional"


def m_digest_stale(b):
    p = pin(b, "mut")
    stale = hashlib.sha256("\n".join(n for n, _ in exact.MUTATIONS[:3]).encode()).hexdigest()
    return b.replace(p, "mutations_sha256:" + stale, 1), {}, \
        "mutations_sha256 recomputed over three of the four mutations"


def m_pin_mismatch(b):
    p = pin(b, "self")
    return b.replace(p, "interpreter_sha256:" + "0" * 64, 1), {}, \
        "interpreter_sha256 -> 64 zeros"


def m_refs_no_selector(b):
    return re.sub(r"(corpus/lessons/round-46\.md):57-66", r"\1", b, count=1), {}, \
        "first citation loses its line selector"


def m_refs_must_cite(b):
    return b.replace("corpus/lessons/round-46.md", "corpus/lessons/round-45.md"), {}, \
        "every round-46.md citation retargeted to round-45.md (MUST_CITE gone)"


CORE = [
    ("token-substring", "token", m_token_substring),
    ("token-synonym", "token", m_token_synonym),
    ("id-duplicate-row", "id", m_id_duplicate),
    ("id-two-per-cell", "id", m_id_two_per_cell),
    ("cells-five", "cells", m_cells_five),
    ("exit-out-of-range", "exit", m_exit_out_of_range),
    ("title-unnumbered", "title", m_title_unnumbered),
    ("marker-duplicated", "marker", m_marker_duplicated),
    ("header-reordered", "header", m_header_reordered),
    ("digest-stale", "digest", m_digest_stale),
    ("pin-mismatch", "pin", m_pin_mismatch),
    ("refs-no-selector", "refs", m_refs_no_selector),
    ("refs-must-cite-missing", "refs", m_refs_must_cite),
]

# --- supplementary probes (beyond the 13; survival is the interesting result) -----

def m_cells_three_extra(b):
    return m_cells_three(b)


def m_exit_semantics(b):
    r = cells_of(b, 0)
    return replace_row(b, 0, r[:3] + ["0"]), {}, \
        "row 1 exit cell -> `0` (in-range digit, wrong meaning)"


def m_hole_empty(b):
    r = cells_of(b, 1)
    return replace_row(b, 1, [r[0], "", r[2], r[3]]), {}, "row 2 v2-hole cell emptied"


def m_arm_permuted(b):
    a, d = cells_of(b, 0), cells_of(b, 3)
    out = replace_row(b, 0, a[:2] + [d[2]] + a[3:])
    return replace_row(out, 3, d[:2] + [a[2]] + d[3:]), {}, \
        "arm tokens of rows 1 and 4 swapped (still exact vocabulary)"


def m_id_permuted(b):
    a, c = cells_of(b, 0), cells_of(b, 2)
    out = replace_row(b, 0, [c[0]] + a[1:])
    return replace_row(out, 2, [a[0]] + c[1:]), {}, \
        "trigger ids of rows 1 and 3 swapped (each id still exactly once)"


def m_id_substituted(b):
    r = cells_of(b, 3)
    return replace_row(b, 3, ["R46-CL7 " + r[0].split(" ", 1)[1]] + r[1:]), {}, \
        "row 4 trigger -> R46-CL7 (an unrouted id)"


def m_marker_missing(b):
    return b.replace(MARKER + " ", "", 1), {}, "marker removed"


def m_header_renamed(b):
    return set_header(b, ["trigger", "v2 hole", "arm", "exit"]), {}, \
        "header cell `v3 arm` -> `arm`"


def m_digest_absent(b):
    p = pin(b, "mut")
    return b.replace(p, "unpinned", 1), {}, "mutations_sha256 pin removed"


def m_pin_absent(b):
    p = pin(b, "self")
    return b.replace(p, "unpinned", 1), {}, "interpreter_sha256 pin removed"


def m_digest_reordered(b):
    p = pin(b, "mut")
    rev = hashlib.sha256("\n".join(n for n, _ in reversed(exact.MUTATIONS)).encode()).hexdigest()
    return b.replace(p, "mutations_sha256:" + rev, 1), {}, \
        "mutations_sha256 computed over the same names in reversed order"


def m_mutation_name_dropped(b):
    return b.replace("`stale-mutations-digest`, ", "", 1), {}, \
        "one mutation name removed from the prose, digest left correct"


def m_flag_order(b):
    return b, {exact.GATE46: ("gate_order_swapped", None)}, \
        "the fixture's gate.py carries the reversed flag pair"


def m_header_extra_cell(b):
    return set_header(b, ["trigger", "v2 hole", "v3 arm", "exit", "note"]), {}, \
        "header carries a fifth cell"


def m_arm_token_case(b):
    r = cells_of(b, 0)
    return replace_row(b, 0, r[:2] + ["Symbol"] + r[3:]), {}, \
        "row 1 v3-arm cell -> `Symbol` (case differs)"


def m_self_ref_bad_line(b):
    lines = b.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("Refs:"):
            lines[i] = line.rstrip() + ", `tools/round-47/exact.py:9999`"
            break
    return "\n".join(lines), {}, \
        "a citation to the interpreter with a line selector past EOF"


def m_refs_only_self(b):
    lines = b.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("Refs:"):
            lines[i] = ("  Refs: `tools/round-47/exact.py:1`, "
                        "`tools/round-47/exact.py:2`, `tools/round-47/exact.py:3`")
            break
    return "\n".join(lines), {}, \
        "all three citations point at the interpreter itself"


def m_title_renumbered(b):
    return b.replace("24. ", "25. ", 1), {}, "title renumbered `25. `"


def m_mutation_name_extra(b):
    return b.replace("flag-order-drift", "flag-order-drift, fifth-forgery", 1), {}, \
        "a fifth mutation name added to the pinned list prose"


def m_refs_outside(b):
    return b.replace("plans/round-47-claims.md:", "corpus/QUALITY.md:", 1), {}, \
        "first claims citation retargeted outside the validated path set"


def m_refs_unresolvable(b):
    return b.replace("round-46.md:57-66", "round-46.md:57-9999", 1), {}, \
        "first citation line range past EOF"


def m_refs_two(b):
    lines = b.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("Refs:"):
            lines[i] = ("  Refs: `corpus/lessons/round-46.md:57-66`, "
                        "`plans/round-47-claims.md:45-113`")
            break
    return "\n".join(lines), {}, "citations cut to two"


ALL_BLOCKS = []


def m_block23_relabelled(b):
    prev = ALL_BLOCKS[-2]
    text = prev.replace("23. ", "24. ", 1).replace("**", "** " + MARKER, 1)
    return text, {}, "block 23's text relabelled `24. ` with the marker attached"


def m_rows_three(b):
    rows = [cells_of(b, i) for i in range(len(row_lines(b)))]
    return exact.rewrite_rows(b, rows[:3]), {}, "one data row deleted (3 rows)"


def m_arm_all_order(b):
    rows = [cells_of(b, i) for i in range(len(row_lines(b)))]
    rows = [r[:2] + ["order"] + r[3:] for r in rows]
    return exact.rewrite_rows(b, rows), {}, "every v3-arm cell -> `order` (membership, not bijection)"


def m_arm_duplicate_symbol(b):
    rows = [cells_of(b, i) for i in range(len(row_lines(b)))]
    arms = ["symbol", "symbol", "once", "order"]
    rows = [r[:2] + [arms[i]] + r[3:] for i, r in enumerate(rows)]
    return exact.rewrite_rows(b, rows), {}, \
        "arm tokens [symbol, symbol, once, order] — `digest` absent, duplicate `symbol`"


def m_exit_all_two(b):
    rows = [cells_of(b, i) for i in range(len(row_lines(b)))]
    rows = [r[:3] + ["2"] for r in rows]
    return exact.rewrite_rows(b, rows), {}, "every exit cell -> `2` (could-not-evaluate)"


EXTRA = [
    ("exit-semantics-0", "exit", m_exit_semantics),
    ("hole-cell-empty", "cells", m_hole_empty),
    ("arm-permuted", "token", m_arm_permuted),
    ("id-permuted", "id", m_id_permuted),
    ("id-substituted-unrouted", "id", m_id_substituted),
    ("cells-three", "cells", m_cells_three_extra),
    ("marker-missing", "marker", m_marker_missing),
    ("header-renamed", "header", m_header_renamed),
    ("digest-absent", "digest", m_digest_absent),
    ("pin-absent", "pin", m_pin_absent),
    ("title-renumbered", "title", m_title_renumbered),
    ("mutation-name-extra", "digest", m_mutation_name_extra),
    ("refs-outside-allowlist", "refs", m_refs_outside),
    ("refs-unresolvable-line", "refs", m_refs_unresolvable),
    ("refs-two", "refs", m_refs_two),
    ("digest-reordered", "digest", m_digest_reordered),
    ("mutation-name-dropped", "digest", m_mutation_name_dropped),
    ("flag-order-swapped", "digest", m_flag_order),
    ("header-extra-cell", "header", m_header_extra_cell),
    ("arm-token-case", "token", m_arm_token_case),
    ("self-ref-line-past-eof", "refs", m_self_ref_bad_line),
    ("refs-only-self", "refs", m_refs_only_self),
    ("composite-block23-relabelled", "composite", m_block23_relabelled),
    ("rows-three", "cells", m_rows_three),
    ("arm-all-order", "token", m_arm_all_order),
    ("arm-duplicate-symbol", "token", m_arm_duplicate_symbol),
    ("exit-all-two", "exit", m_exit_all_two),
]


def main():
    skill = gate.show(LANE, REV, "SKILL.md")
    if skill is None:
        raise SystemExit("SKILL.md absent at rev")
    blocks = exact.blocks_of(skill)
    marked = [b for b in blocks if MARKER in b]
    if len(marked) != 1:
        raise SystemExit(f"marker blocks {len(marked)} != 1")
    block = marked[0]
    ALL_BLOCKS[:] = blocks
    base = exact._fixture_files(LANE, REV)
    out = {"lane": LANE, "rev": REV, "block_sha256": sha(block),
           "skill_sha256": sha(skill), "block_title": block.split("**", 1)[0],
           "genuine": {}, "core": [], "extra": []}

    def run(name, category, fn, kind):
        try:
            mutated, overrides, desc = fn(block)
        except Exception as exc:  # noqa: BLE001
            out[kind].append({"name": name, "category": category,
                              "error": f"{type(exc).__name__}: {exc}"})
            return
        files = dict(base)
        files["SKILL.md"] = skill.replace(block, mutated, 1)
        if overrides:
            for path, (how, _) in overrides.items():
                body = files.get(path)
                if how == "gate_order_swapped" and body:
                    files[path] = body.replace(ORDER, REVERSED, 1)
        d, frev = exact._repo(files, SCRATCH, prefix="mut-")
        try:
            f = lambda p: gate.show(d, frev, p)  # noqa: E731
            c2, r2 = exact.score(files["SKILL.md"], f, "v2", frev, battery=None)
            c3, r3 = exact.score(files["SKILL.md"], f, "v3", frev, battery=None)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        out[kind].append({
            "name": name, "category": category, "description": desc,
            "mutation_sha256": sha(mutated),
            "v2_exit": c2, "v3_exit": c3,
            "v2_failing": r2.get("failing", r2.get("reason")),
            "v3_failing": r3.get("failing", r3.get("reason")),
            "v3_receipt_sha256": hashlib.sha256(
                json.dumps(r3, sort_keys=True).encode()).hexdigest(),
        })

    # genuine control in the same fixture shape
    files = dict(base)
    d, frev = exact._repo(files, SCRATCH, prefix="genuine-")
    try:
        f = lambda p: gate.show(d, frev, p)  # noqa: E731
        for prof in ("v3", "v2"):
            code, rec = exact.score(skill, f, prof, frev, battery=None)
            out["genuine"][prof] = {"exit": code, "failing": rec.get("failing"),
                                    "met_target": rec.get("met_target")}
    finally:
        shutil.rmtree(d, ignore_errors=True)

    for name, cat, fn in CORE:
        run(name, cat, fn, "core")
    for name, cat, fn in EXTRA:
        run(name, cat, fn, "extra")

    out["core_v3_killed"] = sum(1 for r in out["core"] if r.get("v3_exit") == 1)
    out["core_v2_green"] = sum(1 for r in out["core"] if r.get("v2_exit") == 0)
    out["core_survived_v3"] = [r["name"] for r in out["core"] if r.get("v3_exit") == 0]
    out["extra_survived_v3"] = [r["name"] for r in out["extra"] if r.get("v3_exit") == 0]
    out["core_exit2"] = [r["name"] for r in out["core"] if r.get("v3_exit") == 2]
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps({"rev": REV, "core": len(out["core"]), "extra": len(out["extra"]),
                      "genuine": out["genuine"],
                      "core_v3_killed": out["core_v3_killed"],
                      "core_v2_green": out["core_v2_green"],
                      "core_survived_v3": out["core_survived_v3"],
                      "extra_survived_v3": out["extra_survived_v3"]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
