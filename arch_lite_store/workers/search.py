"""
SearchWorker — busca pacotes em três fontes em paralelo (via QThread):
  - Pacman (repositórios oficiais via pyalpm)
  - AUR   (API RPC v5)
  - Flatpak (flatpak search)
"""
import subprocess

import pyalpm
import requests
from pyalpm import Handle
from PySide6.QtCore import QThread, Signal


class SearchWorker(QThread):
    results_ready = Signal(list)
    error_occurred = Signal(str)

    def __init__(self, query: str, buscar_pacman: bool, buscar_aur: bool, buscar_flatpak: bool):
        super().__init__()
        self.query = query
        self.buscar_pacman = buscar_pacman
        self.buscar_aur = buscar_aur
        self.buscar_flatpak = buscar_flatpak

    # ------------------------------------------------------------------ #
    # Helpers de busca por fonte                                           #
    # ------------------------------------------------------------------ #

    def _buscar_pacman(self) -> list:
        resultados = []
        handle = Handle("/", "/var/lib/pacman")
        repos = ["core", "extra", "multilib"]
        termo = self.query.lower()

        for repo in repos:
            try:
                db = handle.register_syncdb(repo, pyalpm.SIG_DATABASE_OPTIONAL)
                for pkg in db.pkgcache:
                    if termo in pkg.name.lower() or (pkg.desc and termo in pkg.desc.lower()):
                        resultados.append(self._pacman_para_dict(pkg))
            except Exception:
                pass  # repositório indisponível — segue para o próximo

        return resultados

    def _buscar_aur(self) -> list:
        resultados = []
        try:
            url = f"https://aur.archlinux.org/rpc/v5/search/{self.query}"
            resposta = requests.get(url, timeout=5).json()
            for pkg in resposta.get("results", []):
                resultados.append(self._aur_para_dict(pkg))
        except Exception:
            pass
        return resultados

    def _buscar_flatpak(self) -> list:
        resultados = []
        try:
            fp = subprocess.run(
                ["flatpak", "search", self.query],
                capture_output=True, text=True
            )
            linhas = fp.stdout.strip().split("\n")[1:]  # pula cabeçalho
            for linha in linhas:
                partes = linha.split("\t")
                if len(partes) > 2:
                    resultados.append(self._flatpak_para_dict(partes))
        except Exception:
            pass
        return resultados

    # ------------------------------------------------------------------ #
    # Conversores de formato                                               #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _fmt_mb(bytes_val) -> str:
        if not bytes_val:
            return "Desconhecido"
        return f"{bytes_val / (1024 * 1024):.2f} MB"

    def _pacman_para_dict(self, pkg) -> dict:
        return {
            "tipo": "Pacman",
            "nome": pkg.name,
            "exibicao": f"{pkg.name} ({pkg.version})\n{pkg.desc}",
            "comando": f"sudo pacman -S {pkg.name}",
            "versao": pkg.version,
            "desc_completa": pkg.desc or "Sem descrição detalhada.",
            "tamanho_download": self._fmt_mb(pkg.size),
            "tamanho_instalado": self._fmt_mb(pkg.isize),
            "url": pkg.url or "Não disponível",
            "licenca": ", ".join(pkg.licenses) if pkg.licenses else "Desconhecido",
            "dependencias": ", ".join(pkg.depends) if pkg.depends else "Nenhuma",
        }

    @staticmethod
    def _aur_para_dict(pkg) -> dict:
        return {
            "tipo": "AUR",
            "nome": pkg["Name"],
            "exibicao": f"{pkg['Name']} ({pkg['Version']})\n{pkg.get('Description', '')}",
            "comando": f"yay -S {pkg['Name']}",
            "versao": pkg["Version"],
            "desc_completa": pkg.get("Description", "Sem descrição detalhada."),
            "tamanho_download": "Fará compilação (AUR)",
            "tamanho_instalado": "Depende da compilação",
            "url": pkg.get("URL", "Não disponível"),
            "licenca": pkg.get("License", "Desconhecido"),
            "dependencias": "Geridas automaticamente pelo Yay",
        }

    @staticmethod
    def _flatpak_para_dict(partes: list) -> dict:
        app_id = partes[2] if "." in partes[2] else partes[0]
        versao = partes[3] if len(partes) > 3 else "N/A"
        return {
            "tipo": "Flatpak",
            "nome": partes[0],
            "app_id": app_id,
            "exibicao": f"{partes[0]}\n{partes[1]}",
            "comando": f"flatpak install {app_id}",
            "versao": versao,
            "desc_completa": partes[1] or "Sem descrição.",
            "tamanho_download": "Descarregado via Flathub",
            "tamanho_instalado": "Variável",
            "url": f"https://flathub.org/apps/{app_id}",
            "licenca": "Ver no Flathub",
            "dependencias": "Runtimes do Flatpak",
        }

    # ------------------------------------------------------------------ #
    # Thread principal                                                     #
    # ------------------------------------------------------------------ #

    def run(self):
        resultados = []
        try:
            if self.buscar_pacman:
                resultados.extend(self._buscar_pacman())
            if self.buscar_aur:
                resultados.extend(self._buscar_aur())
            if self.buscar_flatpak:
                resultados.extend(self._buscar_flatpak())

            self.results_ready.emit(resultados)
        except Exception as exc:
            self.error_occurred.emit(str(exc))
