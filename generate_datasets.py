import random
import json

variables = ["i", "x", "y", "n", "count", "val"]
funcnames = ["add", "square", "greet", "check"]
arrnames = ["nums", "items", "values", "data"]

templates = [
    ("{var}={num}","Assigns{num} to {var}"),
    ("{var}={num}+{num}","Adds and Assigns the addition to {var}"),
    # --- PRINT ---
    ("print({val})", "Prints the value {val}."),

    # --- SIMPLE IF ELSE ---
    ("""if {var} > {num}:
    print("Big")
else:
    print("Small")""",
     "Checks if {var} is greater than {num} and prints 'Big' or 'Small'."),

    # --- IF ELIF ELSE LADDER ---
    ("""if {var} == {num}:
    print("Equal")
elif {var} < {num}:
    print("Less")
else:
    print("Greater")""",
     "Checks if {var} equals, is less than, or greater than {num}, and prints the result."),

    # --- FOR LOOPS with range variants ---
    ("""for {var} in range({limit}):
    print({var})""",
     "Prints numbers from 0 to {limit_minus_1}."),

    ("""for {var} in range({start}, {end}):
    print({var})""",
     "Prints numbers from {start} to {end_minus_1}."),

    ("""for {var} in range({start}, {end}, {step}):
    print({var})""",
     "Prints numbers from {start} to {end_minus_1} stepping by {step}."),

    # --- FOR with continue ---
    ("""for {var} in range({limit}):
    if {var} == {skip}:
        continue
    print({var})""",
     "Loops from 0 to {limit_minus_1}, skips {skip}, and prints the remaining numbers."),

    # --- FOR with break ---
    ("""for {var} in range({limit}):
    if {var} == {stop}:
        break
    print({var})""",
     "Loops from 0 to {limit_minus_1}, stops early when {var} equals {stop}."),

    # --- NESTED FOR ---
    ("""for {var} in range({outer}):
    for j in range({inner}):
        print({var}, j)""",
     "Nested loops printing all pairs of numbers with {var} from 0 to {outer_minus_1} and j from 0 to {inner_minus_1}."),

    # --- NESTED FOR with condition ---
    ("""for {var} in range({outer}):
    for j in range({inner}):
        if j == {skip}:
            continue
        print(j)""",
     "Nested loops, skipping when j equals {skip}, printing remaining numbers."),

    # --- WHILE LOOP ---
    ("""while {var} < {limit}:
    print({var})
    {var} += 1""",
     "Prints {var} while it is less than {limit}, incrementing it each time."),

    # --- WHILE inside FOR ---
    ("""for {var} in range({limit}):
    while {var} < {stop}:
        print({var})
        {var} += 1""",
     "For each value in 0 to {limit_minus_1}, keeps printing {var} until it reaches {stop}."),

    # --- LIST + LEN ---
    ("""{arr} = [1, 2, 3, 4]
print(len({arr}))""",
     "Creates a list and prints its length."),

    ("""{arr} = [10, 20, 30]
print({arr}[1])""",
     "Creates a list and prints the element at index 1."),

    ("""{arr} = [0, 0, 0]
{arr}[1] = 99
print({arr})""",
     "Creates a list, updates index 1 with 99, and prints the list."),

    # --- SIMPLE FUNCTION ---
    ("""def {fname}({a}, {b}):
    return {a} + {b}
print({fname}(2, 3))""",
     "Defines a function {fname} that returns the sum of two values and calls it with 2 and 3."),

    ("""def {fname}({a}):
    print("Hello", {a})
{fname}("Alice")""",
     "Defines a function {fname} that prints a greeting with the argument, then calls it."),

    # --- FUNCTION with loop ---
    ("""def {fname}({a}):
    for i in range({limit}):
        print(i)
    return {a}

print({fname}(5))""",
     "Defines a function {fname} that prints numbers 0 to {limit_minus_1}, then returns its argument."),

    # --- RECURSIVE FACTORIAL ---
    ("""def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
print(factorial({num}))""",
     "Defines a recursive function to calculate factorial of {num} and prints it."),

    # --- RECURSIVE FIBONACCI ---
    ("""def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
print(fib({num}))""",
     "Defines a recursive function to calculate the {num}-th Fibonacci number and prints it."),

    # --- FUNCTION calling another function ---
    ("""def square(x):
    return x * x
def compute(y):
    return square(y) + 1
print(compute({num}))""",
     "Defines two functions: square and compute. compute calls square and adds 1, then prints result for {num}."),

    # --- FUNCTION with break ---
    ("""def find_first_even(n):
    for i in range(n):
        if i % 2 == 0:
            return i
    return -1
print(find_first_even({num}))""",
     "Defines a function that finds and returns the first even number up to {num}."),

    # --- FUNCTION with len() ---
    ("""def list_size(arr):
    return len(arr)
print(list_size([1, 2, 3, 4, 5]))""",
     "Defines a function that returns the length of a list and prints it."),
]

# --- GENERATE DATASET ---
dataset = []

for _ in range(5000):  # number of examples
    code, summary = random.choice(templates)

    var = random.choice(variables)
    a, b = random.sample(variables, 2)
    fname = random.choice(funcnames)
    arr = random.choice(arrnames)
    limit = random.randint(3, 10)
    start = random.randint(0, 3)
    end = start + random.randint(3, 10)
    step = random.randint(1, 3)
    skip = random.randint(1, max(1, limit - 1))
    stop = random.randint(1, max(1, limit - 1))
    num = random.randint(1, 10)
    outer = random.randint(2, 5)
    inner = random.randint(2, 5)
    outer_minus_1 = outer - 1
    inner_minus_1 = inner - 1

    filled_code = code.format(
        var=var, a=a, b=b, fname=fname, arr=arr,
        limit=limit, skip=skip, stop=stop, num=num,
        limit_minus_1=limit - 1,
        val=random.choice([num, f'"{fname}"']),
        start=start, end=end, end_minus_1=end - 1, step=step,
        outer=outer, inner=inner,
        outer_minus_1=outer_minus_1, inner_minus_1=inner_minus_1
    )

    filled_summary = summary.format(
        var=var, a=a, b=b, fname=fname, arr=arr,
        limit=limit, skip=skip, stop=stop, num=num,
        limit_minus_1=limit - 1, val=num,
        start=start, end=end, end_minus_1=end - 1, step=step,
        outer=outer, inner=inner,
        outer_minus_1=outer_minus_1, inner_minus_1=inner_minus_1
    )

    dataset.append({"code": filled_code, "summary": filled_summary})

# --- SAVE TO JSON ---
with open("codesage_dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)

print(f"Generated {len(dataset)} examples in codesage_dataset.json")
