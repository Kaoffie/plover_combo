import random
import sys

from plover.engine import StenoEngine
from plover.gui_qt.tool import Tool
from plover.gui_qt.utils import ToolBar
from plover.steno import Stroke

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QGraphicsView, 
    QGraphicsScene, QApplication, QGraphicsTextItem,
    QGridLayout, QLabel, QSpacerItem, QSizePolicy,
    QGraphicsDropShadowEffect, QAction
)
from PyQt5.QtGui import (
    QMouseEvent, QFont, QKeyEvent, QPen, QBrush, 
    QFontDatabase, QColor, QKeySequence, QPainter,
    QPaintEvent
)
from PyQt5.QtCore import (
    Qt, QPoint, QVariantAnimation, QRectF, QSettings,
    QTimer
)

from plover_combo.combo_colors import (
    COLORS, round_to_checkpoint, set_label_color
)
from plover_combo.combo_config import (
    CONFIG_ITEMS, CONFIG_TYPES, ComboAlignment, 
    ComboConfig
)
from plover_combo.config_ui import ConfigUI
from plover_combo.resources_rc import *


STYLESHEET = "border:0px; background:transparent;"


class ComboTool(Tool):
    TITLE = "Combo Counter"
    ICON = ":/combo/icon.svg"
    ROLE = "combo"

    def __init__(self, engine: StenoEngine) -> None:
        super().__init__(engine)
        self.setObjectName("combo")
        engine.signal_connect("stroked", self.on_stroke)

        QFontDatabase.addApplicationFont(":/combo/PloverRetro.ttf")

        self.drag_position = QPoint()
        self.counter = 0
        self.setting_highscore = False

        self.config = ComboConfig()
        self.restore_state()

        self.reload_config()
        self.setup_actions()
        self.setup_header()
        self.setup_counter()
        self.setup_cooldown_bar()
        self.setup_layout()

        self.finished.connect(self.save_state)

        self.timer = QTimer()


    def _restore_state(self, settings: QSettings) -> None:
        for field_name in CONFIG_ITEMS.keys():
            if settings.contains(field_name):
                setattr(
                    self.config, 
                    field_name, 
                    settings.value(field_name, type=CONFIG_TYPES[field_name])
                )

    def _save_state(self, settings: QSettings) -> None:
        for key, value in self.config.as_dict().items():
            settings.setValue(key, value)

    def paint_event(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setCompositionMode(QPainter.CompositionMode_Overlay)

        if self.config.dark_mode:
            painter.fillRect(self.rect(), QColor(0, 0, 0, alpha=self.config.bg_opacity))
        else:
            painter.fillRect(self.rect(), QColor(255, 255, 255, alpha=self.config.bg_opacity))

    def on_settings(self) -> None:
        config_dialog = ConfigUI(self.config.copy(), self)
        if config_dialog.exec():
            self.config = config_dialog.temp_config
            self.reload_config()
    
    def on_stroke(self, stroke: Stroke) -> None:
        if self.config.reset_on_undo and stroke.is_correction:
            self.reset_counter()
            return
        
        self.increment_counter()

    def on_translate(self, undo: list, do: list, _) -> None:
        if self.config.reset_on_undo and len(undo) == 1:
            self.reset_counter()
            return
        
        self.increment_counter()

    def reload_config(self) -> None:
        self.zoom_scale = self.config.get_zoom_scale()
        self.counter_font = QFont(self.config.font_name, self.config.counter_font_size)
        self.title_font = QFont(self.config.font_name, self.config.title_font_size)
        self.subtitle_font = QFont(self.config.font_name, self.config.subtitle_font_size)
        self.main_color, self.sub_color = COLORS[0]

        if hasattr(self, "combo_header"):
            if self.config.dark_mode:
                set_label_color(self.combo_header, QColor(Qt.white))
            else:
                set_label_color(self.combo_header, QColor(Qt.black))

        if hasattr(self, "combo_header_shadow"):
            self.combo_header_shadow.setXOffset(self.config.shadow_x_offset)
            self.combo_header_shadow.setYOffset(self.config.shadow_y_offset)

    def setup_actions(self) -> None:
        self.close_action = QAction(self)
        self.close_action.setText("Close Widget")
        self.close_action.triggered.connect(self.accept)
        self.close_action.setShortcut(QKeySequence("Ctrl+X"))
        self.addAction(self.close_action)

        self.settings_action = QAction(self)
        self.settings_action.setText("Configure Widget")
        self.settings_action.triggered.connect(self.on_settings)
        self.settings_action.setShortcut(QKeySequence("Ctrl+S"))
        self.addAction(self.settings_action)

    def setup_header(self) -> None:
        self.combo_header = QLabel(self)
        self.combo_header.setText("Combo")
        self.combo_header.setFont(self.title_font)
        if self.config.dark_mode:
            set_label_color(self.combo_header, QColor(Qt.white))
        else:
            set_label_color(self.combo_header, QColor(Qt.black))

        self.combo_header_shadow = QGraphicsDropShadowEffect()
        self.combo_header_shadow.setBlurRadius(0)
        self.combo_header_shadow.setXOffset(self.config.shadow_x_offset)
        self.combo_header_shadow.setYOffset(self.config.shadow_y_offset)
        self.combo_header_shadow.setColor(self.main_color)
        self.combo_header.setGraphicsEffect(self.combo_header_shadow)
        
        self.highscore_header = QLabel(self)
        self.highscore_header.setText(f"HI {self.config.highscore}")
        self.highscore_header.setFont(self.subtitle_font)
        set_label_color(self.highscore_header, self.sub_color)

    def setup_counter(self) -> None:
        self.text_view = QGraphicsView(self)
        self.text_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_view.setStyleSheet(STYLESHEET)

        self.text_scene = QGraphicsScene(self)
        self.text_view.setScene(self.text_scene)
        self.counter_text = self.text_scene.addText(str(self.counter), self.counter_font)
        self.counter_text.setPos(self.config.horz_margin, self.config.top_margin)
        self.counter_text.setDefaultTextColor(self.main_color)

        self.text_view.mouseMoveEvent = self.view_mouse_move
        self.text_view.mousePressEvent = self.view_mouse_press
    
    def setup_cooldown_bar(self) -> None:
        self.cooldown_view = QGraphicsView(self)
        self.cooldown_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.cooldown_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.cooldown_view.setStyleSheet(STYLESHEET)

        self.cooldown_scene = QGraphicsScene(self)
        self.cooldown_view.setScene(self.cooldown_scene)
        self.cooldown_pen = QPen(Qt.NoPen)
        self.cooldown_brush = QBrush(self.sub_color)
        self.cooldown_bar = self.cooldown_scene.addRect(
            QRectF(),
            self.cooldown_pen,
            self.cooldown_brush
        )

        self.cooldown_view.mouseMoveEvent = self.view_mouse_move
        self.cooldown_view.mousePressEvent = self.view_mouse_press

    def setup_layout(self) -> None:
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("QWidget#combo {background:transparent;}")

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 10, 0, 10)
        self.layout.addWidget(self.combo_header, 0, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.highscore_header, 1, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.text_view, 2, 0, 2, 1)
        self.layout.addWidget(self.cooldown_view, 3, 0, 1, 1)
        self.setLayout(self.layout)

        self.mouseMoveEvent = self.view_mouse_move
        self.mousePressEvent = self.view_mouse_press
        self.paintEvent = self.paint_event

        self.animate()
        self.show()

    def view_mouse_move(self, event: QMouseEvent) -> None:
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)

    def view_mouse_press(self, event: QMouseEvent) -> None:
        if event.buttons() & Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
    
    def increment_counter(self) -> None:
        self.counter += 1
        shaked = False

        if self.counter in COLORS:
            self.update_colors()
        
        self.animate()

        if self.counter in COLORS and self.counter > 0:
            shaked = True
            self.animate_shake()

        if self.counter > self.config.highscore:
            self.config.highscore = self.counter
            self.highscore_header.setText(f"HI {self.config.highscore}")
            if not (self.setting_highscore or shaked):
                self.animate_shake()

            self.setting_highscore = True
    
    def reset_counter(self) -> None:
        self.counter = 0
        if hasattr(self, "cooldown_animation") and self.cooldown_animation is not None:
            self.cooldown_animation.stop()
            self.cooldown_bar.setRect(QRectF())

        self.setting_highscore = False
        self.update_colors()
        self.animate()
    
    def update_colors(self) -> None:
        color_index = self.counter
        if self.counter not in COLORS:
            color_index = round_to_checkpoint(self.counter)
        
        self.main_color, self.sub_color = COLORS.get(color_index)
        self.combo_header_shadow.setColor(self.main_color)
        set_label_color(self.highscore_header, self.sub_color)
        self.counter_text.setDefaultTextColor(self.main_color)
        self.cooldown_brush.setColor(self.sub_color)
        self.cooldown_bar.setBrush(self.cooldown_brush)

    def animate(self) -> None:
        self.counter_text.setPlainText(str(self.counter))
        self.adjust_window()
        self.animate_counter()
        self.animate_cooldown()

    def adjust_window(self) -> None:
        text_bound = self.counter_text.boundingRect()
        self.text_width = text_bound.width()
        self.text_height = text_bound.height()

        self.width = int(self.text_width + self.config.horz_margin * 2)
        self.height = int(self.text_height + self.config.top_margin + self.config.bottom_margin)

        prev_geometry = self.frameGeometry()
        self.setFixedWidth(self.width)
        self.text_view.setFixedSize(self.width, self.height)
        self.text_scene.setSceneRect(0, 0, self.width, self.height)
        self.cooldown_view.setFixedSize(self.width, self.config.bar_width)
        self.cooldown_scene.setSceneRect(0, 0, self.width, self.config.bar_width)

        if self.config.alignment == ComboAlignment.CENTER:
            self.move(self.pos() - self.frameGeometry().center() + prev_geometry.center())
        elif self.config.alignment == ComboAlignment.RIGHT:
            self.move(self.pos() - self.frameGeometry().topRight() + prev_geometry.topRight())
        elif self.config.alignment == ComboAlignment.LEFT:
            self.move(self.pos() - self.frameGeometry().topLeft() + prev_geometry.topLeft())
        
        self.update()

    def animate_counter(self) -> None:
        self.counter_animation: QVariantAnimation
        if hasattr(self, "counter_animation") and self.counter_animation is not None:
            self.counter_animation.stop()
        
        self.counter_animation = QVariantAnimation(self.text_view)
        self.counter_animation.setStartValue(QRectF(
            self.width * (1.0 - self.zoom_scale) * 0.5, 
            self.height * (1.0 - self.zoom_scale), 
            self.width * self.zoom_scale, 
            self.height * self.zoom_scale
        ))
        self.counter_animation.setEndValue(QRectF(
            0, 0, self.width, self.height
        ))
        
        self.counter_animation.valueChanged.connect(
            lambda x: self.text_view.fitInView(x, Qt.KeepAspectRatio)
        )

        self.counter_animation.setDuration(self.config.counter_anim_duration)
        self.counter_animation.start()

    def animate_cooldown(self) -> None:
        if self.counter == 0:
            return

        self.cooldown_animation: QVariantAnimation
        if hasattr(self, "cooldown_animation") and self.cooldown_animation is not None:
            self.cooldown_animation.stop()
        
        self.cooldown_animation = QVariantAnimation(self.cooldown_view)
        self.cooldown_view.fitInView(QRectF(0, 0, self.width, self.config.bar_width))
        self.cooldown_animation.setStartValue(QRectF(
            self.config.horz_margin, 0, self.text_width, self.config.bar_width
        ))
        self.cooldown_animation.setEndValue(QRectF(
            self.width/2, 0, 0, self.config.bar_width
        ))
        self.cooldown_animation.valueChanged.connect(
            lambda x: self.cooldown_bar.setRect(x)
        )
        self.cooldown_animation.finished.connect(self.reset_counter)

        self.cooldown_animation.setDuration(self.config.cooldown_duration)
        self.cooldown_animation.start()
    
    def animate_shake(self) -> None:
        if not self.config.shake_enabled:
            return

        shake_animation = QVariantAnimation(self)

        animation_time = 0.0
        shake_interval = 1.0 / self.config.shake_count
        for count in range(self.config.shake_count):
            shake_animation.setKeyValueAt(
                animation_time, 
                QPoint(
                    self.pos().x() + random.randint(-1, 1) * self.config.shake_intensity,
                    self.pos().y() + random.randint(-1, 1) * self.config.shake_intensity,
                )
            )
            animation_time += shake_interval
        
        shake_animation.valueChanged.connect(
            lambda x: self.move(x)
        )
        shake_animation.setEndValue(QPoint(self.pos()))
        shake_animation.setDuration(self.config.shake_duration)
        shake_animation.start()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ComboTool()

#     app.exec()
