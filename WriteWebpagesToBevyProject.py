import urllib.request, urllib.error, urllib.parse, asyncio, sys

BEVY_PROJECT_PATH = sys.argv[-1]

def WriteWebpageToFile (url : str, filePath : str):
	response = urllib.request.urlopen(url)
	webContent = response.read()
	open(filePath, 'wb').write(webContent)

async def WriteWebpagesToProject ():
	await asyncio.sleep(10)
	WriteWebpageToFile ('http://127.0.0.1:1334/api/wasm.js', BEVY_PROJECT_PATH + '/api/wasm.js')
	WriteWebpageToFile ('http://127.0.0.1:1334/api/wasm.wasm', BEVY_PROJECT_PATH + '/api/wasm.wasm')

asyncio.run(WriteWebpagesToProject ())