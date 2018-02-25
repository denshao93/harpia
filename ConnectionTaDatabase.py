import psycopg2

# conn = None


def open_connect():
    """ Connect to the PostgreSQL database server """

    # conn = None

    try:
        # read connection parameters
        params = "host=localhost dbname=ta7 user=postgres password=postgres"

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')

        conn = psycopg2.connect(params)

        conn.autocommit = True

        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def close_connect(conn):
    """ Close connect to the PostgreSQL database server """
    try:
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':

    open_connect()
