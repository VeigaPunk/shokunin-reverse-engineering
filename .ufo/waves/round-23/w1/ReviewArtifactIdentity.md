# ReviewArtifactIdentity — R23-C1 signal carrier boundary

## Findings

### Medium — QUALITY12 is contradicted by the synthetic generator's reproducibility claim

- **Observation:** `corpus/QUALITY.md:22` requires retaining the exact synthesized carrier bytes or a full regenerating recipe, and prohibits byte-exactness claims for re-synthesized output. The generated input is otherwise well identified: `tools/make-uart.py:2-6,16-26` describes an offline synthetic UART carrier, with channel-0 bytes, 960 kHz sampling, 100 samples/bit, 9600 baud, ASCII `Hi`, and fixed idle/start/data/stop bits. The generated instance is `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/evidence/c1/uart-hi.bin`, 2,500 bytes, SHA-256 `4a2e729f514482287c17596cff3b29f07141fae9e86353680c99b1065e861727`; direct `sha256sum` of that path returned that digest.
- **Concrete defect:** `tools/make-uart.py:6` says “All fixture bytes are reproducible.” In this context that asserts exact byte-for-byte regeneration of a re-synthesized carrier, the claim QUALITY12 explicitly bars. The actual recipe and current carrier are retained, so the observed run remains identifiable; the defect is the unqualified reproducibility statement, not missing carrier identity. Scope the wording to say the recipe is retained and the current generated instance is identified by its path/hash, without asserting a future re-synthesis is byte-identical.
- **Run linkage observed:** `evidence/c1/generate-uart.run.json:1` records `python3 -I -B …/tools/make-uart.py …/evidence/c1/uart-hi.bin`, exit 0, empty stderr, and stdout containing the output path/hash/size/rate/baud/payload/bit list plus `acquisition: synthetic; no hardware`. `evidence/c1/decode-uart-hi.envelope.json:1` binds the decoded artifact to the same absolute path and SHA, reports provider `sigrok-cli@0.7.2`, and says `hardware_acquisition: not-performed`. The envelope's annotations are `48` and `69` under `uart:rx=0:baudrate=9600`; these are decoder observations for this carrier, not evidence of hardware acquisition.

### Low — the public fixture scout's in-memory archive inspection lacks the absolute artifact path required by QUALITY4

- **Observation:** `corpus/QUALITY.md:14` requires an absolute path plus stable identity for the artifact under analysis. `w1/SignalCarrierAlternatives.md:20-30` names the public `.sr` fixture and its pinned URL/SHA-256, while `:62-88` reports inspection of its embedded archive metadata. The same report says at `:128-130` that the bytes were kept only in process memory and no fixture file was written or retained. Thus the report supplies a strong URL/hash identity, but not an absolute local path for the artifact whose archive metadata it describes. This is a strict QUALITY4 documentation gap for that artifact-inspection claim; it does not make the fixture identity ambiguous or invalidate the separate REA decode, which does have a local absolute path and matching hash in `evidence/c1/decode-official-uart.envelope.json:1`.
- **No acquisition claim observed:** the scout report's scope at `:3-6` and closeout at `:128-130` expressly disclaims acquisition. The retained `evidence/c1/official-download.json:1` identifies the upstream immutable GitHub URL, HTTP 200, 58,381 bytes and SHA-256 `01b72610cdc4510dd46c8ce82b163947adbbab5b9883aea164c00e15af900b61`; the local decoded file has that same digest. This supports “public-source fixture downloaded for offline decoding,” not “recording acquired by this round.” The README's analyzer description in `SignalCarrierAlternatives.md:36-60` remains documentary upstream metadata, not direct observation of acquisition.

## Residual risk

- The generation run records the script pathname and argv but not a generator-source digest. During this review the current `tools/make-uart.py` SHA-256 was `e22a8f1f11b4cf844904ce78c63d12f6e280f041653bced0c639ef03a21f0fce`; preserve that source revision with the run if later edits could make its recipe attribution ambiguous. This is a provenance risk, not evidence that the current recipe is incomplete: the full current script is present and its command and output are retained.
- `git status --short` showed the round-23 material as untracked at review time; this report is author-side review of the present workspace, not integrated or committed verification.

## Verification gaps

- No LSP device is mounted (`read xd://lsp` returned “No such tool” and listed the available mounted tools). Accordingly, no LSP references/definition/diagnostics queries were possible. Grep was used only to locate material, not as semantic proof.
- I did not run REA, regenerate either carrier, or re-run decoding/tests. The evidence cited above is the retained run record plus read-only source inspection and `sha256sum`.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/ReviewArtifactIdentity.md` — this author-side review; its SHA-256 is supplied in the handoff (self-hash omitted here).

## Installs

- None.

## Open risks

- The QUALITY12 wording and QUALITY4 local-path gap remain for the owning author/integration review; this seat did not edit other seats' files.