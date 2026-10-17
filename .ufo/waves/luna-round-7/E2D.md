## CLAIM
Draft one admission-ready, narrowly scoped `inspect_rust_binary` entry at `corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md`; this handoff does not land it.

## METHOD
Read `corpus/QUALITY.md:11-24`, SC2 and both leg-4 receipts. No live probe, MCP call, network access, corpus/map edit, or PROVINCE change.

## FINDINGS
Proposed entry:

> # `inspect_rust_binary` 6.5.0: bounded Rust metadata reading
>
> - **Observation:** `rea-agents@6.5.0` MCP `inspect_rust_binary` returned typed `RESULT` Evidence from provider `rust-auditable` v1 on `/usr/lib/signal-desktop/resources/app.asar.unpacked/node_modules/@signalapp/libsignal-client/prebuilds/linux-x64/@signalapp+libsignal-client.node` (SHA-256 `1b44ed531f404f5358ee0618a423560463819534a38db5176bb1064b9d14d1f7`, Evidence `ev_0618e7a50e32ff9556490beeff7e0debc5d6aecf3deedb92b0d4953c747c99d3`) and `/usr/bin/rg` (SHA-256 `d006acfe51619144af4709e85945fe3b5a6f05038d356c4d8f752a33b4ecae42`, Evidence `ev_9ea97685bf6313d1e1816a43ba644a25d68459d9ec37f06dfc1b39934eb1bff2`). Exact calls, inputs, and outputs: `.ufo/waves/luna-round-6/receipts/leg-4.md:7-13,27-29` and `.ufo/waves/luna-round-6/receipts-B/leg-4.md:11-18,46-53`.
> - **Observation:** Both outputs report `auditable_metadata: null` and no `.dep-v0` section. The first reports rustc hash `da80ed0708a09dc096c184345d6eb42cbcd50a1e` as inferred from a read-only path at offset 2287779; the second reports no `/rustc/<40-hex>/` path and `rustc_commit: null` (same receipts).
> - **Inference:** This operation reads `.dep-v0` metadata and read-only compiler-path strings; it is not evidence of recovered functions, types, or runtime behavior. Missing `.dep-v0` does not establish that the binary has no dependencies.
> - **Unknown:** Embedded metadata does not authenticate dependency names, versions, sources, or the producing compiler. No runtime behavior was tested.
> - **Limitations (reported by the tool):** inspection is limited to `.dep-v0` and read-only compiler paths; resource bounds are 256 MiB input, 1 MiB dependency section, min(8 MiB, 64× section) inflated JSON, and 8 MiB report.
> - **Admission:** `RESULT` is limited to the calls and byte-pinned inputs above; it is not a Core promotion.

## THREATS
Lane-A receipt documents its Signal ELF as a fallback because SC2 carrier attribution was unavailable (`receipts/leg-4.md:15-16`). SC2 calls `/usr/bin/rg` a candidate and says `file` alone does not prove language (`SC2.md:12-15`); do not present that scout as independent Rust-language proof. Both typed outputs remain evidenced. The six entries/map rows and prior-file identity are parent integration checks, not verified here.

## VERDICT
CLEAN