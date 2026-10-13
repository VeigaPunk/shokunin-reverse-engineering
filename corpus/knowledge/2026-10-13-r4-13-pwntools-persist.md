<!-- corpus entry — kaidoku-shokunin round 4 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r4/13-pwntools-persist.md. -->

# 13 — Persistent pwntools provisioning + first-ever `inspect-binary-layout` run (round-4)

Axes: persistence (venv survives rounds, not /tmp), coverage (first-ever
`inspect-binary-layout` emission after r1/r2/r3 all gated on
`provider_unavailable`), reproducibility (r2 crash path re-verified against
the persistent env), operator-documentation (exact persistence key).

Provisioning target per r2 recipe (`.ufo/waves/kaidoku-r2/06-crash-probe.md`),
moved from ephemeral `/tmp/kaidoku-pwnenv` to persistent
`~/.local/share/kaidoku-pwnenv`. Version contract re-verified live: the
refusal text still demands pwntools 4.15.0 + pyelftools 0.33 + Unicorn 2.1.2.
Note: `rea doctor` does NOT surface this requirement — its
`providerInspections` lists only `ghidra` (available) and `ida`
(unavailable); `pwntools-elf` is an aux provider invisible to doctor (r3's
"doctor blind to aux providers" observation reconfirmed this round).

## Candidate: persistent venv at `~/.local/share/kaidoku-pwnenv` — provisioned, pins exact

- claim: `uv venv ~/.local/share/kaidoku-pwnenv --python 3.11` built a venv on
  the managed cpython-3.11.17 already in the uv cache (same interpreter r2
  used at /tmp); `uv pip install --python …/bin/python pwntools==4.15.0
  pyelftools==0.33 unicorn==2.1.2` resolved cleanly. `importlib.metadata`
  reports pwntools 4.15.0, pyelftools 0.33, unicorn 2.1.2 on Python 3.11.17;
  `bin/python` symlinks to
  `/home/vgpnk/.local/share/uv/python/cpython-3.11.17-linux-x86_64-gnu/bin/python3.11`.
  Footprint 174M. This survives reboots and future rounds — unlike r2's
  `/tmp/kaidoku-pwnenv`, which r3 confirmed was gone.
