"""
ArchStore — janela principal da Arch Lite Store.

Orquestradora: conecta abas ↔ workers ↔ ações do sistema.
Layout em cada aba:   ui/tabs/
Botões inline:        ui/package_item.py
I/O pesada:           workers/
"""
import subprocess

from PySide6.QtWidgets import (
    QMainWindow, QTabWidget,
    QListWidget, QListWidgetItem, QMessageBox,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap

from arch_lite_store.assets import LOGO_ICON
from arch_lite_store.data.featured import FEATURED_APPS
from arch_lite_store.workers.search import SearchWorker
from arch_lite_store.workers.installed import InstalledWorker
from arch_lite_store.workers.updates import UpdateWorker
from arch_lite_store.workers.icons import IconWorker
from arch_lite_store.ui.dialogs import DetailsDialog
from arch_lite_store.ui.package_item import PackageItemWidget
from arch_lite_store.ui.tabs.search_tab import SearchTab
from arch_lite_store.ui.tabs.installed_tab import InstalledTab
from arch_lite_store.ui.tabs.updates_tab import UpdatesTab
from arch_lite_store.ui.tabs.maintenance_tab import MaintenanceTab

_ICONES_TIPO = {
    "Pacman": "system-software-install",
    "Flatpak": "application-x-executable",
    "AUR": "emblem-system",
}


class ArchStore(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arch Lite Store")
        self.resize(820, 660)

        if LOGO_ICON.exists():
            self.setWindowIcon(QIcon(str(LOGO_ICON)))

        # Dicts para rastrear widgets inline → atualizar ícones baixados
        self._search_widgets: dict[str, PackageItemWidget] = {}
        self._installed_widgets: dict[str, PackageItemWidget] = {}

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self._registrar_abas()
        self._conectar_sinais()

        self.carregar_instalados()
        self._exibir_aplicativos_populares()

    # ================================================================== #
    # Configuração                                                         #
    # ================================================================== #

    def _registrar_abas(self):
        self.search_tab      = SearchTab()
        self.installed_tab   = InstalledTab()
        self.updates_tab     = UpdatesTab()
        self.maintenance_tab = MaintenanceTab()

        self.tabs.addTab(self.search_tab,      "🔍  Buscar")
        self.tabs.addTab(self.installed_tab,   "📦  Instalados")
        self.tabs.addTab(self.updates_tab,     "🔄  Atualizações")
        self.tabs.addTab(self.maintenance_tab, "🛠  Manutenção")

    def _conectar_sinais(self):
        st = self.search_tab
        it = self.installed_tab
        ut = self.updates_tab
        mt = self.maintenance_tab

        # Busca
        st.search_button.clicked.connect(self.realizar_busca)
        st.search_input.returnPressed.connect(self.realizar_busca)

        # Instalados
        it.filter_input.textChanged.connect(self.filtrar_instalados)
        it.refresh_button.clicked.connect(self.carregar_instalados)

        # Atualizações
        ut.check_updates_button.clicked.connect(self.verificar_atualizacoes)
        ut.sys_update_button.clicked.connect(self.atualizar_sistema_completo)

        # Manutenção
        mt.btn_cache.clicked.connect(self.limpar_cache)
        mt.btn_orfaos.clicked.connect(self.limpar_orfaos)
        mt.btn_flatpak.clicked.connect(self.limpar_flatpaks)

    # ================================================================== #
    # Aba: Buscar                                                          #
    # ================================================================== #

    def realizar_busca(self):
        st    = self.search_tab
        termo = st.search_input.text().strip()
        if not termo:
            return

        buscar_pacman  = st.chk_pacman.isChecked()
        buscar_aur     = st.chk_aur.isChecked()
        buscar_flatpak = st.chk_flatpak.isChecked()

        if not (buscar_pacman or buscar_aur or buscar_flatpak):
            QMessageBox.warning(self, "Aviso", "Selecione pelo menos uma fonte de busca!")
            return

        st.results_list.clear()
        self._search_widgets.clear()
        st.status_label.setText(f"Buscando por '{termo}'...")
        st.search_button.setEnabled(False)

        self._search_worker = SearchWorker(termo, buscar_pacman, buscar_aur, buscar_flatpak)
        self._search_worker.results_ready.connect(self._on_busca_concluida)
        self._search_worker.start()

    def _on_busca_concluida(self, resultados: list):
        st = self.search_tab
        st.search_button.setEnabled(True)
        if not resultados:
            st.status_label.setText("Nenhum pacote encontrado.")
            return
        st.status_label.setText(f"{len(resultados)} pacotes encontrados.")
        self._popular_lista(
            st.results_list, resultados,
            modo="instalar", widgets_dict=self._search_widgets, buscar_icones=True,
        )

    def _exibir_aplicativos_populares(self):
        self.search_tab.status_label.setText("⭐  Aplicativos Populares")
        self._popular_lista(
            self.search_tab.results_list, FEATURED_APPS,
            modo="instalar", widgets_dict=self._search_widgets, buscar_icones=True,
        )

    # ================================================================== #
    # Aba: Instalados                                                      #
    # ================================================================== #

    def carregar_instalados(self):
        it = self.installed_tab
        it.installed_list.clear()
        self._installed_widgets.clear()
        it.filter_input.clear()
        it.status_instalados.setText("Lendo base de dados local...")
        it.refresh_button.setEnabled(False)

        self._installed_worker = InstalledWorker()
        self._installed_worker.results_ready.connect(self._on_instalados_carregados)
        self._installed_worker.start()

    def _on_instalados_carregados(self, resultados: list):
        it = self.installed_tab
        it.refresh_button.setEnabled(True)
        it.status_instalados.setText(f"{len(resultados)} pacotes instalados.")
        self._popular_lista(
            it.installed_list, resultados,
            modo="remover", widgets_dict=self._installed_widgets,
        )

    def filtrar_instalados(self, texto: str):
        termo = texto.lower().strip()
        lista = self.installed_tab.installed_list
        for i in range(lista.count()):
            item   = lista.item(i)
            widget = lista.itemWidget(item)
            nome   = widget.pacote["nome"] if isinstance(widget, PackageItemWidget) else ""
            item.setHidden(bool(termo) and termo not in nome.lower())

    # ================================================================== #
    # Aba: Atualizações                                                    #
    # ================================================================== #

    def verificar_atualizacoes(self):
        ut = self.updates_tab
        ut.update_list.clear()
        ut.status_atualizacoes.setText("Sincronizando bancos de dados... Aguarde.")
        ut.check_updates_button.setEnabled(False)
        ut.sys_update_button.setEnabled(False)

        self._update_worker = UpdateWorker()
        self._update_worker.results_ready.connect(self._on_atualizacoes_verificadas)
        self._update_worker.start()

    def _on_atualizacoes_verificadas(self, resultados: list):
        ut = self.updates_tab
        ut.check_updates_button.setEnabled(True)

        if not resultados:
            ut.status_atualizacoes.setText("Seu sistema está 100% atualizado! 🎉")
            ut.sys_update_button.setEnabled(False)
            return

        ut.status_atualizacoes.setText(f"{len(resultados)} pacotes aguardando atualização:")
        ut.sys_update_button.setEnabled(True)

        for pacote in resultados:
            item = QListWidgetItem(f"[{pacote['tipo']}] {pacote['exibicao']}")
            item.setIcon(QIcon.fromTheme(_ICONES_TIPO.get(pacote["tipo"], "emblem-system")))
            ut.update_list.addItem(item)

    def atualizar_sistema_completo(self):
        resp = QMessageBox.question(
            self, "Atualização",
            "Deseja aplicar todas as atualizações agora?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if resp != QMessageBox.Yes:
            return
        try:
            subprocess.run([
                "xterm", "-e",
                "yay -Syu; echo '\n--- Flatpaks ---'; flatpak update; "
                "echo '\nConcluído. ENTER para fechar...'; read",
            ])
            self.updates_tab.update_list.clear()
            self.updates_tab.sys_update_button.setEnabled(False)
        except Exception as exc:
            QMessageBox.critical(self, "Erro", str(exc))

    # ================================================================== #
    # Aba: Manutenção                                                      #
    # ================================================================== #

    def limpar_cache(self):
        if QMessageBox.question(
            self, "Limpar Cache",
            "Remove pacotes antigos do cache, liberando espaço.\nDeseja continuar?",
            QMessageBox.Yes | QMessageBox.No,
        ) == QMessageBox.Yes:
            subprocess.run([
                "xterm", "-e",
                "sudo pacman -Sc; echo '\nConcluído. ENTER para fechar...'; read",
            ])

    def limpar_orfaos(self):
        try:
            resultado = subprocess.run(["pacman", "-Qdtq"], capture_output=True, text=True)
            orfaos    = resultado.stdout.strip()

            if not orfaos:
                QMessageBox.information(
                    self, "Sistema Limpo",
                    "Não existem pacotes órfãos no seu sistema.",
                )
                return

            if QMessageBox.question(
                self, "Remover Órfãos",
                "Foram encontrados pacotes órfãos.\nDeseja removê-los agora?",
                QMessageBox.Yes | QMessageBox.No,
            ) == QMessageBox.Yes:
                comando = f"sudo pacman -Rns {orfaos.replace(chr(10), ' ')}"
                subprocess.run([
                    "xterm", "-e",
                    f"{comando}; echo '\nConcluído. ENTER para fechar...'; read",
                ])
                self.carregar_instalados()
        except Exception as exc:
            QMessageBox.critical(self, "Erro", f"Erro ao verificar órfãos: {exc}")

    def limpar_flatpaks(self):
        if QMessageBox.question(
            self, "Limpar Flatpaks",
            "Remove bibliotecas Flatpak sem uso.\nDeseja continuar?",
            QMessageBox.Yes | QMessageBox.No,
        ) == QMessageBox.Yes:
            subprocess.run([
                "xterm", "-e",
                "flatpak uninstall --unused; echo '\nConcluído. ENTER para fechar...'; read",
            ])

    # ================================================================== #
    # Helpers partilhados                                                  #
    # ================================================================== #

    def _popular_lista(
        self,
        lista_widget: QListWidget,
        dados: list,
        modo: str = "instalar",
        widgets_dict: dict | None = None,
        buscar_icones: bool = False,
    ):
        """Preenche lista com PackageItemWidget inline por linha."""
        for pacote in dados:
            item   = QListWidgetItem()
            widget = PackageItemWidget(pacote, modo=modo)
            widget.info_requested.connect(self._on_info_requested)
            widget.action_requested.connect(self._on_action_requested)
            item.setSizeHint(QSize(0, 72))
            lista_widget.addItem(item)
            lista_widget.setItemWidget(item, widget)
            if widgets_dict is not None:
                widgets_dict[pacote["nome"]] = widget

        if buscar_icones:
            self._icon_worker = IconWorker(dados)
            self._icon_worker.icon_ready.connect(self._aplicar_icone_baixado)
            self._icon_worker.status_update.connect(
                lambda msg: self.search_tab.icon_log_label.setText(msg)
            )
            self._icon_worker.start()

    def _aplicar_icone_baixado(self, nome: str, image_bytes: bytes):
        """Atualiza ícone no widget inline após download."""
        widget = self._search_widgets.get(nome)
        if widget:
            pixmap = QPixmap()
            pixmap.loadFromData(image_bytes)
            widget.set_icon(pixmap)

    def _on_info_requested(self, pacote: dict):
        """Abre dialog de detalhes a partir do botão Info inline."""
        nome   = pacote["nome"]
        widget = self._search_widgets.get(nome) or self._installed_widgets.get(nome)
        icone  = QIcon()
        if widget:
            pm = widget._icon_lbl.pixmap()
            if pm and not pm.isNull():
                icone = QIcon(pm)
        DetailsDialog(pacote, icone, self).exec()

    def _on_action_requested(self, pacote: dict):
        """Instala ou desinstala conforme o comando embutido no pacote."""
        comando   = pacote.get("comando", "")
        eh_remove = "-Rns" in comando or "uninstall" in comando
        txt       = "DESINSTALAR" if eh_remove else "instalar"

        if QMessageBox.question(
            self, "Confirmar",
            f"Deseja {txt} {pacote['nome']}?\n\n{comando}",
            QMessageBox.Yes | QMessageBox.No,
        ) != QMessageBox.Yes:
            return

        try:
            subprocess.run([
                "xterm", "-e",
                f"{comando}; echo '\nConcluído. ENTER...'; read",
            ])
            self.carregar_instalados()
        except Exception as exc:
            QMessageBox.critical(self, "Erro", str(exc))
