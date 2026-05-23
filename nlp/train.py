# train.py
import torch
import pickle
from scanner import Scanner
from parser import Parser, ASTPathExtractor
from prepare_embeddings import run_embedding_pipeline
from decoder import Decoder, SummaryVocab, train_decoder
import json

# -----------------------------
# Global: Load trained decoder & vocab
# -----------------------------
try:
    with open("summary_vocab.pkl", "rb") as f:
        vocab = pickle.load(f)

    hidden_dim = 256
    embedding_dim = 64
    decoder = Decoder(embedding_dim=embedding_dim, hidden_dim=hidden_dim, vocab_size=len(vocab))
    decoder.load_state_dict(torch.load("decoder.pth"))
    decoder.eval()
except FileNotFoundError:
    decoder = None
    vocab = None

# -----------------------------
# Function: Generate NLP summary from code
# -----------------------------
def generate_summary_from_code(code: str) -> str:
    """Return NLP summary of a Python code snippet using the trained decoder."""
    if decoder is None or vocab is None:
        return "[NLP Error] Decoder or vocab not loaded."

    try:
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        statements = parser.parse()
        statements = [stmt for stmt in statements if stmt]

        extractor = ASTPathExtractor()
        all_paths = []
        for stmt in statements:
            all_paths.extend(extractor.extract_paths(stmt))
        if not all_paths:
            return "[NLP Error] No AST paths extracted."

        program_vec = run_embedding_pipeline(all_paths).squeeze()
        if len(program_vec.shape) == 1:
            hidden = program_vec.unsqueeze(0).unsqueeze(0)
        else:
            hidden = program_vec.unsqueeze(0)
        cell = torch.zeros_like(hidden)

        tokens_out = ["<SOS>"]
        for _ in range(20):
            last_token_id = vocab.encode(tokens_out[-1])
            inp_id = torch.tensor([last_token_id])
            with torch.no_grad():
                logits, hidden, cell = decoder(inp_id, hidden, cell)
            next_id = logits.argmax(dim=-1).item()
            next_token = vocab.decode(next_id)
            if next_token == "<EOS>":
                break
            tokens_out.append(next_token)

        summary = " ".join(tokens_out[1:])
        return summary if summary else "[NLP Error] Decoder returned empty output."

    except Exception as e:
        return f"[NLP Error] {e}"

# -----------------------------
# Original training code
# -----------------------------
if __name__ == "__main__":
    # Load dataset
    with open("codesage_dataset.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)

    code_snippets = [item["code"] for item in dataset]
    summaries = [item["summary"] for item in dataset]

    program_vectors = []
    valid_summaries = []

    print("Generating program vectors...")
    for i, snippet in enumerate(code_snippets):
        try:
            scanner = Scanner(snippet)
            tokens = scanner.scan_tokens()
            parser = Parser(tokens)
            statements = parser.parse()

            extractor = ASTPathExtractor()
            all_paths = []
            for stmt in statements:
                if stmt:
                    all_paths.extend(extractor.extract_paths(stmt))

            if not all_paths:
                continue

            vec = run_embedding_pipeline(all_paths).squeeze() if len(run_embedding_pipeline(all_paths).shape) > 1 else run_embedding_pipeline(all_paths)
            program_vectors.append(vec)
            valid_summaries.append(summaries[i])
        except Exception as e:
            continue

    summaries = valid_summaries

    # Prepare vocab
    vocab = SummaryVocab()
    vocab.add_word("<SOS>")
    vocab.add_word("<EOS>")
    for summary in summaries:
        for token in summary.split():
            vocab.add_word(token)

    # Initialize decoder
    embedding_dim = 64
    hidden_dim = program_vectors[0].shape[0]
    decoder = Decoder(embedding_dim=embedding_dim, hidden_dim=hidden_dim, vocab_size=len(vocab))

    # Train decoder
    print("Starting decoder training...")
    train_decoder(decoder, program_vectors, summaries, vocab, epochs=30, lr=0.001)

    # Save trained model
    torch.save(decoder.state_dict(), "decoder.pth")
    with open("summary_vocab.pkl", "wb") as f:
        pickle.dump(vocab, f)

    print("Training finished and models saved!")
