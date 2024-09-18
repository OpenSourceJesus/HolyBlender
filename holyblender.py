#!/usr/bin/env python3
import os, sys, subprocess, atexit

try:
	import gi
except:
	gi = None

if gi:
	gi.require_version('Gtk', '3.0')
	from gi.repository import Gtk

	def run_frontend():
		w = HolyBlender()
		w.show_all()
		Gtk.main()

	class HolyBlender(Gtk.Window):
		def __init__(self):
			super().__init__(title="HolyBlender")
			self.connect("destroy", Gtk.main_quit)

			self.set_default_size(180, 200)
			vbox = Gtk.VBox(spacing=6)
			self.add(vbox)
			btn = Gtk.Button(label='Open HolyBlender')
			btn.connect("clicked", self.on_open_blender)
			vbox.pack_start(btn, False, False, 0)

			btn = Gtk.Button(label='Make Character')
			btn.connect("clicked", self.on_open_ink)
			vbox.pack_start(btn, False, False, 0)

		def on_open_blender(self, btn):
			open_holyblender()
		def on_open_ink(self, btn):
			open_ink3d()

def open_ink3d():
	if not os.path.isdir('./inkscape2019'):
		cmd = 'git clone --depth 1 https://github.com/brentharts/inkscape2019.git'
		print(cmd)
		subprocess.check_call(cmd.split())
	cmd = ['python3', './inkscape.py']
	print(cmd)
	subprocess.check_call(cmd, cwd='./inkscape2019')

def open_holyblender():
	cmd = ['python3', './BlenderPlugin.py']
	print(cmd)
	proc = subprocess.Popen(cmd)
	atexit.register(lambda : proc.kill())
	return proc

if __name__=='__main__':
	if gi:
		run_frontend()
	else:
		if os.path.isfile('/usr/bin/dnf'):
			print('you need to run: sudo dnf install python3-gobject')
		else:
			print('you need to run: sudo apt install python3-gi')
