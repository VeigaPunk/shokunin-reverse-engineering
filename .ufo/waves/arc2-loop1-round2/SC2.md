# SC2 (scout) — round-2 read-only corroboration: config pins, .bak variants, :1478, structural diffs

Wave arc2-loop1-round2 · Seat SC2 · 2026-10-18 · read-only corroboration (only write: this report). Versions, key names, line numbers and hashes only — no secret values printed anywhere.

## Verdict

**CONFIRMED — all round-1 SC2 findings hold byte-for-byte at this round's pre-pair; the three-file pin census is unchanged, `config.toml:1478` still reads `model = "kimi-k3"` (no rea pin there), and both `.bak` variants are strict additive subsets of the current file (0 deletions, 0 modifications in every pairwise diff) — every pin-relevant line is identical across all three, including the `rea-agents@6.7.0` pin line itself (byte-identical grep output, sha256 `eb1c7da7…`).** The round-2 pre-pair receipt (6-line 5-path form, `2026-10-18T16:57:35Z`, self-hash `4097ec77…`) matches live hashes exactly: 5/5 `sha256sum -c` OK. The only line-1478 divergence among the three files is a pure line-shift artifact (the files are 2939/2956/2964 lines), not a content change: no file has a `rea-agents` pin anywhere near :1478.

## Evidence — exact commands run this session with observed output

Census stamp: `date -Is` → `2026-10-18T13:59:28-03:00`.

### 1. Pin census (three configs)

`grep -n 'rea-agents'` on each config:
```
/home/vgpnk/.config/devin/mcp_config.json:7:        "rea-agents@6.5.0",
/home/vgpnk/.omp/agent/mcp.json:8:        "rea-agents@6.5.0",
/home/vgpnk/.kimi-code/config.toml:2940:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
```
Kimi targeted scan `grep -n 'rea-agents\|mcp_servers\.rea' /home/vgpnk/.kimi-code/config.toml`:
```
2938:[mcp_servers.rea]
2940:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
2943:[mcp_servers.rea.env]
```
Word-boundary sweep `grep -nE '(^|[^a-z])rea([^a-z]|$)' config.toml | grep -v reasoning` returns **only** those same three lines (2938/2940/2943) — the file's entire `rea` footprint is the one MCP table. Accounting for all 163 case-insensitive `rea` hits: 159 are `reasoning_key = "reasoning_content"` in model tables, 3 are the MCP-table lines above, and 1 is the `[read]` table header at :2897 (`default_max_chars` at :2898) — none pin-related. `~/.kimi-code/mcp.json`: zero `rea` matches.

### 2. `config.toml:1478` — still `model = "kimi-k3"`, no pin there

```
$ sed -n '1478p' /home/vgpnk/.kimi-code/config.toml
model = "kimi-k3"
$ awk 'NR<=1478 && /^\[/ {t=$0; n=NR} END {printf "last table header before 1478: %s at line %d\n", t, n}' config.toml
last table header before 1478: [models."opencode-go-3/kimi-k3"] at line 1476
```
File is 2964 lines (`wc -l`). :1478 sits inside a models table — no rea pin there, confirming round 1's refutation of PROVINCE.md:10/:18.

### 3. The two `.bak` variants

```
config.toml.20261018-085645.bak  2939 lines  51352d2606d765ac73cc9d16b201cbb540a7b6928249d27a310e75eb168538ed
config.toml.20261018-114557.bak  2956 lines  84acf4fba17c376e070fc11ea2609a401e034a3578979259bef50189286793a3
config.toml (current)            2964 lines  3546e033aeaf68093faf4099ea8289de5dea7ec224e7c557f08bfa9d51cf9a2a
```
Pin line in each (`grep -n 'rea-agents'`):
```
config.toml.20261018-085645.bak:2915:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
config.toml.20261018-114557.bak:2932:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
```
Both backups already carried 6.7.0 → drift predates both 2026-10-18 backups (consistent with round 1). The three files' `rea-agents` grep outputs are byte-identical (same sha256 `eb1c7da74fc5f870d7c6537e87beeaf043491b5cdd00ee7a2f65e426d9f2b675` when hashed per-file).

### 4. Structural diffs (line ranges only; values redacted)

