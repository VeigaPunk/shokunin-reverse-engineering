# EX-5 — C2 freshness: PROVINCE pin re-anchor + receipt

Scope: seat evidence and proposed patch only. No source file or live config was edited. The receipt is carried here because this seat may write only inside its own round-8 artifact directory; it is not represented as landed in `.ufo/receipts/`.

## Re-derived evidence

Measured against lane repo `HEAD` `904b724258fc9396a016bd9952b5cd40225fb7d8` (from `git rev-parse HEAD`).

- **VERIFIED — live pin location/content.** Grep search for `rea-agents@` in `/home/vgpnk/.kimi-code/config.toml` returned `/home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]`. A bounded read of line 4126 returned the same content. The independently measured file length is `4150` lines (`wc -l /home/vgpnk/.kimi-code/config.toml` → `4150`).
- **VERIFIED — cited pointer is stale.** Grep search for `config.toml:3546` in `PROVINCE.md` returned one match at `PROVINCE.md:18`, in the Kimi 6.7.0 pin citation. The live config line 3546 is `max_output_size = 64000`, under `[models."github-copilot/gemini-3.7-flash"]` at line 3541; it is not the REA pin. Grep search for `config.toml:4126` in `PROVINCE.md` found no match.
- **VERIFIED — line-neutral patch shape.** In-memory substitution found exactly one old pointer, changes only line 18, preserves `162` lines, and preserves `19908` bytes. Pointer text lengths are both `29` bytes. The proposed patch is:

```diff
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -18 +18 @@
-`rea-agents@6.7.0` (`~/.kimi-code/config.toml:3546` at the 2026-10-19 re-read; the 17:55:49Z receipt's pointer :3298, and earlier :2940 [16:57:35Z] and :3227 [17:32Z], are historical). Cache/catalog
+`rea-agents@6.7.0` (`~/.kimi-code/config.toml:4126` at the 2026-10-19 re-read; the 17:55:49Z receipt's pointer :3298, and earlier :2940 [16:57:35Z] and :3227 [17:32Z], are historical). Cache/catalog
```

The historical pointer numbers and timestamps in the unchanged suffix are preserved solely to make this exact one-line diff applicable; EX-5 did not remeasure or rely on them. The only live location asserted here is `:4126`, independently measured above.

## Receipt — live line content

```text
source: /home/vgpnk/.kimi-code/config.toml
line: 4126
content: args = [ "-y", "rea-agents@6.7.0", "mcp" ]
sha256(line content bytes, excluding LF/CRLF): eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1
measured: 2026-10-19
```

The hash was derived by streaming the live file and hashing only the selected line's bytes after stripping its line terminator. Reproduction command and observed output:

```text
python3 - <<'PY'
from hashlib import sha256
from pathlib import Path
p = Path.home() / '.kimi-code/config.toml'
selected = {}
line_count = 0
with p.open('rb') as stream:
    for line_count, raw in enumerate(stream, 1):
        if line_count in (3546, 4126):
            selected[line_count] = raw.rstrip(b'\r\n')
for n in (3546, 4126):
    value = selected[n]
    print(f'{n}:{value.decode()}')
    print(f'{n}_content_sha256={sha256(value).hexdigest()}')
print(f'line_count={line_count}')
old = b'~/.kimi-code/config.toml:3546'
new = b'~/.kimi-code/config.toml:4126'
print(f'pointer_bytes_old={len(old)} pointer_bytes_new={len(new)}')
PY

3546:max_output_size = 64000
3546_content_sha256=e773a2c14c9eb4e57fb0d320c9e39b024650e6a0e180ed2e36e97f76423cf28b
4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
4126_content_sha256=eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1
line_count=4150
pointer_bytes_old=29 pointer_bytes_new=29
```

The corresponding PROVINCE substitution check printed:

```text
pointer_occurrences=1
changed_lines=[18]
line_count_before=162 line_count_after=162
bytes_before=19908 bytes_after=19908
```

## Landing status

- **CORRECTED (patch prepared, not applied):** the replacement target is the freshly measured `:4126` pin; the exact patch is above.
- **UNVERIFIABLE — same-commit condition:** this seat artifact cannot establish that the PROVINCE edit and C1 `ptr_check` extension land in the required same commit. The patch remains a draft until the integrator applies it alongside C1 and records/commits the receipt. No C1 gate or source change was made by EX-5.
