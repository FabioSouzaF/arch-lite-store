"""
Aplicativos populares exibidos na tela inicial de busca.
Cada item é um dicionário com os mesmos campos usados pelos workers de busca.
"""

FEATURED_APPS = [
    {
        "tipo": "Pacman",
        "nome": "firefox",
        "exibicao": "Firefox\nO clássico navegador web de código aberto.",
        "comando": "sudo pacman -S firefox",
        "icon_url": (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/"
            "Firefox_logo%2C_2019.svg/120px-Firefox_logo%2C_2019.svg.png"
        ),
        "versao": "Estável",
        "desc_completa": "Navegador focado em privacidade desenvolvido pela Mozilla.",
        "tamanho_download": "~70 MB",
        "tamanho_instalado": "~230 MB",
        "url": "https://mozilla.org/firefox/",
        "licenca": "MPL-2.0",
        "dependencias": "gtk3, nss, libpulse",
    },
    {
        "tipo": "Pacman",
        "nome": "vlc",
        "exibicao": "VLC Media Player\nReprodutor de vídeo que roda absolutamente tudo.",
        "comando": "sudo pacman -S vlc",
        "icon_url": (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/"
            "VLC_Icon.svg/120px-VLC_Icon.svg.png"
        ),
        "versao": "Estável",
        "desc_completa": "Reprodutor multimídia capaz de ler a grande maioria dos codecs.",
        "tamanho_download": "~15 MB",
        "tamanho_instalado": "~85 MB",
        "url": "https://videolan.org/vlc/",
        "licenca": "GPL",
        "dependencias": "qt6-base, ffmpeg, lua",
    },
    {
        "tipo": "AUR",
        "nome": "visual-studio-code-bin",
        "exibicao": "VS Code\nEditor de código moderno.",
        "comando": "yay -S visual-studio-code-bin",
        "icon_url": (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/"
            "Visual_Studio_Code_1.35_icon.svg/120px-Visual_Studio_Code_1.35_icon.svg.png"
        ),
        "versao": "Estável",
        "desc_completa": "Editor profissional da Microsoft.",
        "tamanho_download": "~90 MB",
        "tamanho_instalado": "~310 MB",
        "url": "https://code.visualstudio.com/",
        "licenca": "Proprietária",
        "dependencias": "electron, nss",
    },
    {
        "tipo": "AUR",
        "nome": "spotify",
        "exibicao": "Spotify\nServiço de streaming de músicas.",
        "comando": "yay -S spotify",
        "icon_url": (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/"
            "Spotify_icon.svg/120px-Spotify_icon.svg.png"
        ),
        "versao": "Estável",
        "desc_completa": "Cliente oficial de desktop Linux do Spotify.",
        "tamanho_download": "~130 MB",
        "tamanho_instalado": "~360 MB",
        "url": "https://spotify.com",
        "licenca": "Proprietária",
        "dependencias": "alsa-lib, nss",
    },
    {
        "tipo": "Flatpak",
        "nome": "Discord",
        "exibicao": "Discord\nChat para gamers e comunidades.",
        "comando": "flatpak install com.discordapp.Discord",
        "icon_url": (
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/"
            "Discord_logo.svg/120px-Discord_logo.svg.png"
        ),
        "app_id": "com.discordapp.Discord",
        "versao": "Estável",
        "desc_completa": "Aplicação de chat de voz e texto.",
        "tamanho_download": "Via Flathub",
        "tamanho_instalado": "Variável",
        "url": "https://discord.com",
        "licenca": "Proprietária",
        "dependencias": "Runtimes Flathub",
    },
]
