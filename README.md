# Arch Lite Store

<p align="center">
  <img src="arch_lite_store/Assets/Logo_128x128.png" alt="Arch Lite Store Logo" width="96"/>
</p>

<p align="center">
  Gerenciador gráfico de pacotes para <strong>Arch Linux</strong> — leve, rápido e simples.<br/>
  Suporta <strong>Pacman</strong>, <strong>AUR (via Yay)</strong> e <strong>Flatpak (Flathub)</strong>.
</p>

---

## Funcionalidades

- 🔍 **Busca** em Pacman, AUR e Flathub simultaneamente (com filtros)
- 📦 **Lista de instalados** com filtro por nome e remoção inline
- 🔄 **Verificação de atualizações** (Pacman + AUR + Flatpak)
- 🛠 **Manutenção**: limpar cache, remover órfãos, limpar Flatpaks inutilizados
- Botões **ℹ Info**, **⬇ Instalar** e **🗑 Remover** inline em cada linha — sem duplo clique

## Requisitos de Hardware

Projetado para rodar em hardware modesto — testado num notebook com **Intel Core i3 330M** rodando **Arch Linux + LXQt**.

---

## Instalação e Execução

### Modo 1 — Arch Linux (nativo)

> Recomendado para uso no dia a dia. Instala as dependências diretamente no sistema.

**1. Instale as dependências via Pacman:**

```bash
sudo pacman -S python pyside6 python-requests pyalpm xterm flatpak adwaita-icon-theme qt6-svg appstream
```

**2. Instale o Yay (AUR helper) — se ainda não tiver:**

```bash
# Precisa de base-devel e git
sudo pacman -S --needed base-devel git
git clone https://aur.archlinux.org/yay-bin.git
cd yay-bin && makepkg -si --noconfirm && cd .. && rm -rf yay-bin
```

**3. Clone o repositório:**

```bash
git clone https://github.com/seu-usuario/arch-lite-store.git
cd arch-lite-store
```

**4. Adicione o Flathub (se ainda não tiver):**

```bash
flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
```

**5. Execute:**

```bash
python -m arch_lite_store
```

---

### Modo 2 — Docker (desenvolvimento / testes)

> Ideal para testar sem instalar dependências no sistema host. Requer Docker + Docker Compose.

**Pré-requisitos:**

- Docker e Docker Compose instalados
- Servidor X11 rodando (necessário para a interface gráfica)

**1. Clone o repositório:**

```bash
git clone https://github.com/seu-usuario/arch-lite-store.git
cd arch-lite-store
```

**2. Permita conexões X11 do container:**

```bash
xhost +local:docker
```

**3. Suba o container (primeira vez faz o build automático):**

```bash
sudo docker compose up --build
```

**Execuções seguintes** (sem rebuild):

```bash
sudo docker compose up
```

**4. Ao terminar, revogue a permissão X11:**

```bash
xhost -local:docker
```

#### Cache persistente

O Docker Compose monta volumes para evitar baixar tudo a cada execução:

| Volume local | Destino no container | Conteúdo |
|---|---|---|
| `.cache/pacman/` | `/var/cache/pacman/pkg` | Cache do Pacman |
| `.cache/yay/` | `/home/devuser/.cache/yay` | Cache do Yay/AUR |
| `.cache/flatpak/` | `/home/devuser/.local/share/flatpak` | Apps e runtimes Flatpak |

---

## Estrutura do Projeto

```
arch_lite_store/
├── __main__.py          # Entry-point: python -m arch_lite_store
├── assets.py            # Caminhos centralizados dos assets
├── Assets/
│   ├── Logo.png
│   └── Logo_128x128.png
├── data/
│   └── featured.py      # Apps em destaque na tela inicial
├── workers/             # Threads de background (sem bloquear a UI)
│   ├── search.py        # Busca: Pacman / AUR / Flatpak
│   ├── installed.py     # Lista pacotes instalados localmente
│   ├── updates.py       # Verifica atualizações disponíveis
│   └── icons.py         # Download assíncrono de ícones
└── ui/
    ├── main_window.py   # Janela principal (orquestradora)
    ├── package_item.py  # Widget inline por linha (ícone + botões)
    ├── dialogs.py       # Diálogo de detalhes do pacote
    └── tabs/
        ├── search_tab.py
        ├── installed_tab.py
        ├── updates_tab.py
        └── maintenance_tab.py
```

---

## Dependências Python

| Pacote | Origem | Uso |
|---|---|---|
| `pyside6` | Pacman | Interface gráfica (Qt6) |
| `python-requests` | Pacman | API AUR + download de ícones |
| `pyalpm` | Pacman | Leitura do banco de dados do Pacman |

Todas disponíveis nos repositórios oficiais do Arch — **sem `pip`**.

---

## Licença

MIT — veja [LICENSE](LICENSE).
