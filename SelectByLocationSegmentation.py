import fiona
import LandsatFileInfo as LcInfo
import Connection2Database as Conn
from shapely.geometry import shape, MultiPolygon


def get_geom_from_lc_ba_scene(self):
    connection = Conn.Connection("host=localhost dbname=ta7 user=postgres password=postgres")
    pathrow = LcInfo.LandsatFileInfo(self.image_file_path_targz).get_path_row_from_file()
    path_row = '{}/{}'.format(pathrow[0], pathrow[1])
    lc_scene_geom = connection.get_scene_path_row_geom(path_row)[0][2]

    return lc_scene_geom


def read_segmentation_shp(self):
    """
    Reading segmentation results from output folder
    :return: Segments from segmentation that intersect landsat scene interested to Bahia monitoring forest project
    """
    file_path = '{out}{file_name}-seeds.shp'.format(out=self.get_folder_output_file_processed_path(),
                                                    file_name=self.get_file_name_targz)
    # MultiPolygon from the list of Polygons
    multipoly = MultiPolygon([shape(pol['geometry']) for pol in fiona.open(file_path)])

    return multipoly