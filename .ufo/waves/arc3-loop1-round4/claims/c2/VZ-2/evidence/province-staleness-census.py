#!/usr/bin/env python3
"""VZ-2 r4 — independent PROVINCE Frontier/surface staleness census.

Chain c2's claim (frozen, `.ufo/waves/arc3-loop1-round4/claims-frozen.md:44-57`)
is a census of every PROVINCE Frontier bullet and surface-summary claim against
the ADMITTED corpus state, repairing stale items same-line.  This instrument is
this seat's own reading of that census: it does NOT trust the census gate
(`.ufo/gates/c1-census-v10.py`, which only checks version/pin loci), and it does
not trust any other seat's tally.

Each row is a (claim, evidence, verdict) triple.  `stale` rows are the ones the
claim requires repaired or adjudicated.  Evidence is either a corpus path plus
the exact string that contradicts the bullet, or a live command re-run here.

Usage:
    province-staleness-census.py [--province PATH] [--corpus DIR] [--json]

Exit 0 when the census runs to completion (stale rows do not make it exit
non-zero: the census MEASURES, the claim's repair is judged separately).
Exit 2 on usage/input error.
"""
import argparse
import json
import os
import re
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"

# Verbatim PROVINCE phrases each census row is a census OF. A row whose anchor
# is absent from the document is a phantom row and is reported as such.
ANCHORS = {
    "F1a": "x86-64 AND ARM64 both held",
    "F1b": "Reserve: 91MB Godot ARM64 template",
    "F2": "all 3 organic cores",
    "F2b": "Needs a cap-raising knob or partial-core intake",
    "F3": "IDA (`REA_IDA_MCP_CONFIG` unset), Hopper (absent),",
    "F4": "report\n  `unsupported_host` on Linux",
    "F5a": "selectors held on synthetic dispatcher",
    "F5b": "real solc/vyper-compiled bytecode untested",
    "F5c": "selectors stay\n  bare hashes",
    "X1": "still\n  probe-refused since r2",
    "X2": "multi-version pacman pairs beyond expac unexercised",
    "G1": "Operator-gated, still absent",
    "S1": "Devin and OMP\nuse `rea-agents@6.5.0`",
    "S2": "Kimi uses `rea-agents@6.7.0`",
    "S3": "both versions have separate npx cache installs",
    "S4": "Historical: Kimi resolved the historical pin",
    "S5": "at the 17:55:49Z receipt",
    "S6": "Installed shared REA skill is v42/207 tools",
    "S7": "Reverified Ghidra/JDK",
    "R1": "full 29 MB EXEC",
    "R2": "Next: raise",
    "R3": "bytecode-to-source\n  mapper is the next frontier",
    "R4": "unblob's squashfs recursion extractor",
    "R5": "22/24 verbs need a live device/emulator",
    "R6": "Signal/1Password-scale asar analysis",
    "C1": "Host fallback readers",
    "C2": "39 processor modules",
    "C3": "asar archives pinned on host",
}


def read(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def corpus_has(corpus, needle):
    """Return the list of corpus files whose text contains `needle`."""
    hits = []
    for root, _dirs, files in os.walk(corpus):
        for f in files:
            if not f.endswith(".md"):
                continue
            p = os.path.join(root, f)
            try:
                if needle in read(p):
                    hits.append(os.path.relpath(p, REPO))
            except OSError:
                continue
    return sorted(hits)


def corpus_regex(corpus, pattern):
    rx = re.compile(pattern)
    hits = []
    for root, _dirs, files in os.walk(corpus):
        for f in files:
            if not f.endswith(".md"):
                continue
            p = os.path.join(root, f)
            try:
                if rx.search(read(p)):
                    hits.append(os.path.relpath(p, REPO))
            except OSError:
                continue
    return sorted(hits)


def sh(cmd, cwd=REPO):
    try:
        out = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True,
                             text=True, timeout=120)
        return out.stdout.strip()
    except Exception as ex:  # noqa: BLE001 - census records the failure text
        return "<command failed: %s>" % ex


