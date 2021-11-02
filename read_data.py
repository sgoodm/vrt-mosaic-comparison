'''
Read data from VRT and mosaiced GeoTIFF
'''


from pathlib import Path
from random import randint
import atexit
import rasterio
from rasterio.merge import merge
from rasterio.vrt import WarpedVRT
from rasterio.windows import from_bounds
import line_profiler

# Start a profiler
profile = line_profiler.LineProfiler()
atexit.register(profile.print_stats)


base_path = Path('data')
vrt_path = base_path / 'test_vrt.vrt'
mosaic_path = base_path / 'test_mosaic.tif'

##################
# define series of windows/points/etc to read
windows = []

# TODO: grab the dimensions of the VRT itself and use that
for i in range(100):
    window_width = randint(1, 180)
    window_height = randint(1, 90)

    window_x = randint(-180, 180 - window_width)
    window_y = randint(-90, 90 - window_height)

    """
    # bounds of this window
    # left, bottom, right, top
    window_bnds = (left, bottom, right, top)

    windows.append(rasterio.windows.from_bounds(*window_bnds))
    """

#################

# read data from VRT

@profile
def fromVRT(bounds_or_window):
    with rasterio.Env():
        with rasterio.open(vrt_path) as src:
            with WarpedVRT(src) as vrt:
                r = vrt.read(1, window=win)



# read data from mosaiced GeoTIFF

@profile
def fromMosaic(bounds_or_window):
    with rasterio.Env():
        with rasterio.open(mosaic_path) as src:
            r = src.read(1, window=win)

