# pg2NoSql
A simple psycopg2 based wrapper for nosql like database interaction with python.

### Background
The wrapper was developed to work with JSON postgre storage like a real NoSQL DB (e.g. MongoDB) . After a long research with Google There Was No library found Which helps to work with JSON and PostgreSQL.

### Example
This example shows the funcionality of the wrapper. It simply stores events into an event table and then reads all the events which are of type **XRA**
```python
# connect db
db_client.connect(database=DATABASE, host=SERVER)
events_table = db_client.get_table(EVENTS_TABLE_NAME)

# create table if it not exists
if events_table is None:
    events_table = db_client.create_table(EVENTS_TABLE_NAME)

# store event documents into the db
for e in flat_events:
    events_table.put(e)

# read all documents of type 'XRA'
all_xra = events_table.query(query="data->>'type' = 'XRA'")

# commit all changes and close db connection
events_table.commit()
db_client.close()
```

### Details
The wrapper contains only two classes called **PostgresNoSQLClient** and **PostgresNoSQLTable**:

##### PostgresNoSQLClient
Method | Description
------ | -----------
constructor | creates a new client
connect | connects to a postgre database
close | closes the connection to the database
create_table | creates a new table and returns a **PostgresNoSQLTable**
drop_table | drops a table form the database
get_table | returns an existing table or None
commit | commit transactions
table_exists | check if a table already exists on the database

##### PostgresNoSQLTable
Method | Description
------ | -----------
commit | commit transactions
put | inserts document into the table
get | returns document by id
query | returns a list of documents by a given query
drop | not implemented yet!

### About
The wrapper has been written for a science project in is an early alpha version!