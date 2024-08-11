import openai
import numpy as np
import faiss
import json

class Searching:
    def __init__(self,api_key, api_type, api_version, api_base,embed_model):
        """
        Initialize the Searching class by setting up OpenAI API credentials.
        """
        openai.api_key = api_key
        openai.api_type = api_type
        openai.api_base = api_base
        openai.api_version = api_version
        self.embed_model=embed_model

    def load_data(self):
        """
        Load data from a JSON file.

        Returns:
        - A list of documents loaded from 'sample_data.json'.
        """
        with open('sample_data.json', 'r') as file:
            data = json.load(file)  # Load data from the JSON file
        return data
   
    def question_embedding(self, question):
        """
        Create an embedding vector for the given question using OpenAI's API.

        - **question**: The input text to be converted into an embedding.

        Returns:
        - A vector representation of the question.
        """
        query_vector = openai.Embedding.create(
            input=question,
            engine=self.embed_model
        )["data"][0]["embedding"]  # Extract the embedding vector from the response
        return query_vector
    
    def question_answering_model(self, query_vector):
        """
        Use FAISS to find the most relevant documents based on the query vector.

        - **query_vector**: The embedding vector of the question.

        Returns:
        - A string containing relevant documents based on the search results.
        """
        try:
            embedd = np.array(query_vector)  # Convert the query vector to a NumPy array
            embed_reshaped = embedd.reshape(1, 1536)  # Reshape the vector to match FAISS index input
            indexer = faiss.read_index("sample_index.index")  # Load the FAISS index
            distances, indices = indexer.search(embed_reshaped, k=2)  # Perform the search
            relevant_documents = ''
            print("Distances Between Context Vectors and Query Vectors:",distances[0],"Indexes:", indices[0])  # Print distances and indices for debugging
            paragraph = self.load_data()  # Load documents from the JSON file
            for i, index in enumerate(indices[0]):
                # Append documents to the result if their distance is below the threshold
                if (distances[0][i]) < 0.4999:
                    document = paragraph[index]
                    relevant_documents += (document + " ")
            return relevant_documents
        except Exception as e:
            # Print any errors encountered during the process
            print(f"Error: {e}")
            return ""
    
    def searching(self, text):
        """
        Perform the search process for the given text.

        - **text**: The input text to be embedded and searched.

        Returns:
        - A string with relevant documents or "fail" if an error occurs.
        """
        try:
            query_vector = self.question_embedding(text)  # Get the embedding vector for the text
            data = self.question_answering_model(query_vector)  # Find relevant documents
            return data
        except Exception as e:
            # Print any errors encountered and return "fail"
            print(f"Error: {e}")
            return "fail"
