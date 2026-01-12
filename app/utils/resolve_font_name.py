def resolve_font_name(base: str, bold: bool, italic: bool) -> str:
  suffix = ""
  if bold and italic:
    suffix = "-BoldOblique" if base == "Helvetica" else "-BoldItalic"
  elif bold:
    suffix = "-Bold"
  elif italic:
    suffix = "-Oblique" if base == "Helvetica" else "-Italic"
  return base + suffix
