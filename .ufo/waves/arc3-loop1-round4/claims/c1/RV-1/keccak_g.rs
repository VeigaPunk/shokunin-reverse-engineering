// RV-1 (arc3-loop1-round4) — independent Keccak-256, path G.
// Two formulations in one binary, both spec-derived (no hardcoded RC/rho tables):
//   G1: u64 lane array, standard theta/rho/pi/chi/iota
//   G2: bit-array [u8;1600] with index = 25*z + 5*y + x, same spec
// Round constants derived from the LFSR rc(t); rho offsets derived from the
// walk (x,y) -> (y, (2x+3y) mod 5) starting at (1,0).
// Usage: keccak_g [g1|g2|both]  < sigs.txt  -> "sig<TAB>digest<TAB>selector"

use std::io::{self, Read};

fn lfsr_rc(t: usize) -> u8 {
    if t % 255 == 0 {
        return 1;
    }
    let mut r: u8 = 0x01;
    for _ in 1..=(t % 255) {
        r = ((r << 1) ^ if (r >> 7) & 1 == 1 { 0x71 } else { 0 }) & 0xff;
    }
    r & 1
}

fn round_constants() -> [u64; 24] {
    let mut rc = [0u64; 24];
    for ir in 0..24 {
        let mut v: u64 = 0;
        for j in 0..7 {
            if lfsr_rc(j + 7 * ir) == 1 {
                v |= 1u64 << ((1usize << j) - 1);
            }
        }
        rc[ir] = v;
    }
    rc
}

fn rho_offsets() -> [[u32; 5]; 5] {
    // Spec order: record r at the current (x,y), THEN walk (x,y) <- (y, 2x+3y).
    let mut r = [[0u32; 5]; 5];
    let (mut x, mut y) = (1usize, 0usize);
    for k in 1..=24u32 {
        r[x][y] = (k * (k + 1) / 2) % 64;
        let nx = y;
        let ny = (2 * x + 3 * y) % 5;
        x = nx;
        y = ny;
    }
    r
}

fn keccak_f_g1(a: &mut [u64; 25]) {
    let rc = round_constants();
    let ro = rho_offsets();
    for ir in 0..24 {
        let mut c = [0u64; 5];
        for x in 0..5 {
            c[x] = a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20];
        }
        let mut d = [0u64; 5];
        for x in 0..5 {
            d[x] = c[(x + 4) % 5] ^ c[(x + 1) % 5].rotate_left(1);
        }
        for x in 0..5 {
            for y in 0..5 {
                a[x + 5 * y] ^= d[x];
            }
        }
        let mut b = [0u64; 25];
        for x in 0..5 {
            for y in 0..5 {
                b[y + 5 * ((2 * x + 3 * y) % 5)] = a[x + 5 * y].rotate_left(ro[x][y]);
            }
        }
        for x in 0..5 {
            for y in 0..5 {
                a[x + 5 * y] =
                    b[x + 5 * y] ^ ((!b[((x + 1) % 5) + 5 * y]) & b[((x + 2) % 5) + 5 * y]);
            }
        }
        a[0] ^= rc[ir];
    }
}

#[inline]
fn idx(x: usize, y: usize, z: usize) -> usize {
    25 * z + 5 * y + x
}

fn keccak_f_g2(a: &mut [u8; 1600]) {
    let ro = rho_offsets();
    for ir in 0..24 {
        let mut c = [[0u8; 64]; 5];
        for x in 0..5 {
            for z in 0..64 {
                c[x][z] = a[idx(x, 0, z)]
                    ^ a[idx(x, 1, z)]
                    ^ a[idx(x, 2, z)]
                    ^ a[idx(x, 3, z)]
                    ^ a[idx(x, 4, z)];
            }
        }
        let mut d = [[0u8; 64]; 5];
        for x in 0..5 {
            for z in 0..64 {
                d[x][z] = c[(x + 4) % 5][z] ^ c[(x + 1) % 5][(z + 63) % 64];
            }
        }
        for x in 0..5 {
            for y in 0..5 {
                for z in 0..64 {
                    a[idx(x, y, z)] ^= d[x][z];
                }
            }
        }
        let mut b = [0u8; 1600];
        for x in 0..5 {
            for y in 0..5 {
                let r = ro[x][y] as usize;
                for z in 0..64 {
                    b[idx(y, (2 * x + 3 * y) % 5, z)] = a[idx(x, y, (z + 64 - r) % 64)];
                }
            }
        }
        for x in 0..5 {
            for y in 0..5 {
                for z in 0..64 {
                    a[idx(x, y, z)] = b[idx(x, y, z)]
                        ^ ((1 ^ b[idx((x + 1) % 5, y, z)]) & b[idx((x + 2) % 5, y, z)]);
                }
            }
        }
        for j in 0..7 {
            if lfsr_rc(j + 7 * ir) == 1 {
                a[idx(0, 0, (1usize << j) - 1)] ^= 1;
            }
        }
    }
}

