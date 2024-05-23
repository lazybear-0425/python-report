def ex1():
	for i in range(1,4):
		yield i
	return 'END'
def ex2():
	x = yield from ex1()
	print('now :',x)
for y in ex2():
	print(y)
