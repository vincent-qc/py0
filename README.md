# Py0
> C0 but Python. What could go wrong...

## About
Py0 is an interpreted, dynamically-typed, language designed to remove complixities of python. Similar to what C0 does to C, Py0 literally removes every ~~useful~~ unsafe aspect of Python, in order to make it easier to use.

## Try
`TODO`

## Documentation
### Variables

Simple variables can be declared as such, that is, the same as how variables are declared in python.
```py
num = 10
str = "foo"
```

Arrays are also supported with the same syntax as python.
```py
arr = [1, 2, 3]
```

To ensure simplicity, Py0 is dynamically typed, with three primitive types: `int`, `float`, and `str`.
```
int = 1
float = 2.0
str = "bar"
```

### Comments
Comments are supported as such. Similar to python, there are no multiline comments.
```py
# This is a comment
```

### Control Flow

Similar to python, Py0 introduces control flow with syntax identical to python.

If, elif, and else statements are supported as such
```py
index = 0

if index == 0:
  print("zero")

elif index == 1:
  print("one")

else:
  print("other")
```
Like python, variables are scoped within their blocks, which are defined by their level of indentation.

Next, loops can be implemented using `for` loops or `while` loops. While loops are identical to python, and accept a single condition.
```py
index = 0

while index < 10:
  index = index + 1

print(index) # 10
```

For loops are closely similar to python, where the iterator must be an array.
```py
for var in iterator:
  print(var)
```

### Functions
`TODO`
