import os

os.system('''sudo add-apt-repository ppa:flatpak/stable
	sudo apt update
	sudo apt install flatpak
	flatpak install flathub org.godotengine.Godot''')