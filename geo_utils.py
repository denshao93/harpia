from osgeo import ogr, osr
from shapely.geometry import Point, Polygon


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

def create_polygon_from_bbox(bbox):

    p1 = Point(bbox[0], bbox[3])
    p2 = Point(bbox[2], bbox[3])
    p3 = Point(bbox[2], bbox[1])
    p4 = Point(bbox[0], bbox[1])

    np1 = (p1.coords.xy[0][0], p1.coords.xy[1][0])
    np2 = (p2.coords.xy[0][0], p2.coords.xy[1][0])
    np3 = (p3.coords.xy[0][0], p3.coords.xy[1][0])
    np4 = (p4.coords.xy[0][0], p4.coords.xy[1][0])

    bb_polygon = Polygon([np1, np2, np3, np4])

    return bb_polygon


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