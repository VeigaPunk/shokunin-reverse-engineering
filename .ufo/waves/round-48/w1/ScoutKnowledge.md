# ScoutKnowledge — round 48 knowledge citation

Cite this, with this line range:

`corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:38-61`

Those lines say that five structure-blind readers still reach the green target of 8/8 while the gate keeps trusting its registered shortcut set, and that the same gate still prints clean when it trusts `met_target` without checking `matched`, when a shortcut is relabelled `structural`, when the class set is dropped to three, or when the counter does not carry the frozen predicate.

That record is what block 25's knowledge cite has to ground. A registered class set can hold while the surface stays shortcut-reachable (the file's own word on line 10 is "shape-recoverable"). A check has to fail on the binding it names: here, a meaning class for each exit digit, and a floor for the arm, because a green digit row or a membership count can hold while the claimed work is skipped. The lines record the checks that stayed green; they do not themselves use the words "must fail".

## Why this entry

QUALITY row 77(a) is the appended paragraph at `corpus/QUALITY.md:139`. It requires a new `## Queue-drain craft` block to cite at least one `corpus/knowledge/` entry with a line range. It does not name the entry. The table cell `| 77 |` at `corpus/QUALITY.md:85` is a different criterion (enumerate every statement shape).

The knowledge catalog row is `corpus/README.md:208`. The coverage-map row for the same stem is `corpus/README.md:88` ("held as a tool, not as capability" — five unregistered structure-blind classes met the green surface 8/8). No other file under `corpus/knowledge/` states a registered class set holding while unregistered shortcuts reach the target, or a gate staying clean when its claimed binding is false. The shortcut mentions in the r30, r31, and r43 entries are reader-control notes of a different claim.

Load-bearing lines inside `38-61` (file has 79 lines):

- 38: name-pool reordering left every record-array invariant intact; five structure-blind readers reach 8/8.
- 48: registering any of those classes flips the gate to `REFUSED`, so the registered set was unfaithful to the class it names; a target a control that skips the claimed work can reach is not an improvement.
- 54: the frozen green surface did not force bounded record traversal.
- 58: a 1,979-byte gate that runs no reader satisfies all six clauses.
- 59: a shortcut relabelled `structural` prints `CLEAN` on the red config.
- 60: dropping classes to `MIN_SHORTCUTS = 3` still prints `CLEAN`.
- 61: the frozen predicate is not the sentence the counter and receipts carry (`PREDICATE_IDENTITY_FALSE`).

Blocks 23 and 24 already cite `:40-66` of this file. That span includes lines 48 and 58-61, starts at the table header (the 8/8 sentence is line 38), and runs through the pin, permutation, and fixture limits on lines 62-66. `38-61` is the span whose ends are the reach sentence and the predicate-identity failure. Either range satisfies the line-selector check in `tools/round-48/meanings.py` (`1 <= 38 <= 61 <= 79`). The cite to land is `38-61`.

## Identity of the bytes

Blob `d9904ddcb99e9055d7d96bfec6906458af322f8a` is the same object at base `61b87d742032e65fca9c38267d7d6ed7e555edad`, freeze `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`, and `HEAD` `0d76deedd7ce9dd17c510494c33b7b00c3282554` (measured 2026-10-28T18:53:04Z). Worktree `git status --porcelain` for this file, `corpus/README.md`, and `corpus/QUALITY.md` was empty. `git diff --stat` base..HEAD for the knowledge file was empty. Content sha256 `305927792b13975708754d21d96bcbe879844d572ff6a8c620b29070f424eb50` (8890 bytes, 79 lines). Last commit that touched the file: `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930` (2026-10-26 01:50:56 -0300).

## What this seat did not run

`tools/round-48/meanings.py` and `tools/round-48/record2.py` were not run. Their clauses are not passed here. No package was installed.

## Receipts

Disk guard before the pass: exit 0, `/fast/scratch/hyaku` 32% used, 546.2G free (`receipts/disk-guard.*`, utc 2026-10-28T18:52:32Z, stdout sha256 `b8e778e1dce05fb0fe54843c690db3f704e579e6c9f9227d26699b7456d48809`).

| receipt | exit | utc | stdout sha256 |
|---|---|---|---|
| `head` `git -C <lane> rev-parse HEAD` | 0 | 2026-10-28T18:53:04Z | `a06c0a7c8821c220dd9946b2c82f626fd431f18bdf01e0263384f2f80f12816f` |
| `base` `git rev-parse 61b87d74…` | 0 | 2026-10-28T18:53:04Z | `c00042392af3a38f8ece3777d023afcf50c04943fb9c247d19235da21e6436e0` |
| `freeze` `git rev-parse dc73587a…` | 0 | 2026-10-28T18:53:04Z | `b1500dada38bd3f73a4643517feebb0fb14f74741f260d06ff614e5d6c729047` |
| `know-log` | 0 | 2026-10-28T18:53:04Z | `a56d807e6bdc012e848860268926c4f70fab877e0115f17a373ad71c070a3eb8` |
| `know-head-blob` / `know-base-blob` / `know-freeze-blob` | 0 | 2026-10-28T18:53:04Z | `2f7d251853be3db4b709b28bd26e857d54aaca9636e8fb730c9892754b4c0325` (same stdout: blob `d9904ddc…`) |
| `know-diff-base-head` | 0 | 2026-10-28T18:53:04Z | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) |
| `worktree-vs-head` | 0 | 2026-10-28T18:53:04Z | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) |
| `lines-38-61` (line extract + content sha256) | 0 | 2026-10-28T18:53:04Z | `7cc35c0f67a6f20c60454e451bc5d1179673cb2c267a314283299b46b610f3a1` |
| `index-pins` (README 88 and 208, QUALITY 85 and 139) | 0 | 2026-10-28T18:53:04Z | `9e62b70f1fcbf1ff20d960ca5a236bfcbd8d1c71fe5116c901db3aaac94074b5` |

Copies: `.ufo/waves/round-48/w1/ScoutKnowledge/receipts/`.

## Confidence and unknowns

Confidence high on the entry and on `38-61`. The historical 8/8 runs named inside the entry were not re-executed. An integrator who wants the same selector string as blocks 23 and 24 can keep `:40-66`; that span still contains lines 48 and 58-61.
