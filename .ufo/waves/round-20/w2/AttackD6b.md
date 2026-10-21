HOLDS — D6b’s tested write/network isolation holds; `--host-home` exposes a read-only host-home view, including `.ssh` names, but no write escape was observed.

Scope/provenance: Used the `revexec.py` blob from measured revision `5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9` (SHA-256 `d30c503bccf426318c01c811c8e2edae4909f6a7b834936bc1f333eea9853e2c`), not a working-tree copy. A harmless one-file fixture at temporary commit `2b4a8f5a3b1ff9a7536472948158c61f26cc2f69` supplied the payloads. Fixture and helper lived under `mkdtemp` `/tmp/r20-revexec-probe-00nny1q2`, removed after the runs; `REVEXEC_WORK_BASE=/fast/scratch`.

Commands and observations (each outer command exit 0; stderr empty):
```text
python3 -I -B /tmp/r20-revexec-probe-00nny1q2/revexec.py run --root /tmp/r20-revexec-probe-00nny1q2/fixture-repo --rev 2b4a8f5a3b1ff9a7536472948158c61f26cc2f69 --entry probe.py -- home ..revexec-probe-616eac7e6ada4f40bcaa8736f982b12c
  HOME_WRITE_SUCCEEDED; HOME_IS_CWD=True
python3 -I -B /tmp/r20-revexec-probe-00nny1q2/revexec.py run --root /tmp/r20-revexec-probe-00nny1q2/fixture-repo --rev 2b4a8f5a3b1ff9a7536472948158c61f26cc2f69 --entry probe.py --host-home -- home .revexec-probe-616eac7e6ada4f40bcaa8736f982b12c
  HOME_WRITE_REFUSED errno=30 (read-only filesystem)
python3 -I -B /tmp/r20-revexec-probe-00nny1q2/revexec.py run --root /tmp/r20-revexec-probe-00nny1q2/fixture-repo --rev 2b4a8f5a3b1ff9a7536472948158c61f26cc2f69 --entry probe.py -- hosttmp /tmp/revexec-probe-616eac7e6ada4f40bcaa8736f982b12c
  HOSTTMP_WRITE_SUCCEEDED inside the unit; host marker absent after run
python3 -I -B /tmp/r20-revexec-probe-00nny1q2/revexec.py run --root /tmp/r20-revexec-probe-00nny1q2/fixture-repo --rev 2b4a8f5a3b1ff9a7536472948158c61f26cc2f69 --entry probe.py -- scratch /fast/scratch/revexec-probe-616eac7e6ada4f40bcaa8736f982b12c
  SCRATCH_WRITE_REFUSED errno=30; host marker absent
python3 -I -B /tmp/r20-revexec-probe-00nny1q2/revexec.py run --root /tmp/r20-revexec-probe-00nny1q2/fixture-repo --rev 2b4a8f5a3b1ff9a7536472948158c61f26cc2f69 --entry probe.py -- tcp 44919
  TCP_CONNECT_REFUSED errno=111; a host listener on 127.0.0.1:44919 accepted no connection
python3 -I -B /tmp/r20-revexec-probe-00nny1q2/revexec.py run --root /tmp/r20-revexec-probe-00nny1q2/fixture-repo --rev 2b4a8f5a3b1ff9a7536472948158c61f26cc2f69 --entry probe.py -- bus
  BUS_CONNECT_REFUSED errno=13 (PermissionError) for /run/user/1000/bus; no data sent
python3 -I -B /tmp/r20-revexec-probe-00nny1q2/revexec.py run --root /tmp/r20-revexec-probe-00nny1q2/fixture-repo --rev 2b4a8f5a3b1ff9a7536472948158c61f26cc2f69 --entry probe.py -- ssh
  SSH_NAMES_REFUSED errno=2 (default HOME is the workspace; no ~/.ssh there)
python3 -I -B /tmp/r20-revexec-probe-00nny1q2/revexec.py run --root /tmp/r20-revexec-probe-00nny1q2/fixture-repo --rev 2b4a8f5a3b1ff9a7536472948158c61f26cc2f69 --entry probe.py --host-home -- ssh
  SSH_NAMES_LISTED count=4; enumerated basenames only, no file contents read or retained
```
After runs, the unique host-home marker, host `/tmp` marker, and `/fast/scratch` marker were all absent. The fixture payload only attempted writes, TCP connect, AF_UNIX connect (closed without sending), and `os.listdir(~/.ssh)`; it did not read file contents.

Evidence/anchors at S: `revexec.py:137-160` configures `PrivateNetwork=yes`, `ProtectSystem=strict`, `ProtectHome=read-only`, the sole `ReadWritePaths=workdir`, `PrivateTmp=yes`, `InaccessiblePaths=/run/user`, and switches only `HOME` for `--host-home`; `:178-197` creates the workdir under the configured base and removes it in `finally`. The stated residual trust includes same-UID execution at `:11-15`. The D6b expected contract is `contract.md:58-61`.

Severity / exploit path / impact: No integrity or network bypass observed for these probes. Conditional confidentiality risk (inference, not tested): an untrusted payload run with `--host-home` executes as the same UID and can read host-home files permitted to that UID; `ProtectHome=read-only` prevents writes, not reads. The observed four `.ssh` basenames confirm that the option exposes that directory’s listing. A malicious payload could disclose readable contents through its output; no secret content was accessed. Smallest mitigation: do not combine `--host-home` with untrusted revisions; where host checks are needed, provide only the specific sanitized read-only inputs required.