def IndexOf (array : [], value):
	if value in array:
		return array.index(value)
	else:
		return -1

def Equals (array : [], array2 : []):
	if len(array) != len(array2):
		return False
	else:
		for i in range(len(array)):
			if array[i] != array2[i]:
				return False
	return True