"""
Lab4 样本基线采集脚本（课程工具）
用法: python baseline.py samples/lab4_license.exe

采集项：文件大小、MD5/SHA256、PE 头、节区表、熵值、可疑字符串
产出：直接粘进 solutions/<学号>/notes.md 的「0. 样本基线」段
"""

import argparse
import hashlib
import math
import os
import struct
import sys

SUSPECT_PATTERNS = [
    b"license", b"licence", b"activate", b"activation", b"serial",
    b"registr", b"invalid key", b"trial", b"expire", b"unlock",
    b"keygen", b"crack", b"check_key", b"verify_key",
]


def file_hashes(path: str):
    md5 = hashlib.md5()
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            md5.update(chunk)
            sha.update(chunk)
    return md5.hexdigest(), sha.hexdigest()


def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    n = len(data)
    return -sum((c / n) * math.log2(c / n) for c in counts if c)


def parse_pe(path: str):
    """极简 PE 解析：机器类型、时间戳、节区表。"""
    with open(path, "rb") as f:
        data = f.read()
    if data[:2] != b"MZ":
        return None
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    if data[e_lfanew:e_lfanew + 4] != b"PE\0\0":
        return None
    coff = e_lfanew + 4
    machine, nsect, timestamps = struct.unpack_from("<HHI", data, coff)
    opt_size = struct.unpack_from("<H", data, coff + 16)[0]
    opt = coff + 20
    magic = struct.unpack_from("<H", data, opt)[0]
    pe32p = (magic == 0x20B)

    arch = {0x8664: "x64", 0x14C: "x86", 0xAA64: "arm64"}.get(machine, hex(machine))
    sections = []
    sec_off = opt + opt_size
    for i in range(nsect):
        off = sec_off + i * 40
        name = data[off:off + 8].rstrip(b"\0").decode("latin1", "replace")
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", data, off + 8)
        if rawsize:
            sec_ent = entropy(data[rawptr:rawptr + rawsize])
        else:
            sec_ent = 0.0
        sections.append({
            "name": name, "vaddr": vaddr, "vsize": vsize,
            "rawsize": rawsize, "rawptr": rawptr, "entropy": sec_ent,
        })
    return {
        "arch": arch, "bits": 64 if pe32p else 32,
        "timestamp": timestamps, "sections": sections,
    }


def suspected_strings(path: str, limit: int = 40):
    hits = []
    with open(path, "rb") as f:
        blob = f.read()
    low = blob.lower()
    for pat in SUSPECT_PATTERNS:
        start = 0
        while True:
            idx = low.find(pat, start)
            if idx < 0:
                break
            hits.append((idx, pat.decode()))
            start = idx + 1
            if len(hits) >= limit:
                return hits
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("sample")
    args = ap.parse_args()
    p = args.sample
    if not os.path.isfile(p):
        print(f"[!] not found: {p}")
        return 1

    size = os.path.getsize(p)
    md5, sha = file_hashes(p)
    with open(p, "rb") as f:
        head = f.read(64)
    overall_ent = entropy(open(p, "rb").read())

    print("## 0. 样本基线\n")
    print(f"| 文件名 | {os.path.basename(p)} |")
    print("| --- | --- |")
    print(f"| 大小 | {size} bytes |")
    print(f"| MD5 | {md5} |")
    print(f"| SHA256 | {sha} |")
    print(f"| 魔数 | {head[:2].decode('latin1')} |")
    print(f"| 整文件熵 | {overall_ent:.3f} |")

    pe = parse_pe(p)
    if pe:
        print(f"| 架构 | {pe['arch']} / {pe['bits']}bit |")
        print(f"| 节区数 | {len(pe['sections'])} |")
        print("\n### 节区表\n")
        print("| 节区 | 虚拟地址 | 原始大小 | 熵 |")
        print("| --- | --- | --- | --- |")
        for s in pe["sections"]:
            flag = " ⚠高熵" if s["entropy"] > 7.0 else ""
            print(f"| {s['name']} | 0x{s['vaddr']:X} | {s['rawsize']} | {s['entropy']:.3f}{flag} |")

    hits = suspected_strings(p)
    print(f"\n### 可疑字符串（命中 {len(hits)} 处）\n")
    for off, word in hits[:20]:
        print(f"- 偏移 0x{off:X}: `{word}`")
    return 0


if __name__ == "__main__":
    sys.exit(main())
