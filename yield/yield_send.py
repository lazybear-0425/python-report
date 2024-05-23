def foo():
	print("start...")
	while True:
		throw = yield 10
		print("throw:",throw)
g = foo()
print(next(g))
print("*"*20)
print(g.send(100)) #注意這邊用send()
