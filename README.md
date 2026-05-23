# CodeSage — AI-Powered Code Interpreter & Explainer

> A Python framework combining **compiler principles**, **tree-walk interpretation**, and **AI-based summarization** to not just run your code — but explain it in plain English.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![AST](https://img.shields.io/badge/AST-Tree--Walk-6c5ce7?style=flat-square)
![NLP](https://img.shields.io/badge/NLP-Rule--based-00b894?style=flat-square)
![GUI](https://img.shields.io/badge/GUI-Tkinter-e17055?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

📄 **[Full Documentation →](https://Mokshii46.github.io/CODESAGE/)**

---

## What is CodeSage?

CodeSage helps developers, students, and educators **understand code behaviour and structure** — not just run it. It parses Python code into an Abstract Syntax Tree, walks it to produce structured summaries, and optionally refines them into natural language explanations through a built-in Tkinter IDE.

---

## Pipeline

```
Source Code
     │
     ▼
┌─────────────┐    Tokenizes raw source into keywords,
│   Scanner   │ →  operators, literals, identifiers
└─────────────┘    Catches unrecognized symbols early
     │
     ▼
┌─────────────┐    Recursive descent builds an
│   Parser    │ →  Abstract Syntax Tree (AST)
└─────────────┘    Generates meaningful syntax errors
     │
     ▼
┌───────────────┐  Traverses AST node by node,
│ AST Summarizer│→ converts constructs to readable text
└───────────────┘
     │
     ▼
┌──────────────────────┐  Recursively executes the AST —
│ Tree-Walk Interpreter│→ evaluates expressions, runs loops,
└──────────────────────┘  handles functions & conditionals
     │
     ▼
┌──────────────────┐   (Optional) Refines AST summaries
│ NLP Integration  │→  into human-like prose using NL models
└──────────────────┘
     │
     ▼
┌──────────┐   Editor + console + AST view +
│ GUI/IDE  │→  explanation panel in one window
└──────────┘
```

---

## Supported Constructs

| Construct | Details |
|-----------|---------|
| Variables | Declarations, assignments, arithmetic & logical ops |
| Loops | `for` and `while` with full iteration |
| Conditionals | `if`, `elif`, `else` branching |
| Functions | Return statements & built-ins (`len`, `range`) |
| Lists | Index-based access and list operations |

**Example input:**
```python
# print numbers 0 to 4
x = 0
while x < 5:
    print(x)
    x = x + 1
```

**CodeSage output:**
```
→ Interpreter output
0 · 1 · 2 · 3 · 4

→ Plain English explanation
x starts at 0. The while loop runs as long as x is less than 5,
printing x each time and incrementing it by 1. Loop exits when x reaches 5.
```

---

## Challenges Faced

**No suitable NLP dataset**
No proper code-summary dataset existed. A custom template-based dataset was built and filtered to match the interpreter's capabilities.

**NLP accuracy limitations**
Even after training, NLP output lacked precision — leading to a strategic pivot toward AST-based summarization as the primary engine, with NLP as an optional refinement layer.

---

## Roadmap

- **Advanced NLP** — integrate CodeT5 / LLaMA for richer explanations
- **Extended language support** — classes, modules, imports, advanced constructs  
- **Web-based IDE** — replace Tkinter with a modern browser interface
- **Real-time explanation** — summarize code live as the user types

---

## Team

**Mentors**
- Yadnyesh Patil · Project X, VJTI
- Rupak Gupta · Project X, VJTI

**Contributors**
- Mokshi Shah · VJTI
