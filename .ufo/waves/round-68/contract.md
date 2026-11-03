# R68 independent prospective contract

Independent reviewer judge_kaidoku_round68 wrote this before candidate implementation or scored data. Scope: static byte custody of a PE certificate directory, not validity, trust, signature verification, loader behavior or general RVA mapping.

CLI reader receives one owned regular file. On supported results print one JSON object and exit0; on refused input print exactly {"status":"refused"} and exit1. Usage is64. No subject execution, extraction, network or path supplied by subject.

Profile: file at most1MiB; DOS MZ, 64-byte minimum, e_lfanew points to PE signature plus full20-byte COFF header. Optional magic0x10b/0x20b selects fixed96/112-byte prefix respectively. SizeOfOptionalHeader bounds all optional bytes and must fit file. NumberOfRvaAndSizes must fit that size; no hidden directory4 reads when count<5. At most96sections, complete40-byte section-table extents. Other image/machine/alignment semantics remain unvalidated.

Certificate directory4 is a FILE OFFSET, never an RVA. If count<5 output {"status":"absent","format":"pe32" or "pe32plus"}. If count>=5 and pointer/size bothzero same absent result. Mixedzero refuses. Nonempty table pointer must be8-aligned, at or beyond the end of optional+section structural headers. Entire table must fit file, size at most4096. No implicit integer wrap.

Each record starts at table cursor with8-byte prefix: little-endian u32 declared length and u16 revision/type. Length>=8; advance round_up(length,8); both declared and rounded extents fit table; consume exact total table size; maximum64records. Preserve physical order, repetitions and unknown revision/type values. Do not decode DER, infer payload length, strip zeros, deduplicate or sort.

Success exact schema:
status ok; format pe32/pe32plus; table_offset, table_size; records list with integer offset,length,revision,type and lowercase SHA256 declared_content_sha256 for bytes [record+8,record+length), alignment_padding_sha256 for [record+length,record+roundup(length,8)). No other keys. Nonzero external padding is reported, not rejected: this is descriptive byte custody, not normative certificate conformance.

Microsoft PE Format primary page opened2026-11-03: optional-header bounds and magic sections, Certificate Table address exception and attribute-certificate traversal. https://learn.microsoft.com/en-us/windows/win32/debug/pe-format . Its traversal rounds dwLength, while later WIN_CERTIFICATE description says declared length should include alignment. This profile explicitly supports descriptive rounded traversal and separates outside-length padding. An unaligned declared length or unknown fields never establishes conforming WIN_CERTIFICATE, Authenticode validity or Windows acceptance.

Construction oracle fixtures.py writes bytes and expected rows from explicit construction records, never reader output or parsing its generated subject. Salt changes content and inert DOS stub bytes. Repeated refusal outputs are disclosed. Known recipe results do not establish unseen population accuracy. Before scoring, comparator must bind every input digest and reject absent/duplicate/bool-for-int/no-op outputs. Controls must expose treating directory4 as RVA, wrong PE32/PE32+ offset, ignoring header/count bounds, sorting/deduplication, truncation, stride-not-rounded, and ignoring declared/padding distinction.
