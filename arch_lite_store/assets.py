"""
Arch Store — resolução de caminhos de assets do pacote.
Centraliza o acesso a imagens, ícones e outros recursos estáticos
para que todos os módulos referenciem o mesmo local.
"""
from pathlib import Path

# Raiz da pasta Assets (relativa a este arquivo)
ASSETS_DIR = Path(__file__).parent / "Assets"

# Logotipos
LOGO_ICON = ASSETS_DIR / "Logo_128x128.png"   # ícone da janela e taskbar
LOGO_FULL = ASSETS_DIR / "Logo.png"            # uso futuro (splash, about…)
