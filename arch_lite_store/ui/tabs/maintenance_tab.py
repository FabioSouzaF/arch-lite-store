"""
MaintenanceTab — aba "Manutenção".

Responsabilidades:
  - Título e subtítulo
  - Botão "Limpar Cache do Pacman" + descrição
  - Botão "Remover Pacotes Órfãos" + descrição
  - Botão "Limpar Flatpaks Inutilizados" + descrição
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout,
    QPushButton, QLabel,
)


class MaintenanceTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        titulo = QLabel("<b>Ferramentas de Limpeza e Otimização</b>")
        titulo.setStyleSheet("font-size: 16px;")
        layout.addWidget(titulo)

        layout.addWidget(QLabel(
            "Mantenha o seu sistema Arch Linux rápido e livre de arquivos desnecessários."
        ))
        layout.addSpacing(20)

        self._adicionar_acao(
            layout,
            attr="btn_cache",
            texto="Limpar Cache do Pacman",
            descricao="<i>Remove pacotes de versões antigas armazenados no HD, liberando Gigabytes.</i>",
        )
        self._adicionar_acao(
            layout,
            attr="btn_orfaos",
            texto="Remover Pacotes Órfãos",
            descricao=(
                "<i>Remove dependências de programas que já foram desinstalados "
                "e não têm mais uso.</i>"
            ),
        )
        self._adicionar_acao(
            layout,
            attr="btn_flatpak",
            texto="Limpar Flatpaks Inutilizados",
            descricao=(
                "<i>Remove runtimes e bibliotecas do ecossistema Flatpak "
                "que já não são necessárias.</i>"
            ),
        )

        layout.addStretch()

    # ------------------------------------------------------------------ #

    def _adicionar_acao(self, layout: QVBoxLayout, attr: str, texto: str, descricao: str):
        """Cria um botão + label descritivo e armazena o botão como atributo."""
        btn = QPushButton(texto)
        btn.setMinimumHeight(40)
        setattr(self, attr, btn)
        layout.addWidget(btn)
        layout.addWidget(QLabel(descricao))
        layout.addSpacing(15)
