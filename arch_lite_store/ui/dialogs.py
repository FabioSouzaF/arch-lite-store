"""
DetailsDialog — janela de detalhes de um pacote.
Exibe ícone, nome, versão, descrição, tamanhos, licença, URL e dependências.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QTextBrowser, QDialogButtonBox,
)
from PySide6.QtGui import QIcon


class DetailsDialog(QDialog):
    def __init__(self, pacote: dict, icone: QIcon, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Detalhes do Pacote: {pacote['nome']}")
        self.resize(550, 450)

        layout = QVBoxLayout(self)
        layout.addLayout(self._criar_header(pacote, icone))
        layout.addWidget(self._criar_info_browser(pacote))
        botoes = self._criar_botoes()
        botoes.accepted.connect(self.accept)
        layout.addWidget(botoes)

    # ------------------------------------------------------------------ #

    @staticmethod
    def _criar_header(pacote: dict, icone: QIcon) -> QHBoxLayout:
        header = QHBoxLayout()

        icon_label = QLabel()
        if not icone.isNull():
            icon_label.setPixmap(icone.pixmap(64, 64))
        header.addWidget(icon_label)

        info = QVBoxLayout()
        info.addWidget(QLabel(f"<b><font size='5'>{pacote['nome']}</font></b>"))
        info.addWidget(QLabel(
            f"<b>Origem:</b> {pacote['tipo']} | "
            f"<b>Versão:</b> {pacote.get('versao', 'N/A')}"
        ))
        header.addLayout(info)
        header.addStretch()
        return header

    @staticmethod
    def _criar_info_browser(pacote: dict) -> QTextBrowser:
        browser = QTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setHtml(f"""
            <h3>Descrição</h3>
            <p>{pacote.get('desc_completa', 'Sem descrição.')}</p>
            <hr>
            <table width="100%" cellpadding="4" style="border-collapse: collapse;">
                <tr><td><b>Tamanho Download:</b></td>
                    <td>{pacote.get('tamanho_download', 'N/A')}</td></tr>
                <tr><td><b>Tamanho Instalado:</b></td>
                    <td>{pacote.get('tamanho_instalado', 'N/A')}</td></tr>
                <tr><td><b>Licença:</b></td>
                    <td>{pacote.get('licenca', 'N/A')}</td></tr>
                <tr><td><b>Site Oficial:</b></td>
                    <td><a href="{pacote.get('url', '#')}">{pacote.get('url', 'N/A')}</a></td></tr>
            </table>
            <hr>
            <h3>Dependências</h3>
            <p style="color: #555; font-family: monospace;">
                {pacote.get('dependencias', 'N/A')}
            </p>
        """)
        return browser

    @staticmethod
    def _criar_botoes() -> QDialogButtonBox:
        botoes = QDialogButtonBox(QDialogButtonBox.Ok)
        return botoes

    def _conectar_sinais(self):
        # chamado pelo __init__ via layout — atalho: reutilizamos accept direto
        pass
