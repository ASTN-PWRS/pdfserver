
# pdfの左端に縦にtextを追加する

# config = SignatureConfig( 
#   font_name="Times-Roman", 
#   font_size=16, 
#   min_margin=20,
#   rgba= [0.5, 0.5, 0.5, 0.5]
# )
# text = "test@gmail.com"
# signature_page = add_signature(page_width, page_height, text, config)

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from io import BytesIO
from pypdf import PdfReader

from models import SignatureConfig
from resolve_font_name import resolve_font_name

def create_signature(page_width, page_height, config:SignatureConfig):

  font_name = resolve_font_name(config.font_name, config.bold, config.italic)
  left_margin = config.min_margin+(config.font_size / 2)
  # テキストの横幅（回転後は縦方向の長さになる） 
  text_width = pdfmetrics.stringWidth(config.text, font_name, config.font_size)
  # 縦方向の位置を調整：中央からテキストの半分を引く 
  vertical_position = (page_height / 2) + (text_width / 2)
  # メモリ上にPDFを作成
  packet = BytesIO()
  c = canvas.Canvas(packet, pagesize=(page_width, page_height))

  c.saveState()
  r, g, b, alpha = config.rgba
  c.setFillColor(Color(r, g, b, alpha))
  
  c.setFont(font_name, config.font_size)

  # 左端に配置（少し内側にオフセット）
  c.translate(left_margin, vertical_position)
  c.rotate(90)
  c.drawCentredString(0, 0, config.text)
  c.restoreState()

  c.showPage()
  c.save()
  packet.seek(0)

 # pypdfで読み込めるように変換
  pdfobj = PdfReader(packet)
  return pdfobj.pages[0]