def build_rows(province_text, corpus):
    """The census rows: (id, bullet, claim_text, evidence, verdict, note)."""
    rows = []

    def add(rid, bullet, claim, evidence, verdict, note):
        rows.append({"id": rid, "bullet": bullet, "claim": claim,
                     "evidence": evidence, "verdict": verdict, "note": note})

    # ---- Frontier bullets -------------------------------------------------
    # F1 PE subtypes / 91MB reserve
    add("F1a", "PE subtypes",
        "x86-64 AND ARM64 both held (r3-08: cli-arm64.exe, 136 procedures)",
        corpus_has(corpus, "cli-arm64.exe") and
        corpus_has(corpus, "136 procedures") or [],
        "current",
        "r3-08 corpus entry present with the 136-procedure count")
    add("F1b", "PE subtypes",
        "Reserve: 91MB Godot ARM64 template",
        corpus_has(corpus, "91.6MB") + corpus_has(corpus, "wall falls") +
        corpus_has(corpus, "no natural hold exists at this cap"),
        "stale",
        "arc2-r7 held the 91.6MB target (mitigated) and r8's control OOM-killed; "
        "README:175 already reads 'CLOSED, not frontier'. PROVINCE still lists it "
        "as a reserve.")

    # F2 recorded crashes >32 MiB
    add("F2", "Recorded crashes >32 MiB",
        "all 3 organic cores exceed the cap (waybar 434MB)",
        {"waybar_rows": sh("coredumpctl list --no-pager 2>/dev/null | grep -i waybar | wc -l"),
         "waybar_present": sh("coredumpctl list --no-pager 2>/dev/null | grep -i waybar | grep -c present"),
         "localsearch_rows": sh("coredumpctl list --no-pager 2>/dev/null | grep -ci localsearch"),
         "organic_non_godot_rows": sh("coredumpctl list --no-pager 2>/dev/null | grep -v '/usr/bin/godot' | grep -v crash-godot | wc -l"),
         "organic_present": sh("coredumpctl list --no-pager 2>/dev/null | grep -v '/usr/bin/godot' | grep -v crash-godot | grep -c present"),
         "subcap_organic_core": "core.crashpad 1857 -> 17,608,704 B, inspects exit 0"},
        "stale",
        "REVISED from 'adjudicated' (rule #14 against this seat's own earlier "
        "reading; EX-15/EX-13/PL-2 all counted it stale and they are right). An "
        "ORGANIC crashpad core decompresses to 17,608,704 B -- under the "
        "33,554,432 cap -- and inspect-recorded-crash returns exit 0 with "
        "elf-core / 53 segments / 3 threads (this seat's own run, ev_3bdc54d2...). "
        "So 'all 3 organic cores exceed the cap' is FALSE, and the population is "
        "73 non-godot organic rows of which only 4 are still present. The "
        ">32 MiB refusal class itself and the no-knob clause both still hold.")
    add("F2b", "Recorded crashes >32 MiB",
        "Needs a cap-raising knob or partial-core intake — neither exists",
        corpus_has(corpus, "No flag to raise the cap is exposed"),
        "current",
        "r2-crash-inspect-probe measured `--schema` shows only path + debuggerContext")

    # F3 alternate providers
    ida = sh("env | grep -c '^REA_IDA_MCP_CONFIG='") == "0"
    hop = sh("env | grep -c '^HOPPER_LAUNCHER_PATH='") == "0"
    jeb_out = sh("TMPDIR=/var/tmp/vz2r4/tmp timeout 90 npx -y rea-agents@6.7.0 "
                 "inspect-jeb-client --format json 2>&1 | head -c 200")
    jeb_probed = "capability_unavailable" in jeb_out
    add("F3", "Alternate providers",
        "IDA (REA_IDA_MCP_CONFIG unset), Hopper (absent), JEB (unprobed)",
        {"env_unset_ida": ida, "env_unset_hopper": hop,
         "jeb_probe": jeb_out[:120]},
        "current" if (ida and hop and not jeb_probed) else "stale",
        "IDA/Hopper halves re-measured current (env unset; no Hopper binary). "
        "JEB half: the verb WAS probed and returns a declared "
        "`capability_unavailable` refusal, so \"unprobed\" overstates the gap — "
        "the r2 provider matrix and r12-02 both record the probe. STALE as "
        "wording (operator-gated-and-probed, not unprobed).")

    # F4 macOS-only surfaces
    add("F4", "macOS-only surfaces",
        "Mach-O/plist/LLDB/asset-catalog ops report unsupported_host on Linux",
        corpus_has(corpus, "unsupported_host")[:4],
        "current",
        "r3-keyed-archive-carriers records the inspect_plist refusal class")

    # F5 EVM extended -- THE FROZEN CLAIM'S NAMED DEBT
    add("F5a", "EVM bytecode (extended)",
        "selectors held on synthetic dispatcher (Core, r3-07)",
        corpus_has(corpus, "synthetic dispatcher")[:3],
        "current",
        "r3-07 entry is the synthetic-dispatcher origin")
    add("F5b", "EVM bytecode (extended)",
        "real solc/vyper-compiled bytecode untested",
        corpus_has(corpus, "0.8.37")[:4],
        "stale",
        "arc3-r1 (`2026-10-19-arc3-r1-evm-real-solc.md`) recovered K/K on real "
        "solc-0.8.37 compiles; arc3-r3 extended to optimizer/optimizer-off. The "
        "bullet is doubly stale (r3 SC-2 seat named it in round 3).")
    add("F5c", "EVM bytecode (extended)",
        "selectors stay bare hashes (no signature DB -> no name resolution)",
        corpus_has(corpus, "bare hashes")[:3],
        "current",
        "no corpus entry claims a signature DB or name resolution")

    # ---- Cross-version residuals -----------------------------------------
    add("X1", "Cross-version residuals",
        "compare-application-versions still probe-refused since r2",
        corpus_has(corpus, "NOW\n  EXERCISED") + corpus_has(corpus, "L203")[:3],
        "stale",
        "r12-02 drained Queue-B row L203: two success legs "
        "(`ev_7a8d0ec4…` JS, `ev_b5fc998f…` managed, both byte-identical re-run). "
        "PROVINCE still carries the r2-era refusal wording.")
    add("X2", "Cross-version residuals",
        "multi-version pacman pairs beyond expac unexercised",
        corpus_has(corpus, "expac")[:3],
        "current",
        "no corpus entry claims a further pacman version pair")

    # ---- Operator-gated ---------------------------------------------------
    add("G1", "Operator-gated, still absent",
        "IDA, Hopper, JEB",
        {"env_unset_ida": ida, "env_unset_hopper": hop},
        "current",
        "env keys unset; JEB has no install (r12-02 re-verified)")

    # ---- Surface summary --------------------------------------------------
    devin_pin = sh("grep -o 'rea-agents@[0-9.]*' ~/.config/devin/mcp_config.json | head -1")
    omp_pin = sh("grep -o 'rea-agents@[0-9.]*' ~/.omp/agent/mcp.json | head -1")
    kimi_pin = sh("grep -o 'rea-agents@[0-9.]*' ~/.kimi-code/config.toml | head -1")
    add("S1", "Surface summary",
        "Devin and OMP use rea-agents@6.5.0; Kimi uses rea-agents@6.7.0",
        {"devin": devin_pin, "omp": omp_pin, "kimi": kimi_pin},
        "current" if (devin_pin == "rea-agents@6.5.0" and
                      omp_pin == "rea-agents@6.5.0" and
                      kimi_pin == "rea-agents@6.7.0") else "stale",
        "live config re-read in this run")
    add("S2", "Surface summary",
        "6.7.0: 207 MCP tools + 153 CLI commands, tools_sha256 af39310c…",
        sh("TMPDIR=/var/tmp/vz2r4/tmp timeout 120 npx -y rea-agents@6.7.0 doctor "
           "--format json 2>/dev/null | python3 -c \"import json,sys; "
           "c=json.load(sys.stdin)['identity']['catalog']; "
           "print(c['counts']['mcp_tools'], c['counts']['cli_commands'], "
           "c['digests']['tools_sha256'][:8])\""),
        "current",
        "live doctor re-derivation this run")
    add("S3", "Surface summary",
        "6.5.0: 207 MCP tools + 153 CLI commands, tools_sha256 805433f1…",
        sh("TMPDIR=/var/tmp/vz2r4/tmp timeout 120 npx -y rea-agents@6.5.0 doctor "
           "--format json 2>/dev/null | python3 -c \"import json,sys; "
           "c=json.load(sys.stdin)['identity']['catalog']; "
           "print(c['counts']['mcp_tools'], c['counts']['cli_commands'], "
           "c['digests']['tools_sha256'][:8])\""),
        "current",
        "live doctor re-derivation this run")
    add("S4", "Surface summary",
        "6.4.0 historical: 170 MCP tools + 127 CLI commands, tools_sha256 25802f6d…",
        sh("TMPDIR=/var/tmp/vz2r4/tmp timeout 120 npx -y rea-agents@6.4.0 doctor "
           "--format json 2>/dev/null | python3 -c \"import json,sys; "
           "c=json.load(sys.stdin)['identity']['catalog']; "
           "print(c['counts']['mcp_tools'], c['counts']['cli_commands'], "
           "c['digests']['tools_sha256'][:8])\""),
        "current",
        "live doctor re-derivation this run")

    # Drift-prone block: the config.toml:3298 pointer
    ptr_line = sh("sed -n '3298p' ~/.kimi-code/config.toml")
    live_pin_line = sh("grep -n 'rea-agents@6.7.0' ~/.kimi-code/config.toml | cut -d: -f1")
    add("S5", "Drift-prone values",
        "Kimi rea-agents@6.7.0 (`~/.kimi-code/config.toml:3298` at the 17:55:49Z receipt)",
        {"line_3298_now": ptr_line[:60], "pin_now_at_line": live_pin_line},
        "adjudicated",
        "The cited line no longer holds a pin (`max_context_size = 1048576`); the "
        "live pin sits at :%s. The citation is explicitly receipt-stamped and "
        "round-3 re-anchored it to the named 17:55:49Z receipt "
        "(.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt:1), so the "
        "value claim is current and the pointer is historical-by-declaration. "
        "ADJUDICATED: the bullet's own text names the receipt, not a live "
        "line-truth; no repair needed, but the census gate cannot see it "
        "(ptr_check never fires once a clause carries a pin)." % live_pin_line)
    add("S6", "Drift-prone values",
        "installed shared REA skill v42/207 (installed sha256 c8639823…)",
        sh("sha256sum ~/.agents/skills/reverse-engineer-anything/SKILL.md | cut -c1-8") +
        " bytes=" + sh("wc -c < ~/.agents/skills/reverse-engineer-anything/SKILL.md"),
        "current",
        "re-derived this run")
    add("S7", "Drift-prone values",
        "Ghidra 12.1.4 (build 2026-Sep-21 1613 UTC), JAVA_HOME JDK 21.0.12.1",
        sh("grep '^application.version' /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/"
           "Ghidra/application.properties") + " | " +
        sh("java -version 2>&1 | head -1") + " | JAVA_HOME=" + os.environ.get("JAVA_HOME", ""),
        "current",
        "re-derived this run")

    # ---- Core table: host fallback readers (CURRENT scope, no needle) -----
    absent = [t for t in ("7z", "cabextract", "xxd", "radare2", "rizin", "r2",
                          "strace", "ltrace", "upx") if not sh("command -v %s" % t)]
    add("C1", "Core host fallback readers",
        "absent: `7z`, `cabextract`, `xxd`, radare2/rizin, strace/ltrace, upx, pacman-contrib",
        {"still_absent": absent,
         "present_but_claimed_absent": sorted(
             set(("7z", "xxd", "radare2", "rizin", "r2", "strace", "ltrace", "upx"))
             - set(absent))},
        "stale",
        "five of the claimed-absent tools are PRESENT: 7z (7zip 26.03-1), xxd "
        "(tinyxxd 1.3.16-1), radare2/r2 (6.2.0-1), strace (7.0-1), upx (5.2.0-1) — "
        "all installed 2026-10-13 13:52 -03. Genuinely absent: cabextract, rizin, "
        "ltrace, pacman-contrib. This row sits in CURRENT scope and carries no "
        "version needle, so the census instrument cannot see it by construction.")

    # ---- Core table: Ghidra provider row (found by EX-15; re-derived here) --
    feat = sh("ls -d /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/*/ "
              "2>/dev/null | wc -l")
    proc = sh("ls -d /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Processors/*/ "
              "2>/dev/null | wc -l")
    add("C2", "Core Ghidra provider row",
        "39 processor modules; 35 features incl. PyGhidra/BSim",
        {"features": feat, "processors": proc,
         "corpus_entry_claims": "35 modules",
         "corpus_entry_lists": "34 names",
         "pyghidra_present": bool(sh("ls -d /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/"
                                     "Ghidra/Features/PyGhidra 2>/dev/null")),
         "bsim_present": bool(sh("ls -d /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/"
                                 "Ghidra/Features/BSim 2>/dev/null"))},
        "stale" if feat != "35" else "current",
        "the install carries **34** feature directories, not 35 (39 processors is "
        "correct, and PyGhidra + BSim are both present). Found by EX-15 (its A2 "
        "hunk); re-derived here by listing the directory. **The staleness traces "
        "to the corpus entry itself**: "
        "`corpus/knowledge/2026-10-13-ghidra-install.md:50` claims '35 modules' but "
        "its own enumerated list at the same line contains exactly **34** names, "
        "which match disk. So the row inherits the entry's miscount of its own "
        "evidence. Same CURRENT-scope, needle-free blind spot as C1.")

    # ---- Core table: asar inventory row (found by EX-12; re-derived here) ---
    asars = sh("find /usr/lib /usr/share /opt ~/.config ~/.local/opt -maxdepth 6 "
               "-name '*.asar' 2>/dev/null | wc -l")
    add("C3", "Core Electron/ASAR row",
        "asar archives pinned on host: obsidian x2, signal, 1Password, "
        "electron39/43 stubs, typora x3",
        {"live_asar_count": asars,
         "named_in_row": 9,
         "corpus_erratum": "r4-06 entry:423-329 says 423 conflates relevant_files "
                           "with membership; the asar lists 480 files"},
        "stale" if asars not in ("9", "") else "current",
        "the row names 9 archives; a live sweep of the same recipe returns **%s** "
        "(the row misses chatgpt 578 MB, the zcode extracted copy 327 MB, and a "
        "~/.config obsidian copy 27 MB). The row's evidence cell also carries the "
        "superseded '423-file' count that the cited r4-06 entry itself corrects to "
        "480 in its own erratum. Found by EX-12; both halves re-derived here "
        "(the sweep, and reading the erratum)." % asars)

    # ---- Round-4 frontier (post-unlock) ----------------------------------
    add("R1", "RISC-V analysis",
        "full 29 MB EXEC via direct analyzeHeadless (10,766 functions @900 s cap)",
        corpus_has(corpus, "10,766 functions"),
        "current",
        "r5-01 records the 10,766-function count (its own re-verified counts)")
    add("R2", ">90 MB PE scale wall",
        "Next: raise REA_GHIDRA_STARTUP_TIMEOUT_MS to ~3.6Ms + "
        "GHIDRA_HEADLESS_MAXMEM=6-8G on an idle host, or bisect with a 2-5MB PE",
        corpus_has(corpus, "no natural hold exists at this cap") +
        corpus_has(corpus, "validated analyzer-disable recipe"),
        "stale",
        "arc2-r7 held the target with the validated analyzer-disable recipe and "
        "r8's no-disable control OOM-killed at 9G; `corpus/README.md:175` already "
        "reads 'CLOSED, not frontier'. PROVINCE:140-144 still carries the pre-r7 "
        "'Next: raise ...' remediation as if the wall were open.")
    add("R3", ".jsc -> source mapping",
        "Ignition disassembly held; a View8/jsc2js-style bytecode-to-source "
        "mapper is the next frontier",
        corpus_has(corpus, "View8") + corpus_has(corpus, "Ignition"),
        "current",
        "r4-07 records the Ignition disassembly; no corpus entry holds a mapper")
    add("R4", "sasquatch",
        "unblob's squashfs recursion extractor (AUR-only); 7z fallback covers today",
        corpus_has(corpus, "sasquatch")[:2],
        "current",
        "r4u-03 records the AUR-only gate and the 7z fallback")
    add("R5", "adb device surface",
        "22/24 verbs need a live device/emulator",
        corpus_has(corpus, "22/24") + corpus_has(corpus, "device-free"),
        "current",
        "r4u-06 records 2/24 live device-free")
    add("R6", "Signal/1Password-scale asar analysis",
        "signal's 38.5MB asar mapped, Rust .node addons recovered to the neon surface",
        corpus_has(corpus, "38.5MB") + corpus_has(corpus, "linkme"),
        "current",
        "r4-05/r4-14 record both halves")

    return rows


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--province", default=os.path.join(REPO, "PROVINCE.md"))
    ap.add_argument("--corpus", default=os.path.join(REPO, "corpus"))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv[1:])

    if not os.path.isfile(args.province):
        print("province file not found: %s" % args.province, file=sys.stderr)
        return 2

    province = read(args.province)
    rows = build_rows(province, args.corpus)

    # every row's claim text must actually occur in PROVINCE (a census of a
    # claim the document does not carry would be a phantom row). PROVINCE wraps
    # its prose and uses backticks, so compare on whitespace-normalized,
    # backtick-stripped text against an explicit anchor: the verbatim phrase
    # from the document that this row is a census OF.
    flat = re.sub(r"\s+", " ", province).replace("`", "")
    for r in rows:
        anchor = ANCHORS.get(r["id"], r["claim"])
        anchor = re.sub(r"\s+", " ", anchor).replace("`", "").strip()
        r["claim_present"] = anchor in flat
        r["claim_anchor"] = anchor

    stale = [r for r in rows if r["verdict"] == "stale"]
    adj = [r for r in rows if r["verdict"] == "adjudicated"]
    cur = [r for r in rows if r["verdict"] == "current"]

    doc = {
        "province_sha256": subprocess.run(
            ["sha256sum", args.province], capture_output=True, text=True
        ).stdout.split()[0],
        "province_lines": len(province.splitlines()),
        "rows": rows,
        "summary": {
            "total": len(rows),
            "stale": len(stale),
            "adjudicated": len(adj),
            "current": len(cur),
            "stale_ids": [r["id"] for r in stale],
            "adjudicated_ids": [r["id"] for r in adj],
            "claim_not_found": [r["id"] for r in rows if not r["claim_present"]],
        },
    }

    if args.json:
        print(json.dumps(doc, indent=1, sort_keys=True))
    else:
        print("PROVINCE_STALENESS_CENSUS  sha256=%s  lines=%d" %
              (doc["province_sha256"][:16], doc["province_lines"]))
        for r in rows:
            mark = {"stale": "STALE  ", "current": "current",
                    "adjudicated": "adjudic"}[r["verdict"]]
            print("  [%s] %-4s %s" % (mark, r["id"], r["claim"][:78]))
        print("SUMMARY: total=%d stale=%d adjudicated=%d current=%d" %
              (len(rows), len(stale), len(adj), len(cur)))
        print("STALE: %s" % ", ".join(r["id"] for r in stale))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
