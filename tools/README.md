# 课程推荐工具清单（Local Toolchain）

本课程所有练习均可在本地完成，无需任何线上服务授权。

## Android 侧

| 工具 | 用途 | 获取方式 |
| --- | --- | --- |
| apktool | 拆包/回编译，读 AndroidManifest 与 smali | 官方 release |
| jadx / jadx-gui | dex 反编译成 Java，找 check 函数首选 | 官方 release |
| dex2jar | dex → jar，配合 JD-GUI | 官方 release |
| baksmali / smali | 精细改 smali 后回编译 | 官方 release |
| frida + frida-server | 动态 hook，抓输入输出明文 | pip + 设备端 server |
| objection | frida 之上的探索层，一键绕 SSL pinning | pip |
| BlackDex / FRIDA-DEXDump | 脱壳（若样本带加固） | 开源项目 |
| radare2 | 无 GUI 环境下的静态分析 | 官方 release |

## 桌面侧

| 工具 | 用途 |
| --- | --- |
| Ghidra | 免费反编译，IDA 缺失时的主力 |
| IDA Free / Pro | 反汇编 + 交叉引用 |
| x64dbg | 用户态动态调试（Windows 样本） |
| DIE (Detect It Easy) | 查壳 / 查编译器 |
| upx -d | UPX 壳一键脱 |

## 环境建议

- 逆向台建议放在**隔离虚拟机**里跑：样本可能有反调试/反虚拟机逻辑，也要防真实恶意行为
- 工具路径统一登记到课程 `tools/README.md`，缺哪个补哪个
- 建议同时装 `python3`（写 keygen、写自动化脚本用）

## 必需环境变量（示例）

```
JADX_HOME       = D:\tools\jadx
APKTOOL_JAR     = D:\tools\apktool\apktool.jar
GHIDRA_HOME     = D:\tools\ghidra
FRIDA_SERVER    = /data/local/tmp/frida-server   (设备端)
```
