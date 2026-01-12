import os
import math
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from io import BytesIO
from datetime import datetime

from create_watermark import create_watermark

def process_pdfs(pdf_paths, watermark_text, email, output_path, user_pw, owner_pw):
  writer = PdfWriter()

  for path in pdf_paths:
    reader = PdfReader(path)
    
    for page in reader.pages:
      width = float(page.mediabox.width)
      height = float(page.mediabox.height)

      # 透かしを生成してマージ
      vertical_text = f"{email} / {created_at}"
      watermark = create_watermark(
        page_width=width, 
        page_height=height, 
        text=watermark_text, 
        vertical_text=vertical_text, 
        percent=0.7, 
        alpha=0.3)
      watermark_pdf = PdfReader(watermark)
      page.merge_page(watermark_pdf.pages[0])
      writer.add_page(page)

  writer.encrypt( 
    user_password="", 
    owner_password=owner_pw, 
    use_128bit=True)
  with open(output_path, "wb") as f:
    writer.write(f)

