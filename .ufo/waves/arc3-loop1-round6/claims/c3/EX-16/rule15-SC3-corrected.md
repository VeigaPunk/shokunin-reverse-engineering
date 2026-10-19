- **A parsed-and-empty result is a statement about the parser's scope, never
  proof of byte absence — settle byte questions with a census (decode, locate,
  hash), not with the probe's function count.** The r1 creation legs probed
  0 functions on blobs that byte-contain the full runtime
  (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:24`); the round-3
  byte census measured that embedding and the entry's append-only erratum
  corrected the wording to tool-scope parsed-and-empty, "not byte-level
  absence" (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:31`). The
  same correction re-landed on the r3 entry
  (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:41-51`) and on
  r4's initcode legs — "creation probes parse empty while the runtime bytes
  are present verbatim"
  (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:39-46`) — after the
  entry had repeated the r1/r3 class
  (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:17`). The trap legs
  are the second face of the same mistake: raw-over-hex-text reads exit 0 /
  0 functions on ASCII bytes — a probe-input trap, not a carrier defect
  (`corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:27`;
  Vyper repetition `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:25`).
  The tool's own limitation says it: "empty results do not prove absence of
  dispatch" (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:29`). Word
  zero-findings at their class (parsed-and-empty vs excluded-from-inventory,
  `corpus/QUALITY.md:21`) and only then claim or deny byte presence.
