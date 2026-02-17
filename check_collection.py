import chromadb
from pathlib import Path

# Open client without specifying embedding function
client = chromadb.PersistentClient(path=str(Path('chromadb')))

# Get collection without embedding function to see what's there
try:
    collection = client.get_collection(name='icc-policies')
    count = collection.count()
    print(f"Collection 'icc-policies' exists with {count} documents")
    
    # Get metadata about the collection
    print(f"Collection metadata: {collection.metadata}")
    
    # Get a sample document (without querying, which would need embeddings)
    if count > 0:
        data = collection.get(limit=2, include=['documents', 'metadatas'])
        print(f"\nSample document IDs: {data['ids']}")
        print(f"Sample metadata: {data['metadatas'][0] if data['metadatas'] else 'None'}")
        print(f"Sample doc preview: {data['documents'][0][:200] if data['documents'] else 'None'}")
except Exception as e:
    print(f"Error: {e}")
