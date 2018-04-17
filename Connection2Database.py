import psycopg2
import LandsatFileInfo as LCinfo


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
        sql = "SELECT fid, path_row, ST_GeomFromWKB(ogr_geometry) FROM lc_ba WHERE path_row = '{path_row}';"\
            .format(path_row=path_row)
        cursor.execute(sql)
        qtd = cursor.fetchall()
        cursor.close()
        return qtd
    
    def create_scene_path_row_schema(self, schema_name):
                
        cursor = self.conn.cursor()
        sql = "CREATE SCHEMA IF NOT EXISTS lc8_{path_row};".format(schema_name=schema_name)
        cursor.execute(sql)
        cursor.close()
        
    def load_segmentation_database(self, shapefile_path, shapefile_name)   
        
        shapefile = osgeo.ogr.Open(shapefile_path)
        layer = shapefile.GetLayer(0)

        cursor = self.conn.cursor()
        
        cursor.execute("DELETE FROM {shapefile_name}".format(shapefile_name))
        cursor.execute("CREATE TABLE {shapefile_name} (id SERIAL PRIMARY KEY,\
                         geom GEOMETRY)".format(shapefile_name))

        #First delete the existing contents of this table in case we want to run the code multiple times.
        cursor.execute("DELETE FROM {shapefile_name}".format(shapefile_name))
        

        for i in range(layer.GetFeatureCount()):
            feature = layer.GetFeature(i)
            #Get feature geometry
            geometry = feature.GetGeometryRef()
            #Convert geometry to WKT format
            wkt = geometry.ExportToWkt()
            #Insert data into database, converting WKT geometry to a PostGIS geography
            cursor.execute("INSERT INTO {shapefile_name} (geom) VALUES (ST_GeogFromText('{}'))".format(wkt))
        self.open_connect.commit()


if __name__ == '__main__':

    conn_rascunho = Connection("host=localhost dbname=ta7_rascunho user=postgres password=postgres")
    conn_rascunho.create_scene_path_row_schema("215_068")
    

