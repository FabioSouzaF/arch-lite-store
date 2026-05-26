"""
Arch Store — Entry-point do pacote.
Execute com: python -m arch_lite_store
"""
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from arch_lite_store.ui.main_window import ArchStore
from arch_lite_store.assets import LOGO_ICON


def main():
    app = QApplication(sys.argv)

    # Ícone do processo — aparece na taskbar e no alt+tab do LXQt
    if LOGO_ICON.exists():
        app.setWindowIcon(QIcon(str(LOGO_ICON)))

    window = ArchStore()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
