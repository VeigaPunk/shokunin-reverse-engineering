# CR8 (critic) — provenance attack on the round-2 5-path pre-pair receipt

Seat CR8, wave arc2-loop1-round2, 2026-10-18. Read-only except this report (the
seat's only write; scratch confined to `/tmp/arc2-l2r2-CR8-*`). Every command
below was run by this seat in this session (16:59:54Z–17:09:14Z) at HEAD
`165057e`; every `path:line` pointer was re-resolved this session. No repo file
was modified (`git status --porcelain` → `?? .ufo/waves/arc2-loop1-round2/` only).

## 1. Verdict

**ATTACK FAILS on the artifact; PARTIAL REFUTE of the seat line's premise.**

The receipt survives all three attacks: its creation instant is filesystem-proven
and provably precedes every round-2 probe and every round-2 seat artifact; its
five values are true at every instant from creation to my last check because
neither shell file has been written since 2026-10-15/16; and the cross-seat
agreement is 4-way on raw digests under two hash tools, not parent-only.

**The seat line's premise — "two new files nobody corroborated pre-dispatch — the
pre-pair is parent-only this time" — is false for `~/.bashrc` and true with an
asterisk for `~/.profile`:**

- `~/.bashrc` `7d2ca28a…` has **8 pre-dispatch records in committed blobs**
  (luna rounds 6–9, committed 2026-10-17T00:28:57-03:00 at `4b806e14`), i.e.
  ~17 h before the receipt. "Nobody corroborated" is wrong.
- `~/.profile` `6c6be761…` has **exactly one** pre-dispatch record —
  `.ufo/waves/arc2-loop1-round1/E15.md:101` — written by **the same seat that
  proposed the extension**, committed at `df31bfb`
  (`2026-10-18T13:54:36-03:00` = `16:54:36Z`), **2 m 59 s** before the parent's
  receipt btime. It is not "nobody", but it is a single proposer-only witness.
  This does **not** falsify the zero-drift claim (§4.5) because `.profile` was
  frozen 3 days earlier, but it is the one place where the agreement chain rests
  on one seat's word.
- "The pre-pair is parent-only this time" is unsupported: round 2 already carries
  ≥4 independent post-dispatch capture events (§3.6). What round 2 lacks is
  *pre-dispatch* corroboration of `.profile` specifically — and no round-2 seat
  could have supplied it, since the receipt precedes the first seat artifact by
  106 s by construction (§3.3).

**The real gaps are landing gaps, not forgery gaps:** the post-pair does not
exist, the receipt is untracked, and `SKILL.md`'s custody SOP still specifies the
3-path/4-line/3-hash form — so the round-2 receipt **fails the landed SOP's own
shape gate as written** (§4.2). The cross-seat agreement bar is specified in §5;
it has no landed definition today (§4.8).

## 2. Target

`.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt` — 6 lines, 501 bytes,
sha256 `4097ec77397308855bfb170733cf32d8c001de298ed1bf9bc1f4753ec25c6245`:

- `:1` timestamp `2026-10-18T16:57:35Z`
- `:2` `16f496e6…263a4` `/home/vgpnk/.config/devin/mcp_config.json`
- `:3` `38d2a1d0…b926b` `/home/vgpnk/.omp/agent/mcp.json`
- `:4` `3546e033…f9a2a` `/home/vgpnk/.kimi-code/config.toml`
- `:5` `7d2ca28a…6598` `/home/vgpnk/.bashrc` ← new path this round
- `:6` `6c6be761…4f30` `/home/vgpnk/.profile` ← new path this round

Attack 1 (timestamp): `:1` is self-asserted text; a forger could backdate it.
Attack 2 (content): the receipt could be fabricated from a state the battery did
not run under. Attack 3 (agreement): corroborating seats could be echoing the
parent rather than observing independently. Attack 4 (scope): the 5-path set
could omit a carrier of the same drift-prone material, so the pair would report
zero drift while the environment drifted (E15's own falsification case,
`.ufo/waves/arc2-loop1-round1/E15.md:31`).

## 3. Evidence — commands run and observed output

### 3.1 Creation forensics — single write burst, self-stamp matches to sub-second

```
$ stat -c '%n size=%s mtime=%y ctime=%z btime=%w' \
    .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt \
    .ufo/waves/arc2-loop1-round2/receipts .ufo/waves/arc2-loop1-round2
config-pre-pair.txt size=501 mtime=2026-10-18 13:57:35.906141732 -0300
  ctime=2026-10-18 13:57:35.906141732 -0300 btime=2026-10-18 13:57:35.906141732 -0300
receipts        size=38  mtime=2026-10-18 13:57:35.906141732 -0300
  ctime=2026-10-18 13:57:35.906141732 -0300 btime=2026-10-18 13:57:35.905141729 -0300
arc2-loop1-round2 size=16 mtime=2026-10-18 13:57:35.905141729 -0300
  ctime=2026-10-18 13:57:35.905141729 -0300 btime=2026-10-18 13:57:35.905141729 -0300
$ stat -f -c '%n fstype=%T' .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt
...config-pre-pair.txt fstype=btrfs
```

`btime == ctime == mtime == 16:57:35.906Z` (UTC). On btrfs `btime` is creation
time: the file was created in one write burst and has never been edited (any
later edit moves `ctime`/`mtime`). The self-asserted `:1` stamp `16:57:35Z`
matches the creation instant to within 0.906 s. The wave dir, `receipts/` dir and
the file differ by ≤1 ms — a single `mkdir -p` + write sequence with no room for
a hidden earlier artifact in that directory.

### 3.2 Byte accounting closes exactly (independent of `stat`)

```
$ wc -c < .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt   → 501
$ stat -c %s .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt → 501
$ awk '{print NR": len="length($0)}' .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt
1: len=20   2: len=107   3: len=97   4: len=100   5: len=85   6: len=86
$ awk '{s+=length($0)}END{print s"+"NR" = "s+NR}' <receipt>   → 495+6 = 501
$ tail -c 1 <receipt> | xxd   → 00000000: 0a   (single trailing LF)
$ wc -l < <receipt> → 6 ; grep -cE '^[0-9a-f]{64}  /' <receipt> → 5
$ grep -cE '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$' <receipt> → 1
```

Shape gate **6/5/1 passes**; line lengths sum to the file size with exactly 6 LF.
The receipt is a well-formed, complete 5-path artifact — not a truncated 4-line
one with an appended tail.

### 3.3 Ordering — the receipt provably precedes every round-2 probe and seat

```
$ stat -c '%W %w %n' /tmp/arc2-l2r2-* | sort -n | head -3
1792342761 2026-10-18 13:59:21.723407134 -0300 /tmp/arc2-l2r2-E13-scratch
1792342767 2026-10-18 13:59:27.740422230 -0300 /tmp/arc2-l2r2-E2-probe
1792342768 2026-10-18 13:59:28.179423332 -0300 /tmp/arc2-l2r2-E14
$ stat -c '%W %w %n' .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt
1792342655 2026-10-18 13:57:35.906141732 -0300 .../config-pre-pair.txt
```

The earliest round-2 seat artifact of any kind (50 entries in `/tmp/arc2-l2r2-*`)
is `16:59:21.723Z`; the receipt's creation instant is `16:57:35.906Z` — **106 s
earlier**. Battery legs are later still: leg 1 (doctor) start
`2026-10-18T16:59:31Z` (`E13.md:12`, `E13.md:106`); leg 2 census at
`E14.md:146-147`. Earliest round-2 report mtime is `E1.md` at `14:00:09.72 -0300`
= `17:00:09Z`. **No probe and no seat artifact precedes the receipt.**

### 3.4 Value truth — five captures across the window, zero divergence

```
$ sha256sum ~/.config/devin/mcp_config.json ~/.omp/agent/mcp.json \
    ~/.kimi-code/config.toml ~/.bashrc ~/.profile
16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4  /home/vgpnk/.config/devin/mcp_config.json
38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b  /home/vgpnk/.omp/agent/mcp.json
3546e033aeaf68093faf4099ea8289de5dea7ec224e7c557f08bfa9d51cf9a2a  /home/vgpnk/.kimi-code/config.toml
7d2ca28a245c44a1f5458921f0dff54823aa1e74ffa02eac2013b486e6a26598  /home/vgpnk/.bashrc
6c6be761d3b199c964c95e724d7cdc9f4f902e0c3bdd6a532361b20a53db4f30  /home/vgpnk/.profile
$ tail -n +2 <receipt> | diff - <(sha256sum <5 paths>)    → rc=0, empty
```

Captured at `16:59:54Z`, `17:00:45Z`, `17:04:49Z`, `17:08:01Z`; every capture
identical to the receipt `:2-6` (`diff` rc=0 each time).

```
$ tail -n +2 .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
rc=0
```
`-c` rc=0, 5/5 OK at `17:08:01Z`.

**No-write window for the two new paths** (this is what collapses the capture
instant for the shell files, exactly as round-1 CR8 did for the configs):

```
$ stat -c '%n size=%s mtime=%y ctime=%z btime=%w' ~/.bashrc ~/.profile
/home/vgpnk/.bashrc size=3601 mtime=2026-10-16 13:33:16.272618342 -0300
  ctime=2026-10-16 13:33:16.272618342 -0300 btime=2026-10-16 13:33:16.270642011 -0300
/home/vgpnk/.profile size=736 mtime=2026-10-15 03:12:07.440808802 -0300
  ctime=2026-10-15 03:12:07.440808802 -0300 btime=2026-10-03 19:47:18.586788370 -0300
$ stat -c '%n %F' ~/.bashrc ~/.profile ...   → all "regular file" (no symlink indirection)
$ openssl dgst -sha256 ~/.bashrc ~/.profile
SHA2-256(/home/vgpnk/.bashrc)= 7d2ca28a245c44a1f5458921f0dff54823aa1e74ffa02eac2013b486e6a26598
SHA2-256(/home/vgpnk/.profile)= 6c6be761d3b199c964c95e724d7cdc9f4f902e0c3bdd6a532361b20a53db4f30
```

`.bashrc` was last written `2026-10-16 13:33:16` (2 d before the receipt);
`.profile` `2026-10-15 03:12:07` (3 d before). Both are regular files (no symlink
could be re-pointed while the hash stayed "true"). Since neither has been written
in `[creation, 17:08:01Z]`, the receipt's `:5`/`:6` values are true at **every**
instant of the window, not merely at the claimed capture instant.

### 3.5 Cross-seat agreement — re-derived mechanically, not trusted from prose

Whole-wave scan for **path-adjacent** hash claims (a 64-hex immediately followed
by one of the five paths) across both waves:

```
$ python3 <scan>   # regex: ([0-9a-f]{64})(  |\s+)<path>(?![\w/.-])
adjacent-shape occurrences matching expected: 129
DIVERGENT (path-adjacent, wrong hash): NONE
```

129 path-adjacent occurrences across `.ufo/waves/arc2-loop1-round1/` and
`round2/`, **zero divergent values**. No seat anywhere claims a different hash
for any of the five paths.

**Independent raw-digest captures (not merely `sha256sum -c` against the parent's
file)** — this is what defeats attack 3:

- `V3.md:20` capture instant `2026-10-18T16:59:43Z`; `V3.md:56-60` prints
  `openssl dgst -sha256` raw digests for **all five** paths; `V3.md:44-48` diffs
  its own 5-line block against the receipt's block (`b4d87ab8…` identical on both
  sides); `V3.md:71` measures `stat -c %s` → 501.
