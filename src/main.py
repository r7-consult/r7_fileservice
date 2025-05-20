from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from svc_xls_files import (
    get_file_list,
    get_file_available,
    get_file_meta,
    register_file_sql,
    execute_sql_on_file,
)

import logging
 
logger = logging.getLogger(__name__)
app = FastAPI()
origins = ["*", "http://localhost", "http://127.0.0.1:58081", "http://localhost:58081", ]
app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"], )

http_server_default_response = 'Ok.'

@app.get("/ping/")
async def ping():
    return http_server_default_response

@app.get("/file/list")
def get_file_list_endpoint(path: str):
    """
    Get the list of files in the specified path.
    """
    get_all_request_params = locals()
    logger.info(get_all_request_params)    
    try:
        return {"files": get_file_list(path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/file/available")
def get_file_available_endpoint(path: str, file_name: str):
    """
    Check if a file is available in the specified path.
    """
    get_all_request_params = locals()
    logger.info(get_all_request_params)    
    try:
        return {"status": "OK" if get_file_available(path, file_name) else "Error"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/file/meta")
def get_file_meta_endpoint(path: str, file_name: str):
    """
    Get metadata of a file in the specified path.
    """
    get_all_request_params = locals()
    logger.info(get_all_request_params)    
    try:
        return get_file_meta(path, file_name) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/file/register")
def register_file_sql_endpoint(path: str = '', file_name: str = '', sheet_name: str= '',usecols: str= '',skiprows:int = 0,nrows:int= 10000000):
    """
    Register a file as a pandas DataFrame source.
    """
    get_all_request_params = locals()
    logger.info(get_all_request_params)
    try:
        df = register_file_sql(path_loc = path, file_name_loc = file_name, sheet_name_loc= sheet_name, usecols_loc=usecols, skiprows_loc=skiprows, nrows_loc=nrows)
        return { "columns": df.columns.tolist()
                , "rows": len(df)
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/file/sql")
def execute_sql_on_file_endpoint(query: str = '', path: str = '', file_name: str = '', sheet_name: str= '',usecols: str= '',skiprows:int = 0,nrows:int= 10000000)  :
    """
    Execute an SQL query on the registered file (pandas DataFrame).
    """
    get_all_request_params = locals()
    logger.info(get_all_request_params)
    try:
        result = execute_sql_on_file(query, path, file_name, sheet_name= sheet_name, usecols=usecols, skiprows=skiprows, nrows=nrows)
        return result.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))