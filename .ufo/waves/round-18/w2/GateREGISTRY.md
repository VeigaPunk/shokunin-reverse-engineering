BROKEN — I reproduced both disjuncts. An 80-byte token commit on the red baseline closes R17-REGISTRY without fixing it (F1). At REV, several SKILL.md-only commits re-open the routed defect while `routed-defects.py --strict` exits 0 with `open_count` 0 (F2–F6).

# GateREGISTRY — falsify routed-defects.py R17-REGISTRY (round 18, wave 2)

Seat: author-side advisory (falsify), read-only. REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, BASE `9011581d84527ba34c675f9cf912e54d2e72d470`. Axes: calibration (does the verdict track the defect), operability (every finding ships a reproducing command), depth (10 attack commits plus a rendered-view check).

**Calibration up front (observation).** The REV content is a real fix. SKILL.md:540-542,545 carry `Pinned values:` and `Write scope:` clauses, and :448 is `gate / kaidoku` with `--strict` in the argv. The tool also implements contract.md:41-43 faithfully. What is broken is the check set: it cannot tell that fix from a token edit. So C1's "REGISTRY closed" holds only because of what is in the content. The tool's verdict adds nothing to it.

## Setup (observation)

```
mktemp -d                                                      # → /tmp/tmp.3yL5L8ypc7, exit 0
git clone --no-local /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/tmp.3yL5L8ypc7/lane \
  && git -C /tmp/tmp.3yL5L8ypc7/lane remote remove origin && git -C /tmp/tmp.3yL5L8ypc7/lane remote -v
                                                               # → exit 0, no remotes; clone HEAD b2aad08
sha256sum routed-defects.REV.py <LANE>/.ufo/waves/round-18/tools/routed-defects.py
                                                               # → both 034f5ead5af0bb18…e584b2, exit 0
python3 -I -B routed-defects.REV.py --root lane --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94 --strict  # exit 0, open_count 0
python3 -I -B routed-defects.REV.py --root lane --rev 9011581d84527ba34c675f9cf912e54d2e72d470 --strict  # exit 1, open_count 6
```

At BASE, all 9 R17-REGISTRY checks are false. At REV, all 9 are true. Every attack runs the tool from the REV blob (`git show REV:.ufo/waves/round-18/tools/routed-defects.py`), never from a mutated file. Every attack commit touches only `SKILL.md` (`git diff --name-only` = `['SKILL.md']`).

## Check surface at REV (observation)

- Spec, contract.md:41-43: the four rows' 5th cell must contain `Write scope:`, and the citation-drift row's 2nd cell must start with `gate`. That is all the spec requires.
- Named check (routed-defects.py:672): `"Write scope:" in r[4]`.
- Substance check (`_scope_cell_ok`, :628-646): `cell.find("Write scope:")` followed by at least 3 words from `tail.split()` (:631-637). Then every backticked token starting with `.ufo/` or `corpus/` must exist at REV (:639-643, prefix test at :641).
- citation-drift (:688-698): a named check only, `r[1].startswith("gate")` (:695). There is no substance check.
- Row discovery (:617-625): any line in SKILL.md that starts with `|` and whose first naive cell equals the name. Cells come from a plain `split("|")` (:142-143).
- What is never checked: any pinned-value path, which is half of the routed text (lessons/round-17-verifier-spotcheck.md:145). Also unchecked: the four rows' kind, citation-drift's entry and exit map, and the rendered Markdown structure.
- Coverage at REV (eval over the REV rows): the existence test touches 4 tokens in total. Three sit in go-route-compare's *Pinned values* clause and one in receipt-validate's write scope. pins and go-buildinfo-probe have no testable token, so their substance check is just the ≥3-word count.

## Reproduction and results (observation)

```
python3 -I -B /tmp/tmp.3yL5L8ypc7/attack.py /tmp/tmp.3yL5L8ypc7/lane /tmp/tmp.3yL5L8ypc7      # exit 0 (harness: Appendix A)
```

Harness output, verbatim:

