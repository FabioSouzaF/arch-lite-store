"""
InstalledWorker — lê os pacotes instalados localmente:
  - Pacman/Yay: banco de dados local via pyalpm
  - Flatpak:    `flatpak list`
"""
import subprocess

from pyalpm import Handle
from PySide6.QtCore import QThread, Signal


class InstalledWorker(QThread):
    results_ready = Signal(list)

    def run(self):
        instalados = []
        try:
            instalados.extend(self._listar_pacman())
            instalados.extend(self._listar_flatpak())
            instalados.sort(key=lambda x: x["nome"].lower())
            self.results_ready.emit(instalados)
        except Exception:
            self.results_ready.emit([])

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _fmt_mb(bytes_val) -> str:
        if not bytes_val:
            return "Desconhecido"
        return f"{bytes_val / (1024 * 1024):.2f} MB"

    def _listar_pacman(self) -> list:
        resultados = []
        handle = Handle("/", "/var/lib/pacman")
        for pkg in handle.get_localdb().pkgcache:
            resultados.append({
                "tipo": "Pacman",
                "nome": pkg.name,
                "exibicao": f"{pkg.name} ({pkg.version})\nInstalado via Pacman/Yay",
                "comando": f"sudo pacman -Rns {pkg.name}",
                "versao": pkg.version,
                "desc_completa": pkg.desc or "Sem descrição.",
                "tamanho_download": "Já instalado",
                "tamanho_instalado": self._fmt_mb(pkg.isize),
                "url": pkg.url or "Não disponível",
                "licenca": ", ".join(pkg.licenses) if pkg.licenses else "Desconhecido",
                "dependencias": ", ".join(pkg.depends) if pkg.depends else "Nenhuma",
            })
        return resultados

    @staticmethod
    def _listar_flatpak() -> list:
        resultados = []
        try:
            fp = subprocess.run(
                ["flatpak", "list", "--columns=name,application,version"],
                capture_output=True, text=True
            )
            for linha in fp.stdout.strip().split("\n"):
                partes = linha.split("\t")
                if len(partes) >= 3:
                    nome, app_id, versao = partes[0], partes[1], partes[2]
                    resultados.append({
                        "tipo": "Flatpak",
                        "nome": nome,
                        "app_id": app_id,
                        "exibicao": f"{nome} ({versao})\nID: {app_id}",
                        "comando": f"flatpak uninstall {app_id}",
                        "versao": versao,
                        "desc_completa": f"Aplicação Flatpak instalada localmente.\nID: {app_id}",
                        "tamanho_download": "Já instalado",
                        "tamanho_instalado": "Variável",
                        "url": f"https://flathub.org/apps/{app_id}",
                        "licenca": "Ver no Flathub",
                        "dependencias": "Runtimes locais",
                    })
        except Exception:
            pass
        return resultados
