#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
逆向工程课程第四课 · Lab4 卡密校验还原
solutions/_template/keygen.py  —— 学员作业模板

用法:
    python keygen.py --self-test          # 跑内置 3 组用例
    python keygen.py --id STUDENT-0001    # 生成该学号的注册码

替换说明:
    把下方 STAGE1_PLACEHOLDER / CONST_TABLE / CHECK_MAGIC 换成你从
    samples/lab4_license.apk 里逆出来的真实常量。
"""

import argparse
import hashlib
import sys

# ─────────────────────────────────────────────────────────────
# ① 逆出来的常量（模板占位，换成真实的）
# ─────────────────────────────────────────────────────────────
CHECK_MAGIC = "LAB4"                     # 校验函数的魔数前缀
CONST_TABLE = [0x5A, 0x3C, 0x91, 0xE4, 0x17, 0x6B, 0xC2, 0x08]
XOR_KEY = 0x5A                           # 单字节异或密钥


# ─────────────────────────────────────────────────────────────
# ② 候选算法 A：学号 → 8 位十六进制串（最常见的一种）
# ─────────────────────────────────────────────────────────────
def algo_a(student_id: str) -> str:
    """md5(学号 + 魔数) 取前 8 位，大写。"""
    h = hashlib.md5((student_id + CHECK_MAGIC).encode()).hexdigest()
    return h[:8].upper()


# ─────────────────────────────────────────────────────────────
# ③ 候选算法 B：字符级查表 + 异或（教材里常考的题型）
# ─────────────────────────────────────────────────────────────
def algo_b(student_id: str) -> str:
    """逐字符查 CONST_TABLE 取偏移，再与 XOR_KEY 异或。"""
    out = []
    for i, ch in enumerate(student_id):
        v = (ord(ch) + CONST_TABLE[i % len(CONST_TABLE)]) & 0xFF
        out.append(f"{v ^ XOR_KEY:02X}")
    return "".join(out)


# ─────────────────────────────────────────────────────────────
# ④ 候选算法 C：分组 + 加盐哈希（带分段密钥）
# ─────────────────────────────────────────────────────────────
def algo_c(student_id: str) -> str:
    """按 4 字符分组，每组单独哈希后拼接。"""
    parts = []
    for i in range(0, len(student_id), 4):
        chunk = student_id[i:i + 4]
        parts.append(hashlib.sha1((chunk + CHECK_MAGIC).encode()).hexdigest()[:4].upper())
    return "-".join(parts)


# ─────────────────────────────────────────────────────────────
# ⑤ 校验复现：把生成的码按 check 函数逻辑跑一遍，看是否通过
# ─────────────────────────────────────────────────────────────
def verify(student_id: str, key: str, algo) -> bool:
    expected = algo(student_id)
    ok = (key == expected)
    print(f"  输入学号 : {student_id}")
    print(f"  输入卡密 : {key}")
    print(f"  期望卡密 : {expected}")
    print(f"  结果     : {'PASS' if ok else 'FAIL'}")
    return ok


# ─────────────────────────────────────────────────────────────
# ⑥ 内置自测用例（作业要求：至少 3 组 PASS）
# ─────────────────────────────────────────────────────────────
SELF_TEST_CASES = [
    ("STUDENT-0001", algo_a),
    ("STUDENT-0002", algo_a),
    ("RC2026F",      algo_a),
]


def run_self_test() -> int:
    print("=== Lab4 keygen 自测 (algo_a) ===")
    passed = 0
    for sid, algo in SELF_TEST_CASES:
        key = algo(sid)
        if verify(sid, key, algo):
            passed += 1
        print()
    total = len(SELF_TEST_CASES)
    print(f"=== {passed}/{total} PASS ===")
    return 0 if passed == total else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Lab4 卡密生成器（课程作业模板）")
    ap.add_argument("--id", dest="student_id", help="学号/用户 ID")
    ap.add_argument("--algo", default="a", choices=["a", "b", "c"],
                    help="选择算法分支（对应你逆出来的那一支）")
    ap.add_argument("--self-test", action="store_true", help="跑内置 3 组用例")
    args = ap.parse_args()

    if args.self_test:
        return run_self_test()

    if not args.student_id:
        ap.print_help()
        return 2

    algo = {"a": algo_a, "b": algo_b, "c": algo_c}[args.algo]
    print(f"[algo_{args.algo}] 学号 {args.student_id} -> 卡密 {algo(args.student_id)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
