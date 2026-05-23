import sys
import pickle
import torch
from codesage.scanner import Scanner
from codesage.parser import Parser, ASTTreePrinter, ASTPathExtractor, ASTSummarizer
from nlp.prepare_embeddings import run_embedding_pipeline
from nlp.decoder import Decoder, SummaryVocab
from codesage.interpreter import CODESAGE, Interpreter
from codesage.resolver import Resolver
from openai import OpenAI
# import os
from dotenv import load_dotenv

load_dotenv()

# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# def gpt_line_by_line_summary(code: str) -> str:
#     messages = [
#         {"role": "system", "content": "You are CodeSage, a helpful assistant that explains Python code line by line.But make sure it is short"},
#         {"role": "user", "content": f"Explain this Python code line by line, including the type of statement:\n\n{code}"}
#     ]
    
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=messages,
#         temperature=0.2
#     )
    
#     return response.choices[0].message.content.strip()

# -----------------------------
# 1. Load trained decoder and vocabulary
# -----------------------------
# with open("summary_vocab.pkl", "rb") as f:
#     vocab = pickle.load(f)

# hidden_dim = 256  # Must match training
# embedding_dim = 64

# decoder = Decoder(embedding_dim=embedding_dim, hidden_dim=hidden_dim, vocab_size=len(vocab))
# decoder.load_state_dict(torch.load("decoder.pth"))
# decoder.eval()  # Set model to evaluation mode

# -----------------------------
# 2. Main function
# -----------------------------
def main():
    print("Enter Python code below. Press Enter twice to finish:")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    source_code = "\n".join(lines)

    # -----------------------------
    # 2a. Scan tokens
    # -----------------------------
    scanner = Scanner(source_code)
    try:
        tokens = scanner.scan_tokens()
    except Exception as e:
        print(f"[Scanner Error] {e}", file=sys.stderr)
        sys.exit(65)

    print("\n[Scanner Output]:")
    for token in tokens:
        print(token)

    # -----------------------------
    # 2b. Parse tokens to AST
    # -----------------------------
    parser = Parser(tokens)
    try:
        statements = parser.parse()
    except Exception as e:
        print(f"[Parser Error] {e}", file=sys.stderr)
        sys.exit(65)

    print("\n[Parser Output]:")
    printer = ASTTreePrinter()
    for stmt in statements:
        if stmt:
            print(printer.print(stmt))

    # -----------------------------
    # 2c. Extract AST paths
    # -----------------------------
    # extractor = ASTPathExtractor()
    # all_paths = []
    # for stmt in statements:
    #     if stmt:
    #         all_paths.extend(extractor.extract_paths(stmt))

    # if not all_paths:
    #     print("Warning: No AST paths extracted. Cannot generate summary.")
    #     program_vector = torch.zeros(hidden_dim)  # fallback
    # else:
    #     program_vector = run_embedding_pipeline(all_paths).squeeze()  # Ensure 1D

    # -----------------------------
    # 3. Generate summary
    # -----------------------------
    # hidden = program_vector.unsqueeze(0).unsqueeze(0)  # [1,1,hidden_dim]
    # cell = torch.zeros_like(hidden)
    # tokens_out = ["<SOS>"]

    # for _ in range(20):  # Max length
    #     last_token_id = vocab.encode(tokens_out[-1])
    #     inp_id = torch.tensor([last_token_id])

    #     with torch.no_grad():
    #         logits, hidden, cell = decoder(inp_id, hidden, cell)

    #     # Sampling with temperature to avoid repeating same token
    #     temperature = 1.0
    #     probs = torch.softmax(logits / temperature, dim=-1)
    #     next_id = torch.multinomial(probs, 1).item()
    #     next_token = vocab.decode(next_id)

    #     if next_token == "<EOS>":
    #         break

    #     tokens_out.append(next_token)

    # summary = " ".join(tokens_out[1:])  # Exclude <SOS>
    # print("\nGenerated Summary:", summary)

    # summary = gpt_line_by_line_summary(source_code)
    # print("\nGenerated Summary:\n")
    # print(summary)
    summarizer = ASTSummarizer()
    printer_output = [summarizer.print(stmt) for stmt in statements]
    for line in summarizer.summary_lines:
        print(line)


    # -----------------------------
    # 4. Interpret AST
    # -----------------------------
    interpreter = Interpreter()
    CODESAGE.interpreter = interpreter
    try:
        statements = [stmt for stmt in statements if stmt is not None]
        resolver = Resolver(CODESAGE.interpreter)
        resolver.resolve(statements)
        CODESAGE.interpret(statements)
    except Exception as e:
        print(f"[Runtime Error] {e}", file=sys.stderr)
        sys.exit(70)


if __name__ == "__main__":
    main()
