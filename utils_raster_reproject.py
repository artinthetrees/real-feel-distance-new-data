# https://rasterio.readthedocs.io/en/stable/topics/reproject.html

import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling


def rasterio_convert_crs_file_to_file(src_file_path, dst_file_path, dst_crs = 'EPSG:4326'):

    with rasterio.open(src_file_path) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        with rasterio.open(dst_file_path, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest)
            

rasterio_convert_crs_file_to_file(src_file_path="./downloads/cog-year2021-month7-day15-hour10-minute0-MRT-mask.tif",dst_file_path="./downloads/crs-converted-cog-year2021-month7-day15-hour10-minute0-MRT-mask.tif")

with rasterio.open("./downloads/crs-converted-cog-year2021-month7-day15-hour10-minute0-MRT-mask.tif") as src:
    print(src.crs)
    