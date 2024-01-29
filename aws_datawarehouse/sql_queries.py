import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE STAGING TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (artist text distkey, 
                                           auth text, 
                                           first_name text, 
                                           gender text, 
                                           item_in_session text,
                                           last_name text,
                                           leng float, 
                                           level text, 
                                           location text, 
                                           method text, 
                                           page text,
                                           registration float, 
                                           session_id int, 
                                           song text, 
                                           status int, 
                                           ts timestamp,
                                           user_agent text, 
                                           user_id int)
""")



staging_songs_table_create = (""" 
CREATE TABLE IF NOT exists staging_songs (artist_name text distkey,
                                          artist_id text,
                                          artist_latitude float,
                                          artist_longitude float,
                                          artist_location text,
                                          song_id text,
                                          title text,
                                          duration float,
                                          year int,
                                          num_songs int)
""")

# CREATE STARSCHEMA TABLES
#fact table
songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (songplay_id int identity(0,1) primary key,
                                     start_time timestamp NOT NULL,
                                     user_id text NOT NULL,
                                     level text NOT NULL,
                                     song_id text NOT NULL,
                                     artist_id text NOT NULL distkey,
                                     session_id int NOT NULL,
                                     location text,
                                     user_agent text NOT NULL)
""")
#dim tables

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (user_id int primary key,
                                  first_name text NOT NULL,
                                  last_name text NOT NULL,
                                  gender text NOT NULL,
                                  level text sortkey NOT NULL)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (song_id text primary key,
                                  title text NOT NULL,
                                  artist_id text sortkey NOT NULL,
                                  year int NOT NULL,
                                  duration float NOT NULL)
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists(artist_id text PRIMARY KEY sortkey,
                                   artist_name text NOT NULL,
                                   location text,
                                   latitude float,
                                   longitude float)
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time(start_time timestamp PRIMARY KEY sortkey,
                                hour int NOT NULL,
                                day int NOT NULL,
                                week int NOT NULL,
                                month int NOT NULL,
                                year int NOT NULL,
                                weekday int NOT NULL)
""")

# LOADING STAGING TABLES

staging_events_copy = ("""copy staging_events from {} 
                        credentials 'aws_iam_role={}'
                        compupdate off region 'us-west-2' 
                        FORMAT AS JSON {}
                        TIMEFORMAT as 'epochmillisecs'""").format(config['S3']['LOG_DATA'],
                                                                  config['DWH']['DWH_IAM_ROLE'],
                                                                  config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""copy staging_songs from {}
                      credentials 'aws_iam_role={}'
                      compupdate off region 'us-west-2' 
                      FORMAT AS JSON 'auto'""").format(config['S3'].get('SONG_DATA'),
                                                config['DWH'].get('DWH_IAM_ROLE').strip("'"))


# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
                            SELECT 
                            (events.ts)              AS start_time, 
                            events.user_id           AS user_id, 
                            events.level             AS level,
                            songs.song_id            AS song_id, 
                            songs.artist_id          AS artist_id, 
                            events.session_id        AS session_id, 
                            events.location          AS location, 
                            events.user_agent        AS user_agent
                            FROM staging_events events 
                            JOIN staging_songs songs ON 
                            events.artist = songs.artist_name AND events.song = songs.title
                            WHERE events.page = 'NextSong' """)

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level)
                        SELECT DISTINCT
                        user_id,
                        first_name,
                        last_name,
                        gender,
                        level
                        FROM staging_events events
                        WHERE user_id is NOT NULL""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration)
                     SELECT DISTINCT 
                     song_id, 
                     title, 
                     artist_id, 
                     year, 
                     duration
                     FROM staging_songs
                     WHERE song_id IS NOT NULL""")

artist_table_insert = ("""INSERT INTO artists (artist_id, artist_name, location, latitude, longitude)
                       SELECT DISTINCT 
                       artist_id, 
                       artist_name, 
                       artist_location,
                       artist_latitude, 
                       artist_longitude
                       FROM staging_songs
                       WHERE artist_id IS NOT NULL""")

time_table_insert = ("""INSERT INTO time (start_time, hour, day,week, month, year, weekday)
                     SELECT DISTINCT 
                     ts                        AS start_time, 
                     extract(hour from ts)     AS hour, 
                     extract(day from ts)      AS day,
                     extract(week from ts)     AS week,
                     extract(month from ts)    AS month,
                     extract(year from ts)     AS year, 
                     extract(weekday from ts)  AS weekday
                     FROM staging_events WHERE ts IS NOT NULL""")

# QUERY LISTS
create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
