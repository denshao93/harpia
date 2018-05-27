#  import raster, rp

r = raster.open('/media/diogocaribe/56A22ED6A22EBA7F/PROCESSADA/LC08/2017/12/215068/LC08_L1TP_215068_20171205_20171222_01_T1/LC08_L1TP_215068_20171205_20171222_01_T1.TIF')

# raster.SegmenterRegionGrowingMean(r, range(r.getNumberOfBands()), 'mean.tif', minSegmentSize=100, segmentsSimilarityThreshold=0.1)
rp.SegmenterRegionGrowingBaatz(r, [0,1], 'baatz.tif', bandsWeights=[0.5, 0.5], segmentsSimilarityThreshold=0.5, colorWeight=0.9, compactnessWeight=0.5)