```
tool /tmp/tmp.3yL5L8ypc7/routed-defects.REV.py sha256=034f5ead5af0bb1844f9d71c5460e9684b75f6550e820f8c2bf1d46e4de584b2
A1 on 9011581 -> cbbbf748896d files=['SKILL.md'] 1 file changed, 5 insertions(+), 5 deletions(-); --strict exit=1 open_count=5 R17-REGISTRY open=False (named_open=False, substance_open=False)
A2 on b2aad08 -> 4e0f27196aa7 files=['SKILL.md'] 1 file changed, 4 insertions(+), 4 deletions(-); --strict exit=0 open_count=0 R17-REGISTRY open=False (named_open=False, substance_open=False)
A3 on b2aad08 -> 3810e66d5819 files=['SKILL.md'] 1 file changed, 5 insertions(+), 5 deletions(-); --strict exit=0 open_count=0 R17-REGISTRY open=False (named_open=False, substance_open=False)
A4 on b2aad08 -> c5b6f0964cc1 files=['SKILL.md'] 1 file changed, 1 insertion(+), 1 deletion(-); --strict exit=0 open_count=0 R17-REGISTRY open=False (named_open=False, substance_open=False)
A5 on b2aad08 -> 5cf691561ef8 files=['SKILL.md'] 1 file changed, 1 insertion(+), 1 deletion(-); --strict exit=0 open_count=0 R17-REGISTRY open=False (named_open=False, substance_open=False)
A6 on b2aad08 -> 4a0db675c002 files=['SKILL.md'] 1 file changed, 13 insertions(+), 5 deletions(-); --strict exit=0 open_count=0 R17-REGISTRY open=False (named_open=False, substance_open=False)
A7 on b2aad08 -> f509483a3211 files=['SKILL.md'] 1 file changed, 1 insertion(+), 1 deletion(-); --strict exit=0 open_count=0 R17-REGISTRY open=False (named_open=False, substance_open=False)
A8 on b2aad08 -> de0dc41caf6b files=['SKILL.md'] 1 file changed, 1 insertion(+), 1 deletion(-); --strict exit=0 open_count=0 R17-REGISTRY open=False (named_open=False, substance_open=False)
A8c on b2aad08 -> 094edb6a534c files=['SKILL.md'] 1 file changed, 1 insertion(+), 1 deletion(-); --strict exit=1 open_count=1 R17-REGISTRY open=True (named_open=False, substance_open=True)
    FAIL substance:skill-scope-pins: scoped paths absent at rev: ['.ufo/no-such-dir']
A9 on b2aad08 -> 862995d21a7a files=['SKILL.md'] 1 file changed, 1 insertion(+), 1 deletion(-); --strict exit=1 open_count=1 R17-REGISTRY open=True (named_open=True, substance_open=False)
    FAIL named:skill-row-citation-drift: 2nd cell is 'probe / kaidoku'
```

The floor token set (A1min) was run separately, reusing the harness helpers. Exit codes are shown:

```
cd $D && git -C lane checkout -q -f -B atk-A1min 9011581d84527ba34c675f9cf912e54d2e72d470 && python3 -I -B -c "
import sys; sys.path.insert(0, '$D'); import attack as a, pathlib
p = pathlib.Path('lane/SKILL.md'); t = p.read_text(encoding='utf-8')
for n in a.SCOPED: t = a.append_cell5(t, n, ' Write scope: a b c')
t = a.sub_in_row(t, 'citation-drift', '| probe / kaidoku |', '| gateprobe / kaidoku |')
p.write_text(t, encoding='utf-8')" && git -C lane -c user.name=GateREGISTRY -c user.email=gate-registry@localhost commit -q -am 'A1min: floor token set' \
 && C=$(git -C lane rev-parse HEAD) && python3 -I -B routed-defects.REV.py --root lane --rev "$C" --strict > a1min.json; echo "strict exit=$?"
# → A1min=5af9bad94b3903c764b9c08801ed44bc6194b9c5; strict exit=1
# → open_count 5 R17-REGISTRY open False named_open False substance_open False
```

At BASE, `--strict` still exits 1 for A1 and A1min because the other five defects stay open. R17-REGISTRY itself flips to closed.

Each diff below is condensed from `git diff <base> <commit> -- SKILL.md`, using `[-old-]{+new+}`. Line numbers are the same at BASE and REV.

