from pathlib import Path
from gen_data import generate_all
from read_data import time_reads

# Set variables
base_path = Path("data")
num_of_windows = 10000
vrt_path = base_path / "test_vrt.vrt"
mosaic_path = base_path / "test_mosaic.tif"

# Generate data
generate_all(base_path = base_path, resolution = 0.5, tile_sqrt = 4)

# Time reads
vrt_tpr, mosaic_tpr = time_reads(num_of_windows, vrt_path, mosaic_path)

# Print results
print("vrt average time to read:")
print(vrt_tpr)
print("mosaic average time to read:")
print(mosaic_tpr)
