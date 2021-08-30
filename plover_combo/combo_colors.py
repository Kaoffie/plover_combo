from typing import Optional, List, Tuple, Dict

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QColor

BAR_ALPHA = 220
COLORS = {
    0:      (QColor(62, 167, 237),  QColor(106, 187, 241)),
    10:     (QColor(98, 221, 223),  QColor(136, 229, 231)),
    25:     (QColor(62, 221, 160),  QColor(99, 227, 178)),
    50:     (QColor(229, 189, 69),  QColor(235, 204, 112)),
    100:    (QColor(217, 114, 110), QColor(225, 145, 142)),
    250:    (QColor(227, 120, 166), QColor(234, 154, 188)),
    500:    (QColor(217, 61, 194),  QColor(225, 102, 206)),
    1000:   (QColor(147, 79, 219),  QColor(172, 120, 227)),
    2500:   (QColor(85, 81, 211),   QColor(128, 124, 222))
}


COLOR_STR = """0: #3EA7ED, #6ABBF1
10: #62DDDF, #88E5E7
25: #3EDDA0, #63E3B2
50: #E5BD45, #EBCC70
100: #D9726E, #E1918E
250: #E378A6, #EA9ABC
500: #D93DC2, #E166CE
1000: #934FDB, #AC78E3
2500: #5551D3, #807CDE"""


COLOR_FORMAT = """Format example:
0: #3EA7ED, #6ABBF1
10: #62DDDF, #88E5E7

Primary color affects the title shadow and counter, 
while the secondary color affects the highscore and cooldown bar.

Colors for 0 must be added."""


COLOR_NUMS = list(sorted(COLORS.keys()))


# def validate_string_hex(string: str) -> bool:
#     string = string.strip()
#     if len(string) != 7:
#         return False
    
#     if not string.startswith("#"):
#         return False
    
#     color_hex = string[1:]
#     color_int = int(color_hex, 16)
#     return color_int <= 0xFFFFFF


def string_hex_to_color(string: str, default: Optional[QColor], alpha: Optional[int] = None) -> QColor:
    string = string.strip()
    
    if not string.startswith("#") or len(string) != 7:
        return default

    try:
        color_hex = string[1:]
        color_int = int(color_hex, 16)
        return QColor(color_int)
    except ValueError:
        return default


def to_int(string: str) -> Optional[int]:
    try:
        return int(string)
    except ValueError:
        return None


def convert_str_color_config(string: str) -> Tuple[Dict[int, Tuple[QColor, QColor]], List[int]]:
    """
    Format:
    0: #AAAAAA, #BBBBBB
    1: #CCCCCC, #DDDDDD
    """
    color_dict = dict()
    color_list = []

    for line in string.split("\n"):
        if ":" not in line:
            continue
        
        num_str, colors_str = line.split(":", 1)
        num_int = to_int(num_str)
        if num_int is None or num_int < 0:
            continue
            
        if "," not in colors_str:
            continue
            
        pri_color_str, sec_color_str = colors_str.split(",", 1)
        pri_color = string_hex_to_color(pri_color_str, None)
        sec_color = string_hex_to_color(sec_color_str, None)

        if pri_color is None or sec_color is None:
            continue
            
        color_list.append(num_int)
        color_dict[num_int] = (pri_color, sec_color)
    
    if 0 not in color_dict:
        color_dict[0] = COLORS[0]
        color_list.append(0)
    
    return color_dict, sorted(color_list)


def round_to_checkpoint(num: int, color_nums: Optional[List[int]] = None) -> int:    
    if num <= 0:
        return 0

    if color_nums is None:
        color_nums = COLOR_NUMS

    prev = 0
    for color_num in color_nums:
        if num < color_num:
            return prev
        
        prev = color_num
    
    return prev


def set_label_color(label: QLabel, color: QColor) -> None:
    values = "{r}, {g}, {b}, {a}".format(
        r = color.red(),
        g = color.green(),
        b = color.blue(),
        a = color.alpha()
    )

    label.setStyleSheet(f"color: rgba({values});")


if __name__ == "__main__":
    conf, l = convert_str_color_config(COLOR_STR)
    for num, (pri, sec) in conf.items():
        print(f"{num}: {hex(pri.rgb())}, {hex(sec.rgb())}")

    print(l)