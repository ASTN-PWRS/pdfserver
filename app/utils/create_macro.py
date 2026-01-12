from pathlib import Path

# ディレクトリ設定
BASE_DIR = Path(__file__).resolve().parent.parent
components_dir = BASE_DIR / "templates" / "components"
output_path = BASE_DIR / "templates" / "macro" / "macros.jinja"

# .html ファイルを取得
component_files = sorted([f for f in components_dir.glob("*.jinja")])

# import 文と条件分岐の生成
import_lines = []
case_lines = []

for file in component_files:
    name = file.stem  # ファイル名（拡張子なし）
    import_lines.append(f'{{% import "components/{file.name}" as {name} %}}')
    case_lines.append(f'  {{% elif name == "{name}" %}}')
    case_lines.append(f'    {{{{ {name}.render(data) }}}}')

# マクロ全体の構築
macro_lines = [
    *import_lines,
    "",
    "{% macro renderComponent(name, data) %}",
    "  {% if false %}",  # ダミー条件
    *case_lines,
    "  {% endif %}",
    "{% endmacro %}",
]

# ファイルに書き出し
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text("\n".join(macro_lines), encoding="utf-8")

print("🍄 macros.jinja を生成しました！")
