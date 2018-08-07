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

        values = []

        for i in range(layer.GetFeatureCount()):
            
            feature = layer.GetFeature(i)
            # Get feature geometry
            geometry = feature.GetGeometryRef()
            # Convert geometry to WKT format
            wkt = geometry.ExportToWkt()
            # Check intersect
            geom = loads(wkt)
            img_path = os.path.join(self.tmp_dir, f"{self.output_file_name}.TIF")
            intersection = R.Raster(img_path=img_path).intersetion_pathrow_ba_()

            intersect = geom.intersects(intersection)

            
            intersection = gpd.GeoDataFrame(intersect)
            intersection.plot()
            plt.show()

            if intersect:
                print(i)
                values = values.append(wkt)
        
        return values


    def insert_geom(self):
        
        sql = f"INSERT INTO  {self.satellite_initials_name}_{self.satellite_index}_{self.date} (geom)"\
              f"VALUES ({self.load_segmentation_database()})"
        self.runQuery(sql)

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
        self.create_scene_path_row_schema()
        self.create_table_scene_path_row_scene()
        self.del_table_scene_path_row_scene()
        self.insert_geom()
        self.set_geom_srid_as_4674()
        self.create_gist_index_geom_colum()


# if __name__ == "__main__":

#     load_seg = LoadSegmentationDatabase(segmentation_file_path="/media/diogocaribe/56A22ED6A22EBA7F/PROCESSADA/CBERS/151116/2017/07_Julho/CBERS_4_MUX_20170718_151_116_L4/CBERS_151116_20170718_SLICO.shp",
#     output_dir="/media/diogocaribe/56A22ED6A22EBA7F/PROCESSADA/CBERS/151116/2017/07_Julho/CBERS_4_MUX_20170718_151_116_L4",
#     output_file_name="CBERS_151116_20170718", tmp_dir = 
#     satellite_index="151116", satellite_initials_name="CBERS", date="20170718")
#     load_seg.run_load_segmentation()