- `V4.md:30` four captures `17:00:06Z / :09 / :17` (`sha256sum`) and `:40`
  (`openssl dgst -sha256`) — "same six digests"; `V4.md:117-118` prints the
  `.bashrc`/`.profile` digests in its verbatim block; `V4.md:125` "a second tool
  reproduces all six digests".

Corroboration via `-c` only (still valid for value-truth, weaker for instant):
`E1.md:97-103` (rc=0, 5/5 OK; captures `16:59:18Z`/`16:59:40Z`),
`E2.md:147-152`, `SC2.md:85`, `E19.md:72-75`, `E13.md:78` (leg-1, `16:59:31Z`),
`E14.md:146,158` (pre **and** post battery). My own four captures add a 5th seat.

### 3.6 Cross-round continuity is anchored in a committed blob

```
$ diff <(git show HEAD:.ufo/waves/arc2-loop1-round1/receipts/config-post-pair.txt | tail -n +2) \
       <(tail -n +2 .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt | head -n3)
rc=0   (empty)
$ git ls-files .ufo/waves/arc2-loop1-round1/receipts/
.../MANIFEST.txt .../config-post-pair.txt .../config-pre-pair.txt ... (9 files)
$ cmp -s <(git show HEAD:.../config-pre-pair.txt) .../config-pre-pair.txt  → IDENTICAL
$ cmp -s <(git show HEAD:.../config-post-pair.txt) .../config-post-pair.txt → IDENTICAL
```