| Id | On | SKILL.md change | Bytes | R17-REGISTRY |
|---|---|---|---|---|
| A1min | BASE | `:540,541,542,545` 5th cell `…{+ Write scope: a b c+} \|`; `:448` `\| citation-drift \| {+gate+}probe / kaidoku \|` | +80 | **closed** |
| A1 | BASE | same four cells `{+. Write scope: not yet declared+}`; `:448` `{+gateless +}probe / kaidoku` | +133 | **closed** |
| A2 | REV | removes the four `Pinned values: …` clauses (`:540` the frozen-prediction paths, `:541` receipt digests, `:542` "none (no expected digests…)", `:545` go1.25.0 buildinfo constants) | −547 | **closed** |
| A3 | REV | `:540-542,545` 5th cell := BASE text + ` <!-- Write scope: not yet declared -->`; `:448` `gate`→`gateless probe` | −1454 | **closed** |
| A4 | REV | `:448` `…/expected.json[- --strict-]\`` | −9 | **closed** |
| A5 | REV | `:542` `\| pins \| [-probe-]{+tool+} / kaidoku \|` | −1 | **closed** |
| A6 | REV | `:448,540-542,545` := BASE row with the leading `\| ` stripped; EOF += `<!--` + the five REV rows + `-->` | +3721 | **closed** |
| A7 | REV | `:542` := `…(mutated-file red case) \| Write scope: not yet declared \| Identical bytes at two instants only, never continuity \|`, where the first `\|` is a GFM escaped pipe | −350 | **closed** |
| A8 | REV | `:542` write scope := `only \`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/no-such-dir/\` and \`./corpus/no-such-dir/\`` | −56 | **closed** |
| A8c | REV | control: same edit with `` `.ufo/no-such-dir/` `` | −125 | open (substance) |
| A9 | REV | `:448` `gate`→`probe`, drop ` --strict`, closing sentence → "Registered `probe` … omits `--strict` and cannot exit 1" | −20 | open (named) |

**Rendered check (observation).** Command, exit 0 (Appendix B):
`uv run --no-project --with 'markdown-it-py==4.0.0' python3 -I -B render.py lane <REV> <BASE> <A1> <A2> <A3> <A4> <A5> <A6> <A7> <A8>`

This renders each SKILL.md with CommonMark plus the GFM table rule, then reads the visible cell text; HTML comments are excluded from that text.

- REV: all four rows show `Write scope:` and `Pinned values:` in column 5. citation-drift shows `gate / kaidoku` with `--strict`.
- A2: `Pinned values:` is gone from all four rows.
- A3: four HTML comments. No visible `Write scope:` in any column 5, and citation-drift shows `gateless probe / kaidoku`.
- A4: citation-drift's entry has no `--strict`.
- A5: pins shows `tool / kaidoku`.
- A6: all five rows render from the pipe-less BASE lines: no scope, no pinned values, pins `tool`, citation-drift `probe`. The decoys sit in one invisible comment.
- A7: pins column 5 has no `Write scope:`. Column 4 has it.

## Findings (by severity)

**F1 HIGH — a token-only edit closes the defect on the red baseline (disjunct 1).**
- *Observation:* A1min adds 80 bytes to SKILL.md only, and R17-REGISTRY goes from open to closed (`named_open=False`, `substance_open=False`).
- *Observation:* A1 does the same with text that states the defect outright ("Write scope: not yet declared", kind "gateless probe").
- *Cause:* For REGISTRY, the "substance" set is a word count plus a prefix-gated existence test. That test passes vacuously when there is no token (:631-643).
- *Contradiction:* The tool's docstring (routed-defects.py:10-11) says "tokens alone cannot close it". So does the claims.json amendment C1 (claims.json:37).
- *Selftest gap:* The only REGISTRY substance red case (:1205-1221) uses a 2-word scope ("Write scope: none here", :1209-1210) and a missing `corpus/` path. Both are forms the check already catches.

**F2 HIGH — the defect re-opens at REV while `--strict` exits 0 with open_count 0 (disjunct 2).**
- *A2:* It removes every pinned-value field. That makes lessons :145 true again ("give no pinned-value path…"), and the tool still says closed.
- *Cause:* No REGISTRY check mentions pinned values. `grep -i pinned` hits only other defects (:436-523), and contract.md:41-43 omits the field.
- *A3:* It is the cheapest full re-open. Every element routed in :145-146 is back at its baseline state in the rendered table; the only added bytes are 4 HTML comments and `gateless`.

