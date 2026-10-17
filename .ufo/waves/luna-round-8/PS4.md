## CLAIM
The dispatch brief is the immutable source of the preregistered L1–L10 predictions; the local restatements match it. Repo evidence does not establish that seats were technically unable to alter local copies.

## METHOD
Compared the parent-provided brief marked “PREDICTIONS FROZEN PRE-DISPATCH” with `.ufo/waves/luna-round-8/PR1.md:10-19` and `PR2.md:13`. Checked tracking and modes with `git ls-files .ufo/waves/luna-round-8; git status --short -- .ufo/waves/luna-round-8; stat -c '%A %a %n' .ufo/waves/luna-round-8 .ufo/waves/luna-round-8/PR1.md .ufo/waves/luna-round-8/PR2.md`.

## FINDINGS
PR1 repeats the expected version, 170-tool count, six named refusals, six-name absence check, and jq control result without a discrepancy; PR2’s compact prediction summary also agrees. `git ls-files` returned no paths; status returned `?? .ufo/waves/luna-round-8/`. `stat` reported directory mode 755 and PR1/PR2 mode 644, owner-writable. No evidence shows a local prediction change, but the copies are neither tracked nor write-protected.

## THREATS
Repo checks cannot prove other seats’ credentials, prevent same-owner edits, or attest a timestamped pre-probe copy. The dispatch text itself is outside repo write paths; no seat can alter that source through these repo operations.

## VERDICT
FINDING: Source predictions remain intact and local restatements agree; only the source brief is protected from repo edits, not its writable local copies.
