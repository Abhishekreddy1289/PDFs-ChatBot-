from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from read_pdf import PDFReader
from index import TextIndexing
from qna import ChatBot
import os
from config import api_key, api_type, api_version, api_base,model,embed_model

app = FastAPI()

# Initialize the indexing and chatbot
index = TextIndexing(api_key, api_type, api_version, api_base,embed_model)  # This handles the indexing of text data
qna = ChatBot(api_key, api_type, api_version, api_base,model,embed_model)         # This manages interactions with the chatbot

# Define a model for the chat messages
class ChatMessage(BaseModel):
    user_input: str  # The user's input text for the chat

class UploadResponse(BaseModel):
    message: str

# Define the file paths to be deleted
INDEX_FILE_PATH = "sample_index.index"
JSON_FILE_PATH = "sample_data.json"

@app.post("/delete-files")
async def delete_files():
    def delete_file(file_path: str):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return {"status": "success", "file": file_path}
            else:
                return {"status": "error", "file": file_path, "message": "File does not exist"}
        except Exception as e:
            return {"status": "error", "file": file_path, "message": str(e)}

    # Delete the predefined files
    index_result = delete_file(INDEX_FILE_PATH)
    json_result = delete_file(JSON_FILE_PATH)
    
    return {
        "index_file": index_result,
        "json_file": json_result
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    API Endpoint to upload a PDF file and index its content.
    
    - **file**: The PDF file to be uploaded.
    
    This endpoint reads the PDF file, extracts the text, and performs indexing. 
    If indexing is successful, it returns a success message; otherwise, it raises an HTTP 500 error.
    """
    try:
        pdf_text, message = PDFReader().extract_text_from_pdf(file.file)  # Extract text from the PDF

        if message != "done":
            raise HTTPException(status_code=500, detail="PyPDF failed")
        # Index the extracted text
        index_message = index.indexing(pdf_text)
        if index_message != "done":
            raise HTTPException(status_code=500, detail="Indexing failed")
        
        return JSONResponse(content={"message": "File uploaded and indexed successfully!"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(message: ChatMessage):
    """
    API Endpoint for chatting with the chatbot.
    
    - **message**: Contains user input text.
    
    This endpoint takes user input, processes it through the chatbot, and returns the bot's response.
    If an error occurs during processing, it prints the error.
    """
    try:
        user_input = message.user_input  # Get user input from the request
        data = qna.get_bot_response(user_input)  # Get chatbot response based on user input
        return JSONResponse(content={"message": data})
    except Exception as e:
        print(e)  # Print any exception that occurs during chat processing

# Run the app using Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
