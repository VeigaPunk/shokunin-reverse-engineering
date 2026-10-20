# AttackCausality — installed selection is not historical causation

**Axes:** depth and calibration. Advisory source/data review only; no judgment, execution, or provider-capability claim.

## Counterexample

**[INFERENCE FROM SOURCE] Selection can succeed while the analyzer still refuses the Program.** Hold the installed root, requested version, GOOS, GOARCH, and selected file identities fixed. The preview has no target `Program` input. S003 `GoRttiMapper.java:441-468` subsequently reads the located module's pcHeader and explicitly throws `IOException("Mismatched ptrSize: …")` when its pointer size differs from the mapper's. `getSharedGoBinary` calls this initialization only after `getGoBinary` and catches the IOException before returning null (`:104-126`); `GolangSymbolAnalyzer.java:133-151` returns false for that null mapper before type recovery. Thus even a correct nonmissing selection/bucket preview cannot establish provider recovery. This is a source-level countermodel, **not an observed mismatched-header carrier or the cause of the old op result**.

This does not repeat the previously corrected “snapshot affects only wording” error: `GoRttiMapper.java:379-396` dispatches type lookup to `GoTypeManager.java:402-455`, including `apiSnapshot.getTypeDef`. Snapshot-backed bootstrap can be necessary without selection being sufficient for recovery.

## Exact historical evidence gap

- The historical op entry explicitly supersedes its layout-cause sentence: the retained inventories establish different recovery outcomes, while the transient analyzer log was not retained and the original cause remains **UNKNOWN**. Anchor: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:196-211` (original log qualification at `:69-73`).
- Reopening the installed data directory shows no `go1.26.0.json`. Under S003 `GoApiSnapshot.java:119-145`, request `1.26.8` therefore predicts a missing same-minor base before diff lookup. That is a **current installed source-model prediction**, not evidence that the historical executing provider used these data bytes or reached this branch.
- The companion source archive was not authenticated against executing compiled classes, and no controlled target rerun was performed: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md:81-99`. The preview supplies neither the lost historical diagnostic nor a same-carrier before/after recovery observation. File digests cannot replace either.

S003 anchors above were reopened in `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`; mapper/snapshot/type-manager members are under `ghidra/app/util/bin/format/golang/rtti/`, analyzer under `ghidra/app/plugin/core/analysis/`.

## Impact and smallest safe correction

C1 already excludes historical cause, compiled provider, target execution, and patch application (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/claims.json:4-8`). Preserve that boundary; the causal promotion is not a necessary tradeoff or a selector defect. In any lesson interpreting the output, state: **“Current installed source-model selection only; original op cause remains UNKNOWN; no provider recovery demonstrated.”** Keep `patch_applied:false` and `evidence_class:'source_model'`; selected-diff bucket matching remains an unpatched-base preview. Do not convert model controls into historical repair evidence or a held target capability.

Only this report was written. No checks, target/source execution, runtime invocation, installs, or updates were performed.
