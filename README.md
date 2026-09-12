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
hugo --cleanDestinationDir --gc --minify --environment production \
  --printPathWarnings --panicOnWarning
```

任何警告都会中断构建，这是发布门禁；CI 跑的是同一条命令。

## 写作

```bash
hugo new content blog/my-first-post.md
```

中文文件名不带语言后缀，英文对页用 `.en.md`，两者标题锚点必须一致。约定详见 [AGENTS.md](AGENTS.md)。

## 上线前的替换清单

| 占位值 | 位置 |
| --- | --- |
| `Site Name` | `hugo.yaml` 的 `title`（YAML 锚点，一处改动覆盖所有语言） |
| `https://example.pages.dev/` | `hugo.yaml` 的 `baseURL` |
| `Your Name`、`you@example.com` | `content/about/`、`hugo.yaml` 的 `params.copyright` |
| `OWNER`、`OWNER/REPO` | `content/about/`、`content/projects/`、`data/home/*.yaml`，以及 `hugo.yaml` 里注释掉的 `params.github_repo` |

## 部署

推送到 `main` 后由 `.github/workflows/cloudflare-pages.yaml` 构建并直传 Cloudflare Pages。需要在仓库中配置：

- Secrets：`CLOUDFLARE_ACCOUNT_ID`、`CLOUDFLARE_API_TOKEN`（权限 Pages:Edit）
- Repository variable：`CLOUDFLARE_PROJECT_NAME`（可选，缺省用仓库名）
- Repository variable：`CLOUDFLARE_PAGES_ENABLED=true`（开启自动部署的开关）
- Repository variable：`CLOUDFLARE_SITE_URL`（可选，缺省按 `<项目名>.pages.dev` 生成）
