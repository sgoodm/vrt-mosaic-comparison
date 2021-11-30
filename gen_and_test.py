from pathlib import Path
from gen_data import generate_all
from read_data import time_reads
import statistics
import pandas as pd
import plotly.express as px

# Set variables
base_path = Path("data")
num_of_windows = 300
vrt_path = base_path / "test_vrt.vrt"
mosaic_path = base_path / "test_mosaic.tif"
resolutions = [1, 0.5, 0.25]
tile_sqrts = [2, 4, 6, 8, 10]
repeats = 15

# Create dataframe to store read times
times_df = pd.DataFrame(columns=["res", "sqrt", "time", "type"])

# Time reads
# TODO: Control the block size for each?
for i, res in enumerate(resolutions):
    for j, sqrt in enumerate(tile_sqrts):
        # generate data for this round of tests
        generate_all(base_path=base_path, resolution=res, tile_sqrt=sqrt)
        vrt_times, mosaic_times = ([], [])
        # Measure read times for this data
        for _ in range(repeats):
            try:
                vrt_tpr, mosaic_tpr = time_reads(num_of_windows, vrt_path, mosaic_path)
            except AssertionError:
                print(f"{str(sqrt)}, {str(res)}")
            vrt_times.append(vrt_tpr)
            mosaic_times.append(mosaic_tpr)
        # Append results to dataframe
        times_df = times_df.append(
            {
                "res": res,
                "sqrt": sqrt,
                "time": statistics.median(vrt_times),
                "type": "VRT",
            },
            ignore_index=True,
        )
        times_df = times_df.append(
            {
                "res": res,
                "sqrt": sqrt,
                "time": statistics.median(mosaic_times),
                "type": "Mosaic",
            },
            ignore_index=True,
        )

# Generate an interactive 3D plot with plotly
fig = px.scatter_3d(times_df, x="sqrt", y="res", z="time", color="type")
fig.show()
