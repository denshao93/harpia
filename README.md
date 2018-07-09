## Routine to preprocess satellite image to forest monitoring
_______________________________________________________________________________________________

The aim of this routine is automate stepts for forest monotoring used with TerraAmazon 7 program.

The main steps that it will do are:

    1) Download landsat and Sentinel2 imagem from USGS.
    2) Organize directories where output images processed will be stored.
    3) Stack bands that will be used in visual interpretation.
    4) Create pyramid of the raster.
    5) Classify cloud and shadow from raster with fmask algorithm.
    6) Segment satellite image.
    7) Load segmentation to draft database.
    8) Create image server
