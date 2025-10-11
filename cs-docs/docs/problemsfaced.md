# Problems Faced

Building **CodeSage** — a system that integrates a Tree-Walk Interpreter, AST-based summarization, and NLP-driven code explanation — was a challenging process.  
Throughout the project, several major and minor issues were encountered, both on the **NLP (Natural Language Processing)** side and the **compiler/interpreter** implementation side.

---

## 1. Lack of Suitable Dataset for NLP Training

One of the **primary challenges** in this project was the **unavailability of a proper dataset** to train the NLP engine.

- There was no existing dataset that matched the structure of the interpreter’s output or the format of code summaries required.  
- Public datasets (like CodeSearchNet or CodeT5 datasets) were either **too complex**, making them unsuitable for training a summarization model aligned with CodeSage’s interpreter logic.

###  Solution Attempt
To overcome this, a **custom template-based dataset** was created:
- Templates were manually designed for various code constructs (loops, functions, assignments, etc.).
- Each template included example code and a structured explanation.
- The dataset was later filtered and aligned with the interpreter’s grammar and AST patterns.

However, despite this effort, the model **did not yield accurate or meaningful results** due to:
- Insufficient training data
- Lack of variety in examples
- Model overfitting to repetitive patterns

### Result
Due to the low accuracy and unstable summarization quality, the project shifted focus from a **pure NLP-based summarization** to a **Tree-based summarization** approach.  
This allowed deterministic and consistent explanations derived directly from the **Abstract Syntax Tree (AST)**, ensuring interpretability and stability.

---

##  2. Complexity in Building Recursive-Descent Parser

Designing a **recursive-descent parser** manually required handling:
- Tokenization edge cases
- Parsing ambiguity (especially nested expressions)
- Error recovery (panic mode)
- Grammar synchronization between parser and interpreter

Even small syntax mistakes often caused cascading parse failures, making debugging time-consuming.

---

##  3. Tree-Walk Interpreter Challenges

Implementing a working **Tree-Walk Interpreter** involved:
- Managing nested scopes and variable environments  
- Handling return, break, and continue flow control correctly  
- Avoiding infinite loops or stack overflows in recursive evaluation  
- Debugging runtime errors that stemmed from incorrect AST traversal

The **scope resolution (Resolver)** also introduced complexity, since incorrect distance tracking caused runtime variable access errors.

---

## 🔍 4. Error Handling and Debugging

Runtime errors (like undefined variables or division by zero) were difficult to trace back to exact source lines.  
Adding meaningful error messages and implementing **panic mode recovery** in the parser required careful thought and testing.

---

##  Final Reflection

The biggest learning from these challenges was understanding **how theory from compiler design meets the practical constraints of AI and UI development**.  
While the NLP summarization goal was not fully achieved, the shift to a **Tree-based system** made CodeSage more reliable, interpretable, and educational — staying true to its core purpose:  
“To explain code, not just execute it.”
