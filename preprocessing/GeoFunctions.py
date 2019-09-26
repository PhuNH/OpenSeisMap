#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 07:56:58 2019

@author: phunh
"""

import ogr


def open_shapefile(file_path):
    """Opens the shapefile, gets the first layer and returns the ogr datasource
    """
    datasource = ogr.Open(file_path)
    layer = datasource.GetLayerByIndex(0)
    print("Opening {} with {} features".format(file_path, layer.GetFeatureCount()))
    return datasource


def show_field_names(datasource, nth):
    """Prints field names of layer number 'nth' in 'datasource'
    """
    layer = datasource.GetLayerByIndex(nth)
    defn = layer.GetLayerDefn()
    names = []
    for index in range(defn.GetFieldCount()):
        names.append(defn.GetFieldDefn(index).GetName())
    print(names)


def get_shapefile_srs_from_ds(datasource):
    """Get the spatial reference object of the shapefile
    :param datasource: The shapefile datasource
    :return: The spatial reference object
    """
    layer = datasource.GetLayerByIndex(0)
    spatial_ref = layer.GetSpatialRef()
    return spatial_ref


def get_shapefile_srs(file_path):
    """Get the spatial reference object of the shapefile
    :param file_path: Path of the shapefile
    :return: The spatial reference object
    """
    ds = open_shapefile(file_path)
    srs = get_shapefile_srs_from_ds(ds)
    return srs
