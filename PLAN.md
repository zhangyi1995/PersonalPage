# 个人主页搭建计划：基于 OINK (Hugo) 的中英双语技术站

- 生成日期：2026-09-12
- 状态：待实施（本文档只记录分析与方案，站点骨架尚未创建）
- 站点目录：`~/Proj/personal-site`
- 固定版本事实：Hugo Extended 0.166.0（主题下限 0.160.1）、Go 1.27.1、OINK v1.0.0（2026-08-29 发布）

下一步：执行第 3 节「实施方案」，先装项目内工具链并从 OINK Starter 拉出骨架，再替换身份信息上线第一版。

---

## 1. 参考分析

### 1.1 vonng.com/ai/sdd —— 文档驱动的方法论

这篇文章（《文档驱动：AI 软件工程的第一秘籍》）回答的是"AI 写得快，如何保证不是屎山"，核心是四条实践：文档驱动、对抗审查、暴力测试、复杂度惩罚，其中展开的是第一条。

关键论点：

| 论点 | 含义 |
| --- | --- |
| 文档是输入而非补记 | 以前文档是代码写完后的补充；现在文档首先是写代码之前的输入、开发过程中的工作记忆、交付时的验收标准 |
| 许愿要落到 PRD | 中型项目值得花半天到一个上午生成并审阅 PRD；你可以不读代码，但不能不读需求文档 |
| Agent 是失忆的天才 | 它只有代码、测试、文档三样东西可依靠，缺了部落知识（Tribal Knowledge）就会把被否掉的方案重新实现一遍 |
| 工作记忆分两层 | 底层按时间或议题完整保存原始记录，上层定期总结成索引写进 `AGENTS.md`，两层缺一不可 |
| 验收不可外包 | 单元测试可以交给 Agent 自测，验收测试必须人工签字；交付物里必须包含与代码同等质量的使用手册 |
| 质量成本在后期 | 追求工程质量时，70%–80% 的 token 应花在 QC 与测试上，而不是写代码上 |
| 每个项目配一个伴生文档站 | 文档是交付物的一部分，第一天就该写好并用像样的方式管理 |

对本站的启示：个人主页不只是"展示面"，它本身就是这份"伴生文档站"——技术文章的 Why、项目决策记录、架构取舍都沉淀在同一个内容源里，人和 Agent 读的是同一份 Markdown。

### 1.2 oink.pgsty.com/zh —— 框架能力面

OINK 是作者为落地上述方法论而做的 Hugo 主题（基于 Google Docsy 大幅定制与融合），本站页面兼作手册、设计参考、组件画廊与回归样本，当前版本 v1.0.0。

| 能力 | 说明 |
| --- | --- |
| 引入方式 | Hugo Module（`module.imports` + `go.mod`/`go.sum` 固定版本），一次解析后用一个 `hugo` 二进制构建；也可 submodule、离线归档、克隆 |
| 依赖 | 站点侧不需要 Node.js、npm、PostCSS、打包器与 CDN；字体、图标、搜索、图表运行时随主题分发 |
| Markdown 原生组件 | 提示块、图片属性、代码块标题、标签页、表格、参数表、步骤、卡片、文件树、公式、Mermaid、ECharts、画廊、徽章、按键、Asciinema，全部用原生 Markdown 语法与属性行表达，不引入 MDX |
| 阅读外壳 | Docs、Blog、Book、Swagger/Redoc、发布页、下载页、打印 |
| 多语言 | 语言路由、译文对页、界面文案、中文分词搜索均内置 |
| Agent 输出 | 每页额外产出 `.md`，站点根产出 `llms.txt` 与 `navigation.json`，人和 Agent 共用一份源 |
| 首页 | 不是模板而是数据：`data/home/<语言>.yaml` 的 `sections` 决定页面分区，共 22 种分区类型（`hero`、`cards`、`capabilities`、`timeline`、`faq`、`cta`、`download` 等） |
| 部署 | GitHub Pages 与 Cloudflare Pages 的自动 CI/CD |
| 许可 | 主题 Apache-2.0；随主题分发的第三方运行时各自保留原许可 |

### 1.3 关键事实：vonng.com 本身就是一个 OINK 个人站

`vonng.com` 的源码仓库公开（`github.com/Vonng/vonng.com`），构型可以直接照搬：

