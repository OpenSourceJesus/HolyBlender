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

		def on_open_blender(self, btn):
			#self.close()
			open_holyblender()

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
