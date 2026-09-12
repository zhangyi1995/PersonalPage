# personal-site

个人主页：中英双语、纯静态，用 [Hugo](https://gohugo.io/) 加 [OINK](https://oink.pgsty.com/zh/) 主题构建。

- 中文在根路径 `/`，英文在 `/en/`
- 每页同时产出 HTML、Markdown、打印视图；站点根另有 `llms.txt` 与 RSS
- 构建只需要 `hugo` 与 Go 模块解析，不需要 Node、npm 或 CDN

站点方案与分析见 [PLAN.md](PLAN.md)。

## 本地预览

```bash
source tools/env.sh   # 把项目内的 hugo 与 go 加进 PATH
hugo server
```

打开 <http://localhost:1313/>。首次运行会通过 Go 模块代理下载 OINK v1.0.0，之后走本地缓存。

## 发布前自检

```bash
STRICT=1 bash bin/build.sh
```

`STRICT=1` 让任何警告都中断构建，这是发布门禁；CI 跑的是同一条命令。不带 `STRICT` 就是普通构建。

`bin/build.sh` 自己保证 Hugo 版本：先看 PATH 里现有的 Hugo 是否为 `0.166.0+extended`，不是就下载官方 Extended 二进制。版本只在这一个脚本里定义。

## 写作

```bash
hugo new content blog/my-first-post.md
```

中文文件名不带语言后缀，英文对页用 `.en.md`，两者标题锚点必须一致。约定详见 [AGENTS.md](AGENTS.md)。

## 身份信息

仓库地址 `https://github.com/zhangyi1995/PersonalPage` 已写入站点：仓库链接、编辑此页、项目页与首页项目卡片都已指向它。

仍待替换的占位值：

| 占位值 | 位置 | 说明 |
| --- | --- | --- |
| `zhangyi1995` | `hugo.yaml` 的 `title`、各语言首页 `title`、`params.copyright.authors`、`data/home/*.yaml` 的 `eyebrow` | 站点名与署名，用 GitHub 用户名占位 |
| `you@example.com` | `content/about/index.md`、`content/about/index.en.md` | 公开邮箱，按需填写 |
| `https://personalpage-dvh.pages.dev/` | `hugo.yaml` 的 `baseURL` | `pages.dev` 子域全局唯一，`personalpage` 已被占用故加 `-dvh` 后缀；绑定自定义域名后同步修改 |

## 部署

发布由 **Cloudflare Pages 的 Git 集成**完成：Cloudflare 监听 `main`，自己构建并发布。仓库里的 `.github/workflows/build.yaml` 只做严格构建检查，不参与发布。

Cloudflare 项目的构建设置：

| 项 | 值 |
| --- | --- |
| Build command | `bash bin/build.sh` |
| Build output directory | `public` |
| Root directory | 留空 |
| 环境变量 | `HUGO_VERSION=0.166.0` |
| 环境变量 | `GO_VERSION=1.27.1` |

构建命令交给 `bin/build.sh` 是有原因的：Cloudflare 镜像预装的 Hugo 是 0.147.7，低于 OINK 要求的 0.160.1，实测会在解析主题的 `i18n/bg.yaml` 时报错；而环境变量 `HUGO_VERSION` 在这套构建系统上并不生效（同时设的 `GO_VERSION` 也被忽略，Go 是靠自身工具链下载机制救回来的）。脚本改为显式下载官方 Extended 二进制来固定版本，不依赖镜像内容。那两个环境变量可以留着不用，删掉也行。

### 备用发布通道：Direct Upload

`.github/workflows/cloudflare-pages.yaml` 是备用方案：在 GitHub Actions 里用固定版本的工具链构建后直传 Cloudflare，适合 Cloudflare 侧构建不可用时切换。它默认不触发，启用方式是在仓库里配置：

- Secrets：`CLOUDFLARE_ACCOUNT_ID`、`CLOUDFLARE_API_TOKEN`（权限 `Account · Cloudflare Pages · Edit`）
- Repository variable：`CLOUDFLARE_PROJECT_NAME=personalpage`（必须小写，不用则退回仓库名 `PersonalPage`）
- Repository variable：`CLOUDFLARE_PAGES_ENABLED=true`（总开关，不设则工作流不运行）
- Repository variable：`CLOUDFLARE_SITE_URL=https://personalpage-dvh.pages.dev/`（绑定自定义域名后用它覆盖）

两条通道同时开启会导致同一次推送重复部署，切换时记得关掉另一条。