- 根路径 `/` 是数据驱动的落地页，顶层一级目录（数据库、云计算、PG、AI、行万里路、人生旅途）各自是一条博客专栏，每列自带卡片索引、Hero 与标签体系。
- 站点级品牌定制集中在两个 SCSS 入口：`assets/scss/_variables_project.scss` 与 `assets/scss/_styles_project.scss`。
- 该站启用的可选能力包括 giscus 评论、Google Analytics、`offline_search`、`quick_links`、`page_context_menu`、`reading_time`、`image_zoom`，可作为后续扩展的对照清单。
- 版权边界：站点内容为 CC BY 4.0，只参考结构与排版，不复制其正文文字。

---

## 2. 决策记录

| 决策项 | 选择 | 理由 |
| --- | --- | --- |
| 站点定位 | 技术博客为主 | 首页落地页 + 博客专栏 + 关于页 + 项目页，最贴近 vonng.com 的做法，写作即更新 |
| 语言 | 中英双语 | 用 Starter 自带 bilingual profile 一次配好；后期再加语言需手工合并配置 |
| 部署 | Cloudflare Pages | 零成本零运维、免备案、推送即自动发布；国内速度一般但可接受 |
| 构建环境 | 项目内自带二进制 | Hugo 与 Go 解压到 `tools/`，不污染系统、不需要 root，本地可即时预览 |
| 存量内容 | 从零写 | 无旧博客需要迁移，直接按 OINK 的目录约定新建 |
| 外部集成 | 暂不开评论与统计 | 搜索、`llms.txt`、每页 `.md` 均为主题内置，不需外部账号；评论与统计留注释块，随时开启 |
| 默认语言 | 中文在根路径，英文在 `/en/` | 中文读者与搜索引擎优先；若日后要改为英文在根，需调整 `defaultContentLanguage` 并整体对调文件后缀，属机械替换但必须在写内容之前决定 |

补充决定：站点骨架的字段占位值（站点名、域名、作者名、仓库名）在实施时一次性替换，见第 6 节。

---

## 3. 实施方案

目标形态：一个根路径为中文、`/en/` 为英文的双语静态站，站点根附带 `sitemap.xml`、`robots.txt`、`llms.txt` 与 RSS，每个页面额外产出可被 Agent 直接读取的 `.md`。

```text
https://<你的域名>/
├── /                     中文首页（数据驱动落地页）
├── /blog/                中文文章列表（卡片索引 + 年份/标签）
├── /blog/<slug>/         文章页（附加 <slug>/index.md 供 Agent 读取）
├── /about/               关于我
├── /projects/            作品与项目
├── /tags/ /categories/   横切索引
└── /en/ ...              英文站点（结构与中文镜像，通过语言切换器互跳）
```

### 3.1 工具链与骨架（全部本地化，免 root）

- 下载 `hugo_extended_0.166.0_linux-amd64.tar.gz` 与 `go1.27.1.linux-amd64.tar.gz`，分别解压到 `<site>/tools/hugo` 与 `<site>/tools/go`。
- 写 `tools/env.sh`：把 `PATH` 指向上述两个目录，同时把 `GOPATH`、`GOMODCACHE`、`HUGO_CACHEDIR` 一并指到 `tools/` 下，保证构建状态不落到用户主目录。

```bash
source tools/env.sh
hugo version   # 期望输出 extended 0.166.0
go version     # 期望输出 go1.27.1
```

- 以 `pgsty/oink-starter` 为起点初始化站点仓库（模板或直接克隆），确认 `go.mod` 与 `go.sum` 中固定 `github.com/pgsty/oink v1.0.0`，两者都要提交。
- 提交前确认仓库根不含构建产物：`public/`、`resources/`、`.hugo_build.lock` 与模块缓存均在忽略清单内。

### 3.2 双语配置裁剪

- 用 `examples/hugo.bilingual.yaml` 覆盖根 `hugo.yaml`，然后做三处修改：`defaultContentLanguage: zh`、`disableLanguages: [fr]`、用 YAML 锚点把 `title` 收敛成一处定义。
- 删除 `i18n/fr.yaml`；中文界面文案由主题自带的 32 份语言文件覆盖，无需自建。
- 文件后缀随之确定：中文为无后缀 `.md`，英文为 `.en.md`，首页根分别为 `content/_index.md` 与 `content/_index.en.md`。
- 必须完整保留：三项 Goldmark 前置（`renderer.unsafe`、`parser.attribute.block`、`parser.wrapStandAloneImageWithinParagraph`）、`outputs`（含 `markdown`、`LLMS`、`print`）、`module.imports` 与 `module.hugoVersion`。

```yaml
markup:
  goldmark:
    renderer:
      unsafe: true
    parser:
      attribute:
        block: true
      wrapStandAloneImageWithinParagraph: false
  highlight:
    noClasses: false

outputs:
  home: [HTML, RSS, markdown, LLMS]
  page: [HTML, markdown]
  section: [HTML, RSS, print, markdown]
```

