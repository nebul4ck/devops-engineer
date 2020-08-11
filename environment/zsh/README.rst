Configure ZSH
#############

1. Download and install ohmyzsh
2. Instalar Powerlevel9k theme
    https://github.com/Powerlevel9k/powerlevel9k/wiki/Install-Instructions#step-1-install-powerlevel9k3. Instalar powerline font
    cd ~/tmp
    wget https://github.com/powerline/powerline/raw/develop/font/PowerlineSymbols.otf
    wget https://github.com/powerline/powerline/raw/develop/font/10-powerline-symbols.conf
    xset q (para mirar el path)
    sudo mv PowerlineSymbols.otf /usr/share/fonts/X11/Type1/
    fc-cache -vf /usr/share/fonts/X11/Type1
    mkdir ~/.config/fontconfig/conf.d/
    mv 10-powerline-symbols.conf ~/.config/fontconfig/conf.d/•
    exit

4. Dejo algunos archivos de configuración de backup
    ~/.zshrc
    ~/.oh-my-zsh/themes/avit.zsh-theme

