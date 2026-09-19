#!/usr/bin/env python3
"""Single-source QA for nature-figure-pdf deliverables.

One canonical implementation of the skill's mandatory checks. Import these
functions or run the CLI — do NOT copy-paste variants into plotting scripts
(divergent copies are how the font check silently weakened once before).

CLI:
    python scripts/figure_qa.py verify 图.pdf --width-mm 88.9
    python scripts/figure_qa.py preview 图.pdf
    python scripts/figure_qa.py audit-text 图.pdf
    python scripts/figure_qa.py font.check

Requires: pymupdf (verification + preview), matplotlib (font availability).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

BASE_PT = 7.0            # the skill's uniform text size
COLORBAR_MICRO_PT = 5.5  # sanctioned only inside the locked heatmap house style
WIDTH_TOL_MM = 0.3


def verify_figure_pdf(path: str | Path, width_mm: float = 88.9) -> dict:
    """Assert: one page, Arial-only fonts at ANY nesting depth, exact width.

    The font scan walks the whole page resource tree, including fonts nested
    inside Form XObjects, which a page-level /Resources/Font read silently
    misses. Do not replace this with a shallower check.
    """
    import pymupdf

    doc = pymupdf.open(path)
    try:
        if doc.page_count != 1:
            raise AssertionError(f"expected 1 page, got {doc.page_count}")
        page = doc[0]
        w_mm = page.rect.width / 72 * 25.4
        h_mm = page.rect.height / 72 * 25.4
        fonts = {f[3] for f in page.get_fonts(full=True)}  # f[3] = BaseFont
        non_arial = {f for f in fonts if "Arial" not in f}
        if non_arial:
            raise AssertionError(f"non-Arial fonts embedded: {non_arial} — fix font lock")
        if abs(w_mm - width_mm) >= WIDTH_TOL_MM:
            raise AssertionError(f"width {w_mm:.1f} mm != {width_mm} mm")
        print(f"OK: {w_mm:.1f} x {h_mm:.1f} mm, fonts = {sorted(fonts)}")
        return {"width_mm": round(w_mm, 2), "height_mm": round(h_mm, 2),
                "fonts": sorted(fonts)}
    finally:
        doc.close()


def render_preview(pdf_path: str | Path) -> Path:
    """Render the one-page figure PDF to a 300 dpi <stem>_预览.png next to it.

    The PNG is the user's review companion; the PDF is the submission file.
    Never produce any other image file.
    """
    import pymupdf

    pdf_path = Path(pdf_path)
    doc = pymupdf.open(pdf_path)
    try:
        if doc.page_count != 1:
            raise AssertionError(f"expected 1 page, got {doc.page_count}")
        out = pdf_path.with_suffix("").with_name(pdf_path.stem + "_预览.png")
        doc[0].get_pixmap(dpi=300).save(out)
    finally:
        doc.close()
    print(f"preview OK: {out}")
    return out


def audit_text_sizes(pdf_path: str | Path,
                     allowed_pt: tuple[float, ...] = (BASE_PT, COLORBAR_MICRO_PT)) -> dict:
    """Content-stream Tf scan: every font-size command must be an allowed size
    (7 pt text; 5.5 pt only in the heatmap house style colorbar) or the
    mathtext sub/superscript scale (0.7 x the base). Any other size is a
    delivery blocker. Needs an uncompressed or decodable content stream."""
    import re

    import pymupdf

    doc = pymupdf.open(pdf_path)
    try:
        stream = doc[0].read_contents().decode("latin-1", errors="replace")
    finally:
        doc.close()

    sizes: dict[float, int] = {}
    for m in re.finditer(r"/(\S+)\s+([\d.]+)\s+Tf", stream):
        size = float(m.group(2))
        sizes[round(size, 2)] = sizes.get(round(size, 2), 0) + 1

    mathtext_scale = round(0.7 * BASE_PT, 2)
    bad = {}
    for size, count in sizes.items():
        if any(abs(size - a) <= 0.05 for a in allowed_pt):
            continue
        if abs(size - mathtext_scale) <= 0.05:
            continue
        bad[size] = count
    if not sizes:
        raise AssertionError("no Tf font-size commands found — text may be outlined")
    if bad:
        raise AssertionError(
            f"non-sanctioned text sizes (pt): {bad} — allowed: {sorted(allowed_pt)} "
            f"+ mathtext {mathtext_scale}")
    print(f"audit-text OK: sizes = {sizes} pt")
    return sizes


def check_font_available() -> None:
    """Blocker check: Arial must resolve to a real Arial file on this machine.
    Lookalike substitutes (Liberation Sans, Helvetica clones) are forbidden."""
    from matplotlib import font_manager

    path = font_manager.findfont("Arial", fallback_to_default=False)
    name = Path(path).name.lower()
    if "arial" not in name:
        raise AssertionError(
            f"Arial not installed (resolved to {path}). This is a delivery "
            "blocker: install a real Arial (Windows ships it; on Linux install "
            "ttf-mscorefonts-installer or copy Arial.ttf into ~/.fonts and "
            "rebuild the matplotlib cache). Substitutes like Liberation Sans "
            "are forbidden.")
    print(f"font OK: Arial -> {path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("verify", help="one page / Arial-only fonts / exact width")
    p.add_argument("pdf")
    p.add_argument("--width-mm", type=float, default=88.9)

    sub.add_parser("preview", help="render <stem>_预览.png at 300 dpi").add_argument("pdf")

    p = sub.add_parser("audit-text", help="content-stream 7 pt Tf scan")
    p.add_argument("pdf")
    p.add_argument("--allow-colorbar-micro", action="store_true", default=True)

    sub.add_parser("font.check", help="assert a real Arial is installed")

    args = parser.parse_args(argv)
    try:
        if args.cmd == "verify":
            verify_figure_pdf(args.pdf, args.width_mm)
        elif args.cmd == "preview":
            render_preview(args.pdf)
        elif args.cmd == "audit-text":
            audit_text_sizes(args.pdf)
        elif args.cmd == "font.check":
            check_font_available()
    except (AssertionError, FileNotFoundError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
