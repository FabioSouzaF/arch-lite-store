"""
PackageItemWidget — linha da lista com botões inline.
Layout: [ícone] [badge + nome + descrição] [Info] [Instalar/Remover]
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QIcon, QPixmap

# _BADGE_CORES = {"Pacman": "#1793d1", "AUR": "#f08000", "Flatpak": "#4a90d9"}
_BADGE_CORES = {
    "Pacman": "#1793d1",   # Azul oficial do Arch Linux
    "AUR": "#ff6600",      # Laranja oficial do AUR
    "Flatpak": "#4CAF50"   # Verde oficial do logotipo do Flatpak
}

_ICONES_PADRAO = {
    "Pacman": "system-software-install",
    "AUR": "emblem-system",
    "Flatpak": "application-x-executable",
}

_CSS_INFO = (
    "QPushButton{background:#4a6fa5;color:white;border:none;border-radius:4px;"
    "padding:3px 8px;font-size:11px;}"
    "QPushButton:hover{background:#5a80b8;}"
)
_CSS_INSTALAR = (
    "QPushButton{background:#4CAF50;color:white;border:none;border-radius:4px;"
    "padding:3px 8px;font-size:11px;font-weight:bold;}"
    "QPushButton:hover{background:#00C853;}"
)
_CSS_REMOVER = (
    "QPushButton{background:#922b21;color:white;border:none;border-radius:4px;"
    "padding:3px 8px;font-size:11px;font-weight:bold;}"
    "QPushButton:hover{background:#c0392b;}"
)


class PackageItemWidget(QWidget):
    info_requested   = Signal(dict)
    action_requested = Signal(dict)

    def __init__(self, pacote: dict, modo: str = "instalar", parent=None):
        super().__init__(parent)
        self.pacote = pacote
        self._montar_layout(modo)

    # ------------------------------------------------------------------ #

    def _montar_layout(self, modo: str):
        row = QHBoxLayout(self)
        row.setContentsMargins(8, 5, 8, 5)
        row.setSpacing(10)

        # Ícone
        self._icon_lbl = QLabel()
        self._icon_lbl.setFixedSize(48, 48)
        self._icon_lbl.setAlignment(Qt.AlignCenter)
        self._set_icone_padrao()
        row.addWidget(self._icon_lbl)

        # Texto
        col = QVBoxLayout()
        col.setSpacing(2)

        tipo  = self.pacote.get("tipo", "")
        nome  = self.pacote.get("nome", "")
        versao = self.pacote.get("versao", "")
        cor   = _BADGE_CORES.get(tipo, "#888")
        ver_html = (
            f'&nbsp;<span style="color:#999;font-size:10px;">({versao})</span>'
            if versao and versao not in ("Estável", "N/A") else ""
        )
        nome_lbl = QLabel(
            f'<span style="background:{cor};color:white;padding:1px 5px;'
            f'border-radius:3px;font-size:10px;">{tipo}</span>'
            f'&nbsp;<b>{nome}</b>{ver_html}'
        )
        nome_lbl.setTextFormat(Qt.RichText)

        exibicao = self.pacote.get("exibicao", "")
        desc = exibicao.split("\n", 1)[1] if "\n" in exibicao else ""
        desc_lbl = QLabel(desc)
        desc_lbl.setStyleSheet("color:#888;font-size:11px;")

        col.addWidget(nome_lbl)
        col.addWidget(desc_lbl)
        row.addLayout(col, stretch=1)

        # Botões
        btns = QVBoxLayout()
        btns.setSpacing(4)

        btn_info = QPushButton("ℹ  Info")
        btn_info.setFixedSize(85, 26)
        btn_info.setStyleSheet(_CSS_INFO)
        btn_info.clicked.connect(lambda: self.info_requested.emit(self.pacote))

        if modo == "instalar":
            btn_acao = QPushButton("⬇  Instalar")
            btn_acao.setStyleSheet(_CSS_INSTALAR)
        else:
            btn_acao = QPushButton("🗑  Remover")
            btn_acao.setStyleSheet(_CSS_REMOVER)
        btn_acao.setFixedSize(95, 26)
        btn_acao.clicked.connect(lambda: self.action_requested.emit(self.pacote))

        btns.addWidget(btn_info)
        btns.addWidget(btn_acao)
        row.addLayout(btns)

    def _set_icone_padrao(self):
        tipo = self.pacote.get("tipo", "")
        icone = QIcon.fromTheme(_ICONES_PADRAO.get(tipo, "application-x-executable"))
        if not icone.isNull():
            self._icon_lbl.setPixmap(icone.pixmap(48, 48))

    def set_icon(self, pixmap: QPixmap):
        if not pixmap.isNull():
            self._icon_lbl.setPixmap(
                pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )

    def sizeHint(self) -> QSize:
        return QSize(300, 72)
