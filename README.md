![alt text](Images/image-1.png)
![alt text](Images/image-2.png)

Please feel free to contribute!

# Description
This project is for people to use Blender to write code, attach scripts to objects, and then export to Unity, Unreal, Godot, Bevy, or Net Ghost Science Engine.

Additionally, three tools can be used from the command line: UnityToUnreal, UnityToBevy, and KritaToBlender.

UnityToUnreal and UnityToBevy translate a Unity project to an Unreal or bevy project respectively. KritaToBlender is a tool that can be run in Krita to export the current document to Blender so that the content can be animated.


# Installation
Inside the terminal program on your computer, type or copy and paste 'cd ~' and press the Enter key to change directory to your account folder. Then run (type or copy and paste the following and then press Enter) 'git clone https://github.com/OpenSourceJesus/HolyBlender --depth=1' to download the files and folders of this project to the current folder (your account folder). Note that these installation steps except for the first step require internet connection.

Then run 'sudo apt -y install make' to install make.

Now, run 'cd HolyBlender' to change directory to HolyBlender.

## Requirements
Currently, only Linux operating systems are supported. Testing has only been done on Ubuntu 23.10, Ubuntu 24.04, and Pop!_OS 22.04.

# Basic Usage

```bash
python3 BlenderPlugin.py
```

# BlenderPlugin.py
```
python3 BlenderPlugin.py [.blend|.py] [--OPTIONS]
```

In Blender, the export buttons and export paths are in the World Properties. The dropdowns for attaching and detaching scripts are in the Object Properties. All other interface items are found in the Text Editor after you make a text block. Having the 'Unity project import path' empty in the World Properties will export from Blender rather than exporting from the Unity project at the 'Unity project import path'.

For using UnityToBevy without the BlenderPlugin, in the terminal run 'python3 UnityTobevy.py input={path to Unity project to translate from} output={path to bevy project to translate to}'. Replace '{', '}', and what is in between them with the path to the Unity project and the path to the bevy project respectively. You can also add ' exclude={path or part of a path in the Unity project to exclude from the translation}' in the terminal command to not translate any files in the Unity project that contain what is in between the '{' and '}'. UnityToUnreal uses the same rules.

Currently, to use the KritaToBlender tool run the Krita program and then mouse over the 'Tools' dropdown at the top of Krita. Mouse over 'Scripts' and then click on 'Scripter'. Then, mouse over 'File' and click on 'Open'. Navigate to MakeKritaBlenderFile.py in the file browser that automatically opens and then double-click on that file in this file browser. Finally, click on the play button circled in this image:![alt text](Images/image.png) to run the script.

Also, I made this project for testing as an input Unity project for translation: 'https://github.com/OpenSourceJesus/HolyBlender-TestUnityProject'.

# Testing
```bash
python3 BlenderPlugin.py --test-unity
python3 BlenderPlugin.py --test-html
python3 BlenderPlugin.py --test-bevy
```

## Notes

For Unity exports, scripts only get exported if they are attached to objects.

For Unity exports, collections are exported as prefabs. Currently, prefabs instanced as a scene don't have their contents inside the Unity scene.

For Unity exports, mark classes derived from MonoBehaviour with the 'Is MonoBehaviour' checkbox for them to get attacehd to the corresponding GameObjects.

Some comments are treated as code in the output of translations (not desired behvaior).

In UnityToBevy, when float variables in C# scripts are declared they need to be set to a value that contains a decimal and has an 'f' at the end for proper translation.

Currently, there isn't a way to have nested prefabs when exporting from Blender to Unity.

Currently, exporting mesh objects from Blender won't work properly unless a version of Unity is installed.

This project's translation tools rely on my forks of CSharpToPython (https://github.com/OpenSourceJesus/CSharpToPython) and py2many (https://github.com/OpenSourceJesus/py2many). Additionally, UnityToBevy relies on my fork of Blender_bevy_components_workflow (https://github.com/OpenSourceJesus/Blender_bevy_components_workflow).

# Support
Use this webpage to know what should be done in the future of this project (and what has been done) and feel free to add issues (entries) to it: 'https://github.com/OpenSourceJesus/HolyBlender/issues'. Also, my email is 'gileadcosman@gmail.com', and I would love to respond to any questions or comments you have.

# Roadmap
The tools UnityToGodot, and UnityToPygame have been started and will hopefully be done eventually. Also, adding spawning and prefab support to the translation tools will hopefully be done eventually. Additionally, support for using KritaToBlender, UnityToStride, UnityToGodot, and UnityToPygame should be added to BlenderPlugin eventually. For viewing or contributing to the list of what should get be done in the future of this project (and what has been done), use this webpage: 'https://github.com/OpenSourceJesus/HolyBlender/issues'.

# Contributing
I will accept all contributions.

# Authors and acknowledgment
So far Brent Hartshorn and I (Gilead Cosman), have worked on this project.

# License
MIT License

Copyright 2024 Gilead Cosman

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
