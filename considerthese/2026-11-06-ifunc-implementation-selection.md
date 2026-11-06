# A named function may select its implementation

The [GCC4.6.4 manual](https://gcc.gnu.org/onlinedocs/gcc-4.6.4/gcc/Function-Attributes.html) already documents IFUNC: an ELF symbol extension whose resolver returns an implementation pointer selected for system characteristics. This is a historical baseline.

The [current manual](https://gcc.gnu.org/onlinedocs/gcc/Common-Attributes.html), inspected2026-11-06, retains the mechanism and specifies matching implementation signatures. Unlike an ordinary alias, the resolver selects a target. Analysis should distinguish exported interface, selection routine and selected implementation; a symbol name alone does not establish which body ran.

The tradeoff is selection without changing the caller-facing API, at the cost of target and toolchain dependencies. The documented requirements include Binutils2.20.1 and glibc2.11.1; indirect functions cannot be weak. These prerequisites are not proof about an installed loader or analyzer.

This complements relocation encoding notes: interpreting pointer locations does not itself resolve implementation selection. No binary execution, performance claim or universal timing inference.

FSF manual terms are GFDL1.3-or-later with specified invariant sections and cover texts. Original commentary only, no source redistribution.
