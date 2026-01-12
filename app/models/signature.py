from pydantic import BaseModel, Field, confloat, conlist
from typing import Literal, Annotated

from fontstyle import FontStyle
from color import RGBAValue

class SignatureConfig(BaseModel):
  text: str = ""
  font_name: Literal["Helvetica", "Times-Roman", "Courier"] = "Helvetica"
  font_size: int = 16
  min_margin: int = 20
  rgba: RGBAValue = [0.5, 0.5, 0.5, 0.5] 
  style: FontStyle = Field(default_factory=FontStyle)
  