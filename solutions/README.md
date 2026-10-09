# Lab4 学员作业提交说明

## 提交方式

1. Fork 本仓库到自己的账号；
2. 在 `solutions/` 下新建目录，命名为你的学号：
   ```
   solutions/RC2026F-0917/
   ```
3. 把 `_template/` 里的四个文件拷进去，填完；
4. 发 Pull Request 到 `main` 分支，标题格式：`[Lab4] <学号> 提交`。

## 必交文件

| 文件 | 内容 | 是否必需 |
| --- | --- | --- |
| `notes.md` | 五阶段分析记录，每条结论带证据 | 必需 |
| `keygen.py` | 能跑的注册码生成器，`--self-test` 全 PASS | 必需 |
| `hook.js` | Frida hook 脚本，附真实抓到的日志 | 必需 |
| `patch.diff` | 校验分支 Patch | 可选（加分） |

## 常见扣分点

- **只写结论不写证据**：说"校验在 LicenseManager.check"，但没贴反编译片段和偏移 → 该条不计分
- **keygen 不能跑**：`python keygen.py --self-test` 报错或 FAIL → ⑤ 阶段清零
- **hook 日志是编的**：日志里没有时间戳、没有调用栈、与样本行为对不上 → ③ 阶段清零
- **直接抄别人的 patch.diff**：`.locals` 没跟着改，回编译后 VerifyError → 按未提交算

## 截止与答疑

- 截止：`2026-12-20 23:59`
- 答疑：在本仓库开 Issue，标签 `lab4`
- 教研组邮箱：lab@xingchuan-recourse.example
