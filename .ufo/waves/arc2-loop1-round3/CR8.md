# CR8 (critic) — provenance attack: battery receipts, wave-seat capture integrity, the config churn window

Seat CR8, wave arc2-loop1-round3, 2026-10-18. Read-only everywhere except this report (my
only write). Scratch confined to `/tmp/arc2-l3r3-CR8-scratch/` (five files, no secrets).
HEAD at every command: `679af5d749f2fd48b9d543e3c99d348d5458f90f`; `git status --porcelain`
→ `?? .ufo/waves/arc2-loop1-round3/` only. Every command below was run by this seat this
session (17:57Z–18:28Z); every `path:line` was re-resolved at write time (18:28Z). No repo
file, config file, or other seat's scratch was modified; no process of mine is alive.

## 1. Verdict

**ATTACK PARTLY SUCCEEDS — the artifact and the writer attribution survive; three
provenance defects are confirmed and one of them disposes the round's custody claim as
stated.**

1. **Receipt provenance: PASSES.** The round-3 pre-pair (`.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt`,
   6 lines / 501 B, self-hash `3cba32fb…`, btime `17:55:49.984Z`) verifies **5/5, rc 0**
   at my first check (18:02:41Z) and at every re-check through 18:27:28Z. All five hashes
   are live-true *now* (18:28:38Z). Rounds 1 and 2 MANIFESTs re-hash clean 8/8 each.
2. **Writer attribution: RESOLVED, and it is not any wave seat.** All three config writes
   today are attributable to **interactive Kimi sessions running with cwd `/home/vgpnk`**,
   not to the wave: session `61158e8d` wrote at 17:32:20Z (its own wire log shows
   `cp config.toml config-new.toml` → edit → `cp config.toml config.toml.$(date …).bak &&
   mv config-new.toml config.toml`); session `afa2dd53` wrote at 17:50:34Z and then again
   **inside the round-3 bracket** at ~18:01:40Z, and reverted at ~18:02:33Z. No round-3
   seat artifact contains a write, `cp`, or `mv` of `~/.kimi-code/config.toml` (grep of all
   `/tmp/arc2-l3r3-*` artifacts).
