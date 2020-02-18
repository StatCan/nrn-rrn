import fiona
import geopandas as gpd
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], ".."))
import helpers

dframes = helpers.load_gpkg("../../data/interim/nb.gpkg")