The round-1 pair **is** durable and byte-identical to its committed blobs, and
round-2's first three lines are byte-identical to round-1's committed post-pair.
The config 3-path therefore has an unbroken, committed anchor from round 1's
pre-pair through round 2's pre-pair.

### 3.7 Attack 4 — scope: the 5-path set is complete under its own test

E15 justified the extension by "files carrying PROVINCE.md's drift-prone env-key
material". I closed the transitive hole E15 did not examine — `~/.bashrc:33`
sources the omarchy chain:

```
$ sed -n '33p' ~/.bashrc
source ~/.local/share/omarchy/default/bash/rc
$ cat ~/.local/share/omarchy/default/bash/rc
source ~/.local/share/omarchy/default/bash/envs
source ~/.local/share/omarchy/default/bash/shell
source ~/.local/share/omarchy/default/bash/aliases
source ~/.local/share/omarchy/default/bash/functions
source ~/.local/share/omarchy/default/bash/init
[[ $- == *i* ]] && bind -f ~/.local/share/omarchy/default/bash/inputrc
$ grep -rnE 'REA_|GHIDRA_INSTALL_DIR|JAVA_HOME' ~/.local/share/omarchy/default/bash/
rc=0   (no output)
$ for f in envs shell aliases functions init inputrc rc; do ... grep -c ...; done
envs 0 | shell 0 | aliases 0 | functions 0 | init 0 | inputrc 0 | rc 0
```

