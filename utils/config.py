import os

# --- API ---
API_BASE_URL = os.getenv("API_BASE_URL", "https://demoqa.com")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

# --- UI ---
BASE_URL = os.getenv("BASE_URL", "https://demoqa.com")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
TIMEOUT = int(os.getenv("TIMEOUT", "15"))
UPLOAD_FILE = os.path.abspath(os.path.join("resources", "upload.txt"))
