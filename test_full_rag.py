import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from app import rag_chain

# Test the full RAG chain
question = "Qu'est-ce que le commerce électronique en Tunisie?"
print(f"Question: {question}\n")

answer, contexts = rag_chain.answer_question(question, top_k=5)

print(f"Answer: {answer}\n")
print(f"Number of contexts retrieved: {len(contexts)}\n")

for i, ctx in enumerate(contexts, 1):
    print(f"Context {i}:")
    print(f"  Source: {ctx['metadata'].get('source', 'unknown')}")
    print(f"  Distance: {ctx['distance']:.4f}")
    print(f"  Text preview: {ctx['text'][:100]}...")
    print()