`diff` insertion counts (`grep -c '^<'` / `'^>'`):
```
bak1 vs current : 0 deletions, 25 insertions   (added new-file lines 43-50 [8], 1002-1015 [14], 2928-2930 [3])
bak2 vs current : 0 deletions,  8 insertions   (added new-file lines 1002-1008 [7], 2929 [1])
bak1 vs bak2    : 0 deletions, 17 insertions   (added new-file lines 43-50 [8], 1002-1008 [7], 2921-2922 [2])
```
All three diffs are **pure additions** — every line of either `.bak` exists verbatim in the newer file (no changed lines, no removals). Region map (enclosing table / key names only; coordinates are in the newer file of each comparison, from `diff --new-group-format`):

- `43–50` (current; `43-50` in bak2) → new `[providers.antigravity]` table (`type`/`base_url`/`api_key`) + 3 comment lines. bak1 lacked it; it enters with bak1→bak2 and is not re-added by bak2→current.
- `1002–1015` (current) → two new model tables: `[models."antigravity/gemini-4-argon"]` (1002-1008) and `[models."antigravity/gemini-3.8-flash"]` (1009-1015), each `provider`/`model`/`max_context_size`/`capabilities`/`display_name` + blank. bak1→current adds both; bak2→current adds only gemini-4-argon (1002-1008); bak1→bak2 adds only gemini-3.8-flash (bak2 1002-1008).
- `2928–2930` (current) → three new `[secondary_model.models]` keys: `"antigravity/gemini-3.8-flash"` (:2928), `"antigravity/gemini-4-argon"` (:2929), `"zai-coding-plan/glm-5.3-flash"` (:2930). bak1→current adds all three; bak2→current adds only :2929; bak1→bak2 adds two (bak2 :2921-2922).
- bak1→bak2's pair `2921-2922` lands in `[secondary_model.models]` (bak2 :2896), adding the `"antigravity/gemini-3.8-flash"` and `"zai-coding-plan/glm-5.3-flash"` keys — not the `[services.moonshot_search]` region.

Nothing in any hunk touches `[mcp_servers.rea]`, `[mcp_servers.rea.env]`, or any `REA_*`/`GHIDRA`/`JAVA` line: the rea table neighborhoods are byte-identical across all three files (bak1 :2913-2920, bak2 :2930-2937, current :2938-2945, same key sequence `command`/`args`/`startup_timeout_sec` + `[mcp_servers.rea.env]` `GHIDRA_INSTALL_DIR`/`JAVA_HOME`).

### 5. Line-1478 divergence across the three (shift artifact, not content)

```
config.toml:1478                     [model = "kimi-k3"]
config.toml.20261018-085645.bak:1478 [max_output_size = 131072]
config.toml.20261018-114557.bak:1478 []
```
The content at current :1478 is shifted by the insertions above it: `model = "kimi-k3"` sits at bak2 :1471 (+7 = the 1002-1008 insertion) and at bak1 :1456 (+22 = the 43-50 and 1002-1015 insertions) — both verified by direct reads this session. Symmetrically, `max_output_size = 131072` sits at current :1500, bak2 :1493, bak1 :1478. So :1478 in the backups exposes a different (unchanged-in-substance) line only because the files are 25/8 lines shorter above it; the token `kimi-k3` is not at :1478 in either backup, and no rea pin exists anywhere near :1478 in any of the three.

### 6. Round-2 pre-pair receipt verified (6-line / 5-path form)

```
$ wc -l .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt         → 6
$ grep -cE '^[0-9a-f]{64}  /' …                                          → 5
$ grep -cE '^[0-9]{4}-…Z$' …                                             → 1
$ tail -n +2 … | sha256sum -c -                                          → 5× OK, rc=0
$ sha256sum …config-pre-pair.txt                                          → 4097ec77397308855bfb170733cf32d8c001de298ed1bf9bc1f4753ec25c6245
```
Receipt timestamp `2026-10-18T16:57:35Z` (mtime 13:57:35 -03:00); its first three hashes are byte-identical to round-1's `config-pre-pair.txt` (4-line form) — config 3-path hashes unchanged across the round boundary. Its `.bashrc`/`.profile` hashes (`7d2ca28a…`, `6c6be761…`) match E15.md:100-101 byte-for-byte. Zero drift on all five paths during this session's checks (two reads, same values).

### 7. Encoding sanity

All three files: UTF-8, 0 CR characters, LF-terminated (last byte `0a`).

## Text for parent to land VERBATIM

