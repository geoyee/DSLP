import os.path as osp
import numpy as np
from dslpy.utils import rasterToUint8

try:
    from osgeo import gdal
except ImportError:
    import gdal


def readRGB(img_path: str, to_uint8: bool=True) -> np.ndarray:
    if not osp.exists(img_path):
        raise ValueError("The {} does not exist.".format(img_path))
    img = gdal.Open(img_path)
    if img.RasterCount != 3:
        raise ValueError("This file is not a RGB data.")
    img_data = img.ReadAsArray().transpose((1, 2, 0))
    if to_uint8:
        img_data = rasterToUint8(img_data, img_data.dtype.name)
    return img_data