# CodeSage — AI-Powered Code Interpreter & Explainer

> A Python framework combining compiler principles, tree-walk interpretation, and AI-based summarization to execute and explain code in plain English.

📄 **[Full Documentation →](https://Mokshii46.github.io/CODESAGE/)**

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![NLP](https://img.shields.io/badge/NLP-Rule--based-purple?style=flat-square)
![AST](https://img.shields.io/badge/AST-Tree--Walk-green?style=flat-square)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange?style=flat-square)

---

## What is CodeSage?

**CodeSage** helps developers, students, and educators **understand code behavior and structure** — not just run it. It parses Python code into an Abstract Syntax Tree, walks it to produce structured summaries, and optionally refines them into natural language explanations.

---

## Pipeline Overview

```
Source Code
    │
    ▼
┌─────────────┐
│   Scanner   │  →  Tokenizes raw source (keywords, operators, literals)
└─────────────┘
    │
    ▼
┌─────────────┐
│   Parser    │  →  Recursive descent → builds Abstract Syntax Tree (AST)
└─────────────┘
    │
    ▼
┌───────────────┐
│ AST Summarizer│  →  Converts constructs into readable structured summaries
└───────────────┘
    │
    ▼
┌─────────────────────┐
│ Tree-Walk Interpreter│ →  Executes the AST recursively, produces output
└─────────────────────┘
    │
    ▼
┌──────────────────┐
│ NLP Integration  │  →  (Optional) Refines summaries into human-like prose
└──────────────────┘
    │
    ▼
┌──────────┐
│ GUI/IDE  │  →  Tkinter: editor + console + AST view + explanations
└──────────┘
```

---

## Supported Constructs

| Construct | Details |
|-----------|---------|
| Variables | Declarations, assignments, arithmetic & logical ops |
| Loops | `for`, `while` with full iteration |
| Conditionals | `if`, `elif`, `else` branching |
| Functions | Return statements, built-ins (`len`, `range`) |
| Lists | Index-based access and list operations |

**Example input:**
```python
x = 0
while x < 5:
    print(x)
    x = x + 1
```

---

## Challenges Faced

- No suitable NLP training dataset existed initially
- Built a custom template-based dataset filtered to the interpreter's capabilities
- NLP accuracy gaps led to a strategic pivot toward AST-based summarization as the primary explanation engine

---

## Future Prospects

- **Advanced NLP** — integrate CodeT5 or LLaMA for richer, more natural explanations
- **Extended Language Features** — classes, modules, and advanced Python constructs
- **Web-Based IDE** — replace Tkinter with a modern browser interface
- **Real-Time Explanation** — summarize code dynamically as users type

---

## Team

**Mentors**
- Yadnyesh Patil
- Rupak Gupta

**Contributors**
- Mokshi Shah
