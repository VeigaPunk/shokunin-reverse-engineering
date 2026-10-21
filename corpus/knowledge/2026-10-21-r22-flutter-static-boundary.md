source: S051 https://docs.flutter.dev/testing/build-modes (Release), S052 https://developer.android.com/ndk/guides/abis (Native code in app packages), S053 `.ufo/waves/round-22/evidence/c1/identify-godot.evidence.json`
verified-at: 2026-10-21, round 22; REA CLI 6.5.0
recheck: `npx -y rea-agents@6.5.0 identify-flutter-build /home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/android_release.apk --format json --full-output`; compare target digest before comparing fields

# Static Flutter identification: a parsed negative is not a refusal

## Trigger → action → observation

The uncovered catalog surface is `identify-flutter-build`, selected in R22-C1. The supplied Godot export template at `/home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/android_release.apk` has SHA-256 `6d1bb2cfa126a1b1c87e064a35b3cbd181bef0ec784dec1efd1d64dffa8be6cb`, size 104803333 bytes (REA normalized_result.target; reproducing argv and exit retained in `.ufo/waves/round-22/evidence/c1/identify-godot-run.json`). It was parsed, never installed or executed.

**Observation:** the exact recheck argv above exited0 with `ok:true`. Evidence `ev_3458b996b71e3dccde0177728ba60ef94800dd373db5a704048e18526d9d866b`, operation `identify_flutter_build`, reports `flutter_detected:false`, `abis:[]`, `coverage:"complete"`. The raw CLI envelope is `.ufo/waves/round-22/evidence/c1/identify-godot.envelope.json`; its data member was extracted without changing members into `.ufo/waves/round-22/evidence/c1/identify-godot.evidence.json` for the existing R21 record-binding representation. This is explicit extraction, not a new producer call or an authenticated record.

**Inference:** this successful negative belongs in the tool's exercised set, not the refusal set. Its empty ABI list is bounded to the Flutter-identification inventory for this exact APK; it does not say the APK has no native libraries. Android's documented library path is `/lib/<abi>/lib<name>.so` (S052). Mobile release documentation says debugging information is stripped (S051); neither document establishes a build mode or source recovery for this APK.

**Unknown/not examined:** positive Flutter carrier behavior, Dart snapshot parsing, source reconstruction, package installation, device selection, and runtime behavior are not established by this negative. Debugger/Frida ownership remains contested with revenger and is not absorbed here. A successful negative is narrow coverage, not mastery of Flutter/Dart.

## Decision boundary

| Retained result | Decision |
|---|---|
| ok true, exact id/operation/subject, flutter_detected false | Admit one parsed negative, with the limits above |
| Error envelope or absent/unbound Evidence | Reject as held evidence |
| ABI list empty | Do not infer the absence of all native code |
| Static identity metadata | Do not infer runtime behavior or recovered Dart source |

Counting command: `python3 -I -B .ufo/waves/round-22/tools/count-c1.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV>`. Baseline records and delivered measurements live under `.ufo/waves/round-22/verify/`; a mention without a bound record must not count.

## Round-22 source qualification

S054 supersedes S052's teaching clause after W2 `PrimaryAndroid.md`:
the official ABI guide establishes the expected packaged-library path,
not any REA record semantics. **Inference:** the claim about REA ABI fields
is the lane's reading of its retained REA record, not a quotation or promise
from Android documentation. The same seat's read-only ZIP listing found
native libraries in this Godot APK despite the Flutter-specific `abis:[]`;
see its exact command/output in `.ufo/waves/round-22/w2/PrimaryAndroid.json`.
No package was installed or executed. The guide's page date is
2026-05-15 UTC; a digest of one downloaded rendering does not pin every
future rendering. S051/S053 and the exact parsed-negative observation remain
unchanged; no positive Flutter/Dart result is added.

## Current witness authority — round-22 correction

S057 supersedes S053's use of the extracted copy as held-verb authority.
The copy's contents remain accurate historical data, but current C1 does
not count it: the witness is
`.ufo/waves/round-22/evidence/c1/identify-godot.envelope.json`, preserving
`ok:true`, exact `meta.command` and the direct Evidence record. A refused
producer or mismatched command cannot become clean merely because a
detached data record is retained. The final suite separately compares this
envelope with the producing run's exact stdout and verifies the copy equals
its data; that comparison is local consistency, not authentication.

The complementary Saber observation is in
`2026-10-21-r22-flutter-positive-dart-refusal.md`: static identification is
partial-positive, while its Dart reader refuses. Neither observation
changes the scope of the Godot negative or authorizes execution.
