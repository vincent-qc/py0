<img src="https://github.com/vincent-qc/py0/blob/main/assets/banner.png" alt="Alt Text" width="300" height="150">

>C0 but Python. What could go wrong...

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

### Contracts
To ensure code safety and correctness can be proved, contracts are introduced. In particular, preconditions, postconditions, and loop invariants can be direct implemented

Preconditions can be declared following a function decleration as such. If a precondition is not met, Py0 immediately exits execution.
```py
requires bar is not None
def foo(bar):
  # implementation
```

Similarily, postconditions can be implemented as follows. `\res` is used to denote the value that is returned from the function
```py
ensures \res is not None
def baz():
  var = None
  var = "not none"
  return var
```

Finally, loop invariants can be declared both before `for` loops and `while` loops.
```py
loop_invariant x >= 0
for x in range(10):
  print(x)
```
or
```py
var = 1

loop_invariant var >= 1
while True:
  var = var * 2
```


### Tags
For the sake of... writing good code, once a variable is declared, its type cannot be changed. Similar to C0, variables are immediately "tagged" with their respective type upon decleration.

Therefore, unlike python, this is not valid code.
```py
qux = "str" # type is defined as str
quz = 1 # cannot assign into str
```

As a result, in order to prove safety, a function to check if a variable is defined to be a certain type, `hastag`, is provided.
```py
foo_bar = "baz"
print(hastag(foo_bar, str)) # True
print(hastag(foo_bar, int)) # False
```

### Functions
`TODO`
