#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 21:33:58 2019

@author: phunh
"""
from __future__ import division
import os
from math import ceil
import mapnik
from colour import Color
from geo_functions import open_shapefile, show_field_names

cells_ds = open_shapefile("data/seis_cells.shp")
#show_field_names(cells_ds, 0)

cells_layer = cells_ds.GetLayerByIndex(0)
myData = []
cells_layer.ResetReading()
for cell_feature in cells_layer:
    myData.append(cell_feature.GetFieldAsDouble(0))

colorCount = 256
maxData = max(myData)
minData = min(myData)
rangeOneColor = (maxData - minData) / colorCount
stops = [minData+i*rangeOneColor for i in range(0, colorCount)]
colors = list(Color("blue").range_to(Color("red"), colorCount))

m = mapnik.Map(1300, 900) # Create a map with a given width and height in pixels
# Note: m.srs will default to '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
# The 'map.srs' is the target projection of the map and can be whatever you wish
# Output projection
#m.srs = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over'
# or shorter
m.srs = '+init=epsg:3857'
m.background = mapnik.Color('white') # Set background colour
# mapnik.load_map(m, 'text_sym.xml')

world_style = mapnik.Style()
world_rule = mapnik.Rule()
world_psym = mapnik.PolygonSymbolizer()
world_psym.fill = mapnik.Color('#c7e9b4')
world_rule.symbols.append(world_psym)
world_style.rules.append(world_rule)
m.append_style('World Style', world_style)

world_ds = mapnik.Shapefile(file='data/world_merc.shp')
print(world_ds.envelope())
world_layer = mapnik.Layer('world_layer')
world_layer.srs = '+init=epsg:3395'
world_layer.datasource = world_ds
world_layer.styles.append('World Style')
m.layers.append(world_layer)

s = mapnik.Style() # Style object to hold rules
'''
# To add outlines to a polygon we create a LineSymbolizer
line_symbolizer = mapnik.LineSymbolizer()
line_symbolizer.stroke = mapnik.Color('rgb(50%,50%,50%)')
line_symbolizer.stroke_width = 0.1
r.symbols.append(line_symbolizer) # Add the symbolizer to the rule object
'''
for i in range(0, colorCount-1):
    r = mapnik.Rule() # Rule object to hold symbolizers
    # To fill a polygon we create a PolygonSymbolizer
    psym = mapnik.PolygonSymbolizer()
    psym.fill_opacity = (i+1) / colorCount
    psym.fill = mapnik.Color(colors[i].web)
    r.symbols.append(psym) # Add the symbolizer to the rule object
    r.filter = mapnik.Expression("[Data] >= {} and [Data] < {}".format(stops[i], stops[i+1]))
    s.rules.append(r) # Add the rule to the style
    
i += 1
r = mapnik.Rule()
psym = mapnik.PolygonSymbolizer()
psym.fill_opacity = 1
psym.fill = mapnik.Color(colors[i].web)
r.symbols.append(psym)
r.filter = mapnik.Expression("[Data] >= {} and [Data] <= {}".format(stops[i], ceil(maxData)))
s.rules.append(r)

# It is possible to define styles in an xml file then get those styles in python
# text_s = m.find_style('style1')
# for ru in text_s.rules:
#     s.rules.append(ru)

m.append_style('data_style', s) # Styles are given names only as they are applied to the map

ds = mapnik.Shapefile(file='data/seis_cells.shp')
print(ds.envelope())
l = mapnik.Layer('data_layer')
# Note: layer.srs will default to '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
# Input projection
l.srs = '+init=epsg:3395'
l.datasource = ds
l.styles.append('data_style')
m.layers.append(l)

m.zoom_all()
mapnik.render_to_file(m, 'output-mapnik/tile-renderer.png')
os.system('xdg-open output-mapnik/tile-renderer.png')
