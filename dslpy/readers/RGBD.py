import os.path as osp
import numpy as np
from dslpy.utils import rasterToUint8

try:
    from osgeo import gdal
except ImportError:
    import gdal


# TODO: Test
def readRGBD(img_path: str, to_uint8: bool=True) -> np.ndarray:
    if not osp.exists(img_path):
        raise ValueError("The {} does not exist.".format(img_path))
    img = gdal.Open(img_path)
    if img.RasterCount != 4:
        raise ValueError("This file is not a RGBD data.")
    img_data = img.ReadAsArray().transpose((1, 2, 0))
    if to_uint8:
        rgb = img_data[:, :, :3]
        rgb = rasterToUint8(rgb, img_data.dtype.name)
        img_data[:, :, :3] = rgb
    return img_data