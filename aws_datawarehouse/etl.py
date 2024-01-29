import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

def load_staging_tables(cur, conn):
    '''Function to copy data from S3 and load into staging tables inside my DWH'''
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()

def insert_tables(cur, conn):
    '''Function to load data from staging tables to my star schema'''
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()

def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("dbname={} user={} password={} host={} port={}".format(
        config['DWH']['DWH_DB'],
        config['DWH']['DWH_DB_USER'],
        config['DWH']['DWH_DB_PASSWORD'],
        config['DWH']['DWH_ENDPOINT'],
        config['DWH']['DWH_PORT']
    ))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()

if __name__ == "__main__":
    main()
