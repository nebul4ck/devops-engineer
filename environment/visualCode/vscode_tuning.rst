Visual Studio Code

1 Install Visual Studio Code

  .. code:: console

	$ sudo apt update
	$ sudo apt install software-properties-common apt-transport-https wget
	$ wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
	$ sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
	$ sudo apt update
	$ sudo apt install code
  ..
2 Install restructuredText plugin and linters 
3 Install python plugin and linters
4 Install additional thems

	Para cambiar el tema:

	Ctrl+K Ctrl+T

	Para instalar temas adiccionales, por ejemplo "Material Theme"

		Ctrl+P
		ext install material theme
		Enter
		Select "Mattia Astorino as author"



Community Material Them High contrast
Material Theme
Solarized Dark

Cambiar iconos: File > Preferences > FIle Icons Thems 
	Material them icons light


Activar el color de fuentes activas y notificaciones

	Ctrl + Shift + P > Type material theme, choose Material Theme: Set accent color, and pick one color from the list.


Keymaps#
Are you used to keyboard shortcuts from another editor? You can install a Keymap extension that brings the keyboard shortcuts from your favorite editor to VS Code. Go to Preferences > Keymap Extensions to see the current list on the Marketplace. Some of the more popular ones:

Vim


Customize your keyboard shortcuts#
Keyboard Shortcut: Ctrl+K Ctrl+S

Abre los settings via comandos JSON

	Ctrl + Shift + P > Open Settings (JSON) 