# Results and Demonstrations

This document presents sample **code snippets** and their corresponding **outputs** produced by the CodeSage interpreter.  
Each snippet demonstrates how different language constructs — variables, expressions, conditionals, loops, and functions — are executed in the tree-walk interpreter.

---
## 1️.Variable Declaration & Assignment

```
x = 10
y = 5
print(x + y)

```
![alt text](image-6.png)

---


## 2.Variable Declaration & Assignment
```
print (3 + 5 * 2 - 4 / 2)

```
![alt text](image-7.png)

---

## 3️.Comparison & Logical Operators
```
a = 10
b = 20
print(a < b)
print(a > b)
print(a == b)
print(a != b)
print(a < b and b > 15)
print(a > b or a == 10)
```
![alt text](image-8.png)

---

## 4.If–Else Statements
```
score = 72
if score >= 50:
    print("Pass")
else:
    print("Fail")
```
![alt text](image-9.png)

---

## 5.If–Elif–Else Chain
```
marks = 85
if marks >= 90:
    print("Excellent")
elif marks >= 75:
    print("Good")
else:
    print("Needs Improvement")

```
![alt text](image-10.png)

---
## 6.While Loop
```
i = 0
while i < 5:
    print(i)
    i = i + 1
```

![alt text](image-11.png)

---

## 7️.For Loop (with range)
```
for i in range(3):
    print(i)
```
![alt text](image-12.png)

---

## 8.Break and Continue
```
for i in range(5):
    if i == 2:
        continue
    if i == 4:
        break
    print(i)
```
![alt text](image-13.png)

---

## 9.Function Definition and Return
```
def add(a, b):
    return a + b

result = add(4, 6)
print(result)
```
![alt text](image-14.png)

---

## 10.Nested Function Calls
```
def square(x):
    return x * x

def double(y):
    return y + y

print(double(square(3)))
```
![alt text](image-15.png)

---

## 11.Lists and Indexing
```
items = [10, 20, 30]
print(items[0])
items[1] = 100
print(items)
```

![alt text](image-16.png)

---

## 12.Range Expression
```
for i in range(2, 8, 2):
    print(i)
```

![alt text](image-17.png)

## 13.Len Function
```
nums = [1, 2, 3, 4]
print(len(nums))
```
![alt text](image-18.png)
