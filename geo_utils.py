from osgeo import ogr, osr
from shapely.geometry import Point, Polygon
import shapefile
from shapely.geometry import shape


def project_geometry(vector_layer, source_src, target_src):

    try:
        source = osr.SpatialReference()
        source.ImportFromWkt(source_src)

        target = osr.SpatialReference()
        target.ImportFromWkt(target_src)

        transform = osr.CoordinateTransformation(source, target)

        vector_layer = str(vector_layer)
        geometry = ogr.CreateGeometryFromWkt(vector_layer)
        geometry.Transform(transform)
        
        return geometry

    except Exception as e:
        print("Error geo_utils project_geometry+: " + str(e))

def read_shape_file_ogr(shape_file_path):

    file = ogr.Open(shape_file_path)
    layer = file.GetLayer(0)

    return layer

def create_polygon_from_bbox_1(bbox):

    # Create ring
    ring = ogr.Geometry(ogr.wkbLinearRing)

    ring.AddPoint(bbox[0], bbox[3])
    ring.AddPoint(bbox[2], bbox[3])
    ring.AddPoint(bbox[2], bbox[1])
    ring.AddPoint(bbox[0], bbox[1])

    # Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    polygon = poly.AddGeometry(ring)

    print(poly.ExportToWkt())

    return polygon

def read_shapefile_polyt_as_wkt(vector_path):
    
    vct = shapefile.Reader(vector_path)
    feature = vct.shapeRecords()[0]
    first = feature.shape.__geo_interface__  
    
    shp_geom = shape(first)
    print(shp_geom)
    
    return shp_geom