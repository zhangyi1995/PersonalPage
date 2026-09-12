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
| `archetypes/chapter-note.md` | 读书笔记章节的模板：`hugo new content blog/<slug>.md --kind chapter-note` |
| `docs/reading-protocol.md` | 读书笔记的写作协议，取自《如何阅读一本书》，写笔记前先读 |
| `tools/env.sh` | 项目内工具链环境，用 `source tools/env.sh` 激活 |
| `bin/build.sh` | 统一构建入口：校验 Hugo 版本，不匹配就下载 Extended 二进制 |
| `docs/sessions/` | 会话与决策的原始记录，按 `YYYY-MM-DD-主题.md` 命名 |

## 硬性规则

- 正文标题必须写显式锚点：`## 小节标题 {#section-id}`。中文与英文对页使用**相同的锚点 ID**，只翻译可见标题。
- 中文文件为 `<slug>.md`，英文对页为 `<slug>.en.md`，两者放在同一目录、保持同一文件名主干。
- Front matter 必填：`title`、`date`、`description`；建议填 `tags` 或 `categories`。`cover` 留空表示不使用封面图。
- 站内链接写不带前导斜杠的相对路径（如 `blog/why-oink/`），主题会补当前语言前缀。
- 首页分区类型只能取 OINK 注册表里的名字；写错会在构建期报 `unknown section type`。
- 不要删除或改写 `hugo.yaml` 中的三项 Goldmark 设置、`outputs`、`module.imports` 与 `hugoVersion`：OINK 的原生组件、Agent 输出与版本锁定都依赖它们。
- 不要提交 `tools/`、`public/`、`resources/`、`.hugo_cache/`：前两者是本地工具链，后两者是构建产物。

## 系列与读书笔记

- 系列标识符用 ASCII，中文显示名写在术语页的 `title` 里：`series: [mythical-man-month]` + `content/series/mythical-man-month/_index.md` 的 `title`。中文标识符会产出百分号编码 URL，不要用。
- 文件名带系列前缀并与权重对齐：`mythical-man-month-01-tar-pit.md` 对应 `series_weight: 10`。步长 10，为跨章插篇预留（插在第 3、5 章之间就写 35）。
- 读书笔记的分类法写法固定为 `categories: [读书笔记]` + `tags: [人月神话]`。术语按字面匹配，`读书笔记` 必须每次写全，写成"读书"会另开一个类目页。
- 系列页的阅读顺序只认 `series_weight`；文件名前缀管的是文件系统的肉眼顺序，两者要保持一致。
- 日期一律写当天或更早：Hugo 默认不构建未来日期的内容，写明天等于这篇文章不存在。
- 「我读《人月神话》」系列为**中文单语，英文首页有意不设入口**。主题会为首页卡片链接强制补语言前缀，英文侧指向中文系列页必然是死链；补英文版时再对称加上。
- 读书笔记一律按 `docs/reading-protocol.md` 的四节结构与短引规则写，不要跳过节一直接下判断。

## 常用命令

```bash
source tools/env.sh          # 激活项目内 hugo 与 go
hugo server                  # 本地预览，毫秒级热重载
hugo new content blog/<slug>.md

# 发布门禁：零警告退出。CI 与 Cloudflare 走同一个脚本，Hugo 版本只在脚本里定义
STRICT=1 bash bin/build.sh
```

## 工作记忆

- 每次涉及结构、选型或取舍的改动，先在 `content/blog/` 写一篇说明 Why 的文章，再改代码或配置。
- 会话与盘问的原始记录写在 `docs/sessions/`，文件名用 `YYYY-MM-DD-主题.md`；本文档只留稳定约定与索引，细节不往这里堆。
- 临时探索、试错过程与结论记在仓库内的文档里，不要只留在会话或聊天记录中。
- 本文件只放稳定约定；一次性的判断写在对应文章里。

## 身份信息与占位值

仓库：`https://github.com/zhangyi1995/PersonalPage`（已写入 `params.github_repo`、项目页与首页项目卡片）。

仍为占位、需要本人确认后再改：站点名与署名 `zhangyi1995`（`hugo.yaml` 的 `title` 与 `params.copyright.authors`、各语言首页 `title`、`data/home/*.yaml` 的 `eyebrow`）、公开邮箱 `you@example.com`（`content/about/`）、`baseURL`（绑定自定义域名后同步）。
