import psycopg2
import datetime
import yaml


class Connection:

    def __init__(self, str_connection):
        self.conn = None
        # read connection parameters
        self.str_connection = str_connection

        # open connection to database
        self.open_connect()

    def open_connect(self):
        """ Connect to the PostgreSQL database server """

        # conn = None

        try:
            # read connection parameters
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(self.str_connection)
            self.conn.autocommit = True

            return self.conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close_connect(self, conn):
        """ Close connect to the PostgreSQL database server """
        try:
            conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
            
    def save_db_composition_done(self, dict, scene_path):
        """."""
        cursor = self.conn.cursor()
        
        sqlQuery =  f"INSERT INTO public.harpia_img_processed ("\
                    f"save_composition, processing_date, "\
                    f"scene_file_name, satellite, sensor, satellite_index, "\
                    f"aquisition_date, scene_path)"\
                    f"VALUES ("\
                    f"1, {datetime.date.today},"\
                    f"{dict['scene_file_name']},{dict['initials_name']},"\
                    f"{dict['sensor']}, {dict['index']},"\
                    f"{dict['aquisition_date']}, {scene_path});"
        
        cursor.execute(sqlQuery)
        cursor.close()
        