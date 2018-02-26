import psycopg2

# conn = None


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

    def get_scene_path_row_geom(self, path_row):
        """
        :param path_row: Path and row must be writed as: path/row (ex. 215/068)
        :return: Fields from table lc_ba (landsat Bahia): id, path/row, ogr_geom
        """
        cursor = self.conn.cursor()
        sql = "SELECT fid, path_row, ST_AsText(ogr_geometry) FROM lc_ba WHERE path_row = '{path_row}';"\
            .format(path_row=path_row)
        cursor.execute(sql)
        qtd = cursor.fetchall()
        cursor.close()
        return qtd


if __name__ == '__main__':

    conn = Connection("host=localhost dbname=ta7 user=postgres password=postgres")
    print(conn.get_scene_path_row_geom('215/068'))

