# Technical Challenge: Financial Time Series Analysis and Database Management
Develop a robust data pipeline and analytics system using PostgreSQL with TimescaleDB extension to handle and analyze financial time series data

# Requirements

- Install Docker, if you don't already have it. For packages and instructions, see the Docker [installation](https://docs.docker.com/get-docker/) documentation.
- Download [Kaggle Stock Market Dataset](https://www.kaggle.com/datasets/jacksoncrow/stock-market-dataset/) (inside ./data folder)

# How to run

#### Pull docker image
```shell
docker pull timescale/timescaledb-ha:pg14-latest
```
#### Set password for postgres
```shell
export ENV_POSTGRES_PASSWORD=changeme
```
#### Setup postgres
```shell
docker run -d --name timescaledb -p 127.0.0.1:5432:5432 -v timescaledb-data:/var/lib/postgresql/data -e POSTGRES_DB=stocks -e POSTGRES_PASSWORD=$ENV_POSTGRES_PASSWORD timescale/timescaledb-ha:pg14-latest
```
#### Install python lib
```shell
pip install -r requirements
```
#### Set env
```shell
export PYTHONPATH=./
```
#### Run code
```shell
python src/main.py
```
_____

## Part 1: Database Setup and Data Ingestion
1) Install and configure PostgreSQL and TimescaleDB on a server: 
   - [x] __./Dockerfile__
2) Design a database schema suitable for storing financial time series data. This should
include tables for storing stock prices, trading volumes, and other relevant financial
indicators:
    - [x] __./src/models/stocks__
3) Write a script to ingest mock financial time series data into the database. This data can
be generated or sourced from a public financial dataset
    - [x] __./src/pipelines/command.py__

## Part 2: Querying and Data Manipulation

1) Demonstrate your ability to write complex SQL queries by retrieving specific data points,
like finding the average trading volume of a particular stock in the last quarter.
    - [x] __./src/pipelines/command.py:L25__

2) Use TimescaleDB’s time-series functions to perform time-based aggregations and
window functions.
    - [x] __./src/pipelines/command.py:L25__

## Part 3: Data Analysis and Reporting

1) Develop a Python script using psycopg2 or a similar library to connect to the database
and perform data analysis tasks.
    - [x] __./src/database/postgres.py__

## Part 4: Optimization and Scaling

1) Optimize the database for faster query performance, considering indexes and
TimescaleDB-specific optimizations.

   - __I would basically enable ```add_compression_policy``` for old data__
   - __Run ```VACUUM``` command periodically__
   - __Use ``pg_stat_user_indexes`` to identify unused indexes (if they exist)__

   - Ref: https://www.timescale.com/blog/how-to-reduce-your-postgresql-database-size/

2) Write a brief strategy on how the system could be scaled to handle real-time financial
data feeds.
   
I would:

   - __Create a Python producer to read messages/events from a given feed and populate it in a Kafka Topic__
   - __Once the data is populated in Kafka, the message would be retained for 7 days (For backup safety)__
   - __Since that data needs to be available as soon as possible, create a Apache Spark Streaming pipeline to consume events from Kafka__
   - __Dump the information in a storage like (s3, blob storage, cloud storage)__
   - __Refresh the table with the new information (Important: Some databases has the ability to sync new data once you point the table to a storage path)__