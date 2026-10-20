# Round 19 wave 2 — corpus index no-harm review

## Scope and result

Compared baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` with the observed main tip `279e8b19c51658bfd05b9e31a1c0894ab2e70537`. The census uses Git trees and the first-column identifiers in `corpus/README.md`'s `## Knowledge` table, not the mutable worktree.

**Result:** the newly added R19 knowledge file has a matching Knowledge row, and the held Go note is append-only deepened. However, the requested absolute zero-dangling condition does not hold: 17 knowledge files lack a `## Knowledge` entry at both endpoints (pre-existing). The coverage map also gains the R19 identifier, so it is not literally unchanged, although the prior identifiers and their state text remain.

## Findings

### Medium — Knowledge table is not a complete file index at either endpoint (pre-existing)

**Observation:** excluding `.gitkeep`, B contains 96 `corpus/knowledge/*.md` files and 80 `## Knowledge` data rows; 79 distinct corpus-file identifiers occur in those rows. Main contains 97 files and 81 rows; 80 distinct corpus-file identifiers occur. The unindexed file set is unchanged and has 17 members at both revisions:

- `corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md`
- `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md`
- `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`
- `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md`
- `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md`
- `corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md`
- `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md`
- `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md`
- `corpus/knowledge/2026-10-19-arc3-r9-viair-fallback-miss.md`
- `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md`
- `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md`
- `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`
- `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`
- `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md`
- `corpus/knowledge/2026-10-20-r16-go-selection-preview.md`
- `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`
- `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md`

The extra Knowledge-table identifier `lessons/round-13-distillation` (`corpus/README.md:138`) is expressly described there as a `SKILL.md` synthesis, “not a corpus note”; it is not counted as a missing file. Thus the delta itself is balanced—R19 adds one file and one Knowledge row—but the absolute “zero missing/dangling” acceptance is false. The held Go note `2026-10-19-arc3-r12-go-evidence-id-domain.md` is among the 17 not given its own Knowledge-table row, even though the separate Coverage map includes it (`corpus/README.md:41`).

**Inference:** this is an existing index completeness gap, not a regression caused by the R19 addition. If acceptance requires every knowledge file to have a `## Knowledge` row, the delivered state does not meet it.

### Low — Coverage map changed additively, not unchanged

**Observation:** `corpus/README.md:35` changes between B and main: the existing Go compare/analysis group gains `2026-10-20-r19-go125-toolchain-replay`. Main also adds the matching Knowledge row at `corpus/README.md:154` and the round-19 Lessons row at `:170`. The diff removes no identifiers; the existing held-Go membership at `:41` remains.

**Inference:** the prior coverage descriptions were not rewritten or removed, but the Coverage map's indexed set did change by one. This is an additive, correctly paired addition, not literal “coverage ground remains unchanged.” If that phrase means only “do not weaken existing coverage claims,” the diff supports that narrower reading; it does not support byte/identifier-set invariance.

## Deepening of the held Go entry

**Observation:** `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` has a `+41/-0` diff. The existing body ends at the prior scope/limitations; main appends an addendum beginning at line 32 and ending at line 71. The new material records source-row scope, ungrounded claims, custody gaps, current subject-identity drift, and what was checked unchanged. The existing file content is retained; the Coverage-map membership remains at `corpus/README.md:41`.

**Inference:** the held Go evidence note is deepened append-only, without replacing the original measured boundary. This part of the requested no-harm condition is supported, with the indexing caveat above.

## Verification and gaps

- LSP was unavailable: `read xd://lsp` returned “No such tool,” and the mounted-tool inventory contains no LSP device. No LSP status/references/definition/diagnostics were available. This was a documentation/tree census, not a caller analysis.
- No build, tests, formatter, installation, runtime, or carrier execution was performed.
- **Observation:** the working-tree `corpus/README.md` matched main at the earlier check; the report's conclusions are pinned to the explicit Git revisions above, not inferred from other dirty worktree paths.

## Commands and exit codes

```text
git --no-optional-locks rev-parse refs/heads/main
# 279e8b19c51658bfd05b9e31a1c0894ab2e70537; exit 0

git --no-optional-locks merge-base 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 refs/heads/main
# 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0; exit 0

cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B -c 'import re,subprocess; B="8a8da7e19375aadc66c6bcbff0bbcbb596048fb0"; M="279e8b19c51658bfd05b9e31a1c0894ab2e70537"; run=lambda *a: subprocess.run(["git","--no-optional-locks",*a],capture_output=True,text=True);
for rev in (B,M):
 tree=run("ls-tree","-r","--name-only",rev,"--","corpus/knowledge/").stdout.splitlines(); text=run("show",f"{rev}:corpus/README.md").stdout; files={p.removeprefix("corpus/knowledge/")[:-3] for p in tree if p.startswith("corpus/knowledge/") and p.endswith(".md") and not p.endswith(".gitkeep")}; active=False; ids=[]; rows=0
 for line in text.splitlines():
  if line.strip()=="## Knowledge": active=True; continue
  if active and line.startswith("## "): break
  if active and line.startswith("|") and not line.startswith("|---") and "| entry |" not in line: rows+=1; ids.extend(re.findall(r"`([^`]+)`",line.split("|",2)[1]))
 indexed={x.removeprefix("knowledge/") for x in ids if x!="lessons/round-13-distillation"}; absent=sorted(files-indexed); print(f"{rev}: files={len(files)} Knowledge-data-rows={rows} indexed-corpus-files={len(indexed)} unindexed={len(absent)}; set={absent}")
 print("r19-file="+str("2026-10-20-r19-go125-toolchain-replay" in files)+"; r19-Knowledge-row="+str("2026-10-20-r19-go125-toolchain-replay" in indexed))'; rc=$?; echo "census-exit=$rc"
# Output: B: 96 files / 80 rows / 79 indexed corpus files / 17 unindexed; main: 97 / 81 / 80 / 17. Exit 0.

git --no-optional-locks diff --unified=0 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 279e8b19c51658bfd05b9e31a1c0894ab2e70537 -- corpus/README.md
# exit 0; line 35 adds R19 to Coverage map; lines 154 and 170 are inserted rows.

git --no-optional-locks diff --numstat 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 279e8b19c51658bfd05b9e31a1c0894ab2e70537 -- corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md
# exit 0; 41 0 (held Go note), 64 0 (new R19 note).
```