The omarchy chain (7 files, 2 further nested `source` hops into
`/usr/share/bash-completion` and fzf) carries **zero** drift-prone keys. The
`~/.bashrc` hash covers its own exported keys; nothing downstream re-exports them.

Other candidate carriers, checked this session:

```
$ for f in ~/.bash_profile ~/.bash_login ~/.bash_logout ~/.profile ~/.bashrc; do ...; done
/home/vgpnk/.bash_profile exists size=174 lines=8
/home/vgpnk/.bash_login ABSENT
/home/vgpnk/.bash_logout exists size=21 lines=3
$ grep -ln 'REA_\|GHIDRA_INSTALL_DIR\|JAVA_HOME' ~/.bash_profile ~/.bash_login ~/.bash_logout ~/.profile ~/.bashrc
/home/vgpnk/.profile
/home/vgpnk/.bashrc
$ sed -n '5p' ~/.bash_profile
[[ -f ~/.bashrc ]] && . ~/.bashrc
$ grep -cE 'export.*(REA_|GHIDRA|JAVA_HOME)' ~/.bash_profile → 0
```

`.bash_profile` sources `.bashrc` and adds a PATH entry; it exports no key of its
own — E15's exclusion (`E15.md:42-44`) is correct, and its hash `a21bfd7d…` is
unchanged from E15's capture. `.bash_logout` carries none.

**The one named scope-out that is a live drift surface:** the systemd user
environment carries 8 of the same keys, and I verified all 8 are byte-equal to
what a login shell exports:

```
$ systemctl --user show-environment | grep -cE '^REA_'   → 6
$ systemctl --user show-environment | grep -E '^REA_|^GHIDRA|^JAVA_HOME' | cut -d= -f1
GHIDRA_INSTALL_DIR JAVA_HOME REA_ADB_PATH REA_APKTOOL_COMMAND
REA_BINWALK_COMMAND REA_JADX_MCP_JAR REA_PWNTOOLS_PYTHON REA_UNBLOB_COMMAND
$ for k in <those 8>; do compare systemd value vs bash -lc value; done
all 8: systemd==bash-login: YES
```

`REA_WAKARU_COMMAND` is absent from systemd (`grep -c` → 0) and present in
`.bashrc` (`grep -c` → 1) — consistent with E15's `sh -l` observation
(`E15.md:124`). systemd is not a file, so it cannot be receipted; E15 named it as
excluded (`E15.md:57-58`). It remains the strongest surviving form of attack 4.

### 3.8 Receipt artifact identity reproduced; no rival identity anywhere

```
$ sha256sum .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt
4097ec77397308855bfb170733cf32d8c001de298ed1bf9bc1f4753ec25c6245
$ sha256sum .ufo/waves/arc2-loop1-round1/receipts/config-pre-pair.txt
7369fbcb3bfd91cf5bdf48d0871ae670bce133d5d091a35e8fd7826c0cef04e4
$ sha256sum .ufo/waves/arc2-loop1-round1/receipts/config-post-pair.txt
dec9c8c8b96630700f46d7a5ea4d81c1686ccfd1c74a4ca4087c25cc0f7ea00e
$ git grep -n '4097ec77\|7369fbcb' -- . ':(exclude).ufo'   → rc=1
```

Three distinct artifacts, three distinct self-hashes; **neither self-hash appears
in any editable file yet** — no risk of the round-1/round-2 identities being
conflated in the record (V3 flags this risk at `V3.md:76`).

Distinct timestamps appearing on any pre-pair line across all round-2 reports:
`{16:57:35Z, 16:59:31Z, 16:59:43Z, 17:01:02Z}` — only the first is a claim about
the receipt's own stamp; the other three are seats' capture instants.

