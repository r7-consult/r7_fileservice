import uvicorn
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from main import app

if __name__ == '__main__':
    print("copyright : Free for non commercial use https://r7-consult.ru/", flush=True)
    print("Starting R7 File Service on http://127.0.0.1:58081", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=58081, log_level="trace")
