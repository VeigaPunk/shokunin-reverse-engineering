cmd=bash -n /fast/scratch/hyaku/kaidoku-r52/w1-ExecRunsh/copy/c1-run.sh
exit=0
stdout_sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
utc=2026-10-30T10:47:31Z
stdout=
cmd=bash /fast/scratch/hyaku/kaidoku-r52/w1-ExecRunsh/copy/c1-run.sh oracle --id dryprobe --carrier /fast/scratch/hyaku/kaidoku-r52/w1-ExecRunsh/carrier.bin --outdir /fast/scratch/hyaku/kaidoku-r52/w1-ExecRunsh/out --scratch /fast/scratch/hyaku/kaidoku-r52/w1-ExecRunsh/kaidoku-r52 --dry-run
exit=0
stdout_sha256=b0664239f78385a4cf7632ba8c2b5a897ef515ddd036162e4b05fb3d6cf92d84
utc=2026-10-30T10:47:32Z
stdout=
c1-run.sh --dry-run: mode=oracle id=dryprobe
  carrier=/fast/scratch/hyaku/kaidoku-r52/w1-ExecRunsh/carrier.bin  pin=none
  outdir=/fast/scratch/hyaku/kaidoku-r52/w1-ExecRunsh/out  under_evidence=false  data_run=0 force=0
  scratch_base=/fast/scratch/hyaku/kaidoku-r52/w1-ExecRunsh/kaidoku-r52  prov_segment_ok=true  prefix_ok=true
  child_path=/usr/local/bin:/usr/bin:/bin:/home/vgpnk/.local/bin:/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/bin  override=false
  reader: python3 -I -- /fast/scratch/hyaku/kaidoku-r52/w1-ExecRunsh/copy/sqfs-list.py --layout auto|le --files … --nonregular … --inspect /fast/scratch/hyaku/kaidoku-r52/w1-ExecRunsh/carrier.bin
  unsquashfs: /usr/bin/unsquashfs -no-xattrs -f -no-exit-code -d <scratch>/usq/root /fast/scratch/hyaku/kaidoku-r52/w1-ExecRunsh/carrier.bin ; /usr/bin/unsquashfs -lln /fast/scratch/hyaku/kaidoku-r52/w1-ExecRunsh/carrier.bin
  sasquatch: sasquatch -le -f -no-exit-code -n -d <scratch>/sq/root /fast/scratch/hyaku/kaidoku-r52/w1-ExecRunsh/carrier.bin
dry-run_created_no_outdir=true
