"""
UpdatesTab — aba "Atualizações".

Responsabilidades:
  - Label de status da verificação
  - Lista de pacotes com update disponível
  - Botões "Verificar" e "Atualizar Todo o Sistema"
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel,
)
from PySide6.QtCore import QSize


_STYLE_BTN_ATUALIZAR = "background-color: #4CAF50; color: white; font-weight: bold;"


class UpdatesTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        layout.addWidget(self._criar_status())
        layout.addWidget(self._criar_lista())
        layout.addLayout(self._criar_botoes())

    # ------------------------------------------------------------------ #

    def _criar_status(self) -> QLabel:
        self.status_atualizacoes = QLabel(
            "Clique no botão abaixo para verificar atualizações pendentes."
        )
        return self.status_atualizacoes

    def _criar_lista(self) -> QListWidget:
        self.update_list = QListWidget()
        self.update_list.setIconSize(QSize(32, 32))
        self.update_list.setStyleSheet(
            "QListWidget::item { border-bottom: 1px solid #eee; padding: 5px; }"
        )
        return self.update_list

    def _criar_botoes(self) -> QHBoxLayout:
        row = QHBoxLayout()

        self.check_updates_button = QPushButton("Verificar Atualizações")
        self.check_updates_button.setMinimumHeight(40)

        self.sys_update_button = QPushButton("Atualizar Todo o Sistema")
        self.sys_update_button.setEnabled(False)
        self.sys_update_button.setMinimumHeight(40)
        self.sys_update_button.setStyleSheet(_STYLE_BTN_ATUALIZAR)

        row.addWidget(self.check_updates_button, 1)
        row.addWidget(self.sys_update_button, 2)
        return row
