# ConnectorR87 notes

- Seat type: connector (read-only). No production file was edited and no tool was installed. No commands that change scratch or VCS state were run. No scratch dir was created, because none was needed: this seat only read files and grepped, and executed no counter, repair or REA command.
- Deliverable: `links.md` in this directory. The scoped report is `../ConnectorR87.md`.
- Evidence commands (read-only):
  - `grep -n` over `corpus/README.md`, `corpus/SOURCES.md`, `SKILL.md`, `PROVINCE.md`
  - `sed -n` on `tools/round-70/packed-elf.py:85-116` and `tools/round-87/*.py`
  - sibling grep `UPX|NotPackedException|[Pp]acker` over `/home/vgpnk/Projects/shokunin/*-shokunin/corpus`
  - `sha256sum tools/round-87/*.py`, which matches the claim pins f4ebd152… and 0f2d2bd8…
- Proposed move: cite R70 (not R68) as R87's population and packing-mode ancestor, and add a `packhead.cpp` S-row for the checksum-excludes-magic rule. Neither move touches the frozen files.
