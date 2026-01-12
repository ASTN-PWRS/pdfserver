
def merge_pdf(pdf_paths, config:ConfidentialPDF):

  watermark_pdf = create_watermark(width,height,config.watermark)
  signature_pdf = create_signature(width,height,config.signature)

  writer = PdfWriter()

  for path in pdf_paths:
    reader = PdfReader(path)
    for page in reader.pages:
      width = float(page.mediabox.width)
      height = float(page.mediabox.height)
      page.merge_page(watermark_pdf.pages[0])
      page.merge_page(signature_pdf.pages[0])
      writer.add_page(page)

  writer.encrypt( 
    user_password=config.user_pw, 
    owner_password=config.owner_pw, 
    use_128bit=True
  )

  writer.add_metadata({ 
    "/Title": config.title, 
    "/Author": config.author 
  })

  return write

