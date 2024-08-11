from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
api_type = os.getenv("API_TYPE")
api_base = os.getenv("API_BASE")
api_version = os.getenv("API_VERSION")
model = os.getenv("MODEL")
embed_model= os.getenv('EMBED_MODEL')