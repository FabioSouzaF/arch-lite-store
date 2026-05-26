"""
IconWorker — baixa ícones de pacotes em background via requests.
Emite `icon_ready(nome, bytes)` para cada ícone carregado com sucesso,
e `status_update(mensagem)` para log de progresso.
"""
import requests
from PySide6.QtCore import QThread, Signal

# URL base para ícones de apps Flatpak no Flathub
_FLATHUB_ICON_URL = (
    "https://dl.flathub.org/repo/appstream/x86_64/icons/128x128/{app_id}.png"
)


class IconWorker(QThread):
    icon_ready = Signal(str, bytes)
    status_update = Signal(str)

    def __init__(self, pacotes: list):
        super().__init__()
        self.pacotes = pacotes

    def run(self):
        for pkg in self.pacotes:
            url = self._resolver_url(pkg)
            if url:
                self._baixar_icone(pkg["nome"], url)
        self.status_update.emit("Processamento de ícones concluído.")

    # ------------------------------------------------------------------ #

    @staticmethod
    def _resolver_url(pkg: dict) -> str | None:
        """Retorna a URL do ícone ou None se não houver."""
        if pkg.get("icon_url"):
            return pkg["icon_url"]
        if pkg.get("tipo") == "Flatpak" and "app_id" in pkg:
            return _FLATHUB_ICON_URL.format(app_id=pkg["app_id"])
        return None

    def _baixar_icone(self, nome: str, url: str):
        self.status_update.emit(f"Baixando ícone: {nome}...")
        try:
            resposta = requests.get(url, timeout=2)
            if resposta.status_code == 200:
                self.icon_ready.emit(nome, resposta.content)
                self.status_update.emit(f"Ícone carregado: {nome}")
            else:
                self.status_update.emit(f"Sem ícone no servidor: {nome}")
        except Exception:
            self.status_update.emit(f"Falha de rede ao obter ícone de {nome}")
