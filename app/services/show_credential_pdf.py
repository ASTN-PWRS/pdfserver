
from models.confidentialpdf import ConfidentialPDF

# YAMLファイルを読み込んでモデルに変換
def load_config_from_yaml(path: str) -> ConfidentialPDF:
  with open(path, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)
  return ConfidentialPDF(**data)

def show_credential_pdf():
  config = load_config_from_yaml("config.yaml")
  print(config)
  created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
  signature_text = f"{email} / {created_at}"
