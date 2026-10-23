# ReviewProvince — round 30, wave 2

Seat: `KaidokuR30.ReviewProvince` (reviewer). Attacked: the round-30 PROVINCE.md addition (`d210fb8f..92b1dd2d`). Questions: does it move the claimed R30-C1 surface into Core without rewriting Core or Frontier, and is the Core row correct?

## Verdict

- **Surface move: MOVED (holds).** Observation. At `d210fb8f` both parts of the claims.json `unmoved_command` print `0`. At `92b1dd2d` they print `3` and `16`.
- **Append-only / Core and Frontier not rewritten: holds.** Observation. The diff is one hunk, `12 0` (12 lines added, 0 deleted), placed after the last line of the base file. The Core table (PROVINCE.md:38-62) and Frontier list (:73-96) are byte-unchanged. PROVINCE.md is also unchanged between `92b1dd2d` and HEAD `3502b94c`, where numstat prints nothing.
- **"Frontier list unchanged" statement: holds.** Observation. No Frontier line appears in the diff. No Frontier bullet at the base names Rust, `.dep-v0`, `auditable` or `inspect-rust-binary`, so no Frontier item should have been retired.
- **Core row cells: hold, except one.** "5 distinct package documents" is wrong: the 16 committed envelopes carry **7** distinct dependency documents, one per wheel. They carry 5 distinct package *lists*. This is a Low finding (F1 below); every other cell matches the entries and the envelopes.

## Command outputs

### Diff

Command: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff d210fb8f 92b1dd2ddc119fda89a611ba515bdf6cfe906f76 -- PROVINCE.md`. Exit 0, 2026-10-23T03:12:02Z. The output is a single hunk `@@ -326,3 +326,15 @@` with only `+` lines. It adds:

- the heading `## Round-30 \`inspect-rust-binary\` positive class and refusal signatures — 2026-10-23`;
- the line "Addition to Core (the Core table above is not rewritten; the Frontier list is unchanged by this round):";
- a one-row table;
- a "Before round 30 …" limits paragraph;
- an R29-C1 provenance correction.

`git diff --numstat` for the same range printed `12	0	PROVINCE.md`, exit 0. Saved as `province.diff`.

### claims.json `unmoved_command` (R30-C1) at both revisions

Command per revision R:

`git -C <LANE> show R:PROVINCE.md | grep -c 'inspect-rust-binary'`

`git -C <LANE> ls-tree -r --name-only R -- corpus/evidence/round-30/c1/envelopes | grep -c '\.json$'`

Run at 2026-10-23T03:14:53Z (first run 03:12:18Z gave the same results).

```
REV=d210fb8fa62d2af04d009cfa0c65a4e8137dc742 UTC=2026-10-23T03:14:53Z
province_count=0
  pipe_exit=0 1
c1_envelopes_json=0
  pipe_exit=0 1
skill_count(C2)=0
  pipe_exit=0 1
REV=92b1dd2ddc119fda89a611ba515bdf6cfe906f76 UTC=2026-10-23T03:14:53Z
province_count=3
  pipe_exit=0 0
c1_envelopes_json=16
  pipe_exit=0 0
skill_count(C2)=4
  pipe_exit=0 0
```

- At the base, grep exits 1 because a count of 0 means no match. That matches the "(0 at base)" annotations in claims.json.
- The C2 `unmoved_command` line (SKILL.md, 0 → 4) is included for completeness only. It is outside this seat's scope.
- Inference: the 3 PROVINCE hits are the new heading (:330), the row (:336) and the limits paragraph (:338). The counter's `province_ok` requires a PROVINCE line that contains both `inspect-rust-binary` and the entry path, and that line must not exist at the base (`tools/round-30/c1-rust-positive.py:158-166`). Row :336 meets both conditions.

## Core row cells against the entries and evidence (all at `92b1dd2d`)

