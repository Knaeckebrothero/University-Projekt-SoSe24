"""
This script is used to import LinkedIn data from the MongoDB database into the DWH.
"""
import os
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
import pandas as pd
from sqlalchemy import create_engine  # Requires pymysql
from datetime import datetime
# Import conversion functions
from convert import profile as pf


# Load environment variables
load_dotenv(find_dotenv())

# !!!UNENCRYPTED CONNECTION ONLY USE ON LAN!!!
dwh_connection_url = os.getenv("DATABASE_DWH")
dwh = create_engine(dwh_connection_url)
mongodb = MongoClient(os.getenv("MongoClientURI"))["dwh_sources"]
collection = mongodb["KGL_LIN_PRF"]

# Load the collection
documents = collection.find({'public_identifier': 'tatiana-kapkan'})  # collection.find()

# Main loop
for doc in documents:
    # Prepare location data
    location_df = pf.location(doc)

    # Check if a matching record exists in DIM_Languages table
    query = """
        SELECT id
        FROM DIM_LIN_Location
        WHERE countryLetters = %(countryLetters)s 
        AND countryName = %(countryName)s
        AND city = %(city)s
        AND state = %(state)s
    """
    result = pd.read_sql_query(query, dwh, params=location_df.iloc[0].to_dict())

    if not result.empty:
        # If matching record found, use existing id
        location_id = result.iloc[0]['id']
    else:
        # If no matching record found, insert a new record and use its id
        location_df.to_sql('DIM_LIN_Location', dwh, if_exists='append', index=False)
        location_id = pd.read_sql_query("SELECT LAST_INSERT_ID()", dwh).iloc[0, 0]

    # Prepare person data
    person_df = pf.person(doc, location_id, 10)

    # Insert person data
    person_df.to_sql('FACT_PRF_Person', dwh, if_exists='append', index=False)
