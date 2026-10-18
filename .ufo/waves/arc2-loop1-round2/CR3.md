# CR3 (critic) — attack on C3: 5-path overreach — what do `.bashrc`/`.profile` digests actually prove?

Read-only seat. Everything below was run/read by this seat on 2026-10-18 in
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. No repo file was edited; this report is
the seat's only write. Scratch confined to `/tmp/arc2-l2r2-CR3-*`. No git mutations, no
config edits, no installs, no network. No secret values read or emitted (env key NAMES and
paths only; the one live value quoted is compared by bytes, never printed).

## Verdict

**KEEP the 5-path pair — adding `.bashrc`/`.profile` strengthens coverage, not weakens it —
but BOUND the claim wording: the digests prove "five files' bytes unchanged", never
"provider environment unchanged".** The strongest objection stands as a *wording* refutation,
not a pair refutation: a `.bashrc` sha256 is **mode-blind** (on bash 5.3.15-1 the same file
contributes different line-subsets per invocation mode — `bash -c` with socket stdin reads
lines 3–24 only, `bash -i` reads all, `bash -l` reaches it via `.bash_profile` pre-guard,
`sh -l` never reads it at all) and **expansion-blind** (`~/.bashrc:63` is a `$(find "$(npm
root -g)" …)` substitution whose output depends on PATH/fnm state outside the pair — today
`npm root -g` resolves to a root that *has* wakaru under an interactive PATH but to the mise
node root that has *no* wakaru in the bare harness). Against that: the live carrier datum is
real — the running kimi client's `REA_WAKARU_COMMAND` is byte-identical (130 B, verified
twice) to the `~/.bashrc:63` expansion under `bash -i`, while its session-bash parent and
the alacritty ancestor carry that key in neither — so `.bashrc` is on the actual carrier path
of a live client. Net: extension kept; claim constrained; `.profile` kept with an honest
coverage note (it is shadowed by `.bash_profile` for every bash login shell on this host and
only serves sh-mode login shells); two residual gaps named (§4).

## 1. Evidence — commands run THIS session with observed output

### 1.1 The round-2 receipt is real, 6/5/1, and zero-drift holds so far (my own runs)

```
$ wc -l < .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt          → 6
$ grep -cE '^[0-9a-f]{64}  /' …config-pre-pair.txt                          → 5
$ grep -cE '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$' …    → 1
$ sha256sum …config-pre-pair.txt  → 4097ec77397308855bfb170733cf32d8c001de298ed1bf9bc1f4753ec25c6245 (501 B)
$ tail -n +2 …config-pre-pair.txt | sha256sum -c -     # at 17:0xZ and again 17:22Z
… 5/5 OK, rc=0 (devin/omp/kimi/bashrc/profile all OK)
$ sha256sum ~/.bashrc ~/.profile  → 7d2ca28a… / 6c6be761…   (= receipt :5-6, = round-1 E15.md:100-101)
```
Receipt timestamp `:1` = `2026-10-18T16:57:35Z`. Both added paths carry their expected
digests; the extension did enter at THIS round's pre-pair as C3 states.

### 1.2 Carrier-mode map (fake-home marker tests + strace; decisive for the ambiguity question)

Fake homes under `/tmp/arc2-l2r2-CR3/hA…hD`; marker exports placed before/after an
interactive guard; real-home probes with `env -i HOME=/home/vgpnk PATH=/usr/bin:/bin`:

```
bash --noprofile --norc -c   → (no keys)         bash --norc -c            → (no keys)
bash --noprofile -c          → GHIDRA JAVA       (rc read; noprofile = profile off)
bash -l -c (real home)       → GHIDRA JAVA       (via ~/.bash_profile:5 → ~/.bashrc pre-guard)
bash -i -c (real home)       → GHIDRA JAVA + 7 REA_*  (all 9)
sh -l -c (real home)         → GHIDRA JAVA + 6 REA_* (no REA_WAKARU)
script form `bash <file>`    → (no keys)         strace: 0 rc-file opens
```

