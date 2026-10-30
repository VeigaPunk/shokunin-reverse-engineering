# R52-C1 pre-freeze controls — expected verdicts

| Control | Expected observation | Exit |
|---|---|---:|
| CTL-OLD | Round-50 rule: 2/4; Cable passes, both FRITZ!Box carriers fail gaps | 1 |
| CTL-NEW | Round-52 law rule: 4/4 | 0 |
| CTL-DN | No receipts; never green (exit 1 or 2) | 1 or 2 |
| CTL-JUNK | Valid rule requiring all kinds with impossible allowance: 0/4 | 1 |
| M1 | All-thirteen detail whitelist rejected by `law_shape_ok` | 1 |
| M2 | Fourteenth-device census fixture passes law; whitelist rejects | law 0 / whitelist 1 |
| M3 | `required.char-device=true`, only `247:0`: reproduces 2/4 | 1 |
| M4 | Strict-subset whitelist rejected | 1 |

The driver is offline: all substantive evaluation must be performed by the v2 counter's `controls` mode over committed round-50 `after.json` receipts and frozen oracle tables. No REA invocation is part of this control set.
