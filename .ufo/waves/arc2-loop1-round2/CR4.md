# CR4 (critic) — attack on the custody SOP amendment (3-path → 5-path): churn or required?

Seat CR4, wave arc2-loop1-round2, read-only. Every command below was run by
this seat this session at HEAD `165057e36f558c95eb02bf24de4a874d559d6950`
(2026-10-18, checks 17:00–17:10Z); scratch only under
`/tmp/arc2-l2r2-CR4-apply/`. This report is my only write; no repo file was
modified (`git status --porcelain` → `?? .ufo/waves/arc2-loop1-round2/` only).

## 1. Verdict

**REQUIRED FOR CONSISTENCY — not churn, not rewrite-adjacent.** The landed
SOP would, by its own text, classify this round's canonical receipt as
malformed and VOID the round's C3 claim. An amendment one round later is the
minimum-latency discharge of a debt round 1 pre-declared, in the only order
round 1's own rules permit. YAGNI fails because the extension is not
speculative: a 6/5/1 receipt is already frozen this round, the blind spot is
demonstrated (not hypothesized), and the section being edited is a living
forward contract, not a historical record.

The one genuine counter-consideration is a design critique, not a churn
finding: round 1 could have landed the 5-path form as a forward contract
without a same-round 6/5/1 receipt — E15 deliberately did not (evidence-
discipline), so round 2 pays one bounded second-touch. Cost measured in §5.

## 2. The decisive evidence — the landed SOP voids this round's receipt

SOP as landed (`58116aa`, 2026-10-18 13:54:36 -03:00), `SKILL.md:208-256`:

- `SKILL.md:217-218` — "Freeze the pre-pair before the round's first probe —
  no probe runs on an unpaired round. Hash exactly **the three** drift-
  sensitive client configs"
- `SKILL.md:224-225` — "gate the receipt's shape: `wc -l` = **4**,
  `grep -cE '^[0-9a-f]{64}  /'` = **3**"
- `SKILL.md:228` — "the shape gate is **mandatory, not advisory**"
- `SKILL.md:237` — "zero drift is rc 0, **exactly three** `OK` lines"
- `SKILL.md:251-252` — "**Malformed receipt: re-capture once; persistent
  malformation is VOID.**"

Round 2's canonical receipt
`.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt` (timestamp line
`:1` = `2026-10-18T16:57:35Z`, 501 B, self-hash
`4097ec77397308855bfb170733cf32d8c001de298ed1bf9bc1f4753ec25c6245`)
measured against the SOP's own gate — run by me:

```
$ R=.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt
$ wc -l < "$R"                                                     → 6
$ grep -cE '^[0-9a-f]{64}  /' "$R"                                 → 5
$ grep -cE '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$' "$R"  → 1
$ tail -n +2 "$R" | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
rc=0
```

SOP demands 4/3/1; the receipt is 6/5/1. A re-capture yields the same 6/5/1
(the five paths are fixed by the round's declared practice), so under
`SKILL.md:251-252` the outcome is persistent malformation → **VOID** — i.e.
the round's operability axis move dies by the rule round 1 landed. This is a
live contradiction at HEAD, not a hypothetical: the SOP's own preamble
(`SKILL.md:210`) says "Binding for every future live-probe round," and round
2 is one.

Round-1 receipts remain the compliant demonstration of the old form
(byte-verified this session, both 4 lines / 3 hash lines, self-hashes
`7369fbcb…` / `dec9c8c8…` matching `receipts/MANIFEST.txt`).

## 3. Churn test — what would make it churn, and why none of it holds

Churn/rewrite-adjacency would require at least one of: (a) editing round-1's
historical artifacts; (b) amending with no live contradiction; (c) re-landing
the same text again for cosmetic deltas.

- **(a) Refuted.** The amendment's surface is `SKILL.md:217-256` only. I
  scratch-applied E21's replacement block (extraction: `.ufo/waves/arc2-loop1-round2/E21.md:181-244`,
  the content between the ```` fences at `E21.md:180` and `:245`) onto a
  `/tmp` copy of SKILL.md:
  ```
  $ wc -l SKILL.md /tmp/arc2-l2r2-CR4-apply/SKILL.applied.md   → 312 / 336 (+24)
  PREFIX-IDENTICAL      # lines 1-216 byte-identical
  CRAFT-IDENTICAL       # lines 81-206 (craft section) byte-identical
  SUFFIX-IDENTICAL      # old 257+ == new 281+
  stale gate tokens in applied SOP region (208-281): 0
  # (the one grep hit is the block's own new phrase "the three drift-sensitive
  #  client configs plus the two shell files" — correct prose, not a leftover)
  rule blocks in applied craft section: 10   # 10/10 preserved
  ```
  Round-1 receipts, LOG entry (`LOG.md:987-991`), SCORECARD section
  (`SCORECARD.md:656-700`) and report are untouched by the block. No
  historical byte is rewritten.
