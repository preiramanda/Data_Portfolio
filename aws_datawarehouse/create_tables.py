import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries

def drop_tables(cur, conn):
    '''Function to drop all tables'''
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

def create_tables(cur, conn):
    '''Function to create all tables'''
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

def main():
    '''Configurations to connect to Redshift'''
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

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()

if __name__ == "__main__":
    main()
