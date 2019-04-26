#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 07:56:58 2019

@author: phunh
"""

import ogr

def open_shapefile(file_path):
   """Opens the shapefile, gets the first layer and returns the ogr datasource"""
   datasource = ogr.Open(file_path)
   layer = datasource.GetLayerByIndex(0)
   print("Opening {}".format(file_path))
   print("Number of features: {}".format(layer.GetFeatureCount()))
   return datasource

def show_field_names(datasource, nth):
   """Prints field names of layer number 'nth' in 'datasource'
   """
   layer = datasource.GetLayerByIndex(nth)
   defn = layer.GetLayerDefn()
   names = []
   for index in range(defn.GetFieldCount()):
      names.append(defn.GetFieldDefn(index).GetName())
   print names