import tkinter as tk
from tkinter import scrolledtext, font
from scanner import Scanner
from parser import Parser, ASTSummarizer
from interpreter import CODESAGE, Interpreter
from resolver import Resolver
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

# ------------------------ Line-numbered Text Widget ------------------------
class LineNumberedText(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master)
        self.text = tk.Text(self, **kwargs, wrap="none")
        self.scroll = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.scroll.set)

        self.linenumbers = tk.Text(self, width=4, padx=4, takefocus=0, border=0,
                                   background="lightgray", state="disabled", wrap="none")
        self.linenumbers.pack(side="left", fill="y")
        self.scroll.pack(side="right", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<KeyRelease>", self.update_linenumbers)
        self.text.bind("<MouseWheel>", self.sync_scroll)
        self.text.bind("<Button-1>", self.sync_scroll)
        self.update_linenumbers()

    def update_linenumbers(self, event=None):
        self.linenumbers.config(state="normal")
        self.linenumbers.delete("1.0", "end")
        lines = self.text.get("1.0", "end-1c").split("\n")
        numbers = "\n".join(str(i+1) for i in range(len(lines)))
        self.linenumbers.insert("1.0", numbers)
        self.linenumbers.config(state="disabled")

    def sync_scroll(self, event=None):
        self.linenumbers.yview_moveto(self.text.yview()[0])

    def get(self):
        return self.text.get("1.0", "end")

# ------------------------ Interpreter with GUI Error Handling ------------------------
def run_interpreter(code):
    """Capture all errors and output for GUI"""
    CODESAGE.had_error = False
    CODESAGE.had_runtime_error = False

    stdout_buffer = StringIO()
    stderr_buffer = StringIO()

    try:
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            # Scanner
            try:
                scanner = Scanner(code)
                tokens = scanner.scan_tokens()
            except Exception as e:
                return f"[Scanner Error] {e}"
            if CODESAGE.had_error:
                return "[Scanner Error] Invalid token(s)."

            # Parser
            try:
                parser = Parser(tokens)
                statements = parser.parse()
            except Exception as e:
                return f"[Parser Error] {e}"
            if CODESAGE.had_error:
                return "[Parser Error] Invalid syntax."

            statements = [stmt for stmt in statements if stmt is not None]

            # Resolver
            interpreter = Interpreter()
            interpreter.output = []
            CODESAGE.interpreter = interpreter
            try:
                resolver = Resolver(interpreter)
                resolver.resolve(statements)
            except Exception as e:
                return f"[Resolver Error] {e}"
            if CODESAGE.had_error:
                return "[Resolver Error] Variable resolution failed."

            # Interpret
            try:
                CODESAGE.interpret(statements)
            except Exception as e:
                return f"[Runtime Error] {e}"

    except Exception as e:
        return f"[Unknown Error] {e}"

    # Combine outputs
    gui_output = interpreter.output if hasattr(interpreter, "output") else []

    std_out = stdout_buffer.getvalue().strip()
    if std_out:
        gui_output.insert(0, std_out)

    std_err = stderr_buffer.getvalue().strip()
    if std_err:
        gui_output.append(f"[Error] {std_err}")

    return "\n".join(gui_output) if gui_output else "Execution complete"

# ------------------------ AST Summary ------------------------
def summarize_ast(code):
    try:
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        statements = parser.parse()
        summarizer = ASTSummarizer()
        for stmt in statements:
            if stmt:
                stmt.accept(summarizer)
        return "\n".join(summarizer.summary_lines)
    except Exception as e:
        return f"[Summary Error] {e}"

# ------------------------ AST Tree with Color ------------------------
def pretty_ast_gui(statements, indent=""):
    lines = []
    for i, stmt in enumerate(statements):
        branch = "└── " if i == len(statements)-1 else "├── "
        node_name = stmt.__class__.__name__
        # Color assignment
        if "Literal" in node_name:
            color = "green"
        elif "Binary" in node_name:
            color = "blue"
        elif "Variable" in node_name:
            color = "orange"
        elif "Print" in node_name:
            color = "purple"
        else:
            color = "black"
        lines.append((f"{indent}{branch}{node_name}", color))

        # Recurse if stmt has children
        if hasattr(stmt, "children") and stmt.children:
            extension = "    " if i == len(statements)-1 else "│   "
            lines.extend(pretty_ast_gui(stmt.children, indent + extension))
    return lines

def build_ast_lines(node, prefix="", is_last=True):
    """
    Recursive function to generate AST lines with proper branches.
    Returns a list of (line_text, color_tag)
    """
    lines = []

    # Branch prefix
    branch = "└── " if is_last else "├── "
    node_name = node.__class__.__name__

    # Assign color based on node type
    if "Literal" in node_name:
        color = "green"
    elif "Binary" in node_name:
        color = "blue"
    elif "Variable" in node_name:
        color = "orange"
    elif "Print" in node_name:
        color = "purple"
    else:
        color = "black"

    # Add current node
    lines.append((prefix + branch + node_name, color))

    # Determine children
    children = []
    if hasattr(node, "children") and node.children:
        children = node.children
    elif hasattr(node, "left") or hasattr(node, "right"):  # BinaryExpr
        children = []
        if hasattr(node, "left") and node.left:
            children.append(node.left)
        if hasattr(node, "right") and node.right:
            children.append(node.right)
    elif hasattr(node, "expression") and node.expression:
        children = [node.expression]

    # Update prefix for child nodes
    child_prefix = prefix + ("    " if is_last else "│   ")

    for i, child in enumerate(children):
        lines.extend(build_ast_lines(child, child_prefix, i == len(children) - 1))

    return lines


def show_ast_colored():
    code = code_input.get()
    ast_box.config(state="normal")
    ast_box.delete("1.0", tk.END)
    try:
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        statements = parser.parse()
        if not statements:
            ast_box.insert(tk.END, "No AST generated.", "red")
            ast_box.config(state="disabled")
            return

        for stmt in statements:
            lines = build_ast_lines(stmt)
            for line_text, color in lines:
                ast_box.insert(tk.END, line_text + "\n", color)

        # Configure colors
        ast_box.tag_config("green", foreground="green")
        ast_box.tag_config("blue", foreground="blue")
        ast_box.tag_config("orange", foreground="orange")
        ast_box.tag_config("purple", foreground="purple")
        ast_box.tag_config("black", foreground="black")

    except Exception as e:
        ast_box.insert(tk.END, f"[AST Error] {e}", "red")
    ast_box.config(state="disabled")


# ------------------------ GUI Setup ------------------------
root = tk.Tk()
root.title("CodeSage ")
root.geometry("900x900")
mono_font = font.Font(family="Courier New", size=10)

tk.Label(root, text="Enter code:").pack(anchor="w", padx=5)
code_input = LineNumberedText(root, height=15, width=100, font=mono_font)
code_input.pack(fill="both", expand=True, padx=5, pady=2)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

def run_code():
    output = run_interpreter(code_input.get())
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)

    # Split output line by line
    for line in output.split("\n"):
        # Highlight errors in red
        if line.startswith("[Runtime Error]") or line.startswith("[Parser Error]") \
           or line.startswith("[Resolver Error]") or line.startswith("[Scanner Error]") \
           or line.startswith("[Unknown Error]") or line.startswith("[Error]"):
            output_box.insert(tk.END, line + "\n", "error")
        else:
            output_box.insert(tk.END, line + "\n", "normal")

    # Configure tags
    output_box.tag_config("error", foreground="red")
    output_box.tag_config("normal", foreground="black")

    output_box.config(state="disabled")
    

