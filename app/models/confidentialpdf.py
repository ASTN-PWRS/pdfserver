from pydantic import BaseModel
from typing import Optional

from models.signature import SignatureConfig
from models.watermark import WatermarkConfig

class ConfidentialPDF(BaseModel):
  title: str
  author: Optional[str] = None
  user_pw: str
  owner_pw: str
  signature: SignatureConfig
  watermark: WatermarkConfig
