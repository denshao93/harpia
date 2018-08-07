import os # NOQA
import psycopg2


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
        
        self.date = date

    @staticmethod
    def runQuery(query):
        """Run postgres query."""
        connect_text = """dbname='ta7_rascunho' user='postgres'
                          host=172.16.0.175 port=5432 password='123456'"""
        con = psycopg2.connect(connect_text)
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        con.close()

    def create_scene_path_row_schema(self):
        """Create schema in draft database where segmentation will be save."""
        sql =   f"CREATE SCHEMA IF NOT EXISTS "\
                f"{self.satellite_initials_name}_{self.satellite_index}"
        self.runQuery(sql)

    def create_table_scene_path_row_scene(self):
        """Clear table to load segmentation."""
        sql =   f"DROP TABLE IF EXISTS {self.satellite_initials_name}_{self.satellite_index}.{self.output_file_name};"\
                f"CREATE TABLE IF NOT EXISTS "\
                f"{self.satellite_initials_name}_{self.satellite_index}.{self.output_file_name} "\
                f"(id SERIAL PRIMARY KEY, geom GEOMETRY(POLYGON));"
        self.runQuery(sql)

    def del_table_scene_path_row_scene(self):
        """Clear table to load segmentation."""
        sql =   f"DELETE FROM "\
                f"{self.satellite_initials_name}_{self.satellite_index}.{self.output_file_name};"
        self.runQuery(sql)

    def load_segmentation_database(self):

        """Load segmetation in draft database."""
        command =   f"ogr2ogr -f \"PostgreSQL\" -a_srs \"EPSG:4674\" -nlt POLYGON -overwrite "\
                    f"PG:\"host=172.16.0.175 user=postgres dbname=ta7_rascunho password=123456\" -progress "\
                    f"-nln {self.satellite_initials_name.lower()}_{self.satellite_index}.{self.output_file_name} "\
                    f"{self.segmentation_file_path}"
        
        os.system(command)

    def del_nodata_segmentation(self):
        sql =   f"SELECT * FROM {self.satellite_initials_name}_{self.satellite_index}.{self.output_file_name} "\
                f"WHERE '4_average' = 0"

        self.runQuery(sql)

    def delete_columns_from_segmentation(self):
        sql =   f"ALTER TABLE  {self.satellite_initials_name}_{self.satellite_index}.{self.output_file_name}"\
                f"DROP COLUMN class; "\
                f"DROP COLUMN 1_average; "\
                f"DROP COLUMN 2_average; "\
                f"DROP COLUMN 3_average; "\
                f"DROP COLUMN 4_average; "\
                f"DROP COLUMN 1_stddev; "\
                f"DROP COLUMN 2_stddev; "\
                f"DROP COLUMN 3_stddev; "\
                f"DROP COLUMN 4_stddev; "
        
        self.runQuery(sql)

    def run_load_segmentation(self):
        """Run all process to load segmentation in draft database."""
        self.create_scene_path_row_schema()
        # self.load_segmentation_database()
        self.del_nodata_segmentation()
        self.delete_columns_from_segmentation()



if __name__ == "__main__":

    load_seg = LoadSegmentationDatabase(segmentation_file_path="/mnt/cotic/COTIC/GEOPROCESSAMENTO/GEO_DADOS/2_RASTER/2.1_ORTO/PROCESSADA/CBERS/149116/2018/06_Junho/CBERS_4_MUX_20180627_149_116_L2/CBERS_149116_20180627_SLICO.shp",
    output_dir="/mnt/cotic/COTIC/GEOPROCESSAMENTO/GEO_DADOS/2_RASTER/2.1_ORTO/PROCESSADA/CBERS/149116/2018/06_Junho",
    output_file_name="CBERS_149116_20180627", tmp_dir = "/tmp",
    satellite_index="149116", satellite_initials_name="CBERS", date="20180627")
    load_seg.run_load_segmentation()
