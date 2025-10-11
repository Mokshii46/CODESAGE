#  AST Summarizer

##  Overview
The **AST Summarizer** is a component of CodeSage that **traverses the Abstract Syntax Tree (AST)** to generate **structured, human-readable summaries** of source code.  
It converts raw AST nodes into **plain-language explanations** describing the purpose and behavior of each part of the code.

The Summarizer works **without executing the code**, providing insights into program logic, control flow, and variable usage.  
It is particularly useful for **code comprehension, documentation, and education**.

---

##  Responsibilities

- Traverse all AST nodes (statements, expressions, functions, loops, conditionals).  
- Identify and summarize **control structures**, **expressions**, and **assignments**.  
- Generate structured summaries suitable for **NLP refinement**.  
- Avoid low-level syntax noise (like `<expr>` or raw token details).  
- Provide **line-specific and context-aware descriptions**.


---

##  Example

### Input Code:
```
a=25
if a >=18:
    print("Adult")
else:
    print("Child")

```
---

### Ouptput Summary

```
Assigning '25.0' to variable 'a'.
If statement: evaluates condition (a>=18). Executes 'then' branch if true; otherwise checks 'elif' branches or executes 'else' branch if present.
This is a binary operation '>=' between left (a) and right (18.0).
Block statement executing multiple statements sequentially.
Print statement printing the value of expression (Adult).
Else branch executes if all previous conditions are false.
Block statement executing multiple statements sequentially.
Print statement printing the value of expression (Child).

```

