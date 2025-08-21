# kb_loader.py - chunk local txt files and create embeddings with sentence-transformers + Chroma
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
import os

MODEL_NAME = "all-MiniLM-L6-v2"

def load_texts_from_folder(folder="data/docs"):
    texts = []
    if not os.path.exists(folder):
        print(f"Folder {folder} does not exist. Create data/docs and add .txt files to index.")
        return texts
    for fname in os.listdir(folder):
        if fname.lower().endswith(".txt"):
            with open(os.path.join(folder, fname), "r", encoding="utf-8") as f:
                texts.append(f.read())
    return texts

if __name__ == '__main__':
    client = chromadb.Client()
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)
    try:
        collection = client.create_collection(name="neurospark_kb", embedding_function=ef)
    except Exception as e:
        collection = client.get_collection("neurospark_kb")
    docs = load_texts_from_folder()
    for i, d in enumerate(docs):
        collection.add(documents=[d], metadatas=[{"source": f"doc_{i}.txt"}], ids=[str(i)])
    print("KB loaded to Chroma: docs=", len(docs))