| Cell claim | Check | Result |
|---|---|---|
| Surface "Rust dependency metadata (cargo-auditable `.dep-v0`) via `inspect-rust-binary`" | entry `corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md` title and Claim | holds |
| Ports/keys "none (REA's own … reader, provider-free); `rea-agents@6.5.0`" | envelope `c1/envelopes/macho-arm64-uvx.json`: `/data/provider/id = "rust-auditable"`, `name = "REA Rust dependency reader"`; `runs.tsv` pkg_version `6.5.0`, pkg_json_sha256 `a5003023…` | holds (built-in reader, no external engine or environment key) |
| Probe argv `inspect-rust-binary <image> --format json --full-output` | `c1/runs.tsv` argv column: `npx -y rea-agents@6.5.0 inspect-rust-binary /fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uv --format json --full-output` | holds |
| "`__DATA,.dep-v0` on Mach-O" | macho-arm64-uvx envelope: `auditable_metadata/section_name = "__DATA,.dep-v0"` | holds |
| "16 of 16 uv 0.13.0 PyPI wheel members (ELF x86_64/aarch64/riscv64, PE x86_64/arm64, Mach-O x86_64/arm64)" | `c1/carriers.tsv`: 16 rows over 7 wheels; formats and architectures exactly as listed; entry Results table shows 16 `P1-pass` rows with evidence_ids | holds |
| "package multiset, edges, root, kind, section offset and size equal an independent decode" | P1 predicate (claims.json) and entry Results/Method | holds as worded. Edges are compared through each package's dependency (name, version) set, not as raw index pairs. |
| "19 of 19 code-predicted accept/refuse signatures on ELF mutants" | `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md` Results (19 rows, P2-match), Limits "One container (ELF x86_64)" | holds |
| "decision table in SKILL.md" | `git show 92b1dd2d:SKILL.md` lines 966-994: "Decision table for `inspect-rust-binary` refusals …" | holds |
| "Before round 30 the lane held only `auditable_metadata: null` runs" | `git grep` at `d210fb8f`: every non-null form is the MCP output-schema reference `"auditable_metadata":{"$ref":"#/$defs/__schema20"}` (7 hits in luna-round-2/6 tool listings); run records show `auditable_metadata: null` / `auditable_metadata:null` | holds |
| Limits "one producer (5 distinct package documents across 16 carriers)" | see F1 | **fails as worded** |

## Findings by severity

### F1 — Low — PROVINCE row limits sentence miscounts the dependency documents

- **Path:** `PROVINCE.md:338` at `92b1dd2d`. Quote: "Limits: one producer (5 distinct package documents across 16 carriers), one pin, Linux host".
- **Command:** `timeout 120 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/ReviewProvince/distinct_docs.py 92b1dd2ddc119fda89a611ba515bdf6cfe906f76`. Exit 0, 2026-10-23T03:13:30Z. The script reads the 16 committed envelopes with `git show` and does not run REA.
- **Output excerpt:**
  ```
  distinct (name,version,source) package lists=5
  distinct package lists + edges=7
  distinct package lists + edges + kind/root=7
  ```
  Per-wheel figures, from the same output:

  | Carriers | Edges | Compressed bytes |
  |---|---:|---:|
  | ELF x86_64 | 3041 | 9870 |
  | ELF aarch64 | 3042 | 9871 |
  | Mach-O x86_64 | 2974 | 9666 |
  | Mach-O arm64 | 2975 | 9667 |
  | PE x86_64 | 3013 | 9943 |
  | PE arm64 | 3012 | 9938 |
- **Observation:**
  - The 7 wheels carry 7 different `.dep-v0` documents.
  - Only the (name, version, source) package lists collapse to 5: ELF x86_64 shares a list with ELF aarch64, and Mach-O x86_64 shares one with Mach-O arm64. The two PE lists differ from each other.
  - claims.json `limits` says "5 distinct package lists", which is correct. The entry's Limits line uses both phrasings ("5 distinct package documents" and "5 distinct package lists"). PROVINCE copied the wrong one.
- **Effect:** the row understates the width of the evidence. It does not change the move verdict or any scored quantity.
- **Fix (recommendation):** "5 distinct package lists (7 distinct dependency documents, one per wheel)".

