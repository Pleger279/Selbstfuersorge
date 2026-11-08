import json, zipfile, sys
URL = "https://raw.githubusercontent.com/Pleger279/Selbstfuersorge/main/zeilen.txt"
F = "kfile://org.kustom.provider/fonts/"
FONTDIR = "/tmp/claude-0/kw/build/fonts/"
def part(i):
    return f'$tc(split, wg("{URL}", txt), "~", {i})$'

def line(i, bold):
    return {
        "internal_type": "TextModule",
        "internal_title": "Titel" if bold else f"Schritt {i}",
        "text_expression": part(i),
        "text_family": F + ("Lora-Bold.ttf" if bold else "Lora-Regular.ttf"),
        "text_size_type": "FIXED_WIDTH", "text_width": 280.0, "text_lines": 4.0,
        "text_size": 14.0,
        "paint_color": "#FF633806" if bold else "#FF412402",
        "position_padding_bottom": 0.0,
        "internal_toggles": {"text_width": 10, "text_size": 10, "position_padding_bottom": 10},
        "internal_formulas": {
            # Titel schmaler, damit er die Sonne nicht berührt
            "text_width": "$gv(w)*0.62$" if bold else "$gv(w)*0.88$",
            "text_size": "$gv(fs)*1.45$" if bold else "$gv(fs)$",
            "position_padding_bottom": "$gv(fs)/2.5$" if bold else "$0$",
        },
    }

def circle(title, color, size_f, right_f, stroke=False):
    m = {"internal_type": "ShapeModule", "internal_title": title, "shape_type": "CIRCLE",
         "shape_width": 100.0, "paint_color": color,
         "position_anchor": "BOTTOMRIGHT", "position_padding_right": 30.0, "position_offset_y": 50.0,
         "internal_toggles": {"shape_width": 10, "position_padding_right": 10, "position_offset_y": 10},
         "internal_formulas": {
             "shape_width": f"$gv(side)*{size_f}$",
             "position_padding_right": f"$gv(w)*{right_f}$",
             "position_offset_y": f"$gv(side)*{size_f}/2$"}}
    if stroke:
        m["paint_style"] = "STROKE"; m["paint_stroke"] = 3.0
        m["internal_toggles"]["paint_stroke"] = 10
        m["internal_formulas"]["paint_stroke"] = "$gv(side)/120$"
    return m

sonnenkind = {
    "internal_type": "TextModule", "internal_title": "Sonnenkind-Satz",
    "text_expression": part(4),
    "text_family": F + "Lora-Italic.ttf",
    "text_size_type": "FIXED_WIDTH", "text_width": 200.0, "text_lines": 3.0, "text_size": 13.0,
    "paint_color": "#FF854F0B",
    "position_anchor": "BOTTOMLEFT", "position_padding_left": 20.0, "position_padding_bottom": 20.0,
    "internal_toggles": {"text_width": 10, "text_size": 10, "position_padding_left": 10, "position_padding_bottom": 10},
    "internal_formulas": {"text_width": "$gv(w)*0.6$", "text_size": "$gv(fs)$",
                          "position_padding_left": "$gv(w)*0.06$", "position_padding_bottom": "$gv(h)*0.05$"},
}

preset = {
  "preset_info": {"archive": None, "author": "", "description": "Takeaway aus dem Projekt Selbstfürsorge",
    "email": "", "features": "", "pflags": 0, "width": 400, "height": 400, "locked": False,
    "release": 377435216, "title": "Takeaway", "version": 13, "xscreens": 0, "yscreens": 0},
  "preset_root": {
    "internal_type": "RootLayerModule",
    "internal_events": [{"type": "SINGLE_TAP", "action": "KUSTOM_ACTION", "kustom_action": "TEXT_UPDATE"}],
    "globals_list": {
      "side": {"index": 0, "type": "NUMBER", "title": "side", "min": 0, "max": 2000, "toggles": 10,
               "global_formula": "$if(si(rwidth)>si(rheight), si(rheight), si(rwidth))$"},
      "w": {"index": 1, "type": "NUMBER", "title": "w", "min": 0, "max": 4000, "toggles": 10, "global_formula": "$si(rwidth)$"},
      "h": {"index": 2, "type": "NUMBER", "title": "h", "min": 0, "max": 4000, "toggles": 10, "global_formula": "$si(rheight)$"},
      "fs": {"index": 3, "type": "NUMBER", "title": "fs", "min": 0, "max": 500, "toggles": 10,
             "global_formula": "$if(si(rwidth)/16 < si(rheight)/17, si(rwidth)/16, si(rheight)/17)$"},
    },
    "viewgroup_items": [
      {"internal_type": "ShapeModule", "internal_title": "Hintergrund", "shape_type": "RECT",
       "shape_width": 400.0, "shape_height": 400.0, "shape_corners": 22.0, "paint_color": "#EEFAEEDA",
       "internal_toggles": {"shape_width": 100, "shape_height": 100, "shape_corners": 10},
       "internal_globals": {"shape_width": "w", "shape_height": "h"},
       "internal_formulas": {"shape_corners": "$gv(side)/14$"}},
      circle("Sonnenring", "#FFFAC775", 0.50, 0.04, stroke=True),
      circle("Sonne", "#FFEF9F27", 0.34, 0.12),
      sonnenkind,
      {"internal_type": "StackLayerModule", "internal_title": "Schritte",
       "config_stacking": "VERTICAL_LEFT", "config_margin": 4.0,
       "position_anchor": "TOP", "position_padding_top": 20.0,
       "internal_toggles": {"config_margin": 10, "position_padding_top": 10},
       "internal_formulas": {"config_margin": "$gv(fs)/2.5$", "position_padding_top": "$gv(h)*0.05$"},
       "viewgroup_items": [line(0, True), line(1, False), line(2, False), line(3, False)]},
    ],
  },
}
with zipfile.ZipFile(sys.argv[1], "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("preset.json", json.dumps(preset, ensure_ascii=False, indent=1))
    for w in ("Regular", "Bold", "Italic"):
        z.write(FONTDIR + f"Lora-{w}.ttf", f"fonts/Lora-{w}.ttf")
print("ok")
