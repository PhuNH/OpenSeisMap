#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 09:38:22 2019

@author: phunh
"""
from argparse import Namespace, ArgumentParser
from osgeo import ogr, osr
from UnstructuredData import UnstructuredData
from DataLoader import ReadHdf5Posix


def xdmf_args_to_shp(args, output_files, which, base, scale):
    """Uses a argparse.Namespace object
    :param args: the argparse.Namespace object
    :param output_files: see xdmf_to_shp
    :param which: see xdmf_to_shp
    :param base: see xdmf_to_shp
    :param scale: see xdmf_to_shp
    """
    if ((which < 0 or which > 1) and len(output_files) < 2) or (0 <= which <= 1 and len(output_files) < 1):
        raise ValueError("Not enough names for output files")

    unstr = UnstructuredData()
    ReadHdf5Posix(args, unstr)
    my_data = unstr.myData[args.idt].flatten()

    # Set up the shapefile driver
    shp_driver = ogr.GetDriverByName("ESRI Shapefile")
    # Create the spatial reference, WGS84
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(32646)  # a PCS, so no lat-lon, only meter

    # For points - vertices
    if which != 1:
        # Create the data source
        point_ds = shp_driver.CreateDataSource(output_files[0])
        # Create the layer
        point_layer = point_ds.CreateLayer("seis_vertices", srs, ogr.wkbPoint)
        # Add the fields we're interested in
        point_layer.CreateField(ogr.FieldDefn("X", ogr.OFTReal))
        point_layer.CreateField(ogr.FieldDefn("Y", ogr.OFTReal))

        # Process the unstructured data and add the attributes and features to the shapefile
        for vertex in unstr.xyz:
            coord = vertex * scale + base
            # Create the feature
            v_feature = ogr.Feature(point_layer.GetLayerDefn())
            # Set the attributes using the values from the unstructured data
            v_feature.SetField("X", coord[0])
            v_feature.SetField("Y", coord[1])

            # this
#            # Create the WKT for the feature using Python string formatting
#            wkt = "POINT(%f %f)" % (coord[0], coord[1])
#            # Create the point from the Well Known Txt
#            point = ogr.CreateGeometryFromWkt(wkt)
            # or this
            point = ogr.Geometry(ogr.wkbPoint)
            point.AddPoint(coord[0], coord[1])

            # Set the feature geometry using the point
            v_feature.SetGeometry(point)
            # Create the feature in the layer (shapefile)
            point_layer.CreateFeature(v_feature)
            # Dereference the feature
            v_feature = None

    # For triangles - cells
    if which != 0:
        cell_shp = output_files[0] if which == 1 else output_files[1]
        triangle_ds = shp_driver.CreateDataSource(cell_shp)
        triangle_layer = triangle_ds.CreateLayer("seis_cells", srs, ogr.wkbTriangle)
        triangle_layer.CreateField(ogr.FieldDefn("Data", ogr.OFTReal))

        for idx, cell in enumerate(unstr.connect):
            xyz_a, xyz_b, xyz_c = unstr.xyz[cell[0]], unstr.xyz[cell[1]], unstr.xyz[cell[2]]
            coord_a = xyz_a * scale + base
            coord_b = xyz_b * scale + base
            coord_c = xyz_c * scale + base
            c_feature = ogr.Feature(triangle_layer.GetLayerDefn())
            c_feature.SetField("Data", my_data[idx])

            # this
#            wkt = "TRIANGLE((%f %f, %f %f, %f %f, %f %f))" % (coord_a[0], coord_a[1], coord_b[0], coord_b[1],
#                                                              coord_c[0], coord_c[1], coord_a[0], coord_a[1])
#            triangle = ogr.CreateGeometryFromWkt(wkt)
            # or this
            # Create ring
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(coord_a[0], coord_a[1])
            ring.AddPoint(coord_b[0], coord_b[1])
            ring.AddPoint(coord_c[0], coord_c[1])
            ring.AddPoint(coord_a[0], coord_a[1])
            # Create triangle
            triangle = ogr.Geometry(ogr.wkbTriangle)
            triangle.AddGeometry(ring)

            c_feature.SetGeometry(triangle)
            triangle_layer.CreateFeature(c_feature)
            c_feature = None

    # Save and close the data source
    point_ds = None
    triangle_ds = None


def xdmf_to_shp(input_file, data, idt, output_files, which=2, base=(0, 0, 0), scale=50):
    """Converts xdmf to shapefile
    :param input_file: Fault output file name (xdmf), or TODO, maybe: SeisSol netcdf (nc) or ts (Gocad)
    :param data: Data to visualize (example SRs)
    :param idt: The time step to visualize, stored in a list (1st = 0);
    -1 = all is supported by DataLoader but will give wrong results here
    :param output_files: The list of output shapefiles
    :param which: Output shapefile for vertices (0), cells (1), or both (others)
    :param base: (base_x, base_y, base_z) position of the layer
    :param scale: scale of the layer
    """
    args = Namespace(Data=[data], filename=input_file, idt=idt, oneDtMem=False, restart=[0])
    xdmf_args_to_shp(args, output_files, which, base, scale)


if __name__ == '__main__':
    parser = ArgumentParser(description='Read hdf5 fault output')
    parser.add_argument('filename', help='fault output filename (xdmf)')
    parser.add_argument('--Data', nargs=1, metavar='variable', default='', help='Data to visualize (example SRs)')
    parser.add_argument('--idt', nargs='+', help='list of time step to visualize (1st = 0); -1 = all', type=int)
    parser.add_argument('--oneDtMem', dest='oneDtMem', action='store_true', default=False,
                        help='store only the dt to be displayed in RAM')
    parser.add_argument('--restart', nargs=1, metavar='idt', help='in case of a restart at time frame idt, \
                        some postprocessing is necessary on Vr: Vr[n+idt] = Vr[n] + Vr[idt]', type=int, default=[0])
    # args = parser.parse_args()
    xdmf_args_to_shp(Namespace(Data=['v'], filename='../../data/sumatra-surface.xdmf', idt=[50], oneDtMem=False, restart=[0]),  # args
                     output_files=["../../data/sumatra_cells.shp"],
                     which=1,
                     base=(0 * 100000, 0 * 125000, 0),
                     scale=1)
