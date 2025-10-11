import sys
from scanner import Scanner
from parser import Parser, ASTPathExtractor

def is_valid_ast(statements):
    """
    Returns True if AST extraction yields non-empty, 
    complete paths (no 'UnknownStmt' or 'UnknownExpr').
    """
    extractor = ASTPathExtractor()
    all_paths = []

    for stmt in statements:
        if stmt:
            paths = extractor.extract_paths(stmt)
            all_paths.extend(paths)

    if not all_paths:
        return False

    # Reject if incomplete / unknown
    for p in all_paths:
        if "UnknownStmt" in p or "UnknownExpr" in p:
            return False

    return True


def filter_dataset(input_file, output_file):
    valid_snippets = []
    total, kept = 0, 0

    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        code_snippets = f.read().split("\n\n")  # snippets separated by blank lines

    for snippet in code_snippets:
        total += 1
        source_code = snippet.strip()
        if not source_code:
            continue

        # Scan + Parse
        try:
            scanner = Scanner(source_code)
            tokens = scanner.scan_tokens()

            parser = Parser(tokens)
            statements = parser.parse()
        except Exception:
            continue  # skip if scanner/parser fails

        # Validate AST completeness
        if is_valid_ast(statements):
            valid_snippets.append(source_code)
            kept += 1

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(valid_snippets))

    print(f"[Filter Finished] Total: {total}, Kept: {kept}, Rejected: {total - kept}")


if __name__ == "__main__":
    input_file = "Python_code_data.txt"
    output_file = "filtered.txt"
    filter_dataset(input_file, output_file)