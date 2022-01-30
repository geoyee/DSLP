import numpy as np
import operator
from functools import reduce


def rasterToUint8(image: np.ndarray) -> np.ndarray:
    """ Convert raster to uint8.
    Args:
        image (np.ndarray): image.
    Returns:
        np.ndarray: image on uint8.
    """
    dtype = image.dtype.name
    dtypes = ["uint8", "uint16", "float32"]
    if dtype not in dtypes:
        raise ValueError(f"'dtype' must be uint8/uint16/float32, not {dtype}.")
    if dtype == "uint8":
        return image
    else:
        if dtype == "float32":
            image = _sampleNorm(image)
        return _twoPercentLinear(image)


# 2% linear stretch
def _twoPercentLinear(image: np.ndarray, max_out: int=255, min_out: int=0) -> np.ndarray:
    def _gray_process(gray, maxout=max_out, minout=min_out):
        # Get the corresponding gray level at 98% histogram
        high_value = np.percentile(gray, 98)
        low_value = np.percentile(gray, 2)
        truncated_gray = np.clip(gray, a_min=low_value, a_max=high_value)
        processed_gray = ((truncated_gray - low_value) / (high_value - low_value)) * (maxout - minout)
        return processed_gray
    if len(image.shape) == 3:
        processes = []
        for b in range(image.shape[-1]):
            processes.append(_gray_process(image[:, :, b]))
        result = np.stack(processes, axis=2)
    else:  # if len(image.shape) == 2
        result = _gray_process(image)
    return np.uint8(result)


# Simple image standardization
def _sampleNorm(image: np.ndarray, NUMS: int=65536) -> np.ndarray:
    stretches = []
    if len(image.shape) == 3:
        for b in range(image.shape[-1]):
            stretched = _stretch(image[:, :, b], NUMS)
            stretched /= float(NUMS)
            stretches.append(stretched)
        stretched_img = np.stack(stretches, axis=2)
    else:  # if len(image.shape) == 2
        stretched_img = _stretch(image, NUMS)
    return np.uint8(stretched_img * 255)


# Histogram equalization
def _stretch(ima: np.ndarray, NUMS: int) -> np.ndarray:
    hist = _histogram(ima, NUMS)
    lut = []
    for bt in range(0, len(hist), NUMS):
        # Step size
        step = reduce(operator.add, hist[bt : bt + NUMS]) / (NUMS - 1)
        # Create balanced lookup table
        n = 0
        for i in range(NUMS):
            lut.append(n / step)
            n += hist[i + bt]
        np.take(lut, ima, out=ima)
        return ima


# Calculate histogram
def _histogram(ima: np.ndarray, NUMS: int) -> np.ndarray:
    bins = list(range(0, NUMS))
    flat = ima.flat
    n = np.searchsorted(np.sort(flat), bins)
    n = np.concatenate([n, [len(flat)]])
    hist = n[1:] - n[:-1]
    return hist