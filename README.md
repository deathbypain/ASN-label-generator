# ASN Label Generator

A tiny tool for people who run [paperless-ngx], a self-hosted digital document store, and also keep the physical **hard copies** of those documents.

Once a paper document has been scanned and uploaded to paperless-ngx, this tool generates a print-ready label that you **print directly on the back of the original sheet** before filing it. Each label contains:

- A **QR code** that opens the document's paperless-ngx page, so you can scan it from the paper with your phone and jump straight to the digital copy.
- The document's **ASN** (Archival Storage Number) in text form, next to the QR code, for quick visual reference while shelving.

The result is a single-page PDF with the label placed in the top-left corner, sized to print on the back of your scanned sheet. This makes it easy to organize and locate the physical files, and to find the matching digital document instantly.

[paperless-ngx]: https://docs.paperless-ngx.com/

## What It Produces

- QR code containing a Paperless document URL
- ASN text next to the QR code
- Full page PDF (A4 or Letter) with the label in the top-left corner

## Setup

```powershell
python -m pip install -r requirements.txt
```

## Usage

Both ASN and Paperless document number are required.

For `--asn`, you can pass either:
- preformatted ASN, like `ASN000123`
- plain integer, like `123` (auto-formatted to `ASN000123`)

```powershell
python generate_asn_label.py --asn ASN000123 --doc-url "https://paperless.example.com/documents/1"
```

Plain integer ASN example:

```powershell
python generate_asn_label.py --asn 1 --doc-url "https://paperless.example.com/documents/1"
```

Use Letter size and custom output folder:

```powershell
python generate_asn_label.py --page-size LETTER --out-dir labels --doc-url "https://paperless.example.com/documents/1"
```

Keep the intermediate QR PNG:

```powershell
python generate_asn_label.py --asn 1 --doc-url "https://paperless.example.com/documents/1" --keep-qr
```

## Lightweight GUI

Run the small desktop GUI:

```powershell
python asn_label_gui.py
```

The GUI has:
- ASN field
- Document # field
- Increment button (adds 1 to both fields)
- Generate button (runs the same logic as CLI using `--asn` and `--doc-url`)

## Output

By default, files are written to `output/`.

Example PDF filename:
- `output/ASN000001_label.pdf`

## Printing Tip

When printing the generated PDF onto the back of your scanned page, ensure:

- actual size / no scaling
- orientation matches your original scanned sheet
- test one page first for alignment
