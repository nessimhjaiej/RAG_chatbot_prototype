import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from app.vectorstore import get_client, get_collection, query_collection

client = get_client(persist_dir='chromadb')
collection = get_collection(client, name='icc-policies')

# Test query
result = query_collection(collection, 'commerce électronique', n_results=5)

docs = result.get('documents', [[]])[0]
metadatas = result.get('metadatas', [[]])[0]
distances = result.get('distances', [[]])[0]

print(f"Query returned {len(docs)} documents")
print(f"Metadatas: {len(metadatas)} items")
print(f"Distances: {len(distances)} items")
print("\nFirst document preview:")
if docs:
    print(docs[0][:200])
    print(f"\nMetadata: {metadatas[0]}")
    print(f"Distance: {distances[0]}")
