from search import Searching
import openai
from prompts import system_prompt

class ChatBot:
    def __init__(self,api_key, api_type, api_version, api_base,model,embed_model):
        """
        Initialize the ChatBot class by setting up OpenAI API credentials and chat history.
        """
        self.api_key = api_key
        self.api_type = api_type
        self.api_base = api_base
        self.api_version = api_version
        openai.api_key = api_key
        openai.api_type = api_type
        openai.api_base = api_base
        openai.api_version = api_version
        self.model=model
        self.embed_model=embed_model
        self.chat_history = []  # Initialize an empty list to store chat history

    def chat(self, user_input, docs):
        """
        Generate a response from the chatbot based on user input and document context.

        - **user_input**: The input text from the user.
        - **docs**: Contextual documents related to the user query.

        Returns a dictionary containing the chatbot's response message.
        """
        try:
            delimiter = "####"  # Delimiter used to separate sections in the context

            # Create the initial messages for the chat history
            messages = [{"role": "system", "content": system_prompt}]
            context = f'''Query:
    {delimiter} {user_input} {delimiter}

    context:
    {delimiter} {docs} {delimiter}
    '''
            
            # Maintain a rolling history of the last 5 messages
            if len(self.chat_history) > 5:
                self.chat_history = self.chat_history[-4:]
            messages += self.chat_history
            # Add the user query to the messages
            messages.append({'role': 'user', 'content': context})
            print(messages)
            # Generate a response using OpenAI's ChatCompletion API
            response = openai.ChatCompletion.create(
                engine=self.model,
                messages=messages,
                temperature=0.1
            )
            
            # Update chat history with the user input and the assistant's response
            self.chat_history.append({"role": "user", "content": user_input})
            self.chat_history.append({"role": "assistant", "content": response.choices[0]['message']['content']})

            # Return the chatbot's response
            return {"message": response.choices[0]['message']['content']}
        except Exception as e:
            # Print any error that occurs and return it in the response
            print(f"Error: {e}")
            return {"message": str(e)}

    def get_bot_response(self, user_input):
        """
        Retrieve a response from the chatbot based on user input.

        - **user_input**: The input text from the user.

        Returns the chatbot's response by performing a search and generating a response.
        """
        # Initialize the Searching class
        search = Searching(self.api_key, self.api_type, self.api_version, self.api_base,self.embed_model)
        # Perform a search to get relevant documents
        docs = search.searching(user_input)
        
        # Get the chatbot's response based on the search results and user input
        response = self.chat(user_input, docs)
        
        return response
