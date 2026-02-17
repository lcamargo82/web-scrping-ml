
try:
    from google import genai
    print("SUCCESS: google.genai imported successfully")
except ImportError as e:
    print(f"FAILURE: {e}")
except Exception as e:
    print(f"FAILURE: {e}")
