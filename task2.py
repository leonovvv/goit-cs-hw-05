import requests
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

# Function to download text from a URL
def fetch_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return ""

# MapReduce: Mapper function
def mapper(chunk):
    words = re.findall(r"\b\w+\b", chunk.lower())
    return Counter(words)

# MapReduce: Reducer function
def reducer(counter1, counter2):
    return counter1 + counter2

# Split text into chunks for multithreading
def split_text(text, num_chunks):
    length = len(text)
    chunk_size = length // num_chunks
    chunks = [text[i:i + chunk_size] for i in range(0, length, chunk_size)]
    return chunks

# Visualize top words
def visualize_top_words(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)

    plt.barh(words, counts, color='skyblue')
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title("Top 10 Most Frequent Words")
    plt.gca().invert_yaxis()
    plt.show()

if __name__ == "__main__":
    # URL of the text to process
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"  # Example: Pride and Prejudice by Jane Austen

    print("Downloading text...")
    text = fetch_text(url)

    if text:
        print("Splitting text into chunks...")
        num_threads = 8
        chunks = split_text(text, num_threads)

        print("Processing chunks with MapReduce...")
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            mapped_results = list(executor.map(mapper, chunks))

        final_counts = Counter()
        for count in mapped_results:
            final_counts = reducer(final_counts, count)

        print("Visualizing results...")
        visualize_top_words(final_counts, top_n=10)
    else:
        print("Failed to download text. Please check the URL.")