```
$ strace -f -e trace=openat … bash -c true   (socket stdin, as this harness uses)
openat(… "/etc/bash.bashrc", O_RDONLY) = 3
openat(… "/home/vgpnk/.bashrc", O_RDONLY) = 3
$ PS4='+${BASH_SOURCE}:${LINENO}+ ' bash -x -c true
+/etc/bash.bashrc:6+ [[ hxBc != *i* ]]        # /etc guard fires
+/home/vgpnk/.bashrc:3+ export PATH=…          # .bashrc entered
… :18 eval fnm env … :23 export GHIDRA_INSTALL_DIR=… :24 export JAVA_HOME=…
+ return                                       # ~/.bashrc:29 guard — REA_* (:58-64) NOT reached
```
Marker tests by stdin type (fake home with guard): `bash -c` socket stdin → `TOP=1
BOTTOM=unset`; devnull/pipe → `TOP=unset`; script form → unset in all three. So the sshd/rshd
documented path (`bash -c` with a socket on stdin — exactly what this harness uses) DOES
source `~/.bashrc`, but only up to the `:29` guard. `bash <script>` never reads rc files
(E15's table rows A/B used script form, so their "no keys" readings are correct for that
form only; their table contains no `-c` row).

### 1.3 Live carrier datum — kimi's `REA_WAKARU_COMMAND` traces to `~/.bashrc:63`

