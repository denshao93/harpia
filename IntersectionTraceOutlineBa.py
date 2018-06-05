import shapefile
import constants as c
import geo_utils as gu
from shapely.geometry import shape


class IntersectionTraceOulineBa:

    def __init__(self, trace_outline_path):
        
        self.trace_outline_path = trace_outline_path

    def reproject_trace_outline_to_4674(self):
        """Raster file is in 4674 and it is necessary to convert 
        trace outline to it because it is in WGS UTM 24N
        """
        # Bahia buffer
        
        trace_outline = gu.read_shapefile_polyt_as_wkt(self.trace_outline_path)

        teste = gu.project_geometry(vector_layer=trace_outline, source_src=c.wgs84_24N, target_src=c.sirgas2000)
        print("teste"+str(teste))
        
        return trace_outline

if __name__ == '__main__':
    
    IntersectionTraceOulineBa(trace_outline_path="/tmp/tmphxggj49p/trace_outline.shp").reproject_trace_outline_to_4674()