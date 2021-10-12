'''
Read data from VRT and mosaiced GeoTIFF
'''


from pathlib import Path
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


# define series of windows/points/etc to read
#


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

