import os
import pandas as pd
import pandasql as ps
from datetime import datetime
from typing import List

def get_file_list(path: str) -> List[str]:
    """
    Return the list of files in the specified directory.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path '{path}' does not exist.")
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def get_file_available(path: str, file_name: str) -> bool:
    """
    Check if the specified file exists.
    """
    return os.path.isfile(os.path.join(path, file_name))

 
def get_file_meta(path: str, file_name: str) -> dict:
    """
    Get metadata of the specified file.
    """
    file_path = os.path.join(path, file_name)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File '{file_name}' does not exist at path '{path}'.")

    excel_reader = pd.ExcelFile(file_path)
    stats = os.stat(file_path)
    return {
        "file_name": file_name,
        "file_path": file_path,
        "size_bytes": stats.st_size,
        "created_at": datetime.fromtimestamp(stats.st_ctime).isoformat(),
        "modified_at": datetime.fromtimestamp(stats.st_mtime).isoformat(),
        "accessed_at": datetime.fromtimestamp(stats.st_atime).isoformat(),
        "mode": oct(stats.st_mode),
        "sheets": excel_reader.sheet_names,
        "copyright": "Free for non commercial use https://r7-consult.ru/ ",
    }

def register_file_sql(path_loc: str = '', file_name_loc: str = '', sheet_name_loc: str= '',usecols_loc: str= '',skiprows_loc:int = 0,nrows_loc:int= 10000000) -> pd.DataFrame:
    """
    Load the specified Excel file into a pandas DataFrame.
    """
    file_path = os.path.join(path_loc, file_name_loc) 
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File '{file_name_loc}' does not exist at path '{path_loc}' .")      
    if sheet_name_loc == '':
        if usecols_loc == '':
            df = pd.read_excel(file_path, engine='openpyxl', skiprows=skiprows_loc, nrows=nrows_loc)
        else:
            df = pd.read_excel(file_path, engine='openpyxl', usecols=usecols_loc, skiprows=skiprows_loc, nrows=nrows_loc)
    else :
        if usecols_loc == '':
            df = pd.read_excel(file_path, engine='openpyxl',sheet_name= sheet_name_loc, skiprows=skiprows_loc, nrows=nrows_loc)
        else:
            df = pd.read_excel(file_path,engine='openpyxl', sheet_name= sheet_name_loc, usecols=usecols_loc, skiprows=skiprows_loc, nrows=nrows_loc)       
    return df   
 


def execute_sql_on_file(query: str = '', path: str = '', file_name: str = '', sheet_name: str= '',usecols: str= '',skiprows:int = 0,nrows:int= 10000000)  -> pd.DataFrame:
    """
    Execute an SQL query on the pandas DataFrame from the Excel file.
    """
    df = register_file_sql(path_loc = path, file_name_loc = file_name, sheet_name_loc= sheet_name, usecols_loc=usecols, skiprows_loc=skiprows, nrows_loc=nrows)
    return ps.sqldf(query, locals())