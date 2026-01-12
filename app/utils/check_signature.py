from pyhanko.sign.general    import get_signatures
from pyhanko.sign.validation import validate_pdf_signature

def check_signature(file):

  with open(file, "rb") as f:
    sigs = list(get_signatures(f))
    for sig in sigs:
      status = validate_pdf_signature(sig)
      print("署名者:", sig.signer_cert.subject.human_friendly)
      print("検証結果:", status.summary())
