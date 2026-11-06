# Positions are not a grammar

[Polyglot](https://www.cs.ucr.edu/~heng/pubs/polyglot-ccs07.pdf),2007 author version, relates input bytes to parser operations. Direction fields and tainted loop conditions help locate boundaries. Its output describes individual messages; flexible ordering across messages remains unresolved. Pointer decrements were future work.

[Tupni](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tupni-ccs08.pdf),2008, adds repeated records and aggregation across inputs. Processing instructions classify records; collapsing child-loop executions prevents their variable contents dominating parent comparisons. Sequence inference assumes ordered processing and single-entry loops. Unaccessed gaps become virtual fields, not recovered meanings. Sample diversity bounds coverage; compressed payloads were ignored while recovering containers. Byte-level tracking and nonregular formats remain limitations.

The refinement adds grouping evidence, not a complete protocol specification. Retain positional observations separately from repetition hypotheses and semantic names. No parser, binary, experiment or proof audit performed; current tool availability unverified.

Polyglot permits personal use, not redistribution. Tupni allows conditional personal/classroom copying; broader republication requires permission. Original commentary and links only; no code or paper passages reproduced.

Optional exercises omitted; originals retained.