### 3.3 内容结构

删除 starter 的示例 `content/docs/`、`content/book/` 与示例文章，只保留三个表面：

| 路径 | 作用 | 维护方式 |
| --- | --- | --- |
| `content/blog/` | 文章主区 | 叶子文件直接放文章，`tags`/`categories` 做横切索引；日后要分专栏，新建一级目录即可自动获得栏目首页与侧栏，主题无需改动 |
| `content/about/` | 关于我 | 单页，含自我介绍、社交链接与联系方式 |
| `content/projects/` | 作品与项目 | 用 `{.cards}` 链接列表手工维护，首页从中挑精选 |

- 重写 `archetypes/default.md`，让 `hugo new content blog/<slug>.md` 自带 `title`、`date`、`description`、`tags`、`categories`、`cover` 字段。
- 中文页面标题一律手写显式锚点 `{#id}`，英文对页沿用相同锚点，保证双语目录与锚点链接对齐。

### 3.4 首页五分区

`data/home/zh.yaml` 与 `data/home/en.yaml` 的 `sections` 固定为：

```yaml
sections:
  - hero
  - type: cards
    key: featured
  - type: cards
    key: columns
  - type: cards
    key: projects
  - cta
```

| 分区 | 内容 |
| --- | --- |
| `hero` | 一句定位语（`eyebrow`）、分行的主标题（`title_lines`）、`lead` 简介、头像或跟随深浅色的配图、两个按钮（读博客 / 关于我） |
| `cards` / `featured` | 精选文章 3–6 篇，手挑，指向具体文章 |
| `cards` / `columns` | 专栏与主题导航，指向 `blog` 的标签或分类 |
| `cards` / `projects` | 代表作与开源项目，指向 `/projects/` 或外部仓库 |
| `cta` | 联系方式与订阅入口 |

- 所有卡片数据写在同一份 YAML 内联，不使用浏览器端取数；`content/_index.md` 只保留 `title` 与 `description`。
- 站内链接写成不带前导斜杠的相对路径（如 `blog/`），主题会自动补当前语言前缀。
- 分区类型写错不会静默消失，构建期会报 `unknown section type`；CI 的 `--panicOnWarning` 会把它变成失败。

### 3.5 品牌、Agent 输出与写作工作流

- 替换 `assets/icons/logo.svg` 与 `static/favicon.svg`；主色、字体、深浅色只改 `assets/scss/_variables_project.scss` 与 `assets/scss/_styles_project.scss` 两个入口。
- 保留 `offline_search: true`（含中文分词）、`ui.dark_mode`、`image_zoom`、`backlinks`、`keyboard_nav`。
- 在仓库根写 `AGENTS.md`：记录目录约定、锚点规则、发布流程与"每个决策留一份 Why"的写作规约，落实 1.1 节的工作记忆两层结构。
- 站点自带 `llms.txt` 与每页 `index.md`，个人主页同时成为人和 Agent 都能直接读的知识库。

### 3.6 部署流水线

- 保留 `.github/workflows/cloudflare-pages.yaml`（严格构建 + Direct Upload），删除 `.github/workflows/github-pages.yaml` 避免每次推送重复构建。
- 仓库设置：Secrets 填 `CLOUDFLARE_ACCOUNT_ID`、`CLOUDFLARE_API_TOKEN`（权限 Pages:Edit）；Repository variable 填 `CLOUDFLARE_PROJECT_NAME`。
- 首次部署前必须把 `baseURL` 改成真实地址（`https://<project>.pages.dev` 或已绑定的自定义域名），否则 canonical、hreflang 与 sitemap 全部指向错误地址。
- 保留工作流中的 `fetch-depth: 0` 与配置里的 `enableGitInfo: true`，页面"最后修改时间"依赖完整 git 历史。

```bash
# 上线前的本地等效构建
hugo --cleanDestinationDir --gc --minify --environment production \
  --printPathWarnings --panicOnWarning
```

---

## 4. 接口与约定