**F3 MEDIUM — the citation-drift half has no substance check.**
- *A4 (observation):* Deleting ` --strict` (9 bytes) leaves the row registered `gate` on an argv that cannot exit 1. Without `--strict`, `verdict()` returns CLEAN (citation-drift-probe.py:97-98), with `CLEAN, FAILED, CNE = 0, 1, 2` (:74). PROTOCOL.md:378-379 says "A tool that cannot fail is a probe, and is registered as one" (fleet `093c27d`; the working tree equals HEAD). The row's own R17-REGISTRY sentence at SKILL.md:448, "the registered argv carries `--strict` and can exit 1", becomes false. The tool still says closed.
- *[INFERENCE]* A4 is the routed kind/entry mismatch, mirrored.
- *Prefix test:* The kind check accepts `gateless probe` and `gateprobe` (A1, A1min).
- *A9 (calibration, fails closed):* The PROTOCOL-conformant alternative remediation is to keep `probe` and register the non-strict argv. The tool rejects it as open, because contract.md:42-43 hard-codes the single "starts with gate" remedy.

**F4 MEDIUM — row identity and columns are not Markdown-aware (observation via markdown-it-py).**
- *A6:* GFM table rows without a leading pipe still render, but the tool cannot see them (:620). Meanwhile it grades decoy rows inside an HTML comment.
- *A7:* An escaped `\|` keeps the rendered cell intact. The naive split (:143) still splits on it, so the tool reads column 4's text as "5th cell".
- *Implication:* A stricter text rule for each cell would still be defeated unless rows are taken from the rendered registry table.

**F5 LOW — the kind of the four rows is unchecked.**
- *A5:* One byte reverts pins to `tool`, and the tool still says closed.
- *Evidence:* REV SKILL.md:542 attributes "Kind corrected from `tool` to `probe` … (R17-REGISTRY; PROTOCOL row kinds are gate or probe)". PROTOCOL.md:401-402 lists the row field as `gate|probe`.
- *Evidence:* The tool's own closed fixture registers `| pins | tool / k |` (routed-defects.py:924), so the uncorrected kind is the fixture's "closed" state.
- *Why LOW:* The routed text (:145-146) does not name pins' kind.

**F6 LOW — the scope-path existence test is gated by prefix.**
- *A8:* Absolute (`/home/…/.ufo/no-such-dir/`) and `./corpus/…` tokens skip the test, and the tool says closed.
- *A8c control:* The same edit with `.ufo/no-such-dir/` is caught (substance open). So the test is live; it just checks only the `.ufo/` and `corpus/` prefixes (:641).

## Out of scope (observation): the tool's selftest is red at REV

- `python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --selftest` (clone detached at REV) → **exit 1**: `SELFTEST: FAILED closed-fixture-cli: rc=0 opened=['R17-PINMAP', 'R17-PRODUCER-REV'] broken=['receipt-validate-mid-finding', 'producer-revs-are-ancestors']; closed-fixture-inprocess: open_count=1 …; token-only-R17-*: … extra_open=['R17-PINMAP']`.
- Running the copy extracted to /tmp gives the same result.
- The same command on the `eb6c266` blob → **exit 0**, `SELFTEST: CLEAN cases=17`.
- *Cause:* b2aad08 tightened the PINMAP check (:277-283) to require `mid_map_sha256_mismatch` and `mid_map_compare_mismatch`. The closed fixture still ships `FINDING = "mid_map_mismatch"` (:914-916).
- *Consequence [INFERENCE]:* verify.py:157-159 expects every round-18 tool's `--selftest` to exit 0, so the verification pass will record this as red. I did not run verify.py.
- The REGISTRY token-only case still reaches its own target state (`target=(True, False, True)`). It fails only through `extra_open=['R17-PINMAP']`.

## Residual risk and verification gaps

- **[INFERENCE]** At REV, go-route-compare (`1 any mismatch`, :540) and pins (`1 differ`, :542) are registered `probe` although their entries can exit 1. That is the criterion :146 applies to citation-drift. PROTOCOL.md:377-379 defines a gate by comparison against expected values persisted in the repo, which these two lack, so their classification is debatable. This is not a tool defeat, but no check looks at kinds outside citation-drift.
- Rendering was observed with markdown-it-py 4.0.0, not GitHub's cmark-gfm. That GitHub behaves the same for pipe-less rows, `\|` and HTML comments follows from the GFM spec **[INFERENCE]**.
- The scratch SHAs exist only in `/tmp/tmp.3yL5L8ypc7/lane`. A rerun creates new SHAs (timestamps differ), but the verdicts depend only on content.
- I attacked only R17-REGISTRY. In every REV-based attack the other five defects stayed closed (observed).
- Lane safety: lane access was read-only git only (`rev-parse`, `cat-file`, `merge-base`, `show`, `grep`, `log`, `diff`, `clone --no-local` source). There was one `git status --porcelain=v1 -- <3 paths>` (exit 0, empty), which may refresh the `.git/index` stat cache as a side effect. No jj was run, and nothing in the lane was written except this report.
- Install: markdown-it-py 4.0.0 (+1 dependency; uv: "Installed 2 packages"), via `uv run --no-project --with` from PyPI into the uv cache (no global or tool install; uv 0.13.0 was already in ~/.local/bin). Reason: to observe the rendered table for A3, A6 and A7. An earlier `--offline` attempt exited 1 (not cached).

