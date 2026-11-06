# A TLS symbol does not identify one process-wide object

Sun's [Linker and Libraries Guide](https://docs.oracle.com/cd/E19683-01/817-3677/chapter8-1/index.html), edition817-3677-10 carrying2004 copyright, supplies a historical Solaris contract, not evidence about today's Linux loader.

Its TLS section distinguishes a reusable initialization template from each thread's storage. For defined STT_TLS symbols in dynamic executables and shared objects, st_value denotes an offset within that template. PT_TLS separately describes initialized file bytes, total template size and alignment. A template address therefore does not identify a particular live thread's instance.

This sharpens static artifact interpretation: preserve symbol type and coordinate system before presenting a numeric value as an address. The guide trades general dynamic access flexibility against more restricted optimized models; link editing can specialize an access sequence when its assumptions hold. Those historical Solaris restrictions are not portable loader guarantees. Conceptual comparison, not a capability gain. No binary executed. Sun's notice restricts reproduction; original commentary only, with no copied tables, code or source upload.
