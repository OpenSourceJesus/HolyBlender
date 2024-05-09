install_UnityToGodot:
	sudo apt install python3
	python3 install_UnityToGodot.py

build_UnityToGodot:
	rm obj -r -f
	dotnet build Unity2Many.csproj -p:StartupObject=UnityToGodot -o=UnityToGodot

UnityToGodot:
	python3 UnityToGodot.py exclude=/Library

install_UnityToUnreal:
	sudo apt install python3
	python3 install_UnityToUnreal.py

build_UnityToUnreal:
	rm obj -r -f
	dotnet build Unity2Many.csproj -p:StartupObject=UnityToUnreal -o=UnityToUnreal

UnityToUnreal:
	python3 UnityToUnreal.py input=/home/gilead/TestUnityProject output=/home/gilead/Unity2Many/BareUEProject exclude=/Library

new_Unreal_project:
	echo 'Not made yet'

install_UnityToBevy:
	# sudo apt install python3
	python3 install_UnityToBevy.py

build_UnityToBevy:
	rm obj -r -f
	dotnet build Unity2Many.csproj -p:StartupObject=UnityToBevy -o=UnityToBevy

UnityToBevy:
	python3 UnityToBevy.py input=/home/gilead/TestUnityProject output=/home/gilead/Unity2Many exclude=/Library

install_KritaToBlender:
	# sudo apt install python3
	python3 install_KritaToBlender.py

KritaToBlender:
	python3 KritaToBlender.py 'include=/home/gilead/Slime.kra'

install_BlenderPlugin:
	# sudo apt install python3
	python3 install_BlenderPlugin.py

BlenderPlugin:
	python3 BlenderPlugin.py

install_UnityToStride:
	# sudo apt install python3
	python3 install_UnityToStride.py

UnityToStride:
	python3 UnityToStride.py

.PHONY: install_UnityToGodot build_UnityToGodot UnityToGodot install_UnityToUnreal build_UnityToUnreal UnityToUnreal new_Unreal_project install_UnityToBevy build_UnityToBevy UnityToBevy install_KritaToBlender KritaToBlender install_BlenderPlugin BlenderPlugin install_UnityToStride UnityToStride