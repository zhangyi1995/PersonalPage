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

## 身份信息

仓库地址 `https://github.com/zhangyi1995/PersonalPage` 已写入站点：仓库链接、编辑此页、项目页与首页项目卡片都已指向它。

仍待替换的占位值：

| 占位值 | 位置 | 说明 |
| --- | --- | --- |
| `zhangyi1995` | `hugo.yaml` 的 `title`、各语言首页 `title`、`params.copyright.authors`、`data/home/*.yaml` 的 `eyebrow` | 站点名与署名，用 GitHub 用户名占位 |
| `you@example.com` | `content/about/index.md`、`content/about/index.en.md` | 公开邮箱，按需填写 |
| `https://personalpage.pages.dev/` | `hugo.yaml` 的 `baseURL` | 绑定自定义域名后需同步修改，或改用仓库变量 `CLOUDFLARE_SITE_URL` 覆盖 |

## 部署

推送到 `main` 后由 `.github/workflows/cloudflare-pages.yaml` 构建并直传 Cloudflare Pages。需要在仓库中配置：

- Secrets：`CLOUDFLARE_ACCOUNT_ID`、`CLOUDFLARE_API_TOKEN`（权限 Pages:Edit）
- Repository variable：`CLOUDFLARE_PROJECT_NAME=personalpage`（Cloudflare 项目名必须小写；不设置会退回仓库名 `PersonalPage`，可能被拒）
- Repository variable：`CLOUDFLARE_PAGES_ENABLED=true`（开启自动部署的开关）
- Repository variable：`CLOUDFLARE_SITE_URL=https://personalpage.pages.dev/`（可选，绑定自定义域名后用这个覆盖）
