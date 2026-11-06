# A checksum revision is not damaged data

Stewart and colleagues’ [RFC 2960](https://www.rfc-editor.org/rfc/rfc2960.txt), October 2000, §6.8, specifies Adler32 for SCTP packet checks.

Stone, Stewart and Otis’s [RFC 3309](https://www.rfc-editor.org/rfc/rfc3309.txt), September 2002, §§1–2, replaces it with CRC32c because of short packet weaknesses, without a graceful transition. Algorithm version and bit/byte mapping therefore matter before treating a failed check as evidence of corruption. These historical definitions do not establish current implementation behavior.

Both are official Standards Track texts under Internet Society copyright. Conditional copying and explanatory derivative permissions retain document alteration restrictions. Public access establishes neither unrestricted reuse nor training permission.

Optional exercises omitted; originals retained.
