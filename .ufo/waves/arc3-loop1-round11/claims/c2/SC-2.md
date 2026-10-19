# SC-2 — C2 freshness receipt: Ghidra inventory counts

**Measurement date:** 2026-10-19  
**Disposition:** no drift; no erratum required.

## Re-derived values

`PROVINCE.md:40,46` records the Ghidra provider installation and the inventory as 34 feature directories and 39 processor modules (verified there on 2026-10-13). I independently counted the immediate directories in the live install tree at `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`; the command also read its `application.version` to identify the installation.

- Features: recorded 34; live 34; delta 0 — **VERIFIED / REPRODUCED**.
- Processors: recorded 39; live 39; delta 0 — **VERIFIED / REPRODUCED**.

## Exact measurement

Command:

```bash
python3 - <<'PY'
from pathlib import Path
import re
root = Path('/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC')
properties = (root / 'Ghidra/application.properties').read_text()
version = re.search(r'(?m)^application\.version=(.+)$', properties).group(1)
for label, rel in [('features', 'Ghidra/Features'), ('processors', 'Ghidra/Processors')]:
    path = root / rel
    entries = sorted(p.name for p in path.iterdir() if p.is_dir())
    print(f'{label}: count={len(entries)}')
    print(f'{label}_directories={entries}')
print(f'application.version={version}')
PY
```

Output:

```text
features: count=34
features_directories=['BSim', 'BSimFeatureVisualizer', 'Base', 'BytePatterns', 'ByteViewer', 'CodeCompare', 'DataGraph', 'DebugUtils', 'Decompiler', 'DecompilerDependent', 'FileFormats', 'FunctionGraph', 'FunctionGraphDecompilerExtension', 'FunctionID', 'GhidraGo', 'GhidraServer', 'GnuDemangler', 'GraphFunctionCalls', 'GraphServices', 'MicrosoftCodeAnalyzer', 'MicrosoftDemangler', 'MicrosoftDmang', 'PDB', 'ProgramDiff', 'ProgramGraph', 'PyGhidra', 'Recognizers', 'Sarif', 'SourceCodeLookup', 'SwiftDemangler', 'SystemEmulation', 'VersionTracking', 'VersionTrackingBSim', 'WildcardAssembler']
processors: count=39
processors_directories=['6502', '68000', '8048', '8051', '8085', 'AARCH64', 'ARM', 'Atmel', 'BPF', 'CP1600', 'CR16', 'DATA', 'Dalvik', 'HCS08', 'HCS12', 'Hexagon', 'JVM', 'Loongarch', 'M16C', 'M8C', 'MC6800', 'MCS96', 'MIPS', 'NDS32', 'PA-RISC', 'PIC', 'PowerPC', 'RISCV', 'Sparc', 'SuperH', 'SuperH4', 'TI_MSP430', 'Toy', 'V850', 'Xtensa', 'Z80', 'eBPF', 'tricore', 'x86']
application.version=12.1.4
```

## Limits

This receipt verifies the installed tree's immediate directory counts and its declared application version. It does not test that every feature or processor module loads, nor does it re-probe REA provider readiness. No prior seat or round supplied the live measurements above.
