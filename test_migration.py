
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API Key not found.")
    exit(1)

client = genai.Client(api_key=api_key)

import glob

# Find image dynamically
files = glob.glob("input/*.png")
if not files:
    print("No image found in input/")
    exit(1)
img_path = files[0]
print(f"Using image: {img_path}")

with open("test_run.log", "w", encoding="utf-8") as f:
    f.write("Start Test\n")
    try:
        f.write("Listing models...\n")
        # List models to find correct name
        # Note: client.models.list might return iterator
        for model in client.models.list():
            f.write(f"Model: {model.name}\n")

        f.write("Uploading file to Gemini...\n")
        # Using 'file' argument based on previous partial success
        file_ref = client.files.upload(file=img_path)
        f.write(f"File uploaded: {file_ref.name}\n")
        
        f.write("Generating content...\n")
        # Try appending 'models/' prefix just in case as well
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=[file_ref, "Describe this image in 5 words."]
        )
        f.write("Response:\n")
        f.write(f"{response.text}\n")
    
    except Exception as e:
        f.write(f"Error: {e}\n")
        import traceback
        f.write(traceback.format_exc())

print("Test finished. Check test_run.log")
