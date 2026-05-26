# Usa a imagem oficial do Arch Linux
FROM archlinux:latest


# Atualiza os repositórios e instala as dependências essenciais
RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm \
    base-devel \
    git \
    sudo \
    python \
    pyside6 \
    python-requests \
    pyalpm \
    xterm \
    flatpak \
    mesa-libgl \
    dbus \
    ttf-dejavu \
    noto-fonts \
    fontconfig \
    adwaita-icon-theme \
    qt6-svg \
    appstream

# Força a atualização do cache de fontes do Arch Linux
RUN fc-cache -f -v

# Cria um interceptador para forçar o Flatpak a rodar sempre no modo usuário
RUN echo '#!/bin/bash' > /usr/local/bin/flatpak && \
    echo 'exec /usr/bin/flatpak --user "$@"' >> /usr/local/bin/flatpak && \
    chmod +x /usr/local/bin/flatpak

# O makepkg/yay não pode ser executado como root. Criamos o usuário 'devuser'.
RUN useradd -m -G wheel devuser && \
    echo "devuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER devuser
WORKDIR /home/devuser

# Instala o Yay (AUR helper)
RUN git clone https://aur.archlinux.org/yay-bin.git && \
    cd yay-bin && \
    makepkg -si --noconfirm && \
    cd .. && rm -rf yay-bin

# Define o diretório de trabalho onde o HD externo será montado
WORKDIR /app

# Executa a aplicação
CMD ["python", "-m", "arch_lite_store"]