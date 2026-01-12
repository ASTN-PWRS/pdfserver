from pydantic import BaseModel, Field, confloat
from typing import Literal

from fontstyle import FontStyle
from color import RGBAValue

class WatermarkConfig(BaseModel):
  text: str = ""
  font_name: Literal["Helvetica", "Times-Roman", "Courier"] = "Helvetica"
  font_size: int = 16
  percent: conint(ge=0, le=100) = 20
  rgba: RGBAValue = [0.5, 0.5, 0.5, 0.5] 
  style: FontStyle = Field(default_factory=FontStyle)
