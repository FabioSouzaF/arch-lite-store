"""
InstalledTab — aba "Pacotes Instalados".

Responsabilidades:
  - Campo de filtro por nome
  - Contador/status
  - Lista de pacotes instalados (botões Info/Remover inline em cada linha)
  - Botão "Recarregar Lista"
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QLabel,
)

_STYLE_LIST = "QListWidget::item { border-bottom: 1px solid #ddd; }"
_STYLE_BTN_REFRESH = "QPushButton { padding: 6px 16px; }"


class InstalledTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        layout.addWidget(self._criar_filtro())
        layout.addWidget(self._criar_status())
        layout.addWidget(self._criar_lista())
        layout.addLayout(self._criar_botoes())

    # ------------------------------------------------------------------ #

    def _criar_filtro(self) -> QLineEdit:
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText(
            "Filtrar instalados por nome (Dica: Clique duplo para ver detalhes)..."
        )
        return self.filter_input

    def _criar_status(self) -> QLabel:
        self.status_instalados = QLabel("Carregando pacotes locais...")
        return self.status_instalados

    def _criar_lista(self) -> QListWidget:
        self.installed_list = QListWidget()
        self.installed_list.setStyleSheet(_STYLE_LIST)
        return self.installed_list

    def _criar_botoes(self) -> QHBoxLayout:
        row = QHBoxLayout()
        self.refresh_button = QPushButton("⟳  Recarregar Lista")
        self.refresh_button.setMinimumHeight(36)
        self.refresh_button.setStyleSheet(_STYLE_BTN_REFRESH)
        row.addStretch()
        row.addWidget(self.refresh_button)
        return row
