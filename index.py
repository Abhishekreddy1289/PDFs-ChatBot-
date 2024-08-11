import openai
import numpy as np
import faiss
import json
import time
import os

class TextIndexing:
    def __init__(self, api_key, api_type, api_version, api_base, embed_model):
        """
        Initialize the TextIndexing class by setting up OpenAI API credentials.
        """
        openai.api_key = api_key
        openai.api_type = api_type
        openai.api_base = api_base
        openai.api_version = api_version
        self.embed_model = embed_model
        self.index_path = "sample_index.index"
        self.json_path = "sample_data.json"

    def preprocess_embeddings(self, embeddings):
        """
        Preprocess the embeddings to ensure they are in a consistent format.
        """
        flat_embeddings = []

        for emb in embeddings:
            if isinstance(emb[0], list):
                flat_emb = [item for sublist in emb for item in sublist]
            else:
                flat_emb = emb

            flat_embeddings.append(flat_emb)

        embeddings_array = np.array(flat_embeddings, dtype=np.float32)

        if len(set(len(e) for e in flat_embeddings)) != 1:
            raise ValueError("All embeddings must have the same length.")

        return embeddings_array

    def embeddings_creation(self, chunks):
        """
        Create embeddings for the given text chunks using OpenAI's API.
        """
        paragraph = []
        embeddings = []

        for chunk in chunks:
            paragraph.append(chunk)
            if len(chunks) > 20:
                time.sleep(1)
            response = openai.Embedding.create(input=[chunk], engine=self.embed_model)
            embeddings.append(response['data'][0]['embedding'])

        return embeddings, paragraph

    def load_or_create_indexer(self, embedding_dim):
        """
        Load an existing FAISS index or create a new one if it doesn't exist.
        """
        if os.path.exists(self.index_path):
            print("Loading existing index...")
            indexer = faiss.read_index(self.index_path)
        else:
            print("Creating new index...")
            quantiser = faiss.IndexFlatL2(embedding_dim)
            indexer = faiss.IndexIVFFlat(quantiser, embedding_dim, 1, faiss.METRIC_L2)
            indexer.train(np.zeros((1, embedding_dim), dtype=np.float32))  # Dummy training
        return indexer

    def embeddings_to_indexer(self, embeddings):
        """
        Add embeddings to the FAISS indexer.
        """
        try:
            embeddings = self.preprocess_embeddings(embeddings)
        except ValueError as e:
            print(f"Error during preprocessing: {e}")
            return None

        embedding_dim = embeddings.shape[1]
        indexer = self.load_or_create_indexer(embedding_dim)

        if isinstance(indexer, faiss.IndexIVFFlat):
            if not indexer.is_trained:
                indexer.train(embeddings)
        indexer.add(embeddings)

        faiss.write_index(indexer, self.index_path)

        return indexer

    def load_existing_json(self):
        """
        Load existing data from the JSON file.
        """
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r') as file:
                return json.load(file)
        return []

    def update_json(self, new_data):
        """
        Update the JSON file with new data.
        """
        existing_data = self.load_existing_json()
        existing_data.extend(new_data)
        with open(self.json_path, 'w') as file:
            json.dump(existing_data, file)

    def indexing(self, text):
        """
        Perform the full indexing process for the provided text.
        """
        try:
            embeddings, paragraphs = self.embeddings_creation(text)
            self.embeddings_to_indexer(embeddings)
            self.update_json(paragraphs)
            return "done"
        except Exception as e:
            print(f"Error: {e}")
            return "fail"
