import ogr, osr


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