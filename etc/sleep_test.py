import time

def printer(string):
	for char in string:
		print(char, end='')
		time.sleep(0.5)
	print()

printer('. . . . .')

