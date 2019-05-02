#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 09:38:22 2019

@author: phunh
"""
from argparse import Namespace, ArgumentParser
from osgeo import ogr, osr
from TuSeisSolScripts.displayh5vtk.UnstructuredData import UnstructuredData
from TuSeisSolScripts.displayh5vtk.DataLoader import ReadHdf5Posix


def xdmf_args_to_shp(args, output_files, which, base, scale):
    """Uses a argparse.Namespace object
    :param args: the argparse.Namespace object
    :param output_files: see to_shp
    :param which: see to_shp
    :param base: see to_shp
    :param scale: see to_shp
    """
    if ((which < 0 or which > 1) and len(output_files) < 2) or (which >=0 and which <= 1 and len(output_files) < 1):
        raise ValueError("Not enough names for output files")

    unstr = UnstructuredData()
    ReadHdf5Posix(args, unstr)
    myData = unstr.myData[args.idt].flatten()

    # Set up the shapefile driver
    shpDriver = ogr.GetDriverByName("ESRI Shapefile")
    # Create the spatial reference, WGS84
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(3395) # a PCS, so no lat-lon, only meter

    # For points - vertices
    if which != 1:
        # Create the data source
        pointDs = shpDriver.CreateDataSource(output_files[0])
        # Create the layer
        pointLayer = pointDs.CreateLayer("seis_vertices", srs, ogr.wkbPoint)
        # Add the fields we're interested in
        pointLayer.CreateField(ogr.FieldDefn("X", ogr.OFTReal))
        pointLayer.CreateField(ogr.FieldDefn("Y", ogr.OFTReal))

        # Process the unstructured data and add the attributes and features to the shapefile
        for vertex in unstr.xyz:
            coord = vertex * scale + base
            # Create the feature
            vFeature = ogr.Feature(pointLayer.GetLayerDefn())
            # Set the attributes using the values from the unstructured data
            vFeature.SetField("X", coord[0])
            vFeature.SetField("Y", coord[1])

            #this
#            # Create the WKT for the feature using Python string formatting
#            wkt = "POINT(%f %f)" % (coord[0], coord[1])
#            # Create the point from the Well Known Txt
#            point = ogr.CreateGeometryFromWkt(wkt)
            #or this
            point = ogr.Geometry(ogr.wkbPoint)
            point.AddPoint(coord[0], coord[1])

            # Set the feature geometry using the point
            vFeature.SetGeometry(point)
            # Create the feature in the layer (shapefile)
            pointLayer.CreateFeature(vFeature)
            # Dereference the feature
            vFeature = None

    # For triangles - cells
    if which != 0:
        cell_shp = output_files[0] if which == 1 else output_files[1]
        triangleDs = shpDriver.CreateDataSource(cell_shp)
        triangleLayer = triangleDs.CreateLayer("seis_cells", srs, ogr.wkbTriangle)
        triangleLayer.CreateField(ogr.FieldDefn("Data", ogr.OFTReal))

        for idx, cell in enumerate(unstr.connect):
            xyzA, xyzB, xyzC = unstr.xyz[cell[0]], unstr.xyz[cell[1]], unstr.xyz[cell[2]]
            coordA = xyzA * scale + base
            coordB = xyzB * scale + base
            coordC = xyzC * scale + base
            cFeature = ogr.Feature(triangleLayer.GetLayerDefn())
            cFeature.SetField("Data", myData[idx])

            #this
#            wkt = "TRIANGLE((%f %f, %f %f, %f %f, %f %f))" % (coordA[0], coordA[1], coordB[0], coordB[1], coordC[0], coordC[1], coordA[0], coordA[1])
#            triangle = ogr.CreateGeometryFromWkt(wkt)
            #or this
            # Create ring
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(coordA[0], coordA[1])
            ring.AddPoint(coordB[0], coordB[1])
            ring.AddPoint(coordC[0], coordC[1])
            ring.AddPoint(coordA[0], coordA[1])
            # Create triangle
            triangle = ogr.Geometry(ogr.wkbTriangle)
            triangle.AddGeometry(ring)

            cFeature.SetGeometry(triangle)
            triangleLayer.CreateFeature(cFeature)
            cFeature = None

    # Save and close the data source
    pointDs = None
    triangleDs = None

def xdmf_to_shp(input_file, data, idt, output_files, which = 2, base = (0, 0, 0), scale = 50):
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
    parser.add_argument('--Data', nargs=1, metavar=('variable'), default = (''), help='Data to visualize (example SRs)')
    parser.add_argument('--idt', nargs='+', help='list of time step to visualize (1st = 0); -1 = all', type=int)
    parser.add_argument('--oneDtMem', dest='oneDtMem', action='store_true', default = False, help='store only the dt to be displayed in RAM')
    parser.add_argument('--restart', nargs=1, metavar = ('idt'), help='in case of a restart at time frame idt, \
                        some postprocessing is necessary on Vr: Vr[n+idt] = Vr[n] + Vr[idt]', type=int, default = [0])
    #args = parser.parse_args()
    args = Namespace(Data=['v3d'], filename='data/data-surface.xdmf', idt=[160], oneDtMem=False, restart=[0])
    output_files = ["data/seis_cells.shp"]
    base = (11.588271 * 100000, 47.751307 * 125000, 0)
    scale = 10
    xdmf_args_to_shp(args, output_files, 1, base, scale)
