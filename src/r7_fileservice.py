import uvicorn
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
 
 

if __name__ == '__main__':
    print ("copyright : Free for non commercial use https://r7-consult.ru/")
    uvicorn.run("main:app", host="127.0.0.1", port=58081, log_level="trace" )