### 3.9 Session closure and repo state

```
$ pgrep -af '[r]ea.mjs'   → rc=1 (no match), checked at 16:59:54Z, 17:08:01Z, 17:09:14Z
$ find .ufo/waves/arc2-loop1-round2 -type f
.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt   (+ 21 seat .md reports)
$ git ls-files .ufo/waves/arc2-loop1-round2/ | wc -l   → 0
$ git rev-parse --short HEAD → 165057e ; git status --porcelain → ?? .ufo/waves/arc2-loop1-round2/
$ git diff --stat HEAD -- SKILL.md   → (empty, rc=0)
```

No REA process remains. No post-pair receipt and no battery leg artifact exist
under `receipts/`. The round-2 directory is entirely untracked.

## 4. Residual holes (ranked by what could falsify a claim)

1. **Post-pair absent; receipts untracked — C3's own gate is unmet.** The seat
   line conditions the capability row on "zero drift + committed receipts".
   `git ls-files .ufo/waves/arc2-loop1-round2/` → **0**; `receipts/` holds only
   the pre-pair. Round-1's durability precedent is satisfied (its 9 receipt files
   are tracked and byte-identical to their blobs), but round 2's is not. Not a
   forgery hole — a landing hole, and it is hard-gating.
2. **The landed SOP contradicts the receipt in hand.** `SKILL.md:218` says "Hash
   exactly the **three** drift-sensitive client configs"; `SKILL.md:224-226` gates
   the shape at `wc -l` = 4, hash lines = 3, timestamp = 1. The round-2 receipt
   measures **6/5/1** and would be **rejected as malformed by the SOP as landed**.
   `git diff HEAD -- SKILL.md` is empty, so C3's "custody SOP amendment (3-path →
   5-path)" has **not** landed. Independently observed by `E18.md:137-146`
   ("The custody SOP still specifies the 3-path / 4-line / 3-hash form") and
   drafted by `E21.md:1-13`; the durable practice and the durable SOP disagree
   until the parent lands the amendment. This is the sharpest outstanding item.
3. **`tail -n3` is no longer a config selector.** On a 4-line receipt `tail -n3`
   and `tail -n +2` were content-identical; on this 6-line receipt `tail -n3`
   selects **kimi + bashrc + profile** — not the three client configs.
   `E21.md:82-91` demonstrates it; `E21.md:221-225` and `R7.md:125` carry the fix.
   Round 1's idiom (`S2.md:103`, `tail -n3` on the pre receipt) is now unsafe to
   reuse; any integration script copied from round 1 would silently compare the
   wrong set. E15's own round-1 note (`E15.md:214-217`) warned of this.
4. **Scope-out with no receipt: the systemd user environment.** It carries 8 of
   the same drift-prone keys, byte-equal to the login-shell values today (§3.7).
   A drift there would change provider wiring while all five hashed files stayed
   byte-identical — the exact falsification shape E15 used to justify the
   extension, one level out. Named as excluded by E15 (`E15.md:57-58`) and not a
   file, so it cannot be receipted; it must land as an explicit limitation, not
   silence.
5. **`.profile`'s pre-dispatch chain is single-witness and proposer-only.**
   `6c6be761…` appears pre-dispatch only in `.ufo/waves/arc2-loop1-round1/E15.md`
   (4 occurrences: `:101` the capture, `:42`/`:138` the "0 hits" claim, `:229` the
   conclusion), committed `16:54:36Z` — 2 m 59 s before the receipt's btime. No
   other seat and no other round ever recorded `.profile`. **This does not
   falsify zero drift**: `.profile` has mtime `2026-10-15 03:12:07`, so any honest
   capture between then and now necessarily yields `6c6be761…`; the value is
   over-determined by the no-write window. Record it as a *thin* pre-dispatch
   chain, not as a defect.
6. **Inherent custody limits (must land as limitations, unchanged from round 1).**
   Hash custody cannot exclude mutate-and-revert *before* the first capture:
   `.profile`'s `btime` is `2026-10-03 19:47:18` but its `mtime` is
   `2026-10-15 03:12:07` — the Oct 3→15 window is unprovable by this instrument.
   The pair also proves byte-identity of five named files only; it does not prove
   the battery *ran under* those configs (legs were launched via explicit pins,
   not via the configured clients). Neither falsifies zero drift.
7. **Clerical defect to fix at integration: `E1.md:106` states "(313 B)" for the
   round-2 receipt.** The artifact is **501 B** (`wc -c` = `stat -c %s` = 501;
   `495 + 6 LF` = 501). Correct in `V3.md:7`/`:71`, `E19.md:75`, `E13.md:78`,
   `E21.md:36`; already flagged independently by `E21.md:43` and `R6.md:256`.
   My check is a third independent confirmation. The hash is right in all of
   them — only the size is wrong. Do not carry E1's size into the record.
