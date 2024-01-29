 
# This project aims to create a Data Warehouse on AWS.
### There's 2 ways to follow the project: 
#### 1. There's a juyter notebook (.ipynb) and in the same directory, a config document.Add your credentials to the config and you can use the jupyter notebook directly or
#### 2. You can follow by the scripts mentioned on the template.

# Project context:

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights into what songs their users are listening to.

You'll be working with 3 datasets that reside in S3. Here are the S3 links for each:

Song data: s3://udacity-dend/song_data
Log data: s3://udacity-dend/log_data
This third file s3://udacity-dend/log_json_path.jsoncontains the meta information that is required by AWS to correctly load s3://udacity-dend/log_data


### Project Template

- sql_queries.py is where you'll define you SQL statements, which will be imported
- create_table.py is where you'll create your fact and dimension tables for the star schema in Redshift.
- etl.py is where you'll load data from S3 into staging tables on Redshift and then process that data into your analytics tables on Redshift.


*Below, there's the documentation of each step I did in this project.*


#### A -   I've created a star schema diagram via https://dbdiagram.io/. It is available inside the folder named **Starschema.png**

#### B - There's a notebook named **Data warehouse in AWS- Steps followed.ipynb** where you can find step by step the execution of:

1 - Configuring credentials to AWS;
2 - Creating boto clients to interact with AWS; 
3 - Checking the bucket to confirm that the S3 data is available;
4 - Connecting to Redshift (assuming I already have a cluster created);
5 - Drop possibly existing tables and create all tables needed in the project;
6 - Make a copy from the s3 bucket to staging tables;
7 - Loading the starschema tables from staging tables;
8 - Simple analytics;
9 - Disconnection.

#### C - I've altered the scripts sql_queries.py , create_table.py and etl.py, so they can make sense to the project goal.



