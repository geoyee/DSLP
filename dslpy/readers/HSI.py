import os.path as osp
import numpy as np
from typing import List, Tuple, Union
from dslpy.utils import rasterToUint8

try:
    from osgeo import gdal
except ImportError:
    import gdal


def readHSI(img_path: str, 
            band_list: Union[List, Tuple, None]=None, 
            to_uint8: bool=True) -> np.ndarray:
    if not osp.exists(img_path):
        raise ValueError("The {} does not exist.".format(img_path))
    img = gdal.Open(img_path)
    img_data = img.ReadAsArray().transpose((1, 2, 0))
    if isinstance(band_list, (List, Tuple)):
        if max(band_list) >= img.RasterCount or min(band_list) < 0:
            raise IndexError("This band list is not available.")
        img_res = []
        for b in band_list:
            img_res.append(img_data[..., int(b)])
        img_res = np.stack(img_res, axis=2)
    else:
        img_res = img_data
    if to_uint8 and img_res.shape[-1] == 3:
        img_res = rasterToUint8(img_res, img_res.dtype.name)
    return img_res