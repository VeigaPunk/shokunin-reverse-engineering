# SC2 (scout) — round-3 read-only config pin corroboration: pre-pair receipt 5/5, pin values unchanged, config.toml churn re-bounded

Wave arc2-loop1-round3 · Seat SC2 · 2026-10-18 · read-only corroboration (only write: this report). Versions, key names, line numbers and hashes only — no secret values printed anywhere.

## Verdict

**CONFIRMED with a churn addendum — the round-3 pre-pair receipt verifies 5/5 (`sha256sum -c` rc=0) and all pin values are unchanged (Kimi `rea-agents@6.7.0`, Devin/OMP `rea-agents@6.5.0`), but `~/.kimi-code/config.toml` was rewritten a SECOND time outside the round-2 bracket — at 17:50:34Z, between the round-2 drift receipt (17:32:20Z) and this round's pre-pair (17:55:49Z) — pure additions again (+71 lines, 0 deletions), hash `f10b01e9…` → `bd5a78d1…`; the pin line is byte-identical across all five known config states, now at `config.toml:3298` (`[mcp_servers.rea]` :3296), which means PROVINCE.md:18's fresh `:3227` pointer and SCORECARD.md:59/:698's `:2940` pointers are stale as of the 17:50 rewrite.** Zero drift during this leg (live hash re-checked twice, 17:57:24Z and 17:58:27Z, identical).

## Evidence — exact commands run this session with observed output

Census stamps: `date -u` → `2026-10-18T17:57:24Z`, `2026-10-18T17:58:03Z`, `2026-10-18T17:58:27Z` (local `14:57–14:58 -0300`).

### 1. Round-3 pre-pair receipt — shape and integrity

