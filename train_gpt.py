# train_gpt.py
import json
from openai import OpenAI

# -----------------------------
# 1. Initialize OpenAI client
# -----------------------------
client = OpenAI(api_key="APIKEY")  # put your key here or load from env

def summarize_code(code_snippet: str) -> str:
    """Send code snippet to GPT and return summary."""
    prompt = f"Summarize the following Python code in one sentence:\n\n{code_snippet}\n\nSummary:"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or gpt-4o for higher quality
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,  # low randomness for consistent summaries
    )
    return response.choices[0].message.content.strip()

# -----------------------------
# 2. Load dataset (code only)
# -----------------------------
code_snippets = []
with open("codesage_dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)
    code_snippets = [item["code"] for item in dataset]

print(f"Loaded {len(code_snippets)} snippets.")

# -----------------------------
# 3. Generate summaries with GPT
# -----------------------------
new_dataset = []
for i, code in enumerate(code_snippets):
    try:
        summary = summarize_code(code)
        new_dataset.append({"code": code, "summary": summary})
        print(f"[{i+1}] ✅ {summary}")
    except Exception as e:
        print(f"[{i+1}] ⚠️ Error summarizing: {e}")

# -----------------------------
# 4. Save new dataset
# -----------------------------
with open("codesage_dataset_gpt.json", "w", encoding="utf-8") as f:
    json.dump(new_dataset, f, indent=2)

print(f"Finished! Saved {len(new_dataset)} examples to codesage_dataset_gpt.json")
