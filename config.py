import urllib
import pyodbc
import os
from urllib.parse import quote_plus
from urllib import parse
from dotenv import load_dotenv
from os import path
from sqlalchemy import create_engine

load_dotenv()

import urllib
params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=Guilherme;DATABASE=Ecommerce;UID=sa;PWD=123")
SQLALCHEMY_DATABASE_URI = ("mssql+pyodbc:///?odbc_connect=%s" % params)