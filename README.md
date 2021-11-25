# Simple API for Streamplate recruitment

## Local Deployment
Replace `os.environ['MONGO_CONNECTION']` in `app.py` and `insert_data.py` with a connection string for an empty MongoDB instance connection string.

Install requirements and insert data into database. By default the file `venues.csv` will be used unless otherwise specified.
``` 
pip install -r requirements.txt
python3 insert_data.py [ CSV_FILE ]
```

Start the API using:
``` 
python3 app.py
```

API will be available at the following url, where limit is optional:
```
http://127.0.0.1:<PORT>/?longitude=-97.0&latitude=49.0&limit=3
```