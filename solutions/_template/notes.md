# Lab4 分析记录 —— 学号 <STUDENT_ID>

> 交作业时按本模板填，每一条结论后面必须跟证据（文件+偏移 / 调试日志 / 反汇编片段）。
> "看起来对"不算还原，要能被 `keygen.py --self-test` 复现。

## 0. 样本基线

| 项目 | 值 |
| --- | --- |
| 文件名 | samples/lab4_license.exe |
| 大小 | 18349760 bytes |
| MD5 | 5d9028e659ed6b16214938df482fbb96 |
| SHA256 | cb58739fb8a75dadb770d8dea8d3fd083067b6b4b84a09851540313b88645fc0 |
| 魔数 | MZ（PE） |
| 架构 | x86 / 32bit |
| 节区数 | 5 |
| 整文件熵 | 8.000 |
| 是否有壳 | `<是/否>` → 依据：`<DIE / 节区熵 / 导入表体积>` |

> 以上基线由 `python tools/baseline.py samples/lab4_license.exe` 自动生成，
> 完整输出见 `samples/baseline.txt`。

## ① 静态基线

**Windows / PE 路线**

```
# 查壳 / 编译器
diec samples/lab4_license.exe
# 节区 + 可疑字符串
python tools/baseline.py samples/lab4_license.exe
# 反汇编（任选其一）
ghidraRun                     # GUI 导入后跑 auto-analysis
r2 -A samples/lab4_license.exe
```

已知节区（基线阶段实测）：

| 节区 | 虚拟地址 | 原始大小 | 熵 |
| --- | --- | --- | --- |
| .text | 0x1000 | 26624 | 6.454 |
| .rdata | 0x8000 | 5120 | 5.100 |
| .data | 0xA000 | 1536 | 4.123 |
| .ndata | 0x2A000 | 0 | 0.000 |
| .rsrc | 0x58000 | 18432 | 5.877 |

- 可疑字符串：偏移 `0x7E30` 命中 `unlock`
- 候选校验函数：`<地址 0x?????? + 函数名 / 符号>`

**Android 路线（样本若为 apk）**

```
apktool d samples/lab4_license.apk -o out_apk
jadx -d out_jadx samples/lab4_license.apk
```

- dex 清单：`<classes.dex, classes2.dex, ...>`
- 候选校验类：`<com.xxx.LicenseManager>`

## ② 保护识别

| 检查项 | 命令 | 结果 |
| --- | --- | --- |
| 查壳 | `diec samples/lab4_license.exe` | `<无 / UPX / VMProtect>` |
| 节区熵 | `python tools/baseline.py` | `.text 6.454`（<7.0，提示未加壳） |
| 导入表体积 | `r2 -q -c "ii"` | `<函数数>` |
| 反调试 | `r2 -q -c "/x 6489" ./lab4_license.exe`（查 fs:30 访问） | `<有/无>` |
| 完整性校验 | `<签名自校验位置>` | `<结论>` |

结论：`<一句话>`

## ③ 动态调试

x64dbg 附加，断在 `<0x??????>`（校验分支）：

```
<粘贴 x64dbg 日志：输入明文 / 比较值 / 跳转是否被取 / 时间戳>
```

若走 Frida（Android 分支），脚本见同目录 `hook.js`：

```javascript
Java.perform(function () {
  var C = Java.use("com.xxx.LicenseManager");
  C.check.implementation = function (key) {
    console.log("[in ] key = " + key);
    var r = this.check(key);
    console.log("[out] ret = " + r);
    return r;
  };
});
```

实际抓到的日志：

```
<粘贴 frida / x64dbg 输出：输入明文 / 返回值 / 时间戳>
```

## ④ 脱壳 / 解混淆

（若 ② 判定无壳，写"样本未加固，无需脱壳"并附 ② 的证据）

```
产物路径：out_dump/unpacked.exe
产物 SHA256：<HASH>
修复项：IAT / 重定位 / 节区对齐
验证：Ghidra 能正常反编译 ✔
```

## ⑤ 算法还原

**定位**：`<函数地址 0x??????>` @ 文件偏移 `<0x????>`

**逻辑**：
1. 输入卡密被 `<转大写 / 去横线 / 拆分>`；
2. 逐字符与常量表 `CONST_TABLE`（位于 `<.rdata 0x????>`）做 `<运算>`；
3. 结果与 `<魔数>` 比较，相等则进入已注册分支。

**反汇编片段**：

```asm
; 关键 5-10 条指令，标出比较与跳转
```

**还原实现**：见同目录 `keygen.py` 的 `algo_<'a'|'b'|'c'>()`

**自测**：

```
$ python keygen.py --self-test
=== 3/3 PASS ===
```

## ⑥ （可选）Patch 记录

见同目录 `patch.diff`，或文件偏移级 Patch：

| 文件偏移 | 原始字节 | 替换字节 | 说明 |
| --- | --- | --- | --- |
| `0x????` | `<原>` | `<新>` | `<跳过校验>` |

验证方式：

```
# Android
apktool b out_apk -o patched.apk
# Windows：改完直接跑，输入任意卡密 → 进入已注册界面 ✔
```
