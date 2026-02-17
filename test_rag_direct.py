import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

print("Testing rag_chain.answer_question directly...\n")

from app import rag_chain

question = "c'est quoi le commerce électronique en tunisie ?"
print(f"Question: {question}")
print(f"Requesting top_k=5 contexts\n")

answer, contexts = rag_chain.answer_question(question, top_k=5)

print("=" * 80)
print(f"Answer returned: {len(answer)} chars")
print(f"Contexts returned: {len(contexts)} items")
print("=" * 80)
print()

if contexts:
    print("Contexts retrieved successfully!")
    for i, ctx in enumerate(contexts, 1):
        print(f"\nContext {i}:")
        print(f"  Source: {ctx['metadata'].get('source', 'unknown')}")
        print(f"  Distance: {ctx['distance']:.4f}")
        print(f"  Text: {ctx['text'][:100]}...")
else:
    print("❌ NO CONTEXTS RETURNED!")
    print("\nThis means the problem is in the RAG chain, not the API")

print()
print(f"Answer preview:")
print(answer[:300])
