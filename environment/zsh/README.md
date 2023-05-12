# Install and configure ZSH with plugins and fonts

## Requirements
(todo add to ansible zsh role)

* Install zsh-autosuggestions => github.com/zsh-users/zsh-autosuggestions
* Install fuzzy-finder git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
* Install aws-iam-authenticator => https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html
* (private) see private files into mediaCenter for kubeconfig, zshrc, zsh_history configuration
* Install aws session manager plugin: https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html#install-plugin-linux
* Install brew: ```/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"```
* Install k9s: ```https://k9scli.io/topics/install/```


## Overview

The following packages will be downloaded/cloned, installed and configured.

* **name**: zsh, **description**: ZSH, also called the Z shell, is an extended version of the Bourne Shell (sh), with plenty of new features, and support for plugins and themes., **package**: zsh

- **name**: Oh My Zsh., **description**: Oh My Zsh is an open source, community-driven framework for managing your zsh configuration., **url**: https://ohmyz.sh/

- **name**: Powerlevel10k Theme, **description**: Powerlevel10k is a theme for Zsh. It emphasizes speed, flexibility and out-of-the-box experience., **url**: https://github.com/romkatv/powerlevel10k

- **name**: Powerline Fonts and Symbols, **description**: Powerline is a statusline plugin for vim, and provides statuslines and prompts for several other applications, including zsh, bash, fish, tmux, IPython, Awesome, i3 and Qtile., **url**: https://github.com/powerline/powerline/raw/develop/font/PowerlineSymbols.otf | https://github.com/powerline/powerline/raw/develop/font/10-powerline-symbols.conf

- **name**: awesome-terminal-fonts, **description**: Use fancy symbols in your standard monospace font., **url**: https://github.com/gabrielelana/awesome-terminal-fonts.git

- **name**: fonts-powerline by apt/yum, **description**: powerline symbols font., **url**: Debian/RedHat repositories

- **name**: python-fontforge, **description**: font editor - Python bindings, **url**: Debian/RedHat repositories

- **name**: Install xclip., **description**: Create xclip Alia to use clipboard as MacOS., **url**: by zsh aliases.

## How to install

1. Clone the repository
2. move to environment/zsh/ansible-role folder
3. Run the playbook:
```
$ ansible-playbook zsh-tunning.yaml \
  -K \
  --tags install_packages,configure,optional
```

# Troubleshooting

Fix vscode fonts problem https://github.com/romkatv/powerlevel10k/issues/671
