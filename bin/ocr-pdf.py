#!/usr/bin/env python3
"""把扫描版 PDF 的指定页范围 OCR 成文本。

扫描件（每页是一张图、没有文字层）用 pdftotext 提不出内容，这个脚本先渲染再识别。

用法：
    python3 bin/ocr-pdf.py <pdf> <起始页> <结束页> [输出文件]

依赖：
    poppler-utils（pdftoppm）
    pip install --user rapidocr-onnxruntime

页号从 1 开始，闭区间。输出是纯文本，每页前有 `===== 第 N 页 =====` 分隔标记。
"""

import os
import shutil
import subprocess
import sys
import tempfile


def render(pdf: str, first: int, last: int, outdir: str, dpi: int = 200) -> list[str]:
    subprocess.run(
        ["pdftoppm", "-f", str(first), "-l", str(last), "-r", str(dpi), "-png",
         pdf, os.path.join(outdir, "p")],
        check=True,
    )
    return sorted(
        os.path.join(outdir, name) for name in os.listdir(outdir) if name.endswith(".png")
    )


def ocr_pages(images: list[str], first: int) -> list[str]:
    from rapidocr_onnxruntime import RapidOCR

    engine = RapidOCR()
    out = []
    for offset, image in enumerate(images):
        page = first + offset
        result, _ = engine(image)
        lines = [item[1] for item in (result or [])]
        out.append(f"===== 第 {page} 页 =====\n" + "\n".join(lines))
        print(f"  第 {page} 页完成（{len(lines)} 行）", file=sys.stderr, flush=True)
    return out


def main() -> int:
    if len(sys.argv) < 4:
        print(__doc__)
        return 2

    pdf, first, last = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    target = sys.argv[4] if len(sys.argv) > 4 else None

    workdir = tempfile.mkdtemp(prefix="ocr-pdf-")
    try:
        images = render(pdf, first, last, workdir)
        if not images:
            print("没有渲染出任何页面", file=sys.stderr)
            return 1
        pages = ocr_pages(images, first)
        text = "\n\n".join(pages) + "\n"
        if target:
            with open(target, "w", encoding="utf-8") as handle:
                handle.write(text)
            print(f"已写入 {target}", file=sys.stderr)
        else:
            sys.stdout.write(text)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
