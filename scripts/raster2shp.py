# FIXME: Need fix
import os
import os.path as osp
import numpy as np

try:
    from osgeo import gdal, ogr, osr
except ImportError:
    import gdal
    import ogr
    import osr


def __mask2tif(mask, tmp_path, proj, geot):
    row, columns = mask.shape[:2]
    driver = gdal.GetDriverByName("GTiff")
    dst_ds = driver.Create(tmp_path, columns, row, 1, gdal.GDT_UInt16)
    dst_ds.SetGeoTransform(geot)
    dst_ds.SetProjection(proj)
    dst_ds.GetRasterBand(1).WriteArray(mask)
    dst_ds.FlushCache()
    return dst_ds


def polygonize_raster(mask, shp_save_path, proj, geot, rm_tmp=True):
    if type(mask) is np.ndarray:
        tmp_path = shp_save_path.replace(".shp", ".tif")
        ds = __mask2tif(mask, tmp_path, proj, geot)
    else:
        tmp_path = mask.file_name
        ds = mask.gdal_data
    srcband = ds.GetRasterBand(1)
    maskband = srcband.GetMaskBand()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF-8")
    ogr.RegisterAll()
    drv = ogr.GetDriverByName("ESRI Shapefile")
    if osp.exists(shp_save_path):
        os.remove(shp_save_path)
    dst_ds = drv.CreateDataSource(shp_save_path)
    prosrs = osr.SpatialReference(wkt=ds.GetProjection())
    # print("proj_1: ", prosrs)  # test
    # ESPGValue = prosrs.GetAttrValue("AUTHORITY", 1)
    # sr = osr.SpatialReference()
    # sr.ImportFromEPSG(int(ESPGValue))
    # print("proj_2:", sr)  # test
    dst_layer = dst_ds.CreateLayer("Building boundary", geom_type=ogr.wkbPolygon, srs=prosrs)
    dst_fieldname = "DN"
    fd = ogr.FieldDefn(dst_fieldname, ogr.OFTInteger)
    dst_layer.CreateField(fd)
    gdal.Polygonize(srcband, maskband, dst_layer, 0, [])
    lyr = dst_ds.GetLayer()
    lyr.SetAttributeFilter("DN = '0'")
    for holes in lyr:
        lyr.DeleteFeature(holes.GetFID())
    dst_ds.Destroy()
    ds = None
    if rm_tmp:
        mask.close()
        os.remove(tmp_path)


if __name__ == "__main__":
    import numpy as np
    from PIL import Image
    ras_path = r"C:\Users\Geoyee\Desktop\dd\ras.tif"
    shp_save_path = r"C:\Users\Geoyee\Desktop\dd\shp_2.shp"
    mask = np.asarray(Image.open(ras_path).convert("P"))
    ras_ds = gdal.Open(ras_path)
    geot = ras_ds.GetGeoTransform()
    proj = ras_ds.GetProjection()
    polygonize_raster(mask, shp_save_path, proj, geot, display=False)