## Appendix A — attack.py (sha256 c904d5e0785fc70be56dfd52fa37e0d0d461ad6abbd02d7cac7ec05ea4655e5a)

Rerun: `D=$(mktemp -d) && git clone -q --no-local /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$D/lane" && git -C "$D/lane" remote remove origin`, save this block as `$D/attack.py`, then `python3 -I -B "$D/attack.py" "$D/lane" "$D"`.

```python
#!/usr/bin/env python3
"""GateREGISTRY (kaidoku r18 w2) falsification harness: R17-REGISTRY checks.

Usage: python3 -I -B attack.py CLONE OUTDIR

CLONE is a `git clone --no-local` of the lane with its origin remote removed.
Each attack is one commit that touches only SKILL.md, on top of BASE (red
baseline) or REV (delivered revision). routed-defects.py is always run from
the REV blob extracted to OUTDIR, never from the clone's working tree.
"""
import hashlib
import json
import os
import subprocess
import sys

REV = "b2aad08ceeee8dd125ce0d316056d8bd766c7f94"
BASE = "9011581d84527ba34c675f9cf912e54d2e72d470"
TOOL_PATH = ".ufo/waves/round-18/tools/routed-defects.py"
SCOPED = ("go-route-compare", "receipt-validate", "pins", "go-buildinfo-probe")
NAMES = SCOPED + ("citation-drift",)
NEG = "Write scope: not yet declared"


def git(clone, *args):
    p = subprocess.run(["git", "-C", clone, *args], capture_output=True,
                       text=True)
    if p.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} rc={p.returncode}: {p.stderr}")
    return p.stdout


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def row_index(lines, name):
    hits = [i for i, l in enumerate(lines)
            if l.startswith("|") and cells(l)[0] == name]
    assert len(hits) == 1, (name, hits)
    return hits[0]


def get_row(text, name):
    lines = text.split("\n")
    return lines[row_index(lines, name)]


def set_row(text, name, new):
    lines = text.split("\n")
    lines[row_index(lines, name)] = new
    return "\n".join(lines)


def sub_in_row(text, name, old, new):
    line = get_row(text, name)
    assert line.count(old) == 1, (name, old)
    return set_row(text, name, line.replace(old, new, 1))


def rebuild(cs):
    return "| " + " | ".join(cs) + " |"


def set_cell(text, name, k, value):
    line = get_row(text, name)
    cs = cells(line)
    assert len(cs) == 5 and rebuild(cs) == line, (name, len(cs))
    cs[k] = value
    return set_row(text, name, rebuild(cs))


def append_cell5(text, name, suffix):
    cs = cells(get_row(text, name))
    return set_cell(text, name, 4, cs[4] + suffix)


PINNED = {
    "go-route-compare": "Pinned values: the frozen prediction it is given "
    "(round 17: `.ufo/waves/round-17/predictions/`, manifest "
    "`.ufo/waves/round-17/predictions/SHA256SUMS`; round 18: "
    "`.ufo/waves/round-18/predictions/`); ",
    "receipt-validate": "Pinned values: the digests recorded in the receipt "
    "itself; no external expected file. ",
    "pins": "Pinned values: none (no expected digests; each entry records "
    "sha256, size and mtime_ns at the instant read). ",
    "go-buildinfo-probe": "Pinned values: the build-info magic and header "
    "constants of go1.25.0 `debug/buildinfo` (keeps the writable-segment "
    "fallback that go1.27.3 removed, S024); ",
}
PINS_SCOPE_REV = ("Write scope: `snapshot --out FILE` writes `FILE.tmp` then "
                  "replaces FILE (no no-clobber check); `compare` writes "
                  "nothing; `--selftest` writes only a removed mkdtemp tree.")


def attacks(base_text):
    base_cell5 = {n: cells(get_row(base_text, n))[4] for n in SCOPED}

    def a1(t):  # on BASE: negated tokens flip closed
        for n in SCOPED:
            t = append_cell5(t, n, ". " + NEG)
        return sub_in_row(t, "citation-drift", "| probe / kaidoku |",
                          "| gateless probe / kaidoku |")

    def a2(t):  # on REV: strip every pinned-value field
        for n, s in PINNED.items():
            t = sub_in_row(t, n, s, "")
        return t

    def a3(t):  # on REV: baseline cell 5 + invisible token; kind still probe
        for n in SCOPED:
            t = set_cell(t, n, 4, base_cell5[n] + " <!-- " + NEG + " -->")
        return sub_in_row(t, "citation-drift", "| gate / kaidoku |",
                          "| gateless probe / kaidoku |")

    def a4(t):  # on REV: registered gate argv loses --strict (cannot fail)
        return sub_in_row(t, "citation-drift", "expected.json --strict`",
                          "expected.json`")

    def a5(t):  # on REV: pins kind back to the non-PROTOCOL `tool`
        return sub_in_row(t, "pins", "| pins | probe / kaidoku |",
                          "| pins | tool / kaidoku |")

    def a6(t):  # on REV: real rows = baseline, no leading pipe; decoys hidden
        decoys = [get_row(t, n) for n in NAMES]
        for n in NAMES:
            t = set_row(t, n, get_row(base_text, n)[2:])
        return t.rstrip("\n") + "\n\n<!--\n" + "\n".join(decoys) + "\n-->\n"

    def a7(t):  # on REV: escaped pipe shifts the naive 5th cell
        line = get_row(t, "pins")
        cs = cells(line)
        new = rebuild(cs[:3] + [cs[3] + " \\| " + NEG, base_cell5["pins"]])
        return set_row(t, "pins", new)

    def a8(t):  # on REV: scoped paths outside the .ufo/ corpus/ prefix test
        return sub_in_row(t, "pins", PINS_SCOPE_REV,
                          "Write scope: only "
                          "`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/"
                          ".ufo/no-such-dir/` and `./corpus/no-such-dir/`.")

    def a8c(t):  # control: same scope with a bare `.ufo/` token -> caught
        return sub_in_row(t, "pins", PINS_SCOPE_REV,
                          "Write scope: only `.ufo/no-such-dir/` files.")

    def a9(t):  # on REV: legitimate alternative fix (probe, no --strict)
        t = sub_in_row(t, "citation-drift", "| gate / kaidoku |",
                       "| probe / kaidoku |")
        t = sub_in_row(t, "citation-drift", "expected.json --strict`",
                       "expected.json`")
        return sub_in_row(
            t, "citation-drift",
            "Registered `gate` from round 18 (R17-REGISTRY): the registered "
            "argv carries `--strict` and can exit 1",
            "Registered `probe` (R17-REGISTRY): the registered argv omits "
            "`--strict` and cannot exit 1")

    return [
        ("A1", BASE, "flip: negated 'Write scope: not yet declared' x4 + "
         "'gateless probe'", a1),
        ("A2", REV, "reopen: strip all four 'Pinned values:' fields", a2),
        ("A3", REV, "reopen: baseline 5th cells + HTML-comment scope token; "
         "'gateless probe'", a3),
        ("A4", REV, "reopen: drop --strict from registered gate argv", a4),
        ("A5", REV, "reopen: pins kind probe -> tool", a5),
        ("A6", REV, "reopen: real rows baseline without leading pipe; REV "
         "rows as decoys inside <!-- -->", a6),
        ("A7", REV, "reopen: escaped pipe moves scope token out of column 5",
         a7),
        ("A8", REV, "reopen: nonexistent scope paths not prefixed .ufo/ or "
         "corpus/", a8),
        ("A8c", REV, "control: nonexistent bare .ufo/ scope path", a8c),
        ("A9", REV, "false-open probe: legitimate probe-kind fix", a9),
    ]