- **(b) Refuted.** §2 — the contradiction is executable: the gate command
  fails against the frozen receipt at HEAD.
- **(c) Refuted.** The 5-path form has never been landed anywhere; `git grep
  'three drift-sensitive|4/3/1|exactly three'` over non-`.ufo` files returns
  only `SKILL.md:218,:237` as gate text (other hits are unrelated corpus
  phrases like "exactly three DT_NEEDED entries"). The amendment is the
  first forward-contract landing of the 5-path form, not a re-touch.

**Living-contract distinction:** `SKILL.md` is edited in place by precedent
(`82af3a2` rewrote section-heading text; luna-round-3 rewrote craft rules in
place), while records (`LOG.md`, `corpus/*`) are append-only. The SOP sits in
the living-contract class; amending it does not violate the repo's
append-only convention, which binds records.

## 4. YAGNI test — is the extension speculative?

No, on three independently verifiable grounds:

1. **A real past drift exists in the uncovered surface.** r4u-05's
   `.bashrc:63` misbinding (node shim instead of the wakaru ELF) changed
   provider behavior while all three client-config hashes stayed
   byte-identical — the falsification case for a 3-path zero-drift claim
   (`corpus/knowledge/2026-10-13-r4u-05-wakaru-oom.md:104-108`; `PROVINCE.md:124-125`).
2. **The repo's own drift-prone section names those files.**
   `PROVINCE.md:15` opens the "Drift-prone values" section; it cites
   `.bashrc:23-24` and `:61` (`:25-26`), `.profile:4` (`:47`), `.bashrc:63`
   (`:124-125`). I re-read all five pointer targets this session; all resolve.
