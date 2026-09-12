# AGENTS.md — 这个站点的约定

面向所有在本仓库工作的 Agent 与协作者。改动站点前先读完本页。

## 站点事实

- 形态：Hugo Extended 0.166.0 + OINK v1.0.0（Hugo Module，`go.mod`/`go.sum` 锁定），纯静态。
- 语言：`zh` 为默认语言（根路径 `/`），`en` 在 `/en/`，`fr` 仅声明不启用。
- 首页：`data/home/<语言>.yaml` 的 `sections` 列表，不是模板文件。
- 输出：每页 HTML + Markdown，栏目另有 RSS 与 print，站点根有 `llms.txt`。
- 工具链：全部在 `tools/` 内（`hugo`、`go`、模块缓存），不写入系统目录。

## 目录约定

| 路径 | 作用 |
| --- | --- |
| `content/blog/` | 文章主区，叶子文件直接放文章 |
| `content/about/` | 关于页，身份信息的唯一权威来源 |
| `content/projects/` | 项目与作品页 |
| `data/home/zh.yaml`、`data/home/en.yaml` | 首页分区数据，两种语言结构保持一致 |
| `archetypes/default.md` | `hugo new content blog/<slug>.md` 的模板 |
| `tools/env.sh` | 项目内工具链环境，用 `source tools/env.sh` 激活 |

## 硬性规则

- 正文标题必须写显式锚点：`## 小节标题 {#section-id}`。中文与英文对页使用**相同的锚点 ID**，只翻译可见标题。
- 中文文件为 `<slug>.md`，英文对页为 `<slug>.en.md`，两者放在同一目录、保持同一文件名主干。
- Front matter 必填：`title`、`date`、`description`；建议填 `tags` 或 `categories`。`cover` 留空表示不使用封面图。
- 站内链接写不带前导斜杠的相对路径（如 `blog/why-oink/`），主题会补当前语言前缀。
- 首页分区类型只能取 OINK 注册表里的名字；写错会在构建期报 `unknown section type`。
- 不要删除或改写 `hugo.yaml` 中的三项 Goldmark 设置、`outputs`、`module.imports` 与 `hugoVersion`：OINK 的原生组件、Agent 输出与版本锁定都依赖它们。
- 不要提交 `tools/`、`public/`、`resources/`、`.hugo_cache/`：前两者是本地工具链，后两者是构建产物。

## 常用命令

```bash
source tools/env.sh          # 激活项目内 hugo 与 go
hugo server                  # 本地预览，毫秒级热重载
hugo new content blog/<slug>.md

# 发布门禁：零警告退出，CI 跑同一条命令
hugo --cleanDestinationDir --gc --minify --environment production \
  --printPathWarnings --panicOnWarning
```

## 工作记忆

- 每次涉及结构、选型或取舍的改动，先在 `content/blog/` 写一篇说明 Why 的文章，再改代码或配置。
- 临时探索、试错过程与结论记在仓库内的文档里，不要只留在会话或聊天记录中。
- 本文件只放稳定约定；一次性的判断写在对应文章里。

## 待替换的占位值

上线前必须替换：`Site Name`、`https://example.pages.dev/`、`Your Name`、`you@example.com`、`OWNER`、`OWNER/REPO`（含 `hugo.yaml` 中注释掉的 `params.github_repo`）。
