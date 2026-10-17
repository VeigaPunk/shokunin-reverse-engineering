# HB1 — pointer resolver: four final texts at HEAD a280e07

## CLAIM
Every path:line pointer in the four item-closing final texts resolves at HEAD `a280e07`. Texts taken per Z5's landing list (`Z5.md:8-11`): Z1's r4-16 append (`Z1.md:10`), Z2's SCORECARD note (`Z2.md:10`), Z3's `/tmp` audit (`Z3.md`), Z4's jq qualification (`Z4.md:10`).

## METHOD
`git rev-parse HEAD` → `a280e07133f52f719b0805fc73c0b997e77b5062`; `git diff --quiet HEAD` exit 0; PROVINCE worktree sha256 == HEAD blob (`fe7f3f61…3b37c1c`), diff empty. Extracted every `path:N` token via `grep -oE '[A-Za-z0-9_./{}~-]+:[0-9]+(,[0-9]+)*(-[0-9]+)?'` from Z1–Z4; tracked targets resolved via `git show HEAD:<p> | sed -n 'a,bp'`; untracked wave/report paths by direct read. Range valid iff file exists and end ≤ content lines (`awk END{print NR}`). Read-only; only this receipt written (no probes, network, `/tmp`, deletions).

## FINDINGS
~30 distinct targets; all resolve; content at cited lines matches each text's claim:
- Z1: r4-16 `:750-754` (two-site account at `:751-752`); r12-01 `:97`, `:99-104`, `:110-120`, `:115-118` ("attributed, not re-derived — the /tmp receipts are gone"); BB1 `:10-14,:30-33` (`:30` flags the r4-16 residual); A1–A3 exist.
- Z2: X1 `:32` (comma-grouped needles `29,367,752`/`84,258,816`); CB4 `:11` (both subchecks False); r4 report `:43-45` (F18); r5 report `:63-67` (opener); SCORECARD `:407-410,:453-460`; QUALITY `:7-25`.
- Z3: AGENTS `:1-5`; PROVINCE `:48`; SKILL `:242-251`,`:249-251`; verify-recovery.py `:120-144`, with `:123` = `dir=HERE`; l7-01/l7-03/l7-05/l8-01 `:5` (each `cd /tmp`); PROTOCOL `:341-344`; SB1 `:12-23`; SB3 `:12,:16`. Reproduced Z3's grep claim: exactly 4 occurrences, 4 files.
- Z4: jq-shadow `:10-13`, `:204-219`, `:217`, `:236-237`; PROVINCE `:107-109` (stale, not the refusal), `:114-116` (refusal); D2 `:1-18`; R4 `:1-14`.
- Supplementary alternate drafts: LOG `:751-780`; SCORECARD `:86-142,:402-415,:453-465,:556-559` (B2's set ⊂ Z2's).

## THREATS
- Z1–Z4, D2, R4 and wave receipts are untracked: resolved against this worktree snapshot (D2 mtime 21:45:28, stable over recheck). Later appends can shift end points; starts cannot.
- `PROTOCOL.md` is not in-repo; `:341-344` verified byte-identical at `../PROTOCOL.md` and `~/.kimi-code/skills/shokunin/protocol/PROTOCOL.md`.
- `wc -l` undercounts an unterminated last line (D2: 17 vs 18) — use `awk`/`grep -c ''`.
- Textual resolution only; "7 values" and the jq hash were not re-derived. Z1's "R1 unavailable" note is snapshot-bound: R1.md now exists.

## VERDICT
CLEAN — all path:line pointers in the four final texts resolve at HEAD a280e07; no stale, dangling, or out-of-range pointer found.
