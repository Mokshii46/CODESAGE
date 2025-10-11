# CodeSage — AI-Powered Code Interpreter & Explainer

For full documentation-->[https://Mokshii46.github.io/CODESAGE/]
**CodeSage** is a Python-based framework that combines **compiler principles**, **tree-walk interpretation**, and **AI-based summarization** to not only execute code but also explain it in human-readable form.  
It is designed to help developers, students, and educators **understand code behavior and structure**.

---

##  Pipeline Overview

CodeSage processes code through several well-defined stages:

1. **Scanner / Lexer**  
   - Reads raw source code character by character.  
   - Converts it into **tokens** (keywords, operators, literals, identifiers).  
   - Detects lexical errors (unrecognized symbols, missing delimiters).  

2. **Parser**  
   - Applies a **recursive descent parser** to transform tokens into an **Abstract Syntax Tree (AST)**.  
   - The AST represents the **logical and hierarchical structure** of the code.  
   - Detects syntax errors and provides meaningful error messages.  

3. **AST Summarizer**  
   - Traverses the AST to create **structured summaries** of code behavior.  
   - Converts programming constructs (loops, conditionals, assignments) into readable explanations.  

4. **Interpreter (Tree-Walk Execution)**  
   - Executes the AST recursively.  
   - Evaluates expressions, executes statements, handles loops, functions, and conditionals.  
   - Provides runtime output, including results of calculations and print statements.  

5. **NLP Integration (Optional)**  
   - Takes the AST summaries and refines them using **natural language models**.  
   - Produces **human-like explanations** of the code’s logic.  

6. **GUI / IDE**  
   - Built with Tkinter, the interface integrates:  
     - Code editor  
     - Output console  
     - AST visualization  
     - Summaries and explanations  

---

## Results

CodeSage can handle a variety of Python constructs:

- Variable declarations and assignments  
- Arithmetic and logical operations  
- Loops (`for`, `while`) and conditionals (`if`, `elif`, `else`)  
- Functions, return statements, and built-in utilities (`len`, `range`)  
- Lists and index-based operations  

Example snippet:

```
x = 0
while x < 5:
    print(x)
    x = x + 1
```
![alt text](image.png)

## Problems Faced

- Lack of suitable dataset for NLP training:
    - Initially, no proper code-summary dataset was available.
    -  Had to create a custom template-based dataset and filter it according to the interpreter’s capabilities.
    - Even after training, the NLP output lacked accuracy, so the system shifted toward AST-based summarization.
    
##  Future Prospects
- Advanced NLP Integration: Use pre-trained models like CodeT5 or LLaMA for more natural explanations.
- Extended Language Features: Classes, modules, and advanced Python constructs.
- Web-Based IDE: Replace Tkinter with a modern web interface for better usability.
- Real-Time Code Explanation: Summarize code dynamically as users type.

## Mentors
 - Yadnyesh Patil
 - Rupak Gupta

## Contributers
 - Mokshi Shah