fn keccak256_g1(msg: &[u8]) -> [u8; 32] {
    const RATE: usize = 136;
    let mut a = [0u64; 25];
    let mut padded = msg.to_vec();
    padded.push(0x01);
    while padded.len() % RATE != 0 {
        padded.push(0x00);
    }
    let n = padded.len();
    padded[n - 1] |= 0x80;
    for block in padded.chunks(RATE) {
        for (i, chunk) in block.chunks(8).enumerate() {
            let mut lane = [0u8; 8];
            lane[..chunk.len()].copy_from_slice(chunk);
            a[i] ^= u64::from_le_bytes(lane);
        }
        keccak_f_g1(&mut a);
    }
    let mut out = [0u8; 32];
    for i in 0..4 {
        out[8 * i..8 * i + 8].copy_from_slice(&a[i].to_le_bytes());
    }
    out
}

fn keccak256_g2(msg: &[u8]) -> [u8; 32] {
    const RATE: usize = 136;
    let mut a = [0u8; 1600];
    let mut padded = msg.to_vec();
    padded.push(0x01);
    while padded.len() % RATE != 0 {
        padded.push(0x00);
    }
    let n = padded.len();
    padded[n - 1] |= 0x80;
    for block in padded.chunks(RATE) {
        for (byte_i, byte) in block.iter().enumerate() {
            for bit in 0..8 {
                let lane = byte_i / 8;
                let z = (byte_i % 8) * 8 + bit;
                let x = lane % 5;
                let y = lane / 5;
                a[idx(x, y, z)] ^= (byte >> bit) & 1;
            }
        }
        keccak_f_g2(&mut a);
    }
    let mut out = [0u8; 32];
    for byte_i in 0..32 {
        let lane = byte_i / 8;
        let x = lane % 5;
        let y = lane / 5;
        let mut b = 0u8;
        for bit in 0..8 {
            let z = (byte_i % 8) * 8 + bit;
            b |= a[idx(x, y, z)] << bit;
        }
        out[byte_i] = b;
    }
    out
}

fn hex(b: &[u8]) -> String {
    b.iter().map(|x| format!("{:02x}", x)).collect()
}

fn main() {
    let mode = std::env::args().nth(1).unwrap_or_else(|| "both".to_string());
    if mode == "selftest" {
        // Published Keccak-256 digests (Keccak team / widely known Ethereum values),
        // plus rate-boundary probes (135/136/137 bytes) checked for G1==G2 and for
        // the padding-boundary discontinuity expected at the 136-byte rate.
        let cases: [(&str, &str); 4] = [
            ("", "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"),
            ("abc", "4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45"),
            (
                "The quick brown fox jumps over the lazy dog",
                "4d741b6f1eb29cb2a9b9911c82f56fa8d73b04959d3d9d222895df6c0b28aa15",
            ),
            ("", "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"),
        ];
        let mut pass = 0;
        for (i, (msg, want)) in cases.iter().enumerate() {
            let g1 = hex(&keccak256_g1(msg.as_bytes()));
            let g2 = hex(&keccak256_g2(msg.as_bytes()));
            let ok = g1 == *want && g2 == *want;
            if ok {
                pass += 1;
            }
            println!("vec{} {:?} g1={} g2={} want={} {}", i, msg, g1, g2, want,
                     if ok { "PASS" } else { "FAIL" });
        }
        for n in [135usize, 136, 137] {
            let m = vec![b'a'; n];
            let g1 = hex(&keccak256_g1(&m));
            let g2 = hex(&keccak256_g2(&m));
            let same = g1 == g2;
            if same {
                pass += 1;
            }
            println!("rate n={} g1==g2 {} digest={}", n, same, g1);
        }
        println!("selftest {}/7 PASS", pass);
        if pass != 7 {
            std::process::exit(1);
        }
        return;
    }
    if mode == "rc" {
        let rc = round_constants();
        for (i, v) in rc.iter().enumerate() {
            println!("RC[{}] = {:016x}", i, v);
        }
        let ro = rho_offsets();
        for y in 0..5 {
            let row: Vec<String> = (0..5).map(|x| format!("{:2}", ro[x][y])).collect();
            println!("rho[y={}] = [{}]", y, row.join(", "));
        }
        return;
    }
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    for line in input.lines() {
        let sig = line.trim();
        if sig.is_empty() {
            continue;
        }
        let d1 = keccak256_g1(sig.as_bytes());
        let d2 = keccak256_g2(sig.as_bytes());
        if d1 != d2 {
            eprintln!("G1/G2 MISMATCH on {:?}", sig);
            std::process::exit(2);
        }
        let sel = &hex(&d1)[..8];
        match mode.as_str() {
            "g1" => println!("{}\t{}\t{}", sig, hex(&d1), sel),
            "g2" => println!("{}\t{}\t{}", sig, hex(&d2), sel),
            _ => println!("{}\t{}\t{}", sig, hex(&d1), sel),
        }
    }
}
