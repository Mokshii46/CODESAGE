import torch
import pickle
from scanner import Scanner
from parser import Parser, ASTPathExtractor
from prepare_embeddings import run_embedding_pipeline
from decoder import Decoder, SummaryVocab

# -----------------------------
# 1. Load Trained Model and Vocabulary
# -----------------------------
print("Loading model and vocabulary...")
try:
    with open("summary_vocab.pkl", "rb") as f:
        vocab = pickle.load(f)

    vocab_size = len(vocab)
    hidden_dim = 256  # Must match the hidden_dim used during training
    embedding_dim = 64

    decoder = Decoder(embedding_dim=embedding_dim, hidden_dim=hidden_dim, vocab_size=vocab_size)
    decoder.load_state_dict(torch.load("decoder.pth"))
    decoder.eval()  # Set model to evaluation mode
    print("Model loaded successfully.")

except FileNotFoundError as e:
    print(f"Error: Could not find model or vocab file. Make sure 'decoder.pth' and 'summary_vocab.pkl' exist. {e}")
    exit()


# -----------------------------
# 2. Define and Process New Code Snippet
# -----------------------------
print("Enter your code. Type 'done' on a new line when you are finished.")

lines = []
while True:
    line = input()
    if line.lower() == 'done':
        break
    lines.append(line)


new_code = "\n".join(lines)
print(f"\nProcessing code:\n{new_code.strip()}")

try:
    scanner = Scanner(new_code)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    statements = parser.parse()

    extractor = ASTPathExtractor()
    all_paths = []
    for stmt in statements:
        if stmt:
            all_paths.extend(extractor.extract_paths(stmt))

    if not all_paths:
        raise ValueError("Could not extract any AST paths from the code snippet.")

    # Convert paths to the program vector
    program_vec = run_embedding_pipeline(all_paths)

except Exception as e:
    print(f"Error processing the code snippet: {e}")
    exit()


# -----------------------------
# 3. Generate Summary
# -----------------------------
hidden = program_vec.unsqueeze(0).unsqueeze(0)
cell = torch.zeros_like(hidden)

tokens = ["<SOS>"]
for _ in range(20):  # max 20 tokens
    # --- FIX 2: Correct the tensor shape ---
    last_token_id = vocab.encode(tokens[-1])
    inp_id = torch.tensor([last_token_id]) # Should be 1D: [1]

    # The decoder should not track gradients during inference
    with torch.no_grad():
        logits, hidden, cell = decoder(inp_id, hidden, cell)

    next_id = logits.argmax(dim=-1).item()
    next_token = vocab.decode(next_id)

    if next_token == "<EOS>":
        break
    
    # --- FIX 3: Correct the typo ---
    tokens.append(next_token)

summary = " ".join(tokens[1:]) # Exclude the <SOS> token from the final output
print("\nGenerated Summary:", summary)