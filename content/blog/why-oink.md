---
title: 我为什么用 OINK 搭这个站
date: 2026-09-12
description: 选型、取舍与放弃的方案：静态站、Markdown 单一内容源、人和 Agent 共用一份材料。
tags: [建站, Hugo, 文档驱动]
categories: [工程]
cover: ''
---

这个站点是用来放技术笔记、项目记录与决策备忘的。开工第一件事不是选模板，而是想清楚它要承担什么：既要给读者看，也要能被 Agent 直接读取，还要在几年后仍然能改。

## 结论先给 {#decision}

用 Hugo + [OINK](https://oink.pgsty.com/zh/) 主题，纯静态构建、Markdown 单一内容源、Cloudflare Pages 托管。

理由有三条。

## 一、内容源只有一份 {#single-source}

OINK 的每一页都同时产出 HTML、Markdown、打印视图与 `llms.txt` 索引。人和 Agent 读到的是同一份源，不需要维护两套材料。

```yaml {title="hugo.yaml 中的输出格式"}
outputs:
  home: [HTML, RSS, markdown, LLMS]
  page: [HTML, markdown]
  section: [HTML, RSS, print, markdown]
```

## 二、正文就是 Markdown {#native-markdown}

提示块、标签页、步骤、参数表、文件树、图表都用原生 Markdown 语法加一行属性表达，源码本身仍然可读，不引入 MDX 或组件语法。

> [!NOTE]
> 写页面时不要引入只在渲染后才有意义的写法；下一个接手的人（或 Agent）读的是源文件。

## 三、构建链足够短 {#toolchain}

一个 `hugo` 二进制加 Go 模块解析，没有 Node、npm、打包器，也没有 CDN 依赖。本地预览是毫秒级热重载，发布交给 CI。

## 放弃的方案 {#alternatives}

| 方案 | 放弃原因 |
| --- | --- |
| 现成的博客 SaaS | 内容不在自己手里，导出与迁移都受制于人 |
| 前端框架 + 静态导出 | 为了写文章维护一套 npm 依赖链，收益不匹配 |
| 手写 HTML | 组件与多语言要全部自己来，长期维护成本高 |

选型是决策，不是事实。写在这里，是为了将来想换的时候知道自己当初为什么这么选。