```
$ cat .ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt
2026-10-18T17:55:49Z
16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4  /home/vgpnk/.config/devin/mcp_config.json
38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b  /home/vgpnk/.omp/agent/mcp.json
bd5a78d1a829f480f12735bdfc18f6f8778e702caac7d766a776eda5597a9f3c  /home/vgpnk/.kimi-code/config.toml
7d2ca28a245c44a1f5458921f0dff54823aa1e74ffa02eac2013b486e6a26598  /home/vgpnk/.bashrc
6c6be761d3b199c964c95e724d7cdc9f4f902e0c3bdd6a532361b20a53db4f30  /home/vgpnk/.profile

$ tail -n +2 .ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt | sha256sum -c -
…/mcp_config.json: OK / mcp.json: OK / config.toml: OK / .bashrc: OK / .profile: OK   rc=0
$ wc -l < receipt → 6 ; grep -cE '^[0-9a-f]{64}  /' → 5 ; grep -cE timestamp → 1
$ sha256sum .ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt
3cba32fba1a9724c0ba3bdfdd6fe393afcc51b5354a982c3045f23cedb182553   (501 B; mtime 14:55:49.985 -0300)
```
**5/5 verified before my leg** (the receipt is 6-line / 5-path, matching the round-2 SOP form; round-1's 4-line form is superseded). Live re-hash matches the receipt byte-for-byte — zero drift in the leg.

### 2. Pin census (three clients) — values unchanged

```
$ grep -n 'rea-agents' /home/vgpnk/.config/devin/mcp_config.json
7:        "rea-agents@6.5.0",
$ grep -n 'rea-agents' /home/vgpnk/.omp/agent/mcp.json
8:        "rea-agents@6.5.0",
$ grep -n 'rea-agents' /home/vgpnk/.kimi-code/config.toml
3298:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
```
Word-boundary sweep `grep -nE '(^|[^a-z])rea([^a-z]|$)' config.toml | grep -v reasoning_key` returns **only** three lines — the file's entire `rea` footprint is one MCP table:
```
3296:[mcp_servers.rea]
3298:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
3301:[mcp_servers.rea.env]
```
Neighborhood (key names only; values redacted): `:3297 command`, `:3299 startup_timeout_sec`, `:3302 GHIDRA_INSTALL_DIR`, `:3303 JAVA_HOME`. Devin/omp files: single `rea-agents` occurrence each, both at their round-1/2 lines (:7 / :8), both hashes identical to every prior receipt (see §4). Bonus sweep: `~/.grok/config.toml:30` still `"rea-agents@6.5.0"`; `~/.codex/config.toml` has no `rea-agents` token (its :77 is an absolute `rea` binary path, no version token — unchanged).

### 3. Churn timeline for `~/.kimi-code/config.toml` — two rewrites, both pure additions

```
$ for f in /home/vgpnk/.kimi-code/config.toml*; do printf '%s  ' "$(sha256sum "$f"|cut -c1-16)"; stat -c '%y %s %n' "$f"; done
bd5a78d1a829f480  2026-10-18 14:50:34.896 -0300 107496  config.toml                      (= 17:50:34Z, LIVE)
51352d2606d765ac  2026-10-18 08:56:45.825 -0300  94141  config.toml.20261018-085645.bak
84acf4fba17c376e  2026-10-18 11:45:57.909 -0300  95083  config.toml.20261018-114557.bak
3546e033aeaf6809  2026-10-18 14:32:36.366 -0300  95470  config.toml.20261018-143236.bak  (pre-17:32 copy = round-1/2 receipt state)
f10b01e912205482  2026-10-18 14:32:20.674 -0300 104752  config.toml.20261018-145016.bak  (17:32 state, as recorded in round-2 drift receipt)
```
```
$ diff .20261018-143236.bak .20261018-145016.bak | grep -c '^<'  → 0 ; '^>' → 287   (17:32:20Z rewrite)
$ diff .20261018-145016.bak  config.toml           | grep -c '^<'  → 0 ; '^>' → 71    (17:50:34Z rewrite)
   hunks: 3124a3125,3194 (70 lines) + 3196a3267 (1 line) — all additions sit below :3124,
   which is why :1478 kept its 17:32 content through the 17:50 rewrite.
```
Receipt lineage: round-1 pre/post and round-2 pre/post all carried config.toml `3546e033…`; the 17:32 rewrite was already recorded verbatim (`.ufo/waves/arc2-loop1-round2/receipts/drift-config-toml-20261018T173220Z.txt:1` — "live hash at record time: `f10b01e9…`"); the **17:50:34Z second rewrite is new this round** and is exactly what the round-3 receipt re-baselines as `bd5a78d1…`. Both rewrites touched neither the pin line's bytes nor any `rea` line (grep-output sha256 `eb1c7da7…` in all five states, §4).

### 4. Pin line byte-identity across all five known config states

```
$ for f in *.085645.bak *.114557.bak *.143236.bak *.145016.bak config.toml; do printf '%s  %s  ' "$(grep -h 'rea-agents' $f | sha256sum | cut -c1-16)" "$(grep -c 'rea-agents' $f)"; echo "$f"; done
eb1c7da74fc5f870  1  config.toml.20261018-085645.bak
eb1c7da74fc5f870  1  config.toml.20261018-114557.bak
eb1c7da74fc5f870  1  config.toml.20261018-143236.bak
eb1c7da74fc5f870  1  config.toml.20261018-145016.bak
eb1c7da74fc5f870  1  config.toml
```
The pin line (`args = [ "-y", "rea-agents@6.7.0", "mcp" ]`) is byte-identical in all five; only its line number moved: `:2915` → `:2932` → `:2940` → `:3227` → **`:3298`**. Table headers: `[mcp_servers.rea]` `:2938` → `:3225` → `:3296`; `[mcp_servers.rea.env]` `:2943` → `:3230` → `:3301`.

### 5. Pointer casualties of the two post-bracket rewrites (for the parent's C1/C3 work)

```
$ sed -n '3227p' config.toml → default_effort = "high"                 (PROVINCE.md:18's pointer — now DEAD)
$ sed -n '2940p' config.toml → capabilities = [ "thinking", "tool_use" ]  (SCORECARD.md:59,:698 pointers — now DEAD)
$ sed -n '1478p' config.toml → max_output_size = 131072                 (round-2's ":1478 = model = \"kimi-k3\"" is also superseded)
```
Repo loci citing the now-dead numbers: `PROVINCE.md:18` (`:2940` … relocated `:3227` — both stale vs live), `SCORECARD.md:59`, `SCORECARD.md:698` (`:2940`), `LOG.md:1018` (`:2940`, historical log entry), `SCORECARD.md:291` (`:1478` → 6.4.0 — dated/historical record). `SCORECARD.md:698` already labels its statement "SC2-refuted" context but its `:2940` pointer no longer resolves to the pin; `PROVINCE.md:18`'s `:3227` was accurate at 17:32Z and is dead since 17:50:34Z. These are candidate C1 loci beyond the ones named in the round declaration.

### 6. Live drift re-check inside this leg

```
17:57:24Z  bd5a78d1a829f480f12735bdfc18f6f8778e702caac7d766a776eda5597a9f3c  (config.toml)
17:58:27Z  bd5a78d1a829f480f12735bdfc18f6f8778e702caac7d766a776eda5597a9f3c  (config.toml)
```
Devin/omp mtimes remain 2026-10-14 17:53:20 -0300 (pre-date all rounds) — no churn possible on those two since the receipt.

## Text for parent to land VERBATIM

```text
REA pin corroboration, round 3 (read-only, SC2 scout, 2026-10-18): round-3 pre-pair receipt (.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt, 2026-10-18T17:55:49Z, 501 B, self-hash 3cba32fba1a9724c0ba3bdfdd6fe393afcc51b5354a982c3045f23cedb182553) verified 6/5/1 shape, 5x sha256sum -c OK, rc=0 — 5/5 before the leg; zero drift during it. Pin values UNCHANGED: Devin rea-agents@6.5.0 (/home/vgpnk/.config/devin/mcp_config.json:7, sha256 16f496e6… — identical in all four prior receipts), OMP rea-agents@6.5.0 (/home/vgpnk/.omp/agent/mcp.json:8, 38d2a1d0… — identical), Kimi rea-agents@6.7.0 at /home/vgpnk/.kimi-code/config.toml:3298 (only rea line; [mcp_servers.rea] :3296, env :3301; word-boundary sweep shows the file's whole rea footprint is these 3 lines). CHURN ADDENDUM: config.toml was rewritten a SECOND time outside the round-2 bracket — 17:50:34Z, pure additions +71 lines / 0 deletions (f10b01e9… -> bd5a78d1…; the 17:32:20Z rewrite 3546e033… -> f10b01e9… is already recorded in .ufo/waves/arc2-loop1-round2/receipts/drift-config-toml-20261018T173220Z.txt). The pin line is byte-identical across ALL FIVE known config states (grep-output sha256 eb1c7da74fc5f870d7c6537e87beeaf043491b5cdd00ee7a2f65e426d9f2b675): :2915 -> :2932 -> :2940 -> :3227 -> :3298. Consequently PROVINCE.md:18's ":2940 … relocated to :3227" is doubly stale (:3227 now = default_effort = "high") and SCORECARD.md:59/:698's ":2940" no longer resolves to the pin — candidate C1 loci. Live hash re-checked twice during the leg (17:57:24Z, 17:58:27Z), identical.
```

## Conclusions by label

- **Observation** — (a) receipt 6/5/1, 5× OK rc=0, self-hash `3cba32fb…`, timestamp `2026-10-18T17:55:49Z`; (b) live hashes byte-match the receipt, re-checked twice (17:57:24Z / 17:58:27Z); (c) Kimi pin `rea-agents@6.7.0` at live `config.toml:3298`, the file's only rea occurrence; Devin/OMP pins `rea-agents@6.5.0` at :7/:8 with hashes identical to all prior receipts; (d) five config states (4 backups + live) all carry the same single, byte-identical pin line (`eb1c7da7…`), line number `:2915→:2932→:2940→:3227→:3298`; (e) two rewrites post-bracket: 17:32:20Z (+287, 0 del) and 17:50:34Z (+71, 0 del); (f) live `:3227` = `default_effort = "high"` and `:2940` ≠ pin → PROVINCE.md:18 / SCORECARD.md:59,:698 pointers dead; live `:1478` = `max_output_size = 131072` (round-2's `model = "kimi-k3"` statement superseded by the 17:32 shift); (g) grok `~/.grok/config.toml:30` still 6.5.0; codex has no `rea-agents` token.
- **Inference** — the two rewrites are ordinary operator config growth (provider/model tables, per the round-2 drift receipt's characterization and the pure-addition diffs); the pin's 6.7.0 value has been stable since at/before 08:56:45 and is unaffected by either rewrite. The round-3 pre-pair correctly re-baselines the post-17:50 state, so this round's custody bracket starts clean. Any current-state prose in the repo that names `config.toml:2940` or `:3227` as the live pin is stale as of 17:50:34Z; the safe current pointer is `config.toml:3298` (and it should be marked with its capture stamp, given the observed rewrite cadence of ~2/hour today).
- **Unknown** — whether further rewrites land before the post-pair capture (cadence suggests possible; post-pair seat must re-baseline, not assume); why the writer backs up with preserved mtimes (`.20261018-145016.bak` has mtime 14:32:20.674, same as the 17:32-state file it contains — backup naming vs content mtime do not line up, so do not date-state by bak filename); whether the parent lands the `:3298` re-point in PROVINCE.md:18/SCORECARD.md:59/:698 this round (C1 scope); whether the Kimi client actually loads the config.toml pin (configured ≠ held; CR1's 0-of-2195 wire-log finding stands unrefuted here).

## Scope compliance

Read-only on every repo and home file except this report; no git mutations; no config edits (the drifted config was NOT restored); no installs; no network; no secrets read or emitted (only key names, versions, line numbers, hashes; neighborhood printed with values redacted). Scratch: none — no `/tmp` writes, no residue (`ls -d /tmp/arc2-l3r3-SC2*` → no such file). Threats: all observations are point-in-time hashes/lines; the "pure additions" characterization relies on `diff` line counts, not content review of the added tables (values not inspected).