```
$ tr '\0' '\n' < /proc/2342280/environ | grep '^REA_WAKARU_COMMAND=' | cut -c1-70
REA_WAKARU_COMMAND=/home/vgpnk/.local/share/fnm/node-versions/v24.21.0
$ env -i HOME=/home/vgpnk PATH=/usr/bin:/bin bash -i -c 'printf "%s" "$REA_WAKARU_COMMAND"'
/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/lib/node_modules/wakaru/node_modules/@wakaru/cli-linux-x64/wakaru
$ cmp … → BYTE-IDENTICAL (130 B)   # verified twice: ~17:0xZ and 17:17:01Z
$ diff key-NAME sets, kimi vs its parent session bash:
16a17  > REA_WAKARU_COMMAND        # kimi has it; parent bash's /proc environ does not
```
`/proc/PID/environ` is an exec-time snapshot (controls: node `process.env` marker → 0;
bash exporting then exec'ing `sleep` → 1), so the session bash's own environ predates its
interactive rc run while kimi inherited the post-rc runtime env. Ancestors: alacritty
`2341401` (started 11:41:07) and systemd user env both carry 6 `REA_*` keys but **no**
WAKARU; kimi started 11:41:35. The kimi binary embeds `src/utils/process/shell-env.ts` /
`detectShellEnvironment` / `shellEnv` (strings at byte offsets ~1134094+), i.e. the client
may also refresh its own shell env — either path, the value traces to `.bashrc:63`.
Expansion input caveat: `npm root -g` under the harness resolves to
`/home/vgpnk/.local/share/mise/installs/node/26.12.0/lib/node_modules` (no `wakaru/` dir
there — checked), while under an interactive PATH it resolves to the fnm v24.21.0 root
(where the wakaru ELF exists, `664fa067…`, 26793296 B); the fnm alias
`~/.local/share/fnm/aliases/default → …/v24.21.0/installation` is a symlink outside the pair.

### 1.4 What the other records say (pointers resolved this session)

- Round-1 `E15.md:117-131` — the env -i table (script form only) and the "supplies keys only
  to interactive shells" reading; my §1.2 sharpens it: script form reads nothing, `-c`+socket
  reads the pre-guard subset, so "which subset executed" is mode-dependent.
- Round-1 `E15.md:14-31,39-44` — grounds (PROVINCE.md:15-26/47/124-125 drift-prone pointers;
  r4u-05 precedent; `.bash_profile` exclusion; systemd-env not a file).
- `PROVINCE.md:47` resolves (`JAVA_HOME … .bashrc:24 + .profile:4`); `PROVINCE.md:124-125`
  (wakaru ELF-not-shim, fix at `.bashrc:63`) resolves; `corpus/knowledge/2026-10-13-r4u-05-wakaru-oom.md:104-105`
  documents the version-robust resolver that IS the current `.bashrc:63`.
- `~/.bashrc:23,24` GHIDRA/JAVA; `:29` guard; `:58-64` 7× `REA_*`; `:69,:73` token
  substitutions. `~/.profile:3,4,7-12` (6× `REA_*`, no WAKARU). `~/.bash_profile:5` sources
  `.bashrc`, `:8` prepends `~/.local/bin`; no key exports (exclusion accurate).
- `SKILL.md:218` still says "Hash exactly the three drift-sensitive client configs";
  `:224-225` gate `wc -l`=4/`grep -cE`=3; `:237` "exactly three `OK` lines" — the SOP
  contradicts live practice (E21 drafts the amendment; `E21.md:39-44` notes the stale text
  and flags E1.md:106's "313 B" vs measured 501 B — my `wc -c` = **501**).
- `SCORECARD.md:621` capability row still says "three operator-config sha256s" — needs the
  5-path wording if the row is re-entered. `LOG.md:1010-1011` records the extension as
  carried debt from round 1.
- `tail -n3` false-pass hazard (E15 round-2 `:15-19`; `E21.md:82-90`): my own reproduction —
  `tail -n3` on the 6-line receipt selects config.toml + .bashrc + .profile and **silently
  drops devin/omp**; the round-1 diff idiom would still print MATCH while never examining
  them. Correct selector: `tail -n +2 … | head -n3`.

### 1.5 Landing-condition status (C3's own gate: zero drift + committed receipts)

At my last check (17:22:17Z): `.ufo/waves/arc2-loop1-round2/receipts/` holds only
`config-pre-pair.txt`; the post-pair exists only as a /tmp draft (`E15.md:94-101`, capture E
17:08:57Z); `git status --porcelain` → `?? .ufo/waves/arc2-loop1-round2/`; HEAD `165057e`.
Zero drift holds (5/5, multiple captures); **the commit half of the entry condition is not
yet met** — same class of landing dependency round-1 CR3 recorded.

## 2. The strongest objection, at full strength

- **O1 — mode-blindness.** A `.bashrc` digest does not pin which invocation mode sourced it
  or which lines executed. On this host the same unchanged file yields 0 keys (script form),
  GHIDRA+JAVA (socket-stdin `-c`, login via `.bash_profile`), or all 9 (interactive).
  A zero-drift claim over the digest therefore cannot support any statement about what the
  client's shell actually executed.
- **O2 — expansion-blindness.** `.bashrc:63` and `:69,:73` are command substitutions; their
  outputs depend on PATH, the fnm alias symlink, node installs and helper binaries — none in
  the pair. `.bashrc` bytes constant ⇒ the wakaru binding can still flip (mise root has no
  wakaru; the harness's own `npm root -g` resolves there) while all five receipts stay green.
- **O3 — `.profile` is nearly dormant for bash users.** `~/.bash_profile` exists and shadows
  `.profile` for every bash login shell (fake-home T3/T4: `bash -l` reads `.bash_profile`
  only; `.profile` is read by `sh -l`). One of the two added paths therefore adds much less
  than its presence suggests.
- **O4 — false-pass instrumentation.** The old `tail -n3` selector now silently drops
  devin/omp (§1.5) — an unchanged idiom that would report MATCH on a drifted pair.
- **Why these do not refute the pair.** They refute *wording*, not the measurement: the pair
  never claimed mode- or expansion-level custody; and the extension's purpose (E15 grounds
  1–2) is to close a false-green blind spot — which §1.3 shows is live, not theoretical
  (kimi's WAKARU came through `.bashrc:63` while the 3-config pair would have stayed green
  through any `.bashrc` edit). The costs of keeping it are claim fragility (an operator edit
  voids the round's claim — SOP already disposes the claim, not the config) and precision
  dilution if misread — both handled by wording, not by dropping the paths.

## 3. Text for the parent to land VERBATIM (fenced)

```
C3 5-path custody extension — critic disposition (arc2-loop1-round2, seat CR3): KEEP the
5-path pair; bound the claim wording to "five files' bytes unchanged", never "provider
environment unchanged". What the digests prove: the five files' bytes were unchanged across
the battery window (pre .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt,
2026-10-18T16:57:35Z, 6/5/1 shape, self-hash 4097ec77397308855bfb170733cf32d8c001de298ed1bf9bc1f4753ec25c6245;
5/5 sha256sum -c OK; post drafts 17:00-17:09Z). What they do not prove: (a) carrier mode —
a .bashrc digest is mode-blind: on bash 5.3.15-1, `bash -c` with socket stdin (sshd/rshd
path; the form this harness uses) reads ~/.bashrc lines 3-24 only (guard ~/.bashrc:29),
`bash -i` reads all (incl. :58-64), `bash -l` reaches it via ~/.bash_profile:5 (pre-guard),
`sh -l` reads ~/.profile instead, and script-form `bash <file>` reads neither (strace: 0
rc-file opens); (b) expansion — ~/.bashrc:63 is `$(find "$(npm root -g)" ...)`, PATH/fnm
dependent (fnm alias ~/.local/share/fnm/aliases/default and node installs are outside the
pair; the mise node root has no wakaru dir). Live carrier datum (OBSERVATION): the running
kimi client's REA_WAKARU_COMMAND (130 B) is byte-identical to the ~/.bashrc:63 expansion
under `bash -i` (verified twice, ~17:05Z and 17:17:01Z), while its session-bash parent and
alacritty ancestor carry the key in neither — ~/.bashrc:63 is on the actual carrier path of
a live client, so the extension closes a real false-green blind spot. Honest residuals:
~/.bash_profile (sources ~/.bashrc, prepends PATH) is excluded; the systemd-user-env chain
(6 REA_ keys, no WAKARU) is not a file; ~/.profile is shadowed by ~/.bash_profile for bash
login shells (serves sh-mode login shells only — `sh -l` reads it; kept, with this note).
Instrument hazard (unchanged): `tail -n3` on the 6-line receipt silently drops devin/omp and
can false-pass a drifted pair — the correct selector is `tail -n +2 <receipt> | head -n3`.
Entry condition: zero drift holds (5/5, multiple captures); committed receipts do NOT yet
(round-2 post-pair is a /tmp draft, E15.md:94-101; .ufo/waves/arc2-loop1-round2/ untracked at
HEAD 165057e) — the capability row enters only after the parent commits both receipts.
```

SOP-amendment addendum the parent should append to E21's drafted block (carrier caveat):

```
- **The shell-file digests are mode- and expansion-blind.** A ~/.bashrc hash does not say
  which invocation mode sourced it or which lines ran (script form: none; socket-stdin
  `bash -c`: lines to the ~/.bashrc:29 guard; interactive: all; `bash -l` via
  ~/.bash_profile:5: pre-guard). And its key values are command substitutions
  (~/.bashrc:63/:69/:73) whose outputs depend on PATH and state outside the pair. Treat the
  pair as byte-custody of the carrier files — never as custody of the provider environment.
```

## 4. Honest residual value (labeled)

- **OBSERVATION** — round-2 receipt reproduces 6/5/1 with self-hash `4097ec77…` (501 B);
  `sha256sum -c` 5/5 OK at 17:0xZ and 17:22Z; `.bashrc` `7d2ca28a…`, `.profile` `6c6be761…`.
- **OBSERVATION** — mode map: script form reads no rc files (strace 0); socket-stdin `bash
  -c` reads `~/.bashrc` to the `:29` guard (GHIDRA+JAVA only); `bash -i` all 9 keys;
  `bash -l` via `.bash_profile` → pre-guard; `sh -l` reads `.profile` (8 keys, no WAKARU).
- **OBSERVATION** — kimi's `REA_WAKARU_COMMAND` == `~/.bashrc:63` `bash -i` expansion,
  byte-identical 130 B, twice; kimi has the key while parent bash and alacritty lack it.
- **OBSERVATION** — `tail -n3` on the 6-line receipt selects config.toml/.bashrc/.profile
  (drops devin/omp); receipts uncommitted; post-pair only as /tmp draft; E1.md:106's
  "313 B" is wrong (my `wc -c` = 501; E21.md:42-43 and V3.md:71 also say 501).
- **INFERENCE** — the 5-path extension does not weaken the pair; it removes a real
  false-green blind spot for the WAKARU binding and (thinner) for sh-mode login shells.
  Its costs are wording discipline and claim fragility, not measurement quality.
- **INFERENCE** — `.bashrc` is the only *file* on the observed carrier path of the live
  client's WAKARU; the other 8 keys reached the client through the systemd-user-env chain
  whose seeding file is not identifiable from today's artifacts (session start 11:41:07
  predates this session's observation).
- **UNKNOWN** — which mode kimi's env refresh used (`detectShellEnvironment` in the binary
  vs inheritance at exec); whether the session-env 6 REA_ keys were seeded from `.profile`,
  uwsm env files, or elsewhere at session start; whether the parent lands the 5-path SOP
  amendment this round; exact future drift risk (point-in-time captures only; mutate-and-
  revert undetectable — BC3.md:14 threat transfers).

## 5. Scope compliance / threats

- Read-only on every repo and home file except this report; no git mutations; no config
  edits; no installs; no network (no command attempted one). Scratch `/tmp/arc2-l2r2-CR3-*`.
- No MCP sessions opened by this seat; final closure check `pgrep -af 'rea-agents|scripts/[r]ea.mjs'`
  → no rea-agents server processes (one unrelated node tool-contract probe process was
  observed at ~17:15Z, not this seat's, not touched).
- Threats carried: hashes cannot exclude mutate-and-revert; mtime is forgeable; both
  captures are point-in-time; the expansion inputs (fnm alias symlink, node installs) are
  unmonitored.
