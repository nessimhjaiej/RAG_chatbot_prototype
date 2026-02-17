import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from app.vectorstore import get_client, get_collection, query_collection

client = get_client(persist_dir='chromadb')
collection = get_collection(client, name='icc-policies')

question = "c'est quoi le commerce électronique en tunisie ?"
print(f"Question: {question}\n")

# Query the collection
result = query_collection(collection, question, n_results=5)

print("Raw result keys:", result.keys())
print()

docs = result.get('documents', [[]])
print(f"Documents structure: {type(docs)}, length: {len(docs)}")
if docs:
    print(f"First level: {type(docs[0])}, length: {len(docs[0])}")
    print(f"Documents retrieved: {len(docs[0])}")
print()

metadatas = result.get('metadatas', [[]])
print(f"Metadatas structure: {type(metadatas)}, length: {len(metadatas)}")
if metadatas:
    print(f"First level: {type(metadatas[0])}, length: {len(metadatas[0])}")
print()

distances = result.get('distances', [[]])
print(f"Distances structure: {type(distances)}, length: {len(distances)}")
if distances:
    print(f"First level: {type(distances[0])}, length: {len(distances[0])}")
print()

# Show first result if any
if docs and docs[0]:
    print("=" * 80)
    print("FIRST RESULT:")
    print("=" * 80)
    print(f"Text: {docs[0][0][:200]}...")
    print(f"Metadata: {metadatas[0][0] if metadatas and metadatas[0] else 'None'}")
    print(f"Distance: {distances[0][0] if distances and distances[0] else 'None'}")
else:
    print("⚠️  NO RESULTS RETURNED!")
