<!-- corpus entry — kaidoku-shokunin round 1 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r1/09-elf-observe.md. Each candidate's `suggested:` field is its curation verdict; `reject` rows are retained calibration entries. -->

# Worked example — observation vs inference on a shipped artifact

Target: `/usr/bin/jq` (read-only; executed only `--version`, never modified).
Host evidence collected 2026-10-13. File: 30,800 bytes, mode 0755 root:root,
sha256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`.

Discipline demonstrated: every candidate states a *claim*, then separates
**OBSERVATION** (bytes the tool emitted, reproducible verbatim) from
**INFERENCE** (interpretation layered on top, which needs its own evidence).
Candidates whose claim smuggles inference in as fact are marked `reject`.

---

## Candidate: ELF64 little-endian PIE executable for x86-64, System V ABI

- claim: /usr/bin/jq is a 64-bit, little-endian, position-independent ELF
  executable for AMD x86-64 targeting the UNIX System V ABI.
- source: `file /usr/bin/jq`; `readelf -h /usr/bin/jq`
- verify: `file /usr/bin/jq && readelf -h /usr/bin/jq | grep -E 'Class|Data|Type|Machine|ABI'`
- verified-at: 2026-10-13
- suggested: admit — pure observation, two independent tools agree.

**OBSERVATION (raw):**
- `file`: `ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically
  linked, interpreter /lib64/ld-linux-x86-64.so.2, ... for GNU/Linux 4.4.0, stripped`
- `readelf -h`: `Class: ELF64`, `Data: 2's complement, little endian`,
  `OS/ABI: UNIX - System V`, `Type: DYN (Position-Independent Executable file)`,
  `Machine: Advanced Micro Devices X86-64`, entry point `0x3cf0`.

**INFERENCE (labeled, not admitted as observation):**
- `Type: DYN` + `file` saying "pie executable" ⇒ the distro built jq with PIE
  enabled, so the loader can randomize the image base (ASLR). This is an
  inference about *link-time intent*; the bytes only prove the type field.
- `for GNU/Linux 4.4.0` (from `.note.ABI-tag`, `OS: Linux, ABI: 4.4.0`) is the
  *minimum kernel ABI stamped at build time*, not the kernel it runs on.

---

## Candidate: dynamically linked; runtime deps are libjq.so.1, libonig.so.5, libc.so.6

- claim: the binary declares exactly three DT_NEEDED entries — `libjq.so.1`,
  `libonig.so.5`, `libc.so.6` — and interpreter `/lib64/ld-linux-x86-64.so.2`.
- source: `readelf -d /usr/bin/jq`; section `[ 2] .interp` in `readelf -S`
- verify: `readelf -d /usr/bin/jq | grep NEEDED && readelf -x .interp /usr/bin/jq`
- verified-at: 2026-10-13
- suggested: admit — pure observation from the DYNAMIC section.

**OBSERVATION (raw):**
- `NEEDED Shared library: [libjq.so.1]`
- `NEEDED Shared library: [libonig.so.5]`
- `NEEDED Shared library: [libc.so.6]`
- `.interp` PROGBITS at file offset 0x3ac, size 0x1c (= 28 bytes, the
  NUL-terminated path `/lib64/ld-linux-x86-64.so.2`).

**INFERENCE (labeled):**
- `/usr/bin/jq` is only 30,800 bytes yet links `libjq.so.1` ⇒ the jq engine
  almost certainly lives in the shared library and this file is a thin CLI
  driver. *Not proven by these bytes alone* — confirm by checking which
  undefined `.dynsym` symbols resolve to libjq (`nm -D /usr/bin/jq`) and by
  sizing `libjq.so.1` itself.
- `libonig.so.5` ⇒ regex support via Oniguruma. The bytes prove only the
  dependency edge, not that regex code paths are reachable.
- `DT_NEEDED` lists *declared* deps; transitives pulled by libjq are not shown
  here (would need `ldd`).

---

## Candidate: stripped of symbols, but with a split-debug breadcrumb

- claim: the binary has no `.symtab` (stripped per `file`), and carries a
  `.gnu_debuglink` section naming `jq.debug`.
- source: `file /usr/bin/jq` ("stripped"); `readelf -S /usr/bin/jq` (28
  sections, no `.symtab`); `readelf --string-dump=.gnu_debuglink /usr/bin/jq`
- verify: `readelf -S /usr/bin/jq | grep -c symtab; readelf --string-dump=.gnu_debuglink /usr/bin/jq`
- verified-at: 2026-10-13
- suggested: admit — observation; the `grep -c symtab` check must print `1`
  (`.dynstr`/`.dynsym` match the substring? verify precisely:
  `readelf -S /usr/bin/jq | grep -w symtab` should print nothing).

**OBSERVATION (raw):**
- `file` reports `stripped`.
- Section headers (28 total) contain `.dynsym`/`.dynstr` but **no `.symtab` /
  `.strtab`**.
- `.gnu_debuglink` string dump: `[0] jq.debug` plus a 4-byte CRC (`v` row is
  the checksum field).
- `.comment` string dump: `GCC: (GNU) 16.1.1 20260430`.

**INFERENCE (labeled):**
- `jq.debug` ⇒ the packaging system ships separated debuginfo resolvable via
  build-id `cc56d2fd644ddd549b5339882e77f22f781525d3` (observed in
  `.note.gnu.build-id`). *Inference*: that debug file existing on this host is
  unproven — check `/usr/lib/debug/.build-id/cc/56d2fd...debug`.
