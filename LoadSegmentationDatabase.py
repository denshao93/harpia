import os
import psycopg2
from osgeo import ogr
import multiprocessing
import geo_utils as gu
from shapely.wkt import loads
from SatelliteFileInfo import LandsatFileInfo as LCinfo


class LoadSegmentationDatabase:

    def __init__(self, segmentation_file_path, full_scene_name, img_file_name_stored, dir_tmp_img):

        self.dir_tmp_img = dir_tmp_img
        self.conn = psycopg2.connect("host='localhost' dbname='ta7_rascunho' user='postgres' password='postgres'")
        self._cur = self.conn.cursor()
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
        cursor = self._cur
        sql = 'CREATE SCHEMA IF NOT EXISTS {satellite_name}_{path_row}'.format(path_row=self.path_row, satellite_name=self.satellite_name)
        # sql = """SELECT datname from pg_database"""
        cursor.execute(sql)
        self.conn.commit()
        # cursor.close()
    # 2)
    def create_table_scene_path_row_scene(self):
        """Clear table to load segmentation

        Arguments:
            satellite_name {string} -- The initials from satelite name (Lansat 8 = lc8)
            _path_row {string} -- The index where find scene from Lansat 8.
            They have to be all together (i.e. 215068)
        """
        cursor = self._cur
        sql =   "CREATE TABLE IF NOT EXISTS {satellite_name}_{path_row}.{file_name}" \
                "(id SERIAL PRIMARY KEY, geom GEOMETRY(POLYGON));".format(path_row=self.path_row,
                                                                                satellite_name=self.satellite_name,
                                                                                file_name=self.img_file_name_stored)
        cursor.execute(sql)
        self.conn.commit()
        # cursor.close()
    # 3)
    def del_table_scene_path_row_scene(self):
        """Clear table to load segmentation

        Arguments:
            satellite_name {string} -- The initials from satelite name (Lansat 8 = lc8)
            _path_row {string} -- The index where find scene from Lansat 8.
            They have to be all together (i.e. 215068)
        """
        cursor = self._cur
        sql = "DELETE FROM {satellite_name}_{path_row}.{file_name};".format(path_row=self.path_row,
                                                                            satellite_name=self.satellite_name,
                                                                            file_name=self.img_file_name_stored)
        cursor.execute(sql)
        self.conn.commit()
        # cursor.close()

    @staticmethod
    def runQuery(query):
        connect_text = "dbname='ta7_rascunho' user='postgres' host=localhost port=5432 password='postgres'"
        con = psycopg2.connect(connect_text)
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        con.close()

    def load_segmentation_database(self):

        file = ogr.Open(self.segmentation_file_path)
        layer = file.GetLayer(0)

        # cursor = self._cur
        intersect_pathrow_path = os.path.join(self.dir_tmp_img, "intersect_pathrow_ba.shp")
        geom2 = gu.read_shapefile_poly(intersect_pathrow_path)
        queries = []
        count = 0
        for i in range(layer.GetFeatureCount()):
            feature = layer.GetFeature(i)
            #Get feature geometry
            geometry = feature.GetGeometryRef()
            #Convert geometry to WKT format
            wkt = geometry.ExportToWkt()

            # TODO Colocar a toque como condição para carga no banco do poligono
            geom1 = loads(wkt)

            intersetc = geom1.intersects(geom2)
            if intersetc:
                count+=1
                #Insert data into database, converting WKT geometry to a PostGIS geometry
                # cursor.execute
                if count < 5000:
                    query = "INSERT INTO {satellite_name}_{path_row}.{file_name} (geom)" \
                            " VALUES (ST_GeomFromText('{_wkt}'))".format(path_row=self.path_row,
                                                                        satellite_name=self.satellite_name,
                                                                        file_name=self.img_file_name_stored,
                                                                        _wkt=wkt)
                    queries.append(query)
                else:
                    print("Salvando no banco")
                    count=0
                    pool = multiprocessing.Pool(6)
                    for i in pool.imap_unordered(self.runQuery, queries):
                        continue
                    pool.close()
                    queries = []
    def set_geom_srid_as_4674(self):

        cursor = self._cur
        sql =   "ALTER TABLE {satellite_name}_{path_row}.{file_name} " \
                "ALTER COLUMN geom  TYPE geometry(POLYGON, 4674) USING ST_SetSRID(geom, 4674);" \
                                                    .format(path_row=self.path_row,
                                                            satellite_name=self.satellite_name,
                                                            file_name=self.img_file_name_stored)
        cursor.execute(sql)
        self.conn.commit()
        # cursor.close()

    def create_gist_index_geom_colum(self):

        cursor = self._cur
        sql =   "CREATE INDEX {file_name}_geom_idx ON {satellite_name}_{path_row}.{file_name}" \
                " USING GIST (geom);".format(path_row=self.path_row,
                                            satellite_name=self.satellite_name,
                                            file_name=self.img_file_name_stored)
        cursor.execute(sql)
        self.conn.commit()
        cursor.close()

    def run_load_segmentation(self):
        self.create_scene_path_row_schema()
        self.create_table_scene_path_row_scene()
        self.del_table_scene_path_row_scene()
        self.load_segmentation_database()
        self.set_geom_srid_as_4674()
        self.create_gist_index_geom_colum()

if __name__ == "__main__":

    load_seg = LoadSegmentationDatabase(segmentation_file_path="/media/diogocaribe/56A22ED6A22EBA7F/PROCESSADA/LC08/2017/12_Dezembro/215068/LC08_L1TP_215068_20171205_20171222_01_T1/LC08_215068_20171205_SLIC.shp",
                                        full_scene_name="LC08_L1TP_215068_20171205_20171222_01_T1",
                                        img_file_name_stored="LC08_215068_20171205",
                                        dir_tmp_img="/tmp/tmp9zbcy28w")
    load_seg.run_load_segmentation()