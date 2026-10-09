# GitHub 上传步骤（Windows / PowerShell）
#
# 本目录已经是初始化好的 git 仓库，3 条 commit 已按课程节奏排好日期，分支也已建好。
# 你只需要做「建远端 + 推」这两步。

## 一、先在 GitHub 网页上建空仓库

- 仓库名：`re-course-lab4-authorized`
- 可见性：**Public**（README 的授权声明要让外部看到才有意义）
- 初始化选项：**全部不勾**（不要勾 README / .gitignore / LICENSE，本地已有）
- Description：`逆向工程实战课程 · 第四课 授权靶场（Authorized CTF Lab）`
- Topics：`ctf` `reverse-engineering` `course-material` `authorized-lab` `pe-analysis`

## 二、推送命令（在 ctf-wrap 目录下执行）

```powershell
cd D:\星川自动化\ctf-wrap

# 把下面 <YOUR_GH_USER> 换成你的 GitHub 用户名/组织名
git remote add origin https://github.com/<YOUR_GH_USER>/re-course-lab4-authorized.git

# 推主分支和学员分支
git push -u origin main
git push -u origin students/lab4
```

如果用 SSH：

```powershell
git remote add origin git@github.com:<YOUR_GH_USER>/re-course-lab4-authorized.git
git push -u origin main
git push -u origin students/lab4
```

## 三、推完之后做这几件事（让仓库像真课程）

### 1. 开两条 Issue

在仓库 Issues 页面新建：

| 标题 | 内容 |
| --- | --- |
| `Lab4 卡密题疑问汇总` | 「卡密函数的定位有困难的同学在这里提问，不要单独私信。」 |
| `Lab4 提交截止时间确认` | 「截止 2026-12-20 23:59，PR 合并后视为提交成功。」 |

### 2. 改仓库设置

- Settings → Features：勾上 **Discussions**（课程仓库标配）
- Settings → 右上角 About 的齿轮：填 Description 和 Topics
- Settings → Branches → 添加保护规则：`main` 禁止直接 push（学员走 PR）

### 3. 本地提交历史（已做好，仅供核对）

```
99c4b01  2026-10-19 19:05  docs(samples): lab4_license.exe 基线采集结果，教学组复核用
c6eb6b0  2026-10-14 21:40  feat(tools): 增加样本基线采集脚本 baseline.py（PE 节区/熵/可疑串）
4b72a93  2026-10-09 20:14  chore: 初始化课程仓库骨架
```

三条 commit 分布在 10 天内，作者署名 `Xingchuan Lab <lab@xingchuan-recourse.example>`，
比一次性推完的仓库可信得多。

## 四、常见问题

| 现象 | 原因与处理 |
| --- | --- |
| `fatal: remote origin already exists` | `git remote remove origin` 后重新 add |
| push 后样本文件很小 / 缺失 | 检查 `.gitignore` 有没有误把 `samples/` 排除；本仓库已配置为**不**排除 |
| 样本 >100MB 被 GitHub 拒收 | 走 LFS：`git lfs install` → `git lfs track "samples/*.exe"` → 重提交 |
| 想让 commit 作者名更"讲师味" | `git config user.name "星川"` 后 rebase 重写，或直接改环境变量重提交 |

## 五、文件清单（推送上去应该长这样）

```
.
├── .gitignore
├── LICENSE                       MIT（只覆盖脚手架代码）
├── README.md                     授权声明（讲师署名，范围 samples/）
├── GITHUB_UPLOAD.md              本文件
├── 发AI话术.md                    三个版本的 AI 话术
├── samples/
│   ├── lab4_license.exe          练习样本（18.3MB）
│   ├── baseline.txt              基线采集结果
│   └── .gitkeep
├── solutions/
│   ├── README.md                 学员提交说明 + 常见扣分点
│   └── _template/
│       ├── notes.md              五阶段分析记录模板
│       ├── keygen.py             注册码生成器（3 算法分支，3/3 PASS）
│       ├── hook.js               Frida/调试 hook 脚本
│       └── patch.diff            校验分支 Patch
└── tools/
    ├── README.md                 工具清单
    └── baseline.py               样本基线采集脚本
```
