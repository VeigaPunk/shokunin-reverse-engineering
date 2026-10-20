Round-17 L1 pilot (2026-10-20 ~10:17-10:19 -03), NOT the final measured runs.
Argv (cwd /tmp/kr17-pilot): timeout 900 npx -y rea-agents@6.5.0 analyze /usr/bin/shfmt --format json
                            timeout 1200 npx -y rea-agents@6.5.0 analyze <kimi-code pnpm>/@esbuild+linux-x64@0.25.12/.../bin/esbuild --format json
Log retention: 1 s polling `cp -f /tmp/rea-ghidra-<new>/ghidra.log script.log` while REA ran (REA deletes its runtime root at close;
no keep knob found: grep REA_GHIDRA_ in rea-agents 6.5.0 dist lists LANGUAGE_ID, COMPILER_SPEC_ID, SEED_FILE, NATIVEAOT_JAR, DISABLED_ANALYZERS, STARTUP_TIMEOUT_MS).
The last copy can miss lines written after the final poll; pre/post carrier pins were NOT recorded in the pilot.
Carrier ids: shfmt sha256 58f765638eed5309573967726d9f9f54c8ba16cbcc65a6a5dfe0e5285aeab459 (go1.27.0-X:nodwarf5 per rea inspect-go-binary);
esbuild 0.25.12 sha256 bab29b2ca7a9e89b67cf720b77b2d743f9f31f5cf0d5bd74ee8c8de30ced7014 (go1.23.12).
