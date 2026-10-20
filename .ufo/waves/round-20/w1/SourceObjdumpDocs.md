# SourceObjdumpDocs — objdump `-i` / `--info` (round 20, w1)

Seat: `KaidokuR20.SourceObjdumpDocs-2` (author-side advisory, read-only; no lane file changed; no subagent dispatched).
Scope: what `list-objdump-architectures` reflects, read from the GNU objdump manual.

## Source opened

- URL: https://sourceware.org/binutils/docs/binutils/objdump.html (HTTP 200; `Last-Modified: Sun, 26 Jul 2026 17:43:39 GMT`; `content-length: 68879`).
- Access (clock, `date -Iseconds`, before fetch): `2026-10-20T17:46:58-03:00`.
- sha256 of fetched bytes (`/tmp/objdump.html`): `4fe129bd37a262b2db8e7f55f35fdd2644ec6f76b03a8e4a405614b0715e8028`.
- Quote (16 words, contiguous, verbatim): "Display a list showing all architectures and object formats available for specification with -b or -m."
- Location: `-i` / `--info` option entry, fetched HTML lines 347–348 (`<dd><p>Display a list showing all architectures and object formats available` / `for specification with <samp>-b</samp> or <samp>-m</samp>.`). Reader-text extraction (my own tag strip, not a canonical rendering): lines 333–336.

## Findings

1. **Observation (manual defines the list):** `-i` lists "architectures and object formats available for specification with -b or -m" (HTML 347–348).
2. **Observation (`-b` ties object formats to BFD names):** `-b bfdname` / `--target=bfdname` "Specify that the object-code format for the object files is bfdname." (HTML 163–167 region, reader text 163–167). So the object formats in the `-i` list are the names `-b` accepts.
3. **Observation (`-m` points back to `-i`):** "You can list the available architectures with the -i option." (reader text 372–373; HTML `-m machine` entry).
4. **Observation (verb's own wording):** `npx -y rea-agents@6.5.0 list-objdump-architectures --help` prints "List BFD targets advertised by the installed GNU objdump". The manual never uses the phrase "BFD targets" in the `-i` entry.
5. **Inference:** the verb's output is the `objdump -i` list of whichever objdump binary is on PATH, so it reflects that binary's build, not an REA-held catalogue. The manual does not itself say the list is build-dependent, exhaustive, ordered, or how it is formatted.
6. **Inference:** "BFD targets" (verb) ≈ "object formats" (manual) is an identification made from finding 2, not a sentence in the manual.
7. **Not established by this source:** the output format of `objdump -i`; whether the verb's parsing is correct; any per-build list contents. The manual does not describe the build-time mechanism that determines availability.

## Commands run (all read-only; exit codes as observed)

- `curl -sSL -o /tmp/objdump.html -w '%{http_code} %{url_effective}\n' <url>` → `200`, exit 0.
- `sha256sum /tmp/objdump.html` → `4fe129bd…8028`, exit 0.
- `python3` stdlib tag-strip + line print of the manual (reader text), exit 0.
- `grep -n` on the fetched HTML for the quote and `-b`/`-m` entries, exit 0.
- `curl -sI <url>` → `last-modified` / `content-length` as above, exit 0.
- `objdump --version` → `GNU objdump (GNU Binutils) 2.47`; `pacman -Q binutils` → `binutils 2.47-4` (read-only query).
- `objdump -i | head -12`, `objdump -i | wc -l` → 94 lines, exit 0. Host observation only; the first entries are `elf64-x86-64` (header little/little endian) with arch `i386`, then `elf32-i386`, `elf32-x86-64`, `pei-i386`. This is not the REA verb's run and is not source evidence.
- `npx -y rea-agents@6.5.0 list-objdump-architectures --help` → usage text (finding 4); `… --schema` → `args: type: object`, no input properties. The `npx` cache now holds rea-agents@6.5.0 (fetched by npx, not installed by this seat). The verb itself was not executed on any target.
- No tool installed or upgraded by this seat.

## Draft

Row for `corpus/SOURCES.md` (id is a placeholder; L1 assigns the number at integration):

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0NN | GNU Binutils objdump manual, `-i` / `--info` — https://sourceware.org/binutils/docs/binutils/objdump.html | docs | A | The `-i` option's stated meaning: the architectures and object formats selectable with `-b` or `-m`; not the output format, ordering, or the list contents of any one build | Fetched 2026-10-20T17:46:58-03:00; sha256 `4fe129bd37a262b2db8e7f55f35fdd2644ec6f76b03a8e4a405614b0715e8028` (68879 bytes; Last-Modified 2026-07-26); `-i`/`--info` entry, fetched HTML lines 347–348 | Defines the `-i` list as the architectures and object formats selectable with `-b` or `-m`, and `-b bfdname` as naming the object-code format; so `list-objdump-architectures` output can be read as the installed objdump's own selection list, not an REA catalogue. The manual does not give output format, ordering, or build dependence. | queued | 2026-10-20 | on-release | — |

## Limits and leads

- Limits: one manual page; no build-time or output-format claim is supported by it. The verb's "BFD targets" gloss is an identification (finding 6), not manual text.
- Lead (unopened, not part of this row): the binutils `objdump` source implementing `-i` would ground the list's mechanism and output format. Not opened in this seat; it is outside the manual scope.
- Reach: no REA verb was executed against a target; no Go toolchain binary was touched; the lane and baseline were not modified.

## Verdict

ACCEPTED (queued) on scope: the manual supports what `-i` lists and how `-b`/`-m` consume it, which is the part of `list-objdump-architectures` that the manual reaches. It does not support claims about the verb's parsing, output shape, or build-specific contents.
