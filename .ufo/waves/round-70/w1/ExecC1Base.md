# ExecC1Base — R70-C1 base-side rederivation

Detailed transcripts and preserved forged receipt: `w1/ExecC1Base/rederive.md` and `w1/ExecC1Base/forged-base-receipt.json`.

- Independent round-69 reader forgery: kept genuine `instrument` and `rev`, invented jq counts (orig procedures 5000, packed procedures 1), while retaining apparent green verdict fields. Base checker returned exit 0, `met:true`, empty `failing` — reproduces M69-8.
- Frozen `forged-receipts.py --selftest`: 7 cases, 0 failed, `ok:true`, exit 0.
- Frozen `mutation-check.py --validate` on constant empty receipt: rejected, exit 1; identifies missing pristine flag, target hash, work directory and mutant rows.
- Validation of genuine r69-era c1 receipt: rejected, exit 1, sole defect `work_dir absent` (expected schema-era distinction, not evidence its r69-era measurement failed).
- Tool installs/updates: none. No general build/lint/test run.

VERDICT: met — base M69-8 forgery accepted; r70 battery self-test passes and validator rejects the empty constant receipt.