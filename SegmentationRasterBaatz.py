from terralib import raster, rp

r = raster.open('/tmp/LC08_L1TP_215068_20151114_20170402_01_T1/LC08_L1TP_215068_20151114_20170402_01_T1_B5.TIF')

raster.SegmenterRegionGrowingMean(r, range(r.getNumberOfBands()), 'mean.tif', minSegmentSize=100, segmentsSimilarityThreshold=0.1)
# rp.SegmenterRegionGrowingBaatz(rst, [0,1], 'baatz.tif', bandsWeights=[0.5, 0.5], segmentsSimilarityThreshold=0.5, colorWeight=0.9, compactnessWeight=0.5)