3. **The extension was pre-declared in round-1's records, with the mechanism
   and the ordering constraint.** `SCORECARD.md:699-700`: "`.bashrc`/`~/.profile`
   into the custody pair from the next round's pre-pair (E15 — retro-append
   void)"; `LOG.md:1008-1010` the same. Round 2 IS that round: the 5-path
   pre-pair was captured at `16:57:35Z`, before this round's first probe
   (battery leg 2 window opens `16:59:35Z`, `.ufo/waves/arc2-loop1-round2/E14.md:19`;
   SC1's first session stamp `16:59:24Z`, `SC1.md:11`) — the SOP's own
   ordering rule is honored by the practice.

**Timing was forced, not chosen.** E15's rule ("retro-appending the shell
paths to this round's post-pair alone would create a post-only leg; under the
round's own rule draft that is void", `E15.md:236-239`) means round 1 could
not demonstrate the 5-path pair; and landing a 6/5/1 gate in round 1 with no
6/5/1 receipt in the repo would have shipped an unverified gate — exactly the
defect class round 1's depth discipline forbids. One round of latency is the
minimum consistent with round 1's own evidence rules.

**Born-stale sequencing (mtimes, this host):** `E15.md` (5-path decision)
written 13:44:22; `E12.md` (SOP text source) written 13:46:38; work commit
13:54:36. The SOP text was authored after the extension decision existed on
disk. Whether E12/the parent *read* E15 before writing is unknown (mtimes
prove write order only); that the round-1 *records* carry the debt
(`SCORECARD.md:699-700`, `LOG.md:1008-1010`) is observed.

## 5. Independent verification of E21's block (what I re-ran vs echoed)

Every load-bearing claim in E21's block, re-run by me:

| Claim | My result |
|---|---|
| gate 6/5/1 on the round-2 receipt | 6 / 5 / 1 ✓ (§2) |
| path-identity grep = 5 (`E21.md:192-193`) | 5 ✓ |
| `tail -n3` no longer selects configs | selects kimi + `.bashrc` + `.profile` ✓ (`E21.md:221-226` accurate) |
| `tail -n +2 \| head -n3` = the three configs | hashes `16f496e6/38d2a1d0/3546e033` ✓ |
| `-c` rc=0, 5× OK, empty stderr | ✓ |
| scratch application prefix/craft/suffix identical, +24 lines | ✓ (§3) |
| `.bashrc:23-24/:58-64` (7 REA\_), `.profile:3-4/:7-12` (6 REA\_) | names-only read; counts 7/6 ✓ |
| `.bash_profile` exports no REA\_/GHIDRA/JAVA | 0 ✓; `~/.kimi-code/mcp.json` no `rea-agents` ✓ |
| SKILL.md sha256 at read time `04e92d07…` | `04e92d075f3aaad4ceb0ad247edcedca82a50e678a98005087e056842e183cb9` ✓ |
| line-shift safety: no editable file cites SKILL.md ≥ 208 | true as stated, but see defect (c) below |

**Defects found (none block the block):**

- (a) **E21.md:178 prose misdescribes the replace range.** "Replace
  `SKILL.md:217-256` (the **eight** bullets; …)" — the range `:217-256` holds
  **six** bullets (I counted `^- \*\*` at :217, :229, :233, :241, :246, :253);
  the replacement block holds eight. Cosmetic ambiguity in the instruction
  sentence, not in the block. Corrected sentence in §8.
- (b) **E1.md:106's "(313 B)" for the round-2 receipt is unreproduced.** My
  `stat` measures 501 B; `V3.md:7,71` independently says 501; `E21.md:42-44`
  flags it. Two-of-two independent measurements vs one stray number.
- (c) **Pre-existing stale pointer the amendment neither creates nor fixes:**
  `corpus/lessons/2026-10-15-round-1.md:37` cites `SKILL.md:207-210`; at HEAD
  those lines are the blank + `## Config custody for live-probe rounds (SOP)`
  heading + blank + "Binding for every future…" — the intended content
  (evidence-id path-sensitivity debt) now sits in `## Known limits (r4)` at
  `SKILL.md:268`. Made stale by round-1's insert (SKILL.md 251 → 312 lines),
  not by this amendment (region ≥217 is untouched by it, and 207-210 stays
  fixed under the block). E21's sweep checked "≥ 208" and this citation
  straddles; parent's records pass may note it as one more baseline-scoped
  pointer of the same family as the PROVINCE `:152` item round 1 documented.
- (d) **Receipts not yet tracked for this round.** SOP bullet
  `SKILL.md:253-256` requires "Commit both receipts tracked"; round-2's
  `receipts/` is untracked (`git status` → `?? .ufo/waves/arc2-loop1-round2/`).
  Parent action, not a defect of the amendment.

## 6. Verdict against the two framings

- **"Churn / rewrite-adjacent"** — refuted by §3 (no historical byte
  touched; zero re-touch; living-contract class) and by §2 (the contradiction
  is executable at HEAD).
- **"Required for consistency"** — sustained by §2 (the binding SOP voids the
  round's own receipt) and §4 (the extension is demonstrated, pre-declared,
  and ordered exactly as round 1 prescribed). A binding rule that mis-voids
  its first subject round is the worst state available: strictly worse than
  either amending now or never having landed the SOP.

## 7. Conclusions, labeled

- **OBSERVATIONS** (ran/read this session): the SOP gate values at
  `SKILL.md:218,:224-225,:237,:251-252`; the round-2 receipt's 6/5/1 + 5× OK
  rc=0; round-1 receipts 4/3 with MANIFEST-matching self-hashes; the scratch
  application results (336 lines, PREFIX/CRAFT/SUFFIX-IDENTICAL, 10/10 rule
  blocks, 0 stale gate tokens); the gate/stale-token greps; E15/E12/report
  mtimes and the 13:54:36 commit time; the 16:57:35Z pre-pair vs 16:59:35Z
  first battery leg; the five PROVINCE pointer targets; `.bashrc`/`.profile`
  key counts and the two exclusions; SKILL.md sha256; E21 block extraction
  lines 181-244; the defects (a)-(d).
- **INFERENCES:** the unamended SOP classifies the round-2 receipt as
  malformed → VOID (from the SOP's own text applied to measured shape); the
  amendment is forward-binding and non-destructive; the one-round latency was
  forced by E15's retro-append-void rule plus the evidence-discipline
  constraint; E21's block is landable verbatim (scratch-proven).
- **UNKNOWNS:** whether E12/the parent read E15 before authoring the SOP text
  (write order only); whether the parent lands the block as written and
  whether it also re-words `SCORECARD.md:621`'s capability row to the
  forward 5-path form (that row accurately describes round 1 as historical —
  E21 §3 flags the same); this round's post-pair closing state (parent's
  capture); the 313-B number's provenance in E1.

## 8. Text for the parent to land VERBATIM (fenced)

Certification for the round-2 report/LOG (paste as-is), plus the two
integration strings:

```text
CR4 (critic) certified, 2026-10-18: the custody SOP amendment (3-path → 5-path)
is REQUIRED FOR CONSISTENCY, not churn. At HEAD 165057e the landed SOP
(SKILL.md:208-256, commit 58116aa) mandates a 4/3/1 shape gate ("mandatory, not
advisory", :228) and classifies non-conforming receipts as malformed →
persistent malformation → VOID (:251-252); this round's frozen receipt
(.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt, 2026-10-18T16:57:35Z,
501 B, self-hash 4097ec77…) measures 6/5/1 with 5× OK rc=0. Unamended, the
round's C3 zero-drift claim is void by the rule round 1 landed. The amendment
edits only SKILL.md:217-256 (living forward contract); scratch application of
E21.md:181-244 at HEAD leaves lines 1-216, the craft section 81-206, and 257+
byte-identical (applied file 336 lines, +24), 10/10 rule blocks preserved, zero
stale gate tokens. Round-1 receipts stay byte-identical (4/3, self-hashes
7369fbcb…/dec9c8c8…) and remain the compliant 3-path demonstration. The
extension was pre-declared at SCORECARD.md:699-700 and LOG.md:1008-1010
("from the next round's pre-pair (E15 — retro-append void)"); this round's
pre-pair precedes its first probe (16:57:35Z < 16:59:35Z). E21's block is
landable verbatim; see CR4.md §5 for two non-blocking prose/pointer defects.

Correction if E21's instruction sentence is copied: read it as "Replace the six
bullets at SKILL.md:217-256 (keep lines 208-216 and 257+ unchanged) with the
eight bullets below" — not "the eight bullets" describing the replaced range.

Landing checklist (parent): (1) apply the block to SKILL.md:217-256; (2)
verify the amended gate against the actual receipt (6/5/1 + path-identity 5 +
5× OK rc=0); (3) commit this round's receipts tracked per SOP :253-256; (4)
decide the SCORECARD.md:621 capability-row wording (historical 3-path vs
forward 5-path); (5) mark the round-1 debt at SCORECARD.md:699-700 /
LOG.md:1008-1010 discharged by this round's pre-pair; (6) optional: note
corpus/lessons/2026-10-15-round-1.md:37's SKILL.md:207-210 citation as
baseline-scoped-and-stale-at-HEAD (pre-existing, not amendment-caused).
```

## 9. Reproduction commands

```bash
git rev-parse HEAD; git status --porcelain
R=.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt
wc -l < "$R"; grep -cE '^[0-9a-f]{64}  /' "$R"
grep -cE '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$' "$R"
tail -n +2 "$R" | sha256sum -c -
tail -n3 "$R"; tail -n +2 "$R" | head -n3
grep -cE '^[0-9a-f]{64}  /home/vgpnk/\.(config/devin/mcp_config\.json|omp/agent/mcp\.json|kimi-code/config\.toml|bashrc|profile)$' "$R"
sed -n '208,256p' SKILL.md
S=/tmp/arc2-l2r2-CR4-apply; mkdir -p "$S"
head -n 216 SKILL.md > "$S/SKILL.applied.md"
sed -n '181,244p' .ufo/waves/arc2-loop1-round2/E21.md >> "$S/SKILL.applied.md"
tail -n +257 SKILL.md >> "$S/SKILL.applied.md"
wc -l SKILL.md "$S/SKILL.applied.md"
diff <(head -n 216 SKILL.md) <(head -n 216 "$S/SKILL.applied.md") && echo PREFIX-IDENTICAL
diff <(sed -n '81,206p' SKILL.md) <(sed -n '81,206p' "$S/SKILL.applied.md") && echo CRAFT-IDENTICAL
sha256sum .ufo/waves/arc2-loop1-round1/receipts/config-pre-pair.txt \
          .ufo/waves/arc2-loop1-round1/receipts/config-post-pair.txt
cat .ufo/waves/arc2-loop1-round1/receipts/MANIFEST.txt
awk 'NR>=217 && NR<=256 && /^- \*\*/{n++} END{print n}' SKILL.md   # 6
git grep -nE 'three drift-sensitive|4/3/1|exactly three' -- . ':(exclude).ufo'
grep -n 'SKILL.md:207-210' corpus/lessons/2026-10-15-round-1.md; sed -n '207,210p;268p' SKILL.md
sed -n '699,700p' SCORECARD.md; sed -n '1008,1010p' LOG.md
```

## 10. Scope compliance

Read-only on every repo and home file except this report; no git mutations,
no config edits, no installs, no network (no `npx` ran from this seat), no
other seat's files touched. Scratch: `/tmp/arc2-l2r2-CR4-apply/` only. No
secret values read or emitted — hashes, pins, and export names only. No
REA/MCP session was opened by this seat, so nothing was left to close.
