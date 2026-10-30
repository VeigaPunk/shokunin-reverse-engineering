# Prior carrier table wiring

Draft constant block: `priors.json`. Values are transcribed from the round-50 carrier manifest; JSON Pointer fragments below are relative to `tools/round-50/carriers.json`.

| Carrier | Prior pin SHA-256 | External image SHA-256 | Member / member SHA-256 | Oracle table | Nonregular table |
|---|---|---|---|---|---|
| g7581 | `/carriers/0/sha256` | `/carriers/0/external/image_sha256` | `/carriers/0/external/member`, `/carriers/0/external/member_sha256` | `/carriers/0/oracle` | `/carriers/0/nonregular` |
| g7582 | `/carriers/1/sha256` | `/carriers/1/external/image_sha256` | `/carriers/1/external/member`, `/carriers/1/external/member_sha256` | `/carriers/1/oracle` | `/carriers/1/nonregular` |
| c6490 | `/carriers/2/sha256` | `/carriers/2/external/image_sha256` | `/carriers/2/external/member`, `/carriers/2/external/member_sha256` | `/carriers/2/oracle` | `/carriers/2/nonregular` |
| c6430 | `/carriers/3/sha256` | `/carriers/3/external/image_sha256` | `/carriers/3/external/member`, `/carriers/3/external/member_sha256` | `/carriers/3/oracle` | `/carriers/3/nonregular` |

`re_scored_pins` contains exactly these four IDs. Oracle and nonregular values in `priors.json` are repository-relative paths. The URL values are documented in the source manifest but intentionally not copied into the constant block; the requested wiring block is limited to pins, source pointers, and prior table paths.

## Retained path check

The eight table paths were checked against commit `ab0eafedc41402b43b41a4362084119578dfe7ce` using `git cat-file -e <commit>:<path>`; all returned exit 0. Receipt:

- Exact command: `python -c 'import subprocess,json,hashlib,datetime,pathlib; root="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; base="ab0eafedc41402b43b41a4362084119578dfe7ce"; d=json.load(open(root+"/tools/round-50/carriers.json")); carriers=d["carriers"]; selected=[x for x in carriers if x["id"] in {"g7581","g7582","c6490","c6430"}]; paths=[p for x in selected for p in (x["oracle"],x["nonregular"])]; results=[(p,subprocess.run(["git","-C",root,"cat-file","-e",base+":"+p],capture_output=True).returncode) for p in paths]; out="\\n".join(f"{p} {rc}" for p,rc in results)+"\\n"; print("COMMAND=python -c <path-validation-script>"); print("EXIT_CODE="+("0" if all(rc==0 for _,rc in results) else "1")); print("STDOUT_BEGIN"); print(out,end=""); print("STDOUT_END"); print("STDOUT_SHA256="+hashlib.sha256(out.encode()).hexdigest()); print("UTC="+datetime.datetime.now(datetime.timezone.utc).isoformat()); raise SystemExit(0 if all(rc==0 for _,rc in results) else 1)'`
- Exit code: `0`
- Stdout (exact):
  `tools/round-50/oracle/g7581.oracle.tsv 0`  
  `tools/round-50/oracle/g7581.nonregular.tsv 0`  
  `tools/round-50/oracle/g7582.oracle.tsv 0`  
  `tools/round-50/oracle/g7582.nonregular.tsv 0`  
  `tools/round-50/oracle/c6490.oracle.tsv 0`  
  `tools/round-50/oracle/c6490.nonregular.tsv 0`  
  `tools/round-50/oracle/c6430.oracle.tsv 0`  
  `tools/round-50/oracle/c6430.nonregular.tsv 0`
- Stdout SHA-256: `63cb8340544fa0a3970a58301443ac41be9a001b9e8241302f8d12f0bb2c25ce`
- UTC: `2026-10-30T10:45:58.560979+00:00`

This check validates table-path presence only, not table contents or pin correctness beyond transcription from the manifest. No vendor download, REA run, or other check was performed.
