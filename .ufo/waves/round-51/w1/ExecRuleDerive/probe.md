# Synthetic unprivileged device-node probe

Executed as uid 1000 (`vgpnk`), unsquashfs 4.7.5. No REA run.

First attempted command used `-p "$S/pseudo"` (a file containing `devnode c 1 3 0 0`); mksquashfs returned 1 and reported “Not enough or invalid arguments in pseudo file definition” followed by the accepted pseudo-entry syntax. This was a malformed attempt, not evidence about extraction.

Successful image build command:
`mksquashfs "$S/src" "$S/probe.sqfs" -noappend -quiet -p 'devnode c 600 1000 1000 1 3' -no-xattrs`
Exit 0; stderr empty (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). Image SHA-256: `d111309795a5f4e005627bc2f014707de426f43c013f33b2f8c06d2bb3710b9a`. The source also held `regular.txt` and symlink `link -> regular.txt`.

Extraction command:
`/usr/bin/unsquashfs -d "$S/out" "$S/probe.sqfs"`
Exit 2. stdout SHA-256 `dbb1afcd2074675f8cf7c4d17a77d808d3b004fc3747e6afced51c14ce8704c3`; observed output included `created 1 file`, `created 1 directory`, `created 1 symlink`, `created 0 devices`, `created 0 fifos`, `created 0 sockets`. stderr SHA-256 `06cdf16b1b37a492e115aa444b9ce0735c19d26b3287771677b30a81a916b452`; exact device warning: `create_inode: could not create character device /fast/scratch/hyaku/kaidoku-r51/w1-ExecRuleDerive/out/devnode, because you're not superuser!`

Observed extracted tree: directory root, regular file `regular.txt`, symlink `link -> regular.txt`; no `devnode` exists. This directly supports the unprivileged unsquashfs mknod premise. UTC capture: `2026-10-30T04:58:34Z` (hash and filesystem observation). Image/probe files remained only in scratch during capture; no vendor bytes involved.
