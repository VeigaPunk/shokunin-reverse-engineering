import re,sys
files={"linux.h":"linux.h","p_lx_elf.cpp":"p_lx_elf.cpp","packhead.cpp":"packhead.cpp","p_unix.cpp":"extra/p_unix.cpp"}
cases=[
("linux.h",540,'#define UPX_MAGIC_LE32  0x21585055          /* "UPX!" */'),
("linux.h",572,'uint32_t sz_cpr;            // compressed_size'),
("linux.h",579,'struct l_info       // 12-byte trailer in header for loader (offset 116)'),
("linux.h",582,'uint32_t l_magic;'),
("p_lx_elf.cpp",7755,'void PackLinuxElf64::unpack(OutputFile *fo)'),
("p_lx_elf.cpp",7778,'if (UPX_MAGIC_LE32 != get_le32(&linfo.l_magic)) {'),
("p_lx_elf.cpp",7993,'// Getting past the loader is problematic, due to unintended'),
("p_lx_elf.cpp",8065,'if (sz_cpr != UPX_MAGIC_LE32)  // sz_cpr must be h->magic'),
("p_lx_elf.cpp",9023,'void PackLinuxElf32::unpack(OutputFile *fo)'),
("p_lx_elf.cpp",9046,'if (UPX_MAGIC_LE32 != get_le32(&linfo.l_magic)) {'),
("p_lx_elf.cpp",9239,'// Getting past the loader is problematic, due to unintended'),
("p_lx_elf.cpp",9310,'if (sz_cpr != UPX_MAGIC_LE32)  // sz_cpr must be h->magic'),
("p_lx_elf.cpp",6654,'super::pack4(fo, ft);  // write PackHeader and overlay_offset'),
("packhead.cpp",62,'static upx_uint8_t get_packheader_checksum(SPAN_S(const byte) buf, int blen) {'),
("packhead.cpp",64,'assert(get_le32(buf) == UPX_MAGIC_LE32);'),
("packhead.cpp",65,'buf += 4;'),
("packhead.cpp",66,'blen -= 4;'),
("packhead.cpp",70,'c %= 251;'),
("packhead.cpp",114,'assert(get_le32(p) == UPX_MAGIC_LE32);'),
("packhead.cpp",282,'if (size > blen || p[size - 1] != get_packheader_checksum(p, size - 1))'),
("p_unix.cpp",671,'if (sz_cpr != UPX_MAGIC_LE32)  // sz_cpr must be h->magic'),
("p_unix.cpp",278,'void PackUnix::pack4(OutputFile *fo, Filter &)'),
("p_unix.cpp",327,'pack4(fo, ft);  // append PackHeader and overlay_offset; update Elf header'),
]
bad=0
cache={}
for f,n,q in cases:
    if f not in cache: cache[f]=open(files[f],encoding='utf-8').read().split('\n')
    line=cache[f][n-1]
    ok = q.strip() in re.sub(r'\s+',' ',line).strip() or q.strip()==line.strip()
    # tolerant: compare with whitespace collapsed
    ok = re.sub(r'\s+',' ',q).strip() in re.sub(r'\s+',' ',line)
    print(('OK  ' if ok else 'BAD '), f, n, repr(line.strip()[:90]))
    bad += not ok
print('bad=',bad)
