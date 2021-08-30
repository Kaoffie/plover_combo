from enum import Enum
from typing import Callable

from plover_combo.combo_colors import COLOR_STR


class ComboAlignment(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2


ALIGNMENT_OPTIONS = [
    "Align Left (Expand Right)",
    "Align Center",
    "Align Right (Expand Left)"
]


CONFIG_ITEMS = {
    "highscore": 0,
    "cooldown_duration": 2000,
    "reset_on_undo": True,
    "bg_opacity": 0,
    "bg_color": "#000000",
    "force_repaint": False,
    "force_repaint_px": 1,
    "top_margin": 10,
    "bottom_margin": 10,
    "horz_margin": 30,
    "bar_width": 12,
    "zoom_scale_percent": 84,
    "alignment": ComboAlignment.CENTER,
    "font_name": "Plover Retro",
    "title_font_color": "#000000",
    "title_font_size": 15,
    "title_font_opacity": 255,
    "shadow_x_offset": 2,
    "shadow_y_offset": 2,
    "subtitle_font_size": 12,
    "subtitle_font_opacity": 220,
    "counter_font_size": 65,
    "counter_font_opacity": 255,
    "counter_anim_duration": 180,
    "shake_enabled": True,
    "shake_duration": 250,
    "shake_count": 20,
    "shake_intensity": 3,
    "combo_colors": COLOR_STR
}


CONFIG_TYPES = {k: type(v) for k, v in CONFIG_ITEMS.items()}


class ComboConfig:
    def __init__(self, values: dict = None):
        if values is None:
            values = dict()

        for key, default in CONFIG_ITEMS.items():
            if key in values:
                setattr(self, key, values[key])
            else:
                setattr(self, key, default)

    def copy(self) -> "ComboConfig":
        value_dict = {k: getattr(self, k) for k in CONFIG_ITEMS.keys()}
        return ComboConfig(value_dict)

    def get_zoom_scale(self) -> float:
        return self.zoom_scale_percent / 100
    
    def as_dict(self) -> dict:
        results = dict()
        for key in CONFIG_ITEMS.keys():
            results[key] = getattr(self, key)
        
        return results


CONFIG_NAMES = {
    "cooldown_duration": "Cooldown Duration",
    "reset_on_undo": "Reset Combo on Undo",
    "bg_color": "Background Color (Hex)",
    "bg_opacity": "Background Opacity (0-255)",
    "force_repaint": "Force Repaint (macOS)",
    "force_repaint_px": "Repaint Width (macOS)",
    "top_margin": "Counter Top Margin",
    "bottom_margin": "Counter Bottom Margin",
    "horz_margin": "Counter Horizontal Margin",
    "bar_width": "Cooldown Bar Thickness",
    "zoom_scale_percent": "Counter Normal to Enlarged Ratio",
    "alignment": "Widget Alignment",
    "font_name": "Font Name",
    "title_font_color": "Title Font Color (Hex)",
    "title_font_size": "Title Font Size",
    "title_font_opacity": "Title Font Opacity",
    "shadow_x_offset": "Title Shadow Horizontal (X) Offset",
    "shadow_y_offset": "Title Shadow Vertical (Y) Offset",
    "subtitle_font_size": "Highscore Font Size",
    "subtitle_font_opacity": "Highscore Font Opacity (Hex)",
    "counter_font_size": "Counter Font Size",
    "counter_font_opacity": "Counter Font Opacity",
    "counter_anim_duration": "Counter Animation Duration",
    "shake_enabled": "Enable Shake Animation",
    "shake_duration": "Shake Animation Duration",
    "shake_count": "Shake Speed",
    "shake_intensity": "Shake Intensity"
}


CONFIG_ORDER = [
    "Combo Settings",
    "reset_on_undo",
    "cooldown_duration",

    "Display Settings",
    "force_repaint",
    "force_repaint_px",
    "bg_color",
    "bg_opacity",
    "top_margin",
    "bottom_margin",
    "horz_margin",
    "bar_width",
    "zoom_scale_percent",
    "alignment",
    
    "Font Settings (Requires Plugin Restart)",
    "font_name",
    "title_font_color",
    "title_font_size",
    "title_font_opacity",
    "shadow_x_offset",
    "shadow_y_offset",
    "subtitle_font_size",
    "subtitle_font_opacity",
    "counter_font_size",
    "counter_font_opacity",

    "Animation Settings",
    "shake_enabled",
    "shake_duration",
    "shake_count",
    "shake_intensity",
    "counter_anim_duration"
]


CONFIG_RANGES = {
    "cooldown_duration": (100, 30000, 100, "ms"),
    "force_repaint_px": (1, 10, 1, "px"),
    "bg_opacity": (0, 255, 1, None),
    "top_margin": (-300, 300, 1, "px"),
    "bottom_margin": (-300, 300, 1, "px"),
    "horz_margin": (-300, 300, 1, "px"),
    "bar_width": (1, 300, 1, "px"),
    "zoom_scale_percent": (1, 100, 1, "%"),
    "title_font_size": (1, 300, 1, None),
    "title_font_opacity": (0, 255, 1, None),
    "shadow_x_offset": (-100, 100, 1, "px"),
    "shadow_y_offset": (-100, 100, 1, "px"),
    "subtitle_font_size": (1, 300, 1, None),
    "subtitle_font_opacity": (0, 255, 1, None),
    "counter_font_size": (1, 300, 1, None),
    "counter_font_opacity": (0, 255, 1, None),
    "counter_anim_duration": (10, 500, 10, "ms"),
    "shake_duration": (10, 500, 10, "ms"),
    "shake_count": (1, 100, 1, None),
    "shake_intensity": (1, 100, 1, "px")
}
