# decoder.py
import torch
import torch.nn as nn
import torch.nn.functional as F

class SummaryVocab:
    """Simple vocabulary class for target summaries."""
    def __init__(self):
        self.word2idx = {"<PAD>":0, "<SOS>":1, "<EOS>":2, "<UNK>":3}
        self.idx2word = {0:"<PAD>", 1:"<SOS>", 2:"<EOS>", 3:"<UNK>"}
        self.count = 4

    def add_word(self, word):
        if word not in self.word2idx:
            self.word2idx[word] = self.count
            self.idx2word[self.count] = word
            self.count += 1

    def encode(self, word):
        return self.word2idx.get(word, self.word2idx["<UNK>"])

    def decode(self, idx):
        return self.idx2word.get(idx, "<UNK>")

    def __len__(self):
        return len(self.word2idx)


class Decoder(nn.Module):
    """
    Simple LSTM decoder with program vector as initial hidden state.
    """
    def __init__(self, embedding_dim, hidden_dim, vocab_size):
        super(Decoder, self).__init__()
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.vocab_size = vocab_size

        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.fc_out = nn.Linear(hidden_dim, vocab_size)

    def forward(self, input_seq, hidden, cell):
        """
        input_seq: [batch_size] current token ids
        hidden, cell: [1, batch_size, hidden_dim] initial states
        """
        input_seq = input_seq.unsqueeze(1)  # [batch, 1]
        embedded = self.embedding(input_seq)  # [batch, 1, embed_dim]
        output, (hidden, cell) = self.lstm(embedded, (hidden, cell))
        logits = self.fc_out(output.squeeze(1))  # [batch, vocab_size]
        return logits, hidden, cell


def train_decoder(decoder, encoder_vectors, summaries, vocab, epochs=10, lr=0.001):
    """
    encoder_vectors: list of program vectors (torch tensors) [hidden_dim]
    summaries: list of target summaries (list of strings)
    """
    optimizer = torch.optim.Adam(decoder.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        total_loss = 0
        for program_vec, summary in zip(encoder_vectors, summaries):
            decoder.zero_grad()
            
            # Initialize hidden and cell with program vector
            hidden = program_vec.detach().unsqueeze(0).unsqueeze(0)  # [1,1,hidden_dim]
            cell = torch.zeros_like(hidden)

            # Prepare input/output sequences
            tokens = ["<SOS>"] + summary.split() + ["<EOS>"]
            input_ids = [vocab.encode(tok) for tok in tokens[:-1]]
            target_ids = [vocab.encode(tok) for tok in tokens[1:]]
            
            # --- START OF CORRECTION ---
            
            # Instead of loss = 0, create a list to hold losses
            losses = []
            for inp, tgt in zip(input_ids, target_ids):
                inp_tensor = torch.tensor([inp])
                tgt_tensor = torch.tensor([tgt])
                logits, hidden, cell = decoder(inp_tensor, hidden, cell)
                
                # Append the loss for the current token to the list
                losses.append(criterion(logits, tgt_tensor))

            # Sum all the losses at the end to create the final loss tensor
            loss = torch.stack(losses).sum()

            # --- END OF CORRECTION ---

            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch {epoch+1}/{epochs} | Loss: {total_loss/len(summaries):.4f}")


def generate_summary(decoder, program_vec, vocab, max_len=15):
    """
    Generate a summary from a program vector using greedy decoding.
    """
    hidden = program_vec.unsqueeze(0).unsqueeze(0)
    cell = torch.zeros_like(hidden)
    input_id = torch.tensor([vocab.encode("<SOS>")])

    summary_tokens = []

    for _ in range(max_len):
        logits, hidden, cell = decoder(input_id, hidden, cell)
        next_id = torch.argmax(logits, dim=-1).item()
        if next_id == vocab.encode("<EOS>"):
            break
        summary_tokens.append(vocab.decode(next_id))
        input_id = torch.tensor([next_id])

    return " ".join(summary_tokens)
