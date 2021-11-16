'''
Generate new data for testing
'''

from pathlib import Path
import numpy as np
import rasterio
from rasterio.merge import merge
from osgeo import gdal
from affine import Affine


base_path = Path('data')


tiles_path = base_path / 'tiles'
tiles_path.mkdir(parents=True, exist_ok=True)

# define individual tiles/scenes bounds/size/transform
resolution = 0.5

# define number of tiles (square this number)
tile_sqrt = 2

bounds_list = []
for i in range(tile_sqrt):
    xmin = i * (360 / tile_sqrt) - 180
    xmax = (i + 1) * (360 / tile_sqrt) - 180
    for j in range(tile_sqrt):
        ymin = j * (180 / tile_sqrt) - 90
        ymax = (j + 1) * (180 / tile_sqrt) - 90
        bounds_list.append((xmin, ymin, xmax, ymax))
# xmin, ymin, xmax, ymax

transform_list = [ Affine(resolution, 0, i[0], 0, -resolution, i[3]) for i in bounds_list ]

dims_list = [rasterio.transform.rowcol(transform_list[i], bounds_list[i][2], bounds_list[i][1]) for i in range(len(transform_list)) ]

# generate data for each tile
# save each tile as geotiff

tile_list = []
for i, (transform, dims) in enumerate(zip(transform_list, dims_list)):
    # create empty raster
    out_img = np.random.random(size=dims)
    out_meta = {
        'driver': 'GTiff',
        'height': dims[0],
        'width': dims[1],
        'transform': transform,
        'crs': 'epsg:4326',
        'dtype': 'float64',
        'count': 1,
        'nodata': 0
    }
    out_path = tiles_path / f'tile_{i}.tif'
    tile_list.append(str(out_path))
    with rasterio.open(out_path, 'w', **out_meta) as dst:
        dst.write(out_img, 1)

# -------------------------------------


# generate vrt
# vrt_options = gdal.BuildVRTOptions(resampleAlg='cubic', addAlpha=False)
vrt_path = base_path / 'test_vrt.vrt'
my_vrt = gdal.BuildVRT(str(vrt_path), tile_list)#, options=vrt_options)
my_vrt = None


# -------------------------------------


# generate mosaiced geotiff
bounds =(min([i[0] for i in bounds_list]), min([i[1] for i in bounds_list]), max([i[2] for i in bounds_list]), max([i[3] for i in bounds_list]))
sources = [rasterio.open(raster) for raster in tile_list]
mosaic, out_transform = merge(sources, bounds=bounds)
out_meta = sources[0].meta.copy()
out_meta.update(
    {
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_transform
    }
)
mosaic_path = base_path / 'test_mosaic.tif'
with rasterio.open(str(mosaic_path), "w", **out_meta) as dst:
    dst.write(mosaic)