| 项目 | 约定 |
| --- | --- |
| URL | `/`（中文首页）、`/en/`（英文首页）、`/blog/<slug>/`、`/en/blog/<slug>/`、`/tags/<tag>/`、`/categories/<cat>/`；每页附加 `<页面路径>/index.md`，站根附加 `/llms.txt`、`/sitemap.xml` |
| Front matter | `title`、`linkTitle`、`description`、`date`、`weight`、`tags`、`categories`、`cover`；正文各级标题带显式 `{#id}` 锚点 |
| 首页数据契约 | `data/home/<语言>.yaml` 只有两层：`sections` 列表与被列表引用的同名键；分区条目支持 `type`、`key`、`data`、`id`、`enabled`、`partial` |
| 目录与导航 | `content/` 一级目录即栏目，目录结构与 `weight` 共同决定侧栏与翻页顺序；顶部导航来自栏目根 `_index` 的 `menus.main`，译文根保持相同 `identifier` 与 `weight`，只翻译可见标签 |
| 译文对齐 | 中文 `foo.md` 对应英文 `foo.en.md`；两边的 `identifier`、`weight` 与标题锚点必须一致 |
| 可选集成 | giscus 评论与统计在 `hugo.yaml` 中留有注释块，填好 repo/repoId/categoryId 或测量 ID 后取消注释即可，不需要改模板 |

---

## 5. 测试与验收

| 阶段 | 检查项 |
| --- | --- |
| 本地预览 | `hugo server` 下逐项确认：中文根路径与 `/en/` 双向语言切换、暗色模式、中文关键词搜索、键盘快捷键、首页五个分区的渲染与深浅色配图切换、移动端与窄屏布局 |
| 构建门禁 | `hugo --cleanDestinationDir --gc --minify --environment production --printPathWarnings --panicOnWarning` 必须零警告退出 |
| 产物断言 | `public/index.html`、`public/en/index.html`、`public/llms.txt`、`public/sitemap.xml`、`public/robots.txt`、`public/blog/<slug>/index.md`、RSS 均存在 |
| 双语一致性 | 中英页面 hreflang 互指；标题锚点一一对应；导航标签只翻译不改变 `identifier` 与 `weight` |
| 链接与回归 | `--printPathWarnings` 无内链断裂；删除示例栏目后确认首页卡片与顶部导航不再指向已删路径 |
| 上线验收 | Cloudflare 预览 URL 打开正常 → 绑定自定义域名与 HTTPS → 404 页 → 移动端抽查 → 推送一次确认 CI 自动发布成功 |

验收标准：上述六项全部通过，且严格构建零警告，即为第一版可交付。

---

## 6. 假设与默认选择

- 站点目录为 `~/Proj/personal-site`，本次只落地本文档，目录中不创建 git 仓库、`.gitignore` 与 `hugo.yaml`。
- 身份信息先用占位值，实施时按下列位置一次替换：

| 占位值 | 替换位置 |
| --- | --- |
| `Site Name` | `hugo.yaml` 的 `title`（YAML 锚点，一处改动覆盖所有语言）与各语言 `title` |
| `https://example.pages.dev` | `hugo.yaml` 的 `baseURL` |
| 站点描述 | 各语言 `params.description` |
| `Your Name` 与社交链接 | 各语言 `params.copyright`、`content/about/index.md`、页脚 |
| `OWNER/REPO` | `hugo.yaml` 的 `params.github_repo`、`params.github_branch`（用于"编辑此页""查看历史"与 issue 链接） |
| `personal-site` | Cloudflare Pages 项目名与仓库变量 `CLOUDFLARE_PROJECT_NAME` |

- 暂不接 giscus 与 Google Analytics；日后若需统计，建议改用 Umami 等自托管方案以规避国内采集不稳。
- Cloudflare Pages 免备案；若后续要求国内高速访问，只需修改 CI 的上传目标迁到阿里云 OSS + CDN（需 ICP 备案），站点产物与内容无需任何改动。
- 本文档位于仓库根、不在 `content/` 下，`hugo` 构建不会把它当作页面内容。
- 版权边界：OINK 主题为 Apache-2.0，可直接使用并保留 `LICENSE` 与 `NOTICE`；vonng.com 的正文内容为 CC BY 4.0，只参考结构与排版，不复制其文字。
- 本文档为中文单语版本；若后续需要英文版计划，另建 `PLAN.en.md`。

---

## 7. 参考链接

| 资源 | 地址 |
| --- | --- |
| 文档驱动方法论原文 | <https://vonng.com/ai/sdd/> |
| OINK 主题站点与文档 | <https://oink.pgsty.com/zh/> |
| OINK 主题仓库 | <https://github.com/pgsty/oink> |
| OINK Starter 脚手架 | <https://github.com/pgsty/oink-starter> |
| vonng.com 个人站源码 | <https://github.com/Vonng/vonng.com> |
| OINK 安装方式说明 | <https://oink.pgsty.com/zh/docs/start/from-scratch/> |
| OINK 首页与落地页 | <https://oink.pgsty.com/zh/docs/customize/home/> |
| Hugo 官方下载 | <https://github.com/gohugoio/hugo/releases> |
| Go 官方下载 | <https://go.dev/dl/> |
