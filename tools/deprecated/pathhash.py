def _rotl64(x: int, b: int) -> int:
    return ((x << b) | (x >> (64 - b))) & 0xFFFFFFFFFFFFFFFF

def siphash24(data: bytes, key: bytes = b"\x00" * 16) -> int:
    if len(key) != 16:
        raise ValueError("key must be 16 bytes")
    k0 = int.from_bytes(key[:8], "little")
    k1 = int.from_bytes(key[8:], "little")

    v0 = 0x736f6d6570736575 ^ k0
    v1 = 0x646f72616e646f6d ^ k1
    v2 = 0x6c7967656e657261 ^ k0
    v3 = 0x7465646279746573 ^ k1

    def sipround():
        nonlocal v0, v1, v2, v3
        v0 = (v0 + v1) & 0xFFFFFFFFFFFFFFFF
        v1 = _rotl64(v1, 13) ^ v0
        v0 = _rotl64(v0, 32)
        v2 = (v2 + v3) & 0xFFFFFFFFFFFFFFFF
        v3 = _rotl64(v3, 16) ^ v2
        v0 = (v0 + v3) & 0xFFFFFFFFFFFFFFFF
        v3 = _rotl64(v3, 21) ^ v0
        v2 = (v2 + v1) & 0xFFFFFFFFFFFFFFFF
        v1 = _rotl64(v1, 17) ^ v2
        v2 = _rotl64(v2, 32)
        
    i = 0
    n = len(data)
    while i + 8 <= n:
        m = int.from_bytes(data[i:i+8], "little")
        v3 ^= m
        sipround(); sipround()
        v0 ^= m
        i += 8

    b = (n & 0xff) << 56
    rem = n - i
    tail = data[i:] + b"\x00" * (8 - rem)
    for j in range(rem):
        b |= tail[j] << (8 * j)

    v3 ^= b
    sipround(); sipround()
    v0 ^= b

    v2 ^= 0xFF
    for _ in range(4): sipround()

    out = (v0 ^ v1 ^ v2 ^ v3) & 0xFFFFFFFFFFFFFFFF
    return out

def byteswap64(x: int) -> int:
    return int.from_bytes(x.to_bytes(8, "little")[::-1], "little")

_SUFFIX_W = "xp3hnp"
_KEY_128  = b"\x00" * 16

def _utf16le_no_bom(s: str) -> bytes:
    return s.encode("utf-16le")

def get_path_hash(path: str) -> int:
    if path == "/":
        data = _utf16le_no_bom(_SUFFIX_W)
        h = siphash24(data, _KEY_128)
        return byteswap64(h)

    data = _utf16le_no_bom(path + _SUFFIX_W)
    h = siphash24(data, _KEY_128)
    return byteswap64(h)

if __name__ == "__main__":
    tests = ["/", "xp3hnp", "/"]
    for t in tests:
        hv = get_path_hash(t)
        print(f"{t!r} -> {hv:016x}")
