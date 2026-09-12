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
