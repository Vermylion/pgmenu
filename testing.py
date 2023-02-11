#test1 = 'hello'

def starter(string):
    global test1; test1 = string
starter('hello')

def func(var = test1):
    global test1
    print(var)
    test1 = 'hey'

starter('hey')
input()
func()
func()