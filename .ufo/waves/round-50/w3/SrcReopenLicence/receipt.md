# Receipt — S249 re-open fetch (SrcReopenLicence, R50 attempt-2 wave 3)

- URL: `https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/info_en.txt`
- UTC: 2026-10-29T20:33:15Z → 2026-10-29T20:33:16Z
- Command: `curl -sS -D headers-raw.txt -o info_en.txt -w '%{http_code} %{size_download} %{url_effective}' --max-time 60 https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/info_en.txt` (cwd = scratch `/fast/scratch/hyaku/kaidoku-r50/w3-SrcReopenLicence`)
- Exit code: 0
- curl `-w` stdout: `200 67591 https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/info_en.txt` (stdout sha256 `2667f16f8640e50db4664f792913caa4642be1ac70d4fa2ccc51214c15e5dafb`)
- Body bytes: 67,591 — body sha256 `6c601b342da91f7598dde1e7842ba92a61a1ec7f4b3d00564573fea3d11070a7` (**identical to attempt-1**, 2026-10-28)
- Response headers (Set-Cookie: none present): HTTP/1.1 200 OK, Server nginx, Date Thu 29 Oct 2026 20:33:16 GMT, Content-Type text/plain, Content-Length 67591, Last-Modified Mon 04 Sep 2023 17:07:50 GMT, ETag "64f60ee6-10807", Accept-Ranges bytes
- Anchor quote (18 words) located verbatim on **line 850**: "The licensee may create only one copy of the software, which may be used exclusively for backup use."
- Artifacts here: `info_en.txt` (served body, byte-exact), `headers.txt` (sanitized, no cookie headers)
- Encoding note: CRLF line endings (`\r\n`), 854 LF-terminated lines + final line 855 `HKR 2023-07-13.` without trailing newline.