### F2 — Low — The PROVINCE Core-admission convention is not met by LOG at the measured revision

- **Rule:** `PROVINCE.md:31-32` (unchanged since the base): "ground moves to Core only after an end-to-end probe lands a `LOG.md` entry citing its `evidence_id` and subject sha256".
- **Command:** `git show 92b1dd2d:LOG.md | grep -n -i -E 'round-30|R30|inspect-rust|rust'`. Exit 0, 2026-10-23T03:12:2xZ. It returns no round-30 lines; the last section is "## 2026-10-22 — round 29".
- **Observation:** the round-30 LOG entry first appears at HEAD `3502b94c` (2026-10-23T00:11:31-03:00, after `92b1dd2d` at 00:07:42-03:00). That section contains 0 `ev_…` ids, 0 hex digests of 12 or more characters, and 0 references to the r30 entry paths: `git show HEAD:LOG.md | awk '/^## 2026-10-23 — round 30/{f=1} f' | grep -c -E 'ev_[0-9a-f]|[0-9a-f]{12}|2026-10-23-r30-rust'` printed `0`, 2026-10-23T03:14:43Z.
- **Mitigation:**
  - The PROVINCE row points to the entry, which lists every evidence_id plus 12-character sha256 prefixes, and `carriers.tsv` has the full digests.
  - LOG entries from rounds 24-29 also cite no `ev_` ids (awk count over HEAD LOG). Inference: this is lane-wide drift in the convention, not a round-30-only lapse.
- **Effect:** none on the counter, which checks PROVINCE and the entry only, not LOG. It is a documentation-contract gap against PROVINCE's own admission rule.

### F3 — Informational — The new table uses its own column headers

- The appended table's header is `| Surface | Ports / keys | Probe | Verified evidence |`. The Core table (`PROVINCE.md:42`) uses `| Surface | Ports / paths / config keys | Liveness / readiness probe | Verified evidence |`.
- Four columns in the same order, so the meaning is unchanged. Cosmetic only. The "addition section with its own table" pattern itself has precedent: "Round-4 additions to Core", "Round-20 additions to Core".

### Not a finding

- The Frontier bullet "macOS-only surfaces — Mach-O/plist/LLDB/asset-catalog ops report `unsupported_host` on Linux" sits alongside the new row's thin Mach-O class. The Mach-O envelopes are `ok: true` with `format = "mach-o"`, so this op is not one of the macOS-gated ones. Core :55 already holds other Mach-O ops on Linux.
- Inference: the unchanged Frontier bullet does not contradict the row.

## Residual risk and verification gaps

- **Unknown.** I did not re-run either counter or REA. The live 16/16 agreement rests on the after receipts and on the ReRunC1 seat. My checks read only committed bytes, via `git show` / `ls-tree` / `grep`.
- **Text grep only.** No language server applies to Markdown or TSV. The counter's `province_ok` is a token check: any new line containing `inspect-rust-binary` and the entry path passes. That limit is already disclosed in the entry (w1 `CriticTargetsControls.md`), and this seat verified the row's content by hand.
- **Correction paragraph out of scope.** The appended R29-C1 provenance correction (`PROVINCE.md:340`) is outside the asked scope. I did not check it against S088.

## Artifacts

All under `/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReviewProvince/`.

| File | sha256 |
|---|---|
| `distinct_docs.py` | `f58ade899d4f8868917cf1a17b535b6173b6545fe674b4af6d7827583a3944d5` |
| `distinct_docs.out` | `e317950532b90c5de0617f6e6931cdd78cab3a5b2cc1ab0b84cbb0ead718c9d0` |
| `unmoved.out` | `93d507f3ee0ab46e6393716dfae6f8cb80d1241151cb0cf13ec3fc4bdf5e8793` |
| `province.diff` | `f082f9d26e2edc255578aaeae02c79ae8b452d80095fd6abfa3b14909ed6dff7` |

No tools were installed. No REA was run, and no carrier or mutant was opened or executed. No lane file other than this report was written, and nothing was run with git writes.
