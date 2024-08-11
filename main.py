import streamlit as st
from read_pdf import PDFReader
from index import TextIndexing
from qna import ChatBot
from config import api_version, api_type
import os
import json

st.sidebar.title("💬 Chatbot")

# Azure OpenAI key
with st.sidebar.form(key='api_key_form'):
    api_key = st.text_input("Azure OpenAI Key:", type="password", key="api_key")
    api_base = st.text_input("Azure OpenAI Base:", type="default", key="api_base")
    model = st.text_input("RAG Model Name", type="default", key="rag_model")
    embed_model = st.text_input("Embedding Model Name", type="default", key="embed_model")
    submit_button = st.form_submit_button("Submit")

if submit_button:
    if not api_key:
        st.sidebar.error("Azure OpenAI Key Missing")
    elif not api_base:
        st.sidebar.error("Azure OpenAI Base Missing")
    elif not model:
        st.sidebar.error("RAG Model Name Missing")
    elif not embed_model:
        st.sidebar.error("Embedding Model Name Missing")
    else: 
        st.sidebar.success("Submitted successfully!")

# Initialize the indexing and chatbot
index = TextIndexing(api_key, api_type, api_version, api_base, embed_model)  # This handles the indexing of text data
qna = ChatBot(api_key, api_type, api_version, api_base, model,embed_model)  # This manages interactions with the chatbot


# File uploader widget for PDF files
uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    if not api_key:
        st.sidebar.error("Azure OpenAI Key Missing")
    elif not api_base:
        st.sidebar.error("Azure OpenAI Base Missing")
    elif not model:
        st.sidebar.error("RAG Model Name Missing")
    elif not embed_model:
        st.sidebar.error("Embedding Model Name Missing")
    else:
        pdf_reader = PDFReader()
        # Extract and display text from the PDF file
        pdf_text, message = pdf_reader.extract_text_from_pdf(uploaded_file)
        
        if message == "done":
            index_message = index.indexing(pdf_text)
            if index_message == "done":
                add_message=pdf_reader.pdf_add(uploaded_file.name)
                if add_message == "done":
                    st.sidebar.success("File uploaded successfully 👍")
                else:
                    st.sidebar.error("Filed store PDF Name 😒")
            else:
                st.sidebar.error("File indexing failed 😒")
            
            # Button to show the text
            if st.button('Show PDF Text'):
                pdf_text1 = "\n".join(pdf_text)
                # Create a container for text with custom styling
                with st.container():
                    st.markdown(
                        """
                        <style>
                        .pdf-text-container {
                            height: 200px;  /* Adjust height according to needs */
                            overflow-y: scroll;
                            margin-top: 0.1cm;  /* 10 cm margin from the top */
                        }
                        </style>
                        <div class="pdf-text-container">
                            """ + pdf_text1.replace("\n", "<br>") + """
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.sidebar.error("File Read failed 😒")



# Define the file paths to be deleted
INDEX_FILE_PATH = "sample_index.index"
JSON_FILE_PATH = "sample_data.json"
PDF_NAMES="pdf_names.json"

# Initialize session state for the list visibility in the sidebar
if 'show_list' not in st.session_state:
    st.session_state.show_list = False

# Function to toggle the list visibility
def toggle_list():
    st.session_state.show_list = not st.session_state.show_list

# Sidebar button to toggle the list visibility
with st.sidebar:
    st.button("View PDFs List", on_click=toggle_list)

    # Conditionally display the list based on session state
    if st.session_state.show_list:
        try:
            with open('pdf_names.json', 'r') as f:
                data = json.load(f)
            list_markdown = "\n".join(f"- {item}" for item in data)
            st.markdown(list_markdown)
        except:
            st.markdown("No PDFs Available")

def delete_file(file_path: str):
    """Delete a file and return the status."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"status": "success", "file": file_path}
        else:
            return {"status": "error", "file": file_path, "message": "File does not exist"}
    except Exception as e:
        return {"status": "error", "file": file_path, "message": str(e)}

if st.sidebar.button("Delete all PDFs"):
    index_result = delete_file(INDEX_FILE_PATH)
    json_result = delete_file(JSON_FILE_PATH)
    pdf_name_result=delete_file(PDF_NAMES)
    if index_result["status"] == "success" and json_result["status"] == "success" and pdf_name_result["status"] == "success":
        st.sidebar.success("Deleted all PDFs")
    else:
        st.sidebar.error("PDFs is unavailable")
st.caption("🚀 A Streamlit PDF Chatbot powered by OpenAI")

st.caption("🤔 Have a question? I'm here to help! 🤖")

# Streamlit UI
def main():
    # Create a container to hold chat history
    chat_container = st.container()

    # Initialize session state for storing chat history and user input
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    # Function to handle sending a message
    def handle_send(user_input):
        if user_input:
            # Add user input to chat history
            st.session_state.chat_history.append(
                f"""
                <div style='text-align: right; margin-bottom: 10px;'>
                    <div style='display: inline-block; max-width: 80%; padding: 10px; border-radius: 20px; background-color: #F0F0F0; color: black;'>
                        {user_input}
                    </div>
                </div>
                """
            )

            # Generate bot response
            bot_response = qna.get_bot_response(user_input)
            
            # Add bot response to chat history
            st.session_state.chat_history.append(
                f"""
                <div style='margin-bottom: 10px;'>
                    <div style='display: inline-block; max-width: 80%; padding: 10px; border-radius: 20px; background-color: #F0F0F0; color: black;'>
                        {bot_response['message']}
                    </div>
                </div>
                """
            )


    # Form for chat input
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input(label="Query:", placeholder="Ask your query here", key='user_input')
        submit_button = st.form_submit_button("Send")

        if submit_button:
            handle_send(user_input)

    # Display chat history
    with chat_container:
        for message in st.session_state.chat_history:
            st.markdown(message, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
