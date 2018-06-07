import os
import shapefile
import constants as const
import geo_utils as gu
from osgeo import ogr
from shapely.geometry import shape


class IntersectionTraceOutlineBa:

    def __init__(self, dir_tmp_img):

        self.dir_tmp_img = dir_tmp_img

    def intersetion_pathrow_ba(self):
        """Raster file is in 4674 and it is necessary to convert
        trace outline to it because it is in WGS UTM 24N
        """
        # Bahia buffer
        trace_outline_path = os.path.join(self.dir_tmp_img, "trace_outline.shp")

        read_trace_outline = gu.read_shapefile_poly(trace_outline_path)
        ba_buffer = gu.read_shapefile_poly("vector/ba_4674_buffer.shp").to_wkt()
        ba_buffer = ogr.CreateGeometryFromWkt(ba_buffer)

        trace_outline = gu.project_geometry(vector_layer=read_trace_outline.to_wkt(),
                                            source_src=const.wgs84_24N, target_src=const.sirgas2000)


        inter = trace_outline.Intersection(ba_buffer).ExportToWkt()

        return inter

    def save_intersection_as_shapefile(self):

        gu.save_wkt_as_shapefile(self.intersetion_pathrow_ba(), self.dir_tmp_img)


if __name__ == '__main__':

    IntersectionTraceOutlineBa(trace_outline_path="/tmp/tmpvyzesrkd/trace_outline.shp",
                                dir_tmp_img="/tmp/tmpvyzesrkd").save_intersection_as_shapefile()