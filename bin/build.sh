#!/usr/bin/env bash
# 统一的构建入口：本地、GitHub Actions、Cloudflare 三处共用。
#
# 为什么要自己管 Hugo 版本：Cloudflare 构建镜像预装的是 Hugo 0.147.7，
# 低于 OINK 要求的 0.160.1，会在解析主题 i18n 文件时报错；而它的
# HUGO_VERSION 环境变量在部分构建系统上并不生效。所以这里显式检查版本，
# 不合适就下载官方 Extended 二进制，构建结果不再取决于镜像里装了什么。
#
# 用法：
#   bash bin/build.sh              # 常规构建（Cloudflare 用这个）
#   STRICT=1 bash bin/build.sh     # 警告即失败（CI 与发布前自检用这个）

set -euo pipefail

HUGO_VERSION="${HUGO_VERSION:-0.166.0}"
export GOWORK="${GOWORK:-off}"
export HUGO_MODULE_WORKSPACE="${HUGO_MODULE_WORKSPACE:-off}"

has_matching_hugo() {
  command -v hugo >/dev/null 2>&1 || return 1
  local reported
  reported="$(hugo version)"
  [[ "$reported" == *"+extended"* && "$reported" == *"v${HUGO_VERSION}"* ]]
}

if ! has_matching_hugo; then
  hugo_dir="/tmp/hugo-${HUGO_VERSION}"
  if [ ! -x "${hugo_dir}/hugo" ]; then
    tarball="/tmp/hugo-${HUGO_VERSION}.tar.gz"
    url="https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
    echo "现有 Hugo 版本不匹配，下载 Hugo Extended ${HUGO_VERSION}"
    mkdir -p "${hugo_dir}"
    curl -fsSL -o "${tarball}" "${url}"
    tar -xzf "${tarball}" -C "${hugo_dir}"
  fi
  export PATH="${hugo_dir}:${PATH}"
fi

hugo version

build_args=(--gc --minify --environment production --cleanDestinationDir)
if [ "${STRICT:-0}" = "1" ]; then
  build_args+=(--printPathWarnings --panicOnWarning)
fi

hugo "${build_args[@]}"
