#!/usr/bin/env python3
"""Round-32 a2residual FinalSourceReopen verification. stdlib only."""
import hashlib, json, re, sys
from pathlib import Path

SNAP = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-32/sources")
C1IN = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-32/c1/inputs")
RE = Path("/fast/scratch/hyaku/kaidoku-r32/a2residual/FinalSourceReopen/reopen")

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def wc(s):
    return len(s.split())

results = []
def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))

# ---------- 1. Identity of retained vs live ----------
EXPECT = {
    "arm64x-pe.md": "a9be76a821bc44cc2257c9cfb7f72100257a6ad0e28944f982e6acf6e1092d66",
    "pe-format.html": "d0c584f14a3a464c45f3544d35cd0146cc6bf480aeb2e47ce5c3fcab42a6f0b1",
    "pe-format.md": "b17271a341f9b6e3204cf3f04ed905c25c03fd4cadb7a57bd4aaf38cf56a2fe0",
}
for f, h in EXPECT.items():
    got = sha(SNAP / f)
    check(f"retained:{f}:sha256", got == h, f"got={got[:16]} want={h[:16]}")

LIVE_EXPECT = {
    RE / "loadconfig-arm64ec.s": "c043b74850a4c3033d21fa22701eb808a6b0bd5b46fd2bfab08d4ae43332c0d4",
    RE / "loadconfig-arm64.s": "7c29f128a447f8ce481159961b14932d7011c6af3bc55a1830387d433864ba2d",
    RE / "arm64x-pe.md": "a9be76a821bc44cc2257c9cfb7f72100257a6ad0e28944f982e6acf6e1092d66",
}
for p, h in LIVE_EXPECT.items():
    got = sha(p)
    check(f"live:{p.name}:sha256", got == h, f"got={got[:16]} want={h[:16]}")

# retained c1 inputs equal upstream digests (lesson S098 claim)
for f, h in (("loadconfig-arm64ec.s", "c043b74850a4c3033d21fa22701eb808a6b0bd5b46fd2bfab08d4ae43332c0d4"),
             ("loadconfig-arm64.s", "7c29f128a447f8ce481159961b14932d7011c6af3bc55a1830387d433864ba2d")):
    got = sha(C1IN / f)
    check(f"retained-c1:{f}:sha256", got == h, f"got={got[:16]} want={h[:16]}")

