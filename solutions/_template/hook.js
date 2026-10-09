# Lab4 Frida Hook 模板（solutions/_template/hook.js）

用途：不脱壳、不改包，运行时直接看 check 函数的输入与返回值。
用法：
```bash
adb shell su -c "/data/local/tmp/frida-server &"
frida -U -f <PACKAGE> -l hook.js --no-pause
```

```javascript
Java.perform(function () {
    var TAG = "[lab4]";

    // ── ① 枚举类，找疑似校验类（类名不确定时先跑这段） ──────────
    Java.enumerateLoadedClasses({
        onMatch: function (name) {
            if (/license|activ|regist|serial|key/i.test(name)) {
                console.log(TAG + " candidate class: " + name);
            }
        },
        onComplete: function () {}
    });

    // ── ② Hook 校验方法：抓输入、返回值、耗时 ────────────────────
    try {
        var LM = Java.use("com.xxx.LicenseManager");
        LM.check.implementation = function (key) {
            console.log(TAG + " [in ] key = " + key);
            var t0 = Date.now();
            var ret = this.check(key);
            console.log(TAG + " [out] ret = " + ret + "  (" + (Date.now() - t0) + "ms)");
            console.log(TAG + " [stk] " + Java.use("android.util.Log").getStackTraceString(
                Java.use("java.lang.Exception").$new()));
            return ret;
        };
    } catch (e) {
        console.log(TAG + " hook check failed: " + e);
    }

    // ── ③ 抓算法中间量：常量表 / 中间字符串 ──────────────────────
    try {
        var LM2 = Java.use("com.xxx.LicenseManager");
        LM2.compute.implementation = function (s) {
            var r = this.compute(s);
            console.log(TAG + " compute(" + s + ") = " + r);
            return r;
        };
    } catch (e) { /* 类名可能不同，忽略 */ }

    // ── ④ 绕过检测（若样本有 root/调试检测） ──────────────────────
    try {
        var Debug = Java.use("android.os.Debug");
        Debug.isDebuggerConnected.implementation = function () {
            console.log(TAG + " isDebuggerConnected() -> false (spoofed)");
            return false;
        };
    } catch (e) {}
});
```

## 说明

- **② 抓到的 `[in ]` / `[out]` 两行就是作业要求的"hook 日志"证据**，直接贴进 `notes.md` 的 ③ 段
- `[stk]` 调用栈用来确认是不是真的加载了这个包里的类（防止 hook 到同名混淆类）
- 若 ① 打印出多个候选类，逐个换 ② 的类名试
- 无壳样本用这套就够了；有壳先走 ④ 脱壳（BlackDex / FRIDA-DEXDump），拿到真实 dex 再回来 hook