8. **The "cross-seat agreement bar" has no landed definition.** `git grep
   'agreement bar' -- . ':(exclude).ufo'` → **rc=1**; the phrase exists only as
   seat-report prose (`E11.md:3` "2-way agreement bar met"; `V3.md:7` "The 2-way
   agreement bar is met"). Round 1's de-facto bar was recorded in the record
   layer as "3-way corroborated E11/V4/V5" (`SCORECARD.md:681`). §5 specifies a
   durable bar; without one, "2-way met" is unfalsifiable prose.

## 5. The cross-seat agreement bar (specified)

Four clauses; all four must hold for a custody receipt to support a zero-drift
claim. Clauses A/B/C are the bar; D is the symmetry condition.

- **A — ordering is filesystem-proven, not self-asserted.** The receipt file's
  `btime` (and `ctime`/`mtime`, showing no later edit) must precede the earliest
  probe artifact and the earliest seat artifact of the round. Measured this
  round: receipt `16:57:35.906Z` vs earliest seat artifact `16:59:21.723Z`
  (Δ = 106 s) and leg 1 `16:59:31Z`. **MET.**
- **B — value truth is re-derived by ≥2 seats under ≥2 hash tools.** At least two
  seats other than the capturing party must print the **raw digest lines** for
  **every** path (not merely `sha256sum -c` against the receipt, which cannot
  distinguish an honest receipt from a forged one that happens to match), and at
  least one of those must use a second tool. Measured: `V3.md:56-60`
  (`openssl dgst`, all 5, `16:59:43Z`) and `V4.md:30,117-118` (4 captures,
  both tools, `17:00:06–17:00:40Z`) — two independent seats, two tools, all five
  paths, plus `-c` corroboration from `E1`/`E2`/`SC2`/`E19`/`E13`/`E14` and this
  seat. **MET** — and note the bar is met *for the two new paths*, not only for
  the three configs.
- **C — durability.** Both receipts committed TRACKED before the round closes.
  Measured: `git ls-files .ufo/waves/arc2-loop1-round2/` → 0. **NOT MET** (parent
  step).
- **D — symmetry.** The post-pair must be the identical 5-path/6-line form;
  a pre-only or post-only shell-file leg is void (`E15.md:237-239`), and the
  config-only comparison must use `tail -n +2 … | head -n3`, never `tail -n3`.
  **NOT YET APPLICABLE** (no post-pair exists).

Corollary the parent should apply: for the **two new paths**, clause B is met by
post-dispatch seats only. That is sufficient for a zero-drift claim (clause A
supplies the ordering, and §3.4's no-write window supplies truth across the whole
window) but it is **not** sufficient to claim the shell-file leg was
*independently corroborated pre-dispatch* — for `.profile` no such corroboration
exists, and for `.bashrc` it exists only via luna rounds 6–9.

## 6. Text for the parent to land VERBATIM (fenced)

**6a — zero-drift + agreement statement for the round report / LOG (C3):**

```text
C3 custody verdict (round-2 5-path pre-pair, arc2-loop1-round2): 0/5 paths drifted.
Receipt .ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt — 6 lines,
5 hash lines, 1 timestamp, 501 B, sha256 4097ec77397308855bfb170733cf32d8c001de298ed1bf9bc1f4753ec25c6245
(stamp 2026-10-18T16:57:35Z; file btime==ctime==mtime==16:57:35.906Z, single write
burst, never edited). Ordering is filesystem-proven: the receipt's creation
instant precedes the earliest round-2 seat artifact (/tmp/arc2-l2r2-*, btime
16:59:21.723Z) by 106 s and leg 1 (16:59:31Z, E13.md:12) by 116 s.
Value truth: sha256sum -c over the receipt rc=0, 5/5 OK at 17:08:01Z; four
independent CR8 captures (16:59:54Z, 17:00:45Z, 17:04:49Z, 17:08:01Z) each
diff-empty against :2-6. Raw-digest captures by two other seats under two tools
cover all five paths: V3 (openssl dgst -sha256, 16:59:43Z, V3.md:56-60) and V4
(4 captures 17:00:06-17:00:40Z, sha256sum + openssl, V4.md:30,117-118); `-c`
rc=0 also recorded by E1, E2, SC2, E19, E13, E14. Whole-wave mechanical scan of
both arc2 waves: 129 path-adjacent hash occurrences, zero divergent values.
No-write window: ~/.bashrc mtime 2026-10-16 13:33:16, ~/.profile mtime
2026-10-15 03:12:07 — neither written in [16:57:35Z, 17:08:01Z], so :5/:6 are
true at every instant of the window, not only at the capture instant.
Cross-round continuity: round-2 :2-4 are byte-identical to round-1's COMMITTED
config-post-pair.txt (diff rc=0; round-1's 9 receipt files tracked and
byte-identical to their blobs).
Limitations (carry verbatim): (i) hash custody cannot exclude mutate-and-revert
before the first capture — ~/.profile btime 2026-10-03, mtime 2026-10-15;
(ii) byte-identity of the five named files only, not proof the battery ran under
them; (iii) ~/.profile has exactly ONE pre-dispatch in-repo record (round-1
E15.md:101, the proposing seat, committed 16:54:36Z) while ~/.bashrc has eight
(luna rounds 6-9) — the pre-dispatch chain for .profile is thin, though the
no-write window makes the value over-determined; (iv) the systemd user
environment carries 8 of the same drift-prone keys byte-equal to the login-shell
values and is NOT covered by the pair (not a file; E15.md:57-58).
Status: pre-half complete; post-pair receipt, battery leg artifacts and the
tracked commit are the parent's steps (git ls-files .ufo/waves/arc2-loop1-round2/
-> 0 at 17:09:14Z). No REA process remains (pgrep -af '[r]ea.mjs' rc=1).
```

**6b — SOP hazard bullet (for the SKILL.md amendment; E21.md:221-225 drafts it —
this is the same point, re-derived and confirmed by this seat):**

```text
- **`tail -n3` is not a config selector on a five-hash receipt.** On the
  superseded four-line three-path receipt `tail -n3` and `tail -n +2` were
  content-identical; on the six-line five-path receipt `tail -n3` selects kimi
  plus the two shell files, not the three client configs. Configs-only:
  `tail -n +2 "$R/config-pre-pair.txt" | head -n3`. Shell-file leg:
  `tail -n +2 "$R/config-pre-pair.txt" | tail -n2`.
```

**6c — integration note (do not propagate the size error):**

```text
Receipt size: the round-2 pre-pair artifact is 501 B (6 lines, 5 hash lines).
E1.md:106 states "(313 B)" — that is wrong and must not be carried into the
record. Confirmed three ways this round: CR8 (wc -c = stat -c %s = 501;
495 content bytes + 6 LF = 501), E21.md:43, R6.md:256. The sha256 is correct in
every report that cites it. Note also that round-1's receipt is a DIFFERENT
artifact (328 B, 4 lines, self-hash 7369fbcb...) — never conflate the two.
```

## 7. Conclusions (labeled)

- **OBSERVATION** — the round-2 receipt has `btime == ctime == mtime ==
  16:57:35.906Z` on btrfs, single write burst, never edited, created ≤1 ms after
  its parent dirs; its self-asserted `:1` matches to sub-second; 501 B by `wc -c`,
  `stat -c %s` and line-length arithmetic (495+6); shape 6/5/1 (§3.1, §3.2).
- **OBSERVATION** — the receipt's creation instant precedes the earliest round-2
  seat artifact by 106 s and leg 1 by 116 s; no probe or seat artifact precedes it
  (§3.3).
- **OBSERVATION** — four CR8 captures (`16:59:54Z`–`17:08:01Z`) and one
  `sha256sum -c` run (`17:08:01Z`, rc=0, 5/5 OK) all equal receipt `:2-6`;
  `.bashrc`/`.profile` are regular files with mtimes `2026-10-16 13:33:16` /
  `2026-10-15 03:12:07`, so no write occurred inside the window (§3.4).
- **OBSERVATION** — a mechanical path-adjacent scan across both arc2 waves found
  129 occurrences and **zero divergent** hash values; `V3` and `V4` printed raw
  digests for all five paths under two tools (§3.5).
- **OBSERVATION** — round-2 `:2-4` are byte-identical to round-1's **committed**
  `config-post-pair.txt`, and round-1's receipts are byte-identical to their
  committed blobs (§3.6).
- **OBSERVATION** — `~/.bashrc:33` sources a 7-file omarchy chain carrying zero
  drift-prone keys; `.bash_login` is absent, `.bash_logout` carries none,
  `.bash_profile` sources `.bashrc` and exports none (§3.7).
- **OBSERVATION** — the systemd user environment carries 8 of the same keys,
  byte-equal to login-shell values for all 8; `REA_WAKARU_COMMAND` is absent
  there and present in `.bashrc` (§3.7).
- **OBSERVATION** — `git ls-files .ufo/waves/arc2-loop1-round2/` → 0;
  `git diff HEAD -- SKILL.md` → empty; `SKILL.md:218`/`:224-226` still specify
  3 paths / 4 lines / 3 hashes; `pgrep -af '[r]ea.mjs'` rc=1 (§3.9).
- **OBSERVATION** — `.profile` `6c6be761…` has exactly one pre-dispatch in-repo
  record (`E15.md:101`, the proposing seat, committed `16:54:36Z`);
  `.bashrc` `7d2ca28a…` has eight committed luna-round-6–9 records (§1, §3.5).
- **OBSERVATION** — `E1.md:106` states 313 B for a 501 B artifact (§4.7).
- **INFERENCE** — attacks 1–3 fail. The receipt is timestamp-credible,
  content-true across the whole window, and corroborated by raw-digest captures
  from two independent seats under two tools, not by parent-only assertion.
- **INFERENCE** — attack 4 fails for the file surface (the omarchy chain is
  clean; `.bash_profile`/`.bash_logout` carry no keys) but **survives for the
  systemd user environment**, which carries 8 of the same keys and is outside the
  pair by construction. It must land as a stated limitation.
- **INFERENCE** — the seat line's premise is a **partial refute**: `.bashrc` was
  strongly corroborated pre-dispatch; `.profile` was corroborated only by its own
  proposer, 2 m 59 s before the receipt. Neither fact falsifies zero drift,
  because the shell files' mtimes make the values over-determined.
- **INFERENCE** — C3 cannot be closed on this evidence alone: the SOP amendment
  has not landed (so durable practice still contradicts the receipt), the
  post-pair is absent, and the receipt is untracked. Clause C of the bar in §5 is
  the gating one.
- **UNKNOWN** — whether the parent lands the SOP amendment verbatim from
  `E21.md` or a variant; whether the post-pair will be captured in the identical
  6-line form; whether any config drift occurs between my last check (`17:08:01Z`)
  and the parent's post-pair; the pre-`2026-10-15` history of `.profile` and the
  pre-`2026-10-16` history of `.bashrc` (unprovable by this instrument); whether
  the systemd user environment has drifted at any point in the past (no monitor
  exists).

## 8. Scope compliance

Read-only on all configs and shell files (`sha256sum`, `openssl dgst`, `stat`,
`grep` for key *names*, `systemctl --user show-environment` key names and
non-secret values only); read-only on every repo file except this report; no git
mutations; no installs; no network (the only outbound attempt observed was E13's
`npx` registry metadata revalidation, reported by that seat, not run by me);
scratch confined to `/tmp/arc2-l2r2-CR8-*`. No secret values were read or
emitted: `.bashrc` token lines (`:69`, `:73`) were not opened; the systemd
comparison hashed values without printing them. LOG.md/SCORECARD.md entries are
the parent's integration step (AGENTS.md rule).

## 9. Reproduction commands

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
git rev-parse --short HEAD; git status --porcelain
R=.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt
stat -c '%n size=%s mtime=%y ctime=%z btime=%w' "$R" "$(dirname "$R")"; stat -f -c '%T' "$R"
wc -c < "$R"; wc -l < "$R"; grep -cE '^[0-9a-f]{64}  /' "$R"
sha256sum "$R"
tail -n +2 "$R" | sha256sum -c -
tail -n +2 "$R" | diff - <(sha256sum ~/.config/devin/mcp_config.json ~/.omp/agent/mcp.json ~/.kimi-code/config.toml ~/.bashrc ~/.profile)
stat -c '%n %F mtime=%y btime=%w' ~/.bashrc ~/.profile
openssl dgst -sha256 ~/.bashrc ~/.profile
stat -c '%W %w %n' /tmp/arc2-l2r2-* | sort -n | head -3   # earliest seat artifact
diff <(git show HEAD:.ufo/waves/arc2-loop1-round1/receipts/config-post-pair.txt | tail -n +2) \
     <(tail -n +2 "$R" | head -n3)
git ls-files .ufo/waves/arc2-loop1-round2/ | wc -l
git diff --stat HEAD -- SKILL.md; sed -n '218p;224,226p' SKILL.md
grep -rnE 'REA_|GHIDRA_INSTALL_DIR|JAVA_HOME' ~/.local/share/omarchy/default/bash/
systemctl --user show-environment | grep -E '^REA_|^GHIDRA|^JAVA_HOME' | cut -d= -f1
pgrep -af '[r]ea.mjs'
```