# ---------- 2. Quote support: contiguous, located, <=25 words ----------
def line_of(path, needle, start=1):
    for i, line in enumerate(Path(path).read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if i >= start and needle in line:
            return i, line
    return None, None

QUOTES = [
    # (source file, exact quote, claimed line or None, label)
    (SNAP / "arm64x-pe.md",
     "Arm64X is a new type of binary that can contain both the classic Arm64 code and [Arm64EC code](arm64ec) together.",
     50, "S099 lesson line 50"),
    (SNAP / "arm64x-pe.md",
     "The built Arm64X binary has two sets of code, entry points, and other elements",
     56, "S099 primary line 56"),
    (C1IN / "loadconfig-arm64ec.s", ".xword __chpe_metadata", 20, "S098 line 20"),
    (C1IN / "loadconfig-arm64ec.s", ".rva __hybrid_code_map", None, "S098 line 59-67 range"),
    (C1IN / "loadconfig-arm64ec.s", ".rva __x64_code_ranges_to_entry_points", None, "S098 line 59-67 range"),
    (C1IN / "loadconfig-arm64ec.s", ".rva __arm64x_redirection_metadata", None, "S098 line 59-67 range"),
    (C1IN / "loadconfig-arm64.s", '.section .rdata,"dr"', 1, "S098 paired line 1-5"),
    (C1IN / "loadconfig-arm64.s", ".word 0x140", None, "S098 paired line 1-5"),
    (SNAP / "pe-format.md",
     "Binary format that allows both native ARM64 and ARM64EC code to coexist in the same file.",
     131, "S100 lesson line 131"),
    (SNAP / "pe-format.md",
     "ABI that enables interoperability between native ARM64 and emulated x64 code.",
     130, "S100 reject line 130"),
    (SNAP / "pe-format.md",
     "The load configuration structure has the following layout for 32-bit and 64-bit PE files:",
     1926, "S100 reject line 1926"),
    (SNAP / "pe-format.md",
     "The low 2 bits of the displacement are zero and are not stored.",
     560, "S100 reject line 560"),
    (SNAP / "pe-format.md",
     "The Windows SDK winnt.h header defines the following macros:",
     2174, "S100 reject line 2174"),
]
for path, q, want_line, label in QUOTES:
    ln, raw = line_of(path, q, start=(want_line or 1))
    ok = ln is not None and (want_line is None or ln == want_line) and wc(q) <= 25
    check(f"quote:{label}", ok, f"line={ln} words={wc(q)} contiguous={'yes' if ln else 'NO'}")

# S099 line 64 default-Arm64 appearance (locate only; lesson paraphrase)
arm = (SNAP / "arm64x-pe.md").read_text(errors="replace").splitlines()
check("S099:line64-exists", len(arm) >= 64, f"lines={len(arm)} line64={arm[63][:80]!r}")
check("S099:line50-located", "Arm64X is a new type of binary" in arm[49], arm[49][:100])
# word counts of the two lesson-table quotes
q_s099 = "Arm64X is a new type of binary that can contain both the classic Arm64 code and [Arm64EC code](arm64ec) together."
q_s100 = "Binary format that allows both native ARM64 and ARM64EC code to coexist in the same file."
check("wordcount:S099<=25", wc(q_s099) <= 25, f"{wc(q_s099)} words (markdown tokens counted)")
plain_s099 = "Arm64X is a new type of binary that can contain both the classic Arm64 code and Arm64EC code together."
check("wordcount:S099-plain<=25", wc(plain_s099) <= 25, f"{wc(plain_s099)} words (link flattened)")
check("wordcount:S100<=25", wc(q_s100) <= 25, f"{wc(q_s100)} words")

# S100 HTML side: ARM64X row value 0xA64E near line 968, ARM64EC definition sentence near 964
html_lines = (SNAP / "pe-format.html").read_text(errors="replace").splitlines()
h964 = html_lines[963] if len(html_lines) >= 964 else ""
h968 = html_lines[967] if len(html_lines) >= 968 else ""
h969 = html_lines[968] if len(html_lines) >= 969 else ""
a641_line = next((i for i, l in enumerate(html_lines, 1) if "0xA641" in l), None)
a64e_line = next((i for i, l in enumerate(html_lines, 1) if "0xA64E" in l), None)
check("S100html:ARM64EC-def@964", "ABI that enables interoperability between native ARM64 and emulated x64 code" in h964, f"line964 def={'ABI that enables interoperability between native ARM64 and emulated x64 code' in h964}")
check("S100html:0xA64E@968", "0xA64E" in h968, f"line968 value cell={'0xA64E' in h968}")
check("S100html:quote@969", "Binary format that allows both native ARM64 and ARM64EC code" in h969, f"line969 match={'Binary format that allows both native ARM64 and ARM64EC code' in h969}")
check("S100html:0xA641-located", a641_line is not None and abs(a641_line - 964) <= 8, f"0xA641 at line {a641_line}; 0xA64E at line {a64e_line}")

# ---------- 3. Negative controls: fabricated / off-topic / >25 words must FAIL ----------
def supports(path, quote, want_line=None):
    ln, _ = line_of(path, quote, start=(want_line or 1))
    if ln is None:
        return False, "absent"
    if want_line is not None and ln != want_line:
        return False, f"line mismatch {ln}!={want_line}"
    if wc(quote) > 25:
        return False, f"{wc(quote)} words >25"
    return True, f"line={ln}"

neg = [
    # fabricated: one-word perturbation of the S099 quote
    (SNAP / "arm64x-pe.md",
     "Arm64X is a brand new type of binary that can contain both the classic Arm64 code and [Arm64EC code](arm64ec) together.",
     50, "fabricated-perturbed-S099"),
    # fabricated: fabricated CHPE claim attributed to PE spec
    (SNAP / "pe-format.md",
     "CHPEMetadataPointer is stored at offset 0xC8 in the load configuration directory.",
     None, "fabricated-CHPE-attributed-to-S100"),
    # off-topic: true sentence from the wrong source, checked against pe-format.md
    (SNAP / "pe-format.md",
     "Arm64X is a new type of binary that can contain both the classic Arm64 code and [Arm64EC code](arm64ec) together.",
     None, "off-topic-S099-quote-against-S100"),
    # off-topic: PE-spec sentence checked against arm64x-pe.md
    (SNAP / "arm64x-pe.md",
     "Binary format that allows both native ARM64 and ARM64EC code to coexist in the same file.",
     None, "off-topic-S100-quote-against-S099"),
]
for path, q, wl, label in neg:
    ok, why = supports(path, q, wl)
    check(f"negative:{label}:must-fail", ok is False, f"result={'SUPPORTED(bad!)' if ok else 'fails'} ({why})")

# >25-word quote support check: a contiguous >25-word run ON ONE RAW LINE of TRUE source text
# must be found in bytes (presence) yet fail the <=25 word-count rule.
long_line_no, run26, raw_line = None, None, None
for i, l in enumerate((SNAP / "pe-format.md").read_text(errors="replace").splitlines(), 1):
    w = l.split()
    if len(w) < 27:
        continue
    for k in range(len(w) - 25):
        cand = " ".join(w[k:k + 26])
        if cand in l:
            long_line_no, run26, raw_line = i, cand, l
            break
    if run26:
        break
assert run26 is not None, "no contiguous 26-word raw-line window found"
ok, why = supports(SNAP / "pe-format.md", run26, None)
check("negative:contiguous-26-words-must-fail", (not ok) and "25" in why, f"src_line={long_line_no} words={wc(run26)} support={ok} reason={why}")

# live flip-URL and learn-markdown identities/scope
gh_sha = sha(RE / "pe-format-gh-docs.md")
check("live:pe-format-gh-docs.md:sha256-unchanged", gh_sha == "b17271a341f9b6e3204cf3f04ed905c25c03fd4cadb7a57bd4aaf38cf56a2fe0", f"got={gh_sha[:16]}")
ghl = (RE / "pe-format-gh-docs.md").read_text(errors="replace").splitlines()
ln131 = ghl[130] if len(ghl) >= 131 else ""
check("live:gh-docs:quote-still-at-131", "Binary format that allows both native ARM64 and ARM64EC code to coexist in the same file." in ln131, f"line131 match={('Binary format that allows' in ln131)}")
learn = (RE / "pe-format-learn.md").read_text(errors="replace")
check("scope:learn-md:ARM64EC-def-present", "Binary format that allows both native ARM64 and ARM64EC code to coexist" in learn, "")
check("scope:learn-md:ARM64X-def-present", "ABI that enables interoperability between native ARM64 and emulated x64 code" in learn, "")
check("scope:learn-md:0xA64E-present", "0xA64E" in learn, "")
llines = learn.splitlines()
learn_q_line = next((i for i, l in enumerate(llines, 1) if "Binary format that allows both native ARM64 and ARM64EC code to coexist" in l), None)
check("scope:learn-md:quote-located", learn_q_line is not None, f"ARM64X def at line {learn_q_line} of {len(llines)}")

# ---------- 4. S100 reject scope: absence census + machine types present, all representations ----------
TOKENS = ["CHPEMetadataPointer", "CHPE", "chpe", "MetadataPointer", "CodeMap", "code map", "code-map",
          "0xC8", "0xc8", "200/0xC8"]
files = {
    "pe-format.md(retained)": SNAP / "pe-format.md",
    "pe-format.html(retained)": SNAP / "pe-format.html",
    "pe-format-gh-docs.md(live flip-URL)": RE / "pe-format-gh-docs.md",
    "pe-format-learn.md(live Accept:text/markdown)": RE / "pe-format-learn.md",
    "pe-format.html(live)": RE / "pe-format.html",
}
census = {}
for label, p in files.items():
    text = Path(p).read_text(errors="replace")
    census[label] = {t: text.count(t) for t in TOKENS}
    check(f"absence:{label}:CHPEMetadataPointer==0", text.count("CHPEMetadataPointer") == 0, f"count={text.count('CHPEMetadataPointer')}")
    check(f"absence:{label}:0xC8==0", text.count("0xC8") + text.count("0xc8") == 0, f"count={text.count('0xC8')+text.count('0xc8')}")
    check(f"absence:{label}:CodeMap==0", text.count("CodeMap") == 0, f"count={text.count('CodeMap')}")

# machine-type scope evidence present (not pagewide rejection): ARM64EC + ARM64X definitions
for label in ["pe-format.md(retained)", "pe-format.html(retained)"]:
    p = files[label]
    text = Path(p).read_text(errors="replace")
    check(f"scope:{label}:ARM64EC-def-present", "Binary format that allows both native ARM64 and ARM64EC code to coexist" in text, "")
    check(f"scope:{label}:ARM64X-def-present", "ABI that enables interoperability between native ARM64 and emulated x64 code" in text, "")
    check(f"scope:{label}:0xA64E-present", "0xA64E" in text, "")
    check(f"scope:{label}:0xA641-present", "0xA641" in text, "")

# flip conjunct 2 candidate: any code-map tag/bit-type definition? search "range type"/"low 2 bits" context
gh = Path(files["pe-format-gh-docs.md(live flip-URL)"]).read_text(errors="replace")
check("flip:live-gh-docs:no-CHPEMetadataPointer", "CHPEMetadataPointer" not in gh, "")
learn_md = Path(files["pe-format-learn.md(live Accept:text/markdown)"]).read_text(errors="replace")
check("flip:live-learn-md:no-CHPEMetadataPointer", "CHPEMetadataPointer" not in learn_md, "")
check("flip:live-learn-md:no-0xC8", ("0xC8" not in learn_md) and ("0xc8" not in learn_md), "")

# ---------- 5. HTML drift characterization: captured vs live ----------
a = (SNAP / "pe-format.html").read_text(errors="replace").splitlines()
b = (RE / "pe-format.html").read_text(errors="replace").splitlines()
import difflib
diff = list(difflib.unified_diff(a, b, lineterm="", n=0))
changed = [l for l in diff if l[:1] in "+-" and l[:3] not in ("+++", "---")]
check("drift:html:changed-lines", True, f"captured_lines={len(a)} live_lines={len(b)} diff_lines={len(changed)}")
ts_hits = [l for l in changed if re.search(r"20\d\d-\d\d-\d\d|updated_at|ms\.date|git_commit_id|timestamp|__NEXT_DATA__", l)]
check("drift:html:timestamp-class", True, f"timestamp-ish diff lines={len(ts_hits)} of {len(changed)}")
for l in changed[:6]:
    results.append(("drift:html:sample", True, l[:120]))

# ---------- report ----------
out = []
bad = 0
for name, ok, detail in results:
    if not ok:
        bad += 1
    out.append(f"{'PASS' if ok else 'FAIL'} {name} {detail}")
print("\n".join(out))
print(f"\nTOTAL={len(results)} FAIL={bad}")
with open(RE.parent / "census.json", "w") as fh:
    json.dump(census, fh, indent=1)
sys.exit(1 if bad else 0)
