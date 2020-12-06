# Install and configure Vim with plugins.

source: https://www.redhat.com/sysadmin/ansible-configure-vim

## Plugins

This playbook configures vim editor and install the following plugins:
- **name**: vim-airline, **description**: vim-airline is a powerful status and tab line for Vim., **url**: https://github.com/vim-airline/vim-airline
- **name**: nerdtree, **description**: The NERDTree is a file system explorer for the Vim editor.
  install_cmd: vim -u NONE -c "helptags ~/.vim/pack/vendor/start/nerdtree/doc" -c q
  default_shortcut: '<F5>', **url**: https://github.com/preservim/nerdtree
- **name**: fzf-vim, **description**: It's an interactive Unix filter for command-line that can be used with any list; files, command history, processes, hostnames, bookmarks, git commits, etc., **url**: https://github.com/junegunn/fzf.vim
- **name**: vim-gitgutter, **description**: A Vim plugin which shows a git diff in the sign column.
  install_command: vim -u NONE -c "helptags vim-gitgutter/doc" -c q, **url**: https://github.com/airblade/vim-gitgutter
- **name**: vim-fugitive, **description**: Fugitive is the premier Vim plugin for Git. Run git command (ie, :Git commit)
  install_command: vim -u NONE -c "helptags fugitive/doc" -c q, **url**: https://github.com/tpope/vim-fugitive
- **name**: vim-floaterm, **description**: Customizable terminal window style.
  default_shortcut: '<F12>', **url**: https://github.com/voldikss/vim-floaterm

# Default Vim config file: vimrc

```
execute pathogen#infect()
syntax on
filetype plugin indent on

colo darkblue

" Configuration vim Airline
set laststatus=2

let g:airline#extensions#tabline#enabled=1
let g:airline_powerline_fonts=1

" Configuration NERDTree
map <F5> :NERDTreeToggle<CR>

" Configuration floaterm
let g:floaterm_keymap_toggle = '<F12>'
let g:floaterm_width = 0.9
let g:floaterm_height = 0.9

" Configuration Vim.FZF
let g:fzf_preview_window = 'right:50%'
let g:fzf_layout = { 'window': { 'width': 0.9, 'height': 0.6  }  }
```

## Run de playbook

Execute the playbook using the ansible-playbook command and the playbook name. Since this playbook targets the localhost only, an inventory is not strictly required. You can still create one. Also, because one of the tasks requires privilege escalation, provide the parameter -K to type your sudo password, allowing Ansible to execute those tasks.

Note: Backup an existing .vimrc configuration file before running this playbook.

```
$ ansible-playbook vim-config.yaml \
    -K \
    --tags install_packages,install_plugins,configure
SUDO password: 

```
