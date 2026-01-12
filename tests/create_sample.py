import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, B5, landscape
from reportlab.lib.units import mm

def create_sample_pdf(path, pagesize, title):
    c = canvas.Canvas(path, pagesize=pagesize)
    width, height = pagesize
    c.setFont("Helvetica", 16)
    c.drawString(30 * mm, height - 30 * mm, f"Sample Document: {title}")
    c.drawString(30 * mm, height - 40 * mm, f"Size: {int(width)} x {int(height)}")
    c.drawString(30 * mm, height - 50 * mm, "This is a test page for watermarking.")
    c.showPage()
    c.save()

def generate_input_pdfs():
    os.makedirs("./input", exist_ok=True)

    create_sample_pdf("./input/invoice_A4.pdf", A4, "Invoice A4")
    create_sample_pdf("./input/report_B5.pdf", B5, "Report B5")
    create_sample_pdf("./input/summary_custom.pdf", (500, 700), "Custom Summary")
    create_sample_pdf("./input/presentation_landscape.pdf", landscape(A4), "Presentation A4 Landscape")
