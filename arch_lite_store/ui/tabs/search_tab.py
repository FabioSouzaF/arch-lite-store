"""
SearchTab — aba "Buscar Pacotes".

Responsabilidades:
  - Filtros de fonte (Pacman, AUR, Flatpak)
  - Campo de busca + botão
  - Lista de resultados (botões Info/Instalar inline em cada linha)
  - Log de progresso de download de ícones
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget,
    QLabel, QCheckBox,
)
from PySide6.QtCore import QSize

_STYLE_LIST = "QListWidget::item { border-bottom: 1px solid #ddd; }"


class SearchTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        layout.addLayout(self._criar_filtros())
        layout.addLayout(self._criar_barra_busca())
        layout.addWidget(self._criar_status())
        layout.addWidget(self._criar_lista())
        layout.addWidget(self._criar_icon_log())

    # ------------------------------------------------------------------ #

    def _criar_filtros(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.addWidget(QLabel("<b>Buscar em:</b>"))

        self.chk_pacman = QCheckBox("Pacman (Oficiais)")
        self.chk_pacman.setChecked(True)

        self.chk_aur = QCheckBox("AUR (Comunidade)")
        self.chk_aur.setChecked(True)

        self.chk_flatpak = QCheckBox("Flatpak (Flathub)")
        self.chk_flatpak.setChecked(True)

        row.addWidget(self.chk_pacman)
        row.addWidget(self.chk_aur)
        row.addWidget(self.chk_flatpak)
        row.addStretch()
        return row

    def _criar_barra_busca(self) -> QHBoxLayout:
        row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar aplicativos por nome...")
        self.search_button = QPushButton("Buscar")
        row.addWidget(self.search_input)
        row.addWidget(self.search_button)
        return row

    def _criar_status(self) -> QLabel:
        self.status_label = QLabel("Pronto para buscar.")
        return self.status_label

    def _criar_lista(self) -> QListWidget:
        self.results_list = QListWidget()
        self.results_list.setStyleSheet(_STYLE_LIST)
        return self.results_list

    def _criar_icon_log(self) -> QLabel:
        self.icon_log_label = QLabel("")
        self.icon_log_label.setStyleSheet("color: gray; font-size: 11px;")
        return self.icon_log_label
