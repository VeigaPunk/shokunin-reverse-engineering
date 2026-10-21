# R21Attack56 — R20 Harmony retained witness

Axes: calibration; depth.

## Supported local binding

- Directly read the exact CLI response at `.ufo/waves/round-20/evidence/c2/harmony/project-stage-json/stdout.txt` and the retained record view at `project-stage-json/projection-evidence.pretty.json`. Both carry output Evidence ID `ev_a437cf77ed5381ee7e71d36a87a7407bd5f38cb911a2432e8eb69ff554a74820` and operation `project_harmony_application_graph`. The exact same knowledge entry, `corpus/knowledge/2026-10-20-r20-harmony-application-graph.md:15`, cites this output ID, projection `hmp_a9fd23092c373ec51ff385d2936c5c1e2631d8fc33dccc7e1fbd0916f81954f6`, and Stage result. Adjacent receipt `project-stage-json/receipt.json:20-30,40-45` records exit 0 and the exact stdout/retained-view paths and hashes.
- The record's `parameters.inventory_evidence_ids` is `ev_ae4600c27ed4b6ed50dccafeb3983157577ab59835d2d0d21c9876e4ab25031b`. This is the input inventory Evidence ID, not the projection's output Evidence ID used for this binding.
- Stage scope is synthetic: the same knowledge entry says the run used recipe-retained synthetic HAPs (`:2,9-11,36`), and the record subject is `stage.hap`, format `hap`, digest `21d46dbc88ba8f8c1306a70f727d8ee0383dc37c19430463dc7849f557c4a65f`. The projection is path-presence evidence only, not proof of manifest semantics, a valid shipped app, device/runtime behavior, or whole-package semantic completeness.

## Assigned verification

Ran the inert local validator against the retained JSON record view (twice with identical script argv; the second call exposed the exit status):

```text
argv: ["python3", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/verb-coverage.py", "--evidence", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/evidence/c2/harmony/project-stage-json/projection-evidence.pretty.json", "--verb", "project-harmony-application-graph", "--evidence-id", "ev_a437cf77ed5381ee7e71d36a87a7407bd5f38cb911a2432e8eb69ff554a74820"]
exit: 0
stdout: {"bound": true, "finding": "evidence_bound", "pathless": false}
stderr: empty (no stderr output observed)
```

This is a supported local record binding, not cryptographic authentication. The explicitly reported `pathless: false` matches the record's non-null `subject` object and its recorded temporary `local_path`; it does not establish that the temporary carrier path still exists. No carrier/provider execution or production changes were made.

## Gaps and method note

No LSP device is mounted (`xd://lsp` returned “No such tool”); no caller/definition claim was needed or made. No unresolved gap prevents this one local binding. The validator establishes the record's declared Evidence ID and operation only.
