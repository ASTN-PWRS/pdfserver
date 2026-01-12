import os
from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse


router = APIRouter()

# @router.post("/show-pdf/")
# async def generate_pdf(
#     files: List[UploadFile] = File(...),
#     email: str = Form(...),
# ):

# signature_text = = f"{email} / {created_at}"
# write = merge_pdf(files,watermark_text, signature_text, config)
# output_stream = BytesIO()
# writer.write(output_stream)
# output_stream.seek(0)

# return StreamingResponse( 
#   output_stream, 
#   media_type="application/pdf", 
#   headers={ 
#     filename="merged_watermarked.pdf"
#   })
