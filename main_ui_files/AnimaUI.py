from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from modules.BaseWidget import BaseWidget
from modules.DragDropLineEdit import DragDropLineEdit


class AnimaWidget(BaseWidget):
    Toggled = Signal(bool)

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("Anima Args")
        self.name = "anima_args"

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.content.setLayout(QVBoxLayout())
        self.content.layout().setContentsMargins(0, 0, 0, 0)

        self.anima_training_box = QGroupBox("Train Anima")
        self.anima_training_box.setCheckable(True)
        self.anima_training_box.setChecked(False)
        self.content.layout().addWidget(self.anima_training_box)

        self.main_layout = QGridLayout(self.anima_training_box)
        self.main_layout.setContentsMargins(8, 8, 8, 8)

        selector_icon = QIcon(str(Path("icons/folder.svg")))

        self.qwen3_input = DragDropLineEdit(self.anima_training_box)
        self.qwen3_input.setMode("file", [".safetensors", ".pt", ".pth", ".ckpt", ".bin"])
        self.qwen3_input.highlight = True
        self.qwen3_selector = QPushButton(self.anima_training_box)
        self.qwen3_selector.setIcon(selector_icon)

        self.qwen3_max_token_input = QSpinBox(self.anima_training_box)
        self.qwen3_max_token_input.setRange(1, 4096)
        self.qwen3_max_token_input.setValue(512)

        self.t5_max_token_input = QSpinBox(self.anima_training_box)
        self.t5_max_token_input.setRange(1, 4096)
        self.t5_max_token_input.setValue(512)

        self.attn_mode_selector = QComboBox(self.anima_training_box)
        self.attn_mode_selector.addItems(["Auto", "Torch", "Xformers", "Flash"])

        self.split_attn_enable = QCheckBox("Split Attention", self.anima_training_box)

        self.timestep_sampling_selector = QComboBox(self.anima_training_box)
        self.timestep_sampling_selector.addItems(["Sigmoid", "Sigma", "Uniform", "Shift", "Flux Shift"])

        self.discrete_flow_shift_input = QDoubleSpinBox(self.anima_training_box)
        self.discrete_flow_shift_input.setRange(0.0, 8.0)
        self.discrete_flow_shift_input.setDecimals(3)
        self.discrete_flow_shift_input.setSingleStep(0.05)
        self.discrete_flow_shift_input.setValue(1.0)

        self.sigmoid_scale_input = QDoubleSpinBox(self.anima_training_box)
        self.sigmoid_scale_input.setRange(0.0, 8.0)
        self.sigmoid_scale_input.setDecimals(3)
        self.sigmoid_scale_input.setSingleStep(0.05)
        self.sigmoid_scale_input.setValue(1.0)

        self.vae_chunk_size_enable = QCheckBox("VAE Chunk Size", self.anima_training_box)
        self.vae_chunk_size_input = QSpinBox(self.anima_training_box)
        self.vae_chunk_size_input.setRange(2, 1024)
        self.vae_chunk_size_input.setSingleStep(2)
        self.vae_chunk_size_input.setValue(64)
        self.vae_chunk_size_input.setEnabled(False)

        self.vae_disable_cache_enable = QCheckBox("Disable VAE Cache", self.anima_training_box)

        self.add_file_row(0, "Qwen3", self.qwen3_input, self.qwen3_selector)
        self.main_layout.addWidget(QLabel("Qwen3 Max Token"), 1, 0)
        self.main_layout.addWidget(self.qwen3_max_token_input, 1, 1)
        self.main_layout.addWidget(QLabel("T5 Max Token"), 2, 0)
        self.main_layout.addWidget(self.t5_max_token_input, 2, 1)
        self.main_layout.addWidget(QLabel("Attention Mode"), 3, 0)
        self.main_layout.addWidget(self.attn_mode_selector, 3, 1)
        self.main_layout.addWidget(self.split_attn_enable, 4, 1)
        self.main_layout.addWidget(QLabel("Timestep Sampling"), 5, 0)
        self.main_layout.addWidget(self.timestep_sampling_selector, 5, 1)
        self.main_layout.addWidget(QLabel("Discrete Flow Shift"), 6, 0)
        self.main_layout.addWidget(self.discrete_flow_shift_input, 6, 1)
        self.main_layout.addWidget(QLabel("Sigmoid Scale"), 7, 0)
        self.main_layout.addWidget(self.sigmoid_scale_input, 7, 1)
        self.main_layout.addWidget(self.vae_chunk_size_enable, 8, 0)
        self.main_layout.addWidget(self.vae_chunk_size_input, 8, 1)
        self.main_layout.addWidget(self.vae_disable_cache_enable, 9, 1)

    def add_file_row(
        self, row: int, label_text: str, line_edit: DragDropLineEdit, selector: QPushButton
    ) -> None:
        line_layout = QHBoxLayout()
        line_layout.setContentsMargins(0, 0, 0, 0)
        line_layout.addWidget(line_edit)
        line_layout.addWidget(selector)
        self.main_layout.addWidget(QLabel(label_text), row, 0)
        self.main_layout.addLayout(line_layout, row, 1)

    def setup_connections(self) -> None:
        self.anima_training_box.clicked.connect(self.enable_disable)
        self.qwen3_input.textChanged.connect(lambda x: self.edit_args("qwen3", x))
        self.qwen3_selector.clicked.connect(
            lambda: self.set_file_from_dialog(self.qwen3_input, "Qwen3 Text Encoder", "Qwen3 Model")
        )
        self.qwen3_max_token_input.valueChanged.connect(
            lambda x: self.edit_args("qwen3_max_token_length", x)
        )
        self.t5_max_token_input.valueChanged.connect(lambda x: self.edit_args("t5_max_token_length", x))
        self.attn_mode_selector.currentTextChanged.connect(self.change_attn_mode)
        self.split_attn_enable.clicked.connect(lambda x: self.edit_args("split_attn", x, True))
        self.timestep_sampling_selector.currentTextChanged.connect(self.change_timestep_sampling)
        self.discrete_flow_shift_input.valueChanged.connect(
            lambda x: self.edit_args(
                "discrete_flow_shift",
                x if self.discrete_flow_shift_input.isEnabled() else False,
                True,
            )
        )
        self.sigmoid_scale_input.valueChanged.connect(
            lambda x: self.edit_args("sigmoid_scale", x if self.sigmoid_scale_input.isEnabled() else False, True)
        )
        self.vae_chunk_size_enable.clicked.connect(self.toggle_vae_chunk)
        self.vae_chunk_size_input.valueChanged.connect(
            lambda x: self.edit_vae_chunk_size(x if self.vae_chunk_size_enable.isChecked() else False)
        )
        self.vae_disable_cache_enable.clicked.connect(
            lambda x: self.edit_args("vae_disable_cache", x, True)
        )

    def enable_disable(self, checked: bool) -> None:
        self.args = {}
        self.Toggled.emit(checked)
        if not checked:
            return
        self.edit_args("anima_mode", True)
        self.edit_args("qwen3", self.qwen3_input.text())
        self.edit_args("qwen3_max_token_length", self.qwen3_max_token_input.value())
        self.edit_args("t5_max_token_length", self.t5_max_token_input.value())
        self.change_attn_mode(self.attn_mode_selector.currentText())
        self.edit_args("split_attn", self.split_attn_enable.isChecked(), True)
        self.change_timestep_sampling(self.timestep_sampling_selector.currentText())
        self.toggle_vae_chunk(self.vae_chunk_size_enable.isChecked())
        self.edit_args("vae_disable_cache", self.vae_disable_cache_enable.isChecked(), True)

    def external_enable_disable(self, checked: bool) -> None:
        self.args = {}
        self.anima_training_box.setEnabled(not checked)
        if self.anima_training_box.isEnabled() and self.anima_training_box.isChecked():
            self.enable_disable(True)

    def change_attn_mode(self, value: str) -> None:
        value = value.lower()
        self.edit_args("attn_mode", value if value != "auto" else False, True)

    def change_timestep_sampling(self, value: str) -> None:
        value = value.lower().replace(" ", "_")
        self.discrete_flow_shift_input.setEnabled(value == "shift")
        self.sigmoid_scale_input.setEnabled(value in {"sigmoid", "shift", "flux_shift"})
        self.edit_args("timestep_sampling", value)
        self.edit_args(
            "discrete_flow_shift",
            self.discrete_flow_shift_input.value() if self.discrete_flow_shift_input.isEnabled() else False,
            True,
        )
        self.edit_args(
            "sigmoid_scale",
            self.sigmoid_scale_input.value() if self.sigmoid_scale_input.isEnabled() else False,
            True,
        )

    def toggle_vae_chunk(self, checked: bool) -> None:
        self.vae_chunk_size_input.setEnabled(checked)
        self.edit_vae_chunk_size(self.vae_chunk_size_input.value() if checked else False)

    def edit_vae_chunk_size(self, value: int | bool) -> None:
        if isinstance(value, int) and value % 2 != 0:
            value += 1
            self.vae_chunk_size_input.setValue(value)
        self.edit_args("vae_chunk_size", value, True)

    def load_args(self, args: dict) -> bool:
        args = args.get(self.name, {})
        self.anima_training_box.setChecked(bool(args))
        self.qwen3_input.setText(args.get("qwen3", ""))
        self.qwen3_max_token_input.setValue(args.get("qwen3_max_token_length", 512))
        self.t5_max_token_input.setValue(args.get("t5_max_token_length", 512))
        self.attn_mode_selector.setCurrentText(args.get("attn_mode", "Auto").capitalize())
        self.split_attn_enable.setChecked(args.get("split_attn", False))
        self.timestep_sampling_selector.setCurrentText(
            " ".join([x.capitalize() for x in args.get("timestep_sampling", "sigmoid").split("_")])
        )
        self.discrete_flow_shift_input.setValue(args.get("discrete_flow_shift", 1.0))
        self.sigmoid_scale_input.setValue(args.get("sigmoid_scale", 1.0))
        self.vae_chunk_size_enable.setChecked(bool(args.get("vae_chunk_size", False)))
        self.vae_chunk_size_input.setValue(args.get("vae_chunk_size", 64))
        self.vae_disable_cache_enable.setChecked(args.get("vae_disable_cache", False))
        self.enable_disable(self.anima_training_box.isChecked())
        return True