- source: `uv venv` output ("Using CPython 3.11.17", "Creating virtual
  environment at: .local/share/kaidoku-pwnenv"); `uv pip install` resolution
  tail (`+ unicorn==2.1.2` etc.); `importlib.metadata` version print;
  `readlink -f` on the venv python; `du -sh` → 174M.
- verify: `uv venv ~/.local/share/kaidoku-pwnenv --python 3.11 && uv pip
  install --python ~/.local/share/kaidoku-pwnenv/bin/python pwntools==4.15.0
  pyelftools==0.33 unicorn==2.1.2 && ~/.local/share/kaidoku-pwnenv/bin/python
  -c "import importlib.metadata as m; [print(p, m.version(p)) for p in
  ('pwntools','pyelftools','unicorn')]"`.
- verified-at: 2026-10-13 round-4 lane (shells f0f633, d46084, b14330 —
  all exit 0).
- suggested: admit — the only delta from the r2 recipe is the persistent
  path; version pins are unchanged and still match REA's refusal text
  verbatim.

## Candidate: `inspect-binary-layout /usr/bin/jq` — FIRST-EVER successful run (r1/r2/r3 all gated)

- claim: with `REA_PWNTOOLS_PYTHON` pointing at the persistent venv the verb
  emits a full Evidence envelope: exit 0, 79,955 B JSON,
  `provider.id: "pwntools-elf"`, `provider.version:
  "pwntools@4.15.0;pyelftools@0.33;unicorn@2.1.2"`, `confidence: "observed"`,
  `authority: "shipped-artifact"`, evidence
  `ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd`.
  `normalized_result` carries 16 keys: artifact (path + sha256
  `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`, 30,800
  B), format `elf`, architecture `EM_X86_64`/64-bit/LE, image_type `ET_DYN`,
  entry_point `0x3cf0` (linked-virtual-address, execution_status unknown),
  runtime_load_base `null`, 28 sections, 15 segments, 80 symbols, 79
  relocations + 1 packed RELR entry, relocation_inventory_completeness
  `unknown`, linkage (needed_libraries `libjq.so.1`, `libonig.so.5`,
  `libc.so.6` — each with raw bytes + file offsets; plus interpreters, GOT,
  PLT, convenience_maps_completeness, runtime_library_paths), mitigations
  (evidence_kind `inferred`: PIE true, NX true, no executable stack, stack
  canary true, RELRO `Full`), diagnostics (empty stdout/stderr, not
  truncated), and 12 limitations (PT_NULL payloads carry no file-byte claims;
  SHN_XINDEX unresolved; linked vs runtime addresses kept distinct;
  relocation inventory completeness unknown; etc.).
- source: live run `/tmp/kaidoku-r4-jq-layout.json` (parsed then deleted);
  envelope keys and `normalized_result` dissection above.
- verify: `REA_PWNTOOLS_PYTHON=$HOME/.local/share/kaidoku-pwnenv/bin/python
  npx -y rea-agents@6.4.0 inspect-binary-layout /usr/bin/jq --format json`
  → exit 0; bare run (no env) → exit 1 `provider_unavailable` /
  `candidate_ids:["pwntools-elf"]`, identical refusal text to r1–r3.
- verified-at: 2026-10-13 round-4 lane (shell d05f3f exit 0 79,955 B;
  bare-run shell 95f90e exit 1).
- suggested: admit — the last gated analysis verb on this host is now
  exercised end-to-end. The layout output is strictly observed/mechanical
  (no disassembly — sections/segments/symbols/relocations/linkage/
  mitigations only), complementing rather than overlapping the ghidra-backed
  verbs. Frontier next: a non-DYN object (kernel module `.ko`, relocatable
  `.o`) to exercise the `ET_REL` branch of the limitations list.

## Candidate: `inspect-recorded-crash` re-verified against the persistent env — works, byte-identical core paths

- claim: `coredumpctl dump 1150573 -o /tmp/kaidoku-r4-core` emits an
  already-decompressed ELF core (724,992 B, magic `7f 45 4c 46`, `file`:
  "ELF 64-bit LSB core file, x86-64, from '/bin/bash …/crash-godot…'") —
  **manual `zstd -d` is NOT needed on the dump path** because coredumpctl
  decompresses the stored `.zst` (65.4K on disk) itself. The manual path was
  still verified: `zstd -dc` on
  `/var/lib/systemd/coredump/core.crash-godot.1000.73a8e2fc…1150573….zst`
  (root-owned but group/ACL-readable) produces a byte-identical 724,992 B
  file (`cmp` clean). `inspect-recorded-crash` on the dumped core with the
  persistent env: exit 0, 25,690 B JSON (r2 measured 25,700 B — the 10-byte
  delta is the fresh evidence_id/parameter echo), same shape: 1 thread × 27
  named registers with file locations (r15 `0x55ba48dff690` at note offset
  `0x984` …), 40 segments, 8 notes, signals `[{note_index:2, number:11
  (SIGSEGV), code:0, errno:0, fault_address null/unknown}]`,
  target_execution `not-performed`, live_process_identity `unknown`.
- source: live run `/tmp/kaidoku-r4-crash.json` (parsed then deleted);
  `od -N 8` magic check; `file` identification; `cmp` of dump vs zstd-dc
  outputs; `coredumpctl` metadata (Storage path, Size on Disk 65.4K).
- verify: `coredumpctl dump 1150573 -o /tmp/c && od -A x -t x1z -N 8 /tmp/c`
  → ELF magic; `REA_PWNTOOLS_PYTHON=$HOME/.local/share/kaidoku-pwnenv/bin/
  python npx -y rea-agents@6.4.0 inspect-recorded-crash /tmp/c --format
  json` → exit 0; cross-check `zstd -dc /var/lib/systemd/coredump/
  core.crash-godot.1000.…1150573….zst | cmp - /tmp/c` → identical.
- verified-at: 2026-10-13 round-4 lane (shells af40e1 dump, 739f98 inspect
  exit 0, 34a91f… zstd-dc+cmp identical).
- suggested: admit — the r2 mechanism is unchanged; the persistent venv
  makes it a stable capability instead of a per-round bootstrap. Update the
  standing note: "`coredumpctl dump` already decompresses; `zstd -d` is
  only needed if reading the journal's `.zst` storage file directly."

## Candidate: `REA_PWNTOOLS_PYTHON` must be set at invocation — confirmed; persistence documented (no shell files edited)

- claim: the variable is read per-invocation from the process environment —
  it is NOT persisted by REA itself (no config file, no doctor-settable
  state). Inline `REA_PWNTOOLS_PYTHON=<abs> npx …` works; a bare run in the
  same shell fails `provider_unavailable`; a **relative** path
  (`REA_PWNTOOLS_PYTHON=kaidoku-pwnenv/bin/python` from `~/.local/share`) is
  refused with the same `provider_unavailable` — the "absolute
  caller-supplied Python executable" requirement is enforced, not just
  documented. Operator persistence recipe (documented only, per task — no
  shell files modified): add to `~/.bashrc` (interactive shells; exists,
  2,399 B, currently has no REA vars) AND `~/.profile` (login/session
  environment; exists, 256 B) the line:
  `export REA_PWNTOOLS_PYTHON="$HOME/.local/share/kaidoku-pwnenv/bin/python"`
  (expands to an absolute path; a literal unexpanded `~` or a relative path
  would be refused). No `~/.zshrc` exists on this host (bash shell).
  Alternative for non-interactive/systemd use: a drop-in or wrapper script
  exporting the same absolute path.
- source: bare run exit 1 (`provider_unavailable`, same JSON as r1–r3);
  inline-env run exit 0; relative-path run refused; `ls -la ~/.bashrc
  ~/.profile ~/.zshrc` (no .zshrc); grep of both files — `REA_PWNTOOLS`
  absent.
- verify: `npx -y rea-agents@6.4.0 inspect-binary-layout /usr/bin/jq
  --format json` (no env) → exit 1; `(cd ~/.local/share &&
  REA_PWNTOOLS_PYTHON=kaidoku-pwnenv/bin/python npx -y rea-agents@6.4.0
  inspect-binary-layout /usr/bin/jq --format json)` → exit 1
  `provider_unavailable`.
- verified-at: 2026-10-13 round-4 lane (shells 95f90e, 38f3f5).
- suggested: admit — persistence is an operator concern REA deliberately
  does not own ("REA never installs Python or packages" extends to never
  persisting its config). The one-line export is the entire contract.

## Run log

| # | command | result |
|---|---------|--------|
| 1 | `uv venv ~/.local/share/kaidoku-pwnenv --python 3.11` | created on managed CPython 3.11.17 |
| 2 | `uv pip install --python ~/.local/share/kaidoku-pwnenv/bin/python pwntools==4.15.0 pyelftools==0.33 unicorn==2.1.2` | resolved; all transitive deps installed |
| 3 | `importlib.metadata` version check | pwntools 4.15.0 / pyelftools 0.33 / unicorn 2.1.2, Python 3.11.17 |
| 4 | `npx -y rea-agents@6.4.0 doctor --json` | `providerInspections` = ghidra (avail) + ida (unavail) only; zero pwntools-elf checks — doctor still blind to aux providers |
| 5 | bare `inspect-binary-layout /usr/bin/jq --format json` | exit 1 `provider_unavailable`, `candidate_ids:["pwntools-elf"]` (r1–r3 refusal verbatim) |
| 6 | `REA_PWNTOOLS_PYTHON=<venv> inspect-binary-layout /usr/bin/jq --format json` | **exit 0, 79,955 B — FIRST-EVER RUN** (ev_294a449c…) |
| 7 | `coredumpctl dump 1150573 -o /tmp/kaidoku-r4-core` | 724,992 B decompressed ELF core (source .zst 65.4K) |
| 8 | `REA_PWNTOOLS_PYTHON=<venv> inspect-recorded-crash /tmp/kaidoku-r4-core --format json` | exit 0, 25,690 B; 1 thread × 27 regs, 40 segments, 8 notes, SIGSEGV note_index 2 |
| 9 | `zstd -dc` stored `.zst` → `cmp` vs dump | byte-identical 724,992 B — manual `zstd -d` only needed when bypassing coredumpctl |
| 10 | relative `REA_PWNTOOLS_PYTHON=kaidoku-pwnenv/bin/python` | refused `provider_unavailable` — absolute path enforced |
| 11 | `ls ~/.bashrc ~/.profile ~/.zshrc`; grep REA_PWNTOOLS | .bashrc + .profile exist, no .zshrc, var unset in both — documented, not edited |
| 12 | `rm -f /tmp/kaidoku-r4-*` | all scratch files removed; venv (174M) is the only persistent artifact |

## Summary

Round-4 closed the last provider gap on this host. The r2 ephemeral recipe
was promoted to a persistent venv at `~/.local/share/kaidoku-pwnenv`
(CPython 3.11.17, pins pwntools 4.15.0 / pyelftools 0.33 / unicorn 2.1.2
verified exact, 174M). With `REA_PWNTOOLS_PYTHON` pointed at it,
`inspect-binary-layout` ran successfully **for the first time** (r1–r3 all
gated `provider_unavailable`): a complete observed-evidence ELF layout of
`/usr/bin/jq` — 28 sections, 15 segments, 80 symbols, 79+1 RELR
relocations, DT_NEEDED linkage, inferred mitigations (PIE/NX/canary/Full
RELRO). `inspect-recorded-crash` was re-verified end-to-end on a fresh
724,992 B bash core (exit 0, 25,690 B, same schema as r2). Contract
findings: the env var is read per-invocation, must be **absolute**
(relative refused), and REA persists nothing — operator persistence is one
`export` line in `~/.bashrc`/`~/.profile` (documented above, files not
touched). `rea doctor` remains blind to the pwntools-elf aux provider; the
verb's typed refusal is the only place the requirement surfaces.
