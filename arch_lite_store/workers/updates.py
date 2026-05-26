"""
UpdateWorker — verifica pacotes com atualizações disponíveis:
  - Pacman: checkupdates
  - AUR:    yay -Qua
  - Flatpak: flatpak remote-ls --updates
"""
import subprocess

from PySide6.QtCore import QThread, Signal


class UpdateWorker(QThread):
    results_ready = Signal(list)

    def run(self):
        atualizacoes = []
        atualizacoes.extend(self._checar_pacman())
        atualizacoes.extend(self._checar_aur())
        atualizacoes.extend(self._checar_flatpak())
        self.results_ready.emit(atualizacoes)

    # ------------------------------------------------------------------ #

    @staticmethod
    def _checar_pacman() -> list:
        resultados = []
        try:
            p = subprocess.run(["checkupdates"], capture_output=True, text=True)
            for linha in p.stdout.strip().split("\n"):
                if linha:
                    resultados.append({"tipo": "Pacman", "exibicao": linha})
        except Exception:
            pass
        return resultados

    @staticmethod
    def _checar_aur() -> list:
        resultados = []
        try:
            p = subprocess.run(["yay", "-Qua"], capture_output=True, text=True)
            for linha in p.stdout.strip().split("\n"):
                if linha:
                    resultados.append({"tipo": "AUR", "exibicao": linha})
        except Exception:
            pass
        return resultados

    @staticmethod
    def _checar_flatpak() -> list:
        resultados = []
        try:
            p = subprocess.run(
                ["flatpak", "remote-ls", "--updates", "--columns=name,version"],
                capture_output=True, text=True
            )
            for linha in p.stdout.strip().split("\n"):
                if linha:
                    resultados.append({"tipo": "Flatpak", "exibicao": linha.replace("\t", " -> ")})
        except Exception:
            pass
        return resultados
