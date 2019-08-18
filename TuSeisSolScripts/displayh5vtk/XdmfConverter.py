#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 09:38:22 2019

@author: phunh
"""
import os
from argparse import Namespace, ArgumentParser
from osgeo import ogr, osr
import json
from UnstructuredData import UnstructuredData
from DataLoader import ReadHdf5Posix
from UnstructuredDataVtkSupport import unstr_to_poly_data, clean, decimate, poly_data_to_unstr, map_cell_attribute
import GeoFunctions


# def enum(*names):
#     enums = dict(zip(names, range(len(names))))
#     return type('Enum', (), enums)
#
#
# Which = enum('VERTEX', 'CELL', 'BOTH')


def make_json(shapefile, min_zoom, max_zoom):
    cells_ds = GeoFunctions.open_shapefile(shapefile)
    cells_layer = cells_ds.GetLayerByIndex(0)
    my_data = []
    cells_layer.ResetReading()
    for cell_feature in cells_layer:
        my_data.append(cell_feature.GetFieldAsDouble(0))
    min_data = min(my_data)
    max_data = max(my_data)
    min_x, max_x, min_y, max_y = cells_layer.GetExtent()

    min_lon = None
    min_lat = None
    max_lon = None
    max_lat = None
    srs = GeoFunctions.get_shapefile_srs_from_ds(cells_ds)
    lonlat = osr.SpatialReference()
    lonlat.ImportFromEPSG(4326)
    transform = osr.CoordinateTransformation(srs, lonlat)
    min_point = ogr.CreateGeometryFromWkt("POINT (" + str(min_x) + " " + str(min_y) + ")")
    min_point.Transform(transform)
    for ip in range(min_point.GetPointCount()):
        min_lon, min_lat, _ = min_point.GetPoint(ip)
    max_point = ogr.CreateGeometryFromWkt("POINT (" + str(max_x) + " " + str(max_y) + ")")
    max_point.Transform(transform)
    for ip in range(max_point.GetPointCount()):
        max_lon, max_lat, _ = max_point.GetPoint(ip)
    # print(min_data, max_data, min_lon, max_lon, min_lat, max_lat)

    path_name, ext = os.path.splitext(shapefile)
    name = os.path.basename(path_name)
    obj = {"sites": []}
    obj["sites"].append({
        "name": name,
        "minLon": min_lon,
        "minLat": min_lat,
        "maxLon": max_lon,
        "maxLat": max_lat,
        "minVal": min_data,
        "maxVal": max_data,
        "minZoom": min_zoom,
        "maxZoom": max_zoom
    })

    json_path_name = path_name + '.json'
    f = open(json_path_name, "w+")
    f.write(json.dumps(obj, indent=4))
    f.close()
    print("json file written")
    # with open(json_path_name, 'w+') as outfile:
    #     json.dump(obj, outfile)


def xdmf_args_to_shp(args):
    """Uses a argparse.Namespace object
    :param args: a argparse.Namespace object
    """
    # if not (Which.VERTEX <= args.which <= Which.BOTH):
    #     raise ValueError("which should be 0, 1, or 2")
    # if (args.which == Which.BOTH and len(args.outputs) < 2)\
    #         or (Which.VERTEX <= args.which <= Which.CELL and len(args.outputs) < 1):
    #     raise ValueError("Not enough names for output files")
    if not (0 <= args.reduction < 1):
        raise ValueError("reduction should be in the [0, 1) interval")

    base = tuple(args.base)

    unstr = UnstructuredData()
    ReadHdf5Posix(args, unstr)
    my_data = unstr.myData[args.idt].flatten()

    # Set up the shapefile driver
    shp_driver = ogr.GetDriverByName("ESRI Shapefile")
    # Create the spatial reference, WGS84
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(args.epsg)

    def create_cell_layer_shp(file_name, xyz, connect, attr):
        triangle_ds = shp_driver.CreateDataSource(file_name)
        triangle_layer = triangle_ds.CreateLayer("cells", srs, ogr.wkbTriangle)
        triangle_layer.CreateField(ogr.FieldDefn("Data", ogr.OFTReal))

        for idx, cell in enumerate(connect):
            coord_a, coord_b, coord_c = xyz[cell] * args.scale + base
            # this
            # wkt = "TRIANGLE((%f %f, %f %f, %f %f, %f %f))" % (coord_a[0], coord_a[1], coord_b[0], coord_b[1],
            #                                                  coord_c[0], coord_c[1], coord_a[0], coord_a[1])
            # triangle = ogr.CreateGeometryFromWkt(wkt)
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

            c_feature = ogr.Feature(triangle_layer.GetLayerDefn())
            c_feature.SetField("Data", attr[idx])
            c_feature.SetGeometry(triangle)
            triangle_layer.CreateFeature(c_feature)
            c_feature = None

        # Save and close the data source
        triangle_ds = None

    # Create multiple shapefiles, each for one zoom level
    if args.reduction > 0:
        # For points - vertices
        # if args.which != Which.CELL:
        #     # Create the data source
        #     point_ds = shp_driver.CreateDataSource(args.outputs[0])
        #     # Create the layer
        #     point_layer = point_ds.CreateLayer("vertices", srs, ogr.wkbPoint)
        #     # Add the fields we're interested in
        #     point_layer.CreateField(ogr.FieldDefn("X", ogr.OFTReal))
        #     point_layer.CreateField(ogr.FieldDefn("Y", ogr.OFTReal))
        #
        #     # Process the unstructured data and add the attributes and features to the shapefile
        #     for vertex in xyz:
        #         coord = vertex * args.scale + base
        #         # Create the feature
        #         v_feature = ogr.Feature(point_layer.GetLayerDefn())
        #         # Set the attributes using the values from the unstructured data
        #         v_feature.SetField("X", coord[0])
        #         v_feature.SetField("Y", coord[1])
        #
        #         # this
        #         # # Create the WKT for the feature using Python string formatting
        #         # wkt = "POINT(%f %f)" % (coord[0], coord[1])
        #         # # Create the point from the Well Known Txt
        #         # point = ogr.CreateGeometryFromWkt(wkt)
        #         # or this
        #         point = ogr.Geometry(ogr.wkbPoint)
        #         point.AddPoint(coord[0], coord[1])
        #
        #         # Set the feature geometry using the point
        #         v_feature.SetGeometry(point)
        #         # Create the feature in the layer (shapefile)
        #         point_layer.CreateFeature(v_feature)
        #         # Dereference the feature
        #         v_feature = None
        #     # Save and close the data source
        #     point_ds = None

        # For triangles - cells
        # if args.which != Which.VERTEX:
        cell_shp, ext = os.path.splitext(args.outputs[0])  # if args.which == 1 else args.outputs[1]

        xyz_lvl = unstr.xyz
        connect_lvl = unstr.connect
        attr_lvl = my_data
        poly_data_lvl = unstr_to_poly_data(xyz_lvl, connect_lvl, attr_lvl)
        if args.needs_cleaning:
            poly_data_lvl = clean(poly_data_lvl)
            xyz_lvl, connect_lvl, _ = poly_data_to_unstr(poly_data_lvl)
        
        cell_shp_lvl = cell_shp + '_' + str(args.maxzoom//2) + ext
        create_cell_layer_shp(cell_shp_lvl, xyz_lvl, connect_lvl, attr_lvl)
        make_json(cell_shp_lvl, args.minzoom, args.maxzoom)

        for i in range(args.maxzoom//2-1, args.minzoom//2-1, -1):
            poly_data_lvl = decimate(poly_data_lvl, args.reduction, len(xyz_lvl) >= 1000000)
            xyz_lvl, connect_lvl, attr_lvl = map_cell_attribute(xyz_lvl, connect_lvl, attr_lvl, poly_data_lvl)
            cell_shp_lvl = cell_shp + '_' + str(i) + ext
            create_cell_layer_shp(cell_shp_lvl, xyz_lvl, connect_lvl, attr_lvl)
    else:  # args.reduction == 0: create only 1 shapefile for all zoom levels
        cell_shp = args.outputs[0]
        create_cell_layer_shp(cell_shp, unstr.xyz, unstr.connect, my_data)
        make_json(cell_shp, args.minzoom, args.maxzoom)


def xdmf_to_shp(input_file, data, idt, output_files=None, epsg=3857, max_zoom=10, min_zoom=0, reduction=0.5,
                base=(0, 0, 0), scale=1, needs_cleaning=False):
    """Converts xdmf to shapefile
    :param input_file: Fault output file name (xdmf), or TODO, maybe: SeisSol netcdf (nc) or ts (Gocad)
    :param data: Data to visualize (example SRs)
    :param idt: The time step to visualize, stored in a list (1st = 0);
    -1 = all is supported by DataLoader but will give wrong results here
    :param output_files: The list of output shapefiles
    :param epsg: EPSG code of the layer
    :param max_zoom: Max zoom level for the dataset
    :param min_zoom: Min zoom level for the dataset
    :param reduction: Empirical target reduction for each zoom level
    :param base: (base_x, base_y, base_z) position of the dataset
    :param scale: Scale of the dataset
    :param needs_cleaning: Whether the data needs cleaning for the first decimation
    """
    if output_files is None:
        # if which == Which.BOTH:
        #     output_files = ['output0.shp', 'output1.shp']
        # else:
        output_files = ['output.shp']
    args = Namespace(filename=input_file, Data=data, idt=idt, oneDtMem=False, restart=[0],
                     outputs=output_files, epsg=epsg, maxzoom=max_zoom, minzoom=min_zoom, reduction=reduction,
                     base=base, scale=scale, needs_cleaning=needs_cleaning)
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
    # parser.add_argument('--which', help='extract vertice data (0) or cell data (1) or both (2)',
    #                     type=int, choices=[0, 1, 2], default=Which.CELL)
    parser.add_argument('--maxzoom', help='max zoom level for this dataset', type=int, default=10)
    parser.add_argument('--minzoom', help='min zoom level for this dataset', type=int, default=0)
    parser.add_argument('--reduction', help='target reduction for each zoom level', type=float, default=0.5)
    parser.add_argument('--base', help='base_x, base_y, base_z position of the layer', nargs=3,
                        type=float, default=[0, 0, 0])
    parser.add_argument('--scale', help='scale of the layer', type=int, default=1)
    parser.add_argument('--needs-cleaning', action='store_true',
                        help='whether the data needs cleaning for the first decimation')
    arguments = parser.parse_args()
    # arguments = Namespace(filename='../../data/data-surface.xdmf',
    #                       Data=['v3d'], idt=[160], oneDtMem=False, restart=[0],
    #                       outputs=["../../data/seis_cells.shp"],
    #                       epsg=3857, which=Which.CELL, base=[11.588271 * 100000, 47.751307 * 125000, 0], scale=10)
    # arguments = Namespace(filename='../../data/sumatra-surface.xdmf',
    #                       Data=['V'], idt=[50], oneDtMem=False, restart=[0],
    #                       outputs=['../../data/sumatra_cells.shp'],
    #                       epsg=32646, which=Which.CELL, base=[0, 0, 0], scale=1)
    xdmf_args_to_shp(arguments)
    # xdmf_to_shp(input_file='../../data/sumatra-surface.xdmf',
    #             data=['V'], idt=[50],
    #             output_files=['../../data/sumatra_cells.shp'],
    #             epsg=32646, which=Which.CELL)
    # reduction: seis - 0.025, sumatra - 0.2