def main():
    clone, outdir = sys.argv[1], sys.argv[2]
    assert git(clone, "remote").strip() == "", "clone still has a remote"
    tool = os.path.join(outdir, "routed-defects.REV.py")
    blob = subprocess.run(["git", "-C", clone, "show", f"{REV}:{TOOL_PATH}"],
                          capture_output=True, check=True).stdout
    with open(tool, "wb") as fh:
        fh.write(blob)
    print(f"tool {tool} sha256={hashlib.sha256(blob).hexdigest()}")
    base_text = git(clone, "show", f"{BASE}:SKILL.md")
    results = []
    for aid, start, desc, fn in attacks(base_text):
        git(clone, "checkout", "-q", "-f", "-B", f"atk-{aid}", start)
        path = os.path.join(clone, "SKILL.md")
        with open(path, encoding="utf-8") as fh:
            old = fh.read()
        new = fn(old)
        assert new != old, aid
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new)
        git(clone, "add", "SKILL.md")
        git(clone, "-c", "user.name=GateREGISTRY",
            "-c", "user.email=gate-registry@localhost", "commit", "-q",
            "-m", f"{aid}: {desc}")
        sha = git(clone, "rev-parse", "HEAD").strip()
        files = git(clone, "diff", "--name-only", start, sha).split()
        stat = git(clone, "diff", "--shortstat", start, sha).strip()
        p = subprocess.run([sys.executable, "-I", "-B", tool, "--root", clone,
                            "--rev", sha, "--strict"],
                           capture_output=True, text=True)
        doc = json.loads(p.stdout)
        reg = next(d for d in doc["defects"] if d["id"] == "R17-REGISTRY")
        res = {"id": aid, "base": start[:7], "commit": sha, "desc": desc,
               "files": files, "shortstat": stat, "strict_exit": p.returncode,
               "open_count": doc["open_count"], "registry_open": reg["open"],
               "registry_named_open": reg["named_open"],
               "registry_substance_open": reg["substance_open"],
               "failing_checks": [f"{c['set']}:{c['name']}: {c['detail']}"
                                  for c in reg["checks"] if not c["ok"]]}
        results.append(res)
        print(f"{aid} on {start[:7]} -> {sha[:12]} files={files} {stat}; "
              f"--strict exit={p.returncode} open_count={doc['open_count']} "
              f"R17-REGISTRY open={reg['open']} "
              f"(named_open={reg['named_open']}, "
              f"substance_open={reg['substance_open']})")
        for f in res["failing_checks"]:
            print(f"    FAIL {f[:160]}")
    with open(os.path.join(outdir, "results.json"), "w") as fh:
        json.dump(results, fh, indent=2, sort_keys=True)
        fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## Appendix B — render.py (sha256 be28cdca4467926040de3e140f346e9f71c297cbf7f9a137c039b2eb4431f4e9)

