import time

def wait_for_seconds(seconds):
	for i in range(seconds):
		yield i
		time.sleep(1)

for i in wait_for_seconds(5):
	print(i)