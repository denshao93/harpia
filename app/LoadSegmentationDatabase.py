import os # NOQA
import psycopg2
from osgeo import ogr
import multiprocessing
import geo_utils as gu
from shapely.wkt import loads
import Raster as R

import matplotlib.pyplot as plt
import geopandas as gpd


class LoadSegmentationDatabase:
    """Load segmetation in draft database."""

    def __init__(self, segmentation_file_path, output_dir, output_file_name, 
                    satellite_index, satellite_initials_name, date, tmp_dir):
        """Init."""
        
        self.segmentation_file_path = segmentation_file_path

        self.output_file_name = output_file_name

        self.satellite_index = satellite_index
        self.satellite_initials_name = satellite_initials_name

        self.output_dir = output_dir
        self.tmp_dir = tmp_dir
        self.date = date

    @staticmethod
    def runQuery(query):
        """Run postgres query."""
        connect_text = """dbname='harpia_rascunho' user='postgres'
                          host=localhost port=5432 password='postgres'"""
        con = psycopg2.connect(connect_text)
        cur = con.cursor()
        cur.execute(query)
        rowcount = cur.rowcount
        con.commit()
        con.close()
        if rowcount == -1:
            print(query)
        return rowcount

    def create_scene_path_row_schema(self):
        """Create schema in draft database where segmentation will be save."""
        sql = """CREATE SCHEMA IF NOT EXISTS
                    {satellite_name}_{path_row}""".format(
                    path_row=self.satellite_index, satellite_name=self.satellite_initials_name)
        self.runQuery(sql)

    def create_table_scene_path_row_scene(self):
        """Clear table to load segmentation."""
        sql = """DROP TABLE IF EXISTS {satellite_name}_{path_row}.{file_name};
                 CREATE TABLE IF NOT EXISTS
                    {satellite_name}_{path_row}.{file_name}
                    (id SERIAL PRIMARY KEY, geom GEOMETRY(POLYGON));""" \
                    .format(path_row=self.satellite_index,
                            satellite_name=self.satellite_initials_name,
                            file_name=self.output_file_name)
        self.runQuery(sql)

    def del_table_scene_path_row_scene(self):
        """Clear table to load segmentation."""
        sql = """DELETE FROM
                    {satellite_name}_{path_row}.{file_name};""" \
                    .format(path_row=self.satellite_index,
                            satellite_name=self.satellite_initials_name,
                            file_name=self.output_file_name)
        self.runQuery(sql)

    def create_insert_geom_query(self, wkt):
        """Create string query to insert geom to table database."""
        sql = """INSERT INTO
                   {satellite_name}_{path_row}.{file_name} (geom)
                   VALUES (ST_GeomFromText('{_wkt}'))""" \
                   .format(path_row=self.satellite_index,
                           satellite_name=self.satellite_initials_name,
                           file_name=self.output_file_name,
                           _wkt=wkt)
        return sql

    def load_segmentation_database(self):
        """Load segmetation in draft database."""
        file = ogr.Open(self.segmentation_file_path)
        layer = file.GetLayer(0)

        img_path = os.path.join(self.tmp_dir, f"{self.output_file_name}.TIF")
        intersection = R.Raster(img_path=img_path).intersetion_img_useless_ba()
        values = []

        for i in range(layer.GetFeatureCount()):
            
            feature = layer.GetFeature(i)
            # Get feature geometry
            geometry = feature.GetGeometryRef()
            # Convert geometry to WKT format
            wkt = geometry.ExportToWkt()
            # Check intersect
            geom = loads(wkt)
            
            intersect = geom.intersects(intersection)

            if intersect:
                # print(i)
                values.append(wkt)
                if len(values) == 10:
                    
                    sql = f"INSERT INTO  {self.satellite_initials_name}_{self.satellite_index}_{self.date} (geom)"\
                        f" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    self.runQuery(sql)
        # return values


    def insert_geom(self):
        pass
        

    def set_geom_srid_as_4674(self):
        """Set SRID as 4674 to geom column."""
        sql = """ALTER TABLE {satellite_name}_{path_row}.{file_name}
                ALTER COLUMN geom TYPE geometry(POLYGON, 4674)
                        USING ST_SetSRID(geom, 4674);""" \
                        .format(path_row=self.satellite_index,
                                satellite_name=self.satellite_initials_name,
                                file_name=self.output_file_name)
        self.runQuery(sql)

    def create_gist_index_geom_colum(self):
        """Create gist index to geom column."""
        sql = """CREATE INDEX {file_name}_geom_idx
                 ON {satellite_name}_{path_row}.{file_name}
                 USING GIST (geom);""" \
                 .format(path_row=self.satellite_index,
                         satellite_name=self.satellite_initials_name,
                         file_name=self.output_file_name)
        self.runQuery(sql)

    def run_load_segmentation(self):
        """Run all process to load segmentation in draft database."""
        # self.create_scene_path_row_schema()
        # self.create_table_scene_path_row_scene()
        # self.del_table_scene_path_row_scene()
        self.load_segmentation_database()
        # self.insert_geom()
        self.set_geom_srid_as_4674()
        self.create_gist_index_geom_colum()


if __name__ == "__main__":

    load_seg = LoadSegmentationDatabase(segmentation_file_path="/media/diogocaribe/56A22ED6A22EBA7F/PROCESSADA/LC08/215068/2017/12_Dezembro/LC08_L1TP_215068_20171205_20171222_01_T1/LC08_215068_20171205_SLICO.shp",
    output_dir="/media/diogocaribe/56A22ED6A22EBA7F/PROCESSADA/LC08/215068/2017/12_Dezembro/LC08_L1TP_215068_20171205_20171222_01_T1",
    output_file_name="LC08_215068_20171205", tmp_dir = "/tmp/tmp8nyi8g30",
    satellite_index="215068", satellite_initials_name="LC08", date="20171205")
    load_seg.run_load_segmentation()
