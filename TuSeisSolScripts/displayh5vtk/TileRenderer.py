#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 21:33:58 2019

@author: phunh
"""
from __future__ import division, print_function
import os
from argparse import ArgumentParser
import mapnik
from colour import Color
from GeoFunctions import open_shapefile, show_field_names


def make_colors(shapefile, color_count=256):
    cells_ds = open_shapefile(shapefile)
    # show_field_names(cells_ds, 0)

    cells_layer = cells_ds.GetLayerByIndex(0)
    my_data = []
    cells_layer.ResetReading()
    for cell_feature in cells_layer:
        my_data.append(cell_feature.GetFieldAsDouble(0))

    max_data = max(my_data)
    min_data = min(my_data)
    range_one_color = (max_data - min_data) / color_count
    print("color ranges:", max_data, min_data, range_one_color)
    stops = [min_data + i * range_one_color for i in range(0, color_count)]
    stops.append(max_data+1)
    colors = list(Color("blue").range_to(Color("red"), color_count))

    return stops, colors


def make_image(shapefile, output, epsg, color_count=256, show=True):
    stops, colors = make_colors(shapefile, color_count)

    m = mapnik.Map(1300, 900)  # Create a map with a given width and height in pixels
    # Note: m.srs will default to '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs' which is epsg:4326
    # The 'map.srs' is the target projection of the map and can be whatever you wish
    # Output projection
    # m.srs = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over'
    # or shorter
    m.srs = '+init=epsg:3857'
    m.background = mapnik.Color('white')  # Set background colour
    # mapnik.load_map(m, 'text_sym.xml')

    world_style = mapnik.Style()
    world_rule = mapnik.Rule()
    world_psym = mapnik.PolygonSymbolizer()
    world_psym.fill = mapnik.Color('#c7e9b4')
    world_rule.symbols.append(world_psym)
    world_style.rules.append(world_rule)
    m.append_style('World Style', world_style)

    world_ds = mapnik.Shapefile(file='../../data/world_merc.shp')
    print(world_ds.envelope())
    world_layer = mapnik.Layer('world_layer')
    world_layer.srs = '+init=epsg:3857'
    world_layer.datasource = world_ds
    world_layer.styles.append('World Style')
    m.layers.append(world_layer)

    s = mapnik.Style()  # Style object to hold rules
    '''
    # To add outlines to a polygon we create a LineSymbolizer
    line_symbolizer = mapnik.LineSymbolizer()
    line_symbolizer.stroke = mapnik.Color('rgb(50%,50%,50%)')
    line_symbolizer.stroke_width = 0.1
    r.symbols.append(line_symbolizer) # Add the symbolizer to the rule object
    '''
    for i in range(0, color_count):
        r = mapnik.Rule()  # Rule object to hold symbolizers
        # To fill a polygon we create a PolygonSymbolizer
        psym = mapnik.PolygonSymbolizer()
        psym.fill_opacity = (i+1) / color_count
        psym.fill = mapnik.Color(colors[i].web)
        r.symbols.append(psym)  # Add the symbolizer to the rule object
        r.filter = mapnik.Expression("[Data] >= {} and [Data] < {}".format(stops[i], stops[i+1]))
        s.rules.append(r)  # Add the rule to the style

    # It is possible to define styles in an xml file then get those styles in python
    # text_s = m.find_style('style1')
    # for ru in text_s.rules:
    #     s.rules.append(ru)

    m.append_style('data_style', s)  # Styles are given names only as they are applied to the map

    ds = mapnik.Shapefile(file=shapefile)
    print(ds.envelope())
    l_shp = mapnik.Layer('data_layer')
    # Note: layer.srs will default to '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
    # Input projection
    l_shp.srs = '+init=epsg:' + epsg
    l_shp.datasource = ds
    l_shp.styles.append('data_style')
    m.layers.append(l_shp)

    m.zoom_all()
    mapnik.render_to_file(m, output)
    if show:
        os.system('xdg-open ' + output)


if __name__ == '__main__':
    parser = ArgumentParser(description='Render a tile')
    parser.add_argument('shapefile', help='path of the shapefile')
    parser.add_argument('output', help='path of the output file')
    parser.add_argument('--epsg', nargs=1, metavar='number', default='3857', help='EPSG code of the shapefile')
    parser.add_argument('--colors', nargs=1, type=int, default=[256], help='Number of colors to use')
    # args = parser.parse_args()
    make_image(shapefile="../../data/sumatra_cells.shp",
               output='../../output-mapnik/sumatra-tile-renderer.png',
               epsg='32646',
               show=True)