```text
REA pin census corroboration, round 2 (read-only, SC2 scout, 2026-10-18): unchanged from round 1. Devin `rea-agents@6.5.0` (/home/vgpnk/.config/devin/mcp_config.json:7), OMP `rea-agents@6.5.0` (/home/vgpnk/.omp/agent/mcp.json:8), Kimi `rea-agents@6.7.0` — the Kimi file's ONLY rea occurrence (word-boundary grep -nE '(^|[^a-z])rea([^a-z]|$)', which excludes all 159 reasoning_key lines) is config.toml:2940 inside [mcp_servers.rea] (:2938), env table [mcp_servers.rea.env] (:2943). config.toml:1478 still reads `model = "kimi-k3"` (enclosing table [models."opencode-go-3/kimi-k3"] :1476; file 2964 lines) — no rea pin there; PROVINCE.md:10/:18's 6.4.0-at-:1478 claim remains refuted. Both .bak variants already carried the 6.7.0 pin: config.toml.20261018-085645.bak:2915 (2939 lines, sha256 51352d26…), config.toml.20261018-114557.bak:2932 (2956 lines, sha256 84acf4fb…). Structural diffs are PURE ADDITIONS, zero deletions/modifications (coordinates below are added-line ranges in the newer file): bak1→current +25 lines (3 hunks: antigravity provider table +43..50, antigravity model tables +1002..1015, three secondary_model.models keys +2928..2930), bak2→current +8 lines (gemini-4-argon model table +1002..1008, one secondary_model key +2929), bak1→bak2 +17 lines. No hunk touches [mcp_servers.rea] or any REA_*/GHIDRA/JAVA line; the pin line content is byte-identical across all three files (grep-output sha256 eb1c7da74fc5f870d7c6537e87beeaf043491b5cdd00ee7a2f65e426d9f2b675). Round-2 pre-pair receipt (.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt) verified 6/5/1 shape, 5× sha256sum -c OK, self-hash 4097ec77397308855bfb170733cf32d8c001de298ed1bf9bc1f4753ec25c6245; its first 3 lines byte-identical to round-1's receipt; zero drift across all 5 paths.
```

## Conclusions by label

- **Observation** — (a) three-config pin values and lines exactly as listed (reproduced by fresh greps this session); (b) `config.toml:1478` = `model = "kimi-k3"` inside `[models."opencode-go-3/kimi-k3"]` (:1476), and the file's only `rea` lines are :2938/:2940/:2943; (c) both `.bak` variants already carried `rea-agents@6.7.0` at :2915 / :2932; (d) all three pairwise diffs contain zero `<`-lines — pure insertions (25 / 8 / 17); (e) no diff hunk intersects the rea table or any env-key line, and the pin line's content hash is identical across all three files; (f) round-2 pre-pair receipt is 6/5/1, 5× OK, self-hash `4097ec77…`, first-3 hashes identical to round-1's receipt; (g) `.bashrc`/`.profile` hashes in the round-2 receipt match E15.md:100-101; (h) all three config files UTF-8/LF, no CR.
- **Inference** — the `config.toml.20261018-114557.bak` snapshot (mtime 11:45:57.909, 0.25 s after current's 11:45:57.656 — same edit window) is consistent with being the pre-edit state of the 11:45 edit that produced the current file: current = bak2 + one 7-line model table (1002-1008) + one secondary_model key (:2929). The earlier edit (08:56:45 bak1 → 11:45 bak2) added the antigravity provider table, one model table, and two keys. Neither edit touched the rea pin, so the Kimi pin's 6.7.0 value is stable across both 2026-10-18 snapshots — the pin drift predates 08:56:45 (as round 1 bounded it). The `.bak`-as-prefix property (pure additions) is consistent with Kimi Code's config writer appending tables without rewriting earlier ones; the bak2-mtime-after-current ordering (writer may touch the backup after writing) does not affect the content-prefix property, which is diff-verified.
- **Unknown** — the semantic content of the redacted values (out of scope; values deliberately not emitted); exact drift date of the 6.4.0→6.7.0 pin change (still bounded: after 2026-10-16 reverify, at/before 2026-10-18 08:56:45); whether PROVINCE.md:10/:18 will be corrected by this round's C1 claim (still stale as of this census — the parent's integration step must land that edit); 6.7.0 tool counts (not probed here; battery seats' scope).

## Scope compliance

Read-only on every repo and home file except this report; no git mutations; no config edits; no installs; no network attempted; no secret values read or emitted (diff outputs redacted via `s/=(.*)$/= <redacted>/`; only version pins, key names, line numbers, hashes). Scratch: none needed beyond pipelines — no `/tmp` writes. Threats: hashes/line-reads are point-in-time; the writer-prefix inference is from two snapshots only (a rewriting writer that happened to produce supersets cannot be excluded).
