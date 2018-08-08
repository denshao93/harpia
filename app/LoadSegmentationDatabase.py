import os
import psycopg2


class LoadSegmentationDatabase:
    """Load segmetation in draft database."""

    def __init__(self, output_dir, 
                satellite_parameters, 
                output_file_name):
        """Set docstring here.

        Parameters
        ----------
        self: 
        output_dir: str
            Directory where image file be.
        output_file_name: str
            Name give to image file save in output directory.
        satellite_parameters: dict
            Important parameters from satellite file.
            Options:
                dict["initials_name]
                dict["sensor"]
                dict["scene_file_name"]
                dict["aquisition_date"]
                dict["aquisition_year"]
                dict["aquisition_month"]
                dict["aquisition_day"]
                dict["julian_day"]
                dict["days_from_today"]
                dict["index"]
        Returns
        -------

        """   
        # Directory where image file is stored.
        self.output_dir = output_dir
        # Dictionary with all parameters from satellite files.
        self.satellite_parameters = satellite_parameters
        # Name given to file store in output directory
        self.output_file_name = output_file_name

        # Select variables from satellite parameters in order to use.
        self.satellite_initials_name = self.satellite_parameters["initials_name"]
        self.satellite_index = self.satellite_parameters["index"]

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
        segmentation_file_path = os.path.join(self.output_dir, f"{self.output_file_name}_*.shp")

        command =   f"ogr2ogr -f \"PostgreSQL\" -a_srs \"EPSG:4674\" -nlt POLYGON -overwrite "\
                    f"PG:\"host=172.16.0.175 user=postgres dbname=ta7_rascunho password=123456\" -progress "\
                    f"-nln {self.satellite_initials_name.lower()}_{self.satellite_index}.{self.output_file_name} "\
                    f"{segmentation_file_path}"
        
        os.system(command)

    def del_nodata_segmentation(self):
        """Delete polygons created in dummy region from raster (background)."""   
        sql =   f"DELETE FROM {self.satellite_initials_name}_{self.satellite_index}.{self.output_file_name} "\
                f"WHERE \"4_average\" = 0.0"

        self.runQuery(sql)

    def delete_columns_from_segmentation(self):
        """Delete created by segmentation shapefile that are useless."""
        sql =   f"ALTER TABLE  {self.satellite_initials_name}_{self.satellite_index}.{self.output_file_name} "\
                f"DROP COLUMN class, "\
                f"DROP COLUMN area, "\
                f"DROP COLUMN \"1_average\", "\
                f"DROP COLUMN \"2_average\", "\
                f"DROP COLUMN \"3_average\", "\
                f"DROP COLUMN \"4_average\", "\
                f"DROP COLUMN \"1_stddev\", "\
                f"DROP COLUMN \"2_stddev\", "\
                f"DROP COLUMN \"3_stddev\", "\
                f"DROP COLUMN \"4_stddev\"; "
        
        self.runQuery(sql)

    def run_load_segmentation(self):
        """Run all process to load segmentation in draft database."""
        self.create_scene_path_row_schema()
        self.load_segmentation_database()
        self.del_nodata_segmentation()
        self.delete_columns_from_segmentation()


# if __name__ == '__main__':
    
#     import SatelliteFileInfo as SFI
#     s = SFI.SatelliteFileInfo(file_path="/home/diogocaribe/BRUTA/CEBERS4/CBERS_4_MUX_20180627_149_116_L2_BAND5.zip")
#     LoadSegmentationDatabase(output_dir="/home/diogocaribe/PROCESSADA/CBERS/149116/2018/06_Junho/CBERS_4_MUX_20180627_149_116_L2",
#                             satellite_parameters=s.get_parameter_satellite(),
#                             output_file_name="CBERS_149116_20180627").run_load_segmentation()

    