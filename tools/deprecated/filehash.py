from typing import List

def rotr32(x: int, n: int) -> int:
    x &= 0xFFFFFFFF
    return ((x >> n) | ((x << (32 - n)) & 0xFFFFFFFF)) & 0xFFFFFFFF

def le32_load(b: bytes, i: int) -> int:
    return b[i] | (b[i+1] << 8) | (b[i+2] << 16) | (b[i+3] << 24)

IV = [
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
    0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
]

SIGMA = [
    [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15 ],
    [14,10, 4, 8, 9,15,13, 6, 1,12, 0, 2,11, 7, 5, 3 ],
    [11, 8,12, 0, 5, 2,15,13,10,14, 3, 6, 7, 1, 9, 4 ],
    [ 7, 9, 3, 1,13,12,11,14, 2, 6, 5,10, 4, 0,15, 8 ],
    [ 9, 0, 5, 7, 2, 4,10,15,14, 1,11,12, 6, 8, 3,13 ],
    [ 2,12, 6,10, 0,11, 8, 3, 4,13, 7, 5,15,14, 1, 9 ],
    [12, 5, 1,15,14,13, 4,10, 0, 7, 6, 3, 9, 2, 8,11 ],
    [13,11, 7,14,12, 1, 3, 9, 5, 0,15, 4, 8, 6, 2,10 ],
    [ 6,15,14, 9,11, 3, 0, 8,12, 2,13, 7, 1, 4,10, 5 ],
    [10, 2, 8, 4, 7, 6, 1, 5,15,11, 9,14, 3,12,13, 0 ],
]

def G(v: List[int], a: int, b: int, c: int, d: int, x: int, y: int) -> None:
    v[a] = (v[a] + v[b] + x) & 0xFFFFFFFF
    v[d] = rotr32(v[d] ^ v[a], 16)
    v[c] = (v[c] + v[d]) & 0xFFFFFFFF
    v[b] = rotr32(v[b] ^ v[c], 12)
    v[a] = (v[a] + v[b] + y) & 0xFFFFFFFF
    v[d] = rotr32(v[d] ^ v[a], 8)
    v[c] = (v[c] + v[d]) & 0xFFFFFFFF
    v[b] = rotr32(v[b] ^ v[c], 7)

def blake2s_compress(h: List[int], block: bytes, t0: int, t1: int, f0: int, f1: int) -> None:
    m = [le32_load(block, 4*i) for i in range(16)]

    v = [0]*16
    v[0:8] = h[0:8]
    v[8:16] = IV[0:8]
    v[12] ^= (t0 & 0xFFFFFFFF)
    v[13] ^= (t1 & 0xFFFFFFFF)
    v[14] ^= (f0 & 0xFFFFFFFF)
    v[15] ^= (f1 & 0xFFFFFFFF)

    for r in range(10):
        s = SIGMA[r]

        G(v, 0, 4, 8,12, m[s[0]], m[s[1]])
        G(v, 1, 5, 9,13, m[s[2]], m[s[3]])
        G(v, 2, 6,10,14, m[s[4]], m[s[5]])
        G(v, 3, 7,11,15, m[s[6]], m[s[7]])

        G(v, 0, 5,10,15, m[s[8]],  m[s[9]])
        G(v, 1, 6,11,12, m[s[10]], m[s[11]])
        G(v, 2, 7, 8,13, m[s[12]], m[s[13]])
        G(v, 3, 4, 9,14, m[s[14]], m[s[15]])

    for i in range(8):
        h[i] = (h[i] ^ v[i] ^ v[i+8]) & 0xFFFFFFFF

SUFFIX = "xp3hnp"

H0_INIT = [
    0x6B08E647, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
    0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
]

def get_filename_hash(path: str) -> str:
    data = (path + SUFFIX).encode("utf-16le")
    h = H0_INIT.copy()
    t0 = 0
    t1 = 0
    i = 0
    while i < len(data):
        take = min(64, len(data) - i)
        blk = data[i:i+take] + b"\x00"*(64 - take)
        t0 = (t0 + take) & 0xFFFFFFFF
        f0 = 0xFFFFFFFF if (i + take) == len(data) else 0
        f1 = 0
        blake2s_compress(h, blk, t0, t1, f0, f1)
        i += take
    out = b"".join((x & 0xFFFFFFFF).to_bytes(4, "little") for x in h)
    return out.hex()

if __name__ == "__main__":
    p = r"水８.ogg"
    digest = get_filename_hash(p)
    print("digest:", digest)
