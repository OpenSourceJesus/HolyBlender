import os

if not os.path.isdir('svg-path-properties'):
	os.system('''git clone https://github.com/regebro/svg.path.git --depth=1''')
os.system('''sudo apt install krita''')