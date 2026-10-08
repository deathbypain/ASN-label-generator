#!/usr/bin/env python3
"""Generate an ASN label PDF with QR code in the top-left corner."""

from __future__ import annotations

import argparse
from pathlib import Path

import qrcode
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

PREFIX = "ASN"
NUMBER_WIDTH = 6
DEFAULT_PAGE_SIZE = "A4"


def parse_asn(asn: str) -> int:
    """Extract numeric sequence from ASN string like ASN000123 or plain integer like 123."""
    asn = asn.strip().upper()
    if asn.isdigit():
        return int(asn)

    if not asn.startswith(PREFIX):
        raise ValueError(f"ASN must be either a plain integer or start with '{PREFIX}'")

    numeric = asn[len(PREFIX) :]
    if not numeric.isdigit():
        raise ValueError("ASN numeric portion must contain digits only")

    return int(numeric)


def format_asn(sequence: int) -> str:
    return f"{PREFIX}{sequence:0{NUMBER_WIDTH}d}"


def make_qr_png(qr_data: str, output_png: Path, qr_size: int = 6) -> None:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_png)


def create_pdf(asn: str, pdf_path: Path, qr_png: Path, page_size: str = DEFAULT_PAGE_SIZE) -> None:
    if page_size.upper() == "A4":
        width_mm, height_mm = 210, 297
    elif page_size.upper() == "LETTER":
        width_mm, height_mm = 216, 279
    else:
        raise ValueError("page_size must be A4 or LETTER")

    c = canvas.Canvas(str(pdf_path), pagesize=(width_mm * mm, height_mm * mm))

    margin_x = 8 * mm
    margin_top = 8 * mm
    qr_size = 18 * mm

    page_height = height_mm * mm
    y_top = page_height - margin_top
    qr_x = margin_x

    c.drawImage(str(qr_png), qr_x, y_top - qr_size, width=qr_size, height=qr_size, preserveAspectRatio=True, mask="auto")

    c.setFont("Helvetica-Bold", 14)
    text_x = qr_x + qr_size + (2 * mm)
    text_y = y_top - 8 * mm

    c.drawString(text_x, text_y - 1 * mm, asn)

    c.save()


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate ASN label PDF with QR code in the corner of a page"
    )
    parser.add_argument(
        "--asn",
        required=True,
        help="ASN value, e.g. ASN000123 or plain number like 123",
    )
    parser.add_argument(
        "--doc-url",
        required=True,
        help="Paperless document URL to encode into the QR code (https://paperless.example.com/documents/12345)",
    )
    parser.add_argument(
        "--out-dir",
        default="output",
        help="Directory for generated files (default: output)",
    )
    parser.add_argument(
        "--page-size",
        choices=["A4", "LETTER", "a4", "letter"],
        default="A4",
        help="PDF page size (default: A4)",
    )
    parser.add_argument(
        "--keep-qr",
        action="store_true",
        help="Keep generated PNG QR image (default deletes it)",
    )
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    asn = format_asn(parse_asn(args.asn))

    qr_png = out_dir / f"{asn}_qr.png"
    pdf_path = out_dir / f"{asn}_label.pdf"

    make_qr_png(args.doc_url.strip(), qr_png)
    create_pdf(asn, pdf_path, qr_png, args.page_size)

    if not args.keep_qr and qr_png.exists():
        qr_png.unlink()

    print(f"Generated ASN: {asn}")
    print(f"PDF label: {pdf_path.resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
