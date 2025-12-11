
from googlesearch import search

try:
    print("Testing search...")
    results = search("test", num_results=5)
    count = 0
    for url in results:
        print(f"Found: {url}")
        count += 1
    print(f"Total found: {count}")
except Exception as e:
    print(f"Error: {e}")
