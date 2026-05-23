import torch
import torch.nn as nn

# Step 1: Build Vocabulary
def build_vocab(paths):
    vocab = {}
    indexed_paths = []
    for path in paths:
        indexed_path = []
        for token in path:
            if token not in vocab:
                vocab[token] = len(vocab)
            indexed_path.append(vocab[token])
        indexed_paths.append(indexed_path)
    return vocab, indexed_paths

# Step 2: Convert to Embeddings
def paths_to_embeddings(indexed_paths, embedding_dim=64):
    vocab_size = max(max(p) for p in indexed_paths) + 1
    embedding_layer = nn.Embedding(vocab_size, embedding_dim)

    tensor_paths = [torch.tensor(p, dtype=torch.long) for p in indexed_paths]
    embedded_paths = [embedding_layer(t) for t in tensor_paths]
    padded_paths = nn.utils.rnn.pad_sequence(embedded_paths, batch_first=True)

    return padded_paths, embedding_layer

# Step 3: BiLSTM
def run_bilstm(padded_paths, embedding_dim=64, hidden_size=128):
    bilstm = nn.LSTM(
        input_size=embedding_dim,
        hidden_size=hidden_size,
        batch_first=True,
        bidirectional=True
    )
    output, (hn, cn) = bilstm(padded_paths)
    return output

# Step 4: Pooling (Mean over sequence length)
def pool_paths(bilstm_output):
    # bilstm_output: [num_paths, max_len, hidden_dim*2]
    pooled = bilstm_output.mean(dim=1)  # average across tokens
    return pooled  # shape: [num_paths, hidden_dim*2]

# Step 5: Aggregate all path vectors into one program embedding
def aggregate_program(pooled_paths):
    # pooled_paths: [num_paths, hidden_dim*2]
    program_vector = pooled_paths.mean(dim=0)  # average over all paths
    return program_vector  # shape: [hidden_dim*2]

# Main pipeline entry
def run_embedding_pipeline(ast_paths):
    print("\n[Embedding Pipeline Started]")

    # 1. Build vocab
    vocab, indexed_paths = build_vocab(ast_paths)
    print("[Vocabulary Size]:", len(vocab))

    # 2. Embeddings
    padded_paths, _ = paths_to_embeddings(indexed_paths)
    print("[Embeddings Shape]:", padded_paths.shape)

    # 3. BiLSTM
    bilstm_output = run_bilstm(padded_paths)
    print("[BiLSTM Output Shape]:", bilstm_output.shape)

     # 4. Pooling (per-path)
    pooled_paths = pool_paths(bilstm_output)
    print("[Pooled Path Vectors Shape]:", pooled_paths.shape)

    # 5. Aggregate into program vector
    program_vector = aggregate_program(pooled_paths)
    print("[Program Vector Shape]:", program_vector.shape)

    print("[Embedding Pipeline Finished]")
    return program_vector
