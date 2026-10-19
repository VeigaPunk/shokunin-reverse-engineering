EX-6 (arc3-loop1-round6, c2 chain) — verification evidence index
================================================================

Seat artifact: ../EX-6.md  (the claim/adjudication)
Scratch used at run time: /var/tmp/ex06-r6 (never /tmp; EDQUOT rule)

scripts/
  compile3.js        my independent solc standard-JSON driver, three legs
                     (viair-opt200, viair-noopt, std-opt200)
  walk.py            my independent linear-sweep EVM decoder/walker:
                     guard form, PUSH4 sites + following compare op, EQ stride,
                     SUB legs, JUMPDEST set, push4_pc+10 offset rule

src/
  ViaIrVault.sol     byte-for-byte copy of EX-7's carrier (sha256 f5391167…80cbbe)
                     — copied read-only only to recompile it
  RelayDesk.sol      my own 10-external carrier, no fallback
  RelayDeskFb.sol    my own 10-external + receive + fallback(bytes) carrier

receipts/
  repro-compile.txt       recompile of EX-7's carrier — all three legs byte-identical
  own-relay-compile.txt   RelayDesk, three legs
  own-fb-compile.txt      RelayDeskFb, three legs
  sha256.txt              hashes of the retained scripts/sources

walks/                my byte walks of the compiled runtimes (JSON)
  repro_viair-opt200_runtime.bin.json
  repro_viair-noopt_runtime.bin.json
  repro_std-opt200_runtime.bin.json
  own-relay-viair.json, own-relay-std.json
  own-fb-viair.json, own-fb-std.json

probe/                sealed REA envelopes from this seat's runs + summary.json
  6.4.0 legs: hex, raw, noopt, legacy control, raw-on-hex TRAP, creation
  6.7.0 leg:  viair-opt200 hex
  own carriers: RelayDesk viaIR + legacy, RelayDeskFb viaIR
  summary.json: per-leg evidence_id, decoded sha, counts, missing/extra,
                mutability mismatches, offsets
  NOTE: ev ids here are mine at /var/tmp paths; the entry's ids are
        path-sensitive and recorded in EX-7/probe/. Join cross-seat by the
        decoded bytecode sha256, never by ev id (corpus/QUALITY.md #15).

commandA-58c3db7.json      command A at the work commit  (84/84, 14 rules)
commandA-c625d5d.json      command A at the records commit (84/84, 14 rules)
commandA-overlay-85.json   command A on a scratch overlay of c625d5d with the
                           draft entry + EVM-row token (85/85, 14 rules)

bytes-facts.txt       the byte-level facts cited in EX-6.md §2–§4:
                      guard bytes, SUB-leg/offset convention, creation +43 embed,
                      CBOR trailer, probe summary, selector/mutability join,
                      command A results, and the four prose-defect measurements

Reproduce: see EX-6.md §7.
