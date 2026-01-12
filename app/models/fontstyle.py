from pydantic import BaseModel

class FontStyle(BaseModel): 
  bold: bool = False 
  italic: bool = False
