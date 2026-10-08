#!/usr/bin/env python3
"""Small GUI for generate_asn_label.py."""

from __future__ import annotations

import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

PREFIX = "ASN"
NUMBER_WIDTH = 6
DOC_URL_BASE = "https://paperless.deathbypa.in/documents/"


def parse_asn_input(value: str) -> tuple[int, bool]:
    text = value.strip().upper()
    if not text:
        raise ValueError("ASN is required")

    if text.isdigit():
        return int(text), False

    if not text.startswith(PREFIX):
        raise ValueError("ASN must be plain number or start with ASN")

    numeric = text[len(PREFIX) :]
    if not numeric.isdigit():
        raise ValueError("ASN numeric portion must contain digits only")

    return int(numeric), True


def format_asn(sequence: int) -> str:
    return f"{PREFIX}{sequence:0{NUMBER_WIDTH}d}"


def parse_document_number(value: str) -> int:
    text = value.strip()
    if not text:
        raise ValueError("Document # is required")
    if not text.isdigit():
        raise ValueError("Document # must be a positive integer")

    doc_num = int(text)
    if doc_num < 1:
        raise ValueError("Document # must be at least 1")

    return doc_num


class AsnLabelGui:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("ASN Label Generator")
        self.root.resizable(False, False)

        self.asn_var = tk.StringVar(value="1")
        self.doc_var = tk.StringVar(value="1")
        self.status_var = tk.StringVar(value="Ready")

        frame = tk.Frame(root, padx=10, pady=10)
        frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(frame, text="ASN").grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.asn_entry = tk.Entry(frame, textvariable=self.asn_var, width=20)
        self.asn_entry.grid(row=0, column=1, sticky="ew", pady=(0, 6))

        tk.Label(frame, text="Document #").grid(row=1, column=0, sticky="w", pady=(0, 10))
        self.doc_entry = tk.Entry(frame, textvariable=self.doc_var, width=20)
        self.doc_entry.grid(row=1, column=1, sticky="ew", pady=(0, 10))

        button_row = tk.Frame(frame)
        button_row.grid(row=2, column=0, columnspan=2, sticky="ew")

        tk.Button(button_row, text="Increment", width=12, command=self.increment).grid(row=0, column=0, padx=(0, 8))
        tk.Button(button_row, text="Generate", width=12, command=self.generate).grid(row=0, column=1)

        tk.Label(frame, textvariable=self.status_var, fg="#333333").grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 0))

        self.asn_entry.focus_set()

    def increment(self) -> None:
        try:
            asn_seq, asn_has_prefix = parse_asn_input(self.asn_var.get())
            doc_num = parse_document_number(self.doc_var.get())
        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))
            return

        new_asn_seq = asn_seq + 1
        new_doc_num = doc_num + 1

        if asn_has_prefix:
            self.asn_var.set(format_asn(new_asn_seq))
        else:
            self.asn_var.set(str(new_asn_seq))

        self.doc_var.set(str(new_doc_num))
        self.status_var.set("Incremented ASN and Document #")

    def generate(self) -> None:
        try:
            asn_input = self.asn_var.get().strip()
            _asn_seq, _asn_has_prefix = parse_asn_input(asn_input)
            doc_num = parse_document_number(self.doc_var.get())
        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))
            return

        doc_url = f"{DOC_URL_BASE}{doc_num}"
        script_path = Path(__file__).with_name("generate_asn_label.py")

        cmd = [
            sys.executable,
            str(script_path),
            "--asn",
            asn_input,
            "--doc-url",
            doc_url,
        ]

        try:
            completed = subprocess.run(cmd, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as exc:
            detail = exc.stderr.strip() or exc.stdout.strip() or "Unknown error"
            messagebox.showerror("Generation Failed", detail)
            self.status_var.set("Generation failed")
            return

        output = completed.stdout.strip() or "Label generated"
        self.status_var.set("Generated successfully")
        messagebox.showinfo("Done", output)


def main() -> int:
    root = tk.Tk()
    AsnLabelGui(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
