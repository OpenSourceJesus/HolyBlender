I am running out of energy for this project, and it is slowing down. Also, please feel free to contribute!

# Name
Unity2Many

# Description
A set of tools for game and software development  Currently, three tools can be used (as well as an addon for Blender); UnityToUnreaal, UnityToBevy, and KritaToBlender.

UnityToUnreal and UnityToBevy translates a Unity project to an Unreal or Bevy project respectively. KritaToBlender is a tool that can be run in Krita to export the current document to Blender so that the content can be animated.

MakeBlenderPlugin.py (part of the BlenderPlugin tool) provides an interface in Blender for using the tools of this project. The export buttons for UnityToUnreal and UnityToBevy in the Blender interface are found in each Text Editor panel. The Unity project path, Unreal project path, and Bevy project path are found in the World settings.

# Installation
Inside the terminal program on your computer, type or copy and paste 'git clone https://github.com/OpenSourceJesus/Unity2Many --depth=1' and press the Enter key to download the files and folders of this project to your computer. Note that these installation steps require internet to be currently connected.

Then run (type the following and press enter) 'make install_UnityToUnreal' to install the required parts to translate a Unity project to an Unreal project. To install the parts for any of the other tools like UnityToBevy, KritaToBlender, or BlenderPlugin, run 'make install_' and then add the name of the tool to run as one command.

This project's translation tools rely on my forks of CSharpToPython (https://github.com/OpenSourceJesus/CSharpToPython) and py2many (https://github.com/OpenSourceJesus/py2many). Additionally, UnityToBevy relies on Blender_bevy_components_workflow (https://github.com/OpenSourceJesus/Blender_bevy_components_workflow).

## Requirements
Currently, only Linux operating systems are supported. All testing has been done on Ubuntu 23.10.

# Usage
Inside the terminal program on your computer, type or copy and paste 'python3 UnityToUnreal.py input={path to Unity project to translate from} output={path to Unreal project to translate to}' and press the Enter key. Replace '{', '}', and what is in between them with the path to the Unity project and the path to the Unreal project respectively. You can also add ' exclude={path or part of a path in the Unity project to exclude from the translation}' in the terminal command to not translate any files in the Unity project that contain what is in between the '{' and '}'. Note that using '~' as a replacement for '/home/{your computer account username}' in the termainal command will not work.

Currently, to use the KritaToBlender tool run the Krita program and then mouse over the 'Tools' dropdown at the top of Krita. Mouse over 'Scripts' and then click on 'Scripter'. Then, mouse over 'File' and click on 'Open'. Navigate to MakeKritaBlenderFile.py in the file browser that automatically opens and then double-click on that file in this file browser. Finally, click on the play button circled in this image:![alt text](image.png) to run the script.

# Support
Use this webpage to know what should be done in the future of this project (and what has been done) and feel free to add issues (entries) to it: 'https://github.com/OpenSourceJesus/Unity2Many/issues'. Also, my email is 'gileadcosman@gmail.com', and I would love to respond to any questions or comments you have.

# Roadmap
The tools UnityToStride and UnityToGodot have been started and will hopefully be done eventually. Also, adding spawning and prefab support to the translation tools will hopefully be done eventually. Additionally, support for using KritaToBlender, UnityToStride and UnityToGodot should be added to BlenderPlugin eventually. For viewing or contributing to the list of what should get be done in the future of this project (and what has been done), use this webpage: 'https://github.com/OpenSourceJesus/Unity2Many/issues'.

# Contributing
I will accept all contributions.

# Authors and acknowledgment
So far only I, Gilead Cosman, have worked on this project.

# License
MIT License

Copyright 2024 Gilead Cosman

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.