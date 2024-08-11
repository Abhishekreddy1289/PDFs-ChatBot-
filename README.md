# PDF Chatbot

## Overview

This project features a simple chatbot that allows users to upload a PDF file and ask questions about its content. It utilizes FastAPI for the backend API and Streamlit for the frontend interface.

## Components

1. **FastAPI**: Manages file uploads, text extraction, indexing, and chatbot interactions.
2. **Streamlit**: Provides a user-friendly interface for uploading PDFs, displaying text, and interacting with the chatbot.

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Clone the Repository

```bash
git clone https://www.github.com/Abhishekreddy1289/pdf-chatbot.git
cd pdf-chatbot
```

### Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### Running the FastAPI Backend

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

The backend API will be accessible at `http://localhost:8000`.

### Running the Streamlit Frontend

Start the Streamlit application:

```bash
streamlit run main.py
```

The Streamlit app will be accessible at `http://localhost:8501`.

## File Descriptions

### `app.py` (Streamlit)

- **Function**: Provides the frontend interface for users to upload PDFs, view extracted text, and interact with the chatbot.
- **Key Components**:
  - File uploader for PDF files
  - Display area for extracted PDF text
  - Chat interface for interacting with the chatbot

### `main.py` (FastAPI)

- **Function**: Handles backend API requests for uploading PDFs and processing chat messages.
- **Endpoints**:
  - `/upload`: Receives PDF files, extracts and indexes text.
  - `/chat`: Processes user input and returns chatbot responses.

### `read_pdf.py`

- **Function**: Contains the `PDFReader` class responsible for extracting text from PDF files.

### `index.py`

- **Function**: Contains the `TextIndexing` class responsible for indexing extracted text to facilitate quick querying.

### `qna.py`

- **Function**: Contains the `ChatBot` class responsible for interacting with the chatbot, processing user queries, and generating responses.

## Usage

1. **Upload a PDF**:
   - Open the Streamlit application.
   - Use the file uploader widget to upload a PDF file.
   - Click "Show PDF Text" to view the content of the PDF.

2. **Interact with the Chatbot**:
   - Enter your OpenAI API key in the provided form.
   - Type your queries in the chat input box and click "Send" to receive responses from the chatbot.

## Troubleshooting

- **Error: "Upload failed"**:
  - Ensure the PDF file is not corrupted and is in the correct format.
  
- **Error: "Indexing failed"**:
  - Verify that the PDF text extraction is functioning properly. Check logs for detailed error messages.

## Contribution

Feel free to fork the repository and submit pull requests with improvements or bug fixes.

## Contact

For any questions or support, please open an issue in the GitHub repository or contact abhishekreddy38751@gmail.com.