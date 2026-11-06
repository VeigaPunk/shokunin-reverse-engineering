# Kaidoku: recover state at the stopped location

[DWARF2](https://dwarfstd.org/doc/dwarf-2.0.0.pdf), July1993 Industry Review Draft, describes location-indexed unwind rules. Frame-address calculations can change within a routine; its name alone cannot identify the applicable recovery rule.

[ORC](https://github.com/torvalds/linux/blob/bebc6082da0a9f5d47a1ea2edc099bf671058bd4/Documentation/x86/orc-unwinder.txt), Linux4.14, uses objtool-generated stack tables instead of DWARF's richer state machine. Simpler runtime interpretation trades against table memory and dependence on compiler-code analysis; unusual assembly still needs annotations.

Read retained DWARF introductory frame-information passages and the full historical ORC document. Neither establishes successful recovery on a present target, nor makes ORC a universal replacement.

DWARF permits reuse subject to attribution and notice conditions. ORC has no file-specific license notice; document reuse clearance remains unresolved here. Original commentary only, not source redistribution or training approval.

Optional exercises omitted; originals retained.
