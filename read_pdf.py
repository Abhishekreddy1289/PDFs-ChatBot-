import fitz  # PyMuPDF
import json

class PDFReader:
    def extract_text_from_pdf(self, uploaded_file):
        """
        Extracts text from a PDF file.

        - **uploaded_file**: A BytesIO object representing the PDF file to extract text from.

        Returns a tuple containing:
        - A list of strings, where each string is the text content of a page in the PDF.
        - A message indicating the success ("done") or failure ("fail") of the extraction process.
        """
        text = []  # Initialize a list to store text from each page
        message = "fail"  # Default message indicating failure

        try:
            # Open the PDF file from the uploaded BytesIO object
            pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")

            # Iterate through all the pages in the PDF document
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)  # Load the page
                text.append(page.get_text())  # Extract and store the text from the page

            # Close the PDF document
            pdf_document.close()

            # Update the message to indicate successful extraction if text was found
            if len(text) != 0:
                message = "done"

            return text, message  # Return the extracted text and status message

        except Exception as e:
            # Print any error that occurs during the extraction process
            print(f"An error occurred: {e}")
            return text, message  # Return the empty text list and failure message
        
    def pdf_add(self,name):
        try:
            try:
                # Read data from the JSON file
                with open('pdf_names.json', 'r') as f:
                    data = json.load(f)
                # Append a new item to the list
                data.append(name)
            except:
                print("This first PDF")
                data=[name]

            # Write the list to a JSON file
            with open('pdf_names.json', 'w') as f:
                json.dump(data,f)
            return "done"
        except Exception as e:
            print(f"Error: {e}")
            return "fail"

        
