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


def enum(*names):
    enums = dict(zip(names, range(len(names))))
    return type('Enum', (), enums)


Which = enum('VERTEX', 'CELL', 'BOTH')


def xdmf_args_to_shp(args):
    """Uses a argparse.Namespace object
    :param args: the argparse.Namespace object
    """
    if not (Which.VERTEX <= args.which <= Which.BOTH):
        raise ValueError("args.which should be 0, 1, or 2")
    if (args.which == Which.BOTH and len(args.outputs) < 2)\
            or (Which.VERTEX <= args.which <= Which.CELL and len(args.outputs) < 1):
        raise ValueError("Not enough names for output files")

    base = tuple(args.base)

    unstr = UnstructuredData()
    ReadHdf5Posix(args, unstr)
    my_data = unstr.myData[args.idt].flatten()

    # Set up the shapefile driver
    shp_driver = ogr.GetDriverByName("ESRI Shapefile")
    # Create the spatial reference, WGS84
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(args.epsg)

    xyz = unstr.xyz  # collapsed_mesh.vertices
    connect = unstr.connect  # collapsed_mesh.faces

    # For points - vertices
    if args.which != Which.CELL:
        # Create the data source
        point_ds = shp_driver.CreateDataSource(args.outputs[0])
        # Create the layer
        point_layer = point_ds.CreateLayer("vertices", srs, ogr.wkbPoint)
        # Add the fields we're interested in
        point_layer.CreateField(ogr.FieldDefn("X", ogr.OFTReal))
        point_layer.CreateField(ogr.FieldDefn("Y", ogr.OFTReal))

        # Process the unstructured data and add the attributes and features to the shapefile
        for vertex in xyz:
            coord = vertex * args.scale + base
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
    if args.which != Which.VERTEX:
        cell_shp = args.outputs[0] if args.which == 1 else args.outputs[1]
        triangle_ds = shp_driver.CreateDataSource(cell_shp)
        triangle_layer = triangle_ds.CreateLayer("cells", srs, ogr.wkbTriangle)
        triangle_layer.CreateField(ogr.FieldDefn("Data", ogr.OFTReal))

        for idx, cell in enumerate(connect):
            xyz_a, xyz_b, xyz_c = xyz[cell[0]], xyz[cell[1]], xyz[cell[2]]
            coord_a = xyz_a * args.scale + base
            coord_b = xyz_b * args.scale + base
            coord_c = xyz_c * args.scale + base
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


def xdmf_to_shp(input_file, data, idt, output_files=None, epsg=3857, which=Which.CELL, base=(0, 0, 0), scale=1):
    """Converts xdmf to shapefile
    :param input_file: Fault output file name (xdmf), or TODO, maybe: SeisSol netcdf (nc) or ts (Gocad)
    :param data: Data to visualize (example SRs)
    :param idt: The time step to visualize, stored in a list (1st = 0);
    -1 = all is supported by DataLoader but will give wrong results here
    :param output_files: The list of output shapefiles
    :param epsg: EPSG code of the layer
    :param which: Extract data of vertices (0), cells (1), or both (2)
    :param base: (base_x, base_y, base_z) position of the layer
    :param scale: scale of the layer
    """
    if output_files is None:
        if which == Which.BOTH:
            output_files = ['output0.shp', 'output1.shp']
        else:
            output_files = ['output.shp']
    args = Namespace(filename=input_file, Data=data, idt=idt, oneDtMem=False, restart=[0],
                     outputs=output_files, epsg=epsg, which=which, base=base, scale=scale)
    xdmf_args_to_shp(args)


if __name__ == '__main__':
    parser = ArgumentParser(description='Convert xdmf to shapefile')
    parser.add_argument('filename', help='fault output filename (xdmf)')
    parser.add_argument('Data', nargs=1, metavar='data_name', default='', help='Data to visualize (example SRs)')
    parser.add_argument('idt', nargs=1, help='time step to extract (1st = 0)', type=int)
    parser.add_argument('--oneDtMem', dest='oneDtMem', action='store_true', default=False,
                        help='store only the dt to be displayed in RAM')
    parser.add_argument('--restart', nargs=1, metavar='idt', help='in case of a restart at time frame idt, \
                        some postprocessing is necessary on Vr: Vr[n+idt] = Vr[n] + Vr[idt]', type=int, default=[0])
    parser.add_argument('--outputs', help='output shapefiles', nargs='*', default=['cells.shp'])
    parser.add_argument('--epsg', help='EPSG code of the layer', type=int, default=3857)
    parser.add_argument('--which', help='extract vertice data (0) or cell data (1) or both (2)',
                        type=int, choices=[0, 1, 2], default=Which.CELL)
    parser.add_argument('--base', help='base_x, base_y, base_z position of the layer', nargs=3,
                        type=float, default=[0, 0, 0])
    parser.add_argument('--scale', help='scale of the layer', type=int, default=1)
    args = parser.parse_args()
    # args = Namespace(filename='../../data/data-surface.xdmf',
    #                  Data=['v3d'], idt=[160], oneDtMem=False, restart=[0],
    #                  outputs=["../../data/seis_cells.shp"],
    #                  epsg=3857, which=Which.CELL, base=[11.588271 * 100000, 47.751307 * 125000, 0], scale=10)
    # args = Namespace(filename='../../data/sumatra-surface.xdmf',
    #                  Data=['V'], idt=[50], oneDtMem=False, restart=[0],
    #                  outputs=['../../data/sumatra_cells.shp'],
    #                  epsg=32646, which=Which.CELL, base=[0, 0, 0], scale=1)
    xdmf_args_to_shp(args)
    # xdmf_to_shp(input_file='../../data/sumatra-surface.xdmf',
    #             data=['V'], idt=[50],
    #             output_files=['../../data/sumatra_cells.shp'],
    #             epsg=32646, which=Which.CELL)