- `.comment` proves the final link used GCC 16.1.1, but *not* that every
  object came from that compiler (the section records one stamp).

---

## Candidate: version reported at runtime is jq-1.8.2, and it is NOT a stored literal

- claim: `jq --version` prints `jq-1.8.2`, while `strings -a /usr/bin/jq`
  contains no `jq-1.8.2` literal — only the format template
  `jq - commandline JSON processor [version %s]`.
- source: `strings -a /usr/bin/jq | grep -iE 'jq-[0-9]|version' | head`;
  `/usr/bin/jq --version`
- verify: `strings -a /usr/bin/jq | grep -c 'jq-1\.8\.2'` (expect 0);
  `/usr/bin/jq --version`
- verified-at: 2026-10-13
- suggested: admit — the claim is deliberately two-sided: one runtime
  observation plus one negative static observation.

**OBSERVATION (raw):**
- `strings -a` grep yields: `jq - commandline JSON processor [version %s]`,
  `-V, --version             show the version;`, `version`, `VERSION_DIR`,
  `.gnu.version`, `.gnu.version_r`. No `jq-<digits>` literal appears.
- Executing `/usr/bin/jq --version` emits `jq-1.8.2`.

**INFERENCE (labeled):**
- The `%s` is filled at runtime; since the binary NEEDs `libjq.so.1`, the
  version string plausibly lives in the *library* (or a compiled-in macro),
  not in this file. *Unproven here* — verify with
  `strings -a /lib*/libjq.so.1 | grep 'jq-'`.
- Discipline point: "version 1.8.2" is **runtime behavior evidence**, a
  different evidence class than static bytes; the corpus must not file it as
  a strings(1) observation.

---

## Candidate: hardening features observable at rest (BIND_NOW, RELR, CET notes)

- claim: the DYNAMIC section sets `FLAGS BIND_NOW` and `FLAGS_1 NOW PIE`,
  contains a `.relr.dyn` section (RELR, 24 bytes / 3 entries implied), and
  `.note.gnu.property` records `x86 feature: IBT, SHSTK` with ISA
  `x86-64-baseline`.
- source: `readelf -d /usr/bin/jq`; `readelf -S /usr/bin/jq` (`[9] .relr.dyn
  RELR`); `readelf -n /usr/bin/jq`
- verify: `readelf -d /usr/bin/jq | grep -E 'FLAGS|RELR'`; `readelf -n /usr/bin/jq | grep -E 'IBT|SHSTK|baseline'`
- verified-at: 2026-10-13
- suggested: admit — pure observation of flags/notes/sections.

**OBSERVATION (raw):**
- `(FLAGS) BIND_NOW`; `(FLAGS_1) Flags: NOW PIE`; `(RELR) 0x1890`,
  `(RELRSZ) 24 (bytes)`, `(RELRENT) 8 (bytes)`.
- `.note.gnu.property`: `x86 feature: IBT, SHSTK`; `x86 ISA needed:
  x86-64-baseline`; `x86 feature used: x86, XMM`.
- Section `[9] .relr.dyn` type `RELR` at offset 0x1890, size 0x18.

**INFERENCE (labeled):**
- `BIND_NOW` + PIE *suggests* full RELRO, but RELRO also requires a
  `PT_GNU_RELRO` program header — **not observed** (we did not run
  `readelf -l`). Mark "full RELRO" unverified until
  `readelf -lW /usr/bin/jq | grep GNU_RELRO` is run.
- IBT/SHSTK notes mark the binary *CET-capable*; whether the CPU/kernel
  enforce shadow stack is runtime state, not a static fact.

---

## Candidate: "entry point 0x3cf0 is `main`" — REJECTED as stated

- claim: the ELF entry point 0x3cf0 is jq's `main` function.
- source: `readelf -h /usr/bin/jq` (`Entry point address: 0x3cf0`)
- verify: `readelf -h /usr/bin/jq | grep Entry`; then try to bind a name:
  `nm -D /usr/bin/jq | grep -w main` (dynamic table) — expected empty.
- verified-at: 2026-10-13
- suggested: reject — claim overreaches the observation. The bytes prove only
  that the *entry* (ELF `e_entry`) is 0x3cf0. In a stripped glibc binary that
  address is conventionally `_start`, which calls `__libc_start_main` with a
  `main` pointer; nothing in `readelf -h` names the symbol. Recovering `main`
  needs disassembly of the entry thunk or the split `jq.debug` info — an
  inference chain, not an observation.

**OBSERVATION (raw):** `Entry point address: 0x3cf0`; `Type: DYN`; no
`.symtab`.

**INFERENCE shown for contrast:** naming 0x3cf0 `main` skips two hops
(entry→`_start`→`main`) and relies on a stripped symbol that does not exist in
this file. This is the canonical failure mode the lane rejects: laundering an
interpretation through a tool's field name.

---

## Summary

Eight commands, six candidates: five admissions rest on verbatim tool output (ELF64 PIE x86-64; three NEEDED deps + interp; stripped-with-`jq.debug` debuglink; runtime `jq-1.8.2` absent from static strings; BIND_NOW/RELR/CET notes), one rejection demonstrates inference passed off as observation (entry point ≠ `main`), and every inference is quarantined with its own verification command.
