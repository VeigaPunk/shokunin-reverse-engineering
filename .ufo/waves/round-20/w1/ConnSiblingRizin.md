# ConnSiblingRizin — rizin / radare2 / objdump-architecture overlap

Seat: KaidokuR20.ConnSiblingRizin-2 (read-only). Clock at write: `2026-10-20T17:54:18-03:00` (`date -Iseconds`, exit 0).
Axes named: calibration, coverage, depth. No installs or updates.

Scanned bytes of `PROVINCE.md`, `corpus/SOURCES.md`, and `corpus/knowledge/**` match baseline `14f0260ad319ecc26994381b2415d5a999003375` and `refs/heads/main` (`d1d981d2cc041dda4656c5b01d2c8445d8d17124`). Observation: `git status -sb --` those paths printed `## HEAD (no branch)` (exit 0); both `git diff --stat` commands below were empty (exit 0).

## Scan

Token boundary so `authorizing` is not `rizin`. Pattern: `(?<![A-Za-z0-9_])(rizin|radare2|radare|objdump|binutils|rabin2|rz-bin|execute-rizin|list-objdump|inspect-with-objdump|inspect_with_objdump)(?![A-Za-z0-9_])`, case-insensitive, over every text file under the three surfaces in each `*-shokunin` lane (21 lanes; none missing `PROVINCE.md` or `corpus/SOURCES.md`).

```
python3 -I -B - << 'PY'
import os, re
root = "/home/vgpnk/Projects/shokunin"
pat = re.compile(r"(?<![A-Za-z0-9_])(rizin|radare2|radare|objdump|binutils|rabin2|rz-bin|execute-rizin|list-objdump|inspect-with-objdump|inspect_with_objdump)(?![A-Za-z0-9_])", re.I)
lanes = sorted(d for d in os.listdir(root) if d.endswith("-shokunin") and os.path.isdir(os.path.join(root, d)))
text_ext = {".md", ".txt", ".json", ".tsv", ".yml", ".yaml", ""}
print(f"lanes={len(lanes)}")
grand = 0
for lane in lanes:
    base = os.path.join(root, lane)
    files = []
    for rel in ("PROVINCE.md", "corpus/SOURCES.md"):
        p = os.path.join(base, rel)
        if os.path.isfile(p):
            files.append(p)
        else:
            print(f"MISSING {lane}/{rel}")
    kdir = os.path.join(base, "corpus", "knowledge")
    kcount = 0
    if os.path.isdir(kdir):
        for dp, dns, fns in os.walk(kdir):
            dns[:] = [x for x in dns if x != ".git"]
            for fn in fns:
                if os.path.splitext(fn)[1].lower() in text_ext:
                    files.append(os.path.join(dp, fn)); kcount += 1
    else:
        print(f"MISSING {lane}/corpus/knowledge")
    by_file = {}
    for p in files:
        lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
        hits = [i for i, line in enumerate(lines, 1) if pat.search(line)]
        if hits:
            by_file[os.path.relpath(p, root)] = hits
    nh = sum(len(v) for v in by_file.values()); grand += nh
    print(f"{lane} knowledge_files={kcount} scanned={len(files)} hit_lines={nh}")
    for rel, ls in (by_file.items() if lane != "kaidoku-shokunin" else sorted(by_file.items())):
        print(f"  {'SIBLING' if lane != 'kaidoku-shokunin' else 'KAIDOKU'} {rel} lines={ls}")
print(f"TOTAL_HIT_LINES {grand}")
PY
```

Exit 0. `lanes=21`, no `MISSING` lines, `TOTAL_HIT_LINES 55` (kaidoku 54, tsukuroi 1). Sum of the printed `scanned=` fields: 861 (721 sibling knowledge files + 40 sibling province/sources + kaidoku 100).

| lane | knowledge files | hit lines |
|---|---:|---:|
| audio, chousa, game-dev-2d, game-dev-3d, kagi, kake, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi | 18, 29, 5, 33, 24, 22, 15, 30, 32, 35, 225, 40, 26, 35, 27, 6, 8, 36, 27 | 0 each |
| tsukuroi-shokunin | 48 | 1 |
| kaidoku-shokunin | 98 | 54 |

