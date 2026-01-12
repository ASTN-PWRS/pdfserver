from pydantic import confloat, conlist


RGBAValue = conlist(confloat(ge=0.0, le=1.0), min_items=4, max_items=4)
