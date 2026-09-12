---
title: Why I built this site with OINK
date: 2026-09-12
description: "The choice, the trade-offs, and the options I dropped: a static site with one Markdown source for both readers and agents."
tags: [site, Hugo, docs-driven]
categories: [engineering]
cover: ''
---

This site holds technical notes, project logs, and decision records. The first task was not picking a theme but deciding what it has to carry: readable by people, directly readable by agents, and still editable years from now.

## The decision {#decision}

Hugo plus the [OINK](https://oink.pgsty.com/) theme: a purely static build, a single Markdown source, hosted on Cloudflare Pages.

Three reasons.

## One source of truth {#single-source}

OINK emits HTML, Markdown, a print view, and an `llms.txt` index for every page. Readers and agents consume the same source, so there is no second set of material to maintain.

```yaml {title="output formats in hugo.yaml"}
outputs:
  home: [HTML, RSS, markdown, LLMS]
  page: [HTML, markdown]
  section: [HTML, RSS, print, markdown]
```

## Native Markdown authoring {#native-markdown}

Callouts, tabs, steps, field tables, file trees, and diagrams are plain Markdown plus one attribute line. The source stays readable; no MDX or component syntax is involved.

> [!NOTE]
> Avoid anything that only makes sense after rendering. The next person, or agent, reads the source file.

## A short toolchain {#toolchain}

One `hugo` binary plus Go module resolution: no Node, npm, bundler, or CDN dependency. Local preview reloads in milliseconds and publishing is handled by CI.

## What I dropped {#alternatives}

| Option | Why it lost |
| --- | --- |
| A hosted blog service | Content lives elsewhere; export and migration are out of my hands |
| A frontend framework with static export | Maintaining an npm dependency chain to write prose does not pay off |
| Hand-written HTML | Components and multilingual routing become my problem forever |

A choice is not a fact. It is written down so that future me knows why present me decided this way.
