# 🧠 CodeSage — AI Code Interpreter & Explainer

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![AST](https://img.shields.io/badge/AST-Parser-teal)
![NLP](https://img.shields.io/badge/NLP-Summarizer-coral)
![GUI](https://img.shields.io/badge/Tkinter-GUI-blue)
![Terminal](https://img.shields.io/badge/Mode-Terminal-green)
![License](https://img.shields.io/badge/License-Open%20Source-lightgrey)

---

## 🌿 Overview

**CodeSage** is a Python framework that combines **compiler principles**, **tree-walk interpretation**, and **AI-based summarization** to not just run your code — but explain it in plain English.

It reads Python source code, tokenizes it, builds an Abstract Syntax Tree, interprets it live, and produces a structured plain-English summary of what the code does — all available via a **Tkinter GUI** or a **terminal mode**.

📖 [Documentation](https://Mokshii46.github.io/CODESAGE/) &nbsp;|&nbsp; 🐙 [GitHub](https://github.com/Mokshii46/CODESAGE)

---

## ✨ Key Features

- **Scanner / Lexer** — Tokenizes raw source character by character; catches unrecognized symbols early
- **Recursive Descent Parser** — Produces a full AST with meaningful syntax error messages
- **AST Summarizer** — Converts loops, conditionals, and assignments into readable plain English
- **Tree-Walk Interpreter** — Evaluates expressions and executes code live from the AST
- **NLP / GPT Integration** *(optional)* — AI-powered line-by-line explanations via GPT-4o-mini
- **GUI Mode** — Tkinter interface with code editor, output console, AST summary panel, and colored AST tree
- **Terminal Mode** — Scanner output, parser AST, plain English summary, and execution result in the terminal

---

## 📊 At a Glance

| Metric | Value |
|---|---|
| Pipeline stages | 6 |
| Run modes | 2 (GUI + Terminal) |
| Python constructs supported | 5+ |

---

## 🖥️ Two Ways to Run

### GUI Mode
Full Tkinter interface with code editor, interpreter output, AST summary, and colored AST tree — all in one window. Uses the local tree-walk interpreter; no API key required.

```bash
python -m codesage.gui
```

### Terminal Mode
Type code directly in the terminal. Get scanner output, parser AST, plain English summary, and execution result.

```bash
python main.py
```

> Uncomment the GPT block in `main.py` to enable AI-powered summaries.

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Mokshii46/CODESAGE.git
cd CODESAGE
```

### 2️⃣ Set Up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🧬 How It Works — Pipeline

| Stage | Name | Description | Tag |
|---|---|---|---|
| 1 | Scanner / Lexer | Reads raw source character by character; converts to tokens (keywords, operators, literals, identifiers); catches unrecognized symbols early | lexical analysis |
| 2 | Recursive Descent Parser | Transforms the token stream into an AST capturing the logical, hierarchical structure; generates meaningful syntax error messages | syntax analysis |
| 3 | AST Summarizer | Traverses the AST node by node, converting constructs — loops, conditionals, assignments — into structured, readable plain English | code summarization |
| 4 | Tree-Walk Interpreter | Recursively executes the AST — evaluates expressions, runs loops and functions, handles conditionals — producing live runtime output | execution |
| 5 | NLP / GPT Integration *(optional)* | Uncomment the GPT block in `main.py` to enable AI-powered line-by-line explanations via GPT-4o-mini. Requires an OpenAI API key in `.env` | natural language |
| 6 | GUI / IDE | Built with Tkinter — code editor, output console, AST summary panel, and colored AST tree visualization all in one window | tkinter |

---

## 📺 Example Output

**Input code:**
```python
i = 0
while i < 5:
    print(i)
    i = i + 1
```

**AST Summary:**
```
→ Assigning '0' to variable 'i'
→ While loop: runs while i < 5
→ Print value of i each iteration
→ Increment i by 1

Interpreter output: 0 1 2 3 4
```

**GUI Panel Output:**
```
── Code input ──────────────────────────
i = 0
while i < 5:
    print(i)
    i = i + 1

── Interpreter Output ──────────────────
0 · 1 · 2 · 3 · 4

── AST Summary ─────────────────────────
Assigning '0.0' to variable 'i'
While loop: repeatedly executes body while condition is true
Print statement printing the value of expression

── AST Tree ────────────────────────────
└── Expression
    └── Assign
└── While
```

---

## 🧩 Supported Python Constructs

| Construct | Details |
|---|---|
| Variables | Declarations, assignments, arithmetic & logical operations |
| Loops | `for` and `while` with full iteration support |
| Conditionals | `if`, `elif`, `else` branching |
| Functions | Return statements & built-ins like `len`, `range` |
| Lists | Index-based access and list operations |

---

## 🗂️ Project Structure

```
CODESAGE/
├── main.py                    # Terminal entry point
├── README.md
├── requirements.txt           # added
├── .gitignore                 # added
├── .env                       # gitignored
├── codesage/                  # core package
│   ├── __init__.py
│   ├── scanner.py
│   ├── parser.py
│   ├── interpreter.py
│   ├── resolver.py
│   ├── nlp.py
│   └── gui.py                 # GUI entry point
├── nlp/                       # training pipeline
│   ├── train.py
│   ├── train_gpt.py
│   ├── decoder.py
│   ├── filter.py
│   ├── generate_datasets.py
│   └── prepare_embeddings.py
├── models/                    # gitignored
├── data/                      # datasets
└── assets/                    # images
```

---

## ⚠️ Challenges Faced

- No suitable NLP training dataset was available initially
- Built a custom template-based dataset filtered to interpreter capabilities
- NLP accuracy gaps led to a pivot toward AST-based summarization as the primary explanation method

---

## 🚀 Roadmap

- Integrate CodeT5 / LLaMA for richer, more nuanced code explanations
- Add support for classes, modules, and advanced Python constructs
- Replace Tkinter with a modern web-based IDE
- Real-time explanation as users type

---

## 🧰 Tech Stack

| Area | Technology |
|---|---|
| Language | Python 3.9+ |
| GUI | Tkinter |
| AST & Parsing | Python `ast` module + custom recursive descent parser |
| NLP / AI | OpenAI GPT-4o-mini *(optional)* |
| NLP Training | Custom template-based dataset |

---

## 👥 Team

### Mentors
**Yadnyesh Patil** — Mentor, Project X · VJTI  
**Rupak Gupta** — Mentor, Project X · VJTI

### Contributors
**Mokshi Shah** — Developer · VJTI 
---

## ⚠️ Notes
- No API key is required to run the core interpreter or GUI
- GPT-4o-mini integration requires an OpenAI API key stored in `.env` (gitignored)
- The `.env` file and `models/` directory are both excluded from version control

---

⭐ *If you find CodeSage useful, consider starring the repo!*
