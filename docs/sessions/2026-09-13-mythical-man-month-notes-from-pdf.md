# 会话记录：《人月神话》读书笔记生成（2026-09-13）

## 任务

以 `/mnt/virtual_share/SyncVault/personal-vault/_assets/20-Learning/人月神话_40周年纪念版.pdf` 为源书，参考《如何阅读一本书》的方法，生成读书笔记并部署到站点。

## 现状

- 共享文件夹已挂载：`UbuntuShare on /mnt/virtual_share type vboxsf (rw,nodev,relatime)`，说明增强功能包已安装成功。
- 源书文件存在，但读取被拒：挂载点权限为 `drwxrwx--- root vboxsf`，当前用户 `zhangyi` 不在 `vboxsf` 组。
- 解除方式（二选一）：
  1. `sudo usermod -aG vboxsf $USER` 后重新登录，或当前会话执行 `newgrp vboxsf`；
  2. 不动权限，改由宿主机把 PDF 推送进虚拟机：`scp "D:\UbuntuShare\SyncVault\personal-vault\_assets\20-Learning\人月神话_40周年纪念版.pdf" zhangyi@192.168.56.101:~/`
- 取文工具：`pdftotext`、`pdfinfo` 已安装；无 OCR（若 PDF 是扫描件需另想办法）。

## 待办

1. 取得 PDF 读取权限，用 `pdftotext` 或 `pdfinfo` 确认这一版的真实章节结构（40 周年纪念版可能与 20 周年版的 19 章 + 尾声不同）。
2. 按 `docs/reading-protocol.md` 逐章生成笔记，替换 `content/blog/` 下第一章、第二章的草稿骨架。
3. 去掉 `draft: true`、校对日期，跑严格构建后提交推送。

## 进展（同日）

### 源书事实

- 书是**纯扫描件**：390 页，无字体、无文字层，每页是一张 2048×2870 的 300dpi JPEG，`pdftotext` 只能提出 20 字节。
- 版本信息取自版权页：清华大学出版社 2015 年 5 月第 1 版，译自 *The Mythical Man-Month: Essays on Software Engineering, Anniversary Edition*，ISBN 978-7-302-39264-4。
- 目录（OCR 自第 15–21 页）确认结构为 **19 章 + 第 1 版结束语 + 结束语**，另有中文版附录（名家谈人月、名著评人月、读者感言）：

| 章 | 标题 | 印刷页 | 章 | 标题 | 印刷页 |
| --- | --- | --- | --- | --- | --- |
| 1 | 焦油坑 | 1 | 11 | 未雨绸缪 | 113 |
| 2 | 人月神话 | 16 | 12 | 干将莫邪 | 125 |
| 3 | 外科手术队伍 | 27 | 13 | 整体部分 | 139 |
| 4 | 贵族专制、民主政治和系统设计 | 39 | 14 | 祸起萧墙 | 153 |
| 5 | 画蛇添足 | 51 | 15 | 另外一面 | 165 |
| 6 | 贯彻执行 | 59 | 16 | 没有银弹 | 181 |
| 7 | 为什么巴比伦塔会失败 | 71 | 17 | 再论"没有银弹" | 209 |
| 8 | 胸有成竹 | 85 | 18 | 《人月神话》的观点：是与非 | 231 |
| 9 | 削足适履 | 95 | 19 | 20 年后的《人月神话》 | 257 |
| 10 | 提纲挈领 | 105 | 结束语 | 令人向往、激动人心和充满乐趣的 50 年 | 293 |

### 工具与方法

- 新增 `bin/ocr-pdf.py`：把扫描版 PDF 指定页范围渲染后 OCR 成文本，供后续写作引用原文。依赖 poppler 的 `pdftoppm` 与 `pip install --user rapidocr-onnxruntime`。
- 页面对应关系：**PDF 页码 = 印刷页码 + 21**（第 1 章标题页为 PDF 第 22 页）。
- OCR 全文只存 `/tmp/mmm_txt/`，**不入库**，避免把受版权保护的正文提交进仓库。
- 后台任务要用 `setsid nohup` 启动；仅用 `nohup ... &` 会被会话回收。

### 已完成

- 第 1 章《焦油坑》、第 2 章《人月神话》两篇笔记已按 `docs/reading-protocol.md` 的四节结构写完，并解除草稿状态。
