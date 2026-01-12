import os
import math
from pypdf import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
#
from models.watermark import WatermarkConfig
from resolve_font_name import resolve_font_name

def create_watermark(page_width, page_height, text, config: WatermarkConfig):

  packet = BytesIO()
  c = canvas.Canvas(packet, pagesize=(page_width, page_height))
  font_name = resolve_font_name(config.font_name, config.bold, config.italic)

  # 対角線の長さと角度
  diag_len  = math.hypot(page_width, page_height)
  angle_deg = math.degrees(math.atan2(page_height, page_width))

  # ページ中央に配置 
  x = page_width / 2 
  y = page_height / 2
  # 描画
  c.saveState()
  c.translate(x, y)
  c.rotate(angle_deg)
  
  c.setFont(font_name, config.font_size)
  
  r, g, b, alpha = config.rgba
  c.setFillColor(Color(r, g, b, alpha))
  c.drawCentredString(0, 0, text)
  c.restoreState()
  
  c.showPage()
  c.save()
  packet.seek(0)

  # pypdfで読み込めるように変換
  pdfobj = PdfReader(packet)
  return pdfobj.pages[0]
