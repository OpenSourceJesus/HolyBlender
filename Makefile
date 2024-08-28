install_UnityToGodot:
	sudo apt install python3
	python3 install_UnityToGodot.py

build_UnityToGodot:
	rm obj -r -f
	dotnet build HolyBlender.csproj -p:StartupObject=UnityToGodot -o=UnityToGodot

UnityToGodot:
	python3 UnityToGodot.py exclude=/Library

install_UnityToUnreal:
	sudo apt install python3
	python3 install_UnityToUnreal.py

build_UnityToUnreal:
	rm obj -r -f
	dotnet build HolyBlender.csproj -p:TargetFramwork=net6.0 -p:StartupObject=UnityToUnreal -o=UnityToUnreal

UnityToUnreal:
	python3 UnityToUnreal.py input=~/HolyBlender-TestUnityProject output=~/HolyBlender/BareUEProject exclude=/Library

new_Unreal_project:
	echo 'Not made yet'

install_UnityToBevy:
	# sudo apt install python3
	python3 install_UnityToBevy.py

build_UnityToBevy:
	rm obj -r -f
	dotnet build HolyBlender.csproj -p:TargetFramwork=net8.0 -p:StartupObject=UnityToBevy -o=UnityToBevy

UnityToBevy:
	python3 UnityToBevy.py input=~/HolyBlender-TestUnityProject output=~/HolyBlender exclude=/Library

install_KritaToBlender:
	# sudo apt install python3
	python3 install_KritaToBlender.py

KritaToBlender:
	python3 KritaToBlender.py 'include=~/Slime.kra'

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

build_UnityInBlender:
	rm obj -r -f
	dotnet build HolyBlender.csproj -p:TargetFramwork=net8.0 -p:StartupObject=UnityInBlender -o=UnityInBlender

build_CSToPython:
	rm obj -r -f
	dotnet build HolyBlender.csproj -p:TargetFramwork=net8.0 -p:StartupObject=CSToPython -o=CSToPython

build_UnityToPygame:
	rm obj -r -f
	dotnet build HolyBlender.csproj -p:TargetFramwork=net8.0 -p:StartupObject=UnityToPygame -o=UnityToPygame

install_HtmlExport:
	# sudo apt install python3
	python3 install_HtmlExport.py

.PHONY: install_UnityToGodot build_UnityToGodot UnityToGodot install_UnityToUnreal build_UnityToUnreal UnityToUnreal new_Unreal_project install_UnityToBevy build_UnityToBevy UnityToBevy install_KritaToBlender KritaToBlender install_BlenderPlugin BlenderPlugin install_UnityToStride UnityToStride build_UnityInBlender build_CSToPython build_UnityToPygame, install_HtmlExport