Observation: zero `corpus/SOURCES.md` rows in any lane contain these tokens. Kaidoku `corpus/SOURCES.md` is S001–S039 only (read through `:45`); no rizin, radare, objdump, or binutils row.

Sibling hit, in full: `tsukuroi-shokunin/corpus/knowledge/update-safety-note.md:131` is the package-size cell `` `binutils` | 8.20 | 43.76 `` under "libc / toolchain class" (`:120-131`). Not objdump, not an architecture list, not rizin. Tsukuroi province: host package state (`PROVINCE.md:3-14`); it refuses "binary RE of drivers (→ kaidoku/revenger" (`:26-28`).

## Kaidoku holdings (baseline)

Observation, classified:

- Province names the tools. `PROVINCE.md:13` "host binutils as non-REA fallback readers." `:62` present-list includes `` `objdump` ``, `` `radare2` ``, `` `rizin` ``; absent cell is `` `cabextract` ``, `` `ltrace` ``. `:45` owns the `rea` CLI. `:59` verb-families row uses objdump only as the cross-check for `read-bytes`.
- No baseline knowledge names `execute-rizin-command` or `list-objdump-architectures`. `git grep -c -I -e 'execute-rizin' -e 'list-objdump' -e 'execute_rizin' -e 'list_objdump' 14f0260ad319ecc26994381b2415d5a999003375 -- PROVINCE.md corpus/SOURCES.md corpus/knowledge` → exit 1 (no matches).
- Held REA objdump verb is a different operation. `corpus/knowledge/2026-10-16-l7-06-inspect-with-objdump.md:1,7` — `inspect_with_objdump` `operation:"file_headers"`, argv `objdump -f`, Evidence `ev_aa75cc2e…`. `:10` Unknown: format/architecture metadata `unknown`/`null`; other operations, including disassembly, unestablished. `2026-10-16-l8-01-6p4-symmetry-battery.md:12` — the same tool name is absent on REA 6.4.0 (`-32602`).
- Other objdump lines are host cross-checks (`objdump -d` / `-f`), not an architecture catalogue: `2026-10-13-r3-verb-coverage.md:76,192,209`; `2026-10-13-r7-02-queue-a-ops-2.md:22,40`; `2026-10-13-pe-surface.md:37-42`; plus `r3-node-addons.md`, `r4-14-libsignal.md`, `r4-16-frontier-rescan.md`, `r5-02-call-targets-jq.md`, `r10-01-queue-ops.md` (hit lines in the scan stdout).
- Rizin/radare2 knowledge is an absence snapshot. `2026-10-13-pe-surface.md:65-68` claims `radare2`, `rizin`, `rabin2`, `rz-bin` missing from PATH.

Host check this seat (not a REA run): `command -v objdump` → `/usr/bin/objdump` exit 0; `objdump --version` → `GNU objdump (GNU Binutils) 2.47` exit 0; `command -v rizin` → `/usr/bin/rizin` exit 0; `rizin -v` → `rizin 0.8.2 @ linux-x86-64` exit 0; `command -v radare2` → `/usr/bin/radare2` exit 0; `radare2 -v` → `radare2 6.2.2 +37485 abi:142 @ linux-x86_64` exit 0.

## Does the REA-verb framing stay inside province?

Inference from the observations above: yes for the live verb, if the entry stays on kaidoku's `rea` CLI surface and does not swallow the two neighbors.

- Inside. Kaidoku owns the live `rea` CLI (`PROVINCE.md:45`) and names objdump and rizin as fallback readers (`:62`). Round-1 routing, which kaidoku still cites (`PROVINCE.md:64-71` → `revenger-shokunin/reports/round-1/connector.md:25,33-36`), gives kaidoku "what the `rea` tool currently is" and revenger the frozen receipt ledger (`connector.md:31-36`). `execute-rizin-command` and `list-objdump-architectures` are live CLI verbs. No sibling knowledge entry holds them (scan). Opening SOURCES rows does not collide: sibling SOURCES hit count is 0. W1 drafts already queued for L1, not yet corpus: `w1/SourceObjdumpDocs.md:42` (manual `-i` = architectures and object formats for `-b`/`-m`) and `w1/SourceRizinDocs.md:63-64` (book tier B, v0.8.2 source tier A).
- Not inside if blurred. `list-objdump-architectures` is not `inspect_with_objdump` `file_headers` (`l7-06:7` is `objdump -f`; `:10` leaves architecture metadata unknown). Rizin 0.8.2 is not radare2 6.2.2 (two binaries above). A binutils package-size or upgrade fact is tsukuroi's (`update-safety-note.md:131`, `PROVINCE.md:13-14,26-28`), not an objdump-architecture claim. Revenger's current province text still says it owns reverse engineering "using the REA skill and its toolset" and the `rea` CLI (`revenger-shokunin/PROVINCE.md:3-16`) while its knowledge scan is 0 hits and its own connector assigns the live surface to kaidoku.

