from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle
)
from datetime import datetime
from pathlib import Path
import uuid


def generate_invoice(data):
    output_folder = Path("invoices")
    output_folder.mkdir(exist_ok=True)

    invoice_number = "INV-" + datetime.now().strftime("%Y%m%d") + "-" + uuid.uuid4().hex[:5].upper()
    filename = output_folder / f"{invoice_number}.pdf"

    doc = SimpleDocTemplate(
        str(filename),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "InvoiceTitle",
        parent=styles["Title"],
        textColor=colors.HexColor("#1D4ED8"),
        fontSize=24
    )

    story = []

    story.append(Paragraph("TAX INVOICE", title_style))
    story.append(Spacer(1, 8 * mm))

    story.append(Paragraph(
        f"<b>Invoice Number:</b> {invoice_number}<br/>"
        f"<b>Date:</b> {datetime.now().strftime('%d-%m-%Y')}",
        styles["Normal"]
    ))

    story.append(Spacer(1, 8 * mm))

    story.append(Paragraph(
        f"<b>Business:</b> {data['business']}<br/>"
        f"<b>Business Address:</b> {data['business_address']}<br/>"
        f"<b>GSTIN:</b> {data.get('business_gstin', 'N/A')}",
        styles["Normal"]
    ))

    story.append(Spacer(1, 6 * mm))

    story.append(Paragraph(
        f"<b>Bill To:</b> {data['customer']}<br/>"
        f"<b>Customer Address:</b> {data['customer_address']}<br/>"
        f"<b>Customer GSTIN:</b> {data.get('customer_gstin', 'N/A')}",
        styles["Normal"]
    ))

    story.append(Spacer(1, 10 * mm))

    quantity = float(data["quantity"])
    price = float(data["price"])
    discount_percent = float(data["discount"])
    gst_rate = float(data["gst_rate"])

    subtotal = quantity * price
    discount_amount = subtotal * discount_percent / 100
    taxable_amount = subtotal - discount_amount
    gst_amount = taxable_amount * gst_rate / 100
    final_amount = taxable_amount + gst_amount

    if data["tax_type"] == "Interstate":
        tax_rows = [["IGST", f"₹{gst_amount:.2f}"]]
    else:
        tax_rows = [
            ["CGST", f"₹{gst_amount / 2:.2f}"],
            ["SGST", f"₹{gst_amount / 2:.2f}"]
        ]

    table_data = [
        ["Description", "Qty", "Price", "Amount"],
        [
            data["product"],
            str(quantity),
            f"₹{price:.2f}",
            f"₹{subtotal:.2f}"
        ],
        ["", "", "Subtotal", f"₹{subtotal:.2f}"],
        ["", "", f"Discount ({discount_percent}%)", f"-₹{discount_amount:.2f}"],
        ["", "", "Taxable Amount", f"₹{taxable_amount:.2f}"]
    ]

    for label, amount in tax_rows:
        table_data.append(["", "", label, amount])

    table_data.append(["", "", "Grand Total", f"₹{final_amount:.2f}"])

    table = Table(
        table_data,
        colWidths=[75 * mm, 20 * mm, 40 * mm, 40 * mm]
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1D4ED8")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#DBEAFE")),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))

    story.append(table)
    story.append(Spacer(1, 12 * mm))

    story.append(Paragraph(
        "<b>Thank you for your business!</b>",
        styles["Normal"]
    ))

    doc.build(story)

    return str(filename), invoice_number