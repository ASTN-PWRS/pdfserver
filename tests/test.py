from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from typing_extensions import Annotated

class FontStyle(BaseModel): 
  bold: bool = False 
  italic: bool = False

def resolve_font_name(base: str, bold: bool, italic: bool) -> str:
  suffix = ""
  if bold and italic:
    suffix = "-BoldOblique" if base == "Helvetica" else "-BoldItalic"
  elif bold:
    suffix = "-Bold"
  elif italic:
    suffix = "-Oblique" if base == "Helvetica" else "-Italic"
  return base + suffix

class SignatureConfig(BaseModel):
    font_name: Literal["Helvetica", "Times-Roman", "Courier"] = "Helvetica"
    font_size: int = 16
    min_margin: int = 20
    rgba: Annotated[ 
      list[float], 
      Field(min_length=4, max_length=4, description="RGBA値(0.0〜1.0の4要素)") ] = [0.5, 0.5, 0.5, 0.5]
    style: FontStyle = FontStyle()

def add_signature(page_width, page_height, text, config:SignatureConfig):
  left_margin = config.min_margin+(config.font_size / 2)
  # テキストの横幅（回転後は縦方向の長さになる） 
  text_width = pdfmetrics.stringWidth(text, config.font_name, config.font_size)
  # 縦方向の位置を調整：中央からテキストの半分を引く 
  vertical_position = (page_height / 2) + (text_width / 2)
  # メモリ上にPDFを作成
  packet = BytesIO()
  c = canvas.Canvas(packet, pagesize=(page_width, page_height))

  c.saveState()
  r, g, b, alpha = config.rgba
  c.setFillColor(Color(r, g, b, alpha))
  
  font = resolve_font_name(config.font_name, config.bold, config.italic)
  c.setFont(font, config.font_size)

  # 左端に配置（少し内側にオフセット）
  c.translate(left_margin, vertical_position)
  c.rotate(90)
  c.drawCentredString(0, 0, text)
  c.restoreState()

  c.showPage()
  c.save()
  packet.seek(0)

  # pypdfで読み込めるように変換
  watermark_pdf = PdfReader(packet)
  return watermark_pdf.pages[0]


def add_left_watermark(input_path="input.pdf", output_path="output.pdf"):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)

        # 左端透かしページを作成
        config = SignatureConfig( 
          font_name="Times-Roman", 
          font_size=16, 
          min_margin=20,
          rgba= [0.5, 0.5, 0.5, 0.5]
        )
        text = "test@gmail.com"
        watermark_page = add_signature(page_width, page_height, text, config)

        # 元ページに透かしを重ねる
        page.merge_page(watermark_page)
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

# 実行
add_left_watermark()
