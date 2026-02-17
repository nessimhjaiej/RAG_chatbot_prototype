import requests
import json

# Test the backend API
url = "http://localhost:8000/api/query"
question = "c'est quoi le commerce électronique en tunisie ?"

payload = {
    "question": question,
    "top_k": 5
}

print(f"Testing question: {question}")
print(f"Requesting {payload['top_k']} chunks...\n")

try:
    response = requests.post(url, json=payload, timeout=60)
    print(f"Response status code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    response.raise_for_status()
    
    data = response.json()
    print(f"Response data keys: {data.keys()}")
    print()
    
    print("=" * 80)
    print("ANSWER:")
    print("=" * 80)
    print(data.get('answer', 'No answer'))
    print()
    
    contexts = data.get('contexts', [])
    print("=" * 80)
    print(f"SOURCES: {len(contexts)} chunks retrieved")
    print("=" * 80)
    
    for i, ctx in enumerate(contexts, 1):
        print(f"\nChunk {i}:")
        print(f"  Source: {ctx['metadata'].get('source', 'unknown')}")
        print(f"  Distance: {ctx['distance']:.4f}")
        print(f"  Text preview: {ctx['text'][:150]}...")
        print()
    
    if len(contexts) == 0:
        print("\n⚠️  WARNING: No sources retrieved!")
    else:
        print(f"\n✅ SUCCESS: Retrieved {len(contexts)} source chunks")
        
except requests.exceptions.ConnectionError:
    print("❌ ERROR: Cannot connect to backend. Is it running on http://localhost:8000?")
except requests.exceptions.Timeout:
    print("❌ ERROR: Request timeout")
except Exception as e:
    print(f"❌ ERROR: {e}")
