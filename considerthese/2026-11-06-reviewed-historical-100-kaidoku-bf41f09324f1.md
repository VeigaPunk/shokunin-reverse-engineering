# Aggregate classification across calling conventions

Arm, [AAPCS64 2019Q4](https://github.com/ARM-software/abi-aa/blob/be929410dd6890433ccabd93c157b467fdc6fef3/aapcs64/aapcs64.rst), issued January 2020: Homogeneous Aggregates, Parameter Passing and Result Return connect type classification with result transport.

[2025Q1](https://github.com/ARM-software/abi-aa/blob/c51addc3dc03e73a016a1e4edf25440bcac76431/aapcs64/aapcs64.rst), issued April 2025: corresponding sections and Soft-float. Added in 2024Q3 for Arm v8-R without floating-point instructions/registers, soft-float removes HFA/HVA classification. It is incompatible with base; toolchain support is optional. Vector calling conventions remain undefined there.

Retained official pinned editions reread locally; no fresh retrieval or compiler verification. CC-BY-SA4.0 plus additional patent terms, including broader defensive termination; trademarks reserved. Original commentary and links only, no training permission inferred.

Optional exercises omitted; originals retained.
