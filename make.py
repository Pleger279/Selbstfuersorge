import json, zipfile, sys
URL = "https://raw.githubusercontent.com/Pleger279/Selbstfuersorge/main/zeilen.txt"
F = "kfile://org.kustom.provider/fonts/"
def line(i, bold):
    return {
        "internal_type": "TextModule",
        "internal_title": "Titel" if bold else f"Zeile {i}",
        "text_expression": f'$tc(split, wg("{URL}", txt), "~", {i})$',
        "text_family": F + ("Lora-Bold.ttf" if bold else "Lora-Regular.ttf"),
        "text_size_type": "FIXED_WIDTH",
        "text_width": 280.0,
        "text_lines": 3.0,
        "text_size": 18.0 if bold else 14.0,
        "paint_color": "#FF2C2C2A" if bold else "#FF444441",
        "position_padding_bottom": 4.0 if bold else 0.0,
        "internal_toggles": {"text_width": 10, "text_size": 10, "position_padding_bottom": 10},
        "internal_globals": {},
        "internal_formulas": {
            "text_width": "$gv(w)*0.88$",
            "text_size": "$gv(fs)*1.45$" if bold else "$gv(fs)$",
            "position_padding_bottom": "$gv(fs)/2.5$" if bold else "$0$",
        },
    }
preset = {
  "preset_info": {"archive": None, "author": "", "description": "Takeaway aus dem Projekt Selbstfürsorge",
    "email": "", "features": "", "pflags": 0, "width": 400, "height": 400, "locked": False,
    "release": 377435216, "title": "Takeaway", "version": 13, "xscreens": 0, "yscreens": 0},
  "preset_root": {
    "internal_type": "RootLayerModule",
    "globals_list": {
      "side": {"index": 0, "type": "NUMBER", "title": "side", "min": 0, "max": 2000, "toggles": 10,
               "global_formula": "$if(si(rwidth)>si(rheight), si(rheight), si(rwidth))$"},
      "w": {"index": 2, "type": "NUMBER", "title": "w", "min": 0, "max": 4000, "toggles": 10,
               "global_formula": "$si(rwidth)$"},
      "h": {"index": 3, "type": "NUMBER", "title": "h", "min": 0, "max": 4000, "toggles": 10,
               "global_formula": "$si(rheight)$"},
      "fs": {"index": 4, "type": "NUMBER", "title": "fs", "min": 0, "max": 500, "toggles": 10,
               "global_formula": "$if(si(rwidth)/14 < si(rheight)/13, si(rwidth)/14, si(rheight)/13)$"},
      "url": {"index": 1, "type": "TEXT", "title": "Quelle", "value": URL},
    },
    "viewgroup_items": [
      {"internal_type": "ShapeModule", "internal_title": "Hintergrund", "shape_type": "RECT",
       "shape_width": 400.0, "shape_height": 400.0, "shape_corners": 22.0, "paint_color": "#CCF1EFE8",
       "internal_toggles": {"shape_width": 100, "shape_height": 100, "shape_corners": 10},
       "internal_globals": {"shape_width": "w", "shape_height": "h"},
       "internal_formulas": {"shape_corners": "$gv(side)/14$"}},
      {"internal_type": "StackLayerModule", "internal_title": "Text",
       "config_stacking": "VERTICAL_LEFT", "config_margin": 4.0,
       "internal_toggles": {"config_margin": 10}, "internal_formulas": {"config_margin": "$gv(fs)/4$"},
       "viewgroup_items": [line(0, True), line(1, False), line(2, False), line(3, False)]},
    ],
  },
}
out = sys.argv[1]
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("preset.json", json.dumps(preset, ensure_ascii=False, indent=1))
    for w in ("Regular", "Bold"):
        z.write(f"/tmp/claude-0/kw/build/fonts/Lora-{w}.ttf", f"fonts/Lora-{w}.ttf")
print("ok")
