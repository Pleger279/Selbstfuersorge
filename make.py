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
        **({} if bold else {"text_size_type": "FIXED_WIDTH", "text_width": 280.0, "text_lines": 4.0}),
        "text_size": 14.0,
        "paint_color": "#FF633806" if bold else "#FF412402",
        "internal_toggles": {"text_size": 10, "position_padding_bottom": 10} if bold else {"text_width": 10, "text_size": 10},
        "internal_formulas": {"text_size": "$gv(fs)*1.45$", "position_padding_bottom": "$gv(fs)/2.5$"} if bold else {"text_width": "$gv(w)*0.88$", "text_size": "$gv(fs)$"},
    }

def sun_icon():
    def c(title, color, f, stroke=False):
        m = {"internal_type": "ShapeModule", "internal_title": title, "shape_type": "CIRCLE",
             "shape_width": 20.0, "paint_color": color,
             "internal_toggles": {"shape_width": 10}, "internal_formulas": {"shape_width": f"$gv(fs)*{f}$"}}
        if stroke:
            m["paint_style"] = "STROKE"; m["paint_stroke"] = 2.0
            m["internal_toggles"]["paint_stroke"] = 10; m["internal_formulas"]["paint_stroke"] = "$gv(fs)/8$"
        return m
    return {"internal_type": "OverlapLayerModule", "internal_title": "Sonne",
            "viewgroup_items": [c("Sonnenring", "#FFFAC775", 1.55, True), c("Sonne", "#FFEF9F27", 1.0)]}

title_row = {"internal_type": "StackLayerModule", "internal_title": "Titelzeile",
    "config_stacking": "HORIZONTAL_CENTER", "config_margin": 8.0,
    "position_padding_bottom": 4.0,
    "internal_toggles": {"config_margin": 10, "position_padding_bottom": 10},
    "internal_formulas": {"config_margin": "$gv(fs)*0.6$", "position_padding_bottom": "$gv(fs)/2.5$"},
    "viewgroup_items": []}

sonnenkind = {
    "internal_type": "TextModule", "internal_title": "Sonnenkind-Satz",
    "text_expression": part(4),
    "text_family": F + "Lora-Italic.ttf",
    "text_size_type": "FIXED_WIDTH", "text_width": 280.0, "text_lines": 3.0, "text_size": 13.0,
    "paint_color": "#FF854F0B",
    "position_padding_top": 8.0,
    "internal_toggles": {"text_width": 10, "text_size": 10, "position_padding_top": 10},
    "internal_formulas": {"text_width": "$gv(w)*0.88$", "text_size": "$gv(fs)$", "position_padding_top": "$gv(fs)*0.7$"},
}

def big_sun():
    def c(title, color, f, stroke=False):
        m = {"internal_type": "ShapeModule", "internal_title": title, "shape_type": "CIRCLE",
             "shape_width": 100.0, "paint_color": color,
             "internal_toggles": {"shape_width": 10}, "internal_formulas": {"shape_width": f"$gv(side)*{f}$"}}
        if stroke:
            m["paint_style"] = "STROKE"; m["paint_stroke"] = 3.0
            m["internal_toggles"]["paint_stroke"] = 10; m["internal_formulas"]["paint_stroke"] = "$gv(side)/110$"
        return m
    return {"internal_type": "OverlapLayerModule", "internal_title": "Grosse Sonne",
            "position_anchor": "BOTTOMRIGHT", "position_offset_y": -60.0,
            "internal_toggles": {"position_offset_y": 10},
            # negativer Wert schiebt nach unten (positiver hatte die Sonne nach oben verschoben)
            "internal_formulas": {"position_offset_y": "$0-gv(side)*0.24$"},
            "viewgroup_items": [c("Sonnenring", "#AAFAC775", 0.80, True), c("Sonne", "#73EF9F27", 0.56)]}

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
             "global_formula": "$if(si(rwidth)/15 < si(rheight)/17.5, si(rwidth)/15, si(rheight)/17.5)$"},
    },
    "viewgroup_items": [
      {"internal_type": "ShapeModule", "internal_title": "Hintergrund", "shape_type": "RECT",
       "shape_width": 400.0, "shape_height": 400.0, "shape_corners": 22.0, "paint_color": "#EEFAEEDA",
       "internal_toggles": {"shape_width": 100, "shape_height": 100, "shape_corners": 10},
       "internal_globals": {"shape_width": "w", "shape_height": "h"},
       "internal_formulas": {"shape_corners": "$gv(side)/14$"}},
      big_sun(),
      {"internal_type": "StackLayerModule", "internal_title": "Schritte",
       "config_stacking": "VERTICAL_LEFT", "config_margin": 4.0,
       "position_anchor": "TOP", "position_padding_top": 20.0,
       "internal_toggles": {"config_margin": 10, "position_padding_top": 10},
       "internal_formulas": {"config_margin": "$gv(fs)/2.5$", "position_padding_top": "$gv(h)*0.05$"},
       "viewgroup_items": [line(0, True), line(1, False), line(2, False), line(3, False), sonnenkind]},
    ],
  },
}
with zipfile.ZipFile(sys.argv[1], "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("preset.json", json.dumps(preset, ensure_ascii=False, indent=1))
    for w in ("Regular", "Bold", "Italic"):
        z.write(FONTDIR + f"Lora-{w}.ttf", f"fonts/Lora-{w}.ttf")
print("ok")
