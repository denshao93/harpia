import psycopg2
import ogr
from SatelliteFileInfo import LandsatFileInfo as LCinfo
import geo_utils as gu


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
        :param path_row: Path and row must be writed as: pathrow (ex. 215068)
        :return: Fields from table lc_ba (landsat Bahia): id, pr, ogr_geom
        """
        cursor = self.conn.cursor()
        # pr = path_row
        sql = "SELECT fid, pr, ST_GeomFromWKB(ogr_geometry) FROM lc_ba WHERE pr = '{path_row}';"\
              .format(path_row=path_row)
        cursor.execute(sql)
        qtd = cursor.fetchall()
        cursor.close()
        return qtd
    
    def create_scene_path_row_schema(self, satellite_name, path_row):
        """Create the schema in draft database where segmentation will be save.
           In Harpia project the draft database is called as ta7_rascunho
        
        Arguments:
            satellite_name {string} -- The initials from satelite name (Lansat 8 = lc8)
            _path_row {string} -- The index where find scene from Lansat 8.
            They have to be all together (i.e. 215068) 
        """
                
        cursor = self.conn.cursor()
        sql = "CREATE SCHEMA IF NOT EXISTS \
               {satellite_name}_{path_row};".format(path_row=path_row,
                                                    satellite_name=satellite_name)
        cursor.execute(sql)
        cursor.close()
        
    def load_segmentation_database(self, shapefile_path, shapefile_name):  
        
        layer = gu.read_shape_file_ogr(shapefile_path)

        cursor = self.conn.cursor()
        
        # cursor.execute("DELETE FROM \"lc8_215_068\".{shapefile_name};"\
        #                 .format(shapefile_name=shapefile_name))
        cursor.execute("CREATE TABLE IF NOT EXISTS lc8_215_068.{shapefile_name} \
                        (id SERIAL PRIMARY KEY, geom GEOMETRY);".format(shapefile_name=shapefile_name))

        #First delete the existing contents of this table in case we want to run the code multiple times.
        # cursor.execute("DELETE FROM lc8_215_068.{shapefile_name};".format(shapefile_name=shapefile_name))
        
        for i in range(layer.GetFeatureCount()):
            feature = layer.GetFeature(i)
            #Get feature geometry
            geometry = feature.GetGeometryRef()
            #Convert geometry to WKT format
            wkt = geometry.ExportToWkt()
            #Insert data into database, converting WKT geometry to a PostGIS geography
            cursor.execute("INSERT INTO lc8_215_068.{shapefile_name} (geom) \
                            VALUES (ST_GeomFromText('{_wkt}'))"
                            .format(shapefile_name=shapefile_name, _wkt=wkt))   


if __name__ == '__main__':

    conn_rascunho = Connection("host=localhost dbname=ta7_rascunho user=postgres password=postgres")
    # conn_rascunho.create_scene_path_row_schema("215068")
    conn_rascunho.load_segmentation_database(shapefile_path="~/Downloads/teste-slic.shp",
                                             shapefile_name="teste_slic")

    