## Contradictions (not scored away)

1. Revenger `PROVINCE.md:3-16` claims the REA toolset; `reports/round-1/connector.md:31-36` and kaidoku `PROVINCE.md:64-71` assign the live surface to kaidoku and ledger identity to revenger. Keyword overlap on these three tools is empty; the texts still disagree about who owns "REA" in general.
2. `pe-surface.md:65-68` (rizin/radare2 absent, 2026-10-13) vs `PROVINCE.md:62` (both listed present) vs this seat's `command -v` exit 0. Same lane, two presence claims.
3. Tsukuroi hands "binary RE" to both kaidoku and revenger (`PROVINCE.md:26-28`) and separately owns `binutils` as a package row (`update-safety-note.md:131`). That names the dual ownership again; it does not say who owns `objdump -i`.

## One move

Admit the two C2 verbs as kaidoku live-CLI entries only, each with a new SOURCES row after S039 (placeholders already in the w1 drafts; no sibling row to cross-cite). The entry header states four limits: not revenger's frozen receipts (`connector.md:35`); not `file_headers` / `objdump -f` (`l7-06:7,10`); not radare2; not tsukuroi's binutils package (`update-safety-note.md:131`). Point rizin presence at `PROVINCE.md:62`, and cite `pe-surface.md:65-68` only as the 2026-10-13 absence snapshot.

Affected axes: calibration (keeps the three tools and three owners apart; does not treat the revenger province sentence as a duplicate entry), coverage (first SOURCES rows; zero collisions). Depth unchanged: the move blocks counting `file_headers` as the architecture list.

## Risks

- Writing "kaidoku owns all REA" would contradict `connector.md:31-36` and revenger `PROVINCE.md:3-16`. The move is the live verb only.
- Book pages in `SourceRizinDocs.md:10-12` are unversioned; the manual row (`SourceObjdumpDocs.md:42`) does not state output format. Using either draft as proof of REA's parser would overclaim. Verb behavior stays a run receipt.
- Leaving `pe-surface.md:65` uncited lets a later reader treat rizin as absent.

## Verification (for the integrator; not run here)

Re-run the token scan: sibling hit lines stay 1, and that line stays `update-safety-note.md:131`. New SOURCES ids are not S001–S039. Each new knowledge entry names `execute-rizin-command` or `list-objdump-architectures`, and does not claim `file_headers`, radare2, or a binutils upgrade. `verb-coverage.py` is the counter (`claims.json` C2).

## Commands (exit codes)

- Token scan `python3 -I -B` as above → exit 0; `TOTAL_HIT_LINES 55`.
- `git -C …/kaidoku-shokunin rev-parse refs/heads/main` → `d1d981d2cc041dda4656c5b01d2c8445d8d17124`, exit 0.
- `git -C …/kaidoku-shokunin rev-parse 14f0260ad319ecc26994381b2415d5a999003375` → same hash, exit 0.
- `git diff --stat 14f0260ad319ecc26994381b2415d5a999003375 -- PROVINCE.md corpus/SOURCES.md corpus/knowledge` → empty, exit 0.
- `git diff --stat 14f0260ad319ecc26994381b2415d5a999003375 refs/heads/main --` those paths → empty, exit 0.
- `git status -sb --` those paths → `## HEAD (no branch)`, exit 0.
- `git grep` of the four verb spellings at `14f0260` on those paths → exit 1.
- `command -v` / version probes above → exit 0 each.
- `date -Iseconds` → `2026-10-20T17:54:18-03:00`, exit 0.
