from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QColor

# I am way too lazy to make this configurable.
BAR_ALPHA = 220
COLORS = {
    0:      (QColor(62, 167, 237),  QColor(106, 187, 241, BAR_ALPHA)),
    10:     (QColor(98, 221, 223),  QColor(136, 229, 231, BAR_ALPHA)),
    25:     (QColor(62, 221, 160),  QColor(99, 227, 178, BAR_ALPHA)),
    50:     (QColor(229, 189, 69),  QColor(235, 204, 112, BAR_ALPHA)),
    100:    (QColor(217, 114, 110), QColor(225, 145, 142, BAR_ALPHA)),
    250:    (QColor(227, 120, 166), QColor(234, 154, 188, BAR_ALPHA)),
    500:    (QColor(217, 61, 194),  QColor(225, 102, 206, BAR_ALPHA)),
    1000:   (QColor(147, 79, 219),  QColor(172, 120, 227, BAR_ALPHA)),
    2500:   (QColor(85, 81, 211),   QColor(128, 124, 222, BAR_ALPHA))
}


COLOR_NUMS = list(sorted(COLORS.keys()))


def round_to_checkpoint(num: int) -> int:
    if num <= 0:
        return 0

    prev = 0
    for color_num in COLOR_NUMS:
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