```python
#!/usr/bin/env python3
"""Render SKILL.md at a commit with markdown-it-py (CommonMark + GFM tables)
and report what a reader sees in the five R17-REGISTRY rows.

Usage: render.py CLONE COMMIT...
Visible text excludes HTML comments (browsers never display them).
"""
import subprocess
import sys
from html.parser import HTMLParser

from markdown_it import MarkdownIt

NAMES = ("go-route-compare", "receipt-validate", "pins", "go-buildinfo-probe",
         "citation-drift")


class Rows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.row, self.cell, self.comments = [], None, None, 0

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            self.row.append("".join(self.cell).strip())
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_comment(self, data):
        self.comments += 1


def main():
    clone = sys.argv[1]
    md = MarkdownIt("commonmark").enable("table")
    for commit in sys.argv[2:]:
        src = subprocess.run(["git", "-C", clone, "show", f"{commit}:SKILL.md"],
                             capture_output=True, text=True, check=True).stdout
        p = Rows()
        p.feed(md.render(src))
        print(f"== {commit[:12]} html_comments={p.comments}")
        for name in NAMES:
            hits = [r for r in p.rows if r and r[0] == name]
            for r in hits:
                c5 = r[4] if len(r) > 4 else ""
                print(f"  {name}: cells={len(r)} kind={r[1]!r} "
                      f"col5_has_write_scope={'Write scope:' in c5} "
                      f"col5_has_pinned_values={'Pinned values:' in c5} "
                      f"col4_has_write_scope={'Write scope:' in r[3]} "
                      f"entry_has_--strict={'--strict' in r[2].split(' (exercised')[0]}")
            if not hits:
                print(f"  {name}: NO rendered table row")


if __name__ == "__main__":
    main()
```

Report: .ufo/waves/round-18/w2/GateREGISTRY.md
