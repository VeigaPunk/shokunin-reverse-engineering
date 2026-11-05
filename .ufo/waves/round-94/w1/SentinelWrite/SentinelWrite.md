# SentinelWrite — security review: round-94 receipt writer + committed receipt bytes

Seat: SentinelWrite (sentinel), wave r94-w1, lane kaidoku round 94.
Frozen revision reviewed: `dd4524916a0332bb65f83525532da1c1b8d709de` (shared clone at
`/fast/scratch/hyaku/kaidoku-r94/SentinelWrite/clone`, checkout verified `rev-parse HEAD`).
Read-only on the lane; the only lane writes are this report (both prompt-named paths).

## Method (exact commands, exit codes)

1. Pins, on clone bytes:
   `sha256sum tools/round-94/stop-boundary-repair-battery-v4.py tools/round-94/c1-receipt-agreement.py tools/round-93/stop-boundary-repair-battery-v3.py tools/round-92/stop-boundary-repair-battery.py tools/round-92/stop-boundary-battery-v2.py tools/round-92/upx-stop-boundary-search-repair.py`
   → rc 0. v4 `c41d54d72257…6272`, agreement `dc384a4464c2…36c9`, v3 `60026511e54c…d4e3`,
   r92 battery `63e9df431f5d…38bc`, r92 v2 `f6ddb48b4d9c…1874` — all five match the frozen
   pins in claims.json. Repair tool `ce1b1769…` (kill rule requires ≠ `cf2f6e7c…`: satisfied).
   `sha256sum /usr/bin/upx` → `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`
   = v2 `UPX_SHA256` exactly (no packer drift; battery proceeded, see 3).
2. Symlink/path fixture (calls `write_receipt` directly via importlib, not through the battery):
   `python3 -I -B $S/fixture_symlink.py` → rc 0. Driver + output in
   `evidence/fixture_symlink.py`, `evidence/fixture-out.txt`.
3. Full pos run under syscall audit (strace IS installed at /usr/bin/strace):
   `TMPDIR="$S/tmp" strace -f -qq -e trace=%file -o "$S/strace-pos.log" python3 -I -B tools/round-94/stop-boundary-repair-battery-v4.py --root "$S/clone" --repair-cmd tools/round-92/upx-stop-boundary-search-repair.py --work "$S/work" --rev dd4524916a0332bb65f83525532da1c1b8d709de --expect 'repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2' --json-out "$S/work/c1-v4-pos.json"`
   → rc 0, stdout `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2 met True exit 0` (`evidence/pos-run.txt`). 13.7 s wall.
4. Committed-receipt parse pass (read-only) over `.ufo/waves/round-94/pre/` and
   `.ufo/waves/round-94/l1/scores/`: python `json.load` per file — see F8.
5. Greps (case-insensitive) over both receipt dirs — see F5/F6/F7.

## Findings

### F1 — MED — `open(<json-out>.tmp, "w")` follows a pre-planted symlink
- Where: `tools/round-94/stop-boundary-repair-battery-v4.py:56-66` (`write_receipt`):
  `tmp = path + ".tmp"`; `open(tmp, "w", …)`; `os.replace(tmp, path)`; on any exception
  `os.remove(tmp)` then re-raise.
- Exploit path: any process with write access to the directory of `--json-out` (the wave dir
  is shared among same-user seats) pre-creates `<json-out>.tmp` as a symlink to a victim
  file. The write follows the link: the victim is overwritten with the receipt JSON; then
  `os.replace` renames the *symlink itself* onto `<json-out>`, so `<json-out>` remains a
  symlink to the victim. A downstream reader (`c1-receipt-agreement.py`, any auditor) then
  reads the victim's bytes while believing it read the receipt — the "complete JSON or
  absent" atomicity guarantee is silently defeated, and an arbitrary same-user file is
  clobbered.
- Evidence (fixture case A): victim file content replaced by the receipt JSON; post-state
  `outA.json = symlink -> victim`, `.tmp` gone. Reproduce: `evidence/fixture-out.txt`.
- Impact: same-user file clobber + receipt/reader desync; NOT reachable in the frozen flow
  (fresh per-seat wave paths, single writer), hence MED, not HIGH.
- Smallest remediation: create the tmp fd with
  `os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600)` (ELOOP on a
  symlink → failure path → receipt absent, which the contract already defines), or
  `tempfile.mkstemp(dir=os.path.dirname(path) or ".")` + `os.replace`. No pin impact: this
  is a candidate-improvement note for the L1, v4 bytes stay frozen for this round.

### F2 — NONE (correct) — destination symlink is replaced, not followed
Fixture case B: pre-existing symlink at `<json-out>` → victim untouched; `os.replace` swaps
the link itself for the regular receipt file. `rename(2)` never follows the dst link. No action.

