from PyQt5.QtWidgets import (
    QDialog, QWidget, QLabel, QSpinBox, 
    QComboBox, QDialogButtonBox, QGridLayout,
    QGroupBox, QCheckBox, QVBoxLayout,
    QLineEdit, QScrollArea, QSizePolicy,
    QPlainTextEdit, QSizePolicy
)
from PyQt5.QtCore import Qt

from plover_combo.combo_config import (
    ComboAlignment, ComboConfig, CONFIG_NAMES, CONFIG_ORDER, 
    CONFIG_TYPES, CONFIG_RANGES, ALIGNMENT_OPTIONS
)
from plover_combo.combo_colors import COLOR_FORMAT


FIELD_DATA_WIDTH = 250
PLAIN_TEXT_DATA_HEIGHT = 200


class ConfigUI(QDialog):

    def __init__(self, temp_config: ComboConfig, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.temp_config = temp_config
        self.setup_window()

    def setup_window(self) -> None:
        self.scroll_widget = QWidget()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_layout = QVBoxLayout()
        self.fields = dict()

        current_grid_row = 0
        current_grid_layout: QGridLayout = None
        current_groupbox: QGroupBox = None

        for config_name in CONFIG_ORDER:
            if config_name not in CONFIG_NAMES:
                if current_groupbox is not None:
                    current_groupbox.setLayout(current_grid_layout)
                    self.scroll_layout.addWidget(current_groupbox)
                
                current_grid_row = 0
                current_groupbox = QGroupBox()
                current_groupbox.setTitle(config_name)
                current_grid_layout = QGridLayout()
                continue
            
            field_label = QLabel()
            field_label.setText(CONFIG_NAMES[config_name])

            field_type = CONFIG_TYPES[config_name]
            field_data = None

            if field_type == bool:
                field_data = QCheckBox()
                field_data.setChecked(getattr(self.temp_config, config_name))

            elif field_type == int:
                low, high, step, suffix = CONFIG_RANGES[config_name]
                field_data = QSpinBox()
                field_data.setRange(low, high)
                field_data.setSingleStep(step)
                field_data.setSuffix(suffix)
                field_data.setValue(getattr(self.temp_config, config_name))

            elif field_type == str:
                field_data = QLineEdit()
                field_data.setText(getattr(self.temp_config, config_name))

            elif field_type == ComboAlignment:
                field_data = QComboBox()
                field_data.addItems(ALIGNMENT_OPTIONS)
                field_data.setCurrentIndex(
                    getattr(self.temp_config, config_name).value
                )

            if field_data is not None:
                field_data.setMinimumWidth(FIELD_DATA_WIDTH)
                current_grid_layout.addWidget(
                    field_label, current_grid_row, 0, 1, 1, Qt.AlignRight
                )
                current_grid_layout.addWidget(
                    field_data, current_grid_row, 1, 1, 1, Qt.AlignLeft
                )

                self.fields[config_name] = field_data
                current_grid_row += 1

        if current_groupbox is not None:
            current_groupbox.setLayout(current_grid_layout)
            self.scroll_layout.addWidget(current_groupbox)

        combo_color_group = QGroupBox()
        combo_color_group.setTitle("Combo Colors")
        combo_color_layout = QVBoxLayout()

        combo_color_label = QLabel()
        combo_color_label.setText(COLOR_FORMAT)
        combo_color_layout.addWidget(combo_color_label)

        combo_color_data = QPlainTextEdit()
        combo_color_data.setPlainText(self.temp_config.combo_colors)
        combo_color_data.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        combo_color_data.setFixedHeight(PLAIN_TEXT_DATA_HEIGHT)
        combo_color_layout.addWidget(combo_color_data)
        self.fields["combo_colors"] = combo_color_data

        combo_color_group.setLayout(combo_color_layout)
        self.scroll_layout.addWidget(combo_color_group)

        self.button_box = QDialogButtonBox(
            (
                QDialogButtonBox.Cancel | 
                QDialogButtonBox.Ok
            ),
            parent=self
        )
        self.button_box.rejected.connect(self.reject)
        self.button_box.accepted.connect(self.save_settings)

        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def save_settings(self) -> None:
        for config_name in CONFIG_NAMES.keys():
            field_type = CONFIG_TYPES[config_name]
            field_data = self.fields[config_name]
            field_value = None

            if field_type == bool:
                field_value = field_data.isChecked()
            elif field_type == int:
                field_value = field_data.value()
            elif field_type == str:
                field_value = field_data.text()
            elif field_type == ComboAlignment:
                field_value = ComboAlignment(field_data.currentIndex())

            if field_value is not None:
                setattr(self.temp_config, config_name, field_value)
        
        self.temp_config.combo_colors = self.fields["combo_colors"].toPlainText()
        self.accept()