3. **The custody claim is VOID as a bare zero-drift claim.** The pre-pair's `config.toml`
   line was `FAILED` between ~18:01:40Z and ~18:02:33Z — inside the window the receipt
   brackets — and the reverted file has its original mtime and inode. Per `SKILL.md:270-276`
   ("Content drift … the zero-drift claim is VOID — record the path with both hashes
   verbatim … classify as operator-owned incident"), the round must ship the excursion
   record, not "zero drift". Independent seats E2, E4, E19, R7, V2, C3, R5 already reached
   this; my contribution is the **writer-level attribution** none of them made (E19.md:425
   says "operator-driven, not seat-driven" but leaves the mechanism unknown; E19.md:338
   says "the endpoints were observed, the write itself was not" — I observed the write
   itself, in the writer's own persisted wire log).
4. **The round-2 drift note misattributes the added lines** (round-2 artifact, carried into
   LOG.md:1046-1049): it says "~295 added lines: `[providers.opencode-go-7]` +
   `[models.\"alibaba-token-plan/*\"]` tables" — the real `114557.bak → 145016.bak` diff has
   **zero** `alibaba` lines; the 295 additions are 28 `[models.\"opencode-go-7/*\"]` tables +
   `[providers.opencode-go-7]` + its `custom_headers` + one `[models.\"antigravity/gemini-4-argon\"]`.
5. **Two fresh pointer defects were minted inside round 3's own seat reports** —
   `E19.md:36` cites `SC1.md:134-136` for the 18:01:33Z no-op backup, but `SC1.md:134-136`
   is the pre-pair hash-verification block and the string `150133` does not occur anywhere
   in `SC1.md`; and `E19.md:338` repeats the same dead pointer. This is the exact
   pointer-drift class C1 exists to drain, re-created in the same wave.

**Disposition for the parent:** land the round-3 custody record with the excursion verbatim
(§3 block), do not report a bare "zero drift"; correct the round-2 drift-note
characterization and the LOG.md echo of it; the two E19 pointers are the parent's call
(repair in place or record as debt — E19 is itself a live seat report this wave).

## 2. Evidence — commands run THIS session, with observed output

Census stamps: `date -u` → `2026-10-18T17:57:32Z` … `18:28:38Z` (local `14:57–15:28 -0300`).

### 2.1 The round-3 pre-pair receipt — integrity and the path-name discrepancy

```
$ cat -A .ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt
2026-10-18T17:55:49Z$
16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4  /home/vgpnk/.config/devin/mcp_config.json$
38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b  /home/vgpnk/.omp/agent/mcp.json$
bd5a78d1a829f480f12735bdfc18f6f8778e702caac7d766a776eda5597a9f3c  /home/vgpnk/.kimi-code/config.toml$
7d2ca28a245c44a1f5458921f0dff54823aa1e74ffa02eac2013b486e6a26598  /home/vgpnk/.bashrc$
6c6be761d3b199c964c95e724d7cdc9f4f902e0c3bdd6a532361b20a53db4f30  /home/vgpnk/.profile$
$ wc -l -c .ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt
  6 501
$ sha256sum .ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt
3cba32fba1a9724c0ba3bdfdd6fe393afcc51b5354a982c3045f23cedb182553
$ stat -c 'birth=%w mtime=%y size=%s' …config-pre-pair.txt
birth=2026-10-18 17:55:49.984069512 +0000  mtime=2026-10-18 17:55:49.985069519 +0000  size=501
$ tail -n +2 …config-pre-pair.txt | sha256sum -c -        # run 18:02:41Z, 18:07:45Z, 18:09:57Z, 18:11:37Z, 18:15:12Z, 18:20:41Z, 18:23:37Z, 18:24:16Z, 18:25:14Z, 18:26:24Z, 18:27:28Z, 18:28:38Z
…/mcp_config.json: OK / mcp.json: OK / config.toml: OK / .bashrc: OK / .profile: OK   rc=0   (every run)
```

Note on path spelling: the seat line says `~/.config/kimi-code/config.toml`; **no such path
exists** (`stat` → No such file or directory). The live client config is
`/home/vgpnk/.kimi-code/config.toml` (which the receipt correctly carries), and the
`~/.config/…` spelling is wrong for Kimi — the deviation is in the seat line, not the
artifact. The `devin` path is `/home/vgpnk/.config/devin/mcp_config.json` (exists); the
similarly-named `/home/vgpnk/.devin/mcp_config.json` does not exist.

### 2.2 Round-1 and round-2 committed receipts — MANIFEST integrity

```
$ cd .ufo/waves/arc2-loop1-round2/receipts && sha256sum -c MANIFEST.txt    # 8 files
config-pre-pair.txt: OK / config-post-pair.txt: OK / leg-1-doctor.txt: OK / leg-2-binary-session.json: OK /
leg-2-tools-list.json: OK / leg-2-close-binary.json: OK / leg-2-census-client.mjs: OK /
drift-config-toml-20261018T173220Z.txt: OK                                rc=0
$ cd .ufo/waves/arc2-loop1-round1/receipts && sha256sum -c MANIFEST.txt    # 8 files
(all OK)                                                                  rc=0
$ cmp /tmp/arc2-l2r2-E15/config-post-pair-E.txt .ufo/waves/arc2-loop1-round2/receipts/config-post-pair.txt
rc=0    # E15's drafted post-pair (§4 block) is byte-identical to the committed file — the parent landed E15's block verbatim, as required
```

### 2.3 The config churn timeline — five on-disk states, all measured this session

```
$ stat -c 'birth=%w mtime=%y size=%s ino=%i %n' /home/vgpnk/.kimi-code/config.toml*
birth=2026-10-18 17:30:46.188 +0000 mtime=2026-10-18 17:50:34.896 +0000 size=107496 ino=29670088  config.toml
birth=2026-10-18 11:56:45.825 +0000 mtime=2026-10-18 11:56:45.825 +0000 size=94141  ino=28431847  config.toml.20261018-085645.bak
birth=2026-10-18 14:45:57.909 +0000 mtime=2026-10-18 14:45:57.909 +0000 size=95083  ino=28750721  config.toml.20261018-114557.bak
birth=2026-10-18 17:32:36.366 +0000 mtime=2026-10-18 17:32:36.366 +0000 size=95470  ino=29712303  config.toml.20261018-143236.bak
birth=2026-10-18 17:50:16.101 +0000 mtime=2026-10-18 17:32:20.674 +0000 size=104752 ino=30067176  config.toml.20261018-145016.bak
birth=2026-10-18 18:01:33.132 +0000 mtime=2026-10-18 17:50:34.896 +0000 size=107496 ino=30149532  config.toml.20261018-150133.bak
$ sha256sum /home/vgpnk/.kimi-code/config.toml*
bd5a78d1…  config.toml           (live)
51352d26…  .20261018-085645.bak
84acf4fb…  .20261018-114557.bak
3546e033…  .20261018-143236.bak  ← the round-1/2 receipt hash
f10b01e9…  .20261018-145016.bak  ← the round-2 drift-note's "live hash at record time"
bd5a78d1…  .20261018-150133.bak  ← byte-identical to live (cmp rc 0)
```

Content generations, all diffed by me this session (counts = added `>` lines, deletions 0):

```
114557.bak → 143236.bak     +8    ([models."antigravity/gemini-4-argon"] + one secondary row)
143236.bak → 145016.bak   +287    (opencode-go-7 provider + custom_headers + 28 model tables)
114557.bak → 145016.bak   +295    ← the round-2 drift note's diff; alibaba-line count: 0
145016.bak → live          +71    (7 × [models."opencode-go-N/deepseek-v4.1-flash-free"])
live stanza/pin:           :3296 [mcp_servers.rea] / :3298 rea-agents@6.7.0
```

The pin **line** is byte-identical across all six states — verified by hashing the extracted
pin line itself in each file (all six → `eb1c7da74fc5f870` prefix).

### 2.4 Writer attribution — the interactive sessions' own persisted logs

Session dir: `/home/vgpnk/.kimi-code/sessions/wd_vgpnk_403b91ce3657/`. Both sessions have
cwd `/home/vgpnk`; both are ordinary interactive Kimi sessions, created 17:29:11Z and
17:46:13Z, alive during the window (main process `kimi`, PID 530913 started 17:45:29Z).

`session_61158e8d…/state.json` — title: `i need to enter another opencode go auth, the 7th
one, just like we did with the others here on kimi code cli`. Its wire log contains:

```
"command":"cd ~/.kimi-code && cp config.toml config-new.toml && { command -v uuidgen >/dev/null && uuidgen || cat /proc/sys/kernel/random/uuid; }"
"command":"cd ~/.kimi-code && diff config.toml config-new.toml | grep -c '^<' ; echo \"---\"; diff config.toml config-new.toml | grep '^>' | grep -v 'opencode-go-7' | head"
"command":"cd ~/.kimi-code && cp config.toml \"config.toml.$(date +%Y%m%d-%H%M%S).bak\" && mv config-new.toml config.toml && ls config.toml.*.bak"
```

Its file-history holds `32ac4ffe…@v1`, sha256 `3546e033…` — the pre-write state — and
`config.toml.20261018-143236.bak` is the same `3546e033…` bytes. This is the 17:32:20Z write.

`session_afa2dd53…/state.json` — title: `also, include the deepseek v4.1 flash free into
all the auths on opencode, and add them as a secondary model, same as glm 5.3 flash free
(total models should become 29 then) on all 7 accounts`; last prompt `revert`. Its wire log
(1,036,599 B at my read, mtime 18:02:39.996Z) contains, in order:

```
1792345827730 (17:50:27.7Z)  Edit config.toml  old:"…Qwen3.7 Plus (key 7)…" new:+[models."opencode-go/deepseek-v4.1-flash-free"]
1792345834894 (17:50:34.9Z)  Edit config.toml  secondary_model row additions
… notification "Edits are in… I added 7 [models."opencode-go-N/deepseek-v4.1-flash-free"] definition blocks…"
1792346493122 (18:01:33.1Z)  Edit config.toml  new:+[models."zai-coding-plan/glm-5.3-flash-max"] (+ .overrides default_effort="max")
1792346493135 (18:01:33.1Z)  tool result: "config.toml.20261018-150133.bak"     ← the backup was taken HERE
1792346500771 (18:01:40.8Z)  Edit config.toml  secondary_model row for glm-5.3-flash-max
1792346553458 (18:02:33.5Z)  "cd ~/.kimi-code && cp -p config.toml.20261018-150133.bak config.toml && python3 …"
```

and the writer's own reasoning at 18:02:39.99Z: `The user says "revert". … with backup
config.toml.20261018-150133.bak taken right before those edits. "Revert" without
qualification = undo the last change.`

Its file-history confirms the states independently:

```
c240a8a7…@v1  104752 B  birth 17:50:27.728Z  sha256 f10b01e9…  (3251 lines)
c240a8a7…@v2  107496 B  birth 17:52:14.050Z  sha256 bd5a78d1…  (3322 lines)   = the round-3 pre-pair hash
c240a8a7…@v3  108208 B  birth 18:02:12.299Z  sha256 9ac8023b…  (3336 lines, stanza :3310, pin :3312)
```

`@v3` differs from live by exactly: `+[models."zai-coding-plan/glm-5.3-flash-max"]` block,
its `.overrides` table, and one `[secondary_model.models]` row (14 added lines, 0 deletions —
matches E22.md:203's independently observed +14/-0). The `cp -p` restore at 18:02:33.5Z
explains the restored mtime and the surviving ctime:

```
$ stat -c 'size=%s mtime=%y ctime=%z ino=%i' /home/vgpnk/.kimi-code/config.toml
size=107496 mtime=2026-10-18 17:50:34.896343019 +0000 ctime=2026-10-18 18:02:33.462921932 +0000 ino=29670088
$ stat -c 'ctime=%z' /home/vgpnk/.kimi-code/config.toml.20261018-150133.bak
ctime=2026-10-18 18:01:33.132606033 +0000
```

Mechanism (previously "unknown" in E19.md:338-339): **Edit-tool write → `cp -p` restore
from a backup taken 7 s before the write**, both by the interactive session, both persisted
in its wire log and file-history. This is observation, not inference — the tool calls and
results are in the log.

### 2.5 No wave seat wrote config.toml

```
$ grep -rn 'cp .*config\.toml\|mv .*config\.toml\|> ~/.kimi-code/config.toml\|tee ~/.kimi-code' /tmp/arc2-l3r3-* 2>/dev/null
(no hits outside /tmp/arc2-l3r3-C1-inst/**/interactive-sessions/*.jsonl — quoted historical content inside an old session dump, not a command)
$ grep -rln 'kimi-code/config.toml' /tmp/arc2-l3r3-*   # hits are read-only census scripts and clone copies
```

Seat artifacts cite the config only as read targets (census scripts, greps, `stat`s). The
E19.md:425 inference ("operator-driven, not seat-driven") is now upgraded to observation.

### 2.6 Seat-capture integrity — what holds and what does not

- **Holds:** round-2 receipt pair byte-stable in git (`git log -1 -- .ufo/waves/arc2-loop1-round2/receipts`
  → `b3cd790`, `14:53:09 -0300`; both rounds' receipts are tracked, 9+9 files each). The
  round-2 post-pair content equals E15's drafted block (`cmp` rc 0, §2.2). Round-3's
  seat artifacts (54 files present at 18:27Z) each re-verified the pre-pair independently —
  CR1.md:36, CR4.md:89, CR6.md:8, E10.md:22/48, E16.md:111/146 all record 5/5 OK rc 0, with
  timestamps spanning 17:57Z–18:13Z; my own twelve checks agree.
- **Does not hold as "zero drift":** the in-window excursion (§2.3–2.4). The pre-pair
  *hash equality at endpoints* is real; the *no-write-during-window* implication is false.
  R7.md:9 and V2.md:28-31 recorded the same failure at their own shells (18:02:12Z FAILED,
  revert by 18:03:01Z); E2.md:284-288 saw one anomalous read then five clean reads at an
  unchanged inode; E4.md:32-33 saw FAILED at 18:01:53Z and 18:02:30Z.
- **`tail -n3` false-pass hazard (round-2 E15.md:13-18, E21.md:9) still live:** I re-ran the
  selector on the round-3 receipt — `tail -n3 … | sha256sum -c -` → rc 0 while examining
  only config.toml/bashrc/profile; the devin and omp lines are silently skipped. On this
  receipt it currently yields the same verdict as the full check, but the selector remains
  a false-pass trap for any future devin/omp-only drift.
- **/tmp durability:** round-2 artifacts cited by seat reports: 8 of 9 spot-checked paths
  still present (`/tmp/arc2-l2r2-E14`, `E13-scratch`, `E23`, `C3-gate.py`, `R2-e23`,
  `Z1-sim`, `E10-sim`, `CR8-cap3.txt`); `/tmp/arc2-l2r2-C3-clone` is gone (was a
  throwaway clone). Round-1 artifacts spot-checked: 4/4 present. Round-3 artifacts are
  being written as seats run; C2's declared-and-removed scratch (`C2.md:403-404`) verified
  absent — correctly cleaned, per its own disclosure. E17's clones were removed as
  disclosed (`E17.md:7-8`); its `/tmp/arc2-l3r3-E17-clone{,2,3}` are absent, `census.py`
  path pattern is a brace-form citation. `/tmp` is tmpfs (SC1.md:226) — these are
  session-scoped, and PROTOCOL.md:341-343 ("An evidence pointer must resolve at *closure*
  time … paths under `tmpfs` … are not evidence — commit the artifact or cite a
  reproducible command") applies to any seat report whose claim rests on a `/tmp` path.
  The C3 gate and battery artifacts for this round are the load-bearing ones; the parent
  should land them under `receipts/` as in round 2 (E15's §4 pattern).

### 2.7 Pointer defects minted this round (candidate C1-class findings)

```
$ grep -n '150133' .ufo/waves/arc2-loop1-round3/SC1.md          → (no output; absent)
$ sed -n '134,136p' .ufo/waves/arc2-loop1-round3/SC1.md
$ sha256sum /home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json \
            /home/vgpnk/.kimi-code/config.toml /home/vgpnk/.bashrc /home/vgpnk/.profile
$ sed -n '36p' .ufo/waves/arc2-loop1-round3/E19.md
   (byte-identical to the live file), and `E2.md:284-288` independently saw
$ sed -n '338p' .ufo/waves/arc2-loop1-round3/E19.md
  `SC1.md:134-136` — a no-op backup dated 18:01:33Z). Mechanism **unknown**:
```

`E19.md:36` and `E19.md:338` cite `SC1.md:134-136` for the 18:01:33Z backup fact; that
locus is the pre-pair verification block and never mentions the backup. The fact actually
lives at `S1.md:142` ("mtime 15:01:33 -0300 = **18:01:33Z**"), `E4.md:180`, `E16.md:132`,
`E22.md:152`, `C2.md:109`. Second candidate: `R5.md:214` cites `E4.md:24` for E4 having
"read the `9ac8023b` state live and reported the pre-pair as '4/5, rc 1'" — `E4.md:24` is
the C1 re-point-target finding; the 4/5 reading is at `E4.md:32-33`/`:229`/`:452`. Both are
minor citation slips in live seat reports (repairable before the wave dir is committed, or
recordable as debt — parent's call). Neither affects any hash claim.

Also, the round-2 drift note's characterization (§1.4) is wrong in the same class:
`drift-config-toml-20261018T173220Z.txt:4` says `[models."alibaba-token-plan/*"]` tables
were added; the diff contains zero alibaba lines (the `alibaba-token-plan` tables existed
in all states, count 123 throughout — I counted them in all five states).

## 3. Text the parent should land VERBATIM

**(a) Round-3 custody record (drift disposition, to accompany the post-pair capture — the
block below is the minimum the SKILL.md:270-276 clause requires; adapt only if the
post-pair seat's own numbers differ):**

```text
2026-10-18T18:01:40Z (file mtime 15:01:40.773889893 -0300) — ~/.kimi-code/config.toml
rewritten INSIDE the round-3 custody bracket (pre-pair 2026-10-18T17:55:49Z captured
bd5a78d1a829f480f12735bdfc18f6f8778e702caac7d766a776eda5597a9f3c): live hash observed
9ac8023b60c5a05df49d7c11dc7c03079d7865baa4cc566ed544079ba0a9e272, 3336 lines, +14/-0
([models."zai-coding-plan/glm-5.3-flash-max"] + its .overrides + one [secondary_model.models]
row; the [mcp_servers.rea] block byte-identical, pin rea-agents@6.7.0 relocated :3298 -> :3312
by insertion only).
writer (observed, not inferred): interactive Kimi session session_afa2dd53-daad-4e99-9fdd-0a0b03731af0
(cwd /home/vgpnk) — its wire.jsonl records Edit at 18:01:33.122Z, backup
config.toml.20261018-150133.bak born 18:01:33.132Z, second Edit at 18:01:40.771Z, and the
restore command at 18:02:33.458Z ("cp -p config.toml.20261018-150133.bak config.toml",
preceded by the user's "revert").
rollback: by 18:02:33.463Z the live file was byte-identical to the pre-pair state again
(sha256 bd5a78d1…; same inode 29670088, mtime restored to 15:50:34.896343019 -0300 by cp -p;
ctime 18:02:33.462921932 -0300 is the surviving marker of the mutation).
disposition: per the custody SOP the pre-pair receipt verifies 5/5 (sha256sum -c rc=0 at
checks from 18:02:41Z through 18:28:38Z) and the pin value never changed, but the zero-drift
claim for the window is VOID as stated; the in-window mutation is recorded here verbatim,
not repaired (operator-owned surface). The post-pair seat must capture all five paths AND
carry this record — endpoint hash equality hides the mid-window rewrite; ctime plus this
record are the evidence.
```

**(b) Correction text for the round-2 drift note and its LOG.md echo (`LOG.md:1046-1049`):**

```text
Correction (round 3, seat CR8, read-only re-diff): the round-2 drift note's characterization
"~295 added lines: [providers.opencode-go-7] + [models."alibaba-token-plan/*"] tables"
misnames the additions. The measured 114557.bak -> 145016.bak diff (+295/-0) is
[providers.opencode-go-7] + [providers.opencode-go-7.custom_headers] + 28
[models."opencode-go-7/*"] tables + 1 [models."antigravity/gemini-4-argon"]; zero lines
mention alibaba-token-plan (that family's 123 lines are present in every state). The
relocation :2938 -> :3225 and the byte-identical pin stand as recorded.
```

**(c) Addendum for the round-3 drift record already drafted by E22 (Block B, `E22.md:200-206`):**

```text
writer addendum (CR8, observed in the writer's own persisted logs): the 18:01:40Z rewrite
and the 18:02:33Z restore were both performed by interactive Kimi session
session_afa2dd53-daad-4e99-9fdd-0a0b03731af0 (cwd /home/vgpnk, prompt "revert"); the
17:32:20Z write was session session_61158e8d-2beb-4061-8daa-3197020cfa61 (cwd /home/vgpnk,
prompt "enter another opencode go auth, the 7th one"). No arc2 wave seat issued any write,
cp, or mv against ~/.kimi-code/config.toml; the churn is operator activity, and the
mechanism is no longer unknown.
```

## 4. Conclusions — observation vs inference vs unknown

**Observation (measured this session):**
- Receipt 5/5 rc 0 at twelve checks spanning 18:02:41Z–18:28:38Z; self-hash `3cba32fb…`;
  6/5/1 shape; btime 17:55:49.984Z. Round-1/2 MANIFESTs 8/8 OK each.
- Config states and hashes as in §2.3; the live file is `bd5a78d1…`, 3322 lines, stanza
  `:3296`, pin `:3298`, ctime 18:02:33.462Z; the pin line byte-identical in all six states.
- The writer sessions' wire logs and file-history contain the exact Edit/`cp`/`cp -p`
  commands and the resulting hashes (`f10b01e9…`, `bd5a78d1…`, `9ac8023b…`).
- No wave-seat artifact writes config.toml.
- The round-2 drift note's `alibaba` characterization is false against its own base file.
- E19.md:36/:338 cite `SC1.md:134-136`, which does not carry the cited fact; `150133` is
  absent from SC1.md entirely. R5.md:214's `E4.md:24` pointer misses E4's 4/5 reading.

**Inference (stated as such):**
- The restore was `cp -p` from `.20261018-150133.bak` — the command is observed; that it
  *caused* the mtime/ctime state I measured is the (single, consistent) explanation.
- The 17:32:20Z session and the 17:50:34Z session are the two writers of the entire churn
  chain; their file-history snapshots match every intermediate hash, and no other writer
  evidence exists.
- The receipt itself (501 B, hash-shaped, btime predating all seat artifacts) is
  parent-authored; nothing in it is unverifiable.

**Unknown:**
- Whether the interactive session or its user will write again during the remaining window
  (the session was still live at 18:02:39Z; process 530913 has since exited, PID gone at
  18:28Z). The post-pair seat must re-check, not assume.
- Why the C1 instance `M corpus/README.md` (mentioned in E16.md:348) and the round's own
  work-tree edits coexist with a still-live writer on the home surface — orthogonal, but
  the post-pair bracket should note both.

## 5. Scope compliance

Only repo write: this report. No config edits (the drifted file was NOT touched — all my
config access was reads/stat/diff against backups), no git mutations (HEAD `679af5d`,
status `?? .ufo/waves/arc2-loop1-round3/` throughout), no installs, no network, no MCP
session, no battery leg. Secret material (API keys visible in config diffs) was never
printed — where a diff line contained a key, the excerpt is redacted or replaced with a
length marker in this report. Scratch: `/tmp/arc2-l3r3-CR8-scratch/` (`gen1.diff`,
`gen2.diff`, `driftbase.diff`, `cited-r2.txt`, `cited-r3.txt`, `tail3.txt`) — my namespace
only; no other seat's files touched. No processes of mine remain (`ps … | grep
arc2-l3r3-CR8` → empty).
