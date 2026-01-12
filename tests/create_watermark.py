from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from datetime import datetime
import os
import math

# # フォント登録（最初に1回だけ）
# pdfmetrics.registerFont(TTFont("NotoSansJP", "./fonts/NotoSansJP-Regular.ttf"))

def create_watermark(page_width, page_height, text, config: WatermarkConfig):
  packet = BytesIO()
  can = canvas.Canvas(packet, pagesize=(page_width, page_height))

  # 対角線の長さと角度
  diag_len = math.hypot(page_width, page_height)
  angle_deg = math.degrees(math.atan2(page_height, page_width))

  # ページ中央に配置 
  x = page_width / 2 
  y = page_height / 2
  # 描画
  can.saveState()
  can.translate(x, y)
  can.rotate(angle_deg)
  can.setFont("Helvetica-Bold", 120)
  can.setFillAlpha(alpha)
  can.drawCentredString(0, 0, text)
  can.restoreState()
  