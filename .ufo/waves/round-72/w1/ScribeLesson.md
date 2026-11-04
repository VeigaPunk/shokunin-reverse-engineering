# ScribeLesson — round-72 scoped drafting report

## Behavior and gates

Drafted the lesson for L1 KaidokuR72 without landing it in corpus or changing any instrument. Axes: coverage, calibration, operability. Two Mistakes rows distinguish the round-71 route-only observation boundary from checker-mode coverage, and the reported survivor i from a committed selftest kill. Each fix names a round-72 case that can fail.

The claims container was present and read. Base/declaration/operative-freeze values come from the canonical assignment; the freeze gate was not rerun. No C1/C2/C3 landing verification, source admission, or canonical judgment is asserted by this seat.

## Findings and provenance

1. The actual docstring is qualified: “every child of the route” (tools/round-71/packed-elf.py:53), not an unqualified promise about every process in every mode. Its route capture and the checker capture must remain separate. The round-71 lesson reports all 46 route children captured, while explicitly excluding the checker's own git/readelf environments. The round-71 checker git call at lines 514–516 omits env; its readelf call at line 702 omits env/capture. Existing round-72 l1/pre/c1-at-base.json corroborates the gap: 9/11, failures A10_run_binding and A11_checker_env; A11 has empty checker_child_env, both canaries present, keys_exact false, yet checker rc 0.
2. Round-71 MutReaders/mutants.md:27,39,57 reports survivor i at probe:471; its complete A10 arm did NOT become green. The surviving local binding observation is not evidence of false acceptance by the genuine checker. Existing round-72 l1/pre/c2-at-base.json records survivor_count 1, A10_binding_force_true, expect_case null, seven pristine cases. Existing l1/pre/c2-mutant-test.json records the r72 mutant killed only by a10-binding-from-checker, ten pristine cases green, killed_wrong_case empty, target pin matched, rev 306cbb3fb11661fba6f364f73ad0b1eeb24a959f. These are retained prior receipts, not executions by this scribe.
3. ScoutSource-6 was running with “No final output yet” when read. The Gate table therefore preserves the exact required placeholder [L1 — filled by the non-author closure.] for URL/date/quote/digest fields. No guessed URL, quote, digest, or admission was fabricated.

## Actions and outcomes

Read/grep operations inspected the claims container, previous lesson, round-71 MutReaders report, round-71 checker/probe sites, round-72 checker/probe/battery sites, and the three named pre receipts. JSON selections read c1-at-base.json fields {arms_passed,target,failed} and its A11_checker_env arm. No tests, builds, linters, fixtures, or runtime invocations were run.

The only shell command, with cwd /home/vgpnk/Projects/shokunin/kaidoku-shokunin, was:

~~~sh
S=/fast/scratch/hyaku/kaidoku-r72/ScribeLesson; trap 'rm -rf -- "$S"' EXIT; mkdir -p -- "$S" /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-72/w1/ScribeLesson; printf 'Scratch allocated explicitly: %s\nNo runtime or fixture invoked; cleanup registered.\n' "$S"
~~~

It completed successfully, printed the explicit scratch location and cleanup registration, and exited through its cleanup trap. No scratch receipts were generated. No tools installed or updated. No git/jj mutations, commits, pushes, publication, deployment, product-code edits, or other runtime invocation.

## Touched surfaces and artifact paths

- .ufo/waves/round-72/w1/ScribeLesson/round-72.md — requested lesson draft; intended corpus landing belongs to L1.
- .ufo/waves/round-72/w1/ScribeLesson/ScribeLesson.md — this report inside the assigned seat directory.
- .ufo/waves/round-72/w1/ScribeLesson.md — identical scoped report at the explicit Report trailer path.

## Bounds conflicts and limits

The assignment says “Every path you write is absolute under that lane; a write anywhere else is a defect” and also expressly instructs scratch at /fast/scratch/hyaku/kaidoku-r72/<your-seat-name>/. The command used only that named scratch exception, then removed it via trap. The assignment says “Write your Report: inside .../w1/ScribeLesson/” and also “Report: write your scoped findings to .ufo/waves/round-72/w1/ScribeLesson.md”; both report locations are supplied, with identical content. These conflicts are recorded for the canonical Rust judge, not adjudicated here.

Out of scope: corpus landing, final source row, wave-result synthesis, claim acceptance, freeze-gate reruns, and product/instrument repair. L1 must fill the explicit source and wave placeholders from seat evidence; they are requested drafting placeholders, not completed gate results.

## Self-evaluation

Accuracy 4/5: concrete source sites and prior receipts cited; no new execution establishes landing behavior. Completeness 4/5: both requested mistake rows and all draft sections supplied; source/wave fields intentionally await non-author closure. Clarity 4/5: boundary between route/checker and survivor/false-acceptance is explicit; long evidence rows remain dense. Actionability 4/5: exact case names and paths supplied; final closure requires other seats' artifacts. Conciseness 4/5: raw receipts are referenced rather than duplicated; two report copies satisfy conflicting locations. Overall 4.0/5. Highest-impact improvements at L1 closure: replace source placeholders with ScoutSource evidence and bind wave conclusions to measured after receipts. Would the user agree? The deliverable is an explicitly scoped draft, not an invented completed round.

Report: .ufo/waves/round-72/w1/ScribeLesson.md