### F3 — LOW — no path confinement on `--json-out`
Traversal (`../escape.json`, fixture case C) and plain relative (case D) and absolute paths
are used verbatim: the writer will create/overwrite any same-user-writable path. Only
operator-supplied values reach this argument in the frozen commands (no untrusted flow —
the receipts embed no path that is later fed back as `--json-out`), so this is LOW. The
missing-directory case (E) raises `FileNotFoundError` and leaves neither `<json-out>` nor
`.tmp` — the failure contract holds. Remediation optional: none required for the frozen
flow; treat `--json-out` as trusted operator input.

### F4 — NONE (correct) — write confinement of the whole battery run
strace `-f %file` over the complete pos run (parent + every child incl. upx/repair
subprocesses): 968 distinct paths under `--work` (inv-*/rt-* boxes, `fresh-src.bin`, the
receipt, `work/tmp`, `work/home`); **0 write-mode syscalls outside `--work`**; 0 paths under
the parent `TMPDIR` (every `tempfile.mkdtemp` call passes `dir=work`, and children get
`TMPDIR=<work>/tmp` from `v2.env_for`, tools/round-92/stop-boundary-battery-v2.py:75-79);
clone access strictly read (19 paths, no write flags); no `~/.cache`, `/tmp`, or lane
writes. No `.tmp` leftovers in `--work` after the run. Log retained in scratch during the
seat (3.3 MB, audit summarized here); scratch is deleted at cleanup per seat rules.

### F5 — NONE — secrets: zero hits
Patterns `ghp_`, `sk-`, `op://`, `Bearer `, `api_key`, `token=`, `password`
(case-insensitive) over `.ufo/waves/round-94/pre/` (22 files) and
`.ufo/waves/round-94/l1/scores/` (17 files): **0 hits**, and 0 hits in my freshly produced
receipt. Receipts carry only sha256 hexes, counters, labels, child stdout/tails, box
basenames, and hardcoded provenance paths (`/usr/bin/env`, carriers, `/usr/bin/upx`).

### F6 — NONE — no environment-variable value reaches any receipt
Only two `os.environ` uses in the receipt-producing toolchain:
- `tools/round-92/stop-boundary-battery-v2.py:78` — `os.environ.get("PATH")` → child env
  dict; the dict is never serialized (receipt keys audited: tool/class/repair/…/counts/
  label/expect/met_target/exit, fresh/public cells — no env dict).
- `tools/round-94/stop-boundary-repair-battery-v4.py:119` — `os.environ.get("HYAKU_SCRATCH")`
  → default selftest dir only; not serialized.
Grep for `"PATH"|"HOME"|"TMPDIR"|"LANG"|"HYAKU_SCRATCH"` over the round-94 wave tree: hits
only in claims.json (manifest path, fresh oracle path — literal constants) and harness
bookkeeping (dispatch/spec/validate); none in any receipt. Child stdout is embedded
(JSON-escaped), so a malicious repair could echo env values into its own stdout — but the
frozen repair tools are lane-pinned files and none print env values; risk noted, not present.

### F7 — LOW (observation) — committed stderr keeps lane paths, receipts keep none
`pre/c1-base-v3-pos.stderr` and `pre/c1-base-v3-F3.stderr` are the v3 crash tracebacks and
contain the lane repo path (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/…`, lines
2 and 5) — lane-internal path, not a secret; kept deliberately as M93-e evidence. No
receipt JSON contains any `/fast/`, `/home/`, or `/tmp/` path (grep: hits only in harness
bookkeeping JSONs that embed seat text by design).

### F8 — receipt bytes state (evidence, matches the frozen declaration)
- `pre/c1-base-v3-F3.json` and `pre/c1-base-v3-pos.json` are truncated, unparseable JSON
  (`JSONDecodeError` at char 703 / 706, both line 33 col 14) — exactly the declared
  M93-e/D-93-D do-nothing-control evidence, intentionally kept unrewritten.
- All five `l1/scores/` v4 receipts (`pos`, `F1`, `F2`, `F3`, `agreement`) parse as valid
  JSON — the v4 atomic writer delivers "complete JSON or absent" in the committed bytes.

### F9 — LOW (observation, prose/twin divergence in the frozen claims, no action)
`plans/round-94-claims.md` kill-rule phrase "the wrong `upx` sha (`cf2f6e7c6846a7c9…`)"
reads as if `cf2f6e7c…` were a wrong value, while the machine twin `claims.json` ("upx sha
prefix differing") and v2's `UPX_SHA256` constant both pin `cf2f6e7c…` as the REQUIRED
value; the host upx matches it and the battery correctly proceeded. The twin is
unambiguous; noting the prose ambiguity only. Frozen docs: not edited.

## Attestations
- Lane untouched except this report file and its seat-dir twin + `evidence/` — the two
  paths named by the seat spec. No tool installed or upgraded; no host state changed; no
  pacman transactions; no git mutations anywhere (clone via `git clone --shared` +
  `checkout` into scratch only; fixture used no git at all).
- Peer cross-check: ReviewerV4 independently verified the same five pins + upx + env pins
  at the same revision (IRC, all match) — corroborates F8's pin statement.
- Scratch `/fast/scratch/hyaku/kaidoku-r94/SentinelWrite` deleted before yield.
