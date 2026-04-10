import os
import sys
import time
import threading
import webbrowser

# Fix missing stdout/stderr when running as --noconsole exe
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')

# Add the backend folder to the path so 'app' module is found
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, base_dir)

import uvicorn
from app.main import app


def open_browser():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:8000/app")


def main():
    env_path = os.path.join(base_dir, ".env")
    if os.path.exists(env_path):
        from dotenv import load_dotenv
        load_dotenv(env_path)

    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config=None)


if __name__ == "__main__":
    main()