def summarize_code():
    summary = summarize_ast(code_input.get())
    summary_box.config(state="normal")
    summary_box.delete("1.0", tk.END)
    summary_box.insert(tk.END, summary)
    summary_box.config(state="disabled")

tk.Button(button_frame, text="Run Code", command=run_code).pack(side="left", padx=5)
tk.Button(button_frame, text="Summarize AST", command=summarize_code).pack(side="left", padx=5)
tk.Button(button_frame, text="Show AST", command=show_ast_colored).pack(side="left", padx=5)

# Outputs
tk.Label(root, text="Interpreter Output:").pack(anchor="w", padx=5)
output_box = scrolledtext.ScrolledText(root, height=6, font=mono_font, state="disabled")
output_box.pack(fill="both", expand=True, padx=5, pady=2)

tk.Label(root, text="AST Summary:").pack(anchor="w", padx=5)
summary_box = scrolledtext.ScrolledText(root, height=6, font=mono_font, state="disabled")
summary_box.pack(fill="both", expand=True, padx=5, pady=2)

tk.Label(root, text="AST Tree:").pack(anchor="w", padx=5)
ast_box = scrolledtext.ScrolledText(root, height=15, font=mono_font, state="disabled")
ast_box.pack(fill="both", expand=True, padx=5, pady=2)

root.mainloop()
