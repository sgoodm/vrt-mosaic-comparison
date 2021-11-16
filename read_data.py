"""
Read data from VRT and mosaiced GeoTIFF
"""

from pathlib import Path
from random import randint
import atexit
import rasterio
from rasterio.merge import merge
from rasterio.vrt import WarpedVRT
from rasterio.windows import from_bounds
from line_profiler import LineProfiler

# These are the functions we will profile
from vrt_read import read_vrt
from mosaic_read import read_mosaic

"""
Variables!
"""
num_of_windows = 10000
base_path = Path("data")
vrt_path = base_path / "test_vrt.vrt"
mosaic_path = base_path / "test_mosaic.tif"

"""
Start a profiler
"""
lp = LineProfiler(read_mosaic, read_vrt)
mosaic_lp = lp(read_mosaic)
vrt_lp = lp(read_vrt)

def gen_windows(transform) -> list:
    """
    Generates a list of windows to read
    """
    windows = []

    # TODO: grab the dimensions of the VRT itself and use that

    for i in range(num_of_windows):
        window_width = randint(1, 180)
        window_height = randint(1, 90)

        window_x = randint(-180, 180 - window_width)
        window_y = randint(-90, 90 - window_height)

        window_bnds = (
            window_x,  # left
            window_y,  # bottom
            window_x + window_width,  # right
            window_y + window_height,  # top
        )

        windows.append(from_bounds(*window_bnds, transform))
    return windows


# run functions from within a rasterio environment
with rasterio.Env():
    with rasterio.open(vrt_path) as vrt_src:
        with WarpedVRT(vrt_src) as vrt, rasterio.open(mosaic_path) as mosaic:
            # Get transforms for both VRT and mosaic
            vrt_transform = vrt.transform
            mosaic_transform = mosaic.transform
            # Make sure they are the same
            assert vrt_transform == mosaic_transform
            # Now let's generate some windows and iterate through them
            for window in gen_windows(vrt_transform):
                vrt_lp(vrt, window)
                mosaic_lp(vrt, window)


# extract timing information from LineProfiler
lp_timings = lp.get_stats().timings
for timing_key in lp_timings:
    if timing_key[2] == "read_mosaic":
        mosaic_timing = lp_timings[timing_key][0]
    elif timing_key[2] == "read_vrt":
        vrt_timing = lp_timings[timing_key][0]

# double check we ran each function as many times as we planned
assert mosaic_timing[1] == vrt_timing[1] == num_of_windows

print("vrt time per read:")
print(vrt_timing[2] / vrt_timing[1])
print("mosaic time per read:")
print(mosaic_timing[2] / mosaic_timing[1])
