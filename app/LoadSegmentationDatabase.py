import os
import yaml
import psycopg2


class LoadSegmentationDatabase:
    """Load segmetation in draft database."""

    def __init__(self, tmp_dir, 
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
        self.output_dir = tmp_dir
        # Dictionary with all parameters from satellite files.
        self.satellite_parameters = satellite_parameters
        # Name given to file store in output directory
        self.output_file_name = output_file_name

        # Select variables from satellite parameters in order to use.
        self.satellite_initials_name = self.satellite_parameters["initials_name"]
        self.satellite_index = self.satellite_parameters["index"]

    def connection_string_db(self):
        # Open yaml 
        with open("config/const.yaml", 'r') as f:
            const = yaml.load(f)
        host = const['draft_db']['host']
        dbname = const['draft_db']['dbname']
        user = const['draft_db']['user']
        password = const['draft_db']['password']
        port = const['draft_db']['port']

        db_string = f'host={host},database={dbname},user={user},'\
                    f'password={password},port={port}'
        print(db_string)
                        
        return db_string
    
    def runQuery(self, query):
        """Run postgres query."""
        connect_text = self.connection_string_db()
        con = psycopg2.connect(connect_text)
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        con.close()

    def create_scene_path_row_schema(self):
        """Create schema in draft database where segmentation will be save."""
        sql =   f"CREATE SCHEMA IF NOT EXISTS "\
                f"{self.satellite_initials_name.lower()}_{self.satellite_index.lower()};"

        self.runQuery(sql)

    def create_table_scene_path_row_scene(self):
        """Clear table to load segmentation."""
        sql =   f"DROP TABLE IF EXISTS {self.satellite_initials_name.lower()}_{self.satellite_index.lower()}.{self.output_file_name.lower()};"\
                f"CREATE TABLE IF NOT EXISTS "\
                f"{self.satellite_initials_name.lower()}_{self.satellite_index.lower()}.{self.output_file_name.lower()} "\
                f"(id SERIAL PRIMARY KEY, geom GEOMETRY(POLYGON));"

        self.runQuery(sql)

    def del_table_scene_path_row_scene(self):
        """Clear table to load segmentation."""
        sql =   f"DELETE FROM "\
                f"{self.satellite_initials_name.lower()}_{self.satellite_index.lower()}.{self.output_file_name.lower()};"
        
        self.runQuery(sql)

    def load_segmentation_database(self):
        """Load segmetation in draft database."""
        segmentation_file_path = os.path.join(self.output_dir, f"{self.output_file_name}_*.shp")

        command =   f"ogr2ogr -f \"PostgreSQL\" -a_srs \"EPSG:4674\" -nlt POLYGON "\
                    f"-overwrite PG:\"{self.connection_string_db}\" -progress "\
                    f"-nln {self.satellite_initials_name.lower()}_"\
                    f"{self.satellite_index.lower()}.{self.output_file_name.lower()} "\
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


if __name__ == '__main__':
    
    import SatelliteFileInfo as SFI
    s = SFI.SatelliteFileInfo(file_path="/home/diogo.sousa/BRUTA/LANDSAT/LC08_L1TP_215068_20151114_20170402_01_T1.tar.gz")
    LoadSegmentationDatabase(tmp_dir="/home/diogo.sousa/Desktop",
                            satellite_parameters=s.get_parameter_satellite(),
                            output_file_name="LC08_215068_20151114").run_load_segmentation()
