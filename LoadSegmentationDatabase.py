from osgeo import ogr
import geo_utils as gu
import Connection2Database as Con
from SatelliteFileInfo import LandsatFileInfo as LCinfo



class LoadSegmentationDatabase:

    def __init__(self, segmentation_file_path, full_scene_name, img_file_name_stored):
        self.str_connection ="host=localhost dbname=ta7_rascunho" \
                        "user=postgres password=postgres"
        self.connection = Con.Connection(self.str_connection).open_connect()

        self.segmentation_file_path = segmentation_file_path

        self.img_file_name_stored = img_file_name_stored

        self.lcinfo = LCinfo(full_scene_name)
        self.path_row = "".join(self.lcinfo.get_path_row_from_file())
        self.satellite_name = self.lcinfo.get_satellite_name()

    # 1)
    def create_scene_path_row_schema(self):
        """Create the schema in draft database where segmentation will be save.
           In Harpia project the draft database is called as ta7_rascunho

        Arguments:
            satellite_name {string} -- The initials from satelite name (Lansat 8 = lc08)
            _path_row {string} -- The index where find scene from Lansat 8.
            They have to be all together (i.e. 215068)
        """

        cursor = self.connection.cursor()
        sql =   "CREATE SCHEMA IF NOT EXISTS " \
                "{satellite_name}_{path_row};".format(path_row=self.path_row,
                                                      satellite_name=self.satellite_name)
        cursor.execute(sql)
        cursor.close()
    # 2)
    def create_table_scene_path_row_scene(self):
        """Clear table to load segmentation

        Arguments:
            satellite_name {string} -- The initials from satelite name (Lansat 8 = lc8)
            _path_row {string} -- The index where find scene from Lansat 8.
            They have to be all together (i.e. 215068)
        """
        cursor = self.connection.cursor()
        sql =   "CREATE TABLE IF NOT EXISTS {satellite_name}_{path_row}.{file_name}" \
                "(id SERIAL PRIMARY KEY, geom GEOMETRY(MULTIPOLYGON));".format(path_row=self.path_row,
                                                                                satellite_name=self.satellite_name,
                                                                                file_name=self.img_file_name_stored)
        cursor.execute(sql)
        cursor.close()
    # 3)
    def del_table_scene_path_row_scene(self):
        """Clear table to load segmentation

        Arguments:
            satellite_name {string} -- The initials from satelite name (Lansat 8 = lc8)
            _path_row {string} -- The index where find scene from Lansat 8.
            They have to be all together (i.e. 215068)
        """
        cursor = self.connection.cursor()
        sql = "DELETE FROM {satellite_name}_{path_row}.{file_name};".format(path_row=self.path_row,
                                                                            satellite_name=self.satellite_name,
                                                                            file_name=self.img_file_name_stored)
        cursor.execute(sql)
        cursor.close()

    def load_segmentation_database(self):

        file = ogr.Open(self.segmentation_file_path)
        layer = file.GetLayer(0)

        cursor = self.connection.cursor()

        for i in range(layer.GetFeatureCount()):
            feature = layer.GetFeature(i)
            #Get feature geometry
            geometry = feature.GetGeometryRef()
            #Convert geometry to WKT format
            wkt = geometry.ExportToWkt()
            #Insert data into database, converting WKT geometry to a PostGIS geometry
            cursor.execute("INSERT INTO {satellite_name}_{path_row}.{file_name} (geom)" \
                            "VALUES (ST_GeomFromText('{_wkt}'))".format(path_row=self.path_row,
                                                                        satellite_name=self.satellite_name,
                                                                        file_name=self.img_file_name_stored,
                                                                        _wkt=wkt))
            print("Adicionando "+ str(i))

        cursor.close()

    def run_load_segmentation(self):
        self.create_scene_path_row_schema()
        self.create_table_scene_path_row_scene()
        self.del_table_scene_path_row_scene()
        self.load_segmentation_database

if __name__ == "__main__":

    load_seg = LoadSegmentationDatabase(segmentation_file_path="/media/diogocaribe/" \
                                        "56A22ED6A22EBA7F/PROCESSADA/LC08/2017/12/215068/" \
                                        "LC08_L1TP_215068_20171205_20171222_01_T1/" \
                                        "LC08_215068_20171205_SLIC.shp",
                                        full_scene_name="LC08_L1TP_215068_20171205_20171222_01_T1",
                                        img_file_name_stored="LC08_215068_20171205")
    load_seg.